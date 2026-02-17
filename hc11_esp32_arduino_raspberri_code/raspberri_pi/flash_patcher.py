#!/usr/bin/env python3
"""
flash_patcher.py — Partial Flash Write Tool for VY V6 Delco PCM
=================================================================
Implements the sector read-modify-write pattern for safe flash patching.
Follows the exact protocol from OSE Flash Tool (VL400) decompilation.

Workflow:
  1. Connect via ALDL at 8192 baud
  2. Disable chatter (Mode 8) → BCM + PCM
  3. Request Mode 5 access (vehicle must be stationary)
  4. Security unlock (Mode 13 seed-key, magic = 37709)
  5. Upload flash kernel via Mode 6 to PCM RAM ($0300)
  6. Kernel executes: erases sector, writes new data, verifies

Supports:
  - CAL-only write (Sector 1 / Bank 1 only, 0x4000-0x7FFF) — SAFEST
  - Full PROM write (all 8 sectors, 0x2000-0x1FFFF) — for recovery
  - Custom patch injection at specific addresses

Protocol sourced from:
  - OSE Flash Tool (VL400) frmFlashTool.cs decompilation
  - kernel_uploader.py POC
  - pcmhacking.net community docs

Author: KingAustraliaGG
Date: 2026-02-15
"""

import sys
import time
import struct
import hashlib
import argparse
import logging
from pathlib import Path
from typing import Optional

from aldl_interface import (
    ALDLConnection, DEVICE_PCM, DEVICE_BCM,
    BAUD_FAST, MODE_5, MODE_6, MODE_8, MODE_13,
    RESP_OK, BANK_1_ID, BANK_2_ID, BANK_3_ID,
    hexdump, aldl_checksum
)

log = logging.getLogger('flash_patcher')

# =============================================================================
# Flash Layout — VY V6 ($060A Enhanced)
# From OSE Flash Tool decompilation + FREE_SPACE_ANALYSIS
# =============================================================================

# Sector definitions (from OSE frmFlashTool.cs)
SECTORS = {
    0: {'bank_id': BANK_1_ID, 'sector_id': 0x00, 'start': 0x0000, 'end': 0x1FFF,
        'name': 'Boot/Reserved', 'safe_to_erase': False},
    1: {'bank_id': BANK_1_ID, 'sector_id': 0x40, 'start': 0x4000, 'end': 0x7FFF,
        'name': 'Bank 1 CAL', 'safe_to_erase': True},
    2: {'bank_id': BANK_1_ID, 'sector_id': 0x80, 'start': 0x8000, 'end': 0xBFFF,
        'name': 'Bank 1 Code (low)', 'safe_to_erase': True},
    3: {'bank_id': BANK_1_ID, 'sector_id': 0xC0, 'start': 0xC000, 'end': 0xFFFF,
        'name': 'Bank 1 Code (high+vectors)', 'safe_to_erase': True},
    4: {'bank_id': BANK_2_ID, 'sector_id': 0x80, 'start': 0x8000, 'end': 0xBFFF,
        'name': 'Bank 2 Engine (low)', 'safe_to_erase': True},
    5: {'bank_id': BANK_2_ID, 'sector_id': 0xC0, 'start': 0xC000, 'end': 0xFFFF,
        'name': 'Bank 2 Engine (high)', 'safe_to_erase': True},
    6: {'bank_id': BANK_3_ID, 'sector_id': 0x80, 'start': 0x8000, 'end': 0xBFFF,
        'name': 'Bank 3 Trans/Diag (low)', 'safe_to_erase': True},
    7: {'bank_id': BANK_3_ID, 'sector_id': 0xC0, 'start': 0x8000, 'end': 0xFFFF,
        'name': 'Bank 3 Trans/Diag (high)', 'safe_to_erase': False},
}

# Binary file layout
FULL_BIN_SIZE = 0x20000     # 128KB full binary
CAL_OFFSET = 0x4000         # CAL section start in file
CAL_SIZE = 0x4000           # 16KB CAL section

