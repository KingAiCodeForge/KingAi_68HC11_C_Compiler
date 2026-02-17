"""
HC11 Bench Emulator — Pin / Address Configuration
==================================================

⚠ WARNING: ALL PIN NUMBERS AND CONNECTOR ASSIGNMENTS ARE PLACEHOLDERS.
   They must be verified against the actual VY V6 PCM (P/N 16269238)
   wiring diagram before connecting to real hardware.

   Sources to verify against:
   - pcmhacking.net topic 4930 (bench setup guide)
   - pcmhacking.net topic 7880 (bench harness pinout)
   - JustCommodores thread 222112 (VY V6 PCM pinout)
   - VY V6 service manual wiring diagrams (C1/C2/C3)

   When a pin is confirmed, change its 'verified' field to True.
"""

# =============================================================================
#  STATUS FLAG — Set to True only after ALL pins verified on real hardware
# =============================================================================
ALL_PINS_VERIFIED = False


# =============================================================================
#  ALDL / SERIAL CONFIGURATION (these are well-documented and likely correct)
# =============================================================================
ALDL_BAUD = 8192          # 8192 baud exact (from 4.194304 MHz xtal)
ALDL_DATABITS = 8
ALDL_PARITY = "N"         # No parity
ALDL_STOPBITS = 1
ALDL_FORMAT = "8N1"

# Crystal / clock
CRYSTAL_HZ = 4_194_304    # 4.194304 MHz crystal
E_CLOCK_HZ = 2_097_152    # E-clock = crystal / 2
BAUD_DIVIDER = 0x04        # SCI baud register value → 8192 baud

# ALDL is 12V inverted logic — need MAX232 or active inverter + level shifter
ALDL_LOGIC_INVERTED = True
ALDL_VOLTAGE_HIGH = 0.0   # Logic 1 = 0V on the wire
ALDL_VOLTAGE_LOW = 12.0   # Logic 0 = ~12V on the wire


# =============================================================================
#  OBD-II CONNECTOR PIN MAPPING
#  (OBD-II is standardized — these are correct for VY V6)
# =============================================================================
OBD2_PINS = {
    "pin_4":  {"function": "Chassis ground",    "verified": True},
    "pin_5":  {"function": "Signal ground",     "verified": True},
    "pin_9":  {"function": "ALDL data (8192)",  "verified": True},
    "pin_16": {"function": "Battery +12V",      "verified": True},
}


# =============================================================================
#  PCM CONNECTOR C1 — MAIN (32-pin, power / injectors / ignition)
#  ⚠ UNVERIFIED — placeholder pin numbers
# =============================================================================
C1_PINS = {
    # Power & Ground
    "C1_01": {"function": "Battery +12V (main)",      "wire_color": "PLACEHOLDER", "verified": False},
    "C1_02": {"function": "Battery +12V (backup)",     "wire_color": "PLACEHOLDER", "verified": False},
    "C1_03": {"function": "Ignition 12V (run/start)",  "wire_color": "PLACEHOLDER", "verified": False},
    "C1_04": {"function": "Ground",                    "wire_color": "PLACEHOLDER", "verified": False},
    "C1_05": {"function": "Ground",                    "wire_color": "PLACEHOLDER", "verified": False},

    # Injectors (sequential, 6 cyl)
    "C1_10": {"function": "Injector 1 driver",         "wire_color": "PLACEHOLDER", "verified": False},
    "C1_11": {"function": "Injector 2 driver",         "wire_color": "PLACEHOLDER", "verified": False},
    "C1_12": {"function": "Injector 3 driver",         "wire_color": "PLACEHOLDER", "verified": False},
    "C1_13": {"function": "Injector 4 driver",         "wire_color": "PLACEHOLDER", "verified": False},
    "C1_14": {"function": "Injector 5 driver",         "wire_color": "PLACEHOLDER", "verified": False},
    "C1_15": {"function": "Injector 6 driver",         "wire_color": "PLACEHOLDER", "verified": False},

    # Ignition
    "C1_20": {"function": "ICM bypass",                "wire_color": "PLACEHOLDER", "verified": False},
    "C1_21": {"function": "ICM EST (spark timing)",    "wire_color": "PLACEHOLDER", "verified": False},
    "C1_22": {"function": "ICM reference (3X from ICM)", "wire_color": "PLACEHOLDER", "verified": False},

    # Fuel pump
    "C1_25": {"function": "Fuel pump relay control",   "wire_color": "PLACEHOLDER", "verified": False},
}

