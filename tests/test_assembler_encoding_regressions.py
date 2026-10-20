"""Independent byte/layout vectors for the 13 October assembler repair.

Bit opcode vectors: NXP/Freescale M68HC11E Series Programming Reference
Guide Rev. 2.1, printed page 14, Table 1 (Sheet 2 of 8):
https://www.nxp.com/docs/en/reference-manual/M68HC11ERG.pdf
These are pure assembler checks, not ECU execution or flash qualification.
"""

import pytest

from hc11_compiler.assembler import Assembler, AssemblerError


@pytest.mark.parametrize(
    "mnemonic,operand,expected",
    [
        ("BSET", "$23,#$80", b"\x14\x23\x80"),
        ("BCLR", "$23,#$80", b"\x15\x23\x80"),
        ("BSET", "$23,X,#$80", b"\x1c\x23\x80"),
        ("BCLR", "$23,X,#$80", b"\x1d\x23\x80"),
        ("BSET", "$23,Y,#$80", b"\x18\x1c\x23\x80"),
        ("BCLR", "$23,Y,#$80", b"\x18\x1d\x23\x80"),
    ],
)
def test_bit_set_clear_reference_vectors(mnemonic, operand, expected):
    assembler = Assembler()
    assert bytes(assembler.assemble(f"        ORG $8000\n        {mnemonic} {operand}")) == expected


@pytest.mark.parametrize(
    "mnemonic,register,prefix",
    [
        ("BRSET", "X", b"\x1e"),
        ("BRCLR", "X", b"\x1f"),
        ("BRSET", "Y", b"\x18\x1e"),
        ("BRCLR", "Y", b"\x18\x1f"),
    ],
)
def test_indexed_bit_branch_reference_vector_and_forward_label(mnemonic, register, prefix):
    assembler = Assembler()
    source = (
        f"        ORG $8000\n        {mnemonic} $23,{register},#$80,target\n"
        "        NOP\ntarget: RTS"
    )
    assert bytes(assembler.assemble(source)) == prefix + b"\x23\x80\x01\x01\x39"
    assert assembler.symbols["target"] == 0x8000 + len(prefix) + 4


@pytest.mark.parametrize("register,prefix,displacement", [
    ("X", b"\x1e", -5), ("Y", b"\x18\x1e", -6),
])
def test_indexed_bit_branch_backward_label(register, prefix, displacement):
    assembler = Assembler()
    source = f"        ORG $8000\ntarget: NOP\n        BRSET $23,{register},#$80,target"
    assert bytes(assembler.assemble(source)) == b"\x01" + prefix + bytes([0x23, 0x80, displacement & 0xFF])


@pytest.mark.parametrize("register,prefix", [("X", b"\x1e"), ("Y", b"\x18\x1e")])
@pytest.mark.parametrize("displacement", [-128, 127])
def test_indexed_bit_branch_accepts_signed_limits(register, prefix, displacement):
    target = 0x8000 + len(prefix) + 3 + displacement
    source = f"        ORG $8000\n        BRSET $23,{register},#$80,${target:04X}"
    assert bytes(Assembler().assemble(source)) == prefix + bytes([0x23, 0x80, displacement & 0xFF])


@pytest.mark.parametrize("register,instruction_size", [("X", 4), ("Y", 5)])
@pytest.mark.parametrize("displacement", [-129, 128])
def test_indexed_bit_branch_rejects_out_of_range(register, instruction_size, displacement):
    target = 0x8000 + instruction_size + displacement
    source = f"        ORG $8000\n        BRSET $23,{register},#$80,${target:04X}"
    with pytest.raises(AssemblerError, match="out of range"):
        Assembler().assemble(source)


@pytest.mark.parametrize("mnemonic,prefix", [
    ("LDAA", b"\xb6"), ("STAA", b"\xb7"),
    ("LDX", b"\xfe"), ("LDY", b"\x18\xfe"),
])
def test_low_page_forward_reference_keeps_reserved_extended_size(mnemonic, prefix):
    assembler = Assembler()
    target = 0x20 + len(prefix) + 2
    source = f"        ORG $20\n        {mnemonic} target\ntarget: RTS"
    assert bytes(assembler.assemble(source)) == prefix + bytes([0, target, 0x39])
    assert assembler.symbols["target"] == target


def test_branch_after_low_page_forward_reference_keeps_real_target():
    assembler = Assembler()
    source = "        ORG $20\n        LDAA target\n        BRA target\ntarget: FCB $AA"
    assert bytes(assembler.assemble(source)) == b"\xb6\x00\x25\x20\x00\xaa"
    assert assembler.symbols["target"] == 0x25


def test_forward_equ_keeps_extended_and_known_backwards_symbol_keeps_direct():
    assembler = Assembler()
    assert bytes(assembler.assemble("        ORG $20\n        LDAA port\nport: EQU $40")) == b"\xb6\x00\x40"
    # Reuse the assembler to ensure pass-one layout data does not leak.
    assert bytes(assembler.assemble("        ORG $20\nport: EQU $40\n        LDAA port")) == b"\x96\x40"


def test_layout_change_from_redefined_symbol_fails_instead_of_corrupting_labels():
    source = "        ORG $20\nport: EQU $40\n        LDAA port\nport: EQU $1000"
    with pytest.raises(AssemblerError, match="size changed"):
        Assembler().assemble(source)
