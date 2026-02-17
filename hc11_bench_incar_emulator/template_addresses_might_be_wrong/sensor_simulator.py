"""
Sensor Simulator — Phase 2
============================

Generates analog voltage outputs to simulate CTS, TPS, and MAP sensors
for bench testing a VY V6 Delco PCM without a running engine.

Supports two modes:
  - Static: Fixed values for boot-up testing
  - Dynamic: Scripted profiles (idle → accel → decel → idle) for
             testing PCM response to changing conditions

⚠ PINOUT NOTE: The PCM connector pins for CTS, TPS, MAP inputs are
   PLACEHOLDERS in bench_config.py. Verify against the actual C2
   connector pinout before connecting DAC outputs to the PCM.

⚠ VOLTAGE NOTE: The PCM's ADC inputs expect 0-5V signals referenced
   to the PCM's own 5V reference output. Using an external DAC may
   require buffering and level matching. Do NOT exceed 5V on any input.

Hardware options (for generating analog voltages):
  - MCP4725 I2C DAC (12-bit, single channel) — $2-5 each, need 3
  - MCP4728 I2C DAC (12-bit, 4 channels) — $5-10, single board for all
  - Arduino PWM + RC filter (crude but works for CTS)
  - Resistor decade box (manual, for CTS thermistor simulation)
  - Potentiometers (manual adjustment)

For CTS specifically: the sensor is an NTC thermistor. The PCM measures
resistance to ground through a pull-up. Simulating with a fixed resistor:
  ~2.5 kΩ = ~80°C (warm engine, normal operating)
  ~5.0 kΩ = ~50°C (warm-up)
  ~10 kΩ  = ~20°C (cold start)
  ~350 Ω  = ~110°C (overheating — will trigger fan)

Usage:
  python sensor_simulator.py --mode static --profile warm_idle
  python sensor_simulator.py --mode dynamic --script accel_test
  python sensor_simulator.py --list-profiles

Requirements:
  pip install pyserial  (for Arduino DAC bridge)
  # OR
  pip install adafruit-circuitpython-mcp4725  (for direct I2C DAC)
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from typing import Optional


# =============================================================================
#  SENSOR SPECIFICATIONS
#  ⚠ Resistance/voltage values are approximate — verify against VY V6
#     service manual sensor specifications.
# =============================================================================

@dataclass
class SensorSpec:
    """Specification for a simulated sensor."""
    name: str
    pcm_pin: str           # ⚠ PLACEHOLDER — from bench_config.py
    signal_type: str       # "voltage", "resistance", "frequency"
    min_val: float
    max_val: float
    unit: str
    verified: bool = False  # Set True after confirming PCM pin


# Sensor definitions for VY V6 L36
SENSORS = {
    "CTS": SensorSpec(
        name="Coolant Temperature Sensor",
        pcm_pin="C2_01",        # ⚠ UNVERIFIED
        signal_type="resistance",
        min_val=180.0,          # Ω at ~120°C
        max_val=25000.0,        # Ω at ~-40°C
        unit="ohms",
    ),
    "TPS": SensorSpec(
        name="Throttle Position Sensor",
        pcm_pin="C2_05",        # ⚠ UNVERIFIED
        signal_type="voltage",
        min_val=0.4,            # ~0.4V at closed throttle
        max_val=4.6,            # ~4.6V at WOT
        unit="volts",
    ),
    "MAP": SensorSpec(
        name="Manifold Absolute Pressure",
        pcm_pin="C2_08",        # ⚠ UNVERIFIED
        signal_type="voltage",
        min_val=0.5,            # ~0.5V at high vacuum (decel)
        max_val=4.5,            # ~4.5V at atmospheric (WOT/key-on)
        unit="volts",
    ),
    "IAT": SensorSpec(
        name="Intake Air Temperature",
        pcm_pin="C2_02",        # ⚠ UNVERIFIED
        signal_type="resistance",
        min_val=180.0,          # Ω at hot
        max_val=25000.0,        # Ω at cold
        unit="ohms",
    ),
    "O2_B1": SensorSpec(
        name="Oxygen Sensor Bank 1",
        pcm_pin="C2_15",        # ⚠ UNVERIFIED
        signal_type="voltage",
        min_val=0.0,            # Lean
        max_val=1.0,            # Rich
        unit="volts",
    ),
}


# =============================================================================
#  CTS RESISTANCE-TO-TEMPERATURE TABLE (NTC thermistor)
#  ⚠ These are generic GM NTC values — verify against VY V6 specific sensor
# =============================================================================
CTS_TABLE = {
    # temp_c: resistance_ohms (approximate)
    -40: 100700,
    -30: 52700,
    -20: 28680,
    -10: 16180,
      0: 9420,
     10: 5670,
     20: 3520,
     25: 2800,     # ~room temp
     30: 2238,
     40: 1459,
     50: 973,
     60: 667,
     70: 467,
     80: 332,      # Normal operating temp
     90: 241,
    100: 177,
    110: 132,
    120: 100,
    130: 77,
}


def cts_resistance_for_temp(temp_c: float) -> float:
    """
    Interpolate CTS resistance for a given temperature.
    Uses the CTS_TABLE lookup with linear interpolation between points.

    ⚠ Generic GM NTC curve — verify against actual VY V6 sensor.
    """
    temps = sorted(CTS_TABLE.keys())

    if temp_c <= temps[0]:
        return CTS_TABLE[temps[0]]
    if temp_c >= temps[-1]:
        return CTS_TABLE[temps[-1]]

    # Find surrounding points and interpolate
    for i in range(len(temps) - 1):
        if temps[i] <= temp_c <= temps[i + 1]:
            t0, t1 = temps[i], temps[i + 1]
            r0, r1 = CTS_TABLE[t0], CTS_TABLE[t1]
            # Linear interpolation in log-resistance domain (NTC is exponential)
            import math
            frac = (temp_c - t0) / (t1 - t0)
            log_r = math.log(r0) + frac * (math.log(r1) - math.log(r0))
            return math.exp(log_r)

    return CTS_TABLE[80]  # Fallback to normal operating


# =============================================================================
#  STATIC PROFILES (pre-defined sensor states for common test scenarios)
# =============================================================================

STATIC_PROFILES = {
    "cold_start": {
        "description": "Cold engine, key-on engine-off",
        "CTS": {"temp_c": 20, "resistance_ohms": 3520},
        "TPS": {"voltage": 0.5},
        "MAP": {"voltage": 4.5},   # Atmospheric — engine off
        "IAT": {"temp_c": 20, "resistance_ohms": 3520},
    },
    "warm_idle": {
        "description": "Warm engine at idle (~800 RPM)",
        "CTS": {"temp_c": 80, "resistance_ohms": 332},
        "TPS": {"voltage": 0.5},
        "MAP": {"voltage": 1.5},   # ~50 kPa vacuum at idle
        "IAT": {"temp_c": 30, "resistance_ohms": 2238},
    },
    "warm_cruise": {
        "description": "Warm engine at light cruise (~2500 RPM)",
        "CTS": {"temp_c": 85, "resistance_ohms": 290},
        "TPS": {"voltage": 1.2},   # Light throttle
        "MAP": {"voltage": 2.0},   # ~65 kPa
        "IAT": {"temp_c": 35, "resistance_ohms": 1800},
    },
    "wot": {
        "description": "Wide open throttle",
        "CTS": {"temp_c": 90, "resistance_ohms": 241},
        "TPS": {"voltage": 4.5},   # Full throttle
        "MAP": {"voltage": 4.3},   # Near atmospheric
        "IAT": {"temp_c": 40, "resistance_ohms": 1459},
    },
    "overheat_test": {
        "description": "Simulated overheating — should trigger fan high",
        "CTS": {"temp_c": 110, "resistance_ohms": 132},
        "TPS": {"voltage": 0.5},
        "MAP": {"voltage": 1.5},
        "IAT": {"temp_c": 50, "resistance_ohms": 973},
    },
    "boot_minimum": {
        "description": "Minimum sensors for PCM boot (Phase 1 bench)",
        "CTS": {"temp_c": 80, "resistance_ohms": 2500},  # As specified in plan
        "TPS": {"voltage": 0.5},
        "MAP": {"voltage": 1.5},
    },
}


# =============================================================================
#  DYNAMIC PROFILES (time-based sensor sweeps)
# =============================================================================

@dataclass
class SensorKeyframe:
    """A point in time with target sensor values."""
    time_s: float           # Seconds from start
    cts_temp_c: float = 80
    tps_voltage: float = 0.5
    map_voltage: float = 1.5


DYNAMIC_PROFILES = {
    "warmup": {
        "description": "Cold start → warm idle over 120 seconds",
        "keyframes": [
            SensorKeyframe(time_s=0,   cts_temp_c=20,  tps_voltage=0.5, map_voltage=4.5),
            SensorKeyframe(time_s=5,   cts_temp_c=20,  tps_voltage=0.5, map_voltage=1.8),  # Engine starts
            SensorKeyframe(time_s=30,  cts_temp_c=40,  tps_voltage=0.5, map_voltage=1.6),
            SensorKeyframe(time_s=60,  cts_temp_c=60,  tps_voltage=0.5, map_voltage=1.5),
            SensorKeyframe(time_s=90,  cts_temp_c=75,  tps_voltage=0.5, map_voltage=1.5),
            SensorKeyframe(time_s=120, cts_temp_c=85,  tps_voltage=0.5, map_voltage=1.5),
        ],
    },
    "accel_test": {
        "description": "Idle → WOT → idle over 20 seconds",
        "keyframes": [
            SensorKeyframe(time_s=0,  cts_temp_c=85, tps_voltage=0.5, map_voltage=1.5),  # Idle
            SensorKeyframe(time_s=3,  cts_temp_c=85, tps_voltage=0.5, map_voltage=1.5),  # Steady idle
            SensorKeyframe(time_s=5,  cts_temp_c=85, tps_voltage=4.5, map_voltage=4.3),  # WOT snap
            SensorKeyframe(time_s=10, cts_temp_c=85, tps_voltage=4.5, map_voltage=4.3),  # Hold WOT
            SensorKeyframe(time_s=12, cts_temp_c=85, tps_voltage=0.5, map_voltage=0.8),  # Decel (high vacuum)
            SensorKeyframe(time_s=15, cts_temp_c=85, tps_voltage=0.5, map_voltage=1.5),  # Return to idle
            SensorKeyframe(time_s=20, cts_temp_c=85, tps_voltage=0.5, map_voltage=1.5),  # Stable idle
        ],
    },
    "fan_trigger": {
        "description": "Slow temperature ramp to trigger fan thresholds",
        "keyframes": [
            SensorKeyframe(time_s=0,   cts_temp_c=80,  tps_voltage=0.5, map_voltage=1.5),
            SensorKeyframe(time_s=30,  cts_temp_c=90,  tps_voltage=0.5, map_voltage=1.5),
            SensorKeyframe(time_s=60,  cts_temp_c=100, tps_voltage=0.5, map_voltage=1.5),  # Fan low ON?
            SensorKeyframe(time_s=90,  cts_temp_c=110, tps_voltage=0.5, map_voltage=1.5),  # Fan high ON?
            SensorKeyframe(time_s=120, cts_temp_c=105, tps_voltage=0.5, map_voltage=1.5),  # Cool down
            SensorKeyframe(time_s=150, cts_temp_c=95,  tps_voltage=0.5, map_voltage=1.5),  # Fan off?
            SensorKeyframe(time_s=180, cts_temp_c=85,  tps_voltage=0.5, map_voltage=1.5),  # Stable
        ],
    },
}


# =============================================================================
#  DAC OUTPUT INTERFACE (abstract — implement for your hardware)
# =============================================================================

class DACInterface:
    """
    Abstract DAC output interface.

    Implement a subclass for your specific DAC hardware:
    - ArduinoDAC: sends commands to Arduino over serial
    - MCP4725DAC: drives MCP4725 over I2C (Raspberry Pi / CircuitPython)
    - MockDAC: prints values to console (for testing without hardware)
    """

    def set_voltage(self, channel: str, voltage: float):
        """Set a DAC channel to the specified voltage (0-5V)."""
        raise NotImplementedError

    def set_resistance_via_digipot(self, channel: str, resistance_ohms: float):
        """
        Set a digital potentiometer to simulate resistance.
        Only applicable for CTS/IAT simulation.
        Alternative: use fixed resistors or resistor decade box.
        """
        raise NotImplementedError


class MockDAC(DACInterface):
    """Console-only DAC for testing without hardware."""

    def set_voltage(self, channel: str, voltage: float):
        voltage = max(0.0, min(5.0, voltage))
        print(f"  DAC {channel}: {voltage:.3f}V")

    def set_resistance_via_digipot(self, channel: str, resistance_ohms: float):
        print(f"  DIGIPOT {channel}: {resistance_ohms:.0f}Ω")


class ArduinoDAC(DACInterface):
    """
    Sends DAC commands to an Arduino over serial.

    Expected Arduino firmware protocol:
      "V<channel>,<millivolts>\n"  — set voltage
      "R<channel>,<ohms>\n"       — set digital pot resistance

    ⚠ TEMPLATE — implement Arduino firmware to match this protocol.
    """

    def __init__(self, port: str, baud: int = 115200):
        import serial
        self.ser = serial.Serial(port, baud, timeout=1)
        time.sleep(2)  # Wait for Arduino reset

    def set_voltage(self, channel: str, voltage: float):
        voltage = max(0.0, min(5.0, voltage))
        mv = int(voltage * 1000)
        cmd = f"V{channel},{mv}\n"
        self.ser.write(cmd.encode())

    def set_resistance_via_digipot(self, channel: str, resistance_ohms: float):
        cmd = f"R{channel},{int(resistance_ohms)}\n"
        self.ser.write(cmd.encode())


# =============================================================================
#  SIMULATOR ENGINE
# =============================================================================

class SensorSimulator:
    """Drives DAC outputs according to static or dynamic profiles."""

    def __init__(self, dac: DACInterface, verbose: bool = True):
        self.dac = dac
        self.verbose = verbose

    def apply_static(self, profile_name: str):
        """Apply a static sensor profile."""
        if profile_name not in STATIC_PROFILES:
            print(f"ERROR: Unknown profile '{profile_name}'")
            print(f"Available: {', '.join(STATIC_PROFILES.keys())}")
            return

        profile = STATIC_PROFILES[profile_name]
        print(f"\nApplying static profile: {profile_name}")
        print(f"  {profile['description']}")
        print()

        if "CTS" in profile:
            cts = profile["CTS"]
            if "resistance_ohms" in cts:
                self.dac.set_resistance_via_digipot("CTS", cts["resistance_ohms"])
            if "temp_c" in cts and self.verbose:
                print(f"  CTS target: {cts['temp_c']}°C")

        if "TPS" in profile:
            self.dac.set_voltage("TPS", profile["TPS"]["voltage"])

        if "MAP" in profile:
            self.dac.set_voltage("MAP", profile["MAP"]["voltage"])

        if "IAT" in profile:
            iat = profile["IAT"]
            if "resistance_ohms" in iat:
                self.dac.set_resistance_via_digipot("IAT", iat["resistance_ohms"])

        print("\n✓ Static profile applied.")

    def run_dynamic(self, profile_name: str, speed_factor: float = 1.0):
        """
        Run a dynamic (time-based) sensor profile.

        Args:
            profile_name: Name of the dynamic profile
            speed_factor: Time multiplier (0.5 = half speed, 2.0 = double speed)
        """
        if profile_name not in DYNAMIC_PROFILES:
            print(f"ERROR: Unknown dynamic profile '{profile_name}'")
            print(f"Available: {', '.join(DYNAMIC_PROFILES.keys())}")
            return

        profile = DYNAMIC_PROFILES[profile_name]
        keyframes = profile["keyframes"]

        print(f"\nRunning dynamic profile: {profile_name}")
        print(f"  {profile['description']}")
        print(f"  Duration: {keyframes[-1].time_s}s (x{speed_factor} speed)")
        print(f"  Press Ctrl+C to stop\n")

        start_time = time.time()
        kf_idx = 0

        try:
            while True:
                elapsed = (time.time() - start_time) * speed_factor

                # Find current segment
                while kf_idx < len(keyframes) - 1 and keyframes[kf_idx + 1].time_s <= elapsed:
                    kf_idx += 1

                if kf_idx >= len(keyframes) - 1:
                    # Past last keyframe — apply final values and stop
                    kf = keyframes[-1]
                    self._apply_keyframe_values(kf)
                    print(f"\n✓ Dynamic profile complete at t={elapsed:.1f}s")
                    break

                # Interpolate between current and next keyframe
                kf0 = keyframes[kf_idx]
                kf1 = keyframes[kf_idx + 1]
                frac = (elapsed - kf0.time_s) / (kf1.time_s - kf0.time_s)
                frac = max(0.0, min(1.0, frac))

                interp = SensorKeyframe(
                    time_s=elapsed,
                    cts_temp_c=kf0.cts_temp_c + frac * (kf1.cts_temp_c - kf0.cts_temp_c),
                    tps_voltage=kf0.tps_voltage + frac * (kf1.tps_voltage - kf0.tps_voltage),
                    map_voltage=kf0.map_voltage + frac * (kf1.map_voltage - kf0.map_voltage),
                )

                self._apply_keyframe_values(interp)
                time.sleep(0.1)  # Update at 10 Hz

        except KeyboardInterrupt:
            print(f"\n\nStopped at t={elapsed:.1f}s")

    def _apply_keyframe_values(self, kf: SensorKeyframe):
        """Apply a single keyframe's values to all DAC channels."""
        # CTS — convert temperature to resistance
        cts_ohms = cts_resistance_for_temp(kf.cts_temp_c)
        self.dac.set_resistance_via_digipot("CTS", cts_ohms)

        # TPS — direct voltage
        self.dac.set_voltage("TPS", kf.tps_voltage)

        # MAP — direct voltage
        self.dac.set_voltage("MAP", kf.map_voltage)

        if self.verbose:
            print(f"  t={kf.time_s:6.1f}s  CTS={kf.cts_temp_c:5.1f}°C ({cts_ohms:.0f}Ω)  "
                  f"TPS={kf.tps_voltage:.2f}V  MAP={kf.map_voltage:.2f}V")


