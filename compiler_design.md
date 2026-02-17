# 68HC11 C Compiler for Delco PCMs — Design Specification

> **Last updated:** February 2026
> **Status:** Alpha — full C → ASM → binary pipeline working, 74/74 tests passing

## 1. Introduction

This document describes the design and architecture of a subset-C cross-compiler targeting the Motorola 68HC11 microcontroller, built specifically for Delco automotive Powertrain Control Modules (PCMs). The compiler generates efficient, low-level code for the resource-constrained ECU environment, with features for direct hardware manipulation including memory-mapped I/O, interrupt handling, and precise control over memory layout.

## 2. Target Architecture: Motorola 68HC11

The compiler generates assembly code for the 68HC11 instruction set. Key architectural features:

| Feature | Description |
| :--- | :--- |
| **CPU Registers** | 8-bit accumulators (A, B), 16-bit combined accumulator (D), 16-bit index registers (X, Y), stack pointer (SP), program counter (PC). |
| **Memory Model** | Flat 64KB address space with support for 128KB bank-switched ROMs (VY V6). Zero-page RAM ($0000–$00FF) for fast 8-bit direct addressing. |
| **Instruction Set** | Full 68HC11 instruction set — 146 mnemonics, 261 opcode entries across 4 pages (base + $18/$1A/$CD prebytes). |
| **Addressing Modes** | Direct, extended, immediate, indexed (X and Y), relative, inherent, and bit-manipulation modes. |

## 3. Compiler Features

The compiler supports a practical subset of ANSI C with embedded extensions.

### 3.1. Data Types

Supported fundamental data types:

| Data Type | Size | Range |
| :--- | :--- | :--- |
| `char` | 8 bits | -128 to 127 |
| `unsigned char` | 8 bits | 0 to 255 |
| `int` | 16 bits | -32,768 to 32,767 |
| `unsigned int` | 16 bits | 0 to 65,535 |
| `void *` | 16 bits | 0x0000 to 0xFFFF |

### 3.2. Memory Management

- **Stack**: User-configurable initial stack pointer location. All function calls use the hardware stack for arguments and local variables.
- **RAM Allocation**: The `__zeropage` qualifier allocates variables in direct-page RAM ($00–$FF) for faster access using 8-bit direct addressing instead of 16-bit extended addressing.

### 3.3. Low-Level Programming Extensions

- **Inline Assembly**: GCC-style `asm("...")` statements embed raw HC11 instructions directly in C code. Essential for performance-critical sections and direct hardware control.
- **Interrupt Service Routines (ISRs)**: `__attribute__((interrupt))` generates proper RTI epilogue with register save/restore.
- **Memory-Mapped I/O**: Volatile pointers (`*(volatile unsigned char *)0x1030`) access hardware registers without compiler optimization interference.

## 4. Compiler Architecture

The compiler uses a traditional multi-pass architecture, implemented entirely in Python:

1. **Lexer** (`lexer.py`, ~498 lines) — Tokenizes C source into a stream of typed tokens (keywords, identifiers, operators, literals).
2. **Parser** (`parser.py`, ~656 lines) — Recursive-descent parser that builds an Abstract Syntax Tree (AST). No external tools (flex/bison) — hand-written for full control.
3. **AST** (`ast_nodes.py`, ~267 lines) — Node definitions for all supported C constructs.
4. **Code Generator** (`codegen.py`, ~1325 lines) — Translates AST directly to HC11 assembly. Handles instruction selection, register allocation (AccA for 8-bit, AccD for 16-bit), and addressing mode selection.
5. **Peephole Optimizer** (`optimizer.py`, ~170 lines) — 13 post-codegen rules that clean up redundant instructions (TSX dedup, push/pop elimination, dead TSTA removal, `while(1)` optimization).
6. **Built-in Assembler** (`assembler.py`, ~1037 lines) — Two-pass assembler handling 146 mnemonics and 261 opcode entries. Outputs raw binary, Motorola S19, and listing files. No external assembler required.

## 5. Implementation Status

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 — Core infrastructure | Lexer, parser, basic AST | **Complete** |
| Phase 2 — Basic expressions | 8-bit and 16-bit arithmetic codegen | **Complete** |
| Phase 3 — Control flow | `if/else`, `while`, `for`, `do-while`, `break`, `continue` | **Complete** |
| Phase 4 — Functions & stack | JSR/RTS, argument passing, local variables | **Complete** |
| Phase 5 — Pointers & I/O | Pointer dereference, address-of, volatile I/O | **Complete** |
| Phase 6 — Embedded extensions | Inline assembly, ISR support, `__zeropage` | **Complete** |
| Phase 7 — Built-in assembler | Two-pass assembler, S19 + binary output | **Complete** |
| Phase 8 — ROM patcher (`hc11kit`) | Code injection, JSR hook install, checksum fix | **Complete** |
| Phase 9 — Arrays & structs | Parser handles them; codegen in progress | **In progress** |
| Phase 10 — Hardware validation | Test on real ECU with oscilloscope | **Pending** |

74/74 tests passing. ~5,200 lines of compiler + toolkit code.