# =============================================================================
#  PCM CONNECTOR C2 — SENSORS (32-pin)
#  ⚠ UNVERIFIED — placeholder pin numbers
# =============================================================================
C2_PINS = {
    # Temperature sensors
    "C2_01": {"function": "CTS (coolant temp sensor)", "wire_color": "PLACEHOLDER", "verified": False,
              "notes": "NTC thermistor, ~2.5kΩ @ 80°C for bench sim"},
    "C2_02": {"function": "IAT (intake air temp)",     "wire_color": "PLACEHOLDER", "verified": False},

    # Throttle / load
    "C2_05": {"function": "TPS signal",                "wire_color": "PLACEHOLDER", "verified": False,
              "notes": "0.5V idle, 4.5V WOT"},
    "C2_06": {"function": "TPS ground",                "wire_color": "PLACEHOLDER", "verified": False},
    "C2_07": {"function": "TPS 5V ref",                "wire_color": "PLACEHOLDER", "verified": False},
    "C2_08": {"function": "MAP sensor signal",         "wire_color": "PLACEHOLDER", "verified": False,
              "notes": "~1.5V at idle vacuum, ~4.5V at WOT/atm"},

    # Crank / cam position
    "C2_10": {"function": "3X crank reference signal", "wire_color": "PLACEHOLDER", "verified": False,
              "notes": "From ICM — 3 pulses/rev, reluctor signal"},
    "C2_11": {"function": "18X crank signal",          "wire_color": "PLACEHOLDER", "verified": False,
              "notes": "18 pulses/rev, reluctor signal"},
    "C2_12": {"function": "Cam position signal",       "wire_color": "PLACEHOLDER", "verified": False},

    # Oxygen sensors
    "C2_15": {"function": "O2 sensor bank 1",          "wire_color": "PLACEHOLDER", "verified": False},
    "C2_16": {"function": "O2 sensor bank 2",          "wire_color": "PLACEHOLDER", "verified": False},

    # Knock sensor
    "C2_18": {"function": "Knock sensor signal",       "wire_color": "PLACEHOLDER", "verified": False},

    # Vehicle speed
    "C2_20": {"function": "VSS (vehicle speed sensor)", "wire_color": "PLACEHOLDER", "verified": False},

    # Sensor grounds & references
    "C2_30": {"function": "Sensor ground",             "wire_color": "PLACEHOLDER", "verified": False},
    "C2_31": {"function": "5V sensor reference",       "wire_color": "PLACEHOLDER", "verified": False},
}

# =============================================================================
#  PCM CONNECTOR C3 — AUXILIARY (24-pin, ALDL / relays / A/C / misc)
#  ⚠ UNVERIFIED — placeholder pin numbers
# =============================================================================
C3_PINS = {
    # ALDL
    "C3_01": {"function": "ALDL data line (to OBD pin 9)", "wire_color": "PLACEHOLDER", "verified": False},
    "C3_02": {"function": "ALDL diagnostic request",       "wire_color": "PLACEHOLDER", "verified": False,
              "notes": "Ground to force ALDL diagnostic mode"},

    # Relay outputs
    "C3_05": {"function": "Fan low relay control",         "wire_color": "PLACEHOLDER", "verified": False},
    "C3_06": {"function": "Fan high relay control",        "wire_color": "PLACEHOLDER", "verified": False},
    "C3_07": {"function": "A/C compressor clutch relay",   "wire_color": "PLACEHOLDER", "verified": False},
    "C3_08": {"function": "CEL (check engine lamp)",       "wire_color": "PLACEHOLDER", "verified": False},

    # Transmission
    "C3_10": {"function": "TCC solenoid (torque converter lockup)", "wire_color": "PLACEHOLDER", "verified": False},

    # EGR
    "C3_12": {"function": "EGR solenoid",                  "wire_color": "PLACEHOLDER", "verified": False},

    # IAC (idle air control)
    "C3_15": {"function": "IAC coil A",                    "wire_color": "PLACEHOLDER", "verified": False},
    "C3_16": {"function": "IAC coil B",                    "wire_color": "PLACEHOLDER", "verified": False},

    # VSS output
    "C3_20": {"function": "VSS output to cluster",         "wire_color": "PLACEHOLDER", "verified": False},
}


# =============================================================================
#  BENCH POWER REQUIREMENTS
# =============================================================================
BENCH_POWER = {
    "battery_voltage": 12.0,       # Volts
    "min_current": 3.0,            # Amps (PCM alone draws ~1-2A)
    "recommended_psu_amps": 5.0,   # Headroom for relay loads
    "ignition_voltage": 12.0,      # Must be present to wake PCM
}


