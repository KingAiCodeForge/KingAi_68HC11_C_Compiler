#!/usr/bin/env python3
"""
Full HC11 Binary Disassembler with Multi-XDF Cross-Reference
Comprehensive decompilation of VY V6 $060A Enhanced binary with torque reduction analysis
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
import csv
from pathlib import Path
from typing import Dict, Tuple, List, Optional, Set
from collections import defaultdict
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Tuple



class MultiXDFDatabase:
    """Load and cross-reference all XDF versions"""
    
    def __init__(self):
        self.calibrations = {}  # addr -> list of (version, title, type, category)
        self.address_to_versions = defaultdict(list)  # Track which XDFs define each address
        self.torque_addresses = set()  # Addresses related to torque reduction
        self.spark_addresses = set()  # Addresses related to spark/ignition
        self.limiter_addresses = set()  # Addresses related to limiters
        self.load_all_xdfs()
    
    def load_all_xdfs(self):
        """Load all XDF CSV files and build cross-reference"""
        # Try multiple possible locations for XDF CSV files
        possible_dirs = [
            Path(__file__).parent.parent / "xdf_analysis",
            Path(r"C:\Users\jason\OneDrive\Documents\XDF_Comparison"),
            Path(r"R:\VY_V6_Assembly_Modding\xdf_analysis"),
        ]
        
        xdf_dir = None
        for dir_path in possible_dirs:
            if dir_path.exists():
                xdf_dir = dir_path
                break
        
        if not xdf_dir:
            print("[WARNING] XDF analysis directory not found - disassembly will have no XDF annotations")
            return
        
        versions = ["v2.09a", "v2.62", "v1.2", "v0.9h"]
        
        for version in versions:
            version_dir = xdf_dir / version
            if not version_dir.exists():
                continue
            
            csv_file = version_dir / "titles_full.csv"
            if not csv_file.exists():
                continue
            
            print(f"[LOADING] {version} XDF definitions...")
            count = 0
            
            with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        addr_str = (row.get('address', '') or row.get('Address', '')).upper().replace('X', 'x')
                        if not addr_str or not addr_str.startswith('0x'):
                            continue
                        
                        addr = int(addr_str, 16)
                        title = row.get('title', '') or row.get('Title', '')
                        type_str = row.get('type', '') or row.get('Type', '')
                        category = row.get('category_name', '') or row.get('category', '') or ''
                        
                        if title and addr:
                            # Store with version info
                            if addr not in self.calibrations:
                                self.calibrations[addr] = []
                            
                            self.calibrations[addr].append((version, title, type_str, category))
                            self.address_to_versions[addr].append(version)
                            count += 1
                            
                            # Categorize by keywords
                            title_lower = title.lower()
                            if any(kw in title_lower for kw in ['torque', 'traction', 'tcs', 'tcm']):
                                self.torque_addresses.add(addr)
                            if any(kw in title_lower for kw in ['spark', 'ignition', 'timing', 'advance', 'retard']):
                                self.spark_addresses.add(addr)
                            if any(kw in title_lower for kw in ['limit', 'cut', 'rpm >=', 'shut off']):
                                self.limiter_addresses.add(addr)
                    
                    except (ValueError, KeyError):
                        continue
            
            print(f"  Loaded {count} calibrations from {version}")
        
        print(f"\n[ANALYSIS] Cross-Reference Summary:")
        print(f"  Total unique addresses: {len(self.calibrations)}")
        print(f"  Torque reduction addresses: {len(self.torque_addresses)}")
        print(f"  Spark/ignition addresses: {len(self.spark_addresses)}")
        print(f"  Limiter addresses: {len(self.limiter_addresses)}")
        print(f"  Overlap (torque+spark): {len(self.torque_addresses & self.spark_addresses)}")
        print(f"  Overlap (limiter+spark): {len(self.limiter_addresses & self.spark_addresses)}")
    
    def lookup(self, addr: int) -> Optional[List[Tuple[str, str, str, str]]]:
        """Get all XDF entries for address"""
        return self.calibrations.get(addr)
    
    def get_category(self, addr: int) -> str:
        """Get category flags for address"""
        flags = []
        if addr in self.torque_addresses:
            flags.append("TORQUE")
        if addr in self.spark_addresses:
            flags.append("SPARK")
        if addr in self.limiter_addresses:
            flags.append("LIMITER")
        return "|".join(flags) if flags else ""


class HC11FullDisassembler:
    """Complete HC11 disassembler with multi-XDF integration"""
    
    # Extended HC11 opcode table
    OPCODES = {
        # Load/Store A
        0x86: ('LDAA', 2, 'imm'), 0x96: ('LDAA', 2, 'dir'), 0xB6: ('LDAA', 3, 'ext'), 0xA6: ('LDAA', 2, 'idx'),
        0x97: ('STAA', 2, 'dir'), 0xB7: ('STAA', 3, 'ext'), 0xA7: ('STAA', 2, 'idx'),
        
        # Load/Store B
        0xC6: ('LDAB', 2, 'imm'), 0xD6: ('LDAB', 2, 'dir'), 0xF6: ('LDAB', 3, 'ext'), 0xE6: ('LDAB', 2, 'idx'),
        0xD7: ('STAB', 2, 'dir'), 0xF7: ('STAB', 3, 'ext'), 0xE7: ('STAB', 2, 'idx'),
        
        # Load/Store D
        0xCC: ('LDD', 3, 'imm'), 0xDC: ('LDD', 2, 'dir'), 0xFC: ('LDD', 3, 'ext'), 0xEC: ('LDD', 2, 'idx'),
        0xDD: ('STD', 2, 'dir'), 0xFD: ('STD', 3, 'ext'), 0xED: ('STD', 2, 'idx'),
        
        # Load/Store X
        0xCE: ('LDX', 3, 'imm'), 0xDE: ('LDX', 2, 'dir'), 0xFE: ('LDX', 3, 'ext'), 0xEE: ('LDX', 2, 'idx'),
        0xDF: ('STX', 2, 'dir'), 0xFF: ('STX', 3, 'ext'), 0xEF: ('STX', 2, 'idx'),
        
        # Load/Store Stack
        0x8E: ('LDS', 3, 'imm'), 0x9E: ('LDS', 2, 'dir'), 0xBE: ('LDS', 3, 'ext'), 0xAE: ('LDS', 2, 'idx'),
        0x9F: ('STS', 2, 'dir'), 0xBF: ('STS', 3, 'ext'), 0xAF: ('STS', 2, 'idx'),
        
        # Compare
        0x81: ('CMPA', 2, 'imm'), 0x91: ('CMPA', 2, 'dir'), 0xB1: ('CMPA', 3, 'ext'), 0xA1: ('CMPA', 2, 'idx'),
        0xC1: ('CMPB', 2, 'imm'), 0xD1: ('CMPB', 2, 'dir'), 0xF1: ('CMPB', 3, 'ext'), 0xE1: ('CMPB', 2, 'idx'),
        0x8C: ('CPX', 3, 'imm'), 0x9C: ('CPX', 2, 'dir'), 0xBC: ('CPX', 3, 'ext'), 0xAC: ('CPX', 2, 'idx'),
        0x83: ('SUBD', 3, 'imm'), 0x93: ('SUBD', 2, 'dir'), 0xB3: ('SUBD', 3, 'ext'), 0xA3: ('SUBD', 2, 'idx'),
        
        # Branches
        0x20: ('BRA', 2, 'rel'), 0x22: ('BHI', 2, 'rel'), 0x23: ('BLS', 2, 'rel'),
        0x24: ('BCC', 2, 'rel'), 0x25: ('BCS', 2, 'rel'), 0x26: ('BNE', 2, 'rel'),
        0x27: ('BEQ', 2, 'rel'), 0x28: ('BVC', 2, 'rel'), 0x29: ('BVS', 2, 'rel'),
        0x2A: ('BPL', 2, 'rel'), 0x2B: ('BMI', 2, 'rel'), 0x2C: ('BGE', 2, 'rel'),
        0x2D: ('BLT', 2, 'rel'), 0x2E: ('BGT', 2, 'rel'), 0x2F: ('BLE', 2, 'rel'),
        
        # Bit test branches
        0x12: ('BRCLR', 4, 'bit'), 0x13: ('BRSET', 4, 'bit'),
        0x14: ('BSET', 3, 'bit'), 0x15: ('BCLR', 3, 'bit'),
        
        # Jumps/Subroutines
        0xBD: ('JSR', 3, 'ext'), 0xAD: ('JSR', 2, 'idx'), 0x8D: ('BSR', 2, 'rel'),
        0x7E: ('JMP', 3, 'ext'), 0x6E: ('JMP', 2, 'idx'),
        0x39: ('RTS', 1, 'imp'), 0x3B: ('RTI', 1, 'imp'),
        
        # Arithmetic
        0x8B: ('ADDA', 2, 'imm'), 0x9B: ('ADDA', 2, 'dir'), 0xBB: ('ADDA', 3, 'ext'), 0xAB: ('ADDA', 2, 'idx'),
        0xCB: ('ADDB', 2, 'imm'), 0xDB: ('ADDB', 2, 'dir'), 0xFB: ('ADDB', 3, 'ext'), 0xEB: ('ADDB', 2, 'idx'),
        0xC3: ('ADDD', 3, 'imm'), 0xD3: ('ADDD', 2, 'dir'), 0xF3: ('ADDD', 3, 'ext'), 0xE3: ('ADDD', 2, 'idx'),
        0x89: ('ADCA', 2, 'imm'), 0x99: ('ADCA', 2, 'dir'), 0xB9: ('ADCA', 3, 'ext'), 0xA9: ('ADCA', 2, 'idx'),
        0xC9: ('ADCB', 2, 'imm'), 0xD9: ('ADCB', 2, 'dir'), 0xF9: ('ADCB', 3, 'ext'), 0xE9: ('ADCB', 2, 'idx'),
        0x80: ('SUBA', 2, 'imm'), 0x90: ('SUBA', 2, 'dir'), 0xB0: ('SUBA', 3, 'ext'), 0xA0: ('SUBA', 2, 'idx'),
        0xC0: ('SUBB', 2, 'imm'), 0xD0: ('SUBB', 2, 'dir'), 0xF0: ('SUBB', 3, 'ext'), 0xE0: ('SUBB', 2, 'idx'),
        
        # Logic
        0x84: ('ANDA', 2, 'imm'), 0x94: ('ANDA', 2, 'dir'), 0xB4: ('ANDA', 3, 'ext'), 0xA4: ('ANDA', 2, 'idx'),
        0xC4: ('ANDB', 2, 'imm'), 0xD4: ('ANDB', 2, 'dir'), 0xF4: ('ANDB', 3, 'ext'), 0xE4: ('ANDB', 2, 'idx'),
        0x8A: ('ORAA', 2, 'imm'), 0x9A: ('ORAA', 2, 'dir'), 0xBA: ('ORAA', 3, 'ext'), 0xAA: ('ORAA', 2, 'idx'),
        0xCA: ('ORAB', 2, 'imm'), 0xDA: ('ORAB', 2, 'dir'), 0xFA: ('ORAB', 3, 'ext'), 0xEA: ('ORAB', 2, 'idx'),
        0x88: ('EORA', 2, 'imm'), 0x98: ('EORA', 2, 'dir'), 0xB8: ('EORA', 3, 'ext'), 0xA8: ('EORA', 2, 'idx'),
        0xC8: ('EORB', 2, 'imm'), 0xD8: ('EORB', 2, 'dir'), 0xF8: ('EORB', 3, 'ext'), 0xE8: ('EORB', 2, 'idx'),
        0x85: ('BITA', 2, 'imm'), 0x95: ('BITA', 2, 'dir'), 0xB5: ('BITA', 3, 'ext'), 0xA5: ('BITA', 2, 'idx'),
        0xC5: ('BITB', 2, 'imm'), 0xD5: ('BITB', 2, 'dir'), 0xF5: ('BITB', 3, 'ext'), 0xE5: ('BITB', 2, 'idx'),
        
        # Shifts/Rotates
        0x48: ('ASLA', 1, 'imp'), 0x58: ('ASLB', 1, 'imp'), 0x05: ('ASLD', 1, 'imp'),
        0x47: ('ASRA', 1, 'imp'), 0x57: ('ASRB', 1, 'imp'),
        0x44: ('LSRA', 1, 'imp'), 0x54: ('LSRB', 1, 'imp'), 0x04: ('LSRD', 1, 'imp'),
        0x49: ('ROLA', 1, 'imp'), 0x59: ('ROLB', 1, 'imp'),
        0x46: ('RORA', 1, 'imp'), 0x56: ('RORB', 1, 'imp'),
        
        # Increment/Decrement
        0x4C: ('INCA', 1, 'imp'), 0x5C: ('INCB', 1, 'imp'),
        0x6C: ('INC', 2, 'idx'), 0x7C: ('INC', 3, 'ext'),
        0x4A: ('DECA', 1, 'imp'), 0x5A: ('DECB', 1, 'imp'),
        0x6A: ('DEC', 2, 'idx'), 0x7A: ('DEC', 3, 'ext'),
        0x08: ('INX', 1, 'imp'), 0x09: ('DEX', 1, 'imp'), 0x34: ('DES', 1, 'imp'), 0x31: ('INS', 1, 'imp'),
        
        # Clear/Test
        0x4F: ('CLRA', 1, 'imp'), 0x5F: ('CLRB', 1, 'imp'),
        0x6F: ('CLR', 2, 'idx'), 0x7F: ('CLR', 3, 'ext'),
        0x4D: ('TSTA', 1, 'imp'), 0x5D: ('TSTB', 1, 'imp'),
        0x6D: ('TST', 2, 'idx'), 0x7D: ('TST', 3, 'ext'),
        
        # Transfers
        0x16: ('TAB', 1, 'imp'), 0x17: ('TBA', 1, 'imp'),
        0x30: ('TSX', 1, 'imp'), 0x35: ('TXS', 1, 'imp'),
        0x18: ('XGDX', 1, 'imp'), 0x1B: ('ABA', 1, 'imp'),
        0x3A: ('ABX', 1, 'imp'), 0x10: ('SBA', 1, 'imp'),
        
        # Stack
        0x36: ('PSHA', 1, 'imp'), 0x37: ('PSHB', 1, 'imp'), 0x3C: ('PSHX', 1, 'imp'),
        0x32: ('PULA', 1, 'imp'), 0x33: ('PULB', 1, 'imp'), 0x38: ('PULX', 1, 'imp'),
        
        # Condition codes
        0x0C: ('CLC', 1, 'imp'), 0x0D: ('SEC', 1, 'imp'),
        0x0E: ('CLI', 1, 'imp'), 0x0F: ('SEI', 1, 'imp'),
        0x0A: ('CLV', 1, 'imp'), 0x0B: ('SEV', 1, 'imp'),
        0x06: ('TAP', 1, 'imp'), 0x07: ('TPA', 1, 'imp'),
        
        # Misc
        0x01: ('NOP', 1, 'imp'), 0x00: ('TEST', 1, 'imp'),
        0x3D: ('MUL', 1, 'imp'), 0x02: ('IDIV', 1, 'imp'),
        0x03: ('FDIV', 1, 'imp'), 0x3F: ('SWI', 1, 'imp'),
        0x3E: ('WAI', 1, 'imp'), 0x11: ('CBA', 1, 'imp'),
    # Missing opcodes (Motorola HC11 Reference Manual)
    0x82: ('SBCA', 2),
    0x8F: ('XGDX', 1),
    0x92: ('SBCA', 2),
    0xA2: ('SBCA', 2),
    0xB2: ('SBCA', 3),
    0xC2: ('SBCB', 2),
    0xCF: ('STOP', 1),
    0xD2: ('SBCB', 2),
    0xE2: ('SBCB', 2),
    0xF2: ('SBCB', 3),
    }
    
    def __init__(self, binary_path: str, xdf_db: MultiXDFDatabase):
        self.binary_path = Path(binary_path)
        self.xdf = xdf_db
        self.data = self.load_binary()
        self.base_addr = 0xE0000  # VY V6 base
        self.functions = {}  # Start addr -> function info
        self.xrefs = defaultdict(list)  # Target -> list of source addresses
        self.data_refs = defaultdict(list)  # Data addr -> list of code addresses
        
    def load_binary(self) -> bytes:
        """Load binary file"""
        with open(self.binary_path, 'rb') as f:
            return f.read()
    
    def disassemble_full(self, output_file: str = "full_disassembly.asm"):
        """Disassemble entire binary with XDF annotations"""
        
        output_path = Path(__file__).parent.parent / "disassembly_output" / output_file
        output_path.parent.mkdir(exist_ok=True)
        
        print(f"\n[FULL DISASSEMBLY] Starting at base 0x{self.base_addr:08X}")
        print(f"  Binary size: {len(self.data)} bytes (0x{len(self.data):X})")
        print(f"  Output: {output_path}")
        print()
        
        with open(output_path, 'w', encoding='utf-8') as out:
            out.write("; VY V6 $060A Enhanced v1.0a - Full HC11 Disassembly\n")
            out.write("; Multi-XDF Cross-Reference Analysis\n")
            out.write(f"; Base Address: 0x{self.base_addr:08X}\n")
            out.write(f"; Binary Size: {len(self.data)} bytes\n")
            out.write("; Generated: 2025-11-19\n")
            out.write(";\n\n")
            
            # Disassemble code section (last 128KB typically)
            code_start = max(0, len(self.data) - 0x20000)  # Last 128KB
            offset = code_start
            instr_count = 0
            
            while offset < len(self.data):
                addr = self.base_addr + offset
                
                # Check for XDF calibration at this address
                xdf_entries = self.xdf.lookup(addr)
                if xdf_entries:
                    out.write(f"\n; ============== XDF CALIBRATION at 0x{addr:08X} ==============\n")
                    for version, title, type_str, category in xdf_entries:
                        out.write(f"; [{version}] {type_str}: {title}\n")
                        if category:
                            out.write(f";   Category: {category}\n")
                    cat_flags = self.xdf.get_category(addr)
                    if cat_flags:
                        out.write(f";   FLAGS: {cat_flags}\n")
                    out.write("; " + "="*60 + "\n\n")
                
                # Disassemble instruction
                try:
                    opcode = self.data[offset]
                    
                    # Handle 2-byte opcodes (0x18, 0x1A, 0xCD prefixes)
                    if opcode in [0x18, 0x1A, 0xCD] and offset + 1 < len(self.data):
                        # Skip for now - handle in future enhancement
                        offset += 1
                        continue
                    
                    if opcode in self.OPCODES:
                        mnem, length, mode = self.OPCODES[opcode]
                        
                        if offset + length > len(self.data):
                            break
                        
                        # Build instruction string
                        instr_bytes = self.data[offset:offset+length]
                        hex_str = ' '.join(f'{b:02X}' for b in instr_bytes)
                        
                        # Parse operands
                        operand = self.parse_operand(offset, length, mode)
                        
                        # Check if operand references XDF address
                        xdf_comment = ""
                        if mode in ['ext', 'dir'] and operand.startswith('$'):
                            try:
                                operand_addr = int(operand[1:], 16)
                                xdf_data = self.xdf.lookup(operand_addr)
                                if xdf_data:
                                    # Use first XDF entry
                                    ver, title, _, _ = xdf_data[0]
                                    xdf_comment = f"  ; [{ver}] {title}"
                                    # Track data reference
                                    self.data_refs[operand_addr].append(addr)
                            except ValueError:
                                pass
                        
                        # Track cross-references for branches/jumps
                        if mode == 'rel' and mnem.startswith('B'):
                            target = self.calc_branch_target(addr, offset, length)
                            if target:
                                self.xrefs[target].append(addr)
                        elif mode == 'ext' and mnem in ['JSR', 'JMP']:
                            try:
                                target = int(operand[1:], 16)
                                self.xrefs[target].append(addr)
                            except ValueError:
                                pass
                        
                        # Write disassembly line
                        out.write(f"0x{addr:08X}:  {hex_str:<12}  {mnem:<6} {operand:<20}{xdf_comment}\n")
                        
                        offset += length
                        instr_count += 1
                        
                        # Progress indicator
                        if instr_count % 10000 == 0:
                            pct = (offset / len(self.data)) * 100
                            print(f"  Progress: {pct:.1f}% ({instr_count:,} instructions)")
                    
                    else:
                        # Unknown opcode - dump as data
                        out.write(f"0x{addr:08X}:  {opcode:02X}            DB      0x{opcode:02X}\n")
                        offset += 1
                
                except IndexError:
                    break
            
            # Write cross-reference summary
            out.write("\n\n; ============== CROSS-REFERENCE SUMMARY ==============\n")
            out.write(f"; Total instructions disassembled: {instr_count:,}\n")
            out.write(f"; Code cross-references found: {len(self.xrefs)}\n")
            out.write(f"; Data references found: {len(self.data_refs)}\n\n")
            
            # Top referenced functions
            top_funcs = sorted(self.xrefs.items(), key=lambda x: len(x[1]), reverse=True)[:20]
            out.write("; TOP 20 MOST CALLED FUNCTIONS:\n")
            for target, callers in top_funcs:
                out.write(f";   0x{target:08X}: Called {len(callers)} times\n")
            
            out.write("\n; ============== XDF DATA REFERENCE SUMMARY ==============\n")
            # Top referenced calibrations
            top_cals = sorted(self.data_refs.items(), key=lambda x: len(x[1]), reverse=True)[:30]
            for cal_addr, code_refs in top_cals:
                xdf_data = self.xdf.lookup(cal_addr)
                if xdf_data:
                    ver, title, _, _ = xdf_data[0]
                    out.write(f";   0x{cal_addr:04X} ({len(code_refs):2}x): {title}\n")
        
        print(f"\n[COMPLETE] Disassembled {instr_count:,} instructions")
        print(f"  Output written to: {output_path}")
        return output_path
    
    def parse_operand(self, offset: int, length: int, mode: str) -> str:
        """Parse instruction operand based on addressing mode"""
        if mode == 'imp':
            return ""
        elif mode == 'imm':
            if length == 2:
                return f"#${self.data[offset+1]:02X}"
            elif length == 3:
                val = (self.data[offset+1] << 8) | self.data[offset+2]
                return f"#${val:04X}"
        elif mode == 'dir':
            return f"${self.data[offset+1]:02X}"
        elif mode == 'ext':
            addr = (self.data[offset+1] << 8) | self.data[offset+2]
            return f"${addr:04X}"
        elif mode == 'idx':
            return f"${self.data[offset+1]:02X},X"
        elif mode == 'rel':
            rel_offset = self.data[offset+1]
            if rel_offset & 0x80:
                rel_offset = rel_offset - 256
            target = self.base_addr + offset + length + rel_offset
            return f"${target:08X}"
        elif mode == 'bit':
            # BSET/BCLR/BRSET/BRCLR format
            addr = self.data[offset+1]
            mask = self.data[offset+2]
            if length == 4:
                rel = self.data[offset+3]
                return f"${addr:02X}, #${mask:02X}, ${rel:02X}"
            return f"${addr:02X}, #${mask:02X}"
        
        return "???"
    
    def calc_branch_target(self, addr: int, offset: int, length: int) -> Optional[int]:
        """Calculate branch target address"""
        try:
            rel_offset = self.data[offset+length-1]
            if rel_offset & 0x80:
                rel_offset = rel_offset - 256
            return addr + length + rel_offset
        except IndexError:
            return None


def main():
    print("=" * 100)
    print(" VY V6 $060A ENHANCED - FULL BINARY DISASSEMBLY WITH MULTI-XDF ANALYSIS")
    print("=" * 100)
    print()
    
    # Load all XDF databases
    print("[PHASE 1] Loading Multi-XDF Database...")
    xdf_db = MultiXDFDatabase()
    
    # Initialize disassembler
    binary_path = Path(__file__).parent.parent / "VX-VY_V6_$060A_Enhanced_v1.0a - Copy.bin"
    
    if not binary_path.exists():
        print(f"[ERROR] Binary not found: {binary_path}")
        return
    
    print(f"\n[PHASE 2] Initializing HC11 Disassembler...")
    print(f"  Binary: {binary_path.name}")
    
    disasm = HC11FullDisassembler(str(binary_path), xdf_db)
    
    # Full disassembly
    print(f"\n[PHASE 3] Full Binary Disassembly...")
    output = disasm.disassemble_full("VY_V6_Enhanced_v1.0a_FULL.asm")
    
    # Generate analysis reports
    print(f"\n[PHASE 4] Generating Analysis Reports...")
    
    # Torque reduction analysis
    torque_report = output.parent / "torque_reduction_analysis.txt"
    with open(torque_report, 'w') as f:
        f.write("TORQUE REDUCTION SYSTEM ANALYSIS\n")
        f.write("="*80 + "\n\n")
        f.write(f"Torque-related calibrations: {len(xdf_db.torque_addresses)}\n\n")
        
        for addr in sorted(xdf_db.torque_addresses):
            entries = xdf_db.lookup(addr)
            if entries:
                f.write(f"\n0x{addr:04X}:\n")
                for ver, title, type_str, cat in entries:
                    f.write(f"  [{ver}] {type_str}: {title}\n")
                
                # Show code references
                if addr in disasm.data_refs:
                    f.write(f"  Referenced by {len(disasm.data_refs[addr])} code locations:\n")
                    for ref_addr in disasm.data_refs[addr][:10]:  # Top 10
                        f.write(f"    - 0x{ref_addr:08X}\n")
    
    print(f"  Torque analysis: {torque_report}")
    
    # Limiter cross-reference
    limiter_report = output.parent / "limiter_crossref.txt"
    with open(limiter_report, 'w') as f:
        f.write("REV LIMITER CROSS-REFERENCE\n")
        f.write("="*80 + "\n\n")
        
        # Known limiter addresses
        limiter_addrs = [0x77DD, 0x77DE, 0x77DF, 0x77E0, 0x77E1, 0x77E2, 0x77E3, 0x77E4, 0x77E6, 0x77EC, 0x77EE, 0x77EF, 0x77F0]
        
        for addr in limiter_addrs:
            entries = xdf_db.lookup(addr)
            if entries:
                f.write(f"\n0x{addr:04X}:\n")
                for ver, title, _, _ in entries:
                    f.write(f"  [{ver}] {title}\n")
                
                if addr in disasm.data_refs:
                    f.write(f"  Code references ({len(disasm.data_refs[addr])}):\n")
                    for ref_addr in disasm.data_refs[addr]:
                        f.write(f"    - 0x{ref_addr:08X}\n")
    
    print(f"  Limiter crossref: {limiter_report}")
    
    print("\n" + "="*100)
    print("[SUCCESS] Full binary analysis complete!")
    print("="*100)


if __name__ == "__main__":
    main()
