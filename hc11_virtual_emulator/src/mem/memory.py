"""
HC11 Virtual Emulator — 64K Memory Map with Region Routing

SCAFFOLD — needs cross-referencing against:
  - Motorola MC68HC11F1 Technical Data (1990) — memory map chapter
  - hc11_compiler/assembler.py — EQU addresses for I/O registers
  - Stock $060A binary — verify ROM/RAM layout matches

Memory map for HC11F1 (VY V6 PCM variant):
  $0000–$03FF  Internal RAM (1024 bytes)
  $1000–$103F  I/O Registers (64 bytes) — routed to peripheral models
  $4000–$7FFF  External RAM / unused (PCM-specific)
  $8000–$BFFF  ROM Bank 1 (calibration data — tune)
  $C000–$FDFF  ROM Bank 2 (OS code)
  $FE00–$FFBF  Internal EEPROM (512 bytes)
  $FFC0–$FFFF  Interrupt Vectors (32 vectors × 2 bytes)

Note: The HC11F1 in the Delco PCM uses a 128KB address space with bank
switching for the full ROM. For emulator MVP, we model the flat 64K map.
Bank switching support is a Phase 2 addition.
"""

from typing import Optional, Callable, Dict, List
from pathlib import Path


class MemoryRegion:
    """A named region in the 64K address space."""
    def __init__(self, name: str, start: int, end: int, 
                 writable: bool = True, initial: int = 0x00):
        self.name = name
        self.start = start
        self.end = end  # inclusive
        self.writable = writable
        self.initial = initial
    
    def contains(self, addr: int) -> bool:
        return self.start <= addr <= self.end
    
    @property
    def size(self) -> int:
        return self.end - self.start + 1


