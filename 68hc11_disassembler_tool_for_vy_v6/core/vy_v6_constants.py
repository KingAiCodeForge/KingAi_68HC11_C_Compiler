#!/usr/bin/env python3
"""
VY V6 $060A VERIFIED CONSTANTS MODULE
======================================
SINGLE SOURCE OF TRUTH for all VY V6 analysis scripts.

All constants in this file are VERIFIED by:
1. XDF v2.09a cross-reference (the1's work)
2. Chr0m3 Motorsport testing
3. Binary pattern analysis (January 2026)
4. NXP/Motorola MC68HC11 documentation

DO NOT MODIFY without verification!

Usage:
    from vy_v6_constants import *
    
    or
    
    from vy_v6_constants import BINARY_PATH, RAM_ADDRESSES, TIMING_CONSTANTS

Author: Jason King (KingAustraliaGG)
Last Updated: January 14, 2026
"""

from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Tuple

# ============================================================================
# BINARY FILE PATHS
# ============================================================================

# Primary binary (auto-detect drive: R:, C:, or A:, or relative to this script)
BINARY_PATH_R = Path(r"R:\VY_V6_Assembly_Modding\VX-VY_V6_$060A_Enhanced_v1.0a - Copy.bin")
BINARY_PATH_C = Path(r"C:\Repos\VY_V6_Assembly_Modding\VX-VY_V6_$060A_Enhanced_v1.0a - Copy.bin")
BINARY_PATH_A = Path(r"A:\repos\VY_V6_Assembly_Modding\VX-VY_V6_$060A_Enhanced_v1.0a - Copy.bin")
_SCRIPT_DIR = Path(__file__).resolve().parent
BINARY_PATH_REL = _SCRIPT_DIR.parent.parent / "VX-VY_V6_$060A_Enhanced_v1.0a - Copy.bin"

# Try each location in order
BINARY_PATH = next(
    (p for p in [BINARY_PATH_R, BINARY_PATH_C, BINARY_PATH_A, BINARY_PATH_REL] if p.exists()),
    BINARY_PATH_C  # fallback default
)

# Stock binary for comparison
STOCK_BINARY_PATH = Path(r"R:\VY_V6_Assembly_Modding\VX-VY_V6_$060A_Stock.bin")

# XDF files
XDF_PATH = Path(r"R:\VY_V6_Assembly_Modding\xdf_analysis\v2.09a")

# Output directory
OUTPUT_DIR = Path(r"R:\VY_V6_Assembly_Modding\reports")

# ============================================================================
# HARDWARE SPECIFICATIONS (HC11F-family — 68HC11FC0 per DARC/IDA Pro)
# CORRECTED 2026-02-08: Was HC11E9 with 2MHz. Actual = HC11F @ 3.408MHz.
# Evidence: DARC.BIN line 7, VL400 topic_982, Antus scope topic_4539
# ============================================================================

@dataclass(frozen=True)
class HC11Hardware:
    """HC11F-family derivative (68HC11FC0) hardware specs — VERIFIED"""
    
    # CPU
    CPU_NAME: str = "Motorola 68HC11FC0 (HC11F-family)"
    ARCHITECTURE: str = "8-bit Harvard"
    ENDIANNESS: str = "Big-Endian"
    E_CLOCK_HZ: int = 3_407_872  # 3.408MHz (13.631488MHz crystal ÷ 4)
    
    # Memory sizes
    INTERNAL_RAM: int = 1024     # bytes ($0000-$03FF) — HC11F has 1KB
    INTERNAL_EEPROM: int = 512   # bytes (not used in VY V6)
    
    # Binary size
    CALIBRATION_SIZE: int = 131072  # 128KB

HC11 = HC11Hardware()

# ============================================================================
# MEMORY MAP (VERIFIED January 2026)
# ============================================================================

@dataclass(frozen=True)
class MemoryRegion:
    start: int
    end: int
    name: str
    description: str

MEMORY_MAP = {
    'internal_ram': MemoryRegion(0x0000, 0x00FF, "Internal RAM", "256 bytes zero-page RAM"),
    'stack_vars': MemoryRegion(0x0100, 0x01FF, "Stack/Variables", "Stack and working variables"),
    'pseudo_vectors': MemoryRegion(0x2000, 0x202F, "Pseudo-Vectors", "Interrupt redirect jump table"),
    'calibration': MemoryRegion(0x4000, 0x7FFF, "Calibration", "Fuel/spark tables, scalars"),
    'program_code': MemoryRegion(0x8000, 0xFFD5, "Program Code", "Executable code"),
    'vector_table': MemoryRegion(0xFFD6, 0xFFFF, "Vector Table", "HC11 interrupt vectors"),
}

