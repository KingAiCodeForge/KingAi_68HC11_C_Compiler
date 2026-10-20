"""Word-shift regressions using synthetic operands and a bounded byte executor.

The executor implements only the HC11 instructions in the extracted shift
sequence. It is not a hardware emulator or a claim of whole-program correctness.
"""
import re

import pytest

from hc11_compiler import Assembler, compile_source


@pytest.mark.parametrize("target", ["generic", "vy_v6"])
@pytest.mark.parametrize("right", ["count", "wide_count", "0", "1", "7", "15"])
def test_word_left_shift_keeps_restored_d_until_loop(target, right):
    source = ("unsigned int value; unsigned int wide_count; unsigned char count; "
              "unsigned int f() { return value << " + right + "; }")
    assembly = compile_source(source, target=target)
    after_scratch = assembly.split("scratch16 (right)", 1)[1]
    after_restore = after_scratch.split("PULB", 1)[1]
    before_shift = after_restore.split("ASLD", 1)[0]
    assert "TST" in before_shift and "BEQ" in before_shift
    assert not any(instruction in before_shift for instruction in ("LDAA", "LDAB", "PSHA", "PSHB"))
    assert Assembler().assemble(assembly)


def _run_shift_bytes(code, value, count, scratch):
    """Execute the relevant byte subset with D initialized to the left operand."""
    memory = bytearray(65536)
    memory[scratch] = count
    a, b = value >> 8, value & 0xFF
    stack = []
    pc = 0
    zero = False
    for _ in range(4096):
        if pc == len(code):
            assert not stack
            return (a << 8) | b
        assert 0 <= pc < len(code)
        opcode = code[pc]
        pc += 1
        if opcode in (0x96, 0xD6, 0xD7):  # LDAA/LDAB/STAB direct
            address = code[pc]
            pc += 1
            if opcode == 0x96:
                a = memory[address]
            elif opcode == 0xD6:
                b = memory[address]
            else:
                memory[address] = b
        elif opcode in (0x36, 0x37):  # PSHA/PSHB
            stack.append(a if opcode == 0x36 else b)
        elif opcode in (0x32, 0x33):  # PULA/PULB
            if opcode == 0x32:
                a = stack.pop()
            else:
                b = stack.pop()
        elif opcode in (0x7D, 0x7A):  # TST/DEC extended
            address = (code[pc] << 8) | code[pc + 1]
            pc += 2
            if opcode == 0x7A:
                memory[address] = (memory[address] - 1) & 0xFF
            zero = memory[address] == 0
        elif opcode in (0x27, 0x20):  # BEQ/BRA relative
            offset = code[pc]
            pc += 1
            if opcode == 0x20 or zero:
                pc += offset if offset < 0x80 else offset - 0x100
        elif opcode == 0x05:  # ASLD
            result = (((a << 8) | b) << 1) & 0xFFFF
            a, b = result >> 8, result & 0xFF
        else:
            pytest.fail(f"Unexpected instruction ${opcode:02X} in bounded shift executor")
    pytest.fail("Generated shift loop exceeded its instruction bound")


@pytest.mark.parametrize("target", ["generic", "vy_v6", "1227730", "16197427"])
@pytest.mark.parametrize("count_type", ["unsigned char", "unsigned int"])
def test_word_left_shift_executes_all_defined_counts(target, count_type):
    assembly = compile_source(
        f"unsigned int value; {count_type} count; "
        "unsigned int f() { return value << count; }", target=target)
    scratch = int(re.search(r"STD\s+\$([0-9A-Fa-f]+)\s*; scratch16", assembly).group(1), 16) + 1
    restored = assembly.split("scratch16 (right)", 1)[1].split("PULB", 1)[1]
    sequence = re.split(r"(\.shl16e\d+:)", restored, maxsplit=1)
    assert len(sequence) == 3
    code = Assembler().assemble("        ORG $8000\n" + sequence[0] + sequence[1] + "\n")
    for value in (0, 1, 0x80, 0x1234, 0x8001, 0xFFFF):
        for count in range(16):
            assert _run_shift_bytes(code, value, count, scratch) == (value << count) & 0xFFFF
