/*
 * aldl_reader.ino — ALDL Data Stream Reader for Arduino
 * ======================================================
 * Reads Mode 1 data stream from VY V6 Delco PCM over ALDL at 8192 baud.
 * Displays live engine parameters on Serial Monitor.
 *
 * Hardware:
 *   - Arduino Mega 2560 (uses Serial1 for ALDL, Serial for debug)
 *   - MAX232 or FTDI level shifter (ECU is 12V ALDL, Arduino is 5V TTL)
 *   - Connection: Arduino Serial1 TX → level shifter → ALDL pin A (data)
 *   - Protection: 10k resistor in series with RX line
 *
 * Protocol sourced from:
 *   - OSE Flash Tool (VL400) decompilation
 *   - pcmhacking.net community documentation
 *   - kernel_uploader.py POC protocol constants
 *
 * Pin Connections (Mega):
 *   Pin 19 (RX1) ← ALDL data (via level shifter)
 *   Pin 18 (TX1) → ALDL data (via level shifter)
 *
 * ALDL Connector (12-pin GM):
 *   Pin A = Data (ALDL serial)
 *   Pin B = Ground
 *   Pin F = +12V (battery)
 *   Pin M = Ground (additional)
 *
 * Author: KingAustraliaGG
 * Date: 2026-02-15
 */

#include "../shared/aldl_protocol.h"

/* ========================================================================
 * Configuration
 * ======================================================================== */
#define ALDL_SERIAL     Serial1     /* Hardware UART for ALDL bus */
#define DEBUG_SERIAL    Serial      /* USB debug output */
#define DEBUG_BAUD      115200      /* Debug serial baud rate */

#define RX_BUFFER_SIZE  256         /* ALDL receive buffer */
#define SILENCE_MS      20          /* Bus silence threshold */
#define FRAME_TIMEOUT   3000        /* Frame receive timeout (ms) */
#define POLL_INTERVAL   500         /* Data stream poll interval (ms) */

/* ========================================================================
 * Globals
 * ======================================================================== */
uint8_t rxBuffer[RX_BUFFER_SIZE];
uint16_t rxIndex = 0;
uint32_t lastByteTime = 0;
uint32_t lastPollTime = 0;
bool chatterDisabled = false;

/* ========================================================================
 * ALDL Frame Transmission
 * ======================================================================== */

/**
 * Wait for bus silence before transmitting.
 * From OSE ALDLFunctions.cs DetectSilence().
 */
bool detectSilence(uint16_t silence_ms, uint16_t timeout_ms) {
    uint32_t start = millis();
    uint32_t lastByte = millis();

    while ((millis() - start) < timeout_ms) {
        if (ALDL_SERIAL.available()) {
            while (ALDL_SERIAL.available()) {
                ALDL_SERIAL.read();  /* Drain bus */
            }
            lastByte = millis();
        } else if ((millis() - lastByte) >= silence_ms) {
            return true;
        }
        delayMicroseconds(100);
    }
    return false;
}

/**
 * Send an ALDL frame and skip echo bytes.
 * From OSE ALDLFunctions.cs ALDLTxFrame().
 */
bool txFrame(const uint8_t *frame, uint8_t frameLen) {
    if (!detectSilence(SILENCE_MS, 500)) {
        DEBUG_SERIAL.println(F("! Bus congestion"));
        return false;
    }

    /* Calculate TX byte count: length_byte - 82 */
    uint8_t txCount = frame[1] - 82;
    if (txCount > frameLen) txCount = frameLen;

    /* Flush input and send */
    while (ALDL_SERIAL.available()) ALDL_SERIAL.read();
    ALDL_SERIAL.write(frame, txCount);
    ALDL_SERIAL.flush();

    /* Skip echo bytes (most ALDL cables echo TX) */
    uint32_t echoDeadline = millis() + 200;
    uint8_t echoCount = 0;
    while (echoCount < txCount && millis() < echoDeadline) {
        if (ALDL_SERIAL.available()) {
            ALDL_SERIAL.read();
            echoCount++;
        }
    }

    return true;
}

/**
 * Receive ALDL response frame.
 * Collects bytes until bus goes quiet (frame boundary).
 */
uint16_t rxFrame(uint8_t *buffer, uint16_t bufSize, uint16_t timeout_ms) {
    uint16_t idx = 0;
    uint32_t start = millis();
    uint32_t lastRx = millis();

    while ((millis() - start) < timeout_ms && idx < bufSize) {
        if (ALDL_SERIAL.available()) {
            buffer[idx++] = ALDL_SERIAL.read();
            lastRx = millis();
        } else if (idx > 0 && (millis() - lastRx) > 50) {
            break;  /* Bus quiet with data = frame complete */
        }
        delayMicroseconds(100);
    }
    return idx;
}

