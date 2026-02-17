#!/usr/bin/env python3
"""
ULTIMATE ECU BINARY ANALYZER & COMPARATOR v2.0
===============================================
Comprehensive tool combining all binary analysis capabilities for HC11 ECUs.

FEATURES:
- Binary comparison (byte-level diff with context)
- HC11 disassembly with XDF annotation (PAGE2/PAGE3 prefix support)
- Pattern detection and signature matching
- VS/VT/VY/VX platform-specific offset handling
- Duplicate/near-match finding
- ECU type identification (size + signature + vector analysis)
- XDF cross-referencing with EMBEDDEDDATA axis extraction
- Free space detection (0xFF, 0x00, LPG zeroed areas)
- Patch analysis and comparison
- Export to JSON/CSV/Markdown
- Auto-detect platform from binary size and vectors

PLATFORM OFFSET HANDLING:
- VS V6: 32KB Memcal, $8000-$FFFF (XDF address = file offset + $8000)
- VT V6: 32KB Memcal, $8000-$FFFF (same as VS)
- VX V6: 128KB Flash, $0000-$1FFFF (XDF address = file offset direct)
- VY V6: 128KB Flash, $0000-$1FFFF (same as VX)
- The1 Enhanced: 128KB, various calibration sets

HC11 MEMORY NOTES:
- $0000-$00FF: Direct page RAM (8-bit addressing)
- $0100-$01FF: Extended RAM (16-bit addressing)
- $1000-$103F: Hardware registers (PORTA, PORTB, timers, etc.)
- $8000-$BFFF: Banked ROM (Page 0-3 via $103D INIT register)
- $C000-$FFFF: Fixed ROM (always visible)
- $FFD6-$FFFF: Interrupt vectors (14 vectors × 2 bytes)

Sources combined from:
- compare_bin_files_ULTIMATE.py, compare_bin_files_advanced.py
- hc11_disassembler.py, binary_differ.py, xdf_full_parser.py
- vy_v6_constants.py, hc11_opcodes_complete.py
- tunerpro_exporter.py (axis extraction, BASEOFFSET handling)

Author: Jason King (KingAI Automotive Reverse Engineering)
GitHub: https://github.com/KingAiCodeForge
Date: January 19, 2026
License: MIT
"""

import os
import sys
import hashlib
import json
import csv
import struct
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Set, Any, Union
from dataclasses import dataclass, field
from enum import Enum

# ============================================================================
# PLATFORM DEFINITIONS - VS/VT/VY/VX OFFSET HANDLING
# ============================================================================

class HoldenPlatform(Enum):
    """Holden V6 ECU platform types with memory characteristics"""
    UNKNOWN = "unknown"
    VS_V6 = "vs_v6"        # 32KB Memcal EPROM
    VT_V6 = "vt_v6"        # 32KB Memcal EPROM  
    VX_V6 = "vx_v6"        # 128KB Flash
    VY_V6 = "vy_v6"        # 128KB Flash
    VZ_V6 = "vz_v6"        # 128KB Flash (later)
    VL_V8 = "vl_v8"        # Walkinshaw V8 (reference)

@dataclass
class PlatformConfig:
    """Platform-specific memory layout and offsets"""
    name: str
    binary_size: int  # Expected binary size in bytes
    xdf_base_offset: int  # XDF address = file_offset + this
    cal_start: int  # Calibration data start (file offset)
    cal_end: int  # Calibration data end (file offset)
    rom_start: int  # ROM code start (file offset)
    rom_end: int  # ROM code end (file offset)
    vector_table_offset: int  # Interrupt vectors (file offset)
    reset_vector_offset: int  # Reset vector location
    lpg_area_start: Optional[int] = None  # LPG tables (Enhanced ROMs zero this)
    lpg_area_end: Optional[int] = None
    enhanced_code_cave: Optional[int] = None  # Where Enhanced ROMs put custom code
    
PLATFORM_CONFIGS = {
    HoldenPlatform.VS_V6: PlatformConfig(
        name="VS V6 Memcal ($51)",
        binary_size=32768,  # 32KB
        xdf_base_offset=0x8000,  # XDF uses $8000-$FFFF
        cal_start=0x0000,
        cal_end=0x4000,  # First 16KB is calibration
        rom_start=0x4000,
        rom_end=0x8000,  # Last 16KB is code
        vector_table_offset=0x7FD6,  # $FFD6 in CPU space
        reset_vector_offset=0x7FFE,  # $FFFE in CPU space
    ),
    HoldenPlatform.VT_V6: PlatformConfig(
        name="VT V6 Memcal ($A5G)",
        binary_size=32768,  # 32KB
        xdf_base_offset=0x8000,
        cal_start=0x0000,
        cal_end=0x4000,
        rom_start=0x4000,
        rom_end=0x8000,
        vector_table_offset=0x7FD6,
        reset_vector_offset=0x7FFE,
    ),
    HoldenPlatform.VX_V6: PlatformConfig(
        name="VX V6 Flash ($060A)",
        binary_size=131072,  # 128KB
        xdf_base_offset=0x0000,  # XDF uses direct file offsets
        cal_start=0x00000,
        cal_end=0x10000,  # First 64KB is calibration
        rom_start=0x10000,
        rom_end=0x20000,  # Last 64KB is code
        vector_table_offset=0x1FFD6,  # $FFD6 in bank 3
        reset_vector_offset=0x1FFFE,
        lpg_area_start=0x057AF,  # LPG tables The1 zeroed
        lpg_area_end=0x05F73,
        enhanced_code_cave=0x17D84,  # Where The1 puts spark cut
    ),
    HoldenPlatform.VY_V6: PlatformConfig(
        name="VY V6 Flash ($060A)",
        binary_size=131072,  # 128KB
        xdf_base_offset=0x0000,
        cal_start=0x00000,
        cal_end=0x10000,
        rom_start=0x10000,
        rom_end=0x20000,
        vector_table_offset=0x1FFD6,
        reset_vector_offset=0x1FFFE,
        lpg_area_start=0x057AF,
        lpg_area_end=0x05F73,
        enhanced_code_cave=0x17D84,
    ),
}

# VY V6 Specific Constants (from vy_v6_constants.py)
VY_V6_CONSTANTS = {
    # RAM Variables (8-bit direct page $00-$FF)
    'ENGINE_RPM': 0x00A2,  # RPM/25 (8-bit, max 6375 RPM)
    'ENGINE_STATE': 0x00A3,  # Engine state flags
    'COOLANT_TEMP': 0x00A4,  # Coolant temperature
    'DWELL_INTERMEDIATE_HI': 0x017A,  # Dwell intermediate high byte
    'DWELL_INTERMEDIATE_LO': 0x017B,  # Dwell intermediate low byte
    'DWELL_OFFSET': 0x1C33,  # Dwell calculation offset
    'MODE_BYTE': 0x0046,  # Mode flags (bits 3,6,7 FREE)
    'SCRATCH_BYTE': 0x01A0,  # Unused scratch RAM
    
    # Hardware Registers ($1000-$103F)
    'PORTA': 0x1000,  # Port A (EST output bits 3,4)
    'PORTB': 0x1004,  # Port B
    'TCNT': 0x100E,  # Timer counter
    'TIC1': 0x1010,  # Input Capture 1 (24X crank)
    'TIC2': 0x1012,  # Input Capture 2 (24X crank reference)
    'TIC3': 0x1014,  # Input Capture 3 (3X cam reference)
    'TOC1': 0x1016,  # Output Compare 1 (timing)
    'TOC2': 0x1018,  # Output Compare 2 (dwell)
    'TOC3': 0x101A,  # Output Compare 3 (EST)
    'TCTL1': 0x1020,  # Timer Control 1
    'TMSK1': 0x1022,  # Timer Mask 1
    'TFLG1': 0x1023,  # Timer Flag 1
    
    # ISR Handler Addresses (verified from trace_jsr_371a_and_all_isrs.py)
    'TIC3_ISR': 0x35FF,  # 24X crank handler (CPU addr, bank2 file=0x135FF)
    'TIC2_ISR': 0x358A,  # 24X crank handler
    'TOC3_ISR': 0x35BD,  # EST output handler
    'TOC1_ISR': 0x35B5,  # Main timing
    'DWELL_CALC': 0x371A,  # Dwell calculation subroutine
    
    # Calibration Addresses (Enhanced ROM v2.09a)
    'MIN_DWELL': 0x171AA,  # Minimum dwell time (stock: $A2 = 2.46ms)
    'MIN_BURN': 0x19813,  # Minimum burn time (stock: $24 = 0.54ms)
    'FUEL_CUTOFF_RPM': 0x77DD,  # Fuel cut RPM table
    'RPM_AXIS_11': 0x75FA,  # 11-cell RPM axis (400-2400 RPM)
    
    # The1's Spark Cut Addresses (v1.1a/v2.04c only)
    'SPARK_CUT_HOOK': 0x056F4,  # Where The1 hooks for spark cut
    'SPARK_CUT_CODE': 0x17D84,  # Code cave for spark cut routine
    'SPARK_RPM_CUT': 0x78B2,  # Tunable RPM threshold (16-bit)
    
    # Chr0m3's Method
    'CHR0M3_HOOK': 0x101E1,  # Hook point for 3X period injection
    'CHR0M3_CODE_CAVE': 0xC500,  # Code cave for main ROM
}

# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class AnalyzerConfig:
    """Configuration for the analyzer"""
    # Output settings
    output_dir: Path = Path("./analysis_output")
    export_json: bool = True
    export_csv: bool = True
    export_markdown: bool = True
    
    # Analysis settings
    show_context_bytes: int = 16
    max_diff_regions: int = 50
    detect_tables: bool = True
    detect_patterns: bool = True
    
    # HC11 settings
    base_address: int = 0x0000  # VY V6 uses 0x0000 base for 128KB binary
    platform: HoldenPlatform = HoldenPlatform.UNKNOWN
    
    # XDF settings
    xdf_path: Optional[Path] = None
    xdf_base_offset: int = 0  # From BASEOFFSET tag
    
    # Platform auto-detection
    auto_detect_platform: bool = True

