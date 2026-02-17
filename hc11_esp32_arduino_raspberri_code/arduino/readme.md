# Arduino — ALDL ECU Interface Sketches

> **PROTOCOL: ALDL 8192 baud serial — NOT CAN bus.**
> All sketches here communicate with the VY V6 Delco 09356445 ECU via single-wire ALDL serial.

## What's Here

| Sketch | Status | Description |
|--------|--------|-------------|
| `aldl_bluetooth_mega/ALDL-Arduino-mega.ino` | **WORKING** | Bluetooth ALDL bridge with wideband O2 input. From joukoy (ALDL-bt-wb-main). Confirmed working code — bridges BT serial ↔ ALDL 8192 baud on Mega 2560 with WB O2 analog on A0. |
| `aldl_reader/aldl_reader.ino` | **TEMPLATE** | Mode 1 data stream reader with parsed display. Data stream byte offsets (RPM, TPS, coolant, etc.) are approximate and need verification against XDF. Uses `shared/aldl_protocol.h`. |
| `memory_dumper/memory_dumper.ino` | **TEMPLATE** | Mode 6 kernel upload to PCM RAM + memory read back. Uploads a small HC11 read kernel to $0300, which reads memory and sends bytes back over ALDL. Interactive command parser. **WARNING: replaces running ECU code — KOEO only.** |

## Hardware Requirements
- **Arduino Mega 2560** (3 hardware UARTs: Serial=USB debug, Serial1=ALDL, Serial2=Bluetooth)
- Level shifter / protection: 100R resistors on TX3/RX3 lines (joukoy design)
- 12-pin GM ALDL connector: Pin A=data, Pin B=ground, Pin F=+12V
- For BT bridge: HC-05/HC-06/JDY-33 Bluetooth module on Serial2
- For WB O2: AEM X-Series or Innovate MTX-L analog output on A0

## Pin Connections (Mega 2560)
```
Sketch              ALDL           BT Module       Debug
──────              ────           ─────────       ─────
aldl_reader         Serial1        —               Serial (USB)
                    Pin 19 RX1     —               115200 baud
                    Pin 18 TX1     —

memory_dumper       Serial1        —               Serial (USB)
                    Pin 19 RX1     —               115200 baud
                    Pin 18 TX1     —

aldl_bluetooth_mega Serial3        Serial2          Serial (USB)
                    RX3+100R       TX2→BT RX       115200 baud
                    TX3+100R       RX2←BT TX
```

## ALDL Connector Pinout
```
Pin A = ALDL Data (serial, single-wire, bidirectional)
Pin B = Ground
Pin F = +12V Battery
Pin M = Ground (chassis)
```

## Notes
- **Always use Mega** — multiple hardware UARTs needed (ALDL + debug + optional BT)
- 8192 baud is non-standard — `HardwareSerial` handles it fine, `SoftwareSerial` may not
- 160 baud is also supported on some older GM ALDL ECUs but the VY V6 uses 8192
- Start with **key-on engine-off (KOEO)** for safe testing
- The `aldl_reader` and `memory_dumper` use `../shared/aldl_protocol.h` — symlink or copy it
- Data stream byte offsets in the reader are approximate from OSE decompilation — cross-reference with XDF definitions before trusting the parsed values