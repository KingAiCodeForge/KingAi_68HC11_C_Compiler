#!/usr/bin/env python3
"""
hc11_opcodes.py — 68HC11 Opcode Table for Assembler/Disassembler
==================================================================
Complete opcode definitions for the Motorola 68HC11 instruction set.
Used by the flash kernel assembler and simulators.
needs refactoring to be a easier to import script.
make _importable_wrapable.py clone of this with the fixs.
Instruction format sourced from:
  - tonypdmtr/EVBU PySim11/ops.py (full opcode table with cycle counts)
  - GaryOderNichts/ghidra-hc11-lang (instruction definitions)
  - M68HC11 Reference Manual (Motorola/Freescale)

Author: KingAustraliaGG
Date: 2026-02-15
"""

# =============================================================================
# Addressing Modes
# From tonypdmtr/EVBU PySim11/ops.py
# =============================================================================
IMM8    = 'IMM8'      # Immediate 8-bit
IMM16   = 'IMM16'     # Immediate 16-bit
EXT     = 'EXT'       # Extended (16-bit address)
DIR     = 'DIR'       # Direct page (8-bit address, $00-$FF)
INDX    = 'INDX'      # Indexed, X register
INDY    = 'INDY'      # Indexed, Y register
INH     = 'INH'       # Inherent (no operand)
REL     = 'REL'       # Relative (branch offset)

# =============================================================================
# Instruction Size (in bytes)
# =============================================================================
MODE_SIZE = {
    IMM8:  2,   # opcode + 1 byte immediate
    IMM16: 3,   # opcode + 2 byte immediate
    EXT:   3,   # opcode + 2 byte address
    DIR:   2,   # opcode + 1 byte address
    INDX:  2,   # opcode + 1 byte offset
    INDY:  3,   # prebyte + opcode + 1 byte offset
    INH:   1,   # opcode only
    REL:   2,   # opcode + 1 byte signed offset
}

