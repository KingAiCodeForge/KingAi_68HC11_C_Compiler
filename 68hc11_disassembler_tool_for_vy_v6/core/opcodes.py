#!/usr/bin/env python3
"""
HC11 Unified Opcodes - Complete and corrected instruction set
Consolidates hc11_opcode_table.py and hc11_opcodes_complete.py

Source: MC68HC11 Reference Manual + community reverse engineering
Date: January 19, 2026
Author: KingAI Automotive Research
"""

from typing import Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Instruction:
    """HC11 instruction metadata"""
    mnemonic: str
    length: int  # Total bytes including opcode
    cycles: int  # Clock cycles
    mode: str    # Addressing mode
    prebyte: int = 0x00  # 0x00, 0x18, 0x1A, or 0xCD
    description: str = ""
    
    def __str__(self):
        return f"{self.mnemonic:6s} ({self.length}B, {self.cycles}cy, {self.mode})"


# Addressing mode constants
MODE_IMPLIED = "imp"       # Inherent (no operand)
MODE_IMMEDIATE = "imm"     # Immediate data (#$XX)
MODE_DIRECT = "dir"        # Direct/zero page ($XX)
MODE_EXTENDED = "ext"      # Extended/absolute ($XXXX)
MODE_INDEXED_X = "idx"     # Indexed X (offset,X)
MODE_INDEXED_Y = "idy"     # Indexed Y (offset,Y)
MODE_RELATIVE = "rel"      # Relative branch
MODE_BIT_DIR = "bit_dir"   # Bit operation direct
MODE_BIT_IDX = "bit_idx"   # Bit operation indexed X
MODE_BIT_IDY = "bit_idy"   # Bit operation indexed Y


