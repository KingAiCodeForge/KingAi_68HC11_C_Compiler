#!/usr/bin/env python3
"""
aldl_interface.py — ALDL Serial Communication Library for VY V6 Delco PCMs
============================================================================
Core Python library for ALDL protocol communication with HC11-based ECUs.
Used by Raspberry Pi tools and can be imported by any Python project.

Protocol sourced from:
  - OSE Flash Tool (VL400) decompilation
  - kernel_uploader.py POC (hc11_virtual_emulator/poc/)
  - pcmhacking.net community documentation
  - python-OBD (brendan-w) serial patterns

Target: Delco 09356445 (VY V6 L36) - Motorola 68HC11F1
Author: KingAustraliaGG
Date: 2026-02-15
"""

import serial
import serial.tools.list_ports
import time
import struct
import logging
from typing import Optional, List, Tuple, Dict

# =============================================================================
# Logging
# =============================================================================
log = logging.getLogger('aldl')

# =============================================================================
# Protocol Constants
# Sourced from: OSE Flash Tool decompilation + kernel_uploader.py
# =============================================================================

# Device IDs on ALDL bus
DEVICE_PCM = 0xF4       # Powertrain Control Module
DEVICE_BCM = 0xF1       # Body Control Module
DEVICE_IPC = 0xF0       # Instrument Panel Cluster

# Baud rates
BAUD_FAST = 8192         # Standard ALDL (VN-VZ Holden Delco)
BAUD_SLOW = 160          # Legacy datastream

# ALDL Modes
MODE_1  = 0x01           # Data stream request
MODE_3  = 0x03           # Read DTCs
MODE_4  = 0x04           # Actuator test / override
MODE_5  = 0x05           # Flash programming entry
MODE_6  = 0x06           # Upload/execute code in RAM
MODE_7  = 0x07           # Clear DTCs
MODE_8  = 0x08           # Disable chatter
MODE_9  = 0x09           # Enable chatter
MODE_10 = 0x0A           # Enter diagnostics
MODE_13 = 0x0D           # Security access (seed-key)

# Frame constants
LENGTH_OFFSET = 85       # Length byte = payload + 85
SIMPLE_LENGTH = 0x56     # 86 = 85+1 (mode byte only)

# Responses
RESP_OK       = 0xAA
RESP_REJECTED = 0xCC
RESP_FAIL     = 0x55

# Security
PCM_SECURITY_MAGIC = 37709  # 0x934D

# Bank IDs for Mode 6 flash operations
BANK_1_ID = 0x48
BANK_2_ID = 0x58
BANK_3_ID = 0x50

# Timing
SILENCE_WAIT_MS = 20     # Bus silence before TX
COMM_TIMEOUT_MS = 2000   # Default RX timeout
MAX_RETRIES = 5

# HC11F1 SCI Register addresses (for reference in kernels)
REG_BAUD  = 0x102B
REG_SCCR2 = 0x102D
REG_SCSR  = 0x102E
REG_SCDR  = 0x102F

# COP Watchdog
REG_COPRST = 0x103A

# VY V6 RAM addresses (from XDF v2.09b)
RAM_RPM_PERIOD   = 0x00A2
RAM_COOLANT_TEMP = 0x0092
RAM_TPS_RAW      = 0x0052
RAM_MAP_RAW      = 0x0063
RAM_IAT_RAW      = 0x0094
RAM_BATTERY_V    = 0x0065
RAM_O2_LEFT      = 0x006E
RAM_O2_RIGHT     = 0x006F
RAM_ENGINE_STATE = 0x0021


# =============================================================================
# Checksum Helpers
# =============================================================================

def aldl_checksum(data: bytes) -> int:
    """
    Calculate ALDL checksum.
    Sum all bytes, checksum = (256 - sum) & 0xFF
    From OSE Flash Tool protocol.
    """
    total = sum(data) & 0xFF
    return (256 - total) & 0xFF


def verify_checksum(frame: bytes) -> bool:
    """Verify an ALDL frame's checksum (last byte)."""
    if len(frame) < 2:
        return False
    expected = aldl_checksum(frame[:-1])
    return frame[-1] == expected


# =============================================================================
# Frame Builders
# Sourced from OSE ALDLFunctions.cs
# =============================================================================

def build_simple_frame(device_id: int, mode: int) -> bytearray:
    """
    Build simple 4-byte ALDL command: [DeviceID, 0x56, Mode, Checksum]
    From OSE: length 0x56 = 85+1 (just mode byte as payload).
    """
    frame = bytearray([device_id, SIMPLE_LENGTH, mode])
    frame.append(aldl_checksum(frame))
    return frame


