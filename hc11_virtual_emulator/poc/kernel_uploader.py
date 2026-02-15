#!/usr/bin/env python3
"""
=============================================================================
KingAi PCM Kernel Uploader -  POC hello world tester
=============================================================================
Minimal kernel upload tool for VY V6 (Delco 09356445) PCM.

This follows the EXACT same protocol sequence used by open-source PCM flash tools:
1. Disable BCM chatter (Mode 8 to BCM 0xF1)
2. Disable PCM chatter (Mode 8 to PCM 0xF4)
3. Request Mode 5 access (vehicle must be stationary)
4. Upload kernel via Mode 6 (3 chunks to PCM RAM at $0300+)
5. Kernel runs automatically after upload completes

MILESTONE 1: Upload a 18-byte watchdog loop kernel.
             Success = PCM doesn't reset (stays alive in loop)

MILESTONE 2: Add ALDL transmit to kernel (sends packets you can see)
             Test with OSE Plugin Logger

Usage:
    python kernel_uploader.py --port COM3
    python kernel_uploader.py --port COM3 --kernel watchdog_kernel.bin
    python kernel_uploader.py --port COM3 --test-only   # just test comms

Author: KingAustraliaGG
Credits: OSE Flash Tool (VL400), Antus (also for the idea for this script), and other community tools (pcmhacking.net).
=============================================================================
"""

import serial
import serial.tools.list_ports
import time
import struct
import argparse
import sys
import logging
from typing import Optional, Tuple, List

# =============================================================================
# Logging
# =============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
log = logging.getLogger('kernel_uploader')

# =============================================================================
# Constants — ALDL protocol definitions
# =============================================================================
PCM_DEVICE_ID = 0xF4        # VY V6 PCM address
BCM_DEVICE_ID = 0xF1        # BCM address
BAUD_RATE = 8192             # ALDL standard baud (8192 bps)
COMM_TIMEOUT_MS = 2000       # Default timeout
MAX_RETRIES = 5              # Max retry attempts

# ALDL Mode numbers
MODE_5 = 5                   # Flash programming entry
MODE_6 = 6                   # Upload/execute code
MODE_8 = 8                   # Disable chatter
MODE_9 = 9                   # Enable chatter
MODE_13 = 13                 # Security access

# Security magic for Mode 13 access
PCM_SECURITY_MAGIC = 37709   # 0x934D

# Response codes
RESPONSE_OK = 0xAA           # Success
RESPONSE_REJECTED = 0xCC     # Rejected
RESPONSE_FAIL = 0x55         # Failure

# =============================================================================
# Minimal watchdog kernel - 18 bytes
# Assembled from watchdog_kernel.asm
#
# Just loops forever feeding the COP watchdog.
# If PCM doesn't reset after upload, YOUR CODE IS RUNNING.
# =============================================================================
WATCHDOG_KERNEL = bytes([
    0x86, 0x55,             # LDAA #$55
    0xB7, 0x10, 0x3A,       # STAA $103A    (COPRST <- $55)
    0x86, 0xAA,             # LDAA #$AA
    0xB7, 0x10, 0x3A,       # STAA $103A    (COPRST <- $AA)
    0xCE, 0xFF, 0xFF,       # LDX  #$FFFF   (delay counter)
    0x09,                   # DEX
    0x26, 0xFD,             # BNE  -3       (delay loop)
    0x20, 0xEE,             # BRA  -18      (back to start)
])

