"""
68HC11 Code Generator for the KingAI C Compiler.

Translates the AST into Motorola 68HC11 assembly language.

Register usage convention:
  - AccA / AccB (8-bit): primary working registers
  - AccD (A:B combined, 16-bit): 16-bit arithmetic
  - X: transient address/index register for pointers, arrays and member lvalues
  - Y: stable function frame pointer (callee-saved for normal C functions)
  - SP: stack pointer (grows downward)

Function calling convention:
  - Arguments pushed right-to-left on stack
  - Return value in AccA (8-bit) or AccD (16-bit)
  - Caller cleans up arguments after call
  - Callee preserves Y; X is caller-clobbered scratch
  - ISRs save all registers automatically (RTI restores them)

Memory layout:
  - $0000-$00FF: Zero page / direct page RAM (fast access)
  - $0100-$03FF: Extended RAM (HC11F1 has 1KB total)
  - $1000-$105F: I/O registers
  - $2000-$7FFF: Always visible (calibration/shared code)
  - $8000-$FFFF: Bank-switched program ROM
  - $FFD6-$FFFF: Interrupt vector table

Porting to another CPU:
  To retarget this code generator for a different processor (e.g. AVR, ARM,
  6502, or x86), you need to change:
    1. TARGET_PROFILES — replace memory maps and register names
    2. _emit_* helpers — change mnemonics (LDAA→LDA, STAA→STA, etc.)
    3. _gen_function — change prologue/epilogue (TSX→frame pointer setup)
    4. _gen_binary_op — map operations to your ALU instructions
    5. _gen_call — change calling convention (stack vs registers)
    6. _gen_pointer_deref — change addressing modes (indexed → indirect, etc.)
  The AST walking logic (if/while/for/return) is target-independent.
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
    stack_offset: int = 0         # offset from stable Y frame pointer
    fixed_addr: Optional[int] = None
    is_param: bool = False
    is_extern: bool = False
    asm_name: Optional[str] = None

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
                 target: str = "generic", relocatable: bool = False,
                 module_name: Optional[str] = None):
        self.org = org
        self.stack = stack
        self.target = target
        self.profile = TARGET_PROFILES.get(target, TARGET_PROFILES["generic"])
        self.relocatable = relocatable
        raw_module = module_name or "module"
        self.module_name = "".join(c if (c.isalnum() or c == "_") else "_" for c in raw_module)

        # Output sections (accumulated during code generation, joined at the end)
        self._header_lines: List[str] = []    # Assembly file header / ORG directive
        self._data_lines: List[str] = []      # Global variable EQU directives
        self._bss_lines: List[str] = []       # Uninitialized data section
        self._code_lines: List[str] = []      # Generated instructions
        self._vector_lines: List[str] = []    # Interrupt vector table FDB entries

        # Symbol / state tracking
        self._global_scope = Scope()              # Top-level symbol scope
        self._current_scope: Scope = self._global_scope
        self._label_counter = 0                   # Monotonic counter for unique labels
        self._local_offset = 0                    # Current function's stack frame size in bytes
        self._in_function: Optional[FuncDecl] = None  # Currently-generating function
        self._zp_alloc = 0x0040                   # Next free zero-page address for globals
        self._ram_alloc = 0x0100                  # Next free extended RAM address for globals
        self._scratch_addr = 0x003F               # Reserved direct-page scratch byte (never allocated)
        self._scratch_index_addr = 0x003D         # Reserved array-index scratch byte
        self._string_literals: Dict[str, str] = {}    # label -> string data for FCC emission
        self._structs: Dict[str, StructDecl] = {}
        self.resource_requests: List[dict] = []
        self._isr_vectors: Dict[str, str] = {}        # vector name -> function label for vector table
        self._break_labels: List[str] = []            # Stack of break-target labels (loops)
        self._continue_labels: List[str] = []         # Stack of continue-target labels (loops)

    # ── Label generation ──────────────────────

    def _label(self, prefix: str = "L") -> str:
        self._label_counter += 1
        if self.relocatable:
            return f".{self.module_name}_{prefix}{self._label_counter}"
        return f".{prefix}{self._label_counter}"

    @staticmethod
    def _asm_symbol(sym: Symbol) -> str:
        return sym.asm_name or sym.name

    def _qualified_name(self, name: str) -> str:
        return f"__{self.module_name}_{name}"

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

        # First pass: collect aggregate types, then symbols.
        for decl in program.declarations:
            if isinstance(decl, StructDecl) and decl.size > 0:
                self._structs[decl.name] = decl

        for decl in program.declarations:
            if isinstance(decl, VarDecl):
                self._gen_global_var(decl)
            elif isinstance(decl, FuncDecl):
                self._register_function(decl)

        # Second pass: generate code only for function definitions.
        for decl in program.declarations:
            if isinstance(decl, FuncDecl) and decl.body is not None:
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
            f"; ============================================",
            f"; KingAI 68HC11 C Compiler Output",
            f"; Target: {desc}",
            f"; ============================================",
            f"",
            f"; -- Memory Configuration --",
        ]
        if not self.relocatable:
            self._header_lines.append(f"        ORG     {self._hex16(self.org)}")
        else:
            self._header_lines.append(f"; relocatable module: {self.module_name}")
        self._header_lines.append(
            f""
        ]

    def _assemble_output(self) -> str:
        sections = []
        sections.extend(self._header_lines)

        if self._data_lines:
            sections.append("; -- Initialized Data --")
            sections.extend(self._data_lines)
            sections.append("")

        if self._bss_lines:
            sections.append("; -- Uninitialized Data (BSS) --")
            sections.extend(self._bss_lines)
            sections.append("")

        sections.append("; -- Code --")
        sections.extend(self._code_lines)

        if self._vector_lines:
            sections.append("")
            sections.append("; -- Interrupt Vectors --")
            sections.extend(self._vector_lines)

        sections.append("")
        sections.append("; -- End --")
        return "\n".join(sections)

    # ── Global variable generation ────────────

    def _gen_global_var(self, decl: VarDecl):
        if decl.ctype.size <= 0 and not decl.ctype.is_extern:
            raise CodeGenError(f"Variable has incomplete/zero-sized type: {decl.name}", decl)
        if decl.init and (decl.ctype.is_array or decl.ctype.base == "struct"):
            raise CodeGenError("Aggregate initializers are not supported yet", decl)

        asm_name = (self._qualified_name(decl.name)
                    if self.relocatable and decl.ctype.is_static else decl.name)
        sym = Symbol(
            name=decl.name,
            ctype=decl.ctype,
            is_global=True,
            is_zeropage=decl.is_zeropage,
            fixed_addr=decl.fixed_addr,
            is_extern=decl.ctype.is_extern,
            asm_name=asm_name,
        )

        # extern declarations consume no local resource and resolve at link time.
        if decl.ctype.is_extern:
            self._global_scope.define(sym)
            return

        if self.relocatable:
            kind = "zp" if decl.is_zeropage else "ram"
            placeholder = f"__{kind.upper()}_{self.module_name}_{decl.name}"
            sym.fixed_addr = None
            self.resource_requests.append({
                "name": placeholder,
                "symbol": asm_name,
                "kind": kind,
                "size": decl.ctype.size,
                "alignment": 1,
                "module": self.module_name,
            })
            self._global_scope.define(sym)
            init_comment = ""
            if decl.init and isinstance(decl.init, IntLiteral):
                init_comment = f" init={decl.init.value}"
            self._data_lines.append(
                f"{asm_name}:   EQU     {placeholder}    ; {decl.ctype}{init_comment}"
            )
            return

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
                    f"{asm_name}:   EQU     {self._hex16(addr)}    ; {decl.ctype} (init={self._hex8(decl.init.value)})"
                )
            else:
                self._data_lines.append(
                    f"{asm_name}:   EQU     {self._hex16(addr)}    ; {decl.ctype} (init={self._hex16(decl.init.value)})"
                )
        else:
            self._data_lines.append(
                f"{asm_name}:   EQU     {self._hex16(addr)}    ; {decl.ctype}"
            )

    # ── Function generation ───────────────────

    def _register_function(self, decl: FuncDecl):
        asm_name = (self._qualified_name(decl.name)
                    if self.relocatable and decl.is_static else decl.name)
        sym = Symbol(
            name=decl.name,
            ctype=decl.return_type,
            is_global=True,
            is_extern=(decl.body is None),
            asm_name=asm_name,
        )
        self._global_scope.define(sym)

    def _collect_local_decls(self, node: Optional[ASTNode]) -> List[VarDecl]:
        """Flatten local declarations so the whole frame is reserved once."""
        if node is None:
            return []
        if isinstance(node, VarDecl):
            return [node]
        if isinstance(node, Block):
            out: List[VarDecl] = []
            for child in node.statements:
                out.extend(self._collect_local_decls(child))
            return out
        if isinstance(node, IfStmt):
            return (self._collect_local_decls(node.then_body)
                    + self._collect_local_decls(node.else_body))
        if isinstance(node, (WhileStmt, DoWhileStmt)):
            return self._collect_local_decls(node.body)
        if isinstance(node, ForStmt):
            out = self._collect_local_decls(node.init)
            out.extend(self._collect_local_decls(node.body))
            return out
        return []

    def _emit_function_exit(self, decl: FuncDecl):
        if self._local_offset > 0:
            for _ in range(self._local_offset):
                self._emit("INS")
            self._emit_comment(f"free {self._local_offset} byte frame")
        if decl.is_interrupt:
            self._emit("RTI")
        else:
            self._emit("PULY")
            self._emit("RTS")

    def _gen_function(self, decl: FuncDecl):
        self._in_function = decl
        self._emit_blank()
        self._emit_comment(f"{'ISR' if decl.is_interrupt else 'Function'}: {decl.name}")
        func_sym = self._global_scope.lookup(decl.name)
        self._emit_label(self._asm_symbol(func_sym) if func_sym else decl.name)

        func_scope = Scope(parent=self._global_scope)
        self._current_scope = func_scope

        local_decls = self._collect_local_decls(decl.body)
        seen = set()
        frame_size = 0
        for local in local_decls:
            if local.name in seen:
                raise CodeGenError(
                    f"Duplicate/shadowed local '{local.name}' is not supported in the flat frame ABI",
                    local,
                )
            seen.add(local.name)
            if local.ctype.size <= 0:
                raise CodeGenError(f"Local has incomplete/zero-sized type: {local.name}", local)
            if local.init and (local.ctype.is_array or local.ctype.base == "struct"):
                raise CodeGenError("Aggregate local initializers are not supported yet", local)
            sym = Symbol(
                name=local.name,
                ctype=local.ctype,
                is_global=False,
                stack_offset=frame_size,
                is_zeropage=False,
                asm_name=local.name,
            )
            func_scope.define(sym)
            frame_size += local.ctype.size

        if frame_size > 240:
            raise CodeGenError(
                f"Function frame is {frame_size} bytes; Y-indexed frame limit is 240 bytes",
                decl,
            )
        self._local_offset = frame_size

        if decl.is_interrupt and decl.params:
            raise CodeGenError("Interrupt functions cannot take C parameters", decl)

        # Stable-frame ABI: Y is the frame pointer, X remains free for pointer/index work.
        if not decl.is_interrupt:
            self._emit("PSHY")
        for _ in range(frame_size):
            self._emit("DES")
        self._emit("TSY")
        if frame_size:
            self._emit_comment(f"reserve {frame_size} byte frame in Y")

        param_offset = frame_size + 4  # saved Y (2) + return address (2)
        for param in decl.params:
            if param_offset + max(1, param.ctype.size) > 255:
                raise CodeGenError("Parameter frame offset exceeds 8-bit indexed range", param)
            sym = Symbol(
                name=param.name,
                ctype=param.ctype,
                is_global=False,
                stack_offset=param_offset,
                is_param=True,
                asm_name=param.name,
            )
            func_scope.define(sym)
            param_offset += param.ctype.size

        if decl.body:
            for stmt in decl.body.statements:
                self._gen_statement(stmt)

        if decl.is_interrupt:
            if not (decl.body and decl.body.statements and
                    isinstance(decl.body.statements[-1], ReturnStmt)):
                self._emit_function_exit(decl)
        else:
            if not (decl.body and decl.body.statements and
                    isinstance(decl.body.statements[-1], ReturnStmt)):
                self._emit_function_exit(decl)

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
            raise CodeGenError(f"Unhandled statement type: {type(stmt).__name__}", stmt)

    def _gen_local_var(self, decl: VarDecl):
        """Emit only the initializer; storage was reserved in the function prologue."""
        sym = self._current_scope.lookup(decl.name)
        if sym is None or sym.is_global:
            raise CodeGenError(f"Missing frame slot for local: {decl.name}", decl)
        self._emit_comment(
            f"local Y+{sym.stack_offset}: {decl.ctype} {decl.name}"
        )
        if decl.init:
            self._gen_expr(decl.init)
            self._gen_identifier_store(Identifier(name=decl.name, line=decl.line, col=decl.col),
                                       decl.ctype)

    def _gen_return(self, stmt: ReturnStmt):
        """Generate return using the stable Y-frame ABI."""
        if stmt.value:
            self._gen_expr(stmt.value)
        if self._in_function is None:
            raise CodeGenError("return outside function", stmt)
        self._emit_function_exit(self._in_function)

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
        elif isinstance(expr, MemberAccess):
            return self._gen_member_access(expr)
        elif isinstance(expr, TernaryOp):
            return self._gen_ternary(expr)
        elif isinstance(expr, SizeofExpr):
            return self._gen_sizeof(expr)
        else:
            raise CodeGenError(f"Unhandled expression type: {type(expr).__name__}", expr)

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

    def _get_struct_field(self, ctype: CType, member: str,
                              node: ASTNode) -> StructField:
        if ctype.is_pointer:
            ctype = ctype.pointed_to()
        if ctype.base != "struct" or not ctype.struct_name:
            raise CodeGenError(f"Member access requires struct type, got {ctype}", node)
        decl = self._structs.get(ctype.struct_name)
        if decl is None:
            raise CodeGenError(f"Unknown struct layout: {ctype.struct_name}", node)
        for field in decl.fields:
            if field.name == member:
                return field
        raise CodeGenError(f"struct {ctype.struct_name} has no member '{member}'", node)

    def _infer_expr_type(self, expr: Expression) -> CType:
        """Infer expression type without emitting instructions."""
        if isinstance(expr, Identifier):
            sym = self._current_scope.lookup(expr.name)
            if sym is None:
                raise CodeGenError(f"Undefined variable: {expr.name}", expr)
            return sym.ctype
        if isinstance(expr, CharLiteral):
            return CType("char")
        if isinstance(expr, IntLiteral):
            return CType("char", is_unsigned=expr.value >= 0) if -128 <= expr.value <= 255 else CType("int")
        if isinstance(expr, Cast):
            return expr.cast_type
        if isinstance(expr, AddrOf):
            return self._infer_expr_type(expr.expr).pointer_to()
        if isinstance(expr, Deref):
            t = self._infer_expr_type(expr.expr)
            return t.pointed_to() if t.is_pointer else CType("char", is_unsigned=True)
        if isinstance(expr, ArraySubscript):
            t = self._infer_expr_type(expr.array)
            if t.is_array:
                return t.element_type()
            if t.is_pointer:
                return t.pointed_to()
            raise CodeGenError("Subscripted expression is not an array/pointer", expr)
        if isinstance(expr, MemberAccess):
            obj_t = self._infer_expr_type(expr.object)
            if expr.is_arrow:
                if not obj_t.is_pointer:
                    raise CodeGenError("'->' requires pointer-to-struct", expr)
                obj_t = obj_t.pointed_to()
            return self._get_struct_field(obj_t, expr.member, expr).ctype
        if isinstance(expr, FuncCall):
            sym = self._global_scope.lookup(expr.name)
            return sym.ctype if sym else CType("int")
        if isinstance(expr, (Assignment, CompoundAssignment)):
            return self._infer_expr_type(expr.target)
        if isinstance(expr, BinaryOp):
            return self._promote_types(self._infer_expr_type(expr.left),
                                       self._infer_expr_type(expr.right))
        if isinstance(expr, (PreIncDec, PostIncDec)):
            return self._infer_expr_type(expr.operand)
        if isinstance(expr, TernaryOp):
            return self._promote_types(self._infer_expr_type(expr.then_expr),
                                       self._infer_expr_type(expr.else_expr))
        return CType("int")

    def _emit_add_x_const(self, value: int):
        """Add an arbitrary non-negative constant to X using ABX chunks."""
        remaining = int(value)
        while remaining > 0:
            chunk = min(remaining, 255)
            self._emit(f"LDAB    {self._imm8(chunk)}")
            self._emit("ABX")
            remaining -= chunk

    def _emit_scaled_index_add(self, elem_size: int):
        """Add B * elem_size to X without assuming the result fits in 8 bits."""
        if elem_size <= 0:
            raise ValueError("element size must be positive")
        if elem_size == 1:
            self._emit("ABX")
            return
        loop = self._label("idx")
        done = self._label("idx_done")
        self._emit("TSTB")
        self._emit(f"BEQ     {done}")
        self._emit_label(loop)
        for _ in range(elem_size):
            self._emit("INX")
        self._emit("DECB")
        self._emit(f"BNE     {loop}")
        self._emit_label(done)

    def _gen_lvalue_address(self, expr: Expression) -> CType:
        """Put the address of an lvalue in X and return its stored type."""
        if isinstance(expr, Identifier):
            sym = self._current_scope.lookup(expr.name)
            if sym is None:
                raise CodeGenError(f"Undefined variable: {expr.name}", expr)
            if sym.is_global:
                if sym.fixed_addr is not None:
                    self._emit(f"LDX     {self._imm16(sym.fixed_addr)}")
                else:
                    self._emit(f"LDX     #{self._asm_symbol(sym)}")
            else:
                # Copy stable frame pointer Y -> X without changing Y or net SP.
                self._emit("PSHY")
                self._emit("PULX")
                self._emit_add_x_const(sym.stack_offset)
            return sym.ctype

        if isinstance(expr, Deref):
            ptr_t = self._gen_expr(expr.expr)
            if not ptr_t.is_pointer:
                raise CodeGenError("Cannot dereference non-pointer lvalue", expr)
            self._emit("XGDX")
            return ptr_t.pointed_to()

        if isinstance(expr, ArraySubscript):
            base_t = self._infer_expr_type(expr.array)
            elem_t = base_t.element_type() if base_t.is_array else (
                base_t.pointed_to() if base_t.is_pointer else None
            )
            if elem_t is None:
                raise CodeGenError("Subscripted expression is not an array/pointer", expr)

            idx_t = self._gen_expr(expr.index)
            if idx_t.is_byte:
                self._emit("TAB")
            # For 16-bit indices B already holds the low byte. Fixed-size HC11
            # arrays are intentionally limited to 255 elements in this ABI.
            self._emit(f"STAB    {self._hex8(self._scratch_index_addr)}")

            if base_t.is_array:
                self._gen_lvalue_address(expr.array)
            else:
                self._gen_expr(expr.array)
                self._emit("XGDX")

            self._emit(f"LDAB    {self._hex8(self._scratch_index_addr)}")
            self._emit_scaled_index_add(elem_t.size)
            return elem_t

        if isinstance(expr, MemberAccess):
            obj_t = self._infer_expr_type(expr.object)
            if expr.is_arrow:
                if not obj_t.is_pointer:
                    raise CodeGenError("'->' requires pointer-to-struct", expr)
                struct_t = obj_t.pointed_to()
                self._gen_expr(expr.object)
                self._emit("XGDX")
            else:
                struct_t = obj_t
                self._gen_lvalue_address(expr.object)
            field = self._get_struct_field(struct_t, expr.member, expr)
            self._emit_add_x_const(field.offset)
            return field.ctype

        raise CodeGenError(f"Expression is not an addressable lvalue: {type(expr).__name__}", expr)

    def _load_lvalue(self, expr: Expression) -> CType:
        ctype = self._gen_lvalue_address(expr)
        if ctype.is_array:
            # C array-to-pointer decay.
            self._emit("XGDX")
            return ctype.element_type().pointer_to()
        if ctype.base == "struct" and not ctype.is_pointer:
            raise CodeGenError("Whole-struct rvalue copies are not supported", expr)
        if ctype.size == 1:
            self._emit("LDAA    0,X")
        elif ctype.size == 2:
            self._emit("LDD     0,X")
        else:
            raise CodeGenError(f"Cannot scalar-load {ctype.size}-byte object", expr)
        return ctype

    def _coerce_result(self, src: CType, dst: CType):
        """Coerce the current A/D result to the scalar destination width."""
        if dst.size == 1 and src.size == 2:
            self._emit("TBA")
        elif dst.size == 2 and src.size == 1:
            self._emit("TAB")
            if src.is_unsigned:
                self._emit("CLRA")
            else:
                self._emit("CLRA")
                ok = self._label("sext_ok")
                self._emit("TSTB")
                self._emit(f"BPL     {ok}")
                self._emit("LDAA    #$FF")
                self._emit_label(ok)

    def _store_lvalue(self, expr: Expression, src_type: CType) -> CType:
        dst_type = self._infer_expr_type(expr)
        if dst_type.is_array or (dst_type.base == "struct" and not dst_type.is_pointer):
            raise CodeGenError("Aggregate assignment/copy is not supported", expr)
        self._coerce_result(src_type, dst_type)

        if dst_type.size == 1:
            self._emit("PSHA")
        elif dst_type.size == 2:
            self._emit("PSHB")
            self._emit("PSHA")
        else:
            raise CodeGenError(f"Cannot scalar-store {dst_type.size}-byte object", expr)

        self._gen_lvalue_address(expr)

        if dst_type.size == 1:
            self._emit("PULA")
            self._emit("STAA    0,X")
        else:
            self._emit("PULA")
            self._emit("PULB")
            self._emit("STD     0,X")
        return dst_type

    def _gen_identifier_load(self, ident: Identifier) -> CType:
        """Load a scalar identifier or decay an array to a pointer."""
        sym = self._current_scope.lookup(ident.name)
        if sym is None:
            raise CodeGenError(f"Undefined variable: {ident.name}", ident)

        if sym.ctype.is_array:
            self._gen_lvalue_address(ident)
            self._emit("XGDX")
            return sym.ctype.element_type().pointer_to()
        if sym.ctype.base == "struct" and not sym.ctype.is_pointer:
            raise CodeGenError("Whole-struct rvalue copies are not supported", ident)

        if sym.is_global:
            addr = sym.fixed_addr
            asm_name = self._asm_symbol(sym)
            if addr is not None and addr <= 0xFF:
                if sym.ctype.size == 1:
                    self._emit(f"LDAA    {self._hex8(addr)}     ; {sym.name}")
                else:
                    self._emit(f"LDD     {self._hex8(addr)}     ; {sym.name}")
            elif addr is not None:
                if sym.ctype.size == 1:
                    self._emit(f"LDAA    {self._hex16(addr)}   ; {sym.name}")
                else:
                    self._emit(f"LDD     {self._hex16(addr)}   ; {sym.name}")
            else:
                if sym.ctype.size == 1:
                    self._emit(f"LDAA    {asm_name}")
                else:
                    self._emit(f"LDD     {asm_name}")
        else:
            if sym.ctype.size == 1:
                self._emit(f"LDAA    {sym.stack_offset},Y  ; {sym.name}")
            else:
                self._emit(f"LDD     {sym.stack_offset},Y  ; {sym.name}")

        return sym.ctype

    def _gen_identifier_store(self, ident: Identifier, ctype: CType):
        """Store the current scalar result to an identifier."""
        sym = self._current_scope.lookup(ident.name)
        if sym is None:
            raise CodeGenError(f"Undefined variable: {ident.name}", ident)
        if sym.ctype.is_array or (sym.ctype.base == "struct" and not sym.ctype.is_pointer):
            raise CodeGenError("Aggregate assignment/copy is not supported", ident)

        self._coerce_result(ctype, sym.ctype)
        if sym.is_global:
            addr = sym.fixed_addr
            asm_name = self._asm_symbol(sym)
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
                    self._emit(f"STAA    {asm_name}")
                else:
                    self._emit(f"STD     {asm_name}")
        else:
            if sym.ctype.size == 1:
                self._emit(f"STAA    {sym.stack_offset},Y  ; {sym.name}")
            else:
                self._emit(f"STD     {sym.stack_offset},Y  ; {sym.name}")

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
                    raise CodeGenError(f"Unsupported 16-bit binary operator: {op.op}", op)

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
            raise CodeGenError(f"Unsupported 8-bit binary operator: {op.op}", op)

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
            raise CodeGenError(f"Unsupported unary operator: {op.op}", op)

        return result_type

    def _gen_assignment(self, asgn: Assignment) -> CType:
        """Generate scalar assignment through the common lvalue path."""
        rtype = self._gen_expr(asgn.value)
        if isinstance(asgn.target, Identifier):
            dst = self._infer_expr_type(asgn.target)
            self._gen_identifier_store(asgn.target, rtype)
            return dst
        if isinstance(asgn.target, (Deref, ArraySubscript, MemberAccess)):
            return self._store_lvalue(asgn.target, rtype)
        raise CodeGenError(f"Unsupported assignment target: {type(asgn.target).__name__}", asgn)

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
                raise CodeGenError(f"Unsupported compound assignment operator: {asgn.op}", asgn)

            # Store result back
            self._gen_identifier_store(asgn.target, ltype)
            return ltype
        else:
            raise CodeGenError(f"Unsupported compound assignment target: {type(asgn.target).__name__}", asgn)

    def _gen_func_call(self, call: FuncCall) -> CType:
        """Generate function call with right-to-left stack arguments."""
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

        sym = self._global_scope.lookup(call.name)
        call_name = self._asm_symbol(sym) if sym else call.name
        self._emit(f"JSR     {call_name}")

        if total_arg_size > 0:
            for _ in range(total_arg_size):
                self._emit("INS")
            self._emit_comment(f"clean {total_arg_size} bytes args")

        return sym.ctype if sym else CType("int")

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
        """Generate pointer dereference using the common typed lvalue path."""
        return self._load_lvalue(deref)

    def _gen_addr_of(self, addr: AddrOf) -> CType:
        """Generate address-of for any supported lvalue."""
        ctype = self._gen_lvalue_address(addr.expr)
        self._emit("XGDX")
        return ctype.pointer_to()

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
        raise CodeGenError(f"Unsupported pre-{op.op} target: {type(op.operand).__name__}", op)

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
        raise CodeGenError(f"Unsupported post-{op.op} target: {type(op.operand).__name__}", op)

    def _gen_array_subscript(self, sub: ArraySubscript) -> CType:
        """Generate typed array/pointer subscript read."""
        return self._load_lvalue(sub)

    def _gen_member_access(self, member: MemberAccess) -> CType:
        """Generate typed struct member read."""
        return self._load_lvalue(member)

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
        """Generate sizeof resolved entirely at compile time."""
        if expr.target_type:
            size = expr.target_type.size
        elif expr.target_expr is not None:
            size = self._infer_expr_type(expr.target_expr).size
        else:
            size = 0
        if size <= 0xFF:
            self._emit(f"LDAA    {self._imm8(size)}  ; sizeof")
            return CType("char", is_unsigned=True)
        self._emit(f"LDD     {self._imm16(size)}  ; sizeof")
        return CType("int", is_unsigned=True)

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
