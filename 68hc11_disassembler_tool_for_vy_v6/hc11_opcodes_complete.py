"""
Complete Motorola HC11 Opcode Dictionary
=========================================

Comprehensive HC11 opcode tables extracted from:
- dis68hc11/Opcodes.h (C++ disassembler)
- ghidra-hc11-lang/HC11.slaspec (Ghidra SLEIGH processor definition)

Covers all single-byte, 2-byte, 3-byte, and prebyte (Page 1/2/3) instructions.

Author: KingAI Automotive Reverse Engineering
Date: November 25, 2025
Purpose: VY V6 Assembly Modding - Complete disassembly support
"""

# Opcode format: (mnemonic, length, addressing_mode, description)
# Length includes opcode byte(s)
# Addressing modes: imp, imm, dir, ext, ind_x, ind_y, rel, bit_dir, bit_ind

# ============================================================================
# SINGLE-BYTE OPCODES (0x00-0xFF)
# ============================================================================

OPCODES_SINGLE = {
    # 0x00-0x0F: Miscellaneous and Control
    0x00: ("TEST", 1, "imp", "Test (HC11 only, not documented)"),
    0x01: ("NOP", 1, "imp", "No Operation"),
    0x02: ("IDIV", 1, "imp", "Integer Divide (D/X -> X remainder D)"),
    0x03: ("FDIV", 1, "imp", "Fractional Divide (D/X -> X remainder D)"),
    0x04: ("LSRD", 1, "imp", "Logical Shift Right Double (D)"),
    0x05: ("ASLD", 1, "imp", "Arithmetic Shift Left Double (D)"),
    0x06: ("TAP", 1, "imp", "Transfer A to CCR"),
    0x07: ("TPA", 1, "imp", "Transfer CCR to A"),
    0x08: ("INX", 1, "imp", "Increment X"),
    0x09: ("DEX", 1, "imp", "Decrement X"),
    0x0A: ("CLV", 1, "imp", "Clear Overflow Flag"),
    0x0B: ("SEV", 1, "imp", "Set Overflow Flag"),
    0x0C: ("CLC", 1, "imp", "Clear Carry Flag"),
    0x0D: ("SEC", 1, "imp", "Set Carry Flag"),
    0x0E: ("CLI", 1, "imp", "Clear Interrupt Mask"),
    0x0F: ("SEI", 1, "imp", "Set Interrupt Mask"),
    
    # 0x10-0x1F: Bit Manipulation and Special
    0x10: ("SBA", 1, "imp", "Subtract B from A (A - B -> A)"),
    0x11: ("CBA", 1, "imp", "Compare B to A (A - B, set flags)"),
    0x12: ("BRSET", 4, "bit_dir", "Branch if Bits Set (direct: addr + mask + rel offset)"),
    0x13: ("BRCLR", 4, "bit_dir", "Branch if Bits Clear (direct: addr + mask + rel offset)"),
    0x14: ("BSET", 3, "bit_dir", "Bit Set (direct: addr + mask)"),
    0x15: ("BCLR", 3, "bit_dir", "Bit Clear (direct: addr + mask)"),
    0x16: ("TAB", 1, "imp", "Transfer A to B"),
    0x17: ("TBA", 1, "imp", "Transfer B to A"),
    0x18: ("PAGE1", 1, "prefix", "Page 1 Prefix (Y-register instructions)"),
    0x19: ("DAA", 1, "imp", "Decimal Adjust A"),
    0x1A: ("PAGE2", 1, "prefix", "Page 2 Prefix (CPD and extended instructions)"),
    0x1B: ("ABA", 1, "imp", "Add B to A (A + B -> A)"),
    0x1C: ("BSET", 3, "bit_idx", "Bit Set (indexed: offset,X + mask)"),
    0x1D: ("BCLR", 3, "bit_idx", "Bit Clear (indexed: offset,X + mask)"),
    0x1E: ("BRSET", 4, "bit_idx", "Branch if Bits Set (indexed: offset,X + mask + rel)"),
    0x1F: ("BRCLR", 4, "bit_idx", "Branch if Bits Clear (indexed: offset,X + mask + rel)"),
    
    # 0x20-0x2F: Branch Instructions
    0x20: ("BRA", 2, "rel", "Branch Always"),
    0x21: ("BRN", 2, "rel", "Branch Never"),
    0x22: ("BHI", 2, "rel", "Branch if Higher (C=0 AND Z=0)"),
    0x23: ("BLS", 2, "rel", "Branch if Lower or Same (C=1 OR Z=1)"),
    0x24: ("BCC", 2, "rel", "Branch if Carry Clear (BHS)"),
    0x25: ("BCS", 2, "rel", "Branch if Carry Set (BLO)"),
    0x26: ("BNE", 2, "rel", "Branch if Not Equal (Z=0)"),
    0x27: ("BEQ", 2, "rel", "Branch if Equal (Z=1)"),
    0x28: ("BVC", 2, "rel", "Branch if Overflow Clear (V=0)"),
    0x29: ("BVS", 2, "rel", "Branch if Overflow Set (V=1)"),
    0x2A: ("BPL", 2, "rel", "Branch if Plus (N=0)"),
    0x2B: ("BMI", 2, "rel", "Branch if Minus (N=1)"),
    0x2C: ("BGE", 2, "rel", "Branch if Greater or Equal (N XOR V = 0)"),
    0x2D: ("BLT", 2, "rel", "Branch if Less Than (N XOR V = 1)"),
    0x2E: ("BGT", 2, "rel", "Branch if Greater Than (Z=0 AND (N XOR V)=0)"),
    0x2F: ("BLE", 2, "rel", "Branch if Less or Equal (Z=1 OR (N XOR V)=1)"),
    
    # 0x30-0x3F: Stack and Special
    0x30: ("TSX", 1, "imp", "Transfer SP to X (SP + 1 -> X)"),
    0x31: ("INS", 1, "imp", "Increment Stack Pointer"),
    0x32: ("PULA", 1, "imp", "Pull A from Stack"),
    0x33: ("PULB", 1, "imp", "Pull B from Stack"),
    0x34: ("DES", 1, "imp", "Decrement Stack Pointer"),
    0x35: ("TXS", 1, "imp", "Transfer X to SP (X - 1 -> SP)"),
    0x36: ("PSHA", 1, "imp", "Push A onto Stack"),
    0x37: ("PSHB", 1, "imp", "Push B onto Stack"),
    0x38: ("PULX", 1, "imp", "Pull X from Stack"),
    0x39: ("RTS", 1, "imp", "Return from Subroutine"),
    0x3A: ("ABX", 1, "imp", "Add B to X (X + B -> X)"),
    0x3B: ("RTI", 1, "imp", "Return from Interrupt"),
    0x3C: ("PSHX", 1, "imp", "Push X onto Stack"),
    0x3D: ("MUL", 1, "imp", "Multiply (A * B -> D)"),
    0x3E: ("WAI", 1, "imp", "Wait for Interrupt"),
    0x3F: ("SWI", 1, "imp", "Software Interrupt"),
    
    # 0x40-0x4F: A Register Operations
    0x40: ("NEGA", 1, "imp", "Negate A (0 - A -> A)"),
    0x43: ("COMA", 1, "imp", "Complement A (~A -> A)"),
    0x44: ("LSRA", 1, "imp", "Logical Shift Right A"),
    0x46: ("RORA", 1, "imp", "Rotate Right A through Carry"),
    0x47: ("ASRA", 1, "imp", "Arithmetic Shift Right A"),
    0x48: ("ASLA", 1, "imp", "Arithmetic Shift Left A (LSLA)"),
    0x49: ("ROLA", 1, "imp", "Rotate Left A through Carry"),
    0x4A: ("DECA", 1, "imp", "Decrement A"),
    0x4C: ("INCA", 1, "imp", "Increment A"),
    0x4D: ("TSTA", 1, "imp", "Test A (A - 0, set flags)"),
    0x4F: ("CLRA", 1, "imp", "Clear A (0 -> A)"),
    
    # 0x50-0x5F: B Register Operations
    0x50: ("NEGB", 1, "imp", "Negate B (0 - B -> B)"),
    0x53: ("COMB", 1, "imp", "Complement B (~B -> B)"),
    0x54: ("LSRB", 1, "imp", "Logical Shift Right B"),
    0x56: ("RORB", 1, "imp", "Rotate Right B through Carry"),
    0x57: ("ASRB", 1, "imp", "Arithmetic Shift Right B"),
    0x58: ("ASLB", 1, "imp", "Arithmetic Shift Left B (LSLB)"),
    0x59: ("ROLB", 1, "imp", "Rotate Left B through Carry"),
    0x5A: ("DECB", 1, "imp", "Decrement B"),
    0x5C: ("INCB", 1, "imp", "Increment B"),
    0x5D: ("TSTB", 1, "imp", "Test B (B - 0, set flags)"),
    0x5F: ("CLRB", 1, "imp", "Clear B (0 -> B)"),
    
    # 0x60-0x6F: Indexed Addressing (Memory Operations)
    0x60: ("NEG", 2, "ind_x", "Negate Memory (indexed X)"),
    0x63: ("COM", 2, "ind_x", "Complement Memory (indexed X)"),
    0x64: ("LSR", 2, "ind_x", "Logical Shift Right Memory (indexed X)"),
    0x66: ("ROR", 2, "ind_x", "Rotate Right Memory (indexed X)"),
    0x67: ("ASR", 2, "ind_x", "Arithmetic Shift Right Memory (indexed X)"),
    0x68: ("ASL", 2, "ind_x", "Arithmetic Shift Left Memory (indexed X)"),
    0x69: ("ROL", 2, "ind_x", "Rotate Left Memory (indexed X)"),
    0x6A: ("DEC", 2, "ind_x", "Decrement Memory (indexed X)"),
    0x6C: ("INC", 2, "ind_x", "Increment Memory (indexed X)"),
    0x6D: ("TST", 2, "ind_x", "Test Memory (indexed X)"),
    0x6E: ("JMP", 2, "ind_x", "Jump (indexed X)"),
    0x6F: ("CLR", 2, "ind_x", "Clear Memory (indexed X)"),
    
    # 0x70-0x7F: Extended Addressing (Memory Operations)
    0x70: ("NEG", 3, "ext", "Negate Memory (extended)"),
    0x73: ("COM", 3, "ext", "Complement Memory (extended)"),
    0x74: ("LSR", 3, "ext", "Logical Shift Right Memory (extended)"),
    0x76: ("ROR", 3, "ext", "Rotate Right Memory (extended)"),
    0x77: ("ASR", 3, "ext", "Arithmetic Shift Right Memory (extended)"),
    0x78: ("ASL", 3, "ext", "Arithmetic Shift Left Memory (extended)"),
    0x79: ("ROL", 3, "ext", "Rotate Left Memory (extended)"),
    0x7A: ("DEC", 3, "ext", "Decrement Memory (extended)"),
    0x7C: ("INC", 3, "ext", "Increment Memory (extended)"),
    0x7D: ("TST", 3, "ext", "Test Memory (extended)"),
    0x7E: ("JMP", 3, "ext", "Jump (extended)"),
    0x7F: ("CLR", 3, "ext", "Clear Memory (extended)"),
    
    # 0x80-0x8F: A Register Immediate Mode
    0x80: ("SUBA", 2, "imm", "Subtract from A (A - M -> A)"),
    0x81: ("CMPA", 2, "imm", "Compare A (A - M, set flags)"),
    0x82: ("SBCA", 2, "imm", "Subtract with Carry from A"),
    0x83: ("SUBD", 3, "imm", "Subtract from D (D - M:M+1 -> D)"),
    0x84: ("ANDA", 2, "imm", "AND A with Memory"),
    0x85: ("BITA", 2, "imm", "Bit Test A (A AND M, set flags)"),
    0x86: ("LDAA", 2, "imm", "Load A"),
    0x88: ("EORA", 2, "imm", "Exclusive OR A with Memory"),
    0x89: ("ADCA", 2, "imm", "Add with Carry to A"),
    0x8A: ("ORAA", 2, "imm", "OR A with Memory"),
    0x8B: ("ADDA", 2, "imm", "Add to A (A + M -> A)"),
    0x8C: ("CPX", 3, "imm", "Compare X (X - M:M+1, set flags)"),
    0x8D: ("BSR", 2, "rel", "Branch to Subroutine"),
    0x8E: ("LDS", 3, "imm", "Load Stack Pointer"),
    0x8F: ("XGDX", 1, "imp", "Exchange D with X"),
    
    # 0x90-0x9F: A Register Direct Mode
    0x90: ("SUBA", 2, "dir", "Subtract from A (direct)"),
    0x91: ("CMPA", 2, "dir", "Compare A (direct)"),
    0x92: ("SBCA", 2, "dir", "Subtract with Carry from A (direct)"),
    0x93: ("SUBD", 2, "dir", "Subtract from D (direct)"),
    0x94: ("ANDA", 2, "dir", "AND A with Memory (direct)"),
    0x95: ("BITA", 2, "dir", "Bit Test A (direct)"),
    0x96: ("LDAA", 2, "dir", "Load A (direct)"),
    0x97: ("STAA", 2, "dir", "Store A (direct)"),
    0x98: ("EORA", 2, "dir", "Exclusive OR A (direct)"),
    0x99: ("ADCA", 2, "dir", "Add with Carry to A (direct)"),
    0x9A: ("ORAA", 2, "dir", "OR A (direct)"),
    0x9B: ("ADDA", 2, "dir", "Add to A (direct)"),
    0x9C: ("CPX", 2, "dir", "Compare X (direct)"),
    0x9D: ("JSR", 2, "dir", "Jump to Subroutine (direct)"),
    0x9E: ("LDS", 2, "dir", "Load Stack Pointer (direct)"),
    0x9F: ("STS", 2, "dir", "Store Stack Pointer (direct)"),
    
    # 0xA0-0xAF: A Register Indexed X Mode
    0xA0: ("SUBA", 2, "ind_x", "Subtract from A (indexed X)"),
    0xA1: ("CMPA", 2, "ind_x", "Compare A (indexed X)"),
    0xA2: ("SBCA", 2, "ind_x", "Subtract with Carry from A (indexed X)"),
    0xA3: ("SUBD", 2, "ind_x", "Subtract from D (indexed X)"),
    0xA4: ("ANDA", 2, "ind_x", "AND A (indexed X)"),
    0xA5: ("BITA", 2, "ind_x", "Bit Test A (indexed X)"),
    0xA6: ("LDAA", 2, "ind_x", "Load A (indexed X)"),
    0xA7: ("STAA", 2, "ind_x", "Store A (indexed X)"),
    0xA8: ("EORA", 2, "ind_x", "Exclusive OR A (indexed X)"),
    0xA9: ("ADCA", 2, "ind_x", "Add with Carry to A (indexed X)"),
    0xAA: ("ORAA", 2, "ind_x", "OR A (indexed X)"),
    0xAB: ("ADDA", 2, "ind_x", "Add to A (indexed X)"),
    0xAC: ("CPX", 2, "ind_x", "Compare X (indexed X)"),
    0xAD: ("JSR", 2, "ind_x", "Jump to Subroutine (indexed X)"),
    0xAE: ("LDS", 2, "ind_x", "Load Stack Pointer (indexed X)"),
    0xAF: ("STS", 2, "ind_x", "Store Stack Pointer (indexed X)"),
    
    # 0xB0-0xBF: A Register Extended Mode
    0xB0: ("SUBA", 3, "ext", "Subtract from A (extended)"),
    0xB1: ("CMPA", 3, "ext", "Compare A (extended)"),
    0xB2: ("SBCA", 3, "ext", "Subtract with Carry from A (extended)"),
    0xB3: ("SUBD", 3, "ext", "Subtract from D (extended)"),
    0xB4: ("ANDA", 3, "ext", "AND A (extended)"),
    0xB5: ("BITA", 3, "ext", "Bit Test A (extended)"),
    0xB6: ("LDAA", 3, "ext", "Load A (extended)"),
    0xB7: ("STAA", 3, "ext", "Store A (extended)"),
    0xB8: ("EORA", 3, "ext", "Exclusive OR A (extended)"),
    0xB9: ("ADCA", 3, "ext", "Add with Carry to A (extended)"),
    0xBA: ("ORAA", 3, "ext", "OR A (extended)"),
    0xBB: ("ADDA", 3, "ext", "Add to A (extended)"),
    0xBC: ("CPX", 3, "ext", "Compare X (extended)"),
    0xBD: ("JSR", 3, "ext", "Jump to Subroutine (extended)"),
    0xBE: ("LDS", 3, "ext", "Load Stack Pointer (extended)"),
    0xBF: ("STS", 3, "ext", "Store Stack Pointer (extended)"),
    
    # 0xC0-0xCF: B Register and D Register Operations
    0xC0: ("SUBB", 2, "imm", "Subtract from B (B - M -> B)"),
    0xC1: ("CMPB", 2, "imm", "Compare B (B - M, set flags)"),
    0xC2: ("SBCB", 2, "imm", "Subtract with Carry from B"),
    0xC3: ("ADDD", 3, "imm", "Add to D (D + M:M+1 -> D)"),
    0xC4: ("ANDB", 2, "imm", "AND B with Memory"),
    0xC5: ("BITB", 2, "imm", "Bit Test B (B AND M, set flags)"),
    0xC6: ("LDAB", 2, "imm", "Load B"),
    0xC8: ("EORB", 2, "imm", "Exclusive OR B with Memory"),
    0xC9: ("ADCB", 2, "imm", "Add with Carry to B"),
    0xCA: ("ORAB", 2, "imm", "OR B with Memory"),
    0xCB: ("ADDB", 2, "imm", "Add to B (B + M -> B)"),
    0xCC: ("LDD", 3, "imm", "Load D (A:B)"),
    0xCD: ("PAGE3", 1, "prefix", "Page 3 Prefix (HC11 extended)"),
    0xCE: ("LDX", 3, "imm", "Load X"),
    0xCF: ("STOP", 1, "imp", "Stop Clocks"),
    
    # 0xD0-0xDF: B Register Direct Mode
    0xD0: ("SUBB", 2, "dir", "Subtract from B (direct)"),
    0xD1: ("CMPB", 2, "dir", "Compare B (direct)"),
    0xD2: ("SBCB", 2, "dir", "Subtract with Carry from B (direct)"),
    0xD3: ("ADDD", 2, "dir", "Add to D (direct)"),
    0xD4: ("ANDB", 2, "dir", "AND B (direct)"),
    0xD5: ("BITB", 2, "dir", "Bit Test B (direct)"),
    0xD6: ("LDAB", 2, "dir", "Load B (direct)"),
    0xD7: ("STAB", 2, "dir", "Store B (direct)"),
    0xD8: ("EORB", 2, "dir", "Exclusive OR B (direct)"),
    0xD9: ("ADCB", 2, "dir", "Add with Carry to B (direct)"),
    0xDA: ("ORAB", 2, "dir", "OR B (direct)"),
    0xDB: ("ADDB", 2, "dir", "Add to B (direct)"),
    0xDC: ("LDD", 2, "dir", "Load D (direct)"),
    0xDD: ("STD", 2, "dir", "Store D (direct)"),
    0xDE: ("LDX", 2, "dir", "Load X (direct)"),
    0xDF: ("STX", 2, "dir", "Store X (direct)"),
    
    # 0xE0-0xEF: B Register Indexed X Mode
    0xE0: ("SUBB", 2, "ind_x", "Subtract from B (indexed X)"),
    0xE1: ("CMPB", 2, "ind_x", "Compare B (indexed X)"),
    0xE2: ("SBCB", 2, "ind_x", "Subtract with Carry from B (indexed X)"),
    0xE3: ("ADDD", 2, "ind_x", "Add to D (indexed X)"),
    0xE4: ("ANDB", 2, "ind_x", "AND B (indexed X)"),
    0xE5: ("BITB", 2, "ind_x", "Bit Test B (indexed X)"),
    0xE6: ("LDAB", 2, "ind_x", "Load B (indexed X)"),
    0xE7: ("STAB", 2, "ind_x", "Store B (indexed X)"),
    0xE8: ("EORB", 2, "ind_x", "Exclusive OR B (indexed X)"),
    0xE9: ("ADCB", 2, "ind_x", "Add with Carry to B (indexed X)"),
    0xEA: ("ORAB", 2, "ind_x", "OR B (indexed X)"),
    0xEB: ("ADDB", 2, "ind_x", "Add to B (indexed X)"),
    0xEC: ("LDD", 2, "ind_x", "Load D (indexed X)"),
    0xED: ("STD", 2, "ind_x", "Store D (indexed X)"),
    0xEE: ("LDX", 2, "ind_x", "Load X (indexed X)"),
    0xEF: ("STX", 2, "ind_x", "Store X (indexed X)"),
    
    # 0xF0-0xFF: B Register Extended Mode
    0xF0: ("SUBB", 3, "ext", "Subtract from B (extended)"),
    0xF1: ("CMPB", 3, "ext", "Compare B (extended)"),
    0xF2: ("SBCB", 3, "ext", "Subtract with Carry from B (extended)"),
    0xF3: ("ADDD", 3, "ext", "Add to D (extended)"),
    0xF4: ("ANDB", 3, "ext", "AND B (extended)"),
    0xF5: ("BITB", 3, "ext", "Bit Test B (extended)"),
    0xF6: ("LDAB", 3, "ext", "Load B (extended)"),
    0xF7: ("STAB", 3, "ext", "Store B (extended)"),
    0xF8: ("EORB", 3, "ext", "Exclusive OR B (extended)"),
    0xF9: ("ADCB", 3, "ext", "Add with Carry to B (extended)"),
    0xFA: ("ORAB", 3, "ext", "OR B (extended)"),
    0xFB: ("ADDB", 3, "ext", "Add to B (extended)"),
    0xFC: ("LDD", 3, "ext", "Load D (extended)"),
    0xFD: ("STD", 3, "ext", "Store D (extended)"),
    0xFE: ("LDX", 3, "ext", "Load X (extended)"),
    0xFF: ("STX", 3, "ext", "Store X (extended)"),
}

