# Virtual ECU Feasibility Analysis — VY V6 $060A Enhanced

**Date:** February 15, 2026
**Author:** KingAustraliaGG
**Status:** Research complete — Phase 1 is buildable today

---

## The Question

> Can we make the VY V6 PCM binary "run" on a Windows 10/11 PC using only software?
> No physical PCM. Just the 128KB dump, the XDF definitions, and the disassembly we already have.

---

## Short Answer

**YES — in layers, with increasing difficulty:**

| Level | What It Does | Difficulty | We Can Build It? |
|-------|-------------|-----------|-----------------|
| **1. Table Lookup Simulator** | Feed RPM+MAP → get spark/fuel/VE from XDF tables | Easy | **YES — today** |
| **2. Instruction-Level Emulator** | Execute actual HC11 opcodes from the binary | Medium | **YES — 80% already built** |
| **3. Full ECU Simulation (SIL)** | Run the complete main loop with virtual sensors | Hard | **Possible with work** |
| **4. Real-Time HIL Replacement** | Replace physical PCM on a bench/in-car | Very Hard | **Not practical** |

**CPU vs GPU?** → **CPU only.** This is sequential opcode execution (fetch-decode-execute), not parallelisable. A modern i5/Ryzen will run the HC11 at 1000x+ real-time speed. GPU is irrelevant.

---

## What We Already Have (Inventory)

### Binary & Definitions

| Resource | Path | What It Gives Us |
|----------|------|------------------|
| **128KB ROM dump** | `VY_V6_Enhanced.bin` | The actual code + calibration data |
| **XDF v2.09b** | `VX VY_V6_$060A_Enhanced_v2.09b.xdf` | **2,234 parameter definitions**: 1,310 scalars, 548 flags, 330 tables with axes, units, scaling formulas |
| **XDF JSON export** | `Enhanced_v209b_export.json` | Machine-readable version of all 2,234 defs — addresses, sizes, axis info, scaling |
| **XDF MD export** | `Enhanced_v209b_export.md` | Human-readable: every scalar value, flag state, table data with units |
| **XDF TXT export** | `Enhanced_v209b_export.txt` | Flat text version for grep/search |

### Bank-Split Binaries

| Resource | Path | Value for Emulator |
|----------|------|-------------------|
| **Bank 1 binary** (64KB) | `bank_split_output/Enhanced_v1.0a_bank1.bin` | RAM ($0000-$03FF), I/O ($1000-$103F), calibration ($4000-$7FFF), code ($8000-$FFFF), vectors ($FFC0-$FFFF) |
| **Bank 2 binary** (32KB) | `bank_split_output/Enhanced_v1.0a_bank2.bin` | Engine code overlay at $8000-$FFFF (dwell calc, TIC3 ISR, dense math) |
| **Bank 3 binary** (32KB) | `bank_split_output/Enhanced_v1.0a_bank3.bin` | Transmission/diagnostic overlay at $8000-$FFFF |

### Disassembly Tools — Detailed Comparison (6 tools, 4 cross-verified)

We used **6 different disassembly approaches**. Four produce agreeing output and were cross-verified at hook point $81E1 (`STD $017B`). Two (Ghidra, Techedge) had issues.

#### 1. Capstone M680X (`split_and_disassemble.py`)

| Attribute | Detail |
|-----------|--------|
| **Engine** | Capstone library — `CS_ARCH_M680X`, `CS_MODE_M680X_6811` |
| **Output** | `bank_split_output/Enhanced_v1.0a_bank{1,2,3}.asm` |
| **Opcodes** | Full HC11 instruction set (Capstone handles all pages natively, including $18/$1A/$CD prebytes) |
| **Disassembly mode** | **Recursive descent** for bank1 $2000-$5FFF mixed code/data region. Seeds from ISR JMP table at $2000-$202F, JSR/JMP targets from $6000+, cross-bank scanning, manual `EXTRA_CODE_SEEDS` list |
| **Bank awareness** | **Full** — splits 128KB binary into 3 banks (64K+32K+32K) with correct CPU base addresses ($0000, $8000, $8000) |
| **ISR tracing** | Yes — parses vector table at $FFD6-$FFFF, extracts JMP targets |
| **Diff capability** | Yes — `--diff` flag produces byte-level STOCK vs Enhanced per-bank diffs |
| **XDF integration** | **No** — pure disassembly, no calibration labels |
| **RPM/Timer detection** | **No** |
| **Address accuracy** | **CORRECT** — verified at $81E1 (bank2 hook point) |
| **Strengths** | Fastest execution (C library), best for bank-split + diff workflow, recursive descent handles mixed code/data in $2000-$5FFF well |
| **Limitations** | No labels, no XDF overlay, no function boundaries, treats calibration regions ($4000-$7FFF) as code if not masked, no cross-references. External dependency (pip install capstone). Header has truncation artifact in v1.0a bank1 |
| **Output volume** | Bank1: 37,354 lines (36,531 instructions + 11,238 data bytes), Bank2: 14,183 lines, Bank3: 27,616 lines |

