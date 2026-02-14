"""
HC11 Virtual Emulator — Opcode Decoder / Dispatch Table

SCAFFOLD — needs cross-referencing against:
  - tonypdmtr/EVBU PySim11/ops.py (Ops dict, PrebyteList)
  - hc11_compiler/assembler.py (our own opcode table, 313 entries)
  - Motorola MC68HC11A8 Programming Reference Guide (opcode card)
  - Motorola MC68HC11 Reference Manual Rev3 Appendix A

This module maps opcode bytes to (mnemonic, addressing_mode, cycle_count).
Prebyte handling: $18 = Y-indexed, $1A = page 3, $CD = page 4.

The opcode table here is derived from EVBU PySim11/ops.py (GPL-2.0,
tonypdmtr) and cross-referenced against our assembler.py and the
Motorola reference manual. Any discrepancies should be resolved
against the Motorola PDF as the authoritative source.

Addressing modes:
  INH     Inherent (no operand)
  IMM8    Immediate 8-bit
  IMM16   Immediate 16-bit
  DIR     Direct page ($00–$FF)
  EXT     Extended (16-bit address)
  INDX    Indexed via X
  INDY    Indexed via Y (with $18 prefix)
  REL     Relative (signed 8-bit branch offset)
  BIT2DIR   BCLR/BSET direct
  BIT2INDX  BCLR/BSET indexed X
  BIT2INDY  BCLR/BSET indexed Y
  BIT3DIR   BRCLR/BRSET direct
  BIT3INDX  BRCLR/BRSET indexed X
  BIT3INDY  BRCLR/BRSET indexed Y
"""

# ──────────────────────────────────────────────
# Addressing mode constants
# ──────────────────────────────────────────────

INH      = 'INH'
IMM8     = 'IMM8'
IMM16    = 'IMM16'
DIR      = 'DIR'
EXT      = 'EXT'
INDX     = 'INDX'
INDY     = 'INDY'
REL      = 'REL'
BIT2DIR  = 'BIT2DIR'
BIT2INDX = 'BIT2INDX'
BIT2INDY = 'BIT2INDY'
BIT3DIR  = 'BIT3DIR'
BIT3INDX = 'BIT3INDX'
BIT3INDY = 'BIT3INDY'

# Prebyte opcodes that indicate a multi-byte opcode
PREBYTE_LIST = [0x18, 0x1A, 0xCD]


# ──────────────────────────────────────────────
# Main opcode table — Page 1 (single-byte opcodes)
# ──────────────────────────────────────────────
# Format: opcode -> (mnemonic, addressing_mode, cycle_count)
#
# Source: EVBU PySim11/ops.py cross-referenced with Motorola HC11 RM Appendix A
# SCAFFOLD: Full table included. Needs byte-for-byte validation against
#           our assembler.py opcode entries.

