/*
 * aldl_protocol.h — Shared ALDL Protocol Constants for HC11 ECU Tooling
 * ======================================================================
 * Common definitions used by ESP32, Arduino, and Raspberry Pi code.
 * Target: Delco 09356445 (VY V6 L36) 128kb eeprom - Motorola 68HC11F1
 * Author: KingAustraliaGG
 * Date: 2026-02-15
 * Need to make a universal logs output folder 
 * with timestamps and a master_logger.py script that 
 * can be wrapped or imported to any py script in 
 * future or linked to this here for example
 * 
 */

#ifndef ALDL_PROTOCOL_H
#define ALDL_PROTOCOL_H

#include <stdint.h>

/* ========================================================================
 * ALDL Bus Configuration
 * ======================================================================== */
#define ALDL_BAUD_FAST          8192    /* Standard ALDL fast baud rate */
#define ALDL_BAUD_SLOW          160     /* Legacy/datastream baud rate */
#define ALDL_SERIAL_CONFIG      SERIAL_8N1  /* 8 data, no parity, 1 stop */

/* ========================================================================
 * Device IDs (Module Addresses on ALDL Bus)
 * Sourced from OSE Flash Tool decompilation
 * ======================================================================== */
/* IMPORTANT: DeviceID is configurable in OSE Flash Tool settings.
 * 0xF4 is the default for some Holden ECMs, but OSE defaults to 0xF7
 * for VY V6 (09356445). Verified: OSE btnConnect_Click → Defines.TxFrame[0]
 * uses the DeviceID from Settings, default "F7" for 92118883/$060A.
 * Other modules: BCM typically 0xF1. IPC and ABS vary by vehicle.
 */
#define DEVICE_PCM              0xF4    /* PCM — common Holden default */
#define DEVICE_PCM_VY_V6        0xF7    /* PCM — VY V6 $060A Enhanced (OSE default) */
#define DEVICE_BCM              0xF1    /* Body Control Module */
#define DEVICE_IPC              0xF0    /* Instrument Panel Cluster */
#define DEVICE_ABS              0xF9    /* Anti-lock Braking System */
#define DEVICE_SCAN_TOOL        0xF0    /* Scan tool / external device */

/* ========================================================================
 * ALDL Mode Numbers
 * ======================================================================== */
#define MODE_1                  0x01    /* Data stream request */
#define MODE_2                  0x02    /* Freeze frame data */
#define MODE_3                  0x03    /* Diagnostic trouble codes */
#define MODE_4                  0x04    /* Actuator test / override */
#define MODE_5                  0x05    /* Flash programming entry */
#define MODE_6                  0x06    /* Upload/execute code in RAM */
#define MODE_7                  0x07    /* Clear DTCs */
#define MODE_8                  0x08    /* Disable normal communication (chatter) */
#define MODE_9                  0x09    /* Enable normal communication */
#define MODE_10                 0x0A    /* Enter diagnostics / NVRAM read */
#define MODE_13                 0x0D    /* Security access (seed-key) */

/* ========================================================================
 * Frame Structure Constants
 * From OSE: frame = [DeviceID, LengthByte, Mode, ...data..., Checksum]
 * LengthByte encoding: actual_payload_length + 85 (0x55)
 * ======================================================================== */
#define ALDL_LENGTH_OFFSET      85      /* Length byte = payload + 85 */
#define ALDL_SIMPLE_LENGTH      0x56    /* 86 = 85+1 (mode only, no extra data) */
#define ALDL_SEED_REQ_LENGTH    0x57    /* 87 = 85+2 (mode + sub-mode) */
#define ALDL_SEED_RESP_LENGTH   0x59    /* 89 = 85+4 (mode+sub+seed_hi+seed_lo) */
/* Key accept response from ECU uses header byte 0x58 (88 decimal),
 * NOT 0x57 or 0x59. Verified: OSE L24029 checks RxFrame[1]==88.
 * RxFrame[4]==0xAA = security passed, 0xCC = key rejected. */
#define ALDL_KEY_RESP_HEADER    0x58    /* 88 = key accept/reject header */

/* ========================================================================
 * Response Codes
 * ======================================================================== */
