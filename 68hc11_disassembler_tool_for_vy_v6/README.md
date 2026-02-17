# 68HC11 Disassembler & Binary Analysis Tools — VY V6

> **Date added:** 16 February 2026  
> **Status:** Working copies — local backups with paths adjusted for this folder

## What This Is

These are **working versions** of disassembler, binary analysis, patching, and
reverse-engineering tools copied from local/ignored files across other GitHub
repos (primarily `VY_V6_Assembly_Modding/tools`, which alone has 200+ working niche scripts). This is a curated subset of the most useful ones, relocated here while in working form. Quality-of-life improvements and potential frontend integration are planned.

They are placed here for two reasons:

1. **Backup** — the originals live in `.gitignore`d or local-only directories
   that aren't pushed. Having a copy here means they survive repo cleanups.
2. **Convenience** — no more scrolling through 1000 folders to find the right
   tool. Everything compiler/disassembly related is now co-located with the
   C compiler project.

## Path Policy

Scripts are being updated so that **all file paths are relative to this folder**
(or accept paths as CLI arguments). This means anyone cloning the repo can run
them without editing hardcoded paths.

Some scripts still have hardcoded `A:\repos\...` paths from the original
locations — these are being progressively cleaned up. If a script doesn't work
out of the box, check for hardcoded paths first.

### Scripts with remaining hardcoded paths (as of 16/02/2026)

| File | Refs | Notes |
|------|------|-------|
| `hc11_disassembler.py` | 12 | Main disassembler — most paths |
| `hc11_disassembler_060a_enhanced_v1.py` | 12 | $060A-specific variant |
| `hc11_disassembler_enhanced.py` | 5 | Enhanced variant |
| `disassemble_hc11.py` | 1 | |
| `full_binary_disassembler.py` | 1 | |
| `hc11_pattern_analyzer.py` | 1 | |
| `memory_map_analyzer.py` | 1 | |
| `split_and_disassemble.py` | 1 | |
| `ultimate_binary_analyzer.py` | 1 | |
| `xdf_full_parser.py` | 1 | |
| `core/analyze_bank_switching.py` | 3 | |
| `core/analyze_interrupts_v2.py` | 1 | |
| `core/hc11_disassembler.py` | 2 | |
| `core/validate_ignition_cut_patch.py` | 2 | |
| `core/vy_v6_constants.py` | 6 | |

## Upstream / Canonical Versions

The **canonical (actively developed) versions** of these tools live in:

- **`VY_V6_Assembly_Modding/`** — the primary repo with 200+ scripts covering
  disassembly, patching, analysis, XDF work, ALDL, Mode 4, and more.
- **`kingaustraliagg-vy-l36-060a-enhanced-asm-patches`** — the GitHub-pushed
  companion repo with ASM patches and binary analysis docs.

Variants that are more relevant to the **compiler side** of the project will be
pushed here. General-purpose disassembly/analysis enhancements will continue
to be developed in the upstream repos and synced here as needed.

## Tool Inventory

### Top-Level Scripts (19 files)

| Script | Size | Purpose |
|--------|------|---------|
| `hc11_disassembler.py` | 89 KB | Full-featured HC11 disassembler |
| `hc11_disassembler_060a_enhanced_v1.py` | 91 KB | $060A Enhanced binary specific |
| `ultimate_binary_analyzer.py` | 80 KB | Comprehensive binary analysis suite |
| `hc11_complete_binary_mapper.py` | 37 KB | Complete memory region mapper |
| `hc11_opcodes_complete.py` | 32 KB | Full HC11 opcode table |
| `hc11_subroutine_reverse_engineer.py` | 30 KB | Subroutine identification & call graph |
| `hc11_disassembler_enhanced.py` | 28 KB | Enhanced disassembly with annotations |
| `full_binary_disassembler.py` | 25 KB | Full binary linear disassembly |
| `hc11_disassembler_batch.py` | 25 KB | Batch disassembly of multiple bins |
| `split_and_disassemble.py` | 23 KB | Split banked ROMs and disassemble |
| `hc11_pattern_analyzer.py` | 22 KB | Code pattern detection (tables, ISRs) |
| `disassemble_banked.py` | 21 KB | Bank-switched ROM disassembly |
| `hc11_disassembler_complete.py` | 21 KB | Complete disassembly variant |
| `binary_table_extractor.py` | 17 KB | Extract calibration tables from bins |
| `table_auto_detector.py` | 16 KB | Auto-detect table locations |
| `memory_map_analyzer.py` | 13 KB | Memory region analysis |
| `disassemble_hc11.py` | 12 KB | Simple disassembler entry point |
| `find_free_space.py` | 12 KB | Find unused/free ROM space |
| `xdf_full_parser.py` | 11 KB | Parse TunerPro XDF definitions |
| `binary_differ.py` | 9 KB | Diff two binary files |

### Core Library (`core/`, 11 files)

| Module | Size | Purpose |
|--------|------|---------|
| `opcodes.py` | 37 KB | HC11 opcode definitions & decoding |
| `hc11_disassembler.py` | 31 KB | Core disassembler engine |
| `analyze_bank_switching.py` | 23 KB | Bank switching logic analysis |
| `address_conversion.py` | 18 KB | Address format conversion |
| `xdf_verified_analysis.py` | 19 KB | XDF-verified binary analysis |
| `vy_v6_constants.py` | 18 KB | VY V6 specific constants & addresses |
| `analyze_interrupts_v2.py` | 10 KB | Interrupt vector analysis |
| `output_manager.py` | 10 KB | Output formatting |
| `binary_differ.py` | 9 KB | Binary diff core |
| `cli_base.py` | 9 KB | CLI argument parsing base |

> **Note:** Binary patching scripts have been intentionally removed. Use the
> [C compiler workflow](../hc11_compiler/) instead: write C code → compile to
> assembly → validate → flash. This ensures proper understanding and safer
> modifications.

## Relationship to Compiler Project

```
kingai_c_compiler_v0.1/
├── hc11_compiler/               ← C → HC11 compiler
├── hc11_virtual_emulator/       ← Software HC11 emulator
├── hc11_bench_incar_emulator/   ← Bench/in-car testing tools
├── 68hc11_disassembler_tool_for_vy_v6/  ← THIS FOLDER
│   └── Disassemble compiled output, validate against stock,
│       diff patched vs original, find free space for patches,
│       extract tables for compiler test data
└── examples/                    ← Compiler example programs
```

The disassembler tools feed the compiler workflow:
- **Validate compiler output** — disassemble compiled `.bin`, verify instructions are correct
- **Find free space** — locate ROM regions available for compiled code injection
- **Diff binaries** — compare stock vs patched to verify only intended changes
- **Extract tables** — pull calibration data for compiler test inputs
- **Reverse engineer subroutines** — understand stock code that compiled patches must integrate with

> **For actual code modifications:** Use the [C compiler](../hc11_compiler/) → write C,
> compile to HC11 assembly, validate, then flash. Direct binary patching tools have been
> removed to encourage proper development practices.
