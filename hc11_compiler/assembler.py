"""
68HC11 Two-Pass Assembler for the KingAI C Compiler.

Assembles 68HC11 assembly text into binary or Motorola S19 format.

Input:  Assembly text (as produced by the codegen)
Output: Raw bytes, S19 text, or both

Reference: Motorola MC68HC11 Reference Manual Rev3,
           MC68HC11A8 Programming Reference Guide (1985)

Addressing modes:
  INH  — Inherent (no operand)            e.g. RTS, NOP, INCA
  IMM  — Immediate (#value)               e.g. LDAA #$FF
  DIR  — Direct page ($00-$FF)            e.g. LDAA $40
  EXT  — Extended (16-bit address)        e.g. LDAA $1000
  IDX  — Indexed (offset,X or offset,Y)   e.g. LDAA 0,X
  REL  — Relative (branch target)         e.g. BRA label

How the two-pass algorithm works:
  Pass 1: Scan all lines, resolve labels to addresses, compute instruction sizes.
           Labels get assigned the current PC value. Forward references are recorded.
  Pass 2: Emit actual bytes. Now all labels are known, so branch offsets and
           absolute addresses can be filled in.

  This same algorithm works for ANY CPU — only the opcode table and addressing
  mode parser need to change. To port to another instruction set:
    1. Replace OPCODES dict with your CPU's opcodes
    2. Update _parse_operand() for your addressing modes
    3. Adjust _encode_instruction() for your instruction format
    4. Keep the two-pass label resolution logic as-is
"""

from __future__ import annotations
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import re

__all__ = ['Assembler', 'AssemblerError', 'assemble', 'assemble_to_s19']


class AssemblerError(Exception):
    """Raised on assembly errors."""
    def __init__(self, message: str, line_num: int = 0, line_text: str = ""):
        self.line_num = line_num
        self.line_text = line_text
        super().__init__(f"Line {line_num}: {message}" if line_num else message)


# ──────────────────────────────────────────────
# Addressing mode enumeration
# ──────────────────────────────────────────────

INH = 'INH'   # Inherent
IMM8 = 'IMM8'  # Immediate 8-bit
IMM16 = 'IMM16' # Immediate 16-bit
DIR = 'DIR'    # Direct page
EXT = 'EXT'    # Extended
IDX = 'IDX'    # Indexed ,X
IDY = 'IDY'    # Indexed ,Y (uses $18 prefix)
REL = 'REL'    # Relative (8-bit signed offset)


# ──────────────────────────────────────────────
# HC11 Opcode Table
# ──────────────────────────────────────────────
# Format: { 'MNEMONIC': { addr_mode: (opcode_bytes, total_size) } }
#
# For Y-indexed instructions, the opcode_bytes include the $18 prefix.
# total_size includes prefix + opcode + operand bytes.
#
# Source: MC68HC11A8 Programming Reference Guide + Reference Manual Appendix A.

OPCODES: Dict[str, Dict[str, Tuple[bytes, int]]] = {}

def _op(mnemonic: str, mode: str, opcode: int, size: int, prefix: bytes = b''):
    """Register an opcode entry."""
    if mnemonic not in OPCODES:
        OPCODES[mnemonic] = {}
    OPCODES[mnemonic][mode] = (prefix + bytes([opcode]), size)

def _opy(mnemonic: str, mode: str, opcode: int, size: int):
    """Register a Y-prefixed opcode (prefix $18 or $1A or $CD)."""
    _op(mnemonic, mode, opcode, size, prefix=b'\x18')

# ── Inherent instructions ──
_op('NOP',   INH,  0x01, 1)
_op('INCA',  INH,  0x4C, 1)
_op('INCB',  INH,  0x5C, 1)
_op('DECA',  INH,  0x4A, 1)
_op('DECB',  INH,  0x5A, 1)
_op('CLRA',  INH,  0x4F, 1)
_op('CLRB',  INH,  0x5F, 1)
_op('COMA',  INH,  0x43, 1)
_op('COMB',  INH,  0x53, 1)
_op('NEGA',  INH,  0x40, 1)
_op('NEGB',  INH,  0x50, 1)
_op('TSTA',  INH,  0x4D, 1)
_op('TSTB',  INH,  0x5D, 1)
_op('ROLA',  INH,  0x49, 1)
_op('ROLB',  INH,  0x59, 1)
_op('RORA',  INH,  0x46, 1)
_op('RORB',  INH,  0x56, 1)
_op('ASLA',  INH,  0x48, 1)
_op('ASLB',  INH,  0x58, 1)
_op('ASRA',  INH,  0x47, 1)
_op('ASRB',  INH,  0x57, 1)
_op('LSLA',  INH,  0x48, 1)  # same as ASLA
_op('LSLB',  INH,  0x58, 1)  # same as ASLB
_op('LSRA',  INH,  0x44, 1)
_op('LSRB',  INH,  0x54, 1)
_op('TAB',   INH,  0x16, 1)
_op('TBA',   INH,  0x17, 1)
_op('TAP',   INH,  0x06, 1)
_op('TPA',   INH,  0x07, 1)
_op('TSX',   INH,  0x30, 1)
_op('TXS',   INH,  0x35, 1)
_op('TSY',   INH,  0x30, 2, prefix=b'\x18')  # $18 $30
_op('TYS',   INH,  0x35, 2, prefix=b'\x18')  # $18 $35
_op('PSHA',  INH,  0x36, 1)
_op('PSHB',  INH,  0x37, 1)
_op('PSHX',  INH,  0x3C, 1)
_op('PSHY',  INH,  0x3C, 2, prefix=b'\x18')  # $18 $3C
_op('PULA',  INH,  0x32, 1)
_op('PULB',  INH,  0x33, 1)
_op('PULX',  INH,  0x38, 1)
_op('PULY',  INH,  0x38, 2, prefix=b'\x18')  # $18 $38
_op('RTS',   INH,  0x39, 1)
_op('RTI',   INH,  0x3B, 1)
_op('SWI',   INH,  0x3F, 1)
_op('WAI',   INH,  0x3E, 1)
_op('INS',   INH,  0x31, 1)
_op('DES',   INH,  0x34, 1)
_op('INX',   INH,  0x08, 1)
_op('DEX',   INH,  0x09, 1)
_op('INY',   INH,  0x08, 2, prefix=b'\x18')  # $18 $08
_op('DEY',   INH,  0x09, 2, prefix=b'\x18')  # $18 $09
_op('ABA',   INH,  0x1B, 1)
_op('SBA',   INH,  0x10, 1)
_op('CBA',   INH,  0x11, 1)
_op('SEC',   INH,  0x0D, 1)
_op('CLC',   INH,  0x0C, 1)
_op('SEI',   INH,  0x0F, 1)
_op('CLI',   INH,  0x0E, 1)
_op('SEV',   INH,  0x0B, 1)
_op('CLV',   INH,  0x0A, 1)
_op('MUL',   INH,  0x3D, 1)
_op('IDIV',  INH,  0x02, 1)  # actually consumes D/X but is inherent encoding
_op('FDIV',  INH,  0x03, 1)
_op('STOP',  INH,  0xCF, 1)
_op('ABX',   INH,  0x3A, 1)
_op('ABY',   INH,  0x3A, 2, prefix=b'\x18')  # $18 $3A
_op('XGDX',  INH,  0x8F, 1)
_op('XGDY',  INH,  0x8F, 2, prefix=b'\x18')  # $18 $8F
_op('DAA',   INH,  0x19, 1)
_op('LSRD',  INH,  0x04, 1)
_op('ASLD',  INH,  0x05, 1)
_op('LSLD',  INH,  0x05, 1)  # same as ASLD

