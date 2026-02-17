#!/usr/bin/env python3
"""
Minimal HC11 disassembler for analyzing code at specific addresses
Focus on finding spark calculation routine at 0x17283
"""



import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# HC11 opcode table - complete page 1
OPCODES = {
    # Inherent (1-byte)
    0x01: ('NOP', 1, 'imp'), 0x02: ('IDIV', 1, 'imp'), 0x03: ('FDIV', 1, 'imp'),
    0x04: ('LSRD', 1, 'imp'), 0x05: ('ASLD', 1, 'imp'), 0x06: ('TAP', 1, 'imp'),
    0x07: ('TPA', 1, 'imp'), 0x08: ('INX', 1, 'imp'), 0x09: ('DEX', 1, 'imp'),
    0x0A: ('CLV', 1, 'imp'), 0x0B: ('SEV', 1, 'imp'), 0x0C: ('CLC', 1, 'imp'),
    0x0D: ('SEC', 1, 'imp'), 0x0E: ('CLI', 1, 'imp'), 0x0F: ('SEI', 1, 'imp'),
    0x10: ('SBA', 1, 'imp'), 0x11: ('CBA', 1, 'imp'), 0x16: ('TAB', 1, 'imp'),
    0x17: ('TBA', 1, 'imp'), 0x19: ('DAA', 1, 'imp'), 0x1B: ('ABA', 1, 'imp'),
    0x30: ('TSX', 1, 'imp'), 0x31: ('INS', 1, 'imp'), 0x32: ('PULA', 1, 'imp'),
    0x33: ('PULB', 1, 'imp'), 0x34: ('DES', 1, 'imp'), 0x35: ('TXS', 1, 'imp'),
    0x36: ('PSHA', 1, 'imp'), 0x37: ('PSHB', 1, 'imp'), 0x38: ('PULX', 1, 'imp'),
    0x39: ('RTS', 1, 'imp'), 0x3A: ('ABX', 1, 'imp'), 0x3B: ('RTI', 1, 'imp'),
    0x3C: ('PSHX', 1, 'imp'), 0x3D: ('MUL', 1, 'imp'), 0x3E: ('WAI', 1, 'imp'),
    0x3F: ('SWI', 1, 'imp'), 0x8F: ('XGDX', 1, 'imp'), 0xCF: ('STOP', 1, 'imp'),
    # Accumulator A/B inherent
    0x40: ('NEGA', 1, 'imp'), 0x43: ('COMA', 1, 'imp'), 0x44: ('LSRA', 1, 'imp'),
    0x46: ('RORA', 1, 'imp'), 0x47: ('ASRA', 1, 'imp'), 0x48: ('ASLA', 1, 'imp'),
    0x49: ('ROLA', 1, 'imp'), 0x4A: ('DECA', 1, 'imp'), 0x4C: ('INCA', 1, 'imp'),
    0x4D: ('TSTA', 1, 'imp'), 0x4F: ('CLRA', 1, 'imp'),
    0x50: ('NEGB', 1, 'imp'), 0x53: ('COMB', 1, 'imp'), 0x54: ('LSRB', 1, 'imp'),
    0x56: ('RORB', 1, 'imp'), 0x57: ('ASRB', 1, 'imp'), 0x58: ('ASLB', 1, 'imp'),
    0x59: ('ROLB', 1, 'imp'), 0x5A: ('DECB', 1, 'imp'), 0x5C: ('INCB', 1, 'imp'),
    0x5D: ('TSTB', 1, 'imp'), 0x5F: ('CLRB', 1, 'imp'),
    # Bit manipulation (direct)
    0x12: ('BRSET', 4, 'dir_bit'), 0x13: ('BRCLR', 4, 'dir_bit'),
    0x14: ('BSET', 3, 'dir_bit'), 0x15: ('BCLR', 3, 'dir_bit'),
    # Branches (relative)
    0x20: ('BRA', 2, 'rel'), 0x21: ('BRN', 2, 'rel'),
    0x22: ('BHI', 2, 'rel'), 0x23: ('BLS', 2, 'rel'),
    0x24: ('BCC', 2, 'rel'), 0x25: ('BCS', 2, 'rel'),
    0x26: ('BNE', 2, 'rel'), 0x27: ('BEQ', 2, 'rel'),
    0x28: ('BVC', 2, 'rel'), 0x29: ('BVS', 2, 'rel'),
    0x2A: ('BPL', 2, 'rel'), 0x2B: ('BMI', 2, 'rel'),
    0x2C: ('BGE', 2, 'rel'), 0x2D: ('BLT', 2, 'rel'),
    0x2E: ('BGT', 2, 'rel'), 0x2F: ('BLE', 2, 'rel'),
    0x8D: ('BSR', 2, 'rel'),
    # Indexed memory ops (2-byte)
    0x60: ('NEG', 2, 'idx'), 0x63: ('COM', 2, 'idx'),
    0x64: ('LSR', 2, 'idx'), 0x66: ('ROR', 2, 'idx'),
    0x67: ('ASR', 2, 'idx'), 0x68: ('ASL', 2, 'idx'),
    0x69: ('ROL', 2, 'idx'), 0x6A: ('DEC', 2, 'idx'),
    0x6C: ('INC', 2, 'idx'), 0x6D: ('TST', 2, 'idx'),
    0x6E: ('JMP', 2, 'idx'), 0x6F: ('CLR', 2, 'idx'),
    # Extended memory ops (3-byte)
    0x70: ('NEG', 3, 'ext'), 0x73: ('COM', 3, 'ext'),
    0x74: ('LSR', 3, 'ext'), 0x76: ('ROR', 3, 'ext'),
    0x77: ('ASR', 3, 'ext'), 0x78: ('ASL', 3, 'ext'),
    0x79: ('ROL', 3, 'ext'), 0x7A: ('DEC', 3, 'ext'),
    0x7C: ('INC', 3, 'ext'), 0x7D: ('TST', 3, 'ext'),
    0x7E: ('JMP', 3, 'ext'), 0x7F: ('CLR', 3, 'ext'),
    # AccA group - IMM
    0x80: ('SUBA', 2, 'imm'), 0x81: ('CMPA', 2, 'imm'),
    0x82: ('SBCA', 2, 'imm'), 0x83: ('SUBD', 3, 'imm'),
    0x84: ('ANDA', 2, 'imm'), 0x85: ('BITA', 2, 'imm'),
    0x86: ('LDAA', 2, 'imm'), 0x88: ('EORA', 2, 'imm'),
    0x89: ('ADCA', 2, 'imm'), 0x8A: ('ORAA', 2, 'imm'),
    0x8B: ('ADDA', 2, 'imm'), 0x8C: ('CPX', 3, 'imm'),
    0x8E: ('LDS', 3, 'imm'),
    # AccA group - DIR
    0x90: ('SUBA', 2, 'dir'), 0x91: ('CMPA', 2, 'dir'),
    0x92: ('SBCA', 2, 'dir'), 0x93: ('SUBD', 2, 'dir'),
    0x94: ('ANDA', 2, 'dir'), 0x95: ('BITA', 2, 'dir'),
    0x96: ('LDAA', 2, 'dir'), 0x97: ('STAA', 2, 'dir'),
    0x98: ('EORA', 2, 'dir'), 0x99: ('ADCA', 2, 'dir'),
    0x9A: ('ORAA', 2, 'dir'), 0x9B: ('ADDA', 2, 'dir'),
    0x9C: ('CPX', 2, 'dir'), 0x9D: ('JSR', 2, 'dir'),
    0x9E: ('LDS', 2, 'dir'), 0x9F: ('STS', 2, 'dir'),
    # AccA group - IDX
    0xA0: ('SUBA', 2, 'idx'), 0xA1: ('CMPA', 2, 'idx'),
    0xA2: ('SBCA', 2, 'idx'), 0xA3: ('SUBD', 2, 'idx'),
    0xA4: ('ANDA', 2, 'idx'), 0xA5: ('BITA', 2, 'idx'),
    0xA6: ('LDAA', 2, 'idx'), 0xA7: ('STAA', 2, 'idx'),
    0xA8: ('EORA', 2, 'idx'), 0xA9: ('ADCA', 2, 'idx'),
    0xAA: ('ORAA', 2, 'idx'), 0xAB: ('ADDA', 2, 'idx'),
    0xAC: ('CPX', 2, 'idx'), 0xAD: ('JSR', 2, 'idx'),
    0xAE: ('LDS', 2, 'idx'), 0xAF: ('STS', 2, 'idx'),
    # AccA group - EXT
    0xB0: ('SUBA', 3, 'ext'), 0xB1: ('CMPA', 3, 'ext'),
    0xB2: ('SBCA', 3, 'ext'), 0xB3: ('SUBD', 3, 'ext'),
    0xB4: ('ANDA', 3, 'ext'), 0xB5: ('BITA', 3, 'ext'),
    0xB6: ('LDAA', 3, 'ext'), 0xB7: ('STAA', 3, 'ext'),
    0xB8: ('EORA', 3, 'ext'), 0xB9: ('ADCA', 3, 'ext'),
    0xBA: ('ORAA', 3, 'ext'), 0xBB: ('ADDA', 3, 'ext'),
    0xBC: ('CPX', 3, 'ext'), 0xBD: ('JSR', 3, 'ext'),
    0xBE: ('LDS', 3, 'ext'), 0xBF: ('STS', 3, 'ext'),
    # AccB group - IMM
    0xC0: ('SUBB', 2, 'imm'), 0xC1: ('CMPB', 2, 'imm'),
    0xC2: ('SBCB', 2, 'imm'), 0xC3: ('ADDD', 3, 'imm'),
    0xC4: ('ANDB', 2, 'imm'), 0xC5: ('BITB', 2, 'imm'),
    0xC6: ('LDAB', 2, 'imm'), 0xC8: ('EORB', 2, 'imm'),
    0xC9: ('ADCB', 2, 'imm'), 0xCA: ('ORAB', 2, 'imm'),
    0xCB: ('ADDB', 2, 'imm'), 0xCC: ('LDD', 3, 'imm'),
    0xCE: ('LDX', 3, 'imm'),
    # AccB group - DIR
    0xD0: ('SUBB', 2, 'dir'), 0xD1: ('CMPB', 2, 'dir'),
    0xD2: ('SBCB', 2, 'dir'), 0xD3: ('ADDD', 2, 'dir'),
    0xD4: ('ANDB', 2, 'dir'), 0xD5: ('BITB', 2, 'dir'),
    0xD6: ('LDAB', 2, 'dir'), 0xD7: ('STAB', 2, 'dir'),
    0xD8: ('EORB', 2, 'dir'), 0xD9: ('ADCB', 2, 'dir'),
    0xDA: ('ORAB', 2, 'dir'), 0xDB: ('ADDB', 2, 'dir'),
    0xDC: ('LDD', 2, 'dir'), 0xDD: ('STD', 2, 'dir'),
    0xDE: ('LDX', 2, 'dir'), 0xDF: ('STX', 2, 'dir'),
    # AccB group - IDX
    0xE0: ('SUBB', 2, 'idx'), 0xE1: ('CMPB', 2, 'idx'),
    0xE2: ('SBCB', 2, 'idx'), 0xE3: ('ADDD', 2, 'idx'),
    0xE4: ('ANDB', 2, 'idx'), 0xE5: ('BITB', 2, 'idx'),
    0xE6: ('LDAB', 2, 'idx'), 0xE7: ('STAB', 2, 'idx'),
    0xE8: ('EORB', 2, 'idx'), 0xE9: ('ADCB', 2, 'idx'),
    0xEA: ('ORAB', 2, 'idx'), 0xEB: ('ADDB', 2, 'idx'),
    0xEC: ('LDD', 2, 'idx'), 0xED: ('STD', 2, 'idx'),
    0xEE: ('LDX', 2, 'idx'), 0xEF: ('STX', 2, 'idx'),
    # AccB group - EXT
    0xF0: ('SUBB', 3, 'ext'), 0xF1: ('CMPB', 3, 'ext'),
    0xF2: ('SBCB', 3, 'ext'), 0xF3: ('ADDD', 3, 'ext'),
    0xF4: ('ANDB', 3, 'ext'), 0xF5: ('BITB', 3, 'ext'),
    0xF6: ('LDAB', 3, 'ext'), 0xF7: ('STAB', 3, 'ext'),
    0xF8: ('EORB', 3, 'ext'), 0xF9: ('ADCB', 3, 'ext'),
    0xFA: ('ORAB', 3, 'ext'), 0xFB: ('ADDB', 3, 'ext'),
    0xFC: ('LDD', 3, 'ext'), 0xFD: ('STD', 3, 'ext'),
    0xFE: ('LDX', 3, 'ext'), 0xFF: ('STX', 3, 'ext'),
    # Page 2 (0x18 prebyte)
    0x18CE: ('LDY', 4, 'imm'),
}
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Tuple



