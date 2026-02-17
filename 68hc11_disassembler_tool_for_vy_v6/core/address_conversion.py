#!/usr/bin/env python3
"""
================================================================================
 VY V6 $060A Address Conversion Module
================================================================================

WHAT THIS MODULE DOES:
----------------------
Provides unified address conversion between XDF file offsets and CPU addresses
for VY V6 (and compatible) ECU binaries based on MC68HC11 architecture.

This module was inspired by and derived from:
  - tunerpro_exporter.py (KingAI TunerPro Universal Exporter)
  - The1's XDF analysis documentation
  - MC68HC11 reference manual memory maps

KEY CONCEPTS:
-------------
1. XDF Addresses = FILE OFFSETS (byte position in .bin file)
2. CPU Addresses = Runtime memory addresses (what the HC11 sees)
3. The conversion depends on binary size and memory banking

VY V6 128KB BINARY LAYOUT:
--------------------------
The 128KB binary is organized as two 64KB banks:

  File Offset       CPU Address     Region           Description
  ──────────────    ───────────     ──────           ───────────
  0x00000-0x03FFF   N/A             Low Bank Data    Unused/padding
  0x04000-0x07FFF   0x4000-0x7FFF   Calibration      Tables, constants (XDF = CPU!)
  0x08000-0x0FFFF   N/A             Low Bank Code    Rarely used
  0x10000-0x17FFF   0x0000-0x7FFF   High Bank Data   Mirrors low (unused)
  0x18000-0x1FFFF   0x8000-0xFFFF   Program ROM      Executable code

Special Regions (CPU addresses):
  0x0000-0x00FF   Internal RAM (zero page, fast access)
  0x0100-0x01FF   Stack + extended RAM
  0x1000-0x103F   Memory-mapped I/O registers
  0x2000-0x202F   Pseudo-interrupt vectors (jump table)
  0xFFD6-0xFFFF   Hardware interrupt vectors

XDF BASEOFFSET HANDLING:
------------------------
XDF files can specify BASEOFFSET in header:

  <BASEOFFSET offset="0x10000" subtract="1" />

  subtract=0: file_offset = xdf_address + offset
              (File has header/padding before calibration data)
              
  subtract=1: file_offset = xdf_address - offset
              (ECU memory starts at offset, file starts at 0)
              Common for 68HC11-based ECUs

For VY V6 standard binaries, BASEOFFSET is typically 0 (no offset).

USAGE:
------
  from address_conversion import AddressConverter, VY_V6_128KB
  
  # Create converter for VY V6 binary
  conv = AddressConverter(VY_V6_128KB)
  
  # Convert XDF calibration address to CPU
  cpu_addr = conv.xdf_to_cpu(0x77DE)  # Returns 0x77DE (calibration match)
  
  # Convert code address  
  cpu_addr = conv.xdf_to_cpu(0x18000)  # Returns 0x8000 (high bank code)
  
  # Reverse: CPU to file offset
  file_off = conv.cpu_to_file(0x8000)  # Returns 0x18000

SUPPORTED BINARY FORMATS:
-------------------------
- VY_V6_128KB: VY Commodore V6 $060A (128KB)
- VT_V8_256KB: VT-VY V8 LS1 (256KB)
- BMW_512KB: MS42/MS43 512KB (BMW style with BASEOFFSET)

POTENTIAL IMPROVEMENTS:
-----------------------
1. Auto-detect binary format from size and magic bytes
2. Support custom BASEOFFSET from XDF header parsing
3. Add validation against known vector table patterns
4. Handle segmented/banked memory more generically
5. Support for other ECU families (Ford EEC-V, Bosch ME7, etc.)

AUTHOR:
-------
Jason King (KingAIAuto)
Based on tunerpro_exporter.py v3.3.0

Project: VY V6 $060A ECU Reverse Engineering
Date: January 21, 2026
================================================================================
"""

from dataclasses import dataclass
from typing import Optional, Tuple, Dict, List
from enum import Enum, auto


class MemoryRegion(Enum):
    """Memory region types for address classification"""
    UNKNOWN = auto()
    RAM = auto()              # Internal RAM (0x0000-0x01FF)
    IO_REGISTERS = auto()     # Memory-mapped I/O (0x1000-0x103F)
    JUMP_TABLE = auto()       # Pseudo-vectors (0x2000-0x202F)
    CALIBRATION = auto()      # Tables/constants (0x4000-0x7FFF)
    CODE = auto()             # Program ROM (0x8000-0xFFFF)
    VECTOR_TABLE = auto()     # Hardware vectors (0xFFD6-0xFFFF)


