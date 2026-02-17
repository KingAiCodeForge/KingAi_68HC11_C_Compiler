/*
 * aldl_wifi_interface.ino — ESP32 ALDL Interface with Wi-Fi
 * ===========================================================
 * Full-featured ESP32 ALDL interface with:
 *   - 8192 baud ALDL serial to VY V6 Delco PCM
 *   - Wi-Fi AP mode with web server for remote access
 *   - Real-time data stream via WebSocket
 *   - Kernel upload capability (Mode 5/6)
 *   - OTA firmware updates
 *
 * Hardware:
 *   - ESP32-S3 (or any ESP32 with UART1)
 *   - Bi-directional level shifter (3.3V ↔ 5V/12V)
 *   - ALDL connector (pin A = data, pin B = ground)
 *
 * Pin Connections (ESP32):
 *   GPIO16 (RX2) ← ALDL data (via level shifter from 12V/5V)
 *   GPIO17 (TX2) → ALDL data (via level shifter to 12V/5V)
 *
 * Protocol sourced from:
 *   - OSE Flash Tool (VL400) decompilation
 *   - kernel_uploader.py POC
 *   - python-OBD (brendan-w) serial patterns
 *
 * Author: KingAustraliaGG
 * Date: 2026-02-15
 */

#include <WiFi.h>
#include <WebServer.h>
#include <WebSocketsServer.h>
#include <HardwareSerial.h>
#include <ArduinoJson.h>
#include "../shared/aldl_protocol.h"

/* ========================================================================
 * Configuration
 * ======================================================================== */

/* Wi-Fi AP settings */
#define WIFI_SSID       "KingAI-ECU"
#define WIFI_PASSWORD   "flashtool123"
#define WIFI_CHANNEL    6

/* Serial ports */
#define ALDL_SERIAL     Serial2
#define ALDL_RX_PIN     16
#define ALDL_TX_PIN     17
#define DEBUG_SERIAL    Serial

/* Buffers */
#define RX_BUFFER_SIZE  512
#define TX_BUFFER_SIZE  256

/* Timing */
#define SILENCE_MS      20
#define FRAME_TIMEOUT   3000
#define STREAM_INTERVAL 500     /* Data stream poll interval (ms) */
#define WS_INTERVAL     100     /* WebSocket broadcast interval (ms) */

/* ========================================================================
 * Globals
 * ======================================================================== */
WebServer httpServer(80);
WebSocketsServer wsServer(81);

uint8_t rxBuffer[RX_BUFFER_SIZE];
uint8_t txBuffer[TX_BUFFER_SIZE];

uint32_t lastStreamPoll = 0;
uint32_t lastWsBroadcast = 0;
bool streaming = false;
bool chatterDisabled = false;
bool ecuConnected = false;

/* Latest parsed data */
struct {
    uint16_t rpm;
    float coolantC;
    float tpsPct;
    float mapKpa;
    float iatC;
    float batteryV;
    uint8_t o2Left;
    uint8_t o2Right;
    float sparkDeg;
    uint8_t iacSteps;
    uint32_t timestamp;
    bool valid;
} liveData;

/* ========================================================================
 * ALDL Low-Level I/O
 * ======================================================================== */

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
        delayMicroseconds(50);
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
        delayMicroseconds(50);
    }
    return idx;
}

uint16_t sendALDLCommand(uint8_t deviceId, uint8_t mode) {
    uint8_t frame[4];
    frame[0] = deviceId;
    frame[1] = ALDL_SIMPLE_LENGTH;
    frame[2] = mode;
    frame[3] = aldl_checksum(frame, 3);
    if (!txFrame(frame, 4)) return 0;
    return rxFrame(rxBuffer, RX_BUFFER_SIZE, FRAME_TIMEOUT);
}

/* ========================================================================
 * Mode 1 Data Stream
 * ======================================================================== */

uint16_t requestMode1() {
    uint8_t frame[5];
    frame[0] = DEVICE_PCM;
    frame[1] = 0x57;
    frame[2] = MODE_1;
    frame[3] = 0x00;
    frame[4] = aldl_checksum(frame, 4);
    if (!txFrame(frame, 5)) return 0;
    return rxFrame(rxBuffer, RX_BUFFER_SIZE, FRAME_TIMEOUT);
}

