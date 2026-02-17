#!/usr/bin/env python3
"""
Free Space Analyzer with Bank Crossover Comparison + Multi-Layer Validation

Analyzes all 3 VY V6 Enhanced bank-split binaries with multi-layer verification:
  1. Zero-byte scanning (basic free space detection)
  2. JSR/JMP/BSR reference scanning (eliminates false positives)
  3. XDF table overlap detection (catches zero-valued calibration data)
  4. Opcode boundary validation (confirms code termination at region edges)
  5. Multi-bank cross-comparison (detects banked overlay shadows)
  6. Tiered safety classification (Tier 1/2/3 with confidence scores)

Bank layout (128KB total, 68HC11 expanded mode):
  Bank 1: 64KB  file 0x00000-0x0FFFF  CPU $0000-$FFFF  (RAM + I/O + Cal + Code + Vectors)
  Bank 2: 32KB  file 0x10000-0x17FFF  CPU $8000-$FFFF  (Engine code overlay)
  Bank 3: 32KB  file 0x18000-0x1FFFF  CPU $8000-$FFFF  (Trans/diag overlay)

Banks 2 and 3 are swapped via PORTG/PORTC bit — only one is visible to the CPU
at a time. Free space at a given CPU address in bank 2 does NOT mean that
address is free in bank 3 (and vice versa). Code injected into the overlap
region only executes when that bank is active.

IMPORTANT: Enhanced binaries use 0x00 for free space (THE1's convention).
           Stock binaries use 0xFF (erased flash state).

Usage:
  python find_free_space_then_compare_crossovers.py --dir path/to/bin_splits_disasm/
  python find_free_space_then_compare_crossovers.py --dir path/ --xdf path/to/file.xdf
  python find_free_space_then_compare_crossovers.py --bank1 b1.bin --bank2 b2.bin --bank3 b3.bin
  python find_free_space_then_compare_crossovers.py --dir path/ --min-size 32 -o report.md
  python find_free_space_then_compare_crossovers.py --dir path/ --full-bin ../full.bin

Author: KingAI Projects
Date: November 19, 2025
Updated: February 16, 2026 — Multi-layer analysis with JSR scanning, XDF overlap,
         opcode boundary validation, multi-bank cross-comparison, and tier classification
"""

import argparse
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# ---------------------------------------------------------------------------
# HC11 Opcode Length Table (complete)
# ---------------------------------------------------------------------------
# Maps opcode byte -> instruction length in bytes (including opcode).
# Prebyte opcodes (0x18, 0x1A, 0xCD) add 1 to the length of the inner opcode.
# This is the authoritative source for walking instruction boundaries.

# fmt: off
HC11_OPCODE_LENGTHS: Dict[int, int] = {
    # Inherent (1 byte)
    0x00: 1,  # TEST (only in test mode, treat as NOP)
    0x01: 1,  # NOP
    0x02: 1,  # IDIV
    0x03: 1,  # FDIV
    0x04: 1,  # LSRD
    0x05: 1,  # ASLD/LSLD
    0x06: 1,  # TAP
    0x07: 1,  # TPA
    0x08: 1,  # INX
    0x09: 1,  # DEX
    0x0A: 1,  # CLV
    0x0B: 1,  # SEV
    0x0C: 1,  # CLC
    0x0D: 1,  # SEC
    0x0E: 1,  # CLI
    0x0F: 1,  # SEI
    0x10: 1,  # SBA
    0x11: 1,  # CBA
    # Bit manipulation — 0x12-0x1F have VARIABLE lengths
    0x12: 4,  # BRSET dir  (opcode, addr, mask, rel)
    0x13: 4,  # BRCLR dir  (opcode, addr, mask, rel)
    0x14: 3,  # BSET dir   (opcode, addr, mask)
    0x15: 3,  # BCLR dir   (opcode, addr, mask)
    0x16: 1,  # TAB
    0x17: 1,  # TBA
    0x18: 1,  # PREBYTE (Y-indexed page — handled specially)
    0x19: 1,  # DAA
    0x1A: 1,  # PREBYTE (0x1A page — handled specially)
    0x1B: 1,  # ABA
    0x1C: 3,  # BSET idx   (opcode, offset, mask)
    0x1D: 3,  # BCLR idx   (opcode, offset, mask)
    0x1E: 4,  # BRSET idx  (opcode, offset, mask, rel)
    0x1F: 4,  # BRCLR idx  (opcode, offset, mask, rel)
    # Branches and relatives (2 bytes: opcode + rel offset)
    0x20: 2,  # BRA
    0x21: 2,  # BRN
    0x22: 2,  # BHI
    0x23: 2,  # BLS
    0x24: 2,  # BCC/BHS
    0x25: 2,  # BCS/BLO
    0x26: 2,  # BNE
    0x27: 2,  # BEQ
    0x28: 2,  # BVC
    0x29: 2,  # BVS
    0x2A: 2,  # BPL
    0x2B: 2,  # BMI
    0x2C: 2,  # BGE
    0x2D: 2,  # BLT
    0x2E: 2,  # BGT
    0x2F: 2,  # BLE
    # Stack / inherent (1 byte)
    0x30: 1,  # TSX
    0x31: 1,  # INS
    0x32: 1,  # PULA
    0x33: 1,  # PULB
    0x34: 1,  # DES
    0x35: 1,  # TXS
    0x36: 1,  # PSHA
    0x37: 1,  # PSHB
    0x38: 1,  # PULX
    0x39: 1,  # RTS
    0x3A: 1,  # ABX
    0x3B: 1,  # RTI
    0x3C: 1,  # PSHX
    0x3D: 1,  # MUL
    0x3E: 1,  # WAI
    0x3F: 1,  # SWI
    # A-register operations (1 byte inherent)
    0x40: 1, 0x43: 1, 0x44: 1, 0x46: 1, 0x47: 1, 0x48: 1, 0x49: 1,
    0x4A: 1, 0x4C: 1, 0x4D: 1, 0x4F: 1,
    # B-register operations (1 byte inherent)
    0x50: 1, 0x53: 1, 0x54: 1, 0x56: 1, 0x57: 1, 0x58: 1, 0x59: 1,
    0x5A: 1, 0x5C: 1, 0x5D: 1, 0x5F: 1,
    # Indexed (X) — 2 bytes: opcode + offset
    0x60: 2, 0x63: 2, 0x64: 2, 0x66: 2, 0x67: 2, 0x68: 2, 0x69: 2,
    0x6A: 2, 0x6C: 2, 0x6D: 2, 0x6E: 2, 0x6F: 2,
    # Extended — 3 bytes: opcode + 16-bit address
    0x70: 3, 0x73: 3, 0x74: 3, 0x76: 3, 0x77: 3, 0x78: 3, 0x79: 3,
    0x7A: 3, 0x7C: 3, 0x7D: 3, 0x7E: 3, 0x7F: 3,
    # Immediate/direct/indexed/extended — A-register group
    0x80: 2, 0x81: 2, 0x82: 2, 0x83: 3, 0x84: 2, 0x85: 2, 0x86: 2, 0x87: 2,
    0x88: 2, 0x89: 2, 0x8A: 2, 0x8B: 2, 0x8C: 3, 0x8D: 2, 0x8E: 3, 0x8F: 2,
    0x90: 2, 0x91: 2, 0x92: 2, 0x93: 2, 0x94: 2, 0x95: 2, 0x96: 2, 0x97: 2,
    0x98: 2, 0x99: 2, 0x9A: 2, 0x9B: 2, 0x9C: 2, 0x9D: 2, 0x9E: 2, 0x9F: 2,
    0xA0: 2, 0xA1: 2, 0xA2: 2, 0xA3: 2, 0xA4: 2, 0xA5: 2, 0xA6: 2, 0xA7: 2,
    0xA8: 2, 0xA9: 2, 0xAA: 2, 0xAB: 2, 0xAC: 2, 0xAD: 2, 0xAE: 2, 0xAF: 2,
    0xB0: 3, 0xB1: 3, 0xB2: 3, 0xB3: 3, 0xB4: 3, 0xB5: 3, 0xB6: 3, 0xB7: 3,
    0xB8: 3, 0xB9: 3, 0xBA: 3, 0xBB: 3, 0xBC: 3, 0xBD: 3, 0xBE: 3, 0xBF: 3,
    # Immediate/direct/indexed/extended — B-register group
    0xC0: 2, 0xC1: 2, 0xC2: 2, 0xC3: 3, 0xC4: 2, 0xC5: 2, 0xC6: 2, 0xC7: 2,
    0xC8: 2, 0xC9: 2, 0xCA: 2, 0xCB: 2, 0xCC: 3, 0xCD: 1, 0xCE: 3, 0xCF: 2,
    0xD0: 2, 0xD1: 2, 0xD2: 2, 0xD3: 2, 0xD4: 2, 0xD5: 2, 0xD6: 2, 0xD7: 2,
    0xD8: 2, 0xD9: 2, 0xDA: 2, 0xDB: 2, 0xDC: 2, 0xDD: 2, 0xDE: 2, 0xDF: 2,
    0xE0: 2, 0xE1: 2, 0xE2: 2, 0xE3: 2, 0xE4: 2, 0xE5: 2, 0xE6: 2, 0xE7: 2,
    0xE8: 2, 0xE9: 2, 0xEA: 2, 0xEB: 2, 0xEC: 2, 0xED: 2, 0xEE: 2, 0xEF: 2,
    0xF0: 3, 0xF1: 3, 0xF2: 3, 0xF3: 3, 0xF4: 3, 0xF5: 3, 0xF6: 3, 0xF7: 3,
    0xF8: 3, 0xF9: 3, 0xFA: 3, 0xFB: 3, 0xFC: 3, 0xFD: 3, 0xFE: 3, 0xFF: 3,
}
# fmt: on

