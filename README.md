# KingAI 68HC11 C Compiler — v0.3.0-alpha

A subset-C cross-compiler targeting the Motorola 68HC11, built for writing custom code patches for Delco automotive ECUs (Holden VN–VY V6, GM OBD1).

**Status: alpha — compiles C to HC11 assembly, assembles to binary/S19, patches into ROMs.** The complete pipeline (C → ASM → binary → patched PROM) works end-to-end. Hardware validation on a real ECU is the remaining gate.

## What It Does Right Now

The compiler handles a practical subset of C and generates real 68HC11 instructions:

- **Data types**: `unsigned char` (8-bit → AccA), `int` (16-bit → AccD), pointers (16-bit)
- **Arithmetic**: `+ - * / %` — uses ABA/SBA for 8-bit, ADDD/SUBD for 16-bit, MUL, IDIV
- **Bitwise**: `& | ^ ~ << >>` — ANDA, ORAA, EORA, ASLA/ASLD, LSRA/LSRD
- **Comparisons**: `== != < > <= >=` — sets condition codes, branches with BEQ/BNE/BLT/BGE etc.
- **Control flow**: `if/else`, `while`, `do-while`, `for`, `break`, `continue`, `return`
- **Pointers**: dereference (`*ptr`), address-of (`&var`), volatile I/O (`*(volatile unsigned char *)0x1030`)
- **Inline assembly**: `asm("LDAA $1030");` — drops raw HC11 instructions into the output
- **ISR support**: `__attribute__((interrupt))` generates proper RTI epilogue
- **Zero-page placement**: `__zeropage` qualifier allocates variables in direct-page RAM ($00–$FF)
- **Peephole optimizer**: 13 rules that clean up redundant instructions (TSX dedup, push/pop elimination, while(1) optimization, dead TSTA removal)
- **Target profiles**: memory maps for `generic`, `vy_v6` (09356445), `1227730`, `16197427`
- **Built-in assembler**: 146 mnemonics, 261 opcode entries, two-pass label resolution, Motorola S19 + raw binary + listing output — no external assembler needed
- **Unified toolkit** (`hc11kit`): 9-command CLI — assemble, disassemble, compile, patch ROMs, find free space, verify/fix checksums, convert addresses, parse XDFs, identify binaries

## Current State & Limitations

| Area | Status |
|------|--------|
| **Output format** | Assembly text, raw binary, or Motorola S19 — built-in assembler, no external tools needed |
| **ROM patching** | `hc11kit patch` injects code + installs JSR hook + verifies in one command |
| **Structs / arrays** | Parsed by the front-end but not handled in codegen yet |
| **Multi-file** | Single translation unit only, no `#include` resolution beyond `#define` |
| **Standard library** | None — no libc, no printf, no malloc. Bare-metal embedded. |
| **Floating point** | Not supported — HC11 has no FPU, integer arithmetic only |
| **Stack frames** | Simple tracking — works for typical ECU routines (few locals, shallow nesting). Deep or complex scoping may produce wrong offsets |
| **Hardware validation** | Assembly verified against HC11 reference manual + instruction encodings validated byte-by-byte. **Not yet tested on physical hardware** |

This tool is for generating assembly for direct, simple, single-file embedded routines — not for compiling general-purpose C programs.

## Quick Start

```bash
# Clone and install
git clone https://github.com/KingAiCodeForge/KingAi_68HC11_C_Compiler.git
cd KingAi_68HC11_C_Compiler
pip install -e .

# Compile a C file to HC11 assembly
python hc11cc.py examples/blink.c --target vy_v6

# Compile C directly to binary
python hc11kit.py compile examples/rpm_limiter.c -o rpm_limiter.bin --target vy_v6

# Assemble a hand-written .asm file
python hc11kit.py asm spark_cut.asm -o spark_cut.bin

# Patch compiled code into a stock ROM binary
python hc11kit.py patch stock.bin patch.asm --at 0x5D05 --hook 0x101E1:3 --verify

# Find free space in a binary
python hc11kit.py free ECU.bin --min-size 64

# Or use the Python API
python -c "
from hc11_compiler import compile_source
print(compile_source('void main() { *(volatile unsigned char *)0x1000 = 0x55; }', target='vy_v6'))
"
```

## Example Output

Input:
```c
void main() {
    unsigned char x;
    x = 0;
    while (1) {
        x = x + 1;
        *((volatile unsigned char *)0x1000) = x;
    }
}
```

