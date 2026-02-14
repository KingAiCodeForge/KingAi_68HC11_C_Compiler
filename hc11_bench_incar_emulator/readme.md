# HC11 Bench / In-Car Emulator

**Status:** Planning — no code yet (Feb 15, 2026)

Hardware-based testing of compiled HC11 code on real Delco PCM hardware.
This is the "truth test" that validates the virtual emulator's results
against actual silicon.

## What This Is

A bench testing rig that:
1. Flashes compiled code into a VX/VY V6 Delco PCM ($060A calibration)
2. Communicates over ALDL (8192 baud, OBD pin 9) via USB-serial + MAX232
3. Sends Mode 4 commands and reads Mode 1 data streams
4. Validates that real hardware output matches virtual emulator output

## Hardware Required

| Component | Cost | Source |
|-----------|------|--------|
| VX or VY V6 Delco PCM (L36 flash) | $20-50 | Wreckers / eBay |
| USB-serial adapter (FTDI/CH340) | $5-10 | eBay / Amazon |
| MAX232 level shifter board | $2-5 | eBay |
| OBD-II pigtail or pin 9 tap | $5 | Auto parts |
| 12V bench power supply (3A+) | $20-40 | Already owned |
| (Optional) OSEFlashTool or PCMHammer | Free | pcmhacking.net |

**Total: ~$50-100 if starting from scratch**

## Target Hardware

- **L36 N/A V6 VX and VY** — the only flash-based HC11 ECU in the Holden range
- VS VT V6 use socketed MEMCAL PROMs — different workflow (burn EPROM)
- L67 (supercharged) VS VT VY VX all use 128KB MEMCALs
- The $060A calibration is the VY V6 Enhanced OS binary

## ALDL Protocol

- Baud: 8192 baud, 8N1
- Crystal: 4.194304 MHz → 2.097152 MHz E-clock → BAUD=$04 → 8192 exact
- Physical: OBD-II pin 9 (or ALDL connector pin M on older models)
- Logic: Inverted TTL (need MAX232 or equivalent level shifter)

## Phases

### Phase 1: Serial Bridge (target: first)
- Python script that opens COM port at 8192 baud
- Sends "Enter Diagnostics" Mode $0A frame
- Reads Mode 1 data stream
- Displays basic engine parameters (RPM, CTS, TPS, MAP)
- Cross-validates against virtual emulator's Mode 1 parser

### Phase 2: Mode 4 Actuator Testing
- Send Mode 4 frames from mode4_harness.py over real ALDL
- Verify fan relay, CEL, fuel pump toggle on bench hardware
- Compare PORTB state observations with emulator predictions

### Phase 3: Flash + Run Custom Code
- Flash aldl_hello_world.bin to free space ($5D00+) in $060A
- PCM boots, runs custom code, sends "HELLO\r\n" over ALDL
- Capture on laptop → proof that compiler output runs on real hardware
- Compare SCI output with virtual emulator's output (should be identical)

### Phase 4: Compiler Integration Test
- Compile C source → assemble → patch into bin → flash → run → capture ALDL
- Automated pipeline: `hc11kit.py compile hello.c --flash --capture`
- Diff virtual emulator output vs real hardware output

## Relationship to Virtual Emulator

The bench emulator and virtual emulator validate the same binaries.
When both produce identical SCI output for the same input binary,
we have high confidence the compiler output is correct.

```
  Source Code (.c)
       │
       ▼
  hc11kit.py compile → binary (.bin)
       │
       ├──► Virtual Emulator → SCI output (in-memory)
       │                           │
       └──► Bench/In-Car ──────► SCI output (ALDL capture)
                                   │
                              Compare outputs
                              (should match)
```

## Cross-Reference Sources

1. **ALDL_Simulator_Instructions_V1.14.pdf** — MrModule hardware ALDL sim
2. **kingai_srs_commodore_bcm_tool** — Python ALDL tooling, Mode 4 definitions
3. **PCMHacking.net downloads** — OSEFlashTool, VPW/ALDL sniffer tools
4. **ignore/dev_research_plan_for_bench_emulator.md** — full development plan

## Directory Structure

```
hc11_bench_incar_emulator/
  ignore/
    dev_research_plan_for_bench_emulator.md  — Full development plan
  readme.md                                  — This file
  (code to be added in Phase 1)
```
