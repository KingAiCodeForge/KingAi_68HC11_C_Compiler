#!/usr/bin/env python3
"""
datastream_reader.py — Real-Time ALDL Data Stream Reader
=========================================================
Continuously polls the VY V6 PCM for Mode 1 data stream and displays
live engine parameters (RPM, coolant temp, TPS, MAP, battery voltage).

Requires: pyserial
Usage:    python datastream_reader.py --port COM3
          python datastream_reader.py --port /dev/ttyUSB0 --log output.csv

Protocol sourced from OSE Flash Tool (VL400) decompilation.
Author: KingAustraliaGG
Date: 2026-02-15
"""

import time
import csv
import sys
import argparse
import logging
from datetime import datetime
from typing import Optional, Dict

from aldl_interface import (
    ALDLConnection, DEVICE_PCM, DEVICE_BCM,
    BAUD_FAST, MODE_1, build_mode1_request, hexdump
)

log = logging.getLogger('datastream')

# =============================================================================
# Known Mode 1 Data Stream Offsets — VY V6 ($060A)
# Offsets into the Mode 1 response payload (after header bytes).
# Sourced from XDF v2.09b definitions and OSE Plugin Logger.
# These need validation against actual Mode 1 responses.
# =============================================================================

# Approximate byte offsets in Mode 1 response (0-indexed from payload start)
# These are ESTIMATED from the XDF RAM addresses and need cross-referencing
# against actual Mode 1 packet captures. these could be wrong need to double check
STREAM_OFFSETS = {
    'rpm_period_hi':   0x02,  # RPM period high byte
    'rpm_period_lo':   0x03,  # RPM period low byte
    'coolant_raw':     0x05,  # Coolant temp (raw ADC, needs lookup)
    'tps_raw':         0x08,  # Throttle position (0-255)
    'map_raw':         0x0A,  # MAP sensor (raw ADC)
    'iat_raw':         0x0C,  # Intake air temp (raw ADC)
    'battery_raw':     0x10,  # Battery voltage (raw, /10 for volts)
    'o2_left':         0x12,  # Left bank O2 (0-255, ~128 = stoich)
    'o2_right':        0x13,  # Right bank O2
    'spark_advance':   0x15,  # Spark advance (degrees * 2)
    'iac_position':    0x18,  # IAC stepper position
    'injector_pw_hi':  0x1A,  # Injector pulse width high
    'injector_pw_lo':  0x1B,  # Injector pulse width low
}


def parse_datastream(raw: bytes) -> Dict[str, float]:
    """
    Parse Mode 1 response into human-readable values.
    
    Conversions based on XDF scaling formulas:
    - RPM = 120000000 / (period * 3) [for V6, 3 cylinders per revolution]
    - Coolant °C = raw * 0.75 - 40 (approximate linear, real uses lookup table)
    - TPS% = raw / 255 * 100
    - Battery V = raw / 10
    - Spark = raw / 2 degrees
    """
    result = {}

    if len(raw) < 0x20:
        return {'error': 'Response too short', 'raw_len': len(raw)}

    # Skip header bytes (device_id, length, mode) — typically 3 bytes
    payload = raw[3:] if len(raw) > 3 else raw

    try:
        # RPM from period counter
        rpm_hi = payload[STREAM_OFFSETS['rpm_period_hi']]
        rpm_lo = payload[STREAM_OFFSETS['rpm_period_lo']]
        period = (rpm_hi << 8) | rpm_lo
        if period > 0:
            result['rpm'] = round(120000000 / (period * 3))
        else:
            result['rpm'] = 0

        # Coolant temperature
        ct_raw = payload[STREAM_OFFSETS['coolant_raw']]
        result['coolant_c'] = round(ct_raw * 0.75 - 40, 1)

        # Throttle position
        tps_raw = payload[STREAM_OFFSETS['tps_raw']]
        result['tps_pct'] = round(tps_raw / 255 * 100, 1)

        # MAP sensor
        map_raw = payload[STREAM_OFFSETS['map_raw']]
        result['map_kpa'] = round(map_raw * 0.39, 1)  # Approximate scaling

        # Intake air temp
        iat_raw = payload[STREAM_OFFSETS['iat_raw']]
        result['iat_c'] = round(iat_raw * 0.75 - 40, 1)

        # Battery voltage
        batt_raw = payload[STREAM_OFFSETS['battery_raw']]
        result['battery_v'] = round(batt_raw / 10, 1)

        # O2 sensors
        result['o2_left'] = payload[STREAM_OFFSETS['o2_left']]
        result['o2_right'] = payload[STREAM_OFFSETS['o2_right']]

        # Spark advance
        spark_raw = payload[STREAM_OFFSETS['spark_advance']]
        result['spark_deg'] = round(spark_raw / 2, 1)

        # IAC position
        result['iac_steps'] = payload[STREAM_OFFSETS['iac_position']]

    except (IndexError, KeyError) as e:
        result['parse_error'] = str(e)

    return result


