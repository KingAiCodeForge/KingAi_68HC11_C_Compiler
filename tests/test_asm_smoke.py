"""
Assembler Tests for KingAI 68HC11 C Compiler.

Tests the two-pass assembler and S19 emitter against known-good
HC11 machine code derived from the Motorola reference manual.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from hc11_compiler.assembler import Assembler, AssemblerError, assemble, assemble_to_s19


class TestOpcodeEncoding:
    """Verify individual instruction encodings against the HC11 reference manual."""

    def _asm_bytes(self, source: str) -> bytes:
        """Assemble source and return raw bytes."""
        a = Assembler()
        a.assemble(f"        ORG $8000\n{source}")
        return bytes(a.binary)

    def test_inherent_instructions(self):
        """INH mode: single-byte opcodes."""
        cases = [
            ("NOP",   b'\x01'),
            ("INCA",  b'\x4C'),
            ("DECA",  b'\x4A'),
            ("CLRA",  b'\x4F'),
            ("CLRB",  b'\x5F'),
            ("TSTA",  b'\x4D'),
            ("TAB",   b'\x16'),
            ("TBA",   b'\x17'),
            ("TSX",   b'\x30'),
            ("PSHA",  b'\x36'),
            ("PSHB",  b'\x37'),
            ("PSHX",  b'\x3C'),
            ("PULA",  b'\x32'),
            ("PULB",  b'\x33'),
            ("PULX",  b'\x38'),
            ("RTS",   b'\x39'),
            ("RTI",   b'\x3B'),
            ("WAI",   b'\x3E'),
            ("INS",   b'\x31'),
            ("DES",   b'\x34'),
            ("INX",   b'\x08'),
            ("DEX",   b'\x09'),
            ("ABA",   b'\x1B'),
            ("SBA",   b'\x10'),
            ("CBA",   b'\x11'),
            ("MUL",   b'\x3D'),
            ("SEI",   b'\x0F'),
            ("CLI",   b'\x0E'),
        ]
        for mnem, expected in cases:
            result = self._asm_bytes(f"        {mnem}")
            assert result == expected, f"{mnem}: expected {expected.hex()}, got {result.hex()}"

    def test_y_prefixed_inherent(self):
        """Y-register instructions use $18 prefix."""
        cases = [
            ("PSHY",  b'\x18\x3C'),
            ("PULY",  b'\x18\x38'),
            ("INY",   b'\x18\x08'),
            ("DEY",   b'\x18\x09'),
            ("TSY",   b'\x18\x30'),
        ]
        for mnem, expected in cases:
            result = self._asm_bytes(f"        {mnem}")
            assert result == expected, f"{mnem}: expected {expected.hex()}, got {result.hex()}"

    def test_ldaa_all_modes(self):
        """LDAA addressing modes."""
        assert self._asm_bytes("        LDAA    #$FF") == b'\x86\xFF'
        assert self._asm_bytes("        LDAA    $40") == b'\x96\x40'
        assert self._asm_bytes("        LDAA    $1000") == b'\xB6\x10\x00'
        assert self._asm_bytes("        LDAA    0,X") == b'\xA6\x00'
        assert self._asm_bytes("        LDAA    5,X") == b'\xA6\x05'

    def test_staa_all_modes(self):
        """STAA addressing modes."""
        assert self._asm_bytes("        STAA    $40") == b'\x97\x40'
        assert self._asm_bytes("        STAA    $1000") == b'\xB7\x10\x00'
        assert self._asm_bytes("        STAA    0,X") == b'\xA7\x00'

    def test_ldd_16bit(self):
        assert self._asm_bytes("        LDD     #$1234") == b'\xCC\x12\x34'

    def test_ldx_16bit(self):
        assert self._asm_bytes("        LDX     #$ABCD") == b'\xCE\xAB\xCD'

    def test_addd_immediate(self):
        assert self._asm_bytes("        ADDD    #$0100") == b'\xC3\x01\x00'

    def test_subd_immediate(self):
        assert self._asm_bytes("        SUBD    #$0001") == b'\x83\x00\x01'

    def test_arithmetic_8bit(self):
        assert self._asm_bytes("        ADDA    #$10") == b'\x8B\x10'
        assert self._asm_bytes("        ADDB    #$20") == b'\xCB\x20'
        assert self._asm_bytes("        SUBA    #$05") == b'\x80\x05'
        assert self._asm_bytes("        SUBB    #$0A") == b'\xC0\x0A'

    def test_logical_immediate(self):
        assert self._asm_bytes("        ANDA    #$0F") == b'\x84\x0F'
        assert self._asm_bytes("        ORAA    #$80") == b'\x8A\x80'
        assert self._asm_bytes("        EORA    #$FF") == b'\x88\xFF'

    def test_compare_immediate(self):
        assert self._asm_bytes("        CMPA    #$42") == b'\x81\x42'
        assert self._asm_bytes("        CMPB    #$00") == b'\xC1\x00'

    def test_jsr_extended(self):
        assert self._asm_bytes("        JSR     $B600") == b'\xBD\xB6\x00'

    def test_jmp_extended(self):
        assert self._asm_bytes("        JMP     $8000") == b'\x7E\x80\x00'


class TestBranchInstructions:
    """Verify branch offset calculations."""

    def test_branch_forward(self):
        src = "        ORG $8000\n        BRA     target\n        NOP\n        NOP\ntarget:\n        RTS"
        a = Assembler()
        a.assemble(src)
        binary = bytes(a.binary)
        assert binary[0] == 0x20  # BRA opcode
        assert binary[1] == 0x02  # offset +2 (skip 2 NOPs)

    def test_branch_backward(self):
        src = "        ORG $8000\nloop:\n        NOP\n        BRA     loop"
        a = Assembler()
        a.assemble(src)
        binary = bytes(a.binary)
        assert binary[1] == 0x20  # BRA opcode
        assert binary[2] == 0xFD  # offset -3

    def test_beq_forward(self):
        src = "        ORG $8000\n        TSTA\n        BEQ     skip\n        INCA\nskip:\n        RTS"
        a = Assembler()
        a.assemble(src)
        binary = bytes(a.binary)
        assert binary[0] == 0x4D  # TSTA
        assert binary[1] == 0x27  # BEQ
        assert binary[2] == 0x01  # skip INCA
        assert binary[3] == 0x4C  # INCA
        assert binary[4] == 0x39  # RTS

    def test_local_labels(self):
        """Local labels (dot-prefixed) as used by the codegen."""
        src = "        ORG $8000\n        TSTA\n        BEQ     .end\n        INCA\n.end:\n        RTS"
        a = Assembler()
        a.assemble(src)
        binary = bytes(a.binary)
        assert binary[1] == 0x27  # BEQ
        assert binary[2] == 0x01  # skip INCA

    def test_branch_out_of_range_raises(self):
        nops = "\n".join(["        NOP"] * 130)
        src = f"        ORG $8000\n        BRA     target\n{nops}\ntarget:\n        RTS"
        a = Assembler()
        with pytest.raises(AssemblerError, match="out of range"):
            a.assemble(src)


class TestDirectives:
    """Test assembler directives."""

    def test_org_sets_base(self):
        a = Assembler()
        a.assemble("        ORG $B600\n        NOP")
        assert a.base_addr == 0xB600

    def test_equ_defines_symbol(self):
        src = "        ORG $8000\nPORTA:  EQU     $1000\n        LDAA    PORTA"
        a = Assembler()
        a.assemble(src)
        assert bytes(a.binary) == b'\xB6\x10\x00'

    def test_equ_direct_page(self):
        src = "        ORG $8000\nmyvar:  EQU     $40\n        LDAA    myvar"
        a = Assembler()
        a.assemble(src)
        assert bytes(a.binary) == b'\x96\x40'

    def test_fcb_bytes(self):
        src = "        ORG $8000\n        FCB     $10,$20,$30,$FF"
        a = Assembler()
        a.assemble(src)
        assert bytes(a.binary) == b'\x10\x20\x30\xFF'

    def test_fdb_words(self):
        src = "        ORG $8000\n        FDB     $1234,$5678"
        a = Assembler()
        a.assemble(src)
        assert bytes(a.binary) == b'\x12\x34\x56\x78'

    def test_fcc_string(self):
        src = '        ORG $8000\n        FCC     "Hello"'
        a = Assembler()
        a.assemble(src)
        assert bytes(a.binary) == b'Hello'

    def test_rmb_reserves_space(self):
        src = "        ORG $8000\n        RMB     4\n        NOP"
        a = Assembler()
        a.assemble(src)
        assert bytes(a.binary) == b'\x00\x00\x00\x00\x01'


class TestS19Output:
    """Test Motorola S19 format output."""

    def test_s19_has_header(self):
        s19 = assemble_to_s19("        ORG $8000\n        NOP")
        assert s19.startswith("S0")

    def test_s19_has_data_and_end(self):
        s19 = assemble_to_s19("        ORG $8000\n        NOP")
        assert "S1" in s19
        lines = s19.strip().split('\n')
        assert lines[-1].startswith("S9")

    def test_s19_checksum_valid(self):
        s19 = assemble_to_s19("        ORG $8000\n        NOP")
        for line in s19.strip().split('\n'):
            if not line.startswith("S"):
                continue
            hex_data = line[2:]
            raw_bytes = bytes.fromhex(hex_data)
            data, cksum = raw_bytes[:-1], raw_bytes[-1]
            expected = (~sum(data)) & 0xFF
            assert cksum == expected, f"Checksum fail: {line}"


class TestCompleteProgram:
    """Full program assembly with known-good machine code."""

    def test_blink_sequence(self):
        src = """
        ORG     $8000
