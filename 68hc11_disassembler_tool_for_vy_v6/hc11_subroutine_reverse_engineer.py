#!/usr/bin/env python3
"""
HC11 Subroutine Reverse Engineering Tool
=========================================
Deep decompilation of timing calculation subroutines with control flow analysis.

PRIMARY TARGETS:
- JSR $24AB - Spark timing calculation (called from TIC3 24X crank ISR)
- JSR $2311 - Unknown timing calculation (called from TIC3 ISR)
- NOTE: TIC3 ISR at bank2 0x135FF (CPU $35FF), NOT 0x180DB

ANALYSIS CAPABILITIES:
1. Full subroutine disassembly with opcode decode
2. Control flow graph (branches, loops, conditionals)
3. RAM variable access tracking
4. Timer register read/write patterns
5. Mathematical operations (ADDD, SUBD, MUL, DIV)
6. Nested subroutine call tree
7. Return value analysis (accumulator state)

[WARN]️ UNTESTED experimental analysis for VY V6 ECU modification research.
FOR RESEARCH ONLY - requires validation before vehicle use.

Author: KingAI Auto Tuning Research
Date: November 20, 2025
"""


import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from collections import defaultdict
import json

# Complete HC11 instruction set with cycle times (from MC68HC11 reference manual)
HC11_INSTRUCTIONS = {
    # Loads and Stores
    0x86: ("LDAA", "immediate", 2, 2, "Load A immediate"),
    0x96: ("LDAA", "direct", 2, 3, "Load A direct"),
    0xB6: ("LDAA", "extended", 3, 4, "Load A extended"),
    0xA6: ("LDAA", "indexed", 2, 4, "Load A indexed,X"),
    0xC6: ("LDAB", "immediate", 2, 2, "Load B immediate"),
    0xD6: ("LDAB", "direct", 2, 3, "Load B direct"),
    0xF6: ("LDAB", "extended", 3, 4, "Load B extended"),
    0xE6: ("LDAB", "indexed", 2, 4, "Load B indexed,X"),
    0xCC: ("LDD", "immediate", 3, 3, "Load D immediate"),
    0xDC: ("LDD", "direct", 2, 4, "Load D direct"),
    0xFC: ("LDD", "extended", 3, 5, "Load D extended"),
    0xEC: ("LDD", "indexed", 2, 5, "Load D indexed,X"),
    0xCE: ("LDX", "immediate", 3, 3, "Load X immediate"),
    0xDE: ("LDX", "direct", 2, 4, "Load X direct"),
    0xFE: ("LDX", "extended", 3, 5, "Load X extended"),
    0xEE: ("LDX", "indexed", 2, 5, "Load X indexed,X"),
    0x97: ("STAA", "direct", 2, 3, "Store A direct"),
    0xB7: ("STAA", "extended", 3, 4, "Store A extended"),
    0xA7: ("STAA", "indexed", 2, 4, "Store A indexed,X"),
    0xD7: ("STAB", "direct", 2, 3, "Store B direct"),
    0xF7: ("STAB", "extended", 3, 4, "Store B extended"),
    0xE7: ("STAB", "indexed", 2, 4, "Store B indexed,X"),
    0xDD: ("STD", "direct", 2, 4, "Store D direct"),
    0xFD: ("STD", "extended", 3, 5, "Store D extended"),
    0xED: ("STD", "indexed", 2, 5, "Store D indexed,X"),
    0xDF: ("STX", "direct", 2, 4, "Store X direct"),
    0xFF: ("STX", "extended", 3, 5, "Store X extended"),
    0xEF: ("STX", "indexed", 2, 5, "Store X indexed,X"),
    
    # Arithmetic
    0x8B: ("ADDA", "immediate", 2, 2, "Add to A immediate"),
    0x9B: ("ADDA", "direct", 2, 3, "Add to A direct"),
    0xBB: ("ADDA", "extended", 3, 4, "Add to A extended"),
    0xAB: ("ADDA", "indexed", 2, 4, "Add to A indexed,X"),
    0xCB: ("ADDB", "immediate", 2, 2, "Add to B immediate"),
    0xDB: ("ADDB", "direct", 2, 3, "Add to B direct"),
    0xFB: ("ADDB", "extended", 3, 4, "Add to B extended"),
    0xEB: ("ADDB", "indexed", 2, 4, "Add to B indexed,X"),
    0xC3: ("ADDD", "immediate", 3, 4, "Add to D immediate"),
    0xD3: ("ADDD", "direct", 2, 5, "Add to D direct"),
    0xF3: ("ADDD", "extended", 3, 6, "Add to D extended"),
    0xE3: ("ADDD", "indexed", 2, 6, "Add to D indexed,X"),
    0x89: ("ADCA", "immediate", 2, 2, "Add with carry to A"),
    0x99: ("ADCA", "direct", 2, 3, "Add with carry to A direct"),
    0xB9: ("ADCA", "extended", 3, 4, "Add with carry to A extended"),
    0xA9: ("ADCA", "indexed", 2, 4, "Add with carry to A indexed,X"),
    0xC9: ("ADCB", "immediate", 2, 2, "Add with carry to B"),
    0xD9: ("ADCB", "direct", 2, 3, "Add with carry to B direct"),
    0xF9: ("ADCB", "extended", 3, 4, "Add with carry to B extended"),
    0xE9: ("ADCB", "indexed", 2, 4, "Add with carry to B indexed,X"),
    0x80: ("SUBA", "immediate", 2, 2, "Subtract from A immediate"),
    0x90: ("SUBA", "direct", 2, 3, "Subtract from A direct"),
    0xB0: ("SUBA", "extended", 3, 4, "Subtract from A extended"),
    0xA0: ("SUBA", "indexed", 2, 4, "Subtract from A indexed,X"),
    0xC0: ("SUBB", "immediate", 2, 2, "Subtract from B immediate"),
    0xD0: ("SUBB", "direct", 2, 3, "Subtract from B direct"),
    0xF0: ("SUBB", "extended", 3, 4, "Subtract from B extended"),
    0xE0: ("SUBB", "indexed", 2, 4, "Subtract from B indexed,X"),
    0x83: ("SUBD", "immediate", 3, 4, "Subtract from D immediate"),
    0x93: ("SUBD", "direct", 2, 5, "Subtract from D direct"),
    0xB3: ("SUBD", "extended", 3, 6, "Subtract from D extended"),
    0xA3: ("SUBD", "indexed", 2, 6, "Subtract from D indexed,X"),
    
    # Multiply
    0x3D: ("MUL", "inherent", 1, 10, "Multiply A*B -> D"),
    
    # Compare
    0x81: ("CMPA", "immediate", 2, 2, "Compare A immediate"),
    0x91: ("CMPA", "direct", 2, 3, "Compare A direct"),
    0xB1: ("CMPA", "extended", 3, 4, "Compare A extended"),
    0xA1: ("CMPA", "indexed", 2, 4, "Compare A indexed,X"),
    0xC1: ("CMPB", "immediate", 2, 2, "Compare B immediate"),
    0xD1: ("CMPB", "direct", 2, 3, "Compare B direct"),
    0xF1: ("CMPB", "extended", 3, 4, "Compare B extended"),
    0xE1: ("CMPB", "indexed", 2, 4, "Compare B indexed,X"),
    0x8C: ("CPX", "immediate", 3, 3, "Compare X immediate"),
    0x9C: ("CPX", "direct", 2, 4, "Compare X direct"),
    0xBC: ("CPX", "extended", 3, 5, "Compare X extended"),
    0xAC: ("CPX", "indexed", 2, 5, "Compare X indexed,X"),
    
    # 16-bit compare (page 2 opcodes)
    0x1083: ("CPD", "immediate", 4, 5, "Compare D immediate"),
    0x1093: ("CPD", "direct", 3, 6, "Compare D direct"),
    0x10B3: ("CPD", "extended", 4, 7, "Compare D extended"),
    0x10A3: ("CPD", "indexed", 3, 7, "Compare D indexed,X"),
    
    # Branches
    0x20: ("BRA", "relative", 2, 3, "Branch always"),
    0x22: ("BHI", "relative", 2, 3, "Branch if higher"),
    0x23: ("BLS", "relative", 2, 3, "Branch if lower or same"),
    0x24: ("BCC", "relative", 2, 3, "Branch if carry clear"),
    0x25: ("BCS", "relative", 2, 3, "Branch if carry set"),
    0x26: ("BNE", "relative", 2, 3, "Branch if not equal"),
    0x27: ("BEQ", "relative", 2, 3, "Branch if equal"),
    0x2C: ("BGE", "relative", 2, 3, "Branch if >= (signed)"),
    0x2D: ("BLT", "relative", 2, 3, "Branch if < (signed)"),
    0x2E: ("BGT", "relative", 2, 3, "Branch if > (signed)"),
    0x2F: ("BLE", "relative", 2, 3, "Branch if <= (signed)"),
    0x28: ("BVC", "relative", 2, 3, "Branch if overflow clear"),
    0x29: ("BVS", "relative", 2, 3, "Branch if overflow set"),
    0x2A: ("BPL", "relative", 2, 3, "Branch if plus"),
    0x2B: ("BMI", "relative", 2, 3, "Branch if minus"),
    
    # Subroutine calls
    0xBD: ("JSR", "extended", 3, 6, "Jump to subroutine extended"),
    0xAD: ("JSR", "indexed", 2, 6, "Jump to subroutine indexed,X"),
    0x39: ("RTS", "inherent", 1, 5, "Return from subroutine"),
    0x3B: ("RTI", "inherent", 1, 12, "Return from interrupt"),
    
    # Stack operations
    0x36: ("PSHA", "inherent", 1, 3, "Push A onto stack"),
    0x37: ("PSHB", "inherent", 1, 3, "Push B onto stack"),
    0x3C: ("PSHX", "inherent", 1, 4, "Push X onto stack"),
    0x32: ("PULA", "inherent", 1, 4, "Pull A from stack"),
    0x33: ("PULB", "inherent", 1, 4, "Pull B from stack"),
    0x38: ("PULX", "inherent", 1, 5, "Pull X from stack"),
    
    # Logic
    0x84: ("ANDA", "immediate", 2, 2, "AND A immediate"),
    0x94: ("ANDA", "direct", 2, 3, "AND A direct"),
    0xB4: ("ANDA", "extended", 3, 4, "AND A extended"),
    0xA4: ("ANDA", "indexed", 2, 4, "AND A indexed,X"),
    0xC4: ("ANDB", "immediate", 2, 2, "AND B immediate"),
    0xD4: ("ANDB", "direct", 2, 3, "AND B direct"),
    0xF4: ("ANDB", "extended", 3, 4, "AND B extended"),
    0xE4: ("ANDB", "indexed", 2, 4, "AND B indexed,X"),
    0x8A: ("ORAA", "immediate", 2, 2, "OR A immediate"),
    0x9A: ("ORAA", "direct", 2, 3, "OR A direct"),
    0xBA: ("ORAA", "extended", 3, 4, "OR A extended"),
    0xAA: ("ORAA", "indexed", 2, 4, "OR A indexed,X"),
    0xCA: ("ORAB", "immediate", 2, 2, "OR B immediate"),
    0xDA: ("ORAB", "direct", 2, 3, "OR B direct"),
    0xFA: ("ORAB", "extended", 3, 4, "OR B extended"),
    0xEA: ("ORAB", "indexed", 2, 4, "OR B indexed,X"),
    0x88: ("EORA", "immediate", 2, 2, "XOR A immediate"),
    0x98: ("EORA", "direct", 2, 3, "XOR A direct"),
    0xB8: ("EORA", "extended", 3, 4, "XOR A extended"),
    0xA8: ("EORA", "indexed", 2, 4, "XOR A indexed,X"),
    0xC8: ("EORB", "immediate", 2, 2, "XOR B immediate"),
    0xD8: ("EORB", "direct", 2, 3, "XOR B direct"),
    0xF8: ("EORB", "extended", 3, 4, "XOR B extended"),
    0xE8: ("EORB", "indexed", 2, 4, "XOR B indexed,X"),
    
    # Shifts and Rotates
    0x48: ("ASLA", "inherent", 1, 2, "Arithmetic shift left A"),
    0x58: ("ASLB", "inherent", 1, 2, "Arithmetic shift left B"),
    0x47: ("ASRA", "inherent", 1, 2, "Arithmetic shift right A"),
    0x57: ("ASRB", "inherent", 1, 2, "Arithmetic shift right B"),
    0x44: ("LSRA", "inherent", 1, 2, "Logical shift right A"),
    0x54: ("LSRB", "inherent", 1, 2, "Logical shift right B"),
    0x49: ("ROLA", "inherent", 1, 2, "Rotate left A through carry"),
    0x59: ("ROLB", "inherent", 1, 2, "Rotate left B through carry"),
    0x46: ("RORA", "inherent", 1, 2, "Rotate right A through carry"),
    0x56: ("RORB", "inherent", 1, 2, "Rotate right B through carry"),
    
    # Bit operations
    0x14: ("BSET", "direct", 3, 6, "Set bits in memory"),
    0x15: ("BCLR", "direct", 3, 6, "Clear bits in memory"),
    0x85: ("BITA", "immediate", 2, 2, "Bit test A immediate"),
    0x95: ("BITA", "direct", 2, 3, "Bit test A direct"),
    0xB5: ("BITA", "extended", 3, 4, "Bit test A extended"),
    0xA5: ("BITA", "indexed", 2, 4, "Bit test A indexed,X"),
    0xC5: ("BITB", "immediate", 2, 2, "Bit test B immediate"),
    0xD5: ("BITB", "direct", 2, 3, "Bit test B direct"),
    0xF5: ("BITB", "extended", 3, 4, "Bit test B extended"),
    0xE5: ("BITB", "indexed", 2, 4, "Bit test B indexed,X"),
    
    # Other
    0x01: ("NOP", "inherent", 1, 2, "No operation"),
    0x1B: ("ABA", "inherent", 1, 2, "Add B to A"),
    0x10: ("SBA", "inherent", 1, 2, "Subtract B from A"),
    0x16: ("TAB", "inherent", 1, 2, "Transfer A to B"),
    0x17: ("TBA", "inherent", 1, 2, "Transfer B to A"),
    0x30: ("TSX", "inherent", 1, 3, "Transfer SP to X"),
    0x35: ("TXS", "inherent", 1, 3, "Transfer X to SP"),
    0x40: ("NEGA", "inherent", 1, 2, "Negate A"),
    0x50: ("NEGB", "inherent", 1, 2, "Negate B"),
    0x43: ("COMA", "inherent", 1, 2, "Complement A"),
    0x53: ("COMB", "inherent", 1, 2, "Complement B"),
    0x4C: ("INCA", "inherent", 1, 2, "Increment A"),
    0x5C: ("INCB", "inherent", 1, 2, "Increment B"),
    0x4A: ("DECA", "inherent", 1, 2, "Decrement A"),
    0x5A: ("DECB", "inherent", 1, 2, "Decrement B"),
    0x4D: ("TSTA", "inherent", 1, 2, "Test A"),
    0x5D: ("TSTB", "inherent", 1, 2, "Test B"),
    0x4F: ("CLRA", "inherent", 1, 2, "Clear A"),
    0x5F: ("CLRB", "inherent", 1, 2, "Clear B"),
    # Missing opcodes (Motorola HC11 Reference Manual)
    0x02: 1,  # IDIV
    0x03: 1,  # FDIV
    0x82: 2,  # SBCA
    0x8E: 3,  # LDS
    0x8F: 1,  # XGDX
    0x92: 2,  # SBCA
    0x9E: 2,  # LDS
    0x9F: 2,  # STS
    0xA2: 2,  # SBCA
    0xAE: 2,  # LDS
    0xAF: 2,  # STS
    0xB2: 3,  # SBCA
    0xBE: 3,  # LDS
    0xBF: 3,  # STS
    0xC2: 2,  # SBCB
    0xCF: 1,  # STOP
    0xD2: 2,  # SBCB
    0xE2: 2,  # SBCB
    0xF2: 3,  # SBCB
}

