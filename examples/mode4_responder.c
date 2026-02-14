/*
 * mode4_responder.c — Respond to ALDL Mode 4 commands via SCI
 *
 * PURPOSE:
 *   Demonstrates a minimal Mode 4 actuator test handler that listens
 *   for ALDL commands and controls a digital output (fan relay).
 *   This is a real-world ECU patch pattern — intercept Mode 4 requests
 *   and drive outputs based on the control bytes.
 *
 * WHAT IT DOES:
 *   1. Polls SCDR for incoming ALDL bytes
 *   2. Watches for Mode 4 header (0xF7 target, 0x04 mode)
 *   3. If byte 1 bit 0 is set (fan enable), drives PORTB bit 0 high
 *   4. Otherwise drives it low
 *
 * This is a simplified version of what the stock OS does in its SCI ISR
 * at $29D3 when it receives Mode 4 frames.
 *
 * HARDWARE:
 *   PORTB ($1004) bit 0 = cooling fan relay on VY V6
 *   ALDL = SCI at 8192 baud (stock OS configures this)
 *
 * Compile: python hc11kit.py compile examples/mode4_responder.c -o mode4.bin --target vy_v6
 */

#define SCSR    0x102E
#define SCDR    0x102F
#define PORTB   0x1004
#define TDRE    0x80
#define RDRF    0x20

/*
 * sci_rx — receive one byte from SCI (blocking)
 * Returns the byte read from SCDR.
 */
unsigned char sci_rx() {
    /* Wait for Receive Data Register Full */
    while ((*(volatile unsigned char *)SCSR & RDRF) == 0) {
    }
    return *(volatile unsigned char *)SCDR;
}

/*
 * sci_tx — transmit one byte over SCI
 */
void sci_tx(unsigned char b) {
    while ((*(volatile unsigned char *)SCSR & TDRE) == 0) {
    }
    *(volatile unsigned char *)SCDR = b;
}

/*
 * main — Mode 4 listener loop
 *
 * Watches for: [0xF7] [len] [0x04] [control_byte1] ...
 * Byte 1 bit 0 = fan relay: 1=ON, 0=OFF
 *
 * Sends back: [0xF7] [0x56] [0x04] [status] [checksum]
 * (Mode 4 echo with current port state)
 */
void handle_mode4() {
    unsigned char control;
    unsigned char fan_state;
    volatile unsigned char *portb = (volatile unsigned char *)PORTB;

    /* Read first control byte (discrete enables) */
    control = sci_rx();

    /* Bit 0 = fan relay control */
    if ((control & 0x01) != 0) {
        *portb = *portb | 0x01;
        fan_state = 1;
    } else {
        *portb = *portb & 0xFE;
        fan_state = 0;
    }

    /* Send Mode 4 acknowledgement */
    sci_tx(0xF7);           /* target echo */
    sci_tx(0x56);           /* length */
    sci_tx(0x04);           /* mode echo */
    sci_tx(fan_state);      /* status byte */
}

void main() {
    unsigned char target;
    unsigned char mode;

    while (1) {
        /* Wait for target byte */
        target = sci_rx();
        if (target == 0xF7) {
            /* Skip length byte */
            sci_rx();
            /* Read mode byte */
            mode = sci_rx();
            if (mode == 0x04) {
                handle_mode4();
            }
        }
    }
}
