# ESP32 — ALDL ECU Interface + Wi-Fi Tool

> **PROTOCOL: ALDL 8192 baud serial — NOT CAN bus.**
> The VY V6 Delco uses ALDL single-wire serial. The ESP32 TWAI/CAN library in `esp32_twai_can_lib/` is reference code only — it does NOT apply to this ECU.


## Open Question

> ALDL likely works over Bluetooth — Red Devil River sell Bluetooth ALDL adapters for GM and Holden 14-pin and 10-pin connectors. Protocol compatibility needs confirmation.

## What's Here

| Sketch/Folder | Status | Description |
|---------------|--------|-------------|
| `aldl_wifi_interface/aldl_wifi_interface.ino` | **TEMPLATE** | Full Wi-Fi AP + WebSocket real-time ALDL tool. Creates hotspot "KingAI-ECU", serves web dashboard with live gauges (RPM, TPS, coolant, MAP, battery, spark, IAT, IAC), Mode 5/13 security unlock, chatter control. Uses `shared/aldl_protocol.h`. **Data stream byte offsets need verification against XDF.** |
| `esp32_twai_can_lib/` | **⚠️ NOT APPLICABLE — CAN BUS** | ESP32 TWAI/CAN library from sorek. CAN bus does NOT exist on the VY V6 Delco. Kept as reference for future CAN-based ECU projects (E38 LS1/LS2, later Holdens). **Needs complete rewrite to be useful for ALDL ECUs.** |

## Wi-Fi Interface Features
- **AP Mode**: Creates Wi-Fi network "KingAI-ECU" (password: flashtool123)
- **Web Dashboard**: Dark theme with live gauges, all served from ESP32 flash
- **WebSocket**: Real-time data streaming at ~100ms intervals
- **Controls**: Start/stop data stream, disable/enable chatter, Mode 5, security unlock
- **Libraries needed**: WiFi, WebServer, WebSocketsServer, ArduinoJson, HardwareSerial

## Hardware
- **ESP32-S3** (or any ESP32 with UART1/UART2)
- GPIO16 (RX2) ← ALDL data (via 3.3V↔5V/12V level shifter)
- GPIO17 (TX2) → ALDL data (via level shifter)
- ALDL Pin A = data, Pin B = ground

## Template Warnings
- Data stream byte offsets (RPM at 0x02-0x03, TPS at 0x08, etc.) are from OSE decompilation
- These need cross-referencing with the VX VY_V6_$060A_Enhanced XDF definitions
- Security key algorithm may need tuning for specific OS IDs
- Flash read/write timing needs real hardware testing

## About esp32_twai_can_lib/
This is an ESP32 TWAI (Two-Wire Automotive Interface) CAN bus library by sorek.
**It cannot be used with the VY V6 Delco** because:
- The Delco 09356445 has NO CAN bus — it uses ALDL serial (single-wire, 8192 baud)
- TWAI/CAN uses differential signaling (CAN-H/CAN-L) — completely different protocol
- The ESP32 TWAI peripheral is dedicated CAN hardware, not repurposable for ALDL

It's kept here as reference for:
- Future E38 LS1/LS2 ECU projects (which DO use CAN)
- Understanding the ESP32 TWAI driver API structure
- Adapting the frame-based TX/RX patterns to an ALDL equivalent

## Notes
- ESP32 `HardwareSerial` handles 8192 baud fine on UART2
- `yield()` calls in main loop prevent ESP32 watchdog resets
- WebSocket server runs on port 81, HTTP on port 80