#### 2. GNU m6811-elf objdump

| Attribute | Detail |
|-----------|--------|
| **Engine** | GNU binutils 2.15 — `m6811-elf-objdump -D -m m68hc11` |
| **Output** | `bank_split_output/Enhanced_v1.0a_bank{1,2,3}_gnu.asm` |
| **Opcodes** | Full HC11 instruction set including all page 2/3/4 ($18/$1A/$CD) |
| **Disassembly mode** | Linear sweep (stops at $FF fill regions) |
| **Bank awareness** | Yes — base address set via `objcopy --change-section-address` |
| **ISR tracing** | **No** |
| **XDF integration** | **No** |
| **RPM/Timer detection** | **No** |
| **Address accuracy** | **CORRECT** — verified at $81E1 |
| **Strengths** | Authoritative reference (GNU toolchain), also provides GDB HC11 simulator (`m6811-elf-gdb.exe`) for validation oracle. 9 bank outputs generated (3 ROM variants × 3 banks) |
| **Limitations** | Noisy output with long auto-generated symbols, no labels, no function detection, no cross-references, no bank splitting (manual objcopy step required). Not install-friendly on Windows |
| **Output volume** | Bank1: ~1,500 KB, Bank2: ~1,383 KB, Bank3: ~377 KB |

#### 3. KingAI Custom Python HC11 Disassembler (`hc11_disassembler_060a_enhanced_v1.py` v2.2.0)

| Attribute | Detail |
|-----------|--------|
| **Engine** | Custom Python — `hc11_opcodes_complete.py` opcode library (312 opcodes: 236 base + 65 page2 + 7 page3 + 4 page4) |
| **Output** | TXT/JSON/CSV/MD via `OutputManager` module |
| **Opcodes** | **312** — sourced from `dis68hc11/Opcodes.h` + `ghidra-hc11-lang/HC11.slaspec`, most complete of any Python tool |
| **Disassembly mode** | Analytical (not full linear sweep — targeted region analysis with heuristics) |
| **Bank awareness** | **Full** — `--bank bank1|bank2|bank3|full` flag + auto-detect from filename/size |
| **ISR tracing** | **Yes** — vector table parsing at $FFC0-$FFFF, ISR handler entry point tracing with call depth analysis |
| **XDF integration** | **YES — 2,234 calibration definitions** (v2.09b-beta) or 1,757 (v2.09a) loaded as address labels. Shows parameter names inline in disassembly |
| **RPM/Timer detection** | **YES** — 99 RPM comparisons found, 50+ timer/I/O register accesses identified, named HC11 I/O registers ($1000-$103F: TCTL1, PORTG, ADR1, etc.) |
| **Calibration cross-refs** | **YES** — 945 calibration reads identified in bank2 alone, links code to XDF parameter names |
| **Address accuracy** | **CORRECT** — verified at $81E1 |
| **Strengths** | **Best analytical output** for ECU reverse engineering. Only tool with XDF overlay, RPM threshold detection, I/O register naming, ISR tracing, and calibration cross-referencing. Modular architecture via `tools/core/` (opcodes.py, vy_v6_constants.py, address_conversion.py). Bank-split support verified Feb 14, 2026 |
| **Limitations** | Specific to Enhanced v1.0a binary (needs adaptation for other ECUs). Depends on `core/` modules (degrades gracefully without them). Not a full linear sweep — targeted analysis only. No reassemblable output |
| **Supporting modules** | `hc11_opcodes_complete.py` (312 opcodes + ECU helpers), `hc11_opcode_table.py` (246+ opcodes with cycle counts), `hc11_disassembler_batch.py` (spot-check CSV/JSON output) |

#### 4. udis (`6811.py`)

