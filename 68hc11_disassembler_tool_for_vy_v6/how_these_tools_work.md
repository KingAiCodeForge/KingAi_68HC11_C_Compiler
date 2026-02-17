# How These Tools Work

> **Last updated:** 16 February 2026
> **Target:** Holden VY V6 Commodore 3.8L Ecotec (L36/L67), Delco PCM  
> **CPU:** Motorola 68HC11F1 (MC68HC11FC0 mask set), 3.408 MHz E-clock  
> **OS:** THE1 Enhanced OS ($060A) — 128KB flash binary  
> **XDF:** TunerPro XDF v2.09a/v2.09b-beta (up to 2234 definitions)

---

## Overview

This folder contains **30 Python scripts** (19 top-level + 11 in `core/`) for
reverse engineering, disassembling, and analysing the 128KB HC11 ECU binary
used in the VY V6 Commodore. They evolved from November 2025 through February
2026 across multiple repos and were consolidated here on 16/02/2026.

These can be wrapped or imported via the `core/` folder. Refactoring the
addresses and offsets would make them work with other HC11 ECUs, but they are
currently tailored to the VY V6's specific memory map, binary structure, and
XDF definitions. The main disassembler (`hc11_disassembler_060a_enhanced_v1.py`)
is the most feature-rich and actively developed version, with support for bank
switching, XDF label integration, and various analysis features.

The tools cover the reverse engineering pipeline for **analysis only**.
For code modifications, use the [C compiler workflow](../hc11_compiler/).

Some are simple single-purpose scripts — not worth combining into a larger
tool. Better to have focused tools with the correct offsets and opcodes
imported when needed.

```
Binary file (.bin)
    │
    ├── Disassemble ──→ Human-readable HC11 assembly with annotations
    │
    ├── Analyse ──────→ Memory maps, patterns, subroutines, tables, free space
    │
    ├── Cross-reference → XDF calibration labels overlaid on disassembly
    │
    └── Compare ───────→ Byte-level diffs between stock/enhanced/patched bins

    For code modifications: Use ../hc11_compiler/ (C → ASM → validate → flash)
```

---

## The Binary — What We're Working With

The VY V6 uses a **128KB flash** binary (131,072 bytes) organised into 3 banks:

| Bank | File Offset | Size | CPU Address | Contents |
|------|-------------|------|-------------|----------|
| Bank 1 | `0x00000–0x0FFFF` | 64 KB | `$0000–$FFFF` | Calibration tables + low-bank code |
| Bank 2 | `0x10000–0x17FFF` | 32 KB | `$8000–$FFFF` | Engine control code (paged) |
| Bank 3 | `0x18000–0x1FFFF` | 32 KB | `$8000–$FFFF` | Trans/diagnostics code (paged) |

Bank switching is done via PORTC bit 3. Banks 2 and 3 **share the same CPU
address space** (`$8000–$FFFF`) — only one is visible at a time.

Key memory regions within the HC11's address space:

| CPU Address | What's There |
|-------------|-------------|
| `$0000–$00FF` | Internal RAM (zero page — fast 8-bit addressing) |
| `$0100–$01FF` | Stack + extended RAM |
| `$1000–$103F` | Memory-mapped I/O registers (PORTA, PORTB, timers, ADC, SCI, SPI) |
| `$2000–$202F` | Pseudo-ISR vector jump table (JMP instructions) |
| `$2030–$7FFF` | Calibration data (tables, constants — what XDF defines) |
| `$8000–$FFFF` | Program ROM (executable code, banked) |
| `$FFD6–$FFFF` | Hardware interrupt vectors (14 vectors × 2 bytes) |

### XDF Address Convention

XDF addresses = **file offsets**, not CPU addresses. The XDF BASEOFFSET is 0 for
standard VY V6 binaries. So `XDF address 0x77DE` = byte `0x77DE` in the `.bin`
file = CPU address `$77DE` when bank 1 is active.

For code in banks 2/3: `CPU_addr = file_offset - 0x10000` (bank 2) or
`file_offset - 0x18000 + 0x8000` (bank 3).

