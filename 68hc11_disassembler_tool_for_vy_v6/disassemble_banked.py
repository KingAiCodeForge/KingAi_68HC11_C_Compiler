#!/usr/bin/env python3
"""
VY V6 Banked ROM Disassembler
==============================
Handles 128KB banked ROM with automatic LOW/HIGH bank switching.

Memory Map:
- File 0x00000-0x0FFFF: LOW bank (64KB)
- File 0x10000-0x1FFFF: HIGH bank (64KB) = CPU 0x8000-0xFFFF

Author: Jason King (KingAI Pty Ltd)
Date: 2026-01-26
"""

import os
import sys
import argparse
import json
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

# Import opcode table from core module if available
try:
    from core.opcodes import HC11_OPCODES
except ImportError:
    # Inline critical opcodes
    pass

# Complete HC11 opcode table with correct byte lengths
OPCODES = {
    # Inherent (1 byte)
    0x01: ('NOP', 'inh', 1), 0x06: ('TAP', 'inh', 1), 0x07: ('TPA', 'inh', 1),
    0x08: ('INX', 'inh', 1), 0x09: ('DEX', 'inh', 1), 0x0A: ('CLV', 'inh', 1),
    0x0B: ('SEV', 'inh', 1), 0x0C: ('CLC', 'inh', 1), 0x0D: ('SEC', 'inh', 1),
    0x0E: ('CLI', 'inh', 1), 0x0F: ('SEI', 'inh', 1), 0x10: ('SBA', 'inh', 1),
    0x11: ('CBA', 'inh', 1), 0x16: ('TAB', 'inh', 1), 0x17: ('TBA', 'inh', 1),
    0x19: ('DAA', 'inh', 1), 0x1B: ('ABA', 'inh', 1),
    0x30: ('TSX', 'inh', 1), 0x31: ('INS', 'inh', 1), 0x32: ('PULA', 'inh', 1),
    0x33: ('PULB', 'inh', 1), 0x34: ('DES', 'inh', 1), 0x35: ('TXS', 'inh', 1),
    0x36: ('PSHA', 'inh', 1), 0x37: ('PSHB', 'inh', 1), 0x38: ('PULX', 'inh', 1),
    0x39: ('RTS', 'inh', 1), 0x3A: ('ABX', 'inh', 1), 0x3B: ('RTI', 'inh', 1),
    0x3C: ('PSHX', 'inh', 1), 0x3D: ('MUL', 'inh', 1), 0x3E: ('WAI', 'inh', 1),
    0x3F: ('SWI', 'inh', 1),
    0x40: ('NEGA', 'inh', 1), 0x43: ('COMA', 'inh', 1), 0x44: ('LSRA', 'inh', 1),
    0x46: ('RORA', 'inh', 1), 0x47: ('ASRA', 'inh', 1), 0x48: ('ASLA', 'inh', 1),
    0x49: ('ROLA', 'inh', 1), 0x4A: ('DECA', 'inh', 1), 0x4C: ('INCA', 'inh', 1),
    0x4D: ('TSTA', 'inh', 1), 0x4F: ('CLRA', 'inh', 1),
    0x50: ('NEGB', 'inh', 1), 0x53: ('COMB', 'inh', 1), 0x54: ('LSRB', 'inh', 1),
    0x56: ('RORB', 'inh', 1), 0x57: ('ASRB', 'inh', 1), 0x58: ('ASLB', 'inh', 1),
    0x59: ('ROLB', 'inh', 1), 0x5A: ('DECB', 'inh', 1), 0x5C: ('INCB', 'inh', 1),
    0x5D: ('TSTB', 'inh', 1), 0x5F: ('CLRB', 'inh', 1),
    
    # Bit manipulation (CORRECTED lengths)
    0x12: ('BRSET', 'dir', 4), 0x13: ('BRCLR', 'dir', 4),  # 4 bytes!
    0x14: ('BSET', 'dir', 3), 0x15: ('BCLR', 'dir', 3),    # 3 bytes!
    0x1C: ('BSET', 'idx', 3), 0x1D: ('BCLR', 'idx', 3),    # 3 bytes!
    0x1E: ('BRSET', 'idx', 4), 0x1F: ('BRCLR', 'idx', 4),  # 4 bytes!
    
    # Branches (2 bytes)
    0x20: ('BRA', 'rel', 2), 0x21: ('BRN', 'rel', 2), 0x22: ('BHI', 'rel', 2),
    0x23: ('BLS', 'rel', 2), 0x24: ('BCC', 'rel', 2), 0x25: ('BCS', 'rel', 2),
    0x26: ('BNE', 'rel', 2), 0x27: ('BEQ', 'rel', 2), 0x28: ('BVC', 'rel', 2),
    0x29: ('BVS', 'rel', 2), 0x2A: ('BPL', 'rel', 2), 0x2B: ('BMI', 'rel', 2),
    0x2C: ('BGE', 'rel', 2), 0x2D: ('BLT', 'rel', 2), 0x2E: ('BGT', 'rel', 2),
    0x2F: ('BLE', 'rel', 2), 0x8D: ('BSR', 'rel', 2),
    
    # Immediate (2-3 bytes)
    0x80: ('SUBA', 'imm', 2), 0x81: ('CMPA', 'imm', 2), 0x82: ('SBCA', 'imm', 2),
    0x83: ('SUBD', 'imm', 3), 0x84: ('ANDA', 'imm', 2), 0x85: ('BITA', 'imm', 2),
    0x86: ('LDAA', 'imm', 2), 0x88: ('EORA', 'imm', 2), 0x89: ('ADCA', 'imm', 2),
    0x8A: ('ORAA', 'imm', 2), 0x8B: ('ADDA', 'imm', 2), 0x8C: ('CPX', 'imm', 3),
    0x8E: ('LDS', 'imm', 3), 0x8F: ('XGDX', 'inh', 1),
    0xC0: ('SUBB', 'imm', 2), 0xC1: ('CMPB', 'imm', 2), 0xC2: ('SBCB', 'imm', 2),
    0xC3: ('ADDD', 'imm', 3), 0xC4: ('ANDB', 'imm', 2), 0xC5: ('BITB', 'imm', 2),
    0xC6: ('LDAB', 'imm', 2), 0xC8: ('EORB', 'imm', 2), 0xC9: ('ADCB', 'imm', 2),
    0xCA: ('ORAB', 'imm', 2), 0xCB: ('ADDB', 'imm', 2), 0xCC: ('LDD', 'imm', 3),
    0xCE: ('LDX', 'imm', 3), 0xCF: ('STOP', 'inh', 1),
    
    # Direct (2 bytes)
    0x90: ('SUBA', 'dir', 2), 0x91: ('CMPA', 'dir', 2), 0x92: ('SBCA', 'dir', 2),
    0x93: ('SUBD', 'dir', 2), 0x94: ('ANDA', 'dir', 2), 0x95: ('BITA', 'dir', 2),
    0x96: ('LDAA', 'dir', 2), 0x97: ('STAA', 'dir', 2), 0x98: ('EORA', 'dir', 2),
    0x99: ('ADCA', 'dir', 2), 0x9A: ('ORAA', 'dir', 2), 0x9B: ('ADDA', 'dir', 2),
    0x9C: ('CPX', 'dir', 2), 0x9D: ('JSR', 'dir', 2), 0x9E: ('LDS', 'dir', 2),
    0x9F: ('STS', 'dir', 2),
    0xD0: ('SUBB', 'dir', 2), 0xD1: ('CMPB', 'dir', 2), 0xD2: ('SBCB', 'dir', 2),
    0xD3: ('ADDD', 'dir', 2), 0xD4: ('ANDB', 'dir', 2), 0xD5: ('BITB', 'dir', 2),
    0xD6: ('LDAB', 'dir', 2), 0xD7: ('STAB', 'dir', 2), 0xD8: ('EORB', 'dir', 2),
    0xD9: ('ADCB', 'dir', 2), 0xDA: ('ORAB', 'dir', 2), 0xDB: ('ADDB', 'dir', 2),
    0xDC: ('LDD', 'dir', 2), 0xDD: ('STD', 'dir', 2), 0xDE: ('LDX', 'dir', 2),
    0xDF: ('STX', 'dir', 2),
    
    # Indexed (2 bytes)
    0x60: ('NEG', 'idx', 2), 0x63: ('COM', 'idx', 2), 0x64: ('LSR', 'idx', 2),
    0x66: ('ROR', 'idx', 2), 0x67: ('ASR', 'idx', 2), 0x68: ('ASL', 'idx', 2),
    0x69: ('ROL', 'idx', 2), 0x6A: ('DEC', 'idx', 2), 0x6C: ('INC', 'idx', 2),
    0x6D: ('TST', 'idx', 2), 0x6E: ('JMP', 'idx', 2), 0x6F: ('CLR', 'idx', 2),
    0xA0: ('SUBA', 'idx', 2), 0xA1: ('CMPA', 'idx', 2), 0xA2: ('SBCA', 'idx', 2),
    0xA3: ('SUBD', 'idx', 2), 0xA4: ('ANDA', 'idx', 2), 0xA5: ('BITA', 'idx', 2),
    0xA6: ('LDAA', 'idx', 2), 0xA7: ('STAA', 'idx', 2), 0xA8: ('EORA', 'idx', 2),
    0xA9: ('ADCA', 'idx', 2), 0xAA: ('ORAA', 'idx', 2), 0xAB: ('ADDA', 'idx', 2),
    0xAC: ('CPX', 'idx', 2), 0xAD: ('JSR', 'idx', 2), 0xAE: ('LDS', 'idx', 2),
    0xAF: ('STS', 'idx', 2),
    0xE0: ('SUBB', 'idx', 2), 0xE1: ('CMPB', 'idx', 2), 0xE2: ('SBCB', 'idx', 2),
    0xE3: ('ADDD', 'idx', 2), 0xE4: ('ANDB', 'idx', 2), 0xE5: ('BITB', 'idx', 2),
    0xE6: ('LDAB', 'idx', 2), 0xE7: ('STAB', 'idx', 2), 0xE8: ('EORB', 'idx', 2),
    0xE9: ('ADCB', 'idx', 2), 0xEA: ('ORAB', 'idx', 2), 0xEB: ('ADDB', 'idx', 2),
    0xEC: ('LDD', 'idx', 2), 0xED: ('STD', 'idx', 2), 0xEE: ('LDX', 'idx', 2),
    0xEF: ('STX', 'idx', 2),
    
    # Extended (3 bytes)
    0x70: ('NEG', 'ext', 3), 0x73: ('COM', 'ext', 3), 0x74: ('LSR', 'ext', 3),
    0x76: ('ROR', 'ext', 3), 0x77: ('ASR', 'ext', 3), 0x78: ('ASL', 'ext', 3),
    0x79: ('ROL', 'ext', 3), 0x7A: ('DEC', 'ext', 3), 0x7C: ('INC', 'ext', 3),
    0x7D: ('TST', 'ext', 3), 0x7E: ('JMP', 'ext', 3), 0x7F: ('CLR', 'ext', 3),
    0xB0: ('SUBA', 'ext', 3), 0xB1: ('CMPA', 'ext', 3), 0xB2: ('SBCA', 'ext', 3),
    0xB3: ('SUBD', 'ext', 3), 0xB4: ('ANDA', 'ext', 3), 0xB5: ('BITA', 'ext', 3),
    0xB6: ('LDAA', 'ext', 3), 0xB7: ('STAA', 'ext', 3), 0xB8: ('EORA', 'ext', 3),
    0xB9: ('ADCA', 'ext', 3), 0xBA: ('ORAA', 'ext', 3), 0xBB: ('ADDA', 'ext', 3),
    0xBC: ('CPX', 'ext', 3), 0xBD: ('JSR', 'ext', 3), 0xBE: ('LDS', 'ext', 3),
    0xBF: ('STS', 'ext', 3),
    0xF0: ('SUBB', 'ext', 3), 0xF1: ('CMPB', 'ext', 3), 0xF2: ('SBCB', 'ext', 3),
    0xF3: ('ADDD', 'ext', 3), 0xF4: ('ANDB', 'ext', 3), 0xF5: ('BITB', 'ext', 3),
    0xF6: ('LDAB', 'ext', 3), 0xF7: ('STAB', 'ext', 3), 0xF8: ('EORB', 'ext', 3),
    0xF9: ('ADCB', 'ext', 3), 0xFA: ('ORAB', 'ext', 3), 0xFB: ('ADDB', 'ext', 3),
    0xFC: ('LDD', 'ext', 3), 0xFD: ('STD', 'ext', 3), 0xFE: ('LDX', 'ext', 3),
    0xFF: ('STX', 'ext', 3),
    # Missing opcodes (Motorola HC11 Reference Manual)
    0x02: ('IDIV', 1),
    0x03: ('FDIV', 1),
}

