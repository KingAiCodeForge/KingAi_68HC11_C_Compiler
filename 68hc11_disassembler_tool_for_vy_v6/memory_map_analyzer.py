#!/usr/bin/env python3
"""
VY V6 ECU Memory Map Analyzer
============================

This script determines the correct CPU address to file offset mapping for
the 128KB VY V6 ECU binary (Motorola 68HC11 with external flash).

PROBLEM: We need to understand how CPU addresses map to file offsets
for proper Ghidra import and disassembly.

THEORIES:
1. Direct mapping: File offset = CPU address
2. Banked: File 0x10000-0x1FFFF = CPU $8000-$FFFF (upper 64KB = code)
3. Split: Two 64KB banks with bank switching
4. XDF mapping: XDF uses file offsets directly (baseoffset=0)

Author: Jason King (VY V6 Assembly Modding Project)
Date: 2026-01-14
"""

import os
import sys
from pathlib import Path

# Configuration
BIN_DIR = Path(r"R:\VY_V6_Assembly_Modding")
STOCK_BIN = BIN_DIR / "92118883_STOCK.bin"
ENHANCED_BIN = BIN_DIR / "VY_V6_Enhanced.bin"

# Known XDF addresses (file offsets, from v2.09a XDF with baseoffset=0)
KNOWN_XDF_ADDRESSES = {
    0x77DE: ("Rev Limiter High", 0xEC, "Stock=236 (5900 RPM)"),
    0x77DF: ("Rev Limiter Low", 0xEB, "Stock=235 (5875 RPM)"),
    0x19813: ("Min Burn Constant", 0x24, "36 decimal, after LDAA #$24"),
    0x752A: ("Calibration param", None, "From XDF"),
    0x6776: ("Dwell Threshold", None, "If Delta Cylair > This - Then Max Dwell"),
}

# HC11F1 interrupt vectors — Motorola MC68HC11F1 datasheet Table 5-4
# FIXED: Previous version had names scrambled across wrong addresses,
# started at $FFDA (missing SCI+SPI), and swapped COP/CME.
# Verified against: split_and_disassemble.py, vy_v6_constants.py,
# 11p_local_documentation.md, BANK_SWITCHING_AND_ISR_ANALYSIS.md
HC11_VECTORS = {
    0xFFD6: "SCI",              # Serial (ALDL comm)
    0xFFD8: "SPI",              # SPI transfer complete
    0xFFDA: "PAI_Edge",         # Pulse Accumulator Input Edge
    0xFFDC: "PA_Overflow",      # Pulse Accumulator Overflow
    0xFFDE: "Timer_Overflow",   # Timer Overflow (TOF)
    0xFFE0: "TIC4_TOC5",       # Timer IC4 / OC5 (F1 shared)
    0xFFE2: "TOC4",            # Timer Output Compare 4
    0xFFE4: "TOC3",            # Timer Output Compare 3 (EST spark)
    0xFFE6: "TOC2",            # Timer Output Compare 2 (dwell)
    0xFFE8: "TOC1",            # Timer Output Compare 1
    0xFFEA: "TIC3",            # Timer Input Capture 3 (24X crank)
    0xFFEC: "TIC2",            # Timer Input Capture 2 (24X crank)
    0xFFEE: "TIC1",            # Timer Input Capture 1
    0xFFF0: "RTI",             # Real-Time Interrupt
    0xFFF2: "IRQ",             # External IRQ
    0xFFF4: "XIRQ",            # Non-Maskable Interrupt
    0xFFF6: "SWI",             # Software Interrupt
    0xFFF8: "Illegal_Opcode",  # Illegal Opcode Trap
    0xFFFA: "COP_Watchdog",    # COP Failure (watchdog)
    0xFFFC: "Clock_Monitor",   # Clock Monitor Fail
    0xFFFE: "RESET",           # Reset vector
}

def load_binary(path):
    """Load binary file"""
    with open(path, 'rb') as f:
        return f.read()

