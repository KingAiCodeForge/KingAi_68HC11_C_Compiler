#!/usr/bin/env python3
"""
===============================================================================
 KingAI XDF → ASM Auto-Labeler
===============================================================================
*** NOTE: This labeler is now auto-invoked by godlike_disassemble_all.py
*** on ALL disassembly outputs (Capstone, GNU, udis). You can still run it
*** standalone for manual annotation of individual ASM files.
*** Use:  python godlike_disassemble_all.py --target enhanced_v1.0a
===============================================================================

 Reads XDF calibration definitions (exported JSON from tunerpro_exporter.py)
 and annotates disassembled HC11 ASM files with human-readable labels.

 Two annotation modes:
   1. DATA LABELS  — In the calibration data region ($2000-$7FFF), replaces
                     generic Lxxxx labels with XDF names + values
   2. CODE XREFS   — In the code region ($8000-$FFFF), adds inline comments
                     wherever code references a known calibration address

 Supports the custom disassembler format (.asm from split_and_disassemble.py):
   L752A:  .byte   $9F, $38, $A0  →  L752A:  .byte   $9F  ; [XDF] C/L Upper o2 Threshold = 0.70 VOLTS

 Also supports the udis format:
   752A  9F              ldaa   #$9F  →  752A  9F              ldaa   #$9F  ; [XDF] ...

 Address Mapping (verified):
   XDF address = file offset in 128KB binary (BASEOFFSET=0)
   Bank1 = file[0x00000:0x10000], CPU $0000-$FFFF, .org $0000
   → XDF addr 0x752A = CPU $752A in bank1.asm ✓
   → All calibration data ($4000-$7FFC) is in bank1 only
   Bank2 = file[0x10000:0x18000], CPU $8000-$FFFF (paged)
   Bank3 = file[0x18000:0x20000], CPU $8000-$FFFF (paged)

 Usage:
   python xdf_asm_labeler.py <json_export> <input.asm> [output.asm] [--bank N] [--stats]

 If output is omitted, writes to <input>_labeled.asm

===============================================================================
 Author:       Jason King (KingAI)
 GitHub:       https://github.com/KingAiCodeForge
===============================================================================
"""

import json
import re
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict


# ─── Address Translation ────────────────────────────────────────────────────

# Bank definitions: (file_start, file_end, cpu_base)
BANK_MAP = {
    1: (0x00000, 0x10000, 0x0000),  # 64KB, CPU $0000-$FFFF
    2: (0x10000, 0x18000, 0x8000),  # 32KB, CPU $8000-$FFFF
    3: (0x18000, 0x20000, 0x8000),  # 32KB, CPU $8000-$FFFF
}

# Calibration data lives entirely within this CPU address range (bank1)
CAL_RANGE = (0x2000, 0x8000)  # $2000-$7FFF inclusive


def xdf_addr_to_cpu(xdf_addr: int, bank: int = 1) -> Optional[int]:
    """
    Convert an XDF address (= file offset) to a CPU address for a given bank.
    
    For bank1: CPU addr = XDF addr (since file_start=0, cpu_base=0)
    For bank2: CPU addr = XDF addr - 0x10000 + 0x8000 (file offset → CPU)
    For bank3: CPU addr = XDF addr - 0x18000 + 0x8000
    
    Returns None if the XDF address doesn't fall within this bank's file range.
    """
    file_start, file_end, cpu_base = BANK_MAP[bank]
    if file_start <= xdf_addr < file_end:
        file_offset_within_bank = xdf_addr - file_start
        return cpu_base + file_offset_within_bank
    return None


def cpu_to_xdf_addr(cpu_addr: int, bank: int = 1) -> int:
    """Convert CPU address back to XDF file offset for a given bank."""
    file_start, _, cpu_base = BANK_MAP[bank]
    return file_start + (cpu_addr - cpu_base)


# ─── XDF JSON Loader ────────────────────────────────────────────────────────