# ============================================================================
# ECU SIZE CATEGORIES AND SIGNATURES
# ============================================================================

ECU_SIZE_CATEGORIES = {
    # (min_kb, max_kb): (category_name, ecu_description)
    (0, 2): ("Tiny (<2 KB)", "Unknown/Test File"),
    (2, 6): ("4 KB", "GM TPI/EPROM (2732/27C128)"),
    (6, 12): ("8 KB", "GM TPI/EPROM (2764)"),
    (12, 24): ("16 KB", "GM TPI/EPROM (27128)"),
    (24, 36): ("32 KB", "GM TPI/EPROM/VS-VT Memcal (27C256)"),
    (36, 42): ("38-39 KB", "GM TPI Partial Dump"),
    (42, 100): ("64 KB", "BMW MS42 Partial/Early Holden"),
    (100, 192): ("128 KB", "Holden VX/VY V6 ($060A)/VW/VAG"),
    (192, 384): ("256 KB", "BMW ZF Transmission/Bosch ME7"),
    (384, 600): ("512 KB", "BMW MS42/MS43 (E46/E39) Full"),
    (600, 1200): ("1 MB", "BMW MS45/E67 Small"),
    (1200, 1700): ("1.5 MB", "GM E67 Partial/HPT Modified"),
    (1700, 2300): ("2 MB", "GM E67/E78 (LS3/L98/L77/LT1)"),
    (2300, 4500): ("4 MB", "GM E92 (LT4)/HPT Full Export"),
    (4500, 9000): ("8 MB", "HPT/VCM Full Project Export"),
}

ECU_SIGNATURES = {
    # (signature_bytes, ecu_type)
    b'MS42': 'BMW MS42',
    b'MS43': 'BMW MS43',
    b'MS45': 'BMW MS45',
    b'0110C6': 'BMW MS42 (0110C6)',
    b'0110AD': 'BMW MS42 (0110AD)',
    b'430069': 'BMW MS43',
    b'E38': 'GM E38 (LS3/L76)',
    b'E67': 'GM E67 (L98/L77)',
    b'E78': 'GM E78 (LT1)',
    b'E92': 'GM E92 (LT4)',
    b'E40': 'GM E40 (L99)',
    b'TDCO': 'GM Calibration Format',
    b'Holden': 'Holden ECU',
    b'HOLDEN': 'Holden ECU',
    b'$060A': 'Holden V6 Delco ($060A)',
    b'$BD': 'Holden V6 Delco ($BD)',
    b'HPT': 'HP Tuners Export',
    b'VCM': 'VCM Scanner Export',
    b'Siemens': 'Siemens ECU',
    b'Bosch': 'Bosch ECU',
}

# ============================================================================
# HC11 OPCODE TABLE (Complete)
# ============================================================================

HC11_OPCODES = {
    # Format: opcode: (mnemonic, addressing_mode, length)
    # Addressing modes: imp, imm, dir, ext, idx, rel, bit_dir, bit_idx
    
    # Control
    0x00: ("TEST", "imp", 1), 0x01: ("NOP", "imp", 1),
    0x02: ("IDIV", "imp", 1), 0x03: ("FDIV", "imp", 1),
    0x04: ("LSRD", "imp", 1), 0x05: ("ASLD", "imp", 1),
    0x06: ("TAP", "imp", 1), 0x07: ("TPA", "imp", 1),
    0x08: ("INX", "imp", 1), 0x09: ("DEX", "imp", 1),
    0x0A: ("CLV", "imp", 1), 0x0B: ("SEV", "imp", 1),
    0x0C: ("CLC", "imp", 1), 0x0D: ("SEC", "imp", 1),
    0x0E: ("CLI", "imp", 1), 0x0F: ("SEI", "imp", 1),
    
    # Bit manipulation
    0x10: ("SBA", "imp", 1), 0x11: ("CBA", "imp", 1),
    0x12: ("BRSET", "bit_dir", 4), 0x13: ("BRCLR", "bit_dir", 4),
    0x14: ("BSET", "bit_dir", 3), 0x15: ("BCLR", "bit_dir", 3),
    0x16: ("TAB", "imp", 1), 0x17: ("TBA", "imp", 1),
    0x18: ("PAGE1", "prefix", 1), 0x19: ("DAA", "imp", 1),
    0x1A: ("PAGE2", "prefix", 1), 0x1B: ("ABA", "imp", 1),
    0x1C: ("BSET", "bit_idx", 3), 0x1D: ("BCLR", "bit_idx", 3),
    0x1E: ("BRSET", "bit_idx", 4), 0x1F: ("BRCLR", "bit_idx", 4),
    
    # Branches
    0x20: ("BRA", "rel", 2), 0x21: ("BRN", "rel", 2),
    0x22: ("BHI", "rel", 2), 0x23: ("BLS", "rel", 2),
    0x24: ("BCC", "rel", 2), 0x25: ("BCS", "rel", 2),
    0x26: ("BNE", "rel", 2), 0x27: ("BEQ", "rel", 2),
    0x28: ("BVC", "rel", 2), 0x29: ("BVS", "rel", 2),
    0x2A: ("BPL", "rel", 2), 0x2B: ("BMI", "rel", 2),
    0x2C: ("BGE", "rel", 2), 0x2D: ("BLT", "rel", 2),
    0x2E: ("BGT", "rel", 2), 0x2F: ("BLE", "rel", 2),
    
    # Stack
    0x30: ("TSX", "imp", 1), 0x31: ("INS", "imp", 1),
    0x32: ("PULA", "imp", 1), 0x33: ("PULB", "imp", 1),
    0x34: ("DES", "imp", 1), 0x35: ("TXS", "imp", 1),
    0x36: ("PSHA", "imp", 1), 0x37: ("PSHB", "imp", 1),
    0x38: ("PULX", "imp", 1), 0x39: ("RTS", "imp", 1),
    0x3A: ("ABX", "imp", 1), 0x3B: ("RTI", "imp", 1),
    0x3C: ("PSHX", "imp", 1), 0x3D: ("MUL", "imp", 1),
    0x3E: ("WAI", "imp", 1), 0x3F: ("SWI", "imp", 1),
    
    # A register
    0x40: ("NEGA", "imp", 1), 0x43: ("COMA", "imp", 1),
    0x44: ("LSRA", "imp", 1), 0x46: ("RORA", "imp", 1),
    0x47: ("ASRA", "imp", 1), 0x48: ("ASLA", "imp", 1),
    0x49: ("ROLA", "imp", 1), 0x4A: ("DECA", "imp", 1),
    0x4C: ("INCA", "imp", 1), 0x4D: ("TSTA", "imp", 1),
    0x4F: ("CLRA", "imp", 1),
    
    # B register
    0x50: ("NEGB", "imp", 1), 0x53: ("COMB", "imp", 1),
    0x54: ("LSRB", "imp", 1), 0x56: ("RORB", "imp", 1),
    0x57: ("ASRB", "imp", 1), 0x58: ("ASLB", "imp", 1),
    0x59: ("ROLB", "imp", 1), 0x5A: ("DECB", "imp", 1),
    0x5C: ("INCB", "imp", 1), 0x5D: ("TSTB", "imp", 1),
    0x5F: ("CLRB", "imp", 1),
    
    # Indexed X memory ops
    0x60: ("NEG", "idx", 2), 0x63: ("COM", "idx", 2),
    0x64: ("LSR", "idx", 2), 0x66: ("ROR", "idx", 2),
    0x67: ("ASR", "idx", 2), 0x68: ("ASL", "idx", 2),
    0x69: ("ROL", "idx", 2), 0x6A: ("DEC", "idx", 2),
    0x6C: ("INC", "idx", 2), 0x6D: ("TST", "idx", 2),
    0x6E: ("JMP", "idx", 2), 0x6F: ("CLR", "idx", 2),
    
    # Extended memory ops
    0x70: ("NEG", "ext", 3), 0x73: ("COM", "ext", 3),
    0x74: ("LSR", "ext", 3), 0x76: ("ROR", "ext", 3),
    0x77: ("ASR", "ext", 3), 0x78: ("ASL", "ext", 3),
    0x79: ("ROL", "ext", 3), 0x7A: ("DEC", "ext", 3),
    0x7C: ("INC", "ext", 3), 0x7D: ("TST", "ext", 3),
    0x7E: ("JMP", "ext", 3), 0x7F: ("CLR", "ext", 3),
    
    # A register immediate/direct/extended/indexed
    0x80: ("SUBA", "imm", 2), 0x81: ("CMPA", "imm", 2),
    0x82: ("SBCA", "imm", 2), 0x83: ("SUBD", "imm", 3),
    0x84: ("ANDA", "imm", 2), 0x85: ("BITA", "imm", 2),
    0x86: ("LDAA", "imm", 2), 0x88: ("EORA", "imm", 2),
    0x89: ("ADCA", "imm", 2), 0x8A: ("ORAA", "imm", 2),
    0x8B: ("ADDA", "imm", 2), 0x8C: ("CPX", "imm", 3),
    0x8D: ("BSR", "rel", 2), 0x8E: ("LDS", "imm", 3),
    0x8F: ("XGDX", "imp", 1),
    
    0x90: ("SUBA", "dir", 2), 0x91: ("CMPA", "dir", 2),
    0x92: ("SBCA", "dir", 2), 0x93: ("SUBD", "dir", 2),
    0x94: ("ANDA", "dir", 2), 0x95: ("BITA", "dir", 2),
    0x96: ("LDAA", "dir", 2), 0x97: ("STAA", "dir", 2),
    0x98: ("EORA", "dir", 2), 0x99: ("ADCA", "dir", 2),
    0x9A: ("ORAA", "dir", 2), 0x9B: ("ADDA", "dir", 2),
    0x9C: ("CPX", "dir", 2), 0x9D: ("JSR", "dir", 2),
    0x9E: ("LDS", "dir", 2), 0x9F: ("STS", "dir", 2),
    
    0xA0: ("SUBA", "idx", 2), 0xA1: ("CMPA", "idx", 2),
    0xA2: ("SBCA", "idx", 2), 0xA3: ("SUBD", "idx", 2),
    0xA4: ("ANDA", "idx", 2), 0xA5: ("BITA", "idx", 2),
    0xA6: ("LDAA", "idx", 2), 0xA7: ("STAA", "idx", 2),
    0xA8: ("EORA", "idx", 2), 0xA9: ("ADCA", "idx", 2),
    0xAA: ("ORAA", "idx", 2), 0xAB: ("ADDA", "idx", 2),
    0xAC: ("CPX", "idx", 2), 0xAD: ("JSR", "idx", 2),
    0xAE: ("LDS", "idx", 2), 0xAF: ("STS", "idx", 2),
    
    0xB0: ("SUBA", "ext", 3), 0xB1: ("CMPA", "ext", 3),
    0xB2: ("SBCA", "ext", 3), 0xB3: ("SUBD", "ext", 3),
    0xB4: ("ANDA", "ext", 3), 0xB5: ("BITA", "ext", 3),
    0xB6: ("LDAA", "ext", 3), 0xB7: ("STAA", "ext", 3),
    0xB8: ("EORA", "ext", 3), 0xB9: ("ADCA", "ext", 3),
    0xBA: ("ORAA", "ext", 3), 0xBB: ("ADDA", "ext", 3),
    0xBC: ("CPX", "ext", 3), 0xBD: ("JSR", "ext", 3),
    0xBE: ("LDS", "ext", 3), 0xBF: ("STS", "ext", 3),
    
    # B register / D register
    0xC0: ("SUBB", "imm", 2), 0xC1: ("CMPB", "imm", 2),
    0xC2: ("SBCB", "imm", 2), 0xC3: ("ADDD", "imm", 3),
    0xC4: ("ANDB", "imm", 2), 0xC5: ("BITB", "imm", 2),
    0xC6: ("LDAB", "imm", 2), 0xC8: ("EORB", "imm", 2),
    0xC9: ("ADCB", "imm", 2), 0xCA: ("ORAB", "imm", 2),
    0xCB: ("ADDB", "imm", 2), 0xCC: ("LDD", "imm", 3),
    0xCE: ("LDX", "imm", 3), 0xCF: ("STOP", "imp", 1),
    
    0xD0: ("SUBB", "dir", 2), 0xD1: ("CMPB", "dir", 2),
    0xD2: ("SBCB", "dir", 2), 0xD3: ("ADDD", "dir", 2),
    0xD4: ("ANDB", "dir", 2), 0xD5: ("BITB", "dir", 2),
    0xD6: ("LDAB", "dir", 2), 0xD7: ("STAB", "dir", 2),
    0xD8: ("EORB", "dir", 2), 0xD9: ("ADCB", "dir", 2),
    0xDA: ("ORAB", "dir", 2), 0xDB: ("ADDB", "dir", 2),
    0xDC: ("LDD", "dir", 2), 0xDD: ("STD", "dir", 2),
    0xDE: ("LDX", "dir", 2), 0xDF: ("STX", "dir", 2),
    
    0xE0: ("SUBB", "idx", 2), 0xE1: ("CMPB", "idx", 2),
    0xE2: ("SBCB", "idx", 2), 0xE3: ("ADDD", "idx", 2),
    0xE4: ("ANDB", "idx", 2), 0xE5: ("BITB", "idx", 2),
    0xE6: ("LDAB", "idx", 2), 0xE7: ("STAB", "idx", 2),
    0xE8: ("EORB", "idx", 2), 0xE9: ("ADCB", "idx", 2),
    0xEA: ("ORAB", "idx", 2), 0xEB: ("ADDB", "idx", 2),
    0xEC: ("LDD", "idx", 2), 0xED: ("STD", "idx", 2),
    0xEE: ("LDX", "idx", 2), 0xEF: ("STX", "idx", 2),
    
    0xF0: ("SUBB", "ext", 3), 0xF1: ("CMPB", "ext", 3),
    0xF2: ("SBCB", "ext", 3), 0xF3: ("ADDD", "ext", 3),
    0xF4: ("ANDB", "ext", 3), 0xF5: ("BITB", "ext", 3),
    0xF6: ("LDAB", "ext", 3), 0xF7: ("STAB", "ext", 3),
    0xF8: ("EORB", "ext", 3), 0xF9: ("ADCB", "ext", 3),
    0xFA: ("ORAB", "ext", 3), 0xFB: ("ADDB", "ext", 3),
    0xFC: ("LDD", "ext", 3), 0xFD: ("STD", "ext", 3),
    0xFE: ("LDX", "ext", 3), 0xFF: ("STX", "ext", 3),
}

