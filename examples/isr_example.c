/**
 * isr_example.c — Interrupt Service Routine example for Delco 68HC11 PCM
 * ══════════════════════════════════════════════════════════════════════
 * Demonstrates timer ISR for crank signal processing.
 * Uses the TIC3 input capture for 24X crank signal on VY V6.
 *
 * Compile: python hc11cc.py examples/isr_example.c -o isr.asm --target vy_v6
 *
 * Demonstrates: ISR with RTI, volatile I/O, zero-page variables.
 * Full pipeline: C → ASM → binary → S19
 */

#define TFLG1       0x1023
#define TMSK1       0x1022
#define TIC3_H      0x1014
#define TIC3_L      0x1015
#define TFLG1_IC3F  0x01
#define TMSK1_IC3I  0x01

/* Zero-page variables — fast access, critical for ISR performance */
__zeropage unsigned char crank_count;
__zeropage unsigned char crank_period_h;
__zeropage unsigned char crank_period_l;
__zeropage unsigned char last_capture_h;
__zeropage unsigned char last_capture_l;
__zeropage unsigned char rpm_byte;

/* Extended RAM variables */
unsigned int total_teeth;

void init_timer() {
    volatile unsigned char *tmsk1 = (volatile unsigned char *)0x1022;
    volatile unsigned char *tflg1 = (volatile unsigned char *)0x1023;
    unsigned char val;

    /* Enable IC3 interrupt (crank signal) — set bit 0 */
    val = *tmsk1;
    *tmsk1 = val | 0x01;

    crank_count = 0;
    total_teeth = 0;
    rpm_byte = 0;

    /* Clear any pending IC3 flag */
    *tflg1 = 0x01;

    /* Enable interrupts globally */
    asm("CLI");
}

/**
 * TIC3 ISR — Crank signal handler
 * Called on each 24X tooth (24 times per crank revolution).
 * Computes crank period for RPM calculation.
 */
__interrupt void tic3_isr() {
    volatile unsigned char *tflg1 = (volatile unsigned char *)0x1023;
    volatile unsigned char *tic3h = (volatile unsigned char *)0x1014;
    volatile unsigned char *tic3l = (volatile unsigned char *)0x1015;

    /* Clear IC3 flag by writing 1 to bit 0 of TFLG1 */
    *tflg1 = 0x01;

    /* Read captured time */
    crank_period_h = *tic3h;
    crank_period_l = *tic3l;

    /* Increment tooth counter */
    crank_count++;

    /* Every 24 teeth = 1 revolution */
    if (crank_count >= 24) {
        crank_count = 0;
        total_teeth = total_teeth + 24;
    }
}

void main() {
    init_timer();

    /* Main loop — real work happens in ISRs */
    while (1) {
        /* Calculate RPM from crank period */
        /* RPM = 60,000,000 / (period_us * 24) */
        /* For 8-bit approximation: rpm_byte = period-based lookup */
        if (crank_period_h == 0) {
            if (crank_period_l < 10) {
                rpm_byte = 255;   /* Very high RPM (overflow protection) */
            } else {
                rpm_byte = 250;   /* High RPM */
            }
        } else {
            rpm_byte = 100;       /* Moderate RPM estimate */
        }

        /* Wait for interrupt */
        asm("WAI");
    }
}
