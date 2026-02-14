/*
 * aldl_report_rpm.c — Read RPM from Delco RAM and send over ALDL
 *
 * PURPOSE:
 *   Demonstrates reading a live engine parameter from the PCM's internal
 *   RAM and transmitting it over the ALDL serial port. This is a more
 *   practical example than hello world — it proves:
 *   1. The compiled code can access VY V6 RAM addresses
 *   2. The SCI transmitter works from compiled C
 *   3. A scan tool can receive meaningful engine data
 *
 * WHAT IT DOES:
 *   Reads the RPM variable from RAM ($00A2-$00A3 = RPM in counts),
 *   converts to a 2-byte value, and sends it over ALDL with a simple
 *   framing: [0xAA] [RPM_HI] [RPM_LO] [checksum]
 *
 * HOW TO USE:
 *   python hc11kit.py compile examples/aldl_report_rpm.c -o rpm_report.bin --target vy_v6
 *   python hc11kit.py patch stock.bin rpm_report.bin --at 0x5D00 --hook 0x101E1:3
 *
 * RPM SCALING:
 *   VY V6: RPM = 120000 / period_count (16-bit period at $00A2)
 *   At 6000 RPM: period = 20 counts (0x0014)
 *   At 800 RPM:  period = 150 counts (0x0096)
 *   We send the raw period — the PC-side tool converts to RPM.
 *
 * SAFETY:
 *   Read-only access to engine RAM. Only writes to SCI TX register.
 *   Safe for bench and running engine testing.
 */

#define SCSR    0x102E
#define SCDR    0x102F
#define TDRE    0x80

/* VY V6 RAM addresses (from XDF / disassembly) */
#define RPM_PERIOD_HI   0x00A2
#define RPM_PERIOD_LO   0x00A3

void sci_tx(unsigned char b) {
    while ((*(volatile unsigned char *)SCSR & TDRE) == 0) {
    }
    *(volatile unsigned char *)SCDR = b;
}

void main() {
    unsigned char rpm_hi;
    unsigned char rpm_lo;
    unsigned char checksum;

    /* Read RPM period from Delco RAM */
    rpm_hi = *(volatile unsigned char *)RPM_PERIOD_HI;
    rpm_lo = *(volatile unsigned char *)RPM_PERIOD_LO;

    /* Simple frame: [sync] [data_hi] [data_lo] [checksum] */
    checksum = 0xAA + rpm_hi + rpm_lo;

    sci_tx(0xAA);           /* Sync byte */
    sci_tx(rpm_hi);         /* RPM period high byte */
    sci_tx(rpm_lo);         /* RPM period low byte */
    sci_tx(checksum);       /* Simple additive checksum */
}