#define RESPONSE_OK             0xAA    /* Command accepted */
#define RESPONSE_REJECTED       0xCC    /* Command rejected */
#define RESPONSE_FAIL           0x55    /* Command failed */

/* ========================================================================
 * Security / Seed-Key
 * From OSE ALDLFunctions.cs UnlockFlashPCM():
 *   key = 37709 - (seed_low * 256 + seed_high)
 *   if key < 0: key += 65536
 * ======================================================================== */
#define PCM_SECURITY_MAGIC      37709   /* 0x934D */

/* ========================================================================
 * Flash Memory Layout — VY V6 ($060A Enhanced)
 * M29W800DB flash chip (STMicro, TSOP48, 8Mbit = 1MB but only 128KB used)
 * 3-bank architecture with bank switching at $8000-$FFFF
 * ======================================================================== */

/* Bank IDs (sent in Mode 6 requests) */
#define BANK_1_ID               0x48    /* Bank 1: $0000-$FFFF (common + cal) */
#define BANK_2_ID               0x58    /* Bank 2: $8000-$FFFF overlay (engine) */
#define BANK_3_ID               0x50    /* Bank 3: $8000-$FFFF overlay (trans/diag) */

/* Flash Sector Addresses (file offsets) */
#define BANK1_CAL_START         0x4000  /* Calibration data start */
#define BANK1_CAL_END           0x7FFF  /* Calibration data end */
#define BANK1_CODE_START        0x8000  /* Common code start */
#define BANK1_CODE_END          0xFFFF  /* Common code end (vectors at FFC0+) */
#define BANK2_START             0x8000  /* Bank 2 overlay start (file: 0x10000) */
#define BANK3_START             0x8000  /* Bank 3 overlay start (file: 0x18000) */

/* Free space for patches (from FREE_SPACE_ANALYSIS) */
#define PATCH_AREA_START        0x5D00  /* Typical patch injection point */
#define PATCH_AREA_SIZE         0x0300  /* ~768 bytes available */

/* RAM kernel upload address (where Mode 6 uploads to) */
#define KERNEL_RAM_ADDR         0x0300  /* RAM address for uploaded kernels */

/* ========================================================================
 * HC11F1 I/O Register Addresses
 * From M68HC11RM Reference Manual + VY V6 constants
 * ======================================================================== */

/* Port registers */
#define REG_PORTA               0x1000  /* Port A (bidirectional) */
#define REG_PORTB               0x1004  /* Port B (output only - relays) */
#define REG_PORTC               0x1003  /* Port C (bidirectional) */
#define REG_PORTD               0x1008  /* Port D (serial I/O) */
#define REG_PORTE               0x100A  /* Port E (A/D input) */

/* SCI (Serial Communication Interface) — ALDL */
#define REG_BAUD                0x102B  /* Baud rate register */
#define REG_SCCR1               0x102C  /* SCI control register 1 */
#define REG_SCCR2               0x102D  /* SCI control register 2 */
#define REG_SCSR                0x102E  /* SCI status register */
#define REG_SCDR                0x102F  /* SCI data register */

/* SCI status bits */
#define SCSR_TDRE               0x80    /* Transmit Data Register Empty */
#define SCSR_TC                 0x40    /* Transmit Complete */
#define SCSR_RDRF               0x20    /* Receive Data Register Full */
#define SCSR_IDLE               0x10    /* Idle Line Detected */
#define SCSR_OR                 0x08    /* Overrun Error */
#define SCSR_NF                 0x04    /* Noise Flag */
#define SCSR_FE                 0x02    /* Framing Error */

/* SCI control bits */
#define SCCR2_TE                0x08    /* Transmitter Enable */
#define SCCR2_RE                0x04    /* Receiver Enable */
#define SCCR2_RIE               0x20    /* Receive Interrupt Enable */
#define SCCR2_TIE               0x80    /* Transmit Interrupt Enable */

/* Timer */
#define REG_TCNT                0x100E  /* Free-running timer counter (16-bit) */
#define REG_TFLG1               0x1023  /* Timer flag register 1 */
#define REG_TMSK1               0x1022  /* Timer mask register 1 */

/* ADC (Analog-to-Digital) */
#define REG_ADCTL               0x1030  /* A/D control register */
#define REG_ADR1                0x1031  /* A/D result register 1 */
#define REG_ADR2                0x1032  /* A/D result register 2 */
#define REG_ADR3                0x1033  /* A/D result register 3 */
#define REG_ADR4                0x1034  /* A/D result register 4 */

