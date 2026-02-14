/*
 * aldl_hello.c — POC: Send ALDL response from custom HC11 patch
 *
 * PURPOSE:
 *   Demonstrate the C compiler producing code that communicates
 *   over the ALDL diagnostic port via the HC11's SCI peripheral.
 *   This is the minimum viable "proof it runs" test case.
 *
 * WHAT IT DOES:
 *   Enables the SCI transmitter and sends a short byte sequence
 *   out the ALDL pin. A scan tool or serial terminal at 8192 baud
 *   will receive the bytes.
 *
 * HOW TO USE:
 *   python hc11kit.py compile examples/aldl_hello.c -o hello.bin --target vy_v6
 *   python hc11kit.py patch stock.bin hello.bin --at 0x5D00 --hook 0x101E1:3
 *
 * LIMITATIONS:
 *   - The compiler doesn't support string literals or arrays yet,
 *     so we send individual bytes via a helper function.
 *   - FCC/FCB string data requires the assembler directly (see
 *     aldl_hello_world.asm for the pure-assembly version).
 *
 * SAFETY:
 *   Only touches SCI registers. No spark, fuel, or timing changes.
 *   Safe for bench testing with key-on engine-off (KOEO).
 */

/* HC11 SCI registers */
#define SCCR2   0x102D
#define SCSR    0x102E
#define SCDR    0x102F

/* SCCR2 bits */
#define TE      0x08

/* SCSR bits */
#define TDRE    0x80

/*
 * sci_tx_byte — transmit one byte over SCI (ALDL)
 *
 * Waits for TDRE (transmit buffer empty), then writes the byte.
 * Blocking — spins until the previous byte has been sent.
 */
void sci_tx_byte(unsigned char b) {
    /* Wait for transmit buffer empty */
    while ((*(volatile unsigned char *)SCSR & TDRE) == 0) {
        /* spin */
    }
    /* Write byte to SCI data register */
    *(volatile unsigned char *)SCDR = b;
}

/*
 * aldl_hello — send "HI" + CR/LF over ALDL
 *
 * Called once at startup via JSR hook. Sends a short recognisable
 * sequence that a terminal or scan tool can detect.
 *
 * Why "HI" not "HELLO WORLD":
 *   - Without string/array support, each char is a separate call
 *   - "HI\r\n" = 4 bytes, proves the concept with minimum code size
 *   - The assembler version (aldl_hello_world.asm) does the full string
 */
void main() {
    /* Enable SCI transmitter (stock OS may only have RX enabled) */
    volatile unsigned char *sccr2;
    unsigned char val;
    sccr2 = (volatile unsigned char *)SCCR2;
    val = *sccr2;
    val = val | TE;
    *sccr2 = val;

    /* Send "HI\r\n" */
    sci_tx_byte(0x48);      /* 'H' */
    sci_tx_byte(0x49);      /* 'I' */
    sci_tx_byte(0x0D);      /* CR  */
    sci_tx_byte(0x0A);      /* LF  */
}
