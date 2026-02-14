"""
HC11 Virtual Emulator — ALU Operations + Instruction Handlers

SCAFFOLD — needs cross-referencing against:
  - tonypdmtr/EVBU PySim11/ops.py (complete handler implementations)
  - Motorola MC68HC11 Reference Manual Rev3 Appendix A (flag effects)
  - hc11_compiler/assembler.py (which instructions the compiler emits)

Priority 1 instructions (~86) are what the compiler generates.
Priority 2 are for hand-written assembly and stock ROM emulation.
Priority 3 is full HC11 opcode coverage.

CCR flag arithmetic functions are adapted from EVBU PySim11/ops.py
(GPL-2.0, tonypdmtr). Each one has been annotated with which CCR
bits it sets and the overflow formula used.

IMPORTANT: The overflow (V) flag formula for add8/sub8 must match
the HC11 manual exactly. The EVBU implementation is:
  add: V = (A7 & M7 & ~R7) | (~A7 & ~M7 & R7)  (both same sign, result different)
  sub: V = (A7 & ~M7 & ~R7) | (~A7 & M7 & R7)   (different signs, result wrong)
These are the standard 2's complement overflow formulas.
"""

from .regs import CC_S, CC_X, CC_H, CC_I, CC_N, CC_Z, CC_V, CC_C


# ══════════════════════════════════════════════
# 8-bit ALU functions — return (result, flags)
# ══════════════════════════════════════════════
# Each returns a tuple: (result_byte, ccr_flag_bits)
# The caller decides which flag group to apply (HNZVC, NZVC, NZV, etc.)

def add8(a: int, b: int) -> tuple:
    """Add two 8-bit values. Sets H, N, Z, V, C.
    
    H = carry from bit 3 to bit 4 (BCD half-carry)
    N = result bit 7
    Z = result == 0
    V = signed overflow (both same sign → result different sign)
    C = unsigned overflow (result > 255)
    """
    result = a + b
    flags = 0
    if (result & 0xFF) != (result & 0x1FF):  # carry out of bit 7
        flags |= CC_C
    if result & 0x80:
        flags |= CC_N
    if not (result & 0xFF):
        flags |= CC_Z
    # Half carry: carry from bit 3
    if (a & b | a & ~result | b & ~result) & 0x08:
        flags |= CC_H
    # Overflow: both operands same sign, result different
    if (a & b & ~result | ~a & ~b & result) & 0x80:
        flags |= CC_V
    return (result & 0xFF, flags)


def adc8(a: int, b: int, carry: int) -> tuple:
    """Add with carry. Same flag logic as add8 but includes carry in."""
    result = a + b + carry
    flags = 0
    if result > 0xFF:
        flags |= CC_C
    if result & 0x80:
        flags |= CC_N
    if not (result & 0xFF):
        flags |= CC_Z
    if (a & b | a & ~result | b & ~result) & 0x08:
        flags |= CC_H
    if (a & b & ~result | ~a & ~b & result) & 0x80:
        flags |= CC_V
    return (result & 0xFF, flags)


def sub8(a: int, b: int) -> tuple:
    """Subtract two 8-bit values. Sets N, Z, V, C."""
    result = a - b
    flags = 0
    if (result & 0xFF) != result:  # borrow
        flags |= CC_C
    if result & 0x80:
        flags |= CC_N
    if not (result & 0xFF):
        flags |= CC_Z
    if (a & ~b & ~result | ~a & b & result) & 0x80:
        flags |= CC_V
    return (result & 0xFF, flags)


def sbc8(a: int, b: int, carry: int) -> tuple:
    """Subtract with carry (borrow). Same flags as sub8."""
    result = a - b - carry
    flags = 0
    if result < 0:
        flags |= CC_C
    if result & 0x80:
        flags |= CC_N
    if not (result & 0xFF):
        flags |= CC_Z
    if (a & ~b & ~result | ~a & b & result) & 0x80:
        flags |= CC_V
    return (result & 0xFF, flags)


def and8(a: int, b: int) -> tuple:
    """Logical AND. Sets N, Z. Clears V."""
    result = a & b
    flags = 0
    if result & 0x80:
        flags |= CC_N
    if not (result & 0xFF):
        flags |= CC_Z
    return (result & 0xFF, flags)


def or8(a: int, b: int) -> tuple:
    """Logical OR. Sets N, Z. Clears V."""
    result = (a | b) & 0xFF
    flags = 0
    if result & 0x80:
        flags |= CC_N
    if result == 0:
        flags |= CC_Z
    return (result, flags)


def eor8(a: int, b: int) -> tuple:
    """Exclusive OR. Sets N, Z. Clears V."""
    result = a ^ b
    flags = 0
    if result & 0x80:
        flags |= CC_N
    if not (result & 0xFF):
        flags |= CC_Z
    return (result & 0xFF, flags)


def neg8(val: int) -> tuple:
    """Two's complement negate. Sets N, Z, V, C."""
    result = (-val) & 0xFF
    flags = 0
    if result & 0x80:
        flags |= CC_N
    if result == 0:
        flags |= CC_Z
    if result == 0x80:
        flags |= CC_V   # -128 → 128 (can't represent)
    if result != 0:
        flags |= CC_C
    return (result, flags)