# Prebyte opcodes (0x18 = Y-register, 0x1A = CPD, 0xCD = CPD Y-indexed)
PREBYTES = {0x18, 0x1A, 0xCD}


class VYV6BankedDisassembler:
    """Disassembler with automatic VY V6 bank handling"""
    
    def __init__(self, bin_path: str):
        self.bin_path = bin_path
        self.data = None
        self.size = 0
        
    def load(self) -> bool:
        """Load binary file"""
        try:
            with open(self.bin_path, 'rb') as f:
                self.data = f.read()
            self.size = len(self.data)
            return True
        except Exception as e:
            print(f"Error loading: {e}")
            return False
            
    def cpu_to_file(self, cpu_addr: int, bank: str = 'auto') -> int:
        """
        Convert CPU address to file offset for VY V6 128KB ROM.
        
        VY V6 Memory Map:
        - CPU 0x0000-0x1FFF: RAM/IO (not in ROM)
        - CPU 0x2000-0x7FFF: LOW bank code (file 0x2000-0x7FFF)
        - CPU 0x8000-0xFFFF: HIGH bank (file 0x10000-0x1FFFF)
        
        XDF addresses are typically:
        - 0x0000-0x7FFF: LOW bank (calibration + code)
        - 0x8000+: Need +0x8000 offset (but XDF stores as-is)
        """
        if bank == 'high' or (bank == 'auto' and cpu_addr >= 0x8000):
            # HIGH bank: CPU 0x8000-0xFFFF = file 0x10000-0x1FFFF
            return cpu_addr - 0x8000 + 0x10000
        elif bank == 'low' or cpu_addr < 0x8000:
            # LOW bank: CPU 0x2000-0x7FFF = file 0x2000-0x7FFF
            return cpu_addr
        else:
            return cpu_addr
            
    def file_to_cpu(self, file_offset: int) -> Tuple[int, str]:
        """
        Convert file offset to CPU address.
        Returns (cpu_addr, bank)
        """
        if file_offset >= 0x10000:
            # HIGH bank
            return (file_offset - 0x10000 + 0x8000, 'HIGH')
        elif file_offset >= 0x8000:
            # This is ambiguous - could be either bank
            return (file_offset, 'LOW?')
        else:
            return (file_offset, 'LOW')
            
    def disassemble_region(self, start_addr: int, length: int, 
                           bank: str = 'auto', show_bytes: bool = True) -> List[str]:
        """
        Disassemble a region by CPU address.
        
        Args:
            start_addr: CPU address or file offset (auto-detected)
            length: Number of bytes to disassemble
            bank: 'low', 'high', or 'auto'
            show_bytes: Include hex bytes in output
        """
        # Determine if this is a file offset or CPU address
        if start_addr >= 0x10000:
            # This is definitely a file offset in HIGH bank
            file_offset = start_addr
            cpu_addr, bank_name = self.file_to_cpu(file_offset)
        else:
            # Convert CPU address to file offset
            file_offset = self.cpu_to_file(start_addr, bank)
            cpu_addr = start_addr
            bank_name = 'HIGH' if file_offset >= 0x10000 else 'LOW'
            
        lines = []
        lines.append(f"; VY V6 Disassembly - {bank_name} bank")
        lines.append(f"; CPU addr: 0x{cpu_addr:04X}, File offset: 0x{file_offset:05X}")
        lines.append(f"; Length: {length} bytes")
        lines.append("")
        
        pc = file_offset
        end = min(file_offset + length, self.size)
        
        while pc < end:
            opcode = self.data[pc]
            cpu_pc = self._file_to_cpu_addr(pc)
            
            # Handle prebytes
            if opcode in PREBYTES:
                if pc + 1 >= end:
                    lines.append(self._format_unknown(pc, cpu_pc, opcode, show_bytes))
                    pc += 1
                    continue
                    
                next_op = self.data[pc + 1]
                # For now, treat as 2-byte sequence
                lines.append(self._format_prebyte(pc, cpu_pc, opcode, next_op, show_bytes))
                pc += 2
                continue
                
            if opcode in OPCODES:
                mnem, mode, inst_len = OPCODES[opcode]
                
                # Get operand bytes
                if pc + inst_len > self.size:
                    lines.append(self._format_unknown(pc, cpu_pc, opcode, show_bytes))
                    pc += 1
                    continue
                    
                operand_bytes = self.data[pc+1:pc+inst_len]
                
                # Format instruction
                line = self._format_instruction(pc, cpu_pc, opcode, mnem, mode, 
                                                operand_bytes, show_bytes)
                lines.append(line)
                pc += inst_len
            else:
                lines.append(self._format_unknown(pc, cpu_pc, opcode, show_bytes))
                pc += 1
                
        return lines
        
    def _file_to_cpu_addr(self, file_offset: int) -> int:
        """Quick file to CPU conversion"""
        if file_offset >= 0x10000:
            return file_offset - 0x10000 + 0x8000
        return file_offset
        
    def _format_instruction(self, file_pc: int, cpu_pc: int, opcode: int,
                            mnem: str, mode: str, operand_bytes: bytes,
                            show_bytes: bool) -> str:
        """Format a single instruction"""
        # Build hex bytes string
        all_bytes = bytes([opcode]) + operand_bytes
        hex_str = ' '.join(f'{b:02X}' for b in all_bytes)
        
        # Format operand based on mode
        if mode == 'inh':
            operand = ''
        elif mode == 'imm':
            if len(operand_bytes) == 1:
                operand = f'#${operand_bytes[0]:02X}'
            else:
                val = (operand_bytes[0] << 8) | operand_bytes[1]
                operand = f'#${val:04X}'
        elif mode == 'dir':
            if len(operand_bytes) >= 1:
                operand = f'${operand_bytes[0]:02X}'
                # Add bit/mask for BSET/BCLR/BRSET/BRCLR
                if mnem in ('BSET', 'BCLR') and len(operand_bytes) >= 2:
                    operand = f'${operand_bytes[0]:02X}, #${operand_bytes[1]:02X}'
                elif mnem in ('BRSET', 'BRCLR') and len(operand_bytes) >= 3:
                    rel = operand_bytes[2]
                    if rel >= 0x80:
                        rel -= 256
                    target = cpu_pc + len(all_bytes) + rel
                    operand = f'${operand_bytes[0]:02X}, #${operand_bytes[1]:02X}, ${target:04X}'
            else:
                operand = '?'
        elif mode == 'idx':
            if len(operand_bytes) >= 1:
                operand = f'${operand_bytes[0]:02X},X'
                if mnem in ('BSET', 'BCLR') and len(operand_bytes) >= 2:
                    operand = f'${operand_bytes[0]:02X},X, #${operand_bytes[1]:02X}'
                elif mnem in ('BRSET', 'BRCLR') and len(operand_bytes) >= 3:
                    rel = operand_bytes[2]
                    if rel >= 0x80:
                        rel -= 256
                    target = cpu_pc + len(all_bytes) + rel
                    operand = f'${operand_bytes[0]:02X},X, #${operand_bytes[1]:02X}, ${target:04X}'
            else:
                operand = '?,X'
        elif mode == 'ext':
            if len(operand_bytes) >= 2:
                addr = (operand_bytes[0] << 8) | operand_bytes[1]
                operand = f'${addr:04X}'
            else:
                operand = '$????'
        elif mode == 'rel':
            if len(operand_bytes) >= 1:
                rel = operand_bytes[0]
                if rel >= 0x80:
                    rel -= 256
                target = cpu_pc + len(all_bytes) + rel
                operand = f'${target:04X}'
            else:
                operand = '$????'
        else:
            operand = ''
            
        # Format line
        if show_bytes:
            return f'{cpu_pc:04X}  {hex_str:14} {mnem:8} {operand}'
        else:
            return f'{cpu_pc:04X}  {mnem:8} {operand}'
            
    def _format_prebyte(self, file_pc: int, cpu_pc: int, prebyte: int, 
                        next_op: int, show_bytes: bool) -> str:
        """Format prebyte instruction"""
        hex_str = f'{prebyte:02X} {next_op:02X}'
        if prebyte == 0x18:
            mnem = 'XGDY' if next_op == 0x8F else f'(Y){next_op:02X}'
        elif prebyte == 0x1A:
            mnem = f'CPD/{next_op:02X}'
        else:
            mnem = f'PRE{prebyte:02X}/{next_op:02X}'
            
        if show_bytes:
            return f'{cpu_pc:04X}  {hex_str:14} {mnem}'
        else:
            return f'{cpu_pc:04X}  {mnem}'
            
    def _format_unknown(self, file_pc: int, cpu_pc: int, opcode: int, 
                        show_bytes: bool) -> str:
        """Format unknown opcode"""
        if show_bytes:
            return f'{cpu_pc:04X}  {opcode:02X}             DB       ${opcode:02X}'
        else:
            return f'{cpu_pc:04X}  DB       ${opcode:02X}'
            
    def disassemble_isr(self, isr_name: str) -> Optional[List[str]]:
        """Disassemble a named ISR by following the vector table"""
        # ISR vector offsets (file offset in LOW bank at 0xFFD6)
        ISR_VECTORS = {
            'SCI': 0xFFD6, 'SPI': 0xFFD8, 'PAI': 0xFFDA, 'PAO': 0xFFDC,
            'TOF': 0xFFDE, 'OC5': 0xFFE0, 'OC4': 0xFFE2, 'OC3': 0xFFE4,
            'OC2': 0xFFE6, 'OC1': 0xFFE8, 'TOC1': 0xFFE8,  # Alias
            'IC3': 0xFFEA, 'TIC3': 0xFFEA,  # Alias
            'IC2': 0xFFEC, 'IC1': 0xFFEE, 'RTI': 0xFFF0,
            'IRQ': 0xFFF2, 'XIRQ': 0xFFF4, 'RESET': 0xFFFE
        }
        
        isr_upper = isr_name.upper()
        if isr_upper not in ISR_VECTORS:
            print(f"Unknown ISR: {isr_name}")
            print(f"Available: {', '.join(sorted(ISR_VECTORS.keys()))}")
            return None
            
        vec_offset = ISR_VECTORS[isr_upper]
        
        # Read vector (points to jump table)
        jump_addr = (self.data[vec_offset] << 8) | self.data[vec_offset + 1]
        
        # Read JMP target from jump table
        if self.data[jump_addr] != 0x7E:
            print(f"Warning: No JMP at jump table 0x{jump_addr:04X}")
            return None
            
        target = (self.data[jump_addr + 1] << 8) | self.data[jump_addr + 2]
        
        lines = []
        lines.append(f"; ISR: {isr_upper}")
        lines.append(f"; Vector @ 0x{vec_offset:04X} -> Jump table 0x{jump_addr:04X} -> Code 0x{target:04X}")
        lines.append("")
        
        # Disassemble from target (it's in LOW bank)
        region_lines = self.disassemble_region(target, 256, bank='low')
        lines.extend(region_lines[4:])  # Skip header we already added
        
        return lines