@dataclass(frozen=True)
class BinaryFormat:
    """
    Defines a binary format with its memory mapping characteristics.
    
    Attributes:
        name: Human-readable format name
        total_size: Binary file size in bytes
        code_file_start: File offset where code begins
        code_cpu_start: CPU address where code maps to
        cal_file_start: File offset where calibration begins
        cal_cpu_start: CPU address where calibration maps to
        base_offset: BASEOFFSET value (from XDF or known)
        base_subtract: BASEOFFSET subtract flag (0 or 1)
    """
    name: str
    total_size: int
    code_file_start: int
    code_cpu_start: int
    cal_file_start: int
    cal_cpu_start: int
    base_offset: int = 0
    base_subtract: int = 0


# ============================================================================
# PREDEFINED BINARY FORMATS
# ============================================================================

# VY Commodore V6 $060A 128KB binary
VY_V6_128KB = BinaryFormat(
    name="VY V6 $060A 128KB",
    total_size=128 * 1024,  # 0x20000
    code_file_start=0x18000,
    code_cpu_start=0x8000,
    cal_file_start=0x4000,
    cal_cpu_start=0x4000,
    base_offset=0,
    base_subtract=0
)

# VT-VY V8 LS1 256KB binary
VT_V8_256KB = BinaryFormat(
    name="VT V8 LS1 256KB",
    total_size=256 * 1024,  # 0x40000
    code_file_start=0x38000,
    code_cpu_start=0x8000,
    cal_file_start=0x4000,
    cal_cpu_start=0x4000,
    base_offset=0x30000,
    base_subtract=1
)

# BMW MS42/MS43 512KB (typical BASEOFFSET style)
BMW_512KB = BinaryFormat(
    name="BMW MS42/MS43 512KB",
    total_size=512 * 1024,  # 0x80000
    code_file_start=0x48000,
    code_cpu_start=0x8000,
    cal_file_start=0x48000,  # In-ROM calibration
    cal_cpu_start=0x8000,
    base_offset=0x48000,
    base_subtract=0
)

# VL/VN Holden 32KB
VL_VN_32KB = BinaryFormat(
    name="VL/VN Holden 32KB",
    total_size=32 * 1024,  # 0x8000
    code_file_start=0x0000,
    code_cpu_start=0x8000,
    cal_file_start=0x0000,
    cal_cpu_start=0x8000,
    base_offset=0x8000,
    base_subtract=1
)


