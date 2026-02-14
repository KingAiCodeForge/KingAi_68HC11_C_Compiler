"""
HC11 Virtual Emulator — SCI (Serial Communication Interface) Peripheral

SCAFFOLD — needs cross-referencing against:
  - Motorola MC68HC11F1 Technical Data Section 9 (SCI chapter)
  - Stock $060A binary SCI initialization at $29D3
  - examples/aldl_hello.c, mode4_responder.c (SCI usage patterns)
  - ALDL protocol constants from kingai_srs_commodore_bcm_tool

Emulates the HC11 SCI for ALDL communication testing.
This is the most critical peripheral for compiler output validation
because the "proof it works" ALDL hello world depends on SCI TX.

Register map:
  $102B  BAUD   — Baud rate register (prescaler + divider)
  $102C  SCCR1  — SCI control 1 (character length, wake)
  $102D  SCCR2  — SCI control 2 (TE, RE, interrupt enables)
  $102E  SCSR   — SCI status (TDRE, RDRF, OR, NF, FE)
  $102F  SCDR   — SCI data register (read=RX, write=TX)

Simplifications for emulator:
  - TDRE (bit 7 of SCSR) is always ready (instant TX)
  - RDRF (bit 5 of SCSR) is set when data is injected via inject_rx()
  - No framing errors, no noise, no overrun
  - Baud rate is stored but not used for timing
"""

from typing import List, Optional
from collections import deque


# SCI register addresses
BAUD  = 0x102B
SCCR1 = 0x102C
SCCR2 = 0x102D
SCSR  = 0x102E
SCDR  = 0x102F

# SCCR2 bits
TE  = 0x08  # Transmit Enable
RE  = 0x04  # Receive Enable
TIE = 0x80  # Transmit Interrupt Enable
RIE = 0x20  # Receive Interrupt Enable

# SCSR bits
TDRE = 0x80  # Transmit Data Register Empty
RDRF = 0x20  # Receive Data Register Full
OR   = 0x08  # Overrun error
NF   = 0x04  # Noise flag
FE   = 0x02  # Framing error


class SCIPeripheral:
    """SCI (ALDL Serial) peripheral model.
    
    SCAFFOLD: Register behavior validated against HC11F1 datasheet.
    TX output goes to a ringbuffer for programmatic inspection.
    RX data is injected via inject_rx() for Mode 4 testing.
    
    To validate against: 
      - aldl_hello_world.asm should produce b"HELLO\\r\\n" in tx_buffer
      - aldl_hello.c should produce b"HI\\r\\n" in tx_buffer
      - mode4_responder.c should consume injected RX and produce response
    """
    
    def __init__(self):
        self._baud = 0x00    # BAUD register value
        self._sccr1 = 0x00   # Control register 1
        self._sccr2 = 0x00   # Control register 2
        self._scdr_tx = 0x00 # Last byte written to SCDR
        self._scdr_rx = 0x00 # Current RX byte available
        
        # TX output ringbuffer — all transmitted bytes go here
        self.tx_buffer: bytearray = bytearray()
        
        # RX injection queue — push bytes in, they appear as received data
        self._rx_queue: deque = deque()
        
        # Status flags
        self._tdre = True    # Always ready for next TX in emulator
        self._rdrf = False   # Set when RX data available
    
    def register(self, memory):
        """Register I/O handlers with the memory system.
        
        Call this during emulator init to wire SCI registers.
        """
        memory.register_io_handler(BAUD,  self._read_baud,  self._write_baud)
        memory.register_io_handler(SCCR1, self._read_sccr1, self._write_sccr1)
        memory.register_io_handler(SCCR2, self._read_sccr2, self._write_sccr2)
        memory.register_io_handler(SCSR,  self._read_scsr,  None)  # read-only
        memory.register_io_handler(SCDR,  self._read_scdr,  self._write_scdr)
    
    # --- BAUD register ($102B) ---
    
    def _read_baud(self, addr: int) -> int:
        return self._baud
    
    def _write_baud(self, addr: int, value: int):
        self._baud = value & 0xFF
        # SCAFFOLD: Could compute actual baud rate from prescaler bits
        # VY V6 uses value $04 → prescaler ÷1, divider ÷16 → 8192 baud
        # from 4.194304 MHz crystal → 2.097152 MHz E-clock
    
    # --- SCCR1 register ($102C) ---
    
    def _read_sccr1(self, addr: int) -> int:
        return self._sccr1
    
    def _write_sccr1(self, addr: int, value: int):
        self._sccr1 = value & 0xFF
    
    # --- SCCR2 register ($102D) ---
    
    def _read_sccr2(self, addr: int) -> int:
        return self._sccr2
    
    def _write_sccr2(self, addr: int, value: int):
        self._sccr2 = value & 0xFF
    
    # --- SCSR register ($102E) — Status (read-only) ---
    
    def _read_scsr(self, addr: int) -> int:
        """Build status register value.
        
        TDRE is always set (transmitter always ready — instant send).
        RDRF is set when RX data is available in the queue.
        """
        status = 0x00
        
        # TDRE — always ready in emulator (no real baud timing)
        if self._tdre and (self._sccr2 & TE):
            status |= TDRE
        
        # RDRF — set if data waiting in RX queue
        if self._rdrf:
            status |= RDRF
        
        return status
    
    # --- SCDR register ($102F) — Data (bidirectional) ---
    
    def _read_scdr(self, addr: int) -> int:
        """Read SCDR = receive byte from RX queue.
        
        Clears RDRF. If more data in queue, RDRF re-sets on next read_scsr.
        """
        value = self._scdr_rx
        self._rdrf = False
        
        # Preload next byte from queue if available
        if self._rx_queue:
            self._scdr_rx = self._rx_queue.popleft()
            self._rdrf = True
        
        return value
    
    def _write_scdr(self, addr: int, value: int):
        """Write SCDR = transmit byte over SCI (ALDL).
        
        Byte is appended to tx_buffer for inspection.
        TE must be enabled in SCCR2 for actual transmission.
        """
        self._scdr_tx = value & 0xFF
        
        if self._sccr2 & TE:
            self.tx_buffer.append(self._scdr_tx)
    
    # --- External API (test harness / ALDL simulation) ---
    
    def inject_rx(self, data: bytes):
        """Inject bytes into the RX queue (simulates incoming ALDL data).
        
        Used by test harness to send Mode 4 commands to the emulated PCM.
        The emulated code will see RDRF go high and read bytes from SCDR.
        
        Example:
            # Send Mode 4 frame: [0xF7][0x56][0x04][control...][checksum]
            sci.inject_rx(bytes([0xF7, 0x56, 0x04, 0x01, 0x00, ...]))
        """
        for byte in data:
            self._rx_queue.append(byte & 0xFF)
        
        if not self._rdrf and self._rx_queue:
            self._scdr_rx = self._rx_queue.popleft()
            self._rdrf = True
    
    @property
    def sci_output(self) -> bytes:
        """All bytes transmitted via SCI since last reset."""
        return bytes(self.tx_buffer)
    
    def reset(self):
        """Reset SCI state."""
        self._baud = 0x00
        self._sccr1 = 0x00
        self._sccr2 = 0x00
        self._scdr_tx = 0x00
        self._scdr_rx = 0x00
        self.tx_buffer.clear()
        self._rx_queue.clear()
        self._tdre = True
        self._rdrf = False