# ── LDAA ──
_op('LDAA',  IMM8, 0x86, 2)
_op('LDAA',  DIR,  0x96, 2)
_op('LDAA',  EXT,  0xB6, 3)
_op('LDAA',  IDX,  0xA6, 2)
_opy('LDAA', IDY,  0xA6, 3)

# ── LDAB ──
_op('LDAB',  IMM8, 0xC6, 2)
_op('LDAB',  DIR,  0xD6, 2)
_op('LDAB',  EXT,  0xF6, 3)
_op('LDAB',  IDX,  0xE6, 2)
_opy('LDAB', IDY,  0xE6, 3)

# ── LDD ──
_op('LDD',   IMM16, 0xCC, 3)
_op('LDD',   DIR,   0xDC, 2)
_op('LDD',   EXT,   0xFC, 3)
_op('LDD',   IDX,   0xEC, 2)
_opy('LDD',  IDY,   0xEC, 3)

# ── LDX ──
_op('LDX',   IMM16, 0xCE, 3)
_op('LDX',   DIR,   0xDE, 2)
_op('LDX',   EXT,   0xFE, 3)
_op('LDX',   IDX,   0xEE, 2)
_op('LDX',   IDY,   0xEE, 3, prefix=b'\xCD')  # $CD prefix (NOT $18!)

# ── LDY ──
_opy('LDY',  IMM16, 0xCE, 4)  # $18 $CE + 16-bit
_op('LDY',   DIR,   0xDE, 3, prefix=b'\x18')
_op('LDY',   EXT,   0xFE, 4, prefix=b'\x18')
_op('LDY',   IDX,   0xEE, 3, prefix=b'\x1A')  # $1A prefix for IDX!
_op('LDY',   IDY,   0xEE, 3, prefix=b'\x18')

# ── LDS ──
_op('LDS',   IMM16, 0x8E, 3)
_op('LDS',   DIR,   0x9E, 2)
_op('LDS',   EXT,   0xBE, 3)
_op('LDS',   IDX,   0xAE, 2)
_opy('LDS',  IDY,   0xAE, 3)

# ── STAA ──
_op('STAA',  DIR,  0x97, 2)
_op('STAA',  EXT,  0xB7, 3)
_op('STAA',  IDX,  0xA7, 2)
_opy('STAA', IDY,  0xA7, 3)

# ── STAB ──
_op('STAB',  DIR,  0xD7, 2)
_op('STAB',  EXT,  0xF7, 3)
_op('STAB',  IDX,  0xE7, 2)
_opy('STAB', IDY,  0xE7, 3)

# ── STD ──
_op('STD',   DIR,  0xDD, 2)
_op('STD',   EXT,  0xFD, 3)
_op('STD',   IDX,  0xED, 2)
_opy('STD',  IDY,  0xED, 3)

# ── STX ──
_op('STX',   DIR,  0xDF, 2)
_op('STX',   EXT,  0xFF, 3)
_op('STX',   IDX,  0xEF, 2)
_op('STX',   IDY,  0xEF, 3, prefix=b'\xCD')  # $CD prefix

# ── STY ──
_op('STY',   DIR,  0xDF, 3, prefix=b'\x18')
_op('STY',   EXT,  0xFF, 4, prefix=b'\x18')
_op('STY',   IDX,  0xEF, 3, prefix=b'\x1A')  # $1A prefix
_op('STY',   IDY,  0xEF, 3, prefix=b'\x18')

# ── STS ──
_op('STS',   DIR,  0x9F, 2)
_op('STS',   EXT,  0xBF, 3)
_op('STS',   IDX,  0xAF, 2)
_opy('STS',  IDY,  0xAF, 3)

# ── ADDA ──
_op('ADDA',  IMM8, 0x8B, 2)
_op('ADDA',  DIR,  0x9B, 2)
_op('ADDA',  EXT,  0xBB, 3)
_op('ADDA',  IDX,  0xAB, 2)
_opy('ADDA', IDY,  0xAB, 3)

# ── ADDB ──
_op('ADDB',  IMM8, 0xCB, 2)
_op('ADDB',  DIR,  0xDB, 2)
_op('ADDB',  EXT,  0xFB, 3)
_op('ADDB',  IDX,  0xEB, 2)
_opy('ADDB', IDY,  0xEB, 3)

# ── ADDD ──
_op('ADDD',  IMM16, 0xC3, 3)
_op('ADDD',  DIR,   0xD3, 2)
_op('ADDD',  EXT,   0xF3, 3)
_op('ADDD',  IDX,   0xE3, 2)
_opy('ADDD', IDY,   0xE3, 3)

