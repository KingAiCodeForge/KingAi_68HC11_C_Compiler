"""
KingAI 68HC11 C Compiler for Delco PCMs
========================================
A subset-C compiler targeting the Motorola 68HC11 microcontroller,
designed for Delco automotive Powertrain Control Modules (PCMs).

Supports: VY V6 (09356445), 1227165, 1227730, 16197427 and compatible PCMs.
"""

__version__ = "0.2.0"
__author__ = "KingAI"

from .lexer import Lexer, Token, TokenType
from .ast_nodes import *
from .parser import Parser
from .codegen import CodeGenerator

def compile_source(source: str, *, org: int = 0x8000, stack: int = 0x00FF,
                   target: str = "generic") -> str:
    """Compile C source code to 68HC11 assembly.

    Args:
        source: C source code string.
        org: Origin address for code placement (default $8000).
        stack: Initial stack pointer value (default $00FF).
        target: Target PCM profile ('generic', 'vy_v6', '1227730', '16197427').

    Returns:
        68HC11 assembly source as a string.
    """
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens, source)
    ast = parser.parse()
    gen = CodeGenerator(org=org, stack=stack, target=target)
    return gen.generate(ast)