# =============================================================================
# Main Opcode Table
# Format: opcode_byte → (mnemonic, mode, cycles)
# Sourced from tonypdmtr/EVBU PySim11/ops.py
# =============================================================================
OPCODES = {
    0x00: ('TEST', INH,   1),
    0x01: ('NOP',  INH,   2),
    0x02: ('IDIV', INH,   41),
    0x03: ('FDIV', INH,   41),
    0x04: ('LSRD', INH,   3),
    0x05: ('LSLD', INH,   3),     # aka ASLD
    0x06: ('TAP',  INH,   2),
    0x07: ('TPA',  INH,   2),
    0x08: ('INX',  INH,   3),
    0x09: ('DEX',  INH,   3),
    0x0A: ('CLV',  INH,   2),
    0x0B: ('SEV',  INH,   2),
    0x0C: ('CLC',  INH,   2),
    0x0D: ('SEC',  INH,   2),
    0x0E: ('CLI',  INH,   2),
    0x0F: ('SEI',  INH,   2),
    0x10: ('SBA',  INH,   2),
    0x11: ('CBA',  INH,   2),
    0x16: ('TAB',  INH,   2),
    0x17: ('TBA',  INH,   2),
    0x19: ('DAA',  INH,   2),
    0x1B: ('ABA',  INH,   2),

    # Branch instructions (REL mode)
    0x20: ('BRA',  REL,   3),
    0x21: ('BRN',  REL,   3),
    0x22: ('BHI',  REL,   3),
    0x23: ('BLS',  REL,   3),
    0x24: ('BHS',  REL,   3),     # aka BCC
    0x25: ('BLO',  REL,   3),     # aka BCS
    0x26: ('BNE',  REL,   3),
    0x27: ('BEQ',  REL,   3),
    0x28: ('BVC',  REL,   3),
    0x29: ('BVS',  REL,   3),
    0x2A: ('BPL',  REL,   3),
    0x2B: ('BMI',  REL,   3),
    0x2C: ('BGE',  REL,   3),
    0x2D: ('BLT',  REL,   3),
    0x2E: ('BGT',  REL,   3),
    0x2F: ('BLE',  REL,   3),

    # Stack/misc
    0x30: ('TSX',  INH,   3),
    0x31: ('INS',  INH,   3),
    0x32: ('PULA', INH,   4),
    0x33: ('PULB', INH,   4),
    0x34: ('DES',  INH,   3),
    0x35: ('TXS',  INH,   3),
    0x36: ('PSHA', INH,   3),
    0x37: ('PSHB', INH,   3),
    0x38: ('PULX', INH,   5),
    0x39: ('RTS',  INH,   5),
    0x3A: ('ABX',  INH,   3),
    0x3B: ('RTI',  INH,   12),
    0x3C: ('PSHX', INH,   4),
    0x3D: ('MUL',  INH,   10),
    0x3E: ('WAI',  INH,   1),
    0x3F: ('SWI',  INH,   14),

    # Accumulator A operations (INH)
    0x40: ('NEGA', INH,   2),
    0x43: ('COMA', INH,   2),
    0x44: ('LSRA', INH,   2),
    0x46: ('RORA', INH,   2),
    0x47: ('ASRA', INH,   2),
    0x48: ('ASLA', INH,   2),     # aka LSLA
    0x49: ('ROLA', INH,   2),
    0x4A: ('DECA', INH,   2),
    0x4C: ('INCA', INH,   2),
    0x4D: ('TSTA', INH,   2),
    0x4F: ('CLRA', INH,   2),

    # Accumulator B operations (INH)
    0x50: ('NEGB', INH,   2),
    0x53: ('COMB', INH,   2),
    0x54: ('LSRB', INH,   2),
    0x56: ('RORB', INH,   2),
    0x57: ('ASRB', INH,   2),
    0x58: ('ASLB', INH,   2),     # aka LSLB
    0x59: ('ROLB', INH,   2),
    0x5A: ('DECB', INH,   2),
    0x5C: ('INCB', INH,   2),
    0x5D: ('TSTB', INH,   2),
    0x5F: ('CLRB', INH,   2),

    # Indexed X operations
    0x60: ('NEG',  INDX,  6),
    0x63: ('COM',  INDX,  6),
    0x64: ('LSR',  INDX,  6),
    0x66: ('ROR',  INDX,  6),
    0x67: ('ASR',  INDX,  6),
    0x68: ('ASL',  INDX,  6),     # aka LSL
    0x69: ('ROL',  INDX,  6),
    0x6A: ('DEC',  INDX,  6),
    0x6C: ('INC',  INDX,  6),
    0x6D: ('TST',  INDX,  6),
    0x6E: ('JMP',  INDX,  3),
    0x6F: ('CLR',  INDX,  6),

    # Extended operations
    0x70: ('NEG',  EXT,   6),
    0x73: ('COM',  EXT,   6),
    0x74: ('LSR',  EXT,   6),
    0x76: ('ROR',  EXT,   6),
    0x77: ('ASR',  EXT,   6),
    0x78: ('ASL',  EXT,   6),     # aka LSL
    0x79: ('ROL',  EXT,   6),
    0x7A: ('DEC',  EXT,   6),
    0x7C: ('INC',  EXT,   6),
    0x7D: ('TST',  EXT,   6),
    0x7E: ('JMP',  EXT,   3),
    0x7F: ('CLR',  EXT,   6),

    # IMM8 / ACC A operations
    0x80: ('SUBA', IMM8,  2),
    0x81: ('CMPA', IMM8,  2),
    0x82: ('SBCA', IMM8,  2),
    0x83: ('SUBD', IMM16, 4),
    0x84: ('ANDA', IMM8,  2),
    0x85: ('BITA', IMM8,  2),
    0x86: ('LDAA', IMM8,  2),
    0x88: ('EORA', IMM8,  2),
    0x89: ('ADCA', IMM8,  2),
    0x8A: ('ORAA', IMM8,  2),
    0x8B: ('ADDA', IMM8,  2),
    0x8C: ('CPX',  IMM16, 4),
    0x8D: ('BSR',  REL,   6),
    0x8E: ('LDS',  IMM16, 3),
    0x8F: ('XGDX', INH,   3),

    # DIR / ACC A operations
    0x90: ('SUBA', DIR,   3),
    0x91: ('CMPA', DIR,   3),
    0x92: ('SBCA', DIR,   3),
    0x93: ('SUBD', DIR,   5),
    0x94: ('ANDA', DIR,   3),
    0x95: ('BITA', DIR,   3),
    0x96: ('LDAA', DIR,   3),
    0x97: ('STAA', DIR,   3),
    0x98: ('EORA', DIR,   3),
    0x99: ('ADCA', DIR,   3),
    0x9A: ('ORAA', DIR,   3),
    0x9B: ('ADDA', DIR,   3),
    0x9C: ('CPX',  DIR,   5),
    0x9D: ('JSR',  DIR,   5),
    0x9E: ('LDS',  DIR,   4),
    0x9F: ('STS',  DIR,   4),

    # INDX / ACC A operations
    0xA0: ('SUBA', INDX,  4),
    0xA1: ('CMPA', INDX,  4),
    0xA2: ('SBCA', INDX,  4),
    0xA3: ('SUBD', INDX,  6),
    0xA4: ('ANDA', INDX,  4),
    0xA5: ('BITA', INDX,  4),
    0xA6: ('LDAA', INDX,  4),
    0xA7: ('STAA', INDX,  4),
    0xA8: ('EORA', INDX,  4),
    0xA9: ('ADCA', INDX,  4),
    0xAA: ('ORAA', INDX,  4),
    0xAB: ('ADDA', INDX,  4),
    0xAC: ('CPX',  INDX,  6),
    0xAD: ('JSR',  INDX,  6),
    0xAE: ('LDS',  INDX,  5),
    0xAF: ('STS',  INDX,  5),

    # EXT / ACC A operations
    0xB0: ('SUBA', EXT,   4),
    0xB1: ('CMPA', EXT,   4),
    0xB2: ('SBCA', EXT,   4),
    0xB3: ('SUBD', EXT,   6),
    0xB4: ('ANDA', EXT,   4),
    0xB5: ('BITA', EXT,   4),
    0xB6: ('LDAA', EXT,   4),
    0xB7: ('STAA', EXT,   4),
    0xB8: ('EORA', EXT,   4),
    0xB9: ('ADCA', EXT,   4),
    0xBA: ('ORAA', EXT,   4),
    0xBB: ('ADDA', EXT,   4),
    0xBC: ('CPX',  EXT,   6),
    0xBD: ('JSR',  EXT,   6),
    0xBE: ('LDS',  EXT,   5),
    0xBF: ('STS',  EXT,   5),

    # IMM8 / ACC B operations
    0xC0: ('SUBB', IMM8,  2),
    0xC1: ('CMPB', IMM8,  2),
    0xC2: ('SBCB', IMM8,  2),
    0xC3: ('ADDD', IMM16, 4),
    0xC4: ('ANDB', IMM8,  2),
    0xC5: ('BITB', IMM8,  2),
    0xC6: ('LDAB', IMM8,  2),
    0xC8: ('EORB', IMM8,  2),
    0xC9: ('ADCB', IMM8,  2),
    0xCA: ('ORAB', IMM8,  2),
    0xCB: ('ADDB', IMM8,  2),
    0xCC: ('LDD',  IMM16, 3),
    0xCE: ('LDX',  IMM16, 3),
    0xCF: ('STOP', INH,   2),

    # DIR / ACC B operations
    0xD0: ('SUBB', DIR,   3),
    0xD1: ('CMPB', DIR,   3),
    0xD2: ('SBCB', DIR,   3),
    0xD3: ('ADDD', DIR,   5),
    0xD4: ('ANDB', DIR,   3),
    0xD5: ('BITB', DIR,   3),
    0xD6: ('LDAB', DIR,   3),
    0xD7: ('STAB', DIR,   3),
    0xD8: ('EORB', DIR,   3),
    0xD9: ('ADCB', DIR,   3),
    0xDA: ('ORAB', DIR,   3),
    0xDB: ('ADDB', DIR,   3),
    0xDC: ('LDD',  DIR,   4),
    0xDD: ('STD',  DIR,   4),
    0xDE: ('LDX',  DIR,   4),
    0xDF: ('STX',  DIR,   4),

    # INDX / ACC B operations
    0xE0: ('SUBB', INDX,  4),
    0xE1: ('CMPB', INDX,  4),
    0xE2: ('SBCB', INDX,  4),
    0xE3: ('ADDD', INDX,  6),
    0xE4: ('ANDB', INDX,  4),
    0xE5: ('BITB', INDX,  4),
    0xE6: ('LDAB', INDX,  4),
    0xE7: ('STAB', INDX,  4),
    0xE8: ('EORB', INDX,  4),
    0xE9: ('ADCB', INDX,  4),
    0xEA: ('ORAB', INDX,  4),
    0xEB: ('ADDB', INDX,  4),
    0xEC: ('LDD',  INDX,  5),
    0xED: ('STD',  INDX,  5),
    0xEE: ('LDX',  INDX,  5),
    0xEF: ('STX',  INDX,  5),

    # EXT / ACC B operations
    0xF0: ('SUBB', EXT,   4),
    0xF1: ('CMPB', EXT,   4),
    0xF2: ('SBCB', EXT,   4),
    0xF3: ('ADDD', EXT,   6),
    0xF4: ('ANDB', EXT,   4),
    0xF5: ('BITB', EXT,   4),
    0xF6: ('LDAB', EXT,   4),
    0xF7: ('STAB', EXT,   4),
    0xF8: ('EORB', EXT,   4),
    0xF9: ('ADCB', EXT,   4),
    0xFA: ('ORAB', EXT,   4),
    0xFB: ('ADDB', EXT,   4),
    0xFC: ('LDD',  EXT,   5),
    0xFD: ('STD',  EXT,   5),
    0xFE: ('LDX',  EXT,   5),
    0xFF: ('STX',  EXT,   5),
}

