# 68HC11 C Compiler for Delco PCMs - Design Specification

## 1. Introduction

This document outlines the design and architecture for a C compiler targeting the Motorola 68HC11 microcontroller, with a specific focus on its application within Delco automotive Powertrain Control Modules (PCMs). The compiler will prioritize generating efficient, low-level code suitable for the resource-constrained environment of these ECUs. It will provide features for direct hardware manipulation, including memory-mapped I/O, interrupt handling, and precise control over memory layout.

## 2. Target Architecture: Motorola 68HC11

The compiler will generate assembly code for the 68HC11 instruction set. Key architectural features to be supported are summarized in the table below.

| Feature | Description |
| :--- | :--- |
| **CPU Registers** | The compiler will manage the 8-bit accumulators (A, B), 16-bit combined accumulator (D), 16-bit index registers (X, Y), stack pointer (SP), and program counter (PC). |
| **Memory Model** | A single, flat 64KB address space will be assumed. The compiler will support placing data in the faster, zero-page RAM ($0000-$00FF) for performance optimization. |
| **Instruction Set** | The compiler will leverage the full 68HC11 instruction set, including arithmetic, logical, bit-manipulation, and branching instructions. |
| **Addressing Modes** | Support for direct, extended, and indexed addressing modes will be implemented to generate efficient code for data access. |

## 3. Compiler Features

The compiler will support a subset of the ANSI C standard, with extensions for embedded programming.

### 3.1. Data Types

The following fundamental data types will be supported:

| Data Type | Size | Range |
| :--- | :--- | :--- |
| `char` | 8 bits | -128 to 127 |
| `unsigned char` | 8 bits | 0 to 255 |
| `int` | 16 bits | -32,768 to 32,767 |
| `unsigned int` | 16 bits | 0 to 65,535 |
| `void *` | 16 bits | 0x0000 to 0xFFFF |

### 3.2. Memory Management

- **Stack**: The compiler will allow the user to define the initial stack pointer location. All function calls will use the hardware stack for passing arguments and storing local variables.
- **RAM Allocation**: The compiler will provide a mechanism to explicitly place variables in the zero-page for faster access, using a custom keyword or pragma (e.g., `__attribute__((zero_page))`).

### 3.3. Low-Level Programming Extensions

- **Inline Assembly**: A GCC-style `asm()` statement will be supported to allow embedding raw 68HC11 assembly instructions directly within C code. This is essential for performance-critical sections and direct hardware control.
- **Interrupt Service Routines (ISRs)**: A custom function attribute (e.g., `__attribute__((interrupt))`) will be used to declare interrupt handlers. The compiler will automatically generate the correct prologue and epilogue for ISRs, including saving and restoring registers and using the `RTI` (Return from Interrupt) instruction.
- **Memory-Mapped I/O**: Volatile pointers will be used to access memory-mapped I/O registers, preventing the compiler from optimizing away necessary reads and writes.

## 4. Compiler Architecture

The compiler will be designed with a traditional multi-pass architecture:

1.  **Frontend (Parser & Lexer)**: This stage will parse the C source code into an Abstract Syntax Tree (AST). We will use a standard tool like `flex` and `bison` to generate the lexer and parser.
2.  **Semantic Analyzer**: This pass will traverse the AST to perform type checking and other semantic analysis, ensuring the code is well-formed.
3.  **Intermediate Representation (IR) Generator**: The AST will be translated into a simpler, three-address code intermediate representation.
4.  **Code Generator (Backend)**: The IR will be translated into 68HC11 assembly code. This is the most critical and complex part of the compiler, involving instruction selection, register allocation, and optimization.
5.  **Assembler & Linker**: The generated assembly code will be processed by an external assembler (like `as11`) and linker to produce the final executable binary.

## 5. Implementation Plan

The development will proceed in the following phases:

1.  **Phase 1: Core Compiler Infrastructure**: Set up the basic project structure, build system, and implement the frontend (lexer and parser) to recognize a small subset of C.
2.  **Phase 2: Code Generation for Basic Expressions**: Implement the backend to generate assembly for simple arithmetic and logical expressions.
3.  **Phase 3: Control Flow**: Add support for `if`, `else`, `for`, and `while` statements.
4.  **Phase 4: Functions and Stack Management**: Implement function calls, argument passing, and local variable allocation on the stack.
5.  **Phase 5: Pointers and Memory Access**: Add support for pointers and memory-mapped I/O.
6.  **Phase 6: Embedded Extensions**: Implement inline assembly and interrupt handling.

This phased approach will allow for incremental development and testing, ensuring a solid foundation before moving to more complex features.