start:
        LDAA    #$FF
        STAA    $1000
        NOP
        CLRA
        LDAB    #$42
        ABA
        BRA     start
        RTS
"""
        expected = bytes([
            0x86, 0xFF, 0xB7, 0x10, 0x00, 0x01, 0x4F,
            0xC6, 0x42, 0x1B, 0x20, 0xF4, 0x39,
        ])
        binary, base = assemble(src)
        assert base == 0x8000
        assert bytes(binary) == expected

    def test_isr_skeleton(self):
        src = """
        ORG $8000
my_isr:
        PSHA
        PSHB
        PSHX
        LDAA    $1023
        ORAA    #$01
        STAA    $1023
        PULX
        PULB
        PULA
        RTI
"""
        a = Assembler()
        a.assemble(src)
        binary = bytes(a.binary)
        assert binary[0] == 0x36   # PSHA
        assert binary[1] == 0x37   # PSHB
        assert binary[2] == 0x3C   # PSHX
        assert binary[-1] == 0x3B  # RTI

    def test_interrupt_vector_table(self):
        vectors = "\n".join([f"        FDB     $0000"] * 20)
        src = f"        ORG $FFD6\n{vectors}"
        a = Assembler()
        a.assemble(src)
        assert a.base_addr == 0xFFD6
        assert len(a.binary) == 40  # 20 × 2


class TestFullPipeline:
    """Test C source → assembly → binary/S19 pipeline."""

    def test_simple_c_to_binary(self):
        from hc11_compiler import compile_source
        c_src = "void main() { *(volatile unsigned char *)0x1000 = 0x55; }"
        asm_output = compile_source(c_src, org=0x8000, target='generic')
        a = Assembler()
        binary = a.assemble(asm_output)
        assert len(binary) > 0
        assert a.base_addr == 0x8000

    def test_simple_c_to_s19(self):
        from hc11_compiler import compile_source
        c_src = "void main() { *(volatile unsigned char *)0x1000 = 0x55; }"
        s19 = compile_source(c_src, org=0x8000, target='generic', output='s19')
        assert s19.startswith("S0")
        assert "S1" in s19
        assert "S9" in s19


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