class Memory:
    """64K byte-addressable memory with region routing.
    
    SCAFFOLD: Region layout validated against HC11F1 datasheet.
    I/O register routing is stubbed — peripheral models will be
    registered via register_io_handler() and called on R/W.
    Watchpoint support is stubbed for future DTC reverse engineering.
    
    Memory is flat (bytearray), with I/O register reads/writes
    intercepted and routed to peripheral handler callbacks.
    """
    
    # HC11F1 Memory Regions (VY V6 PCM layout)
    REGIONS = [
        MemoryRegion('RAM',     0x0000, 0x03FF, writable=True,  initial=0x00),
        MemoryRegion('IO',      0x1000, 0x103F, writable=True,  initial=0x00),
        MemoryRegion('EXTRAM',  0x0400, 0x0FFF, writable=True,  initial=0x00),
        MemoryRegion('ROM1',    0x8000, 0xBFFF, writable=False, initial=0xFF),
        MemoryRegion('ROM2',    0xC000, 0xFDFF, writable=False, initial=0xFF),
        MemoryRegion('EEPROM',  0xFE00, 0xFFBF, writable=True,  initial=0xFF),
        MemoryRegion('VECTORS', 0xFFC0, 0xFFFF, writable=False, initial=0xFF),
    ]
    
    def __init__(self):
        self._mem = bytearray(0x10000)  # 64K flat address space
        
        # I/O register handlers: addr → (read_fn, write_fn)
        # read_fn(addr) -> int, write_fn(addr, value) -> None
        self._io_read_handlers: Dict[int, Callable] = {}
        self._io_write_handlers: Dict[int, Callable] = {}
        
        # Watchpoints: addr → callback(addr, old_val, new_val, is_write)
        self._watchpoints: Dict[int, List[Callable]] = {}
        
        # Initialize regions to their default values
        for region in self.REGIONS:
            for addr in range(region.start, region.end + 1):
                self._mem[addr] = region.initial
    
    # --- Core read/write ---
    
    def read8(self, addr: int) -> int:
        """Read 8-bit value from address.
        
        If address is in I/O region ($1000–$103F) and a handler is
        registered, the handler is called instead of raw memory read.
        """
        addr &= 0xFFFF
        
        # I/O register intercept
        if 0x1000 <= addr <= 0x103F and addr in self._io_read_handlers:
            return self._io_read_handlers[addr](addr) & 0xFF
        
        return self._mem[addr]
    
    def write8(self, addr: int, value: int):
        """Write 8-bit value to address.
        
        If address is in I/O region and a handler is registered, the 
        handler is called. ROM writes are silently ignored (matches HW).
        Watchpoint callbacks fire on any write.
        """
        addr &= 0xFFFF
        value &= 0xFF
        old = self._mem[addr]
        
        # Watchpoint notification
        if addr in self._watchpoints:
            for cb in self._watchpoints[addr]:
                cb(addr, old, value, True)
        
        # I/O register intercept
        if 0x1000 <= addr <= 0x103F:
            self._mem[addr] = value  # always update raw mem for inspection
            if addr in self._io_write_handlers:
                self._io_write_handlers[addr](addr, value)
            return
        
        # ROM write protection (silent drop — matches real HW behavior)
        if 0x8000 <= addr <= 0xFDFF or 0xFFC0 <= addr <= 0xFFFF:
            return
        
        self._mem[addr] = value
    
    def read16(self, addr: int) -> int:
        """Read 16-bit value (big-endian, HC11 native byte order)."""
        hi = self.read8(addr)
        lo = self.read8(addr + 1)
        return (hi << 8) | lo
    
    def write16(self, addr: int, value: int):
        """Write 16-bit value (big-endian)."""
        self.write8(addr, (value >> 8) & 0xFF)
        self.write8(addr + 1, value & 0xFF)
    
    # --- Bulk load ---
    
    def load_binary(self, data: bytes, base_addr: int):
        """Load binary data into memory at base_addr.
        
        Bypasses write protection — used for loading ROM images.
        """
        for i, byte in enumerate(data):
            addr = (base_addr + i) & 0xFFFF
            self._mem[addr] = byte
    
    def load_s19(self, s19_text: str):
        """Load Motorola S19 records into memory.
        
        SCAFFOLD — needs cross-referencing against:
          - hc11_compiler/assembler.py s19 output format
          - S19 format spec (Wayne State reference)
        
        Parses S1 records (16-bit address), ignores S0/S9.
        Bypasses write protection (ROM loading).
        """
        for line in s19_text.strip().split('\n'):
            line = line.strip()
            if not line or not line.startswith('S'):
                continue
            
            rec_type = line[0:2]
            
            if rec_type == 'S1':
                # S1 LL AAAA DD DD DD ... CC
                byte_count = int(line[2:4], 16)
                addr = int(line[4:8], 16)
                # Data bytes: from position 8 to -(checksum 2 chars)
                data_hex = line[8:8 + (byte_count - 3) * 2]
                for i in range(0, len(data_hex), 2):
                    self._mem[(addr + i // 2) & 0xFFFF] = int(data_hex[i:i+2], 16)
            # S0 = header, S9 = termination — skip
    
    # --- I/O handler registration ---
    
    def register_io_handler(self, addr: int, 
                            read_fn: Optional[Callable] = None,
                            write_fn: Optional[Callable] = None):
        """Register read/write handlers for an I/O register address.
        
        Peripheral models (SCI, ADC, Timer, etc.) call this to intercept
        reads/writes to their registers.
        
        Args:
            addr: I/O register address ($1000–$103F)
            read_fn: Callable(addr) -> int (8-bit value)
            write_fn: Callable(addr, value) -> None
        """
        if read_fn:
            self._io_read_handlers[addr] = read_fn
        if write_fn:
            self._io_write_handlers[addr] = write_fn
    
    # --- Watchpoints (for DTC reverse engineering) ---
    
    def add_watchpoint(self, addr: int, callback: Callable):
        """Add a write watchpoint on an address.
        
        callback(addr, old_val, new_val, is_write) is called on every
        write to that address. Used for DTC mapping — inject a fault
        condition, run emulator, see what RAM addresses get written.
        """
        if addr not in self._watchpoints:
            self._watchpoints[addr] = []
        self._watchpoints[addr].append(callback)
    
    def remove_watchpoint(self, addr: int, callback: Optional[Callable] = None):
        """Remove a watchpoint. If callback is None, removes all on that addr."""
        if addr in self._watchpoints:
            if callback is None:
                del self._watchpoints[addr]
            else:
                self._watchpoints[addr] = [
                    cb for cb in self._watchpoints[addr] if cb != callback
                ]
    
    # --- Snapshots (for DTC analysis — diff RAM state) ---
    
    def snapshot_ram(self, start: int = 0x0000, end: int = 0x03FF) -> bytes:
        """Capture RAM state for later diffing.
        
        Returns bytes copy of RAM region. Default is internal RAM.
        Used for DTC mapping: snapshot before fault → snapshot after → diff.
        """
        return bytes(self._mem[start:end + 1])
    
    def diff_snapshots(self, snap_a: bytes, snap_b: bytes, 
                       base_addr: int = 0x0000) -> Dict[int, tuple]:
        """Compare two RAM snapshots, return {addr: (old, new)} for changes.
        
        SCAFFOLD: Basic byte diff. Could be enhanced with bit-level diff
        for DTC bitfield analysis.
        """
        changes = {}
        for i in range(min(len(snap_a), len(snap_b))):
            if snap_a[i] != snap_b[i]:
                changes[base_addr + i] = (snap_a[i], snap_b[i])
        return changes
    
    # --- EEPROM persistence ---
    
    def save_eeprom(self, filepath: str):
        """Save EEPROM region ($FE00–$FFBF) to file for persistence."""
        eeprom_data = bytes(self._mem[0xFE00:0xFFC0])
        Path(filepath).write_bytes(eeprom_data)
    
    def load_eeprom(self, filepath: str):
        """Load EEPROM state from file. Silently skips if file doesn't exist."""
        path = Path(filepath)
        if path.exists():
            data = path.read_bytes()
            for i, byte in enumerate(data[:512]):
                self._mem[0xFE00 + i] = byte
    
    # --- Hex dump ---
    
    def hexdump(self, start: int, length: int = 256) -> str:
        """Produce a hex dump of memory for debugging."""
        lines = []
        for offset in range(0, length, 16):
            addr = (start + offset) & 0xFFFF
            hex_bytes = ' '.join(f'{self._mem[(addr + i) & 0xFFFF]:02X}' 
                                for i in range(16))
            ascii_bytes = ''.join(
                chr(self._mem[(addr + i) & 0xFFFF]) 
                if 0x20 <= self._mem[(addr + i) & 0xFFFF] < 0x7F else '.'
                for i in range(16)
            )
            lines.append(f'{addr:04X}  {hex_bytes}  {ascii_bytes}')
        return '\n'.join(lines)
