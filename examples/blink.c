/**
 * blink.c — Minimal port toggle example for Delco 68HC11 PCM
 * ═══════════════════════════════════════════════════════════
 * Toggles Port A bit 0 in a delay loop.
 * Compile: python hc11cc.py examples/blink.c -o blink.asm --target generic
 *
 * Demonstrates: volatile pointers for I/O, delay loop, XOR toggle.
 * Full pipeline: C → ASM → binary → S19
 */

#define PORTA_ADDR  0x1000

__zeropage unsigned char pa_state;

void delay() {
    unsigned char i;
    i = 255;
    while (i > 0) {
        i--;
    }
}

void main() {
    volatile unsigned char *porta = (volatile unsigned char *)PORTA_ADDR;
    pa_state = 0;

    while (1) {
        pa_state = pa_state ^ 0x01;

        /* Write toggled state to Port A via volatile pointer */
        *porta = pa_state;

        delay();
    }
}
