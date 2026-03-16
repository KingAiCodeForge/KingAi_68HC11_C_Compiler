# VY V6 $060A Enhanced OS — Bin Splits & Disassembly

## Source Material
- From VY_V6_Assembly_Modding repo — bank switching analysis, 24X handler disassembly, period analysis
- From extracted_ose_flash_tool repo — OSE Flash Tool V1.5.1 decompiled (full flash protocol)

## Bank Splitting — Confirmed from OSE Flash Tool Defines (line 25338+)

The OSE Flash Tool's `Defines` class hardcodes ALL the address maps for every supported config. For VY V6:

### 128K Layout (OSE Enhanced $060A)
```
Full Bin:  0x00000 - 0x1FFFF  (131,072 bytes = 128KB)
Cal:       0x02000 - 0x05FFF  (16,384 bytes = 16KB)
ALDL:      0x01280 - 0x017FF  (1,408 bytes for ALDL definitions)
Checksum:  0x08000 - 0x0FFFF  (32KB verification region)
CS Addr:   0x04006            (checksum stored at 16390)
M16 Range: 0x01280 - 0x0FFFF  (Mode 16 range)
```

### Bank Layout for Flash Operations
The 128K flash chip (typically Am29F010 or SST39SF010) is organized as:
- **Sector size: 16KB (0x4000 bytes)**
- **8 sectors total** to make 128KB
- Erase is per-sector, write is per-byte/16-byte-block

From `ALDLWriteBinCalVXYFlash()` (line 24082+):
- Bank parameter `0x48` (72 decimal) is used for sector operations
- Sector parameter `0x40` (64 decimal) for cal-only erase
- Full bin write: erase all sectors, then write all 128KB
- Cal-only write: erase cal sector(s) only, write 16KB

### Flash Write Timing (Approximate)

> **TODO:** Actual throughput needs measuring. Previous estimate of 8192 baud was wrong.
> Real-world is closer to ~5 kbps effective with 32-byte block writes.
> 64-byte blocks not yet tested — may improve throughput if the flash chip supports it.

```
Effective rate: ~5 kbps (32-byte blocks over ALDL serial)
128KB full write:  128KB × 8 / 5000 ≈ 210s ≈ ~3.5 min (needs real-world timing)
16KB cal write:    16KB × 8 / 5000 ≈ 26s  ≈ ~30 sec
```
These are rough estimates — actual time depends on per-block ACK overhead,
sector erase delays, and whether the tool uses 32 or 64 byte write blocks.

### Checksum Auto-Fix (line 24157+)
The OSE tool auto-fixes checksums before writing:
```
checksum_addr = 16390 (0x4006)  
sum = sum of bytes 0x2000 to 0x1FFFF, skipping 0x4000-0x4007
stored_cs = WriteBin[16390]*256 + WriteBin[16391]
if sum != stored_cs: fix the bytes at 16390-16391
```

## Assembly Disassembly Context
Refer to VY_V6_Assembly_Modding repo for:
- `TIC3_ISR_ANALYSIS.md` — 24X crank signal handler
- `BANK_SWITCHING_AND_ISR_ANALYSIS.md` — Full period/timing analysis
- `4L60E_VY_V6_TUNING_MASTER.md` — Transmission tuning
- `68HC11_C_COMPILER_ANALYSIS.md` — How the C compiler targets this CPU
- Bank switching documentation in the bank switch subfolder

## Related Tool Analysis
See the Red Devil River ALDL Cable repo for:
- Complete OSE Flash Tool protocol analysis
- Python port of ALDL protocol
- Transport layer options (pyserial, D2XX, pyftdi)
- Comparison of 15+ flash tools and their methods

## Disassembly File Status (2026-02-20)

| File Suffix | Tool | Status | Notes |
|-------------|------|--------|-------|
| `bank{N}.asm` | Custom HC11 disassembler | **OK** | Full coverage to $FFFE, labeled vectors |
| `bank{N}_labeled.asm` | Custom HC11 disassembler | **OK** | Same with extra label definitions |
| `bank{N}_gnu.asm` | m68hc11-elf-objdump | **Partial** | bank1 stops at ~$AA40 (skips 0x00-fill free space + vectors) |
| `bank{N}_udis.asm` | udis (Jeff Tranter) | **TRUNCATED** | Needs re-disassembly after bug fix (see below) |
| `bank{N}_udis_labeled.asm` | udis + labels | **TRUNCATED** | Same |

### Fixes Applied 2026-02-20

1. **udis/6811.py** — 3 opcode table bugs fixed:
   - NEGA (0x40): length 3→1, NEGB (0x50): length 3→1
   - CLR indexedy: opcode 0x187F→0x186F
   - These caused all _udis files to hit EOF early (wrong byte count consumed from file)

2. **bank3.asm / bank3_labeled.asm** — Last 3 interrupt vectors ($FFFA/$FFFC/$FFFE) corrected:
   - Were: `subb #21/#25/#17` (disassembler decoded 0xC0 as SUBB instruction)
   - Now: `.word $C015/$C019/$C011` (actual address pointers to bank3 handlers)
   - Bank 3 uses direct address pointers for COP/CMF/RESET, not BRA trampolines like banks 1&2
