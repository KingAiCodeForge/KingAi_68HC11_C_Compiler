#!/usr/bin/env python3
"""hc11kcos — relocatable object compiler/linker CLI for KCOS modules."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from hc11_compiler.codegen import TARGET_PROFILES
from hc11_compiler.linker import LinkError, link_objects
from hc11_compiler.objectfile import (
    ObjectFormatError,
    RelocatableObject,
    compile_kcos_module,
)
from hc11_compiler.resource_map import ResourceMap, ResourceMapError


def _module_name(path: str) -> str:
    return Path(path).stem.replace("-", "_").replace(".", "_")


def _load_resource_map(path: str | None, target: str) -> ResourceMap:
    if path is None:
        return ResourceMap.default_for_target(target)
    return ResourceMap.from_json(Path(path).read_text(encoding="utf-8"))


def _infer_image_format(path: str, explicit: str | None) -> str:
    if explicit:
        return explicit
    ext = Path(path).suffix.lower()
    return {
        ".bin": "bin",
        ".s19": "s19",
        ".srec": "s19",
        ".lst": "listing",
        ".asm": "asm",
        ".s": "asm",
    }.get(ext, "bin")


def _write_image(image, path: str, fmt: str):
    if fmt == "bin":
        Path(path).write_bytes(image.binary)
    elif fmt == "s19":
        Path(path).write_text(image.s19, encoding="utf-8")
    elif fmt == "listing":
        Path(path).write_text(image.listing, encoding="utf-8")
    elif fmt == "asm":
        Path(path).write_text(image.assembly, encoding="utf-8")
    else:
        raise ValueError(f"Unsupported image format: {fmt}")


def cmd_compile(args) -> int:
    source = Path(args.input).read_text(encoding="utf-8")
    module = args.module or _module_name(args.input)
    obj = compile_kcos_module(source, module_name=module, target=args.target)
    output = args.output or str(Path(args.input).with_suffix(".k11o"))
    obj.save(output)
    if args.verbose:
        print(
            f"[hc11kcos] {obj.module}: {len(obj.exports)} export(s), "
            f"{len(obj.imports)} import(s), {len(obj.resources)} resource request(s)",
            file=sys.stderr,
        )
        print(f"[hc11kcos] wrote {output}", file=sys.stderr)
    return 0


def cmd_link(args) -> int:
    objects = [RelocatableObject.load(path) for path in args.objects]
    target = objects[0].target if objects else args.target
    rmap = _load_resource_map(args.resource_map, target)
    image = link_objects(objects, resource_map=rmap)
    fmt = _infer_image_format(args.output, args.format)
    _write_image(image, args.output, fmt)

    if args.map_out:
        Path(args.map_out).write_text(
            image.resource_map.to_json() + "\n", encoding="utf-8"
        )

    if args.verbose:
        print(
            f"[hc11kcos] linked {len(objects)} object(s): "
            f"{image.size} bytes at 0x{image.base_addr:04X}",
            file=sys.stderr,
        )
        print(f"[hc11kcos] wrote {args.output} ({fmt})", file=sys.stderr)
    return 0


def cmd_build(args) -> int:
    objects = []
    seen_modules = set()
    for path in args.inputs:
        module = _module_name(path)
        if module in seen_modules:
            raise LinkError(
                f"Two source paths collapse to module name {module!r}; "
                "compile them separately with explicit --module names"
            )
        seen_modules.add(module)
        source = Path(path).read_text(encoding="utf-8")
        objects.append(
            compile_kcos_module(source, module_name=module, target=args.target)
        )

    rmap = _load_resource_map(args.resource_map, args.target)
    image = link_objects(objects, resource_map=rmap)
    fmt = _infer_image_format(args.output, args.format)
    _write_image(image, args.output, fmt)

    if args.objects_dir:
        outdir = Path(args.objects_dir)
        outdir.mkdir(parents=True, exist_ok=True)
        for obj in objects:
            obj.save(str(outdir / f"{obj.module}.k11o"))

    if args.map_out:
        Path(args.map_out).write_text(
            image.resource_map.to_json() + "\n", encoding="utf-8"
        )

    if args.verbose:
        print(
            f"[hc11kcos] built {len(objects)} module(s): "
            f"{image.size} bytes at 0x{image.base_addr:04X}",
            file=sys.stderr,
        )
    return 0


def cmd_map(args) -> int:
    rmap = ResourceMap.default_for_target(args.target)
    text = rmap.to_json() + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


def cmd_inspect(args) -> int:
    obj = RelocatableObject.load(args.object)
    data = {
        "module": obj.module,
        "target": obj.target,
        "abi": obj.abi,
        "source_sha256": obj.source_sha256,
        "exports": [x.to_dict() for x in obj.exports],
        "imports": [x.to_dict() for x in obj.imports],
        "resources": obj.resources,
    }
    print(json.dumps(data, indent=2, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hc11kcos",
        description="KCOS relocatable-object compiler and collision-checked HC11 linker",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    c = sub.add_parser("compile", help="compile one C file to a .k11o object")
    c.add_argument("input")
    c.add_argument("-o", "--output")
    c.add_argument("--module")
    c.add_argument("--target", choices=sorted(TARGET_PROFILES), default="generic")
    c.add_argument("-v", "--verbose", action="store_true")
    c.set_defaults(func=cmd_compile)

    l = sub.add_parser("link", help="link existing .k11o objects")
    l.add_argument("objects", nargs="+")
    l.add_argument("-o", "--output", required=True)
    l.add_argument("--format", choices=["bin", "s19", "listing", "asm"])
    l.add_argument("--resource-map")
    l.add_argument("--map-out")
    l.add_argument("--target", choices=sorted(TARGET_PROFILES), default="generic")
    l.add_argument("-v", "--verbose", action="store_true")
    l.set_defaults(func=cmd_link)

    b = sub.add_parser("build", help="compile and link multiple C translation units")
    b.add_argument("inputs", nargs="+")
    b.add_argument("-o", "--output", required=True)
    b.add_argument("--format", choices=["bin", "s19", "listing", "asm"])
    b.add_argument("--target", choices=sorted(TARGET_PROFILES), default="generic")
    b.add_argument("--resource-map")
    b.add_argument("--map-out")
    b.add_argument("--objects-dir")
    b.add_argument("-v", "--verbose", action="store_true")
    b.set_defaults(func=cmd_build)

    m = sub.add_parser("map", help="emit the default resource map for a target")
    m.add_argument("--target", choices=sorted(TARGET_PROFILES), default="generic")
    m.add_argument("-o", "--output")
    m.set_defaults(func=cmd_map)

    i = sub.add_parser("inspect", help="print link metadata from a .k11o object")
    i.add_argument("object")
    i.set_defaults(func=cmd_inspect)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except (OSError, ValueError, ObjectFormatError, ResourceMapError, LinkError) as exc:
        print(f"hc11kcos: error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
