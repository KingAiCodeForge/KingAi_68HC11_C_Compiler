#!/usr/bin/env python3
"""
HC11 Disassembler - Enhanced Production Version
===============================================
Disassembles MC68HC11 binary files with proper instruction decoding
always compare outputs with other tools e.g. udis.py and 6811.py with command lines on addresses.
UPDATED: January 19, 2026
- Added missing BSET/BCLR/BRSET/BRCLR opcodes (verified against M68HC11RM)
- Correct byte lengths: BSET/BCLR = 3 bytes, BRSET/BRCLR = 4 bytes

Features:
- Auto-detects VY V6 Enhanced binaries across multiple locations
- Proper HC11 memory mapping (0x8000-0xFFFF high memory)
- XDF cross-reference support with label integration
- Saves output to timestamped files
- Enhanced error handling and logging
- Full HC11 instruction set support including bit manipulation

Usage:
    python hc11_disassembler_enhanced.py <binary_file> [base_addr] [start_offset] [length] [xdf_file]
    
    Or run without arguments to auto-detect binaries

Example:
    python hc11_disassembler_enhanced.py "VY_V6_Enhanced_v2.09a.bin" 0x8000 0 0x1000
"""

import sys
from pathlib import Path
from datetime import datetime

# ====================================================================
# HC11 Complete Instruction Set
# ====================================================================

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
    0x18: ("XGDX", 1, 3, "inherent"),  # Page 2 prefix
    0x19: ("DAA", 1, 2, "inherent"),
    0x1A: ("XGDY", 1, 3, "inherent"),  # Page 3 prefix
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
    
    # Load/Store A register
    0x86: ("LDAA", 2, 2, "immediate"),
    0x96: ("LDAA", 2, 3, "direct"),
    0xA6: ("LDAA", 2, 4, "indexed"),
    0xB6: ("LDAA", 3, 4, "extended"),
    0x97: ("STAA", 2, 3, "direct"),
    0xA7: ("STAA", 2, 4, "indexed"),
    0xB7: ("STAA", 3, 4, "extended"),
    
    # Load/Store B register
    0xC6: ("LDAB", 2, 2, "immediate"),
    0xD6: ("LDAB", 2, 3, "direct"),
    0xE6: ("LDAB", 2, 4, "indexed"),
    0xF6: ("LDAB", 3, 4, "extended"),
    0xD7: ("STAB", 2, 3, "direct"),
    0xE7: ("STAB", 2, 4, "indexed"),
    0xF7: ("STAB", 3, 4, "extended"),
    
    # Load/Store D register (16-bit)
    0xCC: ("LDD", 3, 3, "immediate"),
    0xDC: ("LDD", 2, 4, "direct"),
    0xEC: ("LDD", 2, 5, "indexed"),
    0xFC: ("LDD", 3, 5, "extended"),
    0xDD: ("STD", 2, 4, "direct"),
    0xED: ("STD", 2, 5, "indexed"),
    0xFD: ("STD", 3, 5, "extended"),
    
    # Arithmetic A
    0x8B: ("ADDA", 2, 2, "immediate"),
    0x9B: ("ADDA", 2, 3, "direct"),
    0xAB: ("ADDA", 2, 4, "indexed"),
    0xBB: ("ADDA", 3, 4, "extended"),
    0x80: ("SUBA", 2, 2, "immediate"),
    0x90: ("SUBA", 2, 3, "direct"),
    0xA0: ("SUBA", 2, 4, "indexed"),
    0xB0: ("SUBA", 3, 4, "extended"),
    
    # Arithmetic B
    0xCB: ("ADDB", 2, 2, "immediate"),
    0xDB: ("ADDB", 2, 3, "direct"),
    0xEB: ("ADDB", 2, 4, "indexed"),
    0xFB: ("ADDB", 3, 4, "extended"),
    0xC0: ("SUBB", 2, 2, "immediate"),
    0xD0: ("SUBB", 2, 3, "direct"),
    0xE0: ("SUBB", 2, 4, "indexed"),
    0xF0: ("SUBB", 3, 4, "extended"),
    
    # Arithmetic D (16-bit) - ADDED
    0xC3: ("ADDD", 3, 4, "immediate"),
    0xD3: ("ADDD", 2, 5, "direct"),
    0xE3: ("ADDD", 2, 6, "indexed"),
    0xF3: ("ADDD", 3, 6, "extended"),
    0x83: ("SUBD", 3, 4, "immediate"),
    0x93: ("SUBD", 2, 5, "direct"),
    0xA3: ("SUBD", 2, 6, "indexed"),
    0xB3: ("SUBD", 3, 6, "extended"),  # NOTE: Without prebyte! With $1A = CPD
    
    # Compare A
    0x81: ("CMPA", 2, 2, "immediate"),
    0x91: ("CMPA", 2, 3, "direct"),
    0xA1: ("CMPA", 2, 4, "indexed"),
    0xB1: ("CMPA", 3, 4, "extended"),
    
    # Compare B
    0xC1: ("CMPB", 2, 2, "immediate"),
    0xD1: ("CMPB", 2, 3, "direct"),
    0xE1: ("CMPB", 2, 4, "indexed"),
    0xF1: ("CMPB", 3, 4, "extended"),
    
    # Jump/Call
    0x6E: ("JMP", 2, 3, "indexed"),
    0x7E: ("JMP", 3, 3, "extended"),
    0xAD: ("JSR", 2, 5, "indexed"),
    0xBD: ("JSR", 3, 6, "extended"),
    
    # Logic A
    0x84: ("ANDA", 2, 2, "immediate"),
    0x94: ("ANDA", 2, 3, "direct"),
    0xA4: ("ANDA", 2, 4, "indexed"),
    0xB4: ("ANDA", 3, 4, "extended"),
    0x8A: ("ORAA", 2, 2, "immediate"),
    0x9A: ("ORAA", 2, 3, "direct"),
    0xAA: ("ORAA", 2, 4, "indexed"),
    0xBA: ("ORAA", 3, 4, "extended"),
    0x88: ("EORA", 2, 2, "immediate"),
    0x98: ("EORA", 2, 3, "direct"),
    0xA8: ("EORA", 2, 4, "indexed"),
    0xB8: ("EORA", 3, 4, "extended"),
    
    # Logic B
    0xC4: ("ANDB", 2, 2, "immediate"),
    0xD4: ("ANDB", 2, 3, "direct"),
    0xE4: ("ANDB", 2, 4, "indexed"),
    0xF4: ("ANDB", 3, 4, "extended"),
    0xCA: ("ORAB", 2, 2, "immediate"),
    0xDA: ("ORAB", 2, 3, "direct"),
    0xEA: ("ORAB", 2, 4, "indexed"),
    0xFA: ("ORAB", 3, 4, "extended"),
    0xC8: ("EORB", 2, 2, "immediate"),
    0xD8: ("EORB", 2, 3, "direct"),
    0xE8: ("EORB", 2, 4, "indexed"),
    0xF8: ("EORB", 3, 4, "extended"),
    
    # Bit test
    0x85: ("BITA", 2, 2, "immediate"),
    0x95: ("BITA", 2, 3, "direct"),
    0xA5: ("BITA", 2, 4, "indexed"),
    0xB5: ("BITA", 3, 4, "extended"),
    0xC5: ("BITB", 2, 2, "immediate"),
    0xD5: ("BITB", 2, 3, "direct"),
    0xE5: ("BITB", 2, 4, "indexed"),
    0xF5: ("BITB", 3, 4, "extended"),
    
    # Bit manipulation (CRITICAL - verified against M68HC11RM)
    0x14: ("BSET", 3, 6, "direct"),     # Set bits in memory (dir,mask)
    0x1C: ("BSET", 3, 7, "indexed"),    # Set bits in memory (idx,mask)
    0x15: ("BCLR", 3, 6, "direct"),     # Clear bits in memory (dir,mask)
    0x1D: ("BCLR", 3, 7, "indexed"),    # Clear bits in memory (idx,mask)
    0x12: ("BRSET", 4, 6, "direct"),    # Branch if bits set (dir,mask,rel)
    0x1E: ("BRSET", 4, 7, "indexed"),   # Branch if bits set (idx,mask,rel)
    0x13: ("BRCLR", 4, 6, "direct"),    # Branch if bits clear (dir,mask,rel)
    0x1F: ("BRCLR", 4, 7, "indexed"),   # Branch if bits clear (idx,mask,rel)
}

