# KingAI HC11 disassembler reference qualification — 22 October 2026

**Status: isolated offline engineering review; not an ECU/runtime or hardware qualification.**

## Target
Preserve existing `hc11kit` behavior while adding a strict, read-only Motorola 68HC11 disassembler, using exact opcode-length and addressing-mode tests. Do not silently assume VY bank semantics for VS/VT variants. Separate linear listings (ambiguous code/data) from seed-driven CFG reachability, and report out-of-window/indirect edges rather than inventing their destinations.

## Five independent comparison families
1. Motorola/Freescale M68HC11 Reference Manual Rev 6.1, Appendix A: https://www.nxp.com/docs/en/reference-manual/M68HC11RM.pdf — primary instruction semantics.
2. Freescale M68HC11E Programming Reference Guide: https://www.nxp.com/docs/en/reference-manual/M68HC11ERG.pdf — supplemental opcode and addressing-mode checks.
3. GNU binutils m68hc11 opcode sources: https://sources.debian.org/src/binutils/2.43.1-5/opcodes/m68hc11-opc.c — external comparison only; GPL source not imported into this MIT project.
4. Ghidra HC11 SLEIGH: https://github.com/GaryOderNichts/ghidra-hc11-lang/blob/main/data/languages/HC11.slaspec — independently extracted 307 documented encoding identities (232 base / 64 page $18 / 7 page $1A / 4 page $CD).
5. dis68hc11: https://github.com/cmdrf/dis68hc11 — historical comparison only; its upstream README admits incomplete multibyte-opcode coverage.

## Established faults in retained code
- Existing `hc11kit.py` misses multiple valid $18 indexed-Y operations, including $18 A9 ADCA and $18 E9 ADCB.
- Historical `hc11_opcodes_complete.py` treats $00 as undocumented TEST; do not promote it to the documented opcode inventory without target-specific evidence.
- Legacy `dis68hc11/Opcodes.h` reverses immediate and direct labels for some ADCA/ADCB entries. That source is not controlling authority.

## Verification standard and boundaries
- Compare independent reference table by exact (page, opcode, mnemonic, addressing mode, instruction byte length), not only mnemonic names. Reject truncation and illegal prefix combinations.
- Admit private VS $51 firmware by exact SHA-256 and length; **never commit firmware, XDFs, BINs or data derived from customer secrets**.
- Test branch relative offset signedness and bit-branch displacement, $18/$1A/$CD prefix decoding, bank aliasing, invalid/truncated cases and overlap/refusal behaviour.
- Require local normal and `python -O` tests. **Do not use GitHub Actions** in this repository.
- Keep native Ghidra listing parity, all dynamic bank selection, indirect targets, real interrupt reachability and physical timing unproved until separately tested.

This document is the first provenance commit; source/test/receipt artifacts are staged for separate commits and Git readback on this review branch.