def read_word(data, offset):
    """Read 16-bit big-endian word"""
    if offset + 1 < len(data):
        return (data[offset] << 8) | data[offset + 1]
    return None

def analyze_vectors(data):
    """Analyze interrupt vector table"""
    print("\n" + "="*60)
    print("INTERRUPT VECTOR ANALYSIS")
    print("="*60)
    
    # In a 128KB file, vectors are at end of file (0x1FFFx)
    # HC11 vectors at CPU $FFxx map to file offset 0x1FFxx
    
    print("\n--- Checking file offset 0x1FFFx (end of 128KB file) ---")
    for vec_offset in sorted(HC11_VECTORS.keys(), reverse=True):
        # CORRECTED: Direct calculation for 128KB binary
        # Vector at CPU $FFFx → file offset 0x1FFFx (for 128KB)
        # file_offset = 0x10000 + (vec_offset - 0x8000) was WRONG
        # Correct: file_offset = vec_offset + 0x10000 for CPU $FFxx addresses
        file_offset = vec_offset + 0x10000  # $FFFx + 0x10000 = 0x1FFFx
        if file_offset < len(data):
            value = read_word(data, file_offset)
            print(f"  0x{file_offset:05X} ({HC11_VECTORS[vec_offset]:8s}): ${value:04X}")
    
    # Check RESET vector specifically at file end
    reset_file_offset = 0x1FFFE
    reset_value = read_word(data, reset_file_offset)
    print(f"\n>>> RESET VECTOR: ${reset_value:04X} (at file offset 0x1FFFE)")
    
    return reset_value

def verify_xdf_addresses(data):
    """Verify known XDF addresses against binary"""
    print("\n" + "="*60)
    print("XDF ADDRESS VERIFICATION (baseoffset=0 means file offsets)")
    print("="*60)
    
    for addr, (name, expected, note) in KNOWN_XDF_ADDRESSES.items():
        if addr < len(data):
            actual = data[addr]
            if expected is not None:
                match = "✅" if actual == expected else "❌"
                print(f"  0x{addr:05X} ({name}): 0x{actual:02X} (expected 0x{expected:02X}) {match}")
            else:
                print(f"  0x{addr:05X} ({name}): 0x{actual:02X} ({note})")
        else:
            print(f"  0x{addr:05X} ({name}): OUT OF RANGE")

def find_code_regions(data):
    """Find regions with actual code (not 0x00 or 0xFF)"""
    print("\n" + "="*60)
    print("CODE REGION ANALYSIS")
    print("="*60)
    
    regions = []
    in_code = False
    start = 0
    
    for i in range(len(data)):
        is_code = data[i] not in (0x00, 0xFF)
        
        if is_code and not in_code:
            start = i
            in_code = True
        elif not is_code and in_code:
            if i - start >= 32:  # Only report regions >= 32 bytes
                regions.append((start, i - 1, i - start))
            in_code = False
    
    if in_code:
        regions.append((start, len(data) - 1, len(data) - start))
    
    print(f"\nFound {len(regions)} code regions (>= 32 bytes):\n")
    for start, end, size in regions[:20]:  # Show first 20
        print(f"  0x{start:05X} - 0x{end:05X} ({size:,} bytes)")
    
    if len(regions) > 20:
        print(f"  ... and {len(regions) - 20} more regions")
    
    # Summary
    total_code = sum(r[2] for r in regions)
    print(f"\nTotal code/data: {total_code:,} bytes ({total_code*100/len(data):.1f}%)")
    
    return regions