# =============================================================================
# Prebyte Opcodes (0x18, 0x1A, 0xCD prefixes)
# These are two-byte opcodes for Y-register and CPD instructions.
# From tonypdmtr/EVBU PySim11/ops.py
# =============================================================================
PREBYTE_OPCODES = {
    (0x18, 0x08): ('INY',  INH,   4),
    (0x18, 0x09): ('DEY',  INH,   4),
    (0x18, 0x1C): ('BSET', INDY,  8),
    (0x18, 0x1D): ('BCLR', INDY,  8),
    (0x18, 0x30): ('TSY',  INH,   4),
    (0x18, 0x35): ('TYS',  INH,   4),
    (0x18, 0x38): ('PULY', INH,   6),
    (0x18, 0x3A): ('ABY',  INH,   4),
    (0x18, 0x3C): ('PSHY', INH,   5),
    (0x18, 0x60): ('NEG',  INDY,  7),
    (0x18, 0x63): ('COM',  INDY,  7),
    (0x18, 0x64): ('LSR',  INDY,  7),
    (0x18, 0x66): ('ROR',  INDY,  7),
    (0x18, 0x67): ('ASR',  INDY,  7),
    (0x18, 0x68): ('ASL',  INDY,  7),
    (0x18, 0x69): ('ROL',  INDY,  7),
    (0x18, 0x6A): ('DEC',  INDY,  7),
    (0x18, 0x6C): ('INC',  INDY,  7),
    (0x18, 0x6D): ('TST',  INDY,  7),
    (0x18, 0x6E): ('JMP',  INDY,  4),
    (0x18, 0x6F): ('CLR',  INDY,  7),
    (0x18, 0x8C): ('CPY',  IMM16, 5),
    (0x18, 0x8F): ('XGDY', INH,   4),
    (0x18, 0x9C): ('CPY',  DIR,   6),
    (0x18, 0xA0): ('SUBA', INDY,  5),
    (0x18, 0xA1): ('CMPA', INDY,  5),
    (0x18, 0xBC): ('CPY',  EXT,   7),
    (0x18, 0xCE): ('LDY',  IMM16, 4),
    (0x18, 0xDE): ('LDY',  DIR,   5),
    (0x18, 0xDF): ('STY',  DIR,   5),
    (0x18, 0xEE): ('LDY',  INDY,  6),
    (0x18, 0xEF): ('STY',  INDY,  6),
    (0x18, 0xFE): ('LDY',  EXT,   6),
    (0x18, 0xFF): ('STY',  EXT,   6),

    (0x1A, 0x83): ('CPD',  IMM16, 5),
    (0x1A, 0x93): ('CPD',  DIR,   6),
    (0x1A, 0xA3): ('CPD',  INDX,  7),
    (0x1A, 0xAC): ('CPY',  INDX,  7),
    (0x1A, 0xB3): ('CPD',  EXT,   7),
    (0x1A, 0xEE): ('LDY',  INDX,  6),
    (0x1A, 0xEF): ('STY',  INDX,  6),

    (0xCD, 0xA3): ('CPD',  INDY,  7),
    (0xCD, 0xAC): ('CPX',  INDY,  7),
    (0xCD, 0xEE): ('LDX',  INDY,  6),
    (0xCD, 0xEF): ('STX',  INDY,  6),
}

