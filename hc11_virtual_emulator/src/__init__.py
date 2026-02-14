# HC11 Virtual Emulator — Pure-software 68HC11 CPU simulator
# Part of KingAI 68HC11 C Compiler toolchain
#
# SCAFFOLD STATUS: Headers and structure defined. Implementation needs
# cross-referencing against:
#   - tonypdmtr/EVBU (PySim11) — Python HC11 simulator (GPL-2.0)
#   - GDB sim/m68hc11 — GNU simulator (C, validation oracle)
#   - Motorola MC68HC11 Reference Manual Rev3 (opcode definitions)
#   - hc11_compiler/assembler.py — our own opcode table (313 entries)
#
# Each module below is scaffold — the class signatures and docstrings
# are defined, but instruction handlers need validation byte-for-byte
# against known-good emulators before being marked production-ready.
