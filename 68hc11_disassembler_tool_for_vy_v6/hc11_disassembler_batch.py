#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HC11 Batch Disassembler - Multiple Address Ranges
==================================================
Disassemble multiple addresses from XDF or manual list in one run.
always compare outputs with other tools e.g. udis.py and 6811.py with command lines on addresses.
and other tools in hc11 resources or ghidra with jython to parse xdfs and account for bank switching and offsets.
double check outputs .json for correct models. and masks (definition and firmware and osid.)
Improvements from udis comparison:
- Format string table for operands
- PCR flag in opcode table
- Batch address processing
- CSV/JSON output formats
- XDF address extraction

Date: January 21, 2026
Author: KingAI Automotive Research
"""

import sys
import io
import json
import csv
import argparse
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ============================================================================
# CONSTANTS AND FLAGS (inspired by udis)
# ============================================================================

PCR = 1  # PC-relative flag for branches
VY_CODE_OFFSET = 0x10000  # VY V6 128KB binary: file 0x10000+ = CPU 0x0000+

# Format strings for operands (cleaner than hardcoded f-strings)
FORMAT_TABLE = {
    "inherent": "",
    "immediate": "#${0:02X}",
    "immediate16": "#${0:04X}",
    "direct": "${0:02X}",
    "extended": "${0:04X}",
    "indexed": "${0:02X},X",
    "indexed_y": "${0:02X},Y",
    "relative": "${0:04X}",
    "bset_direct": "${0:02X}, #${1:02X}",
    "brset_direct": "${0:02X}, #${1:02X}, ${2:04X}",
}

# ============================================================================
# COMPLETE OPCODE TABLE (with PCR flags)
# ============================================================================

INSTRUCTIONS = {
    # Inherent (1 byte)
    0x00: ("TEST", 1, 0, "inherent", 0),
    0x01: ("NOP", 1, 2, "inherent", 0),
    0x02: ("IDIV", 1, 41, "inherent", 0),
    0x03: ("FDIV", 1, 41, "inherent", 0),
    0x04: ("LSRD", 1, 3, "inherent", 0),
    0x05: ("ASLD", 1, 3, "inherent", 0),
    0x06: ("TAP", 1, 2, "inherent", 0),
    0x07: ("TPA", 1, 2, "inherent", 0),
    0x08: ("INX", 1, 3, "inherent", 0),
    0x09: ("DEX", 1, 3, "inherent", 0),
    0x0A: ("CLV", 1, 2, "inherent", 0),
    0x0B: ("SEV", 1, 2, "inherent", 0),
    0x0C: ("CLC", 1, 2, "inherent", 0),
    0x0D: ("SEC", 1, 2, "inherent", 0),
    0x0E: ("CLI", 1, 2, "inherent", 0),
    0x0F: ("SEI", 1, 2, "inherent", 0),
    0x10: ("SBA", 1, 2, "inherent", 0),
    0x11: ("CBA", 1, 2, "inherent", 0),
    0x16: ("TAB", 1, 2, "inherent", 0),
    0x17: ("TBA", 1, 2, "inherent", 0),
    0x19: ("DAA", 1, 2, "inherent", 0),
    0x1B: ("ABA", 1, 2, "inherent", 0),
    0x30: ("TSX", 1, 3, "inherent", 0),
    0x31: ("INS", 1, 3, "inherent", 0),
    0x32: ("PULA", 1, 4, "inherent", 0),
    0x33: ("PULB", 1, 4, "inherent", 0),
    0x34: ("DES", 1, 3, "inherent", 0),
    0x35: ("TXS", 1, 3, "inherent", 0),
    0x36: ("PSHA", 1, 3, "inherent", 0),
    0x37: ("PSHB", 1, 3, "inherent", 0),
    0x38: ("PULX", 1, 5, "inherent", 0),
    0x39: ("RTS", 1, 5, "inherent", 0),
    0x3A: ("ABX", 1, 3, "inherent", 0),
    0x3B: ("RTI", 1, 12, "inherent", 0),
    0x3C: ("PSHX", 1, 4, "inherent", 0),
    0x3D: ("MUL", 1, 10, "inherent", 0),
    0x3E: ("WAI", 1, 0, "inherent", 0),
    0x3F: ("SWI", 1, 14, "inherent", 0),
    0x40: ("NEGA", 1, 2, "inherent", 0),
    0x43: ("COMA", 1, 2, "inherent", 0),
    0x44: ("LSRA", 1, 2, "inherent", 0),
    0x46: ("RORA", 1, 2, "inherent", 0),
    0x47: ("ASRA", 1, 2, "inherent", 0),
    0x48: ("ASLA", 1, 2, "inherent", 0),
    0x49: ("ROLA", 1, 2, "inherent", 0),
    0x4A: ("DECA", 1, 2, "inherent", 0),
    0x4C: ("INCA", 1, 2, "inherent", 0),
    0x4D: ("TSTA", 1, 2, "inherent", 0),
    0x4F: ("CLRA", 1, 2, "inherent", 0),
    0x50: ("NEGB", 1, 2, "inherent", 0),
    0x53: ("COMB", 1, 2, "inherent", 0),
    0x54: ("LSRB", 1, 2, "inherent", 0),
    0x56: ("RORB", 1, 2, "inherent", 0),
    0x57: ("ASRB", 1, 2, "inherent", 0),
    0x58: ("ASLB", 1, 2, "inherent", 0),
    0x59: ("ROLB", 1, 2, "inherent", 0),
    0x5A: ("DECB", 1, 2, "inherent", 0),
    0x5C: ("INCB", 1, 2, "inherent", 0),
    0x5D: ("TSTB", 1, 2, "inherent", 0),
    0x5F: ("CLRB", 1, 2, "inherent", 0),
    0x8F: ("XGDX", 1, 3, "inherent", 0),
    0xCF: ("STOP", 1, 2, "inherent", 0),
    
    # Branch instructions (2 bytes) - all have PCR flag
    0x20: ("BRA", 2, 3, "relative", PCR),
    0x21: ("BRN", 2, 3, "relative", PCR),
    0x22: ("BHI", 2, 3, "relative", PCR),
    0x23: ("BLS", 2, 3, "relative", PCR),
    0x24: ("BCC", 2, 3, "relative", PCR),
    0x25: ("BCS", 2, 3, "relative", PCR),
    0x26: ("BNE", 2, 3, "relative", PCR),
    0x27: ("BEQ", 2, 3, "relative", PCR),
    0x28: ("BVC", 2, 3, "relative", PCR),
    0x29: ("BVS", 2, 3, "relative", PCR),
    0x2A: ("BPL", 2, 3, "relative", PCR),
    0x2B: ("BMI", 2, 3, "relative", PCR),
    0x2C: ("BGE", 2, 3, "relative", PCR),
    0x2D: ("BLT", 2, 3, "relative", PCR),
    0x2E: ("BGT", 2, 3, "relative", PCR),
    0x2F: ("BLE", 2, 3, "relative", PCR),
    0x8D: ("BSR", 2, 6, "relative", PCR),
    
    # SUBA - Subtract A (all 4 addressing modes)
    0x80: ("SUBA", 2, 2, "immediate", 0),
    0x90: ("SUBA", 2, 3, "direct", 0),
    0xA0: ("SUBA", 2, 4, "indexed", 0),
    0xB0: ("SUBA", 3, 4, "extended", 0),
    
    # CMPA - Compare A
    0x81: ("CMPA", 2, 2, "immediate", 0),
    0x91: ("CMPA", 2, 3, "direct", 0),
    0xA1: ("CMPA", 2, 4, "indexed", 0),
    0xB1: ("CMPA", 3, 4, "extended", 0),
    
    # SBCA - Subtract with Carry A
    0x82: ("SBCA", 2, 2, "immediate", 0),
    0x92: ("SBCA", 2, 3, "direct", 0),
    0xA2: ("SBCA", 2, 4, "indexed", 0),
    0xB2: ("SBCA", 3, 4, "extended", 0),
    
    # SUBD - Subtract D (16-bit)
    0x83: ("SUBD", 3, 4, "immediate16", 0),
    0x93: ("SUBD", 2, 5, "direct", 0),
    0xA3: ("SUBD", 2, 6, "indexed", 0),
    0xB3: ("SUBD", 3, 6, "extended", 0),
    
    # ANDA - AND A
    0x84: ("ANDA", 2, 2, "immediate", 0),
    0x94: ("ANDA", 2, 3, "direct", 0),
    0xA4: ("ANDA", 2, 4, "indexed", 0),
    0xB4: ("ANDA", 3, 4, "extended", 0),
    
    # BITA - Bit Test A
    0x85: ("BITA", 2, 2, "immediate", 0),
    0x95: ("BITA", 2, 3, "direct", 0),
    0xA5: ("BITA", 2, 4, "indexed", 0),
    0xB5: ("BITA", 3, 4, "extended", 0),
    
    # LDAA - Load A
    0x86: ("LDAA", 2, 2, "immediate", 0),
    0x96: ("LDAA", 2, 3, "direct", 0),
    0xA6: ("LDAA", 2, 4, "indexed", 0),
    0xB6: ("LDAA", 3, 4, "extended", 0),
    
    # STAA - Store A (no immediate mode)
    0x97: ("STAA", 2, 3, "direct", 0),
    0xA7: ("STAA", 2, 4, "indexed", 0),
    0xB7: ("STAA", 3, 4, "extended", 0),
    
    # EORA - Exclusive OR A
    0x88: ("EORA", 2, 2, "immediate", 0),
    0x98: ("EORA", 2, 3, "direct", 0),
    0xA8: ("EORA", 2, 4, "indexed", 0),
    0xB8: ("EORA", 3, 4, "extended", 0),
    
    # ADCA - Add with Carry A
    0x89: ("ADCA", 2, 2, "immediate", 0),
    0x99: ("ADCA", 2, 3, "direct", 0),
    0xA9: ("ADCA", 2, 4, "indexed", 0),
    0xB9: ("ADCA", 3, 4, "extended", 0),
    
    # ORAA - OR A
    0x8A: ("ORAA", 2, 2, "immediate", 0),
    0x9A: ("ORAA", 2, 3, "direct", 0),
    0xAA: ("ORAA", 2, 4, "indexed", 0),
    0xBA: ("ORAA", 3, 4, "extended", 0),
    
    # ADDA - Add A
    0x8B: ("ADDA", 2, 2, "immediate", 0),
    0x9B: ("ADDA", 2, 3, "direct", 0),
    0xAB: ("ADDA", 2, 4, "indexed", 0),
    0xBB: ("ADDA", 3, 4, "extended", 0),
    
    # CPX - Compare X
    0x8C: ("CPX", 3, 4, "immediate16", 0),
    0x9C: ("CPX", 2, 5, "direct", 0),
    0xAC: ("CPX", 2, 6, "indexed", 0),
    0xBC: ("CPX", 3, 6, "extended", 0),
    
    # BSR already listed above (0x8D)
    # JSR
    0x9D: ("JSR", 2, 5, "direct", 0),
    0xAD: ("JSR", 2, 5, "indexed", 0),
    0xBD: ("JSR", 3, 6, "extended", 0),
    
    # LDS - Load Stack Pointer
    0x8E: ("LDS", 3, 3, "immediate16", 0),
    0x9E: ("LDS", 2, 4, "direct", 0),
    0xAE: ("LDS", 2, 5, "indexed", 0),
    0xBE: ("LDS", 3, 5, "extended", 0),
    
    # STS - Store Stack Pointer (no immediate)
    0x9F: ("STS", 2, 4, "direct", 0),
    0xAF: ("STS", 2, 5, "indexed", 0),
    0xBF: ("STS", 3, 5, "extended", 0),
    
    # SUBB - Subtract B
    0xC0: ("SUBB", 2, 2, "immediate", 0),
    0xD0: ("SUBB", 2, 3, "direct", 0),
    0xE0: ("SUBB", 2, 4, "indexed", 0),
    0xF0: ("SUBB", 3, 4, "extended", 0),
    
    # CMPB - Compare B
    0xC1: ("CMPB", 2, 2, "immediate", 0),
    0xD1: ("CMPB", 2, 3, "direct", 0),
    0xE1: ("CMPB", 2, 4, "indexed", 0),
    0xF1: ("CMPB", 3, 4, "extended", 0),
    
    # SBCB - Subtract with Carry B
    0xC2: ("SBCB", 2, 2, "immediate", 0),
    0xD2: ("SBCB", 2, 3, "direct", 0),
    0xE2: ("SBCB", 2, 4, "indexed", 0),
    0xF2: ("SBCB", 3, 4, "extended", 0),
    
    # ADDD - Add D (16-bit)
    0xC3: ("ADDD", 3, 4, "immediate16", 0),
    0xD3: ("ADDD", 2, 5, "direct", 0),
    0xE3: ("ADDD", 2, 6, "indexed", 0),
    0xF3: ("ADDD", 3, 6, "extended", 0),
    
    # ANDB - AND B
    0xC4: ("ANDB", 2, 2, "immediate", 0),
    0xD4: ("ANDB", 2, 3, "direct", 0),
    0xE4: ("ANDB", 2, 4, "indexed", 0),
    0xF4: ("ANDB", 3, 4, "extended", 0),
    
    # BITB - Bit Test B
    0xC5: ("BITB", 2, 2, "immediate", 0),
    0xD5: ("BITB", 2, 3, "direct", 0),
    0xE5: ("BITB", 2, 4, "indexed", 0),
    0xF5: ("BITB", 3, 4, "extended", 0),
    
    # LDAB - Load B
    0xC6: ("LDAB", 2, 2, "immediate", 0),
    0xD6: ("LDAB", 2, 3, "direct", 0),
    0xE6: ("LDAB", 2, 4, "indexed", 0),
    0xF6: ("LDAB", 3, 4, "extended", 0),
    
    # STAB - Store B (no immediate)
    0xD7: ("STAB", 2, 3, "direct", 0),
    0xE7: ("STAB", 2, 4, "indexed", 0),
    0xF7: ("STAB", 3, 4, "extended", 0),
    
    # EORB - Exclusive OR B
    0xC8: ("EORB", 2, 2, "immediate", 0),
    0xD8: ("EORB", 2, 3, "direct", 0),
    0xE8: ("EORB", 2, 4, "indexed", 0),
    0xF8: ("EORB", 3, 4, "extended", 0),
    
    # ADCB - Add with Carry B
    0xC9: ("ADCB", 2, 2, "immediate", 0),
    0xD9: ("ADCB", 2, 3, "direct", 0),
    0xE9: ("ADCB", 2, 4, "indexed", 0),
    0xF9: ("ADCB", 3, 4, "extended", 0),
    
    # ORAB - OR B
    0xCA: ("ORAB", 2, 2, "immediate", 0),
    0xDA: ("ORAB", 2, 3, "direct", 0),
    0xEA: ("ORAB", 2, 4, "indexed", 0),
    0xFA: ("ORAB", 3, 4, "extended", 0),
    
    # ADDB - Add B
    0xCB: ("ADDB", 2, 2, "immediate", 0),
    0xDB: ("ADDB", 2, 3, "direct", 0),
    0xEB: ("ADDB", 2, 4, "indexed", 0),
    0xFB: ("ADDB", 3, 4, "extended", 0),
    
    # LDD - Load D (16-bit)
    0xCC: ("LDD", 3, 3, "immediate16", 0),
    0xDC: ("LDD", 2, 4, "direct", 0),
    0xEC: ("LDD", 2, 5, "indexed", 0),
    0xFC: ("LDD", 3, 5, "extended", 0),
    
    # STD - Store D (no immediate)
    0xDD: ("STD", 2, 4, "direct", 0),
    0xED: ("STD", 2, 5, "indexed", 0),
    0xFD: ("STD", 3, 5, "extended", 0),
    
    # LDX - Load X
    0xCE: ("LDX", 3, 3, "immediate16", 0),
    0xDE: ("LDX", 2, 4, "direct", 0),
    0xEE: ("LDX", 2, 5, "indexed", 0),
    0xFE: ("LDX", 3, 5, "extended", 0),
    
    # STX - Store X (no immediate)
    0xDF: ("STX", 2, 4, "direct", 0),
    0xEF: ("STX", 2, 5, "indexed", 0),
    0xFF: ("STX", 3, 5, "extended", 0),
    
    # Bit manipulation - CRITICAL for ISR code
    0x14: ("BSET", 3, 6, "bset_direct", 0),
    0x1C: ("BSET", 3, 7, "indexed", 0),  # Special handling needed
    0x15: ("BCLR", 3, 6, "bset_direct", 0),
    0x1D: ("BCLR", 3, 7, "indexed", 0),
    0x12: ("BRSET", 4, 6, "brset_direct", PCR),
    0x1E: ("BRSET", 4, 7, "indexed", PCR),
    0x13: ("BRCLR", 4, 6, "brset_direct", PCR),
    0x1F: ("BRCLR", 4, 7, "indexed", PCR),
    
    # Jump/Call
    0x6E: ("JMP", 2, 3, "indexed", 0),
    0x7E: ("JMP", 3, 3, "extended", 0),
    
    # Memory ops (indexed)
    0x60: ("NEG", 2, 6, "indexed", 0),
    0x63: ("COM", 2, 6, "indexed", 0),
    0x64: ("LSR", 2, 6, "indexed", 0),
    0x66: ("ROR", 2, 6, "indexed", 0),
    0x67: ("ASR", 2, 6, "indexed", 0),
    0x68: ("ASL", 2, 6, "indexed", 0),
    0x69: ("ROL", 2, 6, "indexed", 0),
    0x6A: ("DEC", 2, 6, "indexed", 0),
    0x6C: ("INC", 2, 6, "indexed", 0),
    0x6D: ("TST", 2, 6, "indexed", 0),
    0x6F: ("CLR", 2, 6, "indexed", 0),
    
    # Memory ops (extended)
    0x70: ("NEG", 3, 6, "extended", 0),
    0x73: ("COM", 3, 6, "extended", 0),
    0x74: ("LSR", 3, 6, "extended", 0),
    0x76: ("ROR", 3, 6, "extended", 0),
    0x77: ("ASR", 3, 6, "extended", 0),
    0x78: ("ASL", 3, 6, "extended", 0),
    0x79: ("ROL", 3, 6, "extended", 0),
    0x7A: ("DEC", 3, 6, "extended", 0),
    0x7C: ("INC", 3, 6, "extended", 0),
    0x7D: ("TST", 3, 6, "extended", 0),
    0x7F: ("CLR", 3, 6, "extended", 0),
}

# Prebyte tables
PREBYTE_1A = {
    0x83: ("CPD", 4, 5, "immediate16", 0),
    0x93: ("CPD", 3, 6, "direct", 0),
    0xA3: ("CPD", 3, 7, "indexed", 0),
    0xB3: ("CPD", 4, 7, "extended", 0),
    0xEE: ("LDY", 3, 6, "indexed", 0),
    0xEF: ("STY", 3, 6, "indexed", 0),
}

PREBYTE_18 = {
    0x08: ("INY", 2, 4, "inherent", 0),
    0x09: ("DEY", 2, 4, "inherent", 0),
    0x30: ("TSY", 2, 4, "inherent", 0),
    0x35: ("TYS", 2, 4, "inherent", 0),
    0x3A: ("ABY", 2, 4, "inherent", 0),
    0x3C: ("PSHY", 2, 5, "inherent", 0),
    0x38: ("PULY", 2, 6, "inherent", 0),
    0x8C: ("CPY", 4, 5, "immediate16", 0),
    0x8F: ("XGDY", 2, 3, "inherent", 0),
    0x9C: ("CPY", 3, 6, "direct", 0),
    0xAC: ("CPY", 3, 7, "indexed", 0),
    0xBC: ("CPY", 4, 7, "extended", 0),
    0xCE: ("LDY", 4, 4, "immediate16", 0),
    0xDE: ("LDY", 3, 5, "direct", 0),
    0xEE: ("LDY", 3, 6, "indexed_y", 0),
    0xFE: ("LDY", 4, 6, "extended", 0),
    0xDF: ("STY", 3, 5, "direct", 0),
    0xEF: ("STY", 3, 6, "indexed_y", 0),
    0xFF: ("STY", 4, 6, "extended", 0),
}

PREBYTE_CD = {
    0xA3: ("CPD", 3, 7, "indexed_y", 0),
    0xAC: ("CPX", 3, 7, "indexed_y", 0),
    0xEE: ("LDX", 3, 6, "indexed_y", 0),
    0xEF: ("STX", 3, 6, "indexed_y", 0),
}


# ============================================================================
# DISASSEMBLY FUNCTIONS
# ============================================================================

def format_operand(addr_mode, operands, current_addr, instr_len, flags):
    """Format operand using format table (udis-inspired)"""
    
    if addr_mode == "inherent":
        return ""
    
    if addr_mode == "relative" and (flags & PCR):
        # Calculate branch target
        if len(operands) < 1:
            return "???"
        rel = operands[0] if operands[0] < 128 else operands[0] - 256
        target = (current_addr + instr_len + rel) & 0xFFFF
        return f"${target:04X}"
    
    if addr_mode == "immediate":
        if len(operands) >= 1:
            return f"#${operands[0]:02X}"
        return "#$??"
    
    if addr_mode == "immediate16":
        if len(operands) >= 2:
            val = (operands[0] << 8) | operands[1]
            return f"#${val:04X}"
        return "#$????"
    
    if addr_mode == "direct":
        if len(operands) >= 1:
            return f"${operands[0]:02X}"
        return "$??"
    
    if addr_mode == "extended":
        if len(operands) >= 2:
            val = (operands[0] << 8) | operands[1]
            return f"${val:04X}"
        return "$????"
    
    if addr_mode == "indexed":
        if len(operands) >= 1:
            return f"${operands[0]:02X},X"
        return "$??,X"
    
    if addr_mode == "indexed_y":
        if len(operands) >= 1:
            return f"${operands[0]:02X},Y"
        return "$??,Y"
    
    if addr_mode == "bset_direct":
        if len(operands) >= 2:
            return f"${operands[0]:02X}, #${operands[1]:02X}"
        return "$??, #$??"
    
    if addr_mode == "brset_direct":
        if len(operands) >= 3:
            rel = operands[2] if operands[2] < 128 else operands[2] - 256
            target = (current_addr + instr_len + rel) & 0xFFFF
            return f"${operands[0]:02X}, #${operands[1]:02X}, ${target:04X}"
        return "$??, #$??, $????"
    
    return ""


def disassemble_instruction(data, offset, runtime_addr):
    """Disassemble single instruction
    
    Returns: (dict with instruction info, instruction_size)
    """
    if offset >= len(data):
        return None, 1
    
    opcode = data[offset]
    prebyte = None
    opcode_table = INSTRUCTIONS
    
    # Check for prebyte
    if opcode in (0x18, 0x1A, 0xCD):
        prebyte = opcode
        if offset + 1 >= len(data):
            return None, 1
        opcode = data[offset + 1]
        
        if prebyte == 0x1A:
            opcode_table = PREBYTE_1A
        elif prebyte == 0x18:
            opcode_table = PREBYTE_18
        else:
            opcode_table = PREBYTE_CD
    
    # Look up instruction
    if opcode not in opcode_table:
        # Unknown opcode
        if prebyte:
            hex_bytes = f"{prebyte:02X} {opcode:02X}"
            return {
                "addr": runtime_addr,
                "file_offset": offset - 1,
                "hex": hex_bytes,
                "mnemonic": "DB",
                "operand": f"${prebyte:02X}, ${opcode:02X}",
                "comment": "Unknown prebyte"
            }, 2
        else:
            return {
                "addr": runtime_addr,
                "file_offset": offset,
                "hex": f"{opcode:02X}",
                "mnemonic": "DB",
                "operand": f"${opcode:02X}",
                "comment": "Unknown"
            }, 1
    
    mnemonic, total_size, cycles, addr_mode, flags = opcode_table[opcode]
    
    # Calculate operand size
    if prebyte:
        operand_size = total_size - 2
        start_file = offset - 1
    else:
        operand_size = total_size - 1
        start_file = offset
    
    # Read operands
    operands = []
    if prebyte:
        op_start = offset + 1
    else:
        op_start = offset + 1
    
    if op_start + operand_size > len(data):
        return None, 1
    
    for i in range(operand_size):
        operands.append(data[op_start + i])
    
    # Build hex string
    if prebyte:
        all_bytes = [prebyte, opcode] + operands
    else:
        all_bytes = [opcode] + operands
    hex_str = " ".join(f"{b:02X}" for b in all_bytes)
    
    # Format operand
    operand = format_operand(addr_mode, operands, runtime_addr, total_size, flags)
    
    # Add comment for branches
    comment = ""
    if flags & PCR and len(operands) >= 1:
        rel = operands[-1] if operands[-1] < 128 else operands[-1] - 256
        comment = f"offset={rel:+d}"
    
    return {
        "addr": runtime_addr,
        "file_offset": start_file,
        "hex": hex_str,
        "mnemonic": mnemonic,
        "operand": operand,
        "comment": comment,
        "cycles": cycles
    }, total_size


def disassemble_range(data, file_offset, length, name=""):
    """Disassemble a range of bytes"""
    
    results = []
    offset = file_offset
    end = min(file_offset + length, len(data))
    
    while offset < end:
        # Calculate runtime address
        if offset >= VY_CODE_OFFSET:
            runtime_addr = (offset - VY_CODE_OFFSET) & 0xFFFF
        else:
            runtime_addr = offset
        
        instr, size = disassemble_instruction(data, offset, runtime_addr)
        if instr:
            instr["name"] = name
            results.append(instr)
        offset += size
    
    return results


def parse_address_arg(arg):
    """Parse address:length argument"""
    parts = arg.split(":")
    addr = int(parts[0], 0)
    length = int(parts[1], 0) if len(parts) > 1 else 0x20
    return addr, length


def load_batch_file(path):
    """Load batch address file (JSON)"""
    with open(path, 'r') as f:
        data = json.load(f)
    
    addresses = []
    for item in data.get("addresses", []):
        addr = int(item["file_offset"], 0)
        length = int(item.get("length", "0x20"), 0)
        name = item.get("name", f"Region_{addr:05X}")
        addresses.append((addr, length, name))
    
    return addresses


def output_asm(results, file=None):
    """Output as assembly listing"""
    lines = []
    current_name = None
    
    for instr in results:
        if instr["name"] != current_name:
            current_name = instr["name"]
            if lines:
                lines.append("")
            lines.append(f"; === {current_name} ===")
        
        comment = f"  ; {instr['comment']}" if instr.get("comment") else ""
        line = f"{instr['addr']:04X}  {instr['hex']:14s} {instr['mnemonic']:8s} {instr['operand']:15s}{comment}"
        lines.append(line)
    
    output = "\n".join(lines)
    if file:
        Path(file).write_text(output, encoding='utf-8')
        print(f"[OK] Saved ASM to {file}")
    else:
        print(output)
    return output


def output_csv(results, file):
    """Output as CSV for analysis"""
    with open(file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "name", "file_offset", "addr", "hex", "mnemonic", "operand", "cycles", "comment"
        ])
        writer.writeheader()
        for instr in results:
            writer.writerow({
                "name": instr.get("name", ""),
                "file_offset": f"0x{instr['file_offset']:05X}",
                "addr": f"0x{instr['addr']:04X}",
                "hex": instr["hex"],
                "mnemonic": instr["mnemonic"],
                "operand": instr["operand"],
                "cycles": instr.get("cycles", ""),
                "comment": instr.get("comment", "")
            })
    print(f"[OK] Saved CSV to {file}")


def output_json(results, file):
    """Output as JSON for automation"""
    with open(file, 'w', encoding='utf-8') as f:
        json.dump({"instructions": results}, f, indent=2)
    print(f"[OK] Saved JSON to {file}")


def main():
    parser = argparse.ArgumentParser(
        description="HC11 Batch Disassembler - Multiple address ranges in one run"
    )
    parser.add_argument("binary", help="Binary file to disassemble")
    parser.add_argument("--addr", "-a", action="append", 
                        help="Address:length pair (e.g., 0x14839:0x20). Can specify multiple.")
    parser.add_argument("--batch", "-b", help="JSON file with address list")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    parser.add_argument("--format", "-f", choices=["asm", "csv", "json"], default="asm",
                        help="Output format (default: asm)")
    
    args = parser.parse_args()
    
    # Load binary
    bin_path = Path(args.binary)
    if not bin_path.exists():
        print(f"Error: Binary file not found: {bin_path}")
        sys.exit(1)
    
    data = bin_path.read_bytes()
    print(f"Loaded {len(data)} bytes from {bin_path.name}")
    
    # Collect addresses
    addresses = []
    
    if args.batch:
        addresses.extend(load_batch_file(args.batch))
    
    if args.addr:
        for i, addr_arg in enumerate(args.addr):
            addr, length = parse_address_arg(addr_arg)
            addresses.append((addr, length, f"Range_{i+1}"))
    
    if not addresses:
        print("Error: No addresses specified. Use --addr or --batch")
        print("\nExamples:")
        print("  python hc11_disassembler_batch.py binary.bin --addr 0x14839:0x20")
        print("  python hc11_disassembler_batch.py binary.bin --addr 0x14839:0x20 --addr 0x1FD84:0x30")
        print("  python hc11_disassembler_batch.py binary.bin --batch addresses.json")
        sys.exit(1)
    
    # Disassemble all ranges
    all_results = []
    for addr, length, name in addresses:
        print(f"Disassembling: {name} @ 0x{addr:05X} ({length} bytes)")
        results = disassemble_range(data, addr, length, name)
        all_results.extend(results)
    
    print(f"\nTotal: {len(all_results)} instructions from {len(addresses)} regions\n")
    
    # Output
    if args.format == "asm":
        output_asm(all_results, args.output)
    elif args.format == "csv":
        if not args.output:
            args.output = bin_path.stem + "_batch.csv"
        output_csv(all_results, args.output)
    elif args.format == "json":
        if not args.output:
            args.output = bin_path.stem + "_batch.json"
        output_json(all_results, args.output)


if __name__ == "__main__":
    main()
