#!/usr/bin/env python3
"""
hc11kit — Unified 68HC11 ECU Toolkit
=====================================

One CLI for everything:
    hc11kit asm      — Assemble HC11 ASM to binary/S19
    hc11kit disasm   — Disassemble binary regions
    hc11kit compile  — Compile C to ASM/binary/S19
    hc11kit patch    — Inject code into existing binary
    hc11kit free     — Find free space in binary
    hc11kit checksum — Verify/fix GM ROM checksum
    hc11kit addr     — Convert between file offset / CPU address / bank
    hc11kit xdf      — Parse and query XDF definition files
    hc11kit info     — Binary summary and identification

Usage:
    python hc11kit.py <command> [options]
    python hc11kit.py --help
    python hc11kit.py <command> --help

Examples:
    python hc11kit.py asm spark_cut.asm -o spark_cut.bin
    python hc11kit.py disasm ECU.bin --range 0x8000-0x8040
    python hc11kit.py compile main.c -o main.s19 --target vy_v6
    python hc11kit.py patch ECU.bin code.bin --at 0x5D05 --hook 0x101E1:3
    python hc11kit.py free ECU.bin --min-size 64
    python hc11kit.py checksum ECU.bin --fix
    python hc11kit.py addr 0x101E1 --format vy_v6_128k
    python hc11kit.py xdf defs.xdf --list
    python hc11kit.py info ECU.bin
"""

import argparse
import sys
import os

VY_V6_ROM_SIZE = 0x20000

from hc11_compiler import __version__
from hc11_compiler.cli import validate_command_outputs, write_command_output


