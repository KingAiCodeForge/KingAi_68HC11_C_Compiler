## Will It Work on Delco 808 Ecotec or Buick Ecotec? And/or 28-pin/32-pin MEMCAL-Based ECUs?

### Short Answer

**YES** - The dual-mode switch technique can work on MEMCAL-based GM/Holden ECUs, but with important caveats.

---

## MEMCAL-Based ECUs (VN/VP/VR/VS/VT Era) - **Compatible**

### Long MEMCALs (28-pin DIP, 2-connector ECUs)

**Source: pcmhacking.net & mrmodule.com.au**

| Platform | Trans | EPROM Type | Size | Upgrade To | Dual-Mode? |
|----------|-------|------------|------|------------|------------|
| VN/VP V6 | Auto/Man | 27C128 | 16KB | 27C256 | ✅ Yes |
| VR V6 | Manual | 27C256 | 32KB | 27C512 | ✅ Yes |
| VR V6 | Auto | 27C512 | 64KB | 27C010 | ✅ Yes |
| VR/VS V8 | Manual | 27C256 | 32KB | 27C512 | ✅ Yes |
| VR V6 | Auto | 27C512 | 64KB | 27C010 | ✅ Yes |


**Custom OSE Firmware (Real-Time Tuning via NVRAM):**

| Firmware | Base Code | EPROM Type | Size | Notes |
|----------|-----------|------------|------|-------|
| OSE $12P | $12 | 27C256 | 32KB | Enhanced VR/VS manual code |
| OSE $11P | $11 | 27C512 | 64KB | Enhanced VR/VS auto code |

Long MEMCALs contain:

- **Memory EPROM** - Main program + calibration (the chip you swap)
- **NetRes** - Hardware config resistor network (cylinder count, backup fuel)
- **Knock Filter** - Analog ESC filter (V6 and HSV V8 only, code 3U... for V6, 1F... for V8)

### Short MEMCALs (32-pin DIP, 3-connector ECUs)

**VS 3-plug and VT onwards:**

| Platform | Trans | EPROM Type | Size | Upgrade To | Dual-Mode? |
|----------|-------|------------|------|------------|------------|
| VS V6 | Auto | 27C010 | 128KB | 27C020 | ✅ Yes (32-pin) |
| VT V6 | Auto/Man | 27C010 | 128KB | 27C020 | ✅ Yes (32-pin) |
| VT V8 (5.0L) | Auto/Man | 27C010 | 128KB | 27C020 | ✅ Yes (32-pin) |

Short MEMCALs only contain the EPROM chip - no NetRes or knock filter board.

> **Note:** For 128 KB ECUs (VS V6 short memcal), you would need a 27C020 (256 KB) to hold two images. The higher address line (A17) becomes the bank-select pin. The Russian schematic targets 32 KB/64 KB BMW EPROMs, but the principle is identical — only the chip and address pin change.

### How to Apply the Dual-Mode Technique

Same principle as BMW:

1. Use a **double-capacity EPROM** (e.g., 27C512 instead of 27C256)
2. Burn **Stock tune** to lower half (addresses 0x0000-0x7FFF)
3. Burn **Performance tune** to upper half (addresses 0x8000-0xFFFF)
4. Wire switch to **highest address pin (A15 on 27C512, A16 on 27C010)**
5. Both tunes must use the **same base code/mask ID** (e.g., both $12P or both $5D)

### Can You Switch While the Engine is Running? (Live Switching)

**YES - but with conditions!**

Based on the Russian BMW documentation and EPROM switching principles:

| Firmware Setup | Live Switch? | Notes |
|----------------|--------------|-------|
| Same base code, different calibrations only | ✅ **Yes** | Engine won't stall, seamless transition |
| Different full dumps (different base code) | ⚠️ **Maybe** | Engine may stall or run rough |
| Different ISN/EWS data | ❌ **No** | Immobilizer will kill engine |