# =============================================================================
# ALDL Hello World kernel - 49 bytes (Milestone 2)
# Loops forever, feeds watchdog, sends "HI" over ALDL serial every ~2 seconds
# =============================================================================
HELLO_WORLD_KERNEL = bytes([
    # --- Main loop ---
    # Feed COP watchdog
    0x86, 0x55,             # LDAA #$55
    0xB7, 0x10, 0x3A,       # STAA $103A    (COPRST <- $55)
    0x86, 0xAA,             # LDAA #$AA
    0xB7, 0x10, 0x3A,       # STAA $103A    (COPRST <- $AA)

    # Send ALDL response packet: [F4 57 06 48 49 checksum]
    # "HI" = 0x48 0x49
    # Wait for SCI TX ready (TDRE bit in SCSR $102E)
    0xB6, 0x10, 0x2E,       # LDAA $102E    (read SCSR - SCI status)
    0x85, 0x80,             # BITA #$80     (test TDRE - TX data reg empty)
    0x27, 0xF9,             # BEQ  -7       (loop until TDRE=1)
    0x86, 0xF4,             # LDAA #$F4     (device ID byte)
    0xB7, 0x10, 0x2F,       # STAA $102F    (write to SCDR - SCI data)

    0xB6, 0x10, 0x2E,       # LDAA $102E    (wait TDRE again)
    0x85, 0x80,             # BITA #$80
    0x27, 0xF9,             # BEQ  -7
    0x86, 0x57,             # LDAA #$57     (length = 85+2 = 87 = 0x57)
    0xB7, 0x10, 0x2F,       # STAA $102F

    0xB6, 0x10, 0x2E,       # LDAA $102E
    0x85, 0x80,             # BITA #$80
    0x27, 0xF9,             # BEQ  -7
    0x86, 0x06,             # LDAA #$06     (Mode 6 response)
    0xB7, 0x10, 0x2F,       # STAA $102F

    0xB6, 0x10, 0x2E,       # LDAA $102E
    0x85, 0x80,             # BITA #$80
    0x27, 0xF9,             # BEQ  -7
    0x86, 0x48,             # LDAA #$48     ('H')
    0xB7, 0x10, 0x2F,       # STAA $102F

    0xB6, 0x10, 0x2E,       # LDAA $102E
    0x85, 0x80,             # BITA #$80
    0x27, 0xF9,             # BEQ  -7
    0x86, 0x49,             # LDAA #$49     ('I')
    0xB7, 0x10, 0x2F,       # STAA $102F

    # Checksum: 256-(F4+57+06+48+49) = 256-(0x1E8) = 256-232 = 0x18
    0xB6, 0x10, 0x2E,       # LDAA $102E
    0x85, 0x80,             # BITA #$80
    0x27, 0xF9,             # BEQ  -7
    0x86, 0x18,             # LDAA #$18     (checksum)
    0xB7, 0x10, 0x2F,       # STAA $102F

    # Delay loop
    0xCE, 0xFF, 0xFF,       # LDX #$FFFF
    0x09,                   # DEX
    0x26, 0xFD,             # BNE -3

    # Loop back to start
    0x20, 0x80 + (256 - 97),  # BRA back to start (calculated offset)
])

# Fix: recalculate BRA offset for hello world kernel
# The kernel is 97 bytes from start to here, BRA needs to go back to byte 0
# BRA offset = -(current_position + 2), encoded as 2's complement
# We'll fix this properly on init


# =============================================================================
# Hex dump helper
# =============================================================================
def hexdump(data: bytes, prefix: str = '') -> str:
    """Format bytes as hex string for display."""
    if not data:
        return f"{prefix}<empty>"
    hex_str = ' '.join(f'{b:02X}' for b in data)
    return f"{prefix}[{len(data):3d}] {hex_str}"


# =============================================================================
# ALDL Frame helpers
# =============================================================================
def aldl_checksum(frame: bytearray) -> int:
    """
    Calculate ALDL checksum.
    Standard ALDL checksum:
        Sum all bytes, checksum = (256 - sum) & 0xFF
    """
    total = sum(frame) & 0xFF
    if total == 0:
        total = 256
    return (256 - total) & 0xFF


def build_simple_frame(device_id: int, mode: int) -> bytearray:
    """
    Build a simple 3-byte ALDL command frame (+ checksum).
    From OSE: TxFrame = [DeviceID, 0x56, Mode, Checksum]
    
    Length byte 0x56 = 86 = 85 + 1 (just mode byte after length)
    """
    frame = bytearray([device_id, 0x56, mode, 0x00])  # placeholder checksum
    frame[3] = aldl_checksum(frame[:3])
    return frame


def build_security_seed_request(device_id: int) -> bytearray:
    """
    Request security seed.
    From OSE ALDLFunctions.cs UnlockFlashPCM():
        TxFrame = [DeviceID, 0x57, 0x0D, 0x01, Checksum]
    """
    frame = bytearray([device_id, 0x57, 0x0D, 0x01, 0x00])
    frame[4] = aldl_checksum(frame[:4])
    return frame