# ── ADCA ──
_op('ADCA',  IMM8, 0x89, 2)
_op('ADCA',  DIR,  0x99, 2)
_op('ADCA',  EXT,  0xB9, 3)
_op('ADCA',  IDX,  0xA9, 2)
_opy('ADCA', IDY,  0xA9, 3)

# ── ADCB ──
_op('ADCB',  IMM8, 0xC9, 2)
_op('ADCB',  DIR,  0xD9, 2)
_op('ADCB',  EXT,  0xF9, 3)
_op('ADCB',  IDX,  0xE9, 2)
_opy('ADCB', IDY,  0xE9, 3)

# ── SUBA ──
_op('SUBA',  IMM8, 0x80, 2)
_op('SUBA',  DIR,  0x90, 2)
_op('SUBA',  EXT,  0xB0, 3)
_op('SUBA',  IDX,  0xA0, 2)
_opy('SUBA', IDY,  0xA0, 3)

# ── SUBB ──
_op('SUBB',  IMM8, 0xC0, 2)
_op('SUBB',  DIR,  0xD0, 2)
_op('SUBB',  EXT,  0xF0, 3)
_op('SUBB',  IDX,  0xE0, 2)
_opy('SUBB', IDY,  0xE0, 3)

# ── SUBD ──
_op('SUBD',  IMM16, 0x83, 3)
_op('SUBD',  DIR,   0x93, 2)
_op('SUBD',  EXT,   0xB3, 3)
_op('SUBD',  IDX,   0xA3, 2)
_opy('SUBD', IDY,   0xA3, 3)

# ── SBCA ──
_op('SBCA',  IMM8, 0x82, 2)
_op('SBCA',  DIR,  0x92, 2)
_op('SBCA',  EXT,  0xB2, 3)
_op('SBCA',  IDX,  0xA2, 2)
_opy('SBCA', IDY,  0xA2, 3)

# ── SBCB ──
_op('SBCB',  IMM8, 0xC2, 2)
_op('SBCB',  DIR,  0xD2, 2)
_op('SBCB',  EXT,  0xF2, 3)
_op('SBCB',  IDX,  0xE2, 2)
_opy('SBCB', IDY,  0xE2, 3)

# ── ANDA ──
_op('ANDA',  IMM8, 0x84, 2)
_op('ANDA',  DIR,  0x94, 2)
_op('ANDA',  EXT,  0xB4, 3)
_op('ANDA',  IDX,  0xA4, 2)
_opy('ANDA', IDY,  0xA4, 3)

# ── ANDB ──
_op('ANDB',  IMM8, 0xC4, 2)
_op('ANDB',  DIR,  0xD4, 2)
_op('ANDB',  EXT,  0xF4, 3)
_op('ANDB',  IDX,  0xE4, 2)
_opy('ANDB', IDY,  0xE4, 3)

# ── ORAA ──
_op('ORAA',  IMM8, 0x8A, 2)
_op('ORAA',  DIR,  0x9A, 2)
_op('ORAA',  EXT,  0xBA, 3)
_op('ORAA',  IDX,  0xAA, 2)
_opy('ORAA', IDY,  0xAA, 3)

# ── ORAB ──
_op('ORAB',  IMM8, 0xCA, 2)
_op('ORAB',  DIR,  0xDA, 2)
_op('ORAB',  EXT,  0xFA, 3)
_op('ORAB',  IDX,  0xEA, 2)
_opy('ORAB', IDY,  0xEA, 3)

# ── EORA ──
_op('EORA',  IMM8, 0x88, 2)
_op('EORA',  DIR,  0x98, 2)
_op('EORA',  EXT,  0xB8, 3)
_op('EORA',  IDX,  0xA8, 2)
_opy('EORA', IDY,  0xA8, 3)

# ── EORB ──
_op('EORB',  IMM8, 0xC8, 2)
_op('EORB',  DIR,  0xD8, 2)
_op('EORB',  EXT,  0xF8, 3)
_op('EORB',  IDX,  0xE8, 2)
_opy('EORB', IDY,  0xE8, 3)

# ── CMPA ──
_op('CMPA',  IMM8, 0x81, 2)
_op('CMPA',  DIR,  0x91, 2)
_op('CMPA',  EXT,  0xB1, 3)
_op('CMPA',  IDX,  0xA1, 2)
_opy('CMPA', IDY,  0xA1, 3)

# ── CMPB ──
_op('CMPB',  IMM8, 0xC1, 2)
_op('CMPB',  DIR,  0xD1, 2)
_op('CMPB',  EXT,  0xF1, 3)
_op('CMPB',  IDX,  0xE1, 2)
_opy('CMPB', IDY,  0xE1, 3)

# ── CPD ──
_op('CPD',   IMM16, 0x83, 4, prefix=b'\x1A')  # $1A $83
_op('CPD',   DIR,   0x93, 3, prefix=b'\x1A')
_op('CPD',   EXT,   0xB3, 4, prefix=b'\x1A')
_op('CPD',   IDX,   0xA3, 3, prefix=b'\x1A')
_op('CPD',   IDY,   0xA3, 3, prefix=b'\xCD')

# ── CPX ──
_op('CPX',   IMM16, 0x8C, 3)
_op('CPX',   DIR,   0x9C, 2)
_op('CPX',   EXT,   0xBC, 3)
_op('CPX',   IDX,   0xAC, 2)
_op('CPX',   IDY,   0xAC, 3, prefix=b'\xCD')  # $CD prefix (NOT $18!)

# ── CPY ──
_opy('CPY',  IMM16, 0x8C, 4)
_op('CPY',   DIR,   0x9C, 3, prefix=b'\x18')
_op('CPY',   EXT,   0xBC, 4, prefix=b'\x18')
_op('CPY',   IDX,   0xAC, 3, prefix=b'\x1A')
_op('CPY',   IDY,   0xAC, 3, prefix=b'\x18')

# ── BITA ──
_op('BITA',  IMM8, 0x85, 2)
_op('BITA',  DIR,  0x95, 2)
_op('BITA',  EXT,  0xB5, 3)
_op('BITA',  IDX,  0xA5, 2)
_opy('BITA', IDY,  0xA5, 3)

# ── BITB ──
_op('BITB',  IMM8, 0xC5, 2)
_op('BITB',  DIR,  0xD5, 2)
_op('BITB',  EXT,  0xF5, 3)
_op('BITB',  IDX,  0xE5, 2)
_opy('BITB', IDY,  0xE5, 3)

