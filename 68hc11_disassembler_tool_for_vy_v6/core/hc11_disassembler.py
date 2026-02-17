#!/usr/bin/env python3
"""
HC11 Disassembler for VY V6 Enhanced ECU Binary
Decodes Motorola 68HC11 instructions from binary file with XDF integration

Uses opcodes.py for complete HC11 instruction set including all prebyte
prefixes ($18=Y-ops, $1A=CPD, $CD=Y-indexed CPD/CPX).

XDF SCALING CONFIRMED: Rev limiter at 0x77DE/0x77DF uses X*25 scaling
- Stock: 236 (0xEC) = 5900 RPM HIGH, 235 (0xEB) = 5875 RPM LOW
- Enhanced v1.0a: 255 (0xFF) = 6375 RPM (limiter disabled)

Verified against:
- Capstone CS_MODE_M680X_6811 (bank_split_output/*.asm)
- DARC VT SC disassembly (dis11/IDA reassembles to exact binary)
"""

import sys
import csv
from pathlib import Path
from typing import Dict, Tuple, List, Optional

from opcodes import HC11_OPCODES, HC11InstructionSet, Instruction, \
    MODE_IMPLIED, MODE_IMMEDIATE, MODE_DIRECT, MODE_EXTENDED, \
    MODE_INDEXED_X, MODE_INDEXED_Y, MODE_RELATIVE, \
    MODE_BIT_DIR, MODE_BIT_IDX, MODE_BIT_IDY

class XDFCalibrationDB:
    """Load and lookup XDF calibration data"""
    
    def __init__(self):
        self.calibrations = {}  # addr -> (title, type, category, units, scaling_factor)
        self.rpm_scaling_x25 = {  # Known RPM tables with x25 scaling
            0x77DE, 0x77DD  # Rev limiter and related
        }
        self.load_xdf_data()
    
    def load_xdf_data(self):
        """Load all XDF CSV files"""
        xdf_dir = Path(__file__).parent.parent / "xdf_analysis"
        
        # Try v2.09a first (most complete), then others
        for version in ["v2.09a", "v2.62", "v1.2", "v0.9h"]:
            version_dir = xdf_dir / version
            if not version_dir.exists():
                continue
            
            # Try full_data.csv first (has all fields)
            csv_patterns = ["*full_data.csv", "*addresses.csv"]
            for pattern in csv_patterns:
                for csv_file in version_dir.glob(pattern):
                    try:
                        with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
                            reader = csv.DictReader(f)
                            for row in reader:
                                addr_str = (row.get('address', '') or row.get('Address', '')).upper().replace('X', 'x')
                                title = row.get('title', '') or row.get('Title', '')
                                type_str = row.get('type', '') or row.get('Type', '')
                                category = row.get('category_name', '') or row.get('category', '') or ''
                                
                                if addr_str and addr_str.startswith('0x'):
                                    try:
                                        addr = int(addr_str, 16)
                                        if addr not in self.calibrations:  # Keep first
                                            self.calibrations[addr] = (title, type_str, category)
                                    except ValueError:
                                        pass
                    except Exception as e:
                        print(f"Warning: Could not load {csv_file}: {e}")
                if self.calibrations:  # Stop after first successful load
                    break
        
        print(f"[OK] Loaded {len(self.calibrations)} calibration definitions from XDF")
    
    def lookup(self, addr: int) -> Optional[Tuple[str, str, str]]:
        """Look up calibration by address"""
        return self.calibrations.get(addr)