| Attribute | Detail |
|-----------|--------|
| **Engine** | Multi-CPU micro disassembler — Python, full HC11 instruction set |
| **Output** | `bank_split_output/Enhanced_v1.0a_bank{1,2,3}_udis.asm` |
| **Opcodes** | Full HC11 decode, zero unknown opcodes across all banks |
| **Disassembly mode** | **Linear sweep** — processes every byte sequentially, no flow analysis |
| **Bank awareness** | Manual — `-a` flag for base address |
| **ISR tracing** | **No** |
| **XDF integration** | **No** |
| **RPM/Timer detection** | **No** |
| **Address accuracy** | **MISALIGNED in bank2** — linear sweep loses sync at $81A2 where a 2-byte `LDD $9D` is consumed as part of a 3-byte instruction. Result: hook point at $81E1 appears as $81D9 (8 bytes off). This is a fundamental limitation of linear sweep in variable-length HC11 code |
| **Strengths** | Clean assembler-compatible output with `.org` directives (partially reassemblable). brset/brclr branch targets verified correct. Zero unknown opcodes |
| **Limitations** | **DO NOT TRUST udis addresses for patching** without cross-checking against GNU/Capstone/Custom Python. Treats ALL data as code (calibration tables decoded as nonsense instructions). No labels, no function boundaries, no cross-references |
| **Output volume** | Bank1: ~1,235 KB, Bank2: ~477 KB, Bank3: ~779 KB |

#### 5. Ghidra HC11 (multiple scripts — largely UNTESTED)

| Attribute | Detail |
|-----------|--------|
| **Engine** | Ghidra 11.2.1 / 11.4.2 with `HC-11:BE:16:default` processor module |
| **Scripts** | `tools/ghidra/` directory — 21 items: Jython export scripts (`ExportHC11Assembly.py`, `ExportHC11Disassembly.py`), XDF label import scripts (`vy_v6_060a_enhanced_v2_09a_labels.py`, `VY_V6_XDF_Labels_Import.py`), 3-bank analysis (`VY_V6_3Bank_PostAnalysis.py`), MAF failsafe analysis, batch launchers (`run_ghidra_hc11_analysis.bat/.ps1`) |
| **Headless analyzer** | `ghidra_headless_analyzer.py` — automates headless decompilation, processor auto-detection, exports to JSON/CSV. **UNTESTED** |
| **XDF→Ghidra pipeline** | `xdf_to_ghidra_jython.py` — parses TunerPro XDF, generates Ghidra Jython scripts for automatic labeling. Address translation with bank-aware mapping |
| **Re-disassembly** | `redisassemble_with_ghidra_hc11.py` (1,358 lines) — uses BOTH Ghidra 11.2.1 and 11.4.2 with multiple HC11 processor modules, auto-detects base address from vector table, cross-validates with standalone `dis68hc11` |
| **Actual output** | Previous Ghidra headless export produced 63,185 lines but at **WRONG base address** ($352 offset → all addresses shifted). Results were **DELETED Feb 14** as unusable. Comparison directories created (`comparison_20260120_*/`) but **EMPTY** |
| **Strengths** | Most powerful tool: full decompilation, automatic function detection, cross-references, global variable tracking, data type propagation. XDF label import pipeline exists. Potentially the best tool for full ECU understanding |
| **Limitations** | **No working output yet** — all existing exports were at wrong offsets. HC11 processor module in Ghidra is community-contributed (ghidra-hc11-lang), needs correct configuration. Headless mode is complex to set up. Workflow documented in `GHIDRA_HC11_WORKFLOW.md` but not validated end-to-end. Heavy (multi-GB install). Requires Java |
| **Status** | Scripts exist, pipeline designed, but **needs re-export with correct base address configuration** before any output is trustworthy |

#### 6. Techedge DHC11 / DISASM11 (BLOCKED)

| Attribute | Detail |
|-----------|--------|
| **Engine** | Multi-pass flow-tracing disassembler (DHC11) + linear sweep with human-editable .OPC opcode tables (DISASM11) |
| **Status** | **BLOCKED** — both are **16-bit DOS executables**, will not run on 64-bit Windows 10/11 |
| **Purpose** | DHC11 is specifically designed for Delco HC11 ECU binaries with flow-tracing label generation. DISASM11 has editable opcode tables |
| **Files exist** | `techedge_decompiled/` directory contains extracted archives, original files, some disassembly output |
| **Workaround** | Would require DOSBox or similar emulator. Not pursued — Custom Python disassembler fills this role |