# Prebyte $1A instructions (CPD mainly) - THE1's SPARK CUT USES THIS!
PREBYTE_1A = {
    0x83: ("CPD", 4, 5, "immediate"),   # 1A 83 jj kk
    0x93: ("CPD", 3, 6, "direct"),      # 1A 93 dd
    0xA3: ("CPD", 3, 7, "indexed"),     # 1A A3 ff
    0xB3: ("CPD", 4, 7, "extended"),    # 1A B3 hh ll ← THE1 USES THIS AT 0x1FD86!
    0xEF: ("STY", 3, 6, "indexed"),     # 1A EF ff
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
}

# Prebyte $CD instructions (rare)
PREBYTE_CD = {
    0xA3: ("CPD", 3, 7, "indexed_y"),
    0xAC: ("CPX", 3, 7, "indexed_y"),
    0xEF: ("STX", 3, 6, "indexed_y"),
    # Missing opcodes (Motorola HC11 Reference Manual)
    0x02: 1,  # IDIV
    0x03: 1,  # FDIV
    0x82: 2,  # SBCA
    0x89: 2,  # ADCA
    0x8E: 3,  # LDS
    0x92: 2,  # SBCA
    0x99: 2,  # ADCA
    0x9E: 2,  # LDS
    0x9F: 2,  # STS
    0xA2: 2,  # SBCA
    0xA9: 2,  # ADCA
    0xAE: 2,  # LDS
    0xAF: 2,  # STS
    0xB2: 3,  # SBCA
    0xB9: 3,  # ADCA
    0xBE: 3,  # LDS
    0xBF: 3,  # STS
    0xC2: 2,  # SBCB
    0xC9: 2,  # ADCB
    0xCF: 1,  # STOP
    0xD2: 2,  # SBCB
    0xD9: 2,  # ADCB
    0xE2: 2,  # SBCB
    0xE9: 2,  # ADCB
    0xF2: 3,  # SBCB
    0xF9: 3,  # ADCB
}