Output (abbreviated):
```asm
; ============================================
; KingAI 68HC11 C Compiler Output
; Target: VY V6 PCM (09356445) - HC11F1, 128KB bank-switched
; ============================================

; -- Memory Configuration --
        ORG     $8000

; -- Code --

        ; Function: main
main:
        PSHX
        TSX
        DES
        ; local: unsigned char x
        LDAA    #$00
        TSX
        STAA    0,X  ; x
.while1:
        TSX
        LDAA    0,X  ; x
        PSHA
        LDAA    #$01
        TAB
        PULA
        ABA
        TSX
        STAA    0,X  ; x
        TSX
        LDAA    0,X  ; x
        STAA    $1000  ; *($1000) = A direct
        BRA     .while1
```

## Target PCM Profiles

| Target | PCM | RAM | ROM | Notes |
|--------|-----|-----|-----|-------|
| `generic` | Any HC11 | $0000–$00FF | $8000–$FFFF | Default, conservative |
| `vy_v6` | 09356445 | $0000–$03FF | $8000–$FFFF (banked) | Holden VY V6, HC11F1 |


## Project Structure

```
hc11_compiler/
  __init__.py          — Public API (compile_source)
  lexer.py             — Tokenizer (498 lines)
  ast_nodes.py         — AST node definitions (267 lines)
  parser.py            — Recursive-descent parser (656 lines)
  codegen.py           — HC11 code generator (1325 lines)
  optimizer.py         — Peephole optimizer (170 lines)
  assembler.py         — Two-pass assembler, 146 mnemonics (1037 lines)
hc11cc.py              — Standalone compiler CLI (184 lines)
hc11kit.py             — Unified 9-command toolkit CLI (1024 lines)
examples/
  delco_hc11.h         — HC11F1 register definitions + VY V6 RAM addresses
  blink.c, adc_read.c, isr_example.c, rpm_limiter.c,
  sci_serial.c, timer_delay.c, test_rpm.c
tests/                   (gitignored — internal only)
  test_compiler.py     — 40 compiler tests (pytest)
  test_asm_smoke.py    — 34 assembler tests (pytest)
```