# Timer register map
TIMER_REGISTERS = {
    0x100E: "TCNT_HI", 0x100F: "TCNT_LO",
    0x1014: "TIC3_HI", 0x1015: "TIC3_LO",
    0x1016: "TOC1_HI", 0x1017: "TOC1_LO",
    0x1018: "TOC2_HI", 0x1019: "TOC2_LO",
    0x101A: "TOC3_HI", 0x101B: "TOC3_LO",
    0x101C: "TOC4_HI", 0x101D: "TOC4_LO",
    0x1020: "TCTL1", 0x1021: "TCTL2",
    0x1022: "TMSK1", 0x1023: "TFLG1",
}


@dataclass
class Instruction:
    """Decoded instruction"""
    offset: int
    address: int
    opcode: int
    mnemonic: str
    mode: str
    size: int
    cycles: int
    description: str
    operand: Optional[int] = None
    operand_str: str = ""
    is_branch: bool = False
    branch_target: Optional[int] = None
    is_call: bool = False
    call_target: Optional[int] = None
    is_return: bool = False
    accesses_timer: bool = False
    timer_register: str = ""
    accesses_ram: bool = False
    ram_address: Optional[int] = None


@dataclass
class Subroutine:
    """Complete subroutine analysis"""
    name: str
    start_addr: int
    end_addr: int
    size: int
    instructions: List[Instruction] = field(default_factory=list)
    total_cycles: int = 0
    max_stack_depth: int = 0
    nested_calls: List[int] = field(default_factory=list)
    branches: List[Tuple[int, int]] = field(default_factory=list)  # (from, to)
    loops: List[Tuple[int, int]] = field(default_factory=list)  # (start, end)
    timer_accesses: Dict[str, List[str]] = field(default_factory=lambda: defaultdict(list))
    ram_accesses: Dict[int, List[str]] = field(default_factory=lambda: defaultdict(list))
    
    def __post_init__(self):
        if not isinstance(self.timer_accesses, defaultdict):
            self.timer_accesses = defaultdict(list, self.timer_accesses)
        if not isinstance(self.ram_accesses, defaultdict):
            self.ram_accesses = defaultdict(list, self.ram_accesses)