class HC11InstructionSet:
    """Complete HC11 instruction set with prebyte support"""
    
    def __init__(self):
        self._opcodes = self._build_opcode_table()
        self._prebyte_18 = self._build_prebyte_18()
        self._prebyte_1A = self._build_prebyte_1A()
        self._prebyte_CD = self._build_prebyte_CD()
    
    def _build_opcode_table(self) -> Dict[int, Instruction]:
        """Build main opcode table (single-byte opcodes)"""
        return {
            # Inherent/Implied (1 byte)
            0x00: Instruction("TEST", 1, 1, MODE_IMPLIED, description="Test mode (factory only)"),
            0x01: Instruction("NOP", 1, 2, MODE_IMPLIED, description="No operation"),
            0x02: Instruction("IDIV", 1, 41, MODE_IMPLIED, description="Integer divide D/X"),
            0x03: Instruction("FDIV", 1, 41, MODE_IMPLIED, description="Fractional divide"),
            0x04: Instruction("LSRD", 1, 3, MODE_IMPLIED, description="Logical shift right D"),
            0x05: Instruction("ASLD", 1, 3, MODE_IMPLIED, description="Arithmetic shift left D"),
            0x06: Instruction("TAP", 1, 2, MODE_IMPLIED, description="Transfer A to CCR"),
            0x07: Instruction("TPA", 1, 2, MODE_IMPLIED, description="Transfer CCR to A"),
            0x08: Instruction("INX", 1, 3, MODE_IMPLIED, description="Increment X"),
            0x09: Instruction("DEX", 1, 3, MODE_IMPLIED, description="Decrement X"),
            0x0A: Instruction("CLV", 1, 2, MODE_IMPLIED, description="Clear overflow flag"),
            0x0B: Instruction("SEV", 1, 2, MODE_IMPLIED, description="Set overflow flag"),
            0x0C: Instruction("CLC", 1, 2, MODE_IMPLIED, description="Clear carry flag"),
            0x0D: Instruction("SEC", 1, 2, MODE_IMPLIED, description="Set carry flag"),
            0x0E: Instruction("CLI", 1, 2, MODE_IMPLIED, description="Clear interrupt mask"),
            0x0F: Instruction("SEI", 1, 2, MODE_IMPLIED, description="Set interrupt mask"),
            
            # Arithmetic/Logic (inherent)
            0x10: Instruction("SBA", 1, 2, MODE_IMPLIED, description="Subtract B from A"),
            0x11: Instruction("CBA", 1, 2, MODE_IMPLIED, description="Compare B to A"),
            0x16: Instruction("TAB", 1, 2, MODE_IMPLIED, description="Transfer A to B"),
            0x17: Instruction("TBA", 1, 2, MODE_IMPLIED, description="Transfer B to A"),
            0x19: Instruction("DAA", 1, 2, MODE_IMPLIED, description="Decimal adjust A"),
            0x1B: Instruction("ABA", 1, 2, MODE_IMPLIED, description="Add B to A"),
            
            # Bit operations (CRITICAL: These are 3-4 bytes!)
            0x12: Instruction("BRSET", 4, 6, MODE_BIT_DIR, description="Branch if bits set (dir)"),
            0x13: Instruction("BRCLR", 4, 6, MODE_BIT_DIR, description="Branch if bits clear (dir)"),
            0x14: Instruction("BSET", 3, 6, MODE_BIT_DIR, description="Set bits (direct)"),
            0x15: Instruction("BCLR", 3, 6, MODE_BIT_DIR, description="Clear bits (direct)"),
            0x1C: Instruction("BSET", 3, 7, MODE_BIT_IDX, description="Set bits (indexed)"),
            0x1D: Instruction("BCLR", 3, 7, MODE_BIT_IDX, description="Clear bits (indexed)"),
            0x1E: Instruction("BRSET", 4, 7, MODE_BIT_IDX, description="Branch if bits set (idx)"),
            0x1F: Instruction("BRCLR", 4, 7, MODE_BIT_IDX, description="Branch if bits clear (idx)"),
            
            # Prebyte indicators
            0x18: Instruction("PREFIX_18", 1, 0, MODE_IMPLIED, description="Y-register prefix"),
            0x1A: Instruction("PREFIX_1A", 1, 0, MODE_IMPLIED, description="CPD prefix"),
            0xCD: Instruction("PREFIX_CD", 1, 0, MODE_IMPLIED, description="Y-indexed CPD/CPX prefix"),
            
            # Branches (2 bytes)
            0x20: Instruction("BRA", 2, 3, MODE_RELATIVE, description="Branch always"),
            0x21: Instruction("BRN", 2, 3, MODE_RELATIVE, description="Branch never"),
            0x22: Instruction("BHI", 2, 3, MODE_RELATIVE, description="Branch if higher"),
            0x23: Instruction("BLS", 2, 3, MODE_RELATIVE, description="Branch if lower/same"),
            0x24: Instruction("BCC", 2, 3, MODE_RELATIVE, description="Branch if carry clear"),
            0x25: Instruction("BCS", 2, 3, MODE_RELATIVE, description="Branch if carry set"),
            0x26: Instruction("BNE", 2, 3, MODE_RELATIVE, description="Branch if not equal"),
            0x27: Instruction("BEQ", 2, 3, MODE_RELATIVE, description="Branch if equal"),
            0x28: Instruction("BVC", 2, 3, MODE_RELATIVE, description="Branch if overflow clear"),
            0x29: Instruction("BVS", 2, 3, MODE_RELATIVE, description="Branch if overflow set"),
            0x2A: Instruction("BPL", 2, 3, MODE_RELATIVE, description="Branch if plus"),
            0x2B: Instruction("BMI", 2, 3, MODE_RELATIVE, description="Branch if minus"),
            0x2C: Instruction("BGE", 2, 3, MODE_RELATIVE, description="Branch if >= (signed)"),
            0x2D: Instruction("BLT", 2, 3, MODE_RELATIVE, description="Branch if < (signed)"),
            0x2E: Instruction("BGT", 2, 3, MODE_RELATIVE, description="Branch if > (signed)"),
            0x2F: Instruction("BLE", 2, 3, MODE_RELATIVE, description="Branch if <= (signed)"),
            
            # Stack operations
            0x30: Instruction("TSX", 1, 3, MODE_IMPLIED, description="Transfer SP to X"),
            0x31: Instruction("INS", 1, 3, MODE_IMPLIED, description="Increment SP"),
            0x32: Instruction("PULA", 1, 4, MODE_IMPLIED, description="Pull A from stack"),
            0x33: Instruction("PULB", 1, 4, MODE_IMPLIED, description="Pull B from stack"),
            0x34: Instruction("DES", 1, 3, MODE_IMPLIED, description="Decrement SP"),
            0x35: Instruction("TXS", 1, 3, MODE_IMPLIED, description="Transfer X to SP"),
            0x36: Instruction("PSHA", 1, 3, MODE_IMPLIED, description="Push A to stack"),
            0x37: Instruction("PSHB", 1, 3, MODE_IMPLIED, description="Push B to stack"),
            0x38: Instruction("PULX", 1, 5, MODE_IMPLIED, description="Pull X from stack"),
            0x39: Instruction("RTS", 1, 5, MODE_IMPLIED, description="Return from subroutine"),
            0x3A: Instruction("ABX", 1, 3, MODE_IMPLIED, description="Add B to X"),
            0x3B: Instruction("RTI", 1, 12, MODE_IMPLIED, description="Return from interrupt"),
            0x3C: Instruction("PSHX", 1, 4, MODE_IMPLIED, description="Push X to stack"),
            0x3D: Instruction("MUL", 1, 10, MODE_IMPLIED, description="Multiply A * B"),
            0x3E: Instruction("WAI", 1, 9, MODE_IMPLIED, description="Wait for interrupt"),
            0x3F: Instruction("SWI", 1, 14, MODE_IMPLIED, description="Software interrupt"),
            
            # A register operations (inherent)
            0x40: Instruction("NEGA", 1, 2, MODE_IMPLIED, description="Negate A"),
            0x43: Instruction("COMA", 1, 2, MODE_IMPLIED, description="Complement A"),
            0x44: Instruction("LSRA", 1, 2, MODE_IMPLIED, description="Logical shift right A"),
            0x46: Instruction("RORA", 1, 2, MODE_IMPLIED, description="Rotate right A"),
            0x47: Instruction("ASRA", 1, 2, MODE_IMPLIED, description="Arithmetic shift right A"),
            0x48: Instruction("ASLA", 1, 2, MODE_IMPLIED, description="Arithmetic shift left A"),
            0x49: Instruction("ROLA", 1, 2, MODE_IMPLIED, description="Rotate left A"),
            0x4A: Instruction("DECA", 1, 2, MODE_IMPLIED, description="Decrement A"),
            0x4C: Instruction("INCA", 1, 2, MODE_IMPLIED, description="Increment A"),
            0x4D: Instruction("TSTA", 1, 2, MODE_IMPLIED, description="Test A"),
            0x4F: Instruction("CLRA", 1, 2, MODE_IMPLIED, description="Clear A"),
            
            # B register operations (inherent)
            0x50: Instruction("NEGB", 1, 2, MODE_IMPLIED, description="Negate B"),
            0x53: Instruction("COMB", 1, 2, MODE_IMPLIED, description="Complement B"),
            0x54: Instruction("LSRB", 1, 2, MODE_IMPLIED, description="Logical shift right B"),
            0x56: Instruction("RORB", 1, 2, MODE_IMPLIED, description="Rotate right B"),
            0x57: Instruction("ASRB", 1, 2, MODE_IMPLIED, description="Arithmetic shift right B"),
            0x58: Instruction("ASLB", 1, 2, MODE_IMPLIED, description="Arithmetic shift left B"),
            0x59: Instruction("ROLB", 1, 2, MODE_IMPLIED, description="Rotate left B"),
            0x5A: Instruction("DECB", 1, 2, MODE_IMPLIED, description="Decrement B"),
            0x5C: Instruction("INCB", 1, 2, MODE_IMPLIED, description="Increment B"),
            0x5D: Instruction("TSTB", 1, 2, MODE_IMPLIED, description="Test B"),
            0x5F: Instruction("CLRB", 1, 2, MODE_IMPLIED, description="Clear B"),
            
            # Memory operations (indexed X - 2 bytes)
            0x60: Instruction("NEG", 2, 6, MODE_INDEXED_X, description="Negate memory (idx)"),
            0x63: Instruction("COM", 2, 6, MODE_INDEXED_X, description="Complement memory (idx)"),
            0x64: Instruction("LSR", 2, 6, MODE_INDEXED_X, description="Logical shift right (idx)"),
            0x66: Instruction("ROR", 2, 6, MODE_INDEXED_X, description="Rotate right (idx)"),
            0x67: Instruction("ASR", 2, 6, MODE_INDEXED_X, description="Arithmetic shift right (idx)"),
            0x68: Instruction("ASL", 2, 6, MODE_INDEXED_X, description="Arithmetic shift left (idx)"),
            0x69: Instruction("ROL", 2, 6, MODE_INDEXED_X, description="Rotate left (idx)"),
            0x6A: Instruction("DEC", 2, 6, MODE_INDEXED_X, description="Decrement memory (idx)"),
            0x6C: Instruction("INC", 2, 6, MODE_INDEXED_X, description="Increment memory (idx)"),
            0x6D: Instruction("TST", 2, 6, MODE_INDEXED_X, description="Test memory (idx)"),
            0x6E: Instruction("JMP", 2, 3, MODE_INDEXED_X, description="Jump (idx)"),
            0x6F: Instruction("CLR", 2, 6, MODE_INDEXED_X, description="Clear memory (idx)"),
            
            # Memory operations (extended - 3 bytes)
            0x70: Instruction("NEG", 3, 6, MODE_EXTENDED, description="Negate memory (ext)"),
            0x73: Instruction("COM", 3, 6, MODE_EXTENDED, description="Complement memory (ext)"),
            0x74: Instruction("LSR", 3, 6, MODE_EXTENDED, description="Logical shift right (ext)"),
            0x76: Instruction("ROR", 3, 6, MODE_EXTENDED, description="Rotate right (ext)"),
            0x77: Instruction("ASR", 3, 6, MODE_EXTENDED, description="Arithmetic shift right (ext)"),
            0x78: Instruction("ASL", 3, 6, MODE_EXTENDED, description="Arithmetic shift left (ext)"),
            0x79: Instruction("ROL", 3, 6, MODE_EXTENDED, description="Rotate left (ext)"),
            0x7A: Instruction("DEC", 3, 6, MODE_EXTENDED, description="Decrement memory (ext)"),
            0x7C: Instruction("INC", 3, 6, MODE_EXTENDED, description="Increment memory (ext)"),
            0x7D: Instruction("TST", 3, 6, MODE_EXTENDED, description="Test memory (ext)"),
            0x7E: Instruction("JMP", 3, 3, MODE_EXTENDED, description="Jump (ext)"),
            0x7F: Instruction("CLR", 3, 6, MODE_EXTENDED, description="Clear memory (ext)"),
            
            # A register operations (immediate - 2 bytes)
            0x80: Instruction("SUBA", 2, 2, MODE_IMMEDIATE, description="Subtract from A (imm)"),
            0x81: Instruction("CMPA", 2, 2, MODE_IMMEDIATE, description="Compare A (imm)"),
            0x82: Instruction("SBCA", 2, 2, MODE_IMMEDIATE, description="Subtract with carry from A (imm)"),
            0x84: Instruction("ANDA", 2, 2, MODE_IMMEDIATE, description="AND A (imm)"),
            0x85: Instruction("BITA", 2, 2, MODE_IMMEDIATE, description="Bit test A (imm)"),
            0x86: Instruction("LDAA", 2, 2, MODE_IMMEDIATE, description="Load A (imm)"),
            0x88: Instruction("EORA", 2, 2, MODE_IMMEDIATE, description="XOR A (imm)"),
            0x89: Instruction("ADCA", 2, 2, MODE_IMMEDIATE, description="Add with carry to A (imm)"),
            0x8A: Instruction("ORAA", 2, 2, MODE_IMMEDIATE, description="OR A (imm)"),
            0x8B: Instruction("ADDA", 2, 2, MODE_IMMEDIATE, description="Add to A (imm)"),
            
            # D/X/S register operations (immediate - 3 bytes)
            0x83: Instruction("SUBD", 3, 4, MODE_IMMEDIATE, description="Subtract from D (imm)"),
            0x8C: Instruction("CPX", 3, 4, MODE_IMMEDIATE, description="Compare X (imm)"),
            0x8D: Instruction("BSR", 2, 6, MODE_RELATIVE, description="Branch to subroutine"),
            0x8E: Instruction("LDS", 3, 3, MODE_IMMEDIATE, description="Load SP (imm)"),
            0x8F: Instruction("XGDX", 1, 3, MODE_IMPLIED, description="Exchange D with X"),
            
            # A register operations (direct - 2 bytes)
            0x90: Instruction("SUBA", 2, 3, MODE_DIRECT, description="Subtract from A (dir)"),
            0x91: Instruction("CMPA", 2, 3, MODE_DIRECT, description="Compare A (dir)"),
            0x92: Instruction("SBCA", 2, 3, MODE_DIRECT, description="Subtract with carry from A (dir)"),
            0x94: Instruction("ANDA", 2, 3, MODE_DIRECT, description="AND A (dir)"),
            0x95: Instruction("BITA", 2, 3, MODE_DIRECT, description="Bit test A (dir)"),
            0x96: Instruction("LDAA", 2, 3, MODE_DIRECT, description="Load A (dir)"),
            0x97: Instruction("STAA", 2, 3, MODE_DIRECT, description="Store A (dir)"),
            0x98: Instruction("EORA", 2, 3, MODE_DIRECT, description="XOR A (dir)"),
            0x99: Instruction("ADCA", 2, 3, MODE_DIRECT, description="Add with carry to A (dir)"),
            0x9A: Instruction("ORAA", 2, 3, MODE_DIRECT, description="OR A (dir)"),
            0x9B: Instruction("ADDA", 2, 3, MODE_DIRECT, description="Add to A (dir)"),
            
            # D/X/S register operations (direct - 2 bytes)
            0x93: Instruction("SUBD", 2, 5, MODE_DIRECT, description="Subtract from D (dir)"),
            0x9C: Instruction("CPX", 2, 5, MODE_DIRECT, description="Compare X (dir)"),
            0x9D: Instruction("JSR", 2, 5, MODE_DIRECT, description="Jump to subroutine (dir)"),
            0x9E: Instruction("LDS", 2, 4, MODE_DIRECT, description="Load SP (dir)"),
            0x9F: Instruction("STS", 2, 4, MODE_DIRECT, description="Store SP (dir)"),
            
            # A register operations (indexed X - 2 bytes)
            0xA0: Instruction("SUBA", 2, 4, MODE_INDEXED_X, description="Subtract from A (idx)"),
            0xA1: Instruction("CMPA", 2, 4, MODE_INDEXED_X, description="Compare A (idx)"),
            0xA2: Instruction("SBCA", 2, 4, MODE_INDEXED_X, description="Subtract with carry from A (idx)"),
            0xA4: Instruction("ANDA", 2, 4, MODE_INDEXED_X, description="AND A (idx)"),
            0xA5: Instruction("BITA", 2, 4, MODE_INDEXED_X, description="Bit test A (idx)"),
            0xA6: Instruction("LDAA", 2, 4, MODE_INDEXED_X, description="Load A (idx)"),
            0xA7: Instruction("STAA", 2, 4, MODE_INDEXED_X, description="Store A (idx)"),
            0xA8: Instruction("EORA", 2, 4, MODE_INDEXED_X, description="XOR A (idx)"),
            0xA9: Instruction("ADCA", 2, 4, MODE_INDEXED_X, description="Add with carry to A (idx)"),
            0xAA: Instruction("ORAA", 2, 4, MODE_INDEXED_X, description="OR A (idx)"),
            0xAB: Instruction("ADDA", 2, 4, MODE_INDEXED_X, description="Add to A (idx)"),
            
            # D/X/S register operations (indexed X - 2 bytes)
            0xA3: Instruction("SUBD", 2, 6, MODE_INDEXED_X, description="Subtract from D (idx)"),
            0xAC: Instruction("CPX", 2, 6, MODE_INDEXED_X, description="Compare X (idx)"),
            0xAD: Instruction("JSR", 2, 6, MODE_INDEXED_X, description="Jump to subroutine (idx)"),
            0xAE: Instruction("LDS", 2, 5, MODE_INDEXED_X, description="Load SP (idx)"),
            0xAF: Instruction("STS", 2, 5, MODE_INDEXED_X, description="Store SP (idx)"),
            
            # A register operations (extended - 3 bytes)
            0xB0: Instruction("SUBA", 3, 4, MODE_EXTENDED, description="Subtract from A (ext)"),
            0xB1: Instruction("CMPA", 3, 4, MODE_EXTENDED, description="Compare A (ext)"),
            0xB2: Instruction("SBCA", 3, 4, MODE_EXTENDED, description="Subtract with carry from A (ext)"),
            0xB4: Instruction("ANDA", 3, 4, MODE_EXTENDED, description="AND A (ext)"),
            0xB5: Instruction("BITA", 3, 4, MODE_EXTENDED, description="Bit test A (ext)"),
            0xB6: Instruction("LDAA", 3, 4, MODE_EXTENDED, description="Load A (ext)"),
            0xB7: Instruction("STAA", 3, 4, MODE_EXTENDED, description="Store A (ext)"),
            0xB8: Instruction("EORA", 3, 4, MODE_EXTENDED, description="XOR A (ext)"),
            0xB9: Instruction("ADCA", 3, 4, MODE_EXTENDED, description="Add with carry to A (ext)"),
            0xBA: Instruction("ORAA", 3, 4, MODE_EXTENDED, description="OR A (ext)"),
            0xBB: Instruction("ADDA", 3, 4, MODE_EXTENDED, description="Add to A (ext)"),
            
            # D/X/S register operations (extended - 3 bytes)
            0xB3: Instruction("SUBD", 3, 6, MODE_EXTENDED, description="Subtract from D (ext)"),
            0xBC: Instruction("CPX", 3, 6, MODE_EXTENDED, description="Compare X (ext)"),
            0xBD: Instruction("JSR", 3, 6, MODE_EXTENDED, description="Jump to subroutine (ext)"),
            0xBE: Instruction("LDS", 3, 5, MODE_EXTENDED, description="Load SP (ext)"),
            0xBF: Instruction("STS", 3, 5, MODE_EXTENDED, description="Store SP (ext)"),
            
            # B register operations (immediate - 2 bytes)
            0xC0: Instruction("SUBB", 2, 2, MODE_IMMEDIATE, description="Subtract from B (imm)"),
            0xC1: Instruction("CMPB", 2, 2, MODE_IMMEDIATE, description="Compare B (imm)"),
            0xC2: Instruction("SBCB", 2, 2, MODE_IMMEDIATE, description="Subtract with carry from B (imm)"),
            0xC4: Instruction("ANDB", 2, 2, MODE_IMMEDIATE, description="AND B (imm)"),
            0xC5: Instruction("BITB", 2, 2, MODE_IMMEDIATE, description="Bit test B (imm)"),
            0xC6: Instruction("LDAB", 2, 2, MODE_IMMEDIATE, description="Load B (imm)"),
            0xC8: Instruction("EORB", 2, 2, MODE_IMMEDIATE, description="XOR B (imm)"),
            0xC9: Instruction("ADCB", 2, 2, MODE_IMMEDIATE, description="Add with carry to B (imm)"),
            0xCA: Instruction("ORAB", 2, 2, MODE_IMMEDIATE, description="OR B (imm)"),
            0xCB: Instruction("ADDB", 2, 2, MODE_IMMEDIATE, description="Add to B (imm)"),
            
            # D/X register operations (immediate - 3 bytes)
            0xC3: Instruction("ADDD", 3, 4, MODE_IMMEDIATE, description="Add to D (imm)"),
            0xCC: Instruction("LDD", 3, 3, MODE_IMMEDIATE, description="Load D (imm)"),
            0xCE: Instruction("LDX", 3, 3, MODE_IMMEDIATE, description="Load X (imm)"),
            0xCF: Instruction("STOP", 1, 2, MODE_IMPLIED, description="Stop (low power mode)"),
            
            # B register operations (direct - 2 bytes)
            0xD0: Instruction("SUBB", 2, 3, MODE_DIRECT, description="Subtract from B (dir)"),
            0xD1: Instruction("CMPB", 2, 3, MODE_DIRECT, description="Compare B (dir)"),
            0xD2: Instruction("SBCB", 2, 3, MODE_DIRECT, description="Subtract with carry from B (dir)"),
            0xD4: Instruction("ANDB", 2, 3, MODE_DIRECT, description="AND B (dir)"),
            0xD5: Instruction("BITB", 2, 3, MODE_DIRECT, description="Bit test B (dir)"),
            0xD6: Instruction("LDAB", 2, 3, MODE_DIRECT, description="Load B (dir)"),
            0xD7: Instruction("STAB", 2, 3, MODE_DIRECT, description="Store B (dir)"),
            0xD8: Instruction("EORB", 2, 3, MODE_DIRECT, description="XOR B (dir)"),
            0xD9: Instruction("ADCB", 2, 3, MODE_DIRECT, description="Add with carry to B (dir)"),
            0xDA: Instruction("ORAB", 2, 3, MODE_DIRECT, description="OR B (dir)"),
            0xDB: Instruction("ADDB", 2, 3, MODE_DIRECT, description="Add to B (dir)"),
            
            # D/X register operations (direct - 2 bytes)
            0xD3: Instruction("ADDD", 2, 5, MODE_DIRECT, description="Add to D (dir)"),
            0xDC: Instruction("LDD", 2, 4, MODE_DIRECT, description="Load D (dir)"),
            0xDD: Instruction("STD", 2, 4, MODE_DIRECT, description="Store D (dir)"),
            0xDE: Instruction("LDX", 2, 4, MODE_DIRECT, description="Load X (dir)"),
            0xDF: Instruction("STX", 2, 4, MODE_DIRECT, description="Store X (dir)"),
            
            # B register operations (indexed X - 2 bytes)
            0xE0: Instruction("SUBB", 2, 4, MODE_INDEXED_X, description="Subtract from B (idx)"),
            0xE1: Instruction("CMPB", 2, 4, MODE_INDEXED_X, description="Compare B (idx)"),
            0xE2: Instruction("SBCB", 2, 4, MODE_INDEXED_X, description="Subtract with carry from B (idx)"),
            0xE4: Instruction("ANDB", 2, 4, MODE_INDEXED_X, description="AND B (idx)"),
            0xE5: Instruction("BITB", 2, 4, MODE_INDEXED_X, description="Bit test B (idx)"),
            0xE6: Instruction("LDAB", 2, 4, MODE_INDEXED_X, description="Load B (idx)"),
            0xE7: Instruction("STAB", 2, 4, MODE_INDEXED_X, description="Store B (idx)"),
            0xE8: Instruction("EORB", 2, 4, MODE_INDEXED_X, description="XOR B (idx)"),
            0xE9: Instruction("ADCB", 2, 4, MODE_INDEXED_X, description="Add with carry to B (idx)"),
            0xEA: Instruction("ORAB", 2, 4, MODE_INDEXED_X, description="OR B (idx)"),
            0xEB: Instruction("ADDB", 2, 4, MODE_INDEXED_X, description="Add to B (idx)"),
            
            # D/X register operations (indexed X - 2 bytes)
            0xE3: Instruction("ADDD", 2, 6, MODE_INDEXED_X, description="Add to D (idx)"),
            0xEC: Instruction("LDD", 2, 5, MODE_INDEXED_X, description="Load D (idx)"),
            0xED: Instruction("STD", 2, 5, MODE_INDEXED_X, description="Store D (idx)"),
            0xEE: Instruction("LDX", 2, 5, MODE_INDEXED_X, description="Load X (idx)"),
            0xEF: Instruction("STX", 2, 5, MODE_INDEXED_X, description="Store X (idx)"),
            
            # B register operations (extended - 3 bytes)
            0xF0: Instruction("SUBB", 3, 4, MODE_EXTENDED, description="Subtract from B (ext)"),
            0xF1: Instruction("CMPB", 3, 4, MODE_EXTENDED, description="Compare B (ext)"),
            0xF2: Instruction("SBCB", 3, 4, MODE_EXTENDED, description="Subtract with carry from B (ext)"),
            0xF4: Instruction("ANDB", 3, 4, MODE_EXTENDED, description="AND B (ext)"),
            0xF5: Instruction("BITB", 3, 4, MODE_EXTENDED, description="Bit test B (ext)"),
            0xF6: Instruction("LDAB", 3, 4, MODE_EXTENDED, description="Load B (ext)"),
            0xF7: Instruction("STAB", 3, 4, MODE_EXTENDED, description="Store B (ext)"),
            0xF8: Instruction("EORB", 3, 4, MODE_EXTENDED, description="XOR B (ext)"),
            0xF9: Instruction("ADCB", 3, 4, MODE_EXTENDED, description="Add with carry to B (ext)"),
            0xFA: Instruction("ORAB", 3, 4, MODE_EXTENDED, description="OR B (ext)"),
            0xFB: Instruction("ADDB", 3, 4, MODE_EXTENDED, description="Add to B (ext)"),
            
            # D/X register operations (extended - 3 bytes)
            0xF3: Instruction("ADDD", 3, 6, MODE_EXTENDED, description="Add to D (ext)"),
            0xFC: Instruction("LDD", 3, 5, MODE_EXTENDED, description="Load D (ext)"),
            0xFD: Instruction("STD", 3, 5, MODE_EXTENDED, description="Store D (ext)"),
            0xFE: Instruction("LDX", 3, 5, MODE_EXTENDED, description="Load X (ext)"),
            0xFF: Instruction("STX", 3, 5, MODE_EXTENDED, description="Store X (ext)"),
        }
    
    def _build_prebyte_18(self) -> Dict[int, Instruction]:
        """Prebyte 0x18 - Y register operations.
        
        Two effects depending on instruction type:
          1. For most ops (LDAA, ADDA, etc.): changes index register X→Y
             e.g. $18 A6 = LDAA offset,Y (base A6 = LDAA offset,X)
          2. For X-register ops (LDX, STX, CPX): changes register X→Y  
             e.g. $18 CE = LDY #imm (base CE = LDX #imm)
             e.g. $18 EE = LDY offset,Y (base EE = LDX offset,X → Y replaces BOTH)
        
        Cross-validated against assembler (.../hc11_compiler/assembler.py)
        and Motorola MC68HC11 Reference Manual Rev3, Table A-2.
        """
        return {
            # ── Inherent Y-register ops ──
            0x08: Instruction("INY", 2, 4, MODE_IMPLIED, 0x18, "Increment Y"),
            0x09: Instruction("DEY", 2, 4, MODE_IMPLIED, 0x18, "Decrement Y"),
            0x30: Instruction("TSY", 2, 4, MODE_IMPLIED, 0x18, "Transfer SP to Y"),
            0x35: Instruction("TYS", 2, 4, MODE_IMPLIED, 0x18, "Transfer Y to SP"),
            0x38: Instruction("PULY", 2, 5, MODE_IMPLIED, 0x18, "Pull Y from stack"),
            0x3A: Instruction("ABY", 2, 4, MODE_IMPLIED, 0x18, "Add B to Y"),
            0x3C: Instruction("PSHY", 2, 5, MODE_IMPLIED, 0x18, "Push Y to stack"),
            0x8F: Instruction("XGDY", 2, 4, MODE_IMPLIED, 0x18, "Exchange D with Y"),
            
            # ── CPY (Compare Y) ──
            0x8C: Instruction("CPY", 4, 5, MODE_IMMEDIATE, 0x18, "Compare Y (imm)"),
            0x9C: Instruction("CPY", 3, 6, MODE_DIRECT, 0x18, "Compare Y (dir)"),
            0xAC: Instruction("CPY", 3, 7, MODE_INDEXED_Y, 0x18, "Compare Y (idy)"),  # $18 AC = CPY offset,Y (NOT idx!)
            0xBC: Instruction("CPY", 4, 7, MODE_EXTENDED, 0x18, "Compare Y (ext)"),
            
            # ── LDY (Load Y) ──
            0xCE: Instruction("LDY", 4, 4, MODE_IMMEDIATE, 0x18, "Load Y (imm)"),
            0xDE: Instruction("LDY", 3, 5, MODE_DIRECT, 0x18, "Load Y (dir)"),
            0xEE: Instruction("LDY", 3, 6, MODE_INDEXED_Y, 0x18, "Load Y (idy)"),   # $18 EE = LDY offset,Y (NOT idx!)
            0xFE: Instruction("LDY", 4, 6, MODE_EXTENDED, 0x18, "Load Y (ext)"),
            
            # ── STY (Store Y) ──
            0xDF: Instruction("STY", 3, 5, MODE_DIRECT, 0x18, "Store Y (dir)"),
            0xEF: Instruction("STY", 3, 6, MODE_INDEXED_Y, 0x18, "Store Y (idy)"),   # $18 EF = STY offset,Y (NOT idx!)
            0xFF: Instruction("STY", 4, 6, MODE_EXTENDED, 0x18, "Store Y (ext)"),
            
            # ── Y-indexed variants of all standard ops ──
            # Memory ops (offset,Y) — base ops are offset,X ($6x)
            0x60: Instruction("NEG", 3, 7, MODE_INDEXED_Y, 0x18, "Negate memory (idy)"),
            0x63: Instruction("COM", 3, 7, MODE_INDEXED_Y, 0x18, "Complement memory (idy)"),
            0x64: Instruction("LSR", 3, 7, MODE_INDEXED_Y, 0x18, "Logical shift right (idy)"),
            0x66: Instruction("ROR", 3, 7, MODE_INDEXED_Y, 0x18, "Rotate right (idy)"),
            0x67: Instruction("ASR", 3, 7, MODE_INDEXED_Y, 0x18, "Arithmetic shift right (idy)"),
            0x68: Instruction("ASL", 3, 7, MODE_INDEXED_Y, 0x18, "Arithmetic shift left (idy)"),
            0x69: Instruction("ROL", 3, 7, MODE_INDEXED_Y, 0x18, "Rotate left (idy)"),
            0x6A: Instruction("DEC", 3, 7, MODE_INDEXED_Y, 0x18, "Decrement memory (idy)"),
            0x6C: Instruction("INC", 3, 7, MODE_INDEXED_Y, 0x18, "Increment memory (idy)"),
            0x6D: Instruction("TST", 3, 7, MODE_INDEXED_Y, 0x18, "Test memory (idy)"),
            0x6E: Instruction("JMP", 3, 4, MODE_INDEXED_Y, 0x18, "Jump (idy)"),
            0x6F: Instruction("CLR", 3, 7, MODE_INDEXED_Y, 0x18, "Clear memory (idy)"),
            
            # A-register ops (offset,Y) — base ops are $Ax
            0xA0: Instruction("SUBA", 3, 5, MODE_INDEXED_Y, 0x18, "Subtract from A (idy)"),
            0xA1: Instruction("CMPA", 3, 5, MODE_INDEXED_Y, 0x18, "Compare A (idy)"),
            0xA2: Instruction("SBCA", 3, 5, MODE_INDEXED_Y, 0x18, "Subtract with carry from A (idy)"),
            0xA4: Instruction("ANDA", 3, 5, MODE_INDEXED_Y, 0x18, "AND A (idy)"),
            0xA5: Instruction("BITA", 3, 5, MODE_INDEXED_Y, 0x18, "Bit test A (idy)"),
            0xA6: Instruction("LDAA", 3, 5, MODE_INDEXED_Y, 0x18, "Load A (idy)"),
            0xA7: Instruction("STAA", 3, 5, MODE_INDEXED_Y, 0x18, "Store A (idy)"),
            0xA8: Instruction("EORA", 3, 5, MODE_INDEXED_Y, 0x18, "XOR A (idy)"),
            0xA9: Instruction("ADCA", 3, 5, MODE_INDEXED_Y, 0x18, "Add with carry to A (idy)"),
            0xAA: Instruction("ORAA", 3, 5, MODE_INDEXED_Y, 0x18, "OR A (idy)"),
            0xAB: Instruction("ADDA", 3, 5, MODE_INDEXED_Y, 0x18, "Add to A (idy)"),
            
            # D/X/S register ops (offset,Y) — base ops are $Ax (16-bit)
            0xA3: Instruction("SUBD", 3, 7, MODE_INDEXED_Y, 0x18, "Subtract from D (idy)"),
            0xAD: Instruction("JSR", 3, 7, MODE_INDEXED_Y, 0x18, "Jump to subroutine (idy)"),
            0xAE: Instruction("LDS", 3, 6, MODE_INDEXED_Y, 0x18, "Load SP (idy)"),
            0xAF: Instruction("STS", 3, 6, MODE_INDEXED_Y, 0x18, "Store SP (idy)"),
            
            # B-register ops (offset,Y) — base ops are $Ex
            0xE0: Instruction("SUBB", 3, 5, MODE_INDEXED_Y, 0x18, "Subtract from B (idy)"),
            0xE1: Instruction("CMPB", 3, 5, MODE_INDEXED_Y, 0x18, "Compare B (idy)"),
            0xE2: Instruction("SBCB", 3, 5, MODE_INDEXED_Y, 0x18, "Subtract with carry from B (idy)"),
            0xE4: Instruction("ANDB", 3, 5, MODE_INDEXED_Y, 0x18, "AND B (idy)"),
            0xE5: Instruction("BITB", 3, 5, MODE_INDEXED_Y, 0x18, "Bit test B (idy)"),
            0xE6: Instruction("LDAB", 3, 5, MODE_INDEXED_Y, 0x18, "Load B (idy)"),
            0xE7: Instruction("STAB", 3, 5, MODE_INDEXED_Y, 0x18, "Store B (idy)"),
            0xE8: Instruction("EORB", 3, 5, MODE_INDEXED_Y, 0x18, "XOR B (idy)"),
            0xE9: Instruction("ADCB", 3, 5, MODE_INDEXED_Y, 0x18, "Add with carry to B (idy)"),
            0xEA: Instruction("ORAB", 3, 5, MODE_INDEXED_Y, 0x18, "OR B (idy)"),
            0xEB: Instruction("ADDB", 3, 5, MODE_INDEXED_Y, 0x18, "Add to B (idy)"),
            
            # D-register ops (offset,Y) — base ops are $Ex (16-bit)
            0xE3: Instruction("ADDD", 3, 7, MODE_INDEXED_Y, 0x18, "Add to D (idy)"),
            0xEC: Instruction("LDD", 3, 6, MODE_INDEXED_Y, 0x18, "Load D (idy)"),
            0xED: Instruction("STD", 3, 6, MODE_INDEXED_Y, 0x18, "Store D (idy)"),
            
            # ── Bit operations (Y-indexed) ──
            0x1C: Instruction("BSET", 4, 8, MODE_BIT_IDY, 0x18, "Set bits (idy)"),
            0x1D: Instruction("BCLR", 4, 8, MODE_BIT_IDY, 0x18, "Clear bits (idy)"),
            0x1E: Instruction("BRSET", 5, 8, MODE_BIT_IDY, 0x18, "Branch if bits set (idy)"),
            0x1F: Instruction("BRCLR", 5, 8, MODE_BIT_IDY, 0x18, "Branch if bits clear (idy)"),
        }
    
    def _build_prebyte_1A(self) -> Dict[int, Instruction]:
        """Prebyte 0x1A - CPD and Y-register IDX operations.
        
        $1A prefix serves two purposes:
          1. CPD instruction (all modes): $1A 83/93/A3/B3
          2. CPY/LDY/STY indexed,X: $1A AC/EE/EF
             (These need $1A because $18 would make them IDY, not IDX)
        """
        return {
            # CPD (Compare D)
            0x83: Instruction("CPD", 4, 5, MODE_IMMEDIATE, 0x1A, "Compare D (imm)"),
            0x93: Instruction("CPD", 3, 6, MODE_DIRECT, 0x1A, "Compare D (dir)"),
            0xA3: Instruction("CPD", 3, 7, MODE_INDEXED_X, 0x1A, "Compare D (idx)"),
            0xB3: Instruction("CPD", 4, 7, MODE_EXTENDED, 0x1A, "Compare D (ext)"),
            # CPY indexed,X
            0xAC: Instruction("CPY", 3, 7, MODE_INDEXED_X, 0x1A, "Compare Y (idx)"),
            # LDY indexed,X
            0xEE: Instruction("LDY", 3, 6, MODE_INDEXED_X, 0x1A, "Load Y (idx)"),
            # STY indexed,X
            0xEF: Instruction("STY", 3, 6, MODE_INDEXED_X, 0x1A, "Store Y (idx)"),
        }
    
    def _build_prebyte_CD(self) -> Dict[int, Instruction]:
        """Prebyte 0xCD - Y-indexed CPD/CPX operations"""
        return {
            0xA3: Instruction("CPD", 3, 7, MODE_INDEXED_Y, 0xCD, "Compare D (idy)"),
            0xAC: Instruction("CPX", 3, 7, MODE_INDEXED_Y, 0xCD, "Compare X (idy)"),
            0xEE: Instruction("LDX", 3, 6, MODE_INDEXED_Y, 0xCD, "Load X (idy)"),
            0xEF: Instruction("STX", 3, 6, MODE_INDEXED_Y, 0xCD, "Store X (idy)"),
        }
    
    def get_instruction(self, opcode: int, prebyte: int = 0x00) -> Optional[Instruction]:
        """
        Get instruction metadata
        
        Args:
            opcode: Main opcode byte
            prebyte: Prebyte (0x00, 0x18, 0x1A, 0xCD)
            
        Returns:
            Instruction object or None
        """
        if prebyte == 0x18:
            return self._prebyte_18.get(opcode)
        elif prebyte == 0x1A:
            return self._prebyte_1A.get(opcode)
        elif prebyte == 0xCD:
            return self._prebyte_CD.get(opcode)
        else:
            return self._opcodes.get(opcode)
    
    def is_prebyte(self, opcode: int) -> bool:
        """Check if opcode is a prebyte"""
        return opcode in (0x18, 0x1A, 0xCD)
    
    def get_all_opcodes(self) -> Dict[int, Instruction]:
        """Get all single-byte opcodes"""
        return self._opcodes.copy()
    
    def get_statistics(self) -> Dict[str, int]:
        """Get instruction set statistics"""
        return {
            'total_base_opcodes': len(self._opcodes),
            'prebyte_18_opcodes': len(self._prebyte_18),
            'prebyte_1A_opcodes': len(self._prebyte_1A),
            'prebyte_CD_opcodes': len(self._prebyte_CD),
            'total_instructions': (len(self._opcodes) + len(self._prebyte_18) + 
                                  len(self._prebyte_1A) + len(self._prebyte_CD))
        }