class HC11Disassembler:
    """Motorola 68HC11 instruction decoder with XDF integration.
    
    Uses the unified opcodes.py table for complete instruction set coverage
    including all prebyte prefixes:
      $18 = Y-register ops (LDY, STY, CPY, INY, DEY, XGDY, etc.)
      $1A = CPD (Compare D - imm, dir, idx, ext)
      $CD = Y-indexed CPD/CPX/LDX/STX
    
    Verified against Capstone CS_MODE_M680X_6811 output and DARC (dis11/IDA).
    """
    
    # HC11 Memory-Mapped I/O Registers (0x1000-0x103F)
    HARDWARE_REGISTERS = {
        0x1000: "PORTA",   0x1001: "PORTB",   0x1002: "PORTC",   0x1003: "PORTD",
        0x1004: "PORTE",   0x1008: "TCNT_HI", 0x1009: "TCNT_LO", 0x101A: "TCTL1",
        0x101B: "TCTL2",   0x101C: "TMSK1",   0x101D: "TFLG1",   0x101E: "TMSK2",
        0x101F: "TFLG2",   0x1020: "PACTL",   0x1021: "PACNT",   0x1022: "SPCR",
        0x1023: "SPSR",    0x1024: "SPDR",    0x1025: "BAUD",    0x1026: "SCCR1",
        0x1027: "SCCR2",   0x1028: "SCSR",    0x1029: "SCDR",    0x102A: "ADCTL",
        0x102B: "ADR1",    0x102C: "ADR2",    0x102D: "ADR3",    0x102E: "ADR4",
        0x1039: "OPTION",  0x103A: "COPRST",  0x103D: "INIT",    0x103F: "CONFIG",
    }
    
    def __init__(self, binary_path: str, base_addr: int = 0xE0000):
        self.binary_path = Path(binary_path)
        self.base_addr = base_addr
        self.iset = HC11_OPCODES  # Use the unified opcode table from opcodes.py
        self.xdf = XDFCalibrationDB()
        with open(self.binary_path, 'rb') as f:
            self.data = f.read()
        print(f"[OK] Loaded {len(self.data)} bytes from {self.binary_path.name}")
        print(f"   Base address: 0x{base_addr:05X}")
        stats = self.iset.get_statistics()
        print(f"   Opcode table: {stats['total_instructions']} instructions "
              f"(base:{stats['total_base_opcodes']} "
              f"+$18:{stats['prebyte_18_opcodes']} "
              f"+$1A:{stats['prebyte_1A_opcodes']} "
              f"+$CD:{stats['prebyte_CD_opcodes']})")
    
    def get_ram_addr(self, file_offset: int) -> int:
        """Convert file offset to RAM address"""
        return self.base_addr + file_offset
    
    def get_file_offset(self, ram_addr: int) -> int:
        """Convert RAM address to file offset"""
        return ram_addr - self.base_addr
    
    def read_byte(self, offset: int) -> int:
        """Read byte at file offset"""
        if 0 <= offset < len(self.data):
            return self.data[offset]
        return 0
    
    def read_word(self, offset: int) -> int:
        """Read big-endian 16-bit word at file offset"""
        if 0 <= offset + 1 < len(self.data):
            return (self.data[offset] << 8) | self.data[offset + 1]
        return 0
    
    def decode_rpm_value(self, addr: int, byte_val: int) -> str:
        """Decode RPM value with appropriate scaling"""
        if addr in self.xdf.rpm_scaling_x25:
            rpm = byte_val * 25
            return f"{rpm} RPM (0x{byte_val:02X} × 25)"
        return f"0x{byte_val:02X}"
    
    def get_xdf_comment(self, addr: int) -> str:
        """Get XDF comment for address if it's a calibration or hardware register"""
        # Check hardware registers first
        if addr in self.HARDWARE_REGISTERS:
            reg_name = self.HARDWARE_REGISTERS[addr]
            return f" ; [HW_REG] {reg_name}"
        
        # Check XDF calibrations
        cal = self.xdf.lookup(addr)
        if cal:
            title, type_str, category = cal
            return f" ; [{type_str}] {title}"
        return ""
    
    def annotate_table_data(self, addr: int, length: int = 12) -> List[str]:
        """Generate annotated hex dump of calibration table"""
        cal = self.xdf.lookup(addr)
        if not cal:
            return []
        
        title, type_str, category = cal
        lines = [f"; === TABLE @ 0x{addr:04X}: {title} ==="]
        
        # Read table data
        offset = addr
        if addr in self.xdf.rpm_scaling_x25:
            lines.append("; RPM Table (scaling: byte × 25 = RPM)")
            for i in range(length):
                if offset + i < len(self.data):
                    byte_val = self.data[offset + i]
                    rpm = byte_val * 25
                    lines.append(f";   Byte {i}: 0x{byte_val:02X} = {rpm:4d} RPM")
        else:
            # Generic hex dump
            hex_bytes = []
            for i in range(length):
                if offset + i < len(self.data):
                    hex_bytes.append(f"{self.data[offset + i]:02X}")
            if hex_bytes:
                lines.append(f"; Data: {' '.join(hex_bytes)}")
        
        return lines
    
    def disassemble_instruction(self, offset: int) -> Tuple[str, int]:
        """Disassemble single instruction at file offset with XDF annotations.
        
        Uses opcodes.py for complete HC11 instruction set including prebyte
        prefixes $18 (Y-ops), $1A (CPD), $CD (Y-indexed CPD/CPX).
        
        Returns: (assembly string, instruction length)
        """
        if offset >= len(self.data):
            return f"0x{self.get_ram_addr(offset):05X}: ??           DB    $??           ; Past end of data", 1
        
        opcode = self.read_byte(offset)
        ram_addr = self.get_ram_addr(offset)
        
        # Check for prebyte prefixes ($18, $1A, $CD)
        prebyte = 0x00
        if self.iset.is_prebyte(opcode) and offset + 1 < len(self.data):
            prebyte = opcode
            sub_opcode = self.read_byte(offset + 1)
            inst = self.iset.get_instruction(sub_opcode, prebyte)
            if inst is None:
                # Unknown prebyte+opcode combination — emit as data
                return (f"0x{ram_addr:05X}: {opcode:02X} {sub_opcode:02X}"
                        f"        DB    ${opcode:02X},${sub_opcode:02X}"
                        f"           ; Unknown prefix ${opcode:02X} op ${sub_opcode:02X}"), 2
            opcode = sub_opcode
        else:
            inst = self.iset.get_instruction(opcode)
            if inst is None:
                return (f"0x{ram_addr:05X}: {opcode:02X}"
                        f"           DB    ${opcode:02X}"
                        f"           ; Unknown opcode"), 1
            # Skip the PREFIX entries themselves (they're handled above)
            if inst.mnemonic.startswith("PREFIX_"):
                # Shouldn't normally get here, but just in case
                return (f"0x{ram_addr:05X}: {opcode:02X}"
                        f"           DB    ${opcode:02X}"
                        f"           ; Orphan prefix byte"), 1
        
        mnemonic = inst.mnemonic
        length = inst.length
        mode = inst.mode
        
        # Read raw bytes for hex dump
        raw_bytes = []
        for i in range(length):
            if offset + i < len(self.data):
                raw_bytes.append(self.read_byte(offset + i))
            else:
                raw_bytes.append(0)
        raw_hex = " ".join(f"{b:02X}" for b in raw_bytes)
        
        # Determine the operand offset (after prebyte if present)
        # For prebyte instructions, operand bytes start at offset+2
        # For normal instructions, operand bytes start at offset+1
        if prebyte:
            op_base = offset + 2  # skip prebyte + opcode
        else:
            op_base = offset + 1  # skip opcode
        
        # Format instruction based on addressing mode
        if mode == MODE_IMPLIED:
            instr = f"0x{ram_addr:05X}: {raw_hex:15s} {mnemonic}"
        
        elif mode == MODE_IMMEDIATE:
            # Immediate can be 1-byte (#$XX) or 2-byte (#$XXXX)
            # operand bytes = length - (1 for opcode) - (1 for prebyte if present)
            operand_len = length - (2 if prebyte else 1)
            if operand_len == 1:
                val = self.read_byte(op_base)
                instr = f"0x{ram_addr:05X}: {raw_hex:15s} {mnemonic} #${val:02X}"
            else:  # 2-byte immediate
                val = self.read_word(op_base)
                instr = f"0x{ram_addr:05X}: {raw_hex:15s} {mnemonic} #${val:04X}"
        
        elif mode == MODE_DIRECT:
            operand = self.read_byte(op_base)
            instr = f"0x{ram_addr:05X}: {raw_hex:15s} {mnemonic} ${operand:02X}"
        
        elif mode == MODE_EXTENDED:
            operand = self.read_word(op_base)
            xdf_comment = self.get_xdf_comment(operand)
            instr = f"0x{ram_addr:05X}: {raw_hex:15s} {mnemonic} ${operand:04X}{xdf_comment}"
        
        elif mode == MODE_INDEXED_X:
            idx_offset = self.read_byte(op_base)
            instr = f"0x{ram_addr:05X}: {raw_hex:15s} {mnemonic} ${idx_offset:02X},X"
        
        elif mode == MODE_INDEXED_Y:
            idx_offset = self.read_byte(op_base)
            instr = f"0x{ram_addr:05X}: {raw_hex:15s} {mnemonic} ${idx_offset:02X},Y"
        
        elif mode == MODE_RELATIVE:
            displacement = self.read_byte(op_base)
            if displacement & 0x80:
                displacement = displacement - 256
            target = ram_addr + length + displacement
            instr = f"0x{ram_addr:05X}: {raw_hex:15s} {mnemonic} $0x{target:05X}"
        
        elif mode == MODE_BIT_DIR:
            # BSET/BCLR direct: opcode, addr, mask (3 bytes)
            # BRSET/BRCLR direct: opcode, addr, mask, rel (4 bytes)
            addr_val = self.read_byte(op_base)
            mask = self.read_byte(op_base + 1)
            hw_comment = self.get_xdf_comment(addr_val)
            if length == (4 if not prebyte else 5):
                # BRSET/BRCLR — has relative branch target
                displacement = self.read_byte(op_base + 2)
                if displacement & 0x80:
                    displacement = displacement - 256
                target = ram_addr + length + displacement
                instr = (f"0x{ram_addr:05X}: {raw_hex:15s} {mnemonic} "
                         f"${addr_val:02X},#${mask:02X},$0x{target:05X}{hw_comment}")
            else:
                # BSET/BCLR — no branch target
                instr = (f"0x{ram_addr:05X}: {raw_hex:15s} {mnemonic} "
                         f"${addr_val:02X},#${mask:02X}{hw_comment}")
        
        elif mode == MODE_BIT_IDX:
            # BSET/BCLR indexed: opcode, offset, mask (3 bytes)
            # BRSET/BRCLR indexed: opcode, offset, mask, rel (4 bytes)
            idx_offset = self.read_byte(op_base)
            mask = self.read_byte(op_base + 1)
            if length == (4 if not prebyte else 5):
                displacement = self.read_byte(op_base + 2)
                if displacement & 0x80:
                    displacement = displacement - 256
                target = ram_addr + length + displacement
                instr = (f"0x{ram_addr:05X}: {raw_hex:15s} {mnemonic} "
                         f"${idx_offset:02X},X,#${mask:02X},$0x{target:05X}")
            else:
                instr = (f"0x{ram_addr:05X}: {raw_hex:15s} {mnemonic} "
                         f"${idx_offset:02X},X,#${mask:02X}")
        
        elif mode == MODE_BIT_IDY:
            # Same as BIT_IDX but with Y register
            idx_offset = self.read_byte(op_base)
            mask = self.read_byte(op_base + 1)
            if length == (4 if not prebyte else 5):
                displacement = self.read_byte(op_base + 2)
                if displacement & 0x80:
                    displacement = displacement - 256
                target = ram_addr + length + displacement
                instr = (f"0x{ram_addr:05X}: {raw_hex:15s} {mnemonic} "
                         f"${idx_offset:02X},Y,#${mask:02X},$0x{target:05X}")
            else:
                instr = (f"0x{ram_addr:05X}: {raw_hex:15s} {mnemonic} "
                         f"${idx_offset:02X},Y,#${mask:02X}")
        
        else:
            instr = f"0x{ram_addr:05X}: {raw_hex:15s} {mnemonic} ???  ; mode={mode}"
        
        return instr, length
    
    def disassemble_range(self, start_offset: int, num_instructions: int = 20) -> List[str]:
        """Disassemble multiple instructions"""
        results = []
        offset = start_offset
        
        for i in range(num_instructions):
            if offset >= len(self.data):
                break
            instr, length = self.disassemble_instruction(offset)
            results.append(instr)
            offset += length
        
        return results
    
    def _get_instruction_at(self, offset: int):
        """Get instruction info at offset, handling prebytes.
        Returns: (Instruction, total_length, operand_base_offset) or (None, 1, None)
        """
        opcode = self.read_byte(offset)
        if self.iset.is_prebyte(opcode) and offset + 1 < len(self.data):
            sub_opcode = self.read_byte(offset + 1)
            inst = self.iset.get_instruction(sub_opcode, opcode)
            if inst:
                return inst, inst.length, offset + 2
            return None, 2, None
        inst = self.iset.get_instruction(opcode)
        if inst and not inst.mnemonic.startswith("PREFIX_"):
            return inst, inst.length, offset + 1
        return None, 1, None

    def find_calibration_reads(self, start_offset: int, end_offset: int) -> List[Tuple[int, str]]:
        """Find all instructions that read from calibration region (0x4000-0x7FFF or 0x1000-0x1FFF)"""
        reads = []
        offset = start_offset
        
        while offset < min(end_offset, len(self.data)):
            inst, length, op_base = self._get_instruction_at(offset)
            
            if inst:
                # Check extended addressing mode loads
                if inst.mode == MODE_EXTENDED and inst.mnemonic in ["LDAA", "LDAB", "LDD", "LDX", "LDY"]:
                    addr = self.read_word(op_base)
                    # Check if reading from calibration regions
                    if (0x4000 <= addr <= 0x7FFF) or (0x1000 <= addr <= 0x1FFF):
                        instr, _ = self.disassemble_instruction(offset)
                        reads.append((offset, instr))
                
                offset += length
            else:
                offset += length
        
        return reads
    
    def find_specific_address_references(self, target_addr: int, start_offset: int = 0, end_offset: int = None) -> List[Tuple[int, str, str]]:
        """Find all instructions that reference a specific address (like 0x77DE limiter)
        Returns: [(file_offset, instruction, context_type)]
        """
        if end_offset is None:
            end_offset = len(self.data)
        
        references = []
        offset = start_offset
        
        while offset < min(end_offset, len(self.data)):
            inst, length, op_base = self._get_instruction_at(offset)
            
            if inst:
                # Check extended addressing mode
                if inst.mode == MODE_EXTENDED and op_base is not None:
                    addr = self.read_word(op_base)
                    if addr == target_addr:
                        instr, _ = self.disassemble_instruction(offset)
                        mnemonic = inst.mnemonic
                        
                        # Determine context type
                        if mnemonic in ["LDAA", "LDAB", "LDD", "LDX", "LDY"]:
                            context = "READ"
                        elif mnemonic in ["STAA", "STAB", "STD", "STX", "STY"]:
                            context = "WRITE"
                        elif mnemonic in ["CMPA", "CMPB", "CPX", "CPY", "CPD"]:
                            context = "COMPARE"
                        elif mnemonic == "JSR":
                            context = "CALL"
                        elif mnemonic in ["SUBD", "ADDD", "SUBA", "ADDA", "SUBB", "ADDB"]:
                            context = "ARITHMETIC"
                        else:
                            context = "OTHER"
                        
                        references.append((offset, instr, context))
                
                offset += length
            else:
                offset += length
        
        return references
    
    def disassemble_with_context(self, center_offset: int, before: int = 10, after: int = 10) -> List[str]:
        """Disassemble instructions around a specific address with context"""
        results = []
        
        # Find start by counting backwards
        start_offset = center_offset
        count = 0
        while count < before and start_offset > 0:
            start_offset -= 1
            # Simple heuristic: assume average instruction is 2 bytes
            if count % 2 == 0:
                count += 1
        
        # Disassemble forward
        offset = start_offset
        instruction_count = 0
        
        while offset < len(self.data) and instruction_count < (before + after + 1):
            if offset == center_offset:
                results.append("; >>> TARGET INSTRUCTION >>>")
            
            instr, length = self.disassemble_instruction(offset)
            results.append(instr)
            
            if offset == center_offset:
                results.append("; <<< TARGET INSTRUCTION <<<")
            
            offset += length
            instruction_count += 1
        
        return results
    
    def find_rpm_comparisons(self, start_offset: int, end_offset: int) -> List[Tuple[int, str, int]]:
        """Find CMPA/CMPB/CPX/CPY/CPD instructions that might be RPM comparisons.
        Now catches CPD via $1A prefix which the old code missed entirely.
        Returns: [(file_offset, instruction, immediate_value_if_present)]
        """
        comparisons = []
        offset = start_offset
        
        while offset < min(end_offset, len(self.data)):
            inst, length, op_base = self._get_instruction_at(offset)
            
            if inst:
                # Look for ALL compare instructions (including CPD via $1A prefix)
                if inst.mnemonic in ["CMPA", "CMPB", "CPX", "CPY", "CPD"]:
                    instr, _ = self.disassemble_instruction(offset)
                    
                    # Get immediate or extended value
                    imm_val = None
                    if inst.mode == MODE_IMMEDIATE:
                        operand_len = length - (2 if inst.prebyte else 1)
                        if operand_len == 1:
                            imm_val = self.read_byte(op_base)
                        else:
                            imm_val = self.read_word(op_base)
                    elif inst.mode == MODE_EXTENDED:
                        imm_val = self.read_word(op_base)
                    elif inst.mode == MODE_DIRECT:
                        imm_val = self.read_byte(op_base)
                    
                    comparisons.append((offset, instr, imm_val))
                
                offset += length
            else:
                offset += length
        
        return comparisons
    
    def find_bit_operations(self, start_offset: int, end_offset: int) -> List[Tuple[int, str, int, int]]:
        """Find BSET/BCLR/BRSET/BRCLR instructions (mode switches, flags, sensor enables)
        Returns: [(file_offset, instruction, address, bit_mask)]
        """
        bit_ops = []
        offset = start_offset
        
        while offset < min(end_offset, len(self.data)):
            inst, length, op_base = self._get_instruction_at(offset)
            
            if inst:
                # Look for bit manipulation instructions
                if inst.mnemonic in ["BSET", "BCLR", "BRSET", "BRCLR"]:
                    instr, _ = self.disassemble_instruction(offset)
                    
                    # Extract address and mask
                    addr = None
                    mask = None
                    
                    if inst.mode in (MODE_BIT_DIR, MODE_BIT_IDX, MODE_BIT_IDY):
                        addr = self.read_byte(op_base)
                        mask = self.read_byte(op_base + 1)
                    
                    if addr is not None:
                        bit_ops.append((offset, instr, addr, mask))
                
                offset += length
            else:
                offset += length
        
        return bit_ops

