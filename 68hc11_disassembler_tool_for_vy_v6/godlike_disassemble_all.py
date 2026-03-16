#!/usr/bin/env python3
"""
===============================================================================
 KingAI Godlike HC11 Disassembler & XDF Labeler — All-In-One Orchestrator
===============================================================================
 HC11F CONFIRMED: DARC.BIN=68HC11FC0, IDA Pro=HC11F1,
 PCMhacking topic_1573 (sabercatpuck). Crystal=13.631488MHz,
 E-clock=3.408MHz, TMSK2 prescaler=÷16 (PR1:PR0=11).
 ISR vectors: RESET→$202A, TIC3→$200F, TOC3→$2009,
 TOC2→$2000, TIC2→$2012, IRQ→$2018, SCI→$2003.
 See HARDWARE_SPECS.md for full details.

 Runs ALL disassembly backends on bank-split .bin files, then auto-applies
 XDF annotation labeling to every output. One script to rule them all.

 BACKENDS:
   1. Capstone M680X  — via split_and_disassemble.py (recursive descent + linear)
   2. GNU m6811-elf   — via m6811-elf-objdump (external binary)
   3. udis            — via udis.py + 6811.py (Jeff Tranter's universal disassembler)
  4. OPCODE . PY
  
 POST-PROCESSING:
   XDF Auto-Labeler   — via xdf_asm_labeler.py (annotates ALL outputs with
                         calibration names, flag states, table boundaries,
                         and code cross-references from TunerPro XDF exports)

 TARGETS SUPPORTED:
   - VY V6 Enhanced v1.0a ($060A, 128KB, 3 banks)
   - VY V6 Enhanced v1.1a ($060A spark cut, 128KB, 3 banks)
   - VY V6 STOCK 92118883 ($060A, 128KB, 3 banks)
   - OSE 11P V104 (64KB, 2 banks: upper + lower)
   - Any future 128KB HC11 binary with matching XDF

  TODO: add cli options to choose number of banks then offsets for each split.
  TODO: full enhanced ose 12p/11p support for people who want to see the guts.
 USAGE:
   python godlike_disassemble_all.py [--target TARGET] [--backends BACKENDS]
                                     [--no-label] [--no-diff] [--dry-run]

   --target    Which binary set to process (default: enhanced_v1.0a)
               Choices: enhanced_v1.0a, enhanced_v1.1a, stock, 11p, all
   --backends  Comma-separated list (default: capstone,gnu,udis)
   --no-label  Skip XDF labeling pass
   --no-diff   Skip STOCK-vs-Enhanced diffs
   --dry-run   Show what would be done without executing

 OUTPUT (per bank, per backend):
   {name}_bank{N}.asm              — Capstone disassembly (with fixed vectors)
   {name}_bank{N}_gnu.asm          — GNU m6811-elf-objdump output
   {name}_bank{N}_udis.asm         — udis HC11 output
   {name}_bank{N}_labeled.asm      — Capstone + XDF labels
   {name}_bank{N}_gnu_labeled.asm  — GNU + XDF labels
   {name}_bank{N}_udis_labeled.asm — udis + XDF labels

===============================================================================
 Author:       Jason King (KingAI)
 Date:         2026-02-20
 GitHub:       https://github.com/KingAiCodeForge
===============================================================================
"""

import os
import sys
import argparse
import subprocess
import shutil
import struct
import tempfile
from pathlib import Path
from datetime import datetime

# ─── Path Configuration ─────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).resolve().parent  # tools/
PROJECT_DIR = SCRIPT_DIR.parent               # VY_V6_Assembly_Modding/
OUTPUT_DIR = PROJECT_DIR / "bank_split_output"

# Tool paths
SPLIT_AND_DISASSEMBLE = SCRIPT_DIR / "split_and_disassemble.py"
XDF_ASM_LABELER = SCRIPT_DIR / "xdf_asm_labeler.py"
UDIS_DIR = PROJECT_DIR / "68HC11_Reference" / "udis"
UDIS_SCRIPT = UDIS_DIR / "udis.py"