def main():
    parser = argparse.ArgumentParser(
        description='VY V6 Banked ROM Disassembler',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Disassemble by CPU address (auto-detect bank)
  python disassemble_banked.py binary.bin --addr 0x37A6 --len 128
  
  # Disassemble by file offset
  python disassemble_banked.py binary.bin --file-offset 0x137A6 --len 128
  
  # Disassemble named ISR
  python disassemble_banked.py binary.bin --isr TOC1
  python disassemble_banked.py binary.bin --isr TIC3
  
  # Force specific bank
  python disassemble_banked.py binary.bin --addr 0x5000 --bank low
"""
    )
    
    parser.add_argument('binary', help='Binary file to disassemble')
    parser.add_argument('--addr', '-a', type=lambda x: int(x, 0),
                        help='CPU address to disassemble')
    parser.add_argument('--file-offset', '-f', type=lambda x: int(x, 0),
                        help='File offset to disassemble')
    parser.add_argument('--len', '-l', type=int, default=128,
                        help='Number of bytes to disassemble (default: 128)')
    parser.add_argument('--bank', '-b', choices=['low', 'high', 'auto'],
                        default='auto', help='Force bank selection')
    parser.add_argument('--isr', '-i', help='Disassemble named ISR (TOC1, TIC3, SCI, etc.)')
    parser.add_argument('--output', '-o', help='Output file (default: stdout)')
    parser.add_argument('--no-bytes', action='store_true',
                        help='Hide hex bytes in output')
    
    args = parser.parse_args()
    
    disasm = VYV6BankedDisassembler(args.binary)
    if not disasm.load():
        return 1
        
    print(f"Loaded {disasm.size} bytes from {os.path.basename(args.binary)}")
    
    lines = []
    
    if args.isr:
        lines = disasm.disassemble_isr(args.isr)
        if not lines:
            return 1
    elif args.file_offset:
        lines = disasm.disassemble_region(args.file_offset, args.len, 
                                          show_bytes=not args.no_bytes)
    elif args.addr:
        lines = disasm.disassemble_region(args.addr, args.len, args.bank,
                                          show_bytes=not args.no_bytes)
    else:
        print("Error: Specify --addr, --file-offset, or --isr")
        return 1
        
    output = '\n'.join(lines)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Saved to {args.output}")
    else:
        print(output)
        
    return 0


if __name__ == '__main__':
    sys.exit(main())