# HC11F Hardware Registers (VY V6 uses 68HC11FC0, NOT HC11E9)
HC11_REGISTERS = {
    0x1000: "PORTA", 0x1001: "DDRA", 0x1002: "PORTG", 0x1003: "DDRG",
    0x1004: "PORTB", 0x1005: "PORTF", 0x1006: "PORTC", 0x1007: "DDRC",
    0x1008: "PORTD", 0x1009: "DDRD", 0x100A: "PORTE", 0x100B: "CFORC",
    0x100C: "OC1M", 0x100D: "OC1D", 0x100E: "TCNT_HI", 0x100F: "TCNT_LO",
    0x1010: "TIC1_HI", 0x1011: "TIC1_LO", 0x1012: "TIC2_HI", 0x1013: "TIC2_LO",
    0x1014: "TIC3_HI", 0x1015: "TIC3_LO", 0x1016: "TOC1_HI", 0x1017: "TOC1_LO",
    0x1018: "TOC2_HI", 0x1019: "TOC2_LO", 0x101A: "TOC3_HI", 0x101B: "TOC3_LO",
    0x101C: "TOC4_HI", 0x101D: "TOC4_LO", 0x101E: "TI4_O5_HI", 0x101F: "TI4_O5_LO",
    0x1020: "TCTL1", 0x1021: "TCTL2", 0x1022: "TMSK1", 0x1023: "TFLG1",
    0x1024: "TMSK2", 0x1025: "TFLG2", 0x1026: "PACTL", 0x1027: "PACNT",
    0x1028: "SPCR", 0x1029: "SPSR", 0x102A: "SPDR", 0x102B: "BAUD",
    0x102C: "SCCR1", 0x102D: "SCCR2", 0x102E: "SCSR", 0x102F: "SCDR",
    0x1030: "ADCTL", 0x1031: "ADR1", 0x1032: "ADR2", 0x1033: "ADR3",
    0x1034: "ADR4", 0x1035: "BPROT", 0x1036: "EPROG", 0x1039: "OPTION",
    0x103A: "COPRST", 0x103B: "PPROG", 0x103C: "HPRIO", 0x103D: "INIT",
    0x103E: "TEST1", 0x103F: "CONFIG",
}

# ============================================================================
# XDF PARSER
# ============================================================================

class XDFParser:
    """Parse TunerPro XDF files for calibration addresses"""
    
    def __init__(self, xdf_path: Optional[Path] = None):
        self.calibrations = {}  # addr -> (title, type, category)
        self.categories = {}
        if xdf_path and xdf_path.exists():
            self.load_xdf(xdf_path)
    
    def load_xdf(self, xdf_path: Path):
        """Parse XDF file and extract calibration addresses"""
        try:
            tree = ET.parse(xdf_path)
            root = tree.getroot()
            
            # Parse categories
            for cat in root.findall('.//XDFCATEGORY'):
                cat_id = cat.get('id')
                name_elem = cat.find('XDFCATEGORYNAME')
                if cat_id and name_elem is not None:
                    self.categories[cat_id] = name_elem.text or "Unknown"
            
            # Parse constants
            for const in root.findall('.//XDFCONSTANT'):
                self._parse_element(const, 'CONSTANT')
            
            # Parse tables
            for table in root.findall('.//XDFTABLE'):
                self._parse_element(table, 'TABLE')
            
            # Parse flags
            for flag in root.findall('.//XDFFLAG'):
                self._parse_element(flag, 'FLAG')
            
            print(f"[XDF] Loaded {len(self.calibrations)} calibration addresses")
            
        except Exception as e:
            print(f"[XDF] Error loading {xdf_path}: {e}")
    
    def _parse_element(self, elem, elem_type: str):
        """Parse a single XDF element"""
        title_elem = elem.find('title')
        title = title_elem.text if title_elem is not None else "Unknown"
        
        cat_mem = elem.find('CATEGORYMEM')
        cat_id = cat_mem.get('category', '0') if cat_mem is not None else '0'
        category = self.categories.get(cat_id, "Uncategorized")
        
        emb = elem.find('EMBEDDEDDATA') or elem.find('.//EMBEDDEDDATA')
        if emb is not None:
            addr_str = emb.get('mmedaddress', '')
            if addr_str:
                try:
                    addr = int(addr_str, 16) if addr_str.startswith('0x') else int(addr_str)
                    self.calibrations[addr] = (title, elem_type, category)
                except ValueError:
                    pass
    
    def lookup(self, addr: int) -> Optional[Tuple[str, str, str]]:
        """Look up calibration by address"""
        return self.calibrations.get(addr)

# ============================================================================
# HC11 DISASSEMBLER
# ============================================================================

