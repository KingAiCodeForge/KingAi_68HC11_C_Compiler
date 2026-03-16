# VS Commodore V6 L36 — Real-Time Memcal Emulator (Conceptual Plan)

Why live tuning and emulators instead of pull-the-chip-and-burn cycles:

- **Map tracking and tracing** — TunerPro RT highlights which cells the ECU is actually reading in real time. You can see exactly where in the spark/fuel tables the engine is operating at any given RPM/load point, instead of guessing. would be good to get a cobra rtp to try this on a e38 ls2 6.0l to make a xdf with the live tracking. there is a 0.80 on pcmhacking.net that is 0.5 percent mapp
- **Human in the loop** — watch the AFR, knock, and timing values live, click the cell that's wrong, drag it, and the change takes effect immediately. No key-off, no EPROM pull, no 3-minute burn cycle.
- **Auto-tuner corrections** — log a drive, let the averaging/correction tools calculate the delta, write the corrected table back in one hit. Repeat until the whole map is dialled in.
- **No dyno required** — tune on the road under real driving conditions (heat soak, hills, overtaking load, cold starts). Dyno time is expensive and doesn't cover every cell in the map. Road tuning with live emulation covers the cells you actually use.
- **Dual-bank A/B testing** — flash two calibrations, flip between them with a switch or command, compare results back to back without any downtime.
- **Anyone can do the click-and-drag part** — once the hardware is working and the laptop is showing the live map, even a passenger can tap the red (lean/knock) cells and nudge them while the driver holds steady-state. Not ideal, but it works for filling in cells during highway cruising. For definition creation on PCMs and TCMs that have an EEPROM but no existing definition file, this workflow is essential.

> **STATUS: CONCEPTUAL / UNVERIFIED**
> Nothing in this document has been built or tested. Pinouts, addresses,
> protocols, and part selections are brainstorm-grade and need validation
> against real datasheets and hardware before any PCB is fabbed. Flux AI was
> tried ~1 year ago to generate a PCB layout but could not route the wires
> to components, so the design stalled at schematic stage.
>
> This may be useful to real-time emulator developers (CobraRTP, Moates)
> — some different parts are used here compared to their designs.
>
> Moates reopened (~2023) and products are available again at moates.net.
> CobraRTP FlashOnline protocol docs archived in `./hwflashonlineprotocols/`.

**Author**: KingAI (Jason King)  
**First written**: ~Nov 2025 (ChatGPT sessions)  
**Consolidated**: Feb 2026  
**Last updated**: Feb 19, 2026

### Cross-References (Feb 19, 2026)

| Related Project | Location | Relationship |
|----------------|----------|-------------|
| **SRAM Brick Recovery Device** | `../kingai_commie_flasher/ignore/sram_brick_recovery_device_plan.md` | Parallel design for flash-socket ECUs (VX/VY) — shares CY14B101NA, CPLD architecture, FlashOnline protocol. This plan is for memcal-socket ECUs (VS/VR). |
| **Verilog RTL** | `../kingai_hardware_project/memcal_emulator.v` | 397-line CPLD module used by both this plan and the SRAM device plan |
| **FlashOnline Protocol** | `../kingai_hardware_project/FLASHONLINE_PROTOCOL_INTEGRATION.md` | Protocol spec shared between this plan and SRAM device |
| **KingAI Commie Flasher** | `../kingai_commie_flasher/` | ALDL flash tool — prerequisite for validating any emulator hardware (bench setup, read/write round-trip) |
| **11P Disassembler** | `../11p-unlocking-and-re/split_and_disassemble_11p_64kb_version.py` | 808/424 binary analysis — understanding the 11P (memcal-based) binary layout informs what this emulator needs to serve |
| **11P Local Documentation** | `../VY_V6_Assembly_Modding/11p_local_documentation.md` | XDF address map and calibration analysis for 808/424 ECUs |
| **New Ideas Tracker** | `../kingai_commie_flasher/ignore/new_ideas_from_ant_emails_feb2026.md` | Master phased roadmap — this plan fits after Phase 2 (flash round-trip proven) |

---

## 1. What This Project Is

A drop-in replacement for the factory **27C010 EPROM** inside a Holden VS
Commodore V6 (L36 Ecotec) short memcal. The board plugs into the PCM's
memcal socket and provides:

- **Real-time tuning** via ALDL + TunerPro RT (same workflow as PCMHacking NVRAM kits)
- **Dual-bank switching** (two 128 KB images, selectable without removing the board)
- **Fast bulk-write** via USB or Bluetooth (FlashOnline-style loader protocol)
- **No battery** — uses FRAM or nvSRAM instead of Dallas DS1245Y

