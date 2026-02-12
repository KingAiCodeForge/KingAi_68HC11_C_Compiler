"""
68HC11 Code Generator for the KingAI C Compiler.

Translates the AST into Motorola 68HC11 assembly language.

Register usage convention:
  - AccA / AccB (8-bit): primary working registers
  - AccD (A:B combined, 16-bit): 16-bit arithmetic
  - X: index register, used for stack-frame access (via TSX) and pointers
  - Y: secondary index register, used for second pointer operand
  - SP: stack pointer (grows downward)

Function calling convention:
  - Arguments pushed right-to-left on stack
  - Return value in AccA (8-bit) or AccD (16-bit)
  - Caller cleans up arguments after call
  - Callee saves/restores X and Y if used
  - ISRs save all registers automatically (RTI restores them)

Memory layout:
  - $0000-$00FF: Zero page / direct page RAM (fast access)
  - $0100-$03FF: Extended RAM (HC11F1 has 1KB total)
  - $1000-$105F: I/O registers
  - $2000-$7FFF: Always visible (calibration/shared code)
  - $8000-$FFFF: Bank-switched program ROM
  - $FFD6-$FFFF: Interrupt vector table
"""

from __future__ import annotations
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from .ast_nodes import *
from .optimizer import optimize as peephole_optimize


# ──────────────────────────────────────────────
# Symbol / scope tracking
# ──────────────────────────────────────────────

@dataclass
class Symbol:
    name: str
    ctype: CType
    is_global: bool = True
    is_zeropage: bool = False
    stack_offset: int = 0         # offset from frame pointer (X after TSX)
    fixed_addr: Optional[int] = None
    is_param: bool = False

@dataclass
class Scope:
    symbols: Dict[str, Symbol] = field(default_factory=dict)
    parent: Optional[Scope] = None

    def lookup(self, name: str) -> Optional[Symbol]:
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        return None

    def define(self, sym: Symbol):
        self.symbols[sym.name] = sym


# ──────────────────────────────────────────────
# Target profiles for specific PCMs
# ──────────────────────────────────────────────

TARGET_PROFILES = {
    "generic": {
        "org": 0x8000,
        "stack": 0x00FF,
        "ram_start": 0x0000,
        "ram_end": 0x00FF,
        "io_base": 0x1000,
        "vectors": 0xFFD6,
        "description": "Generic 68HC11 target",
    },
    "vy_v6": {
        "org": 0x8000,
        "stack": 0x03FF,
        "ram_start": 0x0000,
        "ram_end": 0x03FF,
        "io_base": 0x1000,
        "vectors": 0xFFD6,
        "bank_select_port": 0x03,
        "bank_select_bit": 3,
        "description": "VY V6 PCM (09356445) - HC11F1, 128KB bank-switched",
    },
    "1227730": {
        "org": 0x8000,
        "stack": 0x00FF,
        "ram_start": 0x0000,
        "ram_end": 0x00FF,
        "io_base": 0x1000,
        "vectors": 0xFFD6,
        "description": "Delco 1227730 PCM - 27C256 (32KB)",
    },
    "16197427": {
        "org": 0x8000,
        "stack": 0x01FF,
        "ram_start": 0x0000,
        "ram_end": 0x01FF,
        "io_base": 0x1000,
        "vectors": 0xFFD6,
        "description": "Delco 16197427 PCM - 27C512 (64KB) bank-switched",
    },
}


class CodeGenError(Exception):
    def __init__(self, message: str, node: ASTNode):
        self.node = node
        super().__init__(f"Code generation error at L{node.line}:{node.col}: {message}")