class XDFLabelMap:
    """
    Loads XDF export JSON and builds lookup tables:
      addr_to_scalar[cpu_addr] → {title, value, unit, equation, ...}
      addr_to_flag[cpu_addr]   → {title, mask, is_set}
      addr_to_table[cpu_addr]  → {title, axis, dimensions, ...}
    """
    
    def __init__(self, json_path: str, bank: int = 1):
        self.bank = bank
        self.scalars: Dict[int, dict] = {}      # cpu_addr → scalar info
        self.flags: Dict[int, dict] = {}         # cpu_addr → flag info
        self.tables: Dict[int, dict] = {}        # cpu_addr → table info (z-axis = data addr)
        self.table_axes: Dict[int, dict] = {}    # cpu_addr → axis info for x/y axes
        self.all_addrs: Dict[int, str] = {}      # cpu_addr → short label (any type)
        
        # Always load calibration entries as bank1 CPU addresses since
        # COMMON area ($2000-$7FFF) is visible from all banks.
        # Code in bank2/3 references these same CPU addresses.
        self._load(json_path, load_bank=1)
    
    def _load(self, json_path: str, load_bank: int = 1):
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        meta = data.get('metadata', {})
        self.definition_name = meta.get('source_definition', 'Unknown')
        self.bin_name = meta.get('source_file', 'Unknown')
        
        # Process scalars
        for s in data.get('scalars', []):
            addr_str = s.get('address')
            if not addr_str:
                continue
            xdf_addr = int(addr_str, 16)
            cpu_addr = xdf_addr_to_cpu(xdf_addr, load_bank)
            if cpu_addr is not None:
                self.scalars[cpu_addr] = s
                # Create short label — append if duplicate address
                title = s.get('title', '')
                val = s.get('value', '')
                unit = s.get('unit', '')
                entry = f"{title} = {val} {unit}".strip()
                if cpu_addr in self.all_addrs:
                    self.all_addrs[cpu_addr] += f" | {entry}"
                else:
                    self.all_addrs[cpu_addr] = entry
        
        # Process flags
        for f_entry in data.get('flags', []):
            addr_str = f_entry.get('address')
            if not addr_str:
                continue
            xdf_addr = int(addr_str, 16)
            cpu_addr = xdf_addr_to_cpu(xdf_addr, load_bank)
            if cpu_addr is not None:
                self.flags[cpu_addr] = f_entry
                title = f_entry.get('title', '')
                mask = f_entry.get('mask', '')
                is_set = f_entry.get('is_set', False)
                state = "SET" if is_set else "NOT SET"
                if cpu_addr not in self.all_addrs:
                    self.all_addrs[cpu_addr] = f"[FLAG] {title} mask={mask} ({state})"
                else:
                    # Address shared with a scalar — append flag info
                    self.all_addrs[cpu_addr] += f" | [FLAG] {title} ({state})"
        
        # Process tables (z-axis address = start of table data)
        for t in data.get('tables', []):
            axes = t.get('axes', {})
            z = axes.get('z', {})
            z_addr_str = z.get('address')
            if z_addr_str:
                xdf_addr = int(z_addr_str, 16)
                cpu_addr = xdf_addr_to_cpu(xdf_addr, load_bank)
                if cpu_addr is not None:
                    self.tables[cpu_addr] = t
                    dims = t.get('dimensions', {})
                    rows = dims.get('rows', 0)
                    cols = dims.get('cols', 0)
                    title = t.get('title', '')
                    if cpu_addr not in self.all_addrs:
                        self.all_addrs[cpu_addr] = f"[TABLE {rows}x{cols}] {title}"
                    
                    # Calculate table extent (for range-based marking)
                    # Table occupies cpu_addr to cpu_addr + (rows * cols) - 1
            
            # Also track x and y axis addresses if embedded
            for axis_id in ('x', 'y'):
                ax = axes.get(axis_id, {})
                ax_addr_str = ax.get('address')
                if ax_addr_str:
                    xdf_addr = int(ax_addr_str, 16)
                    cpu_addr = xdf_addr_to_cpu(xdf_addr, load_bank)
                    if cpu_addr is not None:
                        title = t.get('title', '')
                        ax_unit = ax.get('unit', '')
                        count = ax.get('count', 0)
                        self.table_axes[cpu_addr] = {
                            'table_title': title,
                            'axis': axis_id.upper(),
                            'unit': ax_unit,
                            'count': count
                        }
                        if cpu_addr not in self.all_addrs:
                            self.all_addrs[cpu_addr] = f"[{axis_id.upper()}-AXIS of {title}] {count} pts, {ax_unit}"
    
    def lookup(self, cpu_addr: int) -> Optional[str]:
        """Get the annotation string for a CPU address, or None."""
        return self.all_addrs.get(cpu_addr)
    
    def get_scalar(self, cpu_addr: int) -> Optional[dict]:
        return self.scalars.get(cpu_addr)
    
    def get_flag(self, cpu_addr: int) -> Optional[dict]:
        return self.flags.get(cpu_addr)
    
    def get_table(self, cpu_addr: int) -> Optional[dict]:
        return self.tables.get(cpu_addr)
    
    def stats(self) -> dict:
        return {
            'scalars': len(self.scalars),
            'flags': len(self.flags),
            'tables': len(self.tables),
            'table_axes': len(self.table_axes),
            'total_unique': len(self.all_addrs),
            'addr_range': (
                f"${min(self.all_addrs):04X}" if self.all_addrs else "N/A",
                f"${max(self.all_addrs):04X}" if self.all_addrs else "N/A"
            )
        }


