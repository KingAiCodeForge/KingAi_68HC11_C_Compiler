"""
KingAI 68HC11 C Compiler for Delco PCMs
========================================
A subset-C compiler targeting the Motorola 68HC11 microcontroller,
designed for Delco automotive Powertrain Control Modules (PCMs).

Supports: VY V6 (09356445), 1227165, 1227730, 16197427 and compatible PCMs.

Architecture (for contributors / porters to other languages):
    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌───────────┐    ┌───────────┐
    │ C Source │───>│  Lexer   │───>│  Parser  │───>│  CodeGen  │───>│ Assembler │
    │ (.c)     │    │ (tokens) │    │  (AST)   │    │ (asm text)│    │ (bin/s19) │
    └──────────┘    └──────────┘    └──────────┘    └───────────┘    └───────────┘

    Each stage is independent and can be replaced:
    - lexer.py:     Regex-based tokenizer → swap for your language's scanner
    - parser.py:    Recursive descent → any LL/LR parser works
    - ast_nodes.py: Dataclass tree → use structs/records/interfaces in your lang
    - codegen.py:   Tree-walk emitter → retarget by changing mnemonics + registers
    - optimizer.py: Peephole on text lines → same pattern works on any asm output
    - assembler.py: Two-pass label resolver → port opcode table for your CPU
    - objectfile.py: K11O relocatable translation-unit container
    - resource_map.py: collision-checked ROM/RAM/ZP allocation
    - linker.py: multi-object symbol/resource linker
"""

__version__ = "0.4.0"
__author__ = "KingAI"

from .lexer import Lexer, Token, TokenType
from .ast_nodes import *
from .parser import Parser
from .codegen import CodeGenerator
from .assembler import Assembler, AssemblerError, assemble, assemble_to_s19
from .objectfile import (
    KCOS_ABI, OBJECT_MAGIC, OBJECT_VERSION, ObjectFormatError,
    ObjectSymbol, RelocatableObject, compile_asm_object, compile_kcos_module, compile_object,
)
from .resource_map import (
    Allocation, MemoryRegion, ResourceCollisionError, ResourceMap, ResourceMapError,
)

def compile_source(source: str, *, org: int = 0x8000, stack: int = 0x00FF,
                   target: str = "generic", output: str = "asm") -> str:
    """Compile C source code to 68HC11 assembly, binary, S19, or listing.

    Full pipeline: Lexer -> Parser -> AST -> CodeGenerator -> Assembler.

    Args:
        source: C source code string.
        org: Origin address for code placement (default $8000).
        stack: Initial stack pointer value (default $00FF).
        target: Target PCM profile ('generic', 'vy_v6', '1227730', '16197427').
        output: Output format — 'asm' (default), 's19', 'binary', or 'listing'.

    Returns:
        Assembly text (str), S19 text (str), listing text (str),
        or raw bytes (bytes) depending on output.
    """
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens, source)
    ast = parser.parse()
    gen = CodeGenerator(org=org, stack=stack, target=target)
    asm_text = gen.generate(ast)

    if output == 'asm':
        return asm_text

    # Assemble to binary, S19, or listing
    assembler = Assembler()
    assembler.assemble(asm_text)

    if output == 's19':
        return assembler.to_s19()
    elif output == 'binary':
        return bytes(assembler.binary)
    elif output == 'listing':
        return assembler.get_listing()
    else:
        return asm_text


def link_objects(objects, *, resource_map=None):
    """Lazy public wrapper to avoid an import cycle at package import time."""
    from .linker import link_objects as _link_objects
    return _link_objects(objects, resource_map=resource_map)


def link_sources(sources, *, target="generic", resource_map=None):
    """Compile named translation units and link them into one image."""
    from .linker import link_sources as _link_sources
    return _link_sources(sources, target=target, resource_map=resource_map)
