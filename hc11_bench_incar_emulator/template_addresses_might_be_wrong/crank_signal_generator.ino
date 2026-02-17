/*
 * VY V6 Crank Signal Generator — Arduino Template
 * ==================================================
 *
 * Generates 3X DES (Dual Edge Sensing) and 18X CKP (Crankshaft Position)
 * square wave signals for bench testing a VY V6 L36 Delco PCM.
 *
 * ⚠ WARNING: PIN ASSIGNMENTS ARE PLACEHOLDERS
 *    The Arduino output pins are arbitrary choices. The PCM input pins
 *    for 3X and 18X signals must be verified against the actual PCM
 *    connector pinout (C2 connector, sensor inputs) before connecting.
 *
 *    Additionally, the PCM expects reluctor-style signals through its
 *    ICM (Ignition Control Module) interface. Direct Arduino 5V square
 *    waves may need signal conditioning (voltage divider, buffer, or
 *    driver circuit) to match what the PCM expects.
 *
 * Signal specifications (VY V6 L36 3.8L):
 *   3X reference: 3 pulses per crankshaft revolution (~120° apart)
 *   18X CKP:      18 pulses per crankshaft revolution (~20° apart)
 *   Both are square waves when coming from the ICM to the PCM.
 *
 * Frequency formulas:
 *   freq_Hz = (RPM / 60) * pulses_per_rev
 *
 *   Example at 800 RPM idle:
 *     3X  = (800/60) * 3  = 40.0 Hz   (25.0 ms period)
 *     18X = (800/60) * 18 = 240.0 Hz  (4.167 ms period)
 *
 * Hardware:
 *   - Arduino Mega 2560 (recommended — multiple hardware timers)
 *   - Or Arduino Uno (limited to 2 timer outputs)
 *   - Signal conditioning circuit between Arduino and PCM
 *
 * References:
 *   - Speeduino Ardu-Stim: https://github.com/speeduino/Ardu-Stim
 *   - ESP32-CKP-Signal-Generator: https://github.com/LucasStraps/ESP32-CKP-Signal-Generator
 *   - Dev plan: ignore/dev_research_plan_for_bench_emulator.md §3B
 *
 * Usage:
 *   1. Upload to Arduino
 *   2. Open Serial Monitor at 115200 baud
 *   3. Send RPM value (e.g. "800") to set target RPM
 *   4. Signals appear on output pins
 *
 * TEMPLATE — adapt pin assignments and signal conditioning for your setup.
 */

// =============================================================================
//  PIN ASSIGNMENTS — ⚠ PLACEHOLDERS
//  Change these to match your wiring. Verify PCM side before connecting.
// =============================================================================
#define PIN_3X_OUTPUT    9    // ⚠ PLACEHOLDER — Timer1 OC1A output (Arduino Mega)
#define PIN_18X_OUTPUT   10   // ⚠ PLACEHOLDER — Timer1 OC1B output (Arduino Mega)
#define PIN_SYNC_LED     13   // On-board LED — blinks once per "revolution"
#define PIN_RPM_POT      A0   // Optional: potentiometer for RPM control

// =============================================================================
//  SIGNAL PARAMETERS
// =============================================================================
#define PULSES_3X_PER_REV    3
#define PULSES_18X_PER_REV   18
#define MIN_RPM              200
#define MAX_RPM              6500
#define DEFAULT_RPM          800
#define DUTY_CYCLE_PCT       50    // 50% duty cycle square wave

// =============================================================================
//  STATE
// =============================================================================
volatile unsigned int target_rpm = DEFAULT_RPM;
volatile unsigned long pulse_count_3x = 0;
volatile unsigned long pulse_count_18x = 0;

// Timer periods in microseconds
unsigned long period_3x_us = 0;
unsigned long period_18x_us = 0;

// For software-generated signals (if not using hardware timers)
unsigned long last_3x_toggle_us = 0;
unsigned long last_18x_toggle_us = 0;
bool state_3x = false;
bool state_18x = false;

// Revolution tracking
unsigned long rev_count = 0;
unsigned int pulse_in_rev_3x = 0;
unsigned int pulse_in_rev_18x = 0;

// Serial input buffer
char serial_buf[16];
int serial_idx = 0;