PREBYTE_LIST = [0x18, 0x1A, 0xCD]

# =============================================================================
# Reverse lookup: mnemonic + mode → opcode byte(s)
# For use by the assembler
# =============================================================================

def build_reverse_table():
    """Build mnemonic → [(opcode, mode, cycles), ...] lookup."""
    table = {}
    for opcode, (mnem, mode, cycles) in OPCODES.items():
        if mnem not in table:
            table[mnem] = []
        table[mnem].append((opcode, mode, cycles))
    # Add prebyte opcodes
    for (pre, op), (mnem, mode, cycles) in PREBYTE_OPCODES.items():
        if mnem not in table:
            table[mnem] = []
        table[mnem].append(((pre, op), mode, cycles))
    return table

MNEMONIC_TABLE = build_reverse_table()

# =============================================================================
# Branch instruction aliases
# =============================================================================
BRANCH_ALIASES = {
    'BCC': 'BHS',
    'BCS': 'BLO',
    'ASLD': 'LSLD',
    'LSLA': 'ASLA',
    'LSLB': 'ASLB',
    'LSL': 'ASL',
}


# =============================================================================
# Simple assembler helper
# =============================================================================

def assemble_instruction(mnemonic: str, operand=None) -> bytes:
    """
    Assemble a single HC11 instruction to bytes.
    Returns the assembled bytes or raises ValueError.
    
    Examples:
        assemble_instruction('NOP')           → b'\\x01'
        assemble_instruction('LDAA', 0x55)    → b'\\x86\\x55'  (IMM8)
        assemble_instruction('STAA', 0x103A)  → b'\\xB7\\x10\\x3A'  (EXT)
        assemble_instruction('BRA', -18)      → b'\\x20\\xEE'  (REL, signed)
    """
    mnem = mnemonic.upper()
    # Handle aliases
    if mnem in BRANCH_ALIASES:
        mnem = BRANCH_ALIASES[mnem]

    if mnem not in MNEMONIC_TABLE:
        raise ValueError(f"Unknown mnemonic: {mnemonic}")

    entries = MNEMONIC_TABLE[mnem]

    # Determine mode from operand
    if operand is None:
        # INH mode
        for opcode, mode, _ in entries:
            if mode == INH:
                if isinstance(opcode, tuple):
                    return bytes(opcode)
                return bytes([opcode])
        raise ValueError(f"No INH mode for {mnem}")

    # Signed offset for branches
    if isinstance(operand, int) and operand < 0:
        # REL mode (branch)
        for opcode, mode, _ in entries:
            if mode == REL:
                offset = operand & 0xFF  # 2's complement
                if isinstance(opcode, tuple):
                    return bytes(list(opcode) + [offset])
                return bytes([opcode, offset])

    if isinstance(operand, int):
        # Try to pick best mode based on operand size
        if operand <= 0xFF:
            # Try DIR first, then IMM8
            for opcode, mode, _ in entries:
                if mode == DIR:
                    if isinstance(opcode, tuple):
                        return bytes(list(opcode) + [operand])
                    return bytes([opcode, operand])
            for opcode, mode, _ in entries:
                if mode == IMM8:
                    if isinstance(opcode, tuple):
                        return bytes(list(opcode) + [operand])
                    return bytes([opcode, operand])
            for opcode, mode, _ in entries:
                if mode == REL:
                    if isinstance(opcode, tuple):
                        return bytes(list(opcode) + [operand])
                    return bytes([opcode, operand])

        # EXT mode (16-bit address)
        for opcode, mode, _ in entries:
            if mode == EXT:
                hi = (operand >> 8) & 0xFF
                lo = operand & 0xFF
                if isinstance(opcode, tuple):
                    return bytes(list(opcode) + [hi, lo])
                return bytes([opcode, hi, lo])

        # IMM16 mode
        for opcode, mode, _ in entries:
            if mode == IMM16:
                hi = (operand >> 8) & 0xFF
                lo = operand & 0xFF
                if isinstance(opcode, tuple):
                    return bytes(list(opcode) + [hi, lo])
                return bytes([opcode, hi, lo])

    raise ValueError(f"Cannot encode {mnem} with operand {operand}")