def main():
    print("=" * 100)
    print("HC11 DISASSEMBLER - VY V6 Enhanced ECU Binary Analysis")
    print("=" * 100)
    
    # Try multiple paths for the binary
    possible_paths = [
        Path(__file__).parent.parent.parent / "VX-VY_V6_$060A_Enhanced_v1.0a - Copy.bin",
        Path(r"R:\VY_V6_Assembly_Modding\VX-VY_V6_$060A_Enhanced_v1.0a - Copy.bin"),
        Path(r"A:\repos\VY_V6_Assembly_Modding\VX-VY_V6_$060A_Enhanced_v1.0a - Copy.bin"),
    ]
    
    binary_path = None
    for p in possible_paths:
        if p.exists():
            binary_path = p
            break
    
    if binary_path is None:
        print(f"[ERROR] Binary not found in any of these locations:")
        for p in possible_paths:
            print(f"  - {p}")
        return 1
    
    dis = HC11Disassembler(binary_path, base_addr=0x0)
    
    # ANALYSIS 0: Rev Limiter Table Annotation
    print("\n" + "=" * 100)
    print(" ANALYSIS 0: REV LIMITER TABLE @ 0x77DE (RPM × 25 SCALING)")
    print("=" * 100)
    table_lines = dis.annotate_table_data(0x77DE, 12)
    for line in table_lines:
        print(line)
    print()
    
    # NEW CRITICAL ANALYSIS: Find what code USES the limiter table
    print("\n" + "=" * 100)
    print(" ANALYSIS 0A: FIND ALL CODE THAT REFERENCES 0x77DE REV LIMITER TABLE")
    print("=" * 100)
    print("Searching entire binary for instructions that read/write/compare 0x77DE...")
    print()
    
    refs = dis.find_specific_address_references(0x77DE, 0, len(dis.data))
    print(f"Found {len(refs)} references to 0x77DE:")
    print()
    
    for offset, instr, context in refs:
        print(f"[{context:8s}] {instr}")
        print(f"   Context (±5 instructions):")
        context_code = dis.disassemble_with_context(offset, before=5, after=5)
        for line in context_code:
            print(f"   {line}")
        print()
    
    # Also check related addresses from XDF
    print("\n" + "=" * 100)
    print(" ANALYSIS 0B: FUEL CUTOFF RELATED PARAMETERS")
    print("=" * 100)
    related_addrs = [
        (0x77EC, "Time delay parameter"),
        (0x77EE, "AFR ratio parameter 1"),
        (0x77EF, "AFR ratio parameter 2"),
    ]
    
    for addr, desc in related_addrs:
        print(f"\n{desc} @ 0x{addr:04X}:")
        refs = dis.find_specific_address_references(addr, 0, len(dis.data))
        if refs:
            for offset, instr, context in refs[:3]:  # Show first 3
                print(f"  [{context:8s}] {instr}")
        else:
            print(f"  No references found")
    print()
    
    # Analyze the address found in BMW Master Plan (file offset 0x17283 = RAM 0xF7283)
    print("\n" + "=" * 100)
    print("[ANALYSIS] ANALYSIS 1: CODE AT FILE OFFSET 0x17283 (RAM ADDRESS 0xF7283)")
    print("=" * 100)
    print("This address was referenced in BMW Master Plan patches")
    print()
    
    instructions = dis.disassemble_range(0x17283, 30)
    for instr in instructions:
        print(instr)
    
    # NEW: Find RPM comparisons
    print("\n" + "=" * 100)
    print(" ANALYSIS 0C: SEARCH FOR RPM COMPARISON INSTRUCTIONS")
    print("=" * 100)
    print("Looking for CMPA/CMPB that might compare current RPM vs limiter...")
    print()
    
    # Search in likely code regions (0x10000-0x1FFFF typical for code)
    comparisons = dis.find_rpm_comparisons(0x10000, 0x1FFFF)
    
    # Filter for likely RPM values (150-255 = 3750-6375 RPM in ×25 scaling)
    rpm_likely = [(off, instr, val) for off, instr, val in comparisons 
                  if val and 150 <= val <= 255]
    
    print(f"Found {len(rpm_likely)} compare instructions with RPM-like values:")
    print()
    for offset, instr, val in rpm_likely[:20]:  # Show first 20
        if val < 256:  # Single byte
            rpm = val * 25
            print(f"{instr}  ; Possible {rpm} RPM (×25)")
        print()
    
    # Find all calibration table reads in the 0x17000-0x18000 region
    print("\n" + "=" * 100)
    print(" ANALYSIS 2: CALIBRATION READS IN CODE REGION")
    print("=" * 100)
    print("Scanning for calibration memory reads (0x4000-0x7FFF)...")
    print()
    
    reads = dis.find_calibration_reads(0x17000, 0x18000)
    print(f"Found {len(reads)} calibration read instructions:")
    print()
    for offset, instr in reads[:50]:  # Show first 50
        print(instr)
    
    # Analyze vector table at end of binary
    print("\n" + "=" * 100)
    print(" ANALYSIS 3: HC11 INTERRUPT VECTOR TABLE (END OF BINARY)")
    print("=" * 100)
    
    vector_offset = len(dis.data) - 16
    print(f"Vector table at file offset 0x{vector_offset:05X} (RAM 0x{dis.get_ram_addr(vector_offset):05X})")
    print()
    
    vectors = [
        ("IRQ", vector_offset + 10),
        ("XIRQ", vector_offset + 8),
        ("SWI", vector_offset + 6),
        ("Illegal Opcode", vector_offset + 4),
        ("COP Failure", vector_offset + 2),
        ("RESET", vector_offset + 0),
    ]
    
    for name, voffset in vectors:
        addr = dis.read_word(voffset)
        print(f"{name:20s} vector: 0x{addr:04X}")
    
    # NEW: Disassemble ISRs at vector addresses
    print("\n" + "=" * 100)
    print(" ANALYSIS 4: INTERRUPT SERVICE ROUTINE (ISR) CODE")
    print("=" * 100)
    print("These are the actual functions that run when hardware events occur:")
    print()
    
    for name, voffset in vectors:
        isr_addr = dis.read_word(voffset)
        
        # Convert RAM address to file offset
        if isr_addr >= dis.base_addr:
            isr_offset = isr_addr - dis.base_addr
            
            if isr_offset < len(dis.data):
                print(f"\n--- {name} Handler @ 0x{isr_addr:04X} (file offset 0x{isr_offset:05X}) ---")
                
                # Disassemble first 20 instructions of ISR
                isr_code = dis.disassemble_range(isr_offset, 20)
                for line in isr_code:
                    print(line)
                    # Stop at RTI (return from interrupt)
                    if "RTI" in line and not "LDAA" in line:
                        print("   ... (RTI - end of ISR)")
                        break
    
    print("\n" + "=" * 100)
    print(" DISASSEMBLY COMPLETE")
    print("=" * 100)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