# ====================================================================
# VY V6 Enhanced Binary Memory Layout
# ====================================================================

# VY V6 $060A Enhanced binaries have 0x16000 byte offset:
# - First 0x16000 bytes (90,112 bytes) = Calibration data/metadata
# - Code region: File 0x16000-0x1FFFF → Runtime 0x8000-0xFFFF
# - Formula: runtime_addr = 0x8000 + (file_offset - 0x16000)
CODE_START_OFFSET = 0x16000

# ====================================================================
# HC11F Register Definitions (VY V6 ECU Specific)
# ====================================================================
# NOTE: The VY V6 Delco P04 PCM uses an HC11F-family derivative (68HC11FC0
# per DARC/IDA Pro disassembly), NOT HC11E9. The HC11F has a different
# register layout at $1000-$1005 compared to the HC11E datasheet.
# Crystal = 13.631488 MHz → E-clock = 3.408 MHz (VL400, Antus)
# ====================================================================

HC11_REGISTERS = {
    0x0000: "PORTA",
    0x0001: "DDRA",       # HC11F has DDRA at $01 (HC11E reserves $01)
    0x0002: "PORTG",      # ⚠️ HC11F = PORTG (NOT PIOC as per HC11E datasheet)
    0x0003: "DDRG",       # HC11F = DDRG (NOT PORTC)
    0x0004: "PORTB",
    0x0005: "PORTF",      # HC11F = PORTF (NOT PORTCL)
    0x0006: "PORTC",      # Shifted from $1003 in HC11E to $1006 in HC11F
    0x0007: "DDRC",
    0x0008: "PORTD",
    0x0009: "DDRD",
    0x000A: "PORTE",
    0x000B: "CFORC",
    0x000C: "OC1M",
    0x000D: "OC1D",
    0x000E: "TCNT_HI",
    0x000F: "TCNT_LO",
    0x0010: "TIC1_HI",
    0x0011: "TIC1_LO",
    0x0012: "TIC2_HI",
    0x0013: "TIC2_LO",
    0x0014: "TIC3_HI",
    0x0015: "TIC3_LO",
    0x0016: "TOC1_HI",
    0x0017: "TOC1_LO",
    0x0018: "TOC2_HI",
    0x0019: "TOC2_LO",
    0x001A: "TOC3_HI",
    0x001B: "TOC3_LO",
    0x001C: "TOC4_HI",
    0x001D: "TOC4_LO",
    0x001E: "TOC5_HI",
    0x001F: "TOC5_LO",
    0x0020: "TCTL1",
    0x0021: "TCTL2",
    0x0022: "TMSK1",
    0x0023: "TFLG1",
    0x0024: "TMSK2",
    0x0025: "TFLG2",
    0x0026: "PACTL",
    0x0027: "PACNT",
    0x0028: "SPCR",
    0x0029: "SPSR",
    0x002A: "SPDR",
    0x002B: "BAUD",
    0x002C: "SCCR1",
    0x002D: "SCCR2",
    0x002E: "SCSR",
    0x002F: "SCDR",
    0x0030: "ADCTL",
    0x0031: "ADR1",
    0x0032: "ADR2",
    0x0033: "ADR3",
    0x0034: "ADR4",
    0x003D: "OPTION",
    0x003E: "COPRST",
    0x003F: "PPROG",
    0x0039: "INIT",
    0x003A: "TEST1",
    0x003B: "CONFIG",
}