**Why it works (same base code):**
- The CPU only reads calibration data (fuel maps, timing maps, etc.) from EPROM
- Switching address line A15/A16 instantly points to the other "half" of the chip
- CPU doesn't care - it just reads different calibration values on the next read cycle
- No reboot, no initialization delay

**From the Russian documentation:**
> "With this option [same base code, different calibrations], switching while driving is possible without problems because the base software is the same - only the calibrations are different."

> "The switching can be live with the engine running, even under load. The engine will not even cough or hesitate when switching."

---

### How This Compares to Moates/Commercial Solutions

| Product | Type | Live Switch? | Maps | Price |
|---------|------|--------------|------|-------|
| **Russian Dual-Mode Switch** | Address line toggle + ATtiny display | ✅ Yes | 2 | ~$20 DIY |
| **Moates Ostrich 2.0** | Full EPROM emulator (RAM-based) | ✅ Yes | Unlimited | ~$200 (discontinued) |
| **Moates G1/G2 Adapter** | Memcal adapter for emulator | N/A | - | ~$50 |
| **CobraRTP MotronicRT R6** | Universal EPROM emulator | ✅ Yes | Unlimited | ~$240 |
| **BNW Socket Booster** | Signal conditioning for memcal | N/A | - | ~$40 |

**Key Differences:**

- **Moates Ostrich/CobraRTP** = Full EPROM emulator, can change maps via laptop while running, unlimited maps, used for tuning development
- **Russian Dual-Mode Switch** = Simple hardware toggle, 2 pre-burned maps only, no laptop needed, cheap DIY solution, for end users who want stock/performance switch

The Russian system is **not** a Moates-style emulator - it's just a physical switch that changes which half of the EPROM the ECU reads from. Much simpler but limited to 2 maps (or 4 with quad-stack).

### Delco 808 ECU Specifics

The "Delco 808" typically refers to the MEMCAL-based Holden ECUs using $8 or $12 code variants:

- Uses removable MEMCAL module
- EPROM can be swapped/upgraded
- Address line switching works identically to BMW method
- **pcmhacking.net** has extensive documentation and bin files

> **TODO:** Can you do quad-stack on 512KB (4x 128KB bins) or on the 32KB OSE $12P / 64KB OSE $11P software? Needs more research.

---

## Flash-Based ECUs (VX/VY/VZ Era) - **NOT Compatible**

### Why It Won't Work

| Platform | Memory Type | Location | Dual-Mode? |
|----------|-------------|----------|------------|
| VX/VY N/A V6 | Internal Flash | Soldered to PCB | ❌ No |
| VZ | Internal Flash | Inside MCU | ❌ No |

Flash-based Ecotec ECUs (VU onwards) have:
- **Internal flash memory** embedded in the microprocessor
- No removable MEMCAL module
- No external EPROM to swap
- Tuning done via **OBD reflash** using ALDL/OSE Flash Tool

You cannot do hardware address-line switching on these because:
1. Memory is inside the CPU die
2. No physical access to address lines
3. Would require desoldering BGA chips

### Alternative for Flash ECUs

For VX/VY/VZ Ecotec, consider:
- **OSE Flash Tool** - Free, uses ALDL cable, can reflash via laptop
- **Map switching in code** - $12P code supports switching between two calibration sets via input pin
- Multiple calibration bins stored, switched via diagnostic input

---

## Buick 3800 / L67 Supercharged

### P04 ECM (1227727/1227730 style)

| ECM | EPROM Type | Dual-Mode? |
|-----|-----------|------------|
| 1227727 | 27C256 (MEMCAL) | ✅ Yes |
| 1227730 | 27C256 (MEMCAL) | ✅ Yes |
| 1228708 (Quad4) | 27C256 | ✅ Yes |

These use the same MEMCAL architecture as Holden - the technique works identically.

### Later 3800 Series II/III

Later PCMs (1996+ OBD-II) typically use:
- Internal flash memory
- No removable chip
- **Not compatible** with hardware dual-mode switching