class HC11Disassembler:
    """Motorola 68HC11 instruction decoder with XDF annotation"""
    
    def __init__(self, data: bytes, base_addr: int = 0x0000, xdf: Optional[XDFParser] = None):
        self.data = data
        self.base_addr = base_addr
        self.xdf = xdf
    
    def read_byte(self, offset: int) -> int:
        """Read byte at file offset"""
        if 0 <= offset < len(self.data):
            return self.data[offset]
        return 0
    
    def read_word(self, offset: int) -> int:
        """Read big-endian 16-bit word"""
        if 0 <= offset + 1 < len(self.data):
            return (self.data[offset] << 8) | self.data[offset + 1]
        return 0
    
    def get_annotation(self, addr: int) -> str:
        """Get XDF/hardware annotation for address"""
        # Check hardware registers
        if addr in HC11_REGISTERS:
            return f"[HW] {HC11_REGISTERS[addr]}"
        
        # Check XDF calibrations
        if self.xdf:
            cal = self.xdf.lookup(addr)
            if cal:
                return f"[{cal[1]}] {cal[0]}"
        
        return ""
    
    def disassemble_instruction(self, offset: int) -> Tuple[str, int]:
        """Disassemble single instruction, return (asm_string, length)"""
        opcode = self.read_byte(offset)
        cpu_addr = self.base_addr + offset
        
        if opcode not in HC11_OPCODES:
            return f"{cpu_addr:05X}: {opcode:02X}           DB    ${opcode:02X}", 1
        
        mnemonic, mode, length = HC11_OPCODES[opcode]
        
        # Format based on addressing mode
        if mode == "imp":
            hex_bytes = f"{opcode:02X}"
            operand = ""
        elif mode == "imm":
            if length == 2:
                op1 = self.read_byte(offset + 1)
                hex_bytes = f"{opcode:02X} {op1:02X}"
                operand = f"#${op1:02X}"
            else:
                op1 = self.read_byte(offset + 1)
                op2 = self.read_byte(offset + 2)
                hex_bytes = f"{opcode:02X} {op1:02X} {op2:02X}"
                operand = f"#${(op1 << 8) | op2:04X}"
        elif mode == "dir":
            op1 = self.read_byte(offset + 1)
            hex_bytes = f"{opcode:02X} {op1:02X}"
            operand = f"${op1:02X}"
        elif mode == "ext":
            op1 = self.read_byte(offset + 1)
            op2 = self.read_byte(offset + 2)
            addr = (op1 << 8) | op2
            hex_bytes = f"{opcode:02X} {op1:02X} {op2:02X}"
            annotation = self.get_annotation(addr)
            operand = f"${addr:04X}" + (f"  ; {annotation}" if annotation else "")
        elif mode == "idx":
            op1 = self.read_byte(offset + 1)
            hex_bytes = f"{opcode:02X} {op1:02X}"
            operand = f"${op1:02X},X"
        elif mode == "rel":
            disp = self.read_byte(offset + 1)
            # Calculate target (signed displacement)
            if disp >= 0x80:
                disp -= 256
            target = cpu_addr + length + disp
            hex_bytes = f"{opcode:02X} {self.read_byte(offset + 1):02X}"
            operand = f"${target:04X}"
        elif mode == "bit_dir":
            op1 = self.read_byte(offset + 1)
            op2 = self.read_byte(offset + 2)
            if length == 4:
                op3 = self.read_byte(offset + 3)
                hex_bytes = f"{opcode:02X} {op1:02X} {op2:02X} {op3:02X}"
                operand = f"${op1:02X},#${op2:02X},${op3:02X}"
            else:
                hex_bytes = f"{opcode:02X} {op1:02X} {op2:02X}"
                operand = f"${op1:02X},#${op2:02X}"
        elif mode == "prefix":
            hex_bytes = f"{opcode:02X}"
            operand = "(page prefix)"
        else:
            hex_bytes = f"{opcode:02X}"
            operand = f"({mode})"
        
        return f"{cpu_addr:05X}: {hex_bytes:14s} {mnemonic:6s} {operand}", length
    
    def disassemble_range(self, start: int, end: int) -> List[str]:
        """Disassemble a range of bytes"""
        lines = []
        offset = start
        while offset < end and offset < len(self.data):
            asm, length = self.disassemble_instruction(offset)
            lines.append(asm)
            offset += length
        return lines

# ============================================================================
# BINARY ANALYZER
# ============================================================================

class BinaryAnalyzer:
    """Comprehensive binary file analyzer"""
    
    def __init__(self, filepath: Path, config: AnalyzerConfig = None):
        self.filepath = Path(filepath)
        self.config = config or AnalyzerConfig()
        
        if not self.filepath.exists():
            raise FileNotFoundError(f"Binary not found: {filepath}")
        
        self.data = self.filepath.read_bytes()
        self.size = len(self.data)
        self.size_kb = self.size / 1024
        
        # Initialize XDF parser if configured
        self.xdf = None
        if self.config.xdf_path:
            self.xdf = XDFParser(self.config.xdf_path)
        
        # Initialize disassembler
        self.disasm = HC11Disassembler(self.data, self.config.base_address, self.xdf)
    
    def categorize_size(self) -> Tuple[str, str]:
        """Categorize by file size"""
        for (min_kb, max_kb), (cat, desc) in ECU_SIZE_CATEGORIES.items():
            if min_kb <= self.size_kb < max_kb:
                return cat, desc
        return "Unknown", "Unknown ECU Type"
    
    def detect_signatures(self) -> List[str]:
        """Detect ECU signatures in header"""
        found = []
        header = self.data[:2048]
        
        for sig, ecu_type in ECU_SIGNATURES.items():
            if sig in header:
                found.append(ecu_type)
        
        return found if found else ["Unknown"]
    
    def calculate_hashes(self) -> Dict[str, str]:
        """Calculate file hashes"""
        return {
            'md5': hashlib.md5(self.data).hexdigest(),
            'sha256': hashlib.sha256(self.data).hexdigest(),
        }
    
    def find_empty_regions(self, min_size: int = 256) -> List[Dict]:
        """Find unprogrammed (0xFF) or empty (0x00) regions"""
        regions = []
        chunk_size = 256
        
        current_type = None
        current_start = None
        
        for i in range(0, len(self.data), chunk_size):
            chunk = self.data[i:i+chunk_size]
            
            if all(b == 0xFF for b in chunk):
                chunk_type = "0xFF"
            elif all(b == 0x00 for b in chunk):
                chunk_type = "0x00"
            else:
                chunk_type = None
            
            if chunk_type != current_type:
                if current_type and i - current_start >= min_size:
                    regions.append({
                        'type': current_type,
                        'start': current_start,
                        'end': i,
                        'size': i - current_start
                    })
                current_type = chunk_type
                current_start = i
        
        # Handle final region
        if current_type and len(self.data) - current_start >= min_size:
            regions.append({
                'type': current_type,
                'start': current_start,
                'end': len(self.data),
                'size': len(self.data) - current_start
            })
        
        return regions
    
    def analyze(self) -> Dict:
        """Full analysis of binary"""
        cat, desc = self.categorize_size()
        
        return {
            'file': str(self.filepath),
            'filename': self.filepath.name,
            'size_bytes': self.size,
            'size_kb': round(self.size_kb, 2),
            'size_category': cat,
            'ecu_description': desc,
            'signatures': self.detect_signatures(),
            'hashes': self.calculate_hashes(),
            'empty_regions': self.find_empty_regions(),
            'empty_space_total': sum(r['size'] for r in self.find_empty_regions()),
        }
    
    def disassemble_at(self, offset: int, length: int = 64) -> List[str]:
        """Disassemble at specific offset"""
        return self.disasm.disassemble_range(offset, offset + length)
    
    def hex_dump(self, offset: int, length: int = 64) -> str:
        """Hex dump at offset"""
        lines = []
        for i in range(0, length, 16):
            addr = offset + i
            chunk = self.data[addr:addr+16]
            hex_str = ' '.join(f'{b:02X}' for b in chunk)
            ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
            lines.append(f"{addr:06X}  {hex_str:48s}  {ascii_str}")
        return '\n'.join(lines)

# ============================================================================
# BINARY COMPARATOR
# ============================================================================

class BinaryComparator:
    """Compare two binary files"""
    
    def __init__(self, file1: Path, file2: Path, config: AnalyzerConfig = None):
        self.file1 = Path(file1)
        self.file2 = Path(file2)
        self.config = config or AnalyzerConfig()
        
        self.data1 = self.file1.read_bytes()
        self.data2 = self.file2.read_bytes()
        
        # Initialize XDF
        self.xdf = None
        if self.config.xdf_path:
            self.xdf = XDFParser(self.config.xdf_path)
    
    def find_differences(self) -> List[Dict]:
        """Find all difference regions"""
        differences = []
        common_len = min(len(self.data1), len(self.data2))
        
        in_diff = False
        diff_start = 0
        
        for i in range(common_len):
            if self.data1[i] != self.data2[i]:
                if not in_diff:
                    diff_start = i
                    in_diff = True
            else:
                if in_diff:
                    differences.append({
                        'start': diff_start,
                        'end': i - 1,
                        'length': i - diff_start,
                        'file1_bytes': self.data1[diff_start:i].hex(),
                        'file2_bytes': self.data2[diff_start:i].hex(),
                    })
                    in_diff = False
        
        if in_diff:
            differences.append({
                'start': diff_start,
                'end': common_len - 1,
                'length': common_len - diff_start,
                'file1_bytes': self.data1[diff_start:common_len].hex(),
                'file2_bytes': self.data2[diff_start:common_len].hex(),
            })
        
        return differences
    
    def compare(self) -> Dict:
        """Full comparison"""
        differences = self.find_differences()
        total_diff = sum(d['length'] for d in differences)
        common_len = min(len(self.data1), len(self.data2))
        
        return {
            'file1': str(self.file1),
            'file2': str(self.file2),
            'size1': len(self.data1),
            'size2': len(self.data2),
            'size_match': len(self.data1) == len(self.data2),
            'total_different_bytes': total_diff,
            'percent_different': round((total_diff / common_len * 100) if common_len else 0, 2),
            'num_diff_regions': len(differences),
            'differences': differences[:self.config.max_diff_regions],
        }
    
    def annotate_differences(self, differences: List[Dict]) -> List[Dict]:
        """Add XDF annotations to differences"""
        for diff in differences:
            addr = diff['start']
            annotations = []
            
            # Check XDF
            if self.xdf:
                cal = self.xdf.lookup(addr)
                if cal:
                    annotations.append(f"[{cal[1]}] {cal[0]}")
            
            # Check hardware registers
            if addr in HC11_REGISTERS:
                annotations.append(f"[HW] {HC11_REGISTERS[addr]}")
            
            diff['annotations'] = annotations
        
        return differences
    
    def print_diff_report(self):
        """Print human-readable diff report"""
        result = self.compare()
        
        print("\n" + "=" * 80)
        print("BINARY COMPARISON REPORT")
        print("=" * 80)
        print(f"\nFile 1: {self.file1.name} ({result['size1']:,} bytes)")
        print(f"File 2: {self.file2.name} ({result['size2']:,} bytes)")
        
        if not result['size_match']:
            print(f"\n⚠️  Size mismatch: {abs(result['size1'] - result['size2'])} bytes")
        
        print(f"\n📊 Statistics:")
        print(f"   Different bytes: {result['total_different_bytes']:,} ({result['percent_different']}%)")
        print(f"   Diff regions: {result['num_diff_regions']}")
        
        if result['differences']:
            print(f"\n🔍 Difference Regions (showing first {len(result['differences'])}):\n")
            
            annotated = self.annotate_differences(result['differences'])
            
            for i, diff in enumerate(annotated):
                print(f"   #{i+1}: 0x{diff['start']:06X} - 0x{diff['end']:06X} ({diff['length']} bytes)")
                if diff.get('annotations'):
                    for ann in diff['annotations']:
                        print(f"        {ann}")
                
                # Show hex for small diffs
                if diff['length'] <= 16:
                    print(f"        File1: {diff['file1_bytes']}")
                    print(f"        File2: {diff['file2_bytes']}")
                print()

