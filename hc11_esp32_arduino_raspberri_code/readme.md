# HC11 / ESP32 / Arduino / Raspberry Pi — Embedded ALDL ECU Tooling

> **PROTOCOL: ALDL serial (8192 baud, 8N1) — NOT CAN bus.**
> The VY Commodore V6 Delco 09356445 (HC11F1 + M29W800DB) uses GM ALDL Class 2 serial protocol over a single-wire data line. There is NO CAN bus on this ECU. Any CAN-based code in this repo is reference material only and needs heavy refactoring before it could be useful.

## Purpose

Code and tooling for interfacing with Motorola HC11-based automotive ECUs (specifically the Delco/Delphi VY Commodore V6 flash-based ECU, OS ID $060A) using ESP32, Arduino, and Raspberry Pi hardware over the ALDL serial bus.

## What Actually Works
| File | Status | Description |
|------|--------|-------------|
| `shared/aldl_protocol.h` | **READY** | C header — ALDL constants, device IDs, modes, security key calc |
| `shared/flash_erase_write_kernel.asm` | **TEMPLATE** | HC11 ASM flash kernel for M29W800DB — addresses need verification against bin |
| `shared/hc11_opcodes.py` | **READY** | Complete 68HC11 opcode table + assembler/disassembler (from EVBU/tonypdmtr patterns) |
| `arduino/aldl_reader/` | **TEMPLATE** | Mode 1 data stream reader — data offsets need verification |
| `arduino/aldl_bluetooth_mega/` | **WORKING** | Bluetooth ALDL bridge (from joukoy, confirmed working code) |
| `arduino/memory_dumper/` | **TEMPLATE** | Mode 6 kernel upload + memory read — needs testing |
| `esp32/aldl_wifi_interface/` | **TEMPLATE** | Wi-Fi AP + WebSocket ALDL tool — data offsets need verification |
| `esp32/esp32_twai_can_lib/` | **NOT APPLICABLE** | CAN bus library — does NOT apply to ALDL ECUs, reference only |
| `raspberri_pi/aldl_interface.py` | **TEMPLATE** | Full ALDL library — connection, modes, security, kernel upload |
| `raspberri_pi/datastream_reader.py` | **TEMPLATE** | Live data stream + CSV logging — data offsets need verification |
| `raspberri_pi/flash_patcher.py` | **TEMPLATE** | Full flash protocol + offline binary patching |

## Flash Timing Math (VY V6 128KB over ALDL)
```
ALDL serial: 8192 baud → 819 bytes/sec raw (8N1)
Effective (with protocol overhead): ~350-460 bytes/sec

READ (full 128KB bin dump):
  131,072 / 458 ≈ 286 seconds ≈ 4.8 minutes
  (OSE screenshot shows ~4.58 kbps, 89 sec remaining at ~70%)

WRITE (full flash — 3 banks):
  Sector erase: ~6-8 seconds total (8 sectors)
  Data write: 131,072 / 350 ≈ 375 seconds ≈ 6.3 minutes
  Total: ~6.5 minutes for full OS+CAL write

CAL-only write (bank 1, 16KB):
  16,384 / 350 ≈ 47 seconds

Block rate: ~5.5 blocks/second (64-byte blocks)
```

## Folder Structure
```
hc11_esp32_arduino_raspberri_code/
├── shared/                          # Cross-platform protocol definitions
│   ├── aldl_protocol.h              # C header — modes, device IDs, checksums
│   ├── flash_erase_write_kernel.asm # HC11 ASM flash kernel (TEMPLATE)
│   └── hc11_opcodes.py              # 68HC11 opcode table + assembler
├── arduino/                         # Arduino Mega 2560 sketches
│   ├── aldl_reader/                 # Mode 1 data stream reader
│   ├── aldl_bluetooth_mega/         # BT ALDL bridge (WORKING — from joukoy)
│   └── memory_dumper/               # Mode 6 kernel upload + memory read
├── esp32/                           # ESP32-S3 sketches
│   ├── aldl_wifi_interface/         # Wi-Fi AP + WebSocket ALDL tool
│   └── esp32_twai_can_lib/          # ⚠️ CAN bus ref — NOT for ALDL ECUs
├── raspberri_pi/                    # Raspberry Pi Python tools
│   ├── aldl_interface.py            # Full ALDL serial library
│   ├── datastream_reader.py         # Live data stream + CSV logging
│   └── flash_patcher.py             # Full flash protocol + binary patching
└── ignore/                          # Research notes, brainstorming
    ├── brainstorms.md
    ├── hardware_i_have.md
    └── research_github_for_repos.md
```

## Sibling Folders (same parent: kingai_c_compiler_v0.1/)
| Folder | Description |
|--------|-------------|
| `68hc11_disassembler_tool_for_vy_v6/` | Full disassembler suite — 34 Python scripts + core/ library |
| `vy_$060a_enhanced_1.0_bin_xdf_example/` | Reference bin + XDF + bank splits + disassembly |
| `hc11_compiler/` | HC11 C cross-compiler toolchain |
| `hc11_bench_incar_emulator/` | Bench/in-car emulator sketches |
| `hc11_virtual_emulator/` | Software-only HC11 CPU simulator |

## Hardware Targets
- **Target MCU:** Motorola 68HC11F1 — processor inside the Delco ECU
- **Flash chip:** STMicro M29W800DB (8Mbit, bottom boot, 128KB used)
- **Interface HW:** ESP32-S3, Arduino Mega 2560, Raspberry Pi 4/5
- **Protocol:** ALDL 8192 baud (Mode 1 data stream, Mode 5/6 flash, Mode 8/9 chatter, Mode 13 security)
- **NOT CAN bus** — the VY V6 Delco is pre-CAN, single-wire ALDL serial only

## Protocol Sources
- OSE Enhanced Flash Tool (VL400) — decompiled C# → protocol constants, ported to python.
- pcmhacking.net — community ALDL documentation
- tonypdmtr/EVBU — HC11 opcode definitions and cycle counts - refactored
- joukoy ALDL-bt-wb — confirmed working Arduino ALDL Bluetooth bridge
