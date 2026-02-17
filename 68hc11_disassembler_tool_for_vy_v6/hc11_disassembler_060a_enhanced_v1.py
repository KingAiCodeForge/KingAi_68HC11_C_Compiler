#!/usr/bin/env python3
"""
hc11_disassembler_060a_enhanced_v1.py
=====================================
Motorola 68HC11 Disassembler for GM/Delco $060A Enhanced OS v1.0a Binary

Target Binary:  VX-VY_V6_$060A_Enhanced_v1.0a.bin (128KB, 92118883 MEMCAL)
Target XDF:     VX VY_V6_$060A_Enhanced_v2.09b-beta.xdf (2234 definitions)
                XDF version mapping:
                  Enhanced v1.0a → v2.09b-beta (2234 defs) or v2.09a (1757 defs)
                  Enhanced v1.1a (spark cut by The1) → v2.04
                  STOCK 92118883 → v2.62
Target CPU:     Motorola 68HC11F1 (MC68HC11FC0 mask set)
Target Vehicle: 2002-2004 Holden VY Commodore 3.8L Ecotec V6 (L36/L67)
OS:             THE1 Enhanced OS ($060A), version 1.0a

*** THIS DISASSEMBLER IS SPECIFIC TO THE ENHANCED v1.0a BINARY ***
To support other bins (STOCK 92118883, Enhanced v1.1a, VX variants),
clone this script and update the binary layout, XDF path, and address maps.

FEATURES:
- Full 312-opcode HC11 instruction decode (all 4 pages: base + $18/$1A/$CD)
- TunerPro XDF integration: loads 2234 calibration definitions as labels
- RPM comparison detection: flags CMPA/CMPB against known RPM thresholds
- Timer/IO access tracking: identifies reads/writes to HC11 hardware registers
- Calibration cross-reference: annotates code that reads XDF-defined parameters
- ISR vector table parsing: traces all interrupt service routine entry points
- Named HC11 I/O registers ($1000-$103F): PORTA, TCTL1, TCNT, ADR1, etc.

ADDRESS FORMAT NOTES:
- XDF addresses:  File offset (e.g., 0x77DE = byte 0x77DE in the .bin file)
- CPU addresses:  Runtime address in HC11 memory map (0x0000-0xFFFF per bank)
- RAM:            $0000-$01FF (zero page + extended on-chip RAM)
- I/O Registers:  $1000-$103F (memory-mapped hardware control/status)
- Calibration:    $4000-$7FFF (XDF parameters in ROM, read-only at runtime)
- Program ROM:    $8000-$FFFF (executable code, banked in 128KB binary)

VY V6 128KB BINARY LAYOUT (3 banks):
- File 0x00000-0x0FFFF (64KB) = Bank 1: Calibration + low-bank code
- File 0x10000-0x17FFF (32KB) = Bank 2: Engine code  (maps to CPU $8000-$FFFF)
- File 0x18000-0x1FFFF (32KB) = Bank 3: Trans/diag   (maps to CPU $8000-$FFFF)
- Address formula: CPU_addr = file_offset - 0x10000

PREBYTE INSTRUCTIONS (0x18, 0x1A, 0xCD):
- 0x18: Y-register operations (LDY, STY, CPY, etc.)
- 0x1A: CPD (Compare D), LDY/STY indexed X, CPY indexed X
- 0xCD: Y-indexed operations for CPD, CPX, LDX

DEPENDENCIES (all stdlib except local modules):
- hc11_opcodes_complete.py  -- 312 opcode definitions (4 pages)
- core/cli_base.py          -- argument parsing and logging
- core/opcodes.py           -- opcode decode engine and addressing modes
- core/output_manager.py    -- output formatting (txt/json/csv/md)
- core/vy_v6_constants.py   -- VY V6 memory map, vector table, register names

HISTORY:
- Nov 2025:  Initial version (hc11_disassembler.py) with ~80 opcodes
- Jan 2026:  Merged hc11_disassembler_complete.py + _enhanced.py into single tool
- Jan 20:    v2.0 - XDF auto-detection, progress tracking, full register map
- Feb 14:    v2.1 - Renamed to hc11_disassembler_060a_enhanced_v1.py for GitHub
             Verified: 312 opcodes, 1757 XDF defs loaded, all pages correct

Author: KingAI Automotive Research
License: MIT
Version: 2.1.0
"""

import sys
import os
import csv

# ====================================================================
# PLATFORM COMPATIBILITY
# Windows terminal encoding fix — must run before ANY print() call.
# Without this, Unicode characters in XDF labels crash on Windows cmd.
# ====================================================================
if sys.platform == 'win32' and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass  # Ignore if already configured or not supported
from pathlib import Path
from typing import Dict, Tuple, List, Optional

# ====================================================================
# MODULE IMPORTS — GRACEFUL DEGRADATION
# The disassembler works standalone with reduced features if core/
# modules are missing. Each import block sets a HAS_* flag.
# ====================================================================

# Import core utilities (argument parsing, opcode engine, output formatting)
sys.path.insert(0, str(Path(__file__).parent / "core"))
try:
    from cli_base import CLIBase
    from opcodes import HC11_OPCODES
    from output_manager import OutputManager
    HAS_CORE_UTILS = True
except ImportError:
    print("WARNING: Core utilities not found. Run from tools/ directory.")
    HAS_CORE_UTILS = False
    CLIBase = object

# Import verified constants for RAM addresses, vector table, and register names
# from vy_v6_constants.py — the single source of truth for the VY V6 memory map
try:
    from vy_v6_constants import (
        RAM_ADDRESSES as VERIFIED_RAM_ADDRESSES, 
        HC11_REGISTERS as VERIFIED_HC11_REGISTERS, 
        BINARY_PATH,
        VECTOR_TABLE,
        JUMP_TABLE,
        FILE_OFFSETS,
        TIMING
    )
    HAS_VERIFIED_CONSTANTS = True
except ImportError:
    HAS_VERIFIED_CONSTANTS = False
    VERIFIED_RAM_ADDRESSES = {}
    VERIFIED_HC11_REGISTERS = {}
    BINARY_PATH = None
    VECTOR_TABLE = {}
    JUMP_TABLE = {}
    FILE_OFFSETS = {}
    TIMING = None

# Import the complete 312-opcode HC11 instruction set from hc11_opcodes_complete.py
# This covers all 4 opcode pages: base (236) + $18 page2 (65) + $1A page3 (7) + $CD page4 (4)
try:
    from hc11_opcodes_complete import (
        decode_opcode as complete_decode_opcode,
        format_instruction as complete_format_instruction,
        is_rpm_comparison,
        is_timer_io_access,
        OPCODES_SINGLE,
        OPCODES_PAGE1,
        OPCODES_PAGE2,
        OPCODES_PAGE3
    )
    HAS_COMPLETE_OPCODES = True
    print("[OK] Loaded complete HC11 opcode module (312 opcodes)")
except ImportError:
    HAS_COMPLETE_OPCODES = False
    is_rpm_comparison = None
    is_timer_io_access = None
    OPCODES_SINGLE = {}
    OPCODES_PAGE1 = {}
    OPCODES_PAGE2 = {}
    OPCODES_PAGE3 = {}
    
import xml.etree.ElementTree as ET
from datetime import datetime

# ====================================================================
# HC11F Direct Page Register Definitions (VY V6 ECU Specific)
# The VY V6 uses HC11F-family (68HC11FC0), NOT HC11E9.
# HC11F has PORTG/DDRG/PORTF at $02/$03/$05 instead of PIOC/PORTC/PORTCL.
# These map to CPU addresses 0x1000+ (memory-mapped I/O via offset)
# ====================================================================

HC11_DIRECT_PAGE_REGISTERS = {
    0x00: "PORTA",    # Port A Data Register
    0x01: "DDRA",     # Port A Data Direction (HC11F only)
    0x02: "PORTG",    # Port G Data — bank switching bit 6 (NOT PIOC)
    0x03: "DDRG",     # Port G Data Direction (NOT PORTC)
    0x04: "PORTB",    # Port B Data Register
    0x05: "PORTF",    # Port F Data (HC11F only — NOT PORTCL)
    0x06: "PORTC",    # Port C Data (shifted from $03 in HC11E)
    0x07: "DDRC",     # Port C Data Direction
    0x08: "PORTD",    # Port D Data Register
    0x09: "DDRD",     # Port D Data Direction
    0x0A: "PORTE",    # Port E Data Register
    0x0B: "CFORC",    # Timer Compare Force
    0x0C: "OC1M",     # OC1 Mask
    0x0D: "OC1D",     # OC1 Data
    0x0E: "TCNT_HI",  # Timer Count (High)
    0x0F: "TCNT_LO",  # Timer Count (Low)
    0x10: "TIC1_HI",  # Input Capture 1 (High)
    0x11: "TIC1_LO",  # Input Capture 1 (Low)
    0x12: "TIC2_HI",  # Input Capture 2 (High)
    0x13: "TIC2_LO",  # Input Capture 2 (Low)
    0x14: "TIC3_HI",  # Input Capture 3 (High)
    0x15: "TIC3_LO",  # Input Capture 3 (Low)
    0x16: "TOC1_HI",  # Output Compare 1 (High)
    0x17: "TOC1_LO",  # Output Compare 1 (Low)
    0x18: "TOC2_HI",  # Output Compare 2 (High)
    0x19: "TOC2_LO",  # Output Compare 2 (Low)
    0x1A: "TOC3_HI",  # Output Compare 3 (High)
    0x1B: "TOC3_LO",  # Output Compare 3 (Low)
    0x1C: "TOC4_HI",  # Output Compare 4 (High)
    0x1D: "TOC4_LO",  # Output Compare 4 (Low)
    0x1E: "TI4O5_HI", # TI4/O5 (High)
    0x1F: "TI4O5_LO", # TI4/O5 (Low)
    0x20: "TCTL1",    # Timer Control 1 (output compare modes)
    0x21: "TCTL2",    # Timer Control 2 (input capture edges)
    0x22: "TMSK1",    # Timer Mask 1 (interrupt enables)
    0x23: "TFLG1",    # Timer Flag 1 (interrupt flags)
    0x24: "TMSK2",    # Timer Mask 2
    0x25: "TFLG2",    # Timer Flag 2
    0x26: "PACTL",    # Pulse Accumulator Control
    0x27: "PACNT",    # Pulse Accumulator Count
    0x28: "SPCR",     # SPI Control Register
    0x29: "SPSR",     # SPI Status Register
    0x2A: "SPDR",     # SPI Data Register
    0x2B: "BAUD",     # SCI Baud Rate
    0x2C: "SCCR1",    # SCI Control 1
    0x2D: "SCCR2",    # SCI Control 2
    0x2E: "SCSR",     # SCI Status Register
    0x2F: "SCDR",     # SCI Data Register
    0x30: "ADCTL",    # A/D Control Register
    0x31: "ADR1",     # A/D Result 1
    0x32: "ADR2",     # A/D Result 2
    0x33: "ADR3",     # A/D Result 3
    0x34: "ADR4",     # A/D Result 4
    0x39: "OPTION",   # System Configuration Options
    0x3A: "COPRST",   # COP Reset Register
    0x3B: "PPROG",    # EEPROM Programming Control
    0x3D: "INIT",     # RAM/IO Mapping Register
    0x3E: "TEST1",    # Test Register 1
    0x3F: "CONFIG",   # Configuration Register
}

# VY V6 RAM Variables (from XDF analysis - common addresses)
VY_V6_RAM_VARIABLES = {
    0x9D: "RPM_16BIT_LO",   # 16-bit RPM (low byte) - used by The1's spark cut
    0x9E: "RPM_16BIT_HI",   # 16-bit RPM (high byte)
    0xA2: "RPM_8BIT",       # 8-bit RPM (÷25, max 6375)
    0xA3: "ENGINE_STATE",   # Engine state flags
}