def main():
    parser = argparse.ArgumentParser(
        prog="hc11kit",
        description="HC11 ECU Toolkit — assemble, disassemble, compile, patch, analyze",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""commands:
  asm        Assemble HC11 source to binary or S19
  disasm     Disassemble binary range to HC11 mnemonics
  compile    Compile C source to ASM/binary/S19
  patch      Inject compiled code into existing ROM binary
  free       Find free (unused) regions in a binary
  checksum   Verify or fix GM ROM checksum
  addr       Convert between file offset, CPU address, and bank
  xdf        Parse and query TunerPro XDF files
  info       Identify and summarize a binary file
""",
    )
    parser.add_argument("--version", action="version", version=f"hc11kit {__version__}")
    sub = parser.add_subparsers(dest="command", metavar="command")

    # ── asm ──────────────────────────────────────────────────────────────
    p_asm = sub.add_parser("asm", help="Assemble HC11 source to binary or S19")
    p_asm.add_argument("input", help="Input .asm file")
    p_asm.add_argument("-o", "--output", help="Output file (.bin, .s19, or .lst)")
    p_asm.add_argument("--org", help="Override ORG address (hex)", default=None)
    p_asm.add_argument("--listing", action="store_true", help="Print listing to stdout")

    # ── disasm ───────────────────────────────────────────────────────────
    p_dis = sub.add_parser("disasm", help="Disassemble binary range")
    p_dis.add_argument("input", help="Input .bin file")
    p_dis.add_argument("--range", help="Address range START-END (hex), e.g. 0x8000-0x8040")
    p_dis.add_argument("--offset", help="File offset range (hex), e.g. 0x18000-0x18040")
    p_dis.add_argument("--format", choices=["vy_v6_128k", "flat_64k", "flat_32k"],
                        default="vy_v6_128k", help="Binary layout format")
    p_dis.add_argument("-o", "--output", help="Output file (default: stdout)")
    p_dis.add_argument("--bank", choices=["1", "2", "3", "common"], default=None,
                        help="Bank context for address resolution")

    # ── compile ──────────────────────────────────────────────────────────
    p_cc = sub.add_parser("compile", help="Compile C source to ASM/binary/S19")
    p_cc.add_argument("input", help="Input .c file")
    p_cc.add_argument("-o", "--output", help="Output file (.asm, .s19, .bin, .lst)")
    p_cc.add_argument("--target", default="vy_v6",
                       choices=["generic", "vy_v6", "1227730", "16197427"],
                       help="Target PCM profile (default: vy_v6)")
    p_cc.add_argument("--org", help="Code origin address (hex)")
    p_cc.add_argument("--stack", help="Initial stack pointer (hex)")
    p_cc.add_argument("-v", "--verbose", action="store_true")

    # ── patch ────────────────────────────────────────────────────────────
    p_pat = sub.add_parser("patch", help="Inject code into existing binary")
    p_pat.add_argument("binary", help="Base binary file to patch")
    p_pat.add_argument("code", help="Code to inject (.bin, .asm, .c, or .s19)")
    p_pat.add_argument("--at", required=True,
                        help="File offset to inject code (hex)")
    p_pat.add_argument("--hook", default=None,
                        help="Hook point OFFSET:SIZE, e.g. 0x101E1:3 — replaces SIZE "
                             "bytes at OFFSET with JSR to injected code")
    p_pat.add_argument("--expect-sha256", help="Required exact input hash for VY research images")
    p_pat.add_argument("--expect-hook-bytes", help="Expected original hook bytes; required for VY hooks")
    p_pat.add_argument("--allow-banked-target", action="store_true", help="Unqualified research override for banked placement")
    p_pat.add_argument("--allow-nonfree", action="store_true", help="Unqualified research override for occupied/mixed fill")
    p_pat.add_argument("--force-generic-checksum", action="store_true", help="Unqualified generic checksum override for VY")
    p_pat.add_argument("--overwrite", dest="force", action="store_true", help="Alias of --force (preserved local variant CLI)")
    p_pat.add_argument("-o", "--output", help="Output patched binary (default: input_patched.bin)")
    p_pat.add_argument("--target", default="vy_v6",
                        choices=["generic", "vy_v6", "1227730", "16197427"])
    p_pat.add_argument("--no-checksum", action="store_true",
                        help="Skip checksum recalculation after patching")
    p_pat.add_argument("--verify", action="store_true",
                        help="Read back and disassemble injected code to verify")
    p_pat.add_argument("--dry-run", action="store_true",
                        help="Show what would be patched without writing")

    # ── free ─────────────────────────────────────────────────────────────
    p_free = sub.add_parser("free", help="Find free (unused) regions in binary")
    p_free.add_argument("input", help="Input .bin file")
    p_free.add_argument("--min-size", type=int, default=16,
                         help="Minimum free region size in bytes (default: 16)")
    p_free.add_argument("--fill", type=lambda x: int(x, 0), default=None,
                         help="Fill byte to search for (default: auto-detect 0x00 and 0xFF)")
    p_free.add_argument("--format", choices=["vy_v6_128k", "flat_64k", "flat_32k"],
                         default="vy_v6_128k")

    # ── checksum ─────────────────────────────────────────────────────────
    p_cks = sub.add_parser("checksum", help="Verify or fix GM ROM checksum")
    p_cks.add_argument("input", help="Input .bin file")
    p_cks.add_argument("--fix", action="store_true",
                        help="Recalculate and write correct checksum")
    p_cks.add_argument("--chk-offset", type=lambda x: int(x, 0), default=6,
                        help="Offset of stored checksum (default: 6)")
    p_cks.add_argument("--sum-offset", type=lambda x: int(x, 0), default=8,
                        help="Offset where summation begins (default: 8)")
    p_cks.add_argument("-o", "--output", help="Output file (default: input_checksum.bin when --fix)")

    # ── addr ─────────────────────────────────────────────────────────────
    p_addr = sub.add_parser("addr", help="Convert between file offset, CPU address, and bank")
    p_addr.add_argument("address", help="Address to convert (hex)")
    p_addr.add_argument("--from", dest="from_type", choices=["file", "cpu"],
                         default="file", help="Input address type")
    p_addr.add_argument("--format", choices=["vy_v6_128k", "flat_64k", "flat_32k"],
                         default="vy_v6_128k")
    p_addr.add_argument("--bank", choices=["1", "2", "3", "common"], default=None,
                         help="Bank context for CPU→file conversion")

    # ── xdf ──────────────────────────────────────────────────────────────
    p_xdf = sub.add_parser("xdf", help="Parse and query TunerPro XDF files")
    p_xdf.add_argument("input", help="Input .xdf file")
    p_xdf.add_argument("--list", action="store_true", help="List all definitions")
    p_xdf.add_argument("--search", help="Search definitions by name")
    p_xdf.add_argument("--addr", help="Look up definition at address (hex)")
    p_xdf.add_argument("--category", help="Filter by category")

    # ── info ─────────────────────────────────────────────────────────────
    p_info = sub.add_parser("info", help="Identify and summarize a binary file")
    p_info.add_argument("input", help="Input .bin file")
    for child in (p_asm, p_dis, p_cc, p_pat, p_cks):
        child.add_argument("--force", action="store_true", help="Replace an existing output; source inputs remain protected")

    # ── Parse and dispatch ───────────────────────────────────────────────
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Import and dispatch to subcommand
    try:
        validate_command_outputs(args)
        handler = COMMANDS[args.command]
        return handler(args)
    except KeyError:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


# ═════════════════════════════════════════════════════════════════════════════
# COMMAND IMPLEMENTATIONS
# ═════════════════════════════════════════════════════════════════════════════

def _parse_hex(s):
    """Parse hex string with optional 0x or $ prefix."""
    if s is None:
        return None
    s = s.strip()
    if s.startswith("0x") or s.startswith("0X"):
        return int(s, 16)
    if s.startswith("$"):
        return int(s[1:], 16)
    return int(s, 16)


# ── asm ──────────────────────────────────────────────────────────────────
def cmd_asm(args):
    from hc11_compiler.assembler import Assembler, AssemblerError

    with open(args.input, "r", encoding="utf-8") as f:
        source = f.read()
    if args.org is not None:
        import re
        origin = _parse_hex(args.org)
        if not 0 <= origin <= 0xFFFF:
            raise ValueError("ORG must be in 0..0xFFFF")
        source, count = re.subn(r"(?im)^\s*ORG\s+[^;\r\n]+", f"        ORG ${origin:04X}", source, count=1)
        if not count:
            source = f"        ORG ${origin:04X}\n" + source

    asm = Assembler()
    try:
        asm.assemble(source)
    except AssemblerError as e:
        print(f"Assembly error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.listing or (not args.output):
        print(asm.get_listing())
        return

    out = args.output
    ext = os.path.splitext(out)[1].lower()
    if ext == ".s19":
        write_command_output(args, out, asm.to_s19())
    elif ext == ".lst":
        write_command_output(args, out, asm.get_listing())
    else:  # .bin or anything else
        write_command_output(args, out, bytes(asm.binary))
    print(f"Assembled {len(asm.binary)} bytes -> {out}")


# ── disasm ───────────────────────────────────────────────────────────────
def cmd_disasm(args):
    with open(args.input, "rb") as f:
        data = f.read()

    start_off, end_off = 0, len(data)
    cpu_base = 0

    if args.range:
        parts = args.range.replace("-", " ").split()
        cpu_start = _parse_hex(parts[0])
        cpu_end = _parse_hex(parts[1]) if len(parts) > 1 else cpu_start + 64
        # Convert CPU to file offset based on format
        if args.format == "vy_v6_128k":
            if cpu_start >= 0x8000 and args.bank is None:
                raise ValueError("Banked CPU ranges require an explicit --bank")
            start_off, end_off, cpu_base = _cpu_to_file_range_vy(cpu_start, cpu_end, args.bank)
        else:
            base = 0x8000 if args.format == "flat_32k" else 0
            start_off, end_off = cpu_start - base, cpu_end - base
            cpu_base = cpu_start
    elif args.offset:
        parts = args.offset.replace("-", " ").split()
        start_off = _parse_hex(parts[0])
        end_off = _parse_hex(parts[1]) if len(parts) > 1 else start_off + 64
        if args.format == "vy_v6_128k":
            cpu_base = _file_to_cpu_vy(start_off)
        else:
            cpu_base = start_off + (0x8000 if args.format == "flat_32k" else 0)

    if args.range and args.offset:
        raise ValueError("Choose --range or --offset, not both")
    if args.format == "vy_v6_128k":
        if len(data) != VY_V6_ROM_SIZE:
            raise ValueError("VY layout requires exactly 128KB; choose a flat layout for other inputs")
        if not args.range and not args.offset:
            raise ValueError("VY disassembly requires an explicit range/offset within one memory window")
        if end_off > start_off and _file_to_bank_vy(start_off) != _file_to_bank_vy(end_off - 1):
            raise ValueError("Disassembly range crosses a VY memory-window boundary")

    if not 0 <= start_off <= end_off <= len(data):
        raise ValueError("Disassembly range must be within the input file")
    chunk = data[start_off:end_off]
    lines = _disassemble_bytes(chunk, cpu_base)

    output = "\n".join(lines)
    if args.output:
        write_command_output(args, args.output, output + "\n")
        print(f"Disassembled {len(chunk)} bytes -> {args.output}")
    else:
        print(output)


# ── compile ──────────────────────────────────────────────────────────────
def cmd_compile(args):
    from hc11_compiler import compile_source
    from hc11_compiler.codegen import TARGET_PROFILES

    with open(args.input, "r", encoding="utf-8") as f:
        source = f.read()

    profile = TARGET_PROFILES.get(args.target, TARGET_PROFILES["generic"])
    org = _parse_hex(args.org) if args.org else profile["org"]
    stack = _parse_hex(args.stack) if args.stack else profile["stack"]

    # Determine output format from extension
    out_format = "asm"
    if args.output:
        ext = os.path.splitext(args.output)[1].lower()
        if ext == ".s19":
            out_format = "s19"
        elif ext == ".bin":
            out_format = "binary"
        elif ext == ".lst":
            out_format = "listing"

    if args.verbose:
        print(f"[compile] {args.input} -> {args.output or 'stdout'}", file=sys.stderr)
        print(f"[compile] target={args.target} org=${org:04X} stack=${stack:04X}", file=sys.stderr)

    result = compile_source(source, org=org, stack=stack,
                            target=args.target, output=out_format)

    if args.output:
        write_command_output(args, args.output, result)
        size = len(result) if isinstance(result, (bytes, bytearray)) else len(result.encode())
        print(f"Compiled {args.input} -> {args.output} ({size} bytes)")
    else:
        if isinstance(result, (bytes, bytearray)):
            sys.stdout.buffer.write(result)
        else:
            print(result)


# ── patch ────────────────────────────────────────────────────────────────
def cmd_patch(args):
    import hashlib

    if args.no_checksum and args.force_generic_checksum:
        raise ValueError("Choose --no-checksum or --force-generic-checksum, not both")

    inject_offset = _parse_hex(args.at)

    # Load base binary
    with open(args.binary, "rb") as f:
        rom = bytearray(f.read())
    rom_size = len(rom)
    print(f"Base binary: {args.binary} ({rom_size} bytes)")

    input_digest = hashlib.sha256(rom).hexdigest()
    print(f"Input SHA256: {input_digest}")

    if inject_offset < 0 or inject_offset >= rom_size:
        raise ValueError(f"Injection offset 0x{inject_offset:X} is outside the binary")

    expected_digest = _normalize_sha256(args.expect_sha256) if args.expect_sha256 else None
    if args.target == "vy_v6":
        if rom_size != VY_V6_ROM_SIZE:
            raise ValueError(
                f"VY target requires a 128KB binary ({VY_V6_ROM_SIZE} bytes), got {rom_size}"
            )
        if expected_digest is None:
            raise ValueError(
                "--expect-sha256 is required for VY patching; each OSID/enhanced variant can differ"
            )
        inject_bank = _file_to_bank_vy(inject_offset)
        if inject_bank != "common" and not args.allow_banked_target:
            raise ValueError(
                f"VY injection offset 0x{inject_offset:05X} resolves to {inject_bank}. "
                "A JSR does not prove the runtime overlay; use common ROM or the explicit "
                "--allow-banked-target research override"
            )

    if expected_digest is not None and input_digest != expected_digest:
        raise ValueError(
            f"Input SHA256 mismatch: expected {expected_digest}, got {input_digest}"
        )
    if expected_digest is not None:
        print("Input SHA256 matches expected variant")

    hook_off = None
    hook_size = None
    original_hook = None
    hook_data = None
    if args.hook:
        hook_off, hook_size = _parse_hook(args.hook)
        if hook_size < 3:
            raise ValueError(f"Hook size {hook_size} is too small for JSR (need at least 3)")
        if hook_off < 0 or hook_off + hook_size > rom_size:
            raise ValueError(
                f"Hook range 0x{hook_off:05X}-0x{hook_off + hook_size - 1:05X} "
                "is outside the binary"
            )
        original_hook = bytes(rom[hook_off:hook_off + hook_size])

        if args.target == "vy_v6" and not args.expect_hook_bytes:
            raise ValueError(
                "--expect-hook-bytes is required for a VY hook; matching size or address is not enough"
            )
        if args.expect_hook_bytes:
            expected_hook = _parse_expected_bytes(args.expect_hook_bytes)
            if len(expected_hook) != hook_size:
                raise ValueError(
                    f"Expected hook byte count ({len(expected_hook)}) does not match hook size ({hook_size})"
                )
            if original_hook != expected_hook:
                raise ValueError(
                    f"Hook bytes mismatch at 0x{hook_off:05X}: expected "
                    f"{expected_hook.hex().upper()}, got {original_hook.hex().upper()}"
                )
            print(f"Hook bytes match at 0x{hook_off:05X}: {original_hook.hex().upper()}")
    elif args.expect_hook_bytes:
        raise ValueError("--expect-hook-bytes requires --hook")

    # Determine code source format and get bytes
    code_path = args.code
    ext = os.path.splitext(code_path)[1].lower()

    if ext == ".c":
        # Compile C to binary first
        from hc11_compiler import compile_source
        from hc11_compiler.codegen import TARGET_PROFILES
        with open(code_path, "r", encoding="utf-8") as f:
            source = f.read()
        profile = TARGET_PROFILES.get(args.target, TARGET_PROFILES["generic"])
        cpu_addr = _file_to_cpu_vy(inject_offset) if args.target == "vy_v6" else inject_offset
        code_bytes = compile_source(source, org=cpu_addr, stack=profile["stack"],
                                    target=args.target, output="binary")
        print(f"Compiled {code_path} -> {len(code_bytes)} bytes at ORG ${cpu_addr:04X}")

    elif ext == ".asm" or ext == ".s":
        # Assemble
        from hc11_compiler.assembler import Assembler
        with open(code_path, "r", encoding="utf-8") as f:
            asm_source = f.read()
        assembler = Assembler()
        assembler.assemble(asm_source)
        cpu_origin = _file_to_cpu_vy(inject_offset) if args.target == "vy_v6" else inject_offset
        if assembler.base_addr != cpu_origin:
            raise ValueError("Assembly origin does not match injection CPU address")
        code_bytes = bytes(assembler.binary)
        print(f"Assembled {code_path} -> {len(code_bytes)} bytes")

    elif ext == ".s19":
        code_bytes = _s19_to_bytes(code_path, expected_origin=_file_to_cpu_vy(inject_offset) if args.target == "vy_v6" else inject_offset)
        print(f"Loaded S19 {code_path} -> {len(code_bytes)} bytes")

    else:  # .bin or raw
        with open(code_path, "rb") as f:
            code_bytes = f.read()
        print(f"Loaded raw {code_path} -> {len(code_bytes)} bytes")

    if not code_bytes:
        raise ValueError("Code input is empty")

    # Validate injection fits
    if inject_offset + len(code_bytes) > rom_size:
        raise ValueError(
            f"Code ({len(code_bytes)} bytes) does not fit at 0x{inject_offset:05X} "
            f"(binary ends at 0x{rom_size:05X})"
        )

    if args.target == "vy_v6":
        start_bank = _file_to_bank_vy(inject_offset)
        end_bank = _file_to_bank_vy(inject_offset + len(code_bytes) - 1)
        if start_bank != end_bank:
            raise ValueError("Injection crosses a VY memory-window boundary")

    if hook_off is not None:
        inject_end = inject_offset + len(code_bytes)
        hook_end = hook_off + hook_size
        if inject_offset < hook_end and hook_off < inject_end:
            raise ValueError("Injection range overlaps the hook range")

    # Check target region is free space
    target_region = rom[inject_offset:inject_offset + len(code_bytes)]
    uniform_free = bool(target_region) and target_region[0] in (0x00, 0xFF)
    uniform_free = uniform_free and all(byte == target_region[0] for byte in target_region)
    if not uniform_free and not args.allow_nonfree:
        sample = bytes(target_region[:16]).hex().upper()
        raise ValueError(
            f"Target region 0x{inject_offset:05X}-0x{inject_offset + len(code_bytes) - 1:05X} "
            f"is not uniform 00/FF fill (first bytes: {sample}); use --allow-nonfree only "
            "for reviewed local research"
        )
    if uniform_free:
        print(
            f"Target region is uniform {target_region[0]:02X} fill: "
            f"0x{inject_offset:05X}-0x{inject_offset + len(code_bytes) - 1:05X}"
        )
    else:
        print("WARNING: --allow-nonfree permits overwriting occupied or mixed-fill bytes")

    cpu_target = _file_to_cpu_vy(inject_offset) if args.target == "vy_v6" else inject_offset
    if cpu_target < 0 or cpu_target > 0xFFFF:
        raise ValueError(f"JSR target 0x{cpu_target:X} is outside the HC11 16-bit address space")

    if hook_off is not None:
        jsr_bytes = bytes([0xBD, (cpu_target >> 8) & 0xFF, cpu_target & 0xFF])
        hook_data = jsr_bytes + bytes([0x01] * (hook_size - 3))

    if args.dry_run:
        print(f"\n[DRY RUN] Would inject {len(code_bytes)} bytes at file 0x{inject_offset:05X}")
        if hook_off is not None:
            print(f"[DRY RUN] Would write hook at file 0x{hook_off:05X} ({hook_size} bytes)")
        if args.target == "vy_v6" and not args.force_generic_checksum:
            print("[DRY RUN] VY checksum would be left unchanged (generic algorithm is unverified)")
        print("[DRY RUN] No files modified.")
        return

    out_path = args.output or _patched_name(args.binary)
    input_abs = os.path.abspath(args.binary)
    output_abs = os.path.abspath(out_path)
    if os.path.normcase(input_abs) == os.path.normcase(output_abs):
        raise ValueError("Output path must not be the input binary")
    if os.path.exists(out_path) and not args.force:
        raise ValueError(f"Output already exists: {out_path}; use --force to replace it")

    # Write code into ROM
    rom[inject_offset:inject_offset + len(code_bytes)] = code_bytes
    print(f"Injected {len(code_bytes)} bytes at file offset 0x{inject_offset:05X}")

    # Install hook if requested
    if hook_off is not None:
        rom[hook_off:hook_off + hook_size] = hook_data

        print(f"Hook at 0x{hook_off:05X}: {original_hook.hex().upper()} -> {hook_data.hex().upper()}"
              f" (JSR ${cpu_target:04X})")

    # The generic checksum implementation is not validated for VY $060A images.
    if args.no_checksum:
        print("Checksum skipped by --no-checksum")
    elif args.target == "vy_v6" and not args.force_generic_checksum:
        print("Checksum left unchanged: generic GM16 checksum is not validated for VY $060A")
    else:
        if args.target == "vy_v6":
            print("WARNING: forcing the unverified generic checksum algorithm for VY")
        _fix_checksum_inplace(rom)

    # Write output
    write_command_output(args, out_path, rom)
    print(f"Patched binary written to {out_path}")

    with open(out_path, "rb") as f:
        written = f.read()
    if written != bytes(rom):
        raise RuntimeError("Readback verification failed for complete output image")
    if written[inject_offset:inject_offset + len(code_bytes)] != code_bytes:
        raise RuntimeError("Readback verification failed for injected code")
    if hook_off is not None and written[hook_off:hook_off + hook_size] != hook_data:
        raise RuntimeError("Readback verification failed for hook bytes")
    print(f"Output SHA256: {hashlib.sha256(written).hexdigest()}")

    # Verify readback
    if args.verify:
        print(f"\nVerification disassembly at 0x{inject_offset:05X}:")
        cpu_base = _file_to_cpu_vy(inject_offset) if args.target == "vy_v6" else inject_offset
        lines = _disassemble_bytes(code_bytes, cpu_base)
        for line in lines:
            print(f"  {line}")


# ── free ─────────────────────────────────────────────────────────────────
def cmd_free(args):
    if args.min_size <= 0 or (args.fill is not None and not 0 <= args.fill <= 255):
        raise ValueError("Minimum size must be positive and fill must be a byte (0..255)")
    with open(args.input, "rb") as f:
        data = f.read()

    fill_bytes = [args.fill] if args.fill is not None else [0x00, 0xFF]
    min_size = args.min_size
    regions = []

    i = 0
    while i < len(data):
        if data[i] in fill_bytes:
            start = i
            fill_val = data[i]
            while i < len(data) and data[i] == fill_val:
                i += 1
            length = i - start
            if length >= min_size:
                if args.format == "vy_v6_128k":
                    cpu = _file_to_cpu_vy(start)
                    bank = _file_to_bank_vy(start)
                else:
                    cpu = start
                    bank = "flat"
                regions.append({
                    "file_start": start,
                    "file_end": i - 1,
                    "cpu_addr": cpu,
                    "bank": bank,
                    "size": length,
                    "fill": fill_val,
                })
        else:
            i += 1

    # Sort by size descending
    regions.sort(key=lambda r: r["size"], reverse=True)

    print(f"Free space in {args.input} ({len(data)} bytes, minimum {min_size} bytes):\n")
    print(f"{'File Offset':>14s}  {'CPU Addr':>10s}  {'Bank':>6s}  {'Size':>7s}  {'Fill':>4s}")
    print(f"{'─'*14}  {'─'*10}  {'─'*6}  {'─'*7}  {'─'*4}")

    total = 0
    for r in regions:
        print(f"  0x{r['file_start']:05X}-0x{r['file_end']:05X}"
              f"  ${r['cpu_addr']:04X}"
              f"  {r['bank']:>6s}"
              f"  {r['size']:>5d} B"
              f"  0x{r['fill']:02X}")
        total += r["size"]

    print(f"\n{len(regions)} regions, {total:,} bytes total free")


# ── checksum ─────────────────────────────────────────────────────────────
def cmd_checksum(args):
    with open(args.input, "rb") as f:
        data = bytearray(f.read())

    stored = _read_checksum(data, args.chk_offset)
    calculated = _calc_checksum(data, args.sum_offset)

    print(f"File:       {args.input} ({len(data)} bytes)")
    print(f"Stored:     0x{stored:04X} (at offset {args.chk_offset})")
    print(f"Calculated: 0x{calculated:04X} (sum from offset {args.sum_offset})")

    if stored == calculated:
        print("Status:     VALID")
    else:
        print("Status:     MISMATCH")
        if args.fix:
            import struct
            struct.pack_into(">H", data, args.chk_offset, calculated)
            out_path = args.output or args.input
            write_command_output(args, out_path, data)
            print(f"Fixed:      Wrote 0x{calculated:04X} to {out_path}")
        else:
            print("Use --fix to correct the checksum")


# ── addr ─────────────────────────────────────────────────────────────────
def cmd_addr(args):
    addr = _parse_hex(args.address)
    limit = (0x20000 if args.format == "vy_v6_128k" else 0x8000 if args.format == "flat_32k" else 0x10000) if args.from_type == "file" else 0x10000
    if not 0 <= addr < limit:
        raise ValueError("Address is outside the selected layout")

    if args.format == "vy_v6_128k":
        if args.from_type == "file":
            cpu = _file_to_cpu_vy(addr)
            bank = _file_to_bank_vy(addr)
            print(f"File offset:  0x{addr:05X}")
            print(f"CPU address:  ${cpu:04X}")
            print(f"Bank:         {bank}")
            # Show all possible banks if in banked region
            if 0x8000 <= cpu <= 0xFFFF:
                print(f"  Bank 1 file: 0x{0x08000 + (cpu - 0x8000):05X}")
                print(f"  Bank 2 file: 0x{0x10000 + (cpu - 0x8000):05X}")
                print(f"  Bank 3 file: 0x{0x18000 + (cpu - 0x8000):05X}")
        else:  # cpu
            if addr >= 0x8000 and (args.bank is None or args.bank == "common"):
                raise ValueError("Banked CPU addresses require --bank 1, 2, or 3")
            bank = args.bank or "common"
            file_off = _cpu_to_file_vy(addr, bank)
            print(f"CPU address:  ${addr:04X}")
            print(f"Bank:         {bank}")
            print(f"File offset:  0x{file_off:05X}")
            if 0x8000 <= addr <= 0xFFFF:
                print(f"  Bank 1 file: 0x{0x08000 + (addr - 0x8000):05X}")
                print(f"  Bank 2 file: 0x{0x10000 + (addr - 0x8000):05X}")
                print(f"  Bank 3 file: 0x{0x18000 + (addr - 0x8000):05X}")
    elif args.format == "flat_32k":
        if args.from_type == "cpu" and addr < 0x8000:
            raise ValueError("32KB layout CPU addresses begin at 0x8000")
        converted = addr + 0x8000 if args.from_type == "file" else addr - 0x8000
        print(f"Converted address: 0x{converted:04X}")
    else:
        print(f"Address: 0x{addr:05X} (flat mapping, no conversion needed)")


# ── xdf ──────────────────────────────────────────────────────────────────
def cmd_xdf(args):
    entries = _parse_xdf(args.input)
    if not entries:
        print(f"No definitions found in {args.input}")
        return

    # Filter
    if args.search:
        q = args.search.lower()
        entries = [e for e in entries if q in e["title"].lower()]
    if args.category:
        q = args.category.lower()
        entries = [e for e in entries if q in e.get("category", "").lower()]
    if args.addr:
        target = _parse_hex(args.addr)
        entries = [e for e in entries if e["address"] == target]

    if args.list or args.search or args.category or args.addr:
        # Force UTF-8 output for XDF titles that may contain unicode
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        print(f"{'Address':>10s}  {'Size':>5s}  {'Title'}")
        print(f"{'─'*10}  {'─'*5}  {'─'*50}")
        for e in sorted(entries, key=lambda x: x["address"]):
            print(f"  0x{e['address']:05X}  {e.get('size', '?'):>5s}  {e['title']}")
        print(f"\n{len(entries)} definitions")
    else:
        print(f"{len(entries)} definitions in {args.input}. Use --list, --search, or --addr.")


# ── info ─────────────────────────────────────────────────────────────────
def cmd_info(args):
    import hashlib
    with open(args.input, "rb") as f:
        data = f.read()

    md5 = hashlib.md5(data).hexdigest()
    size = len(data)

    print(f"File:     {args.input}")
    print(f"Size:     {size} bytes ({size//1024} KB)")
    print(f"MD5:      {md5}")
    print(f"SHA256:   {hashlib.sha256(data).hexdigest()}")
    print("Size/layout hints below do not identify engine, OS, calibration or compatibility.")

    # Identify format
    if size == 131072:
        fmt = "128KB size only; candidate VY layout requires independent identification"
        print(f"Format:   {fmt}")
        # Check reset vector
        reset_vec = (data[0x1FFFE] << 8) | data[0x1FFFF]
        print(f"Reset vector: ${reset_vec:04X}")
        # Check OSID region (typically near start of cal)
        osid_region = data[0x4000:0x4020].hex()
        print(f"Cal start (0x4000): {osid_region[:40]}...")
        # Checksum
        stored = _read_checksum(data, 6)
        calculated = _calc_checksum(data, 8)
        status = "VALID" if stored == calculated else f"MISMATCH (stored=0x{stored:04X} calc=0x{calculated:04X})"
        print(f"Generic GM16 arithmetic: {status} (unqualified for this image)")
        # Free space summary
        free_00 = _count_free(data, 0x00, 64)
        free_ff = _count_free(data, 0xFF, 64)
        print(f"Uniform fill candidates: {free_00:,} bytes (0x00), {free_ff:,} bytes (0xFF); ownership not proven")
    elif size == 262144:
        print("Format:   256KB size; architecture/OS unknown")
    elif size == 524288:
        print("Format:   512KB size; architecture/OS unknown")
    elif size == 32768:
        print("Format:   32KB (1227730 style, flat)")
    elif size == 65536:
        print("Format:   64KB (16197427 style)")
    else:
        print(f"Format:   Unknown ({size} bytes)")


# ═════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════

# ── VY V6 128KB address conversion ───────────────────────────────────────

def _file_to_cpu_vy(file_offset):
    """Convert file offset to CPU address for VY V6 128KB binary.

    VY V6 binary layout (128KB = 0x20000 bytes):
      0x00000-0x07FFF: Common area (calibration/shared), maps 1:1 to CPU $0000-$7FFF
      0x08000-0x0FFFF: Bank 1 program code, maps to CPU $8000-$FFFF
      0x10000-0x17FFF: Bank 2 program code, maps to CPU $8000-$FFFF
      0x18000-0x1FFFF: Bank 3 program code, maps to CPU $8000-$FFFF
    """
    if file_offset < 0x08000:
        return file_offset  # common/cal area maps 1:1
    elif file_offset < 0x10000:
        return 0x8000 + (file_offset - 0x08000)  # bank 1
    elif file_offset < 0x18000:
        return 0x8000 + (file_offset - 0x10000)  # bank 2
    elif file_offset < 0x20000:
        return 0x8000 + (file_offset - 0x18000)  # bank 3
    return file_offset

def _file_to_bank_vy(file_offset):
    """Determine which bank a file offset belongs to."""
    if file_offset < 0x08000:
        return "common"
    elif file_offset < 0x10000:
        return "bank1"
    elif file_offset < 0x18000:
        return "bank2"
    elif file_offset < 0x20000:
        return "bank3"
    return "unknown"

def _cpu_to_file_vy(cpu_addr, bank="2"):
    """Convert CPU address to file offset for a given bank."""
    bank = str(bank).replace("bank", "")
    if cpu_addr < 0x8000:
        return cpu_addr  # common area
    offset = cpu_addr - 0x8000
    if bank in ("1", "bank1"):
        return 0x08000 + offset
    elif bank in ("2", "bank2"):
        return 0x10000 + offset
    elif bank in ("3", "bank3"):
        return 0x18000 + offset
    elif bank in ("common",):
        return cpu_addr
    return 0x10000 + offset  # default bank 2

def _cpu_to_file_range_vy(cpu_start, cpu_end, bank=None):
    """Convert CPU range to file offset range."""
    if bank is None:
        bank = "2"  # default to bank 2 (engine code)
    off_start = _cpu_to_file_vy(cpu_start, bank)
    off_end = _cpu_to_file_vy(cpu_end, bank)
    return off_start, off_end, cpu_start


# ── Disassembler ─────────────────────────────────────────────────────────

# HC11 opcode table — inherent, immediate, direct, extended, indexed, relative, bit ops
# Format: opcode -> (mnemonic, total_length, mode)
# For prebyte instructions ($18, $1A, $CD), handled in decoder
_OPCODES = {
    # Inherent (1 byte)
    0x01: ("NOP", 1, "inh"), 0x02: ("IDIV", 1, "inh"), 0x03: ("FDIV", 1, "inh"),
    0x04: ("LSRD", 1, "inh"), 0x05: ("ASLD", 1, "inh"),
    0x06: ("TAP", 1, "inh"), 0x07: ("TPA", 1, "inh"),
    0x08: ("INX", 1, "inh"), 0x09: ("DEX", 1, "inh"),
    0x0A: ("CLV", 1, "inh"), 0x0B: ("SEV", 1, "inh"),
    0x0C: ("CLC", 1, "inh"), 0x0D: ("SEC", 1, "inh"),
    0x0E: ("CLI", 1, "inh"), 0x0F: ("SEI", 1, "inh"),
    0x10: ("SBA", 1, "inh"), 0x11: ("CBA", 1, "inh"),
    0x16: ("TAB", 1, "inh"), 0x17: ("TBA", 1, "inh"),
    0x19: ("DAA", 1, "inh"), 0x1B: ("ABA", 1, "inh"),
    0x30: ("TSX", 1, "inh"), 0x31: ("INS", 1, "inh"),
    0x32: ("PULA", 1, "inh"), 0x33: ("PULB", 1, "inh"),
    0x34: ("DES", 1, "inh"), 0x35: ("TXS", 1, "inh"),
    0x36: ("PSHA", 1, "inh"), 0x37: ("PSHB", 1, "inh"),
    0x38: ("PULX", 1, "inh"), 0x39: ("RTS", 1, "inh"),
    0x3A: ("ABX", 1, "inh"), 0x3B: ("RTI", 1, "inh"),
    0x3C: ("PSHX", 1, "inh"), 0x3D: ("MUL", 1, "inh"),
    0x3E: ("WAI", 1, "inh"), 0x3F: ("SWI", 1, "inh"),
    # Unary A/B register ops
    0x40: ("NEGA", 1, "inh"), 0x43: ("COMA", 1, "inh"),
    0x44: ("LSRA", 1, "inh"), 0x46: ("RORA", 1, "inh"),
    0x47: ("ASRA", 1, "inh"), 0x48: ("ASLA", 1, "inh"),
    0x49: ("ROLA", 1, "inh"), 0x4A: ("DECA", 1, "inh"),
    0x4C: ("INCA", 1, "inh"), 0x4D: ("TSTA", 1, "inh"),
    0x4F: ("CLRA", 1, "inh"),
    0x50: ("NEGB", 1, "inh"), 0x53: ("COMB", 1, "inh"),
    0x54: ("LSRB", 1, "inh"), 0x56: ("RORB", 1, "inh"),
    0x57: ("ASRB", 1, "inh"), 0x58: ("ASLB", 1, "inh"),
    0x59: ("ROLB", 1, "inh"), 0x5A: ("DECB", 1, "inh"),
    0x5C: ("INCB", 1, "inh"), 0x5D: ("TSTB", 1, "inh"),
    0x5F: ("CLRB", 1, "inh"),
    # Indexed X (offset,X) — 2 bytes
    0x60: ("NEG", 2, "idx"), 0x63: ("COM", 2, "idx"),
    0x64: ("LSR", 2, "idx"), 0x66: ("ROR", 2, "idx"),
    0x67: ("ASR", 2, "idx"), 0x68: ("ASL", 2, "idx"),
    0x69: ("ROL", 2, "idx"), 0x6A: ("DEC", 2, "idx"),
    0x6C: ("INC", 2, "idx"), 0x6D: ("TST", 2, "idx"),
    0x6E: ("JMP", 2, "idx"), 0x6F: ("CLR", 2, "idx"),
    # Extended (3 bytes)
    0x70: ("NEG", 3, "ext"), 0x73: ("COM", 3, "ext"),
    0x74: ("LSR", 3, "ext"), 0x76: ("ROR", 3, "ext"),
    0x77: ("ASR", 3, "ext"), 0x78: ("ASL", 3, "ext"),
    0x79: ("ROL", 3, "ext"), 0x7A: ("DEC", 3, "ext"),
    0x7C: ("INC", 3, "ext"), 0x7D: ("TST", 3, "ext"),
    0x7E: ("JMP", 3, "ext"), 0x7F: ("CLR", 3, "ext"),
    # Branches (relative, 2 bytes)
    0x20: ("BRA", 2, "rel"), 0x21: ("BRN", 2, "rel"),
    0x22: ("BHI", 2, "rel"), 0x23: ("BLS", 2, "rel"),
    0x24: ("BCC", 2, "rel"), 0x25: ("BCS", 2, "rel"),
    0x26: ("BNE", 2, "rel"), 0x27: ("BEQ", 2, "rel"),
    0x28: ("BVC", 2, "rel"), 0x29: ("BVS", 2, "rel"),
    0x2A: ("BPL", 2, "rel"), 0x2B: ("BMI", 2, "rel"),
    0x2C: ("BGE", 2, "rel"), 0x2D: ("BLT", 2, "rel"),
    0x2E: ("BGT", 2, "rel"), 0x2F: ("BLE", 2, "rel"),
    0x8D: ("BSR", 2, "rel"),
    # LDAA / STAA / etc — immediate, direct, extended, indexed
    0x80: ("SUBA", 2, "imm"), 0x81: ("CMPA", 2, "imm"),
    0x82: ("SBCA", 2, "imm"), 0x83: ("SUBD", 3, "imm16"),
    0x84: ("ANDA", 2, "imm"), 0x85: ("BITA", 2, "imm"),
    0x86: ("LDAA", 2, "imm"), 0x88: ("EORA", 2, "imm"),
    0x89: ("ADCA", 2, "imm"), 0x8A: ("ORAA", 2, "imm"),
    0x8B: ("ADDA", 2, "imm"), 0x8C: ("CPX", 3, "imm16"),
    0x8E: ("LDS", 3, "imm16"), 0x8F: ("XGDX", 1, "inh"),
    0x90: ("SUBA", 2, "dir"), 0x91: ("CMPA", 2, "dir"),
    0x92: ("SBCA", 2, "dir"), 0x93: ("SUBD", 2, "dir"),
    0x94: ("ANDA", 2, "dir"), 0x95: ("BITA", 2, "dir"),
    0x96: ("LDAA", 2, "dir"), 0x97: ("STAA", 2, "dir"),
    0x98: ("EORA", 2, "dir"), 0x99: ("ADCA", 2, "dir"),
    0x9A: ("ORAA", 2, "dir"), 0x9B: ("ADDA", 2, "dir"),
    0x9C: ("CPX", 2, "dir"), 0x9D: ("JSR", 2, "dir"),
    0x9E: ("LDS", 2, "dir"), 0x9F: ("STS", 2, "dir"),
    0xA0: ("SUBA", 2, "idx"), 0xA1: ("CMPA", 2, "idx"),
    0xA2: ("SBCA", 2, "idx"), 0xA3: ("SUBD", 2, "idx"),
    0xA4: ("ANDA", 2, "idx"), 0xA5: ("BITA", 2, "idx"),
    0xA6: ("LDAA", 2, "idx"), 0xA7: ("STAA", 2, "idx"),
    0xA8: ("EORA", 2, "idx"), 0xA9: ("ADCA", 2, "idx"),
    0xAA: ("ORAA", 2, "idx"), 0xAB: ("ADDA", 2, "idx"),
    0xAC: ("CPX", 2, "idx"), 0xAD: ("JSR", 2, "idx"),
    0xAE: ("LDS", 2, "idx"), 0xAF: ("STS", 2, "idx"),
    0xB0: ("SUBA", 3, "ext"), 0xB1: ("CMPA", 3, "ext"),
    0xB2: ("SBCA", 3, "ext"), 0xB3: ("SUBD", 3, "ext"),
    0xB4: ("ANDA", 3, "ext"), 0xB5: ("BITA", 3, "ext"),
    0xB6: ("LDAA", 3, "ext"), 0xB7: ("STAA", 3, "ext"),
    0xB8: ("EORA", 3, "ext"), 0xB9: ("ADCA", 3, "ext"),
    0xBA: ("ORAA", 3, "ext"), 0xBB: ("ADDA", 3, "ext"),
    0xBC: ("CPX", 3, "ext"), 0xBD: ("JSR", 3, "ext"),
    0xBE: ("LDS", 3, "ext"), 0xBF: ("STS", 3, "ext"),
    # LDAB / STAB / etc
    0xC0: ("SUBB", 2, "imm"), 0xC1: ("CMPB", 2, "imm"),
    0xC2: ("SBCB", 2, "imm"), 0xC3: ("ADDD", 3, "imm16"),
    0xC4: ("ANDB", 2, "imm"), 0xC5: ("BITB", 2, "imm"),
    0xC6: ("LDAB", 2, "imm"), 0xC8: ("EORB", 2, "imm"),
    0xC9: ("ADCB", 2, "imm"), 0xCA: ("ORAB", 2, "imm"),
    0xCB: ("ADDB", 2, "imm"), 0xCC: ("LDD", 3, "imm16"),
    0xCE: ("LDX", 3, "imm16"),
    0xD0: ("SUBB", 2, "dir"), 0xD1: ("CMPB", 2, "dir"),
    0xD2: ("SBCB", 2, "dir"), 0xD3: ("ADDD", 2, "dir"),
    0xD4: ("ANDB", 2, "dir"), 0xD5: ("BITB", 2, "dir"),
    0xD6: ("LDAB", 2, "dir"), 0xD7: ("STAB", 2, "dir"),
    0xD8: ("EORB", 2, "dir"), 0xD9: ("ADCB", 2, "dir"),
    0xDA: ("ORAB", 2, "dir"), 0xDB: ("ADDB", 2, "dir"),
    0xDC: ("LDD", 2, "dir"), 0xDD: ("STD", 2, "dir"),
    0xDE: ("LDX", 2, "dir"), 0xDF: ("STX", 2, "dir"),
    0xE0: ("SUBB", 2, "idx"), 0xE1: ("CMPB", 2, "idx"),
    0xE2: ("SBCB", 2, "idx"), 0xE3: ("ADDD", 2, "idx"),
    0xE4: ("ANDB", 2, "idx"), 0xE5: ("BITB", 2, "idx"),
    0xE6: ("LDAB", 2, "idx"), 0xE7: ("STAB", 2, "idx"),
    0xE8: ("EORB", 2, "idx"), 0xE9: ("ADCB", 2, "idx"),
    0xEA: ("ORAB", 2, "idx"), 0xEB: ("ADDB", 2, "idx"),
    0xEC: ("LDD", 2, "idx"), 0xED: ("STD", 2, "idx"),
    0xEE: ("LDX", 2, "idx"), 0xEF: ("STX", 2, "idx"),
    0xF0: ("SUBB", 3, "ext"), 0xF1: ("CMPB", 3, "ext"),
    0xF2: ("SBCB", 3, "ext"), 0xF3: ("ADDD", 3, "ext"),
    0xF4: ("ANDB", 3, "ext"), 0xF5: ("BITB", 3, "ext"),
    0xF6: ("LDAB", 3, "ext"), 0xF7: ("STAB", 3, "ext"),
    0xF8: ("EORB", 3, "ext"), 0xF9: ("ADCB", 3, "ext"),
    0xFA: ("ORAB", 3, "ext"), 0xFB: ("ADDB", 3, "ext"),
    0xFC: ("LDD", 3, "ext"), 0xFD: ("STD", 3, "ext"),
    0xFE: ("LDX", 3, "ext"), 0xFF: ("STX", 3, "ext"),
    # Bit manipulation — direct (4 bytes: opcode, addr, mask, rel)
    0x12: ("BRSET", 4, "bit_dir"), 0x13: ("BRCLR", 4, "bit_dir"),
    0x14: ("BSET", 3, "bit_dir_nrel"), 0x15: ("BCLR", 3, "bit_dir_nrel"),
    # Bit manipulation — indexed X (4 bytes: opcode, offset, mask, rel)
    0x1C: ("BSET", 3, "bit_idx_nrel"), 0x1D: ("BCLR", 3, "bit_idx_nrel"),
    0x1E: ("BRSET", 4, "bit_idx"), 0x1F: ("BRCLR", 4, "bit_idx"),
}

# Prebyte $18 — Y-register variants
_OPCODES_18 = {
    0x08: ("INY", 1, "inh"), 0x09: ("DEY", 1, "inh"),
    0x1C: ("BSET", 3, "bit_idy_nrel"), 0x1D: ("BCLR", 3, "bit_idy_nrel"),
    0x1E: ("BRSET", 4, "bit_idy"), 0x1F: ("BRCLR", 4, "bit_idy"),
    0x30: ("TSY", 1, "inh"), 0x35: ("TYS", 1, "inh"),
    0x38: ("PULY", 1, "inh"), 0x3A: ("ABY", 1, "inh"),
    0x3C: ("PSHY", 1, "inh"),
    0x60: ("NEG", 2, "idy"), 0x63: ("COM", 2, "idy"),
    0x64: ("LSR", 2, "idy"), 0x66: ("ROR", 2, "idy"),
    0x67: ("ASR", 2, "idy"), 0x68: ("ASL", 2, "idy"),
    0x69: ("ROL", 2, "idy"), 0x6A: ("DEC", 2, "idy"),
    0x6C: ("INC", 2, "idy"), 0x6D: ("TST", 2, "idy"),
    0x6E: ("JMP", 2, "idy"), 0x6F: ("CLR", 2, "idy"),
    0x8C: ("CPY", 3, "imm16"), 0x8F: ("XGDY", 1, "inh"),
    0x9C: ("CPY", 2, "dir"),
    0xA0: ("SUBA", 2, "idy"), 0xA1: ("CMPA", 2, "idy"),
    0xA3: ("SUBD", 2, "idy"), 0xA4: ("ANDA", 2, "idy"),
    0xA6: ("LDAA", 2, "idy"), 0xA7: ("STAA", 2, "idy"),
    0xA8: ("EORA", 2, "idy"), 0xAA: ("ORAA", 2, "idy"),
    0xAC: ("CPY", 2, "idy"), 0xAD: ("JSR", 2, "idy"),
    0xAE: ("LDS", 2, "idy"), 0xAF: ("STS", 2, "idy"),
    0xBC: ("CPY", 3, "ext"),
    0xCE: ("LDY", 3, "imm16"),
    0xDE: ("LDY", 2, "dir"), 0xDF: ("STY", 2, "dir"),
    0xE0: ("SUBB", 2, "idy"), 0xE1: ("CMPB", 2, "idy"),
    0xE3: ("ADDD", 2, "idy"), 0xE4: ("ANDB", 2, "idy"),
    0xE6: ("LDAB", 2, "idy"), 0xE7: ("STAB", 2, "idy"),
    0xE8: ("EORB", 2, "idy"), 0xEA: ("ORAB", 2, "idy"),
    0xEC: ("LDD", 2, "idy"), 0xED: ("STD", 2, "idy"),
    0xEE: ("LDY", 2, "idy"), 0xEF: ("STY", 2, "idy"),
    0xFE: ("LDY", 3, "ext"), 0xFF: ("STY", 3, "ext"),
}

# Prebyte $1A — CPD instructions
_OPCODES_1A = {
    0x83: ("CPD", 3, "imm16"),
    0x93: ("CPD", 2, "dir"),
    0xA3: ("CPD", 2, "idx"),
    0xB3: ("CPD", 3, "ext"),
}

# Prebyte $CD — Y-indexed CPD and CPX
_OPCODES_CD = {
    0xA3: ("CPD", 2, "idy"),
    0xAC: ("CPX", 2, "idy"),
    0xEE: ("LDX", 2, "idy"),
    0xEF: ("STX", 2, "idy"),
}


def _disassemble_bytes(data, base_addr):
    """Disassemble raw bytes into HC11 mnemonics.

    Handles prebyte sequences ($18 for Y-register, $1A for CPD, $CD for Y-indexed CPD/CPX).
    Returns a list of formatted lines: '$ADDR  HEXBYTES  MNEMONIC OPERAND'.
    """
    lines = []
    i = 0
    while i < len(data):
        addr = base_addr + i
        b = data[i]

        # Check for prebyte
        if b == 0x18 and i + 1 < len(data):
            op2 = data[i + 1]
            if op2 in _OPCODES_18:
                mnem, length, mode = _OPCODES_18[op2]
                total_len = length + 1  # +1 for prebyte
                raw = data[i:i + total_len]
                operand = _format_operand(data, i + 2, mode, addr + total_len)
                lines.append(f"${addr:04X}  {raw.hex().upper():12s}  {mnem:6s} {operand}")
                i += total_len
                continue

        if b == 0x1A and i + 1 < len(data):
            op2 = data[i + 1]
            if op2 in _OPCODES_1A:
                mnem, length, mode = _OPCODES_1A[op2]
                total_len = length + 1
                raw = data[i:i + total_len]
                operand = _format_operand(data, i + 2, mode, addr + total_len)
                lines.append(f"${addr:04X}  {raw.hex().upper():12s}  {mnem:6s} {operand}")
                i += total_len
                continue

        if b == 0xCD and i + 1 < len(data):
            op2 = data[i + 1]
            if op2 in _OPCODES_CD:
                mnem, length, mode = _OPCODES_CD[op2]
                total_len = length + 1
                raw = data[i:i + total_len]
                operand = _format_operand(data, i + 2, mode, addr + total_len)
                lines.append(f"${addr:04X}  {raw.hex().upper():12s}  {mnem:6s} {operand}")
                i += total_len
                continue

        # Normal opcode
        if b in _OPCODES:
            mnem, length, mode = _OPCODES[b]
            if i + length > len(data):
                lines.append(f"${addr:04X}  {b:02X}            FCB    ${b:02X}  ; truncated")
                i += 1
                continue
            raw = data[i:i + length]
            operand = _format_operand(data, i + 1, mode, addr + length)
            lines.append(f"${addr:04X}  {raw.hex().upper():12s}  {mnem:6s} {operand}")
            i += length
        else:
            lines.append(f"${addr:04X}  {b:02X}            FCB    ${b:02X}")
            i += 1

    return lines


def _format_operand(data, operand_start, mode, next_addr):
    """Format operand string for a given addressing mode."""
    if mode == "inh":
        return ""
    elif mode == "imm":
        if operand_start < len(data):
            return f"#${data[operand_start]:02X}"
        return "#??"
    elif mode == "imm16":
        if operand_start + 1 < len(data):
            val = (data[operand_start] << 8) | data[operand_start + 1]
            return f"#${val:04X}"
        return "#????"
    elif mode == "dir":
        if operand_start < len(data):
            return f"${data[operand_start]:02X}"
        return "$??"
    elif mode == "ext":
        if operand_start + 1 < len(data):
            val = (data[operand_start] << 8) | data[operand_start + 1]
            return f"${val:04X}"
        return "$????"
    elif mode in ("idx", "idy"):
        reg = "X" if mode == "idx" else "Y"
        if operand_start < len(data):
            return f"${data[operand_start]:02X},{reg}"
        return f"$??,{reg}"
    elif mode == "rel":
        if operand_start < len(data):
            offset = data[operand_start]
            if offset >= 0x80:
                offset -= 256
            target = next_addr + offset
            return f"${target:04X}"
        return "$????"
    elif mode.startswith("bit_dir"):
        # BRSET/BRCLR: addr, mask, rel  OR  BSET/BCLR: addr, mask
        if "nrel" in mode:
            if operand_start + 1 < len(data):
                addr = data[operand_start]
                mask = data[operand_start + 1]
                return f"${addr:02X},#${mask:02X}"
            return "$??,#$??"
        else:
            if operand_start + 2 < len(data):
                addr = data[operand_start]
                mask = data[operand_start + 1]
                rel = data[operand_start + 2]
                if rel >= 0x80:
                    rel -= 256
                target = next_addr + rel
                return f"${addr:02X},#${mask:02X},${target:04X}"
            return "$??,#$??,${????"
    elif mode.startswith("bit_idx") or mode.startswith("bit_idy"):
        reg = "X" if "idx" in mode else "Y"
        if "nrel" in mode:
            if operand_start + 1 < len(data):
                off = data[operand_start]
                mask = data[operand_start + 1]
                return f"${off:02X},{reg},#${mask:02X}"
            return f"$??,{reg},#$??"
        else:
            if operand_start + 2 < len(data):
                off = data[operand_start]
                mask = data[operand_start + 1]
                rel = data[operand_start + 2]
                if rel >= 0x80:
                    rel -= 256
                target = next_addr + rel
                return f"${off:02X},{reg},#${mask:02X},${target:04X}"
            return f"$??,{reg},#$??,$????"
    return ""


# ── Checksum (GM ROM) ───────────────────────────────────────────────────

def _calc_checksum(data, sum_offset=8):
    """Calculate GM ROM checksum: 16-bit sum of all bytes from sum_offset to end.

    GM PCMs store a 16-bit big-endian checksum near the start of the binary.
    The checksum is the truncated sum of all bytes from a starting offset
    (typically 8) through the end of the file.
    """
    if type(sum_offset) is not int or not 0 <= sum_offset <= len(data):
        raise ValueError("Checksum summation offset is outside the input")
    checksum = 0
    for b in data[sum_offset:]:
        checksum = (checksum + b) & 0xFFFF
    return checksum

def _read_checksum(data, chk_offset=6):
    """Read stored 16-bit big-endian checksum."""
    if type(chk_offset) is not int or not 0 <= chk_offset <= len(data) - 2:
        raise ValueError("Stored checksum requires two bytes inside the input")
    import struct
    return struct.unpack(">H", bytes(data[chk_offset:chk_offset + 2]))[0]

def _fix_checksum_inplace(rom, chk_offset=6, sum_offset=8):
    """Recalculate and write checksum in-place."""
    import struct
    # Zero out current checksum bytes before calculating
    old_stored = struct.unpack(">H", bytes(rom[chk_offset:chk_offset + 2]))[0]
    rom[chk_offset] = 0
    rom[chk_offset + 1] = 0
    # Calculate with zeroed checksum
    total = _calc_checksum(rom, sum_offset)
    # The checksum value should be stored such that total + stored = target
    # For GM: checksum IS the sum, stored directly
    struct.pack_into(">H", rom, chk_offset, total)
    new_stored = total
    if old_stored != new_stored:
        print(f"Checksum updated: 0x{old_stored:04X} -> 0x{new_stored:04X}")
    else:
        print(f"Checksum unchanged: 0x{new_stored:04X}")


# ── Free space finder ────────────────────────────────────────────────────

def _count_free(data, fill_byte, min_size):
    """Count total bytes in free regions >= min_size filled with fill_byte."""
    total = 0
    run = 0
    for b in data:
        if b == fill_byte:
            run += 1
        else:
            if run >= min_size:
                total += run
            run = 0
    if run >= min_size:
        total += run
    return total


# ── Patch helpers ────────────────────────────────────────────────────────

def _parse_hook(hook_str):
    """Parse hook argument 'OFFSET:SIZE' -> (offset, size)."""
    parts = hook_str.split(":")
    offset = _parse_hex(parts[0])
    size = int(parts[1]) if len(parts) > 1 else 3
    return offset, size

def _normalize_sha256(value):
    """Normalize and validate a SHA256 supplied on the command line."""
    import re
    digest = value.strip().lower()
    if digest.startswith("sha256:"):
        digest = digest[7:]
    if not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise ValueError("--expect-sha256 must contain exactly 64 hexadecimal characters")
    return digest


def _parse_expected_bytes(value):
    """Parse human-friendly hex bytes such as 'FD017B' or 'FD 01 7B'."""
    import re
    cleaned = re.sub(r"(?i)0x", "", value)
    cleaned = re.sub(r"\s+", "", cleaned)
    if not re.fullmatch(r"(?:[0-9a-fA-F]{2})+", cleaned):
        raise ValueError("Expected bytes must contain a whole number of hexadecimal bytes")
    return bytes.fromhex(cleaned)


def _patched_name(path):
    """Generate patched output filename."""
    base, ext = os.path.splitext(path)
    return f"{base}_patched{ext}"

def _s19_to_bytes(path, expected_origin=None):
    """Read checksum-validated, contiguous S1 data without losing addresses."""
    data = bytearray()
    next_address = expected_origin
    with open(path, "r", encoding="ascii") as f:
        for number, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            if not line.startswith(("S0", "S1", "S9")):
                raise ValueError(f"S19 line {number}: only S0/S1/S9 records are supported")
            record = bytes.fromhex(line[2:])
            if not record or record[0] < 3 or len(record) != record[0] + 1 or sum(record) & 255 != 255:
                raise ValueError(f"S19 line {number}: invalid count or checksum")
            if line.startswith("S1"):
                address = int.from_bytes(record[1:3], "big")
                payload = record[3:-1]
                if next_address is not None and address != next_address:
                    raise ValueError(f"S19 line {number}: noncontiguous or mismatched address")
                next_address = address + len(payload)
                if next_address > 0x10000:
                    raise ValueError(f"S19 line {number}: exceeds 16-bit address space")
                data.extend(payload)
    if not data:
        raise ValueError("S19 contains no S1 data")
    return bytes(data)


# ── XDF parser ───────────────────────────────────────────────────────────

def _parse_xdf(path):
    """Parse a TunerPro XDF file and return list of definitions.

    XDF files are XML-based definition files used by TunerPro to describe
    the layout of ECU calibration data. This parser extracts table,
    constant, and flag definitions with their addresses and sizes.

    Returns a list of dicts with keys: title, address, size, category, type.
    """
    import xml.etree.ElementTree as ET
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            tree = ET.parse(f)
    except Exception as e:
        print(f"Error parsing XDF: {e}", file=sys.stderr)
        return []

    root = tree.getroot()
    entries = []

    # Find all TABLE/CONSTANT/FLAG definitions
    for tag in ["XDFTABLE", "XDFCONSTANT", "XDFFLAG"]:
        for elem in root.iter(tag):
            title = ""
            address = 0
            category = ""
            size = "?"

            title_elem = elem.find("title")  # direct child only
            if title_elem is not None and title_elem.text:
                title = title_elem.text.strip()

            # For tables, address is on the Z-axis (data) EMBEDDEDDATA
            # For constants/flags, address is on the direct EMBEDDEDDATA child
            embed = None
            if tag == "XDFTABLE":
                # Look for Z-axis (id="z") first, then direct EMBEDDEDDATA
                for axis in elem.findall("XDFAXIS"):
                    if axis.get("id") == "z":
                        embed = axis.find("EMBEDDEDDATA")
                        break
                if embed is None:
                    embed = elem.find("EMBEDDEDDATA")
            else:
                embed = elem.find("EMBEDDEDDATA")

            if embed is not None:
                addr_attr = embed.get("mmedaddress", "")
                if addr_attr:
                    try:
                        address = int(addr_attr, 0)
                    except ValueError:
                        address = 0
                size_attr = embed.get("mmedelementsizebits", "8")
                try:
                    size = str(int(size_attr) // 8) + "B"
                except ValueError:
                    size = "?"

            # Category
            cat_elem = elem.find("CATEGORYMEM")
            if cat_elem is not None:
                cat_id = cat_elem.get("category", "")
                category = cat_id

            if title and address > 0:
                entries.append({
                    "title": title,
                    "address": address,
                    "size": size,
                    "category": category,
                    "type": tag.replace("XDF", "").lower(),
                })

    return entries


# ═════════════════════════════════════════════════════════════════════════════
# COMMAND DISPATCH TABLE
# ═════════════════════════════════════════════════════════════════════════════

COMMANDS = {
    "asm": cmd_asm,
    "disasm": cmd_disasm,
    "compile": cmd_compile,
    "patch": cmd_patch,
    "free": cmd_free,
    "checksum": cmd_checksum,
    "addr": cmd_addr,
    "xdf": cmd_xdf,
    "info": cmd_info,
}


if __name__ == "__main__":
    main()