def analyze_memory_mapping(data, reset_vector):
    """Determine the memory mapping based on reset vector"""
    print("\n" + "="*60)
    print("MEMORY MAPPING ANALYSIS")
    print("="*60)
    
    # The RESET vector tells us where code execution starts
    # For VY V6, RESET = $C011
    
    print(f"\nRESET vector: ${reset_vector:04X}")
    print(f"Binary size: {len(data):,} bytes (0x{len(data):X})")
    
    # Theory 1: Direct mapping (file offset = CPU address)
    # Would only work for addresses < 0x20000
    if reset_vector < len(data):
        t1_bytes = data[reset_vector:reset_vector+4]
        print(f"\nTheory 1: Direct mapping (file offset = CPU addr)")
        print(f"  ${reset_vector:04X} -> 0x{reset_vector:05X}: {' '.join(f'{b:02X}' for b in t1_bytes)}")
        if t1_bytes[0] not in (0x00, 0xFF):
            print(f"  ✅ Could be valid code")
    
    # Theory 2: 128KB = two 64KB banks
    # Upper bank (file 0x10000-0x1FFFF) maps to CPU $8000-$FFFF
    # Lower bank (file 0x00000-0x0FFFF) maps to CPU $0000-$7FFF or another bank
    if reset_vector >= 0x8000:
        t2_offset = 0x10000 + (reset_vector - 0x8000)
        if t2_offset < len(data):
            t2_bytes = data[t2_offset:t2_offset+4]
            print(f"\nTheory 2: Upper bank at $8000 (file 0x10000)")
            print(f"  ${reset_vector:04X} -> 0x{t2_offset:05X}: {' '.join(f'{b:02X}' for b in t2_bytes)}")
            if t2_bytes[0] not in (0x00, 0xFF):
                print(f"  ✅ LOOKS LIKE VALID CODE!")
    
    # Theory 3: XDF direct file offset
    # XDF addresses ARE file offsets (baseoffset=0)
    # So CPU $181C2 from disassembly = file 0x181C2? No, that's > 128KB
    # Actually, the $1xxxx addresses in docs mean bank 1
    print(f"\nTheory 3: Banked addressing with $1xxxx notation")
    print(f"  CPU $181C2 = Bank 1, offset $81C2")
    print(f"  File offset = 0x10000 + $81C2 - $8000 = 0x{0x10000 + 0x81C2 - 0x8000:05X}")
    
    # Check a known address: $181C2 (Dwell routine start)
    dwell_offset = 0x10000 + (0x81C2 - 0x8000)  # 0x101C2
    if dwell_offset < len(data):
        dwell_bytes = data[dwell_offset:dwell_offset+8]
        print(f"\n  Dwell routine @ file 0x{dwell_offset:05X}:")
        print(f"  {' '.join(f'{b:02X}' for b in dwell_bytes)}")
    
    # Check $AAC5 (TI3 ISR)
    ti3_offset = 0x0AAC5
    if ti3_offset < len(data):
        ti3_bytes = data[ti3_offset:ti3_offset+8]
        print(f"\n  TI3 ISR @ file 0x{ti3_offset:05X} (CPU $0AAC5 - lower bank):")
        print(f"  {' '.join(f'{b:02X}' for b in ti3_bytes)}")

def find_free_space(data):
    """Find contiguous regions of 0x00 or 0xFF"""
    print("\n" + "="*60)
    print("FREE SPACE ANALYSIS")
    print("="*60)
    
    free_regions = []
    current_start = None
    current_fill = None
    
    for i in range(len(data)):
        if data[i] in (0x00, 0xFF):
            if current_start is None:
                current_start = i
                current_fill = data[i]
            elif data[i] != current_fill:
                # Different fill byte, end current region
                if i - current_start >= 64:  # Minimum 64 bytes
                    free_regions.append((current_start, i - 1, i - current_start, current_fill))
                current_start = i
                current_fill = data[i]
        else:
            if current_start is not None:
                if i - current_start >= 64:
                    free_regions.append((current_start, i - 1, i - current_start, current_fill))
                current_start = None
    
    if current_start is not None:
        size = len(data) - current_start
        if size >= 64:
            free_regions.append((current_start, len(data) - 1, size, current_fill))
    
    # Sort by size
    free_regions.sort(key=lambda x: x[2], reverse=True)
    
    print(f"\nFree space regions (>= 64 bytes), sorted by size:\n")
    for start, end, size, fill in free_regions[:15]:
        fill_str = "0x00" if fill == 0x00 else "0xFF"
        print(f"  0x{start:05X} - 0x{end:05X}: {size:6,} bytes ({fill_str})")
    
    total_free = sum(r[2] for r in free_regions)
    print(f"\nTotal free space: {total_free:,} bytes ({total_free*100/len(data):.1f}%)")
    
    return free_regions