def find_vy_binaries():
    """Search for VY V6 Enhanced binaries in common locations"""
    search_paths = [
        Path(r"A:\VY_V6_Assembly_Modding"),
        Path(r"A:\VY_V6_Assembly_Modding\bins"),
        Path(r"R:\VY_V6_Assembly_Modding\bins"),
        Path(r"R:\VY_V6_Assembly_Modding\test_bins"),
        Path(r"C:\Repos\Holden_Analysis"),
        Path(r"A:\repos\Holden_Analysis"),
        Path(r"A:\repos\VY_V6_Assembly_Modding\bins"),
        Path.cwd(),
        Path.cwd().parent,
    ]
    
    bin_patterns = [
        "*Enhanced*.bin",
        "*enhanced*.bin",
        "*$060A*.bin",
        "*92118883*.bin",
        "*VY_V6*.bin",
        "*VY*.bin",
        "*_STOCK.bin",
    ]
    
    found_bins = []
    for search_path in search_paths:
        if search_path.exists():
            for pattern in bin_patterns:
                found_bins.extend(search_path.rglob(pattern))
    
    # Remove duplicates and sort by name
    return sorted(set(found_bins), key=lambda p: p.name)


def find_xdf_files():
    """Search for XDF definition files in common locations"""
    search_paths = [
        Path(r"A:\VY_V6_Assembly_Modding"),
        Path(r"A:\VY_V6_Assembly_Modding\xdfs_and_adx_and_bins_related_to_project"),
        Path(r"C:\Users\jason\OneDrive\Documents\TunerPro Files"),
        Path(r"R:\VY_V6_Assembly_Modding\xdfs"),
        Path(r"A:\repos\VY_V6_Assembly_Modding\xdfs"),
        Path(r"E:\Users\jason\Documents\TunerPro Files"),
        Path.cwd(),
    ]
    
    found_xdfs = []
    for search_path in search_paths:
        if search_path.exists():
            found_xdfs.extend(search_path.rglob("*.xdf"))
    
    # Remove duplicates, prefer Enhanced versions
    unique = sorted(set(found_xdfs), key=lambda p: (
        0 if "Enhanced" in p.name else 1,
        0 if "v2.09" in p.name else 1,
        p.name
    ))
    return unique


def load_xdf_labels(xdf_path):
    """Load address labels from XDF file (simplified parser)
    
    Returns dict of {address: label_name}
    """
    labels = {}
    
    try:
        tree = ET.parse(xdf_path)
        root = tree.getroot()
        
        # Extract table addresses and titles
        for table in root.findall(".//XDFTABLE"):
            title_elem = table.find("title")
            addr_elem = table.find(".//mmedaddress")
            
            if title_elem is not None and addr_elem is not None:
                if addr_elem.text:
                    title = title_elem.text
                    try:
                        addr = int(addr_elem.text, 16)
                        labels[addr] = title
                    except ValueError:
                        pass
        
        # Extract constant addresses
        for constant in root.findall(".//XDFCONSTANT"):
            title_elem = constant.find("title")
            addr_elem = constant.find("mmedaddress")
            
            if title_elem is not None and addr_elem is not None:
                if addr_elem.text:
                    title = title_elem.text
                    try:
                        addr = int(addr_elem.text, 16)
                        labels[addr] = title
                    except ValueError:
                        pass
        
        print(f"[OK] Loaded {len(labels)} labels from {xdf_path.name}")
        
    except Exception as e:
        print(f"[WARN] Could not load XDF labels: {e}")
    
    return labels


class XDFCalibrationDB:
    """Load and lookup XDF calibration data"""
    
    def __init__(self):
        self.calibrations = {}  # addr -> (title, type, category)
        self.rpm_scaling_x25 = {  # Known RPM tables with x25 scaling
            0x77DE, 0x77DD  # Rev limiter and related
        }
        self.load_xdf_data()
    
    def load_xdf_data(self):
        """Load all XDF CSV files"""
        xdf_dir = Path(__file__).parent.parent / "xdf_analysis"
        
        # Try v2.09a first (most complete for Enhanced v1.0a), then others
        # XDF ↔ Binary mapping:
        #   Enhanced v1.0a → v2.09b-beta / v2.09a
        #   Enhanced v1.1a (The1's spark cut) → v2.04
        #   STOCK 92118883 → v2.62
        for version in ["v2.09a", "v2.62", "v1.2", "v0.9h"]:
            version_dir = xdf_dir / version
            if not version_dir.exists():
                continue
            
            # Try full_data.csv first (has all fields)
            csv_patterns = ["*full_data.csv", "*addresses.csv"]
            for pattern in csv_patterns:
                for csv_file in version_dir.glob(pattern):
                    try:
                        with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
                            reader = csv.DictReader(f)
                            for row in reader:
                                addr_str = (row.get('address', '') or row.get('Address', '')).upper().replace('X', 'x')
                                title = row.get('title', '') or row.get('Title', '')
                                type_str = row.get('type', '') or row.get('Type', '')
                                category = row.get('category_name', '') or row.get('category', '') or ''
                                
                                if addr_str and addr_str.startswith('0x'):
                                    try:
                                        addr = int(addr_str, 16)
                                        if addr not in self.calibrations:  # Keep first
                                            self.calibrations[addr] = (title, type_str, category)
                                    except ValueError:
                                        pass
                    except Exception as e:
                        print(f"Warning: Could not load {csv_file}: {e}")
                if self.calibrations:  # Stop after first successful load
                    break
        
        print(f"[OK] Loaded {len(self.calibrations)} calibration definitions from XDF")
    
    def lookup(self, addr: int) -> Optional[Tuple[str, str, str]]:
        """Look up calibration by address"""
        return self.calibrations.get(addr)

