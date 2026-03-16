#!/usr/bin/env python3
"""
===============================================================================
 KingAI XDF + HC11 → ASM Auto-Labeler  v2.1
===============================================================================

 Two independent label sources, each in their own module:

   hw_labels.py  → HWLabelMap   (133 labels, no JSON needed)
     [HW]   HC11 hardware registers ($1000-$103F)
     [RAM]  Confirmed RAM variables ($00A2=RPM, $0199=DWELL, etc.)
     [ISR]  ISR entry points & subroutines
     [VEC]  Interrupt vector table ($FFD6-$FFFE)
     [JMP]  Pseudo-vector jump table ($2000-$2021)
     [CODE] Other known addresses

   xdf_labels.py → XDFLabelMap  (1655 addresses, needs Enhanced_v1.json)
     [XDF]  Calibration data from XDF definition (scalars/flags/tables)

 These two modules share ZERO data. They don't import each other.
 This labeler combines both to annotate disassembly.

 Usage:
   python xdf_asm_labeler_v2.py <json_export> <input.asm> [output.asm] [--bank N] [--stats]

===============================================================================
 Author:       Jason King (KingAI)
 GitHub:       https://github.com/KingAiCodeForge
 Version:      2.1 — February 2026
===============================================================================
"""

import json
import re
import sys
import os
from pathlib import Path
from typing import List, Tuple
from collections import defaultdict

# ── Import the two independent label modules ──
from hw_labels import HWLabelMap
from xdf_labels import XDFLabelMap, CAL_RANGE


# ═══════════════════════════════════════════════════════════════════════
#  ASM FORMAT DETECTION & REGEX
# ═══════════════════════════════════════════════════════════════════════

def detect_asm_format(first_lines: List[str]) -> str:
    for line in first_lines[:50]:
        if re.match(r'^L[0-9A-Fa-f]{4}:', line):
            return 'custom'
        if re.match(r'^[0-9A-Fa-f]{4}\s+[0-9A-Fa-f]{2}\s', line):
            return 'udis'
        if re.match(r'^\s+[0-9a-f]+:\s+[0-9a-f]{2}\s', line):
            return 'gnu'
    return 'unknown'


# Custom: "L9058:  1A B3 4D 91      cpd      $4d91"
RE_CUSTOM_LINE = re.compile(
    r'^(L([0-9A-Fa-f]{4}):)\s+'
    r'([0-9A-Fa-f]{2}(?:\s+[0-9A-Fa-f]{2})*)'
    r'\s+(\S+)(?:\s+(.*))?$'
)

# Data: "L752A:  .byte   $9F, $38, $A0, ..."
RE_CUSTOM_DATA = re.compile(
    r'^(L([0-9A-Fa-f]{4}):)\s+'
    r'\.byte\s+(.+?)(?:\s*;.*)?$'
)

# Udis: "752A  9F 38            ldaa   $752B"
RE_UDIS_LINE = re.compile(
    r'^([0-9A-Fa-f]{4})\s+'
    r'([0-9A-Fa-f]{2}(?:\s+[0-9A-Fa-f]{2})*)'
    r'\s+(\S+)(?:\s+(.*))?$'
)

# $XXXX extended address (NOT immediates #$XX)
RE_EXTENDED_ADDR = re.compile(r'(?<!#)\$([0-9A-Fa-f]{4})\b')

# Direct-page $XX address references (NOT immediates #$XX)
# These are 1-byte addresses: ldaa $a2, stab $80, etc.
RE_DIRECT_ADDR = re.compile(
    r'(?<!#)\$([0-9A-Fa-f]{2})\b(?![0-9A-Fa-f])'
)

# Branch mnemonics — targets are code, not data
BRANCH_MNEMONICS = frozenset({
    'bra', 'brn', 'bhi', 'bls', 'bcc', 'bcs', 'bne', 'beq',
    'bvc', 'bvs', 'bpl', 'bmi', 'bge', 'blt', 'bgt', 'ble',
    'jmp',
})

