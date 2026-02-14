/**
 * sci_serial.c — SCI (Serial) ALDL communication for Delco 68HC11 PCM
 * ════════════════════════════════════════════════════════════════════
 * Initializes the SCI at 8192 baud (GM ALDL protocol), then echoes
 * received bytes back to the scan tool.
 *
 * 8192 baud is the standard GM OBD-I ALDL data rate. The Delco PCM
 * uses a 4.194304 MHz crystal (2^22 Hz) giving 2.097152 MHz E-clock.
 * BAUD register $04: SCP1:SCP0=0:0 (÷1, 131.072k highest),
 *                    SCR2:SCR0=1:0:0 (÷16) → 131072/16 = 8192 exact.
 *
 * Reference: M68HC11 Reference Manual ch.9, mrmodule_ALDL_v1.pdf
 * Protocol:  8 data bits, no parity, 1 stop bit (8N1)
 *
 * Compile: python hc11kit.py compile examples/sci_serial.c -o sci_serial.bin
 *
 * Demonstrates: SCI register access, polling loops, function calls.
 * Full pipeline: C → ASM → binary → S19
 */

#define BAUD_ADDR   0x102B
#define SCCR1_ADDR  0x102C
#define SCCR2_ADDR  0x102D
#define SCSR_ADDR   0x102E
#define SCDR_ADDR   0x102F

#define TDRE_MASK   0x80
#define RDRF_MASK   0x20
#define TE_RE_BITS  0x0C

/* BAUD register value for 8192 baud at 4.194304 MHz crystal:
 * SCP1:SCP0 = 0:0 (prescaler ÷1 → 131.072 kBaud highest)
 * SCR2:SCR1:SCR0 = 1:0:0 (÷16 → 131072/16 = 8192 baud exact) */
#define BAUD_8192   0x04

void sci_init() {
    volatile unsigned char *baud  = (volatile unsigned char *)BAUD_ADDR;
    volatile unsigned char *sccr1 = (volatile unsigned char *)SCCR1_ADDR;
    volatile unsigned char *sccr2 = (volatile unsigned char *)SCCR2_ADDR;

    /* 8192 baud for GM ALDL protocol */
    *baud = BAUD_8192;

    /* 8N1 format, no wake, no parity */
    *sccr1 = 0x00;

    /* Enable transmitter and receiver, no interrupts */
    *sccr2 = TE_RE_BITS;
}

unsigned char sci_read() {
    volatile unsigned char *scsr = (volatile unsigned char *)SCSR_ADDR;
    volatile unsigned char *scdr = (volatile unsigned char *)SCDR_ADDR;

    /* Poll RDRF (bit 5) until a byte is received */
    while ((*scsr & RDRF_MASK) == 0) {
    }
    return *scdr;
}

void sci_write(unsigned char ch) {
    volatile unsigned char *scsr = (volatile unsigned char *)SCSR_ADDR;
    volatile unsigned char *scdr = (volatile unsigned char *)SCDR_ADDR;

    /* Poll TDRE (bit 7) until transmit buffer is empty */
    while ((*scsr & TDRE_MASK) == 0) {
    }
    *scdr = ch;
}

void main() {
    unsigned char rx;

    sci_init();

    /* ALDL echo loop: read a byte, send it back */
    while (1) {
        rx = sci_read();
        sci_write(rx);
    }
}