Total: ~5,200 lines of compiler + toolkit code. 74/74 tests passing.

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```

## Who Is This For

People who:
- Already understand Delco PCM firmware at the assembly level
- Want to write custom ECU logic in C instead of hand-assembling HC11
- Need the full pipeline: C source → compiled binary → patched ROM image
- Know the risks of running custom code on an engine controller
- want ida pro and other tools functional on python on window 10/11 pcs as a light all in one opensource repo that is free and fully opensource, no compiled pe or exe here, hopefully this idea get some people involved so i who lov coding and pcmhacking and knowledge sharing or learning. if you spot a error please do a PR or send me the fix. on facebook pcmhacking forum or through github PR and issues. any ideas or questions put in issues.
This is not a "flash and go" tuning tool. It's a C compiler + assembler + ROM patcher for bare-metal ECU work. 

## Looking for Collaborators

This project is a **template** — the architecture (lexer → parser → AST → codegen) is designed to be replicated for other ECU processor targets. The plan is separate repos for each backend:

| Processor | ECU families | Status | What's needed |
|-----------|-------------|--------|---------------|
| **68HC11** (this repo) | Delco VN–VY V6, 1227730, 16197427 | Alpha — full C→binary pipeline, 74/74 tests | Hardware validation, array/struct codegen |
| 68K / 68332 | Later Delco P01/P59, other GM | Not started | Someone with full opcode map + memory layout |
| ? | Ford EEC-IV | Not started | Someone with full opcode map + memory layout |
| c166/167 | TBD | TBD | TBD |

**Why HC11 first?** The Delco 68HC11 PCMs have excellent community documentation — XDF definitions on pcmhacking.net, well-mapped register layouts, and a known instruction set with plenty of reference material. That made it possible to build a working compiler without owning every variant of hardware.

**Other processors are a different story.** A new backend needs someone who has already done the hard work: full opcode table with encodings and cycle counts, complete memory map of the target ECU (RAM, ROM, I/O, vectors, bank switching), and ideally existing disassemblies to validate against. The compiler architecture is reusable — the lexer, parser, AST, and optimizer are processor-independent. Only the codegen module needs to be rewritten per target. But without the opcode and memory map groundwork already done, there's nothing to generate *to*.

If you've already mapped out another ECU family at that level, let's talk.

Open an issue or PR — the codebase is small (~5,200 lines total) and readable.

## hc11kit — Unified Toolkit

`hc11kit.py` consolidates the complete ECU development workflow into one CLI:

| Command | What it does |
|---------|-------------|
| `hc11kit asm` | Assemble .asm → .bin / .s19 / .lst |
| `hc11kit disasm` | Disassemble binary range with bank awareness |
| `hc11kit compile` | C → ASM → binary / S19 (full pipeline) |
| `hc11kit patch` | Inject code + install JSR hook + verify |
| `hc11kit free` | Find free (unused) regions in a binary |
| `hc11kit checksum` | Verify or fix GM ROM checksum |
| `hc11kit addr` | Convert between file offset, CPU address, and bank |
| `hc11kit xdf` | Parse and search TunerPro XDF definitions |
| `hc11kit info` | Identify and summarize a binary file |

## Companion Repository — VY V6 ASM Patches

This compiler is built alongside a work in progress[kingaustraliagg-vy-l36-060a-enhanced-asm-patches](https://github.com/KingAiCodeForge/kingaustraliagg-vy-l36-060a-enhanced-asm-patches) — a collection of 50+ hand-written and opus 4.6 generated 68HC11 assembly patches for the Holden VY V6 Ecotec L36 ($060A Enhanced binary, Delco 92118883).

That repository contains:
- **Spark cut limiter** patches (Chr0m3 dwell method, The1's CPD method, progressive/rolling/two-stage variants) all work in progress.
- **MAFless / Alpha-N / Speed Density** conversions
- **Turbo boost control**, overboost protection, antilag
- **Launch control**, flat shift, no-lift shift
- **Full binary disassemblies** split by bank
- **XDF definitions** for VS, VT, VX, VY (V6 NA, V6 S/C, V8) — all with 68 DTC flags
- **RAM validation research** ($0046 bit analysis, $01A0 scratch byte, runtime methodology)
- some bytes of free ROM space** mapped at $0C468–$0FFBF

All of that was done the old-school way: hand-written assembly, manually hex-patched into the binary with a hex editor with alot of time and manual effort in other tools open. Every patch is a `.asm` file that has to be assembled externally and byte-copied into the ROM image at the right offset.

**This compiler changes that workflow.** Once hardware-validated, the goal is to write those same patches in C instead of raw assembly — compile with `hc11cc`, assemble + inject with `hc11kit patch`, and skip the manual hex editing entirely. Same result, but maintainable, readable, and repeatable. The spark cut patch that took 38 hand-written versions could be a single C function: threshold check, fake period injection, done.

The two repos target the same ECU, the same binary, and the same hook points. This one builds the toolchain; that one has the patches and research.

## End Goals — What This Enables

Right now, writing a custom ECU patch for a Holden VY V6 looks like this: study the disassembly, hand-write 68HC11 assembly, manually calculate byte offsets, hex-edit the binary at the exact right position, pray you didn't get a branch offset wrong, burn the chip, and hope the engine starts. If something's wrong, you start over with a hex editor. That's 38 versions of a spark cut patch to get it right.

Once this compiler is hardware-validated, the same workflow becomes: write a C function, run one command, get a patched binary. Here's what that actually unlocks:

### Write ECU patches in C instead of hand-written assembly

Instead of tracking AccA vs AccB, remembering which branch instruction is signed vs unsigned, and counting stack offsets by hand — write readable C and let the compiler handle it. A spark cut limiter that was 30 lines of carefully hand-crafted assembly becomes:

```c
void spark_cut_hook() {
    unsigned char rpm = *(volatile unsigned char *)0x00A2;  // RPM × 25
    if (rpm > 240) {  // 6000 RPM threshold
        *(volatile int *)0x017B = 0x3E80;  // Inject fake dwell period
    }
}
```

One command: `python hc11kit.py patch enhanced.bin spark_cut.c --at 0xC468 --hook 0x101E1:3 --verify`

The compiler generates correct HC11 instructions, the assembler produces the binary, and hc11kit injects it at the free space address and installs the JSR hook — all verified, checksummed, done. No hex editor.

### Iterate on patches in minutes instead of hours

Hand-written assembly means every change requires re-counting offsets, checking for register clobbers, and redoing the hex math. With C, you change the threshold from 240 to 220, recompile, repatch. The 38-version history of the spark cut patch could have been 38 recompiles, not 38 rewrites.

### Make ECU patching accessible to more people

Most people who understand how engines work and can tune with TunerPro can also read simple C. Almost nobody outside the hardcore pcmhacking community can hand-write correct HC11 assembly and hex-patch binaries. This bridges that gap. If you can write `if (rpm > threshold)` you can write ECU patches — the compiler handles the instruction encoding, stack frames, and branch calculations.

### Build a custom Enhanced OS from source

The long-term goal: instead of binary-patching one feature at a time into The1's Enhanced v1.0a binary, build a complete set of patches from C source files — spark cut, launch control, MAFless, flat shift — all compiled and injected together. Version-controlled, rebuildable, portable to other OSIDs by changing the target profile. An open-source custom operating system extension for these ECUs, compiled from readable source instead of maintained as raw hex diffs.

### Enable the same approach for other ECU platforms

The compiler architecture is processor-independent up to the code generator. The lexer, parser, AST, and optimizer are reusable as-is. A new ECU target (68K, C166, Ford EEC-IV) only needs a new codegen module and target profile — the rest of the pipeline carries over. Someone with a fully mapped P01/P59 or EEC-IV could fork this repo, write a new code generator, and have the same C-to-binary pipeline for their platform. The concepts (find free space, install JSR hook, inject compiled code, verify checksums) apply to every ECU that runs from ROM/Flash.

### Specific features this makes practical

| Feature | Why it needs a compiler | Current status |
|---------|------------------------|----------------|
| **Spark cut rev limiter** | Code injection at hook point, RPM comparison, dwell manipulation | 38 hand-written ASM versions exist — ready to rewrite in C |
| **MAFless / Alpha-N** | Force TPS-based load calc, bypass MAF DTC, multiple RAM writes | Concept ASM exists — too complex to maintain by hand long-term |
| **Speed Density (full VE table)** | Lookup table interpolation, MAP sensor reading, injector PW calculation | Needs arrays/structs in codegen (planned) |
| **Launch control / two-step** | Clutch input reading, RPM window management, state machine | Perfect candidate for C — too many branches for comfortable hand-asm |
| **Flat shift / no-lift shift** | Gear detection, RPM-based spark cut during shifts, timing retard | Multiple I/O reads + state tracking = messy in raw assembly |
| **PID boost controller** | Math-heavy (proportional + integral + derivative), wastegate duty cycle | Nearly impossible to maintain as hand-written HC11 assembly |
| **Antilag** | Timing retard + fuel enrichment + state management per-cylinder | Complex enough that C readability is essential |
| **Multi-patch builds** | Combine 5+ patches into one binary without offset conflicts | Compiler + linker handles address allocation automatically |

### What's still needed to get there

1. **Hardware validation** — compile a simple patch, burn it, scope the EST output, confirm the instructions execute correctly on real silicon. This is the gate. Everything else is blocked on this.
2. **Array/struct codegen** — the parser already handles `unsigned char buf[8]` and `struct sensor { ... }`. The code generator needs to emit correct indexed addressing for array access and struct member offsets. Required for VE tables and lookup-based patches.
3. **Real-world testing** — someone with a VY V6, an Ostrich 2.0 or NVRAM board, and an oscilloscope. Compile `examples/blink.c`, patch it in, watch the port toggle. That's the proof.

## Known Limitations

- ~~Assembler pass~~ **DONE** — built-in two-pass assembler, no external tools needed
- ~~Linker / ROM patcher~~ **DONE** — `hc11kit patch` handles code injection + hook installation
- Struct and array support in codegen — parser handles them, codegen is stubbed
- Register allocation improvements — currently spills to stack aggressively
- Hardware validation — needs bench test on real ECU with oscilloscope
- 68K/68332 backend — different instruction set, would need a separate repo. The compiler architecture (lexer/parser/AST/optimizer) is reusable, only codegen needs rewriting per target. Applicable to any ECU platform with a known opcode map and memory layout.

## License

MIT — see `LICENSE`.

## Contributing

See `CONTRIBUTING.md`. The most useful contributions right now:

1. **Hardware validation** — compile a C function, use `hc11kit patch` to inject it, burn it, report what happened
2. **Bug reports** — C input + expected assembly vs actual assembly
3. **Array/struct codegen** — the parser handles these, but codegen needs implementation
4. **New target profiles** — if you know the memory map of a Delco PCM not listed above
5. Note to self or forkers - Check the gitignore to understand how it ignores tests and ignore folders. theses are for plans and research and internal stuff not needed for public github.