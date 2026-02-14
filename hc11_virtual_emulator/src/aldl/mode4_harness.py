r"""
HC11 Virtual Emulator — ALDL Mode 4 Test Harness

SCAFFOLD — needs cross-referencing against:
  - C:\Repos\kingai_srs_commodore_bcm_tool\VX-VY_Mode 4.md
  - C:\Repos\kingai_srs_commodore_bcm_tool\kingai_auto_holden_edition\modules\mode4_actuator.py
  - C:\Repos\kingai_srs_commodore_bcm_tool\kingai_auto_holden_edition\aldl_constants.py
  - C:\Repos\kingai_srs_commodore_bcm_tool\kingai_auto_holden_edition\docs\MODE4_COMPLETE_REFERENCE.md
  - C:\Repos\kingai_srs_commodore_bcm_tool\kingai_auto_holden_edition\docs\CORRECTED_MODE4_AFR_IAC_IMPLEMENTATION.md

Purpose:
  Builds ALDL Mode 4 frames and injects them into the emulator's SCI RX
  queue, then runs the emulated code and checks SCI TX output + port state.

  This is the "virtual scan tool" that talks to the emulated PCM patch code.
  It validates that:
    1. mode4_responder.c correctly parses the Mode 4 frame
    2. Control bytes properly map to output port changes
    3. Response frames have correct format and checksum

Protocol source: PCMHacking.net Topic 2460 (DieselBob / anthrocide)
Frame structures confirmed against kingai_auto_holden_edition tools.

VX/VY V6 Mode 4 Frame (request from scan tool → PCM):
  [0xF7] [0x55+N] [0x04] [23 control bytes] [checksum]
  
  0xF7 = Device address (VX/VY V6 Flash PCM)
  0x55+N = Length (0x55 base + payload byte count)
  0x04 = Mode 4 (Actuator Test)
  23 bytes = ALDLICB+0 through ALDLICB+22
  checksum = sum of all bytes mod 256 = 0
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict


# ══════════════════════════════════════════════
# ALDL Protocol Constants
# ══════════════════════════════════════════════
# Source: kingai_auto_holden_edition/aldl_constants.py

BAUD_RATE = 8192  # Standard Holden ALDL baud
BASE_BYTE_COUNT = 0x55  # Length byte base (85 decimal)

# Device addresses
ADDR_SCAN_TOOL = 0xF0
ADDR_BCM       = 0xF1
ADDR_IPC       = 0xF2
ADDR_ECM_PRI   = 0xF4
ADDR_TCM       = 0xF5
ADDR_VX_VY_V6  = 0xF7  # VX/VY V6 Flash PCM (our primary target)
ADDR_SRS_VT_VX = 0xFA
ADDR_SRS_VY_VZ = 0xFB

# ALDL Modes
MODE_READ_TABLE  = 0x01
MODE_4_ACTUATOR  = 0x04
MODE_NOCHAT      = 0x08
MODE_CHAT        = 0x09
MODE_ENTER_DIAG  = 0x0A
MODE_SECURITY    = 0x11
MODE_WRITE_MEM   = 0x20
MODE_READ_MEM    = 0x22
MODE_WRITE_TABLE = 0x28


# ══════════════════════════════════════════════
# Mode 4 Control Byte Map (23 bytes)
# ══════════════════════════════════════════════
# Source: PCMHacking Topic 2460, VX-VY_Mode 4.md
# Offsets are ALDLICB+N from the start of control data

class Mode4Offsets:
    """ALDLICB control byte offsets within the 23-byte Mode 4 payload.
    
    SCAFFOLD: Offsets confirmed against VX-VY_Mode 4.md and
    kingai_auto_holden_edition/modules/mode4_actuator.py.
    """
    ALDLMODE  = 0   # Always 0x04
    ALDLDSEN  = 1   # Discrete enables (Fan, FP, A/C, TCC, CEL, Shift A/B)
    ALDLDSST  = 2   # Discrete states (on/off for above)
    ALDLDSE2  = 3   # Injector enables (Cyl 1-6)
    ALDLDSS2  = 4   # Injector states (on/off per cyl)
    ALDLMDEN  = 5   # Mode enables (CL, IAC CL, Bypass Spark, BLM Reset, IAC Reset, Clear DTCs)
    ALDLMDST  = 6   # Mode states (CL, IAC CL, FCV control, LPG mode)
    ALDLINCT  = 7   # Input control word 1 (Slew/Abs, ESC, TransTemp, O2A, O2B, TPS, MAF, ATS)
    ALDLINVA  = 8   # Input control value 1
    ALDLINC2  = 9   # Input control word 2 (Slew, Coolant, Road Speed, CCP duty)
    ALDLINV2  = 10  # Input control value 2
    ALDLFNMD  = 11  # PCM function mods (Force Motor, TCC PWM, Max RPM, etc.)
    ALDLFNVA  = 12  # PCM function value
    ALDLEFMD  = 13  # Engine Function Mode — THE KEY CONTROL BYTE
    ALDLIAC   = 14  # IAC desired position/RPM
    ALDLDSAF  = 15  # Desired AFR × 10
    ALDLSPK   = 16  # Spark timing mod/absolute
    ALDLEGR   = 17  # EGR mod/absolute
    ALDLMAF   = 18  # MAF modify
    ALDLFCV   = 19  # FCV mod/absolute
    RESERVED  = 20  # Not used
    ALDLDSE3  = 21  # Discrete enables 3 (Fuel Pump Speed, Start Inhibit)
    ALDLDSS3  = 22  # Discrete states 3


# ALDLEFMD (byte 13) bit definitions — master engine control enable
class EngineControlBits:
    """Bit definitions for ALDLEFMD (byte 13).
    
    Source: VX-VY_Mode 4.md, CORRECTED_MODE4_AFR_IAC_IMPLEMENTATION.md
    """
    ALIACMOD  = 0x01  # IAC Modify Enabled
    ALIACCTL  = 0x02  # 1=RPM Control, 0=Position Control
    ALAFMOD   = 0x04  # A/F Ratio Modify Enabled
    ALSPKMOD  = 0x08  # Spark Modify Enabled
    ALSPKCTL  = 0x10  # 1=Delta Spark, 0=Absolute
    ALSPKPOL  = 0x20  # 1=Retard, 0=Advance
    ALEGRMOD  = 0x40  # 1=Delta EGR, 0=Absolute
    ALMAFMOD  = 0x80  # 1=Delta MAF, 0=Absolute


# ALDLDSEN (byte 1) discrete enable bits
class DiscreteEnableBits:
    """Bit definitions for ALDLDSEN (byte 1).
    
    SCAFFOLD: Needs confirmation from Mode4 documentation.
    """
    FAN_ENABLE     = 0x01
    FUEL_PUMP      = 0x02
    AC_CLUTCH      = 0x04
    TCC_SOLENOID   = 0x08
    CEL_LAMP       = 0x10
    SHIFT_A        = 0x20
    SHIFT_B        = 0x40
    # Bit 7 reserved


# ══════════════════════════════════════════════
# Checksum
# ══════════════════════════════════════════════

def aldl_checksum(data: bytes) -> int:
    """Calculate ALDL checksum byte.
    
    Sum of all frame bytes (including checksum) mod 256 must equal 0.
    checksum = (0x100 - sum(data)) & 0xFF
    
    Confirmed against 4 independent implementations:
      - kingai_auto_holden_edition/holden_aldl_protocol.py
      - vy_vz_cluster_aldl.py
      - vy_instrument_diagnostics.py
      - aldlparser_FULL_DECOMPILED.py
    """
    total = sum(data) & 0xFF
    return (0x100 - total) & 0xFF if total else 0


def validate_checksum(frame: bytes) -> bool:
    """Validate that sum of all frame bytes mod 256 = 0."""
    return (sum(frame) & 0xFF) == 0


# ══════════════════════════════════════════════
# Mode 4 Frame Builder
# ══════════════════════════════════════════════

@dataclass
class Mode4Frame:
    """Mode 4 control frame contents (23 control bytes).
    
    SCAFFOLD: Structure confirmed against mode4_actuator.py Mode4Frame.
    Individual control byte meanings need runtime validation with
    actual PCM or emulator + stock OS ROM.
    """
    control: bytearray = field(default_factory=lambda: bytearray(23))
    device_addr: int = ADDR_VX_VY_V6
    
    def __post_init__(self):
        self.control[Mode4Offsets.ALDLMODE] = MODE_4_ACTUATOR
    
    def build_frame(self) -> bytes:
        """Build complete ALDL frame bytes ready for transmission.
        
        Frame format: [device_addr] [length] [control_bytes...] [checksum]
        Length = BASE_BYTE_COUNT + len(control_bytes)
        """
        payload = bytes(self.control)
        length = (BASE_BYTE_COUNT + len(payload)) & 0xFF
        frame_without_checksum = bytes([self.device_addr, length]) + payload
        cs = aldl_checksum(frame_without_checksum)
        return frame_without_checksum + bytes([cs])
    
    # ── Discrete outputs ──
    
    def set_fan(self, on: bool):
        """Enable and set fan relay state."""
        self.control[Mode4Offsets.ALDLDSEN] |= DiscreteEnableBits.FAN_ENABLE
        if on:
            self.control[Mode4Offsets.ALDLDSST] |= DiscreteEnableBits.FAN_ENABLE
        else:
            self.control[Mode4Offsets.ALDLDSST] &= ~DiscreteEnableBits.FAN_ENABLE & 0xFF
    
    def set_fuel_pump(self, on: bool):
        """Enable and set fuel pump relay state."""
        self.control[Mode4Offsets.ALDLDSEN] |= DiscreteEnableBits.FUEL_PUMP
        if on:
            self.control[Mode4Offsets.ALDLDSST] |= DiscreteEnableBits.FUEL_PUMP
        else:
            self.control[Mode4Offsets.ALDLDSST] &= ~DiscreteEnableBits.FUEL_PUMP & 0xFF
    
    def set_cel(self, on: bool):
        """Enable and set Check Engine Light state."""
        self.control[Mode4Offsets.ALDLDSEN] |= DiscreteEnableBits.CEL_LAMP
        if on:
            self.control[Mode4Offsets.ALDLDSST] |= DiscreteEnableBits.CEL_LAMP
        else:
            self.control[Mode4Offsets.ALDLDSST] &= ~DiscreteEnableBits.CEL_LAMP & 0xFF
    
    def set_ac_clutch(self, on: bool):
        self.control[Mode4Offsets.ALDLDSEN] |= DiscreteEnableBits.AC_CLUTCH
        if on:
            self.control[Mode4Offsets.ALDLDSST] |= DiscreteEnableBits.AC_CLUTCH
        else:
            self.control[Mode4Offsets.ALDLDSST] &= ~DiscreteEnableBits.AC_CLUTCH & 0xFF
    
    # ── Engine control (byte 13 — ALDLEFMD) ──
    
    def set_iac_rpm(self, rpm: int):
        """Control IAC for target RPM.
        
        SCAFFOLD: Conversion needs validation.
        Byte 14 (ALDLIAC) = RPM / 12.5 (per PCMHacking corrections)
        Byte 13 bit 0 = IAC Modify Enable
        Byte 13 bit 1 = RPM control mode (vs position)
        """
        self.control[Mode4Offsets.ALDLEFMD] |= (
            EngineControlBits.ALIACMOD | EngineControlBits.ALIACCTL
        )
        self.control[Mode4Offsets.ALDLIAC] = min(255, max(0, int(rpm / 12.5)))
    
    def set_iac_position(self, steps: int):
        """Control IAC to absolute step position.
        
        Byte 14 = step count (0-255)
        Byte 13 bit 0 = enable, bit 1 = 0 (position mode)
        """
        self.control[Mode4Offsets.ALDLEFMD] |= EngineControlBits.ALIACMOD
        self.control[Mode4Offsets.ALDLEFMD] &= ~EngineControlBits.ALIACCTL & 0xFF
        self.control[Mode4Offsets.ALDLIAC] = min(255, max(0, steps))
    
    def set_afr(self, afr: float):
        """Set target Air/Fuel Ratio.
        
        SCAFFOLD: Conversion confirmed against CORRECTED_MODE4_AFR_IAC_IMPLEMENTATION.md
        Byte 15 (ALDLDSAF) = AFR × 10 (so 14.7 → 147, 12.5 → 125)
        Byte 13 bit 2 = A/F Modify Enable
        """
        self.control[Mode4Offsets.ALDLEFMD] |= EngineControlBits.ALAFMOD
        self.control[Mode4Offsets.ALDLDSAF] = min(255, max(0, int(afr * 10)))
    
    def set_spark(self, degrees: float, absolute: bool = True, retard: bool = False):
        """Set spark timing.
        
        SCAFFOLD: Conversion needs validation.
        Byte 16 (ALDLSPK) = degrees / 0.352 (per stock XDF SPK conversion)
        Byte 13 bit 3 = Spark Modify Enable
        Byte 13 bit 4 = 1 for delta, 0 for absolute
        Byte 13 bit 5 = 1 for retard polarity
        """
        self.control[Mode4Offsets.ALDLEFMD] |= EngineControlBits.ALSPKMOD
        if not absolute:
            self.control[Mode4Offsets.ALDLEFMD] |= EngineControlBits.ALSPKCTL
        if retard:
            self.control[Mode4Offsets.ALDLEFMD] |= EngineControlBits.ALSPKPOL
        self.control[Mode4Offsets.ALDLSPK] = min(255, max(0, int(degrees / 0.352)))
    
    # ── Utility ──
    
    def clear(self):
        """Reset all control bytes to zero (safe idle state)."""
        self.control = bytearray(23)
        self.control[Mode4Offsets.ALDLMODE] = MODE_4_ACTUATOR
    
    def hexdump(self) -> str:
        """Display frame as hex string for debugging."""
        frame = self.build_frame()
        hex_str = ' '.join(f'{b:02X}' for b in frame)
        return hex_str


# ══════════════════════════════════════════════
# Mode 1 Data Stream Parser
# ══════════════════════════════════════════════
# Source: kingai_auto_holden_edition/aldl_constants.py MODE1_PARAMETERS

@dataclass
class Mode1Data:
    """Parsed Mode 1 data stream values (VX/VY V6).
    
    SCAFFOLD: Byte offsets and conversions confirmed against aldl_constants.py.
    Units and formulas need validation against live ALDL captures.
    """
    raw: bytes = b''  # Raw Mode 1 response data
    
    @property
    def cts_degf(self) -> float:
        """Coolant Temperature (°F). Offset 7, X×1.35 - 40."""
        if len(self.raw) > 7:
            return self.raw[7] * 1.35 - 40
        return 0
    
    @property
    def tps_pct(self) -> float:
        """Throttle Position (%). Offset 10, X/2.56."""
        if len(self.raw) > 10:
            return self.raw[10] / 2.56
        return 0
    
    @property
    def rpm(self) -> int:
        """Engine RPM. Offset 11, X×25."""
        if len(self.raw) > 11:
            return self.raw[11] * 25
        return 0
    
    @property
    def mph(self) -> int:
        """Vehicle Speed (MPH). Offset 17, raw value."""
        if len(self.raw) > 17:
            return self.raw[17]
        return 0
    
    @property
    def o2_mv(self) -> float:
        """O2 Sensor (mV). Offset 19, X×4.42."""
        if len(self.raw) > 19:
            return self.raw[19] * 4.42
        return 0
    
    @property
    def blm(self) -> int:
        """Block Learn Multiplier. Offset 22, raw value."""
        if len(self.raw) > 22:
            return self.raw[22]
        return 0
    
    @property
    def iac_steps(self) -> int:
        """IAC Position (steps). Offset 25, raw value."""
        if len(self.raw) > 25:
            return self.raw[25]
        return 0
    
    @property
    def map_kpa(self) -> float:
        """Manifold Pressure (kPa). Offset 29, (X+28.06)/2.71."""
        if len(self.raw) > 29:
            return (self.raw[29] + 28.06) / 2.71
        return 0
    
    @property
    def battery_v(self) -> float:
        """Battery Voltage (V). Offset 34, X/10."""
        if len(self.raw) > 34:
            return self.raw[34] / 10
        return 0
    
    @property
    def spark_deg(self) -> float:
        """Spark Advance (degrees). Offset 38, X×0.352."""
        if len(self.raw) > 38:
            return self.raw[38] * 0.352
        return 0
    
    @property
    def afr(self) -> float:
        """Desired A/F Ratio. Offset 41, X/10."""
        if len(self.raw) > 41:
            return self.raw[41] / 10
        return 0


# ══════════════════════════════════════════════
# ALDL Message Builder (generic)
# ══════════════════════════════════════════════

class ALDLMessageBuilder:
    """Generic ALDL frame builder for various modes.
    
    SCAFFOLD: Frame construction confirmed against multiple implementations.
    Mode-specific payloads need command-by-command validation.
    """
    
    @staticmethod
    def enter_diagnostics(device_addr: int = ADDR_VX_VY_V6) -> bytes:
        """Build 'Enter Diagnostics' command frame.
        
        Mode $0A — puts the ECU into diagnostic mode.
        Must be sent before Mode 4 commands.
        """
        payload = bytes([MODE_ENTER_DIAG])
        return ALDLMessageBuilder._build(device_addr, payload)
    
    @staticmethod
    def nochat(device_addr: int = ADDR_BCM) -> bytes:
        """Build 'Disable BCM chatter' command.
        
        Mode $08 — stops BCM from filling the bus with unsolicited messages.
        Send to BCM ($F1) before PCM communication.
        """
        payload = bytes([MODE_NOCHAT])
        return ALDLMessageBuilder._build(device_addr, payload)
    
    @staticmethod
    def chat(device_addr: int = ADDR_BCM) -> bytes:
        """Build 'Enable BCM chatter' command (restore normal bus)."""
        payload = bytes([MODE_CHAT])
        return ALDLMessageBuilder._build(device_addr, payload)
    
    @staticmethod
    def read_mode1(device_addr: int = ADDR_VX_VY_V6) -> bytes:
        """Build Mode 1 data stream request."""
        payload = bytes([MODE_READ_TABLE])
        return ALDLMessageBuilder._build(device_addr, payload)
    
    @staticmethod
    def mode4(frame: Mode4Frame) -> bytes:
        """Build Mode 4 command from a Mode4Frame."""
        return frame.build_frame()
    
    @staticmethod
    def _build(device_addr: int, payload: bytes) -> bytes:
        """Build generic ALDL frame: [addr] [len] [payload] [checksum]."""
        length = (BASE_BYTE_COUNT + len(payload)) & 0xFF
        frame = bytes([device_addr, length]) + payload
        cs = aldl_checksum(frame)
        return frame + bytes([cs])


# ══════════════════════════════════════════════
# Emulator Test Harness
# ══════════════════════════════════════════════

class Mode4TestHarness:
    """Test harness that connects ALDL Mode 4 frames to the HC11 emulator.
    
    SCAFFOLD: Integration layer. Needs the emulator to be functional
    before any of these tests can actually run. This is the target
    integration point — when the emulator runs mode4_responder.c
    compiled output, this harness validates the behavior.
    
    Usage:
        from src.emu import HC11Emulator
        from src.aldl.mode4_harness import Mode4TestHarness
        
        emu = HC11Emulator()
        emu.load_binary('mode4_responder.bin', base_addr=0x5D00)
        emu.regs.PC = 0x5D00
        
        harness = Mode4TestHarness(emu)
        harness.test_fan_on()
        harness.test_cel_on()
    """
    
    def __init__(self, emulator=None):
        self.emulator = emulator
        self.results: List[Dict] = []
    
    def send_mode4(self, frame: Mode4Frame, run_cycles: int = 100000) -> dict:
        """Send Mode 4 frame to emulator and run until response or timeout.
        
        Returns dict with:
          'tx_output': bytes sent by emulated code on SCI
          'portb_state': PORTB value after execution
          'portb_bits': decoded PORTB bit names
          'cycles_used': E-clock cycles consumed
          'stop_reason': why execution stopped
        """
        if self.emulator is None:
            raise RuntimeError("No emulator attached")
        
        # Build and inject the ALDL frame into SCI RX
        aldl_frame = frame.build_frame()
        self.emulator.sci.inject_rx(aldl_frame)
        
        # Run emulator
        start_cycles = self.emulator.regs.cycles
        reason = self.emulator.run(max_cycles=run_cycles)
        
        result = {
            'frame_hex': ' '.join(f'{b:02X}' for b in aldl_frame),
            'tx_output': self.emulator.sci.sci_output,
            'portb_state': self.emulator.ports.get_port(0x1004),
            'portb_bits': self.emulator.ports.get_portb_bits(),
            'cycles_used': self.emulator.regs.cycles - start_cycles,
            'stop_reason': reason.value if reason else 'RUNNING',
            'checksum_valid': validate_checksum(aldl_frame),
        }
        self.results.append(result)
        return result
    
    def test_fan_on(self) -> dict:
        """Test: Send Mode 4 with fan relay ON, verify PORTB bit 0 = 1."""
        frame = Mode4Frame()
        frame.set_fan(True)
        return self.send_mode4(frame)
    
    def test_fan_off(self) -> dict:
        """Test: Send Mode 4 with fan relay OFF, verify PORTB bit 0 = 0."""
        frame = Mode4Frame()
        frame.set_fan(False)
        return self.send_mode4(frame)
    
    def test_cel_on(self) -> dict:
        """Test: Send Mode 4 with CEL ON, verify PORTB bit 4 = 1."""
        frame = Mode4Frame()
        frame.set_cel(True)
        return self.send_mode4(frame)
    
    def test_afr_stoich(self) -> dict:
        """Test: Set AFR to 14.7 (stoichiometric), verify control bytes."""
        frame = Mode4Frame()
        frame.set_afr(14.7)
        return self.send_mode4(frame)
    
    def test_idle_rpm(self, rpm: int = 750) -> dict:
        """Test: Set idle RPM via IAC, verify control bytes."""
        frame = Mode4Frame()
        frame.set_iac_rpm(rpm)
        return self.send_mode4(frame)
    
    def test_spark_absolute(self, degrees: float = 10.0) -> dict:
        """Test: Set absolute spark timing."""
        frame = Mode4Frame()
        frame.set_spark(degrees, absolute=True)
        return self.send_mode4(frame)
    
    def report(self) -> str:
        """Generate test results summary."""
        lines = ["═" * 60]
        lines.append("  ALDL Mode 4 Test Results")
        lines.append("═" * 60)
        
        for i, r in enumerate(self.results):
            lines.append(f"\n  Test {i+1}:")
            lines.append(f"    Frame:    {r['frame_hex']}")
            lines.append(f"    Checksum: {'VALID' if r['checksum_valid'] else 'INVALID'}")
            lines.append(f"    TX out:   {r['tx_output'].hex() if r['tx_output'] else '(none)'}")
            lines.append(f"    PORTB:    0x{r['portb_state']:02X} = {r['portb_state']:08b}")
            bits = r['portb_bits']
            active = [k for k, v in bits.items() if v]
            lines.append(f"    Active:   {', '.join(active) if active else '(none)'}")
            lines.append(f"    Cycles:   {r['cycles_used']}")
            lines.append(f"    Stopped:  {r['stop_reason']}")
        
        lines.append("\n" + "═" * 60)
        return '\n'.join(lines)