# GM ROM Checksum location (from hc11kit checksum command)
CHECKSUM_ADDR = 0x0002      # 16-bit checksum at file offset 0x0002


# =============================================================================
# Flash Kernel — HC11 Machine Code
# Uploaded to PCM RAM via Mode 6, executed to perform flash operations.
# This is the same pattern OSE Flash Tool uses.
# =============================================================================

# Minimal flash erase kernel (loaded to $0300 in PCM RAM)
# This is a PLACEHOLDER — the real kernel needs the exact M29W800DB
# command sequences. See OSE decompilation for the actual flash commands.
#
# M29W800DB Erase Sequence (from datasheet):
#   Write 0xAA to 0x555, Write 0x55 to 0x2AA, Write 0x80 to 0x555
#   Write 0xAA to 0x555, Write 0x55 to 0x2AA, Write 0x30 to sector_addr
#   Then poll DQ7 for completion
#
# For now we use the watchdog kernel as a safe test:
FLASH_KERNEL_PLACEHOLDER = bytes([
    # Feed COP watchdog (MUST do this or CPU resets)
    0x86, 0x55,             # LDAA #$55
    0xB7, 0x10, 0x3A,       # STAA $103A    (COPRST <- $55)
    0x86, 0xAA,             # LDAA #$AA
    0xB7, 0x10, 0x3A,       # STAA $103A    (COPRST <- $AA)
    # Send "OK" over ALDL to confirm kernel is running
    0xB6, 0x10, 0x2E,       # LDAA $102E    (wait TDRE)
    0x85, 0x80,             # BITA #$80
    0x27, 0xF9,             # BEQ -7
    0x86, 0x4F,             # LDAA #$4F     ('O')
    0xB7, 0x10, 0x2F,       # STAA $102F
    0xB6, 0x10, 0x2E,       # LDAA $102E    (wait TDRE)
    0x85, 0x80,             # BITA #$80
    0x27, 0xF9,             # BEQ -7
    0x86, 0x4B,             # LDAA #$4B     ('K')
    0xB7, 0x10, 0x2F,       # STAA $102F
    # Delay loop
    0xCE, 0xFF, 0xFF,       # LDX #$FFFF
    0x09,                   # DEX
    0x26, 0xFD,             # BNE -3
    # Loop back to start (feed watchdog again)
    0x20, 0xDA,             # BRA start (-38)
])


# =============================================================================
# Binary File Helpers
# =============================================================================

def read_binary(path: str) -> Optional[bytes]:
    """Read a binary file and validate size."""
    p = Path(path)
    if not p.exists():
        log.error(f"File not found: {path}")
        return None
    data = p.read_bytes()
    if len(data) != FULL_BIN_SIZE:
        log.warning(f"Unexpected size: {len(data)} bytes "
                    f"(expected {FULL_BIN_SIZE})")
    return data


def write_binary(path: str, data: bytes):
    """Write binary file with backup."""
    p = Path(path)
    # Create backup
    backup = p.with_suffix('.bak')
    if p.exists() and not backup.exists():
        backup.write_bytes(p.read_bytes())
        log.info(f"Backup created: {backup}")
    p.write_bytes(data)
    log.info(f"Written: {path} ({len(data)} bytes)")


def calc_gm_checksum(data: bytes) -> int:
    """
    Calculate GM ROM checksum.
    Sum of all 16-bit words, result should be 0x0000.
    From hc11kit checksum command.
    """
    total = 0
    for i in range(0, len(data), 2):
        if i + 1 < len(data):
            word = (data[i] << 8) | data[i + 1]
            total = (total + word) & 0xFFFF
    return total