// =============================================================================
//  SETUP
// =============================================================================
void setup() {
    // Pin modes
    pinMode(PIN_3X_OUTPUT, OUTPUT);
    pinMode(PIN_18X_OUTPUT, OUTPUT);
    pinMode(PIN_SYNC_LED, OUTPUT);

    digitalWrite(PIN_3X_OUTPUT, LOW);
    digitalWrite(PIN_18X_OUTPUT, LOW);

    // Serial for RPM control + monitoring
    Serial.begin(115200);
    Serial.println(F(""));
    Serial.println(F("================================================="));
    Serial.println(F("  VY V6 Crank Signal Generator — TEMPLATE"));
    Serial.println(F("  !! PIN ASSIGNMENTS ARE PLACEHOLDERS !!"));
    Serial.println(F("  Verify PCM pinout before connecting!"));
    Serial.println(F("================================================="));
    Serial.println(F(""));
    Serial.println(F("Commands:"));
    Serial.println(F("  <number>  — Set target RPM (200-6500)"));
    Serial.println(F("  s         — Print status"));
    Serial.println(F("  h         — Print frequency table"));
    Serial.println(F(""));

    // Calculate initial periods
    update_periods(DEFAULT_RPM);

    Serial.print(F("Starting at "));
    Serial.print(DEFAULT_RPM);
    Serial.println(F(" RPM"));
    print_frequencies();
}

// =============================================================================
//  PERIOD CALCULATION
// =============================================================================
void update_periods(unsigned int rpm) {
    if (rpm < MIN_RPM) rpm = MIN_RPM;
    if (rpm > MAX_RPM) rpm = MAX_RPM;

    target_rpm = rpm;

    // freq = (RPM / 60) * pulses_per_rev
    // period_us = 1,000,000 / freq
    // Simplified: period_us = 60,000,000 / (RPM * pulses_per_rev)

    // Half-period for toggle (50% duty cycle)
    period_3x_us  = 60000000UL / ((unsigned long)rpm * PULSES_3X_PER_REV * 2);
    period_18x_us = 60000000UL / ((unsigned long)rpm * PULSES_18X_PER_REV * 2);
}

void print_frequencies() {
    float freq_3x  = ((float)target_rpm / 60.0) * PULSES_3X_PER_REV;
    float freq_18x = ((float)target_rpm / 60.0) * PULSES_18X_PER_REV;
    float period_3x_ms  = 1000.0 / freq_3x;
    float period_18x_ms = 1000.0 / freq_18x;

    Serial.print(F("  RPM="));
    Serial.print(target_rpm);
    Serial.print(F("  3X="));
    Serial.print(freq_3x, 1);
    Serial.print(F(" Hz ("));
    Serial.print(period_3x_ms, 2);
    Serial.print(F(" ms)  18X="));
    Serial.print(freq_18x, 1);
    Serial.print(F(" Hz ("));
    Serial.print(period_18x_ms, 3);
    Serial.println(F(" ms)"));
}

void print_freq_table() {
    Serial.println(F(""));
    Serial.println(F("  RPM  |  3X Hz  | 3X ms   | 18X Hz  | 18X ms"));
    Serial.println(F("  -----|---------|---------|---------|--------"));

    unsigned int rpms[] = {200, 400, 600, 800, 1000, 1500, 2000, 3000, 4000, 5000, 6000, 6500};
    for (int i = 0; i < 12; i++) {
        float f3 = ((float)rpms[i] / 60.0) * 3.0;
        float f18 = ((float)rpms[i] / 60.0) * 18.0;
        char line[80];
        snprintf(line, sizeof(line), "  %4u | %6.1f  | %6.2f  | %6.1f  | %6.3f",
                 rpms[i], f3, 1000.0/f3, f18, 1000.0/f18);
        Serial.println(line);
    }
    Serial.println(F(""));
}