---

## Summary Table

| ECU Type | Years | Memory | Dual-Mode Switch? |
|----------|-------|--------|-------------------|
| Holden VN/VP/VR/VS MEMCAL | 1988-1997 | External EPROM | ✅ **Yes** |
| Holden VS/VT Short MEMCAL | 1995-1999 | External EPROM | ✅ **Yes** |
| Holden VX/VY Flash | 2000-2004 | Internal Flash | ❌ **No** |
| Holden VZ | 2004-2006 | Internal Flash | ❌ **No** |
| GM 1227727/1227730 | 1987-1995 | MEMCAL EPROM | ✅ **Yes** |
| OBD-II Flash PCMs | 1996+ | Internal Flash | ❌ **No** |

---

## Resources

- **pcmhacking.net** - Holden/GM ECU hacking community, bin files, TunerPro XDFs
- **Mr Module (mrmodule.com.au)** - MEMCAL adapters, programming services
- **TunerPro RT** - Free tuning software with definition files
- **OSE Flash Tool** - For VX/VY flash-based ECUs
- **Chr0m3 Motorsport** - YouTube tutorials on Ecotec tuning

## Hardware Needed for MEMCAL Dual-Mode

1. **EPROM Programmer** - TL866II Plus, XGecu T48, GQ-4x4
2. **UV Eraser** - If using OTP EPROMs (not needed for EEPROM/Flash replacements)
3. **MEMCAL Adapter** - 28-pin or 32-pin depending on ECU type
4. **Double-capacity chip** - 27C512, 27SF512 (flash), or SST27SF512
5. **SPDT Toggle Switch** - For address line selection
6. **Optional: ATtiny display** - From original BMW project, shows current mode

---

## Reference: Original BMW ECU Compatibility

The Russian dual-mode switch project was originally designed for BMW. Here are the supported platforms from the original documentation:

### Bosch Motronic ECUs

| ECU | Stock Chip | Upgrade To | Switch Pin | Engines |
|-----|------------|------------|------------|---------|
| M1.1, M1.3, M3.1 | 27C256 | W27C512 | A15 (Pin 1) | M20, M30, M50 |
| M1.7, M3.3 | W27C512 | W27C010 | A16 (Pin 2) | M40, M42, M43, M50TU, M60 |

**Note for M1.7/M3.3:** The 27C010 has 4 more pins than 27C512. Install with offset - first 4 pins hang in air. Connect VCC to the NC pin position.

### Siemens MS4x ECUs

| ECU | Chip Type | Notes |
|-----|-----------|-------|
| MS42 | External Flash | M52TU (E39, E46) - Compatible |
| MS43 | External Flash | M54 (E39, E46, E53) - Compatible |

### Bosch ME7.x ECUs

| ECU | Chip Type | Notes |
|-----|-----------|-------|
| ME7.2 | External Flash | M62 V8 (E38, E39, E53) - Compatible |

### Transmission ECUs - Also Supported!

The dual-mode technique works on **any ECU with external flash** - including automatic transmission controllers:

| TCU | Application | Notes |
|-----|-------------|-------|
| 5HP30 | BMW E38/E39 5-speed auto | Firmware included in pack |

---

## Original Russian Documentation Files

The following files are included in the `Двурежимная прошивка` (Dual-Mode Firmware) folder:

### Documentation Files

| Russian Filename | English Translation | Description |
|------------------|---------------------|-------------|
| `Мануал двухрежимки BMW для всех ЭБУ.pdf` | Dual-Mode BMW Manual for All ECUs | Main technical manual (PDF) |
| `Как собрать переключатель.docx` | How to Build the Switch | Switch assembly guide |
| `Как создать файл двухрежимной прошивки.docx` | How to Create a Dual-Mode Firmware File | Firmware creation guide |

### Schematic Images

