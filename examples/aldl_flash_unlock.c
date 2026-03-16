/*
 * aldl_flash_unlock.c — Security Seed/Key Exchange for ALDL Flash Operations
 * 
 * Target: 68HC11 (VY V6 92118883, $060A Enhanced OS)
 * Purpose: Respond to Mode 13 security seed request with the correct key
 *          to unlock the PCM for flash read/write operations.
 *
 * ALDL Security Protocol (Mode 13):
 *   PC → ECU:  [DevID] [0x57] [0x0D] [0x01] [checksum]     (Request seed, sub 1)
 *   ECU → PC:  [DevID] [0x59] [0x0D] [0x01] [SH] [SL] [cs] (Seed response)
 *   PC → ECU:  [DevID] [0x59] [0x0D] [0x02] [KH] [KL] [cs] (Send key, sub 2)
 *   ECU → PC:  [DevID] [0x58] [0x0D] [0x02] [result] [cs]  (Key accept/reject)
 *                        ^^^^ NOTE: response header is 0x58, NOT 0x57 or 0x59
 *                        result: 0xAA = security passed, 0xCC = key rejected
 *   Verified against: OSE UnlockFlashPCM() L24029 — RxFrame[1]==88(0x58)
 *
 * Key Algorithm (from OSE Flash Tool V1.5.1 decompilation, line 23932):
 *   key = 37709 - byte_swap(seed)
 *   if (key < 0) key += 65536;
 *   
 *   Where byte_swap means: seed bytes [SH][SL] → value = SL*256 + SH
 *   (i.e., the seed bytes are swapped before subtraction)
 *   37709 = 0x934D (same constant used in older VPW PCMs)
 *
 * IMPORTANT: This is a PC-side algorithm reference, not ECU-side code.
 *            The ECU generates the seed, the PC computes and sends the key.
 *
 * Cross-reference:
 *   - OSE Flash Tool: UnlockFlashPCM() at line 23932
 *   - PcmHammer: SeedAndKeyAlgorithm.txt (VPW version uses 0x1934D)
 *   - ALDL_POC_AND_EXAMPLES.md in kingai_c_compiler_v0.1/ignore/
 *
 * Status: WIP — Algorithm extracted, not yet tested on hardware
 */

#include "delco_hc11.h"

/* 
 * This file documents the PC-side key computation.
 * For the Python implementation, see the Python port plan in:
 *   ../Red_Devil_River_ALDL_Cable/flash_over_bluetooth_aldl_to_vy_v6.md
 *
 * Python equivalent:
 *
 *   def compute_aldl_key(seed_hi, seed_lo):
 *       """Compute ALDL security key from 2-byte seed."""
 *       swapped = (seed_lo << 8) | seed_hi  # byte swap
 *       key = 37709 - swapped               # 37709 = 0x934D
 *       if key < 0:
 *           key += 65536
 *       return (key >> 8) & 0xFF, key & 0xFF  # key_hi, key_lo
 */

/* ALDL frame constants */
#define ALDL_DEVICE_PCM   0xF7
#define ALDL_MODE13_REQ   0x57  /* Mode 13 request header byte */
#define ALDL_MODE13_RESP  0x59  /* Mode 13 response header byte */
#define ALDL_SECURITY     0x0D  /* Security sub-command */
#define ALDL_SUB_SEED     0x01  /* Sub-mode: request seed */
#define ALDL_SUB_KEY      0x02  /* Sub-mode: send key */

/* Security key constant — specific to ALDL Delco PCMs */
#define ALDL_KEY_CONSTANT 37709  /* 0x934D */

/*
 * compute_key — Calculate unlock key from seed bytes
 * 
 * seed_hi: High byte of seed (RxFrame[4])
 * seed_lo: Low byte of seed (RxFrame[5])
 * 
 * Returns: 16-bit key value
 *
 * Note: The seed bytes are SWAPPED before subtraction.
 * The OSE decompilation shows: num2 = 37709 - (RxFrame[5]*256 + RxFrame[4])
 * So the "low" byte from the wire becomes the high byte of the integer.
 */
unsigned int compute_key(unsigned char seed_hi, unsigned char seed_lo)
{
    int swapped_seed;
    int key;
    
    /* Byte-swap: wire order [HI][LO] → integer value LO*256+HI */
    swapped_seed = ((int)seed_lo << 8) | (int)seed_hi;
    
    key = ALDL_KEY_CONSTANT - swapped_seed;
    
    if (key < 0)
        key += 65536;
    
    return (unsigned int)(key & 0xFFFF);
}

/*
 * ALDL checksum calculation:
 *   checksum = (256 - sum_of_all_bytes_before_checksum) & 0xFF
 *
 * This is the standard Delco ALDL checksum used in all frames.
 */
unsigned char aldl_checksum(unsigned char *frame, int len)
{
    int sum = 0;
    int i;
    
    for (i = 0; i < len; i++)
        sum += frame[i];
    
    return (unsigned char)((256 - sum) & 0xFF);
}