# GNU m6811-elf tools: resolved via M6811_BIN_DIR env var, shutil.which(), or PATH
_m6811_bin_dir = os.environ.get("M6811_BIN_DIR", "")
GNU_OBJDUMP = (
    Path(_m6811_bin_dir) / "objdump.exe" if _m6811_bin_dir
    else Path(shutil.which("m6811-elf-objdump") or shutil.which("objdump") or "objdump")
)
GNU_OBJCOPY = (
    Path(_m6811_bin_dir) / "objcopy.exe" if _m6811_bin_dir
    else Path(shutil.which("m6811-elf-objcopy") or shutil.which("objcopy") or "objcopy")
)

# Bin/XDF sources
BIN_DIR = PROJECT_DIR / "xdfs_and_adx_and_bins_related_to_project"
XDF_EXPORT_DIR = PROJECT_DIR / "xdf_exports"


# ─── Target Definitions ─────────────────────────────────────────────────────

# Bank layout: (label, bin_start, bin_end, cpu_base)
BANKS_128K = [
    ("bank1", 0x00000, 0x10000, 0x0000),  # 64KB
    ("bank2", 0x10000, 0x18000, 0x8000),  # 32KB
    ("bank3", 0x18000, 0x20000, 0x8000),  # 32KB
]

BANKS_64K = [
    ("lower", 0x00000, 0x08000, 0x8000),  # 32KB lower
    ("upper", 0x08000, 0x10000, 0x8000),  # 32KB upper
]

# Target configurations
TARGETS = {
    "enhanced_v1.0a": {
        "display": "VY V6 Enhanced v1.0a ($060A)",
        "bins": {
            "Enhanced_v1.0a": "VX-VY_V6_$060A_Enhanced_v1.0a - Copy.bin",
        },
        "banks": BANKS_128K,
        "xdf_json": "Enhanced_v209b_export.json",
        "stock_bin": "92118883_STOCK.bin",
        "stock_name": "STOCK",
    },
    "enhanced_v1.1a": {
        "display": "VY V6 Enhanced v1.1a ($060A spark cut)",
        "bins": {
            "Enhanced_v1.1a": "VX-VY_V6_$060A_Enhanced_v1.1a.bin",
        },
        "banks": BANKS_128K,
        "xdf_json": "Enhanced_v209b_export.json",
        "stock_bin": "92118883_STOCK.bin",
        "stock_name": "STOCK",
    },
    "stock": {
        "display": "VY V6 STOCK 92118883",
        "bins": {
            "STOCK": "92118883_STOCK.bin",
        },
        "banks": BANKS_128K,
        "xdf_json": "VY_V6_060A.json",
        "stock_bin": None,
        "stock_name": None,
    },
    "11p": {
        "display": "OSE 11P V104 (CAKH V6)",
        "bins": {
            "11P_Enhanced_V104": "OSE_$11P V104 CAKH V6 __Stacked.BIN",
        },
        "banks": BANKS_128K,
        "xdf_json": "OSE_11P_V104.json",
        "stock_bin": None,  # TODO: find CAKH stock
        "stock_name": None,
    },
}


# ─── Backend Runners ─────────────────────────────────────────────────────────

def run_capstone(bin_path: Path, name: str, output_dir: Path, banks: list) -> list:
    """
    Run split_and_disassemble.py to produce Capstone disassembly.
    Returns list of (bank_label, asm_path) tuples.
    """
    print(f"\n  [CAPSTONE] Running split_and_disassemble.py on {bin_path.name}...")

    # The script expects to be run from its own directory with specific bin paths
    # We call it as a subprocess to keep environments isolated
    cmd = [
        sys.executable, str(SPLIT_AND_DISASSEMBLE),
    ]

    # split_and_disassemble.py has its own bin config; call it directly
    # and let it produce output in its OUTPUT_DIR
    result = subprocess.run(
        cmd,
        cwd=str(SPLIT_AND_DISASSEMBLE.parent),
        capture_output=True, text=True, timeout=300
    )

    if result.returncode != 0:
        print(f"    WARNING: Capstone exited with code {result.returncode}")
        if result.stderr:
            for line in result.stderr.strip().split('\n')[:10]:
                print(f"      {line}")

    # Collect output files
    outputs = []
    for bank_label, _, _, _ in banks:
        asm = output_dir / f"{name}_{bank_label}.asm"
        if asm.exists():
            outputs.append((bank_label, asm))
            print(f"    ✓ {asm.name}")
        else:
            print(f"    ✗ {asm.name} (not found)")

    return outputs


