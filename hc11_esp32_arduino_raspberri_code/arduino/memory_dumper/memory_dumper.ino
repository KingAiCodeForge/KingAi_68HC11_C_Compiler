/*
 * memory_dumper.ino — ECU Memory Read/Write via ALDL
 * ====================================================
 * Arduino Mega sketch that reads ECU RAM/EEPROM/Flash memory regions
 * via ALDL serial commands and dumps them to Serial Monitor in hex format.
 * Can also write bytes to RAM for testing.
 *
 * Uses Mode 1 for data stream reads and can attempt direct memory reads
 * via Mode 6 upload of a tiny read kernel to PCM RAM.
 *
 * Hardware: Arduino Mega 2560 + level shifter + ALDL connector
 * Protocol: OSE Flash Tool (VL400) + kernel_uploader.py
 *
 * Author: KingAustraliaGG
 * Date: 2026-02-15
 */

#include "../shared/aldl_protocol.h"

/* ========================================================================
 * Configuration
 * ======================================================================== */
#define ALDL_SERIAL     Serial1
#define DEBUG_SERIAL    Serial
#define DEBUG_BAUD      115200

#define RX_BUFFER_SIZE  512
#define CMD_BUFFER_SIZE 64
#define SILENCE_MS      20
#define FRAME_TIMEOUT   5000

/* ========================================================================
 * Memory Read Kernel — HC11 machine code
 * Uploaded to PCM RAM via Mode 6, reads memory and sends over ALDL.
 *
 * This kernel reads N bytes starting from a given address and sends
 * each byte over the SCI (ALDL TX). Parameters are passed in the
 * kernel data itself (address and count are patched before upload).
 *
 * Load address: $0300 (PCM RAM)
 *
 * Assembled bytes:
 *   LDAA #$55 / STAA $103A     ; Feed COP
 *   LDAA #$AA / STAA $103A
 *   LDX  #addr                 ; Load start address (patched)
 *   LDB  #count                ; Load byte count (patched)
 * loop:
 *   LDAA $102E / BITA #$80 / BEQ loop  ; Wait TDRE
 *   LDAA 0,X   / STAA $102F   ; Read mem[X] → SCI TX
 *   INX                       ; Next address
 *   DECB / BNE loop           ; Count down
 *   BRA start                 ; Loop forever (watchdog)
 * ======================================================================== */

/* Template — addr and count bytes are patched at runtime */
const uint8_t MEM_READ_KERNEL_TEMPLATE[] PROGMEM = {
    /* Feed COP watchdog */
    0x86, 0x55,             /* LDAA #$55 */
    0xB7, 0x10, 0x3A,       /* STAA $103A */
    0x86, 0xAA,             /* LDAA #$AA */
    0xB7, 0x10, 0x3A,       /* STAA $103A */

    /* Load parameters (patched at upload time) */
    0xCE, 0x00, 0x00,       /* LDX #$0000   [bytes 10-11: start address] */
    0xC6, 0x10,             /* LDAB #$10    [byte 13: byte count] */

    /* Read loop: wait for SCI TX ready */
    0xB6, 0x10, 0x2E,       /* LDAA $102E  (SCSR) */
    0x85, 0x80,             /* BITA #$80   (TDRE) */
    0x27, 0xF9,             /* BEQ -7      (wait loop) */

    /* Read memory at [X] and transmit */
    0xA6, 0x00,             /* LDAA 0,X    (read byte at address) */
    0xB7, 0x10, 0x2F,       /* STAA $102F  (write to SCI TX) */

    /* Increment address and decrement count */
    0x08,                   /* INX */
    0x5A,                   /* DECB */
    0x26, 0xEF,             /* BNE -17     (back to read loop) */

    /* Feed COP and loop forever */
    0x86, 0x55,             /* LDAA #$55 */
    0xB7, 0x10, 0x3A,       /* STAA $103A */
    0x86, 0xAA,             /* LDAA #$AA */
    0xB7, 0x10, 0x3A,       /* STAA $103A */
    0x20, 0xD4,             /* BRA start (-44) */
};

#define KERNEL_ADDR_OFFSET  10  /* Offset of address bytes in template */
#define KERNEL_COUNT_OFFSET 13  /* Offset of count byte in template */

/* ========================================================================
 * Low-Level ALDL I/O (same as aldl_reader.ino)
 * ======================================================================== */

uint8_t rxBuffer[RX_BUFFER_SIZE];
char cmdBuffer[CMD_BUFFER_SIZE];
uint8_t cmdIndex = 0;

