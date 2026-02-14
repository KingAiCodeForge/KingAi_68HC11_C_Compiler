/**
 * pulse_counter.c — Pulse Accumulator event counter for 68HC11
 * ═════════════════════════════════════════════════════════════
 * Counts rising-edge pulses on PAI (Port A bit 7) using the HC11's
 * built-in pulse accumulator in event counting mode.
 *
 * Typical automotive use: Vehicle Speed Sensor (VSS) pulse counting.
 * The VSS generates a fixed number of pulses per revolution. Reading
 * PACNT periodically gives speed proportional to pulse count.
 *
 * HC11 Pulse Accumulator registers:
 *   PACTL ($1026): DDRA7=0 (input), PAEN=1 (enable), PAMOD=0 (event),
 *                  PEDGE=1 (rising edge) → value = $50
 *   PACNT ($1027): 8-bit pulse count, auto-increments on each edge
 *   TFLG2 ($1025): PAOVF (bit 5) = overflow flag, PAIF (bit 4) = input flag
 *
 * Reference: M68HC11 Reference Manual ch.10 (Pulse Accumulator)
 *            68HC11 Notes (Grand Valley State) section 15
 *
 * Compile: python hc11kit.py compile examples/pulse_counter.c -o pulse_counter.bin
 *
 * Demonstrates: Pulse accumulator, flag polling, volatile registers.
 * Full pipeline: C → ASM → binary → S19
 */

#define PACTL_ADDR  0x1026
#define PACNT_ADDR  0x1027
#define TFLG2_ADDR  0x1025
#define PORTA_ADDR  0x1000

/* PACTL: DDRA7=0, PAEN=1, PAMOD=0, PEDGE=1 → $50 */
#define PACTL_RISING_EVENT  0x50
/* TFLG2 bit masks */
#define PAOVF_BIT   0x20
#define PAIF_BIT    0x10

__zeropage unsigned char pulse_count;
__zeropage unsigned char overflow_count;

void pa_init() {
    volatile unsigned char *pactl = (volatile unsigned char *)PACTL_ADDR;
    volatile unsigned char *tflg2 = (volatile unsigned char *)TFLG2_ADDR;

    /* Enable pulse accumulator, event counting, rising edge */
    *pactl = PACTL_RISING_EVENT;

    /* Clear any pending overflow/input flags (write 1 to clear) */
    *tflg2 = PAOVF_BIT | PAIF_BIT;

    pulse_count = 0;
    overflow_count = 0;
}

unsigned char pa_read() {
    volatile unsigned char *pacnt = (volatile unsigned char *)PACNT_ADDR;
    volatile unsigned char *tflg2 = (volatile unsigned char *)TFLG2_ADDR;

    /* Check for overflow (>255 pulses since last read) */
    if ((*tflg2 & PAOVF_BIT) != 0) {
        overflow_count++;
        /* Clear overflow flag (write 1 to clear) */
        *tflg2 = PAOVF_BIT;
    }

    return *pacnt;
}

void main() {
    volatile unsigned char *porta = (volatile unsigned char *)PORTA_ADDR;

    pa_init();

    while (1) {
        pulse_count = pa_read();

        /* Simple speed indicator: light PA0 if pulses > threshold */
        if (pulse_count > 100) {
            *porta = *porta | 0x01;
        } else {
            *porta = *porta & 0xFE;
        }

        asm("WAI");
    }
}