| Filename | Description |
|----------|-------------|
| `Общая схема.png` | **General Schematic** - Overall system wiring diagram |
| `Схема переключателя.jpg` | **Switch Schematic** - Detailed switch circuit diagram |
| `Плата.JPG` | **PCB Board** - Photo of assembled display PCB |

### Folder Translations

| Russian | English |
|---------|---------|
| `Двурежимная прошивка` | Dual-Mode Firmware |
| `Версия на 2 переключателя (ДВС и КПП)` | Version for 2 switches (Engine and Gearbox) |
| `Файлы для создания переключателя` | Files for Building the Switch |
| `Прошивки` | Firmwares |

---

## Advanced: 2-Switch Version (Engine + Transmission)

The Russian project includes a **Version 2** with dual switches for cars with both engine and transmission tuning:

**Folder:** `Версия на 2 переключателя (ДВС и КПП)` (Version for 2 switches - Engine and Gearbox)

**Contents:**

- `tuning switch rev2.hex` - ATtiny firmware for 2-switch display
- `version2.lay` - PCB layout (Sprint Layout format)
- Wiring diagram image

**Use Case:** Switch between stock/performance on both DME and TCU independently:
- Switch 1: Engine calibration (fuel, timing, rev limit)
- Switch 2: Transmission calibration (shift points, firmness, torque converter lockup)

---

## Included Firmware Files (BMW Reference)

The Russian project includes pre-made firmware bins for various BMW engines:

### M60 V8 Variants
| File | Description |
|------|-------------|
| M60B30 АКПП.BIN | M60B30 Auto |
| M60B30 МКПП.bin | M60B30 Manual |
| M60B30 безлямбда | M60B30 No Lambda (O2 delete) |
| M60B40 superchip | M60B40 Performance tune, no lambda |

### M50/M52 Variants
| File | Description |
|------|-------------|
| M50B25 Schnitzer | M50B25 AC Schnitzer tune |
| m50b20siemens | M50B20 Siemens MS41 |

### M30 Variants
| File | Description |
|------|-------------|
| M30B34_chip | M30B34 chip tune pack |
| M30B35 pack | M30B35 firmware collection |

### File Naming Key (Russian → English)
| Russian | English |
|---------|---------|
| МКПП | Manual transmission |
| АКПП | Automatic transmission |
| безлямбда | No lambda / O2 delete |
| безкатовая | Catless / cat delete |
| сток | Stock |
| тюн | Tuned |

---

## Switch Display Module Build (ATtiny Project)

For those who want a display showing which mode is active, the Russian project includes an ATtiny-based display module.

### Components Required

| Component | Value/Type | Notes |
|-----------|------------|-------|
| Microcontroller | **ATtiny 2313** | Pre-programmed with included .hex file |
| 7-Segment Display | Common cathode | Single digit, shows "1" or "2" |
| LED | Any color | Status indicator |
| Resistors | 510Ω SMD | Current limiting for display segments |
| Voltage regulator | LM2931 (5V) | Only needed if powering from 12V |
| Diode | 1N4007 or similar | Reverse polarity protection |
| Capacitors | 100µF, 100nF | Voltage regulator filtering |

### Power Options

| Source | Components Needed |
|--------|-------------------|
| **5V from ECU** | Just ATtiny + display + resistors (no regulator circuit) |
| **12V from car** | Full circuit with LM2931 regulator, diode, capacitors |

### Wiring Logic

| Switch Position | DME Wire | Display Shows |
|-----------------|----------|---------------|
| Position 1 | 5V (logic HIGH) | **1** (Stock) |
| Position 2 | GND (logic LOW) | **2** (Tuned) |

**Important:** The wire from the switch to the ECU's address pin (A15 or A16) must **float in air** - do NOT solder it to the PCB trace. The chip leg can break off easily!

### Files Included

| File | Purpose |
|------|---------|
| `Прошивка платы (Аттини).hex` | ATtiny2313 firmware |
| `Чертеж платы.lay` | PCB layout (Sprint Layout format) |
| `tuning switch rev2.hex` | Version 2 firmware (2-switch) |
| `version2.lay` | Version 2 PCB layout |

