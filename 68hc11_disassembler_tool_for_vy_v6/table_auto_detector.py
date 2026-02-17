#!/usr/bin/env python3
"""
Table Auto-Detector - Find calibration lookup tables by code pattern analysis
==============================================================================
Detects 1D and 2D tables by analyzing instruction patterns:
- LDX #$table followed by table lookup operations
- ABX/ABY for index calculation
- LDAA/LDAB 0,X for value retrieval

Author: Jason King (KingAI Pty Ltd)
Date: 2026-01-26
"""

import os
import sys
import json
import argparse
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
import re


@dataclass
class TableCandidate:
    """Potential calibration table"""
    address: int
    references: List[int] = field(default_factory=list)
    estimated_size: int = 0
    table_type: str = 'unknown'  # '1d', '2d', 'unknown'
    axis_x: Optional[int] = None
    axis_y: Optional[int] = None
    index_source: str = ''  # What register/value is used for indexing
    confidence: float = 0.0
    

@dataclass
class TableAccess:
    """A single table access pattern in code"""
    location: int
    table_addr: int
    pattern: str
    context_before: List[Tuple[int, int]] = field(default_factory=list)  # [(addr, opcode), ...]
    context_after: List[Tuple[int, int]] = field(default_factory=list)


class TableAutoDetector:
    """Detect calibration tables by analyzing code patterns"""
    
    # Common table lookup patterns
    # Pattern 1: LDX #$table; ABX; LDAB 0,X (1D byte table)
    # Pattern 2: LDX #$table; LDAB offset,X (1D direct index)
    # Pattern 3: LDX #$table; ABX; LDD 0,X (1D word table)
    # Pattern 4: Two nested lookups (2D table)
    
    # Opcodes for pattern detection
    LDX_IMM = 0xCE  # LDX #$nnnn
    LDY_IMM = 0x18CD  # 18 CE = LDY #$nnnn (prebyte)
    ABX = 0x3A
    ABY = 0x183A
    LDAA_IDX = 0xA6  # LDAA offset,X
    LDAB_IDX = 0xE6  # LDAB offset,X
    LDD_IDX = 0xEC   # LDD offset,X
    STD_IDX = 0xED   # STD offset,X
    
    # VY V6 calibration regions
    CAL_REGIONS = [
        (0x4000, 0x8000, 'LOW_CAL'),    # Low bank calibration
        (0x8000, 0xE000, 'HIGH_CAL'),   # High bank calibration
    ]
    
    def __init__(self, bin_path: str, xdf_path: str = None):
        self.bin_path = bin_path
        self.xdf_path = xdf_path
        self.data = None
        self.size = 0
        self.xdf_tables: Set[int] = set()
        self.candidates: Dict[int, TableCandidate] = {}
        self.table_accesses: List[TableAccess] = []
        
    def load_binary(self) -> bool:
        try:
            with open(self.bin_path, 'rb') as f:
                self.data = f.read()
            self.size = len(self.data)
            return True
        except Exception as e:
            print(f"Error loading: {e}")
            return False
            
    def load_xdf(self):
        """Load existing XDF table addresses for comparison"""
        if not self.xdf_path or not os.path.exists(self.xdf_path):
            return
            
        try:
            with open(self.xdf_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # Find all table addresses
            for match in re.finditer(r'mmedaddress="0x([0-9A-Fa-f]+)"', content):
                addr = int(match.group(1), 16)
                self.xdf_tables.add(addr)
                
            print(f"Loaded {len(self.xdf_tables)} addresses from XDF")
        except Exception as e:
            print(f"Error loading XDF: {e}")
            
    def _cpu_to_file(self, cpu_addr: int) -> int:
        """Convert CPU address to file offset"""
        if cpu_addr >= 0x8000:
            return cpu_addr - 0x8000 + 0x10000
        return cpu_addr
        
    def _is_calibration_addr(self, addr: int) -> bool:
        """Check if address is in calibration region"""
        for start, end, _ in self.CAL_REGIONS:
            if start <= addr < end:
                return True
        return False
        
    def scan_for_ldx_patterns(self, start: int, end: int) -> List[TableAccess]:
        """Scan code region for LDX #$table patterns"""
        accesses = []
        pc = start
        
        while pc < end - 3:
            opcode = self.data[pc]
            
            # Check for LDX #$nnnn (0xCE)
            if opcode == self.LDX_IMM:
                addr = (self.data[pc + 1] << 8) | self.data[pc + 2]
                
                # Check if this points to calibration region
                if self._is_calibration_addr(addr):
                    access = TableAccess(
                        location=pc,
                        table_addr=addr,
                        pattern='LDX_IMM'
                    )
                    
                    # Analyze following instructions
                    self._analyze_table_access(access, pc + 3, end)
                    accesses.append(access)
                    
                    # Track candidate
                    if addr not in self.candidates:
                        self.candidates[addr] = TableCandidate(addr)
                    self.candidates[addr].references.append(pc)
                    
                pc += 3
                
            # Check for LDY #$nnnn (0x18 0xCE)
            elif opcode == 0x18 and pc + 1 < end and self.data[pc + 1] == 0xCE:
                if pc + 4 <= end:
                    addr = (self.data[pc + 2] << 8) | self.data[pc + 3]
                    
                    if self._is_calibration_addr(addr):
                        access = TableAccess(
                            location=pc,
                            table_addr=addr,
                            pattern='LDY_IMM'
                        )
                        accesses.append(access)
                        
                        if addr not in self.candidates:
                            self.candidates[addr] = TableCandidate(addr)
                        self.candidates[addr].references.append(pc)
                        
                pc += 4
            else:
                pc += 1
                
        return accesses
        
    def _analyze_table_access(self, access: TableAccess, start_pc: int, end: int):
        """Analyze instructions following LDX to determine table type"""
        pc = start_pc
        max_look = min(start_pc + 20, end)  # Look at next 20 bytes max
        
        patterns = []
        
        while pc < max_look:
            opcode = self.data[pc]
            
            if opcode == self.ABX:
                patterns.append('ABX')
                pc += 1
            elif opcode == self.LDAA_IDX:
                offset = self.data[pc + 1] if pc + 1 < end else 0
                patterns.append(f'LDAA_{offset},X')
                pc += 2
            elif opcode == self.LDAB_IDX:
                offset = self.data[pc + 1] if pc + 1 < end else 0
                patterns.append(f'LDAB_{offset},X')
                pc += 2
            elif opcode == self.LDD_IDX:
                offset = self.data[pc + 1] if pc + 1 < end else 0
                patterns.append(f'LDD_{offset},X')
                pc += 2
            elif opcode == 0x3A:  # ABX
                patterns.append('ABX')
                pc += 1
            elif opcode == 0x58:  # ASLB
                patterns.append('ASLB')
                pc += 1
            elif opcode in (0x39, 0x3B, 0x7E, 0x20):  # RTS, RTI, JMP, BRA
                break  # End of sequence
            else:
                # Unknown - just advance
                pc += 1
                
            if len(patterns) >= 5:
                break
                
        access.pattern = ' -> '.join(patterns) if patterns else 'UNKNOWN'
        
        # Determine table type from pattern
        candidate = self.candidates.get(access.table_addr)
        if candidate:
            if 'ABX' in patterns and any('LDD' in p for p in patterns):
                candidate.table_type = '1d_word'
            elif 'ABX' in patterns and any('LDAB' in p or 'LDAA' in p for p in patterns):
                candidate.table_type = '1d_byte'
            elif 'ASLB' in patterns:  # Doubling index often means 2D or word table
                candidate.table_type = '2d_or_word'
            elif any('LDAB_0' in p for p in patterns):
                candidate.table_type = '1d_byte'
                
    def estimate_table_sizes(self):
        """Estimate table sizes based on surrounding tables and patterns"""
        sorted_addrs = sorted(self.candidates.keys())
        
        for i, addr in enumerate(sorted_addrs):
            candidate = self.candidates[addr]
            
            # Simple heuristic: distance to next table
            if i + 1 < len(sorted_addrs):
                next_addr = sorted_addrs[i + 1]
                max_size = next_addr - addr
                
                # Cap at reasonable table sizes
                if max_size > 512:
                    max_size = 256  # Assume 256 max
                candidate.estimated_size = min(max_size, 256)
            else:
                candidate.estimated_size = 16  # Default
                
            # Adjust confidence based on references
            ref_count = len(candidate.references)
            if ref_count >= 5:
                candidate.confidence = 0.9
            elif ref_count >= 3:
                candidate.confidence = 0.7
            elif ref_count >= 2:
                candidate.confidence = 0.5
            else:
                candidate.confidence = 0.3
                
    def scan_all_code(self):
        """Scan all code regions"""
        print("Scanning for table access patterns...")
        
        # LOW bank code (0x2000-0x8000)
        accesses = self.scan_for_ldx_patterns(0x2000, 0x8000)
        print(f"  LOW bank: {len(accesses)} table accesses")
        self.table_accesses.extend(accesses)
        
        # HIGH bank code (0x10000-0x18000)
        accesses = self.scan_for_ldx_patterns(0x10000, 0x18000)
        print(f"  HIGH bank: {len(accesses)} table accesses")
        self.table_accesses.extend(accesses)
        
        self.estimate_table_sizes()
        
    def generate_report(self) -> str:
        """Generate detection report"""
        lines = []
        lines.append("=" * 70)
        lines.append("TABLE AUTO-DETECTION REPORT")
        lines.append("=" * 70)
        lines.append(f"Binary: {os.path.basename(self.bin_path)}")
        lines.append(f"Total Table Candidates: {len(self.candidates)}")
        lines.append(f"Already in XDF: {len(self.xdf_tables & set(self.candidates.keys()))}")
        lines.append(f"New Tables Found: {len(set(self.candidates.keys()) - self.xdf_tables)}")
        lines.append("")
        
        # High confidence tables NOT in XDF
        lines.append("-" * 50)
        lines.append("NEW TABLES (not in XDF, sorted by confidence)")
        lines.append("-" * 50)
        lines.append(f"{'Address':<10} {'Type':<12} {'Size':<6} {'Refs':<5} {'Conf':<6} {'Pattern'}")
        
        new_tables = [c for c in self.candidates.values() if c.address not in self.xdf_tables]
        new_tables.sort(key=lambda x: (-x.confidence, -len(x.references)))
        
        for candidate in new_tables[:40]:
            refs = len(candidate.references)
            lines.append(f"${candidate.address:04X}     {candidate.table_type:<12} "
                        f"{candidate.estimated_size:<6} {refs:<5} {candidate.confidence:.1f}")
        if len(new_tables) > 40:
            lines.append(f"  ... and {len(new_tables) - 40} more")
        lines.append("")
        
        # Already in XDF (verification)
        existing = [c for c in self.candidates.values() if c.address in self.xdf_tables]
        lines.append("-" * 50)
        lines.append(f"VERIFIED XDF TABLES ({len(existing)} found in code)")
        lines.append("-" * 50)
        for candidate in sorted(existing, key=lambda x: x.address)[:20]:
            refs = len(candidate.references)
            lines.append(f"  ${candidate.address:04X}: {refs} refs, type={candidate.table_type}")
        lines.append("")
        
        # Access pattern summary
        lines.append("-" * 50)
        lines.append("ACCESS PATTERN SUMMARY")
        lines.append("-" * 50)
        pattern_counts = defaultdict(int)
        for access in self.table_accesses:
            # Simplify pattern
            if 'ABX' in access.pattern and 'LDAB' in access.pattern:
                pattern_counts['1D Byte (ABX + LDAB)'] += 1
            elif 'ABX' in access.pattern and 'LDD' in access.pattern:
                pattern_counts['1D Word (ABX + LDD)'] += 1
            elif 'ASLB' in access.pattern:
                pattern_counts['2D/Word (ASLB index)'] += 1
            elif 'LDAB' in access.pattern or 'LDAA' in access.pattern:
                pattern_counts['Direct Index'] += 1
            else:
                pattern_counts['Other'] += 1
                
        for pattern, count in sorted(pattern_counts.items(), key=lambda x: -x[1]):
            lines.append(f"  {pattern}: {count} accesses")
        lines.append("")
        
        # Generate XDF suggestions
        lines.append("=" * 50)
        lines.append("XDF TABLE DEFINITIONS TO ADD")
        lines.append("=" * 50)
        lines.append("<!-- Copy these into your XDF file -->")
        
        for candidate in new_tables[:10]:
            if candidate.confidence >= 0.5:
                size = candidate.estimated_size
                lines.append(f"""
<XDFTABLE uniqueid="0x{candidate.address:04X}" flags="0x0">
  <title>TABLE_{candidate.address:04X}</title>
  <description>Auto-detected table ({len(candidate.references)} refs)</description>
  <XDFAXIS id="x" uniqueid="0x0">
    <embeddeddata mmedaddress="0x{candidate.address:04X}" 
                  mmedelementsizebits="8" mmedrowcount="{size}" />
  </XDFAXIS>
</XDFTABLE>""")
                
        return '\n'.join(lines)
        
    def export_json(self) -> str:
        """Export results as JSON"""
        result = {
            'binary': os.path.basename(self.bin_path),
            'total_candidates': len(self.candidates),
            'new_tables': [],
            'verified_xdf': []
        }
        
        for addr, candidate in sorted(self.candidates.items()):
            entry = {
                'address': f'0x{addr:04X}',
                'type': candidate.table_type,
                'estimated_size': candidate.estimated_size,
                'references': len(candidate.references),
                'confidence': candidate.confidence,
                'in_xdf': addr in self.xdf_tables
            }
            
            if addr in self.xdf_tables:
                result['verified_xdf'].append(entry)
            else:
                result['new_tables'].append(entry)
                
        return json.dumps(result, indent=2)
        
    def run_detection(self) -> bool:
        """Run complete table detection"""
        if not self.load_binary():
            return False
            
        self.load_xdf()
        self.scan_all_code()
        
        return True


def main():
    parser = argparse.ArgumentParser(description='Table Auto-Detector')
    parser.add_argument('binary', help='Binary file to analyze')
    parser.add_argument('--xdf', '-x', help='XDF file for comparison')
    parser.add_argument('--output', '-o', help='Output file')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    detector = TableAutoDetector(args.binary, args.xdf)
    
    if not detector.run_detection():
        return 1
        
    if args.json:
        output = detector.export_json()
    else:
        output = detector.generate_report()
        
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"\nSaved to {args.output}")
    else:
        print(output)
        
    return 0


if __name__ == '__main__':
    sys.exit(main())