bool detectSilence(uint16_t silence_ms, uint16_t timeout_ms) {
    uint32_t start = millis();
    uint32_t lastByte = millis();
    while ((millis() - start) < timeout_ms) {
        if (ALDL_SERIAL.available()) {
            while (ALDL_SERIAL.available()) ALDL_SERIAL.read();
            lastByte = millis();
        } else if ((millis() - lastByte) >= silence_ms) {
            return true;
        }
        delayMicroseconds(100);
    }
    return false;
}

bool txFrame(const uint8_t *frame, uint8_t len) {
    if (!detectSilence(SILENCE_MS, 500)) return false;
    
    uint8_t txCount = frame[1] - 82;
    if (txCount > len) txCount = len;
    
    while (ALDL_SERIAL.available()) ALDL_SERIAL.read();
    ALDL_SERIAL.write(frame, txCount);
    ALDL_SERIAL.flush();

    /* Skip echo */
    uint32_t deadline = millis() + 200;
    uint8_t echoed = 0;
    while (echoed < txCount && millis() < deadline) {
        if (ALDL_SERIAL.available()) {
            ALDL_SERIAL.read();
            echoed++;
        }
    }
    return true;
}

uint16_t rxFrame(uint8_t *buffer, uint16_t bufSize, uint16_t timeout_ms) {
    uint16_t idx = 0;
    uint32_t start = millis();
    uint32_t lastRx = millis();
    
    while ((millis() - start) < timeout_ms && idx < bufSize) {
        if (ALDL_SERIAL.available()) {
            buffer[idx++] = ALDL_SERIAL.read();
            lastRx = millis();
        } else if (idx > 0 && (millis() - lastRx) > 50) {
            break;
        }
        delayMicroseconds(100);
    }
    return idx;
}

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
 * Mode 6 Kernel Upload
 * ======================================================================== */

/**
 * Upload a small kernel to PCM RAM via Mode 6.
 * From OSE Mode6VXYUploadExec() — single chunk for small kernels.
 */
bool uploadKernel(const uint8_t *kernel, uint8_t kernelLen,
                  uint16_t loadAddr) {
    /* Build Mode 6 upload frame */
    /* [DeviceID, LenByte, 0x06, BankID, AddrHi, AddrLo, ...data..., CS] */
    uint8_t payloadLen = 1 + 1 + 2 + kernelLen;  /* mode+bank+addr+data */
    uint8_t lengthByte = ALDL_LENGTH_OFFSET + payloadLen;
    uint8_t frameLen = 2 + payloadLen + 1;  /* device+len+payload+checksum */

    if (frameLen > 200) {
        DEBUG_SERIAL.println(F("! Kernel too large for single frame"));
        return false;
    }

    uint8_t frame[200];
    frame[0] = DEVICE_PCM;
    frame[1] = lengthByte;
    frame[2] = MODE_6;
    frame[3] = BANK_1_ID;
    frame[4] = (loadAddr >> 8) & 0xFF;
    frame[5] = loadAddr & 0xFF;
    memcpy(&frame[6], kernel, kernelLen);
    frame[6 + kernelLen] = aldl_checksum(frame, 6 + kernelLen);

    DEBUG_SERIAL.print(F("Uploading "));
    DEBUG_SERIAL.print(kernelLen);
    DEBUG_SERIAL.print(F(" bytes to 0x"));
    DEBUG_SERIAL.println(loadAddr, HEX);

    for (uint8_t attempt = 0; attempt < 5; attempt++) {
        if (!txFrame(frame, frameLen)) continue;
        uint16_t respLen = rxFrame(rxBuffer, RX_BUFFER_SIZE, 5000);
        if (respLen > 0) {
            DEBUG_SERIAL.println(F("Kernel upload OK"));
            return true;
        }
        DEBUG_SERIAL.print(F("  Retry "));
        DEBUG_SERIAL.println(attempt + 1);
    }

    DEBUG_SERIAL.println(F("! Kernel upload FAILED"));
    return false;
}

/* ========================================================================
 * Memory Dump Command
 * ======================================================================== */

/**
 * Dump memory region by uploading a read kernel.
 * The kernel reads memory and sends bytes back over ALDL.
 *
 * WARNING: This replaces the running ECU code with our kernel!
 * Only use with Key-On Engine-Off (KOEO) for safety.
 */