/* COP Watchdog */
#define REG_COPRST              0x103A  /* COP reset register */
#define COP_FEED_1              0x55    /* First COP feed byte */
#define COP_FEED_2              0xAA    /* Second COP feed byte */

/* ========================================================================
 * VY V6 Specific RAM Addresses
 * WARNING: Most of these are UNVERIFIED PLACEHOLDERS. Only 0x00A2 and
 * 0x017B have cross-source confirmation. The rest conflict with addresses
 * found via Vident PID mapping and binary decompilation analysis.
 * DO NOT trust these for production code until hardware-verified.
 *
 * Verified addresses from vy_v6_constants.py / decompilation:
 *   RPM period    = 0x0083 (TIC3 ISR, Vident PID 0x0C) — NOT 0x00A2
 *   Coolant       = 0x0080 (PE2/AN2, Vident PID 0x05)
 *   IAT           = 0x0081 (PE1/AN1, Vident PID 0x0F)
 *   TPS           = 0x0082 (Vident PID 0x11) or 0x00F3 (55R/3W pattern)
 *   O2 Left       = 0x0085 (Vident PID 0x14) or 0x00F7 (39R/1W pattern)
 *   O2 Right      = 0x0087 (Vident PID 0x15)
 *   Battery       = 0x0088 (Vident PID 0x42) or 0x007B (23R/1W)
 *   Dwell calc    = 0x017B (CONFIRMED — 2 sources)
 *
 * Ref: ALDL_PACKET_OFFSET_CROSSREFERENCE.md, ENHANCED_V1_0A_DECOMPILATION_SUMMARY.md
 * ======================================================================== */
/* DISPUTED — 0x00A2 labelled RPM by XDF/Chr0m3 but decompilation says MAP.
 * TIC3 ISR analysis points to RPM at 0x0083 instead. Needs bench test. */
#define RAM_RPM_PERIOD          0x00A2  /* DISPUTED: RPM or MAP? */
// #define RAM_COOLANT_TEMP     0x0092  /* UNVERIFIED — docs say 0x0080 */
// #define RAM_TPS_RAW          0x0052  /* UNVERIFIED — docs say 0x0082 */
// #define RAM_MAP_RAW          0x0063  /* UNVERIFIED — docs say 0x00A2 */
// #define RAM_IAT_RAW          0x0094  /* UNVERIFIED — docs say 0x0081 */
// #define RAM_BATTERY_V        0x0065  /* UNVERIFIED — docs say 0x0088 */
// #define RAM_O2_LEFT          0x006E  /* UNVERIFIED — docs say 0x0085 */
// #define RAM_O2_RIGHT         0x006F  /* UNVERIFIED — docs say 0x0087 */
// #define RAM_DTC_FLAGS        0x0023  /* UNVERIFIED — no source data */
// #define RAM_ENGINE_STATE     0x0021  /* UNVERIFIED — docs say 0x0080 */

/* ========================================================================
 * Checksum Calculation
 * Standard ALDL: sum all bytes, checksum = (256 - sum) & 0xFF
 * ======================================================================== */
static inline uint8_t aldl_checksum(const uint8_t *data, uint8_t len) {
    uint16_t sum = 0;
    for (uint8_t i = 0; i < len; i++) {
        sum += data[i];
    }
    return (uint8_t)((256 - (sum & 0xFF)) & 0xFF);
}

/* ========================================================================
 * Security Key Calculation
 * From OSE ALDLFunctions.cs:
 *   key = 37709 - (seed_low * 256 + seed_high)
 *   if key < 0: key += 65536
 * Note: seed byte order is swapped (low byte * 256 + high byte)
 * ======================================================================== */
static inline uint16_t calculate_security_key(uint8_t seed_hi, uint8_t seed_lo) {
    uint16_t seed = (uint16_t)seed_lo * 256 + (uint16_t)seed_hi;
    int32_t key = (int32_t)PCM_SECURITY_MAGIC - (int32_t)seed;
    if (key < 0) key += 65536;
    return (uint16_t)key;
}

#endif /* ALDL_PROTOCOL_H */
