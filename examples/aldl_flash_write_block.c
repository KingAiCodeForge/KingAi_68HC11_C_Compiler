/*
 * aldl_flash_write_block.c — Write Data to AMD 29F010 Flash via ALDL
 *
 * Target: 68HC11 (VY V6 92118883, $060A Enhanced OS, 128KB flash)
 * Purpose: Write calibration or full bin data after sector erase
 *
 * Write Flow (from OSE Flash Tool ALDLWriteBinCalVXYFlash(), line 24107):
 *   1. Load bin file, auto-fix checksum at 0x4006-0x4007
 *   2. DisableChatter() — silence BCM + PCM
 *   3. UnlockFlashPCM() — Mode 13 seed/key
 *   4. Mode5Request() — enter programming mode
 *   5. Mode6VXYUploadExec() — upload HC11 kernel (3 blocks)
 *   6. Mode6VXYUploadFlashInfo() — detect flash chip
 *   7. Mode6VXYUploadEraseSector() — erase target sector(s)
 *   8. Mode6VXYWriteBin() — write data in blocks
 *   9. Mode6VXYUploadCheckSumBin() — verify checksum
 *   10. EnableChatter() — re-enable periodic messages
 *
 * Checksum Auto-Fix (from OSE decompile, line 24157):
 *   checksum_addr = 0x4006 (16390 decimal)
 *   sum = sum of all bytes 0x2000 to 0x1FFFF, EXCLUDING bytes 0x4000-0x4007
 *   stored_checksum = WriteBin[0x4006]*256 + WriteBin[0x4007]
 *   if sum != stored_checksum:
 *       WriteBin[0x4006] = (sum >> 8) & 0xFF
 *       WriteBin[0x4007] = sum & 0xFF
 *
 * Write Modes (verified against OSE ALDLWriteBinCalVXYFlash L24168-24228):
 *   Full bin write:  Erase sectors 0-6 → write 0x2000-0x1BFFF (~106KB)
 *   PROM recovery:   Erase all 8 sectors → write 0x2000-0x1FFFF (~120KB)
 *   Cal-only write:  Erase sector 1 only → write 0x4000-0x7FFF (16KB)
 *
 * Time Estimates:
 *   Full write:     ≈ 3.5 minutes (erase + 128KB at 8192 baud)
 *   Cal-only write: ≈ 30 seconds (erase + 16KB)
 *
 * CRITICAL Safety Notes:
 *   - NEVER interrupt a write operation mid-sector
 *   - If power is lost during erase/write, the sector is BRICKED
 *   - Always verify checksum after write
 *   - Keep ignition ON and stable throughout
 *   - For bench flash: use a stable 12V power supply
 *   - Store a backup of the ORIGINAL bin before any write
 *
 * Cross-reference:
 *   - OSE Flash Tool: ALDLWriteBinCalVXYFlash() line 24107
 *   - OSE Flash Tool: Mode6VXYWriteBin() line 24956
 *   - OSE Flash Tool: Mode6VXYUploadCheckSumBin() line 24999
 *   - PcmHammer: CKernelWriter.cs (VPW equivalent)
 *   - PcmHammer: flash-amd.c → Amd_WriteToFlash()
 *
 * Status: WIP — Protocol documented, not yet tested
 */

#include "delco_hc11.h"

/*
 * Python PC-side write flow:
 *
 *   def aldl_write_bin(port, bin_path, cal_only=True):
 *       """Write bin file to 92118883 via ALDL."""
 *       
 *       # Load and fix checksum
 *       bin_data = bytearray(open(bin_path, 'rb').read())
 *       assert len(bin_data) == 131072, "Must be exactly 128KB"
 *       fix_checksum(bin_data)
 *       
 *       ser = serial.Serial(port, 8192, timeout=2)
 *       
 *       try:
 *           # 1. Silence bus
 *           disable_chatter(ser, 0xF1)
 *           disable_chatter(ser, 0xF7)
 *           
 *           # 2. Security unlock
 *           seed = request_seed(ser)
 *           key = compute_key(seed[0], seed[1])
 *           send_key(ser, key)
 *           
 *           # 3. Programming mode
 *           mode5_request(ser)
 *           
 *           # 4. Upload kernel
 *           upload_kernel(ser)
 *           
 *           # 5. Detect flash chip
 *           flash_type = detect_flash(ser)
 *           
 *           # 6. Erase
 *           if cal_only:
 *               erase_sectors(ser, [0, 1])      # Cal sectors only
 *           else:
 *               erase_sectors(ser, range(8))     # All sectors
 *           
 *           # 7. Write data
 *           if cal_only:
 *               write_region(ser, bin_data, 0x2000, 0x6000)
 *           else:
 *               write_region(ser, bin_data, 0x0000, 0x20000)
 *           
 *           # 8. Verify checksum
 *           verify_checksum(ser)
 *           
 *       finally:
 *           # ALWAYS re-enable chatter
 *           enable_chatter(ser, 0xF7)
 *           enable_chatter(ser, 0xF1)
 *           ser.close()
 *
 *
 *   def fix_checksum(bin_data):
 *       """Auto-fix checksum at 0x4006-0x4007."""
 *       cs_addr = 0x4006
 *       total = 0
 *       for i in range(0x2000, 0x20000):
 *           if 0x4000 <= i <= 0x4007:
 *               continue  # Skip checksum region
 *           total += bin_data[i]
 *       total &= 0xFFFF
 *       stored = (bin_data[cs_addr] << 8) | bin_data[cs_addr + 1]
 *       if total != stored:
 *           bin_data[cs_addr] = (total >> 8) & 0xFF
 *           bin_data[cs_addr + 1] = total & 0xFF
 *           print(f"Fixed checksum: {stored:04X} → {total:04X}")
 */

/* Checksum region constants */
#define CHECKSUM_ADDR    0x4006
#define CAL_START        0x2000
#define CAL_END          0x5FFF
#define FLASH_SIZE       0x20000  /* 128KB */
#define SECTOR_SIZE      0x4000   /* 16KB */