bool dumpMemory(uint16_t startAddr, uint8_t byteCount) {
    if (byteCount > 128) byteCount = 128;

    /* Copy kernel template and patch address + count */
    uint8_t kernel[sizeof(MEM_READ_KERNEL_TEMPLATE)];
    memcpy_P(kernel, MEM_READ_KERNEL_TEMPLATE,
             sizeof(MEM_READ_KERNEL_TEMPLATE));
    kernel[KERNEL_ADDR_OFFSET]     = (startAddr >> 8) & 0xFF;
    kernel[KERNEL_ADDR_OFFSET + 1] = startAddr & 0xFF;
    kernel[KERNEL_COUNT_OFFSET]    = byteCount;

    DEBUG_SERIAL.print(F("Dumping 0x"));
    DEBUG_SERIAL.print(startAddr, HEX);
    DEBUG_SERIAL.print(F(" - 0x"));
    DEBUG_SERIAL.print(startAddr + byteCount - 1, HEX);
    DEBUG_SERIAL.print(F(" ("));
    DEBUG_SERIAL.print(byteCount);
    DEBUG_SERIAL.println(F(" bytes)"));

    /* Must be in Mode 5 first */
    DEBUG_SERIAL.println(F("Requesting Mode 5..."));
    uint16_t resp = sendCommand(DEVICE_PCM, MODE_5, rxBuffer, RX_BUFFER_SIZE);

    /* Upload the read kernel */
    if (!uploadKernel(kernel, sizeof(MEM_READ_KERNEL_TEMPLATE), 0x0300)) {
        return false;
    }

    /* Listen for returned bytes from kernel */
    DEBUG_SERIAL.println(F("Waiting for memory data..."));
    uint16_t received = rxFrame(rxBuffer, byteCount, 10000);

    if (received > 0) {
        /* Display hex dump */
        DEBUG_SERIAL.println(F("Memory dump:"));
        for (uint16_t i = 0; i < received; i++) {
            if (i > 0 && (i % 16) == 0) {
                DEBUG_SERIAL.println();
            }
            if ((i % 16) == 0) {
                uint16_t addr = startAddr + i;
                if (addr < 0x1000) DEBUG_SERIAL.print('0');
                if (addr < 0x100) DEBUG_SERIAL.print('0');
                if (addr < 0x10) DEBUG_SERIAL.print('0');
                DEBUG_SERIAL.print(addr, HEX);
                DEBUG_SERIAL.print(F(": "));
            }
            if (rxBuffer[i] < 0x10) DEBUG_SERIAL.print('0');
            DEBUG_SERIAL.print(rxBuffer[i], HEX);
            DEBUG_SERIAL.print(' ');
        }
        DEBUG_SERIAL.println();
        DEBUG_SERIAL.print(F("Received: "));
        DEBUG_SERIAL.print(received);
        DEBUG_SERIAL.println(F(" bytes"));
        return true;
    }

    DEBUG_SERIAL.println(F("! No data received from kernel"));
    return false;
}

/* ========================================================================
 * Command Parser
 * ======================================================================== */

/**
 * Parse hex string to uint16_t.
 */
uint16_t parseHex16(const char *str) {
    uint16_t val = 0;
    while (*str) {
        char c = *str++;
        uint8_t nibble;
        if (c >= '0' && c <= '9') nibble = c - '0';
        else if (c >= 'a' && c <= 'f') nibble = c - 'a' + 10;
        else if (c >= 'A' && c <= 'F') nibble = c - 'A' + 10;
        else continue;
        val = (val << 4) | nibble;
    }
    return val;
}

/**
 * Process command from Serial Monitor.
 * Commands:
 *   dump ADDR COUNT  — Dump memory (hex address, hex count)
 *   mode1           — Request Mode 1 data stream
 *   mode5           — Request Mode 5 access
 *   chatter off     — Disable chatter
 *   chatter on      — Enable chatter
 *   help            — Show commands
 */