def disassemble(data: bytes, base_addr: int = 0) -> list:
    """
    Disassemble bytes into instruction tuples.
    Returns: [(address, bytes, mnemonic, operand_str), ...]
    """
    result = []
    i = 0
    while i < len(data):
        addr = base_addr + i
        opcode = data[i]

        # Check for prebyte
        if opcode in PREBYTE_LIST and i + 1 < len(data):
            key = (opcode, data[i + 1])
            if key in PREBYTE_OPCODES:
                mnem, mode, cycles = PREBYTE_OPCODES[key]
                size = 2 + (MODE_SIZE.get(mode, 1) - 1)
                inst_bytes = data[i:i + size]
                operand = _format_operand(data, i + 2, mode, addr + size)
                result.append((addr, inst_bytes, mnem, operand))
                i += size
                continue

        # Normal opcode
        if opcode in OPCODES:
            mnem, mode, cycles = OPCODES[opcode]
            size = MODE_SIZE.get(mode, 1)
            inst_bytes = data[i:i + size]
            operand = _format_operand(data, i + 1, mode, addr + size)
            result.append((addr, inst_bytes, mnem, operand))
            i += size
        else:
            result.append((addr, bytes([opcode]), 'FCB', f'${opcode:02X}'))
            i += 1

    return result