---

## 2. Design Revisions (Concept Only)

### Rev A — Minimum Viable (locked in concept)

**Goal**: Get a VS L36 running on a custom memcal board with zero extras.

| Block | Part | Package | Notes |
|-------|------|---------|-------|
| CPLD (glue) | EPM7064SLC44-10 | PLCC-44 | Gates CE/OE/WE, drives A17, BUS_HOLD logic |
| Memory | CY14B101NA | TSOP-II | 128K×8, 5 V nvSRAM, ~20–45 ns access |
| MCU | STM32F446RET6 | LQFP-64 | SPI→CPLD, GPIO→BUS_HOLD/IMAGE_SEL, SWD only |
| Buck 12→5 V | TPS54202-Q1 | SOT-23-6 | |
| LDO 5→3.3 V | TPS7A1601-Q1 | SOT-223 | Feeds MCU only (CPLD+nvSRAM run at 5 V) |
| Reverse-polarity | SI7141DP | — | Ideal PMOS on 12 V input |
| TVS (12 V) | SMBJ58A-Q | — | |
| ESD (headers) | TPD4E1U06-QDBVR | — | Optional |

**Connectors (Rev A)**:
- J1: ECU memcal edge (27C010-style, 32-pin)
- J2: 1×5 SPI header (GND, SCK, MOSI, MISO, CS_n)
- J3: 1×2 IMAGE_SEL header (+ 10 kΩ pulldown = default bank 0)
- J4: SWD header (3V3, SWDIO, SWCLK, NRST, GND)

**What Rev A intentionally omits**:
- USB-C / FlashOnline loader
- 3.3 V FRAM path (no level shifters needed — everything is 5 V)
- Wideband AFR gauge integration

**Tuning path**: TunerPro RT + $51 Enhanced XDF/ADX over ALDL. No OSE flashtool, no USB needed.

---

### Rev B — Planned Additions (concept only)

| Addition | Detail |
|----------|--------|
| USB-C (CDC) | FlashOnline-style bulk write/verify/bank-switch protocol |
| 3.3 V FRAM option | FM28V100-TG (TSOP-32) + 74LVC/AHCT level shifters |
| Bluetooth SPP | Optional — FlashOnline uses 115200–921600 baud BT |
| Wideband AFR | CJ125 + LSU 4.9 interface on a daughter board |
| Mobile app | KingsFlash (ESP32-based, separate project) |

---

## 3. Architecture Overview

```
ECU Memcal Edge (J1)
    │
    ├── A[0..16]  ───→  CPLD (U1, EPM7064S)  ───→  nvSRAM/FRAM (U2)
    ├── D[0..7]   ↔───  CPLD                 ↔───  nvSRAM/FRAM
    ├── CE_n      ───→  CPLD (gated)         ───→  nvSRAM/FRAM
    ├── OE_n      ───→  CPLD (gated)         ───→  nvSRAM/FRAM
    └── WE_n      ───→  CPLD (gated)         ───→  nvSRAM/FRAM
                          │
                          ├── A17 (bank select, from IMAGE_SEL register)
                          ├── BUS_HOLD_n (from MCU, active-low)
                          └── SPI (from MCU: SCK, MOSI, MISO, CS_n)
                                │
                          MCU (U3, STM32F446)
                            ├── SWD header (J4)
                            ├── SPI header (J2)
                            └── IMAGE_SEL header (J3)
```

**Signal flow**:
- **Normal**: ECU reads nvSRAM through CPLD as if it were a 27C010.
- **BUS_HOLD**: MCU asserts BUS_HOLD_n=0 → CPLD forces CE=OE=WE=1, tri-states D bus → MCU can safely write nvSRAM or switch banks.
- **Bank flip**: Only while held. Set IMAGE_SEL → updates A17 → release hold.

---

## 4. CPLD Behavioral Rules (Conceptual)

```
Pass-through (normal):
  CE_n → nvSRAM CE_n    (directly gated)
  OE_n → nvSRAM OE_n
  WE_n → nvSRAM WE_n
  A[0..16] → nvSRAM A[0..16]   (hard-wired in pass-through design)
  A17 → registered IMAGE_SEL value
  D[0..7] driven only when (~CE_n & ~OE_n & WE_n & BUS_HOLD_n)

BUS_HOLD (maintenance window):
  Force nvSRAM CE_n=1, OE_n=1, WE_n=1
  Tri-state D[0..7]
  MCU can now write nvSRAM or change A17

Banking:
  A17 = latched IMAGE_SEL (only update while held, CE_n=1, WE_n=1)
  Release: set IMAGE_SEL → confirm WE_n=1 → deassert BUS_HOLD_n
```

