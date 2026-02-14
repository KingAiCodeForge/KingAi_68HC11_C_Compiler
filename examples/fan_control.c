/*
 * fan_control.c — Temperature-based cooling fan control
 *
 * PURPOSE:
 *   Replace the stock ECU fan logic with custom ON/OFF temperatures.
 *   Demonstrates reading the coolant temperature sensor via ADC and
 *   controlling a digital output based on thresholds.
 *
 * WHAT IT DOES:
 *   Reads coolant temp from ADC channel (PE0), compares against
 *   configurable on/off thresholds with hysteresis, and drives
 *   the fan relay on PORTB bit 0.
 *
 * THRESHOLDS:
 *   Fan ON  at 95°C (0x62 raw ADC value, depends on sensor curve)
 *   Fan OFF at 88°C (0x5A raw ADC value)
 *   The 7° hysteresis prevents rapid on/off cycling.
 *
 * Compile: python hc11kit.py compile examples/fan_control.c -o fan_ctrl.bin --target vy_v6
 */

/* HC11 ADC registers */
#define ADCTL   0x1030
#define ADR1    0x1031

/* ADCTL bits */
#define CCF     0x80
#define SCAN    0x20

/* HC11 PORTB */
#define PORTB   0x1004

/* Thresholds (raw ADC counts — adjust for your sensor's transfer function) */
#define FAN_ON_THRESHOLD    0x62
#define FAN_OFF_THRESHOLD   0x5A

unsigned char read_coolant_adc() {
    volatile unsigned char *adctl;
    volatile unsigned char *adr1;

    adctl = (volatile unsigned char *)ADCTL;
    adr1 = (volatile unsigned char *)ADR1;

    /* Start single conversion on channel 0 (PE0 = coolant sensor) */
    *adctl = 0x00;

    /* Wait for Conversion Complete Flag */
    while ((*adctl & CCF) == 0) {
    }

    /* Return result from ADR1 */
    return *adr1;
}

__zeropage unsigned char fan_on;

void software_delay() {
    unsigned char d1;
    unsigned char d2;
    d1 = 255;
    while (d1 > 0) {
        d2 = 255;
        while (d2 > 0) {
            d2--;
        }
        d1--;
    }
}

void fan_update() {
    volatile unsigned char *portb;
    unsigned char temp_raw;

    portb = (volatile unsigned char *)PORTB;
    temp_raw = read_coolant_adc();

    if (fan_on == 0) {
        /* Fan is currently OFF — turn ON if above high threshold */
        if (temp_raw >= FAN_ON_THRESHOLD) {
            *portb = *portb | 0x01;
            fan_on = 1;
        }
    } else {
        /* Fan is currently ON — turn OFF if below low threshold */
        if (temp_raw < FAN_OFF_THRESHOLD) {
            *portb = *portb & 0xFE;
            fan_on = 0;
        }
    }
}

void main() {
    fan_on = 0;

    while (1) {
        fan_update();
        software_delay();
    }
}
