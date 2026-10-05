"""Relocatable KCOS object format for the KingAI HC11 compiler."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, fields
from typing import Dict, Iterable, List, Optional

from .ast_nodes import ASTNode, FuncCall, FuncDecl, Program, VarDecl
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

    exports: Dict[str, ObjectSymbol] = {}
    imports: Dict[str, ObjectSymbol] = {}

    for decl in program.declarations:
        if isinstance(decl, FuncDecl):
            if decl.body is not None:
                if not decl.is_static:
                    _append_symbol(exports, decl.name, "function")
            elif decl.name not in function_defs:
                _append_symbol(imports, decl.name, "function")
        elif isinstance(decl, VarDecl):
            if decl.ctype.is_extern:
                _append_symbol(imports, decl.name, "data")
            elif not decl.ctype.is_static:
                _append_symbol(exports, decl.name, "data")

    # A prototype is not required for a cross-module function call. Treat any
    # call without an in-module definition as an import and let the linker
    # prove that exactly one provider exists.
    for node in _walk_ast(program):
        if isinstance(node, FuncCall) and node.name not in function_defs:
            _append_symbol(imports, node.name, "function")

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


def compile_kcos_module(source: str, *, module_name: str,
                        target: str = "generic") -> RelocatableObject:
    """KCOS-named alias for compile_object()."""
    return compile_object(source, module_name=module_name, target=target)