---

## 5. Net Names (Agreed Convention)

| Bus | Labels |
|-----|--------|
| Address | `A[0..16]` |
| Data | `D[0..7]` |
| ECU control | `CE_n`, `OE_n`, `WE_n` |
| MCU/CPLD control | `BUS_HOLD_n` (active-low), `IMAGE_SEL` |
| SPI | `SPI_SCK`, `SPI_MOSI`, `SPI_MISO`, `SPI_CS_n` |
| Power | `+12V`, `+5V`, `+3V3`, `GND` |
| MCU reset | `NRST` |

---

## 6. Memory Map (Conceptual)

| Bank | A17 | Address range | Content |
|------|-----|--------------|---------|
| 0 | 0 | 0x00000–0x1FFFF (128 KB) | Primary calibration |
| 1 | 1 | 0x20000–0x3FFFF (128 KB) | Alternate calibration |

Power-up default: Bank 0 (10 kΩ pulldown on IMAGE_SEL).

---

## 7. FlashOnline-Style Loader Protocol (Rev B Concept)

A clean, custom framed protocol over USB-CDC or UART. **Not** a copy of
FlashOnline or Moates — inspired by the same principle.

### Frame Format (Concept)

```
SOF   : 0x55AA          (2 bytes)
VER   : 0x01            (1 byte)
CMD   :                 (1 byte)
LEN   : N               (2 bytes, LE)
DATA  : …               (N bytes)
CRC16 : X25             (2 bytes, LE, poly 0x1021, init 0xFFFF)
```

### Command Set (Minimum Viable)

| CMD  | Name            | Direction | Payload              | Notes |
|------|-----------------|-----------|----------------------|-------|
| 0x01 | PING            | PC→MCU    | none                 | Returns version string |
| 0x02 | GET_INFO        | PC→MCU    | none                 | Device ID, nvSRAM size, bank count |
| 0x10 | HOLD_ON         | PC→MCU    | none                 | Isolates nvSRAM from ECU |
| 0x11 | HOLD_OFF        | PC→MCU    | none                 | Reconnects bus |
| 0x20 | SELECT_BANK     | PC→MCU    | {bank: 1 byte}       | Sets A17 while held |
| 0x30 | READ_BLOCK      | PC→MCU    | {addr:3, len:2}      | Returns data from nvSRAM |
| 0x31 | WRITE_BLOCK     | PC→MCU    | {addr:3, len:2, data…} | Writes to nvSRAM |
| 0x32 | ERASE_FILL      | PC→MCU    | {addr:3, len:2, fill:1} | Fast fill for large spans |
| 0x40 | VERIFY_CRC      | PC→MCU    | {addr:3, len:2}      | Returns CRC16 over range |

**Rules**:
- WRITE/SELECT_BANK require HOLD_ON first. NACK if not held.
- Max WRITE_BLOCK payload: 512 bytes per frame.
- Full 128 KB upload: ~1–2 seconds over USB-CDC at 1 Mbaud.

---

## 8. How This Compares to Existing Hardware

| Feature | PCMHacking NVRAM | Moates Ostrich 2.0 | CobraRTP FlashOnline | This Design (Rev A) |
|---------|-----------------|-------------------|---------------------|-------------------|
| Memory | DS1245Y (battery-backed SRAM) | SRAM emulation | SRAM emulation | CY14B101NA nvSRAM (no battery) |
| Bus control | None (passive drop-in) | USB + buffered I/O | USB + buffered I/O | CPLD gated + MCU |
| Dual-bank | No | Yes (via software) | Yes (via software) | Yes (A17 + IMAGE_SEL) |
| Write endurance | ~unlimited (SRAM) | unlimited (SRAM) | unlimited (SRAM) | unlimited (nvSRAM) |
| Battery required | Yes (10-year lithium) | Yes (coin cell) | Yes (CR2032) | **No** |
| Real-time tuning | Via ALDL + OSE Enhanced | Via USB + TunerPro plugin | Via USB + TunerPro plugin | Via ALDL (Rev A) / USB (Rev B) |
| Cables | N/A | 28-pin DIP, 32-pin DIP | SOP-44 adapter | Memcal edge (32-pin) |
| Flash chip emulation | N/A (EPROM socket) | N/A (EPROM socket) | 28/29F200, 29F400, 29F800 | N/A (nvSRAM direct) |
| Bluetooth | No | No | Yes (SPP, 115200–921600 baud) | Rev B planned |
| Address hit tracing | No | No | Yes (single-shot) | No (future?) |
| Cost | ~AU$270 | ~US$160 (moates.net) | ~US$200 (cobrartp.com) | ~AU$100 BOM (estimate) |
| Availability | Scarce (Gareth, PCMHacking) | In stock (moates.net, reopened) | In stock (cobrartp.com) | DIY |

