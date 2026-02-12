/**
 * adc_read.c — ADC reading example for Delco 68HC11 PCM
 * ══════════════════════════════════════════════════════
 * Reads engine coolant temperature from ADC channel 0.
 * Sets Port A bit 1 if temp exceeds threshold.
 *
 * Compile: python hc11cc.py examples/adc_read.c -o adc_read.asm --target vy_v6
 */

#define PORTA   0x1000
#define ADCTL   0x1030
#define ADR1    0x1031
#define ADCTL_CCF  0x80

/* Zero-page variables for fast access */
__zeropage unsigned char coolant_temp;
__zeropage unsigned char threshold;

unsigned char read_adc(unsigned char channel) {
    unsigned char status;

    /* Start ADC conversion on selected channel */
    asm("LDAA channel");
    asm("STAA $1030");

    /* Wait for conversion complete (CCF bit 7) */
    status = 0;
    while (status == 0) {
        asm("LDAA $1030");
        asm("ANDA #$80");
        asm("STAA status");
    }

    /* Read result */
    asm("LDAA $1031");
    return 0;  /* result in A from asm */
}

void main() {
    threshold = 200;  /* ~95°C depending on sensor calibration */

    while (1) {
        coolant_temp = read_adc(0);

        if (coolant_temp > threshold) {
            /* Activate cooling fan relay (Port A bit 1) */
            asm("LDAA $1000");
            asm("ORAA #$02");
            asm("STAA $1000");
        } else {
            /* Deactivate cooling fan relay */
            asm("LDAA $1000");
            asm("ANDA #$FD");
            asm("STAA $1000");
        }

        /* Wait for next loop iteration */
        asm("WAI");
    }
}