/**
 * Send a simple ALDL command and receive response.
 */
uint16_t sendCommand(uint8_t deviceId, uint8_t mode,
                     uint8_t *respBuf, uint16_t respSize) {
    uint8_t frame[4];
    frame[0] = deviceId;
    frame[1] = ALDL_SIMPLE_LENGTH;
    frame[2] = mode;
    frame[3] = aldl_checksum(frame, 3);

    if (!txFrame(frame, 4)) return 0;
    return rxFrame(respBuf, respSize, FRAME_TIMEOUT);
}

/* ========================================================================
 * Mode 1 Data Stream Request
 * ======================================================================== */

/**
 * Request Mode 1 data stream.
 * TX: [DeviceID, 0x57, 0x01, 0x00, Checksum]
 */
uint16_t requestMode1(uint8_t *respBuf, uint16_t respSize) {
    uint8_t frame[5];
    frame[0] = DEVICE_PCM;
    frame[1] = 0x57;           /* Length = 85 + 2 */
    frame[2] = MODE_1;
    frame[3] = 0x00;           /* Message number (all) */
    frame[4] = aldl_checksum(frame, 4);

    if (!txFrame(frame, 5)) return 0;
    return rxFrame(respBuf, respSize, FRAME_TIMEOUT);
}

/* ========================================================================
 * Chatter Control
 * ======================================================================== */

/**
 * Disable chatter for a module (Mode 8).
 * From OSE ALDLChatterHandler().
 */
bool disableChatter(uint8_t deviceId) {
    uint8_t resp[32];
    for (uint8_t attempt = 0; attempt < 5; attempt++) {
        uint16_t len = sendCommand(deviceId, MODE_8, resp, sizeof(resp));
        if (len >= 3) {
            /* Check for echo of our Mode 8 command */
            for (uint16_t i = 0; i < len - 2; i++) {
                if (resp[i] == deviceId &&
                    resp[i+1] == ALDL_SIMPLE_LENGTH &&
                    resp[i+2] == MODE_8) {
                    DEBUG_SERIAL.print(F("Chatter disabled: 0x"));
                    DEBUG_SERIAL.println(deviceId, HEX);
                    return true;
                }
            }
        }
        delay(100);
    }
    DEBUG_SERIAL.print(F("! Chatter disable failed: 0x"));
    DEBUG_SERIAL.println(deviceId, HEX);
    return false;
}

/**
 * Re-enable chatter (Mode 9).
 */
bool enableChatter(uint8_t deviceId) {
    uint8_t resp[32];
    uint16_t len = sendCommand(deviceId, MODE_9, resp, sizeof(resp));
    return (len > 0);
}

/* ========================================================================
 * Data Display
 * ======================================================================== */

/**
 * Parse and display Mode 1 data stream response.
 * Offsets are approximate — need cross-reference with XDF definitions.
 */
void displayDataStream(const uint8_t *data, uint16_t len) {
    if (len < 20) {
        DEBUG_SERIAL.println(F("  Response too short"));
        return;
    }

    /* Skip header (device_id, length, mode) = 3 bytes */
    const uint8_t *payload = data + 3;
    uint16_t payloadLen = len - 3;

    if (payloadLen < 0x20) {
        DEBUG_SERIAL.println(F("  Payload too short for parsing"));
        /* Still dump raw hex */
        DEBUG_SERIAL.print(F("  RAW: "));
        for (uint16_t i = 0; i < len && i < 64; i++) {
            if (data[i] < 0x10) DEBUG_SERIAL.print('0');
            DEBUG_SERIAL.print(data[i], HEX);
            DEBUG_SERIAL.print(' ');
        }
        DEBUG_SERIAL.println();
        return;
    }

    /* RPM from period counter (approximate offsets) */
    uint16_t rpmPeriod = ((uint16_t)payload[0x02] << 8) | payload[0x03];
    uint16_t rpm = 0;
    if (rpmPeriod > 0) {
        rpm = (uint16_t)(120000000UL / ((uint32_t)rpmPeriod * 3));
    }

    /* Other parameters (approximate) */
    uint8_t coolantRaw = payload[0x05];
    float coolantC = coolantRaw * 0.75 - 40.0;

    uint8_t tpsRaw = payload[0x08];
    float tpsPct = tpsRaw / 255.0 * 100.0;

    uint8_t battRaw = payload[0x10];
    float battV = battRaw / 10.0;

    /* Display */
    DEBUG_SERIAL.println(F("--- Data Stream ---"));
    DEBUG_SERIAL.print(F("  RPM: "));
    DEBUG_SERIAL.print(rpm);
    DEBUG_SERIAL.print(F("    TPS: "));
    DEBUG_SERIAL.print(tpsPct, 1);
    DEBUG_SERIAL.println(F("%"));
    DEBUG_SERIAL.print(F("  CLT: "));
    DEBUG_SERIAL.print(coolantC, 1);
    DEBUG_SERIAL.print(F("C   BAT: "));
    DEBUG_SERIAL.print(battV, 1);
    DEBUG_SERIAL.println(F("V"));
    DEBUG_SERIAL.print(F("  Bytes: "));
    DEBUG_SERIAL.println(len);
}