def generate_ghidra_import_settings(data, reset_vector):
    """Generate recommended Ghidra import settings"""
    print("\n" + "="*60)
    print("GHIDRA IMPORT RECOMMENDATIONS")
    print("="*60)
    
    print("""
Based on analysis, recommended Ghidra settings:

1. PROCESSOR: 68HC11 (Motorola, Big Endian)
   - Ghidra built-in: "68HC11:BE:16:default"

2. MEMORY MAP (for 128KB binary):
   
   Option A: Two memory blocks (RECOMMENDED)
   ----------------------------------------
   Block 1: "LOWER" 
     - File offset: 0x00000 - 0x0FFFF (65536 bytes)
     - Start address: 0x0000
     - Length: 0x10000
     - Permissions: RWX
     
   Block 2: "UPPER"
     - File offset: 0x10000 - 0x1FFFF (65536 bytes)  
     - Start address: 0x8000
     - Length: 0x8000
     - Permissions: RWX
     - NOTE: This makes $C011 = file offset 0x14011
   
   Option B: Single contiguous block
   ----------------------------------
   Block: "ROM"
     - File offset: 0x00000 - 0x1FFFF (131072 bytes)
     - Start address: 0x0000
     - Length: 0x20000
     - Permissions: RWX
     - NOTE: Addresses in $1xxxx range are file-relative

3. ENTRY POINTS:
   - RESET: $C011 (primary entry point)
   - Add interrupt vectors from $FFD0-$FFFF

4. ADDRESS CONVERSION:
   - For CPU addresses in $8000-$FFFF range:
     file_offset = 0x10000 + (cpu_addr - 0x8000)
   
   - For CPU addresses in $0000-$7FFF range:
     file_offset = cpu_addr
   
   - For "banked" addresses like $181C2:
     Bank 1 ($1xxxx): file_offset = 0x10000 + (addr & 0xFFFF) - 0x8000
     Bank 0 ($0xxxx): file_offset = addr & 0xFFFF
""")
    
    # Verify the conversion
    print("5. ADDRESS VERIFICATION:")
    test_addrs = [
        ("$C011 (RESET)", 0xC011),
        ("0x101C2 (Dwell routine, bank2)", 0x101C2),
        ("$AAC5 (TI3 ISR)", 0x0AAC5),
        ("$77DE (Rev limiter XDF)", 0x77DE),
    ]
    
    for name, addr in test_addrs:
        if addr >= 0x10000:
            # Banked notation ($1xxxx)
            file_offset = 0x10000 + (addr & 0xFFFF) - 0x8000
            cpu_addr = addr & 0xFFFF
        elif addr >= 0x8000:
            # Upper bank
            file_offset = 0x10000 + (addr - 0x8000)
            cpu_addr = addr
        else:
            # Lower bank / direct
            file_offset = addr
            cpu_addr = addr
        
        if file_offset < len(data):
            byte_val = data[file_offset]
            print(f"   {name}: file 0x{file_offset:05X} = 0x{byte_val:02X}")

def main():
    print("="*60)
    print("VY V6 ECU MEMORY MAP ANALYZER")
    print("="*60)
    
    # Choose binary
    if STOCK_BIN.exists():
        bin_path = STOCK_BIN
    elif ENHANCED_BIN.exists():
        bin_path = ENHANCED_BIN
    else:
        print("ERROR: No binary found!")
        return
    
    print(f"\nLoading: {bin_path}")
    data = load_binary(bin_path)
    print(f"Size: {len(data):,} bytes (0x{len(data):X})")
    
    # Run analyses
    reset_vector = analyze_vectors(data)
    verify_xdf_addresses(data)
    find_code_regions(data)
    analyze_memory_mapping(data, reset_vector)
    find_free_space(data)
    generate_ghidra_import_settings(data, reset_vector)
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