class CodeGenerator:
    """Generates 68HC11 assembly from AST."""

    def __init__(self, org: int = 0x8000, stack: int = 0x00FF,
                 target: str = "generic"):
        self.org = org
        self.stack = stack
        self.target = target
        self.profile = TARGET_PROFILES.get(target, TARGET_PROFILES["generic"])

        # Output sections
        self._header_lines: List[str] = []
        self._data_lines: List[str] = []
        self._bss_lines: List[str] = []
        self._code_lines: List[str] = []
        self._vector_lines: List[str] = []

        # State
        self._global_scope = Scope()
        self._current_scope: Scope = self._global_scope
        self._label_counter = 0
        self._local_offset = 0          # Current stack frame size
        self._in_function: Optional[FuncDecl] = None
        self._zp_alloc = 0x0040         # Next free zero-page address
        self._ram_alloc = 0x0100        # Next free extended RAM address
        self._scratch_addr = 0x003F     # Reserved direct-page scratch byte (never allocated to vars)
        self._string_literals: Dict[str, str] = {}  # label -> string data
        self._isr_vectors: Dict[str, str] = {}       # vector name -> function label
        self._break_labels: List[str] = []
        self._continue_labels: List[str] = []

    # ── Label generation ──────────────────────

    def _label(self, prefix: str = "L") -> str:
        self._label_counter += 1
        return f".{prefix}{self._label_counter}"

    # ── Output helpers ────────────────────────

    def _emit(self, line: str):
        """Emit an assembly instruction to the code section."""
        self._code_lines.append(f"        {line}")

    def _emit_label(self, label: str):
        """Emit an assembly label."""
        self._code_lines.append(f"{label}:")

    def _emit_comment(self, text: str):
        """Emit a comment."""
        self._code_lines.append(f"        ; {text}")

    def _emit_blank(self):
        self._code_lines.append("")

    # ── Format helpers ────────────────────────

    @staticmethod
    def _hex8(val: int) -> str:
        return f"${val & 0xFF:02X}"

    @staticmethod
    def _hex16(val: int) -> str:
        return f"${val & 0xFFFF:04X}"

    @staticmethod
    def _imm8(val: int) -> str:
        return f"#${val & 0xFF:02X}"

    @staticmethod
    def _imm16(val: int) -> str:
        return f"#${val & 0xFFFF:04X}"

    # ── Width-aware condition test ──────────

    def _emit_test_zero(self, ctype: CType):
        """Emit instructions to test if value in A (8-bit) or D (16-bit) is zero.

        Sets Z flag: Z=1 if value is zero, Z=0 if nonzero.
        For 8-bit: TSTA is sufficient.
        For 16-bit: need to test both A and B since TSTA only checks A.
        Uses PSHA; ORAB scratch; PULA pattern, or simpler: STD+LDD test.
        Actually the simplest HC11 pattern for testing D==0:
          SUBD #$0000  — sets Z if D was 0. But changes D (to same value).
          Actually SUBD #0 doesn't change D but sets flags. Perfect.
        """
        if ctype.is_word:
            # Test 16-bit D for zero. SUBD #0 sets Z flag based on full D.
            self._emit("SUBD    #$0000  ; test D == 0")
        else:
            self._emit("TSTA")

    # ── Main generation entry point ───────────

    def generate(self, program: Program) -> str:
        """Generate complete assembly output from a Program AST."""
        self._generate_header()

        # First pass: collect global declarations
        for decl in program.declarations:
            if isinstance(decl, VarDecl):
                self._gen_global_var(decl)
            elif isinstance(decl, FuncDecl):
                self._register_function(decl)

        # Second pass: generate code for functions
        for decl in program.declarations:
            if isinstance(decl, FuncDecl):
                self._gen_function(decl)

        # Generate string literal data
        self._gen_string_data()

        # Generate vector table
        self._gen_vector_table()

        # Apply peephole optimizer to code section
        self._code_lines = peephole_optimize(self._code_lines)

        return self._assemble_output()

    def _generate_header(self):
        desc = self.profile.get("description", self.target)
        self._header_lines = [
            f"; ════════════════════════════════════════════",
            f"; KingAI 68HC11 C Compiler Output",
            f"; Target: {desc}",
            f"; ════════════════════════════════════════════",
            f"",
            f"; ── Memory Configuration ──",
            f"        ORG     {self._hex16(self.org)}",
            f"",
        ]

    def _assemble_output(self) -> str:
        sections = []
        sections.extend(self._header_lines)

        if self._data_lines:
            sections.append("; ── Initialized Data ──")
            sections.extend(self._data_lines)
            sections.append("")

        if self._bss_lines:
            sections.append("; ── Uninitialized Data (BSS) ──")
            sections.extend(self._bss_lines)
            sections.append("")

        sections.append("; ── Code ──")
        sections.extend(self._code_lines)

        if self._vector_lines:
            sections.append("")
            sections.append("; ── Interrupt Vectors ──")
            sections.extend(self._vector_lines)

        sections.append("")
        sections.append("; ── End ──")
        return "\n".join(sections)

    # ── Global variable generation ────────────

    def _gen_global_var(self, decl: VarDecl):
        sym = Symbol(
            name=decl.name,
            ctype=decl.ctype,
            is_global=True,
            is_zeropage=decl.is_zeropage,
            fixed_addr=decl.fixed_addr,
        )

        if decl.is_zeropage:
            addr = self._zp_alloc
            self._zp_alloc += decl.ctype.size
            sym.fixed_addr = addr
        elif decl.fixed_addr is not None:
            addr = decl.fixed_addr
        else:
            addr = self._ram_alloc
            self._ram_alloc += decl.ctype.size
            sym.fixed_addr = addr

        self._global_scope.define(sym)

        if decl.init and isinstance(decl.init, IntLiteral):
            if decl.ctype.size == 1:
                self._data_lines.append(
                    f"{decl.name}:   EQU     {self._hex16(addr)}    ; {decl.ctype} (init={self._hex8(decl.init.value)})"
                )
            else:
                self._data_lines.append(
                    f"{decl.name}:   EQU     {self._hex16(addr)}    ; {decl.ctype} (init={self._hex16(decl.init.value)})"
                )
        else:
            self._data_lines.append(
                f"{decl.name}:   EQU     {self._hex16(addr)}    ; {decl.ctype}"
            )

    # ── Function generation ───────────────────

    def _register_function(self, decl: FuncDecl):
        sym = Symbol(
            name=decl.name,
            ctype=decl.return_type,
            is_global=True,
        )
        self._global_scope.define(sym)

    def _gen_function(self, decl: FuncDecl):
        self._in_function = decl
        self._emit_blank()
        self._emit_comment(f"{'ISR' if decl.is_interrupt else 'Function'}: {decl.name}")
        self._emit_label(decl.name)

        # Create new scope for function body
        func_scope = Scope(parent=self._global_scope)
        self._current_scope = func_scope
        self._local_offset = 0

        # Prologue
        if not decl.is_interrupt:
            # Save frame: push X (old frame pointer)
            self._emit("PSHX")
            self._emit("TSX")            # X = SP+1 (frame pointer)

        # Allocate parameter symbols
        # After PSHX + TSX, stack looks like:
        #   [X+0] = saved XH
        #   [X+1] = saved XL
        #   [X+2] = return addr H
        #   [X+3] = return addr L
        #   [X+4] = first param (or first param high byte)
        param_offset = 4  # past saved X (2) + return addr (2)
        for param in decl.params:
            sym = Symbol(
                name=param.name,
                ctype=param.ctype,
                is_global=False,
                stack_offset=param_offset,
                is_param=True,
            )
            func_scope.define(sym)
            param_offset += param.ctype.size

        # Generate body
        if decl.body:
            for stmt in decl.body.statements:
                self._gen_statement(stmt)

        # Epilogue
        if decl.is_interrupt:
            self._emit("RTI")
        else:
            # Default return (if no explicit return was generated)
            if not (decl.body and decl.body.statements and
                    isinstance(decl.body.statements[-1], ReturnStmt)):
                if self._local_offset > 0:
                    # Deallocate locals (HC11 has no LEAS — use INS loop)
                    for _ in range(self._local_offset):
                        self._emit("INS")
                    self._emit_comment(f"free {self._local_offset} bytes locals")
                self._emit("PULX")       # restore old frame pointer
                self._emit("RTS")

        self._in_function = None
        self._current_scope = self._global_scope

    # ── Statement generation ──────────────────

    def _gen_statement(self, stmt: ASTNode):
        if isinstance(stmt, VarDecl):
            self._gen_local_var(stmt)
        elif isinstance(stmt, ExprStatement):
            self._gen_expr(stmt.expr)
        elif isinstance(stmt, ReturnStmt):
            self._gen_return(stmt)
        elif isinstance(stmt, IfStmt):
            self._gen_if(stmt)
        elif isinstance(stmt, WhileStmt):
            self._gen_while(stmt)
        elif isinstance(stmt, DoWhileStmt):
            self._gen_do_while(stmt)
        elif isinstance(stmt, ForStmt):
            self._gen_for(stmt)
        elif isinstance(stmt, Block):
            for s in stmt.statements:
                self._gen_statement(s)
        elif isinstance(stmt, AsmStmt):
            self._gen_asm(stmt)
        elif isinstance(stmt, BreakStmt):
            self._gen_break(stmt)
        elif isinstance(stmt, ContinueStmt):
            self._gen_continue(stmt)
        else:
            self._emit_comment(f"TODO: unhandled statement type {type(stmt).__name__}")

    def _gen_local_var(self, decl: VarDecl):
        """Allocate a local variable on the stack."""
        size = decl.ctype.size
        self._local_offset += size

        sym = Symbol(
            name=decl.name,
            ctype=decl.ctype,
            is_global=False,
            # TSX puts SP+1 in X. After pushing N bytes of locals,
            # the first local is at X+0, second at X+size_of_first, etc.
            # But we need to allocate stack space first.
            stack_offset=0,  # will calculate below
            is_zeropage=decl.is_zeropage,
        )

        # Allocate stack space
        if size == 1:
            self._emit(f"DES")           # SP -= 1
            self._emit_comment(f"local: {decl.ctype} {decl.name}")
        else:
            for _ in range(size):
                self._emit("DES")
            self._emit_comment(f"local: {decl.ctype} {decl.name}")

        # After DES, TSX gives X = SP+1, and the new variable is at X+0
        # But if we had previous locals, we need to account for them
        # The offset from current X depends on how many locals we've declared
        # For simplicity: re-TSX after each local allocation
        sym.stack_offset = 0  # Will be at top of stack after TSX

        self._current_scope.define(sym)

        # Initialize if there's an initializer
        if decl.init:
            self._gen_expr(decl.init)
            self._emit("TSX")
            if decl.ctype.size == 1:
                self._emit(f"STAA    0,X     ; store {decl.name}")
            else:
                self._emit(f"STD     0,X     ; store {decl.name}")

    def _gen_return(self, stmt: ReturnStmt):
        """Generate return statement."""
        if stmt.value:
            self._gen_expr(stmt.value)
            # Result already in A (8-bit) or D (16-bit)

        if self._local_offset > 0:
            # Deallocate locals by adjusting SP
            for _ in range(self._local_offset):
                self._emit("INS")
        self._emit("PULX")       # restore old frame pointer
        self._emit("RTS")

    def _gen_if(self, stmt: IfStmt):
        """Generate if/else statement."""
        else_label = self._label("else")
        end_label = self._label("endif")

        # Evaluate condition — result in A or D
        cond_type = self._gen_expr(stmt.condition)

        # Branch if zero (false)
        self._emit_test_zero(cond_type)
        if stmt.else_body:
            self._emit(f"BEQ     {else_label}")
        else:
            self._emit(f"BEQ     {end_label}")

        # Then body
        self._gen_statement(stmt.then_body)

        if stmt.else_body:
            self._emit(f"BRA     {end_label}")
            self._emit_label(else_label)
            self._gen_statement(stmt.else_body)

        self._emit_label(end_label)

    def _gen_while(self, stmt: WhileStmt):
        """Generate while loop."""
        top_label = self._label("while")
        end_label = self._label("endwhile")

        self._break_labels.append(end_label)
        self._continue_labels.append(top_label)

        self._emit_label(top_label)
        cond_type = self._gen_expr(stmt.condition)
        self._emit_test_zero(cond_type)
        self._emit(f"BEQ     {end_label}")

        self._gen_statement(stmt.body)
        self._emit(f"BRA     {top_label}")

        self._emit_label(end_label)

        self._break_labels.pop()
        self._continue_labels.pop()

    def _gen_do_while(self, stmt: DoWhileStmt):
        """Generate do-while loop."""
        top_label = self._label("do")
        cond_label = self._label("dotest")
        end_label = self._label("enddo")

        self._break_labels.append(end_label)
        self._continue_labels.append(cond_label)

        self._emit_label(top_label)
        self._gen_statement(stmt.body)

        self._emit_label(cond_label)
        cond_type = self._gen_expr(stmt.condition)
        self._emit_test_zero(cond_type)
        self._emit(f"BNE     {top_label}")

        self._emit_label(end_label)

        self._break_labels.pop()
        self._continue_labels.pop()

    def _gen_for(self, stmt: ForStmt):
        """Generate for loop."""
        top_label = self._label("for")
        update_label = self._label("forupd")
        end_label = self._label("endfor")

        self._break_labels.append(end_label)
        self._continue_labels.append(update_label)

        # Init
        if stmt.init:
            self._gen_statement(stmt.init)

        self._emit_label(top_label)

        # Condition
        if stmt.condition:
            cond_type = self._gen_expr(stmt.condition)
            self._emit_test_zero(cond_type)
            self._emit(f"BEQ     {end_label}")

        # Body
        self._gen_statement(stmt.body)

        # Update
        self._emit_label(update_label)
        if stmt.update:
            self._gen_expr(stmt.update)

        self._emit(f"BRA     {top_label}")
        self._emit_label(end_label)

        self._break_labels.pop()
        self._continue_labels.pop()

    def _gen_asm(self, stmt: AsmStmt):
        """Emit inline assembly verbatim."""
        for line in stmt.instructions.split("\\n"):
            stripped = line.strip()
            if stripped:
                self._emit(stripped)

    def _gen_break(self, stmt: BreakStmt):
        if not self._break_labels:
            raise CodeGenError("break outside of loop", stmt)
        self._emit(f"BRA     {self._break_labels[-1]}")

    def _gen_continue(self, stmt: ContinueStmt):
        if not self._continue_labels:
            raise CodeGenError("continue outside of loop", stmt)
        self._emit(f"BRA     {self._continue_labels[-1]}")

    # ── Expression generation ─────────────────
    # Convention: expression result is left in AccA (8-bit) or AccD (16-bit)

    def _gen_expr(self, expr: Expression) -> CType:
        """Generate code for an expression. Returns the result type."""

        if isinstance(expr, IntLiteral):
            return self._gen_int_literal(expr)
        elif isinstance(expr, CharLiteral):
            return self._gen_char_literal(expr)
        elif isinstance(expr, Identifier):
            return self._gen_identifier_load(expr)
        elif isinstance(expr, BinaryOp):
            return self._gen_binary_op(expr)
        elif isinstance(expr, UnaryOp):
            return self._gen_unary_op(expr)
        elif isinstance(expr, Assignment):
            return self._gen_assignment(expr)
        elif isinstance(expr, CompoundAssignment):
            return self._gen_compound_assignment(expr)
        elif isinstance(expr, FuncCall):
            return self._gen_func_call(expr)
        elif isinstance(expr, Deref):
            return self._gen_deref(expr)
        elif isinstance(expr, AddrOf):
            return self._gen_addr_of(expr)
        elif isinstance(expr, Cast):
            return self._gen_cast(expr)
        elif isinstance(expr, PreIncDec):
            return self._gen_pre_incdec(expr)
        elif isinstance(expr, PostIncDec):
            return self._gen_post_incdec(expr)
        elif isinstance(expr, ArraySubscript):
            return self._gen_array_subscript(expr)
        elif isinstance(expr, TernaryOp):
            return self._gen_ternary(expr)
        elif isinstance(expr, SizeofExpr):
            return self._gen_sizeof(expr)
        else:
            self._emit_comment(f"TODO: unhandled expr {type(expr).__name__}")
            return CType("int")

    def _gen_int_literal(self, lit: IntLiteral) -> CType:
        """Load an integer literal into AccA or AccD.

        Per C semantics, integer constants have type 'int' (16-bit on HC11).
        However, for efficiency on an 8-bit CPU, we use LDAA (8-bit) for
        small non-negative values (0-255) but still report the type as
        'char' only if the value fits in unsigned char range AND is clearly
        a byte-sized constant. For values > 255, we must use LDD (16-bit).

        The key insight: the *calling context* (_gen_binary_op, etc.) uses
        _promote_types to decide the operation width. So if a constant 100
        is added to an int, _promote_types will correctly pick 16-bit even
        though we loaded it with LDAA.
        """
        val = lit.value
        if val < 0:
            # Negative: must be int (signed)
            if -128 <= val <= 127:
                self._emit(f"LDAA    {self._imm8(val & 0xFF)}")
                return CType("char", is_unsigned=False)
            else:
                self._emit(f"LDD     {self._imm16(val & 0xFFFF)}")
                return CType("int", is_unsigned=False)
        elif val <= 255:
            self._emit(f"LDAA    {self._imm8(val)}")
            return CType("char", is_unsigned=True)
        else:
            self._emit(f"LDD     {self._imm16(val)}")
            return CType("int", is_unsigned=True)

    def _gen_char_literal(self, lit: CharLiteral) -> CType:
        self._emit(f"LDAA    {self._imm8(lit.value)}")
        return CType("char")

    def _gen_identifier_load(self, ident: Identifier) -> CType:
        """Load a variable's value into AccA or AccD."""
        sym = self._current_scope.lookup(ident.name)
        if sym is None:
            raise CodeGenError(f"Undefined variable: {ident.name}", ident)

        if sym.is_global:
            addr = sym.fixed_addr
            if addr is not None and addr <= 0xFF:
                # Direct page addressing (faster)
                if sym.ctype.size == 1:
                    self._emit(f"LDAA    {self._hex8(addr)}     ; {sym.name}")
                else:
                    self._emit(f"LDD     {self._hex8(addr)}     ; {sym.name}")
            elif addr is not None:
                # Extended addressing
                if sym.ctype.size == 1:
                    self._emit(f"LDAA    {self._hex16(addr)}   ; {sym.name}")
                else:
                    self._emit(f"LDD     {self._hex16(addr)}   ; {sym.name}")
            else:
                # Symbol name reference
                if sym.ctype.size == 1:
                    self._emit(f"LDAA    {sym.name}")
                else:
                    self._emit(f"LDD     {sym.name}")
        else:
            # Local variable: access via frame pointer
            self._emit("TSX")
            if sym.ctype.size == 1:
                self._emit(f"LDAA    {sym.stack_offset},X  ; {sym.name}")
            else:
                self._emit(f"LDD     {sym.stack_offset},X  ; {sym.name}")

        return sym.ctype

    def _gen_identifier_store(self, ident: Identifier, ctype: CType):
        """Store AccA or AccD to a variable location."""
        sym = self._current_scope.lookup(ident.name)
        if sym is None:
            raise CodeGenError(f"Undefined variable: {ident.name}", ident)

        if sym.is_global:
            addr = sym.fixed_addr
            if addr is not None and addr <= 0xFF:
                if sym.ctype.size == 1:
                    self._emit(f"STAA    {self._hex8(addr)}     ; {sym.name}")
                else:
                    self._emit(f"STD     {self._hex8(addr)}     ; {sym.name}")
            elif addr is not None:
                if sym.ctype.size == 1:
                    self._emit(f"STAA    {self._hex16(addr)}   ; {sym.name}")
                else:
                    self._emit(f"STD     {self._hex16(addr)}   ; {sym.name}")
            else:
                if sym.ctype.size == 1:
                    self._emit(f"STAA    {sym.name}")
                else:
                    self._emit(f"STD     {sym.name}")
        else:
            self._emit("TSX")
            if sym.ctype.size == 1:
                self._emit(f"STAA    {sym.stack_offset},X  ; {sym.name}")
            else:
                self._emit(f"STD     {sym.stack_offset},X  ; {sym.name}")

    def _gen_binary_op(self, op: BinaryOp) -> CType:
        """Generate code for a binary operation.

        Width-aware: uses 8-bit (AccA) or 16-bit (AccD) paths based on
        the promoted result type. For 8-bit, left is in A and right in B.
        For 16-bit, operands are saved/restored via the stack using
        PSHB+PSHA / PULA+PULB to preserve the full D register.

        HC11 instructions used:
          8-bit:  ABA, SBA, ANDA, ORAA, EORA, ASLA, LSRA/ASRA, CBA, MUL
          16-bit: ADDD, SUBD, ASLD, LSRD, CPD (via 0x1A prebyte)
        """

        # Short-circuit logical operators (always produce 8-bit boolean)
        if op.op == "&&":
            return self._gen_logical_and(op)
        if op.op == "||":
            return self._gen_logical_or(op)

        # Evaluate left side, push result
        left_type = self._gen_expr(op.left)

        # Determine result width early so we know how to save operands
        # (We need right_type too, but we can infer from left for save strategy)
        # We'll do the actual promote after evaluating both sides.
        is_left_word = left_type.is_word

        if is_left_word:
            self._emit("PSHB")          # save D (16-bit): push B first, then A
            self._emit("PSHA")          # stack: [A_high][B_low]...
        else:
            self._emit("PSHA")          # save A (8-bit)

        # Evaluate right side (result in A or D)
        right_type = self._gen_expr(op.right)
        result_type = self._promote_types(left_type, right_type)

        # ── Comparisons: delegate to _gen_comparison (handles both widths)
        if op.op in ("==", "!=", "<", ">", "<=", ">="):
            return self._gen_comparison_binop(op.op, left_type, right_type,
                                              result_type, is_left_word)

        # ── 16-bit arithmetic path ──
        if result_type.is_word:
            # Right operand is in A (8-bit) or D (16-bit)
            # We need right in a temp location, then restore left into D
            if right_type.is_byte:
                # Widen right from A to D: D = 00:A
                self._emit("TAB")      # B = A (value)
                self._emit("CLRA")     # A = 0, D = 0x00:val
            # Now right is in D. Save it to scratch (2 bytes) or stack.
            self._emit(f"STD     {self._hex8(self._scratch_addr - 1)}  ; scratch16 (right)")
            # Restore left into D
            if is_left_word:
                self._emit("PULA")     # A = high byte
                self._emit("PULB")     # B = low byte → D = left
            else:
                # Left was 8-bit, widen it
                self._emit("PULA")     # A = left (8-bit)
                self._emit("TAB")      # B = A
                self._emit("CLRA")     # D = 00:left
            # Now D = left (16-bit), scratch16 = right (16-bit)
            scratch16 = self._hex8(self._scratch_addr - 1)

            if op.op == "+":
                self._emit(f"ADDD    {scratch16}  ; D = D + right")
            elif op.op == "-":
                self._emit(f"SUBD    {scratch16}  ; D = D - right")
            elif op.op == "&":
                # No 16-bit AND instruction — do byte-by-byte
                self._emit(f"ANDA    {scratch16}")
                self._emit(f"ANDB    {self._hex8(self._scratch_addr)}")
            elif op.op == "|":
                self._emit(f"ORAA    {scratch16}")
                self._emit(f"ORAB    {self._hex8(self._scratch_addr)}")
            elif op.op == "^":
                self._emit(f"EORA    {scratch16}")
                self._emit(f"EORB    {self._hex8(self._scratch_addr)}")
            elif op.op == "<<":
                # Shift D left by N positions (N in scratch low byte)
                self._emit(f"LDAA    {self._hex8(self._scratch_addr)}  ; shift count")
                self._emit("PSHA")     # save count
                # Restore D = left (already there from above, but we just
                # clobbered A with the shift count; need to reload left)
                # Actually D still has left from the ADDD path setup.
                # We need a different approach: save D, get count, loop.
                # Let's redo: D=left is in D. Count is in scratch.
                self._emit("PULA")     # discard the count push (we'll use B)
                self._emit(f"PSHB")    # save D low
                self._emit(f"PSHA")    # save D high
                self._emit(f"LDAB    {self._hex8(self._scratch_addr)}  ; B = shift count")
                self._emit("PULA")     # restore D
                self._emit("PULB")
                # Wait — we overwrote B with count. Let me restructure.
                # Simplest: shift count on stack, D has the value.
                # Pop and restart:
                # Actually, let's just use a clean approach with D=left and
                # shift count in a scratch byte.
                # D was already loaded with left. scratch_addr has right low byte = count.
                lbl_top = self._label("shl16")
                lbl_end = self._label("shl16e")
                # We need to reload D with left since we've been clobbering it.
                # The cleanest way: reload from scratch16 the right (count), then
                # re-derive D.
                # Actually, let's back up. For shifts, count is always small (0-15).
                # The real pattern: D has the value to shift, count is an 8-bit in scratch.
                # Since we already set up D = left above, and then stored right to scratch,
                # D still = left at this point (we haven't done ADDD etc for shift).
                # Hmm, we did STD scratch which didn't change D. Then PULA/PULB restored left.
                # So D = left. And scratch has right. The low byte of right is the count.
                # B is low byte of D (part of the value). We need count somewhere else.
                # Use X as counter via a loop.
                self._emit(f"PSHB")    # save D low byte
                self._emit(f"LDAB    {self._hex8(self._scratch_addr)}  ; B = shift count")
                self._emit("PSHA")     # save D high byte
                # Now stack has [D_high][D_low], B = count
                # We need D back for ASLD. Use scratch to hold count.
                self._emit(f"STAB    {self._hex8(self._scratch_addr)}")  # count in scratch
                self._emit("PULA")     # A = D high
                self._emit("PULB")     # B = D low → D restored
                self._emit_label(lbl_top)
                self._emit(f"TST     {self._hex8(self._scratch_addr)}")
                self._emit(f"BEQ     {lbl_end}")
                self._emit("ASLD")     # shift D left by 1
                self._emit(f"DEC     {self._hex8(self._scratch_addr)}")
                self._emit(f"BRA     {lbl_top}")
                self._emit_label(lbl_end)

            elif op.op == ">>":
                lbl_top = self._label("shr16")
                lbl_end = self._label("shr16e")
                # Same pattern as <<: D=left, count in scratch low byte
                self._emit(f"PSHB")
                self._emit(f"LDAB    {self._hex8(self._scratch_addr)}")
                self._emit("PSHA")
                self._emit(f"STAB    {self._hex8(self._scratch_addr)}")
                self._emit("PULA")
                self._emit("PULB")     # D restored, count in scratch
                self._emit_label(lbl_top)
                self._emit(f"TST     {self._hex8(self._scratch_addr)}")
                self._emit(f"BEQ     {lbl_end}")
                if result_type.is_unsigned:
                    self._emit("LSRD")
                else:
                    self._emit("ASRA")     # arithmetic shift A (high byte)
                    self._emit("RORB")     # rotate carry into B (low byte)
                self._emit(f"DEC     {self._hex8(self._scratch_addr)}")
                self._emit(f"BRA     {lbl_top}")
                self._emit_label(lbl_end)

            elif op.op == "*":
                # MUL: A * B -> D (unsigned 8x8->16). For 16-bit multiply
                # we'd need a runtime helper. For now, truncate to 8-bit operands.
                self._emit("TBA")      # A = low byte of D (left low)
                self._emit(f"LDAB    {self._hex8(self._scratch_addr)}  ; right low byte")
                self._emit("MUL")      # D = A * B
                return CType("int", is_unsigned=True)

            elif op.op == "/":
                # IDIV: D / X -> X quotient, D remainder (unsigned 16/16)
                self._emit(f"LDX     {self._hex8(self._scratch_addr - 1)}  ; X = divisor")
                self._emit("IDIV")     # X = D / X, D = D % X
                self._emit("XGDX")    # D = quotient
                return result_type

            elif op.op == "%":
                # IDIV: D / X -> X quotient, D remainder
                self._emit(f"LDX     {self._hex8(self._scratch_addr - 1)}  ; X = divisor")
                self._emit("IDIV")     # X = D / X, D = D % X
                # D already has remainder
                return result_type

            else:
                self._emit_comment(f"TODO: 16-bit binary op {op.op}")

            return result_type

        # ── 8-bit arithmetic path ──
        # Right is in A. Pop left into B, then swap so A=left, B=right.
        self._emit("TAB")              # B = right (move A to B)
        self._emit("PULA")             # A = left (pop from stack)
        # Now: A = left, B = right

        if op.op == "+":
            self._emit("ABA")          # A = A + B
        elif op.op == "-":
            self._emit("SBA")          # A = A - B
        elif op.op == "&":
            self._emit(f"STAB    {self._hex8(self._scratch_addr)}     ; scratch")
            self._emit(f"ANDA    {self._hex8(self._scratch_addr)}")
        elif op.op == "|":
            self._emit(f"STAB    {self._hex8(self._scratch_addr)}     ; scratch")
            self._emit(f"ORAA    {self._hex8(self._scratch_addr)}")
        elif op.op == "^":
            self._emit(f"STAB    {self._hex8(self._scratch_addr)}     ; scratch")
            self._emit(f"EORA    {self._hex8(self._scratch_addr)}")
        elif op.op == "<<":
            lbl_top = self._label("shl")
            lbl_end = self._label("shle")
            self._emit_label(lbl_top)
            self._emit("TSTB")
            self._emit(f"BEQ     {lbl_end}")
            self._emit("ASLA")
            self._emit("DECB")
            self._emit(f"BRA     {lbl_top}")
            self._emit_label(lbl_end)
        elif op.op == ">>":
            lbl_top = self._label("shr")
            lbl_end = self._label("shre")
            self._emit_label(lbl_top)
            self._emit("TSTB")
            self._emit(f"BEQ     {lbl_end}")
            if result_type.is_unsigned:
                self._emit("LSRA")
            else:
                self._emit("ASRA")
            self._emit("DECB")
            self._emit(f"BRA     {lbl_top}")
            self._emit_label(lbl_end)
        elif op.op == "*":
            # MUL: A * B -> D (unsigned 8x8->16)
            self._emit("MUL")          # D = A * B
            self._emit("TBA")          # A = low byte of result
            return CType("int", is_unsigned=True)
        elif op.op == "/":
            # 8-bit unsigned division via IDIV
            # State: A = left (dividend), B = right (divisor)
            # IDIV needs: D = dividend (16-bit), X = divisor (16-bit)
            # Result: X = quotient, D = remainder
            self._emit(f"STAB    {self._hex8(self._scratch_addr)}  ; save divisor")
            self._emit("TAB")          # B = dividend
            self._emit("CLRA")         # D = 00:dividend (zero-extended)
            self._emit("PSHB")         # save D
            self._emit("PSHA")
            self._emit(f"LDAB    {self._hex8(self._scratch_addr)}  ; B = divisor")
            self._emit("CLRA")         # D = 00:divisor
            self._emit("XGDX")         # X = 00:divisor, D = garbage
            self._emit("PULA")         # restore D = 00:dividend
            self._emit("PULB")
            self._emit("IDIV")         # X = D / X, D = D % X
            self._emit("XGDX")         # D = quotient
            self._emit("TBA")          # A = low byte of quotient
        elif op.op == "%":
            # 8-bit unsigned modulo via IDIV
            # Same setup as division, but keep remainder (in D after IDIV)
            self._emit(f"STAB    {self._hex8(self._scratch_addr)}  ; save divisor")
            self._emit("TAB")          # B = dividend
            self._emit("CLRA")         # D = 00:dividend
            self._emit("PSHB")
            self._emit("PSHA")
            self._emit(f"LDAB    {self._hex8(self._scratch_addr)}  ; B = divisor")
            self._emit("CLRA")         # D = 00:divisor
            self._emit("XGDX")         # X = divisor
            self._emit("PULA")
            self._emit("PULB")         # D = 00:dividend
            self._emit("IDIV")         # X = quotient, D = remainder
            self._emit("TBA")          # A = low byte of remainder
        else:
            self._emit_comment(f"TODO: binary op {op.op}")

        return result_type

    def _gen_comparison_binop(self, op: str, left_type: CType, right_type: CType,
                              result_type: CType, is_left_word: bool) -> CType:
        """Generate comparison from binary op context.

        Called from _gen_binary_op. Operands are on the stack (left) and
        in A or D (right). Produces A=1 (true) or A=0 (false).

        For 16-bit: uses SUBD to compare D (left) - scratch16 (right).
        For 8-bit: uses CBA (A=left, B=right).
        """
        promoted = self._promote_types(left_type, right_type)

        if promoted.is_word:
            # 16-bit comparison path
            # Right operand is in A (byte) or D (word). Widen if needed.
            if right_type.is_byte:
                self._emit("TAB")
                self._emit("CLRA")     # D = 00:right
            # Save right to scratch16
            scratch16 = self._hex8(self._scratch_addr - 1)
            self._emit(f"STD     {scratch16}  ; scratch16 (right)")
            # Restore left into D
            if is_left_word:
                self._emit("PULA")
                self._emit("PULB")     # D = left (16-bit)
            else:
                self._emit("PULA")     # A = left (8-bit)
                self._emit("TAB")
                self._emit("CLRA")     # D = 00:left
            # Compare: SUBD sets N, Z, V, C flags (same as CPD)
            self._emit(f"SUBD    {scratch16}  ; compare D - right")
        else:
            # 8-bit comparison path
            self._emit("TAB")          # B = right
            self._emit("PULA")         # A = left
            self._emit("CBA")          # compare A - B

        true_label = self._label("true")
        end_label = self._label("cend")

        branch_map = {
            "==": "BEQ",
            "!=": "BNE",
            "<":  "BLO" if promoted.is_unsigned else "BLT",
            ">":  "BHI" if promoted.is_unsigned else "BGT",
            "<=": "BLS" if promoted.is_unsigned else "BLE",
            ">=": "BHS" if promoted.is_unsigned else "BGE",
        }

        branch = branch_map.get(op, "BEQ")
        self._emit(f"{branch}    {true_label}")
        self._emit("CLRA")            # false = 0
        self._emit(f"BRA     {end_label}")
        self._emit_label(true_label)
        self._emit("LDAA    #$01")    # true = 1
        self._emit_label(end_label)

        return CType("char", is_unsigned=True)

    def _gen_comparison(self, op: str, result_type: CType) -> CType:
        """Generate comparison: A=left, B=right already loaded. Result: A=1 or A=0."""
        # CBA compares A - B and sets flags
        self._emit("CBA")

        true_label = self._label("true")
        end_label = self._label("cend")

        branch_map = {
            "==": "BEQ",
            "!=": "BNE",
            "<":  "BLO" if result_type.is_unsigned else "BLT",
            ">":  "BHI" if result_type.is_unsigned else "BGT",
            "<=": "BLS" if result_type.is_unsigned else "BLE",
            ">=": "BHS" if result_type.is_unsigned else "BGE",
        }

        branch = branch_map.get(op, "BEQ")
        self._emit(f"{branch}    {true_label}")
        self._emit(f"CLRA")            # false = 0
        self._emit(f"BRA     {end_label}")
        self._emit_label(true_label)
        self._emit(f"LDAA    #$01")    # true = 1
        self._emit_label(end_label)

        return CType("char", is_unsigned=True)

    def _gen_logical_and(self, op: BinaryOp) -> CType:
        """Short-circuit &&."""
        false_label = self._label("andf")
        end_label = self._label("ande")

        lt = self._gen_expr(op.left)
        self._emit_test_zero(lt)
        self._emit(f"BEQ     {false_label}")

        rt = self._gen_expr(op.right)
        self._emit_test_zero(rt)
        self._emit(f"BEQ     {false_label}")

        self._emit("LDAA    #$01")
        self._emit(f"BRA     {end_label}")
        self._emit_label(false_label)
        self._emit("CLRA")
        self._emit_label(end_label)

        return CType("char", is_unsigned=True)

    def _gen_logical_or(self, op: BinaryOp) -> CType:
        """Short-circuit ||."""
        true_label = self._label("ort")
        end_label = self._label("ore")

        lt = self._gen_expr(op.left)
        self._emit_test_zero(lt)
        self._emit(f"BNE     {true_label}")

        rt = self._gen_expr(op.right)
        self._emit_test_zero(rt)
        self._emit(f"BNE     {true_label}")

        self._emit("CLRA")
        self._emit(f"BRA     {end_label}")
        self._emit_label(true_label)
        self._emit("LDAA    #$01")
        self._emit_label(end_label)

        return CType("char", is_unsigned=True)

    def _gen_unary_op(self, op: UnaryOp) -> CType:
        """Generate unary operator (width-aware)."""
        result_type = self._gen_expr(op.operand)

        if op.op == "-":
            if result_type.is_word:
                # Negate D: D = 0 - D (COMA; COMB; ADDD #1 is two's complement)
                self._emit("COMA")
                self._emit("COMB")
                self._emit("ADDD    #$0001  ; negate D")
            else:
                self._emit("NEGA")     # A = -A
        elif op.op == "~":
            if result_type.is_word:
                self._emit("COMA")
                self._emit("COMB")     # ~D
            else:
                self._emit("COMA")     # ~A
        elif op.op == "!":
            # Logical NOT: result = (value == 0) ? 1 : 0
            lbl_zero = self._label("not0")
            lbl_end = self._label("note")
            self._emit_test_zero(result_type)
            self._emit(f"BEQ     {lbl_zero}")
            self._emit("CLRA")
            self._emit(f"BRA     {lbl_end}")
            self._emit_label(lbl_zero)
            self._emit("LDAA    #$01")
            self._emit_label(lbl_end)
            return CType("char", is_unsigned=True)
        else:
            self._emit_comment(f"TODO: unary op {op.op}")

        return result_type

    def _gen_assignment(self, asgn: Assignment) -> CType:
        """Generate simple assignment."""
        # Evaluate RHS
        rtype = self._gen_expr(asgn.value)

        # Store to LHS
        if isinstance(asgn.target, Identifier):
            self._gen_identifier_store(asgn.target, rtype)
        elif isinstance(asgn.target, Deref):
            # *ptr = value  ->  store through pointer
            # Check for constant address (volatile I/O): *(type*)0x1030 = val
            const_addr = self._try_get_const_ptr_addr(asgn.target.expr)
            if const_addr is not None:
                addr, pointed = const_addr
                addr_str = self._hex16(addr) if addr > 0xFF else self._hex8(addr)
                if pointed.size == 1:
                    self._emit(f"STAA    {addr_str}  ; *({self._hex16(addr)}) = A direct")
                else:
                    self._emit(f"STD     {addr_str}  ; *({self._hex16(addr)}) = D direct")
            else:
                # General path: evaluate pointer, store through X
                val_size = rtype.size
                if val_size == 1:
                    self._emit("PSHA")         # save 8-bit value
                else:
                    self._emit("PSHB")         # save 16-bit value (D = A:B)
                    self._emit("PSHA")
                ptr_type = self._gen_expr(asgn.target.expr)  # pointer addr -> D (16-bit)
                self._emit("XGDX")         # X = pointer address
                if val_size == 1:
                    self._emit("PULA")         # A = value to store
                    self._emit("STAA    0,X")  # *ptr = A (byte)
                else:
                    self._emit("PULA")         # restore D (A first, then B)
                    self._emit("PULB")
                    self._emit("STD     0,X")  # *ptr = D (word)
        elif isinstance(asgn.target, ArraySubscript):
            # array[index] = value
            val_size = rtype.size
            if val_size == 1:
                self._emit("PSHA")         # save value (8-bit)
            else:
                self._emit("PSHB")
                self._emit("PSHA")         # save value (16-bit D)
            # Calculate address: base pointer + index
            self._gen_expr(asgn.target.array)  # base addr -> D
            self._emit("PSHB")
            self._emit("PSHA")            # save base addr
            self._gen_expr(asgn.target.index)  # index -> A
            self._emit("TAB")             # B = index
            self._emit("PULA")            # restore base addr into D
            self._emit("PULB")            # (PULA gets A=high, but we need to
            #                               add index to low byte — use ABX)
            self._emit("XGDX")            # X = base address
            self._emit("ABX")             # X = X + B (base + index)
            if val_size == 1:
                self._emit("PULA")         # A = value
                self._emit("STAA    0,X")
            else:
                self._emit("PULA")
                self._emit("PULB")
                self._emit("STD     0,X")
        else:
            self._emit_comment(f"TODO: assignment to {type(asgn.target).__name__}")

        return rtype

    def _gen_compound_assignment(self, asgn: CompoundAssignment) -> CType:
        """Generate compound assignment (+=, -=, |=, &=, etc.)."""
        # Load current value
        if isinstance(asgn.target, Identifier):
            ltype = self._gen_identifier_load(asgn.target)
            self._emit("PSHA")         # save current value

            # Evaluate RHS
            self._gen_expr(asgn.value)
            self._emit("TAB")          # B = rhs
            self._emit("PULA")         # A = current value

            # Apply operation
            base_op = asgn.op.rstrip("=")
            if base_op == "+":
                self._emit("ABA")
            elif base_op == "-":
                self._emit("SBA")
            elif base_op == "&":
                self._emit(f"STAB    {self._hex8(self._scratch_addr)}")
                self._emit(f"ANDA    {self._hex8(self._scratch_addr)}")
            elif base_op == "|":
                self._emit(f"STAB    {self._hex8(self._scratch_addr)}")
                self._emit(f"ORAA    {self._hex8(self._scratch_addr)}")
            elif base_op == "^":
                self._emit(f"STAB    {self._hex8(self._scratch_addr)}")
                self._emit(f"EORA    {self._hex8(self._scratch_addr)}")
            elif base_op == "<<":
                lbl = self._label("cshl")
                lbl_e = self._label("cshle")
                self._emit_label(lbl)
                self._emit("TSTB")
                self._emit(f"BEQ     {lbl_e}")
                self._emit("ASLA")
                self._emit("DECB")
                self._emit(f"BRA     {lbl}")
                self._emit_label(lbl_e)
            elif base_op == ">>":
                lbl = self._label("cshr")
                lbl_e = self._label("cshre")
                self._emit_label(lbl)
                self._emit("TSTB")
                self._emit(f"BEQ     {lbl_e}")
                self._emit("LSRA")
                self._emit("DECB")
                self._emit(f"BRA     {lbl}")
                self._emit_label(lbl_e)
            else:
                self._emit_comment(f"TODO: compound op {asgn.op}")

            # Store result back
            self._gen_identifier_store(asgn.target, ltype)
            return ltype
        else:
            self._emit_comment(f"TODO: compound assign to {type(asgn.target).__name__}")
            return CType("int")

    def _gen_func_call(self, call: FuncCall) -> CType:
        """Generate function call."""
        # Push arguments right-to-left
        total_arg_size = 0
        for arg in reversed(call.args):
            arg_type = self._gen_expr(arg)
            if arg_type.size == 1:
                self._emit("PSHA")
                total_arg_size += 1
            else:
                self._emit("PSHB")
                self._emit("PSHA")
                total_arg_size += 2

        self._emit(f"JSR     {call.name}")

        # Cleanup arguments from stack
        if total_arg_size > 0:
            for _ in range(total_arg_size):
                self._emit("INS")
            self._emit_comment(f"clean {total_arg_size} bytes args")

        # Return value is in A (8-bit) or D (16-bit)
        sym = self._global_scope.lookup(call.name)
        if sym:
            return sym.ctype
        return CType("int")

    def _try_get_const_ptr_addr(self, expr) -> Optional[Tuple[int, CType]]:
        """Check if an expression is a constant pointer (cast of int literal).

        Returns (address, pointed_to_type) if the expression is:
          (type *)0x1030  — a Cast of an IntLiteral to a pointer type.
        Returns None otherwise.

        This enables direct extended-mode addressing for memory-mapped I/O:
          *(volatile unsigned char *)0x1030  →  LDAA $1030
        instead of:
          LDD #$1030; XGDX; LDAA 0,X
        """
        if isinstance(expr, Cast) and expr.cast_type.is_pointer:
            if isinstance(expr.expr, IntLiteral):
                return (expr.expr.value, expr.cast_type.pointed_to())
        return None

    def _gen_deref(self, deref: Deref) -> CType:
        """Generate pointer dereference: *ptr.

        Optimized path for constant addresses (memory-mapped I/O):
          *(volatile unsigned char *)0x1030  →  LDAA $1030  (direct)

        General path: load pointer into D, XGDX, indexed load.
        """
        # Check for constant pointer address (volatile I/O optimization)
        const_addr = self._try_get_const_ptr_addr(deref.expr)
        if const_addr is not None:
            addr, pointed = const_addr
            addr_str = self._hex16(addr) if addr > 0xFF else self._hex8(addr)
            if pointed.size == 1:
                self._emit(f"LDAA    {addr_str}  ; *({self._hex16(addr)}) direct")
            else:
                self._emit(f"LDD     {addr_str}  ; *({self._hex16(addr)}) direct")
            return pointed

        # General path: evaluate pointer expression
        ptr_type = self._gen_expr(deref.expr)

        # Pointer value should be in D (16-bit address)
        # Move to X for indexed load
        self._emit("XGDX")            # X = D (pointer value)
        if ptr_type.is_pointer:
            pointed = ptr_type.pointed_to()
            if pointed.size == 1:
                self._emit("LDAA    0,X     ; *ptr (byte)")
            else:
                self._emit("LDD     0,X     ; *ptr (word)")
            return pointed
        else:
            # Assume byte dereference
            self._emit("LDAA    0,X     ; *ptr")
            return CType("char", is_unsigned=True)

    def _gen_addr_of(self, addr: AddrOf) -> CType:
        """Generate address-of: &var."""
        if isinstance(addr.expr, Identifier):
            sym = self._current_scope.lookup(addr.expr.name)
            if sym is None:
                raise CodeGenError(f"Undefined variable: {addr.expr.name}", addr)
            if sym.is_global and sym.fixed_addr is not None:
                self._emit(f"LDD     {self._imm16(sym.fixed_addr)}  ; &{sym.name}")
            else:
                # Local: compute address from stack frame
                self._emit("TSX")
                self._emit(f"XGDX")   # D = frame pointer
                if sym.stack_offset > 0:
                    self._emit(f"ADDD    {self._imm16(sym.stack_offset)}")
            return sym.ctype.pointer_to()
        else:
            self._emit_comment("TODO: address-of complex expr")
            return CType("void", pointer_depth=1)

    def _gen_cast(self, cast: Cast) -> CType:
        """Generate type cast."""
        src_type = self._gen_expr(cast.expr)

        # 8-bit to 16-bit widening
        if src_type.is_byte and cast.cast_type.is_word:
            if src_type.is_unsigned:
                self._emit("CLRB")     # D = 00:A (zero extend)
                # But D is A:B, so A is high byte, B is low byte
                # Actually: to widen A to D, we need A in B and clear A
                self._emit("TAB")      # B = A
                self._emit("CLRA")     # A = 0, so D = 00:original_A
            else:
                # Sign extend: if bit 7 of A is set, fill B with FF
                self._emit("TAB")
                self._emit("CLRA")
                self._emit("TSTB")
                lbl = self._label("sext")
                self._emit(f"BPL     {lbl}")
                self._emit("LDAA    #$FF")  # sign extend
                self._emit_label(lbl)

        # 16-bit to 8-bit narrowing
        elif src_type.is_word and cast.cast_type.is_byte:
            self._emit("TBA")          # A = B (low byte of D)

        return cast.cast_type

    def _gen_pre_incdec(self, op: PreIncDec) -> CType:
        """Generate ++x or --x (width-aware)."""
        if isinstance(op.operand, Identifier):
            ctype = self._gen_identifier_load(op.operand)
            if ctype.is_word:
                if op.op == "++":
                    self._emit("ADDD    #$0001")
                else:
                    self._emit("SUBD    #$0001")
            else:
                if op.op == "++":
                    self._emit("INCA")
                else:
                    self._emit("DECA")
            self._gen_identifier_store(op.operand, ctype)
            return ctype
        self._emit_comment(f"TODO: pre-{op.op} on complex expr")
        return CType("int")

    def _gen_post_incdec(self, op: PostIncDec) -> CType:
        """Generate x++ or x-- (width-aware)."""
        if isinstance(op.operand, Identifier):
            ctype = self._gen_identifier_load(op.operand)
            if ctype.is_word:
                self._emit("PSHB")     # save D (original)
                self._emit("PSHA")
                if op.op == "++":
                    self._emit("ADDD    #$0001")
                else:
                    self._emit("SUBD    #$0001")
                self._gen_identifier_store(op.operand, ctype)
                self._emit("PULA")     # restore original D
                self._emit("PULB")
            else:
                self._emit("PSHA")     # save original
                if op.op == "++":
                    self._emit("INCA")
                else:
                    self._emit("DECA")
                self._gen_identifier_store(op.operand, ctype)
                self._emit("PULA")     # return original
            return ctype
        self._emit_comment(f"TODO: post-{op.op} on complex expr")
        return CType("int")

    def _gen_array_subscript(self, sub: ArraySubscript) -> CType:
        """Generate array[index] read."""
        # Load base address
        self._gen_expr(sub.array)
        self._emit("PSHA")
        # Load index
        self._gen_expr(sub.index)
        self._emit("TAB")             # B = index
        self._emit("PULA")            # A = base
        self._emit("ABA")             # A = base + index
        self._emit("TAB")
        self._emit("CLRA")
        self._emit("XGDX")            # X = address
        self._emit("LDAA    0,X")     # load byte at address
        return CType("char", is_unsigned=True)

    def _gen_ternary(self, op: TernaryOp) -> CType:
        """Generate ternary: cond ? a : b."""
        else_label = self._label("tern_e")
        end_label = self._label("tern_d")

        cond_type = self._gen_expr(op.condition)
        self._emit_test_zero(cond_type)
        self._emit(f"BEQ     {else_label}")

        self._gen_expr(op.then_expr)
        self._emit(f"BRA     {end_label}")

        self._emit_label(else_label)
        self._gen_expr(op.else_expr)

        self._emit_label(end_label)
        return CType("int")

    def _gen_sizeof(self, expr: SizeofExpr) -> CType:
        """Generate sizeof — resolved at compile time."""
        if expr.target_type:
            size = expr.target_type.size
        else:
            size = 2  # default assumption
        self._emit(f"LDAA    {self._imm8(size)}  ; sizeof")
        return CType("int", is_unsigned=True)

    # ── String data generation ────────────────

    def _gen_string_data(self):
        """Emit string literal data at end of code section."""
        if self._string_literals:
            self._emit_blank()
            self._emit_comment("String data")
            for label, data in self._string_literals.items():
                self._emit_label(label)
                bytes_str = ",".join(f"${ord(c):02X}" for c in data)
                self._emit(f"FCB     {bytes_str},$00")

    # ── Vector table generation ───────────────

    def _gen_vector_table(self):
        """Generate interrupt vector table entries."""
        if self._isr_vectors:
            vec_addr = self.profile.get("vectors", 0xFFD6)
            self._vector_lines.append(f"        ORG     {self._hex16(vec_addr)}")
            for vec_name, func_label in self._isr_vectors.items():
                self._vector_lines.append(f"        FDB     {func_label}    ; {vec_name}")

    # ── Type promotion ────────────────────────

    @staticmethod
    def _promote_types(a: CType, b: CType) -> CType:
        """Determine result type of binary operation between two types."""
        # If either is 16-bit, result is 16-bit
        if a.size == 2 or b.size == 2:
            return CType("int", is_unsigned=(a.is_unsigned or b.is_unsigned))
        # Both 8-bit
        return CType("char", is_unsigned=(a.is_unsigned and b.is_unsigned))
