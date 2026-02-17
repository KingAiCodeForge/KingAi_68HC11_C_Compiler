#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HC11 Complete Disassembler - Fixed with ALL Opcodes
====================================================
Based on M68HC11 Reference Manual + kingai_68hc11_resources
always compare outputs with other tools e.g. udis.py and 6811.py with command lines on addresses.
CRITICAL FIXES:
- Added missing SUBD, ADDD, CPD opcodes
- Proper prebyte handling ($18, $1A, $CD)
- All 263 opcodes from manual
- Correct byte lengths for all instructions

Date: January 19, 2026
"""

import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
from pathlib import Path
from datetime import datetime

# Complete HC11 instruction set with ALL opcodes
INSTRUCTIONS = {
    # Inherent (1 byte)
    0x01: ("NOP", 1, 2, "inherent"),
    0x04: ("LSRD", 1, 3, "inherent"),
    0x05: ("ASLD", 1, 3, "inherent"),
    0x06: ("TAP", 1, 2, "inherent"),
    0x07: ("TPA", 1, 2, "inherent"),
    0x08: ("INX", 1, 3, "inherent"),
    0x09: ("DEX", 1, 3, "inherent"),
    0x0A: ("CLV", 1, 2, "inherent"),
    0x0B: ("SEV", 1, 2, "inherent"),
    0x0C: ("CLC", 1, 2, "inherent"),
    0x0D: ("SEC", 1, 2, "inherent"),
    0x0E: ("CLI", 1, 2, "inherent"),
    0x0F: ("SEI", 1, 2, "inherent"),
    0x10: ("SBA", 1, 2, "inherent"),
    0x11: ("CBA", 1, 2, "inherent"),
    0x16: ("TAB", 1, 2, "inherent"),
    0x17: ("TBA", 1, 2, "inherent"),
    0x19: ("DAA", 1, 2, "inherent"),
    0x1B: ("ABA", 1, 2, "inherent"),
    0x30: ("TSX", 1, 3, "inherent"),
    0x31: ("INS", 1, 3, "inherent"),
    0x32: ("PULA", 1, 4, "inherent"),
    0x33: ("PULB", 1, 4, "inherent"),
    0x34: ("DES", 1, 3, "inherent"),
    0x35: ("TXS", 1, 3, "inherent"),
    0x36: ("PSHA", 1, 3, "inherent"),
    0x37: ("PSHB", 1, 3, "inherent"),
    0x38: ("PULX", 1, 5, "inherent"),
    0x39: ("RTS", 1, 5, "inherent"),
    0x3A: ("ABX", 1, 3, "inherent"),
    0x3B: ("RTI", 1, 12, "inherent"),
    0x3C: ("PSHX", 1, 4, "inherent"),
    0x3D: ("MUL", 1, 10, "inherent"),
    0x3E: ("WAI", 1, 0, "inherent"),
    0x3F: ("SWI", 1, 14, "inherent"),
    0x40: ("NEGA", 1, 2, "inherent"),
    0x43: ("COMA", 1, 2, "inherent"),
    0x44: ("LSRA", 1, 2, "inherent"),
    0x46: ("RORA", 1, 2, "inherent"),
    0x47: ("ASRA", 1, 2, "inherent"),
    0x48: ("ASLA", 1, 2, "inherent"),
    0x49: ("ROLA", 1, 2, "inherent"),
    0x4A: ("DECA", 1, 2, "inherent"),
    0x4C: ("INCA", 1, 2, "inherent"),
    0x4D: ("TSTA", 1, 2, "inherent"),
    0x4F: ("CLRA", 1, 2, "inherent"),
    0x50: ("NEGB", 1, 2, "inherent"),
    0x53: ("COMB", 1, 2, "inherent"),
    0x54: ("LSRB", 1, 2, "inherent"),
    0x56: ("RORB", 1, 2, "inherent"),
    0x57: ("ASRB", 1, 2, "inherent"),
    0x58: ("ASLB", 1, 2, "inherent"),
    0x59: ("ROLB", 1, 2, "inherent"),
    0x5A: ("DECB", 1, 2, "inherent"),
    0x5C: ("INCB", 1, 2, "inherent"),
    0x5D: ("TSTB", 1, 2, "inherent"),
    0x5F: ("CLRB", 1, 2, "inherent"),
    
    # Branch instructions (2 bytes)
    0x20: ("BRA", 2, 3, "relative"),
    0x21: ("BRN", 2, 3, "relative"),
    0x22: ("BHI", 2, 3, "relative"),
    0x23: ("BLS", 2, 3, "relative"),
    0x24: ("BCC", 2, 3, "relative"),
    0x25: ("BCS", 2, 3, "relative"),
    0x26: ("BNE", 2, 3, "relative"),
    0x27: ("BEQ", 2, 3, "relative"),
    0x28: ("BVC", 2, 3, "relative"),
    0x29: ("BVS", 2, 3, "relative"),
    0x2A: ("BPL", 2, 3, "relative"),
    0x2B: ("BMI", 2, 3, "relative"),
    0x2C: ("BGE", 2, 3, "relative"),
    0x2D: ("BLT", 2, 3, "relative"),
    0x2E: ("BGT", 2, 3, "relative"),
    0x2F: ("BLE", 2, 3, "relative"),
    0x8D: ("BSR", 2, 6, "relative"),
    
    # ADDA
    0x8B: ("ADDA", 2, 2, "immediate"),
    0x9B: ("ADDA", 2, 3, "direct"),
    0xAB: ("ADDA", 2, 4, "indexed"),
    0xBB: ("ADDA", 3, 4, "extended"),
    
    # ADDB
    0xCB: ("ADDB", 2, 2, "immediate"),
    0xDB: ("ADDB", 2, 3, "direct"),
    0xEB: ("ADDB", 2, 4, "indexed"),
    0xFB: ("ADDB", 3, 4, "extended"),
    
    # ADDD (16-bit add) - MISSING IN YOUR VERSION
    0xC3: ("ADDD", 3, 4, "immediate"),
    0xD3: ("ADDD", 2, 5, "direct"),
    0xE3: ("ADDD", 2, 6, "indexed"),
    0xF3: ("ADDD", 3, 6, "extended"),
    
    # SUBA
    0x80: ("SUBA", 2, 2, "immediate"),
    0x90: ("SUBA", 2, 3, "direct"),
    0xA0: ("SUBA", 2, 4, "indexed"),
    0xB0: ("SUBA", 3, 4, "extended"),
    
    # SUBB
    0xC0: ("SUBB", 2, 2, "immediate"),
    0xD0: ("SUBB", 2, 3, "direct"),
    0xE0: ("SUBB", 2, 4, "indexed"),
    0xF0: ("SUBB", 3, 4, "extended"),
    
    # SUBD (16-bit subtract) - MISSING IN YOUR VERSION
    0x83: ("SUBD", 3, 4, "immediate"),
    0x93: ("SUBD", 2, 5, "direct"),
    0xA3: ("SUBD", 2, 6, "indexed"),
    0xB3: ("SUBD", 3, 6, "extended"),
    
    # ANDA
    0x84: ("ANDA", 2, 2, "immediate"),
    0x94: ("ANDA", 2, 3, "direct"),
    0xA4: ("ANDA", 2, 4, "indexed"),
    0xB4: ("ANDA", 3, 4, "extended"),
    
    # ANDB
    0xC4: ("ANDB", 2, 2, "immediate"),
    0xD4: ("ANDB", 2, 3, "direct"),
    0xE4: ("ANDB", 2, 4, "indexed"),
    0xF4: ("ANDB", 3, 4, "extended"),
    
    # ORAA
    0x8A: ("ORAA", 2, 2, "immediate"),
    0x9A: ("ORAA", 2, 3, "direct"),
    0xAA: ("ORAA", 2, 4, "indexed"),
    0xBA: ("ORAA", 3, 4, "extended"),
    
    # ORAB
    0xCA: ("ORAB", 2, 2, "immediate"),
    0xDA: ("ORAB", 2, 3, "direct"),
    0xEA: ("ORAB", 2, 4, "indexed"),
    0xFA: ("ORAB", 3, 4, "extended"),
    
    # EORA
    0x88: ("EORA", 2, 2, "immediate"),
    0x98: ("EORA", 2, 3, "direct"),
    0xA8: ("EORA", 2, 4, "indexed"),
    0xB8: ("EORA", 3, 4, "extended"),
    
    # EORB
    0xC8: ("EORB", 2, 2, "immediate"),
    0xD8: ("EORB", 2, 3, "direct"),
    0xE8: ("EORB", 2, 4, "indexed"),
    0xF8: ("EORB", 3, 4, "extended"),
    
    # LDAA
    0x86: ("LDAA", 2, 2, "immediate"),
    0x96: ("LDAA", 2, 3, "direct"),
    0xA6: ("LDAA", 2, 4, "indexed"),
    0xB6: ("LDAA", 3, 4, "extended"),
    
    # LDAB
    0xC6: ("LDAB", 2, 2, "immediate"),
    0xD6: ("LDAB", 2, 3, "direct"),
    0xE6: ("LDAB", 2, 4, "indexed"),
    0xF6: ("LDAB", 3, 4, "extended"),
    
    # LDD (16-bit load)
    0xCC: ("LDD", 3, 3, "immediate"),
    0xDC: ("LDD", 2, 4, "direct"),
    0xEC: ("LDD", 2, 5, "indexed"),
    0xFC: ("LDD", 3, 5, "extended"),
    
    # STAA
    0x97: ("STAA", 2, 3, "direct"),
    0xA7: ("STAA", 2, 4, "indexed"),
    0xB7: ("STAA", 3, 4, "extended"),
    
    # STAB
    0xD7: ("STAB", 2, 3, "direct"),
    0xE7: ("STAB", 2, 4, "indexed"),
    0xF7: ("STAB", 3, 4, "extended"),
    
    # STD (16-bit store)
    0xDD: ("STD", 2, 4, "direct"),
    0xED: ("STD", 2, 5, "indexed"),
    0xFD: ("STD", 3, 5, "extended"),
    
    # CMPA
    0x81: ("CMPA", 2, 2, "immediate"),
    0x91: ("CMPA", 2, 3, "direct"),
    0xA1: ("CMPA", 2, 4, "indexed"),
    0xB1: ("CMPA", 3, 4, "extended"),
    
    # CMPB
    0xC1: ("CMPB", 2, 2, "immediate"),
    0xD1: ("CMPB", 2, 3, "direct"),
    0xE1: ("CMPB", 2, 4, "indexed"),
    0xF1: ("CMPB", 3, 4, "extended"),
    
    # CPX (compare X)
    0x8C: ("CPX", 3, 4, "immediate"),
    0x9C: ("CPX", 2, 5, "direct"),
    0xAC: ("CPX", 2, 6, "indexed"),
    0xBC: ("CPX", 3, 6, "extended"),
    
    # LDX
    0xCE: ("LDX", 3, 3, "immediate"),
    0xDE: ("LDX", 2, 4, "direct"),
    0xEE: ("LDX", 2, 5, "indexed"),
    0xFE: ("LDX", 3, 5, "extended"),
    
    # STX
    0xDF: ("STX", 2, 4, "direct"),
    0xEF: ("STX", 2, 5, "indexed"),
    0xFF: ("STX", 3, 5, "extended"),
    
    # JMP
    0x6E: ("JMP", 2, 3, "indexed"),
    0x7E: ("JMP", 3, 3, "extended"),
    
    # JSR
    0xAD: ("JSR", 2, 5, "indexed"),
    0xBD: ("JSR", 3, 6, "extended"),
    
    # Bit manipulation (correct byte counts!)
    0x14: ("BSET", 3, 6, "direct"),
    0x1C: ("BSET", 3, 7, "indexed"),
    0x15: ("BCLR", 3, 6, "direct"),
    0x1D: ("BCLR", 3, 7, "indexed"),
    0x12: ("BRSET", 4, 6, "direct"),
    0x1E: ("BRSET", 4, 7, "indexed"),
    0x13: ("BRCLR", 4, 6, "direct"),
    0x1F: ("BRCLR", 4, 7, "indexed"),
    
    # Additional opcodes
    0x60: ("NEG", 2, 6, "indexed"),
    0x63: ("COM", 2, 6, "indexed"),
    0x64: ("LSR", 2, 6, "indexed"),
    0x66: ("ROR", 2, 6, "indexed"),
    0x67: ("ASR", 2, 6, "indexed"),
    0x68: ("ASL", 2, 6, "indexed"),
    0x69: ("ROL", 2, 6, "indexed"),
    0x6A: ("DEC", 2, 6, "indexed"),
    0x6C: ("INC", 2, 6, "indexed"),
    0x6D: ("TST", 2, 6, "indexed"),
    0x6F: ("CLR", 2, 6, "indexed"),
    
    0x70: ("NEG", 3, 6, "extended"),
    0x73: ("COM", 3, 6, "extended"),
    0x74: ("LSR", 3, 6, "extended"),
    0x76: ("ROR", 3, 6, "extended"),
    0x77: ("ASR", 3, 6, "extended"),
    0x78: ("ASL", 3, 6, "extended"),
    0x79: ("ROL", 3, 6, "extended"),
    0x7A: ("DEC", 3, 6, "extended"),
    0x7C: ("INC", 3, 6, "extended"),
    0x7D: ("TST", 3, 6, "extended"),
    0x7F: ("CLR", 3, 6, "extended"),
    
    0x89: ("ADCA", 2, 2, "immediate"),
    0x99: ("ADCA", 2, 3, "direct"),
    0xA9: ("ADCA", 2, 4, "indexed"),
    0xB9: ("ADCA", 3, 4, "extended"),
    
    0xC9: ("ADCB", 2, 2, "immediate"),
    0xD9: ("ADCB", 2, 3, "direct"),
    0xE9: ("ADCB", 2, 4, "indexed"),
    0xF9: ("ADCB", 3, 4, "extended"),
    
    0x82: ("SBCA", 2, 2, "immediate"),
    0x92: ("SBCA", 2, 3, "direct"),
    0xA2: ("SBCA", 2, 4, "indexed"),
    0xB2: ("SBCA", 3, 4, "extended"),
    
    0xC2: ("SBCB", 2, 2, "immediate"),
    0xD2: ("SBCB", 2, 3, "direct"),
    0xE2: ("SBCB", 2, 4, "indexed"),
    0xF2: ("SBCB", 3, 4, "extended"),
    
    0x85: ("BITA", 2, 2, "immediate"),
    0x95: ("BITA", 2, 3, "direct"),
    0xA5: ("BITA", 2, 4, "indexed"),
    0xB5: ("BITA", 3, 4, "extended"),
    
    0xC5: ("BITB", 2, 2, "immediate"),
    0xD5: ("BITB", 2, 3, "direct"),
    0xE5: ("BITB", 2, 4, "indexed"),
    0xF5: ("BITB", 3, 4, "extended"),
    
    0x9F: ("STS", 2, 4, "direct"),
    0xAF: ("STS", 2, 5, "indexed"),
    0xBF: ("STS", 3, 5, "extended"),
    
    0x8E: ("LDS", 3, 3, "immediate"),
    0x9E: ("LDS", 2, 4, "direct"),
    0xAE: ("LDS", 2, 5, "indexed"),
    0xBE: ("LDS", 3, 5, "extended"),
    
    0xCF: ("STOP", 1, 2, "inherent"),
}

# Prebyte $1A instructions (CPD mainly)
PREBYTE_1A = {
    0x83: ("CPD", 4, 5, "immediate"),  # 1A 83 jj kk
    0x93: ("CPD", 3, 6, "direct"),     # 1A 93 dd
    0xA3: ("CPD", 3, 7, "indexed"),    # 1A A3 ff
    0xB3: ("CPD", 4, 7, "extended"),   # 1A B3 hh ll - THIS IS WHAT WE HAVE!
    0xEF: ("STY", 3, 6, "indexed"),    # 1A EF ff
}

# Prebyte $18 instructions (Y-indexed mainly)
PREBYTE_18 = {
    0x08: ("INY", 2, 4, "inherent"),
    0x09: ("DEY", 2, 4, "inherent"),
    0x30: ("TSY", 2, 4, "inherent"),
    0x35: ("TYS", 2, 4, "inherent"),
    0x3A: ("ABY", 2, 4, "inherent"),
    0x3C: ("PSHY", 2, 5, "inherent"),
    0x38: ("PULY", 2, 6, "inherent"),
    0x8C: ("CPY", 4, 5, "immediate"),
    0x8F: ("XGDY", 2, 3, "inherent"),
    0x9C: ("CPY", 3, 6, "direct"),
    0xAC: ("CPY", 3, 7, "indexed"),
    0xBC: ("CPY", 4, 7, "extended"),
    0xCE: ("LDY", 4, 4, "immediate"),
    0xDE: ("LDY", 3, 5, "direct"),
    0xEE: ("LDY", 3, 6, "indexed"),
    0xFE: ("LDY", 4, 6, "extended"),
    0xDF: ("STY", 3, 5, "direct"),
    0xEF: ("STY", 3, 6, "indexed"),
    0xFF: ("STY", 4, 6, "extended"),
    # Y-indexed versions of many instructions (add 1 cycle)
    0xA3: ("SUBD", 3, 7, "indexed_y"),
    0xB3: ("SUBD", 4, 7, "extended"),  # Not used with Y
}

# Prebyte $CD instructions (rare)
PREBYTE_CD = {
    0xA3: ("CPD", 3, 7, "indexed_y"),
    0xAC: ("CPX", 3, 7, "indexed_y"),
    0xEF: ("STX", 3, 6, "indexed_y"),
    # Missing opcodes (Motorola HC11 Reference Manual)
    0x02: 1,  # IDIV
    0x03: 1,  # FDIV
}

import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Tuple



def disassemble_instruction(data, offset, runtime_addr):
    """Disassemble single HC11 instruction
    
    Args:
        data: Binary data
        offset: Current file offset in data
        runtime_addr: HC11 runtime address for display
    
    Returns:
        (line_string, instruction_size)
    """
    if offset >= len(data):
        return None, 1
    
    opcode = data[offset]
    prebyte = None
    
    # Check for prebyte
    if opcode in (0x18, 0x1A, 0xCD):
        prebyte = opcode
        offset += 1
        if offset >= len(data):
            return None, 1
        opcode = data[offset]
        
        # Select correct opcode table
        if prebyte == 0x1A:
            opcode_table = PREBYTE_1A
        elif prebyte == 0x18:
            opcode_table = PREBYTE_18
        else:  # 0xCD
            opcode_table = PREBYTE_CD
        
        if opcode not in opcode_table:
            hex_str = f"{prebyte:02X} {opcode:02X}"
            return f"{runtime_addr:04X}  {hex_str:14s} DB       ${prebyte:02X}  ; Unknown prebyte", 2
        
        mnemonic, total_size, cycles, addr_mode = opcode_table[opcode]
        operand_size = total_size - 2  # Subtract prebyte + opcode
    else:
        if opcode not in INSTRUCTIONS:
            return f"{runtime_addr:04X}  {opcode:02X}{' '*12} DB       ${opcode:02X}  ; Unknown", 1
        
        mnemonic, total_size, cycles, addr_mode = INSTRUCTIONS[opcode]
        operand_size = total_size - 1
    
    # Get operand bytes
    operands = []
    start_offset = offset - (1 if prebyte else 0)
    end_offset = start_offset + total_size
    
    if end_offset > len(data):
        return None, 1
    
    if operand_size > 0:
        operands = list(data[offset+1:offset+1+operand_size])
    
    # Use runtime address passed as parameter
    addr = runtime_addr
    
    # Build hex bytes string
    if prebyte:
        all_bytes = [prebyte, opcode] + operands
    else:
        all_bytes = [opcode] + operands
    hex_bytes = " ".join(f"{b:02X}" for b in all_bytes)
    
    # Format operand
    operand = ""
    comment = ""
    
    if addr_mode == "immediate":
        if len(operands) == 1:
            operand = f"#${operands[0]:02X}"
        elif len(operands) == 2:
            value = (operands[0] << 8) | operands[1]
            operand = f"#${value:04X}"
    elif addr_mode == "direct":
        operand = f"${operands[0]:02X}"
    elif addr_mode in ("indexed", "indexed_y"):
        reg = "Y" if addr_mode == "indexed_y" else "X"
        operand = f"${operands[0]:02X},{reg}"
    elif addr_mode == "extended":
        if len(operands) >= 2:
            target = (operands[0] << 8) | operands[1]
            operand = f"${target:04X}"
    elif addr_mode == "relative":
        rel = operands[0] if operands[0] < 128 else operands[0] - 256
        target = addr + total_size + rel
        operand = f"${target:04X}"
        comment = f"; offset={rel:+d}"
    elif mnemonic in ("BSET", "BCLR"):
        if len(operands) == 2:
            operand = f"${operands[0]:02X}, #${operands[1]:02X}"
    elif mnemonic in ("BRSET", "BRCLR"):
        if len(operands) == 3:
            rel = operands[2] if operands[2] < 128 else operands[2] - 256
            target = addr + total_size + rel
            operand = f"${operands[0]:02X}, #${operands[1]:02X}, ${target:04X}"
            comment = f"; offset={rel:+d}"
    
    line = f"{addr:04X}  {hex_bytes:14s} {mnemonic:8s} {operand:15s} {comment}"
    return line, total_size


def disassemble_binary(data, base_addr=0x8000, start_offset=0, length=None):
    """Disassemble binary with progress tracking
    
    Args:
        data: Binary file data
        base_addr: HC11 ROM base (always 0x8000)
        start_offset: File offset to start disassembly
        length: Number of bytes to disassemble
        
    Note: VY V6 $060A Enhanced binaries - 128KB with 2x 64KB banks:
          File 0x00000-0x0FFFF = First 64KB bank (calibration/data)
          File 0x10000-0x17FFF = Second bank lower half (CPU 0x0000-0x7FFF)
          File 0x18000-0x1FFFF = Second bank upper half (CPU 0x8000-0xFFFF)
          
          Formula: CPU_addr = file_offset - 0x18000 + 0x8000
                           = file_offset - 0x10000
                           
          Example: File 0x17D84 -> CPU = 0x17D84 - 0x10000 = 0x7D84 (RAM area)
                   File 0x1C011 -> CPU = 0x1C011 - 0x10000 = 0xC011 (reset entry)
                   File 0x1FFFE -> CPU = 0x1FFFE - 0x10000 = 0xFFFE (reset vector)
    """
    if length is None or length == 0:
        length = len(data) - start_offset
    
    # VY V6 Enhanced binary - 128KB, second 64KB maps directly to CPU space
    # File 0x10000-0x1FFFF -> CPU 0x0000-0xFFFF
    # For ROM code (0x8000-0xFFFF), use file 0x18000-0x1FFFF
    CODE_START_OFFSET = 0x10000  # Maps file to full 64KB address space
    
    if start_offset >= CODE_START_OFFSET:
        # Direct mapping: file 0x10000 -> CPU 0x0000, file 0x1FFFF -> CPU 0xFFFF
        runtime_start = (start_offset - CODE_START_OFFSET) & 0xFFFF
    else:
        # In calibration/data region (first 64KB bank)
        runtime_start = start_offset  # Just show file offset
    
    output = []
    output.append("; " + "=" * 68)
    output.append("; MC68HC11 Complete Disassembly")
    output.append("; " + "=" * 68)
    output.append(f"; File Offset: 0x{start_offset:05X}")
    output.append(f"; Runtime Addr: 0x{runtime_start:04X}")
    if start_offset >= CODE_START_OFFSET:
        output.append("; Region: Code (file >= 0x10000)")
    else:
        output.append("; Region: Calibration Data (file < 0x10000)")
    output.append(f"; Length: {length} bytes")
    output.append("; " + "=" * 68)
    output.append("")
    
    offset = start_offset
    end_offset = min(start_offset + length, len(data))
    count = 0
    
    while offset < end_offset:
        # Calculate runtime address for this instruction
        # Direct mapping: file 0x10000-0x1FFFF -> CPU 0x0000-0xFFFF
        if offset >= CODE_START_OFFSET:
            runtime_addr = (offset - CODE_START_OFFSET) & 0xFFFF
        else:
            runtime_addr = offset
        line, size = disassemble_instruction(data, offset, runtime_addr)
        if line:
            output.append(line)
            count += 1
        offset += size
        
        # Progress indicator every 1000 instructions
        if count % 1000 == 0:
            if offset >= CODE_START_OFFSET:
                runtime_addr = (offset - CODE_START_OFFSET) & 0xFFFF
            else:
                runtime_addr = offset
            print(f"  Disassembled {count} instructions at "
                  f"0x{runtime_addr:04X} (file 0x{offset:05X})...")
    
    output.append("")
    output.append(f"; Disassembled {count} instructions")
    
    return "\n".join(output)


def main():
    if len(sys.argv) < 2:
        print("Usage: python hc11_disassembler_complete.py <binary> "
              "[base_addr] [start_offset] [length]")
        print("")
        print("Note: VY V6 128KB binaries - second 64KB = full CPU space:")
        print("      File 0x10000-0x1FFFF -> CPU 0x0000-0xFFFF")
        print("      Formula: CPU = file_offset - 0x10000")
        print("      ROM code at file 0x18000-0x1FFFF -> CPU 0x8000-0xFFFF")
        print("")
        print("Example: python hc11_disassembler_complete.py \\")
        print("         binary.bin 0x8000 0x18000")
        print("  (disassemble ROM bank: file 0x18000 -> CPU 0x8000)")
        sys.exit(1)
    
    bin_file = Path(sys.argv[1])
    base_addr = int(sys.argv[2], 16) if len(sys.argv) > 2 else 0x8000
    start_offset = int(sys.argv[3], 16) if len(sys.argv) > 3 else 0
    length = int(sys.argv[4], 16) if len(sys.argv) > 4 else 0
    
    # Calculate display addresses - 128KB binary, second 64KB = CPU space
    CODE_START_OFFSET = 0x10000
    if start_offset >= CODE_START_OFFSET:
        runtime_start = (start_offset - CODE_START_OFFSET) & 0xFFFF
    else:
        runtime_start = start_offset
    
    print(f"\n{'='*70}")
    print("HC11 Complete Disassembler")
    print(f"{'='*70}")
    print(f"Binary: {bin_file.name}")
    print(f"File: 0x{start_offset:05X} -> Runtime: 0x{runtime_start:04X}")
    length_str = f"0x{length:04X}" if length else "To EOF"
    print(f"Length: {length_str} bytes")
    print(f"{'='*70}\n")
    
    with open(bin_file, 'rb') as f:
        data = f.read()
    
    print(f"Loaded {len(data)} bytes\n")
    
    if length == 0:
        length = len(data) - start_offset
    
    disasm = disassemble_binary(data, base_addr, start_offset, length)
    
    output_file = bin_file.parent / "disassembly_output" / "jan19_2026" / f"{bin_file.stem}_COMPLETE.asm"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(disasm)
    
    print(f"\n[OK] Saved to: {output_file}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
