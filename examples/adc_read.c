/**
 * adc_read.c — ADC reading example for Delco 68HC11 PCM
 * ══════════════════════════════════════════════════════
 * Reads engine coolant temperature from ADC channel 0.
 * Sets Port A bit 1 if temp exceeds threshold.
 *
 * Compile: python hc11cc.py examples/adc_read.c -o adc_read.asm --target vy_v6
 *
 * Demonstrates: volatile I/O registers, polling loop, bit manipulation.
 * Full pipeline: C → ASM → binary → S19
 */

#define PORTA_ADDR  0x1000
#define ADCTL_ADDR  0x1030
#define ADR1_ADDR   0x1031
#define CCF_MASK    0x80

/* Zero-page variables for fast access */
__zeropage unsigned char coolant_temp;
__zeropage unsigned char threshold;

unsigned char read_adc(unsigned char channel) {
    volatile unsigned char *adctl = (volatile unsigned char *)ADCTL_ADDR;
    volatile unsigned char *adr1  = (volatile unsigned char *)ADR1_ADDR;
    unsigned char status;

    /* Start ADC conversion on selected channel */
    *adctl = channel;

    /* Wait for conversion complete (CCF bit 7) */
    status = 0;
    while (status == 0) {
        status = *adctl & CCF_MASK;
    }

    /* Read and return result */
    return *adr1;
}

void main() {
    volatile unsigned char *porta = (volatile unsigned char *)PORTA_ADDR;
    unsigned char pa_val;

    threshold = 200;  /* ~95C depending on sensor calibration */

    while (1) {
        coolant_temp = read_adc(0);

        pa_val = *porta;
        if (coolant_temp > threshold) {
            /* Activate cooling fan relay (Port A bit 1) */
            *porta = pa_val | 0x02;
        } else {
            /* Deactivate cooling fan relay */
            *porta = pa_val & 0xFD;
        }

        /* Wait for next loop iteration */
        asm("WAI");
    }
}
