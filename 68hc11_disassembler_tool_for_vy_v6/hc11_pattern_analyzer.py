#!/usr/bin/env python3
"""
HC11 Pattern Analyzer - Advanced Code Structure Detection
Identifies common ECU code patterns: ISRs, table lookups, mode switching, error handling

UNTESTED experimental code for VY V6 ECU modification research.
"""


import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict
import json

# Import the base disassembler
try:
    from hc11_disassembler import HC11Disassembler
except ImportError:
    print("ERROR: hc11_disassembler.py must be in the same directory")
    sys.exit(1)


@dataclass
class CodePattern:
    """Represents a detected code pattern"""
    pattern_type: str
    file_offset: int
    ram_address: int
    confidence: float  # 0.0-1.0
    description: str
    instructions: List[str]
    metadata: Dict

import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Tuple



class HC11PatternAnalyzer:
    """Advanced pattern recognition for HC11 ECU code"""
    
    def __init__(self, disassembler: HC11Disassembler):
        self.dis = disassembler
        self.patterns = []
        
    def find_isr_patterns(self, start_offset: int = 0, end_offset: int = None) -> List[CodePattern]:
        """
        Identify Interrupt Service Routines (ISRs)
        Pattern: CLI/SEI instructions, RTI return, stack operations
        """
        if end_offset is None:
            end_offset = len(self.dis.data)
        
        isrs = []
        offset = start_offset
        
        while offset < end_offset:
            opcode = self.dis.read_byte(offset)
            
            # Look for RTI (Return from Interrupt) as anchor
            if opcode == 0x3B:  # RTI
                # Scan backwards to find likely ISR start
                isr_start = self._find_isr_start(offset)
                if isr_start is not None:
                    # Disassemble the ISR
                    instructions = self._disassemble_routine(isr_start, offset + 1)
                    
                    # Calculate confidence based on ISR characteristics
                    confidence = self._calculate_isr_confidence(instructions)
                    
                    pattern = CodePattern(
                        pattern_type="ISR",
                        file_offset=isr_start,
                        ram_address=self.dis.get_ram_addr(isr_start),
                        confidence=confidence,
                        description=f"Interrupt Service Routine ({len(instructions)} instructions)",
                        instructions=instructions,
                        metadata={
                            'size_bytes': offset + 1 - isr_start,
                            'return_offset': offset
                        }
                    )
                    isrs.append(pattern)
            
            offset += 1
        
        return isrs
    
    def find_table_lookup_patterns(self, start_offset: int = 0, end_offset: int = None) -> List[CodePattern]:
        """
        Identify table lookup routines
        Pattern: LDX #table_addr, LDAA offset,X or LDAB offset,X
        """
        if end_offset is None:
            end_offset = len(self.dis.data)
        
        lookups = []
        offset = start_offset
        
        while offset < end_offset - 10:
            opcode = self.dis.read_byte(offset)
            
            # Pattern: LDX #imm (load table address)
            if opcode == 0xCE:  # LDX immediate
                table_addr = self.dis.read_word(offset + 1)
                
                # Check if followed by indexed load within ~10 instructions
                search_end = min(offset + 30, end_offset)
                found_indexed = False
                
                for search_off in range(offset + 3, search_end):
                    search_op = self.dis.read_byte(search_off)
                    # LDAA indexed or LDAB indexed
                    if search_op in [0xA6, 0xE6]:
                        found_indexed = True
                        break
                
                if found_indexed and 0x4000 <= table_addr <= 0x7FFF:
                    # This looks like a table lookup
                    instructions = self._disassemble_routine(offset, search_end)
                    
                    pattern = CodePattern(
                        pattern_type="TABLE_LOOKUP",
                        file_offset=offset,
                        ram_address=self.dis.get_ram_addr(offset),
                        confidence=0.8,
                        description=f"Table lookup from calibration @ ${table_addr:04X}",
                        instructions=instructions[:15],
                        metadata={
                            'table_address': table_addr,
                            'table_type': self._classify_table_address(table_addr)
                        }
                    )
                    lookups.append(pattern)
            
            offset += 1
        
        return lookups
    
    def find_mode_switching_patterns(self, start_offset: int = 0, end_offset: int = None) -> List[CodePattern]:
        """
        Identify mode switching logic (e.g., MAF vs TPS fuel mode)
        Pattern: BRSET/BRCLR followed by different code paths
        """
        if end_offset is None:
            end_offset = len(self.dis.data)
        
        switches = []
        offset = start_offset
        
        while offset < end_offset - 10:
            opcode = self.dis.read_byte(offset)
            
            # BRSET or BRCLR (bit test and branch)
            if opcode in [0x12, 0x13, 0x1E, 0x1F]:
                flag_addr = self.dis.read_byte(offset + 1)
                bit_mask = self.dis.read_byte(offset + 2)
                branch_offset = self.dis.read_byte(offset + 3)
                
                if branch_offset & 0x80:
                    branch_offset = branch_offset - 256
                
                target = offset + 4 + branch_offset
                
                # Disassemble both paths
                path_true = self._disassemble_routine(target, target + 20)
                path_false = self._disassemble_routine(offset + 4, offset + 24)
                
                pattern = CodePattern(
                    pattern_type="MODE_SWITCH",
                    file_offset=offset,
                    ram_address=self.dis.get_ram_addr(offset),
                    confidence=0.7,
                    description=f"Conditional branch on flag ${flag_addr:02X} bit {bin(bit_mask)}",
                    instructions=[self.dis.disassemble_instruction(offset)[0]],
                    metadata={
                        'flag_address': flag_addr,
                        'bit_mask': bit_mask,
                        'branch_target': target,
                        'true_path_preview': path_true[:5],
                        'false_path_preview': path_false[:5]
                    }
                )
                switches.append(pattern)
            
            offset += 1
        
        return switches
    
    def find_error_handlers(self, start_offset: int = 0, end_offset: int = None) -> List[CodePattern]:
        """
        Identify error handling code (DTC setting, limp mode)
        Pattern: Writes to DTC RAM region (0x0100-0x0200), followed by flag sets
        """
        if end_offset is None:
            end_offset = len(self.dis.data)
        
        handlers = []
        offset = start_offset
        
        while offset < end_offset - 3:
            opcode = self.dis.read_byte(offset)
            
            # STAA extended or STAB extended
            if opcode in [0xB7, 0xF7]:
                target_addr = self.dis.read_word(offset + 1)
                
                # Check if writing to DTC region
                if 0x0100 <= target_addr <= 0x0200:
                    # Scan backwards for error detection logic
                    handler_start = max(0, offset - 50)
                    instructions = self._disassemble_routine(handler_start, offset + 10)
                    
                    pattern = CodePattern(
                        pattern_type="ERROR_HANDLER",
                        file_offset=offset,
                        ram_address=self.dis.get_ram_addr(offset),
                        confidence=0.75,
                        description=f"DTC set/error handler writing to ${target_addr:04X}",
                        instructions=instructions,
                        metadata={
                            'dtc_ram_address': target_addr,
                            'likely_dtc_code': self._guess_dtc_code(target_addr)
                        }
                    )
                    handlers.append(pattern)
            
            offset += 1
        
        return handlers
    
    def find_rpm_limiters(self, start_offset: int = 0, end_offset: int = None) -> List[CodePattern]:
        """
        Identify RPM limiter code
        Pattern: CMPA/CMPB with RPM-like values, followed by conditional fuel/spark cut
        """
        if end_offset is None:
            end_offset = len(self.dis.data)
        
        limiters = []
        offset = start_offset
        
        while offset < end_offset - 10:
            opcode = self.dis.read_byte(offset)
            
            # CMPA immediate or CMPB immediate
            if opcode in [0x81, 0xC1]:
                compare_val = self.dis.read_byte(offset + 1)
                
                # Check if RPM-like (150-255 = 3750-6375 RPM in x25 scaling)
                if 150 <= compare_val <= 255:
                    # Check for branch after compare
                    next_op = self.dis.read_byte(offset + 2)
                    if next_op in [0x22, 0x23, 0x24, 0x25, 0x26, 0x27]:  # Branch opcodes
                        rpm = compare_val * 25
                        instructions = self._disassemble_routine(offset, offset + 20)
                        
                        pattern = CodePattern(
                            pattern_type="RPM_LIMITER",
                            file_offset=offset,
                            ram_address=self.dis.get_ram_addr(offset),
                            confidence=0.65,
                            description=f"RPM comparison: {rpm} RPM ({compare_val} × 25)",
                            instructions=instructions,
                            metadata={
                                'rpm_threshold': rpm,
                                'raw_value': compare_val,
                                'branch_type': hex(next_op)
                            }
                        )
                        limiters.append(pattern)
            
            offset += 1
        
        return limiters
    
    def find_subroutine_calls(self, start_offset: int = 0, end_offset: int = None) -> Dict[int, List[int]]:
        """
        Build a call graph: which addresses call which subroutines
        Returns: {target_address: [caller_offset1, caller_offset2, ...]}
        """
        if end_offset is None:
            end_offset = len(self.dis.data)
        
        call_graph = defaultdict(list)
        offset = start_offset
        
        while offset < end_offset - 2:
            opcode = self.dis.read_byte(offset)
            
            # JSR extended (0xBD)
            if opcode == 0xBD:
                target = self.dis.read_word(offset + 1)
                call_graph[target].append(offset)
                offset += 3
            # BSR relative (0x8D)
            elif opcode == 0x8D:
                displacement = self.dis.read_byte(offset + 1)
                if displacement & 0x80:
                    displacement = displacement - 256
                target = offset + 2 + displacement
                call_graph[target].append(offset)
                offset += 2
            else:
                offset += 1
        
        return dict(call_graph)
    
    def analyze_hotspots(self) -> List[Tuple[int, int, str]]:
        """
        Identify "hotspot" code regions with high calibration access
        Returns: [(start_offset, end_offset, description)]
        """
        # Count calibration reads per 256-byte block
        block_counts = defaultdict(int)
        
        for offset in range(0, len(self.dis.data) - 3):
            opcode = self.dis.read_byte(offset)
            
            if opcode in [0xB6, 0xF6, 0xFC, 0xFE]:  # Extended load opcodes
                addr = self.dis.read_word(offset + 1)
                if 0x4000 <= addr <= 0x7FFF:  # Calibration region
                    block = offset // 256
                    block_counts[block] += 1
        
        # Identify blocks with >10 calibration accesses
        hotspots = []
        for block, count in sorted(block_counts.items(), key=lambda x: x[1], reverse=True):
            if count >= 10:
                start = block * 256
                end = start + 256
                hotspots.append((start, end, f"{count} calibration reads"))
        
        return hotspots[:20]  # Top 20 hotspots
    
    # Private helper methods
    
    def _find_isr_start(self, rti_offset: int) -> Optional[int]:
        """Scan backwards from RTI to find likely ISR start"""
        # Look for typical ISR prologue: save registers, clear interrupts
        scan_start = max(0, rti_offset - 100)
        
        for offset in range(rti_offset - 10, scan_start, -1):
            opcode = self.dis.read_byte(offset)
            # Look for PSHA/PSHB/PSHX at start or CLI
            if opcode in [0x36, 0x37, 0x3C, 0x0E]:
                return offset
        
        # Fallback: assume ISR is 50 bytes
        return max(0, rti_offset - 50)
    
    def _disassemble_routine(self, start: int, end: int) -> List[str]:
        """Disassemble a range of code"""
        instructions = []
        offset = start
        
        while offset < end and offset < len(self.dis.data):
            try:
                instr, length = self.dis.disassemble_instruction(offset)
                instructions.append(instr)
                offset += length
            except:
                break
        
        return instructions
    
    def _calculate_isr_confidence(self, instructions: List[str]) -> float:
        """Calculate confidence that this is a real ISR"""
        confidence = 0.5
        
        # Check for ISR characteristics
        has_rti = any('RTI' in i for i in instructions)
        has_stack_ops = any(op in str(instructions) for op in ['PSHA', 'PSHB', 'PULA', 'PULB'])
        has_cli_sei = any(op in str(instructions) for op in ['CLI', 'SEI'])
        
        if has_rti:
            confidence += 0.3
        if has_stack_ops:
            confidence += 0.15
        if has_cli_sei:
            confidence += 0.05
        
        return min(1.0, confidence)
    
    def _classify_table_address(self, addr: int) -> str:
        """Classify what type of calibration table this might be"""
        # Use XDF data if available
        cal = self.dis.xdf.lookup(addr)
        if cal:
            title, type_str, category = cal
            return f"{category}:{type_str}"
        
        # Fallback to address ranges
        if 0x4000 <= addr < 0x5000:
            return "flags/scalars"
        elif 0x5000 <= addr < 0x6000:
            return "1D_tables"
        elif 0x6000 <= addr < 0x7800:
            return "2D_tables"
        else:
            return "unknown"
    
    def _guess_dtc_code(self, ram_addr: int) -> str:
        """Guess DTC code based on RAM address"""
        # GM typically uses sequential DTC storage
        offset = ram_addr - 0x0100
        if offset < 10:
            return f"P010{offset} (likely)"
        return f"DTC_RAM+{offset}"
    
    def generate_report(self, output_path: Path = None):
        """Generate comprehensive pattern analysis report"""
        print("\n" + "="*80)
        print("HC11 PATTERN ANALYZER - Comprehensive Code Structure Analysis")
        print("="*80)
        
        # Find all pattern types
        print("\n[1/6] Scanning for ISRs...")
        isrs = self.find_isr_patterns()
        
        print(f"[2/6] Scanning for table lookups...")
        lookups = self.find_table_lookup_patterns()
        
        print(f"[3/6] Scanning for mode switches...")
        switches = self.find_mode_switching_patterns()
        
        print(f"[4/6] Scanning for error handlers...")
        handlers = self.find_error_handlers()
        
        print(f"[5/6] Scanning for RPM limiters...")
        limiters = self.find_rpm_limiters()
        
        print(f"[6/6] Building call graph and hotspots...")
        call_graph = self.find_subroutine_calls()
        hotspots = self.analyze_hotspots()
        
        # Summary
        print("\n" + "="*80)
        print("PATTERN DETECTION SUMMARY")
        print("="*80)
        print(f"ISRs found:             {len(isrs)}")
        print(f"Table lookups found:    {len(lookups)}")
        print(f"Mode switches found:    {len(switches)}")
        print(f"Error handlers found:   {len(handlers)}")
        print(f"RPM limiters found:     {len(limiters)}")
        print(f"Subroutines called:     {len(call_graph)}")
        print(f"Code hotspots found:    {len(hotspots)}")
        
        # Detailed reports
        print("\n" + "="*80)
        print("ISRs (Interrupt Service Routines)")
        print("="*80)
        for isr in isrs[:10]:  # Show first 10
            print(f"\n  @ 0x{isr.file_offset:05X} (RAM 0x{isr.ram_address:05X})")
            print(f"  Confidence: {isr.confidence:.2f}")
            print(f"  {isr.description}")
            for instr in isr.instructions[:5]:
                print(f"    {instr}")
        
        print("\n" + "="*80)
        print("TABLE LOOKUPS (Top 20)")
        print("="*80)
        for lookup in lookups[:20]:
            print(f"\n  @ 0x{lookup.file_offset:05X} -> Table @ ${lookup.metadata['table_address']:04X}")
            print(f"  Type: {lookup.metadata['table_type']}")
            print(f"  {lookup.instructions[0]}")
        
        print("\n" + "="*80)
        print("RPM LIMITERS (All)")
        print("="*80)
        for limiter in limiters:
            print(f"\n  @ 0x{limiter.file_offset:05X}: {limiter.metadata['rpm_threshold']} RPM")
            for instr in limiter.instructions[:3]:
                print(f"    {instr}")
        
        print("\n" + "="*80)
        print("CODE HOTSPOTS (High Calibration Access)")
        print("="*80)
        for start, end, desc in hotspots[:10]:
            print(f"  0x{start:05X}-0x{end:05X}: {desc}")
        
        print("\n" + "="*80)
        print("MOST CALLED SUBROUTINES")
        print("="*80)
        sorted_calls = sorted(call_graph.items(), key=lambda x: len(x[1]), reverse=True)
        for target, callers in sorted_calls[:15]:
            print(f"  0x{target:05X} called by {len(callers)} locations")
            if len(callers) <= 5:
                for caller in callers:
                    print(f"    from 0x{caller:05X}")
        
        # Export to JSON if requested
        if output_path:
            report_data = {
                'isrs': [self._pattern_to_dict(p) for p in isrs],
                'table_lookups': [self._pattern_to_dict(p) for p in lookups],
                'mode_switches': [self._pattern_to_dict(p) for p in switches],
                'error_handlers': [self._pattern_to_dict(p) for p in handlers],
                'rpm_limiters': [self._pattern_to_dict(p) for p in limiters],
                'call_graph': {f"0x{k:05X}": [f"0x{c:05X}" for c in v] 
                              for k, v in call_graph.items()},
                'hotspots': [{'start': f"0x{s:05X}", 'end': f"0x{e:05X}", 'desc': d} 
                            for s, e, d in hotspots]
            }
            
            with open(output_path, 'w') as f:
                json.dump(report_data, f, indent=2)
            print(f"\n[OK] Full report exported to: {output_path}")
    
    def _pattern_to_dict(self, pattern: CodePattern) -> Dict:
        """Convert CodePattern to JSON-serializable dict"""
        return {
            'type': pattern.pattern_type,
            'offset': f"0x{pattern.file_offset:05X}",
            'ram_addr': f"0x{pattern.ram_address:05X}",
            'confidence': pattern.confidence,
            'description': pattern.description,
            'instructions': pattern.instructions[:10],
            'metadata': pattern.metadata
        }


def main():
    binary_path = r"R:\VY_V6_Assembly_Modding\VX-VY_V6_$060A_Enhanced_v1.0a - Copy.bin"
    
    if not Path(binary_path).exists():
        print(f"[ERROR] Binary not found: {binary_path}")
        return 1
    
    # Create base disassembler
    dis = HC11Disassembler(binary_path, base_addr=0x0)
    
    # Create pattern analyzer
    analyzer = HC11PatternAnalyzer(dis)
    
    # Generate report
    output_file = Path("pattern_analysis_report.json")
    analyzer.generate_report(output_file)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