class AddressConverter:
    """
    Unified address converter for ECU binaries.
    
    Handles conversion between:
    - XDF addresses (file offsets)
    - CPU addresses (runtime memory map)
    - Memory region classification
    
    Based on proven logic from tunerpro_exporter.py _xdf_addr_to_file_offset()
    """
    
    def __init__(self, binary_format: BinaryFormat, custom_base_offset: Optional[int] = None):
        """
        Initialize converter with binary format specification.
        
        Args:
            binary_format: Predefined binary format (VY_V6_128KB, etc.)
            custom_base_offset: Override base offset (e.g., from XDF header)
        """
        self.format = binary_format
        self.base_offset = custom_base_offset if custom_base_offset is not None else binary_format.base_offset
        self.base_subtract = binary_format.base_subtract
        
    def xdf_to_cpu(self, xdf_address: int) -> int:
        """
        Convert XDF file offset to CPU address.
        
        This is the address the HC11 CPU would use at runtime.
        
        Args:
            xdf_address: Address from XDF element (mmedaddress)
            
        Returns:
            int: CPU runtime address
            
        Examples (VY V6 128KB):
            0x77DE -> 0x77DE  (calibration region, direct match)
            0x18000 -> 0x8000 (code region, subtract 0x10000)
        """
        # Calibration region (0x4000-0x7FFF) - direct match
        if self.format.cal_cpu_start <= xdf_address <= (self.format.cal_cpu_start + 0x3FFF):
            return xdf_address
        
        # High bank code region (file 0x18000+ -> CPU 0x8000+)
        if xdf_address >= self.format.code_file_start:
            return (xdf_address - self.format.code_file_start) + self.format.code_cpu_start
        
        # Low bank code (file 0x8000-0xFFFF -> varies)
        if 0x8000 <= xdf_address <= 0xFFFF:
            # For 128KB: this is low bank, typically not used
            return xdf_address
        
        # Default: return as-is (may be RAM or other region)
        return xdf_address
    
    def cpu_to_file(self, cpu_address: int) -> int:
        """
        Convert CPU address to file offset.
        
        This is the byte position in the .bin file.
        
        Args:
            cpu_address: Runtime CPU address
            
        Returns:
            int: File offset to read from
            
        Examples (VY V6 128KB):
            0x8000 -> 0x18000 (code region, add 0x10000)
            0x77DE -> 0x77DE  (calibration, direct match)
        """
        # RAM region - not in file (or at file start for some formats)
        if cpu_address < 0x2000:
            return cpu_address  # May need special handling
        
        # Calibration region (0x4000-0x7FFF)
        if self.format.cal_cpu_start <= cpu_address <= (self.format.cal_cpu_start + 0x3FFF):
            return cpu_address  # Direct match
        
        # Code region (0x8000-0xFFFF -> file 0x18000+)
        if cpu_address >= self.format.code_cpu_start:
            return (cpu_address - self.format.code_cpu_start) + self.format.code_file_start
        
        return cpu_address
    
    def xdf_to_file(self, xdf_address: int, xdf_base_offset: int = 0, xdf_subtract: int = 0) -> int:
        """
        Convert XDF address to file offset using BASEOFFSET rules.
        
        This implements TunerPro's BASEOFFSET semantics:
        - subtract=0: file_offset = xdf_address + offset
        - subtract=1: file_offset = xdf_address - offset
        
        Args:
            xdf_address: Address from XDF mmedaddress
            xdf_base_offset: BASEOFFSET from XDF header (or 0)
            xdf_subtract: subtract flag from XDF header (0 or 1)
            
        Returns:
            int: Actual file offset to read
        """
        # Use provided base offset or instance default
        base_offset = xdf_base_offset if xdf_base_offset != 0 else self.base_offset
        subtract = xdf_subtract if xdf_base_offset != 0 else self.base_subtract
        
        if base_offset == 0:
            return xdf_address
        
        if subtract == 1:
            # subtract=1: ECU addresses start at offset, file starts at 0
            file_offset = xdf_address - base_offset
        else:
            # subtract=0: File has padding/header before calibration
            file_offset = xdf_address + base_offset
        
        # Sanity check
        if file_offset < 0:
            return xdf_address  # Fallback to raw address
        
        return file_offset
    
    def classify_address(self, cpu_address: int) -> MemoryRegion:
        """
        Classify a CPU address by memory region type.
        
        Args:
            cpu_address: CPU runtime address
            
        Returns:
            MemoryRegion: Region classification
        """
        if 0x0000 <= cpu_address <= 0x01FF:
            return MemoryRegion.RAM
        elif 0x1000 <= cpu_address <= 0x103F:
            return MemoryRegion.IO_REGISTERS
        elif 0x2000 <= cpu_address <= 0x202F:
            return MemoryRegion.JUMP_TABLE
        elif 0x4000 <= cpu_address <= 0x7FFF:
            return MemoryRegion.CALIBRATION
        elif 0x8000 <= cpu_address <= 0xFFD5:
            return MemoryRegion.CODE
        elif 0xFFD6 <= cpu_address <= 0xFFFF:
            return MemoryRegion.VECTOR_TABLE
        else:
            return MemoryRegion.UNKNOWN
    
    def is_calibration(self, xdf_address: int) -> bool:
        """Check if XDF address is in calibration region (data, not code)"""
        return self.format.cal_cpu_start <= xdf_address <= (self.format.cal_cpu_start + 0x3FFF)
    
    def is_code(self, xdf_address: int) -> bool:
        """Check if XDF address is in code region"""
        return xdf_address >= self.format.code_file_start
    
    def format_address(self, address: int, include_region: bool = True) -> str:
        """
        Format address for display with optional region label.
        
        Args:
            address: Address to format
            include_region: Include region classification
            
        Returns:
            str: Formatted address string
        """
        cpu_addr = self.xdf_to_cpu(address)
        region = self.classify_address(cpu_addr)
        
        if include_region:
            region_name = {
                MemoryRegion.RAM: "RAM",
                MemoryRegion.IO_REGISTERS: "I/O",
                MemoryRegion.JUMP_TABLE: "JMP",
                MemoryRegion.CALIBRATION: "CAL",
                MemoryRegion.CODE: "CODE",
                MemoryRegion.VECTOR_TABLE: "VEC",
                MemoryRegion.UNKNOWN: "???"
            }.get(region, "???")
            return f"${cpu_addr:04X} [{region_name}]"
        else:
            return f"${cpu_addr:04X}"