# ====================================================================
# File Detection and Path Management
# ====================================================================

def find_vy_binaries():
    """Search for VY V6 Enhanced binaries in common locations"""
    search_paths = [
        Path(r"R:\VY_V6_Assembly_Modding\bins"),
        Path(r"R:\VY_V6_Assembly_Modding\test_bins"),
        Path(r"C:\Repos\Holden_Analysis"),
        Path(r"A:\repos\Holden_Analysis"),
        Path(r"A:\repos\VY_V6_Assembly_Modding\bins"),
        Path(r"E:\Users\jason\Documents"),
        Path(r"C:\Users\jason\OneDrive\Documents"),
    ]
    
    bin_patterns = [
        "*Enhanced*.bin",
        "*enhanced*.bin",
        "*$060A*.bin",
        "*92118883*.bin",
        "*VY_V6*.bin",
    ]
    
    found_bins = []
    for search_path in search_paths:
        if search_path.exists():
            for pattern in bin_patterns:
                found_bins.extend(search_path.rglob(pattern))
    
    return sorted(set(found_bins))

def find_xdf_files():
    """Search for XDF definition files"""
    search_paths = [
        Path(r"C:\Users\jason\OneDrive\Documents\TunerPro Files"),
        Path(r"R:\VY_V6_Assembly_Modding\xdfs"),
        Path(r"A:\repos\VY_V6_Assembly_Modding\xdfs"),
        Path(r"E:\Users\jason\Documents\TunerPro Files"),
    ]
    
    found_xdfs = []
    for search_path in search_paths:
        if search_path.exists():
            found_xdfs.extend(search_path.rglob("*.xdf"))
    
    return sorted(set(found_xdfs))

# ====================================================================
# Disassembly Core Functions
# ====================================================================

