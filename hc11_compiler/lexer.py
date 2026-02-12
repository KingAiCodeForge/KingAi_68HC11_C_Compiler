"""
Lexer / Tokenizer for the 68HC11 C Compiler.

Converts C source text into a stream of tokens for the parser.
Handles C keywords, identifiers, integer literals (decimal, hex, binary, octal),
character literals, string literals, operators, and punctuation.

Includes a minimal preprocessor pass that resolves #define constants
and strips #include lines (since headers are expected to be pre-included
or handled externally for embedded targets).
"""

from __future__ import annotations
import enum
import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict


# ──────────────────────────────────────────────
# Token types
# ──────────────────────────────────────────────

class TokenType(enum.Enum):
    # Literals
    INT_LITERAL = "INT_LITERAL"
    CHAR_LITERAL = "CHAR_LITERAL"
    STRING_LITERAL = "STRING_LITERAL"

    # Identifier
    IDENT = "IDENT"

    # Keywords
    KW_VOID = "void"
    KW_CHAR = "char"
    KW_INT = "int"
    KW_UNSIGNED = "unsigned"
    KW_SIGNED = "signed"
    KW_VOLATILE = "volatile"
    KW_CONST = "const"
    KW_STATIC = "static"
    KW_IF = "if"
    KW_ELSE = "else"
    KW_WHILE = "while"
    KW_FOR = "for"
    KW_DO = "do"
    KW_RETURN = "return"
    KW_BREAK = "break"
    KW_CONTINUE = "continue"
    KW_ASM = "asm"
    KW_SIZEOF = "sizeof"
    KW_TYPEDEF = "typedef"
    KW_STRUCT = "struct"
    KW_ENUM = "enum"

    # GCC-style attributes (used for __interrupt, __zeropage, etc.)
    KW_ATTRIBUTE = "__attribute__"
    KW_INTERRUPT = "__interrupt"
    KW_ZEROPAGE = "__zeropage"
    KW_PRAGMA = "#pragma"

    # Operators
    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"
    PERCENT = "%"
    AMP = "&"
    PIPE = "|"
    CARET = "^"
    TILDE = "~"
    LSHIFT = "<<"
    RSHIFT = ">>"
    BANG = "!"
    ASSIGN = "="
    PLUS_ASSIGN = "+="
    MINUS_ASSIGN = "-="
    STAR_ASSIGN = "*="
    SLASH_ASSIGN = "/="
    PERCENT_ASSIGN = "%="
    AMP_ASSIGN = "&="
    PIPE_ASSIGN = "|="
    CARET_ASSIGN = "^="
    LSHIFT_ASSIGN = "<<="
    RSHIFT_ASSIGN = ">>="
    EQ = "=="
    NEQ = "!="
    LT = "<"
    GT = ">"
    LE = "<="
    GE = ">="
    AND = "&&"
    OR = "||"
    INC = "++"
    DEC = "--"
    ARROW = "->"
    DOT = "."

    # Punctuation
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    LBRACKET = "["
    RBRACKET = "]"
    SEMI = ";"
    COMMA = ","
    COLON = ":"
    QUESTION = "?"
    ELLIPSIS = "..."

    # Special
    EOF = "EOF"


# ──────────────────────────────────────────────
# Token data class
# ──────────────────────────────────────────────

@dataclass
class Token:
    type: TokenType
    value: str | int
    line: int
    col: int

    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, L{self.line}:{self.col})"


# ──────────────────────────────────────────────
# Keyword map
# ──────────────────────────────────────────────