**Hardware on hand**: Author owns a Moates Ostrich 2.0 (with 28-pin and 32-pin cables) and a Moates G6 USB chip burner. These can be used for testing and comparison against this design.

---

## 9. Schematic Sheet Organization (6 Sheets, Conceptual)

1. **Top-level block diagram** — labels only
2. **ECU edge ↔ CPLD** — bussed A/D/control nets, behavioral notes
3. **nvSRAM** — A/D buses, CE/OE/WE from CPLD, A17 from CPLD
4. **MCU + SPI + SWD + IMAGE_SEL** — STM32F446 connections
5. **Power & protection** — 12 V in, buck, LDO, TVS, reverse-polarity PMOS
6. **Net-class legend, test points, operating notes**

Test points: `TP_12V`, `TP_5V`, `TP_3V3`, `TP_GND`, `TP_HOLD`, `TP_BANK`, `TP_CE`, `TP_OE`, `TP_WE`

---

## 10. Bring-Up Sequence (Conceptual)

1. **Rails check**: +12 V → +5 V → +3V3 at test points.
2. **Program CPLD**: Confirm BUS_HOLD forces CE/OE/WE high and D bus = Z; release = pass-through.
3. **Load base BIN** to nvSRAM (bench writer or ALDL upload).
4. **In-car test**: Key-on → engine should run on bank 0.
5. **TunerPro RT**: Connect with correct ADX/XDF; tweak a small table (e.g., fan temps) to verify live edit.
6. **Bank flip**: Assert BUS_HOLD → set IMAGE_SEL → release hold; confirm clean switch.

---

## 11. Related Documents (Source Material)

All conceptual — templates and ideas, not verified designs:

| Document | Location | Content |
|----------|----------|---------|
| Moates vs FlashOnline comparison | `../kingai hardware…/MOATES_VS_FLASHONLINE_COMPARISON.md` | Protocol comparison, TunerPro plugin analysis |
| RT Live ECU Emulator guide | `../kingai hardware…/RT_Live_ECU_Emulator_Complete_Guide.md` | Hardware architecture options, pinout specs |
| ChatGPT hardware brainstorm | `../kingai hardware…/chatgpt more rants hardware proper.md` | Rev A/B design sessions, BOM, CPLD pin tables |
| Manual schematic guide | `../kingai hardware…/Manual_Schematic_Organization_Guide.md` | Sheet organization, net naming |
| Second PCB attempt note | `./my_second_pcb_attempt_for_live_tuner.md` | Placeholder (1 line) |
| Verilog stubs | `../kingai hardware…/memcal_emulator.v`, `tb_memcal_emulator.v` | CPLD HDL concept + testbench |

---

## 12. What's Real vs What's Conceptual

| Item | Status |
|------|--------|
| Part selections (CY14B101NA, EPM7064S, STM32F446) | **Conceptual** — parts exist and are orderable, but no board has been designed |
| CPLD pin-to-net table | **Conceptual** — mapped to PLCC-44 pad numbers but not validated |
| Bus timing (ECU ↔ nvSRAM) | **Assumed OK** — PCMHacking NVRAMs used 70–120 ns parts successfully |
| FlashOnline loader protocol | **Conceptual** — frame format designed, no firmware written |
| Verilog HDL stubs | **Conceptual** — compiles in simulation but not synthesized to real CPLD |
| PCB layout | **Does not exist** — no schematic capture or layout has been done |
| In-car testing | **Not done** — no hardware exists to test |

---

## 13. Key Decisions Still Needed

1. **Memory**: CY14B101NA (5 V nvSRAM, no shifters) vs FM28V100 (3.3 V FRAM, needs level shifters)?
   - Rev A concept chose nvSRAM for simplicity. FRAM is Rev B.

2. **CPLD package**: PLCC-44 (EPM7064S, pass-through) vs TQFP-100 (EPM7128S, full inline control)?
   - Rev A chose PLCC-44. TQFP-100 only if address tracing or full bus isolation is needed.

3. **PC interface**: SPI-only (Rev A) vs USB-CDC (Rev B) vs Bluetooth (Rev B+)?

4. **TunerPro plugin**: Write a custom plugin, or rely purely on ALDL + OSE Enhanced?

5. **Form factor**: Memcal-shaped daughterboard (drop-in) vs external box with ribbon cable?

---

*This document consolidates brainstorm sessions from the `kingai hardware project` repo.
Everything is concept-grade. No PCBs, no tested firmware, no validated pinouts.*