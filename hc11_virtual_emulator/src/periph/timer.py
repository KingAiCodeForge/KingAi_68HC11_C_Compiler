"""
HC11 Virtual Emulator — Timer Peripheral

SCAFFOLD — needs cross-referencing against:
  - Motorola MC68HC11F1 Technical Data Section 10 (Timer chapter)
  - examples/timer_delay.c, pulse_counter.c (timer usage)

Emulates the HC11 free-running timer and output compare system.
The timer is important for:
  - Delay loops in boot sequences
  - Pulse width measurement (crank sensing in stock OS)
  - ISR-driven timing events

Register map (subset):
  $100E-$100F  TCNT   — 16-bit free-running counter (read-only)
  $1016-$1017  TOC1   — Output Compare 1
  $1018-$1019  TOC2   — Output Compare 2
  $101A-$101B  TOC3   — Output Compare 3
  $101C-$101D  TOC4   — Output Compare 4
  $101E-$101F  TOC5   — Output Compare 5
  $1023         TFLG1  — Output compare flags (write 1 to clear)
  $1024         TMSK2  — Timer prescaler
  $1025         TFLG2  — Timer overflow flag
  $1026         PACTL  — Pulse accumulator control
  $1027         PACNT  — Pulse accumulator count
"""


# Timer register addresses
TCNT_H = 0x100E
TCNT_L = 0x100F
TOC1_H = 0x1016
TOC1_L = 0x1017
TOC2_H = 0x1018
TOC2_L = 0x1019
TOC3_H = 0x101A
TOC3_L = 0x101B
TOC4_H = 0x101C
TOC4_L = 0x101D
TOC5_H = 0x101E
TOC5_L = 0x101F
TFLG1  = 0x1023
TMSK2  = 0x1024
TFLG2  = 0x1025
PACTL  = 0x1026
PACNT  = 0x1027

# TFLG1 bits
OC1F = 0x80
OC2F = 0x40
OC3F = 0x20
OC4F = 0x10
OC5F = 0x08

# TFLG2 bits
TOF  = 0x80  # Timer Overflow Flag


class TimerPeripheral:
    """Free-running timer + output compare model.
    
    SCAFFOLD: Basic TCNT counter that increments per E-clock cycle.
    Output compare flag setting needs validation against real timing.
    
    Timer prescaler (TMSK2 bits PR1:PR0):
      00 = ÷1  (E-clock)
      01 = ÷4
      10 = ÷8
      11 = ÷16
    
    At 2.097152 MHz E-clock, TCNT overflows every:
      ÷1  → 31.25 ms
      ÷4  → 125 ms
      ÷8  → 250 ms
      ÷16 → 500 ms
    """
    
    def __init__(self):
        self._tcnt = 0x0000         # 16-bit free counter
        self._toc = [0xFFFF] * 5    # OC1-OC5
        self._tflg1 = 0x00
        self._tflg2 = 0x00
        self._tmsk2 = 0x00
        self._pactl = 0x00
        self._pacnt = 0x00
        self._prescaler = 1
        self._sub_count = 0         # Sub-prescaler counter
    
    def register(self, memory):
        """Register timer I/O handlers."""
        memory.register_io_handler(TCNT_H, self._read_tcnt_h, None)
        memory.register_io_handler(TCNT_L, self._read_tcnt_l, None)
        memory.register_io_handler(TFLG1,  self._read_tflg1,  self._write_tflg1)
        memory.register_io_handler(TFLG2,  self._read_tflg2,  self._write_tflg2)
        memory.register_io_handler(TMSK2,  self._read_tmsk2,  self._write_tmsk2)
        memory.register_io_handler(PACTL,  self._read_pactl,  self._write_pactl)
        memory.register_io_handler(PACNT,  self._read_pacnt,  self._write_pacnt)
        
        # Output compare registers (read/write)
        for i, (h, l) in enumerate([(TOC1_H, TOC1_L), (TOC2_H, TOC2_L),
                                      (TOC3_H, TOC3_L), (TOC4_H, TOC4_L),
                                      (TOC5_H, TOC5_L)]):
            idx = i  # capture for closure
            memory.register_io_handler(h, lambda a, i=idx: (self._toc[i] >> 8) & 0xFF,
                                          lambda a, v, i=idx: self._write_toc_h(i, v))
            memory.register_io_handler(l, lambda a, i=idx: self._toc[i] & 0xFF,
                                          lambda a, v, i=idx: self._write_toc_l(i, v))
    
    def _read_tcnt_h(self, addr: int) -> int:
        return (self._tcnt >> 8) & 0xFF
    
    def _read_tcnt_l(self, addr: int) -> int:
        return self._tcnt & 0xFF
    
    def _read_tflg1(self, addr: int) -> int:
        return self._tflg1
    
    def _write_tflg1(self, addr: int, value: int):
        """Write 1 bits to TFLG1 to CLEAR those flags (HC11 convention)."""
        self._tflg1 &= ~value & 0xFF
    
    def _read_tflg2(self, addr: int) -> int:
        return self._tflg2
    
    def _write_tflg2(self, addr: int, value: int):
        """Write 1 bits to TFLG2 to CLEAR those flags."""
        self._tflg2 &= ~value & 0xFF
    
    def _read_tmsk2(self, addr: int) -> int:
        return self._tmsk2
    
    def _write_tmsk2(self, addr: int, value: int):
        self._tmsk2 = value & 0xFF
        pr = value & 0x03
        self._prescaler = [1, 4, 8, 16][pr]
    
    def _read_pactl(self, addr: int) -> int:
        return self._pactl
    
    def _write_pactl(self, addr: int, value: int):
        self._pactl = value & 0xFF
    
    def _read_pacnt(self, addr: int) -> int:
        return self._pacnt
    
    def _write_pacnt(self, addr: int, value: int):
        self._pacnt = value & 0xFF
    
    def _write_toc_h(self, index: int, value: int):
        self._toc[index] = (value << 8) | (self._toc[index] & 0xFF)
    
    def _write_toc_l(self, index: int, value: int):
        self._toc[index] = (self._toc[index] & 0xFF00) | (value & 0xFF)
    
    def update(self, elapsed_cycles: int):
        """Advance timer by elapsed_cycles E-clock cycles.
        
        Called after each instruction execution. Updates TCNT and
        checks for output compare matches and timer overflow.
        """
        self._sub_count += elapsed_cycles
        ticks = self._sub_count // self._prescaler
        self._sub_count %= self._prescaler
        
        for _ in range(ticks):
            old_tcnt = self._tcnt
            self._tcnt = (self._tcnt + 1) & 0xFFFF
            
            # Check for timer overflow
            if self._tcnt == 0 and old_tcnt == 0xFFFF:
                self._tflg2 |= TOF
            
            # Check output compare matches
            oc_flags = [OC1F, OC2F, OC3F, OC4F, OC5F]
            for i in range(5):
                if self._tcnt == self._toc[i]:
                    self._tflg1 |= oc_flags[i]
    
    def reset(self):
        """Reset timer state."""
        self._tcnt = 0x0000
        self._toc = [0xFFFF] * 5
        self._tflg1 = 0x00
        self._tflg2 = 0x00
        self._tmsk2 = 0x00
        self._pactl = 0x00
        self._pacnt = 0x00
        self._prescaler = 1
        self._sub_count = 0