# ── CLR / INC / DEC / TST / NEG / COM / ROL / ROR / ASL / ASR / LSL / LSR (memory) ──
for mnem, base_ext, base_idx in [
    ('CLR',  0x7F, 0x6F),
    ('INC',  0x7C, 0x6C),
    ('DEC',  0x7A, 0x6A),
    ('TST',  0x7D, 0x6D),
    ('NEG',  0x70, 0x60),
    ('COM',  0x73, 0x63),
    ('ROL',  0x79, 0x69),
    ('ROR',  0x76, 0x66),
    ('ASL',  0x78, 0x68),
    ('ASR',  0x77, 0x67),
    ('LSL',  0x78, 0x68),  # same as ASL
    ('LSR',  0x74, 0x64),
]:
    _op(mnem, EXT,  base_ext, 3)
    _op(mnem, IDX,  base_idx, 2)
    _opy(mnem, IDY, base_idx, 3)

# ── Branch instructions (all REL, 2 bytes) ──
for mnem, opcode in [
    ('BRA',   0x20),
    ('BRN',   0x21),
    ('BHI',   0x22),
    ('BLS',   0x23),
    ('BCC',   0x24),  # BHS
    ('BCS',   0x25),  # BLO
    ('BNE',   0x26),
    ('BEQ',   0x27),
    ('BVC',   0x28),
    ('BVS',   0x29),
    ('BPL',   0x2A),
    ('BMI',   0x2B),
    ('BGE',   0x2C),
    ('BLT',   0x2D),
    ('BGT',   0x2E),
    ('BLE',   0x2F),
    ('BHS',   0x24),  # alias for BCC
    ('BLO',   0x25),  # alias for BCS
]:
    _op(mnem, REL, opcode, 2)

# ── BSR (Branch to Subroutine, relative) ──
_op('BSR', REL, 0x8D, 2)

# ── BRSET / BRCLR — 3-operand instructions (direct + mask + rel) ──
# These have special encoding, handled separately in the assembler.
# DIR: opcode, direct_addr, mask, rel_offset  (4 bytes)
# IDX: opcode, index_offset, mask, rel_offset (4 bytes)
_op('BRSET', DIR, 0x12, 4)
_op('BRSET', IDX, 0x1E, 4)
_op('BRCLR', DIR, 0x13, 4)
_op('BRCLR', IDX, 0x1F, 4)

# ── BSET / BCLR — 2-operand bit manipulation (direct + mask) ──
# DIR: opcode, direct_addr, mask  (3 bytes)
# IDX: opcode, index_offset, mask (3 bytes)
_op('BSET', DIR, 0x14, 3)
_op('BSET', IDX, 0x1C, 3)
_op('BCLR', DIR, 0x15, 3)
_op('BCLR', IDX, 0x1D, 3)

# ── JSR ──
_op('JSR', DIR, 0x9D, 2)
_op('JSR', EXT, 0xBD, 3)
_op('JSR', IDX, 0xAD, 2)
_opy('JSR', IDY, 0xAD, 3)

# ── JMP ──
_op('JMP', EXT, 0x7E, 3)
_op('JMP', IDX, 0x6E, 2)
_opy('JMP', IDY, 0x6E, 3)

# ── FCB / FDB / FCC / RMB directives are handled by the assembler, not here ──


# ── Set of mnemonics that take 16-bit immediate (IMM16) ──
IMM16_MNEMONICS = {
    'LDD', 'LDX', 'LDY', 'LDS',
    'ADDD', 'SUBD',
    'CPD', 'CPX', 'CPY',
}

# ── Set of branch mnemonics (use REL addressing) ──
BRANCH_MNEMONICS = {
    'BRA', 'BRN', 'BHI', 'BLS', 'BCC', 'BCS', 'BNE', 'BEQ',
    'BVC', 'BVS', 'BPL', 'BMI', 'BGE', 'BLT', 'BGT', 'BLE',
    'BHS', 'BLO', 'BSR',
}

# ── Bit manipulation instructions with special multi-operand syntax ──
# BSET/BCLR: addr,mask        → opcode, addr, mask (3 bytes DIR / 3 bytes IDX)
# BRSET/BRCLR: addr,mask,target → opcode, addr, mask, rel (4 bytes DIR / 4 bytes IDX)
BIT_SET_CLR_MNEMONICS = {'BSET', 'BCLR'}              # addr,mask
BIT_BRANCH_MNEMONICS = {'BRSET', 'BRCLR'}             # addr,mask,target
BIT_ALL_MNEMONICS = BIT_SET_CLR_MNEMONICS | BIT_BRANCH_MNEMONICS


# ──────────────────────────────────────────────
# Line Parser
# ──────────────────────────────────────────────

@dataclass
class AsmLine:
    """Parsed assembly source line."""
    label: Optional[str] = None
    mnemonic: Optional[str] = None
    operand: Optional[str] = None
    comment: Optional[str] = None
    line_num: int = 0
    raw: str = ""


def _parse_line(line: str, line_num: int) -> AsmLine:
    """Parse one line of assembly into label, mnemonic, operand, comment."""
    result = AsmLine(line_num=line_num, raw=line)

    # Strip comment
    text = line
    semi_pos = -1
    in_string = False
    for i, ch in enumerate(text):
        if ch == "'" or ch == '"':
            in_string = not in_string
        elif ch == ';' and not in_string:
            semi_pos = i
            break
    if semi_pos >= 0:
        result.comment = text[semi_pos+1:].strip()
        text = text[:semi_pos]

    text = text.rstrip()
    if not text:
        return result

    # Check for label: either starts in column 0 (no whitespace) or ends with ':'
    # Local labels start with '.'
    if text and not text[0].isspace():
        # Label at start of line
        parts = text.split(None, 1)
        label_part = parts[0]
        if label_part.endswith(':'):
            label_part = label_part[:-1]
        result.label = label_part
        text = parts[1] if len(parts) > 1 else ""
    elif ':' in text:
        # Check for label with colon anywhere (like ".while1:")
        stripped = text.strip()
        if stripped.endswith(':') and ' ' not in stripped and '\t' not in stripped:
            result.label = stripped[:-1]
            return result

    text = text.strip()
    if not text:
        return result

    # Split mnemonic and operand
    parts = text.split(None, 1)
    result.mnemonic = parts[0].upper()
    if len(parts) > 1:
        result.operand = parts[1].strip()

    return result