# JSR is special — target is a code address we may know the name of
JSR_MNEMONICS = frozenset({'jsr', 'bsr'})


# ═══════════════════════════════════════════════════════════════════════
#  SECTION 8: CUSTOM FORMAT ANNOTATOR (v2)
# ═══════════════════════════════════════════════════════════════════════

def annotate_custom_format(
    lines: List[str],
    xdf: XDFLabelMap,
    hw: HWLabelMap,
    bank: int = 1,
) -> Tuple[List[str], dict]:
    """
    v2 annotator for the custom disassembler format.

    Three annotation sources checked per code line:
      1. XDF calibration addresses (scalars/flags/tables)
      2. HC11 hardware registers ($1000-$103F)
      3. RAM variables / ISR names / vector table
    """
    output = []
    stats = defaultdict(int)

    for line in lines:
        stripped = line.rstrip()

        # ── Pass 1: .byte data lines ──
        m_data = RE_CUSTOM_DATA.match(stripped)
        if m_data:
            addr = int(m_data.group(2), 16)
            byte_str = m_data.group(3)

            byte_count = len(
                re.findall(r'\$[0-9A-Fa-f]{2}', byte_str)
            )
            if byte_count < 1:
                byte_count = 1

            span_anns = []
            for offset in range(byte_count):
                check = addr + offset
                ann = xdf.lookup(check)
                if ann:
                    if len(ann) > 55:
                        ann = ann[:52] + "..."
                    prefix = (
                        f"${check:04X}"
                        if offset == 0
                        else f"+{offset}:${check:04X}"
                    )
                    span_anns.append(f"{prefix}: {ann}")

            if span_anns:
                combined = " | ".join(span_anns)
                output.append(
                    f"{stripped}  ; [XDF] {combined}"
                )
                stats['data_labeled'] += 1
                continue

            # Table interior check
            for ta, ti in xdf.tables.items():
                dims = ti.get('dimensions', {})
                rows = dims.get('rows', 0)
                cols = dims.get('cols', 0)
                sz = rows * cols
                if ta <= addr < ta + sz and addr != ta:
                    title = ti.get('title', '?')
                    row = (addr - ta) // cols if cols else 0
                    output.append(
                        f"{stripped}  ; [XDF] >> "
                        f"{title} [row {row}]"
                    )
                    stats['data_table_interior'] += 1
                    break
            else:
                output.append(stripped)
                stats['data_unlabeled'] += 1
            continue

        # ── Pass 2: Instruction lines (Lxxxx: hex mnemonic operand) ──
        m_code = RE_CUSTOM_LINE.match(stripped)
        if m_code:
            line_addr = int(m_code.group(2), 16)
            hex_bytes = m_code.group(3)
            mnemonic = m_code.group(4)
            operand = m_code.group(5) or ""
            mnem_lower = mnemonic.lower()

            # ── 2a: Calibration region — label as cal data ──
            if CAL_RANGE[0] <= line_addr < CAL_RANGE[1]:
                byte_count = len(hex_bytes.split())
                span_anns = []
                for offset in range(byte_count):
                    check = line_addr + offset
                    ann = xdf.lookup(check)
                    if ann:
                        if offset == 0:
                            if len(ann) > 70:
                                ann = ann[:67] + "..."
                            span_anns.append(
                                f"${check:04X}: {ann}"
                            )
                        else:
                            if len(ann) > 55:
                                ann = ann[:52] + "..."
                            span_anns.append(
                                f"+{offset}:${check:04X}: {ann}"
                            )

                if span_anns:
                    combined = " | ".join(span_anns)
                    output.append(
                        f"{stripped}  ; [XDF] {combined}"
                    )
                    stats['cal_data_labeled'] += 1
                    if len(span_anns) > 1:
                        stats['cal_multi_in_span'] += (
                            len(span_anns) - 1
                        )
                    continue

                # Table interior
                for ta, ti in xdf.tables.items():
                    dims = ti.get('dimensions', {})
                    rows = dims.get('rows', 0)
                    cols = dims.get('cols', 0)
                    sz = rows * cols
                    if (ta <= line_addr < ta + sz
                            and line_addr != ta):
                        title = ti.get('title', '?')
                        row = (line_addr - ta) // cols if cols else 0
                        output.append(
                            f"{stripped}  ; [XDF] >> "
                            f"{title} [row {row}]"
                        )
                        stats['cal_table_interior'] += 1
                        break
                else:
                    output.append(stripped)
                    stats['cal_no_match'] += 1
                continue

            # ── 2b: Code region — multi-source xref lookup ──
            is_branch = mnem_lower in BRANCH_MNEMONICS
            is_jsr = mnem_lower in JSR_MNEMONICS

            # Collect all comments for this line
            xref_comments = []

            # Extended addresses ($XXXX) in operand
            ext_refs = RE_EXTENDED_ADDR.findall(operand)
            for ref_hex in ext_refs:
                ref_addr = int(ref_hex, 16)

                if is_branch:
                    # Branch target is code — skip XDF, but
                    # check if it's a known ISR/subroutine name
                    hw_ann = hw.lookup(ref_addr)
                    if hw_ann:
                        if len(hw_ann) > 60:
                            hw_ann = hw_ann[:57] + "..."
                        xref_comments.append(hw_ann)
                        stats['hw_branch_target'] += 1
                    continue

                if is_jsr:
                    # JSR target — check ISR/subroutine names first
                    hw_ann = hw.lookup(ref_addr)
                    if hw_ann:
                        if len(hw_ann) > 60:
                            hw_ann = hw_ann[:57] + "..."
                        xref_comments.append(hw_ann)
                        stats['hw_jsr_target'] += 1
                    # Also check XDF (JSR into cal region is rare
                    # but possible for table lookups)
                    xdf_ann = xdf.lookup(ref_addr)
                    if xdf_ann:
                        if len(xdf_ann) > 60:
                            xdf_ann = xdf_ann[:57] + "..."
                        xref_comments.append(
                            f"[XDF] ${ref_hex.upper()}: "
                            f"{xdf_ann}"
                        )
                        stats['code_xref'] += 1
                    continue

                # Normal data access instruction
                # Priority: XDF > HW > RAM > ISR
                xdf_ann = xdf.lookup(ref_addr)
                hw_ann = hw.lookup(ref_addr)

                if xdf_ann:
                    if len(xdf_ann) > 60:
                        xdf_ann = xdf_ann[:57] + "..."
                    xref_comments.append(
                        f"[XDF] ${ref_hex.upper()}: {xdf_ann}"
                    )
                    stats['code_xref'] += 1
                elif hw_ann:
                    if len(hw_ann) > 60:
                        hw_ann = hw_ann[:57] + "..."
                    xref_comments.append(hw_ann)
                    stats['hw_xref'] += 1

            # Direct-page addresses ($XX) — check RAM + HW
            # Only if we haven't already found annotations from
            # extended refs (avoid duplicate hits)
            if not xref_comments and not is_branch:
                dir_refs = RE_DIRECT_ADDR.findall(operand)
                for ref_hex in dir_refs:
                    ref_addr = int(ref_hex, 16)
                    hw_ann = hw.lookup(ref_addr)
                    if hw_ann:
                        if len(hw_ann) > 60:
                            hw_ann = hw_ann[:57] + "..."
                        xref_comments.append(hw_ann)
                        stats['hw_direct'] += 1

            if xref_comments:
                comment = " | ".join(xref_comments)
                output.append(f"{stripped}  ; {comment}")
            else:
                output.append(stripped)
                stats['code_no_xref'] += 1
            continue

        # ── Non-matching lines ──
        output.append(stripped)
        stats['passthrough'] += 1

    return output, dict(stats)


