"""
ALDL Serial Bridge — Phase 1
==============================

Connects to a VY V6 Delco PCM over ALDL (8192 baud, OBD-II pin 9)
via USB-serial + MAX232 level shifter.

Supports:
  - Enter/exit diagnostics mode
  - Mode 1 data stream read (RPM, CLT, TPS, MAP, battery, spark)
  - Mode 4 command passthrough
  - CSV/JSON logging
  - Continuous polling mode

⚠ PINOUT NOTE: The ALDL protocol and serial parameters are well-documented
   and correct. Physical wiring (which PCM connector pin maps to OBD pin 9)
   should be verified — see bench_config.py for connector pin placeholders.

Usage:
  python aldl_bridge.py --port COM3 --mode read
  python aldl_bridge.py --port COM3 --mode poll --interval 0.5
  python aldl_bridge.py --port COM3 --mode diag

Requirements:
  pip install pyserial
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import serial
except ImportError:
    print("ERROR: pyserial not installed. Run: pip install pyserial")
    sys.exit(1)

from aldl_frame import (
    ALDLFrame,
    Mode1Response,
    build_enter_diagnostics,
    build_exit_diagnostics,
    build_mode1_request,
    build_mode4_frame,
    hex_dump,
    parse_mode1_response,
    parse_raw_frame,
    verify_checksum,
)
from bench_config import ALDL_BAUD, ALDL_DATABITS, ALDL_PARITY, ALDL_STOPBITS


class ALDLBridge:
    """
    Serial bridge to Delco PCM over ALDL.

    Handles connection, frame TX/RX, and response parsing.

    ⚠ Physical connection requires:
       - USB-serial adapter (FTDI/CH340)
       - MAX232 level shifter (12V inverted ↔ TTL)
       - OBD-II pin 9 → MAX232 T1IN, pin 5 → GND
       - Verify pinout before connecting!
    """

    def __init__(self, port: str, timeout: float = 2.0, verbose: bool = False):
        self.port = port
        self.timeout = timeout
        self.verbose = verbose
        self.serial: Optional[serial.Serial] = None
        self.in_diagnostics = False
        self.log_entries: list[dict] = []

    def connect(self) -> bool:
        """Open serial connection at 8192 baud."""
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=ALDL_BAUD,
                bytesize=ALDL_DATABITS,
                parity=ALDL_PARITY,
                stopbits=ALDL_STOPBITS,
                timeout=self.timeout,
                write_timeout=self.timeout,
            )
            if self.verbose:
                print(f"Connected to {self.port} at {ALDL_BAUD} baud")
            return True
        except serial.SerialException as e:
            print(f"ERROR: Cannot open {self.port}: {e}")
            return False

    def disconnect(self):
        """Close serial connection."""
        if self.serial and self.serial.is_open:
            if self.in_diagnostics:
                self.exit_diagnostics()
            self.serial.close()
            if self.verbose:
                print(f"Disconnected from {self.port}")

    def send_frame(self, frame: ALDLFrame) -> bool:
        """Send a built ALDL frame over serial."""
        if not self.serial or not self.serial.is_open:
            print("ERROR: Not connected")
            return False

        if self.verbose:
            print(f"  TX: {hex_dump(frame.raw)}")

        try:
            self.serial.write(frame.raw)
            self.serial.flush()
            return True
        except serial.SerialException as e:
            print(f"ERROR: Write failed: {e}")
            return False

    def receive_response(self, max_bytes: int = 256) -> Optional[bytes]:
        """
        Read a response frame from the PCM.

        The PCM echoes back the request then sends its response.
        This reads until we get a valid checksummed frame or timeout.
        """
        if not self.serial or not self.serial.is_open:
            return None

        try:
            # Read available bytes (PCM response)
            raw = self.serial.read(max_bytes)
            if raw:
                if self.verbose:
                    print(f"  RX: {hex_dump(raw)}")
                return raw
            else:
                if self.verbose:
                    print("  RX: (timeout — no response)")
                return None
        except serial.SerialException as e:
            print(f"ERROR: Read failed: {e}")
            return None

    def enter_diagnostics(self) -> bool:
        """Send Mode $0A to enter diagnostic mode."""
        print("Entering diagnostics mode...")
        frame = build_enter_diagnostics()
        if self.send_frame(frame):
            resp = self.receive_response()
            if resp:
                self.in_diagnostics = True
                print("  → PCM acknowledged diagnostic mode")
                return True
            else:
                print("  → No response (PCM may not be powered or cable issue)")
        return False

    def exit_diagnostics(self) -> bool:
        """Send Mode $0F to exit diagnostic mode."""
        print("Exiting diagnostics mode...")
        frame = build_exit_diagnostics()
        if self.send_frame(frame):
            self.in_diagnostics = False
            resp = self.receive_response()
            print("  → Returned to normal mode")
            return True
        return False

    def read_mode1(self) -> Optional[Mode1Response]:
        """
        Send Mode 1 request and parse the data stream response.
        Returns parsed Mode1Response or None on failure.
        """
        frame = build_mode1_request()
        if not self.send_frame(frame):
            return None

        raw = self.receive_response()
        if not raw:
            return None

        # Try to find a valid response frame in the received bytes
        # PCM may echo back our request first, then send response
        for start in range(len(raw)):
            if start + 3 <= len(raw):
                candidate = raw[start:]
                parsed = parse_raw_frame(candidate)
                if parsed and parsed.mode == 0x01:
                    return parse_mode1_response(parsed.data)

        if self.verbose:
            print("  → Could not parse Mode 1 response")
        return None

    def send_mode4(self, payload: bytes) -> Optional[bytes]:
        """
        Send a Mode 4 frame and return the response.

        ⚠ CAUTION: Mode 4 activates actuators (relays, solenoids).
           Only use on bench or with engine off (unless you know what you're doing).
        """
        if not self.in_diagnostics:
            print("WARNING: Not in diagnostics mode — sending Mode $0A first")
            if not self.enter_diagnostics():
                return None

        frame = build_mode4_frame(payload)
        if self.send_frame(frame):
            return self.receive_response()
        return None

    def poll_mode1(self, interval: float = 1.0, count: int = 0, log_file: Optional[str] = None):
        """
        Continuously poll Mode 1 data stream at given interval.

        Args:
            interval: Seconds between polls
            count:    Number of readings (0 = infinite until Ctrl+C)
            log_file: Optional CSV file path for logging
        """
        csv_writer = None
        csv_file = None
        if log_file:
            csv_file = open(log_file, "w", newline="")
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([
                "timestamp", "rpm", "coolant_c", "tps_pct", "map_kpa",
                "spark_deg", "battery_v", "iac_steps", "vehicle_speed", "o2_mv"
            ])
            print(f"Logging to {log_file}")

        if not self.enter_diagnostics():
            return

        iteration = 0
        try:
            print("\nPolling Mode 1 data stream (Ctrl+C to stop)...\n")
            print(f"{'Time':>12} | {'RPM':>6} | {'CLT°C':>5} | {'TPS%':>5} | "
                  f"{'MAP':>5} | {'SPK°':>5} | {'BATT':>5} | {'IAC':>4} | {'SPD':>4}")
            print("-" * 75)

            while count == 0 or iteration < count:
                resp = self.read_mode1()
                now = datetime.now().strftime("%H:%M:%S.%f")[:-3]

                if resp:
                    print(f"{now:>12} | {resp.rpm or 0:>6.0f} | {resp.coolant_c or 0:>5.0f} | "
                          f"{resp.tps_pct or 0:>5.1f} | {resp.map_kpa or 0:>5.0f} | "
                          f"{resp.spark_deg or 0:>5.1f} | {resp.battery_v or 0:>5.1f} | "
                          f"{resp.iac_steps or 0:>4d} | {resp.vehicle_speed or 0:>4d}")

                    if csv_writer:
                        csv_writer.writerow([
                            now, resp.rpm, resp.coolant_c, resp.tps_pct, resp.map_kpa,
                            resp.spark_deg, resp.battery_v, resp.iac_steps,
                            resp.vehicle_speed, resp.o2_mv,
                        ])
                else:
                    print(f"{now:>12} | {'NO RESPONSE':^65}")

                # Log entry for JSON export
                self.log_entries.append({
                    "timestamp": now,
                    "iteration": iteration,
                    "data": resp.__dict__ if resp else None,
                })

                iteration += 1
                time.sleep(interval)

        except KeyboardInterrupt:
            print(f"\n\nStopped after {iteration} readings.")

        finally:
            if csv_file:
                csv_file.close()
                print(f"Log saved to {log_file}")

            self.exit_diagnostics()

    def export_log_json(self, path: str):
        """Export accumulated log entries to JSON."""
        with open(path, "w") as f:
            json.dump({
                "port": self.port,
                "baud": ALDL_BAUD,
                "entries": self.log_entries,
                "count": len(self.log_entries),
            }, f, indent=2, default=str)
        print(f"JSON log exported to {path}")


# =============================================================================
#  CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="ALDL Serial Bridge — VY V6 Delco PCM communicator",
        epilog="⚠ Verify physical pinout before connecting to real hardware!"
    )
    parser.add_argument("--port", required=True, help="Serial port (e.g. COM3, /dev/ttyUSB0)")
    parser.add_argument("--mode", choices=["read", "poll", "diag", "raw"],
                        default="read", help="Operation mode")
    parser.add_argument("--interval", type=float, default=1.0,
                        help="Poll interval in seconds (for --mode poll)")
    parser.add_argument("--count", type=int, default=0,
                        help="Number of readings (0=infinite, for --mode poll)")
    parser.add_argument("--log-csv", type=str, default=None,
                        help="CSV log file path")
    parser.add_argument("--log-json", type=str, default=None,
                        help="JSON log file path")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show raw hex frames")

    args = parser.parse_args()

    bridge = ALDLBridge(port=args.port, verbose=args.verbose)

    if not bridge.connect():
        sys.exit(1)

    try:
        if args.mode == "read":
            # Single Mode 1 read
            if bridge.enter_diagnostics():
                resp = bridge.read_mode1()
                if resp:
                    print(f"\n{resp}")
                else:
                    print("No Mode 1 response received.")
                bridge.exit_diagnostics()

        elif args.mode == "poll":
            bridge.poll_mode1(
                interval=args.interval,
                count=args.count,
                log_file=args.log_csv,
            )

        elif args.mode == "diag":
            # Enter diagnostics and wait
            if bridge.enter_diagnostics():
                print("\nIn diagnostics mode. Press Enter to exit...")
                input()
                bridge.exit_diagnostics()

        elif args.mode == "raw":
            # Raw hex input mode
            if bridge.enter_diagnostics():
                print("\nRaw frame mode. Enter hex bytes (e.g. '04 14 00 ...') or 'quit':")
                while True:
                    line = input("> ").strip()
                    if line.lower() in ("quit", "exit", "q"):
                        break
                    try:
                        raw_bytes = bytes.fromhex(line.replace(" ", ""))
                        bridge.serial.write(raw_bytes)
                        resp = bridge.receive_response()
                        if resp:
                            print(f"  Response: {hex_dump(resp)}")
                    except ValueError:
                        print("  Invalid hex. Format: '04 14 00 ...'")
                bridge.exit_diagnostics()

        # Export JSON log if requested
        if args.log_json and bridge.log_entries:
            bridge.export_log_json(args.log_json)

    finally:
        bridge.disconnect()


if __name__ == "__main__":
    main()