# ============================================================================
# BATCH ANALYZER
# ============================================================================

class BatchBinaryAnalyzer:
    """Analyze multiple binaries, find duplicates and near-matches"""
    
    def __init__(self, search_path: Path, config: AnalyzerConfig = None):
        self.search_path = Path(search_path)
        self.config = config or AnalyzerConfig()
        self.files = []
        self.results = {
            'exact_duplicates': defaultdict(list),
            'near_matches': [],
            'by_size': defaultdict(list),
            'by_signature': defaultdict(list),
        }
    
    def scan(self, extensions: List[str] = ['.bin', '.ecu', '.rom']):
        """Scan directory for binary files"""
        print(f"\n[*] Scanning {self.search_path}...")
        
        for ext in extensions:
            for filepath in self.search_path.rglob(f"*{ext}"):
                try:
                    analyzer = BinaryAnalyzer(filepath, self.config)
                    info = analyzer.analyze()
                    self.files.append(info)
                    
                    # Group by size category
                    self.results['by_size'][info['size_category']].append(info)
                    
                    # Group by signature
                    for sig in info['signatures']:
                        self.results['by_signature'][sig].append(info)
                    
                    print(f"   [+] {filepath.name} ({info['size_category']})")
                    
                except Exception as e:
                    print(f"   [!] Error: {filepath.name}: {e}")
        
        print(f"\n[✓] Found {len(self.files)} files")
    
    def find_duplicates(self):
        """Find exact duplicates by hash"""
        hash_groups = defaultdict(list)
        for info in self.files:
            hash_groups[info['hashes']['md5']].append(info)
        
        for md5, files in hash_groups.items():
            if len(files) > 1:
                self.results['exact_duplicates'][md5] = files
                print(f"[!] Found {len(files)} duplicates: {md5[:12]}...")
    
    def find_near_matches(self, threshold: float = 95.0):
        """Find near-matches by binary similarity"""
        print(f"\n[*] Finding near-matches (>{threshold}% similar)...")
        
        # Group by size for comparison
        size_groups = defaultdict(list)
        for info in self.files:
            size_groups[info['size_bytes']].append(info)
        
        for size, files in size_groups.items():
            if len(files) < 2:
                continue
            
            for i, f1 in enumerate(files):
                for f2 in files[i+1:]:
                    # Quick similarity check
                    data1 = Path(f1['file']).read_bytes()
                    data2 = Path(f2['file']).read_bytes()
                    
                    matches = sum(1 for a, b in zip(data1, data2) if a == b)
                    similarity = (matches / len(data1)) * 100
                    
                    if similarity >= threshold and similarity < 100:
                        self.results['near_matches'].append({
                            'file1': f1['filename'],
                            'file2': f2['filename'],
                            'similarity': round(similarity, 2),
                            'size': size,
                        })
                        print(f"   [{similarity:.1f}%] {f1['filename']} <-> {f2['filename']}")
    
    def export_results(self, output_dir: Path = None):
        """Export results to JSON/CSV/Markdown"""
        output_dir = output_dir or self.config.output_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # JSON export
        if self.config.export_json:
            json_path = output_dir / f"binary_analysis_{timestamp}.json"
            with open(json_path, 'w') as f:
                json.dump({
                    'files': self.files,
                    'duplicates': dict(self.results['exact_duplicates']),
                    'near_matches': self.results['near_matches'],
                    'by_size': {k: [f['filename'] for f in v] for k, v in self.results['by_size'].items()},
                }, f, indent=2, default=str)
            print(f"[✓] JSON: {json_path}")
        
        # Markdown export
        if self.config.export_markdown:
            md_path = output_dir / f"binary_analysis_{timestamp}.md"
            with open(md_path, 'w') as f:
                f.write("# Binary Analysis Report\n\n")
                f.write(f"**Generated:** {datetime.now()}\n\n")
                f.write(f"**Files Analyzed:** {len(self.files)}\n\n")
                
                f.write("## By Size Category\n\n")
                for cat, files in sorted(self.results['by_size'].items()):
                    f.write(f"### {cat} ({len(files)} files)\n\n")
                    for info in files[:10]:
                        f.write(f"- `{info['filename']}` - {', '.join(info['signatures'])}\n")
                    if len(files) > 10:
                        f.write(f"- ... and {len(files) - 10} more\n")
                    f.write("\n")
                
                if self.results['exact_duplicates']:
                    f.write("## Exact Duplicates\n\n")
                    for md5, files in self.results['exact_duplicates'].items():
                        f.write(f"### Hash: {md5[:16]}...\n\n")
                        for info in files:
                            f.write(f"- `{info['filename']}`\n")
                        f.write("\n")
                
                if self.results['near_matches']:
                    f.write("## Near Matches\n\n")
                    f.write("| File 1 | File 2 | Similarity |\n")
                    f.write("|--------|--------|------------|\n")
                    for match in self.results['near_matches']:
                        f.write(f"| {match['file1']} | {match['file2']} | {match['similarity']}% |\n")
            
            print(f"[✓] Markdown: {md_path}")

# ============================================================================
# ENHANCED XDF PARSER (From tunerpro_exporter.py)
# ============================================================================

class EnhancedXDFParser(XDFParser):
    """
    Enhanced XDF parser with full feature support from tunerpro_exporter.py
    
    Features:
    - BASEOFFSET handling for VS/VT memcal vs VX/VY flash
    - EMBEDDEDDATA axis extraction (not just LABEL)
    - embedinfo axis linking (MS42/MS43 style)
    - Math equation parsing
    - mmedtypeflags parsing (signed, endianness)
    - Category and unit extraction
    """
    
    def __init__(self, xdf_path: Optional[Path] = None, bin_data: bytes = None):
        self.base_offset = 0
        self.base_subtract = 0
        self.uniqueid_index = {}
        self.bin_data = bin_data
        self.tables = []
        self.constants = []
        self.flags = []
        self.definition_name = "Unknown"
        super().__init__(xdf_path)
    
    def load_xdf(self, xdf_path: Path):
        """Parse XDF file with full feature extraction"""
        try:
            tree = ET.parse(xdf_path)
            self.root = tree.getroot()
            
            # Extract header info including BASEOFFSET
            self._extract_header()
            
            # Parse categories
            for cat in self.root.findall('.//CATEGORY'):
                index = cat.get('index', '0')
                name = cat.get('name', 'Unknown')
                try:
                    idx = int(index, 16) if index.startswith('0x') else int(index)
                    self.categories[str(idx)] = name
                except ValueError:
                    pass
            
            # Build uniqueid index for embedinfo linking
            self._build_uniqueid_index()
            
            # Parse all element types
            for const in self.root.findall('.//XDFCONSTANT'):
                self._parse_element(const, 'CONSTANT')
                self._parse_constant_full(const)
            
            for table in self.root.findall('.//XDFTABLE'):
                self._parse_element(table, 'TABLE')
                self._parse_table_full(table)
            
            for flag in self.root.findall('.//XDFFLAG'):
                self._parse_element(flag, 'FLAG')
            
            print(f"[XDF] Loaded: {self.definition_name}")
            print(f"[XDF] BASEOFFSET: {self.base_offset} (subtract={self.base_subtract})")
            print(f"[XDF] {len(self.calibrations)} addresses, "
                  f"{len(self.constants)} constants, {len(self.tables)} tables")
            
        except Exception as e:
            print(f"[XDF] Error loading {xdf_path}: {e}")
            import traceback
            traceback.print_exc()
    
    def _extract_header(self):
        """Extract definition name and BASEOFFSET from XDF header"""
        header = self.root.find('.//XDFHEADER')
        if header is not None:
            # Get definition name
            for tag in ['deftitle', 'title', 'name']:
                elem = header.find(tag)
                if elem is not None and elem.text:
                    self.definition_name = elem.text.strip()
                    break
            
            # Extract BASEOFFSET (critical for VS/VT vs VX/VY)
            baseoffset = header.find('.//BASEOFFSET')
            if baseoffset is not None:
                offset_str = baseoffset.get('offset', '0')
                try:
                    self.base_offset = int(offset_str, 16) if offset_str.startswith('0x') else int(offset_str)
                except ValueError:
                    self.base_offset = 0
                
                subtract_str = baseoffset.get('subtract', '0')
                try:
                    self.base_subtract = int(subtract_str)
                except ValueError:
                    self.base_subtract = 0
    
    def _build_uniqueid_index(self):
        """Build index of elements by uniqueid for embedinfo linking"""
        for table in self.root.findall('.//XDFTABLE'):
            uid = table.get('uniqueid')
            if uid:
                self.uniqueid_index[uid] = table
        for const in self.root.findall('.//XDFCONSTANT'):
            uid = const.get('uniqueid')
            if uid:
                self.uniqueid_index[uid] = const
    
    def xdf_addr_to_file_offset(self, xdf_address: int) -> int:
        """Convert XDF address to file offset using BASEOFFSET"""
        if self.base_offset == 0:
            return xdf_address
        
        if self.base_subtract == 1:
            # VS/VT memcal style: XDF uses $8000-$FFFF, file starts at 0
            return xdf_address - self.base_offset
        else:
            # VX/VY flash style: file has offset before calibration
            return xdf_address + self.base_offset
    
    def _parse_embedded_data(self, element) -> Dict:
        """Parse EMBEDDEDDATA attributes for address, size, signedness"""
        result = {
            'address': None, 'size_bits': 8, 'signed': False,
            'lsb_first': False, 'row_count': 1, 'col_count': 1
        }
        
        embedded = element.find('.//EMBEDDEDDATA')
        if embedded is None:
            return result
        
        # Address
        addr_str = embedded.get('mmedaddress', '')
        if addr_str:
            try:
                result['address'] = int(addr_str, 16) if addr_str.startswith('0x') else int(addr_str)
            except ValueError:
                pass
        
        # Size
        size_str = embedded.get('mmedelementsizebits', '8')
        try:
            result['size_bits'] = int(size_str)
        except ValueError:
            pass
        
        # Type flags (Bit 0 = Signed, Bit 1 = LSB first)
        flags_str = embedded.get('mmedtypeflags', '0')
        try:
            flags = int(flags_str, 16) if flags_str.startswith('0x') else int(flags_str)
            result['signed'] = bool(flags & 0x01)
            result['lsb_first'] = bool(flags & 0x02)
        except ValueError:
            pass
        
        # Row/column counts
        for key, attr in [('row_count', 'mmedrowcount'), ('col_count', 'mmedcolcount')]:
            val_str = embedded.get(attr, '')
            if val_str:
                try:
                    result[key] = int(val_str)
                except ValueError:
                    pass
        
        return result
    
    def _parse_constant_full(self, const):
        """Parse constant with full metadata"""
        embedded = self._parse_embedded_data(const)
        if embedded['address'] is None:
            return
        
        title_elem = const.find('title')
        title = title_elem.text.strip() if title_elem is not None and title_elem.text else "Unknown"
        
        unit_elem = const.find('.//units')
        unit = unit_elem.text.strip() if unit_elem is not None and unit_elem.text else ""
        
        math_elem = const.find('.//MATH')
        equation = math_elem.get('equation', '') if math_elem is not None else ''
        
        self.constants.append({
            'title': title,
            'address': embedded['address'],
            'file_offset': self.xdf_addr_to_file_offset(embedded['address']),
            'size_bits': embedded['size_bits'],
            'signed': embedded['signed'],
            'unit': unit,
            'equation': equation
        })
    
    def _parse_table_full(self, table):
        """Parse table with axis information"""
        title_elem = table.find('title')
        title = title_elem.text.strip() if title_elem is not None and title_elem.text else "Unknown"
        
        axes = {}
        for axis in table.findall('.//XDFAXIS'):
            axis_id = axis.get('id', 'unknown')
            embedded = self._parse_embedded_data(axis)
            
            # Get axis count
            count_elem = axis.find('.//indexcount')
            count = 1
            if count_elem is not None and count_elem.text:
                try:
                    count = int(count_elem.text.strip())
                except ValueError:
                    pass
            
            axes[axis_id] = {
                'address': embedded['address'],
                'file_offset': self.xdf_addr_to_file_offset(embedded['address']) if embedded['address'] else None,
                'count': count,
                'size_bits': embedded['size_bits'],
                'row_count': embedded['row_count'],
                'col_count': embedded['col_count']
            }
        
        z_axis = axes.get('z', {})
        if z_axis.get('address'):
            self.tables.append({
                'title': title,
                'address': z_axis['address'],
                'file_offset': z_axis['file_offset'],
                'rows': z_axis.get('row_count', 1),
                'cols': z_axis.get('col_count', 1),
                'x_axis': axes.get('x'),
                'y_axis': axes.get('y')
            })