# ============================================================================
# CONFIRMED RAM ADDRESSES (Binary Analysis + XDF Cross-Reference)
# ============================================================================

RAM_ADDRESSES = {
    # Engine parameters - VERIFIED (72+ reads in code)
    'RPM': 0x00A2,              # Engine RPM (82 reads, 2 writes)
    'RPM_HIGH': 0x00A3,         # RPM high byte (for rev limiter)
    
    # Timing parameters - VERIFIED (TIC3 ISR disassembly 2026-01-31)
    'DWELL_INTERMEDIATE': 0x017B,  # Dwell intermediate calc (STD at file 0x101E1) - NOT crank period!
    'CRANK_PERIOD_24X': 0x194C,    # 24X crank period (STD at $3618 in TIC3 ISR, bank2)
    'DWELL_RAM': 0x0199,        # Dwell time RAM location (3 STD, 1 LDD)
    
    # Status/Mode bytes - CONFIRMED
    'ENGINE_STATUS': 0x0080,    # Engine status flags (needs verification)
}

# ============================================================================
# CONFIRMED FILE OFFSETS (In 128KB Binary)
# ============================================================================

FILE_OFFSETS = {
    # Timing constant locations - VERIFIED
    'MIN_BURN_LDAA': 0x19812,   # LDAA #$24 instruction (MIN_BURN)
    
    # Delta Cylair/Dwell Threshold - VERIFIED Jan 16, 2026
    # XDF: "If Delta Cylair > This - Then Max Dwell"
    'DELTA_CYLAIR_DWELL_VY': 0x6776,   # VY V6 $060A: 0x20 (32) = 125 MG/CYL
    'DELTA_CYLAIR_DWELL_VS': 0x3D49,   # VS V6 $51:   0x20 (32) = 125 MG/CYL
    # NOTE: OSE12P uses 0xA2 (162) but at DIFFERENT address structure!
    
    # Dwell intermediate operations - CORRECTED 2026-02-09
    # $017B is dwell intermediate calc, NOT crank period!
    'DWELL_INTERMEDIATE_STD': 0x101E1,   # STD $017B (store dwell intermediate)
    'DWELL_INTERMEDIATE_LDD': 0x101C2,   # LDD $017B (load dwell intermediate)
    # Actual 24X crank period storage (TIC3 ISR, bank2 only)
    'CRANK_PERIOD_24X_STD': 0x13618,     # STD $194C (store 24X crank period)
    
    # Dwell operations - VERIFIED
    'DWELL_STD_1': 0x1008B,     # STD $0199
    'DWELL_STD_2': 0x101CE,     # STD $0199
    'DWELL_STD_3': 0x101DC,     # STD $0199
    'DWELL_LDD': 0x1007C,       # LDD $0199 (potential hook point)
    
    # Rev limiter scalars - XDF VERIFIED
    'REV_LIMIT_HIGH': 0x77DE,   # Rev limit high threshold (5900 RPM stock)
    'REV_LIMIT_LOW': 0x77DF,    # Rev limit low threshold (5875 RPM stock)
    
    # Timer Control Register Access - VERIFIED Jan 16, 2026
    'TCTL1_INIT_ROUTINE': 0x14769,  # Timer initialization sequence start
    'OC1M_CLEAR': 0x1476F,          # STAA $100C (OC1M = 0)
    'OC1D_CLEAR': 0x14774,          # STAA $100D (OC1D = 0)
    'TCTL1_READ': 0x14778,          # LDAA $1020 (read TCTL1)
    'TCTL1_MASK': 0x1477B,          # ANDA #$30 (mask bits 5-4 only)
    'TCTL1_WRITE': 0x1477D,         # STAA $1020 (write TCTL1)
    'TCTL2_WRITE': 0x14782,         # STAA $1021 (TCTL2 config)
    
    # Free Space Regions - VERIFIED Jan 16, 2026
    'FREE_SPACE_1': (0x0C468, 0x0FFBF, 15192),   # 15KB block
    'FREE_SPACE_2': (0x1CE3F, 0x1FFB1, 12659),   # 12KB block  
    'FREE_SPACE_3': (0x19B0B, 0x1BFFF, 9461),    # 9KB block
}