# =============================================================================
#  MINIMUM SENSOR SET TO BOOT PCM (Phase 1 bench)
#  With these 3 simulated + power, PCM boots with minimal DTCs
# =============================================================================
MINIMUM_BOOT_SENSORS = {
    "CTS": {
        "pin_ref": "C2_01",        # ⚠ UNVERIFIED
        "sim_method": "resistor",
        "value": "2.5kΩ to ground",
        "simulates": "~80°C coolant (warm engine)",
    },
    "TPS": {
        "pin_ref": "C2_05",        # ⚠ UNVERIFIED
        "sim_method": "voltage_divider",
        "value": "0.5V (closed throttle)",
        "simulates": "Idle position",
    },
    "MAP": {
        "pin_ref": "C2_08",        # ⚠ UNVERIFIED
        "sim_method": "voltage_divider",
        "value": "1.5V",
        "simulates": "Normal idle vacuum (~50 kPa)",
    },
}


# =============================================================================
#  HC11F1 MEMORY MAP (these are from the datasheet — correct)
# =============================================================================
HC11_MEMORY = {
    "ram_start":    0x0000,
    "ram_end":      0x03FF,    # 1KB internal RAM
    "registers":    0x1000,    # I/O register block base (CONFIG dependent)
    "eeprom_start": 0xFE00,
    "eeprom_end":   0xFFFF,
    "rom_start":    0x8000,    # External ROM/Flash
    "rom_end":      0xFDFF,

    # VY V6 $060A specific
    "calibration_id": "$060A",
    "free_space_start": 0x5D00,  # Usable for custom code
    "reset_vector":    0xFFFE,
    "sci_vector":      0xFFD6,
}


# =============================================================================
#  HC11F1 I/O REGISTER ADDRESSES (from MC68HC11F1 datasheet — correct)
# =============================================================================
HC11_REGISTERS = {
    "PORTA":  0x1000,  # Port A data register
    "PORTB":  0x1004,  # Port B data register (output only)
    "PORTC":  0x1003,  # Port C data register
    "PORTD":  0x1008,  # Port D data register (SCI/SPI)
    "PORTE":  0x100A,  # Port E data register (ADC inputs)

    "DDRC":   0x1007,  # Data direction register C
    "DDRD":   0x1009,  # Data direction register D

    # SCI (Serial Communications Interface) — used for ALDL
    "BAUD":   0x102B,  # SCI baud rate register
    "SCCR1":  0x102C,  # SCI control register 1
    "SCCR2":  0x102D,  # SCI control register 2
    "SCSR":   0x102E,  # SCI status register
    "SCDR":   0x102F,  # SCI data register

    # Timer
    "TCNT":   0x100E,  # Free-running counter (16-bit)
    "TFLG1":  0x1023,  # Timer interrupt flag 1
    "TFLG2":  0x1025,  # Timer interrupt flag 2
    "TMSK1":  0x1022,  # Timer interrupt mask 1
    "TMSK2":  0x1024,  # Timer interrupt mask 2
    "TCTL1":  0x1020,  # Timer control 1 (OC1-OC5)
    "TCTL2":  0x1021,  # Timer control 2 (IC1-IC3 edge)

    # ADC
    "ADCTL":  0x1030,  # ADC control/status
    "ADR1":   0x1031,  # ADC result 1
    "ADR2":   0x1032,  # ADC result 2
    "ADR3":   0x1033,  # ADC result 3
    "ADR4":   0x1034,  # ADC result 4

    # System
    "CONFIG": 0x103F,  # System configuration register
    "INIT":   0x103D,  # RAM/register map position
    "OPTION": 0x1039,  # System configuration options
    "HPRIO":  0x103C,  # Highest priority I-bit interrupt
}


# =============================================================================
#  PORTB BIT ASSIGNMENTS — Output functions (ALDL Mode 4 controlled)
#  ⚠ UNVERIFIED bit-to-function mapping — verify against $060A disassembly
# =============================================================================
PORTB_BITS = {
    0: {"function": "Fan low relay",        "active": "high", "verified": False},
    1: {"function": "Fan high relay",       "active": "high", "verified": False},
    2: {"function": "A/C clutch relay",     "active": "high", "verified": False},
    3: {"function": "CEL (check engine)",   "active": "high", "verified": False},
    4: {"function": "Fuel pump relay",      "active": "high", "verified": False},
    5: {"function": "TCC solenoid",         "active": "high", "verified": False},
    6: {"function": "EGR solenoid",         "active": "high", "verified": False},
    7: {"function": "Unused / spare",       "active": "high", "verified": False},
}