#### 7. Other Disassembly Scripts (Legacy / Specialized)

| Script | Opcodes | Purpose | Status |
|--------|---------|---------|--------|
| `hc11_disassembler.py` | 312 | Frozen v2.2.0-universal-backup of 060a_enhanced. Generic starting point for other ECU bins | **Not actively developed** — use 060a_enhanced instead |
| `hc11_disassembler_enhanced.py` | ~200+ | Earlier "enhanced production" disassembler. Treats $18 as `XGDX` (incorrect as standalone) | **Legacy — merged into 060a_enhanced** |
| `hc11_disassembler_complete.py` | 263 | "Fixed with ALL Opcodes" — added SUBD/ADDD/CPD. Output in `disassembly_output/jan19_2026/` | **Superseded** — 4 `.asm` files generated (STOCK, Enhanced v1.0a, v1.1a, VY_V6_Enhanced) |
| `hc11_disassembler_batch.py` | ~250+ | Batch disassembler — CSV/JSON output, PCR flags (branch detection), XDF address batch input | **Active** — for targeted spot-checks |
| `hc11_opcode_table.py` | ~263 | Structured opcode metadata library with cycle counts, helper functions | **Active** — shared library |
| `hc11_opcodes_complete.py` | **312** | **Most complete** — 4-page tables with RPM/timer detection ECU helpers | **Active** — used by 060a_enhanced |
| `compare_disassemblers.py` | N/A | Compares 3 Python disassemblers + optional Ghidra at 7 key test addresses | **Outputs empty** — comparison dirs created but no actual results |
| `full_binary_disassembler.py` | ? | Full 128KB binary linear sweep | Legacy |
| `disassemble_banked.py` | ? | Bank-aware disassembly with bank switch detection | Tool exists |

#### Opcode Count Cross-Reference

| Source | Base Page | $18 (Y-indexed) | $1A (Page2) | $CD (Page3) | Total | Notes |
|--------|:---------:|:----------------:|:-----------:|:-----------:|:-----:|-------|
| **hc11_opcodes_complete.py** | ~210 | ~60 | ~20 | ~22 | **312** | dis68hc11 + Ghidra SLEIGH — most complete |
| **hc11_opcode_table.py** | ~246 | 5 (sparse) | 12 | 0 | **~263** | HC11 Ref Manual + SLEIGH — $18 table incomplete |
| **hc11_disassembler_complete.py** | ~200 | inline | inline | inline | **263** | M68HC11 Reference Manual |
| **hc11_disassembler_batch.py** | full | inline | inline | inline | **~250+** | Includes PCR (branch) flags — udis.py inspired |
| **Capstone** | native | native | native | native | **All** | Hardware-accelerated, handles all HC11 opcodes natively |
| **GNU m6811-elf** | native | native | native | native | **All** | GCC/binutils toolchain — authoritative |

#### 4-Way Cross-Check at Hook Point $81E1 (Feb 14, 2026)

Validated `STD $017B` at file offset `0x101E1` (bank2 CPU `$81E1`) — the only write to dwell intermediate RAM in the entire 128KB binary:

| Tool | Reported Address | Decode | Result |
|------|:----------------:|--------|:------:|
| Custom Python | `$81E1` | `FD 01 7B  STD $017B` | **CORRECT** |
| GNU m6811-elf | `$81E1` | `fd 01 7b  std 17b` | **CORRECT** |
| Capstone | `$81E1` | `FD 01 7B  std $017b` | **CORRECT** |
| udis | `$81D9` | `FD 01 7B  std $017B` | **WRONG** (8 bytes off) |
| Raw hex dump | offset `0x01E1` | `FD 01 7B` | Ground truth |

#### Disassembly Output Files Inventory

| Directory | Contents |
|-----------|---------|
| `bank_split_output/` | **27 files**: 9 `.bin` splits + 18 `.asm` files (3 ROM variants × 3 banks × 2-3 tools) + diffs + README |
| `disassembly_output/` | 1 `.asm` file (STOCK Feb 2026), 2 empty comparison dirs |
| `disassembly_output/jan19_2026/` | **4 complete `.asm` files**: STOCK, Enhanced v1.0a, v1.1a, VY_V6_Enhanced + analysis docs |
| `tools/ghidra/` | 21 items: Jython scripts, batch launchers, XDF label import, workflow docs — **largely untested** |
| `techedge_decompiled/` | 5 subdirs: original_files, extracted_zips, disassembly, strings, analysis |