# ──────────────────────────────────────────────
# Operand Analysis
# ──────────────────────────────────────────────

def _parse_value(text: str, symbols: Dict[str, int], line_num: int) -> int:
    """Parse a numeric value or symbol reference.
    Supports: $FF (hex), 0xFF, #$FF, %10101010 (binary), 123 (decimal), SYMBOL
    """
    text = text.strip()
    if text.startswith('#'):
        text = text[1:].strip()

    # Hex: $xx or 0xXX
    if text.startswith('$'):
        return int(text[1:], 16)
    if text.startswith('0x') or text.startswith('0X'):
        return int(text, 16)

    # Binary: %xxxxxxxx
    if text.startswith('%'):
        return int(text[1:], 2)

    # Decimal
    if text.isdigit() or (text.startswith('-') and text[1:].isdigit()):
        return int(text)

    # Symbol
    if text in symbols:
        return symbols[text]

    raise AssemblerError(f"Undefined symbol: '{text}'", line_num)


def _classify_operand(mnemonic: str, operand: Optional[str], symbols: Dict[str, int],
                      line_num: int, pass_num: int = 2) -> Tuple[str, ...]:
    """Classify the addressing mode and return (mode, *params).

    Returns:
        (mode, value) for most modes
        (REL, target_addr) for branches
        (INH,) for inherent
    """
    mnem_upper = mnemonic.upper()

    # No operand → inherent
    if operand is None or operand == '':
        return (INH,)

    operand = operand.strip()

    # Branch instructions → REL mode with target label/address
    if mnem_upper in BRANCH_MNEMONICS:
        target = _parse_value(operand, symbols, line_num)
        return (REL, target)

    # Bit manipulation: BSET/BCLR addr,mask  or  BRSET/BRCLR addr,mask,target
    # Direct form:   BSET $46,#$80       — opcode, addr, mask
    # Indexed form:  BSET $00,X,#$04     — opcode, offset, mask  (IDX mode)
    # Also:          BRSET $29,#$80,$8021 — opcode, addr, mask, rel
    # Indexed:       BRSET $00,X,#$04,$target — opcode, offset, mask, rel
    if mnem_upper in BIT_ALL_MNEMONICS:
        parts = [p.strip() for p in operand.split(',')]
        
        # Detect indexed form: second part is X or Y
        is_indexed = len(parts) >= 2 and parts[1].upper() in ('X', 'Y')
        
        if mnem_upper in BIT_SET_CLR_MNEMONICS:
            if is_indexed:
                # BSET/BCLR offset,X,#mask (3 parts)
                if len(parts) != 3:
                    raise AssemblerError(
                        f"{mnem_upper} indexed form requires offset,X,#mask "
                        f"(got {len(parts)} parts)", line_num)
                offset_val = _parse_value(parts[0], symbols, line_num) & 0xFF
                mask_str = parts[2].lstrip('#').lstrip('$')
                mask = _parse_value(parts[2].lstrip('#'), symbols, line_num) & 0xFF
                return (IDX, offset_val, mask)
            else:
                # BSET/BCLR addr,#mask (2 parts, direct)
                if len(parts) != 2:
                    raise AssemblerError(
                        f"{mnem_upper} requires addr,mask (got {len(parts)} parts)",
                        line_num)
                addr = _parse_value(parts[0], symbols, line_num)
                mask = _parse_value(parts[1].lstrip('#'), symbols, line_num) & 0xFF
                return (DIR, addr, mask)
        else:
            # BRSET/BRCLR
            if is_indexed:
                # BRSET/BRCLR offset,X,#mask,target (4 parts)
                if len(parts) != 4:
                    raise AssemblerError(
                        f"{mnem_upper} indexed form requires offset,X,#mask,target "
                        f"(got {len(parts)} parts)", line_num)
                offset_val = _parse_value(parts[0], symbols, line_num) & 0xFF
                mask = _parse_value(parts[2].lstrip('#'), symbols, line_num) & 0xFF
                target = _parse_value(parts[3], symbols, line_num)
                return (IDX, offset_val, mask, target)
            else:
                # BRSET/BRCLR addr,#mask,target (3 parts, direct)
                if len(parts) != 3:
                    raise AssemblerError(
                        f"{mnem_upper} requires addr,mask,target (got {len(parts)} parts)",
                        line_num)
                addr = _parse_value(parts[0], symbols, line_num)
                mask = _parse_value(parts[1].lstrip('#'), symbols, line_num) & 0xFF
                target = _parse_value(parts[2], symbols, line_num)
                return (DIR, addr, mask, target)

    # Immediate: #value
    if operand.startswith('#'):
        val_text = operand[1:].strip()
        val = _parse_value(val_text, symbols, line_num)
        if mnem_upper in IMM16_MNEMONICS:
            return (IMM16, val)
        else:
            return (IMM8, val)

    # Indexed: offset,X or offset,Y
    idx_match = re.match(r'^([\$\%0-9a-fA-Fx\-]*)\s*,\s*([XxYy])$', operand)
    if idx_match:
        offset_str = idx_match.group(1).strip()
        reg = idx_match.group(2).upper()
        if offset_str.startswith('$'):
            offset = int(offset_str[1:], 16)
        elif offset_str.startswith('0x') or offset_str.startswith('0X'):
            offset = int(offset_str, 16)
        elif offset_str == '':
            offset = 0
        else:
            offset = _parse_value(offset_str, symbols, line_num)
        if reg == 'Y':
            return (IDY, offset)
        else:
            return (IDX, offset)

    # Direct or Extended: bare address/symbol
    val = _parse_value(operand, symbols, line_num)

    # For JSR/JMP: always use EXT for forward references and labels
    if mnem_upper in ('JSR', 'JMP'):
        return (EXT, val)

    # Direct vs Extended: use direct page if address fits in $00-$FF
    if 0 <= val <= 0xFF:
        # Check if the mnemonic supports DIR mode
        if mnem_upper in OPCODES and DIR in OPCODES[mnem_upper]:
            return (DIR, val)
    return (EXT, val)


