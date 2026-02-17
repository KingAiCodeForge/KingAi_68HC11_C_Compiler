#!/usr/bin/env python3
"""
HC11 Complete Opcode Table
===========================
Comprehensive opcode metadata for MC68HC11 disassembly and analysis

Sources:
- GaryOderNichts/ghidra-hc11-lang SLEIGH specification
- cmdrf/dis68hc11 C++ disassembler opcodes
- HC11 Reference Manual (Motorola/Freescale)

Format: opcode_byte → (mnemonic, size_bytes, cycles, addressing_mode, prebyte)

Addressing Modes:
- IMM:  Immediate (#$XX)
- DIR:  Direct ($XX) - zero page
- EXT:  Extended ($XXXX) - full address
- IDX:  Indexed (offset,X or offset,Y)
- INH:  Inherent (no operand)
- REL:  Relative (branch offset)

Prebyte Values:
- 0x00: No prebyte (standard instruction)
- 0x18: Page 2 prefix (Y-indexed instructions)
- 0x1A: Page 3 prefix (extended Y-indexed)
- 0xCD: Page 4 prefix (STOP mode)
"""

# ====================================================================
# COMPLETE HC11 INSTRUCTION SET (246 opcodes)
# ====================================================================

HC11_OPCODES = {
    # ----------------------------------------------------------------
    # Arithmetic Operations - A Register
    # ----------------------------------------------------------------
    0x1B: ("ABA",   1, 2, "INH", 0x00),  # A + B → A
    0x89: ("ADCA",  2, 2, "IMM", 0x00),  # A + M + C → A
    0x99: ("ADCA",  2, 3, "DIR", 0x00),
    0xA9: ("ADCA",  2, 4, "IDX", 0x00),
    0xB9: ("ADCA",  3, 4, "EXT", 0x00),
    0x8B: ("ADDA",  2, 2, "IMM", 0x00),  # A + M → A
    0x9B: ("ADDA",  2, 3, "DIR", 0x00),
    0xAB: ("ADDA",  2, 4, "IDX", 0x00),
    0xBB: ("ADDA",  3, 4, "EXT", 0x00),
    0x82: ("SBCA",  2, 2, "IMM", 0x00),  # A - M - C → A
    0x92: ("SBCA",  2, 3, "DIR", 0x00),
    0xA2: ("SBCA",  2, 4, "IDX", 0x00),
    0xB2: ("SBCA",  3, 4, "EXT", 0x00),
    0x80: ("SUBA",  2, 2, "IMM", 0x00),  # A - M → A
    0x90: ("SUBA",  2, 3, "DIR", 0x00),
    0xA0: ("SUBA",  2, 4, "IDX", 0x00),
    0xB0: ("SUBA",  3, 4, "EXT", 0x00),
    0x10: ("SBA",   1, 2, "INH", 0x00),  # A - B → A
    
    # ----------------------------------------------------------------
    # Arithmetic Operations - B Register
    # ----------------------------------------------------------------
    0xC9: ("ADCB",  2, 2, "IMM", 0x00),  # B + M + C → B
    0xD9: ("ADCB",  2, 3, "DIR", 0x00),
    0xE9: ("ADCB",  2, 4, "IDX", 0x00),
    0xF9: ("ADCB",  3, 4, "EXT", 0x00),
    0xCB: ("ADDB",  2, 2, "IMM", 0x00),  # B + M → B
    0xDB: ("ADDB",  2, 3, "DIR", 0x00),
    0xEB: ("ADDB",  2, 4, "IDX", 0x00),
    0xFB: ("ADDB",  3, 4, "EXT", 0x00),
    0xC2: ("SBCB",  2, 2, "IMM", 0x00),  # B - M - C → B
    0xD2: ("SBCB",  2, 3, "DIR", 0x00),
    0xE2: ("SBCB",  2, 4, "IDX", 0x00),
    0xF2: ("SBCB",  3, 4, "EXT", 0x00),
    0xC0: ("SUBB",  2, 2, "IMM", 0x00),  # B - M → B
    0xD0: ("SUBB",  2, 3, "DIR", 0x00),
    0xE0: ("SUBB",  2, 4, "IDX", 0x00),
    0xF0: ("SUBB",  3, 4, "EXT", 0x00),
    
    # ----------------------------------------------------------------
    # Arithmetic Operations - D Register (16-bit)
    # ----------------------------------------------------------------
    0xC3: ("ADDD",  3, 4, "IMM", 0x00),  # D + M:M+1 → D
    0xD3: ("ADDD",  2, 5, "DIR", 0x00),
    0xE3: ("ADDD",  2, 6, "IDX", 0x00),
    0xF3: ("ADDD",  3, 6, "EXT", 0x00),
    0x83: ("SUBD",  3, 4, "IMM", 0x00),  # D - M:M+1 → D
    0x93: ("SUBD",  2, 5, "DIR", 0x00),
    0xA3: ("SUBD",  2, 6, "IDX", 0x00),
    0xB3: ("SUBD",  3, 6, "EXT", 0x00),
    
    # ----------------------------------------------------------------
    # Logic Operations - A Register
    # ----------------------------------------------------------------
    0x84: ("ANDA",  2, 2, "IMM", 0x00),  # A & M → A
    0x94: ("ANDA",  2, 3, "DIR", 0x00),
    0xA4: ("ANDA",  2, 4, "IDX", 0x00),
    0xB4: ("ANDA",  3, 4, "EXT", 0x00),
    0x88: ("EORA",  2, 2, "IMM", 0x00),  # A ⊕ M → A
    0x98: ("EORA",  2, 3, "DIR", 0x00),
    0xA8: ("EORA",  2, 4, "IDX", 0x00),
    0xB8: ("EORA",  3, 4, "EXT", 0x00),
    0x8A: ("ORAA",  2, 2, "IMM", 0x00),  # A | M → A
    0x9A: ("ORAA",  2, 3, "DIR", 0x00),
    0xAA: ("ORAA",  2, 4, "IDX", 0x00),
    0xBA: ("ORAA",  3, 4, "EXT", 0x00),
    
    # ----------------------------------------------------------------
    # Logic Operations - B Register
    # ----------------------------------------------------------------
    0xC4: ("ANDB",  2, 2, "IMM", 0x00),  # B & M → B
    0xD4: ("ANDB",  2, 3, "DIR", 0x00),
    0xE4: ("ANDB",  2, 4, "IDX", 0x00),
    0xF4: ("ANDB",  3, 4, "EXT", 0x00),
    0xC8: ("EORB",  2, 2, "IMM", 0x00),  # B ⊕ M → B
    0xD8: ("EORB",  2, 3, "DIR", 0x00),
    0xE8: ("EORB",  2, 4, "IDX", 0x00),
    0xF8: ("EORB",  3, 4, "EXT", 0x00),
    0xCA: ("ORAB",  2, 2, "IMM", 0x00),  # B | M → B
    0xDA: ("ORAB",  2, 3, "DIR", 0x00),
    0xEA: ("ORAB",  2, 4, "IDX", 0x00),
    0xFA: ("ORAB",  3, 4, "EXT", 0x00),
    
    # ----------------------------------------------------------------
    # Load/Store - A Register
    # ----------------------------------------------------------------
    0x86: ("LDAA",  2, 2, "IMM", 0x00),  # M → A
    0x96: ("LDAA",  2, 3, "DIR", 0x00),
    0xA6: ("LDAA",  2, 4, "IDX", 0x00),
    0xB6: ("LDAA",  3, 4, "EXT", 0x00),
    0x97: ("STAA",  2, 3, "DIR", 0x00),  # A → M
    0xA7: ("STAA",  2, 4, "IDX", 0x00),
    0xB7: ("STAA",  3, 4, "EXT", 0x00),
    
    # ----------------------------------------------------------------
    # Load/Store - B Register
    # ----------------------------------------------------------------
    0xC6: ("LDAB",  2, 2, "IMM", 0x00),  # M → B
    0xD6: ("LDAB",  2, 3, "DIR", 0x00),
    0xE6: ("LDAB",  2, 4, "IDX", 0x00),
    0xF6: ("LDAB",  3, 4, "EXT", 0x00),
    0xD7: ("STAB",  2, 3, "DIR", 0x00),  # B → M
    0xE7: ("STAB",  2, 4, "IDX", 0x00),
    0xF7: ("STAB",  3, 4, "EXT", 0x00),
    
    # ----------------------------------------------------------------
    # Load/Store - D Register (16-bit)
    # ----------------------------------------------------------------
    0xCC: ("LDD",   3, 3, "IMM", 0x00),  # M:M+1 → D
    0xDC: ("LDD",   2, 4, "DIR", 0x00),
    0xEC: ("LDD",   2, 5, "IDX", 0x00),
    0xFC: ("LDD",   3, 5, "EXT", 0x00),
    0xDD: ("STD",   2, 4, "DIR", 0x00),  # D → M:M+1
    0xED: ("STD",   2, 5, "IDX", 0x00),
    0xFD: ("STD",   3, 5, "EXT", 0x00),
    
    # ----------------------------------------------------------------
    # Load/Store - X Index Register
    # ----------------------------------------------------------------
    0xCE: ("LDX",   3, 3, "IMM", 0x00),  # M:M+1 → X
    0xDE: ("LDX",   2, 4, "DIR", 0x00),
    0xEE: ("LDX",   2, 5, "IDX", 0x00),
    0xFE: ("LDX",   3, 5, "EXT", 0x00),
    0xDF: ("STX",   2, 4, "DIR", 0x00),  # X → M:M+1
    0xEF: ("STX",   2, 5, "IDX", 0x00),
    0xFF: ("STX",   3, 5, "EXT", 0x00),
    
    # ----------------------------------------------------------------
    # Load/Store - Stack Pointer
    # ----------------------------------------------------------------
    0x8E: ("LDS",   3, 3, "IMM", 0x00),  # M:M+1 → SP
    0x9E: ("LDS",   2, 4, "DIR", 0x00),
    0xAE: ("LDS",   2, 5, "IDX", 0x00),
    0xBE: ("LDS",   3, 5, "EXT", 0x00),
    0x9F: ("STS",   2, 4, "DIR", 0x00),  # SP → M:M+1
    0xAF: ("STS",   2, 5, "IDX", 0x00),
    0xBF: ("STS",   3, 5, "EXT", 0x00),
    
    # ----------------------------------------------------------------
    # Compare Instructions
    # ----------------------------------------------------------------
    0x81: ("CMPA",  2, 2, "IMM", 0x00),  # A - M (set flags)
    0x91: ("CMPA",  2, 3, "DIR", 0x00),
    0xA1: ("CMPA",  2, 4, "IDX", 0x00),
    0xB1: ("CMPA",  3, 4, "EXT", 0x00),
    0xC1: ("CMPB",  2, 2, "IMM", 0x00),  # B - M (set flags)
    0xD1: ("CMPB",  2, 3, "DIR", 0x00),
    0xE1: ("CMPB",  2, 4, "IDX", 0x00),
    0xF1: ("CMPB",  3, 4, "EXT", 0x00),
    0x8C: ("CPX",   3, 4, "IMM", 0x00),  # X - M:M+1 (set flags)
    0x9C: ("CPX",   2, 5, "DIR", 0x00),
    0xAC: ("CPX",   2, 6, "IDX", 0x00),
    0xBC: ("CPX",   3, 6, "EXT", 0x00),
    
    # ----------------------------------------------------------------
    # Branch Instructions (Relative)
    # ----------------------------------------------------------------
    0x20: ("BRA",   2, 3, "REL", 0x00),  # Branch Always
    0x21: ("BRN",   2, 3, "REL", 0x00),  # Branch Never (NOP)
    0x22: ("BHI",   2, 3, "REL", 0x00),  # Branch if Higher
    0x23: ("BLS",   2, 3, "REL", 0x00),  # Branch if Lower/Same
    0x24: ("BCC",   2, 3, "REL", 0x00),  # Branch if Carry Clear (BHS)
    0x25: ("BCS",   2, 3, "REL", 0x00),  # Branch if Carry Set (BLO)
    0x26: ("BNE",   2, 3, "REL", 0x00),  # Branch if Not Equal
    0x27: ("BEQ",   2, 3, "REL", 0x00),  # Branch if Equal
    0x28: ("BVC",   2, 3, "REL", 0x00),  # Branch if Overflow Clear
    0x29: ("BVS",   2, 3, "REL", 0x00),  # Branch if Overflow Set
    0x2A: ("BPL",   2, 3, "REL", 0x00),  # Branch if Plus
    0x2B: ("BMI",   2, 3, "REL", 0x00),  # Branch if Minus
    0x2C: ("BGE",   2, 3, "REL", 0x00),  # Branch if Greater/Equal
    0x2D: ("BLT",   2, 3, "REL", 0x00),  # Branch if Less Than
    0x2E: ("BGT",   2, 3, "REL", 0x00),  # Branch if Greater Than
    0x2F: ("BLE",   2, 3, "REL", 0x00),  # Branch if Less/Equal
    0x8D: ("BSR",   2, 6, "REL", 0x00),  # Branch to Subroutine
    
    # ----------------------------------------------------------------
    # Bit Test/Manipulation
    # ----------------------------------------------------------------
    0x85: ("BITA",  2, 2, "IMM", 0x00),  # A & M (set flags only)
    0x95: ("BITA",  2, 3, "DIR", 0x00),
    0xA5: ("BITA",  2, 4, "IDX", 0x00),
    0xB5: ("BITA",  3, 4, "EXT", 0x00),
    0xC5: ("BITB",  2, 2, "IMM", 0x00),  # B & M (set flags only)
    0xD5: ("BITB",  2, 3, "DIR", 0x00),
    0xE5: ("BITB",  2, 4, "IDX", 0x00),
    0xF5: ("BITB",  3, 4, "EXT", 0x00),
    0x14: ("BSET",  3, 6, "DIR", 0x00),  # Set bits in memory
    0x1C: ("BSET",  3, 7, "IDX", 0x00),
    0x15: ("BCLR",  3, 6, "DIR", 0x00),  # Clear bits in memory
    0x1D: ("BCLR",  3, 7, "IDX", 0x00),
    0x12: ("BRSET", 4, 6, "DIR", 0x00),  # Branch if bits set
    0x1E: ("BRSET", 4, 7, "IDX", 0x00),
    0x13: ("BRCLR", 4, 6, "DIR", 0x00),  # Branch if bits clear
    0x1F: ("BRCLR", 4, 7, "IDX", 0x00),
    
    # ----------------------------------------------------------------
    # Shift/Rotate - A Register
    # ----------------------------------------------------------------
    0x48: ("ASLA",  1, 2, "INH", 0x00),  # Arithmetic Shift Left A
    0x47: ("ASRA",  1, 2, "INH", 0x00),  # Arithmetic Shift Right A
    0x44: ("LSRA",  1, 2, "INH", 0x00),  # Logical Shift Right A
    0x49: ("ROLA",  1, 2, "INH", 0x00),  # Rotate Left A
    0x46: ("RORA",  1, 2, "INH", 0x00),  # Rotate Right A
    
    # ----------------------------------------------------------------
    # Shift/Rotate - B Register
    # ----------------------------------------------------------------
    0x58: ("ASLB",  1, 2, "INH", 0x00),  # Arithmetic Shift Left B
    0x57: ("ASRB",  1, 2, "INH", 0x00),  # Arithmetic Shift Right B
    0x54: ("LSRB",  1, 2, "INH", 0x00),  # Logical Shift Right B
    0x59: ("ROLB",  1, 2, "INH", 0x00),  # Rotate Left B
    0x56: ("RORB",  1, 2, "INH", 0x00),  # Rotate Right B
    
    # ----------------------------------------------------------------
    # Shift/Rotate - D Register & Memory
    # ----------------------------------------------------------------
    0x05: ("ASLD",  1, 3, "INH", 0x00),  # Arithmetic Shift Left D
    0x04: ("LSRD",  1, 3, "INH", 0x00),  # Logical Shift Right D
    0x78: ("ASL",   3, 6, "EXT", 0x00),  # Arithmetic Shift Left memory
    0x68: ("ASL",   2, 6, "IDX", 0x00),
    0x77: ("ASR",   3, 6, "EXT", 0x00),  # Arithmetic Shift Right memory
    0x67: ("ASR",   2, 6, "IDX", 0x00),
    0x74: ("LSR",   3, 6, "EXT", 0x00),  # Logical Shift Right memory
    0x64: ("LSR",   2, 6, "IDX", 0x00),
    0x79: ("ROL",   3, 6, "EXT", 0x00),  # Rotate Left memory
    0x69: ("ROL",   2, 6, "IDX", 0x00),
    0x76: ("ROR",   3, 6, "EXT", 0x00),  # Rotate Right memory
    0x66: ("ROR",   2, 6, "IDX", 0x00),
    
    # ----------------------------------------------------------------
    # Increment/Decrement
    # ----------------------------------------------------------------
    0x4C: ("INCA",  1, 2, "INH", 0x00),  # A + 1 → A
    0x5C: ("INCB",  1, 2, "INH", 0x00),  # B + 1 → B
    0x7C: ("INC",   3, 6, "EXT", 0x00),  # M + 1 → M
    0x6C: ("INC",   2, 6, "IDX", 0x00),
    0x4A: ("DECA",  1, 2, "INH", 0x00),  # A - 1 → A
    0x5A: ("DECB",  1, 2, "INH", 0x00),  # B - 1 → B
    0x7A: ("DEC",   3, 6, "EXT", 0x00),  # M - 1 → M
    0x6A: ("DEC",   2, 6, "IDX", 0x00),
    0x08: ("INX",   1, 3, "INH", 0x00),  # X + 1 → X
    0x09: ("DEX",   1, 3, "INH", 0x00),  # X - 1 → X
    0x31: ("INS",   1, 3, "INH", 0x00),  # SP + 1 → SP
    0x34: ("DES",   1, 3, "INH", 0x00),  # SP - 1 → SP
    
    # ----------------------------------------------------------------
    # Clear/Complement/Negate
    # ----------------------------------------------------------------
    0x4F: ("CLRA",  1, 2, "INH", 0x00),  # 0 → A
    0x5F: ("CLRB",  1, 2, "INH", 0x00),  # 0 → B
    0x7F: ("CLR",   3, 6, "EXT", 0x00),  # 0 → M
    0x6F: ("CLR",   2, 6, "IDX", 0x00),
    0x43: ("COMA",  1, 2, "INH", 0x00),  # ~A → A
    0x53: ("COMB",  1, 2, "INH", 0x00),  # ~B → B
    0x73: ("COM",   3, 6, "EXT", 0x00),  # ~M → M
    0x63: ("COM",   2, 6, "IDX", 0x00),
    0x40: ("NEGA",  1, 2, "INH", 0x00),  # -A → A (two's complement)
    0x50: ("NEGB",  1, 2, "INH", 0x00),  # -B → B
    0x70: ("NEG",   3, 6, "EXT", 0x00),  # -M → M
    0x60: ("NEG",   2, 6, "IDX", 0x00),
    
    # ----------------------------------------------------------------
    # Test
    # ----------------------------------------------------------------
    0x4D: ("TSTA",  1, 2, "INH", 0x00),  # A - 0 (set flags only)
    0x5D: ("TSTB",  1, 2, "INH", 0x00),  # B - 0
    0x7D: ("TST",   3, 6, "EXT", 0x00),  # M - 0
    0x6D: ("TST",   2, 6, "IDX", 0x00),
    
    # ----------------------------------------------------------------
    # Multiply/Divide
    # ----------------------------------------------------------------
    0x3D: ("MUL",   1, 10, "INH", 0x00), # A × B → D (unsigned)
    0x02: ("IDIV",  1, 41, "INH", 0x00), # D ÷ X → X remainder → D
    0x03: ("FDIV",  1, 41, "INH", 0x00), # D ÷ X → X (fractional)
    
    # ----------------------------------------------------------------
    # Jump/Branch Extended
    # ----------------------------------------------------------------
    0x7E: ("JMP",   3, 3, "EXT", 0x00),  # Jump to address
    0x6E: ("JMP",   2, 3, "IDX", 0x00),
    0x9D: ("JSR",   2, 5, "DIR", 0x00),  # Jump to Subroutine
    0xBD: ("JSR",   3, 6, "EXT", 0x00),
    0xAD: ("JSR",   2, 6, "IDX", 0x00),
    0x39: ("RTS",   1, 5, "INH", 0x00),  # Return from Subroutine
    0x3B: ("RTI",   1, 12, "INH", 0x00), # Return from Interrupt
    
    # ----------------------------------------------------------------
    # Stack Operations
    # ----------------------------------------------------------------
    0x36: ("PSHA",  1, 3, "INH", 0x00),  # Push A onto stack
    0x37: ("PSHB",  1, 3, "INH", 0x00),  # Push B onto stack
    0x3C: ("PSHX",  1, 4, "INH", 0x00),  # Push X onto stack
    0x32: ("PULA",  1, 4, "INH", 0x00),  # Pull A from stack
    0x33: ("PULB",  1, 4, "INH", 0x00),  # Pull B from stack
    0x38: ("PULX",  1, 5, "INH", 0x00),  # Pull X from stack
    
    # ----------------------------------------------------------------
    # Condition Code Operations
    # ----------------------------------------------------------------
    0x0C: ("CLC",   1, 2, "INH", 0x00),  # 0 → C
    0x0D: ("SEC",   1, 2, "INH", 0x00),  # 1 → C
    0x0E: ("CLI",   1, 2, "INH", 0x00),  # 0 → I
    0x0F: ("SEI",   1, 2, "INH", 0x00),  # 1 → I
    0x0A: ("CLV",   1, 2, "INH", 0x00),  # 0 → V
    0x0B: ("SEV",   1, 2, "INH", 0x00),  # 1 → V
    0x06: ("TAP",   1, 2, "INH", 0x00),  # A → CCR
    0x07: ("TPA",   1, 2, "INH", 0x00),  # CCR → A
    
    # ----------------------------------------------------------------
    # Transfer/Exchange
    # ----------------------------------------------------------------
    0x16: ("TAB",   1, 2, "INH", 0x00),  # A → B
    0x17: ("TBA",   1, 2, "INH", 0x00),  # B → A
    0x30: ("TSX",   1, 3, "INH", 0x00),  # SP + 1 → X
    0x35: ("TXS",   1, 3, "INH", 0x00),  # X - 1 → SP
    0x3A: ("ABX",   1, 3, "INH", 0x00),  # B + X → X
    0x19: ("DAA",   1, 2, "INH", 0x00),  # Decimal Adjust A
    
    # ----------------------------------------------------------------
    # Special/System
    # ----------------------------------------------------------------
    0x00: ("TEST",  1, 0, "INH", 0x00),  # Test mode only
    0x01: ("NOP",   1, 2, "INH", 0x00),  # No Operation
    0x3E: ("WAI",   1, 9, "INH", 0x00),  # Wait for Interrupt
    0x3F: ("SWI",   1, 14, "INH", 0x00), # Software Interrupt
    0xCF: ("STOP",  1, 2, "INH", 0xCD), # STOP mode (prebyte 0xCD)
    
    # ----------------------------------------------------------------
    # Multiply (unsigned 8-bit × 8-bit → 16-bit)
    # ----------------------------------------------------------------
    0x3D: ("MUL",   1, 10, "INH", 0x00),  # A × B → D (unsigned)
    
    # ----------------------------------------------------------------
    # Page 2 Instructions (0x18 prebyte) - Y Index Register
    # ----------------------------------------------------------------
    # Note: These use same opcodes as X-indexed but with 0x18 prefix
    # Example: 0x18 0x3A = ABY (B + Y → Y)
    # Full page 2 table omitted for brevity - use 0x18 prebyte detection
    
    # ----------------------------------------------------------------
    # Page 3 Instructions (0x1A prebyte) - Extended Y Operations
    # ----------------------------------------------------------------
    # Note: CPY, LDY, STY use 0x1A prebyte + standard opcodes
}