# ============================================================================
# PAGE 1 OPCODES (0x18 prefix - Y Register Instructions)
# ============================================================================

OPCODES_PAGE1 = {
    # Y-register instructions (after 0x18 prefix)
    0x08: ("INY", 1, "imp", "Increment Y"),
    0x09: ("DEY", 1, "imp", "Decrement Y"),
    0x1C: ("BSET", 2, "bit_ind_y", "Bit Set (indexed Y + mask)"),
    0x1D: ("BCLR", 2, "bit_ind_y", "Bit Clear (indexed Y + mask)"),
    0x1E: ("BRSET", 3, "bit_ind_y", "Branch if Bits Set (indexed Y + mask + rel)"),
    0x1F: ("BRCLR", 3, "bit_ind_y", "Branch if Bits Clear (indexed Y + mask + rel)"),
    0x30: ("TSY", 1, "imp", "Transfer SP to Y (SP + 1 -> Y)"),
    0x35: ("TYS", 1, "imp", "Transfer Y to SP (Y - 1 -> SP)"),
    0x38: ("PULY", 1, "imp", "Pull Y from Stack"),
    0x3A: ("ABY", 1, "imp", "Add B to Y (Y + B -> Y)"),
    0x3C: ("PSHY", 1, "imp", "Push Y onto Stack"),
    0x60: ("NEG", 2, "ind_y", "Negate Memory (indexed Y)"),
    0x63: ("COM", 2, "ind_y", "Complement Memory (indexed Y)"),
    0x64: ("LSR", 2, "ind_y", "Logical Shift Right Memory (indexed Y)"),
    0x66: ("ROR", 2, "ind_y", "Rotate Right Memory (indexed Y)"),
    0x67: ("ASR", 2, "ind_y", "Arithmetic Shift Right Memory (indexed Y)"),
    0x68: ("ASL", 2, "ind_y", "Arithmetic Shift Left Memory (indexed Y)"),
    0x69: ("ROL", 2, "ind_y", "Rotate Left Memory (indexed Y)"),
    0x6A: ("DEC", 2, "ind_y", "Decrement Memory (indexed Y)"),
    0x6C: ("INC", 2, "ind_y", "Increment Memory (indexed Y)"),
    0x6D: ("TST", 2, "ind_y", "Test Memory (indexed Y)"),
    0x6E: ("JMP", 2, "ind_y", "Jump (indexed Y)"),
    0x6F: ("CLR", 2, "ind_y", "Clear Memory (indexed Y)"),
    0x8C: ("CPY", 3, "imm", "Compare Y (Y - M:M+1, set flags)"),
    0x8F: ("XGDY", 1, "imp", "Exchange D with Y"),
    0x9C: ("CPY", 2, "dir", "Compare Y (direct)"),
    0x9D: ("JSR", 2, "ind_y", "Jump to Subroutine (indexed Y)"),
    0xA0: ("SUBA", 2, "ind_y", "Subtract from A (indexed Y)"),
    0xA1: ("CMPA", 2, "ind_y", "Compare A (indexed Y)"),
    0xA2: ("SBCA", 2, "ind_y", "Subtract with Carry from A (indexed Y)"),
    0xA3: ("SUBD", 2, "ind_y", "Subtract from D (indexed Y)"),
    0xA4: ("ANDA", 2, "ind_y", "AND A (indexed Y)"),
    0xA5: ("BITA", 2, "ind_y", "Bit Test A (indexed Y)"),
    0xA6: ("LDAA", 2, "ind_y", "Load A (indexed Y)"),
    0xA7: ("STAA", 2, "ind_y", "Store A (indexed Y)"),
    0xA8: ("EORA", 2, "ind_y", "Exclusive OR A (indexed Y)"),
    0xA9: ("ADCA", 2, "ind_y", "Add with Carry to A (indexed Y)"),
    0xAA: ("ORAA", 2, "ind_y", "OR A (indexed Y)"),
    0xAB: ("ADDA", 2, "ind_y", "Add to A (indexed Y)"),
    0xAC: ("CPY", 2, "ind_y", "Compare Y (indexed Y)"),
    0xAD: ("JSR", 2, "ind_y", "Jump to Subroutine (indexed Y)"),
    0xAE: ("LDS", 2, "ind_y", "Load Stack Pointer (indexed Y)"),
    0xAF: ("STS", 2, "ind_y", "Store Stack Pointer (indexed Y)"),
    0xBC: ("CPY", 3, "ext", "Compare Y (extended)"),
    0xCE: ("LDY", 3, "imm", "Load Y"),
    0xDE: ("LDY", 2, "dir", "Load Y (direct)"),
    0xDF: ("STY", 2, "dir", "Store Y (direct)"),
    0xE0: ("SUBB", 2, "ind_y", "Subtract from B (indexed Y)"),
    0xE1: ("CMPB", 2, "ind_y", "Compare B (indexed Y)"),
    0xE2: ("SBCB", 2, "ind_y", "Subtract with Carry from B (indexed Y)"),
    0xE3: ("ADDD", 2, "ind_y", "Add to D (indexed Y)"),
    0xE4: ("ANDB", 2, "ind_y", "AND B (indexed Y)"),
    0xE5: ("BITB", 2, "ind_y", "Bit Test B (indexed Y)"),
    0xE6: ("LDAB", 2, "ind_y", "Load B (indexed Y)"),
    0xE7: ("STAB", 2, "ind_y", "Store B (indexed Y)"),
    0xE8: ("EORB", 2, "ind_y", "Exclusive OR B (indexed Y)"),
    0xE9: ("ADCB", 2, "ind_y", "Add with Carry to B (indexed Y)"),
    0xEA: ("ORAB", 2, "ind_y", "OR B (indexed Y)"),
    0xEB: ("ADDB", 2, "ind_y", "Add to B (indexed Y)"),
    0xEC: ("LDD", 2, "ind_y", "Load D (indexed Y)"),
    0xED: ("STD", 2, "ind_y", "Store D (indexed Y)"),
    0xEE: ("LDY", 2, "ind_y", "Load Y (indexed Y)"),
    0xEF: ("STY", 2, "ind_y", "Store Y (indexed Y)"),
    0xFE: ("LDY", 3, "ext", "Load Y (extended)"),
    0xFF: ("STY", 3, "ext", "Store Y (extended)"),
}