def com8(val: int) -> tuple:
    """One's complement. Sets N, Z. Clears V. Sets C."""
    result = (~val) & 0xFF
    flags = CC_C  # C always set
    if result & 0x80:
        flags |= CC_N
    if result == 0:
        flags |= CC_Z
    return (result, flags)


def asl8(val: int) -> tuple:
    """Arithmetic shift left (= logical shift left). Sets N, Z, V, C."""
    result = val << 1
    n = c = 0
    flags = 0
    if result & 0x80:
        flags |= CC_N
        n = 1
    if not (result & 0xFF):
        flags |= CC_Z
    if val & 0x80:
        flags |= CC_C
        c = 1
    if n ^ c:
        flags |= CC_V
    return (result & 0xFF, flags)


def asr8(val: int) -> tuple:
    """Arithmetic shift right (preserves sign). Sets N, Z, V, C."""
    result = ((val & 0xFF) >> 1) | (val & 0x80)  # keep sign bit
    n = c = 0
    flags = 0
    if result & 0x80:
        flags |= CC_N
        n = 1
    if not (result & 0xFF):
        flags |= CC_Z
    if val & 0x01:
        flags |= CC_C
        c = 1
    if n ^ c:
        flags |= CC_V
    return (result & 0xFF, flags)


def lsr8(val: int) -> tuple:
    """Logical shift right. Sets N=0, Z, V=C, C."""
    result = (val & 0xFF) >> 1
    flags = 0
    if not (result & 0xFF):
        flags |= CC_Z
    if val & 0x01:
        flags |= CC_C | CC_V
    return (result & 0xFF, flags)


def rol8(val: int, carry: int) -> tuple:
    """Rotate left through carry. Sets N, Z, V, C."""
    result = ((val << 1) | carry) & 0xFF
    n = c = 0
    flags = 0
    if result & 0x80:
        flags |= CC_N
        n = 1
    if result == 0:
        flags |= CC_Z
    if val & 0x80:
        flags |= CC_C
        c = 1
    if n ^ c:
        flags |= CC_V
    return (result, flags)


def ror8(val: int, carry: int) -> tuple:
    """Rotate right through carry. Sets N, Z, V, C."""
    result = ((val >> 1) | (carry * 0x80)) & 0xFF
    n = c = 0
    flags = 0
    if result & 0x80:
        flags |= CC_N
        n = 1
    if result == 0:
        flags |= CC_Z
    if val & 0x01:
        flags |= CC_C
        c = 1
    if n ^ c:
        flags |= CC_V
    return (result, flags)


def test_nz8(val: int) -> int:
    """Test 8-bit value for N and Z flags only."""
    flags = 0
    if val & 0x80:
        flags |= CC_N
    if not (val & 0xFF):
        flags |= CC_Z
    return flags


# ══════════════════════════════════════════════
# 16-bit ALU functions
# ══════════════════════════════════════════════

def add16(a: int, b: int) -> tuple:
    """Add two 16-bit values. Sets N, Z, V, C (no H for 16-bit)."""
    result = a + b
    flags = 0
    if (result & 0xFFFF) != result:
        flags |= CC_C
    if result & 0x8000:
        flags |= CC_N
    if not (result & 0xFFFF):
        flags |= CC_Z
    if (a & b & ~result | ~a & ~b & result) & 0x8000:
        flags |= CC_V
    return (result & 0xFFFF, flags)


def sub16(a: int, b: int) -> tuple:
    """Subtract two 16-bit values. Sets N, Z, V, C."""
    result = a - b
    flags = 0
    if (result & 0xFFFF) != result:
        flags |= CC_C
    if result & 0x8000:
        flags |= CC_N
    if not (result & 0xFFFF):
        flags |= CC_Z
    if (a & ~b & ~result | ~a & b & result) & 0x8000:
        flags |= CC_V
    return (result & 0xFFFF, flags)


def asl16(val: int) -> tuple:
    """Shift left 16-bit. Sets N, Z, V, C."""
    result = val << 1
    n = c = 0
    flags = 0
    if result & 0x8000:
        flags |= CC_N
        n = 1
    if not (result & 0xFFFF):
        flags |= CC_Z
    if val & 0x8000:
        flags |= CC_C
        c = 1
    if n ^ c:
        flags |= CC_V
    return (result & 0xFFFF, flags)


def lsr16(val: int) -> tuple:
    """Logical shift right 16-bit. Sets Z, C, V=C."""
    result = (val & 0xFFFF) >> 1
    flags = 0
    if not (result & 0xFFFF):
        flags |= CC_Z
    if val & 0x0001:
        flags |= CC_C | CC_V
    return (result & 0xFFFF, flags)


def test_nz16(val: int) -> int:
    """Test 16-bit value for N and Z flags only."""
    flags = 0
    if val & 0x8000:
        flags |= CC_N
    if not (val & 0xFFFF):
        flags |= CC_Z
    return flags


def twos_complement_8(val: int) -> int:
    """Convert unsigned 8-bit to signed Python int (for REL branches)."""
    if val & 0x80:
        return val - 256
    return val