// =============================================================================
//  MAIN LOOP — Software-generated signals
//  (For production use, switch to hardware timer interrupts for jitter-free output)
// =============================================================================
void loop() {
    unsigned long now_us = micros();

    // --- 3X signal generation ---
    if (now_us - last_3x_toggle_us >= period_3x_us) {
        last_3x_toggle_us = now_us;
        state_3x = !state_3x;
        digitalWrite(PIN_3X_OUTPUT, state_3x ? HIGH : LOW);

        if (state_3x) {
            pulse_count_3x++;
            pulse_in_rev_3x++;

            // Track revolutions (3 pulses = 1 revolution)
            if (pulse_in_rev_3x >= PULSES_3X_PER_REV) {
                pulse_in_rev_3x = 0;
                rev_count++;
                // Blink LED once per revolution
                digitalWrite(PIN_SYNC_LED, !digitalRead(PIN_SYNC_LED));
            }
        }
    }

    // --- 18X signal generation ---
    if (now_us - last_18x_toggle_us >= period_18x_us) {
        last_18x_toggle_us = now_us;
        state_18x = !state_18x;
        digitalWrite(PIN_18X_OUTPUT, state_18x ? HIGH : LOW);

        if (state_18x) {
            pulse_count_18x++;
            pulse_in_rev_18x++;
            if (pulse_in_rev_18x >= PULSES_18X_PER_REV) {
                pulse_in_rev_18x = 0;
            }
        }
    }

    // --- Serial command processing ---
    while (Serial.available()) {
        char c = Serial.read();

        if (c == '\n' || c == '\r') {
            if (serial_idx > 0) {
                serial_buf[serial_idx] = '\0';

                if (serial_buf[0] == 's' || serial_buf[0] == 'S') {
                    // Status
                    Serial.print(F("Status: RPM="));
                    Serial.print(target_rpm);
                    Serial.print(F(" revs="));
                    Serial.print(rev_count);
                    Serial.print(F(" 3X_pulses="));
                    Serial.print(pulse_count_3x);
                    Serial.print(F(" 18X_pulses="));
                    Serial.println(pulse_count_18x);
                    print_frequencies();
                } else if (serial_buf[0] == 'h' || serial_buf[0] == 'H') {
                    print_freq_table();
                } else {
                    // Try to parse as RPM value
                    int new_rpm = atoi(serial_buf);
                    if (new_rpm >= MIN_RPM && new_rpm <= MAX_RPM) {
                        update_periods(new_rpm);
                        Serial.print(F("RPM set to "));
                        Serial.println(target_rpm);
                        print_frequencies();
                    } else {
                        Serial.print(F("Invalid RPM: "));
                        Serial.print(serial_buf);
                        Serial.print(F(" (range: "));
                        Serial.print(MIN_RPM);
                        Serial.print(F("-"));
                        Serial.print(MAX_RPM);
                        Serial.println(F(")"));
                    }
                }
                serial_idx = 0;
            }
        } else if (serial_idx < (int)(sizeof(serial_buf) - 1)) {
            serial_buf[serial_idx++] = c;
        }
    }

    // --- Optional: Read RPM from potentiometer ---
    // Uncomment to use analog pot for RPM control instead of serial:
    /*
    static unsigned long last_pot_read = 0;
    if (now_us - last_pot_read > 100000) {  // Read every 100ms
        last_pot_read = now_us;
        int pot_val = analogRead(PIN_RPM_POT);
        unsigned int pot_rpm = map(pot_val, 0, 1023, MIN_RPM, MAX_RPM);
        if (abs((int)pot_rpm - (int)target_rpm) > 20) {
            update_periods(pot_rpm);
        }
    }
    */
}

/*
 * NOTES FOR HARDWARE TIMER VERSION (recommended for production):
 *
 * Using Timer1 on Arduino Mega for jitter-free output:
 *
 * Timer1 in CTC (Clear Timer on Compare) mode:
 *   - OCR1A controls 3X frequency on pin 11 (OC1A)
 *   - OCR1B controls 18X frequency on pin 12 (OC1B)
 *     (But 18X = 6× faster than 3X, so phase relationship needs ISR logic)
 *
 * Better approach: Use Timer1 for 18X (higher frequency, needs precision),
 * and count 18X pulses to derive 3X (every 6th pulse = one 3X edge).
 *
 * For ESP32: Use LEDC/MCPWM hardware timers — much more flexible.
 * See: https://github.com/LucasStraps/ESP32-CKP-Signal-Generator
 *
 * ⚠ SIGNAL CONDITIONING:
 *   Arduino outputs 0-5V TTL. The PCM's crank inputs may expect:
 *   - Reluctor-level signals (~0.5-50V AC from variable reluctance sensor)
 *   - Or ICM-processed 0-12V square waves
 *
 *   For bench testing, the ICM normally processes the raw reluctor signal
 *   and sends the PCM clean 0V/5V or 0V/12V square waves. So Arduino 5V
 *   square waves may work directly IF connected to the ICM output side
 *   of the PCM input, not the raw sensor input.
 *
 *   Verify what voltage levels the PCM expects on its 3X/18X input pins!
 */