# ─── ASM Format Detection ───────────────────────────────────────────────────

def detect_asm_format(first_lines: List[str]) -> str:
    """
    Detect which disassembler produced the ASM file.
    Returns: 'custom', 'udis', 'gnu', or 'unknown'
    """
    for line in first_lines[:50]:
        # Custom format: "L0000:  .byte   $FF, $FF"
        if re.match(r'^L[0-9A-Fa-f]{4}:', line):
            return 'custom'
        # Udis format: "0000  FF FF FF        stx    $FFFF"
        if re.match(r'^[0-9A-Fa-f]{4}\s+[0-9A-Fa-f]{2}\s', line):
            return 'udis'
        # GNU format: "       0: ff ff ff    stx ffff"
        if re.match(r'^\s+[0-9a-f]+:\s+[0-9a-f]{2}\s', line):
            return 'gnu'
    return 'unknown'


# ─── ASM Annotators ─────────────────────────────────────────────────────────

# Regex patterns for extracting addresses from HC11 instruction operands
# Custom format: "L9058:  1A B3 4D 91      cpd      $4d91"
RE_CUSTOM_LINE = re.compile(
    r'^(L([0-9A-Fa-f]{4}):)\s+'     # Label + address
    r'([0-9A-Fa-f]{2}(?:\s+[0-9A-Fa-f]{2})*)'  # Hex bytes
    r'\s+'
    r'(\S+)'                         # Mnemonic
    r'(?:\s+(.*))?$'                 # Operand (optional)
)

# Data region in custom format: "L752A:  .byte   $9F, $38, $A0, ..."
RE_CUSTOM_DATA = re.compile(
    r'^(L([0-9A-Fa-f]{4}):)\s+'     # Label + address
    r'\.byte\s+'                     # .byte directive
    r'(.+?)(?:\s*;.*)?$'            # Byte values, strip existing comments
)

# Udis format: "752A  9F 38            ldaa   $752B"
RE_UDIS_LINE = re.compile(
    r'^([0-9A-Fa-f]{4})\s+'         # Address
    r'([0-9A-Fa-f]{2}(?:\s+[0-9A-Fa-f]{2})*)'  # Hex bytes
    r'\s+'
    r'(\S+)'                         # Mnemonic
    r'(?:\s+(.*))?$'                 # Operand
)

# Match $XXXX address references in operands (common for extended addressing)
RE_ADDR_REF = re.compile(r'\$([0-9A-Fa-f]{4})\b')

# Match #$XX or #$XXXX immediate values (NOT address references)
RE_IMMEDIATE = re.compile(r'#\$[0-9A-Fa-f]+')

