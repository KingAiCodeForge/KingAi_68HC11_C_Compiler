/**
 * rpm_limiter.c — RPM-based ignition cut limiter for Delco 68HC11 PCM
 * ════════════════════════════════════════════════════════════════════
 * Monitors the RPM byte at $00A2 and sets/clears a flag to cut
 * ignition when RPM exceeds the threshold. Uses hysteresis to
 * prevent rapid on/off cycling near the cut point.
 * This is the C equivalent of the hand-written spark cut assembly
 * patches in /asm_wip/spark_cut/. on the vy assembly moding github.
 * still validating and making sure opcodes are correct and methods.
 *
 * Compile: python hc11kit.py compile examples/rpm_limiter.c -o rpm_limiter.bin
 *
 * Demonstrates: Volatile I/O, hysteresis logic, bit manipulation.
 * Full pipeline: C → ASM → binary → S19
 *
 * NOTE: RAM addresses are target-specific. $00A2 = RPM byte on
 * VY V6 (OSID 92118883). $0046 is a user-chosen scratch byte.
 * Adjust for your specific PCM calibration.
 */

#define RPM_BYTE_ADDR    0x00A2  /* VY V6: RPM = E-clock / (period × 24) */
#define FLAGS_ADDR       0x0046  /* Scratch RAM — must be unused by stock code */

#define RPM_CUT_ON       0xF0    /* ~6000 RPM: activate cut    */
#define RPM_CUT_OFF      0xEC    /* ~5900 RPM: deactivate cut  */
#define LIMITER_BIT      0x80    /* Bit 7 of flags byte        */

__zeropage unsigned char limiter_active;

void check_rpm() {
    volatile unsigned char *rpm_ptr   = (volatile unsigned char *)RPM_BYTE_ADDR;
    volatile unsigned char *flags_ptr = (volatile unsigned char *)FLAGS_ADDR;
    unsigned char rpm;
    unsigned char flags;

    rpm = *rpm_ptr;
    flags = *flags_ptr;

    if (limiter_active == 0) {
        /* Not currently limiting — check if we should start */
        if (rpm >= RPM_CUT_ON) {
            limiter_active = 1;
            /* Set limiter flag: starves dwell → kills spark */
            *flags_ptr = flags | LIMITER_BIT;
        }
    } else {
        /* Currently limiting — check if RPM dropped enough */
        if (rpm < RPM_CUT_OFF) {
            limiter_active = 0;
            /* Clear limiter flag: restore normal spark */
            *flags_ptr = flags & 0x7F;
        }
    }
}

void main() {
    limiter_active = 0;

    while (1) {
        check_rpm();
        asm("WAI");
    }
}
