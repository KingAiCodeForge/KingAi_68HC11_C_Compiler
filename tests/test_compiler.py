"""
Test suite for the KingAI 68HC11 C Compiler.

Tests cover:
  - Basic compilation (no crash)
  - 8-bit arithmetic (ABA, SBA, etc.)
  - 16-bit arithmetic (ADDD, SUBD, ASLD, LSRD)
  - Pointer dereference (general path + direct volatile I/O)
  - Control flow (if, while, for, ternary)
  - Peephole optimizer (TSX dedup, PSHA/PULA removal, while(1))
  - Division/modulo via IDIV
  - Increment/decrement (8-bit and 16-bit)
  - Unary operators (negate, complement, logical not)
  - Known regressions
"""

import pytest
from hc11_compiler import compile_source


def _compile(code: str, target: str = "vy_v6") -> str:
    """Compile C source and return assembly text."""
    return compile_source(code, target=target)


def _lines(asm: str) -> list:
    """Return stripped non-empty non-comment instruction lines."""
    result = []
    for line in asm.split("\n"):
        s = line.strip()
        if s and not s.startswith(";") and not s.startswith(".") and not s.endswith(":"):
            result.append(s)
    return result


# ─── Basic compilation ─────────────────────

class TestBasicCompilation:
    def test_empty_function(self):
        asm = _compile("void main() {}")
        assert "main:" in asm
        assert "RTS" in asm

    def test_simple_assignment(self):
        asm = _compile("void f() { unsigned char x; x = 42; }")
        assert "LDAA    #$2A" in asm

    def test_existing_examples_compile(self):
        """All example files should compile without exceptions."""
        import os
        examples_dir = os.path.join(os.path.dirname(__file__), "..", "examples")
        if os.path.isdir(examples_dir):
            for fname in os.listdir(examples_dir):
                if fname.endswith(".c"):
                    with open(os.path.join(examples_dir, fname), encoding='utf-8') as f:
                        src = f.read()
                    # Should not raise
                    _compile(src)


# ─── 8-bit Arithmetic ─────────────────────

class TestArithmetic8Bit:
    def test_add_chars(self):
        asm = _compile("void f() { unsigned char x; x = 5 + 3; }")
        assert "ABA" in asm

    def test_subtract_chars(self):
        asm = _compile("void f() { unsigned char a; a = 10 - 3; }")
        assert "SBA" in asm

    def test_bitwise_and(self):
        asm = _compile("void f() { unsigned char x; x = 0xFF & 0x0F; }")
        assert "ANDA" in asm

    def test_bitwise_or(self):
        asm = _compile("void f() { unsigned char x; x = 0x0F | 0xF0; }")
        assert "ORAA" in asm

    def test_bitwise_xor(self):
        asm = _compile("void f() { unsigned char x; x = 0xAA ^ 0x55; }")
        assert "EORA" in asm

    def test_shift_left(self):
        asm = _compile("void f() { unsigned char x; x = 1 << 3; }")
        assert "ASLA" in asm

    def test_shift_right(self):
        asm = _compile("void f() { unsigned char x; x = 0x80 >> 2; }")
        assert "LSRA" in asm

    def test_multiply(self):
        asm = _compile("void f() { unsigned char x; x = 5 * 3; }")
        assert "MUL" in asm


# ─── 16-bit Arithmetic ────────────────────

class TestArithmetic16Bit:
    def test_add_ints(self):
        asm = _compile("void f() { int a; int b; a = 1000; b = 500; a = a + b; }")
        assert "ADDD" in asm

    def test_subtract_ints(self):
        asm = _compile("void f() { int a; a = 1000; a = a - 100; }")
        assert "SUBD" in asm

    def test_large_literal_uses_ldd(self):
        asm = _compile("void f() { int x; x = 1000; }")
        assert "LDD     #$03E8" in asm

    def test_int_comparison_uses_subd(self):
        """16-bit comparison should use SUBD (not CBA)."""
        asm = _compile("void f() { int a; a = 500; if (a > 100) { a = 0; } }")
        assert "SUBD" in asm

    def test_shift_left_16bit(self):
        asm = _compile("void f() { int x; x = 256; x = x << 1; }")
        assert "ASLD" in asm

    def test_shift_right_16bit(self):
        asm = _compile("void f() { int x; x = 256; x = x >> 1; }")
        assert "LSRD" in asm

    def test_int_increment(self):
        asm = _compile("void f() { int x; x = 100; ++x; }")
        assert "ADDD    #$0001" in asm

    def test_int_decrement(self):
        asm = _compile("void f() { int x; x = 100; --x; }")
        assert "SUBD    #$0001" in asm


# ─── Pointer dereference ──────────────────

class TestPointerDeref:
    def test_volatile_direct_read(self):
        """*(volatile unsigned char *)0x1030 should emit LDAA $1030."""
        asm = _compile("""
        void f() {
            unsigned char x;
            x = *((volatile unsigned char *)0x1030);
        }
        """)
        assert "LDAA    $1030" in asm

    def test_volatile_direct_write(self):
        """*(volatile unsigned char *)0x1030 = val should emit STAA $1030."""
        asm = _compile("""
        void f() {
            unsigned char x;
            x = 0x42;
            *((volatile unsigned char *)0x1030) = x;
        }
        """)
        assert "STAA    $1030" in asm

    def test_no_tab_clra_xgdx_in_deref_store(self):
        """The old pointer corruption bug: TAB+CLRA before XGDX is gone."""
        asm = _compile("""
        void f() {
            unsigned char *p;
            unsigned char v;
            v = 5;
            *p = v;
        }
        """)
        lines = asm.split("\n")
        for i, line in enumerate(lines):
            if "TAB" in line and i + 1 < len(lines) and "CLRA" in lines[i + 1]:
                if i + 2 < len(lines) and "XGDX" in lines[i + 2]:
                    pytest.fail("Found TAB+CLRA+XGDX sequence — pointer corruption bug")