KEYWORDS: Dict[str, TokenType] = {
    "void": TokenType.KW_VOID,
    "char": TokenType.KW_CHAR,
    "int": TokenType.KW_INT,
    "unsigned": TokenType.KW_UNSIGNED,
    "signed": TokenType.KW_SIGNED,
    "volatile": TokenType.KW_VOLATILE,
    "const": TokenType.KW_CONST,
    "static": TokenType.KW_STATIC,
    "if": TokenType.KW_IF,
    "else": TokenType.KW_ELSE,
    "while": TokenType.KW_WHILE,
    "for": TokenType.KW_FOR,
    "do": TokenType.KW_DO,
    "return": TokenType.KW_RETURN,
    "break": TokenType.KW_BREAK,
    "continue": TokenType.KW_CONTINUE,
    "asm": TokenType.KW_ASM,
    "sizeof": TokenType.KW_SIZEOF,
    "typedef": TokenType.KW_TYPEDEF,
    "struct": TokenType.KW_STRUCT,
    "enum": TokenType.KW_ENUM,
    "__attribute__": TokenType.KW_ATTRIBUTE,
    "__interrupt": TokenType.KW_INTERRUPT,
    "__zeropage": TokenType.KW_ZEROPAGE,
}


# ──────────────────────────────────────────────
# Multi-char operator table (longest match first)
# ──────────────────────────────────────────────

MULTI_CHAR_OPS = [
    ("<<=", TokenType.LSHIFT_ASSIGN),
    (">>=", TokenType.RSHIFT_ASSIGN),
    ("...", TokenType.ELLIPSIS),
    ("<<", TokenType.LSHIFT),
    (">>", TokenType.RSHIFT),
    ("<=", TokenType.LE),
    (">=", TokenType.GE),
    ("==", TokenType.EQ),
    ("!=", TokenType.NEQ),
    ("&&", TokenType.AND),
    ("||", TokenType.OR),
    ("+=", TokenType.PLUS_ASSIGN),
    ("-=", TokenType.MINUS_ASSIGN),
    ("*=", TokenType.STAR_ASSIGN),
    ("/=", TokenType.SLASH_ASSIGN),
    ("%=", TokenType.PERCENT_ASSIGN),
    ("&=", TokenType.AMP_ASSIGN),
    ("|=", TokenType.PIPE_ASSIGN),
    ("^=", TokenType.CARET_ASSIGN),
    ("++", TokenType.INC),
    ("--", TokenType.DEC),
    ("->", TokenType.ARROW),
]

SINGLE_CHAR_OPS: Dict[str, TokenType] = {
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.STAR,
    "/": TokenType.SLASH,
    "%": TokenType.PERCENT,
    "&": TokenType.AMP,
    "|": TokenType.PIPE,
    "^": TokenType.CARET,
    "~": TokenType.TILDE,
    "!": TokenType.BANG,
    "=": TokenType.ASSIGN,
    "<": TokenType.LT,
    ">": TokenType.GT,
    ".": TokenType.DOT,
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    "{": TokenType.LBRACE,
    "}": TokenType.RBRACE,
    "[": TokenType.LBRACKET,
    "]": TokenType.RBRACKET,
    ";": TokenType.SEMI,
    ",": TokenType.COMMA,
    ":": TokenType.COLON,
    "?": TokenType.QUESTION,
}


# ──────────────────────────────────────────────
# Minimal Preprocessor
# ──────────────────────────────────────────────

class Preprocessor:
    """Resolve #define macros and strip #include / #pragma lines."""

    def __init__(self, source: str):
        self.source = source
        self.defines: Dict[str, str] = {}

    def process(self) -> str:
        out_lines: List[str] = []
        for line in self.source.splitlines():
            stripped = line.strip()

            # #define NAME value
            m = re.match(r'#\s*define\s+(\w+)\s+(.*)', stripped)
            if m:
                name, value = m.group(1), m.group(2).strip()
                self.defines[name] = value
                out_lines.append("")  # keep line numbering
                continue

            # #define NAME (no value) -> treat as 1
            m = re.match(r'#\s*define\s+(\w+)\s*$', stripped)
            if m:
                self.defines[m.group(1)] = "1"
                out_lines.append("")
                continue

            # #include — skip (headers handled externally)
            if re.match(r'#\s*include\b', stripped):
                out_lines.append("")
                continue

            # #ifndef / #ifdef / #endif — skip (basic guard stripping)
            if re.match(r'#\s*(ifndef|ifdef|endif|else|if|elif|undef)\b', stripped):
                out_lines.append("")
                continue

            # #pragma — emit as-is for codegen to inspect later
            if stripped.startswith("#pragma"):
                out_lines.append(line)
                continue

            # Substitute defines in the line (whole-word replacement)
            for name, value in self.defines.items():
                line = re.sub(rf'\b{re.escape(name)}\b', value, line)

            out_lines.append(line)

        return "\n".join(out_lines)