# =============================================================================
#  MODE 4 COMMAND BYTE OFFSETS
#  Based on VX-VY Mode 4 definition (pcmhacking.net topic 2460)
#  These are protocol-level and likely correct, but verify against oracle files
# =============================================================================
MODE4_OFFSETS = {
    "discrete_outputs":   3,   # Byte 3 — injector kill bits + discrete enables
    "injector_kill_mask":  3,   # Byte 3 bits 0-5 = injectors 1-6
    "fan_control":         4,   # Byte 4 — fan/relay override byte
    "clear_dtc":           5,   # Byte 5 — DTC control
    "iac_position":       14,   # Byte 14 — IAC motor position override
    "afr_command":        15,   # Byte 15 — AFR/fuel command (0x93 = 14.7:1)
    "spark_advance":      16,   # Byte 16 — spark advance override
    "rpm_limit":          17,   # Byte 17 — RPM limiter override
}


# =============================================================================
#  MODE 1 DATA STREAM OFFSETS
#  Byte positions in Mode 1 response for VY V6 $060A
#  ⚠ Some offsets may vary by calibration — verify against data stream def
# =============================================================================
MODE1_OFFSETS = {
    "rpm_high":     0,    # RPM high byte
    "rpm_low":      1,    # RPM low byte (RPM = (hi*256 + lo) / 40 ?)
    "tps_raw":      2,    # TPS ADC value (0-255)
    "map_raw":      3,    # MAP ADC value
    "coolant_raw":  5,    # CTS ADC value (lookup table for °C)
    "iat_raw":      6,    # IAT ADC value
    "o2_bank1":     7,    # O2 sensor voltage (0-255 → 0-1.275V)
    "spark_adv":    8,    # Current spark advance
    "battery_v":    9,    # Battery voltage (V = raw * 0.1)
    "iac_steps":   10,    # IAC motor position (steps)
    "injector_pw": 11,    # Injector pulse width
    "vehicle_spd": 15,    # Vehicle speed
    "dtc_byte1":   20,    # DTC flag byte 1
    "dtc_byte2":   21,    # DTC flag byte 2
}


# =============================================================================
#  CRANK SIGNAL PARAMETERS (VY V6 L36 3.8L)
# =============================================================================
CRANK_SIGNAL = {
    "pulses_3x_per_rev":  3,    # 3X DES (dual edge sensing) — 3 pulses/rev
    "pulses_18x_per_rev": 18,   # 18X CKP — 18 pulses/rev
    "signal_type": "reluctor_square_wave",
    "amplitude_v": 12.0,        # Through driver — verify actual voltage
    "min_rpm": 200,             # Cranking speed
    "max_rpm": 6500,            # Rev limiter
    "idle_rpm": 800,            # Target idle
}

# Pre-calculated pulse frequencies at common RPMs
CRANK_FREQ_TABLE = {
    #  RPM: (3X_Hz, 18X_Hz)
     200: (10.0,   60.0),
     400: (20.0,  120.0),
     600: (30.0,  180.0),
     800: (40.0,  240.0),
    1000: (50.0,  300.0),
    1500: (75.0,  450.0),
    2000: (100.0, 600.0),
    2500: (125.0, 750.0),
    3000: (150.0, 900.0),
    3500: (175.0, 1050.0),
    4000: (200.0, 1200.0),
    4500: (225.0, 1350.0),
    5000: (250.0, 1500.0),
    5500: (275.0, 1650.0),
    6000: (300.0, 1800.0),
    6500: (325.0, 1950.0),
}


def crank_freq(rpm: int, pulses_per_rev: int = 3) -> float:
    """Calculate crank pulse frequency in Hz for given RPM."""
    return (rpm / 60.0) * pulses_per_rev


def get_unverified_pins() -> list[str]:
    """Return list of all pin IDs that haven't been verified yet."""
    unverified = []
    for name, pins in [("C1", C1_PINS), ("C2", C2_PINS), ("C3", C3_PINS)]:
        for pin_id, info in pins.items():
            if not info.get("verified", False):
                unverified.append(f"{pin_id}: {info['function']}")
    return unverified


def print_verification_status():
    """Print summary of pin verification status."""
    total = 0
    confirmed = 0
    for pins in [C1_PINS, C2_PINS, C3_PINS]:
        for info in pins.values():
            total += 1
            if info.get("verified", False):
                confirmed += 1

    print(f"Pin verification: {confirmed}/{total} confirmed")
    if confirmed < total:
        print(f"⚠ {total - confirmed} pins still UNVERIFIED — do NOT wire to real hardware!")
        for pin in get_unverified_pins():
            print(f"  [ ] {pin}")
    else:
        print("✓ All pins verified — safe to wire.")


if __name__ == "__main__":
    print_verification_status()
