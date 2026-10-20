"""Multi-object linker for K11O / KCOS HC11 modules."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence

from .assembler import Assembler, AssemblerError
from .objectfile import KCOS_ABI, ObjectSymbol, RelocatableObject, compile_object
from .resource_map import Allocation, ResourceMap, ResourceMapError


class LinkError(Exception):
    pass


@dataclass
class LinkedImage:
    target: str
    assembly: str
    binary: bytes
    base_addr: int
    s19: str
    listing: str
    symbols: Dict[str, int]
    resource_map: ResourceMap

    @property
    def size(self) -> int:
        return len(self.binary)


def _validate_objects(objects: Sequence[RelocatableObject]) -> str:
    if not objects:
        raise LinkError("No objects supplied")

    target = objects[0].target
    modules = set()
    exports: Dict[str, tuple] = {}

    for obj in objects:
        if obj.abi != KCOS_ABI:
            raise LinkError(
                f"{obj.module}: ABI {obj.abi!r} does not match {KCOS_ABI!r}"
            )
        if obj.target != target:
            raise LinkError(
                f"Target mismatch: {obj.module} is {obj.target}, expected {target}"
            )
        if obj.module in modules:
            raise LinkError(
                f"Duplicate module name {obj.module!r}; static symbol namespaces would collide"
            )
        modules.add(obj.module)

        if re.search(r"^\s*ORG\s+", obj.assembly, flags=re.MULTILINE | re.IGNORECASE):
            raise LinkError(
                f"{obj.module}: relocatable object contains an ORG directive"
            )

        for sym in obj.exports:
            previous = exports.get(sym.name)
            if previous is not None:
                prev_obj, prev_sym = previous
                raise LinkError(
                    f"Duplicate export {sym.name!r}: "
                    f"{prev_obj.module} ({prev_sym.kind}) and {obj.module} ({sym.kind})"
                )
            exports[sym.name] = (obj, sym)

    unresolved = []
    kind_errors = []
    for obj in objects:
        for imp in obj.imports:
            provider = exports.get(imp.name)
            if provider is None:
                unresolved.append(f"{obj.module}:{imp.name} ({imp.kind})")
                continue
            provider_obj, provider_sym = provider
            if provider_sym.kind != imp.kind:
                kind_errors.append(
                    f"{obj.module}:{imp.name} expects {imp.kind}, "
                    f"but {provider_obj.module} exports {provider_sym.kind}"
                )

    if unresolved:
        raise LinkError("Unresolved imports: " + ", ".join(sorted(unresolved)))
    if kind_errors:
        raise LinkError("Symbol kind mismatch: " + "; ".join(sorted(kind_errors)))

    return target


def _allocate_module_resources(objects: Sequence[RelocatableObject],
                               resource_map: ResourceMap) -> Dict[str, Allocation]:
    placements: Dict[str, Allocation] = {}
    for obj in objects:
        for req in obj.resources:
            placeholder = str(req["name"])
            if placeholder in placements:
                raise LinkError(f"Duplicate resource placeholder: {placeholder}")
            try:
                placement = resource_map.allocate(
                    str(req["kind"]),
                    int(req["size"]),
                    int(req.get("alignment", 1)),
                    placeholder,
                    module=obj.module,
                )
            except ResourceMapError as exc:
                raise LinkError(f"{obj.module}: {exc}") from exc
            placements[placeholder] = placement
    return placements


def _equate_block(placements: Dict[str, Allocation]) -> str:
    lines = [
        "; -- Linker-assigned RAM/ZP resources --",
    ]
    for name, alloc in sorted(placements.items(), key=lambda item: item[1].start):
        lines.append(
            f"{name}: EQU ${alloc.start:04X}    ; "
            f"{alloc.kind} {alloc.size} byte(s), {alloc.module}"
        )
    lines.append("")
    return "\n".join(lines)


def _object_block(objects: Sequence[RelocatableObject]) -> str:
    chunks: List[str] = []
    for obj in objects:
        chunks.append("")
        chunks.append(f"; ============================================")
        chunks.append(f"; K11O module: {obj.module}")
        chunks.append(f"; source sha256: {obj.source_sha256}")
        chunks.append(f"; ============================================")
        chunks.append(obj.assembly)
    return "\n".join(chunks)


def _assemble_at(origin: int, equates: str, object_body: str) -> tuple:
    source = (
        f"; KingAI HC11 linked image\n"
        f"        ORG     ${origin:04X}\n\n"
        f"{equates}\n"
        f"{object_body}\n"
    )
    assembler = Assembler()
    try:
        assembler.assemble(source)
    except AssemblerError as exc:
        raise LinkError(f"Assembly failed during link: {exc}") from exc
    return source, assembler


def link_objects(objects: Sequence[RelocatableObject], *,
                 resource_map: Optional[ResourceMap] = None) -> LinkedImage:
    """Resolve symbols/resources and place multiple relocatable objects."""
    objects = list(objects)
    target = _validate_objects(objects)
    rmap = (resource_map.clone() if resource_map is not None
            else ResourceMap.default_for_target(target))

    placements = _allocate_module_resources(objects, rmap)
    equates = _equate_block(placements)
    body = _object_block(objects)

    rom_regions = rmap.regions_for("rom")
    if not rom_regions:
        raise LinkError("Resource map has no ROM region")

    # First assembly is a sizing pass. Absolute code labels are all in ROM, so
    # relocating the same stream within ROM does not change instruction sizes.
    probe_origin = rom_regions[0].start
    _, probe = _assemble_at(probe_origin, equates, body)
    image_size = len(probe.binary)

    if image_size == 0:
        final_origin = probe_origin
    else:
        try:
            rom_alloc = rmap.allocate(
                "rom", image_size, 2, "__linked_code__", module="linker"
            )
        except ResourceMapError as exc:
            raise LinkError(str(exc)) from exc
        final_origin = rom_alloc.start

    final_asm, final = _assemble_at(final_origin, equates, body)

    # Relocation must not change the generated byte count. If it does, a direct
    # vs extended addressing decision became origin-dependent and needs a
    # dedicated relocation record rather than a silent size drift.
    if len(final.binary) != image_size:
        raise LinkError(
            f"Relocation changed image size from {image_size} to {len(final.binary)} bytes"
        )

    base_addr = final.base_addr if final.base_addr is not None else final_origin
    return LinkedImage(
        target=target,
        assembly=final_asm,
        binary=bytes(final.binary),
        base_addr=int(base_addr),
        s19=final.to_s19(),
        listing=final.get_listing(),
        symbols=dict(final.symbols),
        resource_map=rmap,
    )


def link_sources(sources: Dict[str, str], *, target: str = "generic",
                 resource_map: Optional[ResourceMap] = None) -> LinkedImage:
    """Compile several named C translation units then link them."""
    objects = [
        compile_object(source, module_name=name, target=target)
        for name, source in sources.items()
    ]
    return link_objects(objects, resource_map=resource_map)
