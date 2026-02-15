# HC11 Virtual Emulator

**Status:** Scaffold complete — 46/46 integration tests passing (Feb 15, 2026)

Software-only 68HC11 CPU emulator for validating compiler output without
physical hardware. Feed it a compiled binary, it simulates the CPU executing
instructions, and you inspect the results.

## What Works Right Now

- **Full CPU core:** All 256 page-1 opcodes + page 2/3/4 (Y-indexed, CPD, etc.)
- **All addressing modes:** INH, IMM8, IMM16, DIR, EXT, INDX, INDY, REL, BIT2/3
- **Complete ALU:** 8-bit and 16-bit add/sub/and/or/xor/shift/rotate with correct
  HC11 flag semantics (H, N, Z, V, C)
- **SCI peripheral:** TX output capture, RX injection (ALDL simulation)
- **ADC peripheral:** 8-channel sensor value injection with instant conversion
- **Timer peripheral:** TCNT free-running counter, OC1-5 compare, prescaler
- **I/O Ports:** PORTA-E state tracking with change callbacks
- **Memory map:** 64K with ROM write protection, I/O handler routing, S19 loading
- **ALDL Mode 4 harness:** Frame builder, checksum validation, control byte API
- **RAM snapshots + watchpoints:** For DTC reverse engineering workflow
- **Breakpoints, trace logging, EEPROM persistence**

## What's Scaffold (Needs Cross-Reference Validation)

Every module is annotated with `SCAFFOLD` comments listing what needs
cross-referencing before being considered production-quality:

| Module | Cross-reference needed |
|--------|----------------------|
| decoder.py | Validate all page 2/3/4 opcodes against Motorola RM Appendix A |
| alu.py | V flag formula byte-for-byte against EVBU PySim11/ops.py |
| emu.py | DAA instruction is stubbed (low priority — compiler doesn't emit it) |
| mode4_harness.py | Mode 1 data stream offsets need live ALDL capture validation |
| adc.py | Channel assignments need VY V6 stock XDF verification |
| ports.py | PORTB bit→relay mapping needs service manual confirmation |
| timer.py | Output compare match action (pin toggle) not implemented |

## Usage

```python
from src.emu import HC11Emulator, StopReason

emu = HC11Emulator()
emu.load_binary(open('hello.bin','rb').read(), base_addr=0x5D00)
emu.regs.PC = 0x5D00
result = emu.run(max_cycles=50000)
print(emu.sci.sci_output)  # b"HELLO\r\n"
```

## Tests

```bash
cd hc11_virtual_emulator
python tests/test_emulator_core.py
```

46 tests covering: load/store, arithmetic, branches, stack (JSR/RTS),
transfers, bit ops, SCI TX/RX, ADC channel read, multi-instruction programs,
ALDL hello world, memory watchpoints, RAM snapshot diffing, Mode 4 frame
construction and checksum validation.

## Directory Structure

```
hc11_virtual_emulator/
  src/
    emu.py              — Main emulator class (fetch-decode-execute loop)
    cpu/
      regs.py           — CPU register set + CCR flag management
      decoder.py        — Opcode table (all 4 pages, 300+ opcodes)
      alu.py            — ALU functions with flag computation
    mem/
      memory.py         — 64K memory map with I/O routing + watchpoints
    periph/
      sci.py            — SCI serial (ALDL TX/RX)
      adc.py            — A/D converter (sensor injection)
      ports.py          — Parallel I/O ports (PORTB relay tracking)
      timer.py          — Free-running timer + output compare
    aldl/
      mode4_harness.py  — ALDL Mode 4 frame builder + test harness
  tests/
    test_emulator_core.py  — 46 integration tests
  ignore/
    dev_research_plan_for_virtual_emulator.md  — Full development plan
```

## Cross-Reference Sources

These are the authoritative sources. When any scaffold code disagrees
with these, the source wins:

1. **Motorola MC68HC11 Reference Manual Rev3 (1991)** — opcode encoding
2. **Motorola MC68HC11F1 Technical Data (1990)** — VY V6 PCM chip, memory map
3. **tonypdmtr/EVBU** (github.com/tonypdmtr/EVBU) — Python HC11 sim, GPL-2.0
4. **hc11_compiler/assembler.py** — our own opcode table (313 entries)
5. **kingai_srs_commodore_bcm_tool** — ALDL protocol definitions, Mode 4 constants
6. **PCMHacking.net Topic 2460** — Mode 4 control byte documentation
7. **Stock $060A VY V6 binary** — real-world validation target

## Relationship to Other Projects

| Project | Relationship |
|---------|-------------|
| hc11_compiler/ | Produces the binaries this emulator runs |
| hc11_bench_incar_emulator/ | Tests same binaries on real hardware |
| examples/ | Primary test corpus — every example should run in emulator |
| TunerPro-XDF-BIN-Universal-Exporter/ | XDF parsing for bin→table display |