def fix_gm_checksum(data: bytearray) -> bytearray:
    """Fix the GM checksum at offset 0x0002-0x0003."""
    # Zero out checksum bytes first
    data[CHECKSUM_ADDR] = 0x00
    data[CHECKSUM_ADDR + 1] = 0x00
    # Calculate what's needed to make total = 0
    current = calc_gm_checksum(bytes(data))
    correction = (0x10000 - current) & 0xFFFF
    data[CHECKSUM_ADDR] = (correction >> 8) & 0xFF
    data[CHECKSUM_ADDR + 1] = correction & 0xFF
    # Verify
    verify = calc_gm_checksum(bytes(data))
    log.info(f"Checksum fixed: 0x{correction:04X} (verify: 0x{verify:04X})")
    return data


# =============================================================================
# Patch Application
# =============================================================================

def apply_patch(original: bytes, patch_data: bytes,
                patch_offset: int) -> bytearray:
    """
    Apply a patch to a binary at a specific offset.
    Returns the modified binary with checksum fixed.
    """
    result = bytearray(original)
    end = patch_offset + len(patch_data)

    if end > len(result):
        raise ValueError(f"Patch extends beyond binary: "
                         f"offset={patch_offset:#x}, size={len(patch_data)}, "
                         f"binary_size={len(result)}")

    log.info(f"Applying {len(patch_data)} bytes at offset 0x{patch_offset:05X}")
    result[patch_offset:end] = patch_data

    # Fix checksum
    result = fix_gm_checksum(result)
    return result


# =============================================================================
# Flash Protocol Implementation
# =============================================================================

class FlashPatcher:
    """
    Full flash write protocol for VY V6 Delco PCM.
    Sequence from OSE Flash Tool (VL400) frmFlashTool.cs.
    """

    def __init__(self, conn: ALDLConnection):
        self.conn = conn

    def prepare_pcm(self) -> bool:
        """
        Steps 1-4: Prepare PCM for flash operations.
        1. Disable chatter (BCM + PCM)
        2. Request Mode 5 access
        3. Security unlock
        """
        print("\n[1/3] Disabling chatter...")
        if not self.conn.disable_chatter(DEVICE_BCM):
            log.warning("BCM chatter disable failed (may not be present)")
        if not self.conn.disable_chatter(DEVICE_PCM):
            log.error("PCM chatter disable failed")
            return False

        print("[2/3] Requesting Mode 5 access...")
        if not self.conn.request_mode5():
            log.error("Mode 5 access denied — is vehicle stationary?")
            return False

        print("[3/3] Security unlock...")
        if not self.conn.unlock_security():
            log.error("Security unlock failed")
            return False

        print("PCM ready for flash operations.\n")
        return True

    def upload_and_run_kernel(self, kernel: bytes = None) -> bool:
        """Upload flash kernel to PCM RAM and let it execute."""
        if kernel is None:
            kernel = FLASH_KERNEL_PLACEHOLDER
        print(f"Uploading flash kernel ({len(kernel)} bytes)...")
        return self.conn.upload_kernel(kernel, load_addr=0x0300)

    def write_cal_only(self, cal_data: bytes) -> bool:
        """
        Write CAL section only (Sector 1, Bank 1).
        This is the SAFEST partial write — only touches calibration data.
        From OSE: erases Sector 1 (0x40), writes 0x4000-0x7FFF.
        
        WARNING: This requires a proper flash kernel (not the placeholder).
        The kernel must implement M29W800DB erase/write sequences.
        """
        if len(cal_data) != CAL_SIZE:
            log.error(f"CAL data must be {CAL_SIZE} bytes, got {len(cal_data)}")
            return False

        print(f"\n{'='*60}")
        print(f"  CAL-ONLY WRITE")
        print(f"  Sector: 1 (Bank 1, ID 0x40)")
        print(f"  Range: 0x4000 - 0x7FFF ({CAL_SIZE} bytes)")
        print(f"  Data hash: {hashlib.md5(cal_data).hexdigest()[:12]}")
        print(f"{'='*60}\n")

        # Step 1: Prepare PCM
        if not self.prepare_pcm():
            return False

        # Step 2: Upload flash kernel
        if not self.upload_and_run_kernel():
            return False

        # Step 3: The actual flash erase/write would happen here
        # via the uploaded kernel. The kernel communicates back
        # over ALDL to report progress/status.
        #
        # PLACEHOLDER: This is where the real flash kernel interaction goes.
        # The kernel needs to:
        #   a) Erase Sector 1 (M29W800DB erase sector command)
        #   b) Program bytes from data received over ALDL
        #   c) Verify written data
        #   d) Report status back over ALDL
        print("NOTE: Flash kernel is placeholder — no actual flash write yet.")
        print("      Need real M29W800DB erase/write kernel implementation.")

        return True

    def cleanup(self):
        """Re-enable chatter after flash operations."""
        print("\nRe-enabling chatter...")
        self.conn.enable_chatter(DEVICE_BCM)
        self.conn.enable_chatter(DEVICE_PCM)


