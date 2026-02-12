/**
 * blink.c — Minimal port toggle example for Delco 68HC11 PCM
 * ═══════════════════════════════════════════════════════════
 * Toggles Port A bit 0 in a delay loop.
 * Compile: python hc11cc.py examples/blink.c -o blink.asm --target generic
 */

#define PORTA   0x1000
#define DDRA    0x1001

unsigned char delay_count;

void delay() {
    unsigned char i;
    i = 255;
    while (i > 0) {
        i--;
    }
}

void main() {
    /* Set PA0 as output */
    __zeropage unsigned char pa_state;
    pa_state = 0;

    while (1) {
        pa_state = pa_state ^ 0x01;

        /* Write to Port A (memory-mapped I/O) */
        asm("LDAA pa_state");
        asm("STAA $1000");

        delay();
    }
}