# ─── No phantom instructions ──────────────

class TestInstructionCorrectness:
    def test_no_leas(self):
        """LEAS is not an HC11 instruction."""
        asm = _compile("void f() { unsigned char a; unsigned char b; a = 1; b = 2; }")
        assert "LEAS" not in asm

    def test_no_div8_call(self):
        """__div8 helper no longer exists — division uses IDIV directly."""
        asm = _compile("void f() { unsigned char x; x = 10 / 3; }")
        assert "__div8" not in asm
        assert "IDIV" in asm

    def test_no_mod8_call(self):
        asm = _compile("void f() { unsigned char x; x = 10 % 3; }")
        assert "__mod8" not in asm
        assert "IDIV" in asm


# ─── Control flow ─────────────────────────

class TestControlFlow:
    def test_if_generates_beq(self):
        asm = _compile("void f() { unsigned char x; x = 1; if (x) { x = 0; } }")
        assert "BEQ" in asm

    def test_while_generates_bra(self):
        asm = _compile("void f() { unsigned char x; x = 5; while (x) { x = x - 1; } }")
        assert "BRA" in asm

    def test_while_1_optimized(self):
        """while(1) should not contain LDAA #$01 + BEQ (peephole removes them)."""
        asm = _compile("""
        void f() {
            while (1) {
                asm("NOP");
            }
        }
        """)
        lines = _lines(asm)
        # Should have BRA to loop top, but no LDAA #$01 or BEQ
        has_bra = any("BRA" in l for l in lines)
        has_ldaa_01_beq = False
        for i, l in enumerate(lines):
            if "LDAA" in l and "#$01" in l and i + 1 < len(lines) and "BEQ" in lines[i + 1]:
                has_ldaa_01_beq = True
        assert has_bra
        assert not has_ldaa_01_beq

    def test_for_loop(self):
        asm = _compile("""
        void f() {
            unsigned char i;
            for (i = 0; i < 10; i++) {
                asm("NOP");
            }
        }
        """)
        assert "BRA" in asm

    def test_isr_uses_rti(self):
        asm = _compile("""
        __interrupt void my_isr() {
            unsigned char x;
            x = 1;
        }
        """)
        assert "RTI" in asm


# ─── Unary operators ──────────────────────

class TestUnaryOps:
    def test_negate_8bit(self):
        asm = _compile("void f() { unsigned char x; x = 5; x = -x; }")
        assert "NEGA" in asm

    def test_complement_8bit(self):
        asm = _compile("void f() { unsigned char x; x = 0xFF; x = ~x; }")
        assert "COMA" in asm

    def test_negate_16bit(self):
        """16-bit negation uses COMA+COMB+ADDD #1."""
        asm = _compile("void f() { int x; x = 1000; x = -x; }")
        assert "COMA" in asm
        assert "COMB" in asm
        assert "ADDD    #$0001" in asm


# ─── Peephole Optimizer ──────────────────

class TestPeepholeOptimizer:
    def test_no_consecutive_tsx(self):
        """Adjacent TSX instructions should be collapsed to one."""
        from hc11_compiler.optimizer import optimize
        lines = ["        TSX", "        TSX", "        LDAA    0,X"]
        result = optimize(lines)
        tsx_count = sum(1 for l in result if "TSX" in l)
        assert tsx_count == 1

    def test_psha_pula_removed(self):
        from hc11_compiler.optimizer import optimize
        lines = ["        PSHA", "        PULA"]
        result = optimize(lines)
        assert len(result) == 0

    def test_tab_tba_removed(self):
        from hc11_compiler.optimizer import optimize
        lines = ["        TAB", "        TBA"]
        result = optimize(lines)
        assert len(result) == 0

    def test_ldaa_tsta_collapses(self):
        from hc11_compiler.optimizer import optimize
        lines = ["        LDAA    #$05", "        TSTA"]
        result = optimize(lines)
        assert len(result) == 1
        assert "LDAA" in result[0]

    def test_ldd_subd_0_collapses(self):
        from hc11_compiler.optimizer import optimize
        lines = ["        LDD     #$03E8", "        SUBD    #$0000  ; test D == 0"]
        result = optimize(lines)
        assert len(result) == 1
        assert "LDD" in result[0]


# ─── Target profiles ─────────────────────

class TestTargetProfiles:
    def test_generic_target(self):
        asm = _compile("void main() {}", target="generic")
        assert "ORG     $8000" in asm

    def test_vy_v6_target(self):
        asm = _compile("void main() {}", target="vy_v6")
        assert "VY V6" in asm

    def test_unknown_target_falls_back(self):
        """Unknown target should fall back to generic without crashing."""
        asm = _compile("void main() {}", target="nonexistent")
        assert "main:" in asm