# ──────────────────────────────────────────────
# Lexer
# ──────────────────────────────────────────────

class LexerError(Exception):
    def __init__(self, message: str, line: int, col: int):
        self.line = line
        self.col = col
        super().__init__(f"Lexer error at L{line}:{col}: {message}")


class Lexer:
    """Tokenizes preprocessed C source into a list of Tokens."""

    def __init__(self, source: str, preprocess: bool = True):
        if preprocess:
            pp = Preprocessor(source)
            self.source = pp.process()
            self.defines = pp.defines
        else:
            self.source = source
            self.defines = {}
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens: List[Token] = []

    def _peek(self, offset: int = 0) -> str:
        i = self.pos + offset
        return self.source[i] if i < len(self.source) else "\0"

    def _advance(self) -> str:
        ch = self.source[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def _match(self, expected: str) -> bool:
        if self.source[self.pos:self.pos + len(expected)] == expected:
            for _ in expected:
                self._advance()
            return True
        return False

    def _skip_whitespace(self):
        while self.pos < len(self.source) and self.source[self.pos] in " \t\r\n":
            self._advance()

    def _skip_line_comment(self):
        while self.pos < len(self.source) and self.source[self.pos] != "\n":
            self._advance()

    def _skip_block_comment(self):
        while self.pos < len(self.source) - 1:
            if self.source[self.pos] == "*" and self.source[self.pos + 1] == "/":
                self._advance()  # *
                self._advance()  # /
                return
            self._advance()
        raise LexerError("Unterminated block comment", self.line, self.col)

    def _read_number(self) -> Token:
        start_line, start_col = self.line, self.col
        start_pos = self.pos

        # Hex: 0x...
        if self.source[self.pos] == "0" and self.pos + 1 < len(self.source) and self.source[self.pos + 1] in "xX":
            self._advance()  # '0'
            self._advance()  # 'x'
            while self.pos < len(self.source) and self.source[self.pos] in "0123456789abcdefABCDEF_":
                self._advance()
            text = self.source[start_pos:self.pos].replace("_", "")
            return Token(TokenType.INT_LITERAL, int(text, 16), start_line, start_col)

        # Binary: 0b...
        if self.source[self.pos] == "0" and self.pos + 1 < len(self.source) and self.source[self.pos + 1] in "bB":
            self._advance()  # '0'
            self._advance()  # 'b'
            while self.pos < len(self.source) and self.source[self.pos] in "01_":
                self._advance()
            text = self.source[start_pos:self.pos].replace("_", "")
            return Token(TokenType.INT_LITERAL, int(text, 2), start_line, start_col)

        # Octal: 0...
        if self.source[self.pos] == "0" and self.pos + 1 < len(self.source) and self.source[self.pos + 1] in "01234567":
            self._advance()  # '0'
            while self.pos < len(self.source) and self.source[self.pos] in "01234567":
                self._advance()
            text = self.source[start_pos:self.pos]
            return Token(TokenType.INT_LITERAL, int(text, 8), start_line, start_col)

        # Decimal
        while self.pos < len(self.source) and self.source[self.pos].isdigit():
            self._advance()

        # Skip unsigned/long suffixes: u, U, l, L, ul, UL, etc.
        while self.pos < len(self.source) and self.source[self.pos] in "uUlL":
            self._advance()

        text = self.source[start_pos:self.pos].rstrip("uUlL")
        return Token(TokenType.INT_LITERAL, int(text), start_line, start_col)

    def _read_char_literal(self) -> Token:
        start_line, start_col = self.line, self.col
        self._advance()  # opening '
        if self._peek() == "\\":
            self._advance()  # backslash
            escape = self._advance()
            escape_map = {"n": 10, "r": 13, "t": 9, "0": 0, "\\": 92, "'": 39}
            value = escape_map.get(escape, ord(escape))
        else:
            value = ord(self._advance())

        if self._peek() != "'":
            raise LexerError("Unterminated character literal", self.line, self.col)
        self._advance()  # closing '
        return Token(TokenType.CHAR_LITERAL, value, start_line, start_col)

    def _read_string_literal(self) -> Token:
        start_line, start_col = self.line, self.col
        self._advance()  # opening "
        chars: List[str] = []
        while self.pos < len(self.source) and self._peek() != '"':
            if self._peek() == "\\":
                self._advance()
                esc = self._advance()
                escape_map = {"n": "\n", "r": "\r", "t": "\t", "0": "\0", "\\": "\\", '"': '"'}
                chars.append(escape_map.get(esc, esc))
            else:
                chars.append(self._advance())
        if self.pos >= len(self.source):
            raise LexerError("Unterminated string literal", start_line, start_col)
        self._advance()  # closing "
        return Token(TokenType.STRING_LITERAL, "".join(chars), start_line, start_col)

    def _read_identifier_or_keyword(self) -> Token:
        start_line, start_col = self.line, self.col
        start_pos = self.pos

        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == "_"):
            self._advance()

        text = self.source[start_pos:self.pos]

        # __attribute__ special handling
        if text == "__attribute__":
            return Token(TokenType.KW_ATTRIBUTE, text, start_line, start_col)

        if text in KEYWORDS:
            return Token(KEYWORDS[text], text, start_line, start_col)

        return Token(TokenType.IDENT, text, start_line, start_col)

    def tokenize(self) -> List[Token]:
        """Tokenize the entire source and return a list of tokens."""
        self.tokens = []

        while self.pos < len(self.source):
            self._skip_whitespace()
            if self.pos >= len(self.source):
                break

            ch = self._peek()

            # Line comment
            if ch == "/" and self._peek(1) == "/":
                self._skip_line_comment()
                continue

            # Block comment
            if ch == "/" and self._peek(1) == "*":
                self._advance()
                self._advance()
                self._skip_block_comment()
                continue

            # Pragma lines (pass through as special token)
            if ch == "#":
                # Skip preprocessor lines that survived preprocessing
                start_line, start_col = self.line, self.col
                line_start = self.pos
                while self.pos < len(self.source) and self.source[self.pos] != "\n":
                    self._advance()
                # Just skip — preprocessor already handled
                continue

            # Number
            if ch.isdigit():
                self.tokens.append(self._read_number())
                continue

            # Character literal
            if ch == "'":
                self.tokens.append(self._read_char_literal())
                continue

            # String literal
            if ch == '"':
                self.tokens.append(self._read_string_literal())
                continue

            # Identifier or keyword
            if ch.isalpha() or ch == "_":
                self.tokens.append(self._read_identifier_or_keyword())
                continue

            # Multi-character operators
            matched = False
            for op_str, op_type in MULTI_CHAR_OPS:
                if self.source[self.pos:self.pos + len(op_str)] == op_str:
                    start_line, start_col = self.line, self.col
                    for _ in op_str:
                        self._advance()
                    self.tokens.append(Token(op_type, op_str, start_line, start_col))
                    matched = True
                    break

            if matched:
                continue

            # Single-character operators and punctuation
            if ch in SINGLE_CHAR_OPS:
                start_line, start_col = self.line, self.col
                self._advance()
                self.tokens.append(Token(SINGLE_CHAR_OPS[ch], ch, start_line, start_col))
                continue

            # Unknown character
            raise LexerError(f"Unexpected character: {ch!r}", self.line, self.col)

        self.tokens.append(Token(TokenType.EOF, "", self.line, self.col))
        return self.tokens