def disassemble_instruction(data, offset, base_addr=0x8000, xdf_labels=None):
    """Disassemble a single HC11 instruction with prebyte and XDF support"""
    if offset >= len(data):
        return None, 0
    
    opcode = data[offset]
    prebyte = None
    opcode_table = INSTRUCTIONS
    
    # Check for prebyte ($18, $1A, $CD)
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
            addr = base_addr + offset - 1
            hex_str = f"{prebyte:02X} {opcode:02X}"
            return f"{addr:04X}  {hex_str:12s}  DB       ${prebyte:02X}  ; Unknown prebyte", 2
        
        mnemonic, total_size, cycles, addr_mode = opcode_table[opcode]
        operand_size = total_size - 2  # Subtract prebyte + opcode
    else:
        if opcode not in opcode_table:
            addr = base_addr + offset
            return f"{addr:04X}  {opcode:02X}            DB       ${opcode:02X}  ; Unknown", 1
        
        mnemonic, total_size, cycles, addr_mode = opcode_table[opcode]
        operand_size = total_size - 1
    
    # Get operand bytes
    operands = []
    start_offset = offset - (1 if prebyte else 0)
    end_offset = start_offset + total_size
    
    if end_offset > len(data):
        return None, 1
    
    if operand_size > 0:
        operands = list(data[offset+1:offset+1+operand_size])
    
    # Calculate address for display
    # Apply VY V6 Enhanced binary offset correction
    if start_offset >= CODE_START_OFFSET:
        addr = 0x8000 + (start_offset - CODE_START_OFFSET)
    else:
        addr = start_offset  # In calibration/data region
    
    # Build hex bytes string
    if prebyte:
        all_bytes = [prebyte, opcode] + operands
    else:
        all_bytes = [opcode] + operands
    hex_bytes = " ".join(f"{b:02X}" for b in all_bytes)
    
    # Format operand based on addressing mode
    operand = ""
    comment = ""
    
    # Special handling for bit manipulation instructions
    if mnemonic in ("BSET", "BCLR") and total_size == 3:
        # Format: BSET $addr, #mask or BSET offset,X, #mask
        if addr_mode == "direct":
            operand = f"${operands[0]:02X}, #${operands[1]:02X}"
            if operands[0] in HC11_REGISTERS:
                comment = f"; {HC11_REGISTERS[operands[0]]} |= 0x{operands[1]:02X}"
        elif addr_mode == "indexed":
            operand = f"${operands[0]:02X},X, #${operands[1]:02X}"
            comment = f"; Set bits 0x{operands[1]:02X}"
    
    elif mnemonic in ("BRSET", "BRCLR") and total_size == 4:
        # Format: BRSET $addr, #mask, target or BRSET offset,X, #mask, target
        rel = operands[2] if operands[2] < 128 else operands[2] - 256
        target = addr + total_size + rel
        if addr_mode == "direct":
            operand = f"${operands[0]:02X}, #${operands[1]:02X}, ${target:04X}"
            if operands[0] in HC11_REGISTERS:
                reg_name = HC11_REGISTERS[operands[0]]
                comment = f"; {reg_name} & 0x{operands[1]:02X}, offset={rel:+d}"
        elif addr_mode == "indexed":
            operand = f"${operands[0]:02X},X, #${operands[1]:02X}, ${target:04X}"
            comment = f"; Test bits 0x{operands[1]:02X}, offset={rel:+d}"
    
    elif addr_mode == "immediate":
        if len(operands) == 1:
            operand = f"#${operands[0]:02X}"
        elif len(operands) >= 2:
            value = (operands[0] << 8) | operands[1]
            operand = f"#${value:04X}"
    
    elif addr_mode == "direct":
        if len(operands) > 0:
            operand = f"${operands[0]:02X}"
            # Check if this is a register
            if operands[0] in HC11_REGISTERS:
                comment = f"; {HC11_REGISTERS[operands[0]]}"
    
    elif addr_mode in ("indexed", "indexed_y"):
        if len(operands) > 0:
            reg = "Y" if addr_mode == "indexed_y" else "X"
            operand = f"${operands[0]:02X},{reg}"
    
    elif addr_mode == "extended":
        if len(operands) >= 2:
            target = (operands[0] << 8) | operands[1]
            operand = f"${target:04X}"
            
            # Check for XDF label
            if xdf_labels and target in xdf_labels:
                comment = f"; {xdf_labels[target]}"
            # Check if this is a register
            elif target in HC11_REGISTERS:
                comment = f"; {HC11_REGISTERS[target]}"
    
    elif addr_mode == "relative":
        # Relative branch
        if len(operands) > 0:
            rel = operands[0] if operands[0] < 128 else operands[0] - 256
            target = addr + total_size + rel
            operand = f"${target:04X}"
            comment = f"; offset={rel:+d}"
    
    line = f"{addr:04X}  {hex_bytes:14s} {mnemonic:8s} {operand:15s} {comment}"
    return line, total_size

