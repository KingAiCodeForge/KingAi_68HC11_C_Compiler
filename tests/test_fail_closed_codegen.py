"""Fail-closed regression tests for the KCOS/relocatable HC11 compiler lane."""

import pytest

from hc11_compiler import compile_source
from hc11_compiler.ast_nodes import ASTNode, BinaryOp, IntLiteral, UnaryOp
from hc11_compiler.codegen import CodeGenError, CodeGenerator


class UnknownStatement(ASTNode):
    pass


class UnknownExpression(ASTNode):
    pass


def test_unknown_statement_is_hard_error_not_todo_assembly():
    gen = CodeGenerator(target="vy_v6")
    with pytest.raises(CodeGenError, match="Unhandled statement type"):
        gen._gen_statement(UnknownStatement(line=1, col=1))


def test_unknown_expression_is_hard_error_not_default_int():
    gen = CodeGenerator(target="vy_v6")
    with pytest.raises(CodeGenError, match="Unhandled expression type"):
        gen._gen_expr(UnknownExpression(line=1, col=1))


def test_unknown_binary_operator_is_hard_error():
    gen = CodeGenerator(target="vy_v6")
    expr = BinaryOp(
        op="**",
        left=IntLiteral(value=2, line=1, col=1),
        right=IntLiteral(value=3, line=1, col=6),
        line=1,
        col=3,
    )
    with pytest.raises(CodeGenError, match="Unsupported .* binary operator"):
        gen._gen_expr(expr)


def test_unknown_unary_operator_is_hard_error():
    gen = CodeGenerator(target="vy_v6")
    expr = UnaryOp(
        op="@",
        operand=IntLiteral(value=1, line=1, col=2),
        line=1,
        col=1,
    )
    with pytest.raises(CodeGenError, match="Unsupported unary operator"):
        gen._gen_expr(expr)


@pytest.mark.parametrize(
    "source, message",
    [
        (
            "void f(void) { unsigned char a[2]; a[0] += 1; }",
            "Unsupported compound assignment target",
        ),
        (
            "void f(void) { unsigned char a[2]; ++a[0]; }",
            "Unsupported pre-\+\+ target",
        ),
        (
            "void f(void) { unsigned char a[2]; a[0]++; }",
            "Unsupported post-\+\+ target",
        ),
    ],
)
def test_complex_mutating_lvalues_fail_instead_of_emitting_partial_code(source, message):
    with pytest.raises(CodeGenError, match=message):
        compile_source(source, target="vy_v6", output="asm")


def test_supported_codegen_contains_no_todo_markers():
    source = """
    struct Pair {
        unsigned char flag;
        unsigned int value;
    };

    unsigned char samples[8];
    struct Pair state;

    unsigned char update(unsigned char i) {
        samples[i] = 7;
        state.flag = samples[i];
        state.value = 0x1234;
        if (state.flag) {
            return samples[i];
        }
        return 0;
    }
    """
    asm = compile_source(source, target="vy_v6", output="asm")
    assert "TODO:" not in asm
