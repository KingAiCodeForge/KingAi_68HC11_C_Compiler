/*
 * aldl_flash_read_sector.c — Read Flash Contents Over ALDL
 *
 * Target: 68HC11 (VY V6 92118883, $060A Enhanced OS, 128KB AMD 29F010)
 * Purpose: Read the full 128KB flash contents via ALDL Mode 5/6 protocol.
 *
 * Flash Read Flow (from OSE Flash Tool ALDLGetVXYFlash(), line 24082):
 *   1. DisableChatter() — silence BCM + PCM heartbeats
 *   2. UnlockFlashPCM() — Mode 13 seed/key security exchange
 *   3. Mode5Request() — enter programming mode (vehicle must be stationary)
 *   4. Mode6VXYUploadExec() — upload HC11 machine code to PCM RAM (3 blocks)
 *   5. Mode6VXYUploadFlashInfo() — detect flash chip type (AMD vs CAT/Intel)
 *   6. Read loop — request data blocks, accumulate 128KB
 *   7. EnableChatter() — re-enable BCM/PCM periodic messages
 *
 * Mode 5 (Enter Programming Mode):
 *   TX → [DevID] [0x56] [0x05] [checksum]
 *   RX ← [DevID] [0x56] [0x05] [checksum]  (acknowledged)
 *
 * Mode 6 (Upload & Execute):
 *   TX → [DevID] [len] [0x06] [sub] [data...] [checksum]
 *   RX ← [DevID] [0x57] [0x06] [0xAA] [checksum]  (acknowledged)
 *
 * The uploaded kernel runs inside the PCM's HC11 CPU. It implements:
 *   - Flash chip ID query (manufacturer + device ID)
 *   - Sequential read of all flash addresses
 *   - Data streaming back over ALDL SCI
 *
 * Memory Map (92118883, 128KB):
 *   0x00000 - 0x01FFF : Boot block (never overwritten by OSE)
 *   0x02000 - 0x03FFF : OS/cal shared area (written in BIN mode only)
 *   0x04000 - 0x07FFF : Calibration data (16KB) — CAL write target
 *   0x04006 - 0x04007 : Checksum storage (big-endian 16-bit)
 *   0x08000 - 0x1BFFF : Operating system code (BIN write stops here)
 *   0x1C000 - 0x1FFFF : Extended OS (PROM recovery only)
 *
 * Verified against: OSE ALDLWriteBinCalVXYFlash() L24168-24228
 *   CAL write: ALDLWriteCalData(16384, 32767) = 0x4000-0x7FFF
 *   BIN write: 0x2000-0x1BFFF (114687 decimal)
 *   PROM write: 0x2000-0x1FFFF (131071 decimal)
 *
 * Sector Layout (AMD 29F010 = 8 × 16KB sectors):
 *   Sector 0: 0x00000 - 0x03FFF
 *   Sector 1: 0x04000 - 0x07FFF
 *   Sector 2: 0x08000 - 0x0BFFF
 *   Sector 3: 0x0C000 - 0x0FFFF
 *   Sector 4: 0x10000 - 0x13FFF
 *   Sector 5: 0x14000 - 0x17FFF
 *   Sector 6: 0x18000 - 0x1BFFF
 *   Sector 7: 0x1C000 - 0x1FFFF
 *
 * Speed Analysis:
 *   128KB at 8192 baud (effective ~600 bytes/sec with framing overhead)
 *   ≈ 215 seconds ≈ 3.5 minutes for a full read
 *   Cal-only read (16KB): ≈ 27 seconds
 *
 * Cross-reference:
 *   - OSE Flash Tool: ALDLGetVXYFlash() line 24082
 *   - OSE Flash Tool: Mode6VXYUploadExec() line 24464 (kernel bytecode)
 *   - OSE Flash Tool: Mode6VXYUploadFlashInfo() line 24610
 *   - PcmHammer: CKernelReader.cs (VPW equivalent architecture)
 *   - PcmHammer: flash-amd.c (AMD 29F010 command sequences)
 *
 * Status: WIP — Flow documented, kernel bytecode extracted but not disassembled
 *
 * Python PC-side read flow:
 *
 *   import serial, time
 *   
 *   def aldl_read_full_bin(port='COM3'):
 *       """Read full 128KB from 92118883 via ALDL."""
 *       ser = serial.Serial(port, 8192, timeout=2,
 *                           bytesize=8, parity='N', stopbits=1)
 *       
 *       # Step 1: Silence the bus
 *       disable_chatter(ser, 0xF1)  # BCM
 *       disable_chatter(ser, 0xF7)  # PCM
 *       
 *       # Step 2: Security unlock
 *       seed = request_seed(ser)  # Mode 13 sub 1
 *       key = compute_key(seed[0], seed[1])
 *       send_key(ser, key)        # Mode 13 sub 2
 *       
 *       # Step 3: Enter programming mode
 *       mode5_request(ser)
 *       
 *       # Step 4: Upload flash kernel (3 blocks of HC11 machine code)
 *       upload_kernel_block(ser, KERNEL_BLOCK_0)  # 171 bytes
 *       upload_kernel_block(ser, KERNEL_BLOCK_1)  # 172 bytes
 *       upload_kernel_block(ser, KERNEL_BLOCK_2)  # 156 bytes
 *       
 *       # Step 5: Detect flash chip
 *       flash_type = upload_flash_info(ser)
 *       
 *       # Step 6: Read all 128KB
 *       bin_data = bytearray()
 *       for addr in range(0, 0x20000, BLOCK_SIZE):
 *           block = read_flash_block(ser, addr, BLOCK_SIZE)
 *           bin_data.extend(block)
 *           print(f"\r{addr:05X}/{0x1FFFF:05X}", end='')
 *       
 *       # Step 7: Re-enable chatter
 *       enable_chatter(ser, 0xF7)
 *       enable_chatter(ser, 0xF1)
 *       ser.close()
 *       
 *       return bytes(bin_data)
 */

#include "delco_hc11.h"

/* This file is a protocol reference — the actual read operation
 * is performed by the PC-side Python tool sending ALDL commands
 * and the HC11 kernel (uploaded via Mode 6) executing inside the PCM.
 *
 * The kernel bytecode arrays from Mode6VXYUploadExec() are the actual
 * HC11 machine code that runs inside the PCM to perform the read.
 * See the OSE Flash Tool decompilation at line 24464-24560 for the
 * raw byte arrays.
 *
 * Kernel Block 0 (171 bytes): Main loop + SCI frame handler
 * Kernel Block 1 (172 bytes): Flash read + data streaming
 * Kernel Block 2 (156 bytes): Interrupt vectors + checksum verify
 */