def disassemble_at(data, start_addr, count=32):
    """Disassemble count bytes starting at start_addr"""
    
    print(f"\n=== Disassembly at 0x{start_addr:05X} ===\n")
    
    i = 0
    addr = start_addr
    
    while i < count and addr < len(data):
        opcode = data[addr]
        
        # Check for 2-byte opcode (e.g., 0x18 prefix for Y register)
        if opcode == 0x18 and addr + 1 < len(data):
            opcode = (opcode << 8) | data[addr + 1]
        
        if opcode in OPCODES:
            mnemonic, size, mode = OPCODES[opcode]
            
            # Get operand bytes
            operand_bytes = data[addr:addr+size]
            hex_str = ' '.join(f'{b:02X}' for b in operand_bytes)
            
            # Format operand
            if size == 1:
                operand = ''
            elif size == 2:
                if mode == 'imm':
                    operand = f'#${operand_bytes[1]:02X}'
                elif mode == 'dir':
                    operand = f'${operand_bytes[1]:02X}'
                elif mode == 'idx':
                    operand = f'${operand_bytes[1]:02X},X'
                elif mode == 'rel':
                    # Calculate relative branch target
                    offset = operand_bytes[1]
                    if offset >= 128:
                        offset = offset - 256
                    target = addr + 2 + offset
                    operand = f'${target:04X}'
            elif size == 3:
                if mode == 'imm':
                    word = (operand_bytes[1] << 8) | operand_bytes[2]
                    operand = f'#${word:04X}'
                else:
                    word = (operand_bytes[1] << 8) | operand_bytes[2]
                    operand = f'${word:04X}'
            elif size == 4:
                word = (operand_bytes[2] << 8) | operand_bytes[3]
                operand = f'#${word:04X}'
            
            print(f'0x{addr:05X}:  {hex_str:<12}  {mnemonic:<6} {operand}')
            
            addr += size
            i += size
        else:
            # Unknown opcode - show as hex
            print(f'0x{addr:05X}:  {opcode:02X}            .byte  ${opcode:02X}')
            addr += 1
            i += 1

