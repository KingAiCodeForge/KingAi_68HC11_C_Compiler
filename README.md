# KingAI 68HC11 C Compiler — v0.2.0-alphaP, need experts in RE and embedded systems and software dev and systems engineering

A subset-C cross-compiler targeting the Motorola 68HC11, built for writing custom code patches for Delco automotive ECUs (Holden VN–VY V6, GM OBD1).

**Status: alpha / proof of concept.** Built in a single overnight session. It compiles C to HC11 assembly text — it does not produce binary ROMs. You still need a separate assembler (AS11, ASM11, etc.) and a way to patch the output into your PROM image. A built-in assembler pass is planned but the existing DOS-era tools (AS11, ASM11) don't run on modern Windows 10/11 — if anyone has documentation on the HC11 object code encoding or a working cross-assembler, that would unblock this.

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

## What It Does NOT Do

- **No binary output** — generates assembly text, not machine code. Pipe through an HC11 assembler.
- **No linker** — can't patch output into an existing ROM image. Manual placement required.
- **No structs or arrays** — parser recognizes them but codegen doesn't handle them yet.
- **No multi-file compilation** — single translation unit only.
- **No standard library** — no printf, no malloc, nothing. This is bare-metal embedded.
- **No floating point** — HC11 has no FPU. Integer math only.
- **Stack frame tracking is simple** — works for typical ECU functions (few locals, no deep nesting). Complex nested scoping may produce incorrect offsets.
- **Not validated against hardware** — the assembly output has been checked for instruction correctness against the HC11 reference manual, but nobody has burned a PROM with this output yet.

## Quick Start

```bash
# Clone and install
git clone https://github.com/KingAiCodeForge/KingAi_68HC11_C_Compiler.git
cd KingAi_68HC11_C_Compiler
pip install -e .

# Compile a C file to HC11 assembly
python hc11cc.py examples/blink.c --target vy_v6

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
; KingAI 68HC11 C Compiler Output
; Target: VY V6 PCM (09356445) - HC11F1, 128KB bank-switched
        ORG     $8000

main:
        PSHX
        TSX
        DES                     ; local: unsigned char x
        LDAA    #$00
        TSX
        STAA    0,X             ; store x
.while1:
        LDAA    0,X             ; load x
        TAB
        LDAA    #$01
        ABA                     ; 8-bit add
        TSX
        STAA    0,X             ; store x
        LDAA    0,X             ; load x
        STAA    $1000           ; volatile I/O write
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
  lexer.py             — Tokenizer (511 lines)
  ast_nodes.py         — AST node definitions (325 lines)
  parser.py            — Recursive-descent parser (770 lines)
  codegen.py           — HC11 code generator (1528 lines)
  optimizer.py         — Peephole optimizer (203 lines)
examples/
  delco_hc11.h         — HC11F1 register definitions
  blink.c, adc_read.c, isr_example.c
tests/
  test_compiler.py     — 30+ tests (pytest)
```

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```

## Who Is This For

People who:
- Already understand Delco PCM firmware at the assembly level
- Want to write custom ECU logic in C instead of hand-assembling HC11
- Are comfortable with the manual steps: compile → assemble → patch into ROM → burn PROM
- Know the risks of running custom code on an engine controller

This is not a "flash and go" tuning tool. It's a compiler.

## Looking for Collaborators

This project is a **template** — the architecture (lexer → parser → AST → codegen) is designed to be replicated for other ECU processor targets. The plan is separate repos for each backend:

| Processor | ECU families | Status | What's needed |
|-----------|-------------|--------|---------------|
| **68HC11** (this repo) | Delco VN–VY V6, 1227730, 16197427 | Alpha — compiles to assembly | Hardware validation, codegen fixes |
| 68K / 68332 | Later Delco P01/P59, other GM | Not started | Someone with full opcode map + memory layout |
| ? | Ford EEC-IV | Not started | Someone with full opcode map + memory layout |
| c166/167 | TBD | TBD | TBD |

**Why HC11 first?** The Delco 68HC11 PCMs have excellent community documentation — XDF definitions on pcmhacking.net, well-mapped register layouts, and a known instruction set with plenty of reference material. That made it possible to build a working compiler without owning every variant of hardware.

**Other processors are a different story.** A new backend needs someone who has already done the hard work: full opcode table with encodings and cycle counts, complete memory map of the target ECU (RAM, ROM, I/O, vectors, bank switching), and ideally existing disassemblies to validate against. The compiler architecture is reusable — the lexer, parser, AST, and optimizer are processor-independent. Only the codegen module needs to be rewritten per target. But without the opcode and memory map groundwork already done, there's nothing to generate *to*.

If you've already mapped out another ECU family at that level, let's talk.

Open an issue or PR — the codebase is small (~3,300 lines total) and readable.

## Known Limitations & Future Work

- Assembler pass (emit binary, not text) — would eliminate the need for external AS11
- Linker with symbol import — patch compiled functions into stock firmware at known addresses
- Struct and array support in codegen
- Register allocation improvements (currently spills to stack aggressively)
- 68K/68332 backend — different instruction set, would need a new codegen (not a trivial extension)

## License

MIT — see `LICENSE`.

## Contributing

See `CONTRIBUTING.md`. The most useful contributions right now:

1. **Hardware validation** — compile something, assemble it, burn it, report what happened
2. **Bug reports** — C input + expected assembly vs actual assembly
3. **Codegen fixes** — the HC11 instruction selection can always be tighter
4. **New target profiles** — if you know the memory map of a Delco PCM not listed above
