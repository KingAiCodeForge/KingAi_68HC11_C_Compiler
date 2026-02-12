"""
Recursive-descent parser for the 68HC11 C Compiler.

Parses a token stream from the Lexer into an AST defined in ast_nodes.
Supports a practical subset of C suitable for embedded 68HC11 programming:

  - Global/local variable declarations with initializers
  - Function definitions (including __interrupt ISRs)
  - Type qualifiers: volatile, const, unsigned, signed, static
  - Expressions: arithmetic, bitwise, logical, comparison, ternary
  - Pointer dereference, address-of, array subscript
  - Casts: (type)expr
  - Inline assembly: asm("...");
  - Control flow: if/else, while, do-while, for, break, continue, return
  - __zeropage qualifier for direct-page variable placement
  - __attribute__((interrupt)) for ISR marking
"""

from __future__ import annotations
from typing import List, Optional
from .lexer import Token, TokenType
from .ast_nodes import *


class ParseError(Exception):
    def __init__(self, message: str, token: Token):
        self.token = token
        loc = f"L{token.line}:{token.col}"
        super().__init__(f"Parse error at {loc}: {message} (got {token.type.name} = {token.value!r})")


class Parser:
    """Recursive descent parser producing an AST from tokens."""

    def __init__(self, tokens: List[Token], source: str = ""):
        self.tokens = tokens
        self.source = source
        self.pos = 0

    # ── Helpers ─────────────────────────────

    def _cur(self) -> Token:
        return self.tokens[self.pos]

    def _peek(self, offset: int = 0) -> Token:
        i = self.pos + offset
        if i < len(self.tokens):
            return self.tokens[i]
        return self.tokens[-1]  # EOF

    def _at(self, *types: TokenType) -> bool:
        return self._cur().type in types

    def _advance(self) -> Token:
        tok = self.tokens[self.pos]
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return tok

    def _expect(self, ttype: TokenType, msg: str = "") -> Token:
        if self._cur().type != ttype:
            if not msg:
                msg = f"Expected {ttype.value!r}"
            raise ParseError(msg, self._cur())
        return self._advance()

    def _match(self, *types: TokenType) -> Optional[Token]:
        if self._cur().type in types:
            return self._advance()
        return None

    # ── Type parsing ──────────────────────────

    def _is_type_start(self) -> bool:
        """Check if current token starts a type specifier."""
        return self._at(
            TokenType.KW_VOID, TokenType.KW_CHAR, TokenType.KW_INT,
            TokenType.KW_UNSIGNED, TokenType.KW_SIGNED,
            TokenType.KW_VOLATILE, TokenType.KW_CONST,
            TokenType.KW_STATIC, TokenType.KW_STRUCT,
        )

    def _parse_type(self) -> CType:
        """Parse a C type specifier, including qualifiers and pointer stars."""
        is_unsigned = False
        is_signed = False
        is_volatile = False
        is_const = False
        is_static = False
        base = None

        # Collect qualifiers and type keywords in any order
        while True:
            if self._match(TokenType.KW_UNSIGNED):
                is_unsigned = True
            elif self._match(TokenType.KW_SIGNED):
                is_signed = True
            elif self._match(TokenType.KW_VOLATILE):
                is_volatile = True
            elif self._match(TokenType.KW_CONST):
                is_const = True
            elif self._match(TokenType.KW_STATIC):
                is_static = True
            elif self._match(TokenType.KW_VOID):
                base = "void"
            elif self._match(TokenType.KW_CHAR):
                base = "char"
            elif self._match(TokenType.KW_INT):
                base = "int"
            else:
                break

        # If only unsigned/signed given with no base, default to int
        if base is None:
            if is_unsigned or is_signed:
                base = "int"
            else:
                raise ParseError("Expected type specifier", self._cur())

        # Count pointer stars
        pointer_depth = 0
        while self._match(TokenType.STAR):
            pointer_depth += 1

        return CType(
            base=base,
            is_unsigned=is_unsigned,
            is_volatile=is_volatile,
            is_const=is_const,
            is_static=is_static,
            pointer_depth=pointer_depth,
        )

    # ── Top-level parsing ─────────────────────

    def parse(self) -> Program:
        """Parse the full token stream into a Program AST."""
        prog = Program(line=1, col=1)

        while not self._at(TokenType.EOF):
            decl = self._parse_top_level_decl()
            if decl is not None:
                prog.declarations.append(decl)

        return prog

    def _parse_top_level_decl(self) -> Optional[ASTNode]:
        """Parse a top-level declaration: function or global variable."""

        # Handle typedef
        if self._at(TokenType.KW_TYPEDEF):
            return self._parse_typedef()

        # Check for __interrupt keyword before type
        is_interrupt = False
        is_zeropage = False

        if self._match(TokenType.KW_INTERRUPT):
            is_interrupt = True

        if self._match(TokenType.KW_ZEROPAGE):
            is_zeropage = True

        if not self._is_type_start():
            raise ParseError("Expected type or declaration", self._cur())

        ctype = self._parse_type()

        # Check for __attribute__((...))
        attrs = self._try_parse_attributes()
        if "interrupt" in attrs:
            is_interrupt = True
        if "zero_page" in attrs or "zeropage" in attrs:
            is_zeropage = True

        # Name
        name_tok = self._expect(TokenType.IDENT, "Expected identifier")
        name = name_tok.value

        # More attributes after name
        attrs2 = self._try_parse_attributes()
        if "interrupt" in attrs2:
            is_interrupt = True

        # Function definition?
        if self._at(TokenType.LPAREN):
            return self._parse_func_def(name, ctype, is_interrupt, name_tok)

        # Variable declaration
        return self._parse_global_var_decl(name, ctype, is_zeropage, name_tok)

    def _try_parse_attributes(self) -> List[str]:
        """Try to parse __attribute__((...)) and return attribute names."""
        attrs = []
        while self._at(TokenType.KW_ATTRIBUTE):
            self._advance()  # __attribute__
            self._expect(TokenType.LPAREN)
            self._expect(TokenType.LPAREN)
            # Read attribute name(s)
            while not self._at(TokenType.RPAREN):
                if self._at(TokenType.IDENT):
                    attrs.append(self._advance().value)
                elif self._at(TokenType.COMMA):
                    self._advance()
                else:
                    self._advance()  # skip unknown tokens inside attribute
            self._expect(TokenType.RPAREN)
            self._expect(TokenType.RPAREN)
        return attrs

    def _parse_func_def(self, name: str, return_type: CType,
                        is_interrupt: bool, name_tok: Token) -> FuncDecl:
        """Parse function definition: type name(params) { body }"""
        self._expect(TokenType.LPAREN)
        params = self._parse_param_list()
        self._expect(TokenType.RPAREN)

        body = self._parse_block()

        return FuncDecl(
            name=name,
            return_type=return_type,
            params=params,
            body=body,
            is_interrupt=is_interrupt,
            is_static=return_type.is_static,
            line=name_tok.line,
            col=name_tok.col,
        )

    def _parse_param_list(self) -> List[FuncParam]:
        """Parse function parameter list."""
        params = []
        if self._at(TokenType.RPAREN):
            return params
        if self._at(TokenType.KW_VOID) and self._peek(1).type == TokenType.RPAREN:
            self._advance()  # skip 'void'
            return params

        while True:
            ptype = self._parse_type()
            pname = ""
            if self._at(TokenType.IDENT):
                pname = self._advance().value
            params.append(FuncParam(name=pname, ctype=ptype,
                                    line=self._cur().line, col=self._cur().col))
            if not self._match(TokenType.COMMA):
                break
        return params

    def _parse_global_var_decl(self, name: str, ctype: CType,
                               is_zeropage: bool, name_tok: Token) -> VarDecl:
        """Parse global variable declaration."""
        init = None
        if self._match(TokenType.ASSIGN):
            init = self._parse_expr()
        self._expect(TokenType.SEMI, "Expected ';' after variable declaration")
        return VarDecl(
            name=name, ctype=ctype, init=init, is_zeropage=is_zeropage,
            line=name_tok.line, col=name_tok.col,
        )

    def _parse_typedef(self) -> TypedefDecl:
        """Parse typedef declaration."""
        tok = self._advance()  # 'typedef'
        ctype = self._parse_type()
        name = self._expect(TokenType.IDENT).value
        self._expect(TokenType.SEMI)
        return TypedefDecl(name=name, ctype=ctype, line=tok.line, col=tok.col)

    # ── Statements ────────────────────────────

    def _parse_block(self) -> Block:
        """Parse a compound statement { ... }."""
        tok = self._expect(TokenType.LBRACE)
        block = Block(line=tok.line, col=tok.col)

        while not self._at(TokenType.RBRACE, TokenType.EOF):
            stmt = self._parse_statement()
            if stmt is not None:
                block.statements.append(stmt)

        self._expect(TokenType.RBRACE, "Expected '}'")
        return block

    def _parse_statement(self) -> Optional[ASTNode]:
        """Parse a single statement."""

        # Block
        if self._at(TokenType.LBRACE):
            return self._parse_block()

        # Return
        if self._at(TokenType.KW_RETURN):
            return self._parse_return()

        # If
        if self._at(TokenType.KW_IF):
            return self._parse_if()

        # While
        if self._at(TokenType.KW_WHILE):
            return self._parse_while()

        # Do-while
        if self._at(TokenType.KW_DO):
            return self._parse_do_while()

        # For
        if self._at(TokenType.KW_FOR):
            return self._parse_for()

        # Break
        if self._match(TokenType.KW_BREAK):
            self._expect(TokenType.SEMI)
            return BreakStmt(line=self._cur().line, col=self._cur().col)

        # Continue
        if self._match(TokenType.KW_CONTINUE):
            self._expect(TokenType.SEMI)
            return ContinueStmt(line=self._cur().line, col=self._cur().col)

        # Inline assembly
        if self._at(TokenType.KW_ASM):
            return self._parse_asm()

        # Local variable declaration (starts with type keyword)
        if self._is_type_start():
            return self._parse_local_var_decl()

        # Check for __zeropage before type
        if self._at(TokenType.KW_ZEROPAGE):
            self._advance()
            return self._parse_local_var_decl(is_zeropage=True)

        # Expression statement
        return self._parse_expr_statement()

    def _parse_return(self) -> ReturnStmt:
        tok = self._advance()  # 'return'
        value = None
        if not self._at(TokenType.SEMI):
            value = self._parse_expr()
        self._expect(TokenType.SEMI, "Expected ';' after return")
        return ReturnStmt(value=value, line=tok.line, col=tok.col)

    def _parse_if(self) -> IfStmt:
        tok = self._advance()  # 'if'
        self._expect(TokenType.LPAREN)
        cond = self._parse_expr()
        self._expect(TokenType.RPAREN)
        then_body = self._parse_statement()

        else_body = None
        if self._match(TokenType.KW_ELSE):
            else_body = self._parse_statement()

        return IfStmt(condition=cond, then_body=then_body, else_body=else_body,
                      line=tok.line, col=tok.col)

    def _parse_while(self) -> WhileStmt:
        tok = self._advance()  # 'while'
        self._expect(TokenType.LPAREN)
        cond = self._parse_expr()
        self._expect(TokenType.RPAREN)
        body = self._parse_statement()
        return WhileStmt(condition=cond, body=body, line=tok.line, col=tok.col)

    def _parse_do_while(self) -> DoWhileStmt:
        tok = self._advance()  # 'do'
        body = self._parse_statement()
        self._expect(TokenType.KW_WHILE, "Expected 'while' after do body")
        self._expect(TokenType.LPAREN)
        cond = self._parse_expr()
        self._expect(TokenType.RPAREN)
        self._expect(TokenType.SEMI)
        return DoWhileStmt(condition=cond, body=body, line=tok.line, col=tok.col)

    def _parse_for(self) -> ForStmt:
        tok = self._advance()  # 'for'
        self._expect(TokenType.LPAREN)

        # Init
        init = None
        if not self._at(TokenType.SEMI):
            if self._is_type_start():
                init = self._parse_local_var_decl_no_semi()
            else:
                init = ExprStatement(expr=self._parse_expr())
        self._expect(TokenType.SEMI)

        # Condition
        cond = None
        if not self._at(TokenType.SEMI):
            cond = self._parse_expr()
        self._expect(TokenType.SEMI)

        # Update
        update = None
        if not self._at(TokenType.RPAREN):
            update = self._parse_expr()

        self._expect(TokenType.RPAREN)
        body = self._parse_statement()

        return ForStmt(init=init, condition=cond, update=update, body=body,
                       line=tok.line, col=tok.col)

    def _parse_asm(self) -> AsmStmt:
        tok = self._advance()  # 'asm'
        self._expect(TokenType.LPAREN)
        str_tok = self._expect(TokenType.STRING_LITERAL, "Expected assembly string")
        self._expect(TokenType.RPAREN)
        self._expect(TokenType.SEMI)
        return AsmStmt(instructions=str_tok.value, line=tok.line, col=tok.col)

    def _parse_local_var_decl(self, is_zeropage: bool = False) -> VarDecl:
        """Parse local variable declaration with semicolon."""
        decl = self._parse_local_var_decl_no_semi(is_zeropage)
        self._expect(TokenType.SEMI, "Expected ';' after variable declaration")
        return decl

    def _parse_local_var_decl_no_semi(self, is_zeropage: bool = False) -> VarDecl:
        """Parse local variable declaration without consuming semicolon."""
        ctype = self._parse_type()

        # Check for __zeropage / __attribute__ after type
        if self._match(TokenType.KW_ZEROPAGE):
            is_zeropage = True
        attrs = self._try_parse_attributes()
        if "zero_page" in attrs or "zeropage" in attrs:
            is_zeropage = True

        name_tok = self._expect(TokenType.IDENT, "Expected variable name")
        init = None
        if self._match(TokenType.ASSIGN):
            init = self._parse_expr()
        return VarDecl(
            name=name_tok.value, ctype=ctype, init=init, is_zeropage=is_zeropage,
            line=name_tok.line, col=name_tok.col,
        )

    def _parse_expr_statement(self) -> ExprStatement:
        tok = self._cur()
        expr = self._parse_expr()
        self._expect(TokenType.SEMI, "Expected ';' after expression")
        return ExprStatement(expr=expr, line=tok.line, col=tok.col)

    # ── Expression parsing (precedence climbing) ──

    def _parse_expr(self) -> Expression:
        """Parse an expression (entry point: handles assignment and ternary)."""
        return self._parse_assignment()

    def _parse_assignment(self) -> Expression:
        """Parse assignment expressions (right-associative)."""
        left = self._parse_ternary()

        # Simple assignment
        if self._at(TokenType.ASSIGN):
            tok = self._advance()
            right = self._parse_assignment()  # right-associative
            return Assignment(target=left, value=right, line=tok.line, col=tok.col)

        # Compound assignments
        compound_ops = {
            TokenType.PLUS_ASSIGN: "+=",
            TokenType.MINUS_ASSIGN: "-=",
            TokenType.STAR_ASSIGN: "*=",
            TokenType.SLASH_ASSIGN: "/=",
            TokenType.PERCENT_ASSIGN: "%=",
            TokenType.AMP_ASSIGN: "&=",
            TokenType.PIPE_ASSIGN: "|=",
            TokenType.CARET_ASSIGN: "^=",
            TokenType.LSHIFT_ASSIGN: "<<=",
            TokenType.RSHIFT_ASSIGN: ">>=",
        }
        for ttype, op_str in compound_ops.items():
            if self._at(ttype):
                tok = self._advance()
                right = self._parse_assignment()
                return CompoundAssignment(op=op_str, target=left, value=right,
                                          line=tok.line, col=tok.col)

        return left

    def _parse_ternary(self) -> Expression:
        """Parse ternary: cond ? then : else"""
        expr = self._parse_logical_or()

        if self._match(TokenType.QUESTION):
            then_expr = self._parse_expr()
            self._expect(TokenType.COLON, "Expected ':' in ternary")
            else_expr = self._parse_ternary()
            return TernaryOp(condition=expr, then_expr=then_expr, else_expr=else_expr,
                             line=expr.line, col=expr.col)
        return expr

    def _parse_logical_or(self) -> Expression:
        left = self._parse_logical_and()
        while self._at(TokenType.OR):
            tok = self._advance()
            right = self._parse_logical_and()
            left = BinaryOp(op="||", left=left, right=right,
                            line=tok.line, col=tok.col)
        return left

    def _parse_logical_and(self) -> Expression:
        left = self._parse_bitwise_or()
        while self._at(TokenType.AND):
            tok = self._advance()
            right = self._parse_bitwise_or()
            left = BinaryOp(op="&&", left=left, right=right,
                            line=tok.line, col=tok.col)
        return left

    def _parse_bitwise_or(self) -> Expression:
        left = self._parse_bitwise_xor()
        while self._at(TokenType.PIPE):
            tok = self._advance()
            right = self._parse_bitwise_xor()
            left = BinaryOp(op="|", left=left, right=right,
                            line=tok.line, col=tok.col)
        return left

    def _parse_bitwise_xor(self) -> Expression:
        left = self._parse_bitwise_and()
        while self._at(TokenType.CARET):
            tok = self._advance()
            right = self._parse_bitwise_and()
            left = BinaryOp(op="^", left=left, right=right,
                            line=tok.line, col=tok.col)
        return left

    def _parse_bitwise_and(self) -> Expression:
        left = self._parse_equality()
        while self._at(TokenType.AMP):
            tok = self._advance()
            right = self._parse_equality()
            left = BinaryOp(op="&", left=left, right=right,
                            line=tok.line, col=tok.col)
        return left

    def _parse_equality(self) -> Expression:
        left = self._parse_relational()
        while self._at(TokenType.EQ, TokenType.NEQ):
            tok = self._advance()
            right = self._parse_relational()
            left = BinaryOp(op=tok.value, left=left, right=right,
                            line=tok.line, col=tok.col)
        return left

    def _parse_relational(self) -> Expression:
        left = self._parse_shift()
        while self._at(TokenType.LT, TokenType.GT, TokenType.LE, TokenType.GE):
            tok = self._advance()
            right = self._parse_shift()
            left = BinaryOp(op=tok.value, left=left, right=right,
                            line=tok.line, col=tok.col)
        return left

    def _parse_shift(self) -> Expression:
        left = self._parse_additive()
        while self._at(TokenType.LSHIFT, TokenType.RSHIFT):
            tok = self._advance()
            right = self._parse_additive()
            left = BinaryOp(op=tok.value, left=left, right=right,
                            line=tok.line, col=tok.col)
        return left

    def _parse_additive(self) -> Expression:
        left = self._parse_multiplicative()
        while self._at(TokenType.PLUS, TokenType.MINUS):
            tok = self._advance()
            right = self._parse_multiplicative()
            left = BinaryOp(op=tok.value, left=left, right=right,
                            line=tok.line, col=tok.col)
        return left

    def _parse_multiplicative(self) -> Expression:
        left = self._parse_cast()
        while self._at(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            tok = self._advance()
            right = self._parse_cast()
            left = BinaryOp(op=tok.value, left=left, right=right,
                            line=tok.line, col=tok.col)
        return left

    def _parse_cast(self) -> Expression:
        """Parse cast expression: (type)expr or fall through to unary."""
        # Lookahead: ( followed by type keyword followed by ) => cast
        if self._at(TokenType.LPAREN):
            saved = self.pos
            self._advance()  # (

            # Check if this looks like a cast
            if self._is_type_start() or self._at(TokenType.KW_UNSIGNED, TokenType.KW_SIGNED):
                try:
                    cast_type = self._parse_type()
                    if self._at(TokenType.RPAREN):
                        self._advance()  # )
                        expr = self._parse_cast()
                        return Cast(cast_type=cast_type, expr=expr,
                                    line=self._cur().line, col=self._cur().col)
                except ParseError:
                    pass

            # Not a cast — backtrack and parse as parenthesized expression
            self.pos = saved

        return self._parse_unary()

    def _parse_unary(self) -> Expression:
        """Parse unary prefix operators: -, ~, !, *, &, ++, --"""
        tok = self._cur()

        # Pre-increment / pre-decrement
        if self._at(TokenType.INC):
            self._advance()
            operand = self._parse_unary()
            return PreIncDec(op="++", operand=operand, line=tok.line, col=tok.col)

        if self._at(TokenType.DEC):
            self._advance()
            operand = self._parse_unary()
            return PreIncDec(op="--", operand=operand, line=tok.line, col=tok.col)

        # Dereference
        if self._at(TokenType.STAR):
            self._advance()
            operand = self._parse_cast()
            return Deref(expr=operand, line=tok.line, col=tok.col)

        # Address-of
        if self._at(TokenType.AMP):
            self._advance()
            operand = self._parse_cast()
            return AddrOf(expr=operand, line=tok.line, col=tok.col)

        # Unary minus, bitwise NOT, logical NOT
        if self._at(TokenType.MINUS):
            self._advance()
            operand = self._parse_cast()
            return UnaryOp(op="-", operand=operand, line=tok.line, col=tok.col)

        if self._at(TokenType.TILDE):
            self._advance()
            operand = self._parse_cast()
            return UnaryOp(op="~", operand=operand, line=tok.line, col=tok.col)

        if self._at(TokenType.BANG):
            self._advance()
            operand = self._parse_cast()
            return UnaryOp(op="!", operand=operand, line=tok.line, col=tok.col)

        # sizeof
        if self._at(TokenType.KW_SIZEOF):
            return self._parse_sizeof()

        return self._parse_postfix()

    def _parse_sizeof(self) -> SizeofExpr:
        tok = self._advance()  # sizeof
        self._expect(TokenType.LPAREN)
        if self._is_type_start():
            stype = self._parse_type()
            self._expect(TokenType.RPAREN)
            return SizeofExpr(target_type=stype, line=tok.line, col=tok.col)
        expr = self._parse_expr()
        self._expect(TokenType.RPAREN)
        return SizeofExpr(target_expr=expr, line=tok.line, col=tok.col)

    def _parse_postfix(self) -> Expression:
        """Parse postfix operators: [], (), ., ->, ++, --"""
        expr = self._parse_primary()

        while True:
            # Array subscript
            if self._at(TokenType.LBRACKET):
                self._advance()
                index = self._parse_expr()
                self._expect(TokenType.RBRACKET)
                expr = ArraySubscript(array=expr, index=index,
                                      line=expr.line, col=expr.col)
                continue

            # Function call
            if self._at(TokenType.LPAREN) and isinstance(expr, Identifier):
                self._advance()
                args = self._parse_arg_list()
                self._expect(TokenType.RPAREN)
                expr = FuncCall(name=expr.name, args=args,
                                line=expr.line, col=expr.col)
                continue

            # Member access: .member
            if self._at(TokenType.DOT):
                self._advance()
                member = self._expect(TokenType.IDENT).value
                expr = MemberAccess(object=expr, member=member, is_arrow=False,
                                    line=expr.line, col=expr.col)
                continue

            # Arrow access: ->member
            if self._at(TokenType.ARROW):
                self._advance()
                member = self._expect(TokenType.IDENT).value
                expr = MemberAccess(object=expr, member=member, is_arrow=True,
                                    line=expr.line, col=expr.col)
                continue

            # Post-increment
            if self._at(TokenType.INC):
                tok = self._advance()
                expr = PostIncDec(op="++", operand=expr, line=tok.line, col=tok.col)
                continue

            # Post-decrement
            if self._at(TokenType.DEC):
                tok = self._advance()
                expr = PostIncDec(op="--", operand=expr, line=tok.line, col=tok.col)
                continue

            break

        return expr

    def _parse_arg_list(self) -> List[Expression]:
        """Parse function call argument list."""
        args = []
        if self._at(TokenType.RPAREN):
            return args
        args.append(self._parse_assignment())  # assignment level, not full expr with comma
        while self._match(TokenType.COMMA):
            args.append(self._parse_assignment())
        return args

    def _parse_primary(self) -> Expression:
        """Parse primary expressions: literals, identifiers, parenthesized."""
        tok = self._cur()

        # Integer literal
        if self._at(TokenType.INT_LITERAL):
            self._advance()
            return IntLiteral(value=tok.value, line=tok.line, col=tok.col)

        # Character literal
        if self._at(TokenType.CHAR_LITERAL):
            self._advance()
            return CharLiteral(value=tok.value, line=tok.line, col=tok.col)

        # String literal
        if self._at(TokenType.STRING_LITERAL):
            self._advance()
            return StringLiteral(value=tok.value, line=tok.line, col=tok.col)

        # Identifier
        if self._at(TokenType.IDENT):
            self._advance()
            return Identifier(name=tok.value, line=tok.line, col=tok.col)

        # Parenthesized expression
        if self._at(TokenType.LPAREN):
            self._advance()
            expr = self._parse_expr()
            self._expect(TokenType.RPAREN, "Expected ')'")
            return expr

        raise ParseError("Expected expression", tok)