### Existing Emulator (80% Built)

| Module | Path | Status |
|--------|------|--------|
| **CPU core** | `hc11_virtual_emulator/src/cpu/` | All 256 page-1 + page 2/3/4 opcodes decoded. ALU with correct HC11 flag semantics. **46/46 tests passing.** |
| **Memory map** | `hc11_virtual_emulator/src/mem/memory.py` | 64K flat map, ROM write protection, I/O handler routing, S19 loading. **Bank switching NOT yet implemented.** |
| **SCI peripheral** | `hc11_virtual_emulator/src/periph/sci.py` | TX capture, RX injection (ALDL simulation) |
| **ADC peripheral** | `hc11_virtual_emulator/src/periph/adc.py` | 8-channel sensor injection with instant conversion |
| **Timer peripheral** | `hc11_virtual_emulator/src/periph/timer.py` | TCNT free-running, OC1-5 compare, prescaler |
| **I/O Ports** | `hc11_virtual_emulator/src/periph/ports.py` | PORTA-E state tracking with change callbacks |
| **ALDL Mode 4** | `hc11_virtual_emulator/src/aldl/mode4_harness.py` | Frame builder, checksum validation |

### Analysis Tools Portfolio

Over **200 Python analysis tools** in `VY_V6_Assembly_Modding/tools/` including:
- `hc11_hardware_timing_analyzer.py` — Timer/I/O timing linkage
- `enhanced_v1_0a_memory_mapper.py` — Full memory map builder
- `map_ram_variables.py` — RAM variable identification ($0000-$03FF)
- `analyze_interrupts.py` — ISR vector mapping and handler tracing
- `find_rev_limiter.py` — Rev limit function identification
- `analyze_spark_tables.py` — Spark table structure analysis
- `analyze_dwell_enforcement.py` — Dwell calculation path analysis
- `validate_asm_against_xdf.py` — Binary ↔ XDF cross-validation

---

## Binary Structure Analysis

### The VY_V6_Enhanced.bin File

```
Size:       131,072 bytes (128 KB exactly)
Cal ID:     22222999 (found at $40AC)
Reset:      $C011 (reset vector at $FFFE-$FFFF)
CPU:        MC68HC11F1 (Motorola/Freescale)
Clock:      2 MHz E-clock (8 MHz crystal ÷ 4)
```

### Memory Map (HC11F1 in Delco PCM)

```
$0000-$03FF   Internal RAM          1,024 bytes   Read/Write
$0400-$0FFF   Extended RAM           3,072 bytes   Read/Write (PCM-specific)
$1000-$103F   I/O Registers            64 bytes   Peripheral control
$1040-$3FFF   External RAM/Unused   12,224 bytes   PCM-specific
$4000-$7FFF   Flash Calibration     16,384 bytes   The "tune" — tables, scalars
$8000-$BFFF   ROM Bank Window       16,384 bytes   Bank-switched overlay
$C000-$FDFF   Fixed ROM             15,872 bytes   Main OS code (always mapped)
$FE00-$FFBF   Internal EEPROM          448 bytes   Persistent storage
$FFC0-$FFFF   Interrupt Vectors         64 bytes   32 vectors × 2 bytes
```

### Bank Switching Architecture

The 128KB ROM is larger than the 64KB HC11 address space. Three banks overlay into $8000-$FFFF:

```
File Offset       CPU Address   Bank   Contents
$00000-$0FFFF     $0000-$FFFF   1      Main: RAM + I/O + Calibration + Code + Vectors
$10000-$17FFF     $8000-$FFFF   2      Engine code continuation (dwell calc, TIC3 ISR)
$18000-$1FFFF     $8000-$FFFF   3      Transmission/diagnostic overlay
```

Bank selection is controlled by writing to a hardware register (PORTG bit). The emulator needs to intercept writes to this register and swap the $8000-$FFFF memory window.

---

## Feasibility Assessment by Level

### Level 1: Table Lookup Simulator (EASY — buildable today)

**What:** Extract the 330 tables from the XDF, build a Python engine that does table lookups.
Feed in (RPM, MAP/airflow, coolant temp, TPS) → get out (spark advance, fuel pulse width, VE, shift points).