# Match hex addr references in operands like: "ldaa $4d8a", "cpd $4d91", "jsr $a07e"  
# BUT NOT: "bra $9055" (branch targets) or "#$FF" (immediates)
# We want extended addressing mode operands that reference calibration addresses
RE_EXTENDED_ADDR = re.compile(r'(?<!#)\$([0-9A-Fa-f]{4})\b')


def sanitize_label(title: str) -> str:
    """Convert XDF title to a valid ASM label (A-Z, 0-9, underscore)."""
    # Remove special characters, replace spaces with underscores
    label = re.sub(r'[^A-Za-z0-9_]', '_', title)
    # Collapse multiple underscores
    label = re.sub(r'_+', '_', label)
    # Trim
    label = label.strip('_')
    # Limit length
    if len(label) > 48:
        label = label[:48]
    return label


def annotate_custom_format(lines: List[str], labels: XDFLabelMap, bank: int = 1) -> Tuple[List[str], dict]:
    """
    Annotate ASM in the custom disassembler format.
    
    Two passes:
    1. DATA REGION ($2000-$7FFF): Add XDF name comments to .byte lines
    2. CODE REGION ($8000+): Add XDF xref comments to instruction operands
    
    Returns (annotated_lines, stats_dict)
    """
    output = []
    stats = defaultdict(int)
    
    for line in lines:
        stripped = line.rstrip()
        
        # --- Pass 1: Data region labels ---
        m_data = RE_CUSTOM_DATA.match(stripped)
        if m_data:
            label_part = m_data.group(1)
            addr = int(m_data.group(2), 16)
            byte_str = m_data.group(3)
            
            # Count bytes in this .byte line
            byte_count = len(re.findall(r'\$[0-9A-Fa-f]{2}', byte_str))
            if byte_count < 1:
                byte_count = 1
            
            # Check all addresses spanned by this .byte line
            span_annotations = []
            for offset in range(byte_count):
                check_addr = addr + offset
                ann = labels.lookup(check_addr)
                if ann:
                    if len(ann) > 55:
                        ann = ann[:52] + "..."
                    if offset == 0:
                        span_annotations.append(
                            f"${check_addr:04X}: {ann}"
                        )
                    else:
                        span_annotations.append(
                            f"+{offset}:${check_addr:04X}: {ann}"
                        )
            
            if span_annotations:
                combined = " | ".join(span_annotations)
                new_line = f"{stripped}  ; [XDF] {combined}"
                output.append(new_line)
                stats['data_labeled'] += 1
                continue
            
            # Also check if this address falls inside a known table's range
            # (table data spans multiple .byte lines)
            for table_addr, table_info in labels.tables.items():
                dims = table_info.get('dimensions', {})
                rows = dims.get('rows', 0)
                cols = dims.get('cols', 0)
                table_size = rows * cols
                if table_addr <= addr < table_addr + table_size and addr != table_addr:
                    title = table_info.get('title', '?')
                    offset = addr - table_addr
                    row = offset // cols if cols else 0
                    col = offset % cols if cols else 0
                    new_line = f"{stripped}  ; [XDF] ↳ {title} [row {row}]"
                    output.append(new_line)
                    stats['data_table_interior'] += 1
                    break
            else:
                output.append(stripped)
                stats['data_unlabeled'] += 1
            continue
        
        # --- Pass 2: Any line with an Lxxxx label ---
        m_code = RE_CUSTOM_LINE.match(stripped)
        if m_code:
            label_part = m_code.group(1)
            line_addr = int(m_code.group(2), 16)
            hex_bytes = m_code.group(3)
            mnemonic = m_code.group(4)
            operand = m_code.group(5) or ""
            
            # 2a: If THIS line's address is in the calibration range,
            # label it as calibration data (even though disassembler decoded it as code).
            # Multi-byte instructions consume adjacent addresses, so also check
            # XDF entries at line_addr+1, +2, etc. within the instruction span.
            if CAL_RANGE[0] <= line_addr < CAL_RANGE[1]:
                # Count instruction bytes to know the span
                byte_count = len(hex_bytes.split())
                
                # Collect all XDF annotations for addresses in this instruction's span
                span_annotations = []
                for offset in range(byte_count):
                    check_addr = line_addr + offset
                    ann = labels.lookup(check_addr)
                    if ann:
                        # Truncate individual titles but keep addr prefix
                        if offset == 0:
                            if len(ann) > 70:
                                ann = ann[:67] + "..."
                            span_annotations.append(
                                f"${check_addr:04X}: {ann}"
                            )
                        else:
                            if len(ann) > 55:
                                ann = ann[:52] + "..."
                            span_annotations.append(
                                f"+{offset}:${check_addr:04X}: {ann}"
                            )
                
                if span_annotations:
                    combined = " | ".join(span_annotations)
                    new_line = f"{stripped}  ; [XDF] {combined}"
                    output.append(new_line)
                    stats['cal_data_labeled'] += 1
                    if len(span_annotations) > 1:
                        stats['cal_multi_in_span'] += (
                            len(span_annotations) - 1
                        )
                    continue
                
                # Check if inside a table's range
                for table_addr, table_info in labels.tables.items():
                    dims = table_info.get('dimensions', {})
                    rows = dims.get('rows', 0)
                    cols = dims.get('cols', 0)
                    table_size = rows * cols
                    if table_addr <= line_addr < table_addr + table_size and line_addr != table_addr:
                        title = table_info.get('title', '?')
                        offset = line_addr - table_addr
                        row = offset // cols if cols else 0
                        new_line = f"{stripped}  ; [XDF] >> {title} [row {row}]"
                        output.append(new_line)
                        stats['cal_table_interior'] += 1
                        break
                else:
                    output.append(stripped)
                    stats['cal_no_match'] += 1
                continue
            
            # 2b: Code region — check operand references to cal addresses
            # Skip branches/jumps to code targets (they're not cal references)
            is_branch = mnemonic.lower() in (
                'bra', 'brn', 'bhi', 'bls', 'bcc', 'bcs', 'bne', 'beq',
                'bvc', 'bvs', 'bpl', 'bmi', 'bge', 'blt', 'bgt', 'ble',
                'jmp',  # jmp to code address
            )
            is_brclr_brset = mnemonic.lower() in ('brclr', 'brset')
            
            # Find $XXXX address references in the operand
            addr_refs = RE_EXTENDED_ADDR.findall(operand)
            
            xref_comments = []
            for ref_hex in addr_refs:
                ref_addr = int(ref_hex, 16)
                
                # For branch instructions, the target is code, not data
                if is_branch:
                    continue
                
                # For brclr/brset, the first $XXXX is a direct-page addr, interesting
                # but we still check if it's known
                
                annotation = labels.lookup(ref_addr)
                if annotation:
                    if len(annotation) > 70:
                        annotation = annotation[:67] + "..."
                    xref_comments.append(f"${ref_hex.upper()}: {annotation}")
                    stats['code_xref'] += 1
            
            if xref_comments:
                comment = " | ".join(xref_comments)
                new_line = f"{stripped}  ; [XDF] {comment}"
                output.append(new_line)
            else:
                output.append(stripped)
                stats['code_no_xref'] += 1
            continue
        
        # --- Non-matching lines (comments, .org, blank, etc.) ---
        output.append(stripped)
        stats['passthrough'] += 1
    
    return output, dict(stats)