void parseDataStream(const uint8_t *data, uint16_t len) {
    if (len < 20) {
        liveData.valid = false;
        return;
    }

    const uint8_t *p = data + 3;  /* Skip header */
    uint16_t pLen = len - 3;
    if (pLen < 0x20) {
        liveData.valid = false;
        return;
    }

    uint16_t rpmPeriod = ((uint16_t)p[0x02] << 8) | p[0x03];
    liveData.rpm = (rpmPeriod > 0) ?
        (uint16_t)(120000000UL / ((uint32_t)rpmPeriod * 3)) : 0;
    liveData.coolantC  = p[0x05] * 0.75f - 40.0f;
    liveData.tpsPct    = p[0x08] / 255.0f * 100.0f;
    liveData.mapKpa    = p[0x0A] * 0.39f;
    liveData.iatC      = p[0x0C] * 0.75f - 40.0f;
    liveData.batteryV  = p[0x10] / 10.0f;
    liveData.o2Left    = p[0x12];
    liveData.o2Right   = p[0x13];
    liveData.sparkDeg  = p[0x15] / 2.0f;
    liveData.iacSteps  = p[0x18];
    liveData.timestamp = millis();
    liveData.valid = true;
}

/* ========================================================================
 * Chatter Control
 * ======================================================================== */

bool disableChatter() {
    bool bcm = false, pcm = false;
    for (int i = 0; i < 3; i++) {
        uint16_t len = sendALDLCommand(DEVICE_BCM, MODE_8);
        if (len > 0) { bcm = true; break; }
    }
    for (int i = 0; i < 3; i++) {
        uint16_t len = sendALDLCommand(DEVICE_PCM, MODE_8);
        if (len > 0) { pcm = true; break; }
    }
    chatterDisabled = pcm;
    return pcm;
}

void enableChatter() {
    sendALDLCommand(DEVICE_BCM, MODE_9);
    sendALDLCommand(DEVICE_PCM, MODE_9);
    chatterDisabled = false;
}

/* ========================================================================
 * Security Unlock (for Mode 5/6 operations)
 * ======================================================================== */

bool unlockSecurity() {
    /* Step 1: Request seed */
    uint8_t seedFrame[5];
    seedFrame[0] = DEVICE_PCM;
    seedFrame[1] = 0x57;
    seedFrame[2] = MODE_13;
    seedFrame[3] = 0x01;
    seedFrame[4] = aldl_checksum(seedFrame, 4);

    if (!txFrame(seedFrame, 5)) return false;
    uint16_t len = rxFrame(rxBuffer, RX_BUFFER_SIZE, FRAME_TIMEOUT);
    if (len < 6) return false;

    /* Find seed response */
    uint8_t seedHi = 0, seedLo = 0;
    for (uint16_t i = 0; i < len - 5; i++) {
        if (rxBuffer[i] == DEVICE_PCM && rxBuffer[i+2] == MODE_13) {
            seedHi = rxBuffer[i+4];
            seedLo = rxBuffer[i+5];
            break;
        }
    }

    if (seedHi == 0 && seedLo == 0) {
        DEBUG_SERIAL.println(F("Already unlocked"));
        return true;
    }

    /* Step 2: Calculate key */
    uint16_t key = calculate_security_key(seedHi, seedLo);
    DEBUG_SERIAL.print(F("Security key: 0x"));
    DEBUG_SERIAL.println(key, HEX);

    /* Step 3: Send key */
    uint8_t keyFrame[7];
    keyFrame[0] = DEVICE_PCM;
    keyFrame[1] = 0x59;
    keyFrame[2] = MODE_13;
    keyFrame[3] = 0x02;
    keyFrame[4] = (key >> 8) & 0xFF;
    keyFrame[5] = key & 0xFF;
    keyFrame[6] = aldl_checksum(keyFrame, 6);

    if (!txFrame(keyFrame, 7)) return false;
    len = rxFrame(rxBuffer, RX_BUFFER_SIZE, FRAME_TIMEOUT);

    return (len > 0);
}

/* ========================================================================
 * Mode 6 Kernel Upload
 * ======================================================================== */

