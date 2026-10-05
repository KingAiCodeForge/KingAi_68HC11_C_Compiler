"""Relocatable KCOS object format for the KingAI HC11 compiler."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field, fields
from typing import Dict, Iterable, List, Optional

from .ast_nodes import ASTNode, FuncCall, FuncDecl, Identifier, Program, VarDecl
from .assembler import Assembler, AssemblerError
from .codegen import CodeGenerator
from .lexer import Lexer
from .parser import Parser


OBJECT_MAGIC = "K11O"
OBJECT_VERSION = 1
KCOS_ABI = "kcos-hc11-v1"


class ObjectFormatError(Exception):
    pass


@dataclass(frozen=True)
class ObjectSymbol:
    name: str
    kind: str                  # function | data

    def to_dict(self) -> dict:
        return {"name": self.name, "kind": self.kind}

    @classmethod
    def from_dict(cls, data: dict) -> "ObjectSymbol":
        return cls(name=str(data["name"]), kind=str(data["kind"]))


@dataclass
class RelocatableObject:
    """Serializable relocatable HC11 module.

    Assembly remains symbolic. ROM origin and RAM/ZP placeholder EQU values are
    supplied by the linker, which lets the same object be placed in different
    target maps without recompiling C.
    """

    module: str
    target: str
    assembly: str
    source_sha256: str
    exports: List[ObjectSymbol] = field(default_factory=list)
    imports: List[ObjectSymbol] = field(default_factory=list)
    resources: List[dict] = field(default_factory=list)
    abi: str = KCOS_ABI

    def to_dict(self) -> dict:
        return {
            "magic": OBJECT_MAGIC,
            "version": OBJECT_VERSION,
            "abi": self.abi,
            "module": self.module,
            "target": self.target,
            "source_sha256": self.source_sha256,
            "exports": [x.to_dict() for x in self.exports],
            "imports": [x.to_dict() for x in self.imports],
            "resources": list(self.resources),
            "assembly": self.assembly,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "RelocatableObject":
        if data.get("magic") != OBJECT_MAGIC:
            raise ObjectFormatError("Not a K11O relocatable object")
        if int(data.get("version", 0)) != OBJECT_VERSION:
            raise ObjectFormatError(
                f"Unsupported K11O version: {data.get('version')}"
            )
        return cls(
            module=str(data["module"]),
            target=str(data["target"]),
            assembly=str(data["assembly"]),
            source_sha256=str(data["source_sha256"]),
            exports=[ObjectSymbol.from_dict(x) for x in data.get("exports", [])],
            imports=[ObjectSymbol.from_dict(x) for x in data.get("imports", [])],
            resources=[dict(x) for x in data.get("resources", [])],
            abi=str(data.get("abi", KCOS_ABI)),
        )

    def dumps(self, *, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True)

    @classmethod
    def loads(cls, text: str) -> "RelocatableObject":
        return cls.from_dict(json.loads(text))

    def save(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.dumps())
            f.write("\n")

    @classmethod
    def load(cls, path: str) -> "RelocatableObject":
        with open(path, "r", encoding="utf-8") as f:
            return cls.loads(f.read())


def _walk_ast(node):
    if isinstance(node, ASTNode):
        yield node
        for f in fields(node):
            value = getattr(node, f.name)
            if isinstance(value, ASTNode):
                yield from _walk_ast(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, ASTNode):
                        yield from _walk_ast(item)


def _append_symbol(table: Dict[str, ObjectSymbol], name: str, kind: str):
    previous = table.get(name)
    current = ObjectSymbol(name=name, kind=kind)
    if previous is not None and previous != current:
        raise ObjectFormatError(
            f"Symbol {name!r} is declared with conflicting kinds "
            f"({previous.kind} vs {kind})"
        )
    table[name] = current


def _collect_link_symbols(program: Program):
    function_defs = {
        d.name for d in program.declarations
        if isinstance(d, FuncDecl) and d.body is not None
    }
    static_prototypes = {
        d.name for d in program.declarations
        if isinstance(d, FuncDecl) and d.body is None and d.is_static
    }
    extern_data = {
        d.name for d in program.declarations
        if isinstance(d, VarDecl) and d.ctype.is_extern
    }

    exports: Dict[str, ObjectSymbol] = {}
    imports: Dict[str, ObjectSymbol] = {}
    seen_public_defs = set()

    for decl in program.declarations:
        if isinstance(decl, FuncDecl) and decl.body is not None and not decl.is_static:
            if decl.name in seen_public_defs:
                raise ObjectFormatError(f"Duplicate public definition: {decl.name!r}")
            seen_public_defs.add(decl.name)
            _append_symbol(exports, decl.name, "function")
        elif isinstance(decl, VarDecl) and not decl.ctype.is_extern and not decl.ctype.is_static:
            if decl.name in seen_public_defs:
                raise ObjectFormatError(f"Duplicate public definition: {decl.name!r}")
            seen_public_defs.add(decl.name)
            _append_symbol(exports, decl.name, "data")

    called_names = set()
    referenced_identifiers = set()
    for node in _walk_ast(program):
        if isinstance(node, FuncCall):
            called_names.add(node.name)
        elif isinstance(node, Identifier):
            referenced_identifiers.add(node.name)

    # Only references create imports. Merely including a prototype or extern
    # declaration from a shared header does not make the final link depend on it.
    for name in sorted(called_names):
        if name in function_defs:
            continue
        if name in static_prototypes:
            raise ObjectFormatError(
                f"Static function {name!r} is referenced but has no definition "
                "in this translation unit"
            )
        _append_symbol(imports, name, "function")

    for name in sorted(extern_data & referenced_identifiers):
        _append_symbol(imports, name, "data")

    for name in list(imports):
        if name in exports:
            del imports[name]

    return (
        sorted(exports.values(), key=lambda x: (x.name, x.kind)),
        sorted(imports.values(), key=lambda x: (x.name, x.kind)),
    )

def compile_object(source: str, *, module_name: str,
                   target: str = "generic") -> RelocatableObject:
    """Compile one C translation unit into a collision-checkable K11O object."""
    lexer = Lexer(source)
    parser = Parser(lexer.tokenize(), source)
    program = parser.parse()

    exports, imports = _collect_link_symbols(program)

    gen = CodeGenerator(
        target=target,
        relocatable=True,
        module_name=module_name,
    )
    assembly = gen.generate(program)

    # Vector placement has global ownership and must not silently enter a
    # relocatable module. A future vector-table linker can make this explicit.
    if gen._vector_lines:
        raise ObjectFormatError(
            "Relocatable interrupt-vector ownership is not supported yet; "
            "link ISR code as a normal function and bind vectors explicitly"
        )

    return RelocatableObject(
        module=gen.module_name,
        target=target,
        assembly=assembly,
        source_sha256=hashlib.sha256(source.encode("utf-8")).hexdigest(),
        exports=exports,
        imports=imports,
        resources=[dict(x) for x in gen.resource_requests],
    )


def _sanitize_module_name(module_name: str) -> str:
    return "".join(c if (c.isalnum() or c == "_") else "_" for c in module_name)


def _symbol_table(entries, default_kind: str = "function") -> Dict[str, str]:
    """Normalize iterable/dict symbol declarations to name -> kind."""
    if entries is None:
        return {}
    if isinstance(entries, dict):
        result = {str(k): str(v) for k, v in entries.items()}
    else:
        result = {}
        for item in entries:
            if isinstance(item, ObjectSymbol):
                result[item.name] = item.kind
            elif isinstance(item, str):
                if ":" in item:
                    name, kind = item.rsplit(":", 1)
                    result[name] = kind
                else:
                    result[item] = default_kind
            else:
                raise ObjectFormatError(
                    f"Unsupported symbol declaration: {item!r}"
                )
    for name, kind in result.items():
        if kind not in ("function", "data"):
            raise ObjectFormatError(
                f"{name}: symbol kind must be 'function' or 'data', got {kind!r}"
            )
    return result


def compile_asm_object(assembly: str, *, module_name: str,
                       target: str = "generic", exports=None, imports=None,
                       resources=None) -> RelocatableObject:
    """Wrap relocatable HC11 assembly in K11O with module-local label namespacing.

    A source ORG of zero is accepted as an object-relative declaration and
    removed. Any non-zero ORG is rejected because final placement belongs to
    the resource linker.
    """
    module = _sanitize_module_name(module_name)
    export_map = _symbol_table(exports)
    import_map = _symbol_table(imports)
    overlap = set(export_map) & set(import_map)
    if overlap:
        raise ObjectFormatError(
            "Symbols cannot be both imported and exported: "
            + ", ".join(sorted(overlap))
        )

    # Strip only object-relative ORG $0000 / ORG 0 declarations.
    kept_lines = []
    org_re = re.compile(r"^\s*ORG\s+([^;\s]+)", re.IGNORECASE)
    for lineno, line in enumerate(assembly.splitlines(), 1):
        code = line.split(";", 1)[0]
        match = org_re.match(code)
        if match:
            token = match.group(1)
            try:
                value = int(token[1:], 16) if token.startswith("$") else int(token, 0)
            except ValueError as exc:
                raise ObjectFormatError(
                    f"Line {lineno}: relocatable ORG must be a numeric zero"
                ) from exc
            if value != 0:
                raise ObjectFormatError(
                    f"Line {lineno}: absolute ORG {token} is not relocatable"
                )
            continue
        kept_lines.append(line)
    normalized = "\n".join(kept_lines).strip() + "\n"

    # Namespace every defined non-export label so ordinary names such as
    # 'done' or 'invalid' cannot collide between modules.
    label_re = re.compile(
        r"^(\s*)([A-Za-z_.$][A-Za-z0-9_.$]*):",
        re.MULTILINE,
    )
    defined = []
    for match in label_re.finditer(normalized):
        name = match.group(2)
        if name in defined:
            raise ObjectFormatError(f"Duplicate assembly label: {name}")
        defined.append(name)

    missing_exports = sorted(set(export_map) - set(defined))
    if missing_exports:
        raise ObjectFormatError(
            "Assembly exports are not defined: " + ", ".join(missing_exports)
        )

    rename = {
        name: f"__{module}_{name}"
        for name in defined
        if name not in export_map
    }
    if rename:
        symbol_token = re.compile(
            r"(?<![A-Za-z0-9_.$])("
            + "|".join(re.escape(x) for x in sorted(rename, key=len, reverse=True))
            + r")(?![A-Za-z0-9_.$])"
        )
        out_lines = []
        for line in normalized.splitlines():
            code, sep, comment = line.partition(";")
            code = symbol_token.sub(lambda m: rename[m.group(1)], code)
            out_lines.append(code + (sep + comment if sep else ""))
        normalized = "\n".join(out_lines) + "\n"

    # If the object is self-contained, run it through the built-in assembler
    # now. Imported symbols are intentionally left for the final link pass.
    if not import_map:
        probe = f"        ORG     $8000\n{normalized}"
        try:
            Assembler().assemble(probe)
        except AssemblerError as exc:
            raise ObjectFormatError(
                f"Assembly object does not assemble cleanly: {exc}"
            ) from exc

    return RelocatableObject(
        module=module,
        target=target,
        assembly=normalized,
        source_sha256=hashlib.sha256(assembly.encode("utf-8")).hexdigest(),
        exports=[
            ObjectSymbol(name=name, kind=kind)
            for name, kind in sorted(export_map.items())
        ],
        imports=[
            ObjectSymbol(name=name, kind=kind)
            for name, kind in sorted(import_map.items())
        ],
        resources=[dict(x) for x in (resources or [])],
    )


def compile_kcos_module(source: str, *, module_name: str,
                        target: str = "generic") -> RelocatableObject:
    """Compile a KCOS C translation unit supported by the HC11 C subset."""
    return compile_object(source, module_name=module_name, target=target)