**Why it works:**
- The XDF JSON export has all 2,234 parameters with addresses, sizes, axis definitions, and scaling
- We can read the binary, apply XDF scaling formulas, and interpolate tables
- No need to execute actual HC11 opcodes
- This is what TunerPro already does — we'd just script it

**What it tells you:**
- "At 3000 RPM, 80 kPa MAP, 90°C coolant → spark = 32° BTDC, fuel PW = 4.2ms"
- "Rev limiter fuel cut activates at 6000 RPM"
- "Shift points: 1-2 at 22 MPH, 2-3 at 45 MPH, 3-4 at 62 MPH"

**Limitations:**
- No dynamic behavior (no acceleration/deceleration transitions)
- No closed-loop O2 correction, no adaptive learning
- No timing of events (just steady-state snapshots)

**Effort:** 1-2 days. Pure Python + the JSON export.

### Level 2: Instruction-Level Emulator (MEDIUM — 80% built)

**What:** Execute actual HC11 machine code from the binary, instruction by instruction.
The emulator fetches opcodes, decodes them, updates registers and memory.

**What we have:**
- ✅ Full CPU core with all HC11 opcodes (page 1-4)
- ✅ All addressing modes (INH, IMM, DIR, EXT, INDX, INDY, REL, BIT)
- ✅ Complete ALU with correct flag semantics
- ✅ SCI peripheral (ALDL communication)
- ✅ ADC (sensor reading simulation)
- ✅ Timer (free-running counter, output compare)
- ✅ I/O Ports (PORTA-E with callbacks)
- ✅ 46/46 integration tests passing

**What's missing for full binary execution:**

| Gap | Difficulty | Why It Matters |
|-----|-----------|---------------|
| **Bank switching** | Medium | The binary uses 3 banks — code in bank 2 won't be reachable without it. Need to intercept PORTG writes and swap the $8000-$FFFF window. |
| **Interrupt handling** | Medium | The main loop is interrupt-driven. TIC3 (24X crank), TOC1 (main timer), SCI — these fire constantly. Without IRQ dispatch the code won't advance past the idle loop. |
| **Virtual sensor injection** | Easy | ADC channels need simulated values (RPM from virtual crank, TPS, MAP, coolant, IAT). Framework exists in adc.py — just needs VY V6 channel map. |
| **I/O register completeness** | Medium | 64 I/O registers at $1000-$103F. Many control hardware: SPI (slave select for ADC chip), timers, COP watchdog. Missing handlers → code hangs or crashes. |
| **COP watchdog** | Easy | Must be fed periodically or the CPU resets. Either disable it or add an auto-feed. |
| **EEPROM emulation** | Easy | $FE00-$FFBF needs to persist between runs (learned values, DTCs). Just save to a file. |

**What it tells you:**
- Step through the actual code path: reset → init → main loop
- Watch RAM variables change as you inject sensor values
- See exactly when and how the rev limiter fires
- Validate patches BEFORE flashing to real hardware
- Debug the spark cut implementation in software

**Effort:** 2-4 weeks to get the binary running. Bank switching + interrupt dispatch + sensor injection.

### Level 3: Full ECU Simulation / Software-in-the-Loop (HARD)

**What:** Run the complete main loop continuously with a virtual engine model.
The emulator executes HC11 code. A separate "plant model" simulates the engine —
crank position, intake air, combustion, exhaust. The two talk via the ADC/timer/port interfaces.

**Additional requirements beyond Level 2:**
- **Engine plant model:** Calculate RPM from torque balance, air from throttle+MAP, combustion from spark+fuel+air. This is where MATLAB/Simulink normally lives.
- **Real-time crank signal simulation:** TIC3 interrupts at crank tooth intervals. Need a virtual crank wheel generating 24X+1X signals at the correct timing.
- **Closed-loop feedback:** O2 sensor model that responds to air/fuel ratio. BLM (block learn) adaptation.
- **Transmission model:** 4L60E shift logic, TCC lockup, line pressure.

**What it tells you:**
- Full dynamic simulation: stomp throttle → watch RPM climb → watch spark retard → hit rev limiter → fuel cut
- Test transient behavior: cold start, warm-up, acceleration, deceleration
- Validate transmission shift calibration without driving

**Effort:** 2-6 months. Requires engine dynamics knowledge.

### Level 4: Real-Time HIL Replacement (NOT PRACTICAL)