def annotate_udis_format(lines: List[str], labels: XDFLabelMap, bank: int = 1) -> Tuple[List[str], dict]:
    """Annotate ASM in udis86 disassembler format."""
    output = []
    stats = defaultdict(int)
    
    for line in lines:
        stripped = line.rstrip()
        
        m = RE_UDIS_LINE.match(stripped)
        if m:
            addr = int(m.group(1), 16)
            hex_bytes = m.group(2)
            mnemonic = m.group(3)
            operand = m.group(4) or ""
            
            # Check if this address itself is a known calibration location
            annotation = labels.lookup(addr)
            if annotation and CAL_RANGE[0] <= addr < CAL_RANGE[1]:
                if len(annotation) > 80:
                    annotation = annotation[:77] + "..."
                new_line = f"{stripped}  ; [XDF] {annotation}"
                output.append(new_line)
                stats['data_labeled'] += 1
                continue
            
            # Check operand address references 
            addr_refs = RE_EXTENDED_ADDR.findall(operand)
            xref_comments = []
            for ref_hex in addr_refs:
                ref_addr = int(ref_hex, 16)
                ann = labels.lookup(ref_addr)
                if ann:
                    if len(ann) > 70:
                        ann = ann[:67] + "..."
                    xref_comments.append(f"${ref_hex.upper()}: {ann}")
                    stats['code_xref'] += 1
            
            if xref_comments:
                comment = " | ".join(xref_comments)
                new_line = f"{stripped}  ; [XDF] {comment}"
                output.append(new_line)
            else:
                output.append(stripped)
                stats['code_no_xref'] += 1
            continue
        
        output.append(stripped)
        stats['passthrough'] += 1
    
    return output, dict(stats)