# ============================================================================
# PAGE 2 OPCODES (0x1A prefix - Extended Instructions)
# ============================================================================

OPCODES_PAGE2 = {
    # Extended addressing modes and special instructions (after 0x1A prefix)
    0x83: ("CPD", 3, "imm", "Compare D (D - M:M+1, set flags)"),
    0x93: ("CPD", 2, "dir", "Compare D (direct)"),
    0xA3: ("CPD", 2, "ind_x", "Compare D (indexed X)"),
    0xAC: ("CPY", 2, "ind_x", "Compare Y (indexed X)"),
    0xB3: ("CPD", 3, "ext", "Compare D (extended)"),
    0xEE: ("LDY", 2, "ind_x", "Load Y (indexed X)"),
    0xEF: ("STY", 2, "ind_x", "Store Y (indexed X)"),
}

# ============================================================================
# PAGE 3 OPCODES (0xCD prefix - HC11 Extended)
# ============================================================================

OPCODES_PAGE3 = {
    # HC11-specific extended instructions (after 0xCD prefix)
    # Note: Limited usage in most ECU applications
    0xA3: ("CPD", 2, "ind_y", "Compare D (indexed Y)"),
    0xAC: ("CPX", 2, "ind_y", "Compare X (indexed Y)"),
    0xEE: ("LDX", 2, "ind_y", "Load X (indexed Y)"),
    0xEF: ("STX", 2, "ind_y", "Store X (indexed Y)"),
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Tuple



def decode_opcode(data, offset):
    """
    Decode opcode at given offset in binary data.
    
    Args:
        data: Binary data (bytes or bytearray)
        offset: Offset into data
        
    Returns:
        (mnemonic, length, addressing_mode, description, operand_bytes)
    """
    if offset >= len(data):
        return None
    
    opcode = data[offset]
    
    # Check for prebyte (Page 1/2/3)
    if opcode == 0x18:
        # Page 1 - Y-register instructions
        if offset + 1 >= len(data):
            return ("DB", 1, "data", "Data byte (incomplete Page 1)", [opcode])
        next_byte = data[offset + 1]
        if next_byte in OPCODES_PAGE1:
            mnem, length, mode, desc = OPCODES_PAGE1[next_byte]
            total_length = 1 + length  # Include 0x18 prefix
            operand_bytes = list(data[offset:offset + total_length])
            return (mnem, total_length, mode, desc, operand_bytes)
        else:
            return ("DB", 2, "data", f"Unknown Page 1 opcode: 0x18 0x{next_byte:02X}", [opcode, next_byte])
    
    elif opcode == 0x1A:
        # Page 2 - Extended instructions
        if offset + 1 >= len(data):
            return ("DB", 1, "data", "Data byte (incomplete Page 2)", [opcode])
        next_byte = data[offset + 1]
        if next_byte in OPCODES_PAGE2:
            mnem, length, mode, desc = OPCODES_PAGE2[next_byte]
            total_length = 1 + length  # Include 0x1A prefix
            operand_bytes = list(data[offset:offset + total_length])
            return (mnem, total_length, mode, desc, operand_bytes)
        else:
            return ("DB", 2, "data", f"Unknown Page 2 opcode: 0x1A 0x{next_byte:02X}", [opcode, next_byte])
    
    elif opcode == 0xCD:
        # Page 3 - HC11 extended
        if offset + 1 >= len(data):
            return ("DB", 1, "data", "Data byte (incomplete Page 3)", [opcode])
        next_byte = data[offset + 1]
        if next_byte in OPCODES_PAGE3:
            mnem, length, mode, desc = OPCODES_PAGE3[next_byte]
            total_length = 1 + length  # Include 0xCD prefix
            operand_bytes = list(data[offset:offset + total_length])
            return (mnem, total_length, mode, desc, operand_bytes)
        else:
            return ("DB", 2, "data", f"Unknown Page 3 opcode: 0xCD 0x{next_byte:02X}", [opcode, next_byte])
    
    # Single-byte opcode table
    if opcode in OPCODES_SINGLE:
        mnem, length, mode, desc = OPCODES_SINGLE[opcode]
        operand_bytes = list(data[offset:offset + length])
        return (mnem, length, mode, desc, operand_bytes)
    
    # Unknown opcode
    return ("DB", 1, "data", f"Unknown opcode: 0x{opcode:02X}", [opcode])


def format_instruction(mnemonic, operand_bytes, addressing_mode, rom_address):
    """
    Format instruction for disassembly output.
    
    Args:
        mnemonic: Instruction mnemonic (e.g., "LDAA")
        operand_bytes: List of instruction bytes [opcode, operand1, operand2, ...]
        addressing_mode: Addressing mode (imm, dir, ext, ind_x, ind_y, rel, etc.)
        rom_address: ROM address of instruction
        
    Returns:
        Formatted string (e.g., "LDAA #$01", "CMPA $A4", "BNE $ADDF")
    """
    if not operand_bytes:
        return mnemonic
    
    opcode = operand_bytes[0]
    
    # Immediate mode
    if addressing_mode == "imm":
        if len(operand_bytes) == 2:
            return f"{mnemonic} #${operand_bytes[1]:02X}"
        elif len(operand_bytes) == 3:
            return f"{mnemonic} #${operand_bytes[1]:02X}{operand_bytes[2]:02X}"
    
    # Direct mode (zero-page)
    elif addressing_mode == "dir":
        if len(operand_bytes) >= 2:
            return f"{mnemonic} ${operand_bytes[1]:02X}"
    
    # Extended mode
    elif addressing_mode == "ext":
        if len(operand_bytes) >= 3:
            addr = (operand_bytes[1] << 8) | operand_bytes[2]
            return f"{mnemonic} ${addr:04X}"
    
    # Indexed X mode
    elif addressing_mode == "ind_x":
        if len(operand_bytes) >= 2:
            return f"{mnemonic} ${operand_bytes[1]:02X},X"
    
    # Indexed Y mode
    elif addressing_mode == "ind_y":
        if len(operand_bytes) >= 2:
            return f"{mnemonic} ${operand_bytes[1]:02X},Y"
    
    # Relative mode (branches)
    elif addressing_mode == "rel":
        if len(operand_bytes) >= 2:
            offset = operand_bytes[1]
            if offset >= 128:
                offset = offset - 256  # Sign extend
            target = rom_address + len(operand_bytes) + offset
            return f"{mnemonic} ${target:04X}  ; offset={offset:+d}"
    
    # Bit manipulation (direct + mask)
    elif addressing_mode == "bit_dir":
        if len(operand_bytes) == 2:
            return f"{mnemonic} ${operand_bytes[1]:02X}"
        elif len(operand_bytes) == 3:
            addr = operand_bytes[1]
            mask = operand_bytes[2]
            return f"{mnemonic} ${addr:02X}, #${mask:02X}"
    
    # Bit test and branch (direct + mask + rel)
    elif addressing_mode in ["bit_dir", "bit_ind"]:
        if len(operand_bytes) == 3:
            addr = operand_bytes[1]
            if addressing_mode == "bit_ind":
                mask_or_rel = operand_bytes[2]
                return f"{mnemonic} ${addr:02X},X"  # Simplified
            else:
                mask = operand_bytes[2]
                return f"{mnemonic} ${addr:02X}, #${mask:02X}"
        elif len(operand_bytes) == 4:
            addr = operand_bytes[1]
            mask = operand_bytes[2]
            rel = operand_bytes[3]
            if rel >= 128:
                rel = rel - 256
            target = rom_address + 4 + rel
            return f"{mnemonic} ${addr:02X}, #${mask:02X}, ${target:04X}"
    
    # Inherent/Implied (no operands)
    elif addressing_mode == "imp":
        return mnemonic
    
    # Data byte
    elif addressing_mode == "data":
        hex_str = " ".join([f"${b:02X}" for b in operand_bytes])
        return f"DB {hex_str}"
    
    # Default: show raw bytes
    hex_str = " ".join([f"${b:02X}" for b in operand_bytes])
    return f"{mnemonic} {hex_str}"


# ============================================================================
# ECU-SPECIFIC HELPERS
# ============================================================================

def is_rpm_comparison(mnemonic, operand_bytes, addressing_mode):
    """
    Detect if instruction is RPM comparison for rev limiter.
    
    VY V6 uses:
    - CMPA #$A4 (0x81 0xA4) = 6500 RPM comparison
    - CMPA $A4 (0x91 0xA4) = Compare with RPM_LOW_BYTE
    
    Returns: (is_rpm_cmp, threshold_rpm, description)
    """
    RPM_THRESHOLDS = {
        0xA4: 6500,  # 164 decimal * 25 = 6500 RPM
        0xEC: 5900,  # 236 decimal * 25 = 5900 RPM
        0xFA: 6250,  # 250 decimal * 25 = 6250 RPM
    }
    
    if mnemonic in ["CMPA", "CMPB"]:
        if addressing_mode == "imm" and len(operand_bytes) == 2:
            value = operand_bytes[1]
            if value in RPM_THRESHOLDS:
                rpm = RPM_THRESHOLDS[value]
                return (True, rpm, f"RPM comparison: {rpm} RPM")
        elif addressing_mode == "dir" and len(operand_bytes) == 2:
            addr = operand_bytes[1]
            if addr == 0xA4:
                return (True, None, "RPM comparison with RPM_LOW_BYTE ($A4)")
    
    return (False, None, None)


def is_timer_io_access(mnemonic, operand_bytes, addressing_mode):
    """
    Detect Timer/IO register accesses (TCTL1, TOC registers, etc.)
    
    Critical VY V6 registers:
    - 0x1020: TCTL1 (Timer Control 1 - EST output control)
    - 0x1018-0x101F: TOC2-TOC5 (Timer Output Compare - spark timing)
    - 0x1024: TMSK1 (Timer Mask 1 - interrupt enable)
    
    Returns: (is_timer_access, register_name, description)
    """
    TIMER_REGISTERS = {
        0x1020: "TCTL1",
        0x1021: "TCTL2",
        0x1018: "TOC2H",
        0x1019: "TOC2L",
        0x101A: "TOC3H",
        0x101B: "TOC3L",
        0x101C: "TOC4H",
        0x101D: "TOC4L",
        0x101E: "TOC5H",
        0x101F: "TOC5L",
        0x1024: "TMSK1",
        0x1025: "TFLG1",
    }
    
    if addressing_mode == "ext" and len(operand_bytes) >= 3:
        addr = (operand_bytes[1] << 8) | operand_bytes[2]
        if addr in TIMER_REGISTERS:
            reg_name = TIMER_REGISTERS[addr]
            return (True, reg_name, f"Timer/IO access: {reg_name}")
    
    elif addressing_mode == "dir" and len(operand_bytes) >= 2:
        # Some ECUs use direct mode for timer registers
        addr = 0x1000 + operand_bytes[1]  # Assume 0x1000 base
        if addr in TIMER_REGISTERS:
            reg_name = TIMER_REGISTERS[addr]
            return (True, reg_name, f"Timer/IO access: {reg_name} (direct mode)")
    
    return (False, None, None)


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    # Example: Decode some VY V6 instructions
    test_data = bytes([
        0x86, 0xA4,        # LDAA #$A4 (load 164 for 6500 RPM)
        0x91, 0xA4,        # CMPA $A4 (compare with RPM_LOW_BYTE)
        0x26, 0x05,        # BNE +5 (branch if not equal)
        0x18, 0xCE, 0x12, 0x34,  # LDY #$1234 (Page 1 opcode)
        0x12, 0x20, 0x80, 0xFC,  # BRSET $20, #$80, -4 (bit test + branch)
    ])
    
    offset = 0
    rom_base = 0xADD0
    
    print("HC11 Opcode Decoder Test")
    print("=" * 60)
    
    while offset < len(test_data):
        result = decode_opcode(test_data, offset)
        if not result:
            break
        
        mnem, length, mode, desc, operand_bytes = result
        rom_addr = rom_base + offset
        instr = format_instruction(mnem, operand_bytes, mode, rom_addr)
        
        # Check for ECU-specific patterns
        is_rpm, rpm, rpm_desc = is_rpm_comparison(mnem, operand_bytes, mode)
        is_timer, timer_reg, timer_desc = is_timer_io_access(mnem, operand_bytes, mode)
        
        # Print disassembly
        hex_bytes = " ".join([f"{b:02X}" for b in operand_bytes])
        print(f"${rom_addr:04X}: {hex_bytes:12s} {instr:30s} ; {desc}")
        
        if is_rpm:
            print(f"        {'':12s} {'':30s} * {rpm_desc}")
        if is_timer:
            print(f"        {'':12s} {'':30s} * {timer_desc}")
        
        offset += length
    
    print("\nTotal opcodes in tables:")
    print(f"  Single-byte: {len(OPCODES_SINGLE)}")
    print(f"  Page 1 (0x18): {len(OPCODES_PAGE1)}")
    print(f"  Page 2 (0x1A): {len(OPCODES_PAGE2)}")
    print(f"  Page 3 (0xCD): {len(OPCODES_PAGE3)}")
    print(f"  TOTAL: {len(OPCODES_SINGLE) + len(OPCODES_PAGE1) + len(OPCODES_PAGE2) + len(OPCODES_PAGE3)}")