---

## Technical Notes

### CO Adjustment in M60B30 Firmwares

For M60B30 engine firmwares, CO trim is stored at:

| Parameter | Address |
|-----------|---------|
| CO Adjustment | **0xFE8C** |
| CO Trim Values | **0x7E88** to **0x7EB8** |

**Value interpretation:**
- `0x80` = 0 (neutral/stock)
- `0x00` = -127 (lean)
- `0xFE` = +127 (rich)

### Flash Chip Compatibility Notes

| Original | Replace With | Notes |
|----------|--------------|-------|
| 27C256 | W27C512 | Direct drop-in, same pinout |
| W27C512 | W27C010 | 4 extra pins - install with offset |
| 28Fxxx | 29Fxxx | ✅ Can replace 28 with 29 series |
| 29Fxxx | 28Fxxx | ❌ Cannot replace 29 with 28 series |

**Adapter recommended** for 28/29 series flash - constant desoldering damages PCB pads!

---

## How to Create a Dual-Mode Firmware File

There are two methods to create a dual-mode firmware file. This applies to **any** EPROM-based ECU (BMW, Holden, GM, etc.)

### Method 1: Combine Two Full Dumps (Simple but Risky)

1. Take two complete firmware dumps (stock + tuned)
2. Use **ALMI** program or a HEX editor
3. Append tuned firmware to end of stock firmware
4. Save - resulting file should be **exactly 2x the original size**

**Example:** 32KB stock + 32KB tuned = 64KB combined file

**Risks:**
- ⚠️ Live switching may cause engine stall (different base software)
- ⚠️ If EWS/immobilizer present, you must copy ISN from stock to tuned dump
- ⚠️ Exception: MS41 stores ISN in calibrations (can disable EWS via software or write `FF` to ISN area)

### Method 2: Calibration Swap (Recommended)

1. Take your **original full dump** (stock)
2. **Extract calibrations only** from tuned dump
3. Replace calibrations in stock dump with tuned calibrations
4. **Verify checksum** using appropriate tool
5. Combine this modified dump with original stock dump

**This is what MPPS, KESS, etc. do via OBD** - you're doing it manually.

**Benefits:**
- ✅ Live switching works perfectly (same base software)
- ✅ ISN/EWS remains intact (base software unchanged)
- ✅ No immobilizer issues

### Binary Structure

| Address Range | Content |
|---------------|---------|
| 0x0000 - 0x7FFF | **Mode 1** (Stock) - Switch = HIGH |
| 0x8000 - 0xFFFF | **Mode 2** (Tuned) - Switch = LOW |

For 27C010 (128KB → 256KB combined):

| Address Range | Content |
|---------------|---------|
| 0x00000 - 0x1FFFF | **Mode 1** (Stock) |
| 0x20000 - 0x3FFFF | **Mode 2** (Tuned) |

### Tools Mentioned in Russian Documentation

| Tool | Purpose |
|------|---------|
| **ALMI** | Firmware combining/splitting utility |
| **MiniPro** | TL866 programmer software (included in pack) |
| **HxD / Hex Editor** | Manual binary editing |
| **Checksum tools** | Verify firmware integrity after editing |

---

## Complete Firmware Library Index (From Russian Pack)

The Russian project includes an extensive library of pre-made firmwares organized by ECU type:

### Bosch Motronic 1.3 Folder Structure

```
bosch_motronic_1_3/
├── 320=325/           # M50B20/B25 (same tune)
├── 325+15ps/          # M50B25 +15hp tune
├── enzo-m20b20/       # M20B20 Enzo tune
├── enzo-m20b25/       # M20B25 Enzo tune
├── m30 535 m1.3/      # M30B35 E28/E34 535i
└── m30 b35 m1.3/      # M30B35 variants
```

### Siemens MS42 (M52TU) Folder Structure