# ─── Main ───────────────────────────────────────────────────────────────────

def print_usage():
    print("KingAI XDF → ASM Auto-Labeler")
    print()
    print("Usage:")
    print("  python xdf_asm_labeler.py <json_export> <input.asm> [output.asm] [options]")
    print()
    print("Arguments:")
    print("  json_export   JSON file from tunerpro_exporter.py (with addresses)")
    print("  input.asm     Disassembled ASM file to annotate")
    print("  output.asm    Output file (default: <input>_labeled.asm)")
    print()
    print("Options:")
    print("  --bank N      Bank number (1, 2, or 3). Default: auto-detect from filename")
    print("  --stats       Print statistics after labeling")
    print("  --summary     Print XDF summary (address ranges, counts)")
    print("  --dry-run     Don't write output, just show stats")
    print()
    print("Address Mapping:")
    print("  XDF address = file offset in 128KB binary (BASEOFFSET=0)")
    print("  Bank1: file[0x00000:0x10000] → CPU $0000-$FFFF")
    print("  Bank2: file[0x10000:0x18000] → CPU $8000-$FFFF")
    print("  Bank3: file[0x18000:0x20000] → CPU $8000-$FFFF")
    print("  Calibration data: XDF $4000-$7FFC → Bank1 CPU $4000-$7FFC")
    print()
    print("Examples:")
    print("  python xdf_asm_labeler.py Enhanced_v1.json Enhanced_v1.0a_bank1.asm --stats")
    print("  python xdf_asm_labeler.py Enhanced_v1.json bank1.asm bank1_labeled.asm")


def detect_bank_from_filename(filename: str) -> int:
    """Auto-detect bank number from filename."""
    name_lower = filename.lower()
    if 'bank3' in name_lower:
        return 3
    elif 'bank2' in name_lower:
        return 2
    return 1  # Default to bank1


