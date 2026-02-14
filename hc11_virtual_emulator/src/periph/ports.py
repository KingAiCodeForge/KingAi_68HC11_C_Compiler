"""
HC11 Virtual Emulator — I/O Ports Peripheral

SCAFFOLD — needs cross-referencing against:
  - Motorola MC68HC11F1 Technical Data Section 7 (Parallel I/O)
  - examples/blink.c, fan_control.c (PORTB usage)
  - Stock $060A binary port initialization

Emulates HC11 parallel I/O ports for output state tracking.
PORTB is the most important — it drives discrete outputs (fan relay,
fuel pump, CEL, etc.) on the VY V6 PCM.

Register map:
  $1000  PORTA  — Port A data (bidirectional, some timer-related)
  $1003  PORTC  — Port C data (bidirectional)
  $1004  PORTB  — Port B data (OUTPUT ONLY on HC11F1)
  $1007  DDRC   — Port C data direction register
  $1008  PORTD  — Port D data (SPI alternate)
  $1009  DDRD   — Port D data direction register
  $100A  PORTE  — Port E data (INPUT ONLY — ADC alternate)
"""


class PortsPeripheral:
    """Parallel I/O ports model.
    
    SCAFFOLD: Tracks port state for inspection. No pin-level emulation.
    
    For bench testing cross-validation:
      - PORTB bit 0 = Fan relay HIGH
      - PORTB bit 1 = Fuel pump relay
      - PORTB bit 4 = CEL (Check Engine Light)
      - See VY V6 service manual wiring diagrams for full pinout
    
    Port change callbacks allow test harness to watch for state changes:
      ports.on_change(0x1004, lambda addr, old, new: print(f"PORTB: {new:08b}"))
    """
    
    # Port addresses
    PORTA = 0x1000
    PORTC = 0x1003
    PORTB = 0x1004
    DDRC  = 0x1007
    PORTD = 0x1008
    DDRD  = 0x1009
    PORTE = 0x100A
    
    def __init__(self):
        self._ports = {
            self.PORTA: 0x00,
            self.PORTB: 0x00,
            self.PORTC: 0x00,
            self.PORTD: 0x00,
            self.PORTE: 0x00,
            self.DDRC:  0x00,
            self.DDRD:  0x00,
        }
        self._change_callbacks = {}
    
    def register(self, memory):
        """Register I/O handlers for all port addresses."""
        for addr in self._ports:
            if addr == self.PORTE:
                # Port E is input only — no write handler
                memory.register_io_handler(addr, self._read_port, None)
            else:
                memory.register_io_handler(addr, self._read_port, self._write_port)
    
    def _read_port(self, addr: int) -> int:
        return self._ports.get(addr, 0x00)
    
    def _write_port(self, addr: int, value: int):
        old = self._ports.get(addr, 0x00)
        self._ports[addr] = value & 0xFF
        
        if addr in self._change_callbacks and old != value:
            for cb in self._change_callbacks[addr]:
                cb(addr, old, value & 0xFF)
    
    # --- External API ---
    
    def get_port(self, addr: int) -> int:
        """Read current port value."""
        return self._ports.get(addr, 0x00)
    
    def set_input(self, addr: int, value: int):
        """Set input port value (for PORTE simulation)."""
        self._ports[addr] = value & 0xFF
    
    def on_change(self, addr: int, callback):
        """Register a callback for port value changes.
        
        callback(addr, old_value, new_value) is called on any write
        that changes the port value.
        """
        if addr not in self._change_callbacks:
            self._change_callbacks[addr] = []
        self._change_callbacks[addr].append(callback)
    
    def get_portb_bits(self) -> dict:
        """Decode PORTB into named output states (VY V6 specific).
        
        SCAFFOLD: Bit assignments need confirmation from VY V6 service manual.
        These are approximate from PCMHacking Mode 4 documentation.
        """
        portb = self._ports.get(self.PORTB, 0x00)
        return {
            'fan_relay':    bool(portb & 0x01),
            'fuel_pump':    bool(portb & 0x02),
            'ac_clutch':    bool(portb & 0x04),
            'tcc_solenoid': bool(portb & 0x08),
            'cel_lamp':     bool(portb & 0x10),
            'shift_a':      bool(portb & 0x20),
            'shift_b':      bool(portb & 0x40),
            'reserved':     bool(portb & 0x80),
        }
    
    def reset(self):
        """Reset all ports to zero."""
        for addr in self._ports:
            self._ports[addr] = 0x00
