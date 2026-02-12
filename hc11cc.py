#!/usr/bin/env python3
"""
hc11cc — KingAI 68HC11 C Compiler CLI

Usage:
    python hc11cc.py <input.c> [-o output.asm] [--target vy_v6|1227730|16197427|generic]
                                [--org 0x8000] [--stack 0x00FF] [--verbose]

Examples:
    python hc11cc.py main.c -o main.asm --target vy_v6
    python hc11cc.py blink.c --target 1227730 --verbose
    python hc11cc.py test.c                          # generic target, stdout output
"""

import argparse
import sys
import os

# Allow running from project root or as module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hc11_compiler import compile_source
from hc11_compiler.lexer import Lexer, LexerError
from hc11_compiler.parser import Parser, ParseError
from hc11_compiler.codegen import CodeGenError, TARGET_PROFILES


def parse_int_arg(value: str) -> int:
    """Parse an integer argument that may be hex (0x...) or decimal."""
    value = value.strip()
    if value.startswith("0x") or value.startswith("0X"):
        return int(value, 16)
    if value.startswith("$"):
        return int(value[1:], 16)
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
                        version="hc11cc 0.2.0 (KingAI)")

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

    # Determine org and stack
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

        # Full compilation
        asm_output = compile_source(source, org=org, stack=stack, target=args.target)

        # Write output
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(asm_output)
                f.write("\n")
            if args.verbose:
                print(f"[hc11cc] Output: {args.output}", file=sys.stderr)
        else:
            print(asm_output)

        if args.verbose:
            line_count = asm_output.count("\n") + 1
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