OPCODES = {
    # ── Misc / Control ──
    0x00: ('TEST',  INH,      1),
    0x01: ('NOP',   INH,      2),
    0x02: ('IDIV',  INH,     41),
    0x03: ('FDIV',  INH,     41),
    0x04: ('LSRD',  INH,      3),
    0x05: ('LSLD',  INH,      3),   # aka ASLD
    0x06: ('TAP',   INH,      2),
    0x07: ('TPA',   INH,      2),
    0x08: ('INX',   INH,      3),
    0x09: ('DEX',   INH,      3),
    0x0A: ('CLV',   INH,      2),
    0x0B: ('SEV',   INH,      2),
    0x0C: ('CLC',   INH,      2),
    0x0D: ('SEC',   INH,      2),
    0x0E: ('CLI',   INH,      2),
    0x0F: ('SEI',   INH,      2),
    
    # ── Arithmetic / Transfer ──
    0x10: ('SBA',   INH,      2),
    0x11: ('CBA',   INH,      2),
    
    # ── Bit manipulation (direct page) ──
    0x12: ('BRSET', BIT3DIR,  6),
    0x13: ('BRCLR', BIT3DIR,  6),
    0x14: ('BSET',  BIT2DIR,  6),
    0x15: ('BCLR',  BIT2DIR,  6),
    
    # ── Transfer / Stack ──
    0x16: ('TAB',   INH,      2),
    0x17: ('TBA',   INH,      2),
    # 0x18: prebyte for Y-indexed (handled separately)
    0x19: ('DAA',   INH,      2),
    # 0x1A: prebyte for page 3
    0x1B: ('ABA',   INH,      2),
    
    # ── Bit manipulation (indexed X) ──
    0x1C: ('BSET',  BIT2INDX, 7),
    0x1D: ('BCLR',  BIT2INDX, 7),
    0x1E: ('BRSET', BIT3INDX, 7),
    0x1F: ('BRCLR', BIT3INDX, 7),
    
    # ── Branch instructions ──
    0x20: ('BRA',   REL,      3),
    0x21: ('BRN',   REL,      3),
    0x22: ('BHI',   REL,      3),
    0x23: ('BLS',   REL,      3),
    0x24: ('BCC',   REL,      3),   # aka BHS
    0x25: ('BCS',   REL,      3),   # aka BLO
    0x26: ('BNE',   REL,      3),
    0x27: ('BEQ',   REL,      3),
    0x28: ('BVC',   REL,      3),
    0x29: ('BVS',   REL,      3),
    0x2A: ('BPL',   REL,      3),
    0x2B: ('BMI',   REL,      3),
    0x2C: ('BGE',   REL,      3),
    0x2D: ('BLT',   REL,      3),
    0x2E: ('BGT',   REL,      3),
    0x2F: ('BLE',   REL,      3),
    
    # ── Stack operations ──
    0x30: ('TSX',   INH,      3),
    0x31: ('INS',   INH,      3),
    0x32: ('PULA',  INH,      4),
    0x33: ('PULB',  INH,      4),
    0x34: ('DES',   INH,      3),
    0x35: ('TXS',   INH,      3),
    0x36: ('PSHA',  INH,      3),
    0x37: ('PSHB',  INH,      3),
    0x38: ('PULX',  INH,      5),
    0x39: ('RTS',   INH,      5),
    0x3A: ('ABX',   INH,      3),
    0x3B: ('RTI',   INH,     12),
    0x3C: ('PSHX',  INH,      4),
    0x3D: ('MUL',   INH,     10),
    0x3E: ('WAI',   INH,     14),
    0x3F: ('SWI',   INH,     14),
    
    # ── Accumulator A operations (inherent) ──
    0x40: ('NEGA',  INH,      2),
    0x43: ('COMA',  INH,      2),
    0x44: ('LSRA',  INH,      2),
    0x46: ('RORA',  INH,      2),
    0x47: ('ASRA',  INH,      2),
    0x48: ('ASLA',  INH,      2),   # aka LSLA
    0x49: ('ROLA',  INH,      2),
    0x4A: ('DECA',  INH,      2),
    0x4C: ('INCA',  INH,      2),
    0x4D: ('TSTA',  INH,      2),
    0x4F: ('CLRA',  INH,      2),
    
    # ── Accumulator B operations (inherent) ──
    0x50: ('NEGB',  INH,      2),
    0x53: ('COMB',  INH,      2),
    0x54: ('LSRB',  INH,      2),
    0x56: ('RORB',  INH,      2),
    0x57: ('ASRB',  INH,      2),
    0x58: ('ASLB',  INH,      2),   # aka LSLB
    0x59: ('ROLB',  INH,      2),
    0x5A: ('DECB',  INH,      2),
    0x5C: ('INCB',  INH,      2),
    0x5D: ('TSTB',  INH,      2),
    0x5F: ('CLRB',  INH,      2),
    
    # ── Memory operations (indexed X) ──
    0x60: ('NEG',   INDX,     6),
    0x63: ('COM',   INDX,     6),
    0x64: ('LSR',   INDX,     6),
    0x66: ('ROR',   INDX,     6),
    0x67: ('ASR',   INDX,     6),
    0x68: ('ASL',   INDX,     6),   # aka LSL
    0x69: ('ROL',   INDX,     6),
    0x6A: ('DEC',   INDX,     6),
    0x6C: ('INC',   INDX,     6),
    0x6D: ('TST',   INDX,     6),
    0x6E: ('JMP',   INDX,     3),
    0x6F: ('CLR',   INDX,     6),
    
    # ── Memory operations (extended) ──
    0x70: ('NEG',   EXT,      6),
    0x73: ('COM',   EXT,      6),
    0x74: ('LSR',   EXT,      6),
    0x76: ('ROR',   EXT,      6),
    0x77: ('ASR',   EXT,      6),
    0x78: ('ASL',   EXT,      6),   # aka LSL
    0x79: ('ROL',   EXT,      6),
    0x7A: ('DEC',   EXT,      6),
    0x7C: ('INC',   EXT,      6),
    0x7D: ('TST',   EXT,      6),
    0x7E: ('JMP',   EXT,      3),
    0x7F: ('CLR',   EXT,      6),
    
    # ── Accumulator A (immediate) ──
    0x80: ('SUBA',  IMM8,     2),
    0x81: ('CMPA',  IMM8,     2),
    0x82: ('SBCA',  IMM8,     2),
    0x83: ('SUBD',  IMM16,    4),
    0x84: ('ANDA',  IMM8,     2),
    0x85: ('BITA',  IMM8,     2),
    0x86: ('LDAA',  IMM8,     2),
    0x88: ('EORA',  IMM8,     2),
    0x89: ('ADCA',  IMM8,     2),
    0x8A: ('ORAA',  IMM8,     2),
    0x8B: ('ADDA',  IMM8,     2),
    0x8C: ('CPX',   IMM16,    4),
    0x8D: ('BSR',   REL,      6),
    0x8E: ('LDS',   IMM16,    3),
    0x8F: ('XGDX',  INH,      3),
    
    # ── Accumulator A (direct page) ──
    0x90: ('SUBA',  DIR,      3),
    0x91: ('CMPA',  DIR,      3),
    0x92: ('SBCA',  DIR,      3),
    0x93: ('SUBD',  DIR,      5),
    0x94: ('ANDA',  DIR,      3),
    0x95: ('BITA',  DIR,      3),
    0x96: ('LDAA',  DIR,      3),
    0x97: ('STAA',  DIR,      3),
    0x98: ('EORA',  DIR,      3),
    0x99: ('ADCA',  DIR,      3),
    0x9A: ('ORAA',  DIR,      3),
    0x9B: ('ADDA',  DIR,      3),
    0x9C: ('CPX',   DIR,      5),
    0x9D: ('JSR',   DIR,      5),
    0x9E: ('LDS',   DIR,      4),
    0x9F: ('STS',   DIR,      4),
    
    # ── Accumulator A (indexed X) ──
    0xA0: ('SUBA',  INDX,     4),
    0xA1: ('CMPA',  INDX,     4),
    0xA2: ('SBCA',  INDX,     4),
    0xA3: ('SUBD',  INDX,     6),
    0xA4: ('ANDA',  INDX,     4),
    0xA5: ('BITA',  INDX,     4),
    0xA6: ('LDAA',  INDX,     4),
    0xA7: ('STAA',  INDX,     4),
    0xA8: ('EORA',  INDX,     4),
    0xA9: ('ADCA',  INDX,     4),
    0xAA: ('ORAA',  INDX,     4),
    0xAB: ('ADDA',  INDX,     4),
    0xAC: ('CPX',   INDX,     6),
    0xAD: ('JSR',   INDX,     6),
    0xAE: ('LDS',   INDX,     5),
    0xAF: ('STS',   INDX,     5),
    
    # ── Accumulator A (extended) ──
    0xB0: ('SUBA',  EXT,      4),
    0xB1: ('CMPA',  EXT,      4),
    0xB2: ('SBCA',  EXT,      4),
    0xB3: ('SUBD',  EXT,      6),
    0xB4: ('ANDA',  EXT,      4),
    0xB5: ('BITA',  EXT,      4),
    0xB6: ('LDAA',  EXT,      4),
    0xB7: ('STAA',  EXT,      4),
    0xB8: ('EORA',  EXT,      4),
    0xB9: ('ADCA',  EXT,      4),
    0xBA: ('ORAA',  EXT,      4),
    0xBB: ('ADDA',  EXT,      4),
    0xBC: ('CPX',   EXT,      6),
    0xBD: ('JSR',   EXT,      6),
    0xBE: ('LDS',   EXT,      5),
    0xBF: ('STS',   EXT,      5),
    
    # ── Accumulator B (immediate) ──
    0xC0: ('SUBB',  IMM8,     2),
    0xC1: ('CMPB',  IMM8,     2),
    0xC2: ('SBCB',  IMM8,     2),
    0xC3: ('ADDD',  IMM16,    4),
    0xC4: ('ANDB',  IMM8,     2),
    0xC5: ('BITB',  IMM8,     2),
    0xC6: ('LDAB',  IMM8,     2),
    0xC8: ('EORB',  IMM8,     2),
    0xC9: ('ADCB',  IMM8,     2),
    0xCA: ('ORAB',  IMM8,     2),
    0xCB: ('ADDB',  IMM8,     2),
    0xCC: ('LDD',   IMM16,    3),
    0xCE: ('LDX',   IMM16,    3),
    0xCF: ('STOP',  INH,      2),
    
    # ── Accumulator B (direct page) ──
    0xD0: ('SUBB',  DIR,      3),
    0xD1: ('CMPB',  DIR,      3),
    0xD2: ('SBCB',  DIR,      3),
    0xD3: ('ADDD',  DIR,      5),
    0xD4: ('ANDB',  DIR,      3),
    0xD5: ('BITB',  DIR,      3),
    0xD6: ('LDAB',  DIR,      3),
    0xD7: ('STAB',  DIR,      3),
    0xD8: ('EORB',  DIR,      3),
    0xD9: ('ADCB',  DIR,      3),
    0xDA: ('ORAB',  DIR,      3),
    0xDB: ('ADDB',  DIR,      3),
    0xDC: ('LDD',   DIR,      4),
    0xDD: ('STD',   DIR,      4),
    0xDE: ('LDX',   DIR,      4),
    0xDF: ('STX',   DIR,      4),
    
    # ── Accumulator B (indexed X) ──
    0xE0: ('SUBB',  INDX,     4),
    0xE1: ('CMPB',  INDX,     4),
    0xE2: ('SBCB',  INDX,     4),
    0xE3: ('ADDD',  INDX,     6),
    0xE4: ('ANDB',  INDX,     4),
    0xE5: ('BITB',  INDX,     4),
    0xE6: ('LDAB',  INDX,     4),
    0xE7: ('STAB',  INDX,     4),
    0xE8: ('EORB',  INDX,     4),
    0xE9: ('ADCB',  INDX,     4),
    0xEA: ('ORAB',  INDX,     4),
    0xEB: ('ADDB',  INDX,     4),
    0xEC: ('LDD',   INDX,     5),
    0xED: ('STD',   INDX,     5),
    0xEE: ('LDX',   INDX,     5),
    0xEF: ('STX',   INDX,     5),
    
    # ── Accumulator B (extended) ──
    0xF0: ('SUBB',  EXT,      4),
    0xF1: ('CMPB',  EXT,      4),
    0xF2: ('SBCB',  EXT,      4),
    0xF3: ('ADDD',  EXT,      6),
    0xF4: ('ANDB',  EXT,      4),
    0xF5: ('BITB',  EXT,      4),
    0xF6: ('LDAB',  EXT,      4),
    0xF7: ('STAB',  EXT,      4),
    0xF8: ('EORB',  EXT,      4),
    0xF9: ('ADCB',  EXT,      4),
    0xFA: ('ORAB',  EXT,      4),
    0xFB: ('ADDB',  EXT,      4),
    0xFC: ('LDD',   EXT,      5),
    0xFD: ('STD',   EXT,      5),
    0xFE: ('LDX',   EXT,      5),
    0xFF: ('STX',   EXT,      5),
}