def main():
    args = sys.argv[1:]
    
    if not args or '--help' in args or '-h' in args:
        print_usage()
        sys.exit(0)
    
    # Parse positional args
    positional = [a for a in args if not a.startswith('--')]
    flags = [a for a in args if a.startswith('--')]
    
    if len(positional) < 2:
        print("ERROR: Need at least <json_export> and <input.asm>")
        print_usage()
        sys.exit(1)
    
    json_path = positional[0]
    input_asm = positional[1]
    output_asm = positional[2] if len(positional) > 2 else None
    
    # Parse flags
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
    
    # Default output path
    if output_asm is None:
        base = Path(input_asm)
        output_asm = str(base.parent / f"{base.stem}_labeled{base.suffix}")
    
    # Validate inputs
    if not os.path.exists(json_path):
        print(f"ERROR: JSON file not found: {json_path}")
        sys.exit(1)
    if not os.path.exists(input_asm):
        print(f"ERROR: ASM file not found: {input_asm}")
        sys.exit(1)
    
    # Load XDF labels
    print(f"Loading XDF definitions from: {json_path}")
    labels = XDFLabelMap(json_path, bank=bank)
    
    label_stats = labels.stats()
    print(f"  XDF Definition: {labels.definition_name}")
    print(f"  Binary: {labels.bin_name}")
    print(f"  Loaded: {label_stats['scalars']} scalars, {label_stats['flags']} flags, "
          f"{label_stats['tables']} tables, {label_stats['table_axes']} axes")
    print(f"  Address range: {label_stats['addr_range'][0]} - {label_stats['addr_range'][1]}")
    print(f"  Total unique addresses: {label_stats['total_unique']}")
    
    if show_summary:
        print("\n--- XDF Summary ---")
        # Show some sample entries
        sorted_addrs = sorted(labels.all_addrs.items())
        for addr, desc in sorted_addrs[:20]:
            print(f"  ${addr:04X}: {desc}")
        if len(sorted_addrs) > 20:
            print(f"  ... and {len(sorted_addrs) - 20} more")
        print()
    
    # Read ASM
    print(f"Reading ASM: {input_asm}")
    with open(input_asm, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
    print(f"  {len(lines)} lines")
    
    # Detect format
    fmt = detect_asm_format(lines)
    print(f"  Detected format: {fmt}")
    
    # Annotate
    print(f"Annotating (bank {bank})...")
    if fmt == 'custom':
        annotated, stats = annotate_custom_format(lines, labels, bank)
    elif fmt == 'udis':
        annotated, stats = annotate_udis_format(lines, labels, bank)
    else:
        print(f"  WARNING: Unknown format '{fmt}', trying custom parser...")
        annotated, stats = annotate_custom_format(lines, labels, bank)
    
    # Stats
    total_annotated = (stats.get('data_labeled', 0) + stats.get('code_xref', 0) + 
                       stats.get('data_table_interior', 0) + stats.get('cal_data_labeled', 0) +
                       stats.get('cal_table_interior', 0))
    print(f"\n  Results:")
    print(f"    Cal data labels:        {stats.get('cal_data_labeled', 0)}")
    print(f"    Cal table interior:     {stats.get('cal_table_interior', 0)}")
    print(f"    .byte data labels:      {stats.get('data_labeled', 0)}")
    print(f"    .byte table interior:   {stats.get('data_table_interior', 0)}")
    print(f"    Code xrefs added:       {stats.get('code_xref', 0)}")
    print(f"    Cal range no match:     {stats.get('cal_no_match', 0)}")
    print(f"    Total annotations:      {total_annotated}")
    unchanged = stats.get('passthrough', 0) + stats.get('data_unlabeled', 0) + stats.get('code_no_xref', 0) + stats.get('cal_no_match', 0)
    print(f"    Lines unchanged:        {unchanged}")
    
    if show_stats:
        print(f"\n  Detailed stats: {json.dumps(stats, indent=4)}")
    
    # Write output
    if not dry_run:
        print(f"\nWriting: {output_asm}")
        with open(output_asm, 'w', encoding='utf-8') as f:
            # Add header
            f.write(f"; ============================================================================\n")
            f.write(f"; XDF-Labeled Disassembly\n")
            f.write(f"; Generated by: KingAI XDF ASM Auto-Labeler\n")
            f.write(f"; XDF Definition: {labels.definition_name}\n")
            f.write(f"; Binary File: {labels.bin_name}\n")
            f.write(f"; Bank: {bank}\n")
            f.write(f"; Source ASM: {Path(input_asm).name}\n")
            f.write(f"; Annotations: {total_annotated} ({stats.get('data_labeled', 0)} data + "
                    f"{stats.get('code_xref', 0)} xrefs + {stats.get('data_table_interior', 0)} table interior)\n")
            f.write(f"; ============================================================================\n")
            f.write(f";\n")
            
            for line in annotated:
                f.write(line + '\n')
        
        print(f"Done! {total_annotated} annotations added to {output_asm}")
    else:
        print("\n[DRY RUN] No output written.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