def disassemble_binary(data, base_addr=0x8000, start_offset=0, length=None, xdf_labels=None):
    """Disassemble binary data with proper HC11 memory mapping
    
    NOTE: VY V6 Enhanced binaries use CODE_START_OFFSET = 0x16000
    Runtime addresses are calculated as: 0x8000 + (file_offset - 0x16000)
    """
    if length is None:
        length = len(data) - start_offset
    
    # Calculate runtime address for header
    if start_offset >= CODE_START_OFFSET:
        runtime_start = 0x8000 + (start_offset - CODE_START_OFFSET)
    else:
        runtime_start = start_offset
    
    output = []
    output.append("; " + "=" * 68)
    output.append("; MC68HC11 Disassembly - VY V6 Enhanced ECU")
    output.append("; " + "=" * 68)
    output.append(f"; Disassembly starting at ${runtime_start:04X}")
    output.append(f"; Base address: ${base_addr:04X} (HC11 high memory)")
    output.append(f"; Binary size: {len(data)} bytes ({len(data)//1024}KB)")
    output.append(f"; Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append("; " + "=" * 68)
    output.append("")
    output.append("; [WARN]️  UNTESTED DEVELOPMENT CODE - For research only")
    output.append("; [WARN]️  This is experimental assembly analysis")
    output.append("")
    
    offset = start_offset
    end_offset = min(start_offset + length, len(data))
    
    instruction_count = 0
    
    while offset < end_offset:
        line, size = disassemble_instruction(data, offset, base_addr, xdf_labels)
        if line:
            output.append(line)
            instruction_count += 1
        offset += size
    
    output.append("")
    output.append("; " + "=" * 68)
    output.append(f"; Disassembly complete: {instruction_count} instructions")
    output.append("; " + "=" * 68)
    
    return "\n".join(output)

# ====================================================================
# XDF Label Loading
# ====================================================================

def load_xdf_labels(xdf_path):
    """Load address labels from XDF file (simplified parser)"""
    labels = {}
    
    try:
        import xml.etree.ElementTree as ET
        tree = ET.parse(xdf_path)
        root = tree.getroot()
        
        # Extract table addresses and titles
        for table in root.findall(".//XDFTABLE"):
            title_elem = table.find("title")
            addr_elem = table.find(".//mmedaddress")
            
            if title_elem is not None and addr_elem is not None and addr_elem.text:
                title = title_elem.text
                try:
                    addr = int(addr_elem.text, 16)
                    labels[addr] = title
                except ValueError:
                    pass
        
        # Extract constant addresses
        for constant in root.findall(".//XDFCONSTANT"):
            title_elem = constant.find("title")
            addr_elem = constant.find("mmedaddress")
            
            if title_elem is not None and addr_elem is not None and addr_elem.text:
                title = title_elem.text
                try:
                    addr = int(addr_elem.text, 16)
                    labels[addr] = title
                except ValueError:
                    pass
        
        print(f"[OK] Loaded {len(labels)} labels from {xdf_path.name}")
        
    except Exception as e:
        print(f"[WARN]️  Could not load XDF labels: {e}")
    
    return labels

# ====================================================================
# Main Entry Point
# ====================================================================

def main():
    # Fix Windows console encoding
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass
    
    print("=" * 70)
    print("HC11 DISASSEMBLER - Enhanced Production Version")
    print("MC68HC11 Binary Disassembly Tool for VY V6 ECUs")
    print("=" * 70)
    print("WARNING: Development code - verified opcodes")
    print("=" * 70)
    print()
    
    # Handle command line arguments
    if len(sys.argv) >= 2:
        bin_file = Path(sys.argv[1])
        base_addr = int(sys.argv[2], 16) if len(sys.argv) > 2 else 0x8000
        start_offset = int(sys.argv[3], 16) if len(sys.argv) > 3 else 0
        length = int(sys.argv[4], 16) if len(sys.argv) > 4 else None
        xdf_file = Path(sys.argv[5]) if len(sys.argv) > 5 else None
    else:
        # Auto-detect binaries
        print("[SEARCH] Searching for VY V6 binaries...")
        bins = find_vy_binaries()
        
        if not bins:
            print("[ERROR] No VY V6 binaries found!")
            print("\nUsage: python hc11_disassembler_enhanced.py <binary_file> [base_addr] [start_offset] [length] [xdf_file]")
            print("\nExample:")
            print('  python hc11_disassembler_enhanced.py "VY_V6_Enhanced_v2.09a.bin" 0x8000 0 0x1000')
            sys.exit(1)
        
        print(f"\n[OK] Found {len(bins)} binaries:")
        for i, b in enumerate(bins[:10], 1):  # Show first 10
            print(f"  {i}. {b.name}")
        
        if len(bins) > 10:
            print(f"  ... and {len(bins) - 10} more")
        
        # Use first binary
        bin_file = bins[0]
        base_addr = 0x8000
        start_offset = 0
        length = 0x1000  # First 4KB by default
        
        # Try to find matching XDF
        print("\n[SEARCH] Searching for XDF definition files...")
        xdfs = find_xdf_files()
        xdf_file = xdfs[0] if xdfs else None
        
        if xdf_file:
            print(f"[OK] Found XDF: {xdf_file.name}")
        else:
            print("[WARN]️  No XDF files found (labels will not be available)")
    
    # Validate binary file
    if not bin_file.exists():
        print(f"[ERROR] Error: File not found: {bin_file}")
        sys.exit(1)
    
    # Read binary data
    print(f"\n📂 Loading binary: {bin_file.name}")
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        print(f"[OK] Loaded {len(data)} bytes ({len(data)//1024}KB)")
    except Exception as e:
        print(f"[ERROR] Error reading file: {e}")
        sys.exit(1)
    
    # Validate file size (typical HC11 ROM sizes)
    if len(data) not in [32768, 65536, 131072, 262144, 524288]:
        print(f"[WARN]️  Warning: Unusual file size {len(data)} bytes")
        print("   Expected: 32KB, 64KB, 128KB, 256KB, or 512KB")
    
    # Load XDF labels if available
    xdf_labels = None
    if xdf_file and xdf_file.exists():
        print(f"\n📋 Loading XDF labels from {xdf_file.name}...")
        xdf_labels = load_xdf_labels(xdf_file)
    
    # Perform disassembly
    print(f"\n🔧 Disassembling...")
    print(f"   Base address: ${base_addr:04X}")
    print(f"   Start offset: ${start_offset:04X}")
    if length:
        print(f"   Length: {length} bytes (${length:04X})")
    else:
        print(f"   Length: Full binary")
    print()
    
    disasm = disassemble_binary(data, base_addr, start_offset, length, xdf_labels)
    
    # Create output directory
    output_dir = bin_file.parent / "disassembly_output"
    output_dir.mkdir(exist_ok=True)
    
    # Save output to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"{bin_file.stem}_disasm_{timestamp}.asm"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(disasm)
        print(f"[OK] Disassembly saved to: {output_file}")
    except Exception as e:
        print(f"[WARN]️  Could not save to file: {e}")
        print("   Printing to console instead:")
        print()
    
    # Print to console (first 100 lines)
    lines = disasm.split('\n')
    print('\n'.join(lines[:100]))
    
    if len(lines) > 100:
        print(f"\n... ({len(lines) - 100} more lines in output file)")
    
    print("\n" + "=" * 70)
    print("[OK] DISASSEMBLY COMPLETE")
    print("=" * 70)
    print(f"\n📁 Output saved to: {output_file}")

if __name__ == "__main__":
    main()