---

## Tool Categories

### 1. Disassemblers — Turn Bytes Into Instructions

These scripts read raw binary data and decode it into HC11 assembly mnemonics.
All of them implement the full HC11 instruction set (312 opcodes across 4
pages: base + prebyte `$18`, `$1A`, `$CD`).

**How disassembly works:**

1. Read a byte from the binary at the current offset
2. If it's a prebyte (`$18`, `$1A`, `$CD`), read the next byte — that pair
   identifies a Y-register or CPD instruction
3. Look up the opcode in the instruction table to get: mnemonic, byte length,
   addressing mode, cycle count
4. Read the operand bytes (1–2 more bytes depending on addressing mode)
5. Format as assembly: `$8A3C: B6 77DE    LDAA  $77DE    ; [Rev Limiter High]`
6. Advance offset by instruction length, repeat

**Addressing modes the HC11 uses:**

| Mode | Example | Bytes | What It Does |
|------|---------|-------|-------------|
| Inherent | `NOP`, `RTS`, `MUL` | 1 | No operand — acts on registers implicitly |
| Immediate | `LDAA #$42` | 2–3 | Load literal value into register |
| Direct | `LDAA $3F` | 2 | Read from zero page (first 256 bytes of RAM) |
| Extended | `LDAA $77DE` | 3 | Read from any 16-bit address |
| Indexed X | `LDAA $0A,X` | 2 | Read from address X+offset |
| Indexed Y | `LDAA $0A,Y` | 3 | Read from address Y+offset (requires `$18` prebyte) |
| Relative | `BNE $8A50` | 2 | Branch to signed 8-bit offset from PC |
| Bit direct | `BSET $3F,#$80` | 3 | Set/clear/test bits in zero page |
| Bit+branch | `BRSET $3F,#$80,$8A60` | 4 | Branch if bits set in zero page |

#### Script-by-script:

| Script | Lines | What It Does Differently |
|--------|-------|------------------------|
| **`hc11_disassembler_060a_enhanced_v1.py`** | 2001 | **THE main disassembler.** Loads XDF labels, auto-detects binary version, bank-split support (`--bank bank1\|bank2\|bank3\|full`), RPM comparison detection, timer/IO register tracking, ISR vector tracing. This is the actively developed version. |
| **`hc11_disassembler.py`** | 1981 | Frozen universal backup of the above (v2.2.0). Kept as a starting point for adapting to other HC11 ECUs beyond VY V6 $060A. |
| **`hc11_disassembler_enhanced.py`** | 778 | Earlier enhanced version with auto-detect for binary locations across drives, XDF label integration, timestamped output files. Predecessor to the `_060a_enhanced_v1` version. |
| **`hc11_disassembler_complete.py`** | 621 | Focused on opcode correctness — added missing SUBD, ADDD, CPD, proper prebyte handling. All 263+ opcodes from the reference manual. |
| **`hc11_disassembler_batch.py`** | 740 | Batch mode — disassemble multiple address ranges in one run. Can extract addresses from XDF or manual list. Outputs CSV/JSON. Includes `udis.py`-style format strings and PCR flags for branches. |
| **`disassemble_hc11.py`** | 279 | Minimal/focused — originally built to find the spark calculation routine at `0x17283`. Quick single-address disassembly. |
| **`disassemble_banked.py`** | 475 | Bank-aware — handles 128KB banked ROM with automatic LOW/HIGH bank switching. Full opcode table inline. |
| **`full_binary_disassembler.py`** | 529 | Multi-XDF cross-reference — loads XDF CSVs from multiple versions simultaneously, annotates disassembly with which XDF versions define each address. Torque reduction analysis focus. |
| **`split_and_disassemble.py`** | 601 | Splits 128KB binary into its 3 banks per OSE Flash Tool mapping, disassembles each bank separately, and diffs STOCK vs Enhanced. Uses Capstone M680X engine when available. |

### 2. Analysers — Understand What The Code Does

These go beyond raw disassembly to identify **structure**: subroutines, tables,
patterns, memory usage, and knowledge gaps.