def run_gnu(bin_path: Path, name: str, output_dir: Path, banks: list) -> list:
    """
    Run GNU m6811-elf-objdump to produce GNU-format disassembly.
    Returns list of (bank_label, asm_path) tuples.
    """
    if not GNU_OBJDUMP.exists():
        print(f"  [GNU] SKIPPED — objdump not found at {GNU_OBJDUMP}")
        return []

    print(f"\n  [GNU] Running m6811-elf-objdump...")

    # Read full binary
    with open(bin_path, 'rb') as f:
        full_data = f.read()

    outputs = []
    for bank_label, start, end, cpu_base in banks:
        bank_data = full_data[start:end]
        bank_bin = output_dir / f"{name}_{bank_label}.bin"

        # Ensure bank .bin exists
        if not bank_bin.exists():
            with open(bank_bin, 'wb') as f:
                f.write(bank_data)

        # Create temp ELF from raw binary
        tmp_elf = output_dir / f"{bank_label}_temp.elf"
        try:
            objcopy_cmd = [
                str(GNU_OBJCOPY),
                "-I", "binary",
                "-O", "elf32-m68hc11",
                "-B", "m68hc11",
                "--change-section-address", f".data+{cpu_base:#x}",
                str(bank_bin),
                str(tmp_elf)
            ]
            subprocess.run(objcopy_cmd, capture_output=True, text=True, timeout=60, check=True)

            # Disassemble
            objdump_cmd = [
                str(GNU_OBJDUMP),
                "-D", "-m", "m68hc11",
                str(tmp_elf)
            ]
            result = subprocess.run(objdump_cmd, capture_output=True, text=True, timeout=120)

            out_asm = output_dir / f"{name}_{bank_label}_gnu.asm"
            with open(out_asm, 'w', encoding='utf-8') as f:
                f.write(result.stdout)

            outputs.append((bank_label, out_asm))
            print(f"    ✓ {out_asm.name}")
        except subprocess.CalledProcessError as e:
            print(f"    ✗ {bank_label}_gnu.asm — objcopy/objdump failed: {e}")
        except FileNotFoundError:
            print(f"    ✗ {bank_label}_gnu.asm — GNU tools not found")
        finally:
            if tmp_elf.exists():
                tmp_elf.unlink()

    return outputs


def run_udis(bin_path: Path, name: str, output_dir: Path, banks: list) -> list:
    """
    Run udis (Jeff Tranter's universal disassembler) on each bank.
    Returns list of (bank_label, asm_path) tuples.
    """
    if not UDIS_SCRIPT.exists():
        print(f"  [UDIS] SKIPPED — udis.py not found at {UDIS_SCRIPT}")
        return []

    print(f"\n  [UDIS] Running udis HC11 disassembler...")

    # Read full binary
    with open(bin_path, 'rb') as f:
        full_data = f.read()

    outputs = []
    for bank_label, start, end, cpu_base in banks:
        bank_data = full_data[start:end]
        bank_bin = output_dir / f"{name}_{bank_label}.bin"

        # Ensure bank .bin exists
        if not bank_bin.exists():
            with open(bank_bin, 'wb') as f:
                f.write(bank_data)

        out_asm = output_dir / f"{name}_{bank_label}_udis.asm"

        try:
            udis_cmd = [
                sys.executable, str(UDIS_SCRIPT),
                "-c", "6811",         # CPU type
                "-a", f"{cpu_base:#06x}",  # Base address
                "-n",                 # No listing header
                str(bank_bin)
            ]
            result = subprocess.run(
                udis_cmd,
                capture_output=True, text=True, timeout=120,
                cwd=str(UDIS_DIR)
            )

            with open(out_asm, 'w', encoding='utf-8') as f:
                f.write(result.stdout)

            outputs.append((bank_label, out_asm))
            print(f"    ✓ {out_asm.name}")
        except subprocess.CalledProcessError as e:
            print(f"    ✗ {bank_label}_udis.asm — udis failed: {e}")
        except FileNotFoundError:
            print(f"    ✗ {bank_label}_udis.asm — Python or udis not found")

    return outputs