def detect_binary_format(bin_path: str) -> Optional[BinaryFormat]:
    """
    Auto-detect binary format from file size and magic patterns.
    
    Args:
        bin_path: Path to binary file
        
    Returns:
        BinaryFormat or None if unknown
    """
    from pathlib import Path
    
    path = Path(bin_path)
    if not path.exists():
        return None
    
    size = path.stat().st_size
    
    # Match by size
    size_formats = {
        128 * 1024: VY_V6_128KB,
        256 * 1024: VT_V8_256KB,
        512 * 1024: BMW_512KB,
        32 * 1024: VL_VN_32KB,
    }
    
    return size_formats.get(size)


def parse_xdf_baseoffset(xdf_path: str) -> Tuple[int, int]:
    """
    Parse BASEOFFSET from XDF header.
    
    Args:
        xdf_path: Path to XDF file
        
    Returns:
        Tuple[int, int]: (offset, subtract_flag)
    """
    import xml.etree.ElementTree as ET
    from pathlib import Path
    
    path = Path(xdf_path)
    if not path.exists():
        return (0, 0)
    
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        
        # Format 1: <BASEOFFSET offset="294912" subtract="0" />
        baseoffset = root.find('.//BASEOFFSET')
        if baseoffset is not None:
            offset_str = baseoffset.get('offset', '0')
            try:
                offset = int(offset_str, 16) if offset_str.lower().startswith('0x') else int(offset_str)
            except ValueError:
                offset = 0
            
            subtract_str = baseoffset.get('subtract', '0')
            try:
                subtract = int(subtract_str)
            except ValueError:
                subtract = 0
            
            return (offset, subtract)
        
        # Format 2: <baseoffset>0</baseoffset> (lowercase simple format)
        baseoffset_simple = root.find('.//baseoffset')
        if baseoffset_simple is not None and baseoffset_simple.text:
            try:
                offset_text = baseoffset_simple.text.strip()
                offset = int(offset_text, 16) if offset_text.lower().startswith('0x') else int(offset_text)
                return (offset, 0)
            except ValueError:
                pass
        
    except ET.ParseError:
        pass
    
    return (0, 0)


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def create_vy_v6_converter() -> AddressConverter:
    """Create converter preconfigured for VY V6 128KB binaries"""
    return AddressConverter(VY_V6_128KB)


def xdf_addr_to_cpu_vy_v6(xdf_address: int) -> int:
    """Quick conversion for VY V6: XDF file offset → CPU address"""
    conv = AddressConverter(VY_V6_128KB)
    return conv.xdf_to_cpu(xdf_address)


def cpu_to_file_vy_v6(cpu_address: int) -> int:
    """Quick conversion for VY V6: CPU address → file offset"""
    conv = AddressConverter(VY_V6_128KB)
    return conv.cpu_to_file(cpu_address)


# ============================================================================
# MAIN - TEST/DEMO
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("VY V6 Address Conversion Module - Test")
    print("=" * 70)
    
    conv = create_vy_v6_converter()
    
    # Test cases
    test_addresses = [
        (0x77DE, "Fuel Cut RPM Table (calibration)"),
        (0x77E2, "Fuel Cut Restore RPM (calibration)"),
        (0x4000, "Calibration start"),
        (0x7FFF, "Calibration end"),
        (0x18000, "Code start (file offset)"),
        (0x35FF, "ISR_TIC3_24X_CRANK (CPU addr, bank2 file=0x135FF)"),
        (0x1FFFF, "Code end (file offset)"),
        (0x00A2, "RAM: RPM variable"),
        (0x1023, "I/O: Timer flag register"),
        (0xFFFE, "Vector: Reset vector"),
    ]
    
    print("\nXDF Address → CPU Address Conversion:")
    print("-" * 70)
    print(f"{'XDF Addr':>10}  {'CPU Addr':>10}  {'Region':>8}  Description")
    print("-" * 70)
    
    for xdf_addr, desc in test_addresses:
        cpu_addr = conv.xdf_to_cpu(xdf_addr)
        region = conv.classify_address(cpu_addr)
        region_name = region.name.replace('_', ' ')[:8]
        print(f"0x{xdf_addr:05X}  →  0x{cpu_addr:04X}    {region_name:>8}  {desc}")
    
    print("\n" + "=" * 70)
    print("CPU Address → File Offset Conversion:")
    print("-" * 70)
    
    cpu_test = [
        (0x8000, "Code start"),
        (0x8100, "Code region"),
        (0x77DE, "Calibration (direct)"),
        (0xFFFF, "Code end"),
    ]
    
    for cpu_addr, desc in cpu_test:
        file_off = conv.cpu_to_file(cpu_addr)
        print(f"CPU 0x{cpu_addr:04X}  →  File 0x{file_off:05X}  ({desc})")
    
    print("\n✓ Address conversion module ready")