# Prebytes — the inner opcode adds its own length, but the total includes
# the prebyte itself.  Handled in get_instruction_length().
PREBYTES = {0x18, 0x1A, 0xCD}

# Opcodes that terminate a basic block (no fall-through)
TERMINATORS = {
    0x39,  # RTS
    0x3B,  # RTI
    0x3E,  # WAI
    0x3F,  # SWI
    0x7E,  # JMP extended
    0x6E,  # JMP indexed
    0x20,  # BRA  (unconditional branch)
}

# Function-end indicators (instruction at boundary confirms code ends here)
FUNCTION_END_OPCODES = {0x39, 0x3B, 0x7E, 0x20}  # RTS, RTI, JMP, BRA

# Branch mnemonics (for human-readable output)
BRANCH_MNEMONICS = {
    0x20: "BRA", 0x21: "BRN", 0x22: "BHI", 0x23: "BLS",
    0x24: "BCC", 0x25: "BCS", 0x26: "BNE", 0x27: "BEQ",
    0x28: "BVC", 0x29: "BVS", 0x2A: "BPL", 0x2B: "BMI",
    0x2C: "BGE", 0x2D: "BLT", 0x2E: "BGT", 0x2F: "BLE",
    0x8D: "BSR",
}


def get_instruction_length(data: bytes, offset: int) -> int:
    """Get the total byte length of the HC11 instruction at *offset*.
    Handles prebyte sequences (0x18, 0x1A, 0xCD) correctly."""
    if offset >= len(data):
        return 1
    op = data[offset]
    if op in PREBYTES and offset + 1 < len(data):
        inner = data[offset + 1]
        inner_len = HC11_OPCODE_LENGTHS.get(inner, 1)
        return 1 + inner_len  # prebyte + inner instruction
    return HC11_OPCODE_LENGTHS.get(op, 1)


# ---------------------------------------------------------------------------
# Bank definitions
# ---------------------------------------------------------------------------

BANK_DEFS = {
    "bank1": {
        "name": "Bank 1 (Base — always visible $0000-$7FFF, overlay $8000-$FFFF)",
        "file_base": 0x00000,
        "cpu_base": 0x0000,
        "size": 65536,
        "description": (
            "Full 64KB — RAM ($0000-$01FF), I/O regs ($1000-$103F), "
            "calibration ($4000-$7FFF), code ($8000-$FFBF), vectors ($FFC0-$FFFF). "
            "The lower half ($0000-$7FFF) is ALWAYS visible regardless of bank switching."
        ),
    },
    "bank2": {
        "name": "Bank 2 (Engine overlay)",
        "file_base": 0x10000,
        "cpu_base": 0x8000,
        "size": 32768,
        "description": (
            "32KB engine code overlay — mapped to CPU $8000-$FFFF "
            "when PORTG/PORTC selects this bank. Contains main engine "
            "control code (spark, fuel, idle, etc.)"
        ),
    },
    "bank3": {
        "name": "Bank 3 (Trans/diag overlay)",
        "file_base": 0x18000,
        "cpu_base": 0x8000,
        "size": 32768,
        "description": (
            "32KB trans/diagnostic overlay — mapped to CPU $8000-$FFFF "
            "when PORTG/PORTC selects this bank. Contains 4L60E transmission "
            "control and diagnostic routines."
        ),
    },
}

# Known regions in bank 1 (offsets relative to bank start = CPU addresses)
BANK1_KNOWN_REGIONS = [
    (0x0000, 0x01FF, "RAM (volatile at runtime)", "danger"),
    (0x0200, 0x0FFF, "External expansion / unused (0xFF fill)", "danger"),
    (0x1000, 0x103F, "I/O registers ($1000-$103F)", "danger"),
    (0x1040, 0x1FFF, "External expansion / unused", "danger"),
    (0x2000, 0x3FE1, "Pseudo-vector jump table + common code", "caution"),
    (0x3FE2, 0x3FFF, "pcmhacking.net string (safe to overwrite)", "free_verified"),
    (0x4000, 0x7FFF, "Calibration tables (XDF-defined region)", "caution"),
    (0x8000, 0xC467, "Bank 1 overlay code", "caution"),
    (0xC468, 0xFFBF, "Zero-filled area (bank 1 doesn't use this overlay region)", "free_verified"),
    (0xFFC0, 0xFFFF, "Interrupt/pseudo-vector table", "danger"),
]


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class FreeRegion:
    """A contiguous region of free (zero/FF) bytes in a single bank."""
    bank: str                       # "bank1", "bank2", "bank3"
    offset_start: int               # Offset within bank binary
    offset_end: int                 # Inclusive end offset
    size: int
    cpu_start: int                  # CPU address
    cpu_end: int                    # CPU address (inclusive)
    file_start: int                 # Offset in full 128KB binary
    file_end: int                   # File offset (inclusive)
    # Validation results (set by analysis passes)
    jsr_refs: int = 0               # JSR/JMP/BSR targets pointing into this region
    jsr_ref_details: List[str] = field(default_factory=list)
    xdf_overlaps: int = 0           # Number of XDF definitions overlapping
    xdf_overlap_details: List[str] = field(default_factory=list)
    boundary_before: str = ""       # Opcode at the byte before this region
    boundary_after: str = ""        # Opcode at the byte after this region
    clean_entry: bool = False       # True if code terminates cleanly before region
    clean_exit: bool = False        # True if valid code starts after region
    other_bank_nonzero: int = 0     # Count of non-zero bytes at same CPU addr in other banks
    other_bank_pct: float = 0.0     # % non-zero in other banks at same CPU range
    tier: int = 0                   # 1=safe, 2=conditional, 3=risky, 0=unclassified
    tier_label: str = ""
    confidence: float = 0.0         # 0.0-1.0 confidence score
    warnings: List[str] = field(default_factory=list)
    region_type: str = ""           # Human-readable classification


@dataclass
class XdfEntry:
    """A single XDF table/constant/flag definition."""
    title: str
    addr: int           # File offset address (as stored in XDF)
    size: int           # Bytes
    entry_type: str     # "TABLE", "CONSTANT", "FLAG"


