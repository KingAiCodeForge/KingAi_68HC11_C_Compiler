"""
HC11 Virtual Emulator — ADC Peripheral

SCAFFOLD — needs cross-referencing against:
  - Motorola MC68HC11F1 Technical Data Section 12 (ADC chapter)
  - examples/adc_read.c, fan_control.c (ADC usage patterns)

Emulates the HC11 A/D converter for sensor injection testing.
The ADC is critical for DTC reverse engineering (inject fault values,
observe RAM changes) and fan_control.c validation.

Register map:
  $1030  ADCTL  — A/D control/status (write starts conversion, bit 7 = CCF)
  $1031  ADR1   — A/D result register 1 (channel depends on ADCTL)
  $1032  ADR2   — A/D result register 2
  $1033  ADR3   — A/D result register 3
  $1034  ADR4   — A/D result register 4

Simplifications:
  - Conversions complete instantly (CCF set on next read of ADCTL)
  - Channel selection from ADCTL bits 3:0 maps to injected values
  - No scan mode / multi-channel behavior (single conversion only)
"""


# ADC register addresses
ADCTL = 0x1030
ADR1  = 0x1031
ADR2  = 0x1032
ADR3  = 0x1033
ADR4  = 0x1034

# ADCTL bits
CCF   = 0x80  # Conversion Complete Flag (bit 7)
SCAN  = 0x20  # Continuous Scan (bit 5)
MULT  = 0x10  # Multiple Channel (bit 4)
# Bits 3:0 = channel select (CD-CA)


class ADCPeripheral:
    """A/D Converter peripheral model.
    
    SCAFFOLD: Register behavior validated against HC11F1 datasheet.
    Sensor values are pre-loaded via set_channel() for testing.
    
    For DTC testing:
      - set_channel(5, 0xFF) → simulate CTS open circuit
      - set_channel(3, 0x00) → simulate TPS ground short
      - Run emulator, diff RAM snapshots to find DTC bitfield locations
    
    VY V6 ADC channel assignments (from stock XDF):
      CH0 = MAP sensor          CH4 = O2 sensor
      CH1 = MAT (air temp)      CH5 = CTS (coolant temp)
      CH2 = TPS (throttle)      CH6 = Battery voltage
      CH3 = Knock sensor        CH7 = EGR / unused
    """
    
    def __init__(self):
        self._adctl = 0x00
        self._channels = [0x80] * 8  # Default: mid-range for all channels
        self._adr = [0x80] * 4       # Result registers
        self._conversion_done = False
    
    def register(self, memory):
        """Register I/O handlers with the memory system."""
        memory.register_io_handler(ADCTL, self._read_adctl, self._write_adctl)
        memory.register_io_handler(ADR1,  self._read_adr1, None)
        memory.register_io_handler(ADR2,  self._read_adr2, None)
        memory.register_io_handler(ADR3,  self._read_adr3, None)
        memory.register_io_handler(ADR4,  self._read_adr4, None)
    
    def _read_adctl(self, addr: int) -> int:
        """Read ADCTL — returns channel select + CCF if conversion done."""
        val = self._adctl & 0x3F  # Preserve control bits
        if self._conversion_done:
            val |= CCF
        return val
    
    def _write_adctl(self, addr: int, value: int):
        """Write ADCTL — starts A/D conversion.
        
        Channel select bits 3:0 determine which channel(s) to convert.
        In real hardware, conversion takes 32 E-clock cycles.
        In emulator, result is available instantly.
        """
        self._adctl = value & 0xFF
        self._conversion_done = False
        
        # Determine channel(s) and load results
        base_ch = self._adctl & 0x07
        if self._adctl & MULT:
            # Multi-channel: convert 4 channels starting at base_ch & 0x04
            group_base = base_ch & 0x04
            for i in range(4):
                ch = (group_base + i) & 0x07
                self._adr[i] = self._channels[ch]
        else:
            # Single channel: all 4 ADR registers get the same channel
            for i in range(4):
                self._adr[i] = self._channels[base_ch]
        
        # Instant completion
        self._conversion_done = True
    
    def _read_adr1(self, addr: int) -> int:
        return self._adr[0]
    
    def _read_adr2(self, addr: int) -> int:
        return self._adr[1]
    
    def _read_adr3(self, addr: int) -> int:
        return self._adr[2]
    
    def _read_adr4(self, addr: int) -> int:
        return self._adr[3]
    
    # --- External API ---
    
    def set_channel(self, channel: int, value: int):
        """Set the virtual sensor value for an ADC channel (0-7, 0-255).
        
        Call before running emulator to inject sensor readings.
        """
        if 0 <= channel <= 7:
            self._channels[channel] = value & 0xFF
    
    def set_sensors_normal(self):
        """Load typical "engine off, key on" sensor values.
        
        SCAFFOLD: Values need cross-referencing against VY V6 stock XDF
        conversion formulas and actual sensor readings.
        """
        self._channels[0] = 0x55  # MAP: ~100 kPa (atmospheric, engine off)
        self._channels[1] = 0x80  # MAT: ~25°C
        self._channels[2] = 0x1A  # TPS: ~0.5V (closed throttle)
        self._channels[3] = 0x00  # Knock: no knock
        self._channels[4] = 0x80  # O2: ~0.45V (stoich)
        self._channels[5] = 0x50  # CTS: ~80°C (2.5K thermistor)
        self._channels[6] = 0x8C  # Battery: ~14.0V
        self._channels[7] = 0x00  # EGR/unused
    
    def reset(self):
        """Reset ADC state."""
        self._adctl = 0x00
        self._adr = [0x80] * 4
        self._conversion_done = False
