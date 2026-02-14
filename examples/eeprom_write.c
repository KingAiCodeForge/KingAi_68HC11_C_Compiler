/**
 * eeprom_write.c — Internal EEPROM byte programming for 68HC11
 * ═════════════════════════════════════════════════════════════
 * Writes a single byte to the HC11's on-chip EEPROM using the
 * timed programming sequence (BYTE ERASE + BYTE PROGRAM).
 *
 * The HC11F1 has 512 bytes of EEPROM at $FE00-$FFFF (or remapped).
 * The HC11E9 has 512 bytes at $B600-$B7FF.
 * Programming requires a specific PPROG register sequence with
 * precise timing (~10ms erase, ~10ms program).
 *
 * HC11 EEPROM registers:
 *   PPROG ($103B): BYTE=1 for byte erase, ERASE=1, EELAT=1, EPGM=1
 *   CONFIG ($103F): EEON bit enables EEPROM visibility
 *
 * Reference: M68HC11 Reference Manual section 4.3 (EEPROM)
 *            AN1010/D: M68HC11 EEPROM Programming
 *
 * Compile: python hc11kit.py compile examples/eeprom_write.c -o eeprom_write.bin
 *
 * Demonstrates: Timed register sequences, fixed delays, EEPROM I/O.
 * Full pipeline: C → ASM → binary → S19
 */

#define PPROG_ADDR      0x103B
#define EEPROM_BASE     0xB600  /* HC11E9 EEPROM base */

/* PPROG register bits */
#define EELAT   0x02    /* EEPROM Latch mode   */
#define EPGM    0x01    /* EEPROM Program voltage */
#define ERASE   0x04    /* Erase mode          */
#define BYTE_E  0x10    /* Byte erase (vs bulk) */

void delay_10ms() {
    /* Software delay for ~10ms at 2 MHz E-clock.
     * Each loop iteration ≈ 8 cycles = 4 µs.
     * 10000 µs / 4 µs = 2500 iterations.
     * Using nested loops: 10 × 250 = 2500. */
    unsigned char i;
    unsigned char j;

    i = 10;
    while (i > 0) {
        j = 250;
        while (j > 0) {
            j--;
        }
        i--;
    }
}

void eeprom_erase_byte(unsigned char offset) {
    volatile unsigned char *pprog = (volatile unsigned char *)PPROG_ADDR;
    volatile unsigned char *addr;

    /* Calculate EEPROM address: base + offset */
    addr = (volatile unsigned char *)(EEPROM_BASE + offset);

    /* Step 1: Set EELAT + ERASE + BYTE to enter byte-erase latch mode */
    *pprog = BYTE_E | ERASE | EELAT;

    /* Step 2: Write any data to the target EEPROM address */
    *addr = 0xFF;

    /* Step 3: Turn on programming voltage (set EPGM) */
    *pprog = BYTE_E | ERASE | EELAT | EPGM;

    /* Step 4: Wait 10ms for erase to complete */
    delay_10ms();

    /* Step 5: Turn off programming voltage */
    *pprog = BYTE_E | ERASE | EELAT;

    /* Step 6: Clear EELAT to exit latch mode */
    *pprog = 0x00;
}

void eeprom_program_byte(unsigned char offset, unsigned char data) {
    volatile unsigned char *pprog = (volatile unsigned char *)PPROG_ADDR;
    volatile unsigned char *addr;

    addr = (volatile unsigned char *)(EEPROM_BASE + offset);

    /* Step 1: Set EELAT (latch mode for programming) */
    *pprog = EELAT;

    /* Step 2: Write desired data to EEPROM address */
    *addr = data;

    /* Step 3: Turn on programming voltage */
    *pprog = EELAT | EPGM;

    /* Step 4: Wait 10ms for programming */
    delay_10ms();

    /* Step 5: Turn off programming voltage */
    *pprog = EELAT;

    /* Step 6: Exit latch mode */
    *pprog = 0x00;
}

void main() {
    /* Write 0x42 to EEPROM offset 0 ($B600) */
    eeprom_erase_byte(0);
    eeprom_program_byte(0, 0x42);

    /* Verify: read back and compare */
    volatile unsigned char *verify = (volatile unsigned char *)EEPROM_BASE;
    unsigned char readback;

    readback = *verify;
    if (readback == 0x42) {
        /* Success — toggle PA0 as indicator */
        volatile unsigned char *porta = (volatile unsigned char *)0x1000;
        *porta = *porta | 0x01;
    }

    while (1) {
        asm("WAI");
    }
}