# ============================================================================
# TIMING CONSTANTS (Chr0m3 Motorsport VALIDATED)
# ============================================================================

@dataclass(frozen=True)
class TimingConstants:
    """Ignition timing constants - Chr0m3 validated for 7200 RPM
    
    ⚠️ CORRECTED January 16, 2026:
    The 0xA2 values were from OSE12P (32KB memcal), NOT VY!
    VY actually uses 0x20 (32) for Delta Cylair/Dwell threshold.
    
    Platform comparison:
    - VY V6 $060A: 0x20 (32) @ 0x6776 = 125 MG/CYL
    - VS V6 $51:   0x20 (32) @ 0x3D49 = 125 MG/CYL
    - OSE12P:      0xA2 (162) = 633 MG/CYL (DIFFERENT!)
    """
    
    # Delta Cylair/Dwell Threshold - VY V6 VERIFIED
    DELTA_CYLAIR_DWELL_ADDR: int = 0x6776  # XDF: "If Delta Cylair > This - Then Max Dwell"
    DELTA_CYLAIR_DWELL_VY: int = 0x20      # 32 decimal = 125 MG/CYL (VY ACTUAL)
    
    # OSE12P values (FOR REFERENCE ONLY - these are NOT VY values!)
    OSE12P_MIN_DWELL: int = 0xA2   # 162 decimal - OSE12P ONLY, NOT VY!
    OSE12P_MIN_BURN: int = 0x24    # 36 decimal - OSE12P ONLY, NOT VY!
    
    # Chr0m3 7200 RPM optimized values (for OSE12P-style modification)
    MIN_DWELL_7200: int = 0x9A    # 154 decimal (saves 8μs)
    MIN_BURN_7200: int = 0x1C     # 28 decimal (saves 8μs)
    
    # RPM limits
    MAX_RPM_STOCK: int = 6375     # 0xFF × 25 = factory limit
    RPM_SOFT_LIMIT: int = 6350    # Above this, timing control degrades
    RPM_HARD_LIMIT: int = 6500    # Timer overflow territory
    RPM_SCALING_FACTOR: int = 25  # XDF confirmed: RPM = value × 25

TIMING = TimingConstants()

# ============================================================================
# VECTOR TABLE (VERIFIED - From binary mapper January 2026)
# Note: 128KB binary uses Bank 1 addresses (0x1FFxx), CPU sees as 0xFFxx
# ============================================================================

# File offsets in 128KB binary (Bank 1 = 0x10000-0x1FFFF)
VECTOR_TABLE_FILE = {
    # File Offset → (Jump Table Target, ISR Name, Actual ISR Code Address)
    0x1FFD6: (0x2003, "SCI", 0x29D3),
    0x1FFD8: (0x2000, "SPI", 0x2BAF),
    0x1FFDA: (0x2000, "PAIE", 0x2BAF),
    0x1FFDC: (0x2000, "PAO", 0x2BAF),
    0x1FFDE: (0x2000, "TOF", 0x2BAF),
    0x1FFE0: (0x2000, "TOC5", 0x2BAF),
    0x1FFE2: (0x2006, "TOC4", 0x35DE),
    0x1FFE4: (0x2009, "TOC3", 0x35BD),  # EST Output
    0x1FFE6: (0x2000, "TOC2", 0x2BAF),
    0x1FFE8: (0x200C, "TOC1", 0x37A6),
    0x1FFEA: (0x200F, "TIC3", 0x35FF),  # 24X CRANK - CRITICAL
    0x1FFEC: (0x2012, "TIC2", 0x358A),  # CAM Sensor
    0x1FFEE: (0x2015, "TIC1", 0x301F),
    0x1FFF0: (0x2000, "RTI", 0x2BAF),
    0x1FFF2: (0x2018, "IRQ", 0x30BA),
    0x1FFF4: (0x201B, "XIRQ", 0x2BAC),
    0x1FFF6: (0x201E, "SWI", 0x2BA0),
    0x1FFF8: (0x2021, "ILLOP", 0x2BA6),
    0x1FFFA: (0xC015, "COP", 0xC015),   # Bank 0
    0x1FFFC: (0xC019, "CME", 0xC019),   # Bank 0
    0x1FFFE: (0xC011, "RESET", 0xC011), # Bank 0 Entry
}