# ──────────────────────────────────────────────
# Page 2 opcodes ($18 prefix — Y-indexed and Y-specific)
# ──────────────────────────────────────────────

OPCODES_PAGE2 = {
    (0x18, 0x08): ('INY',   INH,    4),
    (0x18, 0x09): ('DEY',   INH,    4),
    (0x18, 0x1C): ('BSET',  BIT2INDY, 8),
    (0x18, 0x1D): ('BCLR',  BIT2INDY, 8),
    (0x18, 0x1E): ('BRSET', BIT3INDY, 8),
    (0x18, 0x1F): ('BRCLR', BIT3INDY, 8),
    (0x18, 0x30): ('TSY',   INH,    4),
    (0x18, 0x35): ('TYS',   INH,    4),
    (0x18, 0x38): ('PULY',  INH,    6),
    (0x18, 0x3A): ('ABY',   INH,    4),
    (0x18, 0x3C): ('PSHY',  INH,    5),
    (0x18, 0x60): ('NEG',   INDY,   7),
    (0x18, 0x63): ('COM',   INDY,   7),
    (0x18, 0x64): ('LSR',   INDY,   7),
    (0x18, 0x66): ('ROR',   INDY,   7),
    (0x18, 0x67): ('ASR',   INDY,   7),
    (0x18, 0x68): ('ASL',   INDY,   7),
    (0x18, 0x69): ('ROL',   INDY,   7),
    (0x18, 0x6A): ('DEC',   INDY,   7),
    (0x18, 0x6C): ('INC',   INDY,   7),
    (0x18, 0x6D): ('TST',   INDY,   7),
    (0x18, 0x6E): ('JMP',   INDY,   4),
    (0x18, 0x6F): ('CLR',   INDY,   7),
    (0x18, 0x8C): ('CPY',   IMM16,  5),
    (0x18, 0x8F): ('XGDY',  INH,    4),
    (0x18, 0x9C): ('CPY',   DIR,    6),
    (0x18, 0xA0): ('SUBA',  INDY,   5),
    (0x18, 0xA1): ('CMPA',  INDY,   5),
    (0x18, 0xA2): ('SBCA',  INDY,   5),
    (0x18, 0xA3): ('SUBD',  INDY,   7),
    (0x18, 0xA4): ('ANDA',  INDY,   5),
    (0x18, 0xA5): ('BITA',  INDY,   5),
    (0x18, 0xA6): ('LDAA',  INDY,   5),
    (0x18, 0xA7): ('STAA',  INDY,   5),
    (0x18, 0xA8): ('EORA',  INDY,   5),
    (0x18, 0xA9): ('ADCA',  INDY,   5),
    (0x18, 0xAA): ('ORAA',  INDY,   5),
    (0x18, 0xAB): ('ADDA',  INDY,   5),
    (0x18, 0xAC): ('CPY',   INDY,   7),
    (0x18, 0xAD): ('JSR',   INDY,   7),
    (0x18, 0xAE): ('LDS',   INDY,   6),
    (0x18, 0xAF): ('STS',   INDY,   6),
    (0x18, 0xBC): ('CPY',   EXT,    7),
    (0x18, 0xCE): ('LDY',   IMM16,  4),
    (0x18, 0xDE): ('LDY',   DIR,    5),
    (0x18, 0xDF): ('STY',   DIR,    5),
    (0x18, 0xE0): ('SUBB',  INDY,   5),
    (0x18, 0xE1): ('CMPB',  INDY,   5),
    (0x18, 0xE2): ('SBCB',  INDY,   5),
    (0x18, 0xE3): ('ADDD',  INDY,   7),
    (0x18, 0xE4): ('ANDB',  INDY,   5),
    (0x18, 0xE5): ('BITB',  INDY,   5),
    (0x18, 0xE6): ('LDAB',  INDY,   5),
    (0x18, 0xE7): ('STAB',  INDY,   5),
    (0x18, 0xE8): ('EORB',  INDY,   5),
    (0x18, 0xE9): ('ADCB',  INDY,   5),
    (0x18, 0xEA): ('ORAB',  INDY,   5),
    (0x18, 0xEB): ('ADDB',  INDY,   5),
    (0x18, 0xEC): ('LDD',   INDY,   6),
    (0x18, 0xED): ('STD',   INDY,   6),
    (0x18, 0xEE): ('LDY',   INDY,   6),
    (0x18, 0xEF): ('STY',   INDY,   6),
    (0x18, 0xFC): ('LDD',   EXT,    5),  # dup? check
    (0x18, 0xFE): ('LDY',   EXT,    6),
    (0x18, 0xFF): ('STY',   EXT,    6),
}