@dataclass
class JsrReference:
    """A JSR/JMP/BSR instruction that references a target address."""
    source_bank: str
    source_cpu_addr: int
    target_cpu_addr: int
    instruction: str     # "JSR", "JMP", "BSR"


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def detect_free_byte(data: bytes) -> int:
    """Auto-detect whether free space uses 0x00 or 0xFF.
    Enhanced binaries use 0x00, stock flash uses 0xFF."""
    count_00 = data.count(b"\x00")
    count_ff = data.count(b"\xff")
    return 0x00 if count_00 > count_ff else 0xFF


def find_free_regions(
    data: bytes, free_byte: int, min_size: int, bank: str
) -> List[FreeRegion]:
    """Scan binary data for contiguous runs of *free_byte* >= *min_size*.
    Returns FreeRegion objects with bank-relative and absolute addresses."""
    bdef = BANK_DEFS[bank]
    regions: List[FreeRegion] = []
    in_free = False
    region_start = 0

    for i, b in enumerate(data):
        if b == free_byte:
            if not in_free:
                in_free = True
                region_start = i
        else:
            if in_free:
                size = i - region_start
                if size >= min_size:
                    regions.append(FreeRegion(
                        bank=bank,
                        offset_start=region_start,
                        offset_end=i - 1,
                        size=size,
                        cpu_start=region_start + bdef["cpu_base"],
                        cpu_end=(i - 1) + bdef["cpu_base"],
                        file_start=region_start + bdef["file_base"],
                        file_end=(i - 1) + bdef["file_base"],
                    ))
                in_free = False

    # Handle data ending in free bytes
    if in_free:
        size = len(data) - region_start
        if size >= min_size:
            regions.append(FreeRegion(
                bank=bank,
                offset_start=region_start,
                offset_end=len(data) - 1,
                size=size,
                cpu_start=region_start + bdef["cpu_base"],
                cpu_end=(len(data) - 1) + bdef["cpu_base"],
                file_start=region_start + bdef["file_base"],
                file_end=(len(data) - 1) + bdef["file_base"],
            ))

    return regions


# ---------------------------------------------------------------------------
# Pass 1: JSR/JMP/BSR reference scanning
# ---------------------------------------------------------------------------

def scan_jsr_jmp_references(data: bytes, bank: str) -> List[JsrReference]:
    """Walk the binary instruction-by-instruction and extract all JSR, JMP,
    and BSR targets.  Returns a list of JsrReference objects.

    Only extended-mode JSR ($BD), extended-mode JMP ($7E), and BSR ($8D)
    have statically-knowable targets. Indexed-mode calls ($AD, $6E) are
    noted but targets cannot be determined statically.
    """
    bdef = BANK_DEFS[bank]
    refs: List[JsrReference] = []
    i = 0

    while i < len(data) - 2:
        op = data[i]

        # Handle prebytes — skip the prebyte, process inner opcode
        if op in PREBYTES and i + 1 < len(data):
            inner = data[i + 1]
            inner_len = HC11_OPCODE_LENGTHS.get(inner, 1)
            i += 1 + inner_len
            continue

        # JSR extended ($BD xx xx) — primary call pattern
        if op == 0xBD and i + 2 < len(data):
            target = (data[i + 1] << 8) | data[i + 2]
            refs.append(JsrReference(
                source_bank=bank,
                source_cpu_addr=i + bdef["cpu_base"],
                target_cpu_addr=target,
                instruction="JSR",
            ))
            i += 3
            continue

        # JMP extended ($7E xx xx)
        if op == 0x7E and i + 2 < len(data):
            target = (data[i + 1] << 8) | data[i + 2]
            refs.append(JsrReference(
                source_bank=bank,
                source_cpu_addr=i + bdef["cpu_base"],
                target_cpu_addr=target,
                instruction="JMP",
            ))
            i += 3
            continue

        # BSR ($8D rel) — relative call
        if op == 0x8D and i + 1 < len(data):
            rel = data[i + 1]
            if rel > 127:
                rel -= 256
            target = (i + 2 + rel) + bdef["cpu_base"]
            target &= 0xFFFF  # Clamp to 16-bit
            refs.append(JsrReference(
                source_bank=bank,
                source_cpu_addr=i + bdef["cpu_base"],
                target_cpu_addr=target,
                instruction="BSR",
            ))
            i += 2
            continue

        # All other instructions — advance by opcode length
        length = HC11_OPCODE_LENGTHS.get(op, 1)
        i += length

    return refs


def build_reference_map(
    all_refs: List[JsrReference],
) -> Dict[int, List[JsrReference]]:
    """Build a map of target_cpu_addr -> list of references pointing there."""
    ref_map: Dict[int, List[JsrReference]] = defaultdict(list)
    for ref in all_refs:
        ref_map[ref.target_cpu_addr].append(ref)
    return ref_map


def check_references_into_region(
    region: FreeRegion,
    ref_map: Dict[int, List[JsrReference]],
) -> None:
    """Check if any JSR/JMP/BSR targets fall within the free region.
    Updates region.jsr_refs and region.jsr_ref_details in place."""
    count = 0
    details = []
    for cpu_addr in range(region.cpu_start, region.cpu_end + 1):
        if cpu_addr in ref_map:
            for ref in ref_map[cpu_addr]:
                count += 1
                details.append(
                    f"{ref.instruction} ${ref.target_cpu_addr:04X} "
                    f"(from {ref.source_bank} ${ref.source_cpu_addr:04X})"
                )
    region.jsr_refs = count
    region.jsr_ref_details = details[:20]  # Cap detail output


# ---------------------------------------------------------------------------
# Pass 2: XDF overlap detection
# ---------------------------------------------------------------------------