| Script | Lines | What It Analyses |
|--------|-------|-----------------|
| **`ultimate_binary_analyzer.py`** | 1968 | **The everything tool.** Binary comparison, HC11 disassembly, pattern/signature matching, VS/VT/VY/VX platform offset handling, duplicate finding, ECU type ID (size + signature + vectors), XDF cross-ref with EMBEDDEDDATA axis extraction, free space detection, patch analysis. Exports JSON/CSV/Markdown. Auto-detects platform from binary size and vectors. |
| **`hc11_complete_binary_mapper.py`** | 926 | Maps *everything* in the binary and identifies what's still unknown. Integrates XDF data (1856 addresses), timer registers (366 ops), JSR calls (1045), RAM variables (243), ISR vectors (21), hardcoded constants (12282). Produces a knowledge map: ✓ Known / ⚠ Inferred / ❓ Unknown. |
| **`hc11_pattern_analyzer.py`** | 553 | Code pattern detection — finds ISRs (by scanning for RTI return instructions and tracing backwards), table lookup sequences (LDX + ABX + LDAA patterns), mode switching code, error handlers. Assigns confidence scores to detected patterns. |
| **`hc11_subroutine_reverse_engineer.py`** | 697 | Deep subroutine decompilation with control flow analysis. Primary targets: spark timing calc at `JSR $24AB` and timing calc at `JSR $2311`. Tracks RAM variable access, timer register R/W, math operations (MUL, IDIV, ADDD), nested call trees, return value analysis (accumulator state). |
| **`memory_map_analyzer.py`** | 368 | Determines the correct CPU address ↔ file offset mapping. Tests multiple mapping theories (direct, banked, split, XDF-based) against known XDF addresses and interrupt vectors. Validates by checking if known vectors point to valid code. |
| **`table_auto_detector.py`** | 426 | Finds calibration lookup tables by scanning for instruction patterns: `LDX #$table` → `ABX` → `LDAA 0,X` (1D byte table), `LDD 0,X` (1D word table), nested lookups (2D tables). Cross-references against XDF to find undocumented tables. Assigns confidence scores. |

### 3. XDF & Table Tools — Bridge Between Code and TunerPro

TunerPro XDF files define where calibration parameters live (address, size,
data type, axes, conversion formulas). These tools parse XDFs and extract
actual data from binaries.

| Script | Lines | What It Does |
|--------|-------|-------------|
| **`xdf_full_parser.py`** | 288 | Parses an XDF file and extracts ALL addresses organised by category (tables, constants, flags, patches). Maps every element to address → title → category → type. Used by other tools to get XDF labels. |
| **`binary_table_extractor.py`** | 490 | Uses XDF definitions to extract **actual calibration data** from a binary. Decodes data types (uint8/16, int8/16), handles row/column layouts, exports tables to CSV/JSON/hex dump. Can compare table values between stock and enhanced. |

### 4. Diffing & Patching — Compare and Modify Binaries

| Script | Lines | What It Does |
|--------|-------|-------------|
| **`binary_differ.py`** | 253 | Byte-level comparison between two binary files. Finds continuous difference regions with context bytes. Reports region count, total changed bytes, and percentage. Useful for understanding what THE1 changed between stock and enhanced OS. |
| **`binary_patcher.py`** | 389 | BMW MS4X-style patchlist system. Defines patches as objects: (address, original_bytes, patched_bytes, description). Validates original bytes match before patching (safety check). Supports patch sets (grouped patches for a feature) with enable flags. MD5 checksum tracking before/after. |
| **`find_free_space.py`** | 290 | Scans binary for regions of consecutive `0x00` or `0xFF` bytes (auto-detects which — Enhanced uses `0x00`, stock uses `0xFF`). Reports regions >= minimum size (default 64 bytes). Essential for knowing where compiled code can be injected without overwriting existing functionality. |

### 5. Core Library (`core/`) — Shared Modules

The `core/` directory contains modules imported by the top-level scripts.
They reduce code duplication and provide a single source of truth for
constants, opcodes, and utilities.