```
MS_42/
├── E39/               # 5-Series (520i, 523i, 528i)
└── E46/
    ├── 320/           # 320i M52TUB20
    └── 328/           # 328i M52TUB28
```

### Siemens MS43 (M54) Folder Structure

```
MS_43/
├── E39/               # 5-Series (525i, 530i)
├── E46/
│   ├── 325i/          # 325i M54B25
│   └── 330i/          # 330i M54B30 (12+ calibration versions)
└── E53/               # X5 3.0i
```

### Bosch ME7.2 (M62 V8) Folder Structure

```
ME_7_2/
├── 0261204620_350411/ # E38 740i
├── 0261204620_350476/ # E39 540i
├── 0261204620_350516/ # Variant
├── 0261207106_368125/ # Later revision
└── X5 E53 4.4 2002... # X5 4.4i tuned
```

### Firmware File Naming Convention

Many files follow a pattern: `[BoschPartNum]_[BMWPartNum]_[variant].bin`

**Example:** `0261204620_350476` = Bosch ECU 0261204620, BMW calibration 350476

---

## ECU Identification Numbers (From Files)

Example from M30 3.5L M1.3 ECU:

| Field | Value |
|-------|-------|
| Bosch ECU Number | 0 261 200 179 |
| Bosch Firmware Number | 1 267 355 796 |
| BMW ECU Number | 1 726 685 |
| Hardware Code | 810 26RT2923 |
| Engine | M30 3.5L |
| Year | 1990 |
| ECU Type | Motronic 1.3 |

These numbers help identify compatible firmwares for your specific ECU.

---

## EWS (Electronic Immobilizer) Considerations

| ECU Type | ISN Location | Dual-Mode Impact |
|----------|--------------|------------------|
| Most ECUs | Base software | Must match if using different base software |
| MS41 | Calibrations | Can disable via software (write `FF` to ISN area) |
| MS42/43 | Separate EEPROM | Usually not affected by calibration swaps |

**If using Method 2 (calibration swap):** No ISN editing required - base software stays the same.

**If using Method 1 (full dump combine):** Copy ISN from your original dump to the tuned dump before combining.

---

## Testing the Switch After Assembly

From the Russian documentation - how to verify your switch is working correctly:

### Pre-Installation Test Procedure

1. **Power up the switch** (5V from bench supply or 12V with regulator circuit)
2. **Toggle the switch** and measure the DME output wire:
   - Position 1: Should read **5V (logic HIGH)**
   - Position 2: Should read **0V / GND (logic LOW)**
3. **Check display**: Should change between "1" and "2" as you toggle
4. If using LED indicator, it should toggle state with the switch

### After Installation Test

1. With ignition ON (engine off), toggle switch
2. Observe if ECU responds differently (may see different idle settings, fan behavior, etc.)
3. Start engine in Mode 1 (stock), let idle stabilize
4. Toggle to Mode 2 - engine should continue running smoothly if same base code
5. If engine stumbles or stalls, you may have mismatched base software

---

## Universal Application Principle

**Key insight from Russian documentation:**

> "Switching works on all ECUs that use external flash for firmware storage - whether transmission or engine ECUs, and not only on BMW but on **any car**. If your ECU is not in this manual, take a photo of the board - if there's a flash chip, this system can be implemented without problems."

This means the dual-mode technique is **not BMW-specific**. It works on:

- ✅ Any ECU with socketed EPROM (GM MEMCAL, Ford EEC-IV, etc.)
- ✅ Any ECU with external flash chip (28Fxxx, 29Fxxx series)
- ✅ Transmission controllers with external memory
- ✅ Standalone ECUs (MegaSquirt with external EPROM)
- ❌ NOT ECUs with internal flash (most OBD-II era vehicles)

---

## Original VK.com Image Links (May Be Expired)

The Russian documentation referenced these images hosted on VK.com (Russian social network). These may no longer be accessible:

### Switch Assembly Images
- `https://pp.userapi.com/c824700/v824700201/eefff/SbHgIj0Sqkc.jpg`
- `https://pp.userapi.com/c824700/v824700201/ef007/v37cV4-ccnQ.jpg`
- `https://pp.userapi.com/c824700/v824700201/ef019/cX-WKD1WF4g.jpg`

### Component Images
- `https://pp.userapi.com/c846216/v846216613/25a2c/fQ7JDeW8L9Y.jpg`
- `https://pp.userapi.com/c834203/v834203613/11088f/JK1ZVmRgcU4.jpg`

**Local alternatives:** Check the included image files:
- `Общая схема.png` - General system schematic
- `Схема переключателя.jpg` - Switch circuit schematic  
- `Плата.JPG` - Assembled PCB photo

---

## Author's Notes and Warnings

Direct quotes translated from the Russian documentation:

### On Chip Leg Breakage
> "The pin to which we solder the DME wire from the switch should remain in the air (not soldered to the board). The chip leg breaks off easily - **I killed several flash chips this way during experiments**. Be careful!"

### On PCB Damage from Desoldering
> "For 28 and 29 series flash chips, it's advisable to buy or make an adapter... Constant desoldering and soldering while you're perfecting the firmware will be destructive to the ECU board. With frequent desoldering/soldering, **the pads for soldering the legs fall off**, and constant heating with a hot air gun **deforms and damages the board**."

### On Tools Mentioned
> "Use the ALMI program (link will be at the bottom)" - Note: The ALMI link was not included in the archived documentation
> "Check the checksum using the program I posted in the group" - Refers to a VK.com group tool

### On EWS Disabling
> "MS41... EWS can be disabled either with a program (**there's a video on the channel on how to disable EWS2**), or manually by entering FF in the ISN area."

---

## Summary: Key Takeaways from Russian Documentation

1. **The technique is universal** - works on any external-flash ECU, not just BMW
2. **Live switching IS possible** - but only with same base software (calibration-only changes)
3. **Calibration swap is preferred** over full dump combining (safer, no ISN issues)
4. **Chip leg is fragile** - keep the switch wire floating, don't solder to PCB trace
5. **Use adapters** for soldered flash chips to avoid board damage
6. **28→29 series OK, 29→28 NOT OK** - flash chip compatibility rule
7. **5V power from ECU** is simpler than 12V with regulator circuit
8. **ALMI tool** for combining binaries (or use HxD hex editor manually)
9. **2-switch version** available for independent DME + TCU switching

---

## External References: Web Research on Dual-Mode Chip Switching

The following information was gathered from various English-language sources online that describe the same or similar dual-mode switching techniques.

### Method 1: Stacked Chips (johna.motortraders.net)

**Source:** "Dual Switchable Chips for BMW E30 M42" - johna's automotive blog

This method involves physically stacking two EPROMs and switching between them:

**Components Needed:**
- Two 27C256 EPROMs (original + copy, or stock + tune)
- SPDT toggle switch
- Two 22kΩ resistors
- Three thin wires (ribbon cable works well)
- Optional: 28-pin IC socket

**Procedure:**
1. Bend up pin 22 (active-low chip enable /CE or /OE) on both EPROMs
2. Stack one chip on top of the other
3. Solder all pins together **except** the bent pin 22s
4. Twist resistor leads together and solder to pin 28 (VCC)
5. Solder other resistor leads to pin 22 of each chip (pull-ups)
6. Wire switch center to one pin 22, outer pins to each chip's pin 22
7. Switch selects which chip is enabled

**Key Quote:**
> "I wouldn't recommend that you switch between chips with the engine running. I am not sure what the result is but it may damage something."

> "The 318is seems to tune itself to fuel quality, etc and store this information. When you disconnect the battery it seems to forget these settings and run rough for the first few miles."

---

### Method 2: Single Double-Capacity Chip with Address Line Switch (qcwo.com)

**Source:** "Dual Performance Chips" - Technical Domain (qcwo.com)

This method uses a single larger EPROM with both programs:

**The Concept:**
> "Dual chips are chips whose memory capacity doubles the memory capacity of the original chip, so two different, same-size programs can be written inside the new chip, and it can be selected between them on the fly, simply by using a small switch."

**Components:**
- 27C512 (64KB) EPROM replacing 27C256 (32KB)
- 1kΩ resistor
- SPDT switch
- Shielded 2-conductor wire (recommended)

**Circuit Details:**
- Pin 1 (A15) controls which half of the chip is read
- Resistor soldered between pins 1 and 28
- Switch wired to pins 1 and 14 (GND)
- **Critical:** Pin 1 must NOT be inserted into socket - leave floating!

**On Live Switching:**
> "In some cars, switching on the fly will have no effect. In these cars, for changes to take place, the car must be turned off, the switch flipped, and then the car turned on again."

> "This is because in those cars, as soon as turned on, the ROM chip is read and transferred to RAM memory, which is called ROM shadowing or ROM masking."

**On Wire Length:**
> "In most cases, the cables for the switch must not be longer than 12 inches... a shielded cable is recommended, and the shielding is connected to ground. Electrical noise can cause the switching of programs to become unstable and turn on the check engine light."

---

### Commercial Products Comparison (Moates)

**Source:** Moates.net - "OBD1 BMWs – what you need"

Moates offers commercial-grade tools for BMW ECU tuning:

| Product | Purpose | Price Range |
|---------|---------|-------------|
| **G2 0.6" Chip Adapter** | Allows 28-pin chips in 24-pin sockets | ~$30-50 |
| **BURN2** | USB EPROM programmer | ~$80-100 |
| **SST27SF512** | Flash-based EPROM replacement (rewritable) | ~$5-10 |
| **Ostrich 2.0** | Full EPROM emulator with trace feature | ~$200 (discontinued) |
| **SocketBooster 1.0** | Signal conditioning for reliable operation | ~$40 |

**BMW ECU Chip Types (from Moates):**
- Early ECUs: 27C32 or 27C64 (24-pin) - requires G2 adapter
- Later ECUs: 27C256 or 27C512 (28-pin) - direct fit for tools

**Recommended Software:**
- **TunerPro RT** - Free, supports Moates hardware
- **Renovelo Domino Tuning Suite** - Commercial, polished, for '413/'506 DMEs (E36 325i/525i/M3 93-95)

---

### Key Differences: DIY Switch vs Commercial Emulators

| Feature | DIY Dual-Mode Switch | Moates Ostrich / CobraRTP |
|---------|---------------------|---------------------------|
| **Maps** | 2 (or 4 with quad) | Unlimited (RAM-based) |
| **Live Tuning** | No | Yes - change while running |
| **Laptop Required** | No | Yes, for changes |
| **Cost** | ~$20 DIY | $200-250 |
| **Complexity** | Low | Medium |
| **Best For** | End users, "set and forget" | Tuners, development |

---

### Bimmerforums.com Tips

From the Bimmerforums community thread "Found this...":

**On Resistor Values:**
> "If you find that the tune is jumping from chip to chip, lower the value of the resistors, you can go as low as 2k, it should work."

**On Pin 22 Function:**
> "When pin 22 gets a low signal this enables the 27C512 chip to enable data output. The 22k resistors are pull ups, so when the switch selects..."

This suggests the 22kΩ pull-up resistors may be too weak in some applications - try 2kΩ to 10kΩ if you experience instability.

---

### ROM Shadowing Explanation

Some ECUs copy the ROM contents to faster RAM at startup (called "ROM shadowing" or "ROM masking"). In these ECUs:

- ❌ Live switching will **NOT** work
- ✅ Switch must be in desired position **before** power-on
- ✅ To change modes, turn ignition OFF, flip switch, turn ON

This is why the Russian documentation specifies "same base software" for live switching - if the ECU shadows the entire ROM at boot, the base software would also need to be identical for seamless mid-operation switching.