def _format_operand(data: bytes, offset: int, mode: str, next_addr: int) -> str:
    """Format operand string for disassembly."""
    if mode == INH:
        return ''
    if offset >= len(data):
        return '?'

    if mode == IMM8:
        return f'#${data[offset]:02X}'
    elif mode == IMM16:
        if offset + 1 < len(data):
            val = (data[offset] << 8) | data[offset + 1]
            return f'#${val:04X}'
    elif mode == DIR:
        return f'${data[offset]:02X}'
    elif mode == EXT:
        if offset + 1 < len(data):
            val = (data[offset] << 8) | data[offset + 1]
            return f'${val:04X}'
    elif mode in (INDX, INDY):
        return f'{data[offset]},{"X" if mode == INDX else "Y"}'
    elif mode == REL:
        off = data[offset]
        if off >= 128:
            off -= 256
        target = next_addr + off
        return f'${target:04X}'
    return '?'


# =============================================================================
# CLI Test
# =============================================================================

if __name__ == '__main__':
    # Test: assemble the watchdog kernel
    print("=== HC11 Opcode Table Test ===\n")

    # Assemble watchdog kernel instructions
    kernel = bytearray()
    kernel += assemble_instruction('LDAA', 0x55)      # 86 55
    kernel += bytes([0xB7, 0x10, 0x3A])                # STAA $103A (manual EXT)
    kernel += assemble_instruction('LDAA', 0xAA)      # 86 AA
    kernel += bytes([0xB7, 0x10, 0x3A])                # STAA $103A
    kernel += bytes([0xCE, 0xFF, 0xFF])                # LDX #$FFFF
    kernel += assemble_instruction('DEX')              # 09
    kernel += bytes([0x26, 0xFD])                      # BNE -3
    kernel += bytes([0x20, 0xEE])                      # BRA -18

    print(f"Assembled kernel ({len(kernel)} bytes):")
    print(' '.join(f'{b:02X}' for b in kernel))
    print()

    # Disassemble it back
    print("Disassembly:")
    for addr, inst_bytes, mnem, operand in disassemble(bytes(kernel), 0x0300):
        hex_str = ' '.join(f'{b:02X}' for b in inst_bytes)
        print(f'  ${addr:04X}: {hex_str:<12s} {mnem} {operand}')

    print(f"\nTotal opcodes in table: {len(OPCODES)}")
    print(f"Prebyte opcodes: {len(PREBYTE_OPCODES)}")
    print(f"Unique mnemonics: {len(MNEMONIC_TABLE)}")
