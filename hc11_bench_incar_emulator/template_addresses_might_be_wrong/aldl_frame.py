"""
ALDL Frame Builder / Parser
============================

Builds and parses GM ALDL (Assembly Line Diagnostic Link) frames
for 8192-baud communication with Delco HC11-based PCMs.

Frame format (GM XDE-5024B specification):
  [MODE] [LENGTH] [DATA...] [CHECKSUM]

  MODE     = 1 byte  — command mode ($01=data stream, $04=actuator, $0A=enter diag)
  LENGTH   = 1 byte  — total frame length including mode, length, and checksum
  DATA     = N bytes — mode-specific payload
  CHECKSUM = 1 byte  — two's complement: sum of all bytes (incl checksum) = $00

⚠ PIN/ADDRESS NOTE: This module handles the protocol/framing layer only.
   No pin assignments are used here — this is pure software.
   Physical wiring is handled by aldl_bridge.py + bench_config.py.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass, field
from typing import Optional


def checksum(data: bytes) -> int:
    """
    Calculate ALDL checksum (two's complement).
    Sum of all bytes in the frame including checksum should equal 0x00 (mod 256).
    Returns the checksum byte to append.
    """
    return (256 - (sum(data) & 0xFF)) & 0xFF


def verify_checksum(frame: bytes) -> bool:
    """Verify that an ALDL frame's checksum is valid."""
    return (sum(frame) & 0xFF) == 0x00


@dataclass
class ALDLFrame:
    """Represents a single ALDL communication frame."""
    mode: int
    data: bytes = b""
    raw: bytes = b""

    @property
    def length(self) -> int:
        """Total frame length (mode + length byte + data + checksum)."""
        return 1 + 1 + len(self.data) + 1

    def build(self) -> bytes:
        """Build the complete frame with length and checksum."""
        payload = bytes([self.mode, self.length]) + self.data
        chk = checksum(payload)
        self.raw = payload + bytes([chk])
        return self.raw

    def __repr__(self) -> str:
        hex_data = self.raw.hex(" ").upper() if self.raw else "(not built)"
        return f"ALDLFrame(mode=0x{self.mode:02X}, len={self.length}, raw={hex_data})"


# =============================================================================
#  STANDARD FRAME BUILDERS
# =============================================================================

def build_mode1_request() -> ALDLFrame:
    """
    Build a Mode 1 data stream request.
    The PCM responds with the full Mode 1 data stream (variable length).
    """
    frame = ALDLFrame(mode=0x01)
    frame.build()
    return frame


def build_enter_diagnostics() -> ALDLFrame:
    """
    Build a Mode $0A "Enter Diagnostics" request.
    Must be sent before Mode 4 commands. PCM enters diagnostic mode
    and begins responding to Mode 1/4 requests.
    """
    frame = ALDLFrame(mode=0x0A)
    frame.build()
    return frame


def build_exit_diagnostics() -> ALDLFrame:
    """
    Build a Mode $0F "Exit Diagnostics" / Return to Normal.
    PCM exits diagnostic mode and resumes normal operation.
    """
    frame = ALDLFrame(mode=0x0F)
    frame.build()
    return frame


def build_mode4_frame(payload: bytes) -> ALDLFrame:
    """
    Build a Mode 4 actuator / override command frame.

    The payload bytes are mode-4-specific control fields.
    See bench_config.MODE4_OFFSETS for byte position meanings.

    Args:
        payload: Raw Mode 4 data bytes (command fields)

    Returns:
        Complete ALDLFrame ready to transmit
    """
    frame = ALDLFrame(mode=0x04, data=payload)
    frame.build()
    return frame


def build_mode4_discrete(
    fan_low: bool = False,
    fan_high: bool = False,
    ac_clutch: bool = False,
    cel: bool = False,
    fuel_pump: bool = False,
) -> ALDLFrame:
    """
    Build a Mode 4 frame for discrete output control.

    ⚠ Bit positions are from the VX-VY Mode 4 definition and may need
       verification against the actual $060A calibration.

    Args:
        fan_low:   Enable fan low relay
        fan_high:  Enable fan high relay
        ac_clutch: Enable A/C compressor clutch
        cel:       Enable check engine lamp
        fuel_pump: Enable fuel pump relay
    """
    # Build the discrete output control byte
    # ⚠ These bit positions are PLACEHOLDERS — verify against Mode 4 oracle
    discrete_byte = 0
    if fan_low:    discrete_byte |= (1 << 0)  # ⚠ bit 0 placeholder
    if fan_high:   discrete_byte |= (1 << 1)  # ⚠ bit 1 placeholder
    if ac_clutch:  discrete_byte |= (1 << 2)  # ⚠ bit 2 placeholder
    if cel:        discrete_byte |= (1 << 3)  # ⚠ bit 3 placeholder
    if fuel_pump:  discrete_byte |= (1 << 4)  # ⚠ bit 4 placeholder

    # Mode 4 frame: need at least enough bytes for the discrete output field
    # Byte 3 = discrete outputs, byte 4 = fan control (per MODE4_OFFSETS)
    # Pad with zeros for unused fields
    payload = bytearray(20)  # 20 bytes covers all Mode 4 fields
    payload[3] = discrete_byte
    payload[4] = discrete_byte  # Fan control byte mirrors for relay commands

    return build_mode4_frame(bytes(payload))


def build_mode4_spark_override(advance_degrees: float) -> ALDLFrame:
    """
    Build a Mode 4 frame to override spark advance.

    ⚠ The encoding formula is a PLACEHOLDER — verify against $060A.
       Common GM formula: byte_value = (advance_degrees + 64) * (256/180)
       or byte_value = advance_degrees * (256/90) for some calibrations.

    Args:
        advance_degrees: Desired spark advance in degrees BTDC
    """
    # ⚠ PLACEHOLDER encoding — verify against Mode 4 oracle
    # Common GM: spark_byte = (advance + 64) * (256/180)
    spark_byte = int((advance_degrees + 64) * (256 / 180))
    spark_byte = max(0, min(255, spark_byte))  # Clamp to byte range

    payload = bytearray(20)
    payload[16] = spark_byte  # Byte 16 = spark advance override

    return build_mode4_frame(bytes(payload))


def build_mode4_afr_override(target_afr: float) -> ALDLFrame:
    """
    Build a Mode 4 frame to override air-fuel ratio.

    ⚠ PLACEHOLDER encoding — verify against $060A
    Known: 0x93 (147 decimal) = stoich 14.7:1 for many Delco calibrations

    Args:
        target_afr: Desired air-fuel ratio (e.g. 14.7 for stoich)
    """
    # ⚠ PLACEHOLDER — simple linear mapping
    afr_byte = int(target_afr * 10)
    afr_byte = max(0, min(255, afr_byte))

    payload = bytearray(20)
    payload[15] = afr_byte  # Byte 15 = AFR command

    return build_mode4_frame(bytes(payload))


def build_mode4_iac_override(position: int) -> ALDLFrame:
    """
    Build a Mode 4 frame to override IAC motor position.

    Args:
        position: IAC position value (0-255, higher = more air)
    """
    payload = bytearray(20)
    payload[14] = max(0, min(255, position))  # Byte 14 = IAC position

    return build_mode4_frame(bytes(payload))


def build_mode4_injector_kill(cylinders_to_kill: list[int]) -> ALDLFrame:
    """
    Build a Mode 4 frame to kill individual injectors (power balance test).

    ⚠ CAUTION: Killing injectors causes cylinder imbalance. Bench only.

    Args:
        cylinders_to_kill: List of cylinder numbers (1-6) to disable
    """
    kill_mask = 0
    for cyl in cylinders_to_kill:
        if 1 <= cyl <= 6:
            kill_mask |= (1 << (cyl - 1))  # Bit 0 = cyl 1, etc

    payload = bytearray(20)
    payload[3] = kill_mask  # Byte 3 = injector kill bits

    return build_mode4_frame(bytes(payload))


def build_clear_dtcs() -> ALDLFrame:
    """Build a Mode 4 frame to clear diagnostic trouble codes."""
    payload = bytearray(20)
    payload[5] = 0x20  # Byte 5 bit 5 = clear DTCs (⚠ verify bit position)
    return build_mode4_frame(bytes(payload))


# =============================================================================
#  FRAME PARSER
# =============================================================================

@dataclass
class Mode1Response:
    """Parsed Mode 1 data stream response."""
    raw: bytes
    rpm: Optional[float] = None
    coolant_c: Optional[float] = None
    tps_pct: Optional[float] = None
    map_kpa: Optional[float] = None
    spark_deg: Optional[float] = None
    battery_v: Optional[float] = None
    iac_steps: Optional[int] = None
    vehicle_speed: Optional[int] = None
    o2_mv: Optional[float] = None

    def __repr__(self) -> str:
        parts = []
        if self.rpm is not None: parts.append(f"RPM={self.rpm:.0f}")
        if self.coolant_c is not None: parts.append(f"CLT={self.coolant_c:.0f}°C")
        if self.tps_pct is not None: parts.append(f"TPS={self.tps_pct:.1f}%")
        if self.battery_v is not None: parts.append(f"BATT={self.battery_v:.1f}V")
        if self.spark_deg is not None: parts.append(f"SPK={self.spark_deg:.1f}°")
        return f"Mode1({', '.join(parts)})"


def parse_mode1_response(data: bytes) -> Mode1Response:
    """
    Parse a Mode 1 data stream response into engineering values.

    ⚠ ALL CONVERSION FORMULAS ARE PLACEHOLDERS.
    The actual scaling factors depend on the $060A calibration's data stream
    definition. Cross-reference with the Mode 1 data stream definition file
    from pcmhacking.net archive (topic 2460).

    Args:
        data: Raw Mode 1 response bytes (checksummed frame already stripped
              of mode byte, length byte, and checksum)
    """
    from bench_config import MODE1_OFFSETS as M1

    resp = Mode1Response(raw=data)

    if len(data) > max(M1.values()) + 1:
        # RPM — ⚠ PLACEHOLDER formula: RPM = (hi*256 + lo) * 0.25
        rpm_raw = (data[M1["rpm_high"]] << 8) | data[M1["rpm_low"]]
        resp.rpm = rpm_raw * 0.25  # ⚠ Verify scaling factor

        # Coolant temp — ⚠ PLACEHOLDER: raw ADC value, needs lookup table
        resp.coolant_c = data[M1["coolant_raw"]] - 40.0  # ⚠ Approximate

        # TPS — ⚠ PLACEHOLDER: linear 0-100%
        resp.tps_pct = (data[M1["tps_raw"]] / 255.0) * 100.0

        # MAP — ⚠ PLACEHOLDER: linear kPa
        resp.map_kpa = data[M1["map_raw"]] * 0.4  # ⚠ Approximate

        # Spark advance — ⚠ PLACEHOLDER
        resp.spark_deg = data[M1["spark_adv"]] * 0.352 - 64.0  # ⚠ Approximate

        # Battery voltage
        resp.battery_v = data[M1["battery_v"]] * 0.1

        # IAC
        resp.iac_steps = data[M1["iac_steps"]]

        # Vehicle speed
        resp.vehicle_speed = data[M1["vehicle_spd"]]

        # O2 sensor
        resp.o2_mv = data[M1["o2_bank1"]] * 5.0  # ⚠ 0-1275 mV

    return resp


def parse_raw_frame(raw: bytes) -> Optional[ALDLFrame]:
    """
    Parse raw bytes received from PCM into an ALDLFrame.

    Returns None if frame is invalid (bad checksum, too short, etc).
    """
    if len(raw) < 3:
        return None

    if not verify_checksum(raw):
        return None

    mode = raw[0]
    length = raw[1]

    if length != len(raw):
        return None

    data = raw[2:-1]  # Strip mode, length, and checksum
    frame = ALDLFrame(mode=mode, data=data, raw=raw)
    return frame


# =============================================================================
#  UTILITY
# =============================================================================

def hex_dump(data: bytes, prefix: str = "") -> str:
    """Format bytes as hex dump for logging."""
    hex_str = " ".join(f"{b:02X}" for b in data)
    return f"{prefix}[{len(data)} bytes] {hex_str}"


if __name__ == "__main__":
    # Quick self-test
    print("=== ALDL Frame Builder Self-Test ===\n")

    # Mode 1 request
    m1 = build_mode1_request()
    print(f"Mode 1 request:    {m1}")
    assert verify_checksum(m1.raw), "Mode 1 checksum failed!"

    # Enter diagnostics
    enter = build_enter_diagnostics()
    print(f"Enter diagnostics: {enter}")
    assert verify_checksum(enter.raw), "Enter diag checksum failed!"

    # Mode 4 fan high
    fan = build_mode4_discrete(fan_high=True)
    print(f"Fan high ON:       {fan}")
    assert verify_checksum(fan.raw), "Fan control checksum failed!"

    # Mode 4 spark override
    spark = build_mode4_spark_override(15.0)
    print(f"Spark 15° BTDC:    {spark}")
    assert verify_checksum(spark.raw), "Spark override checksum failed!"

    # Clear DTCs
    clr = build_clear_dtcs()
    print(f"Clear DTCs:        {clr}")
    assert verify_checksum(clr.raw), "Clear DTC checksum failed!"

    # Injector kill
    kill = build_mode4_injector_kill([1, 3])
    print(f"Kill cyl 1,3:      {kill}")
    assert verify_checksum(kill.raw), "Injector kill checksum failed!"

    print("\n✓ All frame checksums valid.")
