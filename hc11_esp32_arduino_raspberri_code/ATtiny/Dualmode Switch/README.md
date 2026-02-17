# BMW Dual-Mode ECU Switch Project

> **Russian-Language BMW Tuning Resource** - Hardware modification enabling real-time switching between two ECU firmware calibrations without reflashing.

[![Platform](https://img.shields.io/badge/Platform-BMW-blue)]()
[![ECU](https://img.shields.io/badge/ECU-Bosch%20%7C%20Siemens-green)]()
[![Language](https://img.shields.io/badge/Docs-Russian-red)]()
[![MCU](https://img.shields.io/badge/MCU-ATtiny2313-orange)]()

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Technical Background](#-technical-background)
- [Supported ECU Platforms](#-supported-ecu-platforms)
- [Folder Structure](#-folder-structure)
- [How It Works](#-how-it-works)
- [Memory Chip Reference](#-memory-chip-reference)
- [ECU-Specific Wiring Guide](#-ecu-specific-wiring-guide)
- [Display Module Hardware](#-display-module-hardware)
- [Creating Dual-Mode Firmware](#-creating-dual-mode-firmware)
- [Firmware Collection](#-firmware-collection)
- [EWS Immobilizer Considerations](#-ews-immobilizer-considerations)
- [Required Tools & Software](#-required-tools--software)
- [Assembly Instructions](#-assembly-instructions)
- [Important Warnings](#-important-warnings)
- [External Resources](#-external-resources)
- [Translation Reference](#-translation-reference)

---

## 🇷🇺 Overview

This project contains **Russian-language documentation and firmware** for building a hardware switch that allows BMW owners to toggle between **two different ECU calibrations** in real-time without reflashing. Originally developed by the Russian BMW tuning community, it covers ECU platforms from the early Bosch Motronic M1.x series through the later Siemens MS4x systems.

### Key Concept

Replace the ECU's EPROM/Flash chip with a **double-capacity chip** containing two complete firmware images, then use a hardware switch connected to the highest address line to select between the upper or lower memory bank.
### Quick Specifications

| Feature | Details |
|---------|---------|
| **Documentation Language** | Russian (Русский) with English translations in this README |
| **ECU Support** | Bosch M1.1, M1.3, M1.7, M3.1, M3.3, MS41; Siemens MS42, MS43; Bosch ME7.2 |
| **Engine Coverage** | M20, M30, M40, M42, M43, M50, M50TU, M52TU, M54, M60/M62 V8 |
| **Vehicle Years** | Approximately 1988-2006 (E30, E34, E36, E38, E39, E46, E53) |
| **Microcontroller** | ATtiny2313 (20-pin DIP) for switch indicator display |
| **Display** | 7-segment LED, common cathode |
| **Firmware Count** | 330+ binary files across all platforms |

---

## 📚 Technical Background

### The Problem This Solves

Traditional ECU tuning requires physically swapping chips or reflashing the ECU each time you want to change calibrations. This is impractical for:
- Switching between street and track tunes
- Toggling economy vs. performance modes
- Testing different calibrations during development
- Running with/without catalytic converters (emissions testing)

### The Solution

By installing a memory chip with **double the capacity** of the original, you can store two complete firmware images:
- **Bank 1 (Lower half):** Original/Stock calibration
- **Bank 2 (Upper half):** Tuned/Modified calibration

A simple toggle switch controls the highest address line, selecting which bank the ECU reads from.

### Why This Works

EPROM/Flash memory chips are organized by address lines (A0, A1, A2... An). The highest address line effectively divides the chip in half:
- When **LOW (0V)**: ECU accesses addresses 0x0000 to 0x7FFF (lower 32KB)
- When **HIGH (5V)**: ECU accesses addresses 0x8000 to 0xFFFF (upper 32KB)

The ECU has no idea there's double the memory - it just reads from whichever half is selected.

---

## 🔧 Supported ECU Platforms

### Bosch Motronic (Older Generation)

| ECU Model | Part Numbers | Engines | Vehicles | Memory Type |
|-----------|--------------|---------|----------|-------------|
| **M1.1** | 0261200027 | M20B20, M20B25 | E30 320i/325i | 27C256 (32KB) |
| **M1.3** | 0261200172, 0261200179 | M20B25, M30B34, M30B35 | E30/E34 325i, 535i | 27C256 (32KB) |
| **M3.1** | 0261200400, 0261200402 | M50B20, M50B25 | E34 520i/525i | 27C256 (32KB) |
| **M1.7** | 0261200520+ | M40B16, M40B18, M43B16, M43B18 | E36 316i/318i | W27C512 (64KB) |
| **M3.3** | 0261200403, 0261200413 | M42B18, M50TUB25, M60B30, M60B40 | E36/E34/E32/E38 | W27C512 (64KB) |

### Bosch Motronic (Later Generation)

| ECU Model | Part Numbers | Engines | Vehicles | Memory Type |
|-----------|--------------|---------|----------|-------------|
| **MS41** | 1429861+ | M52B20, M52B25, M52B28 | E36/E39 early | Internal + External |
| **ME7.2** | 0261204620, 0261207106 | M62B35, M62B44 V8 | E38/E39/E53 (1998+) | 29F series Flash |

### Siemens MS4x Series

| ECU Model | Engines | Vehicles | Memory Type | Flash Size |
|-----------|---------|----------|-------------|------------|
| **MS42** | M52TUB20 (2.0L), M52TUB25 (2.5L), M52TUB28 (2.8L) | E39 520i/523i/528i, E46 320i/323i/328i | 29F400 series | 512KB |
| **MS43** | M54B25 (2.5L), M54B30 (3.0L) | E39 525i/530i, E46 325i/330i, E53 X5 3.0i | 29F400 series | 512KB |

### Application Reference (by Model)

| Vehicle | Engine Options | ECU Types |
|---------|----------------|-----------|
| **E30 (3-Series 1982-1994)** | M20B20, M20B25 | M1.1, M1.3 |
| **E34 (5-Series 1988-1996)** | M20, M30, M50, M60 | M1.3, M3.1, M3.3 |
| **E36 (3-Series 1990-2000)** | M40, M42, M43, M50, M52 | M1.7, M3.3, MS41, MS42 |
| **E38 (7-Series 1994-2001)** | M60, M62 | M3.3, ME7.2 |
| **E39 (5-Series 1996-2003)** | M52TU, M54, M62 | MS41, MS42, MS43, ME7.2 |
| **E46 (3-Series 1999-2006)** | M52TU, M54 | MS42, MS43 |
| **E53 (X5 2000-2006)** | M54, M62 | MS43, ME7.2 |

---

## 📁 Folder Structure

```
Dualmode Switch/
│
├── README.md                               # This comprehensive guide
├── Dualmode_Switch_Inventory.md            # Complete file inventory with translations
├── KingAi_TODO_README.md                   # Project notes
│
└── Двурежимная прошивка/                   # "Dual-mode firmware" (main folder)
    │
    ├── 📄 Documentation (Russian)
    │   ├── Мануал двухрежимки BMW для всех ЭБУ.pdf    # Master manual for all ECUs
    │   ├── Мануал двухрежимки BMW для всех ЭБУ.md     # Markdown version
    │   ├── Как собрать переключатель.docx              # "How to build the switch"
    │   ├── Как собрать переключатель.md                # Markdown version
    │   ├── Как создать файл двухрежимной прошивки.docx # "How to create dual firmware"
    │   └── Как создать файл двухрежимной прошивки.md   # Markdown version
    │
    ├── 🖼️ Schematics & Images
    │   ├── Общая схема.png                 # General/overall schematic
    │   ├── Схема переключателя.jpg         # Switch circuit diagram
    │   └── Плата.JPG                       # Assembled PCB photo
    │
    ├── 🔧 Файлы для создания переключателя/  # "Files to build switch" (Version 1)
    │   ├── Прошивка платы (Аттини).hex     # ATtiny2313 firmware v1 (390 bytes)
    │   └── Чертеж платы.lay                # Sprint Layout PCB design (7.8KB)
    │
    ├── 🔧 Версия на 2 переключателя (ДВС и КПП)/  # "2-switch version (Engine + Trans)"
    │   ├── tuning switch rev2.hex          # ATtiny2313 firmware v2 (504 bytes)
    │   ├── version2.lay                    # Sprint Layout PCB design (68KB)
    │   └── 575033967.jpg                   # Reference photo
    │
    └── 📦 Прошивки/                        # "Firmwares" - Binary collection
        │
        ├── Bosch M60 V8/                   # M60B30, M60B40 firmwares
        │   ├── *.bin files (15+)
        │   └── *.zip/*.rar archives
        │
        ├── bosch_motronic_1_3/             # M1.3 for M20, M30 engines
        │   ├── enzo-m20b20/
        │   ├── enzo-m20b25/
        │   ├── M30B35 Пак прошивок/        # M30B35 firmware pack
        │   └── various .bin files
        │
        ├── MS_42/                          # Siemens MS42 firmwares
        │   └── (organized by calibration ID)
        │
        ├── MS_43/                          # Siemens MS43 firmwares
        │   └── (organized by calibration ID)
        │
        ├── ME_7_2/                         # Bosch ME7.2 for M62 V8
        │   └── (organized by part number)
        │
        └── MiniPro/                        # EPROM programmer software
            ├── MiniPro.exe                 # Main application
            └── MiniProHelp.chm             # Help documentation
```

---

## 🔧 How It Works

### The Dual-Bank Concept

```
┌─────────────────────────────────────────────────────────────┐
│                     DOUBLE-SIZE EPROM                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  BANK 2 (Upper Half) - Address: 0x8000 - 0xFFFF     │    │
│  │  ════════════════════════════════════════════════   │    │
│  │  Contains: TUNED / PERFORMANCE Firmware             │    │
│  │  Selected when: Switch = HIGH (5V)                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  BANK 1 (Lower Half) - Address: 0x0000 - 0x7FFF     │    │
│  │  ════════════════════════════════════════════════   │    │
│  │  Contains: STOCK / ORIGINAL Firmware                │    │
│  │  Selected when: Switch = LOW (0V / GND)             │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ Highest Address Line
                              │ (A15, A16, or A17)
                              ▼
                    ┌─────────────────┐
                    │  TOGGLE SWITCH  │
                    │   ┌───┬───┐     │
                    │   │ 1 │ 2 │     │
                    │   └───┴───┘     │
                    │  Position 1: GND│
                    │  Position 2: 5V │
                    └─────────────────┘
```

### Switching Logic

| Switch Position | Address Line | Memory Bank | Firmware |
|-----------------|--------------|-------------|----------|
| Position 1 (Down) | LOW (GND) | Bank 1 (Lower) | Stock |
| Position 2 (Up) | HIGH (5V) | Bank 2 (Upper) | Tuned |

---

## 💾 Memory Chip Reference

### EPROM/Flash Upgrade Path

| Original Chip | Upgrade Chip | Size Increase | Pin Compatibility |
|---------------|--------------|---------------|-------------------|
| **27C256** (32KB) | **W27C512** (64KB) | 2× | 100% pin-compatible* |
| **W27C512** (64KB) | **W27C010** (128KB) | 2× | Requires offset mounting |
| **28F400** (512KB) | **28F800** (1MB) | 2× | Pin-compatible |
| **29F400** (512KB) | **29F800** (1MB) | 2× | Pin-compatible |

*\*Pin 1 differs: 27C256 has Vpp (programming voltage), W27C512 has A15 (address line)*

### Detailed Pin Differences: 27C256 vs W27C512

The 27C256 and W27C512 are both 28-pin DIP packages but differ at Pin 1:

| Pin | 27C256 (32KB) | W27C512 (64KB) | Notes |
|-----|---------------|----------------|-------|
| 1 | Vpp (Programming Voltage) | **A15 (Address Line)** | **This is the switch connection!** |
| 2-14 | A14-A0, D0-D7 | A14-A0, D0-D7 | Identical |
| 20 | /CE (Chip Enable) | /CE | Identical |
| 22 | /OE (Output Enable) | /OE | Identical |
| 27 | A14 | A14 | Identical |
| 28 | Vcc (+5V) | Vcc (+5V) | Identical |

**Key Point:** On 27C256, Pin 1 receives 12.5V during programming only. On W27C512, Pin 1 is address line A15 - this is where you connect the switch!

### W27C512 → W27C010 Offset Installation

The W27C010 has 32 pins versus 28 pins on W27C512. Install with a 4-pin offset:

```
W27C010 (32 pins)        Socket (28 pins)
┌──────────────────┐    ┌──────────────────┐
│ Pin 1  - NC      │    │                  │
│ Pin 2  - A16 ◄───┼────┼── SWITCH WIRE    │
│ Pin 3  - A15     │    │ Pin 1 (Socket)   │
│ Pin 4  - A12     │    │ Pin 2 (Socket)   │
│ ...              │    │ ...              │
│ Pin 32 - VCC ────┼────┼── JUMPER TO Pin 28 (Vcc in socket)
└──────────────────┘    └──────────────────┘
```

**Critical:** Solder a jumper wire from W27C010 Pin 32 (Vcc) to the socket's Vcc pin!

---

## 🔌 ECU-Specific Wiring Guide

### Bosch M1.1 / M1.3 / M3.1

**Engines:** M20B20, M20B25, M20B27, M30B34, M30B35, M50B20, M50B25

| Parameter | Specification |
|-----------|---------------|
| Original EPROM | 27C256 (32KB) |
| Upgrade EPROM | W27C512 (64KB) |
| Switch Connection | **Pin 1 (A15)** |
| Pin Status | **Leave unsoldered from PCB** - connect only to switch wire |

```
         W27C512
    ┌───────┴───────┐
    │ 1 ──────────────► To Toggle Switch (other side to GND)
    │ 2             28│
    │ ...          ...│
    │ 14 ○ (notch) 15│
    └─────────────────┘
```

### Bosch M1.7 / M3.3

**Engines:** M40B16, M40B18, M42B18, M43B16, M43B18, M50TUB25, M60B30, M60B40

| Parameter | Specification |
|-----------|---------------|
| Original EPROM | W27C512 (64KB) |
| Upgrade EPROM | W27C010 (128KB) |
| Switch Connection | **Pin 2 (A16)** |
| Installation | 4-pin offset, jumper Vcc |

### Siemens MS42 / MS43

**Engines:** M52TUB20/25/28, M54B25/30

| Parameter | Specification |
|-----------|---------------|
| Original Flash | 29F400 (512KB) or similar |
| Upgrade Flash | 29F800 (1MB) or equivalent |
| Switch Connection | Varies - see schematics |
| Special Notes | Use ZIF socket adapter for repeated access |

### Bosch ME7.2 (M62 V8)

**Engines:** M62B35, M62B44 (E38/E39/E53)

| Parameter | Specification |
|-----------|---------------|
| Original Flash | 29F series (512KB+) |
| Upgrade Flash | 2× capacity |
| Special Notes | May require boot sector handling |

---

## 🖥️ Display Module Hardware

The display module provides visual feedback showing which firmware bank is active.

### ATtiny2313 Specifications

| Parameter | Value |
|-----------|-------|
| **Microcontroller** | ATtiny2313 (Atmel/Microchip) |
| **Package** | 20-pin DIP |
| **Clock** | Internal 8MHz RC oscillator |
| **Operating Voltage** | 2.7V - 5.5V |
| **I/O Pins Used** | ~10 (7-segment + switch input + LED) |

### 7-Segment Display Connection

The ATtiny2313 drives a **common cathode** 7-segment display:

```
    ┌───────────────────────────────────────┐
    │           7-SEGMENT DISPLAY            │
    │                                        │
    │      ━━━━━━ a ━━━━━━                   │
    │     ┃               ┃                  │
    │     f               b                  │
    │     ┃               ┃                  │
    │      ━━━━━━ g ━━━━━━                   │
    │     ┃               ┃                  │
    │     e               c                  │
    │     ┃               ┃                  │
    │      ━━━━━━ d ━━━━━━    ●DP            │
    │                                        │
    └───────────────────────────────────────┘
    
    Each segment: ATtiny pin → 510Ω resistor → segment anode
    Common cathode: Connect to GND
```

### Component List

| Component | Value/Type | Quantity | Notes |
|-----------|------------|----------|-------|
| ATtiny2313 | 20-pin DIP | 1 | Programmed with .hex file |
| 7-segment display | Common cathode, red | 1 | Standard 0.56" or similar |
| Resistor | 510Ω SMD (0805) | 7-8 | Current limiting for segments |
| LED | 3mm or 5mm, any color | 1 | Status indicator |
| Toggle switch | SPDT | 1 | 2-position |
| LM2931 | 5V LDO regulator | 1* | *Only if using 12V power |
| Capacitors | 0.1µF, 10µF | 2 | *Only if using LM2931 |
| PCB | From .lay file | 1 | Order fabricated or DIY etch |

### Power Options

| Source | Voltage | Circuit Required | Pros/Cons |
|--------|---------|------------------|-----------|
| **ECU 5V rail** | 5V DC | None (direct) | ✅ Simpler, ❌ loads ECU supply |
| **Vehicle 12V** | 12V DC | LM2931 regulator circuit | ✅ Independent, ❌ more components |

### Operation Principle

1. Toggle switch changes position
2. Switch input to ATtiny changes logic level (HIGH/LOW)
3. ATtiny firmware reads input state
4. Display updates to show "1" or "2"
5. Same switch signal goes to EPROM address pin
6. ECU begins reading from selected memory bank

**Note:** Switching while engine is running may cause a brief hesitation or stall depending on how different the two calibrations are. Safest to switch with ignition ON but engine OFF.

---

## 📝 Creating Dual-Mode Firmware

### Method 1: Full Binary Concatenation (Different Base Software)

This method merges two **complete different firmware files** (e.g., stock + aftermarket tune).

**Process:**
1. Obtain both firmware binaries (must be same size, e.g., both 32KB)
2. Use **ALMI** software or hex editor to concatenate:
   - File 1 (Stock) → addresses 0x0000 - 0x7FFF
   - File 2 (Tune) → addresses 0x8000 - 0xFFFF
3. Result: 64KB combined file (double original size)
4. Program combined file to double-capacity EPROM

**Pros:** Simple process, any two files can be combined
**Cons:** 
- Switching while running may cause stalling (different base code)
- Requires ISN synchronization if EWS is present (see below)

### Method 2: Same Base + Different Calibrations (Recommended)

This method uses the **same base software** with only the calibration/map area swapped.

**Process:**
1. Read your original firmware (your stock + ISN)
2. Extract calibration area from tuned firmware
3. Patch tuned calibrations into copy of your firmware
4. Verify/correct checksum (use appropriate checksum tool)
5. Concatenate: Original + Patched version
6. Program to double-capacity EPROM

**Pros:** 
- Switching while running is smooth (same code, different data)
- No ISN issues (base software unchanged)
- Better for daily use

**Cons:** Requires knowing calibration area boundaries for your ECU

### Checksum Verification

**Important:** Always verify/correct checksums after modifying firmware!

Each ECU platform has specific checksum locations and algorithms. Tools like:
- **ECU checksum correctors** (various, platform-specific)
- **WinOLS** (commercial, multi-platform)
- **Community tools** on MS4x.net forums

---

## 📦 Firmware Collection

### Overview Statistics

| Platform | File Count | Total Size | Engine Coverage |
|----------|------------|------------|-----------------|
| Bosch M60 V8 | 30+ files | ~2 MB | M60B30, M60B40 |
| Bosch Motronic 1.3 | 20+ files | ~700 KB | M20, M30 |
| Siemens MS42 | 100+ files | ~30 MB | M52TU variants |
| Siemens MS43 | 150+ files | ~80 MB | M54 variants |
| Bosch ME7.2 | 15+ files | ~8 MB | M62 V8 |
| **TOTAL** | **~330 files** | **~125 MB** | - |

### Bosch M60 V8 Firmwares

**ECU Part Numbers:** 0261200404 ("404"), 0261203484 ("484")

| Filename | Engine | Trans | Features | Size |
|----------|--------|-------|----------|------|
| `M60B30 АКПП.BIN` | M60B30 | Auto | Stock | 64KB |
| `M60B30 МКПП lambda.bin` | M60B30 | Manual | With Lambda | 64KB |
| `M60B30 МКПП безлямбда.bin` | M60B30 | Manual | No Lambda | 64KB |
| `m60b30 для V8POWER.bin` | M60B30 | - | V8POWER Tune | 64KB |
| `M60B40akppnolambd1429009superchips.bin` | M60B40 | Auto | Superchips, No Lambda | 64KB |
| `1429180_540МКПП_безлямбдовая_1995г..bin` | M60B40 | Manual | E34 540i 1995, No Lambda | 64KB |
| `E38_M60B30_manual_catless_1429218.bin` | M60B30 | Manual | E38, Catless | 64KB |

### Bosch Motronic 1.3 Firmwares (M20/M30)

**ECU Part Numbers:** 0261200172, 0261200179

#### M30B35 Firmware Pack (Пак прошивок)

Complete matrix of configurations:

| Feature Combination | Auto+Lambda | Auto+No Lambda | Manual+Lambda | Manual+No Lambda |
|---------------------|-------------|----------------|---------------|------------------|
| **EML + ASC+T** | C358 | 6358 | C058 | 6058 |
| **EML, No ASC+T** | C35A | 635A | C05A | 605A |
| **No EML, No ASC+T** | C35E | 635E | C05E | 605E |

*EML = Electronic Engine Power Control; ASC+T = Automatic Stability Control + Traction*

### Siemens MS42 Firmwares

**Calibration ID Prefixes:**
- `Ca0110AB` - Early calibration
- `Ca0110AD` - Mid calibration  
- `Ca0110C6` - Later calibration
- `Ca0110CA` - Latest calibration

**File Naming Pattern:**
```
[HW_ID]_[Cal_ID]_[variant].bin
  │        │         │
  │        │         └── MOD2 = Tuned, Stok = Stock, E0/E2 = EWS delete variants
  │        └── Calibration ID (determines compatibility)
  └── Hardware/Software version code
```

**Example:** `84c3420g_Ca0110C6_MOD2.bin` = Hardware 84c3420g, Calibration 0110C6, Tuned version

### Siemens MS43 Firmwares

**Calibration ID Prefixes:**
- `Ca430037` - Early calibration
- `Ca430056` - Mid calibration
- `Ca430066` - Later calibration
- `Ca430069` - Latest calibration (often X5 specific)

**MOD4 Variants:** The tuned versions include various performance modifications.

### Bosch ME7.2 Firmwares (M62 V8)

For E38/E39/E53 with M62 V8 engines:

| Folder | Part Number | Calibration | Notes |
|--------|-------------|-------------|-------|
| `0261204620_350411/` | 0261204620 | 350411 | Early |
| `0261204620_350476/` | 0261204620 | 350476 | Mid |
| `0261207106_368125/` | 0261207106 | 368125 | X5 4.4 specific |

---

## 🔐 EWS Immobilizer Considerations

### What is EWS?

**EWS (Elektronische Wegfahrsperre)** is BMW's electronic immobilizer system. It prevents engine start without the correct key/transponder. The DME stores an **ISN (Individual Serial Number)** that must match the EWS module.

### EWS Versions by Year

| Version | Years | ECU Types | Notes |
|---------|-------|-----------|-------|
| **EWS I** | 1992-1994 | M1.7, M3.3 | E36 early |
| **EWS II** | 1994-1997 | M3.3, MS41 | Ring antenna |
| **EWS III** | 1998-2003 | MS42, MS43, ME7.2 | Integrated key |
| **EWS IV / CAS** | 2004+ | MSV70+ | Outside scope of this project |

### ISN Handling for Dual-Mode

#### Scenario 1: Same Base Software (Recommended)

If you only change calibrations and keep your original base software:
- **ISN remains intact** - no action needed
- EWS will function normally in both modes

#### Scenario 2: Different Base Software Versions

If combining two different full firmware images:
- **ISN stored in base software area** (most ECUs)
- You must copy your ISN to the secondary firmware
- Use ISN extraction/patch tools specific to your ECU

#### Exception: MS41

On MS41, the ISN is stored in the **calibration area**, not base software:
- Can be disabled programmatically (EWS delete)
- See pazi88's MS41 tuning videos for procedure

### EWS Delete Options

**WARNING:** EWS delete is illegal in some jurisdictions and may affect insurance coverage.

For vehicles with EWS issues or swapped engines:

| Method | Description | Applicable ECUs |
|--------|-------------|-----------------|
| **Software patch** | Modify ISN check routine | MS41, MS42, MS43 |
| **ISN sync** | Copy ISN to new ECU | All |
| **Virginize** | Reset ECU to accept new EWS | MS42, MS43, MS45 |

**Resources:**
- [Bimmer Tuning Tools - EWS IMMO Patcher](https://www.bimmertuningtools.com/) - MS41/42/43 support
- [Kassel Performance](https://www.kasselperformance.com/) - EWS delete services
- [DUDMD Tuning](https://www.dudmd.com/) - Comprehensive EWS solutions

---

## 🛠️ Required Tools & Software

### Hardware Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| **EPROM Programmer** | Read/write memory chips | TL866II Plus (MiniPro) recommended |
| **Soldering Station** | PCB assembly, chip installation | Fine tip for SMD work |
| **Hot Air Rework** | SMD components, chip removal | Optional but helpful |
| **Multimeter** | Continuity, voltage checks | Basic digital multimeter |
| **ZIF Socket Adapter** | Easy chip access during development | For 28F/29F flash chips |

### EPROM Programmer Compatibility

**Recommended:** TL866II Plus (XGecu) - affordable, wide chip support

| Chip Type | Supported | Notes |
|-----------|-----------|-------|
| 27C256 | ✅ | Standard EPROM |
| W27C512 | ✅ | EEPROM (electrically erasable) |
| W27C010 | ✅ | 1Mbit EEPROM |
| 28F400 | ✅ | Flash, may need adapter |
| 29F400 | ✅ | Flash, may need adapter |
| 29F800 | ✅ | Flash, TSOP adapter needed |

### Software Tools

| Software | Purpose | Source |
|----------|---------|--------|
| **MiniPro** | TL866 programmer software | Included in `Прошивки/MiniPro/` |
| **Sprint Layout** | View/edit .lay PCB files | [ABACOM](http://www.abacom-online.de/) (paid) |
| **Sprint Layout Viewer** | View .lay files (free) | [Softpedia](https://www.softpedia.com) |
| **HxD / HexEdit** | Binary file editing | Free hex editors |
| **ALMI** | Firmware concatenation | Russian tuning tool |
| **TunerPro RT** | Calibration editing with XDF | [TunerPro.net](https://www.tunerpro.net/) |
| **RomRaider** | ECU editing/logging | [romraider.com](https://romraider.com/) |

### ATtiny2313 Programming

| Programmer | Interface | Notes |
|------------|-----------|-------|
| **USBasp** | USB | Cheap, widely available |
| **Arduino as ISP** | USB | Use spare Arduino |
| **AVR Dragon** | USB | Atmel official (discontinued) |
| **AVRISP mkII** | USB | Atmel official |

**Software:** Arduino IDE (with ATtiny board package), Atmel Studio, avrdude

---

## 🔨 Assembly Instructions

### Step 1: Gather Components

Refer to the [Display Module Hardware](#-display-module-hardware) section for complete parts list.

### Step 2: Fabricate or Order PCB

**Option A - Professional Fabrication:**
1. Open `.lay` file in Sprint Layout
2. Export Gerber files
3. Upload to PCB fab (JLCPCB, PCBWay, etc.)
4. Order ~5 boards (minimum order usually)

**Option B - DIY Etching:**
1. Print PCB layout at 1:1 scale
2. Transfer to copper-clad board
3. Etch with ferric chloride
4. Drill holes

### Step 3: Program ATtiny2313

1. Connect programmer to ATtiny2313
2. Set fuses (if needed - usually default OK):
   - CKSEL: Internal 8MHz
   - SUT: 65ms startup
   - CKDIV8: Disabled (run at full 8MHz)
3. Flash `.hex` firmware:
   ```bash
   avrdude -c usbasp -p attiny2313 -U flash:w:firmware.hex:i
   ```

### Step 4: Solder PCB Components

**Order of assembly:**
1. SMD resistors (510Ω) first
2. ATtiny2313 (or socket)
3. 7-segment display
4. LED
5. Toggle switch connections
6. Power connections
7. DME connection wire

### Step 5: Prepare Dual Firmware

1. Obtain both firmware binaries
2. Verify equal sizes
3. Concatenate using ALMI or hex editor
4. Verify checksum(s)
5. Program to double-capacity EPROM

### Step 6: Install EPROM in ECU

**For 27C256 → W27C512 upgrade:**
1. Remove original 27C256 from DME board
2. Install W27C512 in same orientation
3. **Bend Pin 1 up** - do NOT solder to PCB
4. Solder thin wire from Pin 1 to switch connection

**For W27C512 → W27C010 upgrade:**
1. Remove original W27C512
2. Install W27C010 with 4-pin offset (pins 1-4 hanging off)
3. Jumper Pin 32 (Vcc) to socket Vcc
4. Solder switch wire to Pin 2 (A16)

### Step 7: Connect and Test

1. Connect display module power (5V from DME or 12V with regulator)
2. Connect switch signal wire to EPROM address pin
3. Verify switch operation: Display shows "1" ↔ "2"
4. Install DME in vehicle
5. Test both firmware banks with engine running

---

## ⚠️ Important Warnings

### Hardware Warnings

1. **Pin Fragility**
   > ⚠️ The EPROM pin connected to the switch must be **bent up and left floating** - not soldered to the PCB. These pins break very easily! Several chips were destroyed during development from broken pins.

2. **Socket Adapters Recommended**
   > For 28F/29F flash chips (MS42/MS43), use a **ZIF socket adapter**. Repeated soldering/desoldering:
   > - Damages PCB pads (copper lifts off)
   > - Deforms board from heat
   > - Weakens solder joints

3. **28F/29F Compatibility**
   > ✅ You CAN replace 28F series with 29F series
   > ❌ You CANNOT replace 29F series with 28F series
   > (29F uses 5V-only programming; 28F requires 12V Vpp)

4. **Static Sensitivity**
   > All memory chips are ESD-sensitive. Use anti-static precautions:
   > - Grounding strap
   > - Anti-static mat
   > - Handle by edges only

### Software/Firmware Warnings

5. **EWS/ISN Issues**
   > If using different base software versions, you must **synchronize the ISN**. The ISN is stored in the base software area (except MS41 where it's in calibrations).
   > - Same base + different calibrations = No ISN issues
   > - Different base software = Must patch ISN

6. **Switching While Running**
   > - **Method 2 (same base):** Switching while engine running is generally safe
   > - **Method 1 (different base):** May cause stalling or rough running during switch
   > - **Recommendation:** Switch with ignition ON, engine OFF

7. **Checksum Verification**
   > Always verify/correct checksums after any firmware modification. Incorrect checksum = ECU may not boot or enter limp mode.

### Legal/Regulatory Warnings

8. **Emissions Compliance**
   > - Deleting catalytic converter monitoring ("catless" tunes) is **illegal** in most jurisdictions
   > - Lambda sensor delete affects emissions
   > - Vehicle may fail emissions testing

9. **EWS Delete**
   > - May be illegal in some regions
   > - Could affect insurance coverage
   > - Intended for race/track vehicles or engine swaps

---

## 🔗 External Resources

### BMW ECU Tuning Communities

| Resource | Description | URL |
|----------|-------------|-----|
| **MS4x.net Wiki** | Definitive MS4x technical resource | [ms4x.net](https://www.ms4x.net/index.php?title=Main_Page) |
| **BMW Tuning Discord** | Active community chat | [discord.gg/vdVsypF](https://discord.gg/vdVsypF) |
| **RomRaider BMW Forum** | ECU editing discussions | [romraider.com/forum](https://romraider.com/forum/viewforum.php?f=41) |
| **TunerPro Forum** | XDF development, general tuning | [forum.tunerpro.net](http://forum.tunerpro.net/) |
| **r3vlimited (E30)** | E30-specific technical forum | [r3vlimited.com](https://www.r3vlimited.com/) |
| **Bimmerforums** | General BMW discussions | [bimmerforums.com](https://www.bimmerforums.com/) |

### Tuning Software & Tools

| Resource | Description | URL |
|----------|-------------|-----|
| **TunerPro RT** | Free calibration editor | [tunerpro.net](https://www.tunerpro.net/) |
| **RomRaider** | Open source ECU suite | [romraider.com](https://romraider.com/) |
| **Bimmer Tuning Tools** | MS4x-specific tools | [bimmertuningtools.com](https://www.bimmertuningtools.com/) |
| **Chaos Calibrations** | BMW tuning files | [chaoscalibrations.com](https://www.chaoscalibrations.com/) |
| **OldSkullTuning** | M1.3/M1.7 XDF files | [oldskulltuning.com](https://oldskulltuning.com/bmw-ecu-tuning/) |

### Video Tutorials

| Creator | Topic | URL |
|---------|-------|-----|
| **pazi88** | How to tune older BMW ECUs (comprehensive) | [YouTube](https://www.youtube.com/watch?v=yDXPBlh53Fs) |
| **pazi88** | MS41 tuning series | YouTube channel |
| **OldSkullTuning** | M1.3/M1.7 TunerPro tutorial | [YouTube](https://www.youtube.com/watch?v=vNCIAy1WZys) |

### Hardware Resources

| Resource | Description | URL |
|----------|-------------|-----|
| **Sprint Layout** | PCB design software (.lay files) | [abacom-online.de](http://www.abacom-online.de/) |
| **Sprint Layout Viewer** | Free .lay file viewer | [Softpedia](https://www.softpedia.com/get/Science-CAD/Sprint-Layout-Viewer.shtml) |
| **XGecu (TL866)** | EPROM programmer | [xgecu.com](http://www.xgecu.com/) |
| **TIMMS BMW Tips** | E32/E38 V8 chip tuning guide | [meeknet.co.uk](https://www.meeknet.co.uk/E32/Chipping/Index.htm) |

---

## 📖 Translation Reference

### Folder/File Names

| Russian | English | Context |
|---------|---------|---------|
| Двурежимная прошивка | Dual-mode firmware | Main concept/folder |
| переключатель | Switch | Hardware toggle |
| Мануал двухрежимки | Dual-mode manual | Documentation |
| Как собрать переключатель | How to build the switch | Assembly guide |
| Как создать файл | How to create the file | Firmware guide |
| Файлы для создания | Files for building | Component folder |
| Версия на 2 переключателя | 2-switch version | Engine + Trans variant |
| ДВС и КПП | Engine and Transmission | "DVS i KPP" |
| Прошивки | Firmwares | Binary collection |
| Прошивка платы | Board firmware | ATtiny hex file |
| Чертеж платы | Board drawing | PCB layout |
| Общая схема | General schematic | Wiring diagram |
| Схема переключателя | Switch schematic | Circuit diagram |
| Плата | Board/PCB | Hardware |
| Пак прошивок | Firmware pack | Collection |

### Technical Terms

| Russian | English | Context |
|---------|---------|---------|
| мозги | "Brains" / ECU | Colloquial for DME |
| ножка | Pin/Leg | IC pin |
| пин | Pin | Direct transliteration |
| флэш / флешка | Flash | Flash memory |
| запайка | Soldering | Assembly |
| выпайка | Desoldering | Removal |
| пятачки | Pads | PCB solder pads |
| смещение | Offset | Pin offset mounting |

### Firmware Naming

| Russian | English | Meaning |
|---------|---------|---------|
| АКПП | Auto / AT | Automatic transmission |
| МКПП | Manual / MT | Manual transmission |
| автомат | Auto | Automatic |
| мех / механика | Manual | Mechanical/Manual |
| лямбда | Lambda | With O2 sensors active |
| безлямбда / безлямбдовая | No-Lambda | O2 sensors disabled |
| безкатовая | Catless | Catalyst delete tune |
| сток / стоковая | Stock | Factory calibration |
| тюн / тюнинг | Tuned / Tune | Modified calibration |
| для | for | Application specifier |

### Feature Codes (M30B35 Pack)

| Code | Meaning |
|------|---------|
| EML | Elektronische Motorleistungsregelung (Electronic throttle) |
| ASC+T | Automatic Stability Control + Traction |
| c / с | with (Cyrillic "с" = Latin "s") |
| без | without |

---

## 📊 Project Statistics

| Metric | Count |
|--------|-------|
| Total firmware files | ~330 |
| ECU platforms supported | 10+ |
| Engine variants covered | 15+ |
| Vehicle models (E-codes) | 7 |
| Documentation files | 6 |
| PCB layout versions | 2 |
| ATtiny firmware versions | 2 |
| Archive total size | ~125 MB |

---

## 📜 Credits & Acknowledgments

- **Original Author:** Unknown — sourced from the Russian-speaking BMW tuning community (believed to originate from VK / Russian automotive forums)
- **English Translation & Documentation:** KingAustraliaGG
- **Community Resources:** MS4x.net, pazi88, OldSkullTuning, Bimmer Tuning Tools

---

## 📄 Disclaimer & License

This project is provided **for educational and archival purposes only**.

- The original Russian documentation and firmware files were sourced from publicly shared community resources. The original author is unknown.
- If you are the original author and would like attribution added or content removed, please open an issue.
- **No warranty is provided.** Use at your own risk. Modifying ECU firmware can damage your vehicle, void warranties, and violate emissions regulations.
- Firmware binaries (.bin files) in this archive are ECU calibration data, not copyrighted software applications. They are shared in the same spirit as the original community distribution.
- EWS/immobilizer deletion and emissions-related modifications may be illegal in your jurisdiction.

> **Note:** The address-line bank-switching technique documented here is generic and applicable to any ECU that uses external parallel EPROM/Flash — not just BMW. It has been successfully applied to GM/Delco MEMCAL-based ECUs (Holden, Buick, etc.) using the same principle.

---

*Last Updated: February 2026*