# ═══════════════════════════════════════════════════════════════════════
#  SECTION 9: UDIS FORMAT ANNOTATOR (v2)
# ═══════════════════════════════════════════════════════════════════════

def annotate_udis_format(
    lines: List[str],
    xdf: XDFLabelMap,
    hw: HWLabelMap,
    bank: int = 1,
) -> Tuple[List[str], dict]:
    """Annotate ASM in udis86 format — v2 with HW/RAM/ISR."""
    output = []
    stats = defaultdict(int)

    for line in lines:
        stripped = line.rstrip()
        m = RE_UDIS_LINE.match(stripped)
        if m:
            addr = int(m.group(1), 16)
            mnemonic = m.group(3)
            operand = m.group(4) or ""
            mnem_lower = mnemonic.lower()

            # Cal region — XDF data annotation
            xdf_ann = xdf.lookup(addr)
            if xdf_ann and CAL_RANGE[0] <= addr < CAL_RANGE[1]:
                if len(xdf_ann) > 80:
                    xdf_ann = xdf_ann[:77] + "..."
                output.append(
                    f"{stripped}  ; [XDF] {xdf_ann}"
                )
                stats['data_labeled'] += 1
                continue

            # Code region — multi-source operand xrefs
            is_branch = mnem_lower in BRANCH_MNEMONICS
            is_jsr = mnem_lower in JSR_MNEMONICS
            xref_comments = []

            ext_refs = RE_EXTENDED_ADDR.findall(operand)
            for ref_hex in ext_refs:
                ref_addr = int(ref_hex, 16)

                if is_branch:
                    hw_ann = hw.lookup(ref_addr)
                    if hw_ann:
                        if len(hw_ann) > 60:
                            hw_ann = hw_ann[:57] + "..."
                        xref_comments.append(hw_ann)
                        stats['hw_branch_target'] += 1
                    continue

                if is_jsr:
                    hw_ann = hw.lookup(ref_addr)
                    if hw_ann:
                        if len(hw_ann) > 60:
                            hw_ann = hw_ann[:57] + "..."
                        xref_comments.append(hw_ann)
                        stats['hw_jsr_target'] += 1
                    continue

                xdf_a = xdf.lookup(ref_addr)
                hw_a = hw.lookup(ref_addr)
                if xdf_a:
                    if len(xdf_a) > 60:
                        xdf_a = xdf_a[:57] + "..."
                    xref_comments.append(
                        f"[XDF] ${ref_hex.upper()}: {xdf_a}"
                    )
                    stats['code_xref'] += 1
                elif hw_a:
                    if len(hw_a) > 60:
                        hw_a = hw_a[:57] + "..."
                    xref_comments.append(hw_a)
                    stats['hw_xref'] += 1

            # Direct-page
            if not xref_comments and not is_branch:
                dir_refs = RE_DIRECT_ADDR.findall(operand)
                for ref_hex in dir_refs:
                    ref_addr = int(ref_hex, 16)
                    hw_a = hw.lookup(ref_addr)
                    if hw_a:
                        if len(hw_a) > 60:
                            hw_a = hw_a[:57] + "..."
                        xref_comments.append(hw_a)
                        stats['hw_direct'] += 1

            if xref_comments:
                comment = " | ".join(xref_comments)
                output.append(f"{stripped}  ; {comment}")
            else:
                output.append(stripped)
                stats['code_no_xref'] += 1
            continue

        output.append(stripped)
        stats['passthrough'] += 1

    return output, dict(stats)