def build_mode1_request(device_id: int = DEVICE_PCM) -> bytearray:
    """
    Request Mode 1 data stream.
    TX: [DeviceID, 0x57, 0x01, 0x00, Checksum]
    Byte after mode = message number (0x00 = all)
    """
    frame = bytearray([device_id, 0x57, MODE_1, 0x00])
    frame.append(aldl_checksum(frame))
    return frame


def build_mode4_frame(device_id: int, control_bytes: bytes) -> bytearray:
    """
    Build Mode 4 actuator override frame.
    TX: [DeviceID, LengthByte, 0x04, control_byte1, ..., Checksum]
    From OSE Mode4 handler and mode4_responder.c example.
    """
    payload_len = 1 + len(control_bytes)  # mode + control bytes
    length_byte = LENGTH_OFFSET + payload_len
    frame = bytearray([device_id, length_byte, MODE_4])
    frame.extend(control_bytes)
    frame.append(aldl_checksum(frame))
    return frame


def build_security_seed_request(device_id: int = DEVICE_PCM) -> bytearray:
    """
    Request security seed for flash access.
    From OSE ALDLFunctions.cs UnlockFlashPCM():
        TX: [DeviceID, 0x57, 0x0D, 0x01, Checksum]
    """
    frame = bytearray([device_id, 0x57, MODE_13, 0x01])
    frame.append(aldl_checksum(frame))
    return frame


def build_security_key_send(device_id: int, key: int) -> bytearray:
    """
    Send calculated security key.
    From OSE: TX [DeviceID, 0x59, 0x0D, 0x02, key_hi, key_lo, Checksum]
    """
    key_hi = (key >> 8) & 0xFF
    key_lo = key & 0xFF
    frame = bytearray([device_id, 0x59, MODE_13, 0x02, key_hi, key_lo])
    frame.append(aldl_checksum(frame))
    return frame


def calculate_security_key(seed_hi: int, seed_lo: int) -> int:
    """
    Calculate PCM security key from seed.
    From OSE ALDLFunctions.cs:
        key = 37709 - (seed_low * 256 + seed_high)
        if key < 0: key += 65536
    Note: byte order is swapped (low * 256 + high)
    """
    seed = seed_lo * 256 + seed_hi
    key = PCM_SECURITY_MAGIC - seed
    if key < 0:
        key += 65536
    return key


def build_mode6_upload_chunk(device_id: int, chunk_data: bytes,
                              load_addr: int, bank_id: int) -> bytearray:
    """
    Build Mode 6 upload frame (upload code to PCM RAM).
    From OSE Mode6VXYUploadExec():
        TX: [DeviceID, LenByte, 0x06, BankID, AddrHi, AddrLo, ...data..., Checksum]
    """
    payload_len = 1 + 1 + 2 + len(chunk_data)  # mode + bank + addr(2) + data
    length_byte = LENGTH_OFFSET + payload_len
    addr_hi = (load_addr >> 8) & 0xFF
    addr_lo = load_addr & 0xFF
    frame = bytearray([device_id, length_byte, MODE_6, bank_id, addr_hi, addr_lo])
    frame.extend(chunk_data)
    frame.append(aldl_checksum(frame))
    return frame


# =============================================================================
# Hex dump helper (from kernel_uploader.py)
# =============================================================================

def hexdump(data: bytes, prefix: str = '') -> str:
    """Format bytes as hex string for logging."""
    if not data:
        return f"{prefix}<empty>"
    hex_str = ' '.join(f'{b:02X}' for b in data)
    return f"{prefix}[{len(data):3d}] {hex_str}"


# =============================================================================
# ALDLConnection — Serial communication class
# Pattern informed by python-OBD (brendan-w) and OSE Flash Tool
# =============================================================================