def run_xdf_labeler(asm_path: Path, xdf_json: Path, bank_num: int) -> Path:
    """
    Run the XDF auto-labeler on a single ASM file.
    Returns path to the labeled output.
    """
    if not XDF_ASM_LABELER.exists():
        print(f"    [XDF] SKIPPED — labeler not found at {XDF_ASM_LABELER}")
        return None

    stem = asm_path.stem
    out_path = asm_path.parent / f"{stem}_labeled{asm_path.suffix}"

    try:
        cmd = [
            sys.executable, str(XDF_ASM_LABELER),
            str(xdf_json),
            str(asm_path),
            str(out_path),
            "--bank", str(bank_num),
            "--stats"
        ]
        result = subprocess.run(
            cmd,
            capture_output=True, text=True, timeout=300,
            cwd=str(XDF_ASM_LABELER.parent)
        )

        if out_path.exists():
            size_kb = out_path.stat().st_size / 1024
            print(f"    ✓ {out_path.name} ({size_kb:.0f} KB)")
            return out_path
        else:
            print(f"    ✗ {out_path.name} — labeler produced no output")
            if result.stderr:
                for line in result.stderr.strip().split('\n')[:5]:
                    print(f"      {line}")
            return None
    except Exception as e:
        print(f"    ✗ {out_path.name} — error: {e}")
        return None


# ─── Diff Engine ─────────────────────────────────────────────────────────────

def diff_banks_binary(stock_data: bytes, enh_data: bytes, bank_label: str,
                      cpu_base: int, output_dir: Path, stock_name: str,
                      enh_name: str) -> Path:
    """Binary diff between two bank extracts."""
    if len(stock_data) != len(enh_data):
        print(f"    ✗ Size mismatch in {bank_label}: {len(stock_data)} vs {len(enh_data)}")
        return None

    diffs = []
    run_start = None
    run_stock = bytearray()
    run_enh = bytearray()

    for i in range(len(stock_data)):
        if stock_data[i] != enh_data[i]:
            if run_start is None:
                run_start = i
                run_stock = bytearray()
                run_enh = bytearray()
            run_stock.append(stock_data[i])
            run_enh.append(enh_data[i])
        else:
            if run_start is not None:
                diffs.append((run_start, bytes(run_stock), bytes(run_enh)))
                run_start = None

    if run_start is not None:
        diffs.append((run_start, bytes(run_stock), bytes(run_enh)))

    out_path = output_dir / f"diff_{stock_name}_vs_{enh_name}_{bank_label}.txt"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(f"Binary Diff: {stock_name} vs {enh_name} — {bank_label}\n")
        f.write(f"{'=' * 70}\n")
        f.write(f"Bank CPU base: ${cpu_base:04X}\n")
        changed_bytes = sum(len(s) for _, s, _ in diffs)
        f.write(f"Total: {len(diffs)} regions, {changed_bytes} bytes changed\n\n")

        for offset, s_bytes, e_bytes in diffs:
            cpu_addr = cpu_base + offset
            f.write(f"--- Offset ${offset:04X} (CPU ${cpu_addr:04X}), {len(s_bytes)} byte(s) ---\n")
            s_hex = " ".join(f"{b:02X}" for b in s_bytes)
            e_hex = " ".join(f"{b:02X}" for b in e_bytes)
            f.write(f"  {stock_name}: {s_hex}\n")
            f.write(f"  {enh_name}:   {e_hex}\n\n")

    print(f"    ✓ {out_path.name} ({len(diffs)} regions, {changed_bytes} bytes)")
    return out_path


# ─── Main Orchestrator ──────────────────────────────────────────────────────