def parse_xdf_file(xdf_path: Path) -> List[XdfEntry]:
    """Parse a TunerPro XDF file and extract all table/constant/flag
    definitions with their file-offset addresses and sizes."""
    entries: List[XdfEntry] = []

    try:
        tree = ET.parse(xdf_path)
    except ET.ParseError as e:
        print(f"  WARNING: XDF parse error: {e}", file=sys.stderr)
        return entries

    root = tree.getroot()

    for elem in root.iter():
        if elem.tag not in ("XDFTABLE", "XDFCONSTANT", "XDFFLAG"):
            continue

        title = ""
        addr = None
        size_bits = 8  # Default 1 byte
        entry_type = elem.tag.replace("XDF", "").upper()

        title_elem = elem.find("title")
        if title_elem is not None and title_elem.text:
            title = title_elem.text

        # Get address and element size from EMBEDDEDDATA
        for emb in elem.iter("EMBEDDEDDATA"):
            addr_str = emb.get("mmedaddress", "")
            if addr_str:
                try:
                    addr = int(addr_str, 0)
                except ValueError:
                    pass
            sb = emb.get("mmedelementsizebits", "")
            if sb:
                try:
                    size_bits = int(sb)
                except ValueError:
                    pass

        # Compute total data size in bytes
        data_size = max(1, size_bits // 8)

        # For tables, try to get row * col * element_size
        if elem.tag == "XDFTABLE":
            rows, cols = 1, 1
            for axis in elem.findall(".//XDFAXIS"):
                axis_id = axis.get("id", "")
                count_elem = axis.find("indexcount")
                if count_elem is not None and count_elem.text:
                    try:
                        c = int(count_elem.text)
                    except ValueError:
                        c = 1
                    if axis_id == "x":
                        cols = c
                    elif axis_id == "y":
                        rows = c
            data_size = rows * cols * max(1, size_bits // 8)

        if addr is not None:
            entries.append(XdfEntry(
                title=title,
                addr=addr,
                size=data_size,
                entry_type=entry_type,
            ))

    return entries


def check_xdf_overlap(
    region: FreeRegion,
    xdf_entries: List[XdfEntry],
) -> None:
    """Check if any XDF definitions overlap with the free region.
    XDF addresses are file offsets in the 128KB binary.
    Updates region.xdf_overlaps and region.xdf_overlap_details in place."""
    count = 0
    details = []

    for xdf in xdf_entries:
        xdf_start = xdf.addr
        xdf_end = xdf.addr + xdf.size - 1

        # Check overlap: two ranges overlap if start_A <= end_B AND start_B <= end_A
        if xdf_start <= region.file_end and xdf_end >= region.file_start:
            count += 1
            details.append(
                f"{xdf.entry_type}: \"{xdf.title}\" at 0x{xdf.addr:05X} "
                f"({xdf.size} bytes)"
            )

    region.xdf_overlaps = count
    region.xdf_overlap_details = details[:15]


# ---------------------------------------------------------------------------
# Pass 3: Opcode boundary validation
# ---------------------------------------------------------------------------

def validate_boundaries(
    region: FreeRegion,
    data: bytes,
) -> None:
    """Check instruction boundaries immediately before and after the
    free region. A clean RTS/RTI/JMP/BRA before the region and valid
    opcodes after it increase confidence that this is truly free space.
    Updates region boundary fields in place."""
    bank_offset = region.offset_start

    # --- Before the region: walk forward from up to 24 bytes before ---
    if bank_offset > 0:
        scan_start = max(0, bank_offset - 24)
        pos = scan_start
        last_op = -1
        last_mnemonic = ""

        while pos < bank_offset:
            if pos >= len(data):
                break
            op = data[pos]
            length = get_instruction_length(data, pos)

            # Track the last complete instruction before the zero region
            if pos + length <= bank_offset:
                last_op = op
                if op in PREBYTES and pos + 1 < len(data):
                    last_op = data[pos + 1]

                if op == 0x39:
                    last_mnemonic = "RTS"
                elif op == 0x3B:
                    last_mnemonic = "RTI"
                elif op == 0x7E and pos + 2 < len(data):
                    target = (data[pos + 1] << 8) | data[pos + 2]
                    last_mnemonic = f"JMP ${target:04X}"
                elif op == 0x20 and pos + 1 < len(data):
                    rel = data[pos + 1]
                    if rel > 127:
                        rel -= 256
                    target = pos + 2 + rel + BANK_DEFS[region.bank]["cpu_base"]
                    last_mnemonic = f"BRA ${target & 0xFFFF:04X}"
                elif op == 0x14 and pos + 2 < len(data):
                    addr_byte = data[pos + 1]
                    mask = data[pos + 2]
                    last_mnemonic = f"BSET ${addr_byte:02X},#${mask:02X}"
                elif op == 0x15 and pos + 2 < len(data):
                    addr_byte = data[pos + 1]
                    mask = data[pos + 2]
                    last_mnemonic = f"BCLR ${addr_byte:02X},#${mask:02X}"
                elif op in BRANCH_MNEMONICS:
                    last_mnemonic = BRANCH_MNEMONICS[op]
                else:
                    last_mnemonic = f"opcode 0x{op:02X}"

            pos += length

        region.boundary_before = last_mnemonic
        region.clean_entry = last_op in FUNCTION_END_OPCODES

    # --- After the region: check if valid code resumes ---
    after_offset = region.offset_end + 1
    if after_offset < len(data):
        op = data[after_offset]

        if op in HC11_OPCODE_LENGTHS:
            if op == 0x7E and after_offset + 2 < len(data):
                target = (data[after_offset + 1] << 8) | data[after_offset + 2]
                region.boundary_after = f"JMP ${target:04X}"
            elif op == 0xBD and after_offset + 2 < len(data):
                target = (data[after_offset + 1] << 8) | data[after_offset + 2]
                region.boundary_after = f"JSR ${target:04X}"
            elif op == 0x20:
                region.boundary_after = "BRA ..."
            elif op in (0x39, 0x3B):
                region.boundary_after = "RTS" if op == 0x39 else "RTI"
            elif op == 0x00 and after_offset + 1 < len(data) and data[after_offset + 1] == 0x00:
                region.boundary_after = "0x00 (more zeros)"
                region.clean_exit = True
            else:
                region.boundary_after = f"opcode 0x{op:02X}"
            region.clean_exit = True
        else:
            region.boundary_after = f"INVALID opcode 0x{op:02X}"
            region.clean_exit = False
    else:
        region.boundary_after = "(end of bank)"
        region.clean_exit = True


# ---------------------------------------------------------------------------
# Pass 4: Multi-bank cross-comparison
# ---------------------------------------------------------------------------

def cross_compare_banks(
    region: FreeRegion,
    bank_data: Dict[str, bytes],
) -> None:
    """Check the same CPU address range in other banks to see if they
    contain code.  If the same CPU addresses have non-zero bytes in
    another bank, this 'free' region may be just bank-shadow.
    Updates region.other_bank_nonzero and region.other_bank_pct in place."""
    cpu_start = region.cpu_start
    cpu_end = region.cpu_end

    # Only meaningful for overlay region $8000-$FFFF
    if cpu_start < 0x8000:
        return

    total_other_bytes = 0
    total_nonzero = 0

    for other_bank in ("bank1", "bank2", "bank3"):
        if other_bank == region.bank:
            continue
        if other_bank not in bank_data:
            continue

        other_data = bank_data[other_bank]
        other_def = BANK_DEFS[other_bank]

        # Convert CPU address to offset in the other bank
        other_start = cpu_start - other_def["cpu_base"]
        other_end = cpu_end - other_def["cpu_base"]

        if other_start < 0 or other_end >= len(other_data):
            continue

        chunk = other_data[other_start:other_end + 1]
        nz = sum(1 for b in chunk if b != 0x00)
        total_other_bytes += len(chunk)
        total_nonzero += nz

    if total_other_bytes > 0:
        region.other_bank_nonzero = total_nonzero
        region.other_bank_pct = 100.0 * total_nonzero / total_other_bytes


# ---------------------------------------------------------------------------
# Pass 5: Tier classification
# ---------------------------------------------------------------------------

def classify_region(region: FreeRegion) -> None:
    """Assign a tier and confidence score based on all validation passes.

    Tier 1: CONFIRMED SAFE — always-visible area, no refs, no XDF overlap,
            clean boundaries.
    Tier 2: CONDITIONAL — banked overlay free space, usable in specific
            bank context only.
    Tier 3: RISKY — has references, XDF overlaps, or unclear boundaries.
    """
    warnings = []
    score = 1.0  # Start at maximum confidence

    cpu_s = region.cpu_start

    # --- Absolute no-go zones ---
    if 0xFFC0 <= cpu_s <= 0xFFFF:
        region.tier = 0
        region.tier_label = "VECTOR TABLE — DO NOT MODIFY"
        region.confidence = 0.0
        region.region_type = "Interrupt vector table"
        return
    if cpu_s < 0x2000:
        region.tier = 0
        region.tier_label = "RAM / I/O / RESERVED — NOT USABLE"
        region.confidence = 0.0
        region.region_type = "RAM or I/O register area"
        return

    # --- JSR/JMP references reduce confidence heavily ---
    if region.jsr_refs > 0:
        score -= 0.4
        warnings.append(
            f"{region.jsr_refs} JSR/JMP/BSR reference(s) target this region — "
            f"may contain code executed in another bank context"
        )

    # --- XDF overlaps are disqualifying for calibration area ---
    if region.xdf_overlaps > 0:
        score -= 0.5
        warnings.append(
            f"{region.xdf_overlaps} XDF definition(s) overlap — bytes are "
            f"zero-valued calibration data, NOT free space"
        )

    # --- Boundary quality ---
    if not region.clean_entry:
        score -= 0.1
        warnings.append(
            f"No clean code termination before region "
            f"(last opcode: {region.boundary_before or 'unknown'})"
        )
    if not region.clean_exit:
        score -= 0.1
        warnings.append(
            f"Invalid or missing opcode after region "
            f"(next: {region.boundary_after or 'unknown'})"
        )

    # --- Multi-bank shadow check ---
    if cpu_s >= 0x8000 and region.other_bank_pct > 50:
        score -= 0.2
        warnings.append(
            f"Same CPU addresses are {region.other_bank_pct:.0f}% non-zero "
            f"in other bank(s) — overlay shadow, not truly globally unused"
        )

    # --- Clamp score ---
    score = max(0.0, min(1.0, score))
    region.confidence = score
    region.warnings = warnings

    # ---- Classify by location ----

    # Always-visible area ($2000-$7FFF)
    if 0x2000 <= cpu_s < 0x8000:
        if score >= 0.8 and region.xdf_overlaps == 0 and region.jsr_refs == 0:
            region.tier = 1
            region.tier_label = "TIER 1: CONFIRMED SAFE (always visible)"
            region.region_type = _classify_always_visible(cpu_s)
        elif score >= 0.5:
            region.tier = 2
            region.tier_label = "TIER 2: CONDITIONAL (needs manual verification)"
            region.region_type = _classify_always_visible(cpu_s)
        else:
            region.tier = 3
            region.tier_label = "TIER 3: RISKY (likely zero-valued data, not free)"
            region.region_type = _classify_always_visible(cpu_s)
        return

    # Banked overlay area ($8000-$FFBF)
    if 0x8000 <= cpu_s < 0xFFC0:
        bank_label = BANK_DEFS[region.bank]["name"]
        if score >= 0.8 and region.jsr_refs == 0:
            region.tier = 2
            region.tier_label = (
                f"TIER 2: FREE IN {region.bank.upper()} CONTEXT ONLY"
            )
        elif score >= 0.4:
            region.tier = 2
            region.tier_label = (
                f"TIER 2: CONDITIONAL ({region.bank} overlay)"
            )
        else:
            region.tier = 3
            region.tier_label = "TIER 3: RISKY (referenced or shadowed)"
        region.region_type = f"{bank_label} overlay"
        return

    # Fallback
    region.tier = 3
    region.tier_label = "TIER 3: UNCLASSIFIED"
    region.region_type = "Unknown"


def _classify_always_visible(cpu_addr: int) -> str:
    """Sub-classify a region in the always-visible $2000-$7FFF area."""
    if 0x2000 <= cpu_addr < 0x4000:
        return "Common code / pseudo-vector area"
    if 0x4000 <= cpu_addr < 0x8000:
        return "Calibration table area"
    return "Unknown"


# ---------------------------------------------------------------------------
# Crossover analysis (bank 2 vs bank 3)
# ---------------------------------------------------------------------------

@dataclass
class OverlapSegment:
    """A contiguous segment of the shared $8000-$FFFF region with
    consistent free/used state across banks 2 and 3."""
    offset_start: int   # Offset within the 32KB overlay
    offset_end: int
    size: int
    cpu_start: int      # CPU address ($8000+offset)
    cpu_end: int
    state: str          # "both_free", "both_used", "b2_free_b3_used", "b2_used_b3_free"


def build_overlap_map(
    b2_data: bytes,
    b3_data: bytes,
    free_byte: int,
    min_size: int = 1,
) -> List[OverlapSegment]:
    """Compare banks 2 and 3 byte-by-byte across their shared $8000-$FFFF."""
    size = min(len(b2_data), len(b3_data))
    segments: List[OverlapSegment] = []
    prev_state: Optional[str] = None
    seg_start = 0

    for i in range(size):
        b2_free = b2_data[i] == free_byte
        b3_free = b3_data[i] == free_byte

        if b2_free and b3_free:
            state = "both_free"
        elif b2_free:
            state = "b2_free_b3_used"
        elif b3_free:
            state = "b2_used_b3_free"
        else:
            state = "both_used"

        if state != prev_state:
            if prev_state is not None:
                seg_size = i - seg_start
                if seg_size >= min_size:
                    segments.append(OverlapSegment(
                        offset_start=seg_start,
                        offset_end=i - 1,
                        size=seg_size,
                        cpu_start=seg_start + 0x8000,
                        cpu_end=(i - 1) + 0x8000,
                        state=prev_state,
                    ))
            seg_start = i
            prev_state = state

    # Final segment
    if prev_state is not None:
        seg_size = size - seg_start
        if seg_size >= min_size:
            segments.append(OverlapSegment(
                offset_start=seg_start,
                offset_end=size - 1,
                size=seg_size,
                cpu_start=seg_start + 0x8000,
                cpu_end=(size - 1) + 0x8000,
                state=prev_state,
            ))

    return segments


# ---------------------------------------------------------------------------
# Report generation (timestamped markdown with full provenance)
# ---------------------------------------------------------------------------

def generate_report(
    bank_files: Dict[str, Path],
    bank_data: Dict[str, bytes],
    all_regions: List[FreeRegion],
    free_byte: int,
    min_size: int,
    overlap_segments: List[OverlapSegment],
    xdf_path: Optional[Path],
    xdf_count: int,
    all_refs: List[JsrReference],
) -> str:
    """Build a comprehensive timestamped markdown report."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# VY V6 $060A Enhanced — Free Space Analysis Report",
        "",
        f"**Generated:** {now}  ",
        f"**Free byte:** `0x{free_byte:02X}` "
        f"({'Enhanced convention (0x00 = unused)' if free_byte == 0 else 'Stock/erased flash (0xFF = unused)'})  ",
        f"**Minimum region size:** {min_size} bytes  ",
        f"**XDF file:** {'`' + xdf_path.name + '`' if xdf_path else 'None (XDF validation skipped)'}  ",
        f"**XDF definitions loaded:** {xdf_count:,}  ",
        f"**JSR/JMP/BSR references scanned:** {len(all_refs):,}  ",
        "",
        "**Analysis passes applied (in order):**",
        "",
        "| Pass | Method | Purpose |",
        "|------|--------|---------|",
        "| 1 | Zero-byte scanning | Find candidate free regions (all-zero or all-0xFF runs) |",
        "| 2 | JSR/JMP/BSR ref scanning | Walk opcodes in all 3 banks, find all call/jump targets |",
        "| 3 | XDF overlap detection | Cross-check against TunerPro calibration definitions |",
        "| 4 | Opcode boundary validation | Confirm RTS/RTI/JMP/BRA before region edge |",
        "| 5 | Multi-bank cross-comparison | Check same CPU addresses across all banks |",
        "| 6 | Tier classification | Score each region 0.0-1.0 confidence, assign Tier 1/2/3 |",
        "",
        "**Source files:**",
    ]
    for key in ("bank1", "bank2", "bank3"):
        if key in bank_files:
            lines.append(
                f"- {BANK_DEFS[key]['name']}: `{bank_files[key].name}` "
                f"({len(bank_data[key]):,} bytes)"
            )
    lines.append("")

    # ---- Memory map reference ----
    lines.extend([
        "---",
        "",
        "## Memory Architecture",
        "",
        "```",
        "128KB Flash (M29W800DB), 68HC11F1 expanded mode:",
        "",
        "Full binary:  0x00000-0x1FFFF  (131,072 bytes)",
        "",
        "Bank 1 (64KB): File 0x00000-0x0FFFF  ->  CPU $0000-$FFFF",
        "  $0000-$01FF  RAM (512 bytes, volatile at runtime)",
        "  $1000-$103F  I/O registers (hardware mapped)",
        "  $2000-$3FFF  ALWAYS VISIBLE: Pseudo-vectors + common code",
        "  $4000-$7FFF  ALWAYS VISIBLE: Calibration tables (XDF-defined)",
        "  $8000-$C467  Bank 1 overlay code (bank-switched region)",
        "  $C468-$FFBF  Zero-filled (bank 1 doesn't use this overlay area)",
        "  $FFC0-$FFFF  Interrupt/pseudo-vector table",
        "",
        "Bank 2 (32KB): File 0x10000-0x17FFF  ->  CPU $8000-$FFFF  (engine overlay)",
        "Bank 3 (32KB): File 0x18000-0x1FFFF  ->  CPU $8000-$FFFF  (trans/diag overlay)",
        "",
        "PORTC bit 3 controls A16.  $0000-$7FFF always comes from bank 1.",
        "$8000-$FFFF is bank-switched: bank 1, 2, or 3 depending on PORTG state.",
        "Free space in one bank does NOT mean the same CPU address is free in another.",
        "```",
        "",
    ])

    # ---- Reference scanning summary ----
    lines.extend([
        "---",
        "",
        "## JSR/JMP/BSR Reference Map",
        "",
        "All 3 banks were disassembled instruction-by-instruction to extract every "
        "statically-knowable call/jump target. Indexed-mode calls (`JSR offset,X`) "
        "and computed jumps are NOT captured — they require runtime tracing.",
        "",
    ])
    ref_by_range = defaultdict(int)
    for ref in all_refs:
        t = ref.target_cpu_addr
        if t < 0x2000:
            ref_by_range["$0000-$1FFF (RAM/IO)"] += 1
        elif t < 0x4000:
            ref_by_range["$2000-$3FFF (common code)"] += 1
        elif t < 0x8000:
            ref_by_range["$4000-$7FFF (calibration)"] += 1
        elif t < 0xC000:
            ref_by_range["$8000-$BFFF (overlay low)"] += 1
        elif t < 0xFFC0:
            ref_by_range["$C000-$FFBF (overlay high)"] += 1
        else:
            ref_by_range["$FFC0-$FFFF (vectors)"] += 1

    lines.append("| Target Range | References | Notes |")
    lines.append("|-------------|-----------|-------|")
    for rng, count in sorted(ref_by_range.items()):
        note = ""
        if "overlay high" in rng:
            note = "Critical: these target bank2/3 code at $C000+"
        elif "common" in rng:
            note = "Always-visible common routines"
        elif "calibration" in rng:
            note = "Table lookups — not code entry points"
        lines.append(f"| {rng} | {count:,} | {note} |")
    lines.append("")

    # ---- Executive Summary (tier breakdown) ----
    tier1 = [r for r in all_regions if r.tier == 1]
    tier2 = [r for r in all_regions if r.tier == 2]
    tier3 = [r for r in all_regions if r.tier == 3]
    tier0 = [r for r in all_regions if r.tier == 0]

    total_t1 = sum(r.size for r in tier1)
    total_t2 = sum(r.size for r in tier2)
    total_t3 = sum(r.size for r in tier3)

    lines.extend([
        "---",
        "",
        "## Executive Summary",
        "",
        "| Tier | Regions | Total Bytes | Meaning |",
        "|------|---------|-------------|---------|",
        f"| **Tier 1** (SAFE) | {len(tier1)} | **{total_t1:,}** | "
        f"Always-visible, no refs, no XDF overlap, clean boundaries |",
        f"| **Tier 2** (CONDITIONAL) | {len(tier2)} | **{total_t2:,}** | "
        f"Bank-context dependent, or needs manual review |",
        f"| **Tier 3** (RISKY) | {len(tier3)} | **{total_t3:,}** | "
        f"Referenced, XDF overlap, or unclear — likely NOT free |",
        f"| *(excluded)* | {len(tier0)} | — | "
        f"Vector tables, RAM, I/O registers |",
        "",
        f"> **Bottom line:** ~{total_t1:,} bytes of truly safe free space "
        f"in the common/calibration area ($2000-$7FFF), plus ~{total_t2:,} bytes "
        f"in bank overlay regions that require bank-context awareness.",
        "",
    ])

    # ---- Tier 1 detail ----
    if tier1:
        lines.extend([
            "---",
            "",
            "## Tier 1: CONFIRMED SAFE — Always Visible ($2000-$7FFF)",
            "",
            "These regions are in the always-visible lower 32KB. No bank switching "
            "concerns. No XDF table overlap. No JSR/JMP/BSR references target them. "
            "Opcode boundaries confirm clean code termination.",
            "",
            "| # | CPU Address | File Offset | Size | Before | After | Region | Confidence |",
            "|---|-------------|-------------|------|--------|-------|--------|------------|",
        ])
        for idx, r in enumerate(tier1, 1):
            lines.append(
                f"| {idx} "
                f"| `${r.cpu_start:04X}`-`${r.cpu_end:04X}` "
                f"| `0x{r.file_start:05X}`-`0x{r.file_end:05X}` "
                f"| {r.size:,} B "
                f"| {r.boundary_before} "
                f"| {r.boundary_after} "
                f"| {r.region_type} "
                f"| {r.confidence:.0%} |"
            )
        lines.extend([
            "",
            f"**Total Tier 1: {total_t1:,} bytes** — safe for patches, "
            f"accessible from any bank context.",
            "",
            "> These are the only regions where you can guarantee "
            "> your code is always reachable regardless of which bank overlay "
            "> is currently active.",
            "",
        ])

    # ---- Tier 2 detail ----
    if tier2:
        lines.extend([
            "---",
            "",
            "## Tier 2: CONDITIONAL — Bank-Context Dependent",
            "",
            "These regions contain all-zero bytes within a specific bank overlay. "
            "The same CPU addresses may contain active code in other banks. "
            "Code placed here is ONLY visible/executable when that specific bank "
            "is paged in by the bank switching hardware.",
            "",
            "| # | Bank | CPU Address | File Offset | Size | "
            "JSR Refs | Other Banks NZ% | Before | After | Confidence |",
            "|---|------|-------------|-------------|------|-"
            "---------|----------------|--------|-------|------------|",
        ])
        for idx, r in enumerate(tier2, 1):
            lines.append(
                f"| {idx} "
                f"| {r.bank} "
                f"| `${r.cpu_start:04X}`-`${r.cpu_end:04X}` "
                f"| `0x{r.file_start:05X}`-`0x{r.file_end:05X}` "
                f"| {r.size:,} B "
                f"| {r.jsr_refs} "
                f"| {r.other_bank_pct:.0f}% "
                f"| {r.boundary_before} "
                f"| {r.boundary_after} "
                f"| {r.confidence:.0%} |"
            )
        lines.append("")

        # Print warnings for any region with them
        warned = [r for r in tier2 if r.warnings]
        if warned:
            lines.append("**Warnings:**")
            lines.append("")
            for r in warned:
                for w in r.warnings:
                    lines.append(
                        f"- `${r.cpu_start:04X}`-`${r.cpu_end:04X}` "
                        f"({r.bank}): {w}"
                    )
            lines.append("")

        lines.extend([
            f"**Total Tier 2: {total_t2:,} bytes** — usable with bank-context awareness.",
            "",
            "**Rules for Tier 2 usage:**",
            "",
            "| Hook Location | Valid Patch Locations |",
            "|---------------|---------------------|",
            "| $2000-$7FFF (always visible) | Tier 1 regions — safest |",
            "| $8000-$C467 (bank 1 overlay) | Tier 2 bank1 ($C468-$FFBF) |",
            "| $8000-$9B0A (bank 3 overlay) | Tier 2 bank3 free regions |",
            "",
            "Hook and patch **must be visible in the SAME bank context**.",
            "",
        ])

    # ---- Tier 3 detail ----
    if tier3:
        lines.extend([
            "---",
            "",
            "## Tier 3: RISKY — Likely NOT Free Space",
            "",
            "These regions contain all-zero bytes but have disqualifying factors. "
            "The zeros are probably **zero-valued calibration data** or "
            "**bank-shadowed code regions**, not genuinely unused space.",
            "",
            "| # | Bank | CPU Address | Size | XDF Overlaps | JSR Refs | Reason |",
            "|---|------|-------------|------|-------------|----------|--------|",
        ])
        for idx, r in enumerate(tier3, 1):
            reason = "; ".join(r.warnings[:2]) if r.warnings else "Unverified"
            lines.append(
                f"| {idx} "
                f"| {r.bank} "
                f"| `${r.cpu_start:04X}`-`${r.cpu_end:04X}` "
                f"| {r.size:,} B "
                f"| {r.xdf_overlaps} "
                f"| {r.jsr_refs} "
                f"| {reason} |"
            )
        lines.append("")

        # Show XDF overlap details for tier 3
        xdf_warned = [r for r in tier3 if r.xdf_overlap_details]
        if xdf_warned:
            lines.append("**XDF overlap details (why these zeros are NOT free):**")
            lines.append("")
            for r in xdf_warned:
                lines.append(
                    f"- `${r.cpu_start:04X}`-`${r.cpu_end:04X}` ({r.size} bytes):"
                )
                for d in r.xdf_overlap_details[:5]:
                    lines.append(f"  - {d}")
            lines.append("")

        lines.extend([
            f"**Total Tier 3: {total_t3:,} bytes** — do NOT use without manual verification.",
            "",
        ])

    # ---- Crossover analysis (banks 2 vs 3) ----
    if overlap_segments:
        lines.extend([
            "---",
            "",
            "## Bank 2 vs Bank 3 — Overlay Crossover Analysis",
            "",
            "Banks 2 and 3 both map to CPU `$8000`-`$FFFF`. This byte-by-byte "
            "comparison shows what's truly free in both overlays simultaneously "
            "vs occupied in one or both.",
            "",
        ])

        both_free_total = sum(s.size for s in overlap_segments if s.state == "both_free")
        both_used_total = sum(s.size for s in overlap_segments if s.state == "both_used")
        b2f_b3u = sum(s.size for s in overlap_segments if s.state == "b2_free_b3_used")
        b2u_b3f = sum(s.size for s in overlap_segments if s.state == "b2_used_b3_free")

        lines.extend([
            "### Summary",
            "",
            "| State | Bytes | % of 32KB | Meaning |",
            "|-------|-------|-----------|---------|",
            f"| Both free | {both_free_total:,} | {100 * both_free_total / 32768:.1f}% "
            f"| Unused in BOTH overlays — safest for overlay injection |",
            f"| Both used | {both_used_total:,} | {100 * both_used_total / 32768:.1f}% "
            f"| Active code/data in BOTH — do not touch |",
            f"| Bank 2 free, Bank 3 used | {b2f_b3u:,} | {100 * b2f_b3u / 32768:.1f}% "
            f"| Free only when engine overlay is active |",
            f"| Bank 2 used, Bank 3 free | {b2u_b3f:,} | {100 * b2u_b3f / 32768:.1f}% "
            f"| Free only when trans/diag overlay is active |",
            "",
        ])

        # Detail table (significant segments)
        sig_segs = [s for s in overlap_segments if s.size >= min_size]
        if sig_segs:
            state_labels = {
                "both_free": ("FREE", "FREE", "SAFE — usable in either overlay"),
                "both_used": ("USED", "USED", "OCCUPIED — do not modify"),
                "b2_free_b3_used": ("FREE", "USED", "Free only in engine overlay"),
                "b2_used_b3_free": ("USED", "FREE", "Free only in trans/diag overlay"),
            }
            lines.extend([
                "### Detail (segments >= minimum size)",
                "",
                "| CPU Address | Size | Bank 2 | Bank 3 | Verdict |",
                "|-------------|------|--------|--------|---------|",
            ])
            for seg in sig_segs:
                b2l, b3l, verdict = state_labels[seg.state]
                lines.append(
                    f"| `${seg.cpu_start:04X}`-`${seg.cpu_end:04X}` "
                    f"| {seg.size:,} B | {b2l} | {b3l} | {verdict} |"
                )
            lines.append("")

    # ---- Practical guide ----
    lines.extend([
        "---",
        "",
        "## Patch Placement Guide",
        "",
        "### Priority order for compiled C code injection:",
        "",
    ])

    # Tier 1 largest
    if tier1:
        largest_t1 = max(tier1, key=lambda r: r.size)
        lines.extend([
            f"1. **Tier 1 free space** (e.g., `${largest_t1.cpu_start:04X}`-"
            f"`${largest_t1.cpu_end:04X}`, {largest_t1.size:,} bytes)",
            f"   - Always accessible, no bank switching concerns",
            f"   - Limited to {total_t1:,} bytes total across {len(tier1)} regions",
            "",
        ])

    # Bank1 overlay
    b1_overlay = [r for r in tier2 if r.bank == "bank1" and r.cpu_start >= 0xC000]
    if b1_overlay:
        largest_b1 = max(b1_overlay, key=lambda r: r.size)
        lines.extend([
            f"2. **Bank 1 overlay** (`${largest_b1.cpu_start:04X}`+, "
            f"{largest_b1.size:,} bytes)",
            f"   - Large contiguous block — ideal ORG target for compiled C",
            f"   - Only accessible when bank 1 overlay is active at $8000+",
            f"   - Hook point must be in $2000-$7FFF or bank 1 overlay code",
            "",
        ])

    # Bank3 free
    b3_free = [r for r in tier2 if r.bank == "bank3"]
    if b3_free:
        largest_b3 = max(b3_free, key=lambda r: r.size)
        lines.extend([
            f"3. **Bank 3 free space** (`${largest_b3.cpu_start:04X}`+, "
            f"{largest_b3.size:,} bytes)",
            f"   - Bank 3 has substantial free space (trans/diag is sparse)",
            f"   - Only accessible when bank 3 overlay is paged in",
            "",
        ])

    lines.extend([
        "### Address notation standard:",
        "",
        "| Context | Format | Example | Meaning |",
        "|---------|--------|---------|---------|",
        "| CPU address | `$xxxx` | `$C468` | Where the HC11 sees data at runtime (16-bit) |",
        "| File offset | `0xnnnnn` | `0x0C468` | Position in the 128KB binary file (17-bit) |",
        "| ORG directive | `ORG $xxxx` | `ORG $C468` | Assembly origin (must be 16-bit) |",
        "",
        "**WRONG:** `$0C468` (5 hex digits), `$14468` — HC11 has 16-bit addresses only.",
        "",
        "### Compiler workflow:",
        "",
        "```",
        "1. Write C code targeting a free region        -> examples/*.c",
        "2. Compile to HC11 assembly                    -> hc11cc.py",
        "3. Assemble to binary                          -> hc11kit.py",
        "4. Validate disassembly of compiled output     -> this tool + disassembler",
        "5. Flash to ECU via ALDL                       -> OSE Flash Tool",
        "```",
        "",
        "---",
        "",
        f"*Report generated by `find_free_space_then_compare_crossovers.py` at {now}*",
    ])

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Multi-layer free space analyzer for VY V6 Enhanced bank-split "
            "binaries. Scans for free regions, validates with JSR/JMP scanning, "
            "XDF overlap detection, opcode boundary checking, and multi-bank "
            "cross-comparison. Outputs a timestamped markdown report."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s --dir path/to/bin_splits_disasm/\n"
            "  %(prog)s --dir path/ --xdf path/to/Enhanced_v2.09b.xdf\n"
            "  %(prog)s --bank1 b1.bin --bank2 b2.bin --bank3 b3.bin\n"
            "  %(prog)s --dir path/ --min-size 64 -o report.md\n"
        ),
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--dir", type=Path,
        help="Directory containing Enhanced_v1.0a_bank{1,2,3}.bin files",
    )
    group.add_argument(
        "--bank1", type=Path,
        help="Path to bank 1 binary (64KB)",
    )

    parser.add_argument("--bank2", type=Path, help="Path to bank 2 binary (32KB)")
    parser.add_argument("--bank3", type=Path, help="Path to bank 3 binary (32KB)")
    parser.add_argument(
        "--xdf", type=Path, default=None,
        help="XDF definition file for overlap detection. If omitted, "
             "auto-searches sibling directories.",
    )
    parser.add_argument(
        "--min-size", type=int, default=32,
        help="Minimum free region size in bytes (default: 32)",
    )
    parser.add_argument(
        "--free-byte", type=lambda x: int(x, 0), default=None,
        help="Byte value for free space: 0x00 (Enhanced) or 0xFF (stock). "
             "Default: auto-detect from bank 1.",
    )
    parser.add_argument(
        "--output", "-o", type=Path,
        help="Output markdown report path (default: free_space_report.md next to bins)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Print detailed per-region progress to stderr",
    )

    args = parser.parse_args()

    def log(msg: str) -> None:
        if args.verbose:
            print(f"  [V] {msg}", file=sys.stderr)

    print("=" * 72)
    print("  VY V6 Free Space Analyzer — Multi-Layer Validation")
    print("=" * 72)

    # ---- Resolve file paths ----
    bank_files: Dict[str, Path] = {}

    if args.dir:
        d = args.dir
        for key in ("bank1", "bank2", "bank3"):
            exact = d / f"Enhanced_v1.0a_{key}.bin"
            if exact.exists():
                bank_files[key] = exact
            else:
                matches = list(d.glob(f"*{key}*.bin"))
                if matches:
                    bank_files[key] = matches[0]
    else:
        if args.bank1:
            bank_files["bank1"] = args.bank1
        if args.bank2:
            bank_files["bank2"] = args.bank2
        if args.bank3:
            bank_files["bank3"] = args.bank3

        # Auto-detect from cwd if nothing specified
        if not bank_files:
            cwd = Path(".")
            for key in ("bank1", "bank2", "bank3"):
                matches = list(cwd.glob(f"*{key}*.bin"))
                if matches:
                    bank_files[key] = matches[0]

    if not bank_files:
        print(
            "ERROR: No bank binaries found.\n"
            "Specify --dir <folder> or --bank1/--bank2/--bank3 <file>.",
            file=sys.stderr,
        )
        return 1

    # ---- Load and validate banks ----
    bank_data: Dict[str, bytes] = {}
    for key, path in sorted(bank_files.items()):
        if not path.exists():
            print(f"ERROR: File not found: {path}", file=sys.stderr)
            return 1
        data = path.read_bytes()
        expected = BANK_DEFS[key]["size"]
        if len(data) != expected:
            print(
                f"  WARNING: {path.name} is {len(data):,} bytes, "
                f"expected {expected:,}",
                file=sys.stderr,
            )
        bank_data[key] = data
        print(f"  Loaded {key}: {path.name} ({len(data):,} bytes)")

    # ---- Detect free byte ----
    if args.free_byte is not None:
        free_byte = args.free_byte
    else:
        ref_key = "bank1" if "bank1" in bank_data else sorted(bank_data.keys())[0]
        free_byte = detect_free_byte(bank_data[ref_key])
    print(f"  Free byte: 0x{free_byte:02X} "
          f"({'Enhanced' if free_byte == 0 else 'Stock'})")

    # ---- Find XDF file ----
    xdf_path = args.xdf
    if xdf_path is None:
        # Auto-search: parent dir, sibling dirs
        search_dirs = set()
        for p in bank_files.values():
            search_dirs.add(p.parent)
            search_dirs.add(p.parent.parent)
        for sd in search_dirs:
            xdf_matches = list(sd.glob("*.xdf"))
            if xdf_matches:
                xdf_path = xdf_matches[0]
                break

    xdf_entries: List[XdfEntry] = []
    if xdf_path and xdf_path.exists():
        print(f"  Loading XDF: {xdf_path.name}")
        xdf_entries = parse_xdf_file(xdf_path)
        print(f"  XDF definitions loaded: {len(xdf_entries):,} "
              f"(tables/constants/flags)")
    else:
        print("  No XDF file found — XDF overlap check will be skipped")

    # ---- Pass 1: Find zero regions per bank ----
    print(f"\n  Pass 1/6: Scanning for zero regions (min {min_size} bytes)...")
    all_regions: List[FreeRegion] = []
    for key in sorted(bank_data.keys()):
        regions = find_free_regions(bank_data[key], free_byte, args.min_size, key)
        total = sum(r.size for r in regions)
        print(f"    {BANK_DEFS[key]['name']}: "
              f"{len(regions)} candidate regions, {total:,} bytes")
        all_regions.extend(regions)

    # ---- Pass 2: JSR/JMP/BSR reference scanning ----
    print("\n  Pass 2/6: Scanning JSR/JMP/BSR references across all banks...")
    all_refs: List[JsrReference] = []
    for key in sorted(bank_data.keys()):
        refs = scan_jsr_jmp_references(bank_data[key], key)
        print(f"    {key}: {len(refs):,} call/jump references extracted")
        all_refs.extend(refs)

    ref_map = build_reference_map(all_refs)
    print(f"    Total unique target addresses: {len(ref_map):,}")

    for region in all_regions:
        check_references_into_region(region, ref_map)
        if region.jsr_refs > 0:
            log(f"${region.cpu_start:04X}-${region.cpu_end:04X} ({region.bank}): "
                f"{region.jsr_refs} refs INTO this zero region")

    refs_into_zeros = sum(1 for r in all_regions if r.jsr_refs > 0)
    print(f"    Regions with incoming references: {refs_into_zeros}")

    # ---- Pass 3: XDF overlap detection ----
    if xdf_entries:
        print(f"\n  Pass 3/6: Checking {len(xdf_entries):,} XDF definitions for overlap...")
        for region in all_regions:
            check_xdf_overlap(region, xdf_entries)
            if region.xdf_overlaps > 0:
                log(f"${region.cpu_start:04X}-${region.cpu_end:04X} ({region.bank}): "
                    f"{region.xdf_overlaps} XDF overlap(s)")

        xdf_hits = sum(1 for r in all_regions if r.xdf_overlaps > 0)
        print(f"    Regions with XDF overlap: {xdf_hits}")
    else:
        print("\n  Pass 3/6: Skipped (no XDF file)")

    # ---- Pass 4: Opcode boundary validation ----
    print("\n  Pass 4/6: Validating opcode boundaries at region edges...")
    for region in all_regions:
        validate_boundaries(region, bank_data[region.bank])

    clean_entries = sum(1 for r in all_regions if r.clean_entry)
    print(f"    Regions with clean code termination before: {clean_entries}/{len(all_regions)}")

    # ---- Pass 5: Multi-bank cross-comparison ----
    print("\n  Pass 5/6: Cross-comparing banks at shared CPU addresses...")
    for region in all_regions:
        cross_compare_banks(region, bank_data)

    shadowed = sum(1 for r in all_regions if r.other_bank_pct > 50)
    print(f"    Regions with >50% non-zero in other banks (overlay shadows): {shadowed}")

    # ---- Pass 6: Tier classification ----
    print("\n  Pass 6/6: Classifying all regions...")
    for region in all_regions:
        classify_region(region)

    tier_counts = defaultdict(int)
    tier_bytes = defaultdict(int)
    for r in all_regions:
        tier_counts[r.tier] += 1
        tier_bytes[r.tier] += r.size

    for t in sorted(tier_counts.keys()):
        if t > 0:
            labels = {1: "SAFE", 2: "CONDITIONAL", 3: "RISKY"}
            print(f"    Tier {t} ({labels.get(t, '?')}): "
                  f"{tier_counts[t]} regions, {tier_bytes[t]:,} bytes")

    # ---- Crossover analysis ----
    overlap_segments: List[OverlapSegment] = []
    if "bank2" in bank_data and "bank3" in bank_data:
        print("\n  Overlay crossover: Comparing bank 2 vs bank 3...")
        overlap_segments = build_overlap_map(
            bank_data["bank2"], bank_data["bank3"], free_byte, min_size=1,
        )
        both_free = sum(s.size for s in overlap_segments if s.state == "both_free")
        both_used = sum(s.size for s in overlap_segments if s.state == "both_used")
        mixed = 32768 - both_free - both_used
        print(f"    Both free: {both_free:,} B | "
              f"Both used: {both_used:,} B | Mixed: {mixed:,} B")

    # ---- Generate and write report ----
    report = generate_report(
        bank_files, bank_data, all_regions,
        free_byte, args.min_size, overlap_segments,
        xdf_path, len(xdf_entries), all_refs,
    )

    if args.output:
        out_path = args.output
    elif args.dir:
        out_path = args.dir / "free_space_report.md"
    elif "bank1" in bank_files:
        out_path = bank_files["bank1"].parent / "free_space_report.md"
    else:
        out_path = Path("free_space_report.md")

    out_path.write_text(report, encoding="utf-8")

    # ---- Final console summary ----
    print("\n" + "=" * 72)
    t1 = [r for r in all_regions if r.tier == 1]
    t2 = [r for r in all_regions if r.tier == 2]
    t3 = [r for r in all_regions if r.tier == 3]
    print(f"  TIER 1 (SAFE):        {len(t1):>3} regions  {sum(r.size for r in t1):>8,} bytes")
    print(f"  TIER 2 (CONDITIONAL): {len(t2):>3} regions  {sum(r.size for r in t2):>8,} bytes")
    print(f"  TIER 3 (RISKY):       {len(t3):>3} regions  {sum(r.size for r in t3):>8,} bytes")
    print(f"\n  Report saved: {out_path}")
    print("=" * 72)

    return 0


if __name__ == "__main__":
    sys.exit(main())
