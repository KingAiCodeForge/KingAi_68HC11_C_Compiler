# HC11 Bench / In-Car Emulator — Template Scaffold

> **⚠ WARNING: PINOUT / ADDRESS PLACEHOLDERS — NOT VERIFIED ⚠**
>
> Still need to add a comprehensive CLI UI with live output display, logging, and bus sniffing capabilities.
>
> Everything in this directory is a **software-side template** with
> **placeholder pin numbers, connector IDs, and I/O addresses**.
> The VY V6 Delco PCM (P/N 92118883 "445", $060A calibration) uses
> C1 / C2 / C3 connectors (32-pin, 32-pin, 24-pin) and the pin-to-function
> mapping **has not been verified against a real harness yet**.
>
> **Before wiring anything to a real PCM:**
> 1. Cross-reference every pin against the VY V6 wiring diagrams in the
>    service manual and community-verified sources:
>    - [pcmhacking.net bench setup guide (topic 4930)](https://pcmhacking.net/forums/viewtopic.php?t=4930)
>    - [pcmhacking.net bench harness pinout (topic 7880)](https://pcmhacking.net/forums/viewtopic.php?t=7880)
>    - [JustCommodores VY V6 PCM pinout thread](https://forums.justcommodores.com.au/threads/vy-v6-pcm-pinout-16269238.222112/)
>    - [customecm.com bench harness pinouts](https://www.customecm.com/tune-file-repo-and-info-here/bench-harness-pinouts)
> 2. Verify with a multimeter / continuity tester on the actual PCM
>    connector before applying 12V to anything.
> 3. Update `bench_config.py` with confirmed pin assignments and remove
>    the `UNVERIFIED` flags.
>
> **The code logic and ALDL framing are believed correct (based on the
> GM XDE-5024B 8192-baud protocol spec). Only the physical wiring map
> needs confirmation.**

## What's Here

```
template_addresses_might_be_wrong/
├── README.md                    ← This file
├── bench_config.py              ← Pin/address config (PLACEHOLDERS)
├── aldl_bridge.py               ← Phase 1: Serial bridge (8192 baud)
├── aldl_frame.py                ← ALDL frame builder / parser
├── mode4_bench_tester.py        ← Mode 4 actuator test harness
├── crank_signal_generator.ino   ← Phase 2: Arduino 3X/18X crank sim
├── sensor_simulator.py          ← Phase 2: DAC-based sensor sim
├── bench_test_runner.py         ← Automated validation framework
├── flash_and_capture.py         ← Phase 3+: Compile → flash → verify
└── tests/
    └── test_aldl_frame.py       ← Unit tests for frame builder
```

## Quick Start (Phase 1 — ALDL Serial Bridge)

**Hardware required:**
- FTDI/CH340 USB-serial adapter
- MAX232 or equivalent level shifter (12V ↔ TTL)
- OBD-II connector with pin 9 (ALDL data) + pin 5 (ground)
- 12V bench PSU (3A+) OR running VY V6 vehicle

```bash
# Install dependencies
pip install pyserial

# Read Mode 1 data stream (read-only, safe)
python aldl_bridge.py --port COM3 --mode read

# Send Mode 4 fan test (BENCH ONLY — actuates relay)
python mode4_bench_tester.py --port COM3 --test fan_high_on
```

## Phases

| Phase | Script | Status |
|-------|--------|--------|
| 1 — ALDL Bridge | `aldl_bridge.py` | Template ready |
| 1 — Mode 4 Tests | `mode4_bench_tester.py` | Template ready |
| 2 — Crank Sim | `crank_signal_generator.ino` | Template ready |
| 2 — Sensor Sim | `sensor_simulator.py` | Template ready |
| 3 — Flash Pipeline | `flash_and_capture.py` | Template ready |

## Relationship to Virtual Emulator

```
  Source Code (.c)
       │
       ▼
  hc11kit.py compile → binary (.bin)
       │
       ├──► Virtual Emulator → SCI output (in-memory)
       │
       └──► Bench (this tool) → SCI output (ALDL capture)
                                   │
                              Compare outputs (should match)
```

## References

- [Dev research plan](../ignore/dev_research_plan_for_bench_emulator.md) — full plan + all references
- [Project readme](../readme.md) — overview