**What:** Replace the physical PCM with a PC running the emulator in real-time, connected to actual sensors/actuators.

**Why not:**
- HC11 timing is cycle-accurate at 2 MHz E-clock (500ns per cycle). A PC can't guarantee this timing.
- Ignition/injection timing requires microsecond precision on hardware outputs.
- The physical wiring harness interface is entirely different (12V logic levels, power transistors).
- Jitter from Windows scheduling would cause misfires.

**This is what dSPACE/NI hardware does** — custom FPGA boards with microsecond I/O. Not a Python job.

---

## Existing Open-Source HC11 Emulators (Research)

| Project | Language | HC11 Support | Status | Useful? |
|---------|----------|-------------|--------|---------|
| **EVBU** (tonypdmtr/EVBU) | **Python 3** | Full HC11 + Buffalo monitor | Active (2019), GPL-2.0 | **YES — reference for our emulator** |
| **sim68xx** (dg1yfe/sim68xx) | C | 6800/6801/6303/6805/**6811** | Mature (1994-2011), GPL-2.0 | Good reference — bus-cycle-level sim |
| **Sim11** (Toronto Met U) | ? | Full bus-cycle simulation | Academic | Architecture reference |
| **THRSim11** | Windows | Full HC11 simulator + assembler | Commercial (shareware) | Good for validation but closed-source |
| **GDB m6811-elf** | C | Full HC11 simulation via GDB | Available as `m6811-elf-gdb` | **YES — can run binary directly for validation** |

### Key Insight: EVBU (Python)

The **EVBU** project on GitHub is a **Python 3 68HC11 simulator** with wxPython GUI. It includes:
- Full instruction set execution (`PySim11/` directory)
- Buffalo EPROM monitor emulation
- Memory display, register tracking
- Open source (GPL-2.0)

Our emulator architecture is already similar but more modular. We can cross-reference EVBU's opcode implementations for validation.

### Key Insight: GDB m6811-elf

We already have GDB with HC11 simulation built in (`m6811-elf-gdb`). This can:
- Load our binary as an ELF (via objcopy)
- Single-step through instructions
- Set breakpoints at XDF addresses
- Inspect registers and memory

This is a **free validation oracle** for our Python emulator — we can compare outputs step-by-step.

---

## Recommended Implementation Plan

### Phase 1: Table Lookup Simulator (Week 1)

Build in `hc11_virtual_emulator/src/` — a new module `table_sim.py`:

1. Parse `Enhanced_v209b_export.json` → load all 330 tables with axes and scaling
2. Read `VY_V6_Enhanced.bin` → extract raw table data at XDF addresses
3. Build interpolation engine (bilinear for 2D tables, linear for 1D)
4. Create CLI: `python -m table_sim --rpm 3000 --map 80 --coolant 90`
5. Output: spark advance, fuel base PW, VE, injector offset, shift points

### Phase 2: Bank Switching + Interrupts (Weeks 2-3)

Upgrade the existing emulator:

1. Add bank switching to `memory.py` — 3 × 32KB banks, PORTG bit selects active bank
2. Implement interrupt dispatch in `emu.py` — vector table at $FFC0-$FFFF, priority handling
3. Add COP watchdog auto-feed (or disable via config)
4. Map ADC channels to VY V6 sensors using XDF channel assignments
5. Generate virtual crank signal → TIC3 interrupts at configurable RPM

### Phase 3: "Run the Binary" MVP (Week 4)

1. Load `VY_V6_Enhanced.bin` into emulator (all 3 banks)
2. Set PC from reset vector ($C011)
3. Inject sensor values: RPM=800, TPS=0%, MAP=30kPa, coolant=90°C
4. Run main loop → watch it initialize, enter idle, stabilize
5. Ramp RPM → watch rev limiter engage
6. Log spark advance, injector PW, dwell time to CSV for visualization

### Phase 4: Interactive Dashboard (Month 2+)

- PySide6/Dear ImGui GUI with:
  - Virtual gauges: RPM, MAP, coolant temp, spark advance
  - Slider inputs: TPS, vehicle speed, gear selector
  - Memory viewer: watch RAM variables in real-time
  - Trace viewer: instruction-by-instruction execution log
  - Breakpoint management: stop at specific addresses

---

## Technical Risks

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **Unknown I/O register behavior** | Code hangs waiting for hardware response | Map all 64 I/O registers, implement stubs that return sensible defaults. Cross-ref with HC11F1 datasheet. |
| **SPI slave select for external ADC** | ADC reads fail → code thinks sensors are dead | Implement SPI model that returns injected sensor values when ADC slave is selected |
| **Immobilizer / anti-theft** | Code enters limp mode or refuses to run | Identify immobilizer routine in disassembly, patch it out (NOP) or satisfy its check |
| **Undocumented bank switch timing** | Bank 2/3 code unreachable or wrong code executes | Study `analyze_bank_switching.py` output, verify PORTG bit mapping with binary analysis |
| **Interrupt timing sensitivity** | Main loop depends on precise interrupt intervals | Use cycle-counted interrupt scheduling (TIC3 fires every N cycles based on RPM) |
| **Checksum validation at startup** | Code detects corrupted ROM and halts | Find checksum routine, either patch it or ensure our memory image passes |

---

## Summary: What's Possible Today

```
┌─────────────────────────────────────────────────────────────┐
│                    FEASIBILITY MATRIX                        │
├──────────────────────┬──────────┬───────────┬──────────────┤
│ Capability           │ Possible │ We Have   │ Build Time   │
├──────────────────────┼──────────┼───────────┼──────────────┤
│ Table lookups        │ YES      │ XDF+BIN   │ 1-2 days     │
│ Opcode execution     │ YES      │ 80% done  │ Done (tests) │
│ Bank switching       │ YES      │ Binary    │ 1-2 days     │
│ Interrupt dispatch   │ YES      │ Vectors   │ 3-5 days     │
│ Virtual sensors      │ YES      │ ADC stub  │ 1-2 days     │
│ Run main loop        │ YES      │ All above │ 2-4 weeks    │
│ Full engine model    │ HARD     │ Partial   │ 2-6 months   │
│ Real-time HIL        │ NO       │ N/A       │ N/A          │
├──────────────────────┴──────────┴───────────┴──────────────┤
│ VERDICT: Level 1-2 are absolutely buildable with what we   │
│ have. Level 3 is achievable but requires engine modeling   │
│ expertise. Level 4 is not practical in Python on Windows.  │
│                                                            │
│ CPU ONLY — no GPU needed. Python on any modern CPU will    │
│ emulate the 2 MHz HC11 at 1000x+ real-time speed.         │
└────────────────────────────────────────────────────────────┘
```

---

## File Locations Quick Reference

```
Binary:
  VY_V6_Enhanced.bin                                                128KB ROM dump (Enhanced v1.0a)

XDF Definition:
  VX VY_V6_$060A_Enhanced_v2.09b.xdf

XDF Exports (machine-readable):
  xdf_exports/Enhanced_v209b_export.json                              1.2 MB — all 2,234 defs
  xdf_exports/Enhanced_v209b_export.md                                458 KB — human-readable
  xdf_exports/Enhanced_v209b_export.txt                               448 KB — flat text

Bank-Split Binaries:
  bank_split_output/Enhanced_v1.0a_bank1.bin                          64KB  (RAM+IO+Cal+Code+Vectors)
  bank_split_output/Enhanced_v1.0a_bank2.bin                          32KB  (Engine code overlay)
  bank_split_output/Enhanced_v1.0a_bank3.bin                          32KB  (Trans/diag overlay)

Disassembly (4 tools, cross-verified at hook point $81E1):
  bank_split_output/Enhanced_v1.0a_bank{1,2,3}.asm                    Capstone M680X
  bank_split_output/Enhanced_v1.0a_bank{1,2,3}_gnu.asm                GNU m6811-elf
  bank_split_output/Enhanced_v1.0a_bank{1,2,3}_udis.asm               udis (linear sweep)

Existing Emulator (46/46 tests passing):
  hc11_virtual_emulator/src/emu.py                                    Main emulator class
  hc11_virtual_emulator/src/cpu/                                      CPU core (decoder, ALU, regs)
  hc11_virtual_emulator/src/mem/                                      Memory map (64K, I/O routing)
  hc11_virtual_emulator/src/periph/                                   SCI, ADC, Timer, Ports
  hc11_virtual_emulator/src/aldl/                                     ALDL Mode 4 harness

Analysis Tools:
  tools/                                                              Binary analysis, XDF parsing, ISR tracing

Validation Oracle:
  m6811-elf-gdb                                                       GDB with HC11 simulation (cross-check)
```
