#!/usr/bin/env python3
"""
HC11 Interrupt Vector & ISR Analysis Tool v2.0
===============================================
UPDATED to use VERIFIED addresses from vy_v6_constants.py

Analyzes interrupt vectors, traces ISR code, and identifies hardware event handlers.

KEY FINDING (January 2026):
All interrupt vectors in the VY V6 $060A point to PSEUDO-VECTORS at $2000-$202F.
This is because the actual code is in banked/paged memory, and the pseudo-vectors
contain JMP instructions to the real ISR code.

Vector Flow:
  Hardware Event → HC11 Vector ($FFD6-$FFFE) → Pseudo-Vector ($2000-$202F) → Real ISR

Author: Jason King (KingAustraliaGG)
Date: January 14, 2026
"""

import sys
from pathlib import Path
from typing import List, Dict

# Import verified constants
sys.path.insert(0, str(Path(__file__).parent))
try:
    from vy_v6_constants import (
        BINARY_PATH, VECTOR_TABLE, HC11_REGISTERS, load_binary
    )
    HAS_CONSTANTS = True
except ImportError:
    HAS_CONSTANTS = False
    print("WARNING: vy_v6_constants.py not found, using fallback values")

# ============================================================================
# HC11 VECTOR TABLE LAYOUT
# ============================================================================

# Vector table is at the end of the binary
# For 128KB binary: offset 0x1FFD6 to 0x1FFFF
# Each vector is a 16-bit address (big-endian)

HC11_VECTORS = {
    # Offset from $FFD6, Name, Description
    0x00: ("SCI", "Serial Communications Interface"),
    0x02: ("SPI", "SPI Transfer Complete"),
    0x04: ("PAIE", "Pulse Accumulator Input Edge"),
    0x06: ("PAO", "Pulse Accumulator Overflow"),
    0x08: ("TOF", "Timer Overflow"),
    0x0A: ("TOC5", "Output Compare 5"),
    0x0C: ("TOC4", "Output Compare 4"),
    0x0E: ("TOC3", "Output Compare 3 - EST Spark"),  # IMPORTANT
    0x10: ("TOC2", "Output Compare 2 - Dwell"),      # IMPORTANT
    0x12: ("TOC1", "Output Compare 1"),
    0x14: ("TIC3", "Input Capture 3 - 24X Crank"),    # IMPORTANT
    0x16: ("TIC2", "Input Capture 2 - Cam"),
    0x18: ("TIC1", "Input Capture 1"),
    0x1A: ("RTI", "Real Time Interrupt"),
    0x1C: ("IRQ", "External Interrupt"),
    0x1E: ("XIRQ", "Non-Maskable Interrupt"),
    0x20: ("SWI", "Software Interrupt"),
    0x22: ("ILLEGAL", "Illegal Opcode Trap"),
    0x24: ("COP", "Watchdog Failure"),
    0x26: ("CLOCK", "Clock Monitor Failure"),
    0x28: ("RESET", "Reset Vector"),                 # IMPORTANT
}

# Important vectors for ignition timing
IGNITION_VECTORS = {"TOC3", "TOC2", "TIC3", "RESET"}