bool uploadKernel(const uint8_t *kernel, uint16_t kernelLen,
                  uint16_t loadAddr) {
    /* Single-chunk upload for small kernels */
    uint8_t payloadLen = 1 + 1 + 2 + kernelLen;
    uint8_t lengthByte = ALDL_LENGTH_OFFSET + payloadLen;
    uint8_t frameLen = 2 + payloadLen + 1;

    if (frameLen > TX_BUFFER_SIZE) return false;

    txBuffer[0] = DEVICE_PCM;
    txBuffer[1] = lengthByte;
    txBuffer[2] = MODE_6;
    txBuffer[3] = BANK_1_ID;
    txBuffer[4] = (loadAddr >> 8) & 0xFF;
    txBuffer[5] = loadAddr & 0xFF;
    memcpy(&txBuffer[6], kernel, kernelLen);
    txBuffer[6 + kernelLen] = aldl_checksum(txBuffer, 6 + kernelLen);

    for (int attempt = 0; attempt < 5; attempt++) {
        if (!txFrame(txBuffer, frameLen)) continue;
        uint16_t len = rxFrame(rxBuffer, RX_BUFFER_SIZE, 5000);
        if (len > 0) return true;
    }
    return false;
}

/* ========================================================================
 * Web Server — HTML Interface
 * ======================================================================== */

