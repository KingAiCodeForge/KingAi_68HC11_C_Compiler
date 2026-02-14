"""
HC11 Virtual Emulator — CPU Register Set + CCR Flag Management

SCAFFOLD — needs cross-referencing against:
  - tonypdmtr/EVBU PySim11/state.py (ucState class)
  - Motorola HC11 Reference Manual Section 6 (CPU registers)
  - hc11_compiler/assembler.py (flag update patterns in codegen)

Register model for 68HC11:
  A   — 8-bit accumulator A
  B   — 8-bit accumulator B
  D   — 16-bit (A:B concatenation, A=high, B=low)
  X   — 16-bit index register
  Y   — 16-bit index register (0x18 prefix instructions)
  SP  — 16-bit stack pointer (grows downward)
  PC  — 16-bit program counter
  CCR — 8-bit condition code register: S X H I N Z V C
        bit 7: S (Stop disable)
        bit 6: X (XIRQ mask — can be cleared but NOT set by software)
        bit 5: H (Half carry — BCD operations)
        bit 4: I (IRQ mask)
        bit 3: N (Negative — MSB of result)
        bit 2: Z (Zero — result is zero)
        bit 1: V (Overflow — signed overflow)
        bit 0: C (Carry — unsigned overflow)
"""

# CCR bit masks
CC_S = 0x80
CC_X = 0x40
CC_H = 0x20
CC_I = 0x10
CC_N = 0x08
CC_Z = 0x04
CC_V = 0x02
CC_C = 0x01


class Registers:
    """68HC11 CPU register set.
    
    SCAFFOLD: Structure validated against EVBU PySim11/state.py.
    CCR flag semantics match HC11 Reference Manual Section 6.7.
    """
    
    __slots__ = ('A', 'B', 'X', 'Y', 'SP', 'PC', 'CC', 'cycles')
    
    def __init__(self):
        self.A: int = 0       # Accumulator A (8-bit)
        self.B: int = 0       # Accumulator B (8-bit)
        self.X: int = 0       # Index register X (16-bit)
        self.Y: int = 0       # Index register Y (16-bit)
        self.SP: int = 0x01FF # Stack pointer — top of internal RAM
        self.PC: int = 0      # Program counter (16-bit)
        self.CC: int = 0xD0   # CCR: S=1, X=1, I=1 (interrupts masked at reset)
        self.cycles: int = 0  # E-clock cycle counter
    
    # --- 16-bit D register (A:B concatenation) ---
    
    @property
    def D(self) -> int:
        """Read D register = (A << 8) | B"""
        return (self.A << 8) | self.B
    
    @D.setter
    def D(self, value: int):
        """Write D register → splits into A (high) and B (low)"""
        value &= 0xFFFF
        self.A = (value >> 8) & 0xFF
        self.B = value & 0xFF
    
    # --- CCR flag access ---
    
    def set_HNZVC(self, flags: int):
        """Set H, N, Z, V, C flags (bits 5, 3-0). Preserves S, X, I."""
        self.CC = (self.CC & 0xD0) | (flags & 0x2F)
    
    def set_NZVC(self, flags: int):
        """Set N, Z, V, C flags (bits 3-0). Preserves S, X, H, I."""
        self.CC = (self.CC & 0xF0) | (flags & 0x0F)
    
    def set_NZV(self, flags: int):
        """Set N, Z, V flags (bits 3-1). Preserves S, X, H, I, C."""
        self.CC = (self.CC & 0xF1) | (flags & 0x0E)
    
    def set_ZVC(self, flags: int):
        """Set Z, V, C flags (bits 2-0). Preserves S, X, H, I, N."""
        self.CC = (self.CC & 0xF8) | (flags & 0x07)
    
    def set_C(self, flags: int):
        """Set C flag only."""
        self.CC = (self.CC & 0xFE) | (flags & 0x01)
    
    def set_Z(self, flags: int):
        """Set Z flag only."""
        self.CC = (self.CC & 0xFB) | (flags & 0x04)
    
    def set_I(self, flags: int):
        """Set I flag."""
        self.CC = (self.CC & 0xEF) | (flags & 0x10)
    
    def set_V(self, flags: int):
        """Set V flag only."""
        self.CC = (self.CC & 0xFD) | (flags & 0x02)
    
    def set_X_bit(self, flags: int):
        """Set X bit — CRITICAL: X can be cleared but NOT set by software.
        Must AND with current value (can only go 1→0, never 0→1).
        Reference: HC11 RM Section 6.7, EVBU ops.py RTI handler.
        """
        self.CC = (self.CC & 0xBF) | (flags & self.CC & CC_X)
    
    @property
    def carry(self) -> bool:
        return bool(self.CC & CC_C)
    
    @property
    def zero(self) -> bool:
        return bool(self.CC & CC_Z)
    
    @property
    def negative(self) -> bool:
        return bool(self.CC & CC_N)
    
    @property
    def overflow(self) -> bool:
        return bool(self.CC & CC_V)
    
    @property
    def irq_masked(self) -> bool:
        return bool(self.CC & CC_I)
    
    @property
    def half_carry(self) -> bool:
        return bool(self.CC & CC_H)
    
    # --- Stack operations ---
    
    def push8(self, memory, value: int):
        """Push 8-bit value onto stack (SP decrements after write)."""
        memory.write8(self.SP, value & 0xFF)
        self.SP = (self.SP - 1) & 0xFFFF
    
    def push16(self, memory, value: int):
        """Push 16-bit value onto stack (low byte first, then high)."""
        memory.write8(self.SP, value & 0xFF)        # low byte at SP
        memory.write8(self.SP - 1, (value >> 8) & 0xFF)  # high byte at SP-1
        self.SP = (self.SP - 2) & 0xFFFF
    
    def pull8(self, memory) -> int:
        """Pull 8-bit value from stack (SP increments before read)."""
        self.SP = (self.SP + 1) & 0xFFFF
        return memory.read8(self.SP)
    
    def pull16(self, memory) -> int:
        """Pull 16-bit value from stack (high byte at SP+1, low at SP+2)."""
        hi = self.pull8(memory)
        lo = self.pull8(memory)
        return (hi << 8) | lo
    
    # --- Display ---
    
    def display(self) -> str:
        """Format register state for debugging (matches EVBU format)."""
        ccr_chars = []
        for i, c in enumerate('SXHINZVC'):
            if self.CC & (0x80 >> i):
                ccr_chars.append(c)
            else:
                ccr_chars.append('.')
        ccr_str = ''.join(ccr_chars)
        return (f"PC={self.PC:04X} A={self.A:02X} B={self.B:02X} "
                f"D={self.D:04X} X={self.X:04X} Y={self.Y:04X} "
                f"SP={self.SP:04X} CCR={self.CC:02X} [{ccr_str}]")
    
    def reset(self):
        """Reset CPU to power-on state."""
        self.A = 0
        self.B = 0
        self.X = 0
        self.Y = 0
        self.SP = 0x01FF  # Top of internal RAM (HC11F1)
        self.CC = 0xD0    # S=1, X=1, I=1 — interrupts masked
        self.PC = 0       # Will be loaded from reset vector $FFFE-$FFFF
        self.cycles = 0