def find_spark_patterns(data, start, end):
    """Look for common spark calculation patterns"""
    
    print(f"\n=== Searching for Spark Calculation Patterns ===\n")
    
    patterns = {
        'RPM_Compare': [0x81, None],           # CMPA #imm
        'RPM_Load': [0x96, None],              # LDAA dir (load RPM)
        'Spark_Store': [0x97, None],           # STAA dir (store spark)
        'JSR_Spark_Table': [0xBD, None, None], # JSR ext (call table lookup)
        'Branch_High': [0x24, None],           # BCC/BHS (branch if RPM high)
    }
    
    matches = []
    
    for name, pattern in patterns.items():
        for addr in range(start, end - len(pattern)):
            match = True
            for j, byte in enumerate(pattern):
                if byte is not None and data[addr + j] != byte:
                    match = False
                    break
            
            if match:
                matches.append((name, addr))
    
    if matches:
        print("Found potential spark-related code:")
        for name, addr in matches:
            print(f"  {name:<20} at 0x{addr:05X}")
    else:
        print("No obvious patterns found. Need full Ghidra analysis.")
    
    return matches

if __name__ == '__main__':
    bin_path = r"R:\VY_V6_Assembly_Modding\VX-VY_V6_$060A_Enhanced_v1.0a - Copy.bin"
    
    with open(bin_path, 'rb') as f:
        data = f.read()
    
    # Disassemble at 0x17283 (XDF spark table swap address)
    print("=" * 70)
    print("TARGET: 0x17283 (XDF 'Performance Mode - Spark Table Swap')")
    print("=" * 70)
    
    disassemble_at(data, 0x17283, count=64)
    
    # Look for patterns in surrounding code
    find_spark_patterns(data, 0x17000, 0x17400)
    
    # Show context before and after
    print(f"\n=== Context Before 0x17283 ===")
    disassemble_at(data, 0x17263, count=32)
    
    print(f"\n=== Context After 0x172A0 ===")
    disassemble_at(data, 0x172A0, count=32)
    
    print(f"\n=== ANALYSIS SUMMARY ===")
    print(f"Address 0x17283: Byte = 0x{data[0x17283]:02X}")
    print(f"\nTo proceed with inline replacement:")
    print(f"1. Identify function boundaries (find RTS or JMP)")
    print(f"2. Calculate available space (bytes between start and RTS)")
    print(f"3. Design 6-10 byte patch to fit inline")
    print(f"4. Verify no multi-byte instructions are split")
    print(f"\nNext: Open in Ghidra GUI for full decompilation")