# CPU-view addresses (what HC11 sees after bank switch)
VECTOR_TABLE = {
    # CPU Address → (Jump Table Target, ISR Name, Description)
    0xFFD6: (0x2003, "SCI", "Serial (ALDL)"),
    0xFFD8: (0x2000, "SPI", "SPI transfer"),
    0xFFDA: (0x2000, "PAIE", "Pulse Accum Input Edge"),
    0xFFDC: (0x2000, "PAO", "Pulse Accum Overflow"),
    0xFFDE: (0x2000, "TOF", "Timer Overflow"),
    0xFFE0: (0x2000, "TOC5", "Output Compare 5"),
    0xFFE2: (0x2006, "TOC4", "Output Compare 4"),
    0xFFE4: (0x2009, "TOC3", "EST Spark Control"),
    0xFFE6: (0x2000, "TOC2", "Dwell Start"),
    0xFFE8: (0x200C, "TOC1", "Output Compare 1"),
    0xFFEA: (0x200F, "TIC3", "24X Crank -> 0x35FF"),  # CRITICAL
    0xFFEC: (0x2012, "TIC2", "24X Crank -> 0x358A"),
    0xFFEE: (0x2015, "TIC1", "Input Capture 1"),
    0xFFF0: (0x2000, "RTI", "Real Time Interrupt"),
    0xFFF2: (0x2018, "IRQ", "Main Interrupt"),
    0xFFF4: (0x201B, "XIRQ", "Non-Maskable Interrupt"),
    0xFFF6: (0x201E, "SWI", "Software Interrupt"),
    0xFFF8: (0x2021, "ILLOP", "Illegal Opcode Trap"),
    0xFFFA: (0xC015, "COP", "Watchdog -> Bank 0"),
    0xFFFC: (0xC019, "CME", "Clock Mon -> Bank 0"),
    0xFFFE: (0xC011, "RESET", "Reset -> Bank 0"),
}

# Jump table at 0x2000 -> actual ISR addresses
JUMP_TABLE = {
    0x2000: (0x2BAF, "Default handler (SPI/PAIE/PAO/TOF/TOC5/TOC2/RTI)"),
    0x2003: (0x29D3, "SCI ISR"),
    0x2006: (0x35DE, "TOC4 ISR"),
    0x2009: (0x35BD, "TOC3/EST ISR"),
    0x200C: (0x37A6, "TOC1 ISR"),
    0x200F: (0x35FF, "TIC3/24X Crank ISR - SPARK CUT TARGET"),
    0x2012: (0x358A, "TIC2/CAM Sensor ISR"),
    0x2015: (0x301F, "TIC1 ISR"),
    0x2018: (0x30BA, "IRQ ISR"),
    0x201B: (0x2BAC, "XIRQ ISR"),
    0x201E: (0x2BA0, "SWI ISR"),
    0x2021: (0x2BA6, "ILLOP ISR"),
}

# ============================================================================
# HC11 REGISTER ADDRESSES (HC11F layout — NOT HC11E9)
# ============================================================================

HC11_REGISTERS = {
    # Port A/G/F - HC11F specific layout
    0x1000: "PORTA",    # Port A data
    0x1001: "DDRA",     # Port A data direction (HC11F only)
    0x1002: "PORTG",    # Port G data — bank switching bit 6
    0x1003: "DDRG",     # Port G data direction
    0x1004: "PORTB",    # Port B data
    0x1005: "PORTF",    # Port F data (HC11F only)
    0x1006: "PORTC",    # Port C data
    0x1007: "DDRC",     # Port C data direction
    0x1008: "PORTD",    # Port D data
    0x1009: "DDRD",     # Port D data direction
    0x100A: "PORTE",    # Port E data (ADC inputs)
    
    # Timer system
    0x100E: "TCNT",     # Timer counter (16-bit)
    0x1010: "TIC1",     # Input capture 1
    0x1012: "TIC2",     # Input capture 2
    0x1014: "TIC3",     # Input capture 3 (24X crank)
    0x1016: "TOC1",     # Output compare 1
    0x1018: "TOC2",     # Output compare 2 (dwell)
    0x101A: "TOC3",     # Output compare 3 (EST)
    0x101C: "TOC4",     # Output compare 4
    0x101E: "TOC5",     # Output compare 5
    0x1020: "TCTL1",    # Timer control 1
    0x1021: "TCTL2",    # Timer control 2
    0x1022: "TMSK1",    # Timer mask 1
    0x1023: "TFLG1",    # Timer flag 1
    0x1024: "TMSK2",    # Timer mask 2
    0x1025: "TFLG2",    # Timer flag 2
    
    # Pulse accumulator
    0x1026: "PACTL",    # Pulse accumulator control
    0x1027: "PACNT",    # Pulse accumulator count
    
    # SPI
    0x1028: "SPCR",     # SPI control register
    0x1029: "SPSR",     # SPI status register
    0x102A: "SPDR",     # SPI data register
    
    # SCI (ALDL)
    0x102B: "BAUD",     # Baud rate register
    0x102C: "SCCR1",    # SCI control register 1
    0x102D: "SCCR2",    # SCI control register 2
    0x102E: "SCSR",     # SCI status register
    0x102F: "SCDR",     # SCI data register
    
    # ADC
    0x1030: "ADCTL",    # ADC control register
    0x1031: "ADR1",     # ADC result 1
    0x1032: "ADR2",     # ADC result 2
    0x1033: "ADR3",     # ADC result 3
    0x1034: "ADR4",     # ADC result 4
    
    # System
    0x103C: "INIT",     # RAM/Register mapping
    0x103D: "TEST1",    # Test register 1
    0x103F: "CONFIG",   # Configuration register
}