# ═══════════════════════════════════════════════════════════════════════
#  SECTION 10: CLI
# ═══════════════════════════════════════════════════════════════════════

def print_usage():
    print("KingAI XDF + HC11 → ASM Auto-Labeler v2.0")
    print()
    print("Usage:")
    print("  python xdf_asm_labeler_v2.py <json> <input.asm>"
          " [output.asm] [options]")
    print()
    print("Arguments:")
    print("  json          JSON from tunerpro_exporter.py")
    print("  input.asm     Disassembled ASM file to annotate")
    print("  output.asm    Output (default: <input>_labeled.asm)")
    print()
    print("Options:")
    print("  --bank N      Bank 1/2/3 (default: auto-detect)")
    print("  --stats       Print detailed statistics")
    print("  --summary     Print XDF + HW label summary")
    print("  --dry-run     Don't write output")
    print()
    print("Label Sources:")
    print("  [XDF]  Calibration (scalars/flags/tables)")
    print("  [HW]   HC11 hardware registers ($1000-$103F)")
    print("  [RAM]  Confirmed RAM variables ($00-$1FFF)")
    print("  [ISR]  ISR handlers & subroutines")
    print("  [VEC]  Interrupt vector table ($FFD6-$FFFE)")
    print("  [JMP]  Pseudo-vector jump table ($2000-$2021)")