def find_bin(target_cfg: dict, bin_name: str) -> Path:
    """Find binary file in known locations."""
    # Check output dir first (already split)
    candidates = [
        BIN_DIR / bin_name,
        OUTPUT_DIR / bin_name,
        PROJECT_DIR / bin_name,
        # Also check cc dir (relative to project root)
        PROJECT_DIR.parent / "vy_$060a_enhanced_1.0_bin_xdf_example" / bin_name,
    ]
    for p in candidates:
        if p.exists():
            return p
    # Recursive search as fallback
    for p in BIN_DIR.rglob(bin_name):
        return p
    return None


def process_target(target_name: str, backends: list, do_label: bool,
                   do_diff: bool, dry_run: bool):
    """Process a single target configuration."""
    cfg = TARGETS[target_name]
    banks = cfg["banks"]

    print(f"\n{'='*72}")
    print(f"  TARGET: {cfg['display']}")
    print(f"  Banks: {len(banks)}")
    print(f"  Backends: {', '.join(backends)}")
    print(f"  XDF Label: {'YES' if do_label else 'NO'}")
    print(f"{'='*72}")

    # Resolve XDF JSON path
    xdf_json = XDF_EXPORT_DIR / cfg["xdf_json"]
    if not xdf_json.exists():
        print(f"\n  WARNING: XDF JSON not found: {xdf_json}")
        if do_label:
            print(f"  XDF labeling will be SKIPPED for this target.")
            do_label = False

    # Process each binary in this target
    for bin_label, bin_filename in cfg["bins"].items():
        bin_path = find_bin(cfg, bin_filename)
        if bin_path is None:
            print(f"\n  ✗ Binary not found: {bin_filename}")
            print(f"    Searched: {BIN_DIR}, {OUTPUT_DIR}, {PROJECT_DIR}")
            continue

        print(f"\n  Binary: {bin_path.name} ({bin_path.stat().st_size // 1024} KB)")

        if dry_run:
            print(f"  [DRY RUN] Would disassemble with: {', '.join(backends)}")
            continue

        OUTPUT_DIR.mkdir(exist_ok=True)
        all_outputs = []  # [(bank_label, backend_name, asm_path), ...]

        # --- Run each backend ---
        if "capstone" in backends:
            # For Capstone, we call split_and_disassemble directly
            # First, ensure the bins are split
            with open(bin_path, 'rb') as f:
                full_data = f.read()

            for bank_label, start, end, cpu_base in banks:
                bank_data = full_data[start:end]
                bank_bin = OUTPUT_DIR / f"{bin_label}_{bank_label}.bin"
                if not bank_bin.exists():
                    with open(bank_bin, 'wb') as f:
                        f.write(bank_data)
                    print(f"    Split: {bank_bin.name} ({len(bank_data)} bytes)")

            capstone_outputs = run_capstone(bin_path, bin_label, OUTPUT_DIR, banks)
            for bank_label, asm_path in capstone_outputs:
                all_outputs.append((bank_label, "capstone", asm_path))

        if "gnu" in backends:
            gnu_outputs = run_gnu(bin_path, bin_label, OUTPUT_DIR, banks)
            for bank_label, asm_path in gnu_outputs:
                all_outputs.append((bank_label, "gnu", asm_path))

        if "udis" in backends:
            udis_outputs = run_udis(bin_path, bin_label, OUTPUT_DIR, banks)
            for bank_label, asm_path in udis_outputs:
                all_outputs.append((bank_label, "udis", asm_path))

        # --- XDF Labeling Pass ---
        if do_label and xdf_json.exists():
            print(f"\n  [XDF LABELER] Applying labels from {cfg['xdf_json']}...")
            for bank_label, backend_name, asm_path in all_outputs:
                if not asm_path.exists():
                    continue
                # Determine bank number from label
                if 'bank1' in bank_label or 'lower' in bank_label:
                    bank_num = 1
                elif 'bank2' in bank_label:
                    bank_num = 2
                elif 'bank3' in bank_label or 'upper' in bank_label:
                    bank_num = 3
                else:
                    bank_num = 1  # default

                run_xdf_labeler(asm_path, xdf_json, bank_num)

    # --- Diffs ---
    if do_diff and cfg.get("stock_bin") and cfg.get("stock_name"):
        stock_bin_path = find_bin(cfg, cfg["stock_bin"])
        if stock_bin_path is None:
            print(f"\n  ✗ Stock binary not found for diff: {cfg['stock_bin']}")
        else:
            print(f"\n  [DIFF] Comparing {cfg['stock_name']} vs Enhanced...")
            with open(stock_bin_path, 'rb') as f:
                stock_data = f.read()

            for bin_label, bin_filename in cfg["bins"].items():
                bin_path = find_bin(cfg, bin_filename)
                if bin_path is None:
                    continue
                with open(bin_path, 'rb') as f:
                    enh_data = f.read()

                for bank_label, start, end, cpu_base in banks:
                    diff_banks_binary(
                        stock_data[start:end],
                        enh_data[start:end],
                        bank_label, cpu_base, OUTPUT_DIR,
                        cfg["stock_name"], bin_label
                    )