# ──────────────────────────────────────────────
# The Assembler
# ──────────────────────────────────────────────

class Assembler:
    """Two-pass HC11 assembler.

    Usage:
        asm = Assembler()
        binary = asm.assemble(source_text)
        s19 = asm.to_s19()
    """

    def __init__(self):
        self.symbols: Dict[str, int] = {}    # Label/EQU symbol table: name -> address
        self.origin: int = 0                  # Current ORG origin
        self.pc: int = 0                      # Program counter (tracks current address)
        self.binary: bytearray = bytearray()  # Final assembled binary output
        self.base_addr: int = 0               # Lowest address written (start of binary)
        self.errors: List[str] = []           # Accumulated error messages
        self._lines: List[AsmLine] = []       # Parsed assembly lines
        self._segments: List[Tuple[int, bytearray]] = []  # (addr, data) pairs for multi-ORG support

    def assemble(self, source: str) -> bytearray:
        """Assemble source text into binary.

        Two-pass assembly:
          Pass 1: Scan all lines, register labels, and compute instruction sizes
                  to determine the address of every symbol.
          Pass 2: Emit actual binary bytes using the now-complete symbol table.

        Returns the assembled bytes. The base address is stored in self.base_addr.
        """
        self.symbols = {}
        self.errors = []
        self._lines = []
        self._segments = []

        # Parse all lines
        raw_lines = source.split('\n')
        for i, line in enumerate(raw_lines, 1):
            self._lines.append(_parse_line(line, i))

        # Pass 1: resolve labels and compute sizes
        self._pass1()

        if self.errors:
            raise AssemblerError("Pass 1 errors:\n" + "\n".join(self.errors))

        # Pass 2: emit binary
        self._pass2()

        if self.errors:
            raise AssemblerError("Pass 2 errors:\n" + "\n".join(self.errors))

        return self.binary

    def _pass1(self):
        """Pass 1: compute label addresses by tracking PC through all instructions."""
        self.pc = 0
        org_set = False

        for line in self._lines:
            try:
                self._pass1_line(line)
                if line.mnemonic == 'ORG' and not org_set:
                    org_set = True
            except AssemblerError as e:
                self.errors.append(str(e))
            except (ValueError, KeyError) as e:
                self.errors.append(f"Line {line.line_num}: {e}")

    def _pass1_line(self, line: AsmLine):
        """Process one line in pass 1 (size calculation + label registration)."""
        # Register label
        if line.label:
            self.symbols[line.label] = self.pc

        mnem = line.mnemonic
        if mnem is None:
            return

        # ── Directives ──
        if mnem == 'ORG':
            self.pc = _parse_value(line.operand, self.symbols, line.line_num)
            return

        if mnem == 'EQU':
            if line.label:
                self.symbols[line.label] = _parse_value(line.operand, self.symbols, line.line_num)
                # EQU doesn't advance PC, but label was already set to current PC — override
                self.symbols[line.label] = _parse_value(line.operand, self.symbols, line.line_num)
            return

        if mnem == 'FCB':
            # Count comma-separated bytes
            parts = line.operand.split(',') if line.operand else []
            self.pc += len(parts)
            return

        if mnem == 'FDB':
            parts = line.operand.split(',') if line.operand else []
            self.pc += 2 * len(parts)
            return

        if mnem == 'FCC':
            # String data: FCC "string" or FCC 'string'
            text = self._extract_fcc_string(line.operand, line.line_num)
            self.pc += len(text)
            return

        if mnem in ('RMB', 'DS', 'DS.B'):
            count = _parse_value(line.operand, self.symbols, line.line_num)
            self.pc += count
            return

        if mnem in ('DS.W',):
            count = _parse_value(line.operand, self.symbols, line.line_num)
            self.pc += count * 2
            return

        if mnem == 'END':
            return  # End of source — stop processing

        # ── Instructions ──
        if mnem not in OPCODES:
            raise AssemblerError(f"Unknown mnemonic: {mnem}", line.line_num)

        # Estimate instruction size
        size = self._estimate_size(mnem, line.operand, line.line_num)
        self.pc += size

    def _estimate_size(self, mnem: str, operand: Optional[str], line_num: int) -> int:
        """Estimate instruction size in pass 1 (before all symbols are known)."""
        if operand is None or operand.strip() == '':
            if INH in OPCODES[mnem]:
                return OPCODES[mnem][INH][1]
            raise AssemblerError(f"{mnem}: missing operand", line_num)

        operand = operand.strip()

        # Branch → always 2 bytes
        if mnem in BRANCH_MNEMONICS:
            return 2

        # Bit manipulation: detect indexed vs direct, both have fixed sizes
        if mnem in BIT_SET_CLR_MNEMONICS:
            parts = [p.strip() for p in operand.split(',')]
            is_idx = len(parts) >= 2 and parts[1].upper() in ('X', 'Y')
            if is_idx:
                return OPCODES[mnem][IDX][1]  # 3 bytes for indexed BSET/BCLR
            return OPCODES[mnem][DIR][1]  # 3 bytes for direct BSET/BCLR
        if mnem in BIT_BRANCH_MNEMONICS:
            parts = [p.strip() for p in operand.split(',')]
            is_idx = len(parts) >= 2 and parts[1].upper() in ('X', 'Y')
            if is_idx:
                return OPCODES[mnem][IDX][1]  # 4 bytes for indexed BRSET/BRCLR
            return OPCODES[mnem][DIR][1]  # 4 bytes for direct BRSET/BRCLR

        # Immediate
        if operand.startswith('#'):
            if mnem in IMM16_MNEMONICS:
                mode = IMM16
            else:
                mode = IMM8
            if mode in OPCODES[mnem]:
                return OPCODES[mnem][mode][1]

        # Indexed
        idx_match = re.match(r'^([\$\%0-9a-fA-Fx\-]*)\s*,\s*([XxYy])$', operand)
        if idx_match:
            reg = idx_match.group(2).upper()
            mode = IDY if reg == 'Y' else IDX
            if mode in OPCODES[mnem]:
                return OPCODES[mnem][mode][1]

        # Address — try to resolve, but on pass 1 symbols might not exist yet
        # Conservatively: if operand looks like it could be direct page, use DIR size.
        # Otherwise use EXT. If unsure, use EXT (larger).
        try:
            val = _parse_value(operand, self.symbols, line_num)
            if 0 <= val <= 0xFF and DIR in OPCODES.get(mnem, {}):
                if mnem in ('JSR', 'JMP'):
                    # JSR/JMP: prefer EXT for labels
                    return OPCODES[mnem][EXT][1]
                return OPCODES[mnem][DIR][1]
            if EXT in OPCODES.get(mnem, {}):
                return OPCODES[mnem][EXT][1]
        except AssemblerError:
            # Symbol not yet defined — assume EXT (worst case, 3 bytes)
            if EXT in OPCODES.get(mnem, {}):
                return OPCODES[mnem][EXT][1]
            # Must be DIR-only
            if DIR in OPCODES.get(mnem, {}):
                return OPCODES[mnem][DIR][1]

        raise AssemblerError(f"{mnem}: cannot determine size for '{operand}'", line_num)

    def _pass2(self):
        """Pass 2: emit binary for all instructions.

        Uses the fully-populated symbol table from pass 1 to resolve all operand
        references and produce the final machine code bytes.
        """
        self.pc = 0
        self.binary = bytearray()
        self.base_addr = None
        current_segment_start = None
        current_segment_data = bytearray()

        for line in self._lines:
            try:
                self._pass2_line(line)
            except AssemblerError as e:
                self.errors.append(str(e))
            except (ValueError, KeyError) as e:
                self.errors.append(f"Line {line.line_num}: {e}")

        # Finalize — build contiguous binary from origin
        # Find the range of addresses actually written
        if not self._segments:
            return

        min_addr = min(addr for addr, _ in self._segments)
        max_addr = max(addr + len(data) for addr, data in self._segments)
        self.base_addr = min_addr
        self.binary = bytearray(max_addr - min_addr)

        for addr, data in self._segments:
            offset = addr - min_addr
            self.binary[offset:offset+len(data)] = data

    def _pass2_line(self, line: AsmLine):
        """Process one line in pass 2 (emit bytes)."""
        mnem = line.mnemonic
        if mnem is None:
            return

        # ── Directives ──
        if mnem == 'ORG':
            self.pc = _parse_value(line.operand, self.symbols, line.line_num)
            return

        if mnem == 'EQU':
            return  # already handled

        if mnem == 'FCB':
            parts = line.operand.split(',') if line.operand else []
            data = bytearray()
            for p in parts:
                val = _parse_value(p.strip(), self.symbols, line.line_num) & 0xFF
                data.append(val)
            self._emit(data)
            return

        if mnem == 'FDB':
            parts = line.operand.split(',') if line.operand else []
            data = bytearray()
            for p in parts:
                val = _parse_value(p.strip(), self.symbols, line.line_num) & 0xFFFF
                data.append((val >> 8) & 0xFF)
                data.append(val & 0xFF)
            self._emit(data)
            return

        if mnem == 'FCC':
            text = self._extract_fcc_string(line.operand, line.line_num)
            self._emit(bytearray(text.encode('ascii')))
            return

        if mnem in ('RMB', 'DS', 'DS.B'):
            count = _parse_value(line.operand, self.symbols, line.line_num)
            self._emit(bytearray(count))  # zeros
            return

        if mnem in ('DS.W',):
            count = _parse_value(line.operand, self.symbols, line.line_num)
            self._emit(bytearray(count * 2))
            return

        if mnem == 'END':
            return  # End of source

        # ── Instructions ──
        if mnem not in OPCODES:
            raise AssemblerError(f"Unknown mnemonic: {mnem}", line.line_num)

        classified = _classify_operand(mnem, line.operand, self.symbols, line.line_num)
        mode = classified[0]

        # ── Special handling for bit manipulation instructions ──
        if mnem in BIT_SET_CLR_MNEMONICS:
            # BSET/BCLR direct: classified = (DIR, addr, mask)
            # BSET/BCLR indexed: classified = (IDX, offset, mask)
            if mode == IDX:
                _, offset_val, mask = classified
                opcode_bytes, total_size = OPCODES[mnem][IDX]
                data = bytearray(opcode_bytes)
                data.append(offset_val & 0xFF)
                data.append(mask & 0xFF)
            else:
                _, addr, mask = classified
                opcode_bytes, total_size = OPCODES[mnem][DIR]
                data = bytearray(opcode_bytes)
                data.append(addr & 0xFF)
                data.append(mask & 0xFF)
            if len(data) != total_size:
                raise AssemblerError(f"{mnem}: expected {total_size} bytes, got {len(data)}", line.line_num)
            self._emit(data)
            return

        if mnem in BIT_BRANCH_MNEMONICS:
            # BRSET/BRCLR direct: classified = (DIR, addr, mask, target)
            # BRSET/BRCLR indexed: classified = (IDX, offset, mask, target)
            if mode == IDX:
                _, offset_val, mask, target = classified
                opcode_bytes, total_size = OPCODES[mnem][IDX]
                data = bytearray(opcode_bytes)
                data.append(offset_val & 0xFF)
                data.append(mask & 0xFF)
            else:
                _, addr, mask, target = classified
                opcode_bytes, total_size = OPCODES[mnem][DIR]
                data = bytearray(opcode_bytes)
                data.append(addr & 0xFF)
                data.append(mask & 0xFF)
            # Relative offset: target - (PC after instruction)
            offset = target - (self.pc + total_size)
            if offset < -128 or offset > 127:
                raise AssemblerError(
                    f"{mnem}: branch target out of range ({offset} bytes, "
                    f"target=${target:04X}, from=${self.pc:04X})", line.line_num)
            data.append(offset & 0xFF)
            if len(data) != total_size:
                raise AssemblerError(f"{mnem}: expected {total_size} bytes, got {len(data)}", line.line_num)
            self._emit(data)
            return

        if mode not in OPCODES[mnem]:
            raise AssemblerError(
                f"{mnem}: addressing mode {mode} not supported (operand: {line.operand})",
                line.line_num
            )

        opcode_bytes, total_size = OPCODES[mnem][mode]
        data = bytearray(opcode_bytes)

        if mode == INH:
            pass  # just the opcode

        elif mode == IMM8:
            val = classified[1] & 0xFF
            data.append(val)

        elif mode == IMM16:
            val = classified[1] & 0xFFFF
            data.append((val >> 8) & 0xFF)
            data.append(val & 0xFF)

        elif mode == DIR:
            val = classified[1] & 0xFF
            data.append(val)

        elif mode == EXT:
            val = classified[1] & 0xFFFF
            data.append((val >> 8) & 0xFF)
            data.append(val & 0xFF)

        elif mode in (IDX, IDY):
            offset = classified[1] & 0xFF
            data.append(offset)

        elif mode == REL:
            target = classified[1]
            # PC is at the instruction start; after this instruction, PC = self.pc + total_size
            offset = target - (self.pc + total_size)
            if offset < -128 or offset > 127:
                raise AssemblerError(
                    f"{mnem}: branch target out of range ({offset} bytes, "
                    f"target=${target:04X}, from=${self.pc:04X})",
                    line.line_num
                )
            data.append(offset & 0xFF)

        # Verify we emitted the right number of bytes
        if len(data) != total_size:
            raise AssemblerError(
                f"{mnem}: expected {total_size} bytes, got {len(data)}",
                line.line_num
            )

        self._emit(data)

    def _emit(self, data: bytearray):
        """Emit bytes at current PC and advance."""
        self._segments.append((self.pc, data))
        self.pc += len(data)

    def _extract_fcc_string(self, operand: str, line_num: int) -> str:
        """Extract string from FCC directive: FCC "text" or FCC 'text'."""
        if not operand:
            raise AssemblerError("FCC: missing string operand", line_num)
        operand = operand.strip()
        if len(operand) >= 2 and operand[0] in ('"', "'") and operand[-1] == operand[0]:
            return operand[1:-1]
        # Try delimiter-style: FCC /text/
        if len(operand) >= 2 and operand[0] == operand[-1]:
            return operand[1:-1]
        raise AssemblerError(f"FCC: cannot parse string: {operand}", line_num)

    def to_s19(self, header: str = "KingAI") -> str:
        """Convert assembled binary to Motorola S19 format.

        Returns S19 text with S0 header, S1 data records, and S9 end record.
        """
        if self.base_addr is None:
            return ""

        lines = []

        # S0 header record
        header_bytes = header.encode('ascii')
        s0_data = bytearray([0x00, 0x00]) + bytearray(header_bytes)
        s0_count = len(s0_data) + 1  # +1 for checksum
        s0_cksum = self._checksum(bytes([s0_count]) + bytes(s0_data))
        lines.append(f"S0{s0_count:02X}{''.join(f'{b:02X}' for b in s0_data)}{s0_cksum:02X}")

        # S1 data records (max 32 data bytes per record for readability)
        CHUNK = 32
        addr = self.base_addr
        offset = 0
        while offset < len(self.binary):
            chunk_len = min(CHUNK, len(self.binary) - offset)
            chunk = self.binary[offset:offset+chunk_len]

            # S1: record length = address(2) + data(n) + checksum(1)
            s1_count = 2 + chunk_len + 1
            addr_hi = (addr >> 8) & 0xFF
            addr_lo = addr & 0xFF
            record_data = bytes([s1_count, addr_hi, addr_lo]) + bytes(chunk)
            cksum = self._checksum(record_data)

            hex_data = ''.join(f'{b:02X}' for b in record_data)
            lines.append(f"S1{hex_data}{cksum:02X}")

            addr += chunk_len
            offset += chunk_len

        # S9 end record (start address = base_addr or 0)
        start = self.base_addr
        s9_count = 3  # 2 addr bytes + 1 checksum
        s9_data = bytes([s9_count, (start >> 8) & 0xFF, start & 0xFF])
        s9_cksum = self._checksum(s9_data)
        lines.append(f"S9{s9_count:02X}{(start >> 8) & 0xFF:02X}{start & 0xFF:02X}{s9_cksum:02X}")

        return '\n'.join(lines) + '\n'

    @staticmethod
    def _checksum(data: bytes) -> int:
        """Compute S-record checksum: one's complement of sum of bytes, low 8 bits."""
        return (~sum(data)) & 0xFF

    def get_listing(self) -> str:
        """Return a human-readable listing showing address, bytes, and source."""
        # Re-run pass 2 capturing per-line data (simplified approach)
        lines = []
        lines.append(f"{'ADDR':>6}  {'BYTES':<16}  SOURCE")
        lines.append("-" * 60)

        pc = 0
        seg_idx = 0
        for asmline in self._lines:
            if asmline.mnemonic == 'ORG' and asmline.operand:
                try:
                    pc = _parse_value(asmline.operand, self.symbols, asmline.line_num)
                except:
                    pass
                lines.append(f"  ORG ${pc:04X}")
                continue

            if asmline.mnemonic == 'EQU':
                sym_val = self.symbols.get(asmline.label, 0)
                lines.append(f"        {'':16}  {asmline.raw.strip()}")
                continue

            if asmline.mnemonic and asmline.mnemonic in OPCODES:
                # Find corresponding segment data
                if seg_idx < len(self._segments):
                    addr, data = self._segments[seg_idx]
                    hex_str = ' '.join(f'{b:02X}' for b in data)
                    raw = asmline.raw.strip()
                    if len(raw) > 40:
                        raw = raw[:40]
                    lines.append(f"${addr:04X}  {hex_str:<16}  {raw}")
                    seg_idx += 1
                    continue

            # Non-instruction lines (comments, labels, directives)
            raw = asmline.raw.strip()
            if raw:
                lines.append(f"        {'':16}  {raw}")

        return '\n'.join(lines)


# ──────────────────────────────────────────────
# Convenience functions
# ──────────────────────────────────────────────

def assemble(source: str) -> Tuple[bytearray, int]:
    """Assemble source text, return (binary, base_address)."""
    asm = Assembler()
    binary = asm.assemble(source)
    return binary, asm.base_addr


def assemble_to_s19(source: str, header: str = "KingAI") -> str:
    """Assemble source text, return Motorola S19 format string."""
    asm = Assembler()
    asm.assemble(source)
    return asm.to_s19(header=header)
