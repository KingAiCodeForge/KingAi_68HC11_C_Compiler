/*
 * aldl_flash_erase_sector.c — AMD 29F010 Sector Erase via ALDL
 *
 * Target: 68HC11 (VY V6 92118883, $060A Enhanced OS)
 * Flash: AMD 29F010 (128KB, 8 × 16KB sectors)
 *
 * This documents the sector erase command sequence that the uploaded
 * HC11 kernel executes inside the PCM. The PC sends the erase command
 * via ALDL Mode 6, and the kernel performs the actual flash chip operations.
 *
 * AMD 29F010 Sector Erase Command Sequence:
 *   (from PcmHammer flash-amd.c + OSE Mode6VXYUploadEraseSector)
 *
 *   Write 0xAA to 0x5555    (1st bus cycle)
 *   Write 0x55 to 0x2AAA    (2nd bus cycle)
 *   Write 0x80 to 0x5555    (3rd bus cycle — erase setup)
 *   Write 0xAA to 0x5555    (4th bus cycle)
 *   Write 0x55 to 0x2AAA    (5th bus cycle)
 *   Write 0x30 to sector_addr  (6th bus cycle — sector erase)
 *
 * Then poll for completion using toggle-bit (bit 6):
 *   Read sector_addr repeatedly
 *   When bit 6 stops toggling, erase is complete
 *   Typical time: 1-2 seconds per sector
 *
 * After erase, verify sector is all 0xFF:
 *   Read every byte in the 16KB sector
 *   All should be 0xFF
 *
 * Sector Addresses:
 *   Sector 0: 0x00000   Sector 4: 0x10000
 *   Sector 1: 0x04000   Sector 5: 0x14000
 *   Sector 2: 0x08000   Sector 6: 0x18000
 *   Sector 3: 0x0C000   Sector 7: 0x1C000
 *
 * OSE Flash Tool sector parameters:
 *   Full erase: bank parameter 0x48 (72 decimal)
 *   Cal-only erase: bank parameter 0x40 (64 decimal)
 *   These values select which sectors the uploaded kernel erases
 *
 * Cross-reference:
 *   - PcmHammer: Kernels/flash-amd.c → Amd_EraseBlock()
 *   - OSE Flash Tool: Mode6VXYUploadEraseSector() line 24739
 *   - AMD 29F010 datasheet: sector erase algorithm
 *
 * Status: WIP — Algorithm documented, not yet compiled or tested
 */

#include "delco_hc11.h"

/* AMD 29F010 command addresses (A0-A14 only) */
#define AMD_CMD_ADDR1  0x5555
#define AMD_CMD_ADDR2  0x2AAA

/* AMD 29F010 command bytes */
#define AMD_CMD_UNLOCK1     0xAA
#define AMD_CMD_UNLOCK2     0x55
#define AMD_CMD_ERASE_SETUP 0x80
#define AMD_CMD_SECTOR_ERASE 0x30
#define AMD_CMD_CHIP_ERASE  0x10
#define AMD_CMD_PROGRAM     0xA0
#define AMD_CMD_READ_RESET  0xF0

/* AMD status bits */
#define AMD_TOGGLE_BIT  0x40  /* Bit 6 — toggles during erase/program */
#define AMD_TIMEOUT_BIT 0x20  /* Bit 5 — exceeds time limit */

/* Sector size = 16KB */
#define SECTOR_SIZE     0x4000

/*
 * amd_erase_sector — Erase one 16KB sector of AMD 29F010
 *
 * This code runs INSIDE the HC11 on the PCM.
 * The flash chip is memory-mapped into the HC11's address space.
 *
 * sector_addr: Base address of sector to erase (0x0000, 0x4000, 0x8000, etc.)
 *
 * Returns: 0 = success, 1 = timeout/failure
 */
unsigned char amd_erase_sector(volatile unsigned char *flash_base, unsigned int sector_addr)
{
    volatile unsigned char *addr1 = flash_base + AMD_CMD_ADDR1;
    volatile unsigned char *addr2 = flash_base + AMD_CMD_ADDR2;
    volatile unsigned char *sector = flash_base + sector_addr;
    unsigned char val1, val2;
    unsigned int timeout;
    unsigned int i;
    
    /* 6-byte erase command sequence */
    *addr1 = AMD_CMD_UNLOCK1;     /* 0xAA → 0x5555 */
    *addr2 = AMD_CMD_UNLOCK2;     /* 0x55 → 0x2AAA */
    *addr1 = AMD_CMD_ERASE_SETUP; /* 0x80 → 0x5555 */
    *addr1 = AMD_CMD_UNLOCK1;     /* 0xAA → 0x5555 */
    *addr2 = AMD_CMD_UNLOCK2;     /* 0x55 → 0x2AAA */
    *sector = AMD_CMD_SECTOR_ERASE; /* 0x30 → sector base */
    
    /* Toggle-bit polling — wait for erase to complete */
    timeout = 65535;
    val1 = *sector;
    while (timeout > 0)
    {
        val2 = *sector;
        if ((val1 & AMD_TOGGLE_BIT) == (val2 & AMD_TOGGLE_BIT))
            break;  /* Toggle stopped — erase complete */
        val1 = val2;
        timeout--;
    }
    
    /* Reset to read mode */
    *addr1 = AMD_CMD_READ_RESET;
    
    if (timeout == 0)
        return 1;  /* Erase timed out */
    
    /* Verify all bytes are 0xFF */
    for (i = 0; i < SECTOR_SIZE; i++)
    {
        if (sector[i] != 0xFF)
            return 1;  /* Verify failed */
    }
    
    return 0;  /* Success */
}

/*
 * amd_program_byte — Program a single byte to AMD 29F010
 *
 * addr: Absolute address in flash
 * data: Byte value to program
 *
 * Returns: 0 = success, 1 = failure
 */
unsigned char amd_program_byte(volatile unsigned char *flash_base, 
                                unsigned int addr, unsigned char data)
{
    volatile unsigned char *addr1 = flash_base + AMD_CMD_ADDR1;
    volatile unsigned char *addr2 = flash_base + AMD_CMD_ADDR2;
    volatile unsigned char *target = flash_base + addr;
    unsigned char val1, val2;
    unsigned int timeout;
    
    /* 3-byte program command sequence */
    *addr1 = AMD_CMD_UNLOCK1;  /* 0xAA → 0x5555 */
    *addr2 = AMD_CMD_UNLOCK2;  /* 0x55 → 0x2AAA */
    *addr1 = AMD_CMD_PROGRAM;  /* 0xA0 → 0x5555 */
    *target = data;            /* Write data to target address */
    
    /* Toggle-bit polling — wait for program to complete */
    timeout = 65535;
    val1 = *target;
    while (timeout > 0)
    {
        val2 = *target;
        if ((val1 & AMD_TOGGLE_BIT) == (val2 & AMD_TOGGLE_BIT))
            break;
        val1 = val2;
        timeout--;
    }
    
    /* Verify */
    if (*target != data)
        return 1;  /* Program verify failed */
    
    return 0;  /* Success */
}