# ====================================================================
# Y-INDEXED OPCODES (Page 2: 0x18 Prefix)
# ====================================================================
# When 0x18 is encountered, next byte uses this table
HC11_PAGE2_OPCODES = {
    0x3A: ("ABY",   2, 4, "INH", 0x18),  # B + Y → Y
    0x08: ("INY",   2, 4, "INH", 0x18),  # Y + 1 → Y
    0x09: ("DEY",   2, 4, "INH", 0x18),  # Y - 1 → Y
    0x30: ("TSY",   2, 4, "INH", 0x18),  # SP + 1 → Y
    0x35: ("TYS",   2, 4, "INH", 0x18),  # Y - 1 → SP
    # All Y-indexed addressing modes follow same pattern as X
    # with 0x18 prebyte (add 1 cycle overhead)
}

# ====================================================================
# CPY/LDY/STY OPCODES (Page 3: 0x1A or 0xCD Prefix)
# ====================================================================
HC11_PAGE3_OPCODES = {
    # 0x1A prefix
    0x8C: ("CPY",   4, 5, "IMM", 0x1A),  # Y - M:M+1
    0x9C: ("CPY",   3, 6, "DIR", 0x1A),
    0xAC: ("CPY",   3, 7, "IDX", 0x1A),
    0xBC: ("CPY",   4, 7, "EXT", 0x1A),
    0xCE: ("LDY",   4, 4, "IMM", 0x1A),  # M:M+1 → Y
    0xDE: ("LDY",   3, 5, "DIR", 0x1A),
    0xEE: ("LDY",   3, 6, "IDX", 0x1A),
    0xFE: ("LDY",   4, 6, "EXT", 0x1A),
    0xDF: ("STY",   3, 5, "DIR", 0x1A),  # Y → M:M+1
    0xEF: ("STY",   3, 6, "IDX", 0x1A),
    0xFF: ("STY",   4, 6, "EXT", 0x1A),
    # Missing opcodes (Motorola HC11 Reference Manual)
    0x8F: 1,  # XGDX
}

