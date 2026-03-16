/*
 * aldl_chatter_disable.c — Silence BCM/PCM Heartbeat Before Flash Operations
 *
 * Target: 68HC11 (VY V6 92118883, $060A Enhanced OS)
 * Purpose: Send Mode 8 commands to disable periodic messages from BCM and PCM
 *          before attempting flash read/write operations.
 *
 * Why This Is Needed:
 *   On VX/VY Commodores, the BCM sends periodic heartbeat messages on the ALDL bus.
 *   These messages collide with flash programming traffic. The OSE Flash Tool sends
 *   Mode 8 "disable chatter" commands to both BCM and PCM before flash ops:
 *
 *   1. Send Mode 8 to BCM (device ID from settings, typically 0xF1)
 *   2. Send Mode 8 to PCM (device ID 0xF7)
 *   3. Detect BCM heartbeat timing first (DetectTimeHeartBeat)
 *   4. Send disable during the gap between heartbeats
 *
 * ALDL Chatter Disable Protocol:
 *   TX → [DevID] [0x56] [0x08] [checksum]     (Disable chatter for device)
 *   RX ← [DevID] [0x56] [0x08] [checksum]     (Acknowledge)
 *
 * Re-Enable (Mode 9):
 *   TX → [DevID] [0x56] [0x09] [checksum]     (Re-enable chatter)
 *   RX ← [DevID] [0x56] [0x09] [checksum]     (Acknowledge)
 *
 * Cross-reference:
 *   - OSE Flash Tool: DisableChatter() at line 23397
 *   - OSE Flash Tool: ALDLChatterHandler() at line 23438
 *   - OSE Flash Tool: DetectTimeHeartBeat() — listens for BCM periodic messages
 *   - OSE Flash Tool: EnableChatter() — sends Mode 9 to re-enable
 *
 * Status: WIP — Protocol documented, not yet tested
 */

#include "delco_hc11.h"

/* Module device IDs on VX/VY ALDL bus */
#define ALDL_DEV_PCM    0xF7   /* Engine Control Module */
#define ALDL_DEV_BCM    0xF1   /* Body Control Module */
#define ALDL_DEV_IPC    0xF2   /* Instrument Panel Cluster */
#define ALDL_DEV_ABS    0xF9   /* Anti-lock Brake System */

/* Chatter control modes */
#define ALDL_MODE_DISABLE_CHATTER  0x08
#define ALDL_MODE_ENABLE_CHATTER   0x09

/* Frame structure for chatter control: [DevID] [0x56] [Mode] [Checksum] */
#define CHATTER_FRAME_LEN  4

/*
 * Python equivalent for PC-side tool:
 *
 *   def disable_chatter(serial_port, device_id=0xF7):
 *       """Send Mode 8 to silence a module's periodic messages."""
 *       frame = bytes([device_id, 0x56, 0x08])
 *       cs = (256 - sum(frame)) & 0xFF
 *       frame += bytes([cs])
 *       aldl_tx_frame(serial_port, frame)
 *       resp = aldl_rx_frame(serial_port, timeout=2.0)
 *       return resp is not None and resp[2] == 0x08
 *
 *   def enable_chatter(serial_port, device_id=0xF7):
 *       """Send Mode 9 to re-enable periodic messages."""
 *       frame = bytes([device_id, 0x56, 0x09])
 *       cs = (256 - sum(frame)) & 0xFF
 *       frame += bytes([cs])
 *       aldl_tx_frame(serial_port, frame)
 *
 *   def disable_all_chatter(serial_port):
 *       """Silence both BCM and PCM before flash operations."""
 *       # 1. Detect BCM heartbeat timing (listen for periodic frames)
 *       # 2. Send disable to BCM in the gap
 *       disable_chatter(serial_port, 0xF1)  # BCM
 *       time.sleep(0.1)
 *       # 3. Send disable to PCM
 *       disable_chatter(serial_port, 0xF7)  # PCM
 *
 * IMPORTANT: Always re-enable chatter (Mode 9) when done with flash operations!
 * Leaving chatter disabled can cause BCM/IPC errors and warning lights.
 *
 * The OSE Flash Tool's EnableChatter() function sends Mode 9 as a cleanup step
 * regardless of whether the flash operation succeeded or failed.
 */

/* 
 * Build a chatter control frame
 * device_id: Target module (0xF7=PCM, 0xF1=BCM)
 * mode: 0x08=disable, 0x09=enable
 * frame: Output buffer (must be at least 4 bytes)
 */
void build_chatter_frame(unsigned char device_id, unsigned char mode, unsigned char *frame)
{
    frame[0] = device_id;
    frame[1] = 0x56;           /* Chatter control header */
    frame[2] = mode;           /* 0x08=disable, 0x09=enable */
    frame[3] = (unsigned char)((256 - (device_id + 0x56 + mode)) & 0xFF);
}