# =============================================================================
#  CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Sensor Simulator — VY V6 bench testing",
        epilog="⚠ Verify PCM sensor input pins before connecting DAC outputs!"
    )
    parser.add_argument("--mode", choices=["static", "dynamic", "list"],
                        default="list", help="Operation mode")
    parser.add_argument("--profile", type=str, default="warm_idle",
                        help="Profile name to apply")
    parser.add_argument("--speed", type=float, default=1.0,
                        help="Speed factor for dynamic profiles")
    parser.add_argument("--dac", choices=["mock", "arduino"], default="mock",
                        help="DAC interface type")
    parser.add_argument("--port", type=str, default=None,
                        help="Serial port for Arduino DAC")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--list-profiles", action="store_true",
                        help="List all available profiles")

    args = parser.parse_args()

    if args.mode == "list" or args.list_profiles:
        print("\n=== Static Profiles ===")
        for name, prof in STATIC_PROFILES.items():
            print(f"  {name:20s} — {prof['description']}")

        print("\n=== Dynamic Profiles ===")
        for name, prof in DYNAMIC_PROFILES.items():
            dur = prof["keyframes"][-1].time_s
            print(f"  {name:20s} — {prof['description']} ({dur:.0f}s)")

        print("\n=== Sensors ===")
        for name, spec in SENSORS.items():
            status = "✓" if spec.verified else "⚠ UNVERIFIED"
            print(f"  {name:6s} pin={spec.pcm_pin:6s} [{status}] {spec.name}")
        return

    # Create DAC interface
    if args.dac == "mock":
        dac = MockDAC()
    elif args.dac == "arduino":
        if not args.port:
            print("ERROR: --port required for Arduino DAC")
            sys.exit(1)
        dac = ArduinoDAC(args.port)
    else:
        dac = MockDAC()

    sim = SensorSimulator(dac, verbose=args.verbose or args.dac == "mock")

    if args.mode == "static":
        sim.apply_static(args.profile)
    elif args.mode == "dynamic":
        sim.run_dynamic(args.profile, speed_factor=args.speed)


if __name__ == "__main__":
    main()