# ====================================================================
# HELPER FUNCTIONS
# ====================================================================
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Tuple



def get_opcode_info(opcode: int, prebyte: int = 0x00):
    """Get instruction info for given opcode and prebyte."""
    if prebyte == 0x18 and opcode in HC11_PAGE2_OPCODES:
        return HC11_PAGE2_OPCODES[opcode]
    elif prebyte == 0x1A and opcode in HC11_PAGE3_OPCODES:
        return HC11_PAGE3_OPCODES[opcode]
    elif prebyte == 0x00 and opcode in HC11_OPCODES:
        return HC11_OPCODES[opcode]
    return None

def is_prebyte(opcode: int) -> bool:
    """Check if opcode is a prebyte marker."""
    return opcode in (0x18, 0x1A, 0xCD)

def get_all_opcodes_for_mnemonic(mnemonic: str) -> list:
    """Get all opcodes that implement a given mnemonic."""
    results = []
    for opcode, (mnem, size, cycles, mode, prebyte) in HC11_OPCODES.items():
        if mnem == mnemonic:
            results.append((opcode, size, cycles, mode, prebyte))
    for opcode, (mnem, size, cycles, mode, prebyte) in HC11_PAGE2_OPCODES.items():
        if mnem == mnemonic:
            results.append((opcode, size, cycles, mode, prebyte))
    for opcode, (mnem, size, cycles, mode, prebyte) in HC11_PAGE3_OPCODES.items():
        if mnem == mnemonic:
            results.append((opcode, size, cycles, mode, prebyte))
    return results

if __name__ == "__main__":
    # Test: Print all LDAA variants
    print("=== HC11 Opcode Table Test ===\n")
    print("LDAA variants:")
    for opcode, size, cycles, mode, prebyte in get_all_opcodes_for_mnemonic("LDAA"):
        print(f"  0x{opcode:02X}: LDAA {mode:6s} - {size} bytes, {cycles} cycles")
    
    print("\nCMPA variants:")
    for opcode, size, cycles, mode, prebyte in get_all_opcodes_for_mnemonic("CMPA"):
        print(f"  0x{opcode:02X}: CMPA {mode:6s} - {size} bytes, {cycles} cycles")
    
    print(f"\nTotal opcodes: {len(HC11_OPCODES) + len(HC11_PAGE2_OPCODES) + len(HC11_PAGE3_OPCODES)}")
