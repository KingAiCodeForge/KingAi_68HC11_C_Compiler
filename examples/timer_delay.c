/**
 * timer_delay.c — Timer-based port toggle for Delco 68HC11 PCM
 * ═════════════════════════════════════════════════════════════
 * Toggles Port A bit 0 using TCNT polling for coarse timing.
 * Reads the free-running counter high byte and waits for it to
 * change a specified number of times (~128 µs per tick at 2 MHz).
 *
 * On the HC11 at 2 MHz E-clock, TCNT increments every 500ns.
 * The high byte rolls over every 256 × 500ns = 128 µs.
 * Waiting for N high-byte changes ≈ N × 128 µs delay.
 *
 * Compile: python hc11kit.py compile examples/timer_delay.c -o timer_delay.bin
 *
 * Demonstrates: Timer register polling, volatile I/O, software timing.
 * Full pipeline: C → ASM → binary → S19
 */

#define TCNT_H_ADDR  0x100E
#define PORTA_ADDR   0x1000

__zeropage unsigned char toggle_state;

void delay_ticks(unsigned char ticks) {
    volatile unsigned char *tcnth = (volatile unsigned char *)TCNT_H_ADDR;
    unsigned char last;
    unsigned char count;

    last = *tcnth;
    count = 0;

    while (count < ticks) {
        if (*tcnth != last) {
            last = *tcnth;
            count++;
        }
    }
}

void main() {
    volatile unsigned char *porta = (volatile unsigned char *)PORTA_ADDR;

    toggle_state = 0;

    while (1) {
        toggle_state = toggle_state ^ 0x01;
        *porta = toggle_state;

        /* ~250 ticks × 128 µs ≈ 32 ms toggle rate */
        delay_ticks(250);
    }
}