# ──────────────────────────────────────────────
# Page 3 opcodes ($1A prefix)
# ──────────────────────────────────────────────

OPCODES_PAGE3 = {
    (0x1A, 0x83): ('CPD',   IMM16,  5),
    (0x1A, 0x93): ('CPD',   DIR,    6),
    (0x1A, 0xA3): ('CPD',   INDX,   7),
    (0x1A, 0xAC): ('CPY',   INDX,   7),
    (0x1A, 0xB3): ('CPD',   EXT,    7),
    (0x1A, 0xEE): ('LDY',   INDX,   6),
    (0x1A, 0xEF): ('STY',   INDX,   6),
}


# ──────────────────────────────────────────────
# Page 4 opcodes ($CD prefix)
# ──────────────────────────────────────────────

OPCODES_PAGE4 = {
    (0xCD, 0xA3): ('CPD',   INDY,   7),
    (0xCD, 0xAC): ('CPX',   INDY,   7),
    (0xCD, 0xEE): ('LDX',   INDY,   6),
    (0xCD, 0xEF): ('STX',   INDY,   6),
}


# ──────────────────────────────────────────────
# Merged lookup for decoder
# ──────────────────────────────────────────────

# Combine all multi-byte opcode tables
ALL_OPCODES_PAGED = {**OPCODES_PAGE2, **OPCODES_PAGE3, **OPCODES_PAGE4}