def detect_bank_from_filename(filename: str) -> int:
    name_lower = filename.lower()
    if 'bank3' in name_lower:
        return 3
    elif 'bank2' in name_lower:
        return 2
    return 1


def main():
    args = sys.argv[1:]

    if not args or '--help' in args or '-h' in args:
        print_usage()
        sys.exit(0)

    positional = [a for a in args if not a.startswith('--')]
    flags = [a for a in args if a.startswith('--')]

    if len(positional) < 2:
        print("ERROR: Need <json_export> and <input.asm>")
        print_usage()
        sys.exit(1)

    json_path = positional[0]
    input_asm = positional[1]
    output_asm = (
        positional[2] if len(positional) > 2 else None
    )

    show_stats = '--stats' in flags
    show_summary = '--summary' in flags
    dry_run = '--dry-run' in flags

    bank = None
    for i, a in enumerate(args):
        if a == '--bank' and i + 1 < len(args):
            try:
                bank = int(args[i + 1])
                break
            except ValueError:
                pass

    if bank is None:
        bank = detect_bank_from_filename(input_asm)
        print(f"Auto-detected bank: {bank}")

    if bank not in (1, 2, 3):
        print(f"ERROR: Bank must be 1, 2, or 3 (got {bank})")
        sys.exit(1)

    if output_asm is None:
        base = Path(input_asm)
        output_asm = str(
            base.parent / f"{base.stem}_labeled{base.suffix}"
        )

    if not os.path.exists(json_path):
        print(f"ERROR: JSON not found: {json_path}")
        sys.exit(1)
    if not os.path.exists(input_asm):
        print(f"ERROR: ASM not found: {input_asm}")
        sys.exit(1)

    # ── Load label sources ──
    print(f"Loading XDF definitions from: {json_path}")
    xdf = XDFLabelMap(json_path, bank=bank)

    xdf_stats = xdf.stats()
    print(f"  XDF Definition: {xdf.definition_name}")
    print(
        f"  Loaded: {xdf_stats['scalars']} scalars, "
        f"{xdf_stats['flags']} flags, "
        f"{xdf_stats['tables']} tables, "
        f"{xdf_stats['table_axes']} axes"
    )
    print(
        f"  Address range: "
        f"{xdf_stats['addr_range'][0]} - "
        f"{xdf_stats['addr_range'][1]}"
    )
    print(
        f"  Total XDF addresses: "
        f"{xdf_stats['total_unique']}"
    )

    print("Loading HC11 hardware/RAM/ISR labels...")
    hw = HWLabelMap()
    hw_stats = hw.stats()
    total_hw = sum(hw_stats.values())
    tag_summary = ", ".join(
        f"{k}={v}" for k, v in sorted(hw_stats.items())
    )
    print(f"  {total_hw} labels: {tag_summary}")

    if show_summary:
        print("\n--- HW/RAM/ISR Label Summary ---")
        for addr in sorted(hw.labels):
            print(f"  ${addr:04X}: {hw.labels[addr]}")
        print()

    # ── Read ASM ──
    print(f"Reading ASM: {input_asm}")
    with open(input_asm, 'r', encoding='utf-8',
              errors='replace') as f:
        asm_lines = f.readlines()
    print(f"  {len(asm_lines)} lines")

    fmt = detect_asm_format(asm_lines)
    print(f"  Detected format: {fmt}")

    # ── Annotate ──
    print(f"Annotating (bank {bank})...")
    if fmt == 'custom':
        annotated, stats = annotate_custom_format(
            asm_lines, xdf, hw, bank
        )
    elif fmt == 'udis':
        annotated, stats = annotate_udis_format(
            asm_lines, xdf, hw, bank
        )
    else:
        print(f"  WARNING: Unknown format '{fmt}', "
              "trying custom parser...")
        annotated, stats = annotate_custom_format(
            asm_lines, xdf, hw, bank
        )

    # ── Results ──
    xdf_total = (
        stats.get('cal_data_labeled', 0)
        + stats.get('cal_table_interior', 0)
        + stats.get('data_labeled', 0)
        + stats.get('data_table_interior', 0)
        + stats.get('code_xref', 0)
    )
    hw_total = (
        stats.get('hw_xref', 0)
        + stats.get('hw_direct', 0)
        + stats.get('hw_jsr_target', 0)
        + stats.get('hw_branch_target', 0)
    )
    grand_total = xdf_total + hw_total

    print(f"\n  Results:")
    print(f"    --- XDF annotations ---")
    print(f"    Cal data labels:        "
          f"{stats.get('cal_data_labeled', 0)}")
    print(f"    Cal table interior:     "
          f"{stats.get('cal_table_interior', 0)}")
    print(f"    .byte data labels:      "
          f"{stats.get('data_labeled', 0)}")
    print(f"    .byte table interior:   "
          f"{stats.get('data_table_interior', 0)}")
    print(f"    Code xrefs (XDF):       "
          f"{stats.get('code_xref', 0)}")
    print(f"    XDF subtotal:           {xdf_total}")

    print(f"    --- HW/RAM/ISR annotations (NEW in v2) ---")
    print(f"    HW register xrefs:      "
          f"{stats.get('hw_xref', 0)}")
    print(f"    RAM direct-page:        "
          f"{stats.get('hw_direct', 0)}")
    print(f"    JSR/BSR targets:        "
          f"{stats.get('hw_jsr_target', 0)}")
    print(f"    Branch targets:         "
          f"{stats.get('hw_branch_target', 0)}")
    print(f"    HW subtotal:            {hw_total}")

    print(f"    --- Grand total ---")
    print(f"    Total annotations:      {grand_total}")
    unchanged = (
        stats.get('passthrough', 0)
        + stats.get('data_unlabeled', 0)
        + stats.get('code_no_xref', 0)
        + stats.get('cal_no_match', 0)
    )
    print(f"    Lines unchanged:        {unchanged}")

    if show_stats:
        print(f"\n  Detailed: {json.dumps(stats, indent=4)}")

    # ── Write output ──
    if not dry_run:
        print(f"\nWriting: {output_asm}")
        with open(output_asm, 'w', encoding='utf-8') as f:
            f.write("; ==========================================\n")
            f.write("; XDF + HC11 Labeled Disassembly  (v2.0)\n")
            f.write("; KingAI XDF+HC11 ASM Auto-Labeler\n")
            f.write(f"; XDF: {xdf.definition_name}\n")
            f.write(f"; Binary: {xdf.bin_name}\n")
            f.write(f"; Bank: {bank}\n")
            f.write(f"; Source: {Path(input_asm).name}\n")
            f.write(f"; XDF annotations: {xdf_total}\n")
            f.write(f"; HW/RAM/ISR annotations: {hw_total}\n")
            f.write(f"; Total annotations: {grand_total}\n")
            f.write("; Tags: [XDF] [HW] [RAM] [ISR] [VEC]"
                    " [JMP] [CODE]\n")
            f.write("; ==========================================\n")
            f.write(";\n")

            for aline in annotated:
                f.write(aline + '\n')

        print(f"Done! {grand_total} annotations added "
              f"to {output_asm}")
    else:
        print("\n[DRY RUN] No output written.")

    return 0


if __name__ == '__main__':
    sys.exit(main())