class ALDLConnection:
    """
    ALDL serial connection for HC11-based Delco ECUs.
    
    Handles low-level serial I/O including:
    - Bus silence detection (from OSE DetectSilence)
    - Frame TX with echo handling
    - Frame RX with timeout
    - Automatic port scanning (from python-OBD scan_serial pattern)
    
    Usage:
        conn = ALDLConnection('/dev/ttyUSB0')
        conn.open()
        response = conn.send_command(DEVICE_PCM, MODE_1)
        conn.close()
    """

    def __init__(self, port: Optional[str] = None, baud: int = BAUD_FAST):
        self.port = port
        self.baud = baud
        self.ser: Optional[serial.Serial] = None
        self.echo_enabled = True  # Most ALDL cables echo TX bytes

    # -------------------------------------------------------------------------
    # Port Management
    # -------------------------------------------------------------------------

    @staticmethod
    def scan_ports() -> List[str]:
        """
        Scan for available serial ports.
        Pattern from python-OBD utils.py scan_serial().
        """
        ports = []
        for p in serial.tools.list_ports.comports():
            try:
                s = serial.Serial(p.device)
                s.close()
                ports.append(p.device)
            except (serial.SerialException, OSError):
                pass
        return ports

    def open(self) -> bool:
        """
        Open serial port for ALDL communication.
        Serial config: 8192 baud, 8N1 (standard ALDL).
        Pattern from python-OBD ELM327.__init__().
        """
        if self.port is None:
            available = self.scan_ports()
            if not available:
                log.error("No serial ports found")
                return False
            self.port = available[0]
            log.info(f"Auto-selected port: {self.port}")

        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baud,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=0.1,
                write_timeout=1.0,
            )
            time.sleep(0.1)
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            log.info(f"Opened {self.port} @ {self.baud} baud (8N1)")
            return True
        except serial.SerialException as e:
            log.error(f"Failed to open {self.port}: {e}")
            return False

    def close(self):
        """Close serial port."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            log.info(f"Closed {self.port}")
            self.ser = None

    @property
    def is_connected(self) -> bool:
        return self.ser is not None and self.ser.is_open

    # -------------------------------------------------------------------------
    # Low-Level I/O
    # -------------------------------------------------------------------------

    def detect_silence(self, silence_ms: int = SILENCE_WAIT_MS,
                       timeout_ms: int = 500) -> bool:
        """
        Wait for bus silence before transmitting.
        From OSE ALDLFunctions.cs DetectSilence():
            Waits until no bytes received for silence_ms period.
        """
        if not self.ser:
            return False

        start = time.monotonic()
        last_byte = time.monotonic()

        while (time.monotonic() - start) * 1000 < timeout_ms:
            if self.ser.in_waiting > 0:
                self.ser.read(self.ser.in_waiting)
                last_byte = time.monotonic()
            elif (time.monotonic() - last_byte) * 1000 >= silence_ms:
                return True
            time.sleep(0.001)

        log.warning("Bus congestion — could not get silence window")
        return False

    def tx_frame(self, frame: bytearray) -> bool:
        """
        Transmit ALDL frame with echo handling.
        From OSE ALDLFunctions.cs ALDLTxFrame().
        """
        if not self.ser:
            return False

        if not self.detect_silence():
            return False

        # OSE calculates TX byte count as frame[1] - 82
        tx_count = frame[1] - 82 if len(frame) > 1 else len(frame)
        tx_count = min(tx_count, len(frame))

        self.ser.reset_input_buffer()
        self.ser.write(bytes(frame[:tx_count]))
        self.ser.flush()
        log.debug(f"TX: {hexdump(bytes(frame[:tx_count]))}")

        # Skip echo bytes (most ALDL cables echo)
        if self.echo_enabled:
            deadline = time.monotonic() + 0.5
            echo = bytearray()
            while len(echo) < tx_count and time.monotonic() < deadline:
                chunk = self.ser.read(tx_count - len(echo))
                if chunk:
                    echo.extend(chunk)
                time.sleep(0.001)
            log.debug(f"Echo: {hexdump(bytes(echo))}")

        return True

    def rx_frame(self, timeout_ms: int = COMM_TIMEOUT_MS) -> Optional[bytearray]:
        """
        Receive ALDL response frame.
        Collects bytes until bus goes quiet (frame boundary).
        """
        if not self.ser:
            return None

        buf = bytearray()
        start = time.monotonic()
        last_rx = time.monotonic()
        quiet_threshold = 0.05  # 50ms quiet = frame complete

        while (time.monotonic() - start) * 1000 < timeout_ms:
            avail = self.ser.in_waiting
            if avail > 0:
                buf.extend(self.ser.read(avail))
                last_rx = time.monotonic()
            elif len(buf) > 0 and (time.monotonic() - last_rx) > quiet_threshold:
                break
            time.sleep(0.002)

        if buf:
            log.debug(f"RX: {hexdump(bytes(buf))}")
        return buf if buf else None

    def send_and_receive(self, frame: bytearray,
                         timeout_ms: int = COMM_TIMEOUT_MS) -> Optional[bytearray]:
        """Send frame and wait for response."""
        if not self.tx_frame(frame):
            return None
        return self.rx_frame(timeout_ms)

    def find_response(self, buf: bytearray, device_id: int,
                      length_byte: int, mode: int) -> Optional[bytearray]:
        """
        Find a valid response frame in buffer.
        Scans for [DeviceID, LengthByte, Mode] pattern.
        From OSE response parsing logic.
        """
        if not buf or len(buf) < 3:
            return None
        for i in range(len(buf) - 2):
            if (buf[i] == device_id and
                buf[i + 1] == length_byte and
                buf[i + 2] == mode):
                return buf[i:]
        return None

    # -------------------------------------------------------------------------
    # High-Level Protocol Commands
    # -------------------------------------------------------------------------

    def send_command(self, device_id: int, mode: int,
                     retries: int = MAX_RETRIES) -> Optional[bytearray]:
        """
        Send a simple mode command and return the response.
        Handles retries automatically.
        """
        for attempt in range(retries):
            frame = build_simple_frame(device_id, mode)
            response = self.send_and_receive(frame)
            if response:
                return response
            log.warning(f"No response, attempt {attempt + 1}/{retries}")
        return None

    def disable_chatter(self, device_id: int) -> bool:
        """
        Disable normal communication for a module (Mode 8).
        From OSE ALDLChatterHandler.
        """
        for attempt in range(MAX_RETRIES):
            frame = build_simple_frame(device_id, MODE_8)
            log.info(f"Disabling chatter for 0x{device_id:02X} "
                     f"(attempt {attempt + 1})")
            response = self.send_and_receive(frame)
            if response:
                found = self.find_response(response, device_id, SIMPLE_LENGTH, MODE_8)
                if found:
                    log.info(f"Chatter disabled for 0x{device_id:02X}")
                    return True
        log.error(f"Failed to disable chatter for 0x{device_id:02X}")
        return False

    def enable_chatter(self, device_id: int) -> bool:
        """Re-enable normal communication (Mode 9)."""
        for attempt in range(MAX_RETRIES):
            frame = build_simple_frame(device_id, MODE_9)
            response = self.send_and_receive(frame)
            if response:
                found = self.find_response(response, device_id, SIMPLE_LENGTH, MODE_9)
                if found:
                    log.info(f"Chatter enabled for 0x{device_id:02X}")
                    return True
        return False

    def request_mode5(self) -> bool:
        """
        Request Mode 5/6 access (flash programming entry).
        Vehicle MUST be stationary.
        From OSE Mode5Request().
        """
        for attempt in range(MAX_RETRIES):
            frame = build_simple_frame(DEVICE_PCM, MODE_5)
            log.info(f"Requesting Mode 5 access (attempt {attempt + 1})")
            response = self.send_and_receive(frame)
            if response:
                found = self.find_response(response, DEVICE_PCM, 0x57, MODE_5)
                if found and len(found) > 3:
                    if found[3] == RESP_OK:
                        log.info("Mode 5 access ALLOWED")
                        return True
                    else:
                        log.error(f"Mode 5 DENIED (status=0x{found[3]:02X}) "
                                  f"— vehicle may be moving")
                        return False
        log.error("Failed to get Mode 5 access")
        return False

    def unlock_security(self) -> bool:
        """
        Perform seed-key security unlock for flash operations.
        From OSE UnlockFlashPCM():
            1. Request seed
            2. Calculate key using magic 37709
            3. Send key
            4. Verify unlock
        """
        # Step 1: Request seed
        seed_frame = build_security_seed_request(DEVICE_PCM)
        response = self.send_and_receive(seed_frame)
        if not response:
            log.error("No response to seed request")
            return False

        found = self.find_response(response, DEVICE_PCM, 0x59, MODE_13)
        if not found or len(found) < 6:
            log.error(f"Invalid seed response: {hexdump(bytes(response))}")
            return False

        seed_hi = found[4]
        seed_lo = found[5]
        log.info(f"Seed received: hi=0x{seed_hi:02X} lo=0x{seed_lo:02X}")

        # Already unlocked?
        if seed_hi == 0x00 and seed_lo == 0x00:
            log.info("PCM already unlocked (seed=0x0000)")
            return True

        # Step 2: Calculate key
        key = calculate_security_key(seed_hi, seed_lo)
        log.info(f"Calculated key: 0x{key:04X} ({key})")

        # Step 3: Send key
        key_frame = build_security_key_send(DEVICE_PCM, key)
        response = self.send_and_receive(key_frame)
        if not response:
            log.error("No response to key send")
            return False

        # Step 4: Verify
        found = self.find_response(response, DEVICE_PCM, 0x59, MODE_13)
        if found and len(found) > 3 and found[3] == 0x02:
            log.info("Security UNLOCKED")
            return True

        log.error("Security unlock FAILED")
        return False

    def upload_kernel(self, kernel_data: bytes,
                      load_addr: int = 0x0300,
                      chunk_size: int = 128) -> bool:
        """
        Upload kernel code to PCM RAM via Mode 6.
        From OSE Mode6VXYUploadExec() — splits into chunks.
        """
        total = len(kernel_data)
        offset = 0
        chunk_num = 0

        log.info(f"Uploading {total} bytes to 0x{load_addr:04X}")

        while offset < total:
            remaining = total - offset
            size = min(chunk_size, remaining)
            chunk = kernel_data[offset:offset + size]
            addr = load_addr + offset

            frame = build_mode6_upload_chunk(
                DEVICE_PCM, chunk, addr, BANK_1_ID
            )

            for attempt in range(MAX_RETRIES):
                response = self.send_and_receive(frame, timeout_ms=3000)
                if response:
                    found = self.find_response(
                        response, DEVICE_PCM, 0x57, MODE_6
                    )
                    if found:
                        chunk_num += 1
                        log.info(f"Chunk {chunk_num}: {size} bytes @ "
                                 f"0x{addr:04X} OK")
                        break
                log.warning(f"Chunk retry {attempt + 1}")
            else:
                log.error(f"Failed to upload chunk at 0x{addr:04X}")
                return False

            offset += size

        log.info(f"Upload complete: {total} bytes in {chunk_num} chunks")
        return True

    def read_mode1_stream(self) -> Optional[Dict[str, int]]:
        """
        Request Mode 1 data stream and parse basic parameters.
        Returns dict of engine parameters or None.
        """
        frame = build_mode1_request(DEVICE_PCM)
        response = self.send_and_receive(frame, timeout_ms=3000)
        if not response:
            return None

        # Mode 1 responses are variable-length
        # Basic parsing — offsets are approximate, need XDF cross-ref
        if len(response) < 10:
            return None

        return {
            'raw_bytes': bytes(response),
            'length': len(response),
        }

    def send_mode4_override(self, control_bytes: bytes) -> bool:
        """
        Send Mode 4 actuator override.
        control_bytes: raw control bits for actuator testing
        (bit 0 = fan relay, etc — see mode4_responder.c)
        """
        frame = build_mode4_frame(DEVICE_PCM, control_bytes)
        response = self.send_and_receive(frame)
        if response:
            found = self.find_response(response, DEVICE_PCM, 0x56, MODE_4)
            return found is not None
        return False


# =============================================================================
# Convenience: CLI entry point for quick testing
# =============================================================================

def main():
    """Quick test: scan ports, connect, read Mode 1 data."""
    import argparse

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%H:%M:%S'
    )

    parser = argparse.ArgumentParser(description='ALDL Interface Test')
    parser.add_argument('--port', '-p', help='Serial port (auto-detect if omitted)')
    parser.add_argument('--baud', '-b', type=int, default=BAUD_FAST,
                        help=f'Baud rate (default: {BAUD_FAST})')
    parser.add_argument('--scan', action='store_true',
                        help='Just scan for serial ports')
    parser.add_argument('--mode1', action='store_true',
                        help='Request Mode 1 data stream')
    parser.add_argument('--disable-chatter', action='store_true',
                        help='Disable BCM + PCM chatter')
    args = parser.parse_args()

    if args.scan:
        ports = ALDLConnection.scan_ports()
        print(f"Available ports: {ports}")
        return

    conn = ALDLConnection(args.port, args.baud)
    if not conn.open():
        return

    try:
        if args.disable_chatter:
            conn.disable_chatter(DEVICE_BCM)
            conn.disable_chatter(DEVICE_PCM)

        if args.mode1:
            result = conn.read_mode1_stream()
            if result:
                print(f"Mode 1 response ({result['length']} bytes):")
                print(hexdump(result['raw_bytes']))
            else:
                print("No Mode 1 response")
        else:
            # Default: just try to get any response
            print("Sending Mode 1 request...")
            result = conn.read_mode1_stream()
            if result:
                print(f"ECU responded! ({result['length']} bytes)")
                print(hexdump(result['raw_bytes']))
            else:
                print("No response from ECU "
                      "(check wiring, ignition, baud rate)")
    finally:
        conn.close()


if __name__ == '__main__':
    main()