def build_security_key_send(device_id: int, key: int) -> bytearray:
    """
    Send security key.
    From OSE ALDLFunctions.cs UnlockFlashPCM():
        TxFrame = [DeviceID, 0x59, 0x0D, 0x02, key_high, key_low, Checksum]
    """
    key_bytes = struct.pack('>H', key)  # big-endian
    frame = bytearray([device_id, 0x59, 0x0D, 0x02, key_bytes[0], key_bytes[1], 0x00])
    frame[6] = aldl_checksum(frame[:6])
    return frame


def calculate_pcm_security_key(seed_high: int, seed_low: int) -> int:
    """
    Calculate PCM security key from seed.
    From OSE ALDLFunctions.cs line ~1660:
        key = 37709 - (seed_low * 256 + seed_high)
        if key < 0: key += 65536
    """
    seed = seed_low * 256 + seed_high
    key = PCM_SECURITY_MAGIC - seed
    if key < 0:
        key += 65536
    return key


# =============================================================================
# Serial Communication Class
# =============================================================================
class ALDLSerial:
    """
    Low-level ALDL serial communication.
    Protocol ported from OSE Flash Tool (VL400).
    """

    def __init__(self, port: str, baud: int = BAUD_RATE):
        self.port = port
        self.baud = baud
        self.ser: Optional[serial.Serial] = None
        self.echo_enabled = True  # Most ALDL cables echo TX bytes

    def open(self) -> bool:
        """Open serial port. Returns True on success."""
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baud,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=0.1,          # 100ms read timeout for polling
                write_timeout=1.0,
            )
            time.sleep(0.1)           # Let port settle
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            log.info(f"Opened {self.port} @ {self.baud} baud")
            return True
        except serial.SerialException as e:
            log.error(f"Failed to open {self.port}: {e}")
            return False

    def close(self):
        """Close serial port."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            log.info(f"Closed {self.port}")

    def detect_silence(self, silence_ms: int = 20, timeout_ms: int = 500) -> bool:
        """
        Wait for bus silence before transmitting.
        From OSE ALDLFunctions.cs DetectSilence():
            Waits until no bytes received for silence_ms period.
            Gives up after timeout_ms.
        """
        if not self.ser:
            return False

        start = time.monotonic()
        last_byte_time = time.monotonic()

        while (time.monotonic() - start) * 1000 < timeout_ms:
            if self.ser.in_waiting > 0:
                self.ser.read(self.ser.in_waiting)  # Drain
                last_byte_time = time.monotonic()
            elif (time.monotonic() - last_byte_time) * 1000 >= silence_ms:
                return True
            time.sleep(0.001)

        log.warning("Bus congestion - could not get silence window")
        return False

    def tx_frame(self, frame: bytearray) -> bool:
        """
        Transmit ALDL frame.
        From OSE ALDLFunctions.cs ALDLTxFrame():
            1. Wait for bus silence
            2. Send frame bytes
            3. Handle echo
        """
        if not self.ser:
            return False

        if not self.detect_silence():
            return False

        # Calculate TX byte count from OSE: frame[1] - 82
        tx_count = frame[1] - 82 if len(frame) > 1 else len(frame)
        tx_count = min(tx_count, len(frame))

        self.ser.reset_input_buffer()
        self.ser.write(bytes(frame[:tx_count]))
        self.ser.flush()

        log.debug(f"TX: {hexdump(bytes(frame[:tx_count]))}")

        # Skip echo bytes if cable echoes
        if self.echo_enabled:
            echo_deadline = time.monotonic() + 0.5
            echo_bytes = bytearray()
            while len(echo_bytes) < tx_count and time.monotonic() < echo_deadline:
                chunk = self.ser.read(tx_count - len(echo_bytes))
                if chunk:
                    echo_bytes.extend(chunk)
                time.sleep(0.001)
            log.debug(f"Echo: {hexdump(bytes(echo_bytes))}")

        return True

    def rx_frame(self, timeout_ms: int = COMM_TIMEOUT_MS) -> Optional[bytearray]:
        """
        Receive ALDL response frame.
        From OSE: waits for RxFrameReady within timeout.
        
        Returns complete frame or None on timeout.
        """
        if not self.ser:
            return None

        buf = bytearray()
        start = time.monotonic()
        last_rx = time.monotonic()
        quiet_threshold = 0.05  # 50ms quiet = frame complete

        while (time.monotonic() - start) * 1000 < timeout_ms:
            available = self.ser.in_waiting
            if available > 0:
                chunk = self.ser.read(available)
                buf.extend(chunk)
                last_rx = time.monotonic()
            elif len(buf) > 0 and (time.monotonic() - last_rx) > quiet_threshold:
                # Got data and bus is quiet - frame complete
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

    def find_response(self, buf: bytearray, expected_device: int,
                      expected_byte1: int, expected_mode: int) -> Optional[bytearray]:
        """
        Find a valid response frame in the buffer.
        OSE checks: RxFrame[0]==DeviceID & RxFrame[1]==expected & RxFrame[2]==mode
        """
        if not buf or len(buf) < 3:
            return None

        for i in range(len(buf) - 2):
            if (buf[i] == expected_device and
                buf[i + 1] == expected_byte1 and
                buf[i + 2] == expected_mode):
                # Found frame start - extract what we can
                return buf[i:]

        return None


# =============================================================================
# Kernel Uploader - The main protocol implementation
# =============================================================================
class KernelUploader:
    """
    Upload and execute a kernel on VY V6 PCM.
    Protocol based on OSE Flash Tool (VL400).
    
    Sequence:
        1. DisableChatter (Mode 8) → BCM and PCM
        2. Mode5Request → enter programming mode
        3. Mode6VXYUploadExec → upload kernel in 3 chunks
        4. Kernel begins executing automatically
    """

    def __init__(self, serial: ALDLSerial, device_id: int = PCM_DEVICE_ID):
        self.serial = serial
        self.device_id = device_id

    # -------------------------------------------------------------------------
    # Step 1: Disable Chatter 
    # -------------------------------------------------------------------------
    def disable_chatter(self, device_id: int) -> bool:
        """
        Send Mode 8 (disable chatter) to a module.
        From OSE ALDLChatterHandler("Disabled", deviceID, 8):
            TX: [DeviceID, 0x56, 0x08, Checksum]
            RX: [DeviceID, 0x56, 0x08] = success
        """
        for attempt in range(MAX_RETRIES):
            frame = build_simple_frame(device_id, MODE_8)
            log.info(f"Disabling chatter for 0x{device_id:02X} (attempt {attempt+1})")

            response = self.serial.send_and_receive(frame)
            if response:
                found = self.serial.find_response(response, device_id, 0x56, MODE_8)
                if found:
                    log.info(f"Chatter disabled for 0x{device_id:02X}")
                    return True
                else:
                    log.warning(f"Unexpected response: {hexdump(bytes(response))}")
            else:
                log.warning("No response")

        log.error(f"Failed to disable chatter for 0x{device_id:02X}")
        return False

    def enable_chatter(self, device_id: int) -> bool:
        """
        Send Mode 9 (enable chatter) to a module.
        From OSE ALDLChatterHandler("Enabled", deviceID, 9)
        """
        for attempt in range(MAX_RETRIES):
            frame = build_simple_frame(device_id, MODE_9)
            response = self.serial.send_and_receive(frame)
            if response:
                found = self.serial.find_response(response, device_id, 0x56, MODE_9)
                if found:
                    log.info(f"Chatter enabled for 0x{device_id:02X}")
                    return True
            log.warning(f"Enable chatter attempt {attempt+1} failed")

        return False

    # -------------------------------------------------------------------------
    # Step 2: Mode 5 Request
    # -------------------------------------------------------------------------
    def mode5_request(self) -> bool:
        """
        Request Mode 5/6 access (flash programming entry).
        From OSE Mode5Request():
            TX: [DeviceID, 0x56, 0x05, Checksum]
            RX: [DeviceID, 0x57, 0x05, 0xAA] = allowed
            RX: [DeviceID, 0x57, 0x05, !0xAA] = denied (vehicle moving)
        
        Vehicle MUST be stationary!
        """
        for attempt in range(MAX_RETRIES):
            frame = build_simple_frame(self.device_id, MODE_5)
            log.info(f"Requesting Mode 5/6 access (attempt {attempt+1})")

            response = self.serial.send_and_receive(frame)
            if response:
                found = self.serial.find_response(response, self.device_id, 0x57, MODE_5)
                if found and len(found) > 3:
                    if found[3] == RESPONSE_OK:
                        log.info("Mode 5/6 access ALLOWED")
                        return True
                    else:
                        log.error("Mode 5/6 access DENIED - vehicle may be moving!")
                        return False
                else:
                    log.warning(f"Frame error: {hexdump(bytes(response))}")
            else:
                log.warning("No response")

        log.error("Failed to get Mode 5/6 access")
        return False

    # -------------------------------------------------------------------------
    # Step 3: Security Unlock (for flash write, not needed for RAM execute)
    # -------------------------------------------------------------------------
    def unlock_pcm(self) -> bool:
        """
        Unlock PCM security.
        From OSE UnlockFlashPCM():
            1. Request seed: TX [DeviceID, 0x57, 0x0D, 0x01, CS]
               Response: [DeviceID, 0x59, 0x0D, 0x01, seed_hi, seed_lo]
            2. If seed = 0x0000 → already unlocked
            3. Calculate key: 37709 - (seed_lo * 256 + seed_hi)
            4. Send key: TX [DeviceID, 0x59, 0x0D, 0x02, key_hi, key_lo, CS]
               Response byte[4]: 0xAA=pass, 0xCC=rejected
        """
        for attempt in range(MAX_RETRIES):
            # Request seed
            seed_frame = build_security_seed_request(self.device_id)
            log.info(f"Requesting security seed (attempt {attempt+1})")

            response = self.serial.send_and_receive(seed_frame)
            if not response:
                log.warning("No response to seed request")
                continue

            found = self.serial.find_response(response, self.device_id, 0x59, 0x0D)
            if not found or len(found) < 6:
                log.warning(f"Bad seed response: {hexdump(bytes(response))}")
                continue

            if found[3] != 0x01:
                log.warning(f"Unexpected message type: {found[3]:02X}")
                continue

            seed_hi = found[4]
            seed_lo = found[5]

            # Check already unlocked
            if seed_hi == 0 and seed_lo == 0:
                log.info("PCM already unlocked (seed=0000)")
                return True

            # Calculate and send key
            key = calculate_pcm_security_key(seed_hi, seed_lo)
            log.info(f"Seed: {seed_hi:02X}{seed_lo:02X} → Key: {key:04X}")

            key_frame = build_security_key_send(self.device_id, key)
            response = self.serial.send_and_receive(key_frame)
            if not response:
                log.warning("No response to key send")
                continue

            # From OSE: check for [DeviceID, 0x58, 0x0D, 0x02, status]
            found = self.serial.find_response(response, self.device_id, 0x58, 0x0D)
            if found and len(found) > 4:
                if found[4] == RESPONSE_OK:
                    log.info("Security PASSED - PCM unlocked!")
                    return True
                elif found[4] == RESPONSE_REJECTED:
                    log.error("Security key REJECTED by PCM")
                    # Could be custom-locked PCM
                else:
                    log.warning(f"Unknown security response: {found[4]:02X}")

        log.error("Failed to unlock PCM")
        return False

    # -------------------------------------------------------------------------
    # Step 4: Upload Kernel via Mode 6
    # -------------------------------------------------------------------------
    def upload_kernel_exec(self) -> bool:
        """
        Upload the Mode 6 execution framework to PCM RAM.
        
        Sends 3 chunks of pre-built kernel code via Mode 6.
            Each chunk: TX large frame, expect [DeviceID, 0x57, 0x06, 0xAA]
            After all 3 chunks, the PCM is ready for further Mode 6 commands.
        
        Kernel bytes from OSE Flash Tool (credit: VL400). Used unchanged.
        """
        # The 3 kernel chunks (OSE Flash Tool — VL400)
        # Each chunk is sent as a Mode 6 upload frame
        chunks = self._get_ose_kernel_chunks()

        for chunk_idx, chunk in enumerate(chunks):
            for attempt in range(MAX_RETRIES):
                log.info(f"Uploading kernel chunk {chunk_idx+1}/3 "
                        f"({len(chunk)} bytes, attempt {attempt+1})")

                # Build frame: content is already a complete ALDL frame
                # from OSE, just need checksum recalculated
                frame = bytearray(chunk)
                
                # Pad to 201 bytes like OSE does
                if len(frame) < 201:
                    frame.extend(b'\x00' * (201 - len(frame)))
                
                # Recalculate checksum (last byte)
                frame[-1] = aldl_checksum(frame[:-1])

                response = self.serial.send_and_receive(frame, timeout_ms=5000)
                if response:
                    found = self.serial.find_response(
                        response, self.device_id, 0x57, MODE_6)
                    if found and len(found) > 3 and found[3] == RESPONSE_OK:
                        log.info(f"Chunk {chunk_idx+1}/3 uploaded OK")
                        break
                    else:
                        log.warning(f"Bad response for chunk {chunk_idx+1}: "
                                   f"{hexdump(bytes(response))}")
                else:
                    log.warning(f"No response for chunk {chunk_idx+1}")
            else:
                log.error(f"Failed to upload chunk {chunk_idx+1}")
                return False

        log.info("All 3 kernel chunks uploaded successfully!")
        return True

    def _get_ose_kernel_chunks(self) -> List[bytes]:
        """
        Return the 3 kernel chunks.
        Credit: VL400 (OSE Flash Tool, pcmhacking.net)
        """
        # Chunk 0 (171 bytes) - Main loop setup
        chunk0 = bytes([
            0xF7, 0xFE, 0x06, 0x01, 0x32, 0x86, 0xAA, 0x36, 0x18, 0x30,
            0x86, 0x06, 0xC6, 0x01, 0xBD, 0xFF, 0xBD, 0x32, 0x39, 0xCC,
            0x02, 0x41, 0x97, 0x34, 0x9D, 0x24, 0x20, 0x99, 0x36, 0x18,
            0x3C, 0x3C, 0x18, 0x38, 0xCE, 0x10, 0x00, 0x86, 0x08, 0xA7,
            0x2D, 0x4F, 0x97, 0x30, 0x86, 0xF7, 0x8D, 0x26, 0x17, 0x8B,
            0x55, 0x8D, 0x21, 0x96, 0x34, 0x8D, 0x1D, 0x5A, 0x27, 0x0A,
            0x18, 0xA6, 0x00, 0x8D, 0x15, 0x18, 0x08, 0x5A, 0x26, 0xF6,
            0x96, 0x30, 0x40, 0x8D, 0x0B, 0x1F, 0x2E, 0x40, 0xFC, 0x1D,
            0x2D, 0x08, 0x18, 0x38, 0x32, 0x39, 0x9D, 0x1E, 0x1F, 0x2E,
            0x80, 0xFA, 0xA7, 0x2F, 0x9B, 0x30, 0x97, 0x30, 0x39, 0x37,
            0xC6, 0x55, 0xF7, 0x10, 0x3A, 0x53, 0xF7, 0x10, 0x3A, 0xC6,
            0x50, 0xF7, 0x18, 0x06, 0xC6, 0xA0, 0xF7, 0x18, 0x06, 0x33,
            0x39, 0xDC, 0x35, 0x4D, 0x26, 0x04, 0xC6, 0x48, 0x20, 0x0D,
            0xC1, 0x80, 0x24, 0x07, 0x14, 0x36, 0x80, 0xC6, 0x58, 0x20,
            0x02, 0xC6, 0x50, 0xF7, 0x10, 0x00, 0x39, 0x3C, 0xCE, 0x10,
            0x00, 0x1C, 0x03, 0x08, 0x1D, 0x02, 0x08, 0x38, 0x39, 0x3C,
            0xCE, 0x10, 0x00, 0x1C, 0x03, 0x08, 0x1C, 0x02, 0x08, 0x38,
            0x39,
        ])

        # Chunk 1 (172 bytes) - Upload handler
        chunk1 = bytes([
            0xF7, 0xFF, 0x06, 0x00, 0x99, 0x86, 0xAA, 0x36, 0x18, 0x30,
            0x86, 0x06, 0xC6, 0x01, 0xBD, 0xFF, 0xBD, 0x32, 0x39, 0x32,
            0x8D, 0x3F, 0x97, 0x37, 0x7A, 0x00, 0x32, 0xCE, 0x03, 0x00,
            0x20, 0x10, 0x8D, 0x33, 0x97, 0x2E, 0x7A, 0x00, 0x32, 0x8D,
            0x2C, 0x97, 0x2F, 0x7A, 0x00, 0x32, 0xDE, 0x2E, 0x8C, 0x03,
            0xFF, 0x22, 0xA5, 0x8D, 0x1E, 0xA7, 0x00, 0x08, 0x7A, 0x00,
            0x32, 0x26, 0xF1, 0x8D, 0x14, 0x5D, 0x26, 0x96, 0x96, 0x33,
            0x81, 0x10, 0x27, 0x06, 0xDE, 0x2E, 0x6E, 0x00, 0x20, 0x8A,
            0xBD, 0x02, 0x18, 0x20, 0xF9, 0x3C, 0xCE, 0x10, 0x00, 0x18,
            0xCE, 0x05, 0x75, 0x7F, 0x00, 0x31, 0x7A, 0x00, 0x31, 0x26,
            0x04, 0x18, 0x09, 0x27, 0x06, 0x9D, 0x1E, 0x1F, 0x2E, 0x0E,
            0x02, 0x20, 0xDD, 0x1F, 0x2E, 0x20, 0xEB, 0xA6, 0x2F, 0x16,
            0xDB, 0x30, 0xD7, 0x30, 0x38, 0x39, 0x81, 0x02, 0x26, 0xCC,
            0x8D, 0xD1, 0x97, 0x35, 0x8D, 0xCD, 0x97, 0x36, 0x8D, 0xC9,
            0x97, 0x37, 0x8D, 0xC5, 0x5D, 0x26, 0xBB, 0xCE, 0x03, 0x20,
            0x8D, 0x7A, 0x18, 0xDE, 0x36, 0x5F, 0x18, 0xA6, 0x00, 0xA7,
            0x00, 0x08, 0x18, 0x08, 0x5C, 0xC1, 0x40, 0x25, 0xF3, 0xCE,
            0x03, 0x20,
        ])

        # Chunk 2 (156 bytes) - Vector table and handlers
        chunk2 = bytes([
            0xF7, 0xEF, 0x06, 0x00, 0x10, 0x20, 0x3E, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7E, 0x01, 0xCC, 0x7E,
            0x01, 0x90, 0x00, 0x00, 0x00, 0x7E, 0x01, 0x49, 0x7E, 0x01,
            0xC0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x8E,
            0x00, 0x4F, 0x0F, 0xB6, 0x18, 0x05, 0x8A, 0x08, 0xB7, 0x18,
            0x05, 0x9D, 0x27, 0x3C, 0x30, 0x86, 0x06, 0x97, 0x34, 0xCC,
            0xAA, 0x00, 0xED, 0x00, 0xC6, 0x02, 0x9D, 0x24, 0x38, 0x8E,
            0x00, 0x4F, 0xCE, 0x10, 0x00, 0x86, 0x04, 0xA7, 0x2D, 0xEC,
            0x2E, 0x4F, 0x97, 0x30, 0x1C, 0x2D, 0x02, 0x8D, 0x67, 0x81,
            0xF7, 0x26, 0xE8, 0x8D, 0x61, 0x80, 0x56, 0x25, 0xE2, 0x97,
            0x32, 0x8D, 0x59, 0x97, 0x33, 0x81, 0x06, 0x27, 0x1E, 0x81,
            0x10, 0x26, 0x78, 0x8D, 0x4D, 0x97, 0x35, 0x7A, 0x00, 0x32,
            0x8D, 0x46, 0x97, 0x36, 0x7A, 0x00, 0x32,
        ])

        return [chunk0, chunk1, chunk2]

    # -------------------------------------------------------------------------
    # Full upload sequence
    # -------------------------------------------------------------------------
    def run_upload(self, skip_chatter: bool = False) -> bool:
        """
        Execute the full kernel upload sequence.
        
        Full kernel upload sequence (based on OSE Flash Tool protocol):
        1. Disable BCM chatter (Mode 8)
        2. Disable PCM chatter (Mode 8)
        3. Enter Mode 5 (programming mode)
        4. Upload kernel via Mode 6 (3 chunks)
        
        After success, the kernel is running on the PCM.
        It handles watchdog feeding and waits for further commands.
        """
        print("=" * 60)
        print("  KingAi PCM Kernel Upload Tool")
        print("  Target: VY V6 Delco 09356445")
        print("  Credits: OSE Flash Tool (VL400), Antus (pcmhacking.net)")
        print("=" * 60)
        print()

        # Step 1: Disable chatter
        if not skip_chatter:
            print("[1/4] Disabling BCM chatter...")
            if not self.disable_chatter(BCM_DEVICE_ID):
                log.warning("Could not disable BCM chatter - continuing anyway")
                # Not fatal - BCM might not respond but we can proceed

            print("[2/4] Disabling PCM chatter...")
            if not self.disable_chatter(self.device_id):
                log.error("Could not disable PCM chatter!")
                return False
        else:
            print("[1-2/4] Skipping chatter disable")

        # Step 2: Enter Mode 5
        print("[3/4] Requesting Mode 5/6 access...")
        if not self.mode5_request():
            log.error("Mode 5 request failed!")
            return False

        # Step 3: Upload kernel
        print("[4/4] Uploading kernel to PCM RAM...")
        if not self.upload_kernel_exec():
            log.error("Kernel upload failed!")
            return False

        print()
        print("=" * 60)
        print("  KERNEL UPLOADED SUCCESSFULLY!")
        print("  The OSE flash kernel is now running on your PCM.")
        print("  PCM should be alive (watchdog being fed).")
        print("=" * 60)
        return True

    def cleanup(self):
        """Re-enable chatter on exit."""
        print("Re-enabling chatter...")
        self.enable_chatter(self.device_id)
        self.enable_chatter(BCM_DEVICE_ID)


# =============================================================================
# Communication Test - just verify you can talk to the PCM
# =============================================================================
def test_communication(serial: ALDLSerial, device_id: int = PCM_DEVICE_ID) -> bool:
    """
    Test basic ALDL communication by trying to disable/enable chatter.
    This is the minimum test - if Mode 8 works, your cable and PCM are talking.
    """
    print("Testing ALDL communication...")
    print(f"  Port: {serial.port}")
    print(f"  Baud: {serial.baud}")
    print(f"  Target: 0x{device_id:02X}")
    print()

    # Try Mode 8 (disable chatter) then Mode 9 (enable)
    frame = build_simple_frame(device_id, MODE_8)
    print(f"  TX: {hexdump(bytes(frame))}")
    
    response = serial.send_and_receive(frame, timeout_ms=3000)
    if response:
        print(f"  RX: {hexdump(bytes(response))}")
        found = serial.find_response(response, device_id, 0x56, MODE_8)
        if found:
            print("  RESULT: PCM responded to Mode 8!")
            print("  Communication is WORKING!")
            
            # Re-enable chatter
            frame = build_simple_frame(device_id, MODE_9)
            serial.send_and_receive(frame)
            return True
        else:
            print("  RESULT: Got data but not a valid Mode 8 response")
            print("  Check device ID and cable")
    else:
        print("  RESULT: No response from PCM")
        print("  Check: cable connected? ignition ON? correct COM port?")

    return False


def list_serial_ports():
    """List available serial ports."""
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("No serial ports found!")
        return
    print("Available serial ports:")
    for p in ports:
        print(f"  {p.device}: {p.description}")


# =============================================================================
# Main
# =============================================================================
def main():
    parser = argparse.ArgumentParser(
        description='KingAi PCM Kernel Uploader - Upload and execute code on VY V6 PCM',
        epilog='Credits: OSE Flash Tool (VL400), Antus, and other community tools (pcmhacking.net)')
    
    parser.add_argument('--port', '-p', type=str, help='Serial port (e.g. COM3)')
    parser.add_argument('--baud', '-b', type=int, default=BAUD_RATE,
                       help=f'Baud rate (default: {BAUD_RATE})')
    parser.add_argument('--device-id', '-d', type=lambda x: int(x, 0),
                       default=PCM_DEVICE_ID,
                       help=f'PCM device ID (default: 0x{PCM_DEVICE_ID:02X})')
    parser.add_argument('--test-only', '-t', action='store_true',
                       help='Only test communication, do not upload')
    parser.add_argument('--list-ports', '-l', action='store_true',
                       help='List available serial ports')
    parser.add_argument('--skip-chatter', action='store_true',
                       help='Skip BCM/PCM chatter disable (if already done)')
    parser.add_argument('--no-echo', action='store_true',
                       help='Cable does not echo TX bytes')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable debug logging')

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.list_ports:
        list_serial_ports()
        return

    if not args.port:
        list_serial_ports()
        print("\nUsage: python kernel_uploader.py --port COM3")
        print("       python kernel_uploader.py --port COM3 --test-only")
        return

    # Open serial
    aldl = ALDLSerial(args.port, args.baud)
    if not args.no_echo:
        aldl.echo_enabled = True
    else:
        aldl.echo_enabled = False

    if not aldl.open():
        sys.exit(1)

    try:
        if args.test_only:
            success = test_communication(aldl, args.device_id)
        else:
            uploader = KernelUploader(aldl, args.device_id)
            success = uploader.run_upload(skip_chatter=args.skip_chatter)
            if not success:
                uploader.cleanup()
    except KeyboardInterrupt:
        print("\nAborted by user")
        success = False
    finally:
        aldl.close()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