# ============================================================================
# MYSTERY RAM FINDER
# ============================================================================

class MysteryRAMFinder:
    """
    Find and analyze mystery RAM variables referenced in code but not in XDF.
    
    Mystery RAM = addresses used in disassembly that:
    1. Are in RAM range ($0000-$01FF for HC11)
    2. Are NOT defined in the XDF file
    3. Are referenced multiple times in code
    
    Key mystery addresses from The1's spark cut code:
    - $149E, $16FA, $78B2 (mentioned in DOCUMENT_CONSOLIDATION_PLAN.md)
    """
    
    def __init__(self, data: bytes, xdf: Optional[EnhancedXDFParser] = None):
        self.data = data
        self.xdf = xdf
        self.references = defaultdict(list)  # addr -> [(file_offset, instruction)]
    
    def scan_for_ram_references(self, start: int = 0, end: int = None) -> Dict[int, int]:
        """
        Scan binary for all RAM address references
        
        Returns:
            Dict[int, int]: RAM address -> reference count
        """
        if end is None:
            end = len(self.data)
        
        offset = start
        while offset < end - 2:
            opcode = self.data[offset]
            
            # Check for direct addressing ($90-$9F, $D0-$DF)
            if (0x90 <= opcode <= 0x9F) or (0xD0 <= opcode <= 0xDF):
                if offset + 1 < end:
                    ram_addr = self.data[offset + 1]
                    self.references[ram_addr].append((offset, 'DIR'))
                offset += 2
                continue
            
            # Check for extended addressing with RAM ($B0-$BF, $F0-$FF, $70-$7F)
            if opcode in HC11_OPCODES:
                _, mode, length = HC11_OPCODES[opcode]
                if mode == 'ext' and offset + 2 < end:
                    addr = (self.data[offset + 1] << 8) | self.data[offset + 2]
                    # Check if in RAM range ($0000-$01FF)
                    if addr <= 0x01FF:
                        self.references[addr].append((offset, 'EXT'))
                offset += length
            else:
                offset += 1
        
        return {addr: len(refs) for addr, refs in self.references.items()}
    
    def find_mystery_ram(self) -> List[Dict]:
        """Find RAM addresses not defined in XDF"""
        mystery = []
        
        for addr, refs in sorted(self.references.items(), key=lambda x: -len(x[1])):
            if len(refs) < 2:  # Ignore single references
                continue
            
            # Check if defined in XDF
            is_defined = False
            xdf_name = None
            
            if self.xdf:
                cal = self.xdf.lookup(addr)
                if cal:
                    is_defined = True
                    xdf_name = cal[0]
            
            # Check if known VY constant
            for name, const_addr in VY_V6_CONSTANTS.items():
                if addr == const_addr:
                    is_defined = True
                    xdf_name = f"VY_CONST: {name}"
                    break
            
            mystery.append({
                'address': addr,
                'hex': f'${addr:04X}',
                'references': len(refs),
                'is_defined': is_defined,
                'xdf_name': xdf_name,
                'ref_locations': refs[:5]  # First 5 references
            })
        
        return mystery


# ============================================================================
# PLATFORM DETECTOR
# ============================================================================

class PlatformDetector:
    """Auto-detect ECU platform from binary characteristics"""
    
    def __init__(self, data: bytes):
        self.data = data
        self.size = len(data)
    
    def detect(self) -> Tuple[HoldenPlatform, PlatformConfig]:
        """Detect platform from binary size and vectors"""
        # Check size first
        if self.size == 32768:  # 32KB
            # VS or VT memcal
            return self._detect_vs_vt()
        elif self.size == 131072:  # 128KB
            # VX or VY flash
            return self._detect_vx_vy()
        else:
            return HoldenPlatform.UNKNOWN, None
    
    def _detect_vs_vt(self) -> Tuple[HoldenPlatform, PlatformConfig]:
        """Detect VS vs VT from 32KB memcal"""
        # Check reset vector for characteristic patterns
        if self.size >= 2:
            reset_vector = (self.data[-2] << 8) | self.data[-1]
            # VS typically jumps to $C0xx, VT similar
            if 0xC000 <= reset_vector <= 0xC100:
                return HoldenPlatform.VS_V6, PLATFORM_CONFIGS[HoldenPlatform.VS_V6]
        return HoldenPlatform.VT_V6, PLATFORM_CONFIGS[HoldenPlatform.VT_V6]
    
    def _detect_vx_vy(self) -> Tuple[HoldenPlatform, PlatformConfig]:
        """Detect VX vs VY from 128KB flash"""
        # Check for Enhanced ROM signature (zeroed LPG area)
        lpg_start = 0x057AF
        lpg_end = 0x05F73
        
        if lpg_start < self.size and lpg_end < self.size:
            lpg_area = self.data[lpg_start:lpg_end]
            if all(b == 0x00 for b in lpg_area):
                print("[DETECT] Enhanced ROM detected (LPG area zeroed)")
        
        # Check vector table at $1FFD6
        if self.size >= 0x20000:
            vector_offset = 0x1FFD6
            # Check TIC3 vector (should point to ~$35FF for VY)
            tic3_vector = (self.data[vector_offset + 10] << 8) | self.data[vector_offset + 11]
            if 0x3500 <= tic3_vector <= 0x3700:
                return HoldenPlatform.VY_V6, PLATFORM_CONFIGS[HoldenPlatform.VY_V6]
        
        return HoldenPlatform.VX_V6, PLATFORM_CONFIGS[HoldenPlatform.VX_V6]
    
    def get_vector_table(self) -> Dict[str, int]:
        """Extract interrupt vector table"""
        vectors = {}
        
        if self.size == 32768:
            base = 0x7FD6  # Memcal vectors at end of 32KB
        elif self.size == 131072:
            base = 0x1FFD6  # Flash vectors at end of 128KB
        else:
            return vectors
        
        vector_names = [
            'SCI', 'SPI', 'PAIE', 'PAO', 'TOF', 'TIC4_TOC5',
            'TOC4', 'TOC3', 'TOC2', 'TOC1', 'TIC3', 'TIC2', 'TIC1',
            'RTI', 'IRQ', 'XIRQ', 'SWI', 'ILLOP', 'COP', 'CMF', 'RESET'
        ]
        
        offset = base
        for i, name in enumerate(vector_names):
            if offset + 1 < self.size:
                addr = (self.data[offset] << 8) | self.data[offset + 1]
                vectors[name] = addr
                offset += 2
        
        return vectors


