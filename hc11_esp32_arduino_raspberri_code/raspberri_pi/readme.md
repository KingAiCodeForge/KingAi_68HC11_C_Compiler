# Raspberry Pi — ALDL ECU Python Tools

> **PROTOCOL: ALDL 8192 baud serial — NOT CAN bus.**
> All Python tools here communicate with the VY V6 Delco 09356445 via USB-TTL serial adapters over the ALDL single-wire bus.

## What's Here

| File | Status | Description |
|------|--------|-------------|
| `aldl_interface.py` | **TEMPLATE** | Full ALDL serial library — connection management, bus silence detection, frame TX/RX with echo cancellation, Mode 1/5/6/8/9/13, security seed-key unlock, kernel upload via Mode 6. ~24KB, well-structured class. **Needs testing on real hardware — timing constants may need tuning.** |
| `datastream_reader.py` | **TEMPLATE** | Live Mode 1 data stream reader — polls ECU, parses RPM/TPS/coolant/MAP/battery/spark/IAC, displays in terminal, optional CSV logging. **Data stream byte offsets need verification against XDF.** |
| `flash_patcher.py` | **TEMPLATE** | Full flash protocol: chatter disable → Mode 5 → security unlock → kernel upload → sector erase → write → verify. Also has offline binary patching with GM checksum correction. **Has not been tested on a real ECU — use with extreme caution.** |

## Dependencies
```bash
pip install pyserial
```

## Usage
```bash
# Read live data stream
python datastream_reader.py --port /dev/ttyUSB0

# Read with CSV logging
python datastream_reader.py --port COM3 --log session_001.csv

# Flash a patched binary (DANGEROUS — backup first!)
python flash_patcher.py --port /dev/ttyUSB0 --bin patched.bin --bank 1

# Offline binary patching (safe — just modifies a file)
python flash_patcher.py --patch --original stock.bin --modified tuned.bin --output patched.bin
```

## Hardware
- **Raspberry Pi 4/5** (or any Linux box with USB)
- **USB-TTL UART adapter** (CP2102, PL2303, FTDI FT232R) — must support 8192 baud
- ALDL connector: Pin A = data (to adapter TX/RX), Pin B = ground
- Level shifter if adapter is 3.3V only (ALDL data line is 5V/12V)

## Flash Protocol Sequence (what flash_patcher.py does)
```
1. Disable chatter (Mode 8 to BCM + PCM)
2. Enter flash mode (Mode 5 to PCM)
3. Security unlock (Mode 13: request seed → calculate key → send key)
4. Upload flash kernel (Mode 6: send HC11 code to PCM RAM at $0300)
5. Kernel takes over — communicates directly:
   a. Erase sector  (CMD 0x01 + sector address)
   b. Write data    (CMD 0x02 + address + length + data)
   c. Verify        (CMD 0x03 + address + length → reads back)
6. Exit kernel (CMD 0xFF)
7. Re-enable chatter (Mode 9)
```

## Template Warnings
- Data stream byte offsets are from OSE Enhanced Flash Tool decompilation
- Security key algorithm sourced from kernel_uploader.py POC — may vary by OS ID
- Flash kernel is assembled for M29W800DB chip — verify flash command addresses
- Timing constants (silence detection, frame timeouts) need real hardware tuning
- **Always dump the full bin and verify before writing anything**

## Notes
- On Windows use COM port names: `--port COM3`
- On Linux/RPi use: `--port /dev/ttyUSB0`
- 8192 baud is non-standard but pyserial handles it on most USB-TTL adapters
- CP2102 confirmed working at 8192 baud
- The flash protocol reads/writes at ~350-460 bytes/sec effective
- Full 128KB flash takes ~6.5 minutes, CAL-only (16KB) takes ~47 seconds