def format_display(data: Dict[str, float]) -> str:
    """Format parsed data for terminal display."""
    if 'error' in data:
        return f"  Error: {data['error']}"

    lines = [
        f"  RPM: {data.get('rpm', '?'):>6}     "
        f"TPS: {data.get('tps_pct', '?'):>5}%    "
        f"MAP: {data.get('map_kpa', '?'):>5} kPa",

        f"  CLT: {data.get('coolant_c', '?'):>5}°C    "
        f"IAT: {data.get('iat_c', '?'):>5}°C    "
        f"BAT: {data.get('battery_v', '?'):>5} V",

        f"  O2L: {data.get('o2_left', '?'):>5}      "
        f"O2R: {data.get('o2_right', '?'):>5}      "
        f"SPK: {data.get('spark_deg', '?'):>5}°",

        f"  IAC: {data.get('iac_steps', '?'):>5} steps",
    ]
    return '\n'.join(lines)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%H:%M:%S'
    )

    parser = argparse.ArgumentParser(
        description='VY V6 ALDL Data Stream Reader'
    )
    parser.add_argument('--port', '-p', required=True,
                        help='Serial port (COM3, /dev/ttyUSB0)')
    parser.add_argument('--baud', '-b', type=int, default=BAUD_FAST,
                        help=f'Baud rate (default: {BAUD_FAST})')
    parser.add_argument('--log', '-l', help='CSV log file path')
    parser.add_argument('--interval', '-i', type=float, default=0.5,
                        help='Poll interval in seconds (default: 0.5)')
    parser.add_argument('--raw', action='store_true',
                        help='Also print raw hex bytes')
    args = parser.parse_args()

    conn = ALDLConnection(args.port, args.baud)
    if not conn.open():
        sys.exit(1)

    csv_writer = None
    csv_file = None
    if args.log:
        csv_file = open(args.log, 'w', newline='')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([
            'timestamp', 'rpm', 'coolant_c', 'tps_pct', 'map_kpa',
            'iat_c', 'battery_v', 'o2_left', 'o2_right', 'spark_deg',
            'iac_steps'
        ])

    print("=" * 60)
    print("  VY V6 ALDL Data Stream Reader")
    print(f"  Port: {args.port} @ {args.baud} baud")
    print("  Press Ctrl+C to stop")
    print("=" * 60)

    # Disable chatter first for cleaner bus
    print("\nDisabling BCM/PCM chatter...")
    conn.disable_chatter(DEVICE_BCM)
    conn.disable_chatter(DEVICE_PCM)
    time.sleep(0.2)

    sample_count = 0
    try:
        while True:
            frame = build_mode1_request(DEVICE_PCM)
            response = conn.send_and_receive(frame, timeout_ms=3000)

            if response:
                sample_count += 1
                data = parse_datastream(bytes(response))

                # Terminal display
                print(f"\n--- Sample {sample_count} "
                      f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] ---")
                print(format_display(data))

                if args.raw:
                    print(f"  RAW: {hexdump(bytes(response))}")

                # CSV logging
                if csv_writer:
                    csv_writer.writerow([
                        datetime.now().isoformat(),
                        data.get('rpm', ''),
                        data.get('coolant_c', ''),
                        data.get('tps_pct', ''),
                        data.get('map_kpa', ''),
                        data.get('iat_c', ''),
                        data.get('battery_v', ''),
                        data.get('o2_left', ''),
                        data.get('o2_right', ''),
                        data.get('spark_deg', ''),
                        data.get('iac_steps', ''),
                    ])
                    csv_file.flush()
            else:
                print(".", end='', flush=True)

            time.sleep(args.interval)

    except KeyboardInterrupt:
        print(f"\n\nStopped. {sample_count} samples collected.")

    finally:
        # Re-enable chatter
        print("Re-enabling chatter...")
        conn.enable_chatter(DEVICE_BCM)
        conn.enable_chatter(DEVICE_PCM)
        conn.close()
        if csv_file:
            csv_file.close()
            print(f"Log saved to: {args.log}")


if __name__ == '__main__':
    main()