# ============================================================================
# XDF KNOWN SCALARS (From v2.09a)
# ============================================================================

XDF_SCALARS = {
    # Rev limiter - VERIFIED
    0x77DE: ("Rev Limit High", "RPM", 25),    # value × 25 = RPM
    0x77DD: ("Rev Limit Low", "RPM", 25),
    
    # Fuel cut
    0x77E0: ("Fuel Cut Enable", "flag", 1),
    
    # Speed limiter
    0x77E2: ("Speed Limit", "km/h", 1),
}

# ============================================================================
# CHR0M3 NOTES (Important Warnings)
# ============================================================================

CHR0M3_WARNINGS = """
CHR0M3 MOTORSPORT NOTES (CRITICAL):
====================================
1. "3x period is used for more than spark, altering that willy nilly is not a great idea"
2. "It's not a simple 1 function patch and done - there's a flow to follow"
3. Without MIN_DWELL/MIN_BURN patches, ECU loses spark control at 6350-6500 RPM
4. To achieve 7200 RPM: MIN_DWELL 0xA2→0x9A, MIN_BURN 0x24→0x1C
"""

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def load_binary(path: Path = None) -> bytes:
    """Load binary file, using default path if not specified"""
    p = path or BINARY_PATH
    if not p.exists():
        raise FileNotFoundError(f"Binary not found: {p}")
    return p.read_bytes()

def get_vector_target(data: bytes, vector_addr: int) -> int:
    """Read 16-bit vector target from binary"""
    if vector_addr < len(data) - 1:
        return (data[vector_addr] << 8) | data[vector_addr + 1]
    return 0

def rpm_to_byte(rpm: int) -> int:
    """Convert RPM to byte value using X*25 scaling"""
    return min(255, rpm // TIMING.RPM_SCALING_FACTOR)

def byte_to_rpm(value: int) -> int:
    """Convert byte value to RPM using X*25 scaling"""
    return value * TIMING.RPM_SCALING_FACTOR


# ============================================================================
# SELF-TEST
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("VY V6 $060A VERIFIED CONSTANTS")
    print("=" * 70)
    print()
    print(f"Binary Path: {BINARY_PATH}")
    print(f"Binary Exists: {BINARY_PATH.exists()}")
    print()
    print("CONFIRMED RAM ADDRESSES:")
    for name, addr in RAM_ADDRESSES.items():
        print(f"  {name:20s} = ${addr:04X}")
    print()
    print("TIMING CONSTANTS (Chr0m3 Validated):")
    print(f"  MIN_DWELL (stock): 0x{TIMING.MIN_DWELL_STOCK:02X} ({TIMING.MIN_DWELL_STOCK})")
    print(f"  MIN_BURN (stock):  0x{TIMING.MIN_BURN_STOCK:02X} ({TIMING.MIN_BURN_STOCK})")
    print(f"  MAX RPM (stock):   {TIMING.MAX_RPM_STOCK}")
    print()
    print("CRITICAL VECTOR TARGETS:")
    for addr, (target, name, desc) in VECTOR_TABLE.items():
        if "CONFIRM" in desc.upper() or name in ["RESET", "TIC3", "TOC3"]:
            print(f"  ${addr:04X} {name:6s} → ${target:04X} ({desc})")
    print()
    print("=" * 70)