class HC11Disassembler:
    """Motorola 68HC11 instruction decoder with XDF integration.
    
    This class implements a linear-sweep disassembler for the MC68HC11FC0
    processor used in GM/Delco VY V6 ECUs. It decodes raw binary into
    assembly mnemonics, annotating each instruction with:
    - XDF calibration label (if the address is a known XDF parameter)
    - HC11 I/O register name (if accessing $1000-$103F range)
    - RPM comparison flag (if comparing against a known RPM threshold)
    - Verified RAM variable name (if accessing a mapped RAM location)
    
    The built-in OPCODES dict handles common instructions for standalone use.
    When hc11_opcodes_complete.py is available, all 312 opcodes are decoded.
    """
    
    # HC11 instruction set (partial - common opcodes)
    OPCODES = {
        # Load/Store instructions
        0x86: ("LDAA", "imm", 2),   # Load A immediate
        0x96: ("LDAA", "dir", 2),   # Load A direct (zero page)
        0xB6: ("LDAA", "ext", 3),   # Load A extended
        0xC6: ("LDAB", "imm", 2),   # Load B immediate
        0xD6: ("LDAB", "dir", 2),   # Load B direct
        0xF6: ("LDAB", "ext", 3),   # Load B extended
        0xCC: ("LDD", "imm", 3),    # Load D (A:B) immediate
        0xDC: ("LDD", "dir", 2),    # Load D direct
        0xFC: ("LDD", "ext", 3),    # Load D extended
        0xCE: ("LDX", "imm", 3),    # Load X immediate
        0xDE: ("LDX", "dir", 2),    # Load X direct
        0xFE: ("LDX", "ext", 3),    # Load X extended
        0x97: ("STAA", "dir", 2),   # Store A direct
        0xB7: ("STAA", "ext", 3),   # Store A extended
        0xD7: ("STAB", "dir", 2),   # Store B direct
        0xF7: ("STAB", "ext", 3),   # Store B extended
        0xDD: ("STD", "dir", 2),    # Store D direct
        0xFD: ("STD", "ext", 3),    # Store D extended
        0xDF: ("STX", "dir", 2),    # Store X direct
        0xFF: ("STX", "ext", 3),    # Store X extended
        
        # Compare instructions
        0x81: ("CMPA", "imm", 2),   # Compare A immediate
        0x91: ("CMPA", "dir", 2),   # Compare A direct
        0xB1: ("CMPA", "ext", 3),   # Compare A extended
        0xC1: ("CMPB", "imm", 2),   # Compare B immediate
        0xD1: ("CMPB", "dir", 2),   # Compare B direct
        0xF1: ("CMPB", "ext", 3),   # Compare B extended
        
        # Branch instructions (complete set 0x20-0x2F)
        0x20: ("BRA", "rel", 2),    # Branch always
        0x21: ("BRN", "rel", 2),    # Branch never
        0x22: ("BHI", "rel", 2),    # Branch if higher (unsigned)
        0x23: ("BLS", "rel", 2),    # Branch if lower or same (unsigned)
        0x24: ("BCC", "rel", 2),    # Branch if carry clear (BHS)
        0x25: ("BCS", "rel", 2),    # Branch if carry set (BLO)
        0x26: ("BNE", "rel", 2),    # Branch if not equal
        0x27: ("BEQ", "rel", 2),    # Branch if equal
        0x28: ("BVC", "rel", 2),    # Branch if overflow clear
        0x29: ("BVS", "rel", 2),    # Branch if overflow set
        0x2A: ("BPL", "rel", 2),    # Branch if plus (N=0)
        0x2B: ("BMI", "rel", 2),    # Branch if minus (N=1)
        0x2C: ("BGE", "rel", 2),    # Branch if >= (signed)
        0x2D: ("BLT", "rel", 2),    # Branch if < (signed)
        0x2E: ("BGT", "rel", 2),    # Branch if > (signed)
        0x2F: ("BLE", "rel", 2),    # Branch if <= (signed)
        
        # Subroutine calls
        0xBD: ("JSR", "ext", 3),    # Jump to subroutine
        0x8D: ("BSR", "rel", 2),    # Branch to subroutine
        0x39: ("RTS", "imp", 1),    # Return from subroutine
        
        # Stack operations
        0x36: ("PSHA", "imp", 1),   # Push A
        0x37: ("PSHB", "imp", 1),   # Push B
        0x3C: ("PSHX", "imp", 1),   # Push X
        0x38: ("PULX", "imp", 1),   # Pull X
        0x32: ("PULA", "imp", 1),   # Pull A
        0x33: ("PULB", "imp", 1),   # Pull B
        
        # Arithmetic
        0x8B: ("ADDA", "imm", 2),   # Add to A immediate
        0x9B: ("ADDA", "dir", 2),   # Add to A direct
        0xBB: ("ADDA", "ext", 3),   # Add to A extended
        0xC3: ("ADDD", "imm", 3),   # Add to D immediate
        0x80: ("SUBA", "imm", 2),   # Subtract from A immediate
        0x90: ("SUBA", "dir", 2),   # Subtract from A direct
        0xB0: ("SUBA", "ext", 3),   # Subtract from A extended
        
        # Logic
        0x84: ("ANDA", "imm", 2),   # AND A immediate
        0x85: ("BITA", "imm", 2),   # Bit test A immediate
        0xC4: ("ANDB", "imm", 2),   # AND B immediate
        0xC5: ("BITB", "imm", 2),   # Bit test B immediate
        
        # Shifts and single-register operations
        0x43: ("COMA", "imp", 1),   # Complement A (1's complement)
        0x48: ("ASLA", "imp", 1),   # Arithmetic shift left A
        0x49: ("ROLA", "imp", 1),   # Rotate left A
        0x4A: ("DECA", "imp", 1),   # Decrement A
        0x4C: ("INCA", "imp", 1),   # Increment A
        0x4D: ("TSTA", "imp", 1),   # Test A
        0x4F: ("CLRA", "imp", 1),   # Clear A
        0x53: ("COMB", "imp", 1),   # Complement B (1's complement)
        0x5F: ("CLRB", "imp", 1),   # Clear B
        
        # Index register operations
        0x08: ("INX", "imp", 1),    # Increment X
        0x09: ("DEX", "imp", 1),    # Decrement X
        
        # Indexed X addressing mode (Row A - register A operations)
        0xA0: ("SUBA", "idx", 2),   # Subtract from A indexed
        0xA1: ("CMPA", "idx", 2),   # Compare A indexed
        0xA2: ("SBCA", "idx", 2),   # Subtract with carry A indexed
        0xA4: ("ANDA", "idx", 2),   # AND A indexed
        0xA5: ("BITA", "idx", 2),   # Bit test A indexed
        0xA6: ("LDAA", "idx", 2),   # Load A indexed
        0xA7: ("STAA", "idx", 2),   # Store A indexed
        0xA8: ("EORA", "idx", 2),   # XOR A indexed
        0xA9: ("ADCA", "idx", 2),   # Add with carry A indexed
        0xAA: ("ORAA", "idx", 2),   # OR A indexed
        0xAB: ("ADDA", "idx", 2),   # Add A indexed
        0xAC: ("CPX", "idx", 2),    # Compare X indexed
        0xAD: ("JSR", "idx", 2),    # Jump to subroutine indexed
        0xAE: ("LDS", "idx", 2),    # Load stack pointer indexed
        0xAF: ("STS", "idx", 2),    # Store stack pointer indexed
        
        # Indexed X addressing mode (Row E - register B/D operations)
        0xE0: ("SUBB", "idx", 2),   # Subtract from B indexed
        0xE1: ("CMPB", "idx", 2),   # Compare B indexed
        0xE2: ("SBCB", "idx", 2),   # Subtract with carry B indexed
        0xE3: ("ADDD", "idx", 2),   # Add to D indexed
        0xE4: ("ANDB", "idx", 2),   # AND B indexed
        0xE5: ("BITB", "idx", 2),   # Bit test B indexed
        0xE6: ("LDAB", "idx", 2),   # Load B indexed
        0xE7: ("STAB", "idx", 2),   # Store B indexed
        0xE8: ("EORB", "idx", 2),   # XOR B indexed
        0xE9: ("ADCB", "idx", 2),   # Add with carry B indexed
        0xEA: ("ORAB", "idx", 2),   # OR B indexed
        0xEB: ("ADDB", "idx", 2),   # Add B indexed
        0xEC: ("LDD", "idx", 2),    # Load D indexed
        0xED: ("STD", "idx", 2),    # Store D indexed
        0xEE: ("LDX", "idx", 2),    # Load X indexed
        0xEF: ("STX", "idx", 2),    # Store X indexed
        
        # Misc
        0x01: ("NOP", "imp", 1),    # No operation
        0x0E: ("CLI", "imp", 1),    # Clear interrupt mask
        0x0F: ("SEI", "imp", 1),    # Set interrupt mask
        0x3D: ("MUL", "imp", 1),    # Multiply A*B -> D
        0x3E: ("WAI", "imp", 1),    # Wait for interrupt
        0x3B: ("RTI", "imp", 1),    # Return from interrupt
        0x3F: ("SWI", "imp", 1),    # Software interrupt
        0x3A: ("ABX", "imp", 1),    # Add B to X
        0x1B: ("ABA", "imp", 1),    # Add B to A
        0x10: ("SBA", "imp", 1),    # Subtract B from A
        
        # Stack operations (complete set)
        0x36: ("PSHA", "imp", 1),   # Push A
        0x37: ("PSHB", "imp", 1),   # Push B
        0x3C: ("PSHX", "imp", 1),   # Push X
        0x32: ("PULA", "imp", 1),   # Pull A
        0x33: ("PULB", "imp", 1),   # Pull B
        0x38: ("PULX", "imp", 1),   # Pull X
        0x34: ("DES", "imp", 1),    # Decrement stack pointer
        0x31: ("INS", "imp", 1),    # Increment stack pointer
        
        # Bit test and branch (direct mode)
        0x12: ("BRSET", "bit", 4),  # Branch if bit(s) set (direct)
        0x13: ("BRCLR", "bit", 4),  # Branch if bit(s) clear (direct)
        0x1E: ("BRSET", "bit_idx", 4),  # Branch if bit(s) set (indexed)
        0x1F: ("BRCLR", "bit_idx", 4),  # Branch if bit(s) clear (indexed)
        
        # More arithmetic
        0x82: ("SBCA", "imm", 2),   # Subtract with carry A
        0xC2: ("SBCB", "imm", 2),   # Subtract with carry B
        0x92: ("SBCA", "dir", 2),   # Subtract with carry A (direct)
        0xD2: ("SBCB", "dir", 2),   # Subtract with carry B (direct)
        0xB2: ("SBCA", "ext", 3),   # Subtract with carry A (extended)
        0xF2: ("SBCB", "ext", 3),   # Subtract with carry B (extended)
        
        # More logic
        0x88: ("EORA", "imm", 2),   # XOR A immediate
        0xC8: ("EORB", "imm", 2),   # XOR B immediate
        0x98: ("EORA", "dir", 2),   # XOR A direct
        0xD8: ("EORB", "dir", 2),   # XOR B direct
        0xB8: ("EORA", "ext", 3),   # XOR A extended
        0xF8: ("EORB", "ext", 3),   # XOR B extended
        
        # More shifts/rotates
        0x58: ("ASLB", "imp", 1),   # Arithmetic shift left B
        0x59: ("ROLB", "imp", 1),   # Rotate left B
        0x5A: ("DECB", "imp", 1),   # Decrement B
        0x5C: ("INCB", "imp", 1),   # Increment B
        0x5D: ("TSTB", "imp", 1),   # Test B
        0x44: ("LSRA", "imp", 1),   # Logical shift right A
        0x54: ("LSRB", "imp", 1),   # Logical shift right B
        0x04: ("LSRD", "imp", 1),   # Logical shift right D
        0x05: ("ASLD", "imp", 1),   # Arithmetic shift left D
        0x46: ("RORA", "imp", 1),   # Rotate right A
        0x56: ("RORB", "imp", 1),   # Rotate right B
        0x47: ("ASRA", "imp", 1),   # Arithmetic shift right A
        0x57: ("ASRB", "imp", 1),   # Arithmetic shift right B
        
        # Transfer/exchange
        0x16: ("TAB", "imp", 1),    # Transfer A to B
        0x17: ("TBA", "imp", 1),    # Transfer B to A
        0x8F: ("XGDX", "imp", 1),   # Exchange D with X
        0x30: ("TSX", "imp", 1),    # Transfer stack pointer to X
        0x35: ("TXS", "imp", 1),    # Transfer X to stack pointer
        
        # Condition code manipulation
        0x06: ("TAP", "imp", 1),    # Transfer A to CCR
        0x07: ("TPA", "imp", 1),    # Transfer CCR to A
        0x0A: ("CLV", "imp", 1),    # Clear overflow flag
        0x0B: ("SEV", "imp", 1),    # Set overflow flag
        0x0C: ("CLC", "imp", 1),    # Clear carry flag
        0x0D: ("SEC", "imp", 1),    # Set carry flag
        
        # Special
        0x19: ("DAA", "imp", 1),    # Decimal adjust A
        0x02: ("IDIV", "imp", 1),   # Integer divide (D/X -> X rem D)
        0x03: ("FDIV", "imp", 1),   # Fractional divide
        0xCF: ("STOP", "imp", 1),   # Stop (low power mode)
        0x00: ("TEST", "imp", 1),   # Test (for mfg testing)
        
        # Page 1 prefix (0x18) for Y-indexed operations - handled separately
        0x18: ("PAGE1", "pfx", 1),  # Page 1 opcode prefix
        
        # Missing opcodes causing "Unknown opcode" errors
        0x11: ("CBA", "imp", 1),    # Compare B to A
        0x14: ("BSET", "bit_dir", 3),  # Bit set direct (special 3-byte)
        0x15: ("BCLR", "bit_dir", 3),  # Bit clear direct (special 3-byte)
        0x1C: ("BSET", "bit_idx", 3),  # Bit set indexed
        0x1D: ("BCLR", "bit_idx", 3),  # Bit clear indexed
        0x40: ("NEGA", "imp", 1),   # Negate A (2's complement)
        0x50: ("NEGB", "imp", 1),   # Negate B
        0x60: ("NEG", "idx", 2),    # Negate indexed
        0x70: ("NEG", "ext", 3),    # Negate extended
        0x6D: ("TST", "idx", 2),    # Test indexed
        0x7D: ("TST", "ext", 3),    # Test extended
        0x6E: ("JMP", "idx", 2),    # Jump indexed
        0x7E: ("JMP", "ext", 3),    # Jump extended
        0x6F: ("CLR", "idx", 2),    # Clear indexed
        0x7F: ("CLR", "ext", 3),    # Clear extended
        
        # Memory modify instructions - indexed X (Row 6)
        0x63: ("COM", "idx", 2),    # Complement indexed
        0x64: ("LSR", "idx", 2),    # Logical shift right indexed
        0x66: ("ROR", "idx", 2),    # Rotate right indexed
        0x67: ("ASR", "idx", 2),    # Arithmetic shift right indexed
        0x68: ("ASL", "idx", 2),    # Arithmetic shift left indexed
        0x69: ("ROL", "idx", 2),    # Rotate left indexed
        0x6A: ("DEC", "idx", 2),    # Decrement indexed
        0x6C: ("INC", "idx", 2),    # Increment indexed
        
        # Memory modify instructions - extended (Row 7)
        0x73: ("COM", "ext", 3),    # Complement extended
        0x74: ("LSR", "ext", 3),    # Logical shift right extended
        0x76: ("ROR", "ext", 3),    # Rotate right extended
        0x77: ("ASR", "ext", 3),    # Arithmetic shift right extended
        0x78: ("ASL", "ext", 3),    # Arithmetic shift left extended
        0x79: ("ROL", "ext", 3),    # Rotate left extended
        0x7A: ("DEC", "ext", 3),    # Decrement extended
        0x7C: ("INC", "ext", 3),    # Increment extended
        
        0x83: ("SUBD", "imm", 3),   # Subtract D immediate
        0x93: ("SUBD", "dir", 2),   # Subtract D direct
        0xB3: ("SUBD", "ext", 3),   # Subtract D extended
        0xA3: ("SUBD", "idx", 2),   # Subtract D indexed
    }
    
    # Prebyte 0x18 opcodes (Y-register operations)
    # Format: {opcode_after_18: (mnemonic, mode, total_bytes, cycles)}
    # Source: 68HC11_COMPLETE_INSTRUCTION_REFERENCE.md lines 190-230
    PREBYTE_18_OPCODES = {
        0x08: ("INY", "imp", 2, 4),      # Increment Y
        0x09: ("DEY", "imp", 2, 4),      # Decrement Y
        0x1C: ("BSET", "bit_idy", 4, 8), # Bit set indexed Y
        0x1D: ("BCLR", "bit_idy", 4, 8), # Bit clear indexed Y
        0x1E: ("BRSET", "bit_idy", 5, 8),# Branch if bits set indexed Y
        0x1F: ("BRCLR", "bit_idy", 5, 8),# Branch if bits clear indexed Y
        0x30: ("TSY", "imp", 2, 4),      # Transfer SP to Y
        0x35: ("TYS", "imp", 2, 4),      # Transfer Y to SP
        0x38: ("PULY", "imp", 2, 5),     # Pull Y from stack
        0x3A: ("ABY", "imp", 2, 4),      # Add B to Y
        0x3C: ("PSHY", "imp", 2, 5),     # Push Y to stack
        0x60: ("NEG", "idy", 3, 7),      # Negate indexed Y
        0x63: ("COM", "idy", 3, 7),      # Complement indexed Y
        0x64: ("LSR", "idy", 3, 7),      # Logical shift right indexed Y
        0x66: ("ROR", "idy", 3, 7),      # Rotate right indexed Y
        0x67: ("ASR", "idy", 3, 7),      # Arithmetic shift right indexed Y
        0x68: ("ASL", "idy", 3, 7),      # Arithmetic shift left indexed Y
        0x69: ("ROL", "idy", 3, 7),      # Rotate left indexed Y
        0x6A: ("DEC", "idy", 3, 7),      # Decrement indexed Y
        0x6C: ("INC", "idy", 3, 7),      # Increment indexed Y
        0x6D: ("TST", "idy", 3, 7),      # Test indexed Y
        0x6E: ("JMP", "idy", 3, 4),      # Jump indexed Y
        0x6F: ("CLR", "idy", 3, 7),      # Clear indexed Y
        0x8C: ("CPY", "imm", 4, 5),      # Compare Y immediate
        0x8F: ("XGDY", "imp", 2, 4),     # Exchange D with Y
        0x9C: ("CPY", "dir", 3, 6),      # Compare Y direct
        0xA0: ("SUBA", "idy", 3, 5),     # Subtract from A indexed Y
        0xA1: ("CMPA", "idy", 3, 5),     # Compare A indexed Y
        0xA2: ("SBCA", "idy", 3, 5),     # Subtract with carry A indexed Y
        0xA3: ("SUBD", "idy", 3, 7),     # Subtract D indexed Y
        0xA4: ("ANDA", "idy", 3, 5),     # AND A indexed Y
        0xA5: ("BITA", "idy", 3, 5),     # Bit test A indexed Y
        0xA6: ("LDAA", "idy", 3, 5),     # Load A indexed Y
        0xA7: ("STAA", "idy", 3, 5),     # Store A indexed Y
        0xA8: ("EORA", "idy", 3, 5),     # XOR A indexed Y
        0xA9: ("ADCA", "idy", 3, 5),     # Add with carry to A indexed Y
        0xAA: ("ORAA", "idy", 3, 5),     # OR A indexed Y
        0xAB: ("ADDA", "idy", 3, 5),     # Add to A indexed Y
        0xAC: ("CPY", "idy", 3, 7),      # Compare Y indexed Y
        0xAD: ("JSR", "idy", 3, 7),      # Jump subroutine indexed Y
        0xAE: ("LDS", "idy", 3, 6),      # Load SP indexed Y
        0xAF: ("STS", "idy", 3, 6),      # Store SP indexed Y
        0xBC: ("CPY", "ext", 4, 7),      # Compare Y extended
        0xCE: ("LDY", "imm", 4, 4),      # Load Y immediate
        0xDE: ("LDY", "dir", 3, 5),      # Load Y direct
        0xDF: ("STY", "dir", 3, 5),      # Store Y direct
        0xE0: ("SUBB", "idy", 3, 5),     # Subtract from B indexed Y
        0xE1: ("CMPB", "idy", 3, 5),     # Compare B indexed Y
        0xE2: ("SBCB", "idy", 3, 5),     # Subtract with carry B indexed Y
        0xE3: ("ADDD", "idy", 3, 7),     # Add to D indexed Y
        0xE4: ("ANDB", "idy", 3, 5),     # AND B indexed Y
        0xE5: ("BITB", "idy", 3, 5),     # Bit test B indexed Y
        0xE6: ("LDAB", "idy", 3, 5),     # Load B indexed Y
        0xE7: ("STAB", "idy", 3, 5),     # Store B indexed Y
        0xE8: ("EORB", "idy", 3, 5),     # XOR B indexed Y
        0xE9: ("ADCB", "idy", 3, 5),     # Add with carry to B indexed Y
        0xEA: ("ORAB", "idy", 3, 5),     # OR B indexed Y
        0xEB: ("ADDB", "idy", 3, 5),     # Add to B indexed Y
        0xEC: ("LDD", "idy", 3, 6),      # Load D indexed Y
        0xED: ("STD", "idy", 3, 6),      # Store D indexed Y
        0xEE: ("LDY", "idy", 3, 6),      # Load Y indexed Y
        0xEF: ("STY", "idy", 3, 6),      # Store Y indexed Y
        0xFE: ("LDY", "ext", 4, 6),      # Load Y extended
        0xFF: ("STY", "ext", 4, 6),      # Store Y extended
    }
    
    # Prebyte 0x1A opcodes (CPD and special operations)
    # Source: 68HC11_COMPLETE_INSTRUCTION_REFERENCE.md line 194 (CPD section)
    # Note: CPD uses 0x1A prebyte, CPY indexed X also uses 0x1A
    PREBYTE_1A_OPCODES = {
        0x83: ("CPD", "imm", 4, 5),      # Compare D immediate (1A 83 jj kk)
        0x93: ("CPD", "dir", 3, 6),      # Compare D direct (1A 93 dd)
        0xA3: ("CPD", "idx", 3, 7),      # Compare D indexed X (1A A3 ff)
        0xAC: ("CPY", "idx", 3, 7),      # Compare Y indexed X (1A AC ff)
        0xB3: ("CPD", "ext", 4, 7),      # Compare D extended (1A B3 hh ll)
        0xEE: ("LDY", "idx", 3, 6),      # Load Y indexed X (1A EE ff)
        0xEF: ("STY", "idx", 3, 6),      # Store Y indexed X (1A EF ff)
    }
    
    # Prebyte 0xCD opcodes (Y-indexed for CPD, CPX, LDX)
    # Source: 68HC11_COMPLETE_INSTRUCTION_REFERENCE.md lines 194, 207
    PREBYTE_CD_OPCODES = {
        0xA3: ("CPD", "idy", 3, 7),      # Compare D indexed Y (CD A3 ff)
        0xAC: ("CPX", "idy", 3, 7),      # Compare X indexed Y (CD AC ff)
        0xEE: ("LDX", "idy", 3, 6),      # Load X indexed Y (CD EE ff)
        0xEF: ("STX", "idy", 3, 6),      # Store X indexed Y (CD EF ff)
    }
    
    # VY V6 Enhanced Binary Memory Layout (128KB = 0x20000 bytes)
    # Structure verified January 2026:
    # - 0x00000-0x0FFFF (64KB) = Low bank / Calibration data
    # - 0x10000-0x1FFFF (64KB) = High bank / Code (maps to CPU $8000-$FFFF)
    # - Formula: runtime_addr = 0x8000 + (file_offset - 0x10000)
    #
    # For bank-split files (32KB/64KB individual bank binaries):
    # - Bank 1 (64KB): base_addr=0x0000, code_start_offset=0x0 (code at $2000+)
    # - Bank 2 (32KB): base_addr=0x8000, code_start_offset=0x0 (all code)
    # - Bank 3 (32KB): base_addr=0x8000, code_start_offset=0x0 (all code)
    CODE_START_OFFSET = 0x10000  # Default for full 128KB binary
    
    # HC11 Memory-Mapped I/O Registers (0x1000-0x103F)
    HARDWARE_REGISTERS = {
        0x1000: "PORTA",   0x1001: "PORTB",   0x1002: "PORTC",   0x1003: "PORTD",
        0x1004: "PORTE",   0x1008: "TCNT_HI", 0x1009: "TCNT_LO", 0x101A: "TCTL1",
        0x101B: "TCTL2",   0x101C: "TMSK1",   0x101D: "TFLG1",   0x101E: "TMSK2",
        0x101F: "TFLG2",   0x1020: "PACTL",   0x1021: "PACNT",   0x1022: "SPCR",
        0x1023: "SPSR",    0x1024: "SPDR",    0x1025: "BAUD",    0x1026: "SCCR1",
        0x1027: "SCCR2",   0x1028: "SCSR",    0x1029: "SCDR",    0x102A: "ADCTL",
        0x102B: "ADR1",    0x102C: "ADR2",    0x102D: "ADR3",    0x102E: "ADR4",
        0x1039: "OPTION",  0x103A: "COPRST",  0x103D: "INIT",    0x103F: "CONFIG",
    }
    
    # Bank split configurations: (base_addr, code_start_offset, description)
    BANK_CONFIGS = {
        'full':  (0x00000, 0x10000, 'Full 128KB binary (3 banks concatenated)'),
        'bank1': (0x00000, 0x00000, 'Bank 1 (64KB) — calibration + common code'),
        'bank2': (0x08000, 0x00000, 'Bank 2 (32KB) — engine code overlay @ $8000-$FFFF'),
        'bank3': (0x08000, 0x00000, 'Bank 3 (32KB) — trans/diag overlay @ $8000-$FFFF'),
    }
    
    def __init__(self, binary_path: str, base_addr: int = 0xE0000, bank: str = None):
        self.binary_path = Path(binary_path)
        self.base_addr = base_addr
        self.bank = bank  # None = legacy/auto, 'bank1'/'bank2'/'bank3'/'full'
        self.xdf = XDFCalibrationDB()
        with open(self.binary_path, 'rb') as f:
            self.data = f.read()
        
        # Auto-detect bank mode from file size if not specified
        file_size = len(self.data)
        if bank is not None:
            # Explicit bank mode — override base_addr and code_start_offset
            cfg_base, cfg_code_start, cfg_desc = self.BANK_CONFIGS[bank]
            self.base_addr = cfg_base
            self.code_start_offset = cfg_code_start
            print(f"[OK] Loaded {file_size} bytes from {self.binary_path.name}")
            print(f"   Bank mode: {bank} — {cfg_desc}")
            print(f"   Base address: 0x{self.base_addr:05X}, Code start offset: 0x{self.code_start_offset:05X}")
        elif file_size == 0x20000:  # 128KB = full binary
            self.code_start_offset = self.CODE_START_OFFSET  # 0x10000
            print(f"[OK] Loaded {file_size} bytes from {self.binary_path.name} (full 128KB binary)")
            print(f"   Base address: 0x{base_addr:05X}")
        elif file_size == 0x10000:  # 64KB = bank 1
            self.code_start_offset = 0x0
            if self.base_addr == 0xE0000:  # Default wasn't overridden
                self.base_addr = 0x0
            print(f"[OK] Loaded {file_size} bytes from {self.binary_path.name} (64KB — bank 1 detected)")
            print(f"   Base address: 0x{self.base_addr:05X}")
        elif file_size == 0x8000:  # 32KB = bank 2 or 3
            self.code_start_offset = 0x0
            if self.base_addr == 0xE0000:  # Default wasn't overridden
                self.base_addr = 0x8000
            print(f"[OK] Loaded {file_size} bytes from {self.binary_path.name} (32KB — bank 2/3 detected)")
            print(f"   Base address: 0x{self.base_addr:05X}")
        else:
            self.code_start_offset = 0x0
            print(f"[OK] Loaded {file_size} bytes from {self.binary_path.name} (unknown size)")
            print(f"   Base address: 0x{base_addr:05X}")
    
    def offset_to_cpu_addr(self, offset: int) -> int:
        """Convert file offset to CPU address, handling both full 128KB and bank-split layouts.
        
        Full 128KB binary:
            offset < 0x10000 → addr = offset (calibration/low bank)
            offset >= 0x10000 → addr = 0x8000 + (offset - 0x10000)
        
        Bank split (32KB/64KB):
            addr = base_addr + offset
        """
        if self.code_start_offset > 0 and offset >= self.code_start_offset:
            return 0x8000 + (offset - self.code_start_offset)
        else:
            return self.base_addr + offset
    
    def get_ram_addr(self, file_offset: int) -> int:
        """Convert file offset to RAM address"""
        return self.base_addr + file_offset
    
    def get_file_offset(self, ram_addr: int) -> int:
        """Convert RAM address to file offset"""
        return ram_addr - self.base_addr
    
    def read_byte(self, offset: int) -> int:
        """Read byte at file offset"""
        if 0 <= offset < len(self.data):
            return self.data[offset]
        return 0
    
    def read_word(self, offset: int) -> int:
        """Read big-endian 16-bit word at file offset"""
        if 0 <= offset + 1 < len(self.data):
            return (self.data[offset] << 8) | self.data[offset + 1]
        return 0
    
    def decode_rpm_value(self, addr: int, byte_val: int) -> str:
        """Decode RPM value with appropriate scaling"""
        if addr in self.xdf.rpm_scaling_x25:
            rpm = byte_val * 25
            return f"{rpm} RPM (0x{byte_val:02X} × 25)"
        return f"0x{byte_val:02X}"
    
    def get_xdf_comment(self, addr: int) -> str:
        """Get XDF comment for address if it's a calibration or hardware
        register. Now includes direct page registers and verified RAM
        addresses."""
        # Check direct page registers (0x00-0x3F - these are critical HC11 I/O)
        if addr in HC11_DIRECT_PAGE_REGISTERS:
            reg_name = HC11_DIRECT_PAGE_REGISTERS[addr]
            return f" ; [DIRECT_REG] {reg_name}"
        
        # Check VY V6 specific RAM variables
        if addr in VY_V6_RAM_VARIABLES:
            var_name = VY_V6_RAM_VARIABLES[addr]
            return f" ; [RAM_VAR] {var_name}"
        
        # Check verified RAM addresses from constants module
        if HAS_VERIFIED_CONSTANTS and addr in VERIFIED_RAM_ADDRESSES.values():
            # Reverse lookup the name
            for name, var_addr in VERIFIED_RAM_ADDRESSES.items():
                if var_addr == addr:
                    return f" ; [VERIFIED_RAM] {name}"
        
        # Check verified HC11 registers
        if HAS_VERIFIED_CONSTANTS and addr in VERIFIED_HC11_REGISTERS:
            reg_name = VERIFIED_HC11_REGISTERS[addr]
            return f" ; [HW_REG] {reg_name}"
        
        # Check memory-mapped I/O hardware registers (0x1000-0x103F)
        if addr in self.HARDWARE_REGISTERS:
            reg_name = self.HARDWARE_REGISTERS[addr]
            return f" ; [HW_REG] {reg_name}"
        
        # Check XDF calibrations
        cal = self.xdf.lookup(addr)
        if cal:
            title, type_str, category = cal
            return f" ; [{type_str}] {title}"
        return ""
    
    def _format_prebyte_instruction(self, offset: int, ram_addr: int,
                                    prebyte: int, opcode2: int,
                                    mnemonic: str, mode: str,
                                    length: int, cycles: int) -> Tuple[str, int]:
        """Format prebyte instruction (0x18, 0x1A, 0xCD) with proper
        operands
        
        Args:
            offset: File offset
            ram_addr: CPU RAM address
            prebyte: Prebyte value (0x18, 0x1A, or 0xCD)
            opcode2: Second opcode byte after prebyte
            mnemonic: Instruction mnemonic (e.g., 'CPD', 'LDY')
            mode: Addressing mode
            length: Total instruction length including prebyte
            cycles: Execution cycles
        
        Returns:
            Tuple of (formatted_instruction_string, instruction_length)
        """
        # Format hex bytes
        hex_bytes = f"{prebyte:02X} {opcode2:02X}"
        
        if mode == "imp":  # Implied (no operand)
            instr = f"0x{ram_addr:05X}: {hex_bytes:12s} {mnemonic}"
            return (instr, length)
        
        elif mode == "imm":  # Immediate
            if length == 4:  # 16-bit immediate (prebyte + opcode + 2 bytes)
                operand = self.read_word(offset + 2)
                b1 = self.read_byte(offset + 2)
                b2 = self.read_byte(offset + 3)
                hex_bytes = f"{prebyte:02X} {opcode2:02X} {b1:02X} {b2:02X}"
                instr = (f"0x{ram_addr:05X}: {hex_bytes:12s} "
                         f"{mnemonic} #${operand:04X}")
                # Add special comment for CPD (16-bit compare)
                if mnemonic == "CPD":
                    instr += f"  ; Compare D (16-bit) to {operand}"
                return (instr, length)
            else:  # 8-bit immediate
                operand = self.read_byte(offset + 2)
                hex_bytes = f"{prebyte:02X} {opcode2:02X} {operand:02X}"
                instr = (f"0x{ram_addr:05X}: {hex_bytes:12s} "
                         f"{mnemonic} #${operand:02X}")
                return (instr, length)
        
        elif mode == "dir":  # Direct (zero page)
            operand = self.read_byte(offset + 2)
            hex_bytes = f"{prebyte:02X} {opcode2:02X} {operand:02X}"
            instr = f"0x{ram_addr:05X}: {hex_bytes:12s} {mnemonic} ${operand:02X}"
            return (instr, length)
        
        elif mode == "ext":  # Extended (16-bit address)
            operand = self.read_word(offset + 2)
            b1 = self.read_byte(offset + 2)
            b2 = self.read_byte(offset + 3)
            hex_bytes = f"{prebyte:02X} {opcode2:02X} {b1:02X} {b2:02X}"
            xdf_comment = self.get_xdf_comment(operand)
            instr = (f"0x{ram_addr:05X}: {hex_bytes:12s} "
                     f"{mnemonic} ${operand:04X}{xdf_comment}")
            return (instr, length)
        
        elif mode in ["idx", "idy"]:  # Indexed X or Y
            operand = self.read_byte(offset + 2)
            hex_bytes = f"{prebyte:02X} {opcode2:02X} {operand:02X}"
            reg = "Y" if mode == "idy" else "X"
            instr = (f"0x{ram_addr:05X}: {hex_bytes:12s} "
                     f"{mnemonic} ${operand:02X},{reg}")
            return (instr, length)
        
        else:
            # Unknown mode
            instr = (f"0x{ram_addr:05X}: {hex_bytes:12s} "
                     f"DB    ${prebyte:02X},${opcode2:02X}  ; Unknown mode")
            return (instr, 2)
    
    def annotate_table_data(self, addr: int, length: int = 12) -> List[str]:
        """Generate annotated hex dump of calibration table"""
        cal = self.xdf.lookup(addr)
        if not cal:
            return []
        
        title, type_str, category = cal
        lines = [f"; === TABLE @ 0x{addr:04X}: {title} ==="]
        
        # Read table data
        offset = addr
        if addr in self.xdf.rpm_scaling_x25:
            lines.append("; RPM Table (scaling: byte × 25 = RPM)")
            for i in range(length):
                if offset + i < len(self.data):
                    byte_val = self.data[offset + i]
                    rpm = byte_val * 25
                    lines.append(f";   Byte {i}: 0x{byte_val:02X} = {rpm:4d} RPM")
        else:
            # Generic hex dump
            hex_bytes = []
            for i in range(length):
                if offset + i < len(self.data):
                    hex_bytes.append(f"{self.data[offset + i]:02X}")
            if hex_bytes:
                lines.append(f"; Data: {' '.join(hex_bytes)}")
        
        return lines
    
    def disassemble_instruction(self, offset: int) -> Tuple[str, int]:
        """Disassemble single instruction at file offset with XDF annotations
        Returns: (assembly string, instruction length)
        
        Handles prebyte instructions (0x18, 0x1A, 0xCD):
        - 0x18: Y-register operations (CPY, LDY, STY, etc.)
        - 0x1A: CPD (Compare D register - 16-bit)
        - 0xCD: Y-indexed CPD, CPX, LDX
        
        Cross-referenced with: 68HC11_COMPLETE_INSTRUCTION_REFERENCE.md
        """
        opcode = self.read_byte(offset)
        
        # Apply VY V6 Enhanced binary offset correction
        ram_addr = self.offset_to_cpu_addr(offset)
        
        # Handle prebyte instructions
        if opcode == 0x18 and offset + 1 < len(self.data):
            # Prebyte 0x18 (Y-register operations)
            opcode2 = self.read_byte(offset + 1)
            if opcode2 in self.PREBYTE_18_OPCODES:
                mnemonic, mode, length, cycles = self.PREBYTE_18_OPCODES[opcode2]
                return self._format_prebyte_instruction(
                    offset, ram_addr, 0x18, opcode2, 
                    mnemonic, mode, length, cycles
                )
            else:
                hex_bytes = f"{opcode:02X} {opcode2:02X}"
                return (f"0x{ram_addr:05X}: {hex_bytes:12s} "
                        f"DB    $18,${opcode2:02X}  ; Unknown 0x18 opcode", 2)
        
        elif opcode == 0x1A and offset + 1 < len(self.data):
            # Prebyte 0x1A (CPD and special operations)
            opcode2 = self.read_byte(offset + 1)
            if opcode2 in self.PREBYTE_1A_OPCODES:
                mnemonic, mode, length, cycles = self.PREBYTE_1A_OPCODES[opcode2]
                return self._format_prebyte_instruction(
                    offset, ram_addr, 0x1A, opcode2,
                    mnemonic, mode, length, cycles
                )
            else:
                hex_bytes = f"{opcode:02X} {opcode2:02X}"
                return (f"0x{ram_addr:05X}: {hex_bytes:12s} "
                        f"DB    $1A,${opcode2:02X}  ; Unknown 0x1A opcode", 2)
        
        elif opcode == 0xCD and offset + 1 < len(self.data):
            # Prebyte 0xCD (Y-indexed for CPD, CPX, LDX)
            opcode2 = self.read_byte(offset + 1)
            if opcode2 in self.PREBYTE_CD_OPCODES:
                mnemonic, mode, length, cycles = self.PREBYTE_CD_OPCODES[opcode2]
                return self._format_prebyte_instruction(
                    offset, ram_addr, 0xCD, opcode2,
                    mnemonic, mode, length, cycles
                )
            else:
                hex_bytes = f"{opcode:02X} {opcode2:02X}"
                return (f"0x{ram_addr:05X}: {hex_bytes:12s} "
                        f"DB    $CD,${opcode2:02X}  ; Unknown 0xCD opcode", 2)
        
        # Regular (non-prebyte) instructions
        if opcode not in self.OPCODES:
            return (f"0x{ram_addr:05X}: {opcode:02X}           "
                    f"DB    ${opcode:02X}           ; Unknown opcode", 1)
        
        mnemonic, mode, length = self.OPCODES[opcode]
        
        # Format instruction based on addressing mode
        if mode == "imp":  # Implied
            instr = f"0x{ram_addr:05X}: {opcode:02X}           {mnemonic}"
        
        elif mode == "imm":  # Immediate
            if length == 2:
                operand = self.read_byte(offset + 1)
                instr = f"0x{ram_addr:05X}: {opcode:02X} {operand:02X}        {mnemonic} #${operand:02X}"
            else:  # length == 3
                operand = self.read_word(offset + 1)
                b1 = self.read_byte(offset + 1)
                b2 = self.read_byte(offset + 2)
                instr = f"0x{ram_addr:05X}: {opcode:02X} {b1:02X} {b2:02X}     {mnemonic} #${operand:04X}"
        
        elif mode == "dir":  # Direct (zero page)
            operand = self.read_byte(offset + 1)
            instr = f"0x{ram_addr:05X}: {opcode:02X} {operand:02X}        {mnemonic} ${operand:02X}"
        
        elif mode == "ext":  # Extended (absolute) - CHECK XDF!
            operand = self.read_word(offset + 1)
            b1 = self.read_byte(offset + 1)
            b2 = self.read_byte(offset + 2)
            xdf_comment = self.get_xdf_comment(operand)
            instr = f"0x{ram_addr:05X}: {opcode:02X} {b1:02X} {b2:02X}     {mnemonic} ${operand:04X}{xdf_comment}"
        
        elif mode == "idx":  # Indexed
            offset_val = self.read_byte(offset + 1)
            instr = f"0x{ram_addr:05X}: {opcode:02X} {offset_val:02X}        {mnemonic} ${offset_val:02X},X"
        
        elif mode == "rel":  # Relative branch
            displacement = self.read_byte(offset + 1)
            # Sign-extend 8-bit displacement
            if displacement & 0x80:
                displacement = displacement - 256
            target = ram_addr + length + displacement
            instr = f"0x{ram_addr:05X}: {opcode:02X} {self.read_byte(offset + 1):02X}        {mnemonic} $0x{target:05X}"
        
        elif mode == "bit":  # BRSET/BRCLR direct mode (4 bytes)
            addr = self.read_byte(offset + 1)
            mask = self.read_byte(offset + 2)
            displacement = self.read_byte(offset + 3)
            if displacement & 0x80:
                displacement = displacement - 256
            target = ram_addr + length + displacement
            b1, b2, b3 = self.read_byte(offset+1), self.read_byte(offset+2), self.read_byte(offset+3)
            instr = f"0x{ram_addr:05X}: {opcode:02X} {b1:02X} {b2:02X} {b3:02X}  {mnemonic} ${addr:02X},#${mask:02X},$0x{target:05X}"
        
        elif mode == "bit_idx":  # BRSET/BRCLR indexed mode (4 bytes)
            idx_offset = self.read_byte(offset + 1)
            mask = self.read_byte(offset + 2)
            displacement = self.read_byte(offset + 3)
            if displacement & 0x80:
                displacement = displacement - 256
            target = ram_addr + length + displacement
            b1, b2, b3 = self.read_byte(offset+1), self.read_byte(offset+2), self.read_byte(offset+3)
            instr = f"0x{ram_addr:05X}: {opcode:02X} {b1:02X} {b2:02X} {b3:02X}  {mnemonic} ${idx_offset:02X},X,#${mask:02X},$0x{target:05X}"
        
        elif mode == "bit_dir":  # BSET/BCLR direct mode (3 bytes)
            addr_val = self.read_byte(offset + 1)
            mask = self.read_byte(offset + 2)
            b1, b2 = self.read_byte(offset+1), self.read_byte(offset+2)
            hw_comment = self.get_xdf_comment(addr_val)
            instr = f"0x{ram_addr:05X}: {opcode:02X} {b1:02X} {b2:02X}     {mnemonic} ${addr_val:02X},#${mask:02X}{hw_comment}"
        
        elif mode == "pfx":  # Page 1 prefix (Y-indexed operations)
            # Next byte is the actual opcode
            page1_opcode = self.read_byte(offset + 1)
            # Common Page 1 opcodes
            page1_ops = {
                0x08: ("INY", "imp", 1),
                0x09: ("DEY", "imp", 1),
                0xCE: ("LDY", "imm", 3),
                0xDE: ("LDY", "dir", 2),
                0xFE: ("LDY", "ext", 3),
                0xEE: ("LDY", "idx_y", 2),
                0xDF: ("STY", "dir", 2),
                0xFF: ("STY", "ext", 3),
                0xEF: ("STY", "idx_y", 2),
                0xA6: ("LDAA", "idx_y", 2),
                0xE6: ("LDAB", "idx_y", 2),
                0xA7: ("STAA", "idx_y", 2),
                0xE7: ("STAB", "idx_y", 2),
                0x8C: ("CPY", "imm", 3),
                0x3A: ("ABY", "imp", 1),
                0x30: ("TSY", "imp", 1),
    # Missing opcodes (Motorola HC11 Reference Manual)
    0x89: 2,  # ADCA
    0x8E: 3,  # LDS
    0x95: 2,  # BITA
    0x99: 2,  # ADCA
    0x9F: 2,  # STS
    0xB5: 3,  # BITA
    0xB9: 3,  # ADCA
    0xBE: 3,  # LDS
    0xBF: 3,  # STS
    0xC0: 2,  # SUBB
    0xC9: 2,  # ADCB
    0xCB: 2,  # ADDB
    0xD0: 2,  # SUBB
    0xD5: 2,  # BITB
    0xD9: 2,  # ADCB
    0xDB: 2,  # ADDB
    0xF0: 3,  # SUBB
    0xF5: 3,  # BITB
    0xF9: 3,  # ADCB
    0xFB: 3,  # ADDB
            }
            if page1_opcode in page1_ops:
                p1_mnem, p1_mode, p1_len = page1_ops[page1_opcode]
                total_length = 1 + p1_len
                if p1_mode == "imp":
                    instr = f"0x{ram_addr:05X}: {opcode:02X} {page1_opcode:02X}        {p1_mnem}"
                elif p1_mode == "imm" and p1_len == 3:
                    val = self.read_word(offset + 2)
                    b1, b2 = self.read_byte(offset+2), self.read_byte(offset+3)
                    instr = f"0x{ram_addr:05X}: {opcode:02X} {page1_opcode:02X} {b1:02X} {b2:02X}  {p1_mnem} #${val:04X}"
                elif p1_mode == "dir":
                    addr = self.read_byte(offset + 2)
                    instr = f"0x{ram_addr:05X}: {opcode:02X} {page1_opcode:02X} {addr:02X}     {p1_mnem} ${addr:02X}"
                elif p1_mode == "ext":
                    addr = self.read_word(offset + 2)
                    b1, b2 = self.read_byte(offset+2), self.read_byte(offset+3)
                    xdf_comment = self.get_xdf_comment(addr)
                    instr = f"0x{ram_addr:05X}: {opcode:02X} {page1_opcode:02X} {b1:02X} {b2:02X}  {p1_mnem} ${addr:04X}{xdf_comment}"
                elif p1_mode == "idx_y":
                    idx = self.read_byte(offset + 2)
                    instr = f"0x{ram_addr:05X}: {opcode:02X} {page1_opcode:02X} {idx:02X}     {p1_mnem} ${idx:02X},Y"
                else:
                    instr = f"0x{ram_addr:05X}: {opcode:02X} {page1_opcode:02X}        PAGE1 {page1_opcode:02X}"
                return instr, total_length
            else:
                instr = f"0x{ram_addr:05X}: {opcode:02X} {page1_opcode:02X}        PAGE1 ${page1_opcode:02X} (unknown)"
                return instr, 2
        
        else:
            instr = f"0x{ram_addr:05X}: {opcode:02X}           {mnemonic} ???"
        
        return instr, length
    
    def disassemble_range(self, start_offset: int, num_instructions: int = 20) -> List[str]:
        """Disassemble multiple instructions"""
        results = []
        offset = start_offset
        
        for i in range(num_instructions):
            if offset >= len(self.data):
                break
            instr, length = self.disassemble_instruction(offset)
            results.append(instr)
            offset += length
        
        return results
    
    def find_calibration_reads(self, start_offset: int, end_offset: int) -> List[Tuple[int, str]]:
        """Find all instructions that read from calibration region (0x4000-0x7FFF or 0x1000-0x1FFF)"""
        reads = []
        offset = start_offset
        
        while offset < min(end_offset, len(self.data)):
            opcode = self.read_byte(offset)
            
            if opcode in self.OPCODES:
                mnemonic, mode, length = self.OPCODES[opcode]
                
                # Check extended addressing mode loads
                if mode == "ext" and mnemonic in ["LDAA", "LDAB", "LDD", "LDX"]:
                    addr = self.read_word(offset + 1)
                    # Check if reading from calibration regions
                    if (0x4000 <= addr <= 0x7FFF) or (0x1000 <= addr <= 0x1FFF):
                        instr, _ = self.disassemble_instruction(offset)
                        reads.append((offset, instr))
                
                offset += length
            else:
                offset += 1
        
        return reads
    
    def find_specific_address_references(self, target_addr: int, start_offset: int = 0, end_offset: int = None) -> List[Tuple[int, str, str]]:
        """Find all instructions that reference a specific address (like 0x77DE limiter)
        Returns: [(file_offset, instruction, context_type)]
        """
        if end_offset is None:
            end_offset = len(self.data)
        
        references = []
        offset = start_offset
        
        while offset < min(end_offset, len(self.data)):
            opcode = self.read_byte(offset)
            
            if opcode in self.OPCODES:
                mnemonic, mode, length = self.OPCODES[opcode]
                
                # Check extended addressing mode (3-byte instructions)
                if mode == "ext" and length == 3:
                    addr = self.read_word(offset + 1)
                    if addr == target_addr:
                        instr, _ = self.disassemble_instruction(offset)
                        
                        # Determine context type
                        if mnemonic in ["LDAA", "LDAB", "LDD", "LDX"]:
                            context = "READ"
                        elif mnemonic in ["STAA", "STAB", "STD", "STX"]:
                            context = "WRITE"
                        elif mnemonic in ["CMPA", "CMPB"]:
                            context = "COMPARE"
                        elif mnemonic == "JSR":
                            context = "CALL"
                        else:
                            context = "OTHER"
                        
                        references.append((offset, instr, context))
                
                offset += length
            else:
                offset += 1
        
        return references
    
    def disassemble_with_context(self, center_offset: int, before: int = 10, after: int = 10) -> List[str]:
        """Disassemble instructions around a specific address with context"""
        results = []
        
        # Find start by counting backwards
        start_offset = center_offset
        count = 0
        while count < before and start_offset > 0:
            start_offset -= 1
            # Simple heuristic: assume average instruction is 2 bytes
            if count % 2 == 0:
                count += 1
        
        # Disassemble forward
        offset = start_offset
        instruction_count = 0
        
        while offset < len(self.data) and instruction_count < (before + after + 1):
            if offset == center_offset:
                results.append("; >>> TARGET INSTRUCTION >>>")
            
            instr, length = self.disassemble_instruction(offset)
            results.append(instr)
            
            if offset == center_offset:
                results.append("; <<< TARGET INSTRUCTION <<<")
            
            offset += length
            instruction_count += 1
        
        return results
    
    def find_rpm_comparisons(self, start_offset: int, end_offset: int) -> List[Tuple[int, str, int]]:
        """Find CMPA/CMPB/CPD instructions that might be RPM comparisons
        Returns: [(file_offset, instruction, immediate_value_if_present)]
        """
        comparisons = []
        offset = start_offset
        
        while offset < min(end_offset, len(self.data)):
            opcode = self.read_byte(offset)
            
            if opcode in self.OPCODES:
                mnemonic, mode, length = self.OPCODES[opcode]
                
                # Look for compare instructions
                if mnemonic in ["CMPA", "CMPB"]:
                    instr, _ = self.disassemble_instruction(offset)
                    
                    # Get immediate value if present
                    imm_val = None
                    if mode == "imm":
                        imm_val = self.read_byte(offset + 1)
                    elif mode == "ext":
                        imm_val = self.read_word(offset + 1)
                    
                    comparisons.append((offset, instr, imm_val))
                
                offset += length
            else:
                offset += 1
        
        return comparisons
    
    def find_bit_operations(self, start_offset: int, end_offset: int) -> List[Tuple[int, str, int, int]]:
        """Find BSET/BCLR/BRSET/BRCLR instructions (mode switches, flags, sensor enables)
        Returns: [(file_offset, instruction, address, bit_mask)]
        """
        bit_ops = []
        offset = start_offset
        
        while offset < min(end_offset, len(self.data)):
            opcode = self.read_byte(offset)
            
            if opcode in self.OPCODES:
                mnemonic, mode, length = self.OPCODES[opcode]
                
                # Look for bit manipulation instructions
                if mnemonic in ["BSET", "BCLR", "BRSET", "BRCLR"]:
                    instr, _ = self.disassemble_instruction(offset)
                    
                    # Extract address and mask
                    addr = None
                    mask = None
                    
                    if mode == "bit_dir":
                        addr = self.read_byte(offset + 1)
                        mask = self.read_byte(offset + 2)
                    elif mode == "bit_idx":
                        addr = self.read_byte(offset + 1)  # offset from X
                        mask = self.read_byte(offset + 2)
                    
                    if addr is not None:
                        bit_ops.append((offset, instr, addr, mask))
                
                offset += length
            else:
                offset += 1
        
        return bit_ops

    def find_byte_pattern(self, pattern: bytes, start_offset: int = 0,
                         end_offset: int = None) -> List[Tuple[int, int]]:
        """
        Search for byte pattern in binary. Returns list of (file_offset, ram_addr).
        
        Used for finding specific instruction sequences like:
        - STAA $1020 (b'\\xB7\\x10\\x20') - TCTL1 write
        - STD $0199 (b'\\xFD\\x01\\x99') - Dwell storage
        - LDAA $00A2 (b'\\x96\\xA2') - RPM read
        """
        if end_offset is None:
            end_offset = len(self.data)
        
        results = []
        for i in range(start_offset, end_offset - len(pattern) + 1):
            if self.data[i:i+len(pattern)] == pattern:
                # Calculate RAM address
                ram_addr = self.offset_to_cpu_addr(i)
                results.append((i, ram_addr))
        
        return results
    
    def find_est_control_code(self) -> Dict[str, List]:
        """
        Find EST (Electronic Spark Timing) control code patterns.
        
        Searches for:
        - TCTL1 writes (timer control for spark)
        - TOC3 writes (EST output compare)
        - TFLG1 access (timer interrupt flags)
        - Dwell storage writes
        
        Returns dict with categorized results.
        """
        est_patterns = {
            # Timer Control Register 1 writes
            'TCTL1_STAA': (b'\xB7\x10\x20', "STAA $1020 (TCTL1)"),
            'TCTL1_STAB': (b'\xF7\x10\x20', "STAB $1020 (TCTL1)"),
            
            # EST output compare (TOC3)
            'TOC3_STD': (b'\xFD\x10\x1A', "STD $101A (TOC3)"),
            
            # Timer flags (interrupt acknowledge)
            'TFLG1_STAA': (b'\xB7\x10\x23', "STAA $1023 (TFLG1)"),
            
            # Dwell time storage
            'DWELL_STD': (b'\xFD\x01\x99', "STD $0199 (Dwell)"),
            
            # RPM reads
            'RPM_HIGH_LDAA': (b'\x96\xA2', "LDAA $A2 (RPM high)"),
            'RPM_LOW_LDAA': (b'\x96\xA4', "LDAA $A4 (RPM low)"),
        }
        
        results = {}
        for name, (pattern, desc) in est_patterns.items():
            matches = self.find_byte_pattern(pattern)
            if matches:
                results[name] = {
                    'description': desc,
                    'matches': matches,
                    'count': len(matches)
                }
        
        return results
    
    def find_rev_limiter_patterns(self, target_rpm: int = 5900) -> Dict[str, List]:
        """
        Find rev limiter code patterns for specific RPM target.
        
        Uses validated scaling factors:
        - Primary: RPM / 25 (e.g., 5900 / 25 = 236 = 0xEC)
        - Alternative: RPM / 40 (e.g., 5900 / 40 = 147.5 ≈ 0x94)
        
        Searches for compare instructions with these thresholds.
        """
        primary_threshold = target_rpm // 25  # 0xEC for 5900 RPM
        alt_threshold = target_rpm // 40      # 0x94 for 5900 RPM
        
        patterns = {
            'CMPA_imm_primary': (bytes([0x81, primary_threshold]),
                                f"CMPA #${primary_threshold:02X} ({target_rpm} RPM)"),
            'CMPA_imm_alt': (bytes([0x81, alt_threshold]),
                            f"CMPA #${alt_threshold:02X} (alt scaling)"),
            'CMPB_imm_primary': (bytes([0xC1, primary_threshold]),
                                f"CMPB #${primary_threshold:02X} ({target_rpm} RPM)"),
        }
        
        results = {}
        for name, (pattern, desc) in patterns.items():
            matches = self.find_byte_pattern(pattern)
            if matches:
                results[name] = {
                    'description': desc,
                    'matches': matches,
                    'count': len(matches)
                }
        
        return results

    def detect_ecu_patterns(self, start_offset: int, end_offset: int) -> Dict[str, List]:
        """
        Detect ECU-specific patterns in disassembly using hc11_opcodes_complete module.
        
        Detects:
        - RPM comparisons (rev limiter thresholds)
        - Timer I/O accesses (TCTL1, TOC registers)
        - Known VY V6 critical addresses
        
        Returns: Dict with 'rpm_comparisons', 'timer_accesses', 'critical_refs'
        """
        patterns = {
            'rpm_comparisons': [],
            'timer_accesses': [],
            'critical_refs': [],
        }
        
        if not HAS_COMPLETE_OPCODES:
            print("[WARN] Complete opcodes module not available - pattern detection limited")
            return patterns
        
        offset = start_offset
        
        while offset < min(end_offset, len(self.data)):
            # Use complete opcode module to decode
            result = complete_decode_opcode(self.data, offset)
            if not result:
                offset += 1
                continue
            
            mnem, length, mode, desc, operand_bytes = result
            
            # Calculate RAM address
            ram_addr = self.offset_to_cpu_addr(offset)
            
            # Check for RPM comparison pattern
            rpm_result = is_rpm_comparison(mnem, operand_bytes, mode)
            if rpm_result[0]:  # is_rpm
                is_rpm, rpm_val, rpm_desc = rpm_result
                patterns['rpm_comparisons'].append({
                    'offset': offset,
                    'ram_addr': ram_addr,
                    'instruction': complete_format_instruction(mnem, operand_bytes, mode, ram_addr),
                    'rpm': rpm_val,
                    'description': rpm_desc
                })
            
            # Check for timer/IO access pattern
            timer_result = is_timer_io_access(mnem, operand_bytes, mode)
            if timer_result[0]:  # is_timer
                is_timer, timer_reg, timer_desc = timer_result
                patterns['timer_accesses'].append({
                    'offset': offset,
                    'ram_addr': ram_addr,
                    'instruction': complete_format_instruction(mnem, operand_bytes, mode, ram_addr),
                    'register': timer_reg,
                    'description': timer_desc
                })
            
            # Check for known VY V6 critical addresses
            if mode == "ext" and len(operand_bytes) >= 3:
                target_addr = (operand_bytes[1] << 8) | operand_bytes[2]
                critical_addrs = {
                    0x77DE: "Rev Limiter High",
                    0x77DD: "Rev Limiter Low",
                    0x35FF: "TIC3 (24X Crank) ISR",
                    0x35BD: "TOC3 (EST) ISR",
                    0x77E0: "Fuel Cut Enable",
                }
                if target_addr in critical_addrs:
                    patterns['critical_refs'].append({
                        'offset': offset,
                        'ram_addr': ram_addr,
                        'instruction': complete_format_instruction(mnem, operand_bytes, mode, ram_addr),
                        'target': target_addr,
                        'target_name': critical_addrs[target_addr],
                    })
            
            offset += length
        
        return patterns
    
    def disassemble_enhanced(self, start_offset: int, num_instructions: int = 50,
                            show_patterns: bool = True) -> List[str]:
        """
        Enhanced disassembly using complete opcode module with ECU pattern detection.
        
        Features:
        - Uses hc11_opcodes_complete for 312 opcodes
        - Annotates RPM comparisons
        - Annotates timer/IO accesses
        - Shows XDF calibration labels
        
        Args:
            start_offset: File offset to start
            num_instructions: Number of instructions
            show_patterns: If True, annotate ECU patterns
            
        Returns:
            List of formatted disassembly lines
        """
        results = []
        offset = start_offset
        count = 0
        
        # Header
        ram_start = self.offset_to_cpu_addr(offset)
        
        results.append(f"; === Enhanced Disassembly @ file 0x{offset:05X} (CPU ${ram_start:04X}) ===")
        
        while count < num_instructions and offset < len(self.data):
            # Calculate RAM address
            ram_addr = self.offset_to_cpu_addr(offset)
            
            # Use complete opcodes if available
            if HAS_COMPLETE_OPCODES:
                result = complete_decode_opcode(self.data, offset)
                if result:
                    mnem, length, mode, desc, operand_bytes = result
                    instr = complete_format_instruction(mnem, operand_bytes, mode, ram_addr)
                    hex_bytes = " ".join([f"{b:02X}" for b in operand_bytes])
                    
                    # Get XDF comment for extended addresses
                    xdf_comment = ""
                    if mode == "ext" and len(operand_bytes) >= 3:
                        target = (operand_bytes[1] << 8) | operand_bytes[2]
                        xdf_comment = self.get_xdf_comment(target)
                    elif mode == "dir" and len(operand_bytes) >= 2:
                        xdf_comment = self.get_xdf_comment(operand_bytes[1])
                    
                    line = f"${ram_addr:04X}: {hex_bytes:12s} {instr:30s}{xdf_comment}"
                    results.append(line)
                    
                    # Pattern annotations
                    if show_patterns:
                        rpm_result = is_rpm_comparison(mnem, operand_bytes, mode)
                        if rpm_result[0]:
                            results.append(f"        ; *** RPM COMPARISON: {rpm_result[2]} ***")
                        
                        timer_result = is_timer_io_access(mnem, operand_bytes, mode)
                        if timer_result[0]:
                            results.append(f"        ; *** TIMER ACCESS: {timer_result[2]} ***")
                    
                    offset += length
                else:
                    # Unknown byte
                    byte_val = self.data[offset]
                    results.append(f"${ram_addr:04X}: {byte_val:02X}           DB ${byte_val:02X}  ; Unknown")
                    offset += 1
            else:
                # Fall back to internal disassembler
                instr, length = self.disassemble_instruction(offset)
                results.append(instr)
                offset += length
            
            count += 1
        
        return results


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='HC11 Disassembler - VY V6 Enhanced ECU Binary Analysis',
        epilog='Bank modes: bank1 (64KB), bank2 (32KB engine), bank3 (32KB trans), full (128KB)')
    parser.add_argument('binary', nargs='?', help='Binary file to disassemble')
    parser.add_argument('--bank', choices=['bank1', 'bank2', 'bank3', 'full'],
                        help='Bank mode (auto-detected from filename/size if omitted)')
    parser.add_argument('--base-addr', type=lambda x: int(x, 0),
                        help='Override base address (hex, e.g. 0x8000)')
    args = parser.parse_args()
    
    print("=" * 100)
    print("HC11 DISASSEMBLER - VY V6 Enhanced ECU Binary Analysis")
    print(f"Version: 2.2.0 | Complete Opcodes: {HAS_COMPLETE_OPCODES} | Bank-split support: YES")
    print("=" * 100)
    
    # Determine binary path
    binary_path = args.binary
    bank_mode = args.bank
    
    if binary_path is None:
        # Auto-detect binary path (legacy behavior)
        search_paths = [
            r"R:\VY_V6_Assembly_Modding\VX-VY_V6_$060A_Enhanced_v1.0a - Copy.bin",
            r"A:\VY_V6_Assembly_Modding\92118883_STOCK.bin",
            r"A:\VY_V6_Assembly_Modding\VX-VY_V6_$060A_Enhanced_v1.0a.bin",
        ]
        for path in search_paths:
            if Path(path).exists():
                binary_path = path
                break
        
        if binary_path is None:
            found = find_vy_binaries()
            if found:
                binary_path = str(found[0])
            else:
                print("[ERROR] No VY V6 binary found!")
                return 1
    
    # Auto-detect bank mode from filename if not specified
    if bank_mode is None:
        name_lower = Path(binary_path).name.lower()
        if 'bank1' in name_lower:
            bank_mode = 'bank1'
        elif 'bank2' in name_lower:
            bank_mode = 'bank2'
        elif 'bank3' in name_lower:
            bank_mode = 'bank3'
        # else: auto-detect from file size in HC11Disassembler.__init__
    
    print(f"[OK] Using binary: {binary_path}")
    if bank_mode:
        print(f"[OK] Bank mode: {bank_mode}")
    
    # Create disassembler with appropriate settings
    if args.base_addr is not None:
        dis = HC11Disassembler(binary_path, base_addr=args.base_addr, bank=bank_mode)
    elif bank_mode:
        dis = HC11Disassembler(binary_path, bank=bank_mode)
    else:
        dis = HC11Disassembler(binary_path, base_addr=0x0)
    
    # Determine scan ranges based on bank mode
    file_size = len(dis.data)
    if bank_mode in ('bank2', 'bank3') or (bank_mode is None and file_size == 0x8000):
        # 32KB bank file — scan entire file as code
        code_scan_start = 0x0000
        code_scan_end = file_size
        cal_scan_start = None  # No calibration in bank 2/3 files
        cal_scan_end = None
    elif bank_mode == 'bank1' or (bank_mode is None and file_size == 0x10000):
        # 64KB bank 1 — code at $2000+, cal at $4000-$7FFF
        code_scan_start = 0x2000
        code_scan_end = file_size
        cal_scan_start = 0x7000
        cal_scan_end = 0x8000
    else:
        # Full 128KB — legacy scan ranges
        code_scan_start = 0x10000
        code_scan_end = 0x1FFFF
        cal_scan_start = 0x17000
        cal_scan_end = 0x18000
    
    # NEW: ECU Pattern Detection (if complete opcodes available)
    if HAS_COMPLETE_OPCODES:
        print("\n" + "=" * 100)
        print(" NEW! ECU PATTERN DETECTION (hc11_opcodes_complete integrated)")
        print("=" * 100)
        print("Scanning code region for ECU-specific patterns...")
        
        patterns = dis.detect_ecu_patterns(code_scan_start, code_scan_end)
        
        print(f"\n  RPM Comparisons Found: {len(patterns['rpm_comparisons'])}")
        for p in patterns['rpm_comparisons'][:10]:  # Show first 10
            print(f"    ${p['ram_addr']:04X}: {p['instruction']}")
            print(f"           -> {p['description']}")
        
        print(f"\n  Timer/IO Accesses Found: {len(patterns['timer_accesses'])}")
        for p in patterns['timer_accesses'][:10]:  # Show first 10
            print(f"    ${p['ram_addr']:04X}: {p['instruction']}")
            print(f"           -> {p['description']}")
        
        print(f"\n  Critical Address References: {len(patterns['critical_refs'])}")
        for p in patterns['critical_refs']:
            print(f"    ${p['ram_addr']:04X}: {p['instruction']}")
            print(f"           -> {p['target_name']} @ ${p['target']:04X}")
    
    # ANALYSIS 0: Rev Limiter Table Annotation
    # Only meaningful for full binary or bank1 (where calibration lives)
    if bank_mode not in ('bank2', 'bank3'):
        print("\n" + "=" * 100)
        print(" ANALYSIS 0: REV LIMITER TABLE @ 0x77DE (RPM × 25 SCALING)")
        print("=" * 100)
        if 0x77DE < len(dis.data):
            table_lines = dis.annotate_table_data(0x77DE, 12)
            for line in table_lines:
                print(line)
        else:
            print("  [SKIP] Address 0x77DE outside this bank's file range")
        print()
    
    # NEW CRITICAL ANALYSIS: Find what code USES the limiter table
    print("\n" + "=" * 100)
    print(" ANALYSIS 0A: FIND ALL CODE THAT REFERENCES 0x77DE REV LIMITER TABLE")
    print("=" * 100)
    print(f"Searching {len(dis.data)} bytes for instructions that reference 0x77DE...")
    print()
    
    refs = dis.find_specific_address_references(0x77DE, 0, len(dis.data))
    print(f"Found {len(refs)} references to 0x77DE:")
    print()
    
    for offset, instr, context in refs:
        print(f"[{context:8s}] {instr}")
        print(f"   Context (±5 instructions):")
        context_code = dis.disassemble_with_context(offset, before=5, after=5)
        for line in context_code:
            print(f"   {line}")
        print()
    
    # Also check related addresses from XDF
    print("\n" + "=" * 100)
    print(" ANALYSIS 0B: FUEL CUTOFF RELATED PARAMETERS")
    print("=" * 100)
    related_addrs = [
        (0x77EC, "Time delay parameter"),
        (0x77EE, "AFR ratio parameter 1"),
        (0x77EF, "AFR ratio parameter 2"),
    ]
    
    for addr, desc in related_addrs:
        print(f"\n{desc} @ 0x{addr:04X}:")
        refs = dis.find_specific_address_references(addr, 0, len(dis.data))
        if refs:
            for offset, instr, context in refs[:3]:  # Show first 3
                print(f"  [{context:8s}] {instr}")
        else:
            print(f"  No references found")
    print()
    
    # Analyze the address found in BMW Master Plan (only for full binary or bank2)
    file_offset_17283 = 0x17283 if bank_mode is None or bank_mode == 'full' else None
    if bank_mode == 'bank2':
        # In bank2, file offset 0x17283 becomes 0x17283 - 0x10000 = 0x7283
        file_offset_17283 = 0x7283
    
    if file_offset_17283 is not None and file_offset_17283 < len(dis.data):
        print("\n" + "=" * 100)
        cpu_addr = dis.offset_to_cpu_addr(file_offset_17283)
        print(f"[ANALYSIS] ANALYSIS 1: CODE AT FILE OFFSET 0x{file_offset_17283:05X} (CPU ${cpu_addr:04X})")
        print("=" * 100)
        print("This address was referenced in BMW Master Plan patches")
        print()
        
        instructions = dis.disassemble_range(file_offset_17283, 30)
        for instr in instructions:
            print(instr)
    else:
        print("\n[SKIP] ANALYSIS 1: BMW Master Plan address not in this bank")
    
    # NEW: Find RPM comparisons
    print("\n" + "=" * 100)
    print(" ANALYSIS 0C: SEARCH FOR RPM COMPARISON INSTRUCTIONS")
    print("=" * 100)
    print("Looking for CMPA/CMPB that might compare current RPM vs limiter...")
    print()
    
    # Search in code regions
    comparisons = dis.find_rpm_comparisons(code_scan_start, code_scan_end)
    
    # Filter for likely RPM values (150-255 = 3750-6375 RPM in ×25 scaling)
    rpm_likely = [(off, instr, val) for off, instr, val in comparisons 
                  if val and 150 <= val <= 255]
    
    print(f"Found {len(rpm_likely)} compare instructions with RPM-like values:")
    print()
    for offset, instr, val in rpm_likely[:20]:  # Show first 20
        if val < 256:  # Single byte
            rpm = val * 25
            print(f"{instr}  ; Possible {rpm} RPM (×25)")
        print()
    
    # Find all calibration table reads in code region
    print("\n" + "=" * 100)
    print(" ANALYSIS 2: CALIBRATION READS IN CODE REGION")
    print("=" * 100)
    print("Scanning for calibration memory reads (0x4000-0x7FFF)...")
    print()
    
    if cal_scan_start is not None:
        reads = dis.find_calibration_reads(cal_scan_start, cal_scan_end)
    else:
        # Bank 2/3: scan entire file for references to calibration addresses
        reads = dis.find_calibration_reads(0, len(dis.data))
    print(f"Found {len(reads)} calibration read instructions:")
    print()
    for offset, instr in reads[:50]:  # Show first 50
        print(instr)
    
    # Analyze vector table at end of binary
    print("\n" + "=" * 100)
    print(" ANALYSIS 3: HC11 INTERRUPT VECTOR TABLE (END OF BINARY)")
    print("=" * 100)
    
    vector_offset = len(dis.data) - 16
    print(f"Vector table at file offset 0x{vector_offset:05X} (RAM 0x{dis.get_ram_addr(vector_offset):05X})")
    print()
    
    vectors = [
        ("IRQ", vector_offset + 10),
        ("XIRQ", vector_offset + 8),
        ("SWI", vector_offset + 6),
        ("Illegal Opcode", vector_offset + 4),
        ("COP Failure", vector_offset + 2),
        ("RESET", vector_offset + 0),
    ]
    
    for name, voffset in vectors:
        addr = dis.read_word(voffset)
        print(f"{name:20s} vector: 0x{addr:04X}")
    
    # NEW: Disassemble ISRs at vector addresses
    print("\n" + "=" * 100)
    print(" ANALYSIS 4: INTERRUPT SERVICE ROUTINE (ISR) CODE")
    print("=" * 100)
    print("These are the actual functions that run when hardware events occur:")
    print()
    
    for name, voffset in vectors:
        isr_addr = dis.read_word(voffset)
        
        # Convert RAM address to file offset
        if isr_addr >= dis.base_addr:
            isr_offset = isr_addr - dis.base_addr
            
            if isr_offset < len(dis.data):
                print(f"\n--- {name} Handler @ 0x{isr_addr:04X} (file offset 0x{isr_offset:05X}) ---")
                
                # Disassemble first 20 instructions of ISR
                isr_code = dis.disassemble_range(isr_offset, 20)
                for line in isr_code:
                    print(line)
                    # Stop at RTI (return from interrupt)
                    if "RTI" in line and not "LDAA" in line:
                        print("   ... (RTI - end of ISR)")
                        break
    
    print("\n" + "=" * 100)
    print(" DISASSEMBLY COMPLETE")
    print("=" * 100)
    
    return 0


