"""
AST Node definitions for the 68HC11 C Compiler.

Defines the Abstract Syntax Tree structure produced by the parser
and consumed by the code generator. Each node type represents a
syntactic construct in the supported C subset.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Union


# ──────────────────────────────────────────────
# Type system
# ──────────────────────────────────────────────

@dataclass
class CType:
    """Represents a C data type."""
    base: str                   # "void", "char", "int"
    is_unsigned: bool = False
    is_volatile: bool = False
    is_const: bool = False
    is_static: bool = False
    is_extern: bool = False
    pointer_depth: int = 0      # 0 = not a pointer, 1 = *, 2 = **, etc.
    array_len: Optional[int] = None
    struct_name: Optional[str] = None
    struct_size: int = 0

    @property
    def scalar_size(self) -> int:
        """Size of one scalar/aggregate element, ignoring an array declarator."""
        if self.pointer_depth > 0:
            return 2  # All pointers are 16-bit
        if self.base == "void":
            return 0
        if self.base == "char":
            return 1
        if self.base == "int":
            return 2
        if self.base == "struct":
            return self.struct_size
        return 2  # conservative default

    @property
    def size(self) -> int:
        """Storage size in bytes on the 68HC11."""
        if self.array_len is not None and self.pointer_depth == 0:
            return self.scalar_size * self.array_len
        return self.scalar_size

    @property
    def is_array(self) -> bool:
        return self.array_len is not None and self.pointer_depth == 0

    def element_type(self) -> "CType":
        """Return the element type for an array, or pointed-to type for a pointer."""
        if self.is_array:
            return CType(
                base=self.base,
                is_unsigned=self.is_unsigned,
                is_volatile=self.is_volatile,
                is_const=self.is_const,
                is_static=self.is_static,
                is_extern=self.is_extern,
                pointer_depth=self.pointer_depth,
                struct_name=self.struct_name,
                struct_size=self.struct_size,
            )
        if self.pointer_depth > 0:
            return self.pointed_to()
        return self

    @property
    def is_pointer(self) -> bool:
        return self.pointer_depth > 0

    @property
    def is_byte(self) -> bool:
        return self.size == 1 and self.pointer_depth == 0

    @property
    def is_word(self) -> bool:
        return self.size == 2

    def pointed_to(self) -> CType:
        """Return the type this pointer points to."""
        assert self.pointer_depth > 0
        return CType(
            base=self.base,
            is_unsigned=self.is_unsigned,
            is_volatile=self.is_volatile,
            is_const=self.is_const,
            is_static=self.is_static,
            is_extern=self.is_extern,
            pointer_depth=self.pointer_depth - 1,
            struct_name=self.struct_name,
            struct_size=self.struct_size,
        )

    def pointer_to(self) -> CType:
        """Return a pointer-to-this type."""
        return CType(
            base=self.base,
            is_unsigned=self.is_unsigned,
            is_volatile=self.is_volatile,
            is_const=self.is_const,
            is_static=self.is_static,
            is_extern=self.is_extern,
            pointer_depth=self.pointer_depth + 1,
            struct_name=self.struct_name,
            struct_size=self.struct_size,
        )

    def __str__(self) -> str:
        parts = []
        if self.is_const:
            parts.append("const")
        if self.is_volatile:
            parts.append("volatile")
        if self.is_extern:
            parts.append("extern")
        if self.is_unsigned:
            parts.append("unsigned")
        if self.base == "struct" and self.struct_name:
            parts.extend(["struct", self.struct_name])
        else:
            parts.append(self.base)
        parts.append("*" * self.pointer_depth)
        rendered = " ".join(p for p in parts if p)
        if self.array_len is not None:
            rendered += f"[{self.array_len}]"
        return rendered


# ──────────────────────────────────────────────
# Base AST node
# ──────────────────────────────────────────────

@dataclass
class ASTNode:
    """Base class for all AST nodes."""
    line: int = 0
    col: int = 0


# ──────────────────────────────────────────────
# Top-level: Program
# ──────────────────────────────────────────────

@dataclass
class Program(ASTNode):
    """Root node: a list of top-level declarations."""
    declarations: List[ASTNode] = field(default_factory=list)


# ──────────────────────────────────────────────
# Declarations
# ──────────────────────────────────────────────

@dataclass
class VarDecl(ASTNode):
    """Variable declaration, possibly with initializer."""
    name: str = ""
    ctype: CType = field(default_factory=lambda: CType("int"))
    init: Optional[Expression] = None
    is_zeropage: bool = False       # Place in direct page ($00-$FF)
    fixed_addr: Optional[int] = None  # Place at specific address

@dataclass
class FuncParam(ASTNode):
    """Function parameter."""
    name: str = ""
    ctype: CType = field(default_factory=lambda: CType("int"))

@dataclass
class FuncDecl(ASTNode):
    """Function definition."""
    name: str = ""
    return_type: CType = field(default_factory=lambda: CType("void"))
    params: List[FuncParam] = field(default_factory=list)
    body: Optional[Block] = None
    is_interrupt: bool = False      # ISR — use RTI, save all regs
    is_static: bool = False

@dataclass
class TypedefDecl(ASTNode):
    """Typedef declaration."""
    name: str = ""
    ctype: CType = field(default_factory=lambda: CType("int"))


@dataclass
class StructField(ASTNode):
    """One field in a named struct, with byte offset fixed by the parser."""
    name: str = ""
    ctype: CType = field(default_factory=lambda: CType("int"))
    offset: int = 0


@dataclass
class StructDecl(ASTNode):
    """Named struct definition."""
    name: str = ""
    fields: List[StructField] = field(default_factory=list)
    size: int = 0


# ──────────────────────────────────────────────
# Statements
# ──────────────────────────────────────────────

@dataclass
class Block(ASTNode):
    """Compound statement: { ... }"""
    statements: List[ASTNode] = field(default_factory=list)

@dataclass
class ExprStatement(ASTNode):
    """Expression used as a statement (e.g., function call, assignment)."""
    expr: Expression = None  # type: ignore

@dataclass
class ReturnStmt(ASTNode):
    """return [expr];"""
    value: Optional[Expression] = None

@dataclass
class IfStmt(ASTNode):
    """if (cond) then_body [else else_body]"""
    condition: Expression = None  # type: ignore
    then_body: ASTNode = None     # type: ignore
    else_body: Optional[ASTNode] = None

@dataclass
class WhileStmt(ASTNode):
    """while (cond) body"""
    condition: Expression = None  # type: ignore
    body: ASTNode = None          # type: ignore

@dataclass
class DoWhileStmt(ASTNode):
    """do body while (cond);"""
    condition: Expression = None  # type: ignore
    body: ASTNode = None          # type: ignore

@dataclass
class ForStmt(ASTNode):
    """for (init; cond; update) body"""
    init: Optional[ASTNode] = None
    condition: Optional[Expression] = None
    update: Optional[Expression] = None
    body: ASTNode = None          # type: ignore

@dataclass
class BreakStmt(ASTNode):
    """break;"""
    pass

@dataclass
class ContinueStmt(ASTNode):
    """continue;"""
    pass

@dataclass
class AsmStmt(ASTNode):
    """Inline assembly: asm("instruction");"""
    instructions: str = ""


# ──────────────────────────────────────────────
# Expressions
# ──────────────────────────────────────────────

Expression = Union[
    "IntLiteral", "CharLiteral", "StringLiteral",
    "Identifier", "BinaryOp", "UnaryOp",
    "Assignment", "CompoundAssignment",
    "FuncCall", "Cast", "Deref", "AddrOf",
    "ArraySubscript", "MemberAccess",
    "SizeofExpr", "TernaryOp",
    "PreIncDec", "PostIncDec",
]

@dataclass
class IntLiteral(ASTNode):
    """Integer constant."""
    value: int = 0

@dataclass
class CharLiteral(ASTNode):
    """Character constant."""
    value: int = 0

@dataclass
class StringLiteral(ASTNode):
    """String constant (for asm() usage mainly)."""
    value: str = ""

@dataclass
class Identifier(ASTNode):
    """Variable or function reference."""
    name: str = ""

@dataclass
class BinaryOp(ASTNode):
    """Binary operation: left op right."""
    op: str = ""
    left: Expression = None   # type: ignore
    right: Expression = None  # type: ignore

@dataclass
class UnaryOp(ASTNode):
    """Unary operation: op operand (prefix)."""
    op: str = ""              # -, ~, !, etc.
    operand: Expression = None  # type: ignore

@dataclass
class Assignment(ASTNode):
    """Simple assignment: target = value."""
    target: Expression = None  # type: ignore
    value: Expression = None   # type: ignore

@dataclass
class CompoundAssignment(ASTNode):
    """Compound assignment: target op= value."""
    op: str = ""              # +=, -=, |=, &=, ^=, <<=, >>=
    target: Expression = None  # type: ignore
    value: Expression = None   # type: ignore

@dataclass
class FuncCall(ASTNode):
    """Function call: name(args...)."""
    name: str = ""
    args: List[Expression] = field(default_factory=list)

@dataclass
class Cast(ASTNode):
    """Type cast: (type)expr."""
    cast_type: CType = field(default_factory=lambda: CType("int"))
    expr: Expression = None  # type: ignore

@dataclass
class Deref(ASTNode):
    """Pointer dereference: *ptr."""
    expr: Expression = None  # type: ignore

@dataclass
class AddrOf(ASTNode):
    """Address-of: &var."""
    expr: Expression = None  # type: ignore

@dataclass
class ArraySubscript(ASTNode):
    """Array subscript: arr[index]."""
    array: Expression = None  # type: ignore
    index: Expression = None  # type: ignore

@dataclass
class MemberAccess(ASTNode):
    """Struct member access: obj.member or ptr->member."""
    object: Expression = None  # type: ignore
    member: str = ""
    is_arrow: bool = False

@dataclass
class SizeofExpr(ASTNode):
    """sizeof(type) or sizeof(expr)."""
    target_type: Optional[CType] = None
    target_expr: Optional[Expression] = None

@dataclass
class TernaryOp(ASTNode):
    """Ternary: cond ? then_expr : else_expr."""
    condition: Expression = None   # type: ignore
    then_expr: Expression = None   # type: ignore
    else_expr: Expression = None   # type: ignore

@dataclass
class PreIncDec(ASTNode):
    """Pre-increment/decrement: ++x or --x."""
    op: str = ""              # "++" or "--"
    operand: Expression = None  # type: ignore

@dataclass
class PostIncDec(ASTNode):
    """Post-increment/decrement: x++ or x--."""
    op: str = ""
    operand: Expression = None  # type: ignore