| Module | Lines | What It Provides |
|--------|-------|-----------------|
| **`opcodes.py`** | 560 | Complete HC11 instruction set with prebyte support. `HC11InstructionSet` class with `_build_opcode_table()` for base page, `_build_prebyte_18()` for Y-register ops, `_build_prebyte_1A()` for CPD etc, `_build_prebyte_CD()`. Dataclass `Instruction(mnemonic, length, cycles, mode, prebyte, description)`. |
| **`hc11_disassembler.py`** | 744ish | Core disassembler engine used by top-level scripts. Imported as `from core.hc11_disassembler import HC11Disassembler`. Provides the `read_byte()`, `disassemble_at()`, and instruction decode loop. |
| **`vy_v6_constants.py`** | 422 | **Single source of truth** for all VY V6 constants. Binary paths (auto-detects R:, C:, A: drives), hardware specs (corrected to HC11F1 @ 3.408 MHz as of Feb 2026), RAM addresses, timing constants (Chr0m3 Motorsport validated), register names, interrupt vector table. |
| **`address_conversion.py`** | 531 | Converts between XDF file offsets and HC11 CPU addresses. Handles BASEOFFSET (subtract flag), the 128KB 3-bank layout, and special regions ($1000–$103F registers). `AddressConverter` class with `file_to_cpu()`, `cpu_to_file()`, `is_ram()`, `is_io_register()`. |
| **`cli_base.py`** | 246 | Standard CLI argument parser base class. Provides `--input`, `--output`, `--format`, `--verbose`, `--timestamp` flags shared by all tools. Consistent logging setup and error handling. |
| **`output_manager.py`** | 316 | Centralised output formatting. Supports timestamped filenames, multiple formats (txt, JSON, CSV, markdown), organised directory structures. Tracks statistics (files written, bytes written). |
| **`analyze_bank_switching.py`** | 558 | Maps HC11 expanded mode memory banking. Scans for PORTC writes that control bank select bit 3. Identifies which code runs in which bank, cross-bank calls, and bank switching sequences. |
| **`analyze_interrupts_v2.py`** | 267ish | Interrupt vector table analysis. Reads the 14 hardware vectors at `$FFD6–$FFFF`, resolves to ISR entry points, traces through the pseudo-vector jump table at `$2000–$202F`, identifies ISR handler code. |
| **`xdf_verified_analysis.py`** | 475 | Strict XDF+binary cross-reference — NO speculation, only verified data. Extracts confirmed addresses from XDF, validates them against actual binary byte patterns. Uses Chr0m3 Motorsport validated constants as ground truth. |
| **`binary_differ.py`** | 253 | Same as top-level `binary_differ.py` (shared copy in core for import). |
| **`binary_patcher.py`** | 389 | Same as top-level `binary_patcher.py` (shared copy in core for import). |
| **`patch_ignition_cut.py`** | 373 | BMW MS43-style ignition cut patch builder for Enhanced v1.0a. Defines patch addresses (`0x1FE00` calibration, `0x1FE0A` code, `0x1007C` hook point), calibration data (RPM thresholds), and the HC11 machine code bytes for the patch routine. **UNTESTED — bench test required.** |
| **`patch_ignition_cut_v2.py`** | 312ish | Revised ignition cut patch with corrected addresses and approach. |
| **`validate_ignition_cut_patch.py`** | 651ish | Validates an ignition cut patch by disassembling the patched region, verifying the hook instruction was correctly inserted, checking that original bytes surrounding the patch are untouched, and tracing the patch code's control flow to confirm it returns correctly. |

---

## How The Disassembler Actually Decodes Instructions

The HC11 has a **variable-length instruction set** (1–5 bytes per instruction)
with 4 opcode pages. Here's the decode logic used by all the disassemblers:

```
read byte at current offset
│
├── if 0x18 (PAGE2 prebyte):
│   read next byte → look up in prebyte_18 table
│   these are Y-register versions of X-register instructions:
│   LDY, STY, CPY, ADDY, indexed-Y addressing, etc.
│   total instruction length = 2 + operand bytes
│
├── if 0x1A (PAGE3 prebyte):
│   read next byte → look up in prebyte_1A table
│   CPD (Compare D), some cross-indexed operations
│   total instruction length = 2 + operand bytes
│
├── if 0xCD (PAGE4 prebyte):
│   read next byte → look up in prebyte_CD table
│   Y-indexed versions of CPD, CPX, LDX, STX
│   total instruction length = 2 + operand bytes
│
└── otherwise:
    look up in base opcode table (page 1)
    standard X-register operations
    total instruction length = 1 + operand bytes
```

### Why Multiple Disassembler Scripts Exist

They evolved iteratively:

1. **`disassemble_hc11.py`** (Nov 2025) — minimal, ~80 opcodes, targeted one address
2. **`hc11_disassembler_complete.py`** (Jan 2026) — fixed missing opcodes, all 263+
3. **`hc11_disassembler_enhanced.py`** (Jan 2026) — added XDF labels, auto-detect
4. **`hc11_disassembler_060a_enhanced_v1.py`** (Feb 2026) — merged everything,
   added bank splitting, the current actively developed version
5. **`hc11_disassembler.py`** — frozen copy of #4 as a universal starting point

The batch, full-binary, and split variants address different use cases (process
many addresses at once, cross-reference multiple XDFs, or handle bank
splitting) but share the same core decode logic.

---

## How XDF Cross-Referencing Works

1. Parse the `.xdf` XML file to extract all `<XDFTABLE>`, `<XDFCONSTANT>`,
   and `<XDFPATCH>` elements
2. For each element, read its `<EMBEDDEDDATA mmedaddress="0x77DE" />`
   attribute — this is the **file offset** of the calibration parameter
3. Build a lookup dict: `{0x77DE: "Rev Limiter High", 0x77DF: "Rev Limiter Low", ...}`
4. During disassembly, when an instruction references an address (e.g.
   `LDAA $77DE`), check the lookup dict
5. If found, append the XDF label as a comment:
   ```
   $8A3C: B6 77DE    LDAA  $77DE    ; [XDF: Rev Limiter High] = 0xEC (5900 RPM)
   ```
6. For the `ultimate_binary_analyzer`, multiple XDF versions are loaded
   simultaneously so you can see which versions define/changed each address

---

## How Table Auto-Detection Works

The `table_auto_detector.py` scans for common HC11 table lookup instruction
sequences:

**1D byte table lookup:**
```asm
LDX  #$table_addr    ; CE xx xx — load table base address
ABX                   ; 3A — add accumulator B to X (index into table)
LDAA 0,X              ; A6 00 — load byte from table at index
```

**1D word table lookup:**
```asm
LDX  #$table_addr    ; CE xx xx
ASLB                  ; 58 — shift left (multiply index by 2 for word table)
ABX                   ; 3A
LDD  0,X              ; EC 00 — load 16-bit word from table
```

**2D table lookup:**
```asm
; First dimension lookup gives an offset
LDX  #$row_table     ; CE xx xx
ABX                   ; 3A
LDAB 0,X              ; E6 00 — get row offset
; Second dimension lookup using that offset
LDX  #$col_table     ; CE xx xx
ABX                   ; 3A
LDAA 0,X              ; A6 00 — get final value
```

When a candidate table address is found, the tool cross-references it against
known XDF definitions to see if it's an already-documented table or a newly
discovered one.

---

## How Free Space Finding Works

The VY V6 Enhanced binary uses `0x00` for free/unused ROM areas (THE1's
convention when building the Enhanced OS). Stock binaries use `0xFF` (erased
flash state).

`find_free_space.py` auto-detects which pattern is dominant, then scans
linearly for consecutive runs of that byte value >= a minimum threshold
(default 64 bytes). The results tell you where compiled code can safely be
injected without overwriting existing functionality.

The ignition cut patches use free space at `0x1FE00+` (near end of bank 3).

---

## How Binary Patching Works

The `binary_patcher.py` follows a BMW MS4X community-style patchlist approach:

1. **Define a Patch:** specify address, expected original bytes, new bytes, and
   description