# Global instance for easy access
HC11_OPCODES = HC11InstructionSet()


def main():
    """Test opcode module"""
    print("=" * 70)
    print("HC11 Unified Opcode Table")
    print("=" * 70)
    
    stats = HC11_OPCODES.get_statistics()
    print(f"\nInstruction Set Statistics:")
    print(f"  Base opcodes: {stats['total_base_opcodes']}")
    print(f"  Prebyte 0x18: {stats['prebyte_18_opcodes']}")
    print(f"  Prebyte 0x1A: {stats['prebyte_1A_opcodes']}")
    print(f"  Prebyte 0xCD: {stats['prebyte_CD_opcodes']}")
    print(f"  Total: {stats['total_instructions']}")
    
    # Test some critical opcodes
    print("\n" + "=" * 70)
    print("Critical Opcode Verification:")
    print("=" * 70)
    
    critical = [
        (0x12, 0x00, "BRSET direct should be 4 bytes"),
        (0x14, 0x00, "BSET direct should be 3 bytes"),
        (0x1C, 0x00, "BSET indexed should be 3 bytes"),
        (0x18, 0x00, "PREFIX_18"),
        (0xCE, 0x18, "LDY immediate (prebyte 0x18)"),
        (0x83, 0x1A, "CPD immediate (prebyte 0x1A)"),
        (0xBD, 0x00, "JSR extended should be 3 bytes"),
    ]
    
    for opcode, prebyte, desc in critical:
        inst = HC11_OPCODES.get_instruction(opcode, prebyte)
        if inst:
            print(f"  0x{opcode:02X} ({prebyte:02X}): {inst.mnemonic:6s} "
                  f"{inst.length}B, {inst.cycles}cy - {desc}")
        else:
            print(f"  0x{opcode:02X} ({prebyte:02X}): NOT FOUND - {desc}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