class IllegalOpcode(Exception):
    """Raised when an undefined opcode is encountered."""
    pass


def decode_opcode(memory, pc: int):
    """Fetch and decode an opcode at the given PC.
    
    Returns: (mnemonic, mode, cycles, new_pc)
    
    Handles prebyte sequences ($18, $1A, $CD) for multi-byte opcodes.
    
    SCAFFOLD: Decoding logic cross-referenced with EVBU PySim11/PySim11.py
    ifetch_raw() method. Needs validation on all page 2/3/4 opcodes.
    """
    opcode = memory.read8(pc)
    pc_next = (pc + 1) & 0xFFFF
    
    if opcode in PREBYTE_LIST:
        opcode2 = memory.read8(pc_next)
        pc_next = (pc_next + 1) & 0xFFFF
        key = (opcode, opcode2)
        
        if key in ALL_OPCODES_PAGED:
            mnem, mode, cycles = ALL_OPCODES_PAGED[key]
            return mnem, mode, cycles, pc_next
        else:
            raise IllegalOpcode(
                f"Unknown paged opcode ${opcode:02X} ${opcode2:02X} at ${pc:04X}")
    
    if opcode in OPCODES:
        mnem, mode, cycles = OPCODES[opcode]
        return mnem, mode, cycles, pc_next
    
    raise IllegalOpcode(f"Unknown opcode ${opcode:02X} at ${pc:04X}")