class HC11DisassemblerCLI(CLIBase if HAS_CORE_UTILS else object):
    """CLI wrapper for HC11 disassembler with modern argument parsing"""
    
    TOOL_NAME = "HC11 Disassembler"
    TOOL_DESCRIPTION = "Motorola 68HC11 binary disassembler with XDF integration"
    TOOL_VERSION = "2.2.0"
    
    def __init__(self):
        if HAS_CORE_UTILS:
            super().__init__()
            self.setup_tool_arguments()
        else:
            # Fallback to legacy mode
            pass
    
    def setup_tool_arguments(self):
        """Add disassembler-specific arguments"""
        self.parser.add_argument('binary', nargs='?', type=str,
                                help='Binary file to disassemble')
        self.parser.add_argument('--bank', choices=['bank1', 'bank2', 'bank3', 'full'],
                                help='Bank mode (auto-detected from filename/size if omitted)')
        self.parser.add_argument('--base-addr', type=lambda x: int(x, 0),
                                help='Override base address (hex, e.g. 0x8000)')
        self.parser.add_argument('--start', type=lambda x: int(x, 0), default=0,
                                help='Start offset in file (default: 0)')
        self.parser.add_argument('--length', type=lambda x: int(x, 0),
                                help='Number of bytes to disassemble')
        self.parser.add_argument('--xdf', type=str,
                                help='XDF file for labels/comments')
        self.parser.add_argument('--show-vectors', action='store_true',
                                help='Display interrupt vector table')
        self.parser.add_argument('--show-isrs', action='store_true',
                                help='Disassemble ISR handlers')
    
    def run(self):
        """Execute disassembly"""
        if not HAS_CORE_UTILS:
            self.logger.warning("Running in legacy mode (core utils not available)")
            return main()
        
        # Pass CLI args through to main() which handles all the analysis
        # Reconstruct sys.argv so main()'s argparse picks up the same args
        import sys
        argv_rebuild = []
        if hasattr(self.args, 'binary') and self.args.binary:
            argv_rebuild.append(self.args.binary)
        if hasattr(self.args, 'bank') and self.args.bank:
            argv_rebuild.extend(['--bank', self.args.bank])
        if hasattr(self.args, 'base_addr') and self.args.base_addr is not None:
            argv_rebuild.extend(['--base-addr', f'0x{self.args.base_addr:X}'])
        
        # Temporarily replace sys.argv for main()'s argparse
        original_argv = sys.argv
        sys.argv = [sys.argv[0]] + argv_rebuild
        try:
            return main()
        finally:
            sys.argv = original_argv


if __name__ == "__main__":
    if HAS_CORE_UTILS:
        tool = HC11DisassemblerCLI()
        sys.exit(tool.execute())
    else:
        sys.exit(main())