import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Tuple



class HC11SubroutineReverseEngineer:
    """Comprehensive subroutine reverse engineering"""
    
    def __init__(self, binary_path: str, base_addr: int = 0x8000):
        self.binary_path = Path(binary_path)
        self.data = self.binary_path.read_bytes()
        self.base_addr = base_addr
        
        # Analysis targets
        self.targets = {
            0x24AB: "SparkTimingCalculation",
            0x2311: "UnknownTimingCalc1",
        }
        
        # Results
        self.subroutines: Dict[int, Subroutine] = {}
        
    def analyze_all(self):
        """Analyze all target subroutines"""
        print("\n" + "=" * 80)
        print("HC11 SUBROUTINE REVERSE ENGINEERING TOOL")
        print("Deep Decompilation with Control Flow Analysis")
        print("=" * 80)
        print(f"Binary: {self.binary_path.name}")
        print(f"Targets: {len(self.targets)} subroutines")
        print("=" * 80 + "\n")
        
        for addr, name in self.targets.items():
            print(f"[SEARCH] Analyzing: {name} at 0x{addr:04X}")
            sub = self.disassemble_subroutine(addr, name)
            if sub:
                self.subroutines[addr] = sub
                print(f"   [OK] {len(sub.instructions)} instructions, {sub.total_cycles} cycles\n")
        
        # Print comprehensive analysis
        self.print_comprehensive_analysis()
        self.export_results()
    
    def disassemble_subroutine(self, addr: int, name: str) -> Optional[Subroutine]:
        """Disassemble entire subroutine until RTS"""
        offset = addr - self.base_addr
        
        if offset < 0 or offset >= len(self.data):
            print(f"   [ERROR] Address out of range")
            return None
        
        sub = Subroutine(name=name, start_addr=addr, end_addr=addr, size=0)
        current_offset = offset
        visited = set()
        to_process = [offset]
        
        while to_process:
            current_offset = to_process.pop(0)
            
            if current_offset in visited or current_offset >= len(self.data):
                continue
            
            visited.add(current_offset)
            
            # Decode instruction
            instr = self.decode_instruction(current_offset)
            if not instr:
                break
            
            sub.instructions.append(instr)
            sub.total_cycles += instr.cycles
            
            # Track control flow
            if instr.is_return:
                sub.end_addr = instr.address
                break
            
            elif instr.is_branch:
                if instr.branch_target:
                    sub.branches.append((instr.address, instr.branch_target))
                    
                    # Add branch target to processing queue
                    target_offset = instr.branch_target - self.base_addr
                    if target_offset not in visited:
                        to_process.append(target_offset)
                    
                    # Check for backward branch (loop)
                    if instr.branch_target < instr.address:
                        sub.loops.append((instr.branch_target, instr.address))
                
                # Continue to next instruction (conditional branches fall through)
                if instr.mnemonic != "BRA":
                    to_process.append(current_offset + instr.size)
            
            elif instr.is_call:
                if instr.call_target:
                    sub.nested_calls.append(instr.call_target)
                to_process.append(current_offset + instr.size)
            
            else:
                # Normal instruction, continue to next
                to_process.append(current_offset + instr.size)
            
            # Track timer/RAM accesses
            if instr.accesses_timer:
                operation = "READ" if "LD" in instr.mnemonic else "WRITE"
                sub.timer_accesses[instr.timer_register].append(
                    f"{operation} at 0x{instr.address:04X}"
                )
            
            if instr.accesses_ram:
                operation = "READ" if "LD" in instr.mnemonic else "WRITE"
                sub.ram_accesses[instr.ram_address].append(
                    f"{operation} at 0x{instr.address:04X}"
                )
        
        # Sort instructions by address
        sub.instructions.sort(key=lambda x: x.address)
        sub.size = sub.end_addr - sub.start_addr if sub.end_addr > sub.start_addr else len(sub.instructions) * 3
        
        return sub
    
    def decode_instruction(self, offset: int) -> Optional[Instruction]:
        """Decode single instruction"""
        if offset >= len(self.data):
            return None
        
        opcode = self.data[offset]
        
        # Check for page 2 opcodes (0x10 prefix for CPD)
        if opcode == 0x10 and offset + 1 < len(self.data):
            opcode2 = self.data[offset + 1]
            full_opcode = (opcode << 8) | opcode2
            
            if full_opcode in HC11_INSTRUCTIONS:
                mnemonic, mode, size, cycles, desc = HC11_INSTRUCTIONS[full_opcode]
                
                # Parse operand
                operand = None
                operand_str = ""
                
                if mode == "immediate" and offset + 3 < len(self.data):
                    operand = (self.data[offset + 2] << 8) | self.data[offset + 3]
                    operand_str = f"#${operand:04X}"
                
                elif mode == "direct" and offset + 2 < len(self.data):
                    operand = self.data[offset + 2]
                    operand_str = f"${operand:02X}"
                
                elif mode == "extended" and offset + 3 < len(self.data):
                    operand = (self.data[offset + 2] << 8) | self.data[offset + 3]
                    operand_str = f"${operand:04X}"
                
                return Instruction(
                    offset=offset,
                    address=self.base_addr + offset,
                    opcode=full_opcode,
                    mnemonic=mnemonic,
                    mode=mode,
                    size=size,
                    cycles=cycles,
                    description=desc,
                    operand=operand,
                    operand_str=operand_str,
                )
        
        # Standard single-byte opcode
        if opcode not in HC11_INSTRUCTIONS:
            return None
        
        mnemonic, mode, size, cycles, desc = HC11_INSTRUCTIONS[opcode]
        
        # Parse operand based on addressing mode
        operand = None
        operand_str = ""
        
        if mode == "immediate":
            if size == 2 and offset + 1 < len(self.data):
                operand = self.data[offset + 1]
                operand_str = f"#${operand:02X}"
            elif size == 3 and offset + 2 < len(self.data):
                operand = (self.data[offset + 1] << 8) | self.data[offset + 2]
                operand_str = f"#${operand:04X}"
        
        elif mode == "direct":
            if offset + 1 < len(self.data):
                operand = self.data[offset + 1]
                addr = 0x1000 + operand if operand < 0x40 else operand
                operand_str = f"${operand:02X}"
        
        elif mode == "extended":
            if offset + 2 < len(self.data):
                operand = (self.data[offset + 1] << 8) | self.data[offset + 2]
                operand_str = f"${operand:04X}"
        
        elif mode == "indexed":
            if offset + 1 < len(self.data):
                operand = self.data[offset + 1]
                operand_str = f"${operand:02X},X"
        
        elif mode == "relative":
            if offset + 1 < len(self.data):
                rel_offset = self.data[offset + 1]
                # Sign extend
                if rel_offset & 0x80:
                    rel_offset = rel_offset - 256
                target = self.base_addr + offset + size + rel_offset
                operand = target
                operand_str = f"${target:04X}"
        
        # Create instruction
        instr = Instruction(
            offset=offset,
            address=self.base_addr + offset,
            opcode=opcode,
            mnemonic=mnemonic,
            mode=mode,
            size=size,
            cycles=cycles,
            description=desc,
            operand=operand,
            operand_str=operand_str,
        )
        
        # Classify instruction type
        instr.is_branch = mnemonic in ["BRA", "BHI", "BLS", "BCC", "BCS", "BNE", "BEQ", 
                                        "BGE", "BLT", "BGT", "BLE", "BVC", "BVS", "BPL", "BMI"]
        if instr.is_branch:
            instr.branch_target = operand
        
        instr.is_call = (mnemonic == "JSR")
        if instr.is_call:
            instr.call_target = operand
        
        instr.is_return = (mnemonic in ["RTS", "RTI"])
        
        # Check timer register access
        if operand and operand in TIMER_REGISTERS:
            instr.accesses_timer = True
            instr.timer_register = TIMER_REGISTERS[operand]
        
        # Check RAM access (0x0000-0x01FF)
        if operand and 0x0000 <= operand <= 0x01FF:
            instr.accesses_ram = True
            instr.ram_address = operand
        
        return instr
    
    def print_comprehensive_analysis(self):
        """Print detailed analysis for all subroutines"""
        for addr, sub in sorted(self.subroutines.items()):
            print("\n" + "=" * 80)
            print(f"SUBROUTINE: {sub.name}")
            print("=" * 80)
            print(f"Address: 0x{sub.start_addr:04X} - 0x{sub.end_addr:04X}")
            print(f"Size: {sub.size} bytes, {len(sub.instructions)} instructions")
            print(f"Execution Time: {sub.total_cycles} cycles ({sub.total_cycles / 8.0:.1f} µs @ 8MHz)")
            print(f"Nested Calls: {len(sub.nested_calls)}")
            print(f"Branches: {len(sub.branches)}")
            print(f"Loops: {len(sub.loops)}")
            print("=" * 80)
            
            # Print disassembly
            print("\n📋 DISASSEMBLY:")
            print("-" * 80)
            
            for i, instr in enumerate(sub.instructions[:100]):  # Limit to first 100
                # Bytes
                bytes_list = []
                for j in range(instr.size):
                    if instr.offset + j < len(self.data):
                        bytes_list.append(f"{self.data[instr.offset + j]:02X}")
                bytes_str = " ".join(bytes_list).ljust(12)
                
                # Instruction
                instr_str = f"{instr.mnemonic} {instr.operand_str}".ljust(20)
                
                # Annotation
                annotation = ""
                if instr.accesses_timer:
                    annotation = f"; {instr.timer_register}"
                elif instr.accesses_ram:
                    annotation = f"; RAM[0x{instr.ram_address:04X}]"
                elif instr.is_call and instr.call_target:
                    annotation = f"; Call to 0x{instr.call_target:04X}"
                elif instr.is_branch and instr.branch_target:
                    annotation = f"; Branch to 0x{instr.branch_target:04X}"
                
                print(f"{instr.address:04X}:  {bytes_str}  {instr_str}  {annotation}")
            
            if len(sub.instructions) > 100:
                print(f"... ({len(sub.instructions) - 100} more instructions)")
            
            # Print timer register accesses
            if sub.timer_accesses:
                print("\n⏱️  TIMER REGISTER ACCESSES:")
                print("-" * 80)
                for reg, ops in sorted(sub.timer_accesses.items()):
                    print(f"{reg:12s}: {len(ops)} operations")
                    for op in ops[:5]:
                        print(f"   {op}")
                    if len(ops) > 5:
                        print(f"   ... ({len(ops) - 5} more)")
            
            # Print RAM accesses
            if sub.ram_accesses:
                print("\n[DISK] RAM VARIABLE ACCESSES:")
                print("-" * 80)
                for ram_addr, ops in sorted(sub.ram_accesses.items()):
                    print(f"0x{ram_addr:04X}:  {len(ops)} operations")
                    for op in ops[:5]:
                        print(f"   {op}")
            
            # Print control flow
            if sub.branches:
                print("\n🔀 CONTROL FLOW (Branches):")
                print("-" * 80)
                for from_addr, to_addr in sub.branches[:20]:
                    direction = "↑ BACKWARD (loop)" if to_addr < from_addr else "↓ FORWARD"
                    print(f"0x{from_addr:04X} → 0x{to_addr:04X}  {direction}")
            
            if sub.loops:
                print("\n🔁 LOOPS DETECTED:")
                print("-" * 80)
                for loop_start, loop_end in sub.loops:
                    print(f"Loop: 0x{loop_start:04X} to 0x{loop_end:04X}")
            
            # Print nested calls
            if sub.nested_calls:
                print("\n📞 NESTED SUBROUTINE CALLS:")
                print("-" * 80)
                for call_addr in sub.nested_calls[:10]:
                    print(f"JSR 0x{call_addr:04X}")
    
    def export_results(self):
        """Export results to JSON"""
        output_file = self.binary_path.parent / f"{self.binary_path.stem}_subroutine_analysis.json"
        
        results = {
            "binary": str(self.binary_path),
            "base_address": f"0x{self.base_addr:04X}",
            "subroutines": {}
        }
        
        for addr, sub in self.subroutines.items():
            results["subroutines"][f"0x{addr:04X}"] = {
                "name": sub.name,
                "start_address": f"0x{sub.start_addr:04X}",
                "end_address": f"0x{sub.end_addr:04X}",
                "size_bytes": sub.size,
                "instruction_count": len(sub.instructions),
                "total_cycles": sub.total_cycles,
                "execution_time_us": sub.total_cycles / 8.0,
                "nested_calls": [f"0x{c:04X}" for c in sub.nested_calls],
                "timer_accesses": {k: len(v) for k, v in sub.timer_accesses.items()},
                "ram_accesses": {f"0x{k:04X}": len(v) for k, v in sub.ram_accesses.items()},
                "branch_count": len(sub.branches),
                "loop_count": len(sub.loops),
            }
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n[DISK] Exported results to: {output_file.name}")
        print("\n[OK] Subroutine Reverse Engineering Complete!")


def main():
    if len(sys.argv) < 2:
        print("Usage: python hc11_subroutine_reverse_engineer.py <binary_file>")
        sys.exit(1)
    
    binary_file = sys.argv[1]
    
    if not Path(binary_file).exists():
        print(f"[ERROR] Error: Binary file not found: {binary_file}")
        sys.exit(1)
    
    engineer = HC11SubroutineReverseEngineer(binary_file)
    engineer.analyze_all()


if __name__ == "__main__":
    main()