/**
 * Dump raw hex bytes to Serial Monitor.
 */
void hexDump(const uint8_t *data, uint16_t len) {
    for (uint16_t i = 0; i < len; i++) {
        if (i > 0 && (i % 16) == 0) DEBUG_SERIAL.println();
        if (data[i] < 0x10) DEBUG_SERIAL.print('0');
        DEBUG_SERIAL.print(data[i], HEX);
        DEBUG_SERIAL.print(' ');
    }
    DEBUG_SERIAL.println();
}

/* ========================================================================
 * Setup & Main Loop
 * ======================================================================== */

void setup() {
    /* Debug serial (USB) */
    DEBUG_SERIAL.begin(DEBUG_BAUD);
    while (!DEBUG_SERIAL) { ; }

    DEBUG_SERIAL.println(F("========================================"));
    DEBUG_SERIAL.println(F("  KingAI ALDL Reader v0.1"));
    DEBUG_SERIAL.println(F("  Target: VY V6 Delco 09356445"));
    DEBUG_SERIAL.println(F("  Protocol: ALDL 8192 baud"));
    DEBUG_SERIAL.println(F("========================================"));

    /* ALDL serial (8192 baud, 8N1) */
    ALDL_SERIAL.begin(ALDL_BAUD_FAST, ALDL_SERIAL_CONFIG);

    DEBUG_SERIAL.println(F("ALDL port open. Waiting for ECU..."));
    DEBUG_SERIAL.println(F("Commands: 'd' = disable chatter, "
                           "'e' = enable chatter, 'r' = raw dump"));
    DEBUG_SERIAL.println();

    delay(500);

    /* Disable chatter for cleaner bus */
    DEBUG_SERIAL.println(F("Disabling chatter..."));
    disableChatter(DEVICE_BCM);
    disableChatter(DEVICE_PCM);
    chatterDisabled = true;

    lastPollTime = millis();
}

void loop() {
    /* Check for user commands via USB Serial */
    if (DEBUG_SERIAL.available()) {
        char cmd = DEBUG_SERIAL.read();
        switch (cmd) {
            case 'd':
                disableChatter(DEVICE_BCM);
                disableChatter(DEVICE_PCM);
                chatterDisabled = true;
                break;
            case 'e':
                enableChatter(DEVICE_BCM);
                enableChatter(DEVICE_PCM);
                chatterDisabled = false;
                break;
            case 'r': {
                /* Raw hex dump of next response */
                DEBUG_SERIAL.println(F("Requesting raw Mode 1..."));
                uint16_t len = requestMode1(rxBuffer, RX_BUFFER_SIZE);
                if (len > 0) {
                    DEBUG_SERIAL.print(F("Raw ("));
                    DEBUG_SERIAL.print(len);
                    DEBUG_SERIAL.println(F(" bytes):"));
                    hexDump(rxBuffer, len);
                } else {
                    DEBUG_SERIAL.println(F("No response"));
                }
                break;
            }
            case 'h':
                DEBUG_SERIAL.println(F("Commands:"));
                DEBUG_SERIAL.println(F("  d = disable chatter"));
                DEBUG_SERIAL.println(F("  e = enable chatter"));
                DEBUG_SERIAL.println(F("  r = raw hex dump"));
                DEBUG_SERIAL.println(F("  h = this help"));
                break;
        }
    }

    /* Periodic Mode 1 data stream poll */
    if (millis() - lastPollTime >= POLL_INTERVAL) {
        lastPollTime = millis();

        uint16_t len = requestMode1(rxBuffer, RX_BUFFER_SIZE);
        if (len > 0) {
            displayDataStream(rxBuffer, len);
        } else {
            DEBUG_SERIAL.print('.');  /* No response indicator */
        }
    }
}
