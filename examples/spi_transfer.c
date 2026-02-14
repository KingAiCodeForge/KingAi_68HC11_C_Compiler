/**
 * spi_transfer.c — SPI master transfer for 68HC11
 * ════════════════════════════════════════════════
 * Sends and receives bytes over the SPI bus in master mode.
 * The HC11 SPI uses Port D: PD2=MISO, PD3=MOSI, PD4=SCK, PD5=/SS.
 *
 * Typical automotive use: Reading external EEPROM (93C46, 25LC256),
 * communicating with external DAC/ADC, or dashpot controllers.
 *
 * HC11 SPI registers:
 *   SPCR ($1028): SPE=1 (enable), MSTR=1 (master), CPOL/CPHA=0/0 (mode 0),
 *                 SPR1:SPR0=0:1 (E/4 clock) → value = $54
 *   SPSR ($1029): SPIF (bit 7) = transfer complete flag
 *   SPDR ($102A): Data register — write to transmit, read to receive
 *   DDRD ($1009): PD3=out(MOSI), PD4=out(SCK), PD5=out(/SS), PD2=in(MISO)
 *
 * Reference: M68HC11 Reference Manual ch.8 (SPI)
 *            MC68HC11F1 Technical Data section 8
 *
 * Compile: python hc11kit.py compile examples/spi_transfer.c -o spi_transfer.bin
 *
 * Demonstrates: SPI master mode, flag polling, data exchange.
 * Full pipeline: C → ASM → binary → S19
 */

#define DDRD_ADDR   0x1009
#define PORTD_ADDR  0x1008
#define SPCR_ADDR   0x1028
#define SPSR_ADDR   0x1029
#define SPDR_ADDR   0x102A

/* SPCR: SPE=1, MSTR=1, CPOL=0, CPHA=1, SPR=01 → $54 + CPHA → $55 */
/* Mode 0 (CPOL=0, CPHA=0) for most EEPROMs: $54 */
#define SPCR_MASTER_MODE0  0x54

/* DDRD: PD3(MOSI)=out, PD4(SCK)=out, PD5(/SS)=out = bits 5,4,3 = $38 */
#define DDRD_SPI_MASTER    0x38

/* SPSR: SPIF bit 7 */
#define SPIF_BIT    0x80

/* /SS is PD5 (bit 5) */
#define SS_BIT      0x20

void spi_init() {
    volatile unsigned char *ddrd = (volatile unsigned char *)DDRD_ADDR;
    volatile unsigned char *spcr = (volatile unsigned char *)SPCR_ADDR;
    volatile unsigned char *portd = (volatile unsigned char *)PORTD_ADDR;

    /* Set MOSI, SCK, /SS as outputs */
    *ddrd = DDRD_SPI_MASTER;

    /* Deselect slave (SS high) */
    *portd = *portd | SS_BIT;

    /* Enable SPI, master mode, clock = E/4 */
    *spcr = SPCR_MASTER_MODE0;
}

unsigned char spi_transfer(unsigned char tx_byte) {
    volatile unsigned char *spsr = (volatile unsigned char *)SPSR_ADDR;
    volatile unsigned char *spdr = (volatile unsigned char *)SPDR_ADDR;
    unsigned char status;

    /* Write byte to transmit — this starts the SPI clock */
    *spdr = tx_byte;

    /* Wait for SPIF (transfer complete) */
    status = 0;
    while ((status & SPIF_BIT) == 0) {
        status = *spsr;
    }

    /* Read received byte (also clears SPIF) */
    return *spdr;
}

void spi_select() {
    volatile unsigned char *portd = (volatile unsigned char *)PORTD_ADDR;
    /* Assert /SS low to select slave */
    *portd = *portd & 0xDF;
}

void spi_deselect() {
    volatile unsigned char *portd = (volatile unsigned char *)PORTD_ADDR;
    /* Deassert /SS high */
    *portd = *portd | SS_BIT;
}

void main() {
    unsigned char rx;

    spi_init();

    while (1) {
        spi_select();

        /* Send command byte, get response */
        spi_transfer(0x03);   /* Read command (typical EEPROM) */
        spi_transfer(0x00);   /* Address high */
        rx = spi_transfer(0x00);  /* Read data byte */

        spi_deselect();

        asm("WAI");
    }
}