def main():
    parser = argparse.ArgumentParser(
        description="KingAI Godlike HC11 Disassembler — All-In-One Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python godlike_disassemble_all.py
  python godlike_disassemble_all.py --target enhanced_v1.0a --backends capstone,gnu
  python godlike_disassemble_all.py --target all --no-label
  python godlike_disassemble_all.py --target 11p --backends capstone --dry-run
        """
    )

    parser.add_argument(
        "--target", "-t",
        default="enhanced_v1.0a",
        choices=list(TARGETS.keys()) + ["all"],
        help="Which binary set to process (default: enhanced_v1.0a)"
    )
    parser.add_argument(
        "--backends", "-b",
        default="capstone,gnu,udis",
        help="Comma-separated backends (default: capstone,gnu,udis)"
    )
    parser.add_argument(
        "--no-label",
        action="store_true",
        help="Skip XDF labeling pass"
    )
    parser.add_argument(
        "--no-diff",
        action="store_true",
        help="Skip STOCK-vs-Enhanced diffs"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without executing"
    )

    args = parser.parse_args()

    backends = [b.strip().lower() for b in args.backends.split(",")]
    valid_backends = {"capstone", "gnu", "udis"}
    for b in backends:
        if b not in valid_backends:
            print(f"ERROR: Unknown backend '{b}'. Valid: {', '.join(valid_backends)}")
            sys.exit(1)

    print("=" * 72)
    print("  KingAI Godlike HC11 Disassembler & XDF Labeler")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Python: {sys.version.split()[0]}")
    print(f"  Output: {OUTPUT_DIR}")
    print("=" * 72)

    # Validate tool availability
    print("\n  Tool Check:")
    tools_ok = True
    if "capstone" in backends:
        if SPLIT_AND_DISASSEMBLE.exists():
            print(f"    ✓ Capstone:  {SPLIT_AND_DISASSEMBLE.name}")
        else:
            print(f"    ✗ Capstone: {SPLIT_AND_DISASSEMBLE} NOT FOUND")
            tools_ok = False
    if "gnu" in backends:
        if GNU_OBJDUMP.exists():
            print(f"    ✓ GNU:       {GNU_OBJDUMP}")
        else:
            print(f"    ✗ GNU:      {GNU_OBJDUMP} NOT FOUND — will skip")
    if "udis" in backends:
        if UDIS_SCRIPT.exists():
            print(f"    ✓ udis:      {UDIS_SCRIPT.name}")
        else:
            print(f"    ✗ udis:     {UDIS_SCRIPT} NOT FOUND — will skip")
    if not args.no_label:
        if XDF_ASM_LABELER.exists():
            print(f"    ✓ XDF Label: {XDF_ASM_LABELER.name}")
        else:
            print(f"    ✗ XDF Label: {XDF_ASM_LABELER} NOT FOUND — will skip labels")

    # Process targets
    if args.target == "all":
        target_list = list(TARGETS.keys())
    else:
        target_list = [args.target]

    for target_name in target_list:
        process_target(
            target_name,
            backends=backends,
            do_label=not args.no_label,
            do_diff=not args.no_diff,
            dry_run=args.dry_run
        )

    print(f"\n{'='*72}")
    print(f"  COMPLETE — All outputs in: {OUTPUT_DIR}")
    print(f"{'='*72}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
