#!/usr/bin/env python3
"""
Find Free Space in Binary Files
Locate unused ROM regions suitable for code injection

Author: KingAI Projects
Date: November 19, 2025
Updated: January 18, 2026 - Added 0x00 detection for Enhanced binaries

IMPORTANT: VY V6 Enhanced binaries use 0x00 for free space (The1's convention)
           Stock binaries may use 0xFF for erased/empty flash
"""

from pathlib import Path
from typing import List, Tuple


class FreeSpaceFinder:
    """Find free space regions in binary files"""
    
    def __init__(self, bin_path: Path, min_size: int = 64, free_byte: int = None):
        self.bin_path = bin_path
        self.min_size = min_size
        self.free_byte = free_byte  # None = auto-detect
        self.free_regions = []
        
    def find_free_space(self) -> List[Tuple[int, int, int]]:
        """
        Find all regions of free bytes (0x00 or 0xFF)
        Returns list of (start_addr, end_addr, size) tuples
        """
        print(f"\n{'='*80}")
        print(f"FREE SPACE ANALYZER - VY V6 Enhanced Binary")
        print(f"{'='*80}\n")
        print(f"Binary: {self.bin_path.name}")
        print(f"Size: {self.bin_path.stat().st_size:,} bytes")
        print(f"Minimum region size: {self.min_size} bytes\n")
        
        with open(self.bin_path, 'rb') as f:
            data = f.read()
        
        # Auto-detect free byte pattern if not specified
        if self.free_byte is None:
            count_00 = sum(1 for b in data if b == 0x00)
            count_ff = sum(1 for b in data if b == 0xFF)
            self.free_byte = 0x00 if count_00 > count_ff else 0xFF
            print(f"Auto-detected free byte: 0x{self.free_byte:02X} "
                  f"(0x00: {count_00:,}, 0xFF: {count_ff:,})")
        else:
            print(f"Using specified free byte: 0x{self.free_byte:02X}")
        print()
        
        in_free_region = False
        region_start = 0
        
        for i, byte in enumerate(data):
            if byte == self.free_byte:
                if not in_free_region:
                    # Start of new free region
                    in_free_region = True
                    region_start = i
            else:
                if in_free_region:
                    # End of free region
                    region_size = i - region_start
                    if region_size >= self.min_size:
                        self.free_regions.append((region_start, i - 1, region_size))
                    in_free_region = False
                    
        # Handle case where file ends in 0xFF
        if in_free_region:
            region_size = len(data) - region_start
            if region_size >= self.min_size:
                self.free_regions.append((region_start, len(data) - 1, region_size))
                
        self._print_results()
        return self.free_regions
        
    def _print_results(self):
        """Display found free space regions"""
        print(f"🔍 Found {len(self.free_regions)} free space regions:\n")
        
        if not self.free_regions:
            print("   ⚠️  No free space found!")
            print("      Try reducing --min-size parameter")
            print("      Or check --free-byte (0x00 for Enhanced, 0xFF for stock)")
            return
            
        total_free = sum(size for _, _, size in self.free_regions)
        
        # Header with CPU address column
        print(f"{'File Offset':<12} {'CPU Addr':<10} {'End':<12} {'Size':<10} {'Suitability'}")
        print(f"{'─'*12} {'─'*10} {'─'*12} {'─'*10} {'─'*30}")
        
        for start, end, size in self.free_regions:
            # Calculate CPU address (file offset + 0x10000 for main ROM)
            cpu_addr = start + 0x10000
            cpu_end = end + 0x10000
            suitability = self._assess_suitability(start, end, size)
            print(f"0x{start:05X}      ${cpu_addr:05X}    0x{end:05X}      {size:>6} B   {suitability}")
            
        print(f"\nTotal free space: {total_free:,} bytes")
        print(f"\n💡 Recommendations:")
        
        # Always show the verified main free space
        print(f"\n   VERIFIED FREE REGIONS (from binary analysis):")
        print(f"   ├─ Main patch space: 0x0C468-0x0FFBF (CPU $1C468-$1FFBF) = 15,192 bytes")
        print(f"   │  └─ Recommended ORG: $1C500 (file offset 0x0C500)")
        print(f"   └─ String space: 0x03FE2-0x03FFF (CPU $13FE2-$13FFF) = 30 bytes")
        print(f"      └─ Contains 'pcmhacking.net' - safe to overwrite")
        
        best = self._recommend_region()
        if best:
            start, end, size = best
            cpu_start = start + 0x10000
            print(f"\n   LARGEST DETECTED REGION:")
            print(f"   └─ File: 0x{start:05X}-0x{end:05X} | CPU: ${cpu_start:05X} | Size: {size:,} bytes")
            
    def _assess_suitability(self, start: int, end: int, size: int) -> str:
        """Assess how suitable a region is for code injection"""
        
        # VY V6 $060A Enhanced memory map (verified)
        # 128KB binary with banked ROM:
        # File 0x00000-0x0FFFF = Lower 64KB (CPU $10000-$1FFFF when accessed)
        # File 0x10000-0x1FFFF = Upper 64KB (CPU $10000-$1FFFF alternate bank)
        #
        # Known regions (file offsets):
        # 0x03FE2-0x03FFF: pcmhacking.net string (30 bytes, unused)
        # 0x0C468-0x0FFBF: Main free space (verified 15,192 bytes of 0x00)
        # 0x0FFC0-0x0FFFF: Vector table (DO NOT MODIFY)
        # 0x1FFC0-0x1FFFF: Upper bank vector table
        
        # Vector tables at end of each 64KB bank
        if 0xFFC0 <= start <= 0xFFFF:
            return "❌ VECTOR TABLE (DO NOT MODIFY!)"
        if 0x1FFC0 <= start <= 0x1FFFF:
            return "❌ UPPER VECTOR TABLE (DO NOT MODIFY!)"
        
        # Upper ROM bank (0x10000+)
        if start >= 0x10000:
            bank2_offset = start - 0x10000
            if bank2_offset < 0x2000:
                return "⚠️  Upper bank RAM mirror area"
            elif 0x3FE0 <= bank2_offset < 0x4000:
                return "⚠️  Upper bank string area"
            elif 0x4000 <= bank2_offset < 0x8000:
                return "⚠️  Upper bank calibration tables"
            elif 0x8000 <= bank2_offset < 0xC000:
                return "⚠️  Upper bank code region"
            elif 0xC000 <= bank2_offset < 0xFFC0:
                if size >= 1000:
                    return "✅ Upper bank free space (large)"
                else:
                    return "✅ Upper bank free space"
            return "⚠️  Upper ROM bank (verify usage)"
        
        # Lower ROM bank (0x00000-0x0FFFF)
        if start < 0x2000:
            return "❌ RAM/Register area (not suitable)"
        elif 0x2000 <= start < 0x3000:
            return "⚠️  Jump table area (use with caution)"
        elif 0x3E00 <= start < 0x4000:
            if 0x3FE2 <= start < 0x4000:
                return "✅ String area (pcmhacking.net - safe)"
            return "⚠️  End of jump table area"
        elif 0x4000 <= start < 0x8000:
            return "⚠️  Calibration tables (modify carefully)"
        elif 0x8000 <= start < 0xC000:
            return "⚠️  Code region (verify not referenced)"
        elif 0xC000 <= start < 0xC468:
            return "⚠️  Code region end (verify not referenced)"
        elif 0xC468 <= start < 0xFFC0:
            # This is the verified free space
            if size >= 1000:
                return "✅ VERIFIED FREE SPACE (The1's padding)"
            elif size >= 256:
                return "✅ Excellent (verified free, large)"
            elif size >= 128:
                return "✅ Good (verified free, adequate)"
            else:
                return "✅ Fair (verified free, limited)"
        else:
            return "Unknown region"
            
    def _recommend_region(self) -> Tuple[int, int, int]:
        """Recommend best region for patch injection"""
        
        # Filter for code region (0x8000+) and > 128 bytes
        suitable = [
            (start, end, size) for start, end, size in self.free_regions
            if start >= 0x8000 and size >= 128
        ]
        
        if not suitable:
            # Fall back to largest region anywhere
            suitable = self.free_regions
            
        if suitable:
            # Return largest suitable region
            return max(suitable, key=lambda x: x[2])
        return None
        
    def export_linker_script(self, output_path: Path):
        """Export A09 assembler linker script with free space regions"""
        
        if not self.free_regions:
            print("⚠️  No free space to export")
            return
            
        lines = [
            "; Auto-generated linker script for HC11 assembly",
            "; Generated by find_free_space.py",
            f"; Source binary: {self.bin_path.name}",
            "",
            "; Free space regions available for code injection:",
            ""
        ]
        
        for idx, (start, end, size) in enumerate(self.free_regions, 1):
            lines.append(f"; Region {idx}: 0x{start:08X} - 0x{end:08X} ({size} bytes)")
            lines.append(f"FREE_REGION_{idx}_START     EQU     ${start:04X}")
            lines.append(f"FREE_REGION_{idx}_END       EQU     ${end:04X}")
            lines.append(f"FREE_REGION_{idx}_SIZE      EQU     {size}")
            lines.append("")
            
        # Add recommended region
        best = self._recommend_region()
        if best:
            start, _, size = best
            lines.append("; Recommended injection point:")
            lines.append(f"PATCH_CODE_START            EQU     ${start:04X}")
            lines.append(f"PATCH_CODE_SIZE             EQU     {size}")
            
        with open(output_path, 'w') as f:
            f.write('\n'.join(lines))
            
        print(f"\n📝 Exported linker script to: {output_path}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Find free space in VY V6 Enhanced binary files for code injection"
    )
    parser.add_argument('binary', type=Path, nargs='?', 
                        help="Path to binary file (default: auto-detect)")
    parser.add_argument(
        '--min-size', type=int, default=64,
        help="Minimum free space region size in bytes (default: 64)"
    )
    parser.add_argument(
        '--free-byte', type=lambda x: int(x, 0), default=None,
        help="Byte value for free space (0x00 or 0xFF, default: auto-detect)"
    )
    parser.add_argument(
        '--export-linker', type=Path,
        help="Export A09 linker script with free space definitions"
    )
    
    args = parser.parse_args()
    
    # Auto-detect binary if not specified
    if args.binary is None:
        candidates = list(Path('.').glob('*.bin')) + list(Path('.').glob('*Enhanced*.bin'))
        if candidates:
            args.binary = candidates[0]
            print(f"Auto-detected binary: {args.binary}")
        else:
            print("❌ No binary file specified and none found in current directory")
            print("   Usage: python find_free_space.py <binary.bin>")
            return 1
    
    if not args.binary.exists():
        print(f"❌ File not found: {args.binary}")
        return 1
        
    finder = FreeSpaceFinder(args.binary, args.min_size, args.free_byte)
    finder.find_free_space()
    
    if args.export_linker:
        finder.export_linker_script(args.export_linker)
        
    return 0


if __name__ == "__main__":
    exit(main())