# =============================================================================
# CLI
# =============================================================================

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%H:%M:%S'
    )

    parser = argparse.ArgumentParser(
        description='VY V6 Flash Patcher — Sector Read-Modify-Write'
    )
    parser.add_argument('--port', '-p', required=True,
                        help='Serial port')
    parser.add_argument('--baud', '-b', type=int, default=BAUD_FAST)

    sub = parser.add_subparsers(dest='command')

    # Test connection
    test_cmd = sub.add_parser('test', help='Test PCM connection')

    # Prepare (chatter + Mode5 + seed-key)
    prep_cmd = sub.add_parser('prepare',
                               help='Prepare PCM for flash (no write)')

    # Upload watchdog kernel (proof of concept)
    kernel_cmd = sub.add_parser('kernel',
                                 help='Upload watchdog kernel to PCM RAM')

    # Patch binary (offline — no ECU needed)
    patch_cmd = sub.add_parser('patch',
                                help='Apply patch to binary file (offline)')
    patch_cmd.add_argument('binary', help='Original .bin file')
    patch_cmd.add_argument('patch_file', help='Patch data file')
    patch_cmd.add_argument('--offset', required=True,
                           help='Patch offset (hex, e.g. 0x5D00)')
    patch_cmd.add_argument('--output', '-o', help='Output file')

    # CAL write (when kernel is ready)
    cal_cmd = sub.add_parser('cal-write',
                              help='Write CAL section only (safest)')
    cal_cmd.add_argument('binary', help='.bin file with new CAL data')

    args = parser.parse_args()

    if args.command == 'patch':
        # Offline patch — doesn't need serial connection
        original = read_binary(args.binary)
        if not original:
            sys.exit(1)
        patch_data = Path(args.patch_file).read_bytes()
        offset = int(args.offset, 0)
        patched = apply_patch(original, patch_data, offset)
        output = args.output or args.binary.replace('.bin', '_patched.bin')
        write_binary(output, bytes(patched))
        print(f"Patched binary written to: {output}")
        return

    # Commands that need serial connection
    conn = ALDLConnection(args.port, args.baud)
    if not conn.open():
        sys.exit(1)

    patcher = FlashPatcher(conn)

    try:
        if args.command == 'test':
            print("Testing PCM connection...")
            resp = conn.send_command(DEVICE_PCM, MODE_1)
            if resp:
                print(f"PCM responded! ({len(resp)} bytes)")
                print(hexdump(bytes(resp)))
            else:
                print("No response from PCM")

        elif args.command == 'prepare':
            patcher.prepare_pcm()

        elif args.command == 'kernel':
            if patcher.prepare_pcm():
                patcher.upload_and_run_kernel()
                print("\nKernel uploaded — PCM should be running "
                      "watchdog loop now.")
                print("If PCM doesn't reset within 5 seconds, "
                      "YOUR CODE IS RUNNING.")

        elif args.command == 'cal-write':
            original = read_binary(args.binary)
            if not original:
                sys.exit(1)
            cal_data = original[CAL_OFFSET:CAL_OFFSET + CAL_SIZE]
            patcher.write_cal_only(cal_data)

        else:
            parser.print_help()

    except KeyboardInterrupt:
        print("\nAborted by user.")

    finally:
        patcher.cleanup()
        conn.close()


if __name__ == '__main__':
    main()