2. **Validate:** before applying, read the binary at the patch address and
   verify the original bytes match — if they don't, the binary isn't what we
   expected and the patch is refused (safety check)
3. **Apply:** overwrite the bytes at the patch address
4. **Checksum:** compute MD5 before and after to track what changed
5. **Patch sets:** group related patches (e.g. "ignition cut" = calibration
   data patch + code injection patch + hook point patch) with an enable flag
   address

The ignition cut patcher (`core/patch_ignition_cut.py`) is a concrete example:
it writes calibration data at `0x1FE00`, injects HC11 machine code at
`0x1FE0A`, and hooks into the dwell calculation routine at `0x1007C` with a
JSR to the patch code. The validator (`core/validate_ignition_cut_patch.py`)
then disassembles the patched region to confirm correctness.

---

## How Address Conversion Works

The `AddressConverter` class in `core/address_conversion.py` handles the
headache of 128KB-in-a-64KB-address-space:

```python
# File offset → CPU address
def file_to_cpu(file_offset):
    if 0x00000 <= file_offset <= 0x0FFFF:
        return file_offset                    # Bank 1: direct mapping
    elif 0x10000 <= file_offset <= 0x17FFF:
        return file_offset - 0x10000          # Bank 2: subtract 0x10000
    elif 0x18000 <= file_offset <= 0x1FFFF:
        return file_offset - 0x18000 + 0x8000 # Bank 3: map to $8000+

# CPU address → file offset (needs to know which bank is active)
def cpu_to_file(cpu_addr, bank=1):
    if bank == 1:
        return cpu_addr
    elif bank == 2:
        return cpu_addr + 0x10000
    elif bank == 3:
        return cpu_addr - 0x8000 + 0x18000
```

The XDF BASEOFFSET handling is also here — some XDFs use a `subtract` flag
that reverses the offset direction.

---

## Typical Workflows

### "I want to see what code does at address $8A3C"

```bash
python hc11_disassembler_060a_enhanced_v1.py --bank bank2 --start 0x8A3C --length 0x100
```

### "I want to find all free space in the Enhanced binary"

```bash
python find_free_space.py "path/to/Enhanced_v1.0a.bin" --min-size 64
```

### "I want to diff stock vs enhanced"

```bash
python binary_differ.py "92118883_STOCK.bin" "Enhanced_v1.0a.bin"
```

### "I want to extract all calibration tables to CSV"

```bash
python binary_table_extractor.py --binary "Enhanced_v1.0a.bin" --xdf "v2.09a.xdf" --format csv
```

### "I want to find undocumented lookup tables"

```bash
python table_auto_detector.py "Enhanced_v1.0a.bin" --xdf "v2.09a.xdf"
```

### "I want the full knowledge map — what's known, what's unknown"

```bash
python hc11_complete_binary_mapper.py "Enhanced_v1.0a.bin"
```

---

## Dependencies

- **Python 3.8+** (all scripts)
- **No pip packages required** for core disassembly — everything uses stdlib
  (`struct`, `argparse`, `xml.etree.ElementTree`, `json`, `csv`, `pathlib`)
- **Optional:** Capstone engine (`pip install capstone`) — `split_and_disassemble.py`
  can use Capstone's M680X backend as an alternative disassembly engine for
  cross-validation
- **Optional:** The binary files themselves (`.bin`) and XDF files (`.xdf`) — 
  not included in the repo, you need to supply your own

---

## Known Issues / In Progress

- Some scripts still have hardcoded `A:\repos\...` or `R:\...` paths from the
  original development locations — being progressively cleaned up
- `core/analyze_bank_switching.py` references `MC68HC11E9` in the hardware spec
  dataclass — should be `MC68HC11FC0` (corrected elsewhere but not in this file)
- `hc11_pattern_analyzer.py` is marked as **UNTESTED experimental**
- `patch_ignition_cut.py` and `patch_ignition_cut_v2.py` are **UNTESTED** —
  require bench testing with hardware emulator before any vehicle use
- `full_binary_disassembler.py` has a duplicated Windows encoding fix block
  (harmless but should be cleaned up)
