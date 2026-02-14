#!/usr/bin/env python3
"""
hc11cc — KingAI 68HC11 C Compiler CLI

Usage:
    python hc11cc.py <input.c> [-o output.asm] [--target vy_v6|1227730|16197427|generic]
                                [--org 0x8000] [--stack 0x00FF] [--verbose]

Output format is auto-detected from file extension:
    .asm / .s  → assembly text (default)
    .s19       → Motorola S19 (burnable)
    .bin       → raw binary
    .lst       → assembly listing with addresses and hex bytes

Examples:
    python hc11cc.py main.c -o main.s19 --target vy_v6
    python hc11cc.py blink.c -o blink.bin --target 1227730
    python hc11cc.py blink.c -o blink.lst --verbose
    python hc11cc.py test.c                          # generic target, asm to stdout
"""

import argparse
import sys
import os

# Fix stdout encoding on Windows (box-drawing chars in assembly comments)
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ('utf-8', 'utf8'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        pass  # Python < 3.7

# Allow running from project root or as module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hc11_compiler import compile_source
from hc11_compiler.lexer import Lexer, LexerError
from hc11_compiler.parser import Parser, ParseError
from hc11_compiler.codegen import CodeGenError, TARGET_PROFILES
from hc11_compiler.assembler import AssemblerError


def parse_int_arg(value: str) -> int:
    """Parse an integer argument that may be hex (0x...), $ prefix, or decimal."""
    value = value.strip()
    if value.startswith("0x") or value.startswith("0X"):
        return int(value, 16)
    if value.startswith("$"):
        return int(value[1:], 16)  # Motorola hex convention
    return int(value)


def main():
    parser = argparse.ArgumentParser(
        prog="hc11cc",
        description="KingAI 68HC11 C Compiler for Delco PCMs",
        epilog="Targets: " + ", ".join(TARGET_PROFILES.keys()),
    )
    parser.add_argument("input", help="Input C source file")
    parser.add_argument("-o", "--output", help="Output assembly file (default: stdout)")
    parser.add_argument("--target", default="generic",
                        choices=list(TARGET_PROFILES.keys()),
                        help="Target PCM profile (default: generic)")
    parser.add_argument("--org", default=None,
                        help="Code origin address (hex, e.g. 0x8000)")
    parser.add_argument("--stack", default=None,
                        help="Initial stack pointer (hex, e.g. 0x00FF)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Print compilation details to stderr")
    parser.add_argument("--tokens", action="store_true",
                        help="Dump token stream and exit (debug)")
    parser.add_argument("--ast", action="store_true",
                        help="Dump AST and exit (debug)")
    parser.add_argument("--version", action="version",
                        version="hc11cc 0.3.0 (KingAI)")
    parser.add_argument("--format", choices=["asm", "s19", "bin", "listing"],
                        default=None,
                        help="Output format (auto-detected from -o extension if not set)")

    args = parser.parse_args()

    # Read input
    try:
        with open(args.input, "r", encoding="utf-8") as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Error reading {args.input}: {e}", file=sys.stderr)
        sys.exit(1)

    # Determine org and stack from target profile, allow CLI overrides
    profile = TARGET_PROFILES.get(args.target, TARGET_PROFILES["generic"])
    org = parse_int_arg(args.org) if args.org else profile["org"]
    stack = parse_int_arg(args.stack) if args.stack else profile["stack"]

    if args.verbose:
        print(f"[hc11cc] Input:  {args.input}", file=sys.stderr)
        print(f"[hc11cc] Target: {args.target} — {profile['description']}", file=sys.stderr)
        print(f"[hc11cc] ORG:    ${org:04X}", file=sys.stderr)
        print(f"[hc11cc] Stack:  ${stack:04X}", file=sys.stderr)

    try:
        # Token dump mode
        if args.tokens:
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            for tok in tokens:
                print(tok)
            sys.exit(0)

        # AST dump mode
        if args.ast:
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            p = Parser(tokens, source)
            ast = p.parse()
            _print_ast(ast)
            sys.exit(0)

        # Determine output format from --format flag, file extension, or default to asm
        if args.format:
            out_format = args.format
        elif args.output:
            ext = os.path.splitext(args.output)[1].lower()
            if ext == '.s19':
                out_format = 's19'
            elif ext == '.bin':
                out_format = 'binary'
            elif ext == '.lst':
                out_format = 'listing'
            else:
                out_format = 'asm'
        else:
            out_format = 'asm'

        # Full compilation
        result = compile_source(source, org=org, stack=stack,
                                target=args.target, output=out_format)

        # Write output
        if args.output:
            if out_format == 'binary':
                with open(args.output, "wb") as f:
                    f.write(result)
            else:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(result)
                    if not result.endswith('\n'):
                        f.write("\n")
            if args.verbose:
                print(f"[hc11cc] Output: {args.output} ({out_format})", file=sys.stderr)
                if out_format in ('binary', 's19'):
                    size = len(result) if out_format == 'binary' else 0
                    print(f"[hc11cc] Binary size: {size} bytes", file=sys.stderr)
        else:
            if out_format == 'binary':
                # Can't write raw bytes to stdout in text mode
                sys.stdout.buffer.write(result)
            else:
                print(result)

        if args.verbose:
            if out_format == 'asm':
                line_count = result.count("\n") + 1
                print(f"[hc11cc] Generated {line_count} lines of assembly", file=sys.stderr)

    except LexerError as e:
        print(f"Lexer error: {e}", file=sys.stderr)
        sys.exit(1)
    except ParseError as e:
        print(f"Parse error: {e}", file=sys.stderr)
        sys.exit(1)
    except CodeGenError as e:
        print(f"Code generation error: {e}", file=sys.stderr)
        sys.exit(1)
    except AssemblerError as e:
        print(f"Assembler error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Internal compiler error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(2)


def _print_ast(node, indent=0):
    """Pretty-print an AST node tree (debug helper)."""
    prefix = "  " * indent
    if hasattr(node, '__dataclass_fields__'):
        print(f"{prefix}{type(node).__name__}:")
        for fname, fval in node.__dataclass_fields__.items():
            val = getattr(node, fname)
            if isinstance(val, list):
                print(f"{prefix}  {fname}:")
                for item in val:
                    _print_ast(item, indent + 2)
            elif hasattr(val, '__dataclass_fields__'):
                print(f"{prefix}  {fname}:")
                _print_ast(val, indent + 2)
            elif val is not None:
                print(f"{prefix}  {fname}: {val}")
    else:
        print(f"{prefix}{node}")


if __name__ == "__main__":
    main()