# ============================================================================
# CLI INTERFACE (ENHANCED)
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Ultimate ECU Binary Analyzer & Comparator v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
=========

  # Analyze single binary with platform detection
  python ultimate_binary_analyzer.py analyze v1.0a.bin
  
  # Analyze with XDF annotation
  python ultimate_binary_analyzer.py analyze v1.0a.bin --xdf v2.09a.xdf
  
  # Compare v1.0a vs v1.1a with XDF
  python ultimate_binary_analyzer.py compare v1.0a.bin v1.1a.bin --xdf v2.09a.xdf
  
  # Disassemble The1's spark cut code cave
  python ultimate_binary_analyzer.py disasm v1.1a.bin 0x17D84 --length 256
  
  # Find mystery RAM variables
  python ultimate_binary_analyzer.py mystery v1.0a.bin --xdf v2.09a.xdf
  
  # Extract vector table
  python ultimate_binary_analyzer.py vectors v1.0a.bin
  
  # Batch scan directory
  python ultimate_binary_analyzer.py scan R:\\ECU_Bins --find-duplicates
  
  # Export XDF summary
  python ultimate_binary_analyzer.py xdf-info v2.09a.xdf

PLATFORMS SUPPORTED:
===================
  - VS V6 (32KB Memcal, $51)
  - VT V6 (32KB Memcal, $A5G)  
  - VX V6 (128KB Flash, $060A)
  - VY V6 (128KB Flash, $060A)
  - Enhanced ROMs (v1.0a, v1.1a, v2.04c, v2.09a)
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze single binary')
    analyze_parser.add_argument('file', type=Path, help='Binary file to analyze')
    analyze_parser.add_argument('--xdf', type=Path, help='XDF file for annotation')
    analyze_parser.add_argument('--json', action='store_true', help='Output JSON')
    analyze_parser.add_argument('--platform', choices=['vs', 'vt', 'vx', 'vy', 'auto'],
                                default='auto', help='Force platform (default: auto)')
    analyze_parser.add_argument('--output', '-o', type=Path, help='Output file')
    
    # Compare command
    compare_parser = subparsers.add_parser('compare', help='Compare two binaries')
    compare_parser.add_argument('file1', type=Path, help='First binary (e.g., v1.0a.bin)')
    compare_parser.add_argument('file2', type=Path, help='Second binary (e.g., v1.1a.bin)')
    compare_parser.add_argument('--xdf', type=Path, help='XDF file for annotation')
    compare_parser.add_argument('--output', '-o', type=Path, help='Output file')
    compare_parser.add_argument('--focus', type=str, help='Focus on address range (e.g., 0x17D84-0x17E00)')
    compare_parser.add_argument('--annotate', action='store_true', help='Add XDF annotations to diff')
    
    # Disassemble command
    disasm_parser = subparsers.add_parser('disasm', help='Disassemble at offset')
    disasm_parser.add_argument('file', type=Path, help='Binary file')
    disasm_parser.add_argument('offset', type=str, help='Offset (hex or decimal)')
    disasm_parser.add_argument('--length', '-l', type=int, default=64, help='Length in bytes')
    disasm_parser.add_argument('--xdf', type=Path, help='XDF file for annotation')
    disasm_parser.add_argument('--base', type=str, default='0x0000', help='Base address')
    disasm_parser.add_argument('--output', '-o', type=Path, help='Output to file')
    disasm_parser.add_argument('--format', choices=['asm', 'md', 'json'], default='asm',
                                help='Output format')
    
    # Mystery RAM command
    mystery_parser = subparsers.add_parser('mystery', help='Find mystery RAM variables')
    mystery_parser.add_argument('file', type=Path, help='Binary file')
    mystery_parser.add_argument('--xdf', type=Path, help='XDF file to check against')
    mystery_parser.add_argument('--min-refs', type=int, default=2, help='Minimum references')
    mystery_parser.add_argument('--output', '-o', type=Path, help='Output file')
    
    # Vectors command
    vectors_parser = subparsers.add_parser('vectors', help='Extract interrupt vector table')
    vectors_parser.add_argument('file', type=Path, help='Binary file')
    vectors_parser.add_argument('--json', action='store_true', help='Output JSON')
    
    # XDF info command
    xdf_parser = subparsers.add_parser('xdf-info', help='Show XDF file information')
    xdf_parser.add_argument('xdf', type=Path, help='XDF file')
    xdf_parser.add_argument('--list-tables', action='store_true', help='List all tables')
    xdf_parser.add_argument('--list-constants', action='store_true', help='List all constants')
    xdf_parser.add_argument('--search', type=str, help='Search for parameter by name')
    
    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Batch scan directory')
    scan_parser.add_argument('path', type=Path, help='Directory to scan')
    scan_parser.add_argument('--find-duplicates', action='store_true', help='Find duplicates')
    scan_parser.add_argument('--find-matches', action='store_true', help='Find near-matches')
    scan_parser.add_argument('--threshold', type=float, default=95.0, help='Similarity threshold')
    scan_parser.add_argument('--output', '-o', type=Path, help='Output directory')
    scan_parser.add_argument('--extensions', type=str, default='.bin,.ecu,.rom',
                             help='File extensions to scan')
    
    # Hexdump command
    hex_parser = subparsers.add_parser('hexdump', help='Hex dump at offset')
    hex_parser.add_argument('file', type=Path, help='Binary file')
    hex_parser.add_argument('offset', type=str, help='Offset (hex or decimal)')
    hex_parser.add_argument('--length', '-l', type=int, default=256, help='Length in bytes')
    hex_parser.add_argument('--output', '-o', type=Path, help='Output file')
    
    # Find-pattern command
    pattern_parser = subparsers.add_parser('find-pattern', help='Search for byte pattern')
    pattern_parser.add_argument('file', type=Path, help='Binary file')
    pattern_parser.add_argument('pattern', type=str, help='Hex pattern (e.g., B6 00 A2)')
    pattern_parser.add_argument('--max-results', type=int, default=50, help='Maximum results')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Helper to parse offset
    def parse_offset(s: str) -> int:
        s = s.strip()
        if s.startswith('0x') or s.startswith('0X'):
            return int(s, 16)
        if s.startswith('$'):
            return int(s[1:], 16)
        return int(s)
    
    config = AnalyzerConfig()
    if hasattr(args, 'xdf') and args.xdf:
        config.xdf_path = args.xdf
    
    # ====== ANALYZE ======
    if args.command == 'analyze':
        analyzer = BinaryAnalyzer(args.file, config)
        result = analyzer.analyze()
        
        # Add platform detection
        detector = PlatformDetector(analyzer.data)
        platform, platform_config = detector.detect()
        result['platform'] = platform.value
        result['platform_name'] = platform_config.name if platform_config else 'Unknown'
        
        if args.json:
            output = json.dumps(result, indent=2)
            if args.output:
                args.output.write_text(output)
                print(f"[OK] Saved to {args.output}")
            else:
                print(output)
        else:
            print("\n" + "=" * 70)
            print(f" BINARY ANALYSIS: {result['filename']}")
            print("=" * 70)
            print(f" Size:        {result['size_bytes']:,} bytes ({result['size_kb']} KB)")
            print(f" Category:    {result['size_category']}")
            print(f" ECU Type:    {result['ecu_description']}")
            print(f" Platform:    {result['platform_name']}")
            print(f" Signatures:  {', '.join(result['signatures'])}")
            print(f" MD5:         {result['hashes']['md5']}")
            print(f" SHA256:      {result['hashes']['sha256'][:32]}...")
            print(f" Empty Space: {result['empty_space_total']:,} bytes")
            print("=" * 70)
    
    # ====== COMPARE ======
    elif args.command == 'compare':
        comparator = BinaryComparator(args.file1, args.file2, config)
        comparator.print_diff_report()
        
        if args.output:
            result = comparator.compare()
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n[OK] Saved to {args.output}")
    
    # ====== DISASM ======
    elif args.command == 'disasm':
        offset = parse_offset(args.offset)
        base = parse_offset(args.base)
        config.base_address = base
        
        analyzer = BinaryAnalyzer(args.file, config)
        lines = analyzer.disassemble_at(offset, args.length)
        
        header = f"=== DISASSEMBLY @ 0x{offset:06X} (Base: 0x{base:04X}) ===\n"
        
        if args.format == 'md':
            output = f"# Disassembly at 0x{offset:06X}\n\n```asm\n"
            output += '\n'.join(lines)
            output += "\n```\n"
        elif args.format == 'json':
            output = json.dumps({'offset': offset, 'base': base, 'lines': lines}, indent=2)
        else:
            output = header + '\n'.join(lines)
        
        if args.output:
            args.output.write_text(output)
            print(f"[OK] Saved to {args.output}")
        else:
            print(f"\n{output}")
    
    # ====== MYSTERY RAM ======
    elif args.command == 'mystery':
        data = args.file.read_bytes()
        xdf = None
        if args.xdf:
            xdf = EnhancedXDFParser(args.xdf, data)
        
        finder = MysteryRAMFinder(data, xdf)
        finder.scan_for_ram_references()
        mystery = finder.find_mystery_ram()
        
        print("\n" + "=" * 70)
        print(" MYSTERY RAM ANALYSIS")
        print("=" * 70)
        print(f" File: {args.file.name}")
        print(f" XDF:  {args.xdf.name if args.xdf else 'None'}")
        print("=" * 70)
        
        undefined = [m for m in mystery if not m['is_defined']]
        defined = [m for m in mystery if m['is_defined']]
        
        print(f"\n UNDEFINED RAM VARIABLES ({len(undefined)}):\n")
        for m in undefined[:30]:
            print(f"   {m['hex']:8s}  refs={m['references']:3d}  [MYSTERY]")
        
        print(f"\n KNOWN RAM VARIABLES ({len(defined)}):\n")
        for m in defined[:20]:
            print(f"   {m['hex']:8s}  refs={m['references']:3d}  {m['xdf_name']}")
    
    # ====== VECTORS ======
    elif args.command == 'vectors':
        data = args.file.read_bytes()
        detector = PlatformDetector(data)
        vectors = detector.get_vector_table()
        
        if args.json:
            print(json.dumps(vectors, indent=2))
        else:
            print("\n" + "=" * 50)
            print(f" INTERRUPT VECTOR TABLE: {args.file.name}")
            print("=" * 50)
            for name, addr in vectors.items():
                print(f"   {name:12s}  ${addr:04X}")
    
    # ====== XDF-INFO ======
    elif args.command == 'xdf_info' or args.command == 'xdf-info':
        xdf = EnhancedXDFParser(args.xdf)
        
        print("\n" + "=" * 60)
        print(f" XDF INFO: {xdf.definition_name}")
        print("=" * 60)
        print(f" File:       {args.xdf.name}")
        print(f" BASEOFFSET: {xdf.base_offset} (subtract={xdf.base_subtract})")
        print(f" Tables:     {len(xdf.tables)}")
        print(f" Constants:  {len(xdf.constants)}")
        print(f" Total Addr: {len(xdf.calibrations)}")
        
        if hasattr(args, 'search') and args.search:
            print(f"\n Searching for '{args.search}'...\n")
            for table in xdf.tables:
                if args.search.lower() in table['title'].lower():
                    print(f"   [TABLE] {table['title']} @ 0x{table['address']:X}")
            for const in xdf.constants:
                if args.search.lower() in const['title'].lower():
                    print(f"   [CONST] {const['title']} @ 0x{const['address']:X}")
        
        if hasattr(args, 'list_tables') and args.list_tables:
            print("\n TABLES:\n")
            for t in xdf.tables[:50]:
                print(f"   0x{t['address']:05X}  {t['title'][:50]}")
        
        if hasattr(args, 'list_constants') and args.list_constants:
            print("\n CONSTANTS:\n")
            for c in xdf.constants[:50]:
                print(f"   0x{c['address']:05X}  {c['title'][:50]}")
    
    # ====== SCAN ======
    elif args.command == 'scan':
        if args.output:
            config.output_dir = args.output
        
        batch = BatchBinaryAnalyzer(args.path, config)
        extensions = [e.strip() for e in args.extensions.split(',')]
        batch.scan(extensions)
        
        if args.find_duplicates:
            batch.find_duplicates()
        
        if args.find_matches:
            batch.find_near_matches(args.threshold)
        
        batch.export_results()
    
    # ====== HEXDUMP ======
    elif args.command == 'hexdump':
        offset = parse_offset(args.offset)
        analyzer = BinaryAnalyzer(args.file, config)
        
        output = f"=== HEX DUMP @ 0x{offset:06X} ===\n\n"
        output += analyzer.hex_dump(offset, args.length)
        
        if args.output:
            args.output.write_text(output)
            print(f"[OK] Saved to {args.output}")
        else:
            print(f"\n{output}")
    
    # ====== FIND-PATTERN ======
    elif args.command == 'find-pattern':
        data = args.file.read_bytes()
        
        # Parse hex pattern
        pattern_str = args.pattern.replace(' ', '').replace('-', '')
        try:
            pattern = bytes.fromhex(pattern_str)
        except ValueError:
            print(f"[ERROR] Invalid hex pattern: {args.pattern}")
            return
        
        print(f"\n Searching for: {pattern.hex(' ').upper()}")
        print(f" In file: {args.file.name}\n")
        
        results = []
        offset = 0
        while offset < len(data) - len(pattern):
            idx = data.find(pattern, offset)
            if idx == -1:
                break
            results.append(idx)
            offset = idx + 1
            if len(results) >= args.max_results:
                break
        
        print(f" Found {len(results)} matches:\n")
        for r in results:
            context = data[max(0, r-4):r+len(pattern)+4].hex(' ').upper()
            print(f"   0x{r:06X}:  {context}")