const char INDEX_HTML[] PROGMEM = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
    <title>KingAI ECU Tool</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Courier New', monospace; background: #1a1a2e;
               color: #e94560; margin: 20px; }
        h1 { color: #0f3460; text-align: center; }
        .card { background: #16213e; border-radius: 8px; padding: 15px;
                margin: 10px 0; border: 1px solid #0f3460; }
        .gauge { display: inline-block; width: 45%; margin: 5px;
                 text-align: center; }
        .gauge .value { font-size: 2em; color: #e94560; font-weight: bold; }
        .gauge .label { color: #a8a8a8; font-size: 0.8em; }
        .btn { background: #0f3460; color: #fff; border: none; padding: 10px 20px;
               border-radius: 5px; cursor: pointer; margin: 5px; font-size: 14px; }
        .btn:hover { background: #e94560; }
        .btn.danger { background: #c0392b; }
        .status { padding: 5px 10px; border-radius: 3px; display: inline-block; }
        .connected { background: #27ae60; color: #fff; }
        .disconnected { background: #c0392b; color: #fff; }
        #log { background: #0d1117; color: #58a6ff; padding: 10px;
               font-size: 12px; height: 200px; overflow-y: auto;
               border-radius: 5px; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h1 style="color:#e94560">&#x1F527; KingAI ECU Tool</h1>
    <div class="card">
        <span id="connStatus" class="status disconnected">Disconnected</span>
        <span style="color:#a8a8a8"> | VY V6 Delco 09356445 | ALDL 8192 baud</span>
    </div>

    <div class="card">
        <h3 style="color:#0f3460">Live Data</h3>
        <div class="gauge"><div class="value" id="rpm">---</div>
            <div class="label">RPM</div></div>
        <div class="gauge"><div class="value" id="tps">---</div>
            <div class="label">TPS %</div></div>
        <div class="gauge"><div class="value" id="clt">---</div>
            <div class="label">Coolant &deg;C</div></div>
        <div class="gauge"><div class="value" id="map">---</div>
            <div class="label">MAP kPa</div></div>
        <div class="gauge"><div class="value" id="bat">---</div>
            <div class="label">Battery V</div></div>
        <div class="gauge"><div class="value" id="spk">---</div>
            <div class="label">Spark &deg;</div></div>
        <div class="gauge"><div class="value" id="iat">---</div>
            <div class="label">IAT &deg;C</div></div>
        <div class="gauge"><div class="value" id="iac">---</div>
            <div class="label">IAC Steps</div></div>
    </div>

    <div class="card">
        <h3 style="color:#0f3460">Controls</h3>
        <button class="btn" onclick="sendCmd('stream_start')">Start Stream</button>
        <button class="btn" onclick="sendCmd('stream_stop')">Stop Stream</button>
        <button class="btn" onclick="sendCmd('chatter_off')">Disable Chatter</button>
        <button class="btn" onclick="sendCmd('chatter_on')">Enable Chatter</button>
        <button class="btn" onclick="sendCmd('mode5')">Mode 5 (Flash Entry)</button>
        <button class="btn danger" onclick="sendCmd('unlock')">Security Unlock</button>
    </div>

    <div class="card">
        <h3 style="color:#0f3460">Log</h3>
        <div id="log"></div>
    </div>

    <script>
        var ws;
        function connect() {
            ws = new WebSocket('ws://' + location.hostname + ':81/');
            ws.onopen = function() {
                document.getElementById('connStatus').className = 'status connected';
                document.getElementById('connStatus').innerText = 'Connected';
                addLog('WebSocket connected');
            };
            ws.onclose = function() {
                document.getElementById('connStatus').className = 'status disconnected';
                document.getElementById('connStatus').innerText = 'Disconnected';
                setTimeout(connect, 2000);
            };
            ws.onmessage = function(evt) {
                try {
                    var d = JSON.parse(evt.data);
                    if (d.type === 'data') {
                        document.getElementById('rpm').innerText = d.rpm || '---';
                        document.getElementById('tps').innerText =
                            d.tps !== undefined ? d.tps.toFixed(1) : '---';
                        document.getElementById('clt').innerText =
                            d.clt !== undefined ? d.clt.toFixed(1) : '---';
                        document.getElementById('map').innerText =
                            d.map !== undefined ? d.map.toFixed(1) : '---';
                        document.getElementById('bat').innerText =
                            d.bat !== undefined ? d.bat.toFixed(1) : '---';
                        document.getElementById('spk').innerText =
                            d.spk !== undefined ? d.spk.toFixed(1) : '---';
                        document.getElementById('iat').innerText =
                            d.iat !== undefined ? d.iat.toFixed(1) : '---';
                        document.getElementById('iac').innerText = d.iac || '---';
                    } else if (d.type === 'log') {
                        addLog(d.msg);
                    }
                } catch(e) {}
            };
        }
        function sendCmd(cmd) {
            if (ws && ws.readyState === 1) {
                ws.send(JSON.stringify({cmd: cmd}));
                addLog('> ' + cmd);
            }
        }
        function addLog(msg) {
            var el = document.getElementById('log');
            el.innerText += new Date().toLocaleTimeString() + ' ' + msg + '\n';
            el.scrollTop = el.scrollHeight;
        }
        connect();
    </script>
</body>
</html>
)rawliteral";

/* ========================================================================
 * Web Server Handlers
 * ======================================================================== */

void handleRoot() {
    httpServer.send_P(200, "text/html", INDEX_HTML);
}

void handleStatus() {
    String json = "{";
    json += "\"connected\":" + String(ecuConnected ? "true" : "false") + ",";
    json += "\"streaming\":" + String(streaming ? "true" : "false") + ",";
    json += "\"chatter_disabled\":" + String(chatterDisabled ? "true" : "false");
    json += "}";
    httpServer.send(200, "application/json", json);
}

/* ========================================================================
 * WebSocket Event Handler
 * ======================================================================== */

void wsEvent(uint8_t num, WStype_t type, uint8_t *payload, size_t length) {
    switch (type) {
        case WStype_CONNECTED:
            DEBUG_SERIAL.printf("WS client %u connected\n", num);
            wsServer.sendTXT(num, "{\"type\":\"log\",\"msg\":\"Connected to KingAI ECU Tool\"}");
            break;

        case WStype_TEXT: {
            /* Parse JSON command */
            StaticJsonDocument<200> doc;
            deserializeJson(doc, payload, length);
            String cmd = doc["cmd"].as<String>();

            if (cmd == "stream_start") {
                streaming = true;
                if (!chatterDisabled) disableChatter();
                wsServer.broadcastTXT("{\"type\":\"log\",\"msg\":\"Data stream started\"}");
            }
            else if (cmd == "stream_stop") {
                streaming = false;
                wsServer.broadcastTXT("{\"type\":\"log\",\"msg\":\"Data stream stopped\"}");
            }
            else if (cmd == "chatter_off") {
                disableChatter();
                wsServer.broadcastTXT("{\"type\":\"log\",\"msg\":\"Chatter disabled\"}");
            }
            else if (cmd == "chatter_on") {
                enableChatter();
                wsServer.broadcastTXT("{\"type\":\"log\",\"msg\":\"Chatter enabled\"}");
            }
            else if (cmd == "mode5") {
                if (!chatterDisabled) disableChatter();
                uint16_t len = sendALDLCommand(DEVICE_PCM, MODE_5);
                String msg = (len > 0) ? "Mode 5 responded" : "Mode 5 no response";
                wsServer.broadcastTXT("{\"type\":\"log\",\"msg\":\"" + msg + "\"}");
            }
            else if (cmd == "unlock") {
                bool ok = unlockSecurity();
                String msg = ok ? "Security UNLOCKED" : "Security unlock FAILED";
                wsServer.broadcastTXT("{\"type\":\"log\",\"msg\":\"" + msg + "\"}");
            }
            break;
        }

        case WStype_DISCONNECTED:
            DEBUG_SERIAL.printf("WS client %u disconnected\n", num);
            break;
    }
}

/* ========================================================================
 * Broadcast Live Data via WebSocket
 * ======================================================================== */

void broadcastLiveData() {
    if (!liveData.valid) return;

    StaticJsonDocument<256> doc;
    doc["type"] = "data";
    doc["rpm"] = liveData.rpm;
    doc["tps"] = liveData.tpsPct;
    doc["clt"] = liveData.coolantC;
    doc["map"] = liveData.mapKpa;
    doc["iat"] = liveData.iatC;
    doc["bat"] = liveData.batteryV;
    doc["spk"] = liveData.sparkDeg;
    doc["iac"] = liveData.iacSteps;
    doc["o2l"] = liveData.o2Left;
    doc["o2r"] = liveData.o2Right;

    String json;
    serializeJson(doc, json);
    wsServer.broadcastTXT(json);
}

/* ========================================================================
 * Setup & Main Loop
 * ======================================================================== */

void setup() {
    /* Debug serial (USB) */
    DEBUG_SERIAL.begin(115200);
    delay(1000);
    DEBUG_SERIAL.println(F("\n========================================"));
    DEBUG_SERIAL.println(F("  KingAI ESP32 ECU Tool v0.1"));
    DEBUG_SERIAL.println(F("  Target: VY V6 Delco 09356445"));
    DEBUG_SERIAL.println(F("  ALDL: 8192 baud on UART2"));
    DEBUG_SERIAL.println(F("========================================\n"));

    /* ALDL serial (8192 baud, 8N1) */
    ALDL_SERIAL.begin(ALDL_BAUD_FAST, ALDL_SERIAL_CONFIG, ALDL_RX_PIN, ALDL_TX_PIN);
    DEBUG_SERIAL.println(F("ALDL serial initialized"));

    /* Wi-Fi Access Point */
    WiFi.softAP(WIFI_SSID, WIFI_PASSWORD, WIFI_CHANNEL);
    IPAddress ip = WiFi.softAPIP();
    DEBUG_SERIAL.print(F("Wi-Fi AP started: "));
    DEBUG_SERIAL.println(WIFI_SSID);
    DEBUG_SERIAL.print(F("IP: "));
    DEBUG_SERIAL.println(ip);
    DEBUG_SERIAL.print(F("Web UI: http://"));
    DEBUG_SERIAL.println(ip);

    /* HTTP server */
    httpServer.on("/", handleRoot);
    httpServer.on("/status", handleStatus);
    httpServer.begin();
    DEBUG_SERIAL.println(F("HTTP server started on port 80"));

    /* WebSocket server */
    wsServer.begin();
    wsServer.onEvent(wsEvent);
    DEBUG_SERIAL.println(F("WebSocket server started on port 81"));

    /* Init live data */
    memset(&liveData, 0, sizeof(liveData));
    liveData.valid = false;

    DEBUG_SERIAL.println(F("\nReady. Connect to Wi-Fi and open web UI."));
}

void loop() {
    /* Handle web clients */
    httpServer.handleClient();
    wsServer.loop();

    /* Poll Mode 1 data stream if streaming enabled */
    if (streaming && (millis() - lastStreamPoll >= STREAM_INTERVAL)) {
        lastStreamPoll = millis();
        uint16_t len = requestMode1();
        if (len > 0) {
            parseDataStream(rxBuffer, len);
            ecuConnected = true;
        } else {
            ecuConnected = false;
        }
    }

    /* Broadcast live data to WebSocket clients */
    if (liveData.valid && (millis() - lastWsBroadcast >= WS_INTERVAL)) {
        lastWsBroadcast = millis();
        broadcastLiveData();
    }

    yield();  /* ESP32 watchdog feed */
}