class InterruptAnalyzer:
    """Analyze HC11 interrupt vectors and ISR code"""
    
    def __init__(self, binary_path: Path = None):
        self.path = binary_path or BINARY_PATH
        self.data = load_binary(self.path) if HAS_CONSTANTS else Path(self.path).read_bytes()
        self.size = len(self.data)
        
        # Vector table offset in file
        # $FFD6 maps to file offset (size - 42) for 128KB binary
        self.vector_base = self.size - 42  # 42 bytes = 21 vectors × 2 bytes
        
    def read_word(self, offset: int) -> int:
        """Read 16-bit big-endian word"""
        if offset < 0 or offset >= self.size - 1:
            return 0
        return (self.data[offset] << 8) | self.data[offset + 1]
    
    def get_vector_target(self, vector_name: str) -> int:
        """Get the target address for a named vector"""
        for offset, (name, desc) in HC11_VECTORS.items():
            if name == vector_name:
                return self.read_word(self.vector_base + offset)
        return 0
    
    def analyze_all_vectors(self):
        """Analyze all interrupt vectors"""
        print("=" * 80)
        print("HC11 INTERRUPT VECTOR ANALYSIS")
        print("=" * 80)
        print()
        print(f"Binary: {self.path.name}")
        print(f"Size: {self.size:,} bytes ({self.size // 1024}KB)")
        print(f"Vector table at file offset: 0x{self.vector_base:05X}")
        print()
        
        # Explain pseudo-vectors
        print("KEY FINDING: All vectors point to PSEUDO-VECTORS at $2000-$202F")
        print("These are JMP instructions that redirect to real ISR code.")
        print()
        
        print("-" * 80)
        print(f"{'Vector':<8} {'Name':<10} {'Target':<8} {'Description':<30} {'Status'}")
        print("-" * 80)
        
        results = []
        for offset in sorted(HC11_VECTORS.keys()):
            name, desc = HC11_VECTORS[offset]
            vec_addr = 0xFFD6 + offset
            target = self.read_word(self.vector_base + offset)
            
            # Check if it's an important vector
            if name in IGNITION_VECTORS:
                status = "⚡ IGNITION"
            elif target >= 0x2000 and target <= 0x202F:
                status = "→ pseudo-vec"
            elif target == 0x0000:
                status = "❌ NULL"
            else:
                status = "→ direct"
            
            print(f"${vec_addr:04X}  {name:<10} ${target:04X}   {desc:<30} {status}")
            results.append((name, vec_addr, target, desc))
        
        print("-" * 80)
        return results
    
    def analyze_pseudo_vectors(self):
        """Analyze the pseudo-vector jump table at $2000-$202F"""
        print()
        print("=" * 80)
        print("PSEUDO-VECTOR TABLE ANALYSIS ($2000-$202F)")
        print("=" * 80)
        print()
        
        # Pseudo-vectors are at file offset 0x2000 (for 128KB binary with $0000 base)
        # But we need to find where $2000 maps in the binary
        # For VY V6, the binary starts at $0000, so $2000 = offset 0x2000
        
        pseudo_base = 0x2000
        if pseudo_base >= self.size:
            print(f"ERROR: Pseudo-vector address ${pseudo_base:04X} outside binary")
            return
        
        print("Pseudo-vectors contain JMP instructions to real ISR code:")
        print()
        print("-" * 60)
        print(f"{'Address':<10} {'Opcode':<15} {'Target':<10} {'Vector'}")
        print("-" * 60)
        
        # Use verified vector table if available
        if HAS_CONSTANTS:
            for vec_addr, (target, name, desc) in VECTOR_TABLE.items():
                # Find pseudo-vector for this target
                offset = target
                if offset < self.size - 2:
                    opcode = self.data[offset]
                    if opcode == 0x7E:  # JMP extended
                        jmp_target = self.read_word(offset + 1)
                        print(f"${target:04X}     JMP ${jmp_target:04X}     ${jmp_target:04X}    {name}")
                    elif opcode == 0x20:  # BRA relative
                        rel = self.data[offset + 1]
                        if rel > 127:
                            rel = rel - 256
                        jmp_target = target + 2 + rel
                        print(f"${target:04X}     BRA ${jmp_target:04X}     ${jmp_target:04X}    {name}")
                    else:
                        print(f"${target:04X}     [{opcode:02X}]           -         {name}")
        else:
            # Scan pseudo-vector area
            for i in range(0, 0x30, 3):
                offset = pseudo_base + i
                if offset >= self.size - 2:
                    break
                opcode = self.data[offset]
                if opcode == 0x7E:  # JMP
                    target = self.read_word(offset + 1)
                    print(f"${pseudo_base + i:04X}     JMP ${target:04X}     ${target:04X}")
                elif opcode == 0x00:
                    continue
                else:
                    print(f"${pseudo_base + i:04X}     [{opcode:02X}]")
        
        print("-" * 60)
    
    def analyze_ignition_isrs(self):
        """Detailed analysis of ignition-related ISRs"""
        print()
        print("=" * 80)
        print("IGNITION TIMING ISR ANALYSIS")
        print("=" * 80)
        print()
        
        print("The ignition system uses these interrupt service routines:")
        print()
        print("1. TIC3 (Input Capture 3) - 24X Crank Sensor")
        print("   - Triggered by each crank tooth (7 per revolution)")
        print("   - Calculates engine RPM from period between pulses")
        print("   - Stores DWELL_INTERMEDIATE at $017B")
        print()
        print("2. TOC3 (Output Compare 3) - EST Spark Control")
        print("   - Generates EST signal to ICM")
        print("   - Controls spark timing angle")
        print("   - Sets next spark event time")
        print()
        print("3. TOC2 (Output Compare 2) - Dwell Control")
        print("   - Controls coil dwell time")
        print("   - Uses DWELL_RAM at $0199")
        print("   - This is where we can hook for ignition cut!")
        print()
        
        # Show vector targets
        for vec_name in ["TIC3", "TOC3", "TOC2"]:
            target = self.get_vector_target(vec_name)
            print(f"   {vec_name} → ${target:04X}")


def main():
    """Main entry point"""
    print()
    
    # Use verified binary path
    if HAS_CONSTANTS:
        binary_path = BINARY_PATH
    else:
        binary_path = Path(r"R:\VY_V6_Assembly_Modding\VX-VY_V6_$060A_Enhanced_v1.0a - Copy.bin")
    
    if not binary_path.exists():
        print(f"ERROR: Binary not found: {binary_path}")
        return 1
    
    analyzer = InterruptAnalyzer(binary_path)
    
    # Run analyses
    analyzer.analyze_all_vectors()
    analyzer.analyze_pseudo_vectors()
    analyzer.analyze_ignition_isrs()
    
    print()
    print("=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print()
    print("KEY TAKEAWAYS:")
    print("• All vectors use pseudo-vector redirection (JMP at $2000-$202F)")
    print("• This allows ISR code to be in banked/paged memory")
    print("• TIC3/TOC3/TOC2 are critical for ignition timing")
    print("• Hook point for ignition cut: DWELL_LDD at file offset 0x1007C")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