# ============================================================================
# QUICK FUNCTIONS FOR INTERACTIVE USE (Python REPL / Jupyter)
# ============================================================================

def quick_compare(file1: str, file2: str, xdf: str = None):
    """
    Quick comparison for interactive use.
    
    Example:
        from ultimate_binary_analyzer import quick_compare
        result = quick_compare('v1.0a.bin', 'v1.1a.bin', 'v2.09a.xdf')
    """
    config = AnalyzerConfig()
    if xdf:
        config.xdf_path = Path(xdf)
    comparator = BinaryComparator(Path(file1), Path(file2), config)
    comparator.print_diff_report()
    return comparator.compare()


def quick_disasm(filepath: str, offset: int, length: int = 64, xdf: str = None):
    """
    Quick disassembly for interactive use.
    
    Example:
        from ultimate_binary_analyzer import quick_disasm
        lines = quick_disasm('v1.1a.bin', 0x17D84, 256)  # The1's spark cut
        for line in lines: print(line)
    """
    config = AnalyzerConfig()
    if xdf:
        config.xdf_path = Path(xdf)
    analyzer = BinaryAnalyzer(Path(filepath), config)
    return analyzer.disassemble_at(offset, length)


def quick_analyze(filepath: str):
    """
    Quick analysis for interactive use.
    
    Example:
        from ultimate_binary_analyzer import quick_analyze
        info = quick_analyze('v1.0a.bin')
        print(info['platform'], info['hashes']['md5'])
    """
    analyzer = BinaryAnalyzer(Path(filepath))
    result = analyzer.analyze()
    
    # Add platform detection
    detector = PlatformDetector(analyzer.data)
    platform, platform_config = detector.detect()
    result['platform'] = platform.value
    result['platform_name'] = platform_config.name if platform_config else 'Unknown'
    
    return result


def quick_mystery(filepath: str, xdf: str = None):
    """
    Find mystery RAM variables for interactive use.
    
    Example:
        from ultimate_binary_analyzer import quick_mystery
        mystery = quick_mystery('v1.0a.bin', 'v2.09a.xdf')
        for m in mystery[:20]: print(m['hex'], m['references'], m['is_defined'])
    """
    data = Path(filepath).read_bytes()
    xdf_parser = None
    if xdf:
        xdf_parser = EnhancedXDFParser(Path(xdf), data)
    
    finder = MysteryRAMFinder(data, xdf_parser)
    finder.scan_for_ram_references()
    return finder.find_mystery_ram()


def quick_vectors(filepath: str):
    """
    Get interrupt vectors for interactive use.
    
    Example:
        from ultimate_binary_analyzer import quick_vectors
        vecs = quick_vectors('v1.0a.bin')
        print(f"TIC3 ISR: ${vecs['TIC3']:04X}")  # Should be $35FF
    """
    data = Path(filepath).read_bytes()
    detector = PlatformDetector(data)
    return detector.get_vector_table()


def quick_xdf(xdf_path: str):
    """
    Load and parse XDF for interactive use.
    
    Example:
        from ultimate_binary_analyzer import quick_xdf
        xdf = quick_xdf('v2.09a.xdf')
        print(xdf.definition_name, xdf.base_offset)
        print(len(xdf.tables), 'tables')
    """
    return EnhancedXDFParser(Path(xdf_path))


# ============================================================================
# VY V6 SPECIFIC HELPERS
# ============================================================================

def disasm_tic3_isr(filepath: str = None, xdf: str = None) -> List[str]:
    """
    Disassemble the TIC3 ISR (3X cam signal handler) at $35FF.
    This is the main timing interrupt for spark control.
    
    Example:
        lines = disasm_tic3_isr('v1.0a.bin')
    """
    if filepath is None:
        # Try common locations
        for path in ['v1.0a.bin', 'VX-VY_V6_$060A_Enhanced_v1.0a.bin']:
            if Path(path).exists():
                filepath = path
                break
    
    if filepath is None:
        raise FileNotFoundError("No binary file found. Specify filepath.")
    
    # TIC3 ISR is at $35FF, disassemble 282 bytes to cover full handler
    return quick_disasm(filepath, 0x35FF, 282, xdf)


def disasm_dwell_calc(filepath: str = None, xdf: str = None) -> List[str]:
    """
    Disassemble the dwell calculation subroutine at $371A.
    Called from TIC3 ISR, this calculates spark timing.
    
    Example:
        lines = disasm_dwell_calc('v1.0a.bin')
    """
    if filepath is None:
        for path in ['v1.0a.bin', 'VX-VY_V6_$060A_Enhanced_v1.0a.bin']:
            if Path(path).exists():
                filepath = path
                break
    
    if filepath is None:
        raise FileNotFoundError("No binary file found. Specify filepath.")
    
    # Dwell calc at $371A
    return quick_disasm(filepath, 0x371A, 128, xdf)


def disasm_the1_spark_cut(filepath: str = None, xdf: str = None) -> List[str]:
    """
    Disassemble The1's spark cut code cave at $17D84.
    This is where the Enhanced ROM v1.1a puts custom spark cut code.
    
    NOTE: This area is empty (0xFF) in v1.0a. Use v1.1a binary.
    
    Example:
        lines = disasm_the1_spark_cut('v1.1a.bin')
    """
    if filepath is None:
        for path in ['v1.1a.bin', 'VX-VY_V6_$060A_Enhanced_v1.1a.bin']:
            if Path(path).exists():
                filepath = path
                break
    
    if filepath is None:
        raise FileNotFoundError("No v1.1a binary found. Specify filepath.")
    
    # The1's spark cut code cave
    return quick_disasm(filepath, 0x17D84, 256, xdf)


def compare_v10a_v11a(bin_dir: str = '.', xdf: str = None) -> Dict:
    """
    Compare v1.0a and v1.1a Enhanced ROM binaries.
    Shows differences, focusing on spark cut implementation.
    
    Example:
        result = compare_v10a_v11a('R:/VY_V6_Assembly_Modding/bins/')
    """
    bin_path = Path(bin_dir)
    
    # Find binaries
    v10a = None
    v11a = None
    
    for f in bin_path.glob('*1.0a*.bin'):
        v10a = f
    for f in bin_path.glob('*1.1a*.bin'):
        v11a = f
    
    if not v10a or not v11a:
        raise FileNotFoundError(
            f"Could not find v1.0a and v1.1a binaries in {bin_dir}"
        )
    
    return quick_compare(str(v10a), str(v11a), xdf)


if __name__ == '__main__':
    main()