void processCommand(const char *cmd) {
    if (strncmp(cmd, "dump ", 5) == 0) {
        /* Parse: dump ADDR COUNT */
        char addrStr[8] = {0};
        char countStr[8] = {0};
        uint8_t field = 0;
        uint8_t wi = 0;
        for (const char *p = cmd + 5; *p; p++) {
            if (*p == ' ') {
                field++;
                wi = 0;
            } else if (field == 0 && wi < 7) {
                addrStr[wi++] = *p;
            } else if (field == 1 && wi < 7) {
                countStr[wi++] = *p;
            }
        }
        uint16_t addr = parseHex16(addrStr);
        uint8_t count = (uint8_t)parseHex16(countStr);
        if (count == 0) count = 16;
        dumpMemory(addr, count);

    } else if (strcmp(cmd, "mode1") == 0) {
        uint16_t len = sendCommand(DEVICE_PCM, MODE_1, rxBuffer, RX_BUFFER_SIZE);
        if (len > 0) {
            DEBUG_SERIAL.print(F("Mode 1 response ("));
            DEBUG_SERIAL.print(len);
            DEBUG_SERIAL.println(F(" bytes):"));
            for (uint16_t i = 0; i < len; i++) {
                if (rxBuffer[i] < 0x10) DEBUG_SERIAL.print('0');
                DEBUG_SERIAL.print(rxBuffer[i], HEX);
                DEBUG_SERIAL.print(' ');
                if ((i + 1) % 16 == 0) DEBUG_SERIAL.println();
            }
            DEBUG_SERIAL.println();
        } else {
            DEBUG_SERIAL.println(F("No response"));
        }

    } else if (strcmp(cmd, "mode5") == 0) {
        uint16_t len = sendCommand(DEVICE_PCM, MODE_5, rxBuffer, RX_BUFFER_SIZE);
        if (len > 0) {
            DEBUG_SERIAL.print(F("Mode 5 response: "));
            for (uint16_t i = 0; i < len; i++) {
                if (rxBuffer[i] < 0x10) DEBUG_SERIAL.print('0');
                DEBUG_SERIAL.print(rxBuffer[i], HEX);
                DEBUG_SERIAL.print(' ');
            }
            DEBUG_SERIAL.println();
        }

    } else if (strcmp(cmd, "chatter off") == 0) {
        sendCommand(DEVICE_BCM, MODE_8, rxBuffer, RX_BUFFER_SIZE);
        sendCommand(DEVICE_PCM, MODE_8, rxBuffer, RX_BUFFER_SIZE);
        DEBUG_SERIAL.println(F("Chatter disabled"));

    } else if (strcmp(cmd, "chatter on") == 0) {
        sendCommand(DEVICE_BCM, MODE_9, rxBuffer, RX_BUFFER_SIZE);
        sendCommand(DEVICE_PCM, MODE_9, rxBuffer, RX_BUFFER_SIZE);
        DEBUG_SERIAL.println(F("Chatter enabled"));

    } else if (strcmp(cmd, "help") == 0) {
        DEBUG_SERIAL.println(F("Commands:"));
        DEBUG_SERIAL.println(F("  dump ADDR COUNT  - Dump memory (hex)"));
        DEBUG_SERIAL.println(F("  mode1            - Data stream request"));
        DEBUG_SERIAL.println(F("  mode5            - Flash programming entry"));
        DEBUG_SERIAL.println(F("  chatter off/on   - Disable/enable chatter"));
        DEBUG_SERIAL.println(F("  help             - This help"));

    } else {
        DEBUG_SERIAL.print(F("Unknown command: "));
        DEBUG_SERIAL.println(cmd);
    }
}

/* ========================================================================
 * Setup & Main Loop
 * ======================================================================== */

void setup() {
    DEBUG_SERIAL.begin(DEBUG_BAUD);
    while (!DEBUG_SERIAL) { ; }

    DEBUG_SERIAL.println(F("========================================"));
    DEBUG_SERIAL.println(F("  KingAI Memory Dumper v0.1"));
    DEBUG_SERIAL.println(F("  Target: VY V6 Delco 09356445"));
    DEBUG_SERIAL.println(F("========================================"));
    DEBUG_SERIAL.println(F("Type 'help' for commands."));

    ALDL_SERIAL.begin(ALDL_BAUD_FAST, ALDL_SERIAL_CONFIG);
    delay(500);

    cmdIndex = 0;
}

void loop() {
    /* Read command from Serial Monitor */
    while (DEBUG_SERIAL.available()) {
        char c = DEBUG_SERIAL.read();
        if (c == '\r' || c == '\n') {
            if (cmdIndex > 0) {
                cmdBuffer[cmdIndex] = '\0';
                DEBUG_SERIAL.print(F("> "));
                DEBUG_SERIAL.println(cmdBuffer);
                processCommand(cmdBuffer);
                cmdIndex = 0;
            }
        } else if (cmdIndex < CMD_BUFFER_SIZE - 1) {
            cmdBuffer[cmdIndex++] = c;
        }
    }
}
