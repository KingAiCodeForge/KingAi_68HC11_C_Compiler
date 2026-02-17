#!/usr/bin/env python3
"""
Binary Differ - Compare Two ECU Binary Files
Shows byte-level differences between stock and patched/tuned binaries
Useful for understanding what changes between OS versions or tune modifications

Author: KingAI Projects  
Date: 2025-11-18
Status: Production Ready
"""

import sys
import argparse
from pathlib import Path
from typing import List, Dict, Tuple
import json


class BinaryDiffer:
    """Compare two binary files and report differences"""
    
    def __init__(self, file1: str, file2: str):
        self.file1 = Path(file1)
        self.file2 = Path(file2)
        
        if not self.file1.exists():
            raise FileNotFoundError(f"File not found: {file1}")
        if not self.file2.exists():
            raise FileNotFoundError(f"File not found: {file2}")
        
        self.data1 = self.file1.read_bytes()
        self.data2 = self.file2.read_bytes()
        
        self.size1 = len(self.data1)
        self.size2 = len(self.data2)
        
    def compare(self, context_bytes: int = 16) -> Dict:
        """
        Compare two binaries and return differences
        
        Args:
            context_bytes: Number of surrounding bytes to show for each difference
            
        Returns:
            Dict with difference analysis
        """
        print(f"\n{'='*80}")
        print(f"BINARY COMPARISON")
        print(f"{'='*80}\n")
        print(f"File 1: {self.file1.name} ({self.size1:,} bytes)")
        print(f"File 2: {self.file2.name} ({self.size2:,} bytes)")
        
        if self.size1 != self.size2:
            print(f"\n⚠️  File sizes differ by {abs(self.size1 - self.size2)} bytes")
        
        # Compare common length
        common_len = min(self.size1, self.size2)
        differences = []
        
        # Find continuous difference regions
        in_diff_region = False
        diff_start = 0
        
        for offset in range(common_len):
            byte1 = self.data1[offset]
            byte2 = self.data2[offset]
            
            if byte1 != byte2:
                if not in_diff_region:
                    diff_start = offset
                    in_diff_region = True
            else:
                if in_diff_region:
                    differences.append((diff_start, offset - 1))
                    in_diff_region = False
        
        # Catch final region if still in diff
        if in_diff_region:
            differences.append((diff_start, common_len - 1))
        
        # Calculate statistics
        total_diff_bytes = sum(end - start + 1 for start, end in differences)
        percent_diff = (total_diff_bytes / common_len) * 100 if common_len > 0 else 0
        
        print(f"\n📊 Statistics:")
        print(f"   Total different bytes: {total_diff_bytes:,} ({percent_diff:.2f}%)")
        print(f"   Number of diff regions: {len(differences)}")
        
        if len(differences) > 0:
            print(f"\n🔍 Difference Regions:\n")
            
            # Show first 20 regions (to prevent overwhelming output)
            for idx, (start, end) in enumerate(differences[:20]):
                length = end - start + 1
                print(f"   Region #{idx+1}: 0x{start:06X} - 0x{end:06X} ({length} bytes)")
                
                # Show hex dump for small regions
                if length <= 64:
                    self._print_hex_diff(start, end, context_bytes)
            
            if len(differences) > 20:
                print(f"\n   ... and {len(differences) - 20} more regions")
        
        result = {
            'file1': str(self.file1),
            'file2': str(self.file2),
            'size1': self.size1,
            'size2': self.size2,
            'total_diff_bytes': total_diff_bytes,
            'percent_different': percent_diff,
            'diff_regions': [{'start': s, 'end': e, 'length': e-s+1} for s, e in differences]
        }
        
        return result
    
    def _print_hex_diff(self, start: int, end: int, context: int):
        """Print hex dump showing differences"""
        # Expand to show context
        ctx_start = max(0, start - context)
        ctx_end = min(min(self.size1, self.size2), end + context + 1)
        
        print(f"\n   Offset   | File 1                     | File 2                     | ASCII")
        print(f"   ---------|----------------------------|----------------------------|-----------------")
        
        for offset in range(ctx_start, ctx_end, 16):
            chunk_end = min(offset + 16, ctx_end)
            
            # File 1 hex
            hex1 = ' '.join(f'{b:02X}' for b in self.data1[offset:chunk_end])
            
            # File 2 hex
            hex2 = ' '.join(f'{b:02X}' for b in self.data2[offset:chunk_end])
            
            # ASCII representation (file1)
            ascii1 = ''.join(chr(b) if 32 <= b < 127 else '.' for b in self.data1[offset:chunk_end])
            
            # Highlight if in diff region
            marker = '>>>' if start <= offset <= end else '   '
            
            print(f"   {marker} {offset:06X} | {hex1:26} | {hex2:26} | {ascii1}")
    
    def export_diff_map(self, output_file: str):
        """Export difference map as JSON for further analysis"""
        result = self.compare()
        
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"\n💾 Difference map exported: {output_file}")
    
    def find_tables(self, min_size: int = 16) -> List[Dict]:
        """
        Identify potential table locations in differences
        Tables often appear as continuous changed regions
        
        Args:
            min_size: Minimum size to consider as a table
            
        Returns:
            List of potential tables with metadata
        """
        result = self.compare()
        
        tables = []
        for region in result['diff_regions']:
            if region['length'] >= min_size:
                # Check if region looks like a table (repetitive structure)
                start = region['start']
                end = region['end']
                
                # Sample data from both files
                sample1 = self.data1[start:end+1]
                sample2 = self.data2[start:end+1]
                
                tables.append({
                    'address': f"0x{start:06X}",
                    'size': region['length'],
                    'potential_type': self._guess_table_type(sample1, sample2)
                })
        
        if tables:
            print(f"\n📋 Potential Tables Found ({len(tables)}):\n")
            for table in tables:
                print(f"   Address: {table['address']}, Size: {table['size']} bytes, Type: {table['potential_type']}")
        
        return tables
    
    def _guess_table_type(self, data1: bytes, data2: bytes) -> str:
        """Heuristic guess at table type based on data patterns"""
        # Check for patterns suggesting table types
        if len(data1) % 2 == 0:  # Could be 16-bit values
            values = [int.from_bytes(data1[i:i+2], 'big') for i in range(0, len(data1), 2)]
            if all(0 <= v <= 100 for v in values):
                return "Percentage/Factor Table"
            elif all(500 <= v <= 8000 for v in values):
                return "RPM Table"
            elif all(0 <= v <= 255 for v in values):
                return "Scalar/Byte Table"
        
        return "Unknown Table Type"


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Compare two ECU binary files and analyze differences",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic comparison
  python binary_differ.py stock.bin tuned.bin
  
  # Export diff map to JSON
  python binary_differ.py stock.bin tuned.bin -o diff_map.json
  
  # Find potential tables
  python binary_differ.py stock.bin enhanced.bin --find-tables
  
  # Custom context bytes
  python binary_differ.py file1.bin file2.bin -c 32
        """
    )
    
    parser.add_argument('file1', help='First binary file (e.g., stock bin)')
    parser.add_argument('file2', help='Second binary file (e.g., tuned bin)')
    parser.add_argument('-o', '--output', help='Output JSON file for diff map')
    parser.add_argument('-c', '--context', type=int, default=16, 
                        help='Context bytes to show (default: 16)')
    parser.add_argument('--find-tables', action='store_true',
                        help='Attempt to identify table locations')
    
    args = parser.parse_args()
    
    try:
        differ = BinaryDiffer(args.file1, args.file2)
        result = differ.compare(context_bytes=args.context)
        
        if args.find_tables:
            differ.find_tables()
        
        if args.output:
            differ.export_diff_map(args.output)
        
        print(f"\n✅ Comparison complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
