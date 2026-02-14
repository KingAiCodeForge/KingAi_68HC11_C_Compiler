"""
HC11 Virtual Emulator — Main Emulator Class

SCAFFOLD — needs cross-referencing against:
  - tonypdmtr/EVBU PySim11/PySim11.py (SimState class — fetch/decode/execute loop)
  - hc11_compiler/assembler.py (our opcode table for validation)
  - examples/*.c (test corpus — every example must run)

This is the top-level class that integrates:
  - CPU registers (regs.py)
  - Memory map (memory.py)
  - Opcode decoder (decoder.py)
  - ALU operations (alu.py)
  - Peripherals: SCI, ADC, Timer, Ports

Execution model:
  1. Fetch opcode at PC
  2. Decode addressing mode → resolve operand address/value
  3. Execute instruction handler → update registers, memory, flags
  4. Advance cycle counter
  5. Update peripherals (timer tick, etc.)
  6. Check termination conditions (max cycles, breakpoint, halt)

Termination reasons:
  - TIMEOUT:  max_cycles exceeded
  - BREAK:    breakpoint address hit
  - HALT:     WAI or SWI instruction
  - STOP:     STOP instruction
  - DONE:     expected SCI output received
  - ILLEGAL:  undefined opcode
"""

from typing import Optional, Set, Callable
from pathlib import Path
from enum import Enum

from .cpu.regs import Registers, CC_I, CC_X
from .cpu.decoder import (
    decode_opcode, IllegalOpcode,
    INH, IMM8, IMM16, DIR, EXT, INDX, INDY, REL,
    BIT2DIR, BIT2INDX, BIT2INDY, BIT3DIR, BIT3INDX, BIT3INDY
)
from .cpu import alu
from .mem.memory import Memory
from .periph.sci import SCIPeripheral
from .periph.adc import ADCPeripheral
from .periph.ports import PortsPeripheral
from .periph.timer import TimerPeripheral


class StopReason(Enum):
    TIMEOUT = 'TIMEOUT'
    BREAK = 'BREAK'
    HALT = 'HALT'
    STOP = 'STOP'
    DONE = 'DONE'
    ILLEGAL = 'ILLEGAL'
    ERROR = 'ERROR'


class HC11Emulator:
    """68HC11 Virtual Emulator.
    
    SCAFFOLD: Instruction execution loop and operand decoding are
    structurally complete but EVERY instruction handler needs
    byte-for-byte validation against EVBU and/or GDB sim.
    
    Usage:
        emu = HC11Emulator()
        emu.load_binary('hello.bin', base_addr=0x5D00)
        emu.regs.PC = 0x5D00  # or load from reset vector
        result = emu.run(max_cycles=50000)
        print(emu.sci.sci_output)  # b"HI\\r\\n"
    """
    
    DEFAULT_MAX_CYCLES = 10_000_000
    
    def __init__(self):
        # Core components
        self.regs = Registers()
        self.mem = Memory()
        
        # Peripherals
        self.sci = SCIPeripheral()
        self.adc = ADCPeripheral()
        self.ports = PortsPeripheral()
        self.timer = TimerPeripheral()
        
        # Register peripherals with memory I/O system
        self.sci.register(self.mem)
        self.adc.register(self.mem)
        self.ports.register(self.mem)
        self.timer.register(self.mem)
        
        # Breakpoints: set of PC addresses that trigger BREAK
        self._breakpoints: Set[int] = set()
        
        # Trace output
        self._trace = False
        self._trace_output = []
        
        # Instruction dispatch table (built in _build_dispatch)
        self._dispatch = self._build_dispatch()
    
    # ══════════════════════════════════════════════
    # Loading
    # ══════════════════════════════════════════════
    
    def load_binary(self, path_or_data, base_addr: int = 0x8000):
        """Load a raw binary file or bytes into memory.
        
        For compiler output: base_addr is the injection address
        (e.g., 0x5D00 for free space in $060A calibration).
        
        For stock ROM: base_addr is typically 0x8000 (bank 1) or
        0xC000 (bank 2).
        """
        if isinstance(path_or_data, (str, Path)):
            data = Path(path_or_data).read_bytes()
        else:
            data = bytes(path_or_data)
        self.mem.load_binary(data, base_addr)
    
    def load_s19(self, path_or_text):
        """Load Motorola S19 format file or text."""
        if isinstance(path_or_text, (str, Path)):
            p = Path(path_or_text)
            if p.exists():
                text = p.read_text()
            else:
                text = path_or_text
        else:
            text = path_or_text
        self.mem.load_s19(text)
    
    def load_reset_vector(self):
        """Load PC from reset vector at $FFFE-$FFFF."""
        self.regs.PC = self.mem.read16(0xFFFE)
    
    # ══════════════════════════════════════════════
    # Execution
    # ══════════════════════════════════════════════
    
    def step(self) -> Optional[StopReason]:
        """Execute one instruction. Returns StopReason if stopped, else None.
        
        SCAFFOLD: Fetch-decode-execute cycle. Cross-referenced with EVBU
        PySim11.py step() method. Interrupt handling is NOT implemented
        yet (Phase 4 in the dev plan).
        """
        pc = self.regs.PC
        
        # Breakpoint check
        if pc in self._breakpoints:
            return StopReason.BREAK
        
        # Fetch + decode opcode
        try:
            mnem, mode, cycles, next_pc = decode_opcode(self.mem, pc)
        except IllegalOpcode:
            return StopReason.ILLEGAL
        
        # Update PC past opcode bytes
        self.regs.PC = next_pc
        
        # Decode operands based on addressing mode
        try:
            operands = self._decode_operands(mode)
        except Exception:
            return StopReason.ERROR
        
        # Trace
        if self._trace:
            self._trace_output.append(
                f"${pc:04X}: {mnem:6s} {self.regs.display()}"
            )
        
        # Execute instruction
        try:
            result = self._execute(mnem, mode, operands)
        except _HaltException:
            return StopReason.HALT
        except _StopException:
            return StopReason.STOP
        except Exception as e:
            if self._trace:
                self._trace_output.append(f"  ERROR: {e}")
            return StopReason.ERROR
        
        # Advance cycle counter + update peripherals
        self.regs.cycles += cycles
        self.timer.update(cycles)
        
        return None
    
    def run(self, max_cycles: int = None, 
            expected_output: bytes = None) -> StopReason:
        """Run until termination condition.
        
        Args:
            max_cycles: Maximum E-clock cycles before TIMEOUT
            expected_output: SCI output bytes to watch for → DONE
        
        Returns:
            StopReason indicating why execution stopped
        """
        if max_cycles is None:
            max_cycles = self.DEFAULT_MAX_CYCLES
        
        while self.regs.cycles < max_cycles:
            reason = self.step()
            if reason is not None:
                return reason
            
            # Check for expected SCI output
            if expected_output and expected_output in self.sci.sci_output:
                return StopReason.DONE
        
        return StopReason.TIMEOUT
    
    # ══════════════════════════════════════════════
    # Operand decoding
    # ══════════════════════════════════════════════
    
    def _decode_operands(self, mode: str) -> tuple:
        """Decode operands based on addressing mode.
        
        Returns: tuple of (addr, value) or (target_addr,) etc.
        
        SCAFFOLD: Decoding logic adapted from EVBU PySim11.py decode().
        Each mode returns different operand combinations:
          INH:    ()
          IMM8:   (None, value)      — value is immediate byte
          IMM16:  (None, value)      — value is immediate word
          DIR:    (addr, None)       — addr is 8-bit direct page
          EXT:    (addr, None)       — addr is 16-bit extended
          INDX:   (addr, None)       — addr is offset+X
          INDY:   (addr, None)       — addr is offset+Y
          REL:    (target_addr,)     — target is PC + signed offset
          BIT2*:  (addr, mask)       — for BSET/BCLR
          BIT3*:  (addr, mask, target) — for BRSET/BRCLR
        """
        if mode == INH:
            return ()
        
        elif mode == IMM8:
            value = self._fetch8()
            return (None, value)
        
        elif mode == IMM16:
            value = self._fetch16()
            return (None, value)
        
        elif mode == DIR:
            addr = self._fetch8()
            return (addr, None)
        
        elif mode == EXT:
            addr = self._fetch16()
            return (addr, None)
        
        elif mode == INDX:
            offset = self._fetch8()
            addr = (offset + self.regs.X) & 0xFFFF
            return (addr, None)
        
        elif mode == INDY:
            offset = self._fetch8()
            addr = (offset + self.regs.Y) & 0xFFFF
            return (addr, None)
        
        elif mode == REL:
            offset = alu.twos_complement_8(self._fetch8())
            target = (self.regs.PC + offset) & 0xFFFF
            return (target,)
        
        elif mode in (BIT2DIR, BIT2INDX, BIT2INDY):
            if mode == BIT2DIR:
                addr = self._fetch8()
            elif mode == BIT2INDX:
                offset = self._fetch8()
                addr = (offset + self.regs.X) & 0xFFFF
            else:  # BIT2INDY
                offset = self._fetch8()
                addr = (offset + self.regs.Y) & 0xFFFF
            mask = self._fetch8()
            return (addr, mask)
        
        elif mode in (BIT3DIR, BIT3INDX, BIT3INDY):
            if mode == BIT3DIR:
                addr = self._fetch8()
            elif mode == BIT3INDX:
                offset = self._fetch8()
                addr = (offset + self.regs.X) & 0xFFFF
            else:  # BIT3INDY
                offset = self._fetch8()
                addr = (offset + self.regs.Y) & 0xFFFF
            mask = self._fetch8()
            rel = alu.twos_complement_8(self._fetch8())
            target = (self.regs.PC + rel) & 0xFFFF
            return (addr, mask, target)
        
        else:
            raise ValueError(f"Unknown addressing mode: {mode}")
    
    def _fetch8(self) -> int:
        """Fetch 8-bit value at PC, advance PC."""
        val = self.mem.read8(self.regs.PC)
        self.regs.PC = (self.regs.PC + 1) & 0xFFFF
        return val
    
    def _fetch16(self) -> int:
        """Fetch 16-bit value at PC (big-endian), advance PC by 2."""
        val = self.mem.read16(self.regs.PC)
        self.regs.PC = (self.regs.PC + 2) & 0xFFFF
        return val
    
    # ══════════════════════════════════════════════
    # Instruction execution
    # ══════════════════════════════════════════════
    
    def _execute(self, mnem: str, mode: str, operands: tuple):
        """Dispatch instruction to handler.
        
        SCAFFOLD: Priority 1 instructions (compiler output) are implemented.
        Priority 2/3 need adding for stock ROM emulation.
        """
        handler = self._dispatch.get(mnem)
        if handler is None:
            raise NotImplementedError(f"Instruction {mnem} not implemented")
        handler(mode, operands)
    
    def _get_operand_value(self, mode: str, operands: tuple) -> int:
        """Get the effective operand value for load/arithmetic instructions.
        
        For immediate modes: return the immediate value directly.
        For memory modes: read from the resolved address.
        """
        addr, value = operands[0], operands[1]
        if addr is None:
            return value  # immediate
        return self.mem.read8(addr)
    
    def _get_operand_value16(self, mode: str, operands: tuple) -> int:
        """Get 16-bit operand value."""
        addr, value = operands[0], operands[1]
        if addr is None:
            return value  # immediate
        return self.mem.read16(addr)
    
    # ══════════════════════════════════════════════
    # Instruction handlers — SCAFFOLD
    # ══════════════════════════════════════════════
    # Each handler needs validation against EVBU PySim11/ops.py
    # and the HC11 Reference Manual for correct flag behavior.
    #
    # Handler signature: handler(mode, operands)
    # operands format depends on mode (see _decode_operands)
    
    def _build_dispatch(self) -> dict:
        """Build mnemonic → handler dispatch table.
        
        SCAFFOLD: Priority 1 instructions (~86) listed.
        Handlers marked TODO need implementation completion.
        """
        return {
            # ── Load/Store ──
            'LDAA': self._op_ldaa,
            'LDAB': self._op_ldab,
            'LDD':  self._op_ldd,
            'LDX':  self._op_ldx,
            'LDY':  self._op_ldy,
            'LDS':  self._op_lds,
            'STAA': self._op_staa,
            'STAB': self._op_stab,
            'STD':  self._op_std,
            'STX':  self._op_stx,
            'STY':  self._op_sty,
            'STS':  self._op_sts,
            
            # ── Arithmetic ──
            'ADDA': self._op_adda,
            'ADDB': self._op_addb,
            'ADDD': self._op_addd,
            'ADCA': self._op_adca,
            'ADCB': self._op_adcb,
            'SUBA': self._op_suba,
            'SUBB': self._op_subb,
            'SUBD': self._op_subd,
            'SBCA': self._op_sbca,
            'SBCB': self._op_sbcb,
            'ABA':  self._op_aba,
            'SBA':  self._op_sba,
            'CBA':  self._op_cba,
            'INCA': self._op_inca,
            'INCB': self._op_incb,
            'INC':  self._op_inc,
            'DECA': self._op_deca,
            'DECB': self._op_decb,
            'DEC':  self._op_dec,
            'NEGA': self._op_nega,
            'NEGB': self._op_negb,
            'NEG':  self._op_neg,
            'MUL':  self._op_mul,
            'IDIV': self._op_idiv,
            'FDIV': self._op_fdiv,
            'DAA':  self._op_daa,
            'ABX':  self._op_abx,
            'ABY':  self._op_aby,
            
            # ── Logic ──
            'ANDA': self._op_anda,
            'ANDB': self._op_andb,
            'ORAA': self._op_oraa,
            'ORAB': self._op_orab,
            'EORA': self._op_eora,
            'EORB': self._op_eorb,
            'COMA': self._op_coma,
            'COMB': self._op_comb,
            'COM':  self._op_com,
            'BITA': self._op_bita,
            'BITB': self._op_bitb,
            
            # ── Compare ──
            'CMPA': self._op_cmpa,
            'CMPB': self._op_cmpb,
            'CPD':  self._op_cpd,
            'CPX':  self._op_cpx,
            'CPY':  self._op_cpy,
            'TSTA': self._op_tsta,
            'TSTB': self._op_tstb,
            'TST':  self._op_tst,
            
            # ── Shift/Rotate ──
            'ASLA': self._op_asla,
            'ASLB': self._op_aslb,
            'ASL':  self._op_asl,
            'ASRA': self._op_asra,
            'ASRB': self._op_asrb,
            'ASR':  self._op_asr,
            'LSRA': self._op_lsra,
            'LSRB': self._op_lsrb,
            'LSR':  self._op_lsr,
            'LSLD': self._op_lsld,
            'LSRD': self._op_lsrd,
            'ROLA': self._op_rola,
            'ROLB': self._op_rolb,
            'ROL':  self._op_rol,
            'RORA': self._op_rora,
            'RORB': self._op_rorb,
            'ROR':  self._op_ror,
            
            # ── Clear ──
            'CLRA': self._op_clra,
            'CLRB': self._op_clrb,
            'CLR':  self._op_clr,
            
            # ── Branch ──
            'BRA':  self._op_bra,
            'BRN':  self._op_brn,
            'BEQ':  self._op_beq,
            'BNE':  self._op_bne,
            'BCC':  self._op_bcc,
            'BCS':  self._op_bcs,
            'BGE':  self._op_bge,
            'BGT':  self._op_bgt,
            'BLE':  self._op_ble,
            'BLT':  self._op_blt,
            'BHI':  self._op_bhi,
            'BLS':  self._op_bls,
            'BMI':  self._op_bmi,
            'BPL':  self._op_bpl,
            'BVC':  self._op_bvc,
            'BVS':  self._op_bvs,
            'BSR':  self._op_bsr,
            
            # ── Jump/Call ──
            'JMP':  self._op_jmp,
            'JSR':  self._op_jsr,
            'RTS':  self._op_rts,
            'RTI':  self._op_rti,
            
            # ── Stack ──
            'PSHA': self._op_psha,
            'PSHB': self._op_pshb,
            'PSHX': self._op_pshx,
            'PSHY': self._op_pshy,
            'PULA': self._op_pula,
            'PULB': self._op_pulb,
            'PULX': self._op_pulx,
            'PULY': self._op_puly,
            
            # ── Transfer ──
            'TAB':  self._op_tab,
            'TBA':  self._op_tba,
            'TAP':  self._op_tap,
            'TPA':  self._op_tpa,
            'TSX':  self._op_tsx,
            'TXS':  self._op_txs,
            'TSY':  self._op_tsy,
            'TYS':  self._op_tys,
            'XGDX': self._op_xgdx,
            'XGDY': self._op_xgdy,
            'INX':  self._op_inx,
            'DEX':  self._op_dex,
            'INY':  self._op_iny,
            'DEY':  self._op_dey,
            'INS':  self._op_ins,
            'DES':  self._op_des,
            
            # ── Bit manipulation ──
            'BSET':  self._op_bset,
            'BCLR':  self._op_bclr,
            'BRSET': self._op_brset,
            'BRCLR': self._op_brclr,
            
            # ── CCR manipulation ──
            'SEI':  self._op_sei,
            'CLI':  self._op_cli,
            'SEV':  self._op_sev,
            'CLV':  self._op_clv,
            'SEC':  self._op_sec,
            'CLC':  self._op_clc,
            
            # ── Control ──
            'NOP':  self._op_nop,
            'WAI':  self._op_wai,
            'SWI':  self._op_swi,
            'STOP': self._op_stop,
            'TEST': self._op_test,
        }
    
    # ── Load/Store handlers ──
    
    def _op_ldaa(self, mode, ops):
        val = self._get_operand_value(mode, ops)
        self.regs.A = val
        self.regs.set_NZV(alu.test_nz8(val))
    
    def _op_ldab(self, mode, ops):
        val = self._get_operand_value(mode, ops)
        self.regs.B = val
        self.regs.set_NZV(alu.test_nz8(val))
    
    def _op_ldd(self, mode, ops):
        val = self._get_operand_value16(mode, ops)
        self.regs.D = val
        self.regs.set_NZV(alu.test_nz16(val))
    
    def _op_ldx(self, mode, ops):
        val = self._get_operand_value16(mode, ops)
        self.regs.X = val
        self.regs.set_NZV(alu.test_nz16(val))
    
    def _op_ldy(self, mode, ops):
        val = self._get_operand_value16(mode, ops)
        self.regs.Y = val
        self.regs.set_NZV(alu.test_nz16(val))
    
    def _op_lds(self, mode, ops):
        val = self._get_operand_value16(mode, ops)
        self.regs.SP = val
        self.regs.set_NZV(alu.test_nz16(val))
    
    def _op_staa(self, mode, ops):
        addr = ops[0]
        self.mem.write8(addr, self.regs.A)
        self.regs.set_NZV(alu.test_nz8(self.regs.A))
    
    def _op_stab(self, mode, ops):
        addr = ops[0]
        self.mem.write8(addr, self.regs.B)
        self.regs.set_NZV(alu.test_nz8(self.regs.B))
    
    def _op_std(self, mode, ops):
        addr = ops[0]
        self.mem.write16(addr, self.regs.D)
        self.regs.set_NZV(alu.test_nz16(self.regs.D))
    
    def _op_stx(self, mode, ops):
        addr = ops[0]
        self.mem.write16(addr, self.regs.X)
        self.regs.set_NZV(alu.test_nz16(self.regs.X))
    
    def _op_sty(self, mode, ops):
        addr = ops[0]
        self.mem.write16(addr, self.regs.Y)
        self.regs.set_NZV(alu.test_nz16(self.regs.Y))
    
    def _op_sts(self, mode, ops):
        addr = ops[0]
        self.mem.write16(addr, self.regs.SP)
        self.regs.set_NZV(alu.test_nz16(self.regs.SP))
    
    # ── Arithmetic handlers ──
    
    def _op_adda(self, mode, ops):
        val = self._get_operand_value(mode, ops)
        result, flags = alu.add8(self.regs.A, val)
        self.regs.A = result
        self.regs.set_HNZVC(flags)
    
    def _op_addb(self, mode, ops):
        val = self._get_operand_value(mode, ops)
        result, flags = alu.add8(self.regs.B, val)
        self.regs.B = result
        self.regs.set_HNZVC(flags)
    
    def _op_addd(self, mode, ops):
        val = self._get_operand_value16(mode, ops)
        result, flags = alu.add16(self.regs.D, val)
        self.regs.D = result
        self.regs.set_NZVC(flags)
    
    def _op_adca(self, mode, ops):
        val = self._get_operand_value(mode, ops)
        result, flags = alu.adc8(self.regs.A, val, int(self.regs.carry))
        self.regs.A = result
        self.regs.set_HNZVC(flags)
    
    def _op_adcb(self, mode, ops):
        val = self._get_operand_value(mode, ops)
        result, flags = alu.adc8(self.regs.B, val, int(self.regs.carry))
        self.regs.B = result
        self.regs.set_HNZVC(flags)
    
    def _op_suba(self, mode, ops):
        val = self._get_operand_value(mode, ops)
        result, flags = alu.sub8(self.regs.A, val)
        self.regs.A = result
        self.regs.set_NZVC(flags)
    
    def _op_subb(self, mode, ops):
        val = self._get_operand_value(mode, ops)
        result, flags = alu.sub8(self.regs.B, val)
        self.regs.B = result
        self.regs.set_NZVC(flags)
    
    def _op_subd(self, mode, ops):
        val = self._get_operand_value16(mode, ops)
        result, flags = alu.sub16(self.regs.D, val)
        self.regs.D = result
        self.regs.set_NZVC(flags)
    
    def _op_sbca(self, mode, ops):
        val = self._get_operand_value(mode, ops)
        result, flags = alu.sbc8(self.regs.A, val, int(self.regs.carry))
        self.regs.A = result
        self.regs.set_NZVC(flags)
    
    def _op_sbcb(self, mode, ops):
        val = self._get_operand_value(mode, ops)
        result, flags = alu.sbc8(self.regs.B, val, int(self.regs.carry))
        self.regs.B = result
        self.regs.set_NZVC(flags)
    
    def _op_aba(self, mode, ops):
        result, flags = alu.add8(self.regs.A, self.regs.B)
        self.regs.A = result
        self.regs.set_HNZVC(flags)
    
    def _op_sba(self, mode, ops):
        result, flags = alu.sub8(self.regs.A, self.regs.B)
        self.regs.A = result
        self.regs.set_NZVC(flags)
    
    def _op_cba(self, mode, ops):
        _, flags = alu.sub8(self.regs.A, self.regs.B)
        self.regs.set_NZVC(flags)
    
    def _op_inca(self, mode, ops):
        result, flags = alu.add8(self.regs.A, 1)
        self.regs.A = result
        self.regs.set_NZV(flags)
    
    def _op_incb(self, mode, ops):
        result, flags = alu.add8(self.regs.B, 1)
        self.regs.B = result
        self.regs.set_NZV(flags)
    
    def _op_inc(self, mode, ops):
        addr = ops[0]
        val = self.mem.read8(addr)
        result, flags = alu.add8(val, 1)
        self.mem.write8(addr, result)
        self.regs.set_NZV(flags)
    
    def _op_deca(self, mode, ops):
        result, flags = alu.sub8(self.regs.A, 1)
        self.regs.A = result
        self.regs.set_NZV(flags)
    
    def _op_decb(self, mode, ops):
        result, flags = alu.sub8(self.regs.B, 1)
        self.regs.B = result
        self.regs.set_NZV(flags)
    
    def _op_dec(self, mode, ops):
        addr = ops[0]
        val = self.mem.read8(addr)
        result, flags = alu.sub8(val, 1)
        self.mem.write8(addr, result)
        self.regs.set_NZV(flags)
    
    def _op_nega(self, mode, ops):
        result, flags = alu.neg8(self.regs.A)
        self.regs.A = result
        self.regs.set_NZVC(flags)
    
    def _op_negb(self, mode, ops):
        result, flags = alu.neg8(self.regs.B)
        self.regs.B = result
        self.regs.set_NZVC(flags)
    
    def _op_neg(self, mode, ops):
        addr = ops[0]
        val = self.mem.read8(addr)
        result, flags = alu.neg8(val)
        self.mem.write8(addr, result)
        self.regs.set_NZVC(flags)
    
    def _op_mul(self, mode, ops):
        result = self.regs.A * self.regs.B
        self.regs.D = result
        self.regs.set_C(alu.CC_C if result & 0x0080 else 0)
    
    def _op_idiv(self, mode, ops):
        if self.regs.X == 0:
            self.regs.X = 0xFFFF
            self.regs.D = 0
            self.regs.set_ZVC(alu.CC_C)
        else:
            q = self.regs.D // self.regs.X
            r = self.regs.D % self.regs.X
            self.regs.X = q & 0xFFFF
            self.regs.D = r & 0xFFFF
            flags = 0
            if q == 0:
                flags |= alu.CC_Z
            self.regs.set_ZVC(flags)
    
    def _op_fdiv(self, mode, ops):
        if self.regs.X == 0 or self.regs.X <= self.regs.D:
            self.regs.X = 0xFFFF
            self.regs.D = 0
            flags = alu.CC_V
            if self.regs.X == 0:
                flags |= alu.CC_C
            self.regs.set_ZVC(flags)
        else:
            q = int(self.regs.D * 0x10000 / self.regs.X)
            r = int(self.regs.D * 0x10000 % self.regs.X)
            self.regs.X = q & 0xFFFF
            self.regs.D = r & 0xFFFF
            flags = 0
            if q == 0:
                flags |= alu.CC_Z
            self.regs.set_ZVC(flags)
    
    def _op_daa(self, mode, ops):
        """Decimal Adjust Accumulator A — BCD correction.
        SCAFFOLD: Complex logic, needs thorough testing. Adapted from EVBU.
        """
        # TODO: Implement DAA properly (low priority — compiler doesn't emit this)
        pass
    
    def _op_abx(self, mode, ops):
        self.regs.X = (self.regs.X + self.regs.B) & 0xFFFF
    
    def _op_aby(self, mode, ops):
        self.regs.Y = (self.regs.Y + self.regs.B) & 0xFFFF
    
    # ── Logic handlers ──
    
    def _op_anda(self, mode, ops):
        val = self._get_operand_value(mode, ops)
        result, flags = alu.and8(self.regs.A, val)
        self.regs.A = result
        self.regs.set_NZV(flags)
    
    def _op_andb(self, mode, ops):
        val = self._get_operand_value(mode, ops)
        result, flags = alu.and8(self.regs.B, val)
        self.regs.B = result
        self.regs.set_NZV(flags)
    
    def _op_oraa(self, mode, ops):
        val = self._get_operand_value(mode, ops)
        result, flags = alu.or8(self.regs.A, val)
        self.regs.A = result
        self.regs.set_NZV(flags)
    
    def _op_orab(self, mode, ops):
        val = self._get_operand_value(mode, ops)
        result, flags = alu.or8(self.regs.B, val)
        self.regs.B = result
        self.regs.set_NZV(flags)
    
    def _op_eora(self, mode, ops):
        val = self._get_operand_value(mode, ops)
        result, flags = alu.eor8(self.regs.A, val)
        self.regs.A = result
        self.regs.set_NZV(flags)
    
    def _op_eorb(self, mode, ops):
        val = self._get_operand_value(mode, ops)
        result, flags = alu.eor8(self.regs.B, val)
        self.regs.B = result
        self.regs.set_NZV(flags)
    
    def _op_coma(self, mode, ops):
        result, flags = alu.com8(self.regs.A)
        self.regs.A = result
        self.regs.set_NZVC(flags)
    
    def _op_comb(self, mode, ops):
        result, flags = alu.com8(self.regs.B)
        self.regs.B = result
        self.regs.set_NZVC(flags)
    
    def _op_com(self, mode, ops):
        addr = ops[0]
        val = self.mem.read8(addr)
        result, flags = alu.com8(val)
        self.mem.write8(addr, result)
        self.regs.set_NZVC(flags)
    
    def _op_bita(self, mode, ops):
        val = self._get_operand_value(mode, ops)
        _, flags = alu.and8(self.regs.A, val)
        self.regs.set_NZV(flags)
    
    def _op_bitb(self, mode, ops):
        val = self._get_operand_value(mode, ops)
        _, flags = alu.and8(self.regs.B, val)
        self.regs.set_NZV(flags)
    
    # ── Compare handlers ──
    
    def _op_cmpa(self, mode, ops):
        val = self._get_operand_value(mode, ops)
        _, flags = alu.sub8(self.regs.A, val)
        self.regs.set_NZVC(flags)
    
    def _op_cmpb(self, mode, ops):
        val = self._get_operand_value(mode, ops)
        _, flags = alu.sub8(self.regs.B, val)
        self.regs.set_NZVC(flags)
    
    def _op_cpd(self, mode, ops):
        val = self._get_operand_value16(mode, ops)
        _, flags = alu.sub16(self.regs.D, val)
        self.regs.set_NZVC(flags)
    
    def _op_cpx(self, mode, ops):
        val = self._get_operand_value16(mode, ops)
        _, flags = alu.sub16(self.regs.X, val)
        self.regs.set_NZVC(flags)
    
    def _op_cpy(self, mode, ops):
        val = self._get_operand_value16(mode, ops)
        _, flags = alu.sub16(self.regs.Y, val)
        self.regs.set_NZVC(flags)
    
    def _op_tsta(self, mode, ops):
        self.regs.set_NZVC(alu.test_nz8(self.regs.A))
    
    def _op_tstb(self, mode, ops):
        self.regs.set_NZVC(alu.test_nz8(self.regs.B))
    
    def _op_tst(self, mode, ops):
        addr = ops[0]
        val = self.mem.read8(addr)
        self.regs.set_NZVC(alu.test_nz8(val))
    
    # ── Shift/Rotate handlers ──
    
    def _op_asla(self, mode, ops):
        result, flags = alu.asl8(self.regs.A)
        self.regs.A = result
        self.regs.set_NZVC(flags)
    
    def _op_aslb(self, mode, ops):
        result, flags = alu.asl8(self.regs.B)
        self.regs.B = result
        self.regs.set_NZVC(flags)
    
    def _op_asl(self, mode, ops):
        addr = ops[0]
        val = self.mem.read8(addr)
        result, flags = alu.asl8(val)
        self.mem.write8(addr, result)
        self.regs.set_NZVC(flags)
    
    def _op_asra(self, mode, ops):
        result, flags = alu.asr8(self.regs.A)
        self.regs.A = result
        self.regs.set_NZVC(flags)
    
    def _op_asrb(self, mode, ops):
        result, flags = alu.asr8(self.regs.B)
        self.regs.B = result
        self.regs.set_NZVC(flags)
    
    def _op_asr(self, mode, ops):
        addr = ops[0]
        val = self.mem.read8(addr)
        result, flags = alu.asr8(val)
        self.mem.write8(addr, result)
        self.regs.set_NZVC(flags)
    
    def _op_lsra(self, mode, ops):
        result, flags = alu.lsr8(self.regs.A)
        self.regs.A = result
        self.regs.set_NZVC(flags)
    
    def _op_lsrb(self, mode, ops):
        result, flags = alu.lsr8(self.regs.B)
        self.regs.B = result
        self.regs.set_NZVC(flags)
    
    def _op_lsr(self, mode, ops):
        addr = ops[0]
        val = self.mem.read8(addr)
        result, flags = alu.lsr8(val)
        self.mem.write8(addr, result)
        self.regs.set_NZVC(flags)
    
    def _op_lsld(self, mode, ops):
        result, flags = alu.asl16(self.regs.D)
        self.regs.D = result
        self.regs.set_NZVC(flags)
    
    def _op_lsrd(self, mode, ops):
        result, flags = alu.lsr16(self.regs.D)
        self.regs.D = result
        self.regs.set_NZVC(flags)
    
    def _op_rola(self, mode, ops):
        result, flags = alu.rol8(self.regs.A, int(self.regs.carry))
        self.regs.A = result
        self.regs.set_NZVC(flags)
    
    def _op_rolb(self, mode, ops):
        result, flags = alu.rol8(self.regs.B, int(self.regs.carry))
        self.regs.B = result
        self.regs.set_NZVC(flags)
    
    def _op_rol(self, mode, ops):
        addr = ops[0]
        val = self.mem.read8(addr)
        result, flags = alu.rol8(val, int(self.regs.carry))
        self.mem.write8(addr, result)
        self.regs.set_NZVC(flags)
    
    def _op_rora(self, mode, ops):
        result, flags = alu.ror8(self.regs.A, int(self.regs.carry))
        self.regs.A = result
        self.regs.set_NZVC(flags)
    
    def _op_rorb(self, mode, ops):
        result, flags = alu.ror8(self.regs.B, int(self.regs.carry))
        self.regs.B = result
        self.regs.set_NZVC(flags)
    
    def _op_ror(self, mode, ops):
        addr = ops[0]
        val = self.mem.read8(addr)
        result, flags = alu.ror8(val, int(self.regs.carry))
        self.mem.write8(addr, result)
        self.regs.set_NZVC(flags)
    
    # ── Clear handlers ──
    
    def _op_clra(self, mode, ops):
        self.regs.A = 0
        self.regs.set_NZVC(alu.CC_Z)
    
    def _op_clrb(self, mode, ops):
        self.regs.B = 0
        self.regs.set_NZVC(alu.CC_Z)
    
    def _op_clr(self, mode, ops):
        addr = ops[0]
        self.mem.write8(addr, 0)
        self.regs.set_NZVC(alu.CC_Z)
    
    # ── Branch handlers ──
    
    def _op_bra(self, mode, ops):
        self.regs.PC = ops[0]
    
    def _op_brn(self, mode, ops):
        pass  # Never branch (2-byte NOP)
    
    def _op_beq(self, mode, ops):
        if self.regs.zero:
            self.regs.PC = ops[0]
    
    def _op_bne(self, mode, ops):
        if not self.regs.zero:
            self.regs.PC = ops[0]
    
    def _op_bcc(self, mode, ops):
        if not self.regs.carry:
            self.regs.PC = ops[0]
    
    def _op_bcs(self, mode, ops):
        if self.regs.carry:
            self.regs.PC = ops[0]
    
    def _op_bge(self, mode, ops):
        if self.regs.negative == self.regs.overflow:
            self.regs.PC = ops[0]
    
    def _op_bgt(self, mode, ops):
        if not self.regs.zero and (self.regs.negative == self.regs.overflow):
            self.regs.PC = ops[0]
    
    def _op_ble(self, mode, ops):
        if self.regs.zero or (self.regs.negative != self.regs.overflow):
            self.regs.PC = ops[0]
    
    def _op_blt(self, mode, ops):
        if self.regs.negative != self.regs.overflow:
            self.regs.PC = ops[0]
    
    def _op_bhi(self, mode, ops):
        if not self.regs.carry and not self.regs.zero:
            self.regs.PC = ops[0]
    
    def _op_bls(self, mode, ops):
        if self.regs.carry or self.regs.zero:
            self.regs.PC = ops[0]
    
    def _op_bmi(self, mode, ops):
        if self.regs.negative:
            self.regs.PC = ops[0]
    
    def _op_bpl(self, mode, ops):
        if not self.regs.negative:
            self.regs.PC = ops[0]
    
    def _op_bvc(self, mode, ops):
        if not self.regs.overflow:
            self.regs.PC = ops[0]
    
    def _op_bvs(self, mode, ops):
        if self.regs.overflow:
            self.regs.PC = ops[0]
    
    def _op_bsr(self, mode, ops):
        self.regs.push16(self.mem, self.regs.PC)
        self.regs.PC = ops[0]
    
    # ── Jump/Call handlers ──
    
    def _op_jmp(self, mode, ops):
        self.regs.PC = ops[0]
    
    def _op_jsr(self, mode, ops):
        self.regs.push16(self.mem, self.regs.PC)
        self.regs.PC = ops[0]
    
    def _op_rts(self, mode, ops):
        self.regs.PC = self.regs.pull16(self.mem)
    
    def _op_rti(self, mode, ops):
        """Return from interrupt — restore all registers from stack.
        HC11 RTI pull order (reverse of push): CCR, B, A, X(hi,lo), Y(hi,lo), PC(hi,lo)
        CRITICAL: X bit in CCR can only be cleared, never set (0→1 forbidden).
        Cross-ref: HC11 RM Section 6.4, EVBU PySim11/ops.py RTI handler.
        """
        new_cc = self.regs.pull8(self.mem)
        self.regs.B = self.regs.pull8(self.mem)
        self.regs.A = self.regs.pull8(self.mem)
        self.regs.X = self.regs.pull16(self.mem)
        self.regs.Y = self.regs.pull16(self.mem)
        self.regs.PC = self.regs.pull16(self.mem)
        # X bit can be cleared but not set (0→1 forbidden by hardware)
        old_x = self.regs.CC & CC_X
        self.regs.CC = (new_cc & ~CC_X) | (new_cc & old_x)
    
    # ── Stack handlers ──
    
    def _op_psha(self, mode, ops):
        self.regs.push8(self.mem, self.regs.A)
    
    def _op_pshb(self, mode, ops):
        self.regs.push8(self.mem, self.regs.B)
    
    def _op_pshx(self, mode, ops):
        self.regs.push16(self.mem, self.regs.X)
    
    def _op_pshy(self, mode, ops):
        self.regs.push16(self.mem, self.regs.Y)
    
    def _op_pula(self, mode, ops):
        self.regs.A = self.regs.pull8(self.mem)
    
    def _op_pulb(self, mode, ops):
        self.regs.B = self.regs.pull8(self.mem)
    
    def _op_pulx(self, mode, ops):
        self.regs.X = self.regs.pull16(self.mem)
    
    def _op_puly(self, mode, ops):
        self.regs.Y = self.regs.pull16(self.mem)
    
    # ── Transfer handlers ──
    
    def _op_tab(self, mode, ops):
        self.regs.B = self.regs.A
        self.regs.set_NZV(alu.test_nz8(self.regs.A))
    
    def _op_tba(self, mode, ops):
        self.regs.A = self.regs.B
        self.regs.set_NZV(alu.test_nz8(self.regs.B))
    
    def _op_tap(self, mode, ops):
        """Transfer A to CCR. X bit can only be cleared, not set."""
        a = self.regs.A
        old_cc = self.regs.CC
        self.regs.CC = (a & ~CC_X) | (a & old_cc & CC_X)
    
    def _op_tpa(self, mode, ops):
        self.regs.A = self.regs.CC
    
    def _op_tsx(self, mode, ops):
        self.regs.X = (self.regs.SP + 1) & 0xFFFF
    
    def _op_txs(self, mode, ops):
        self.regs.SP = (self.regs.X - 1) & 0xFFFF
    
    def _op_tsy(self, mode, ops):
        self.regs.Y = (self.regs.SP + 1) & 0xFFFF
    
    def _op_tys(self, mode, ops):
        self.regs.SP = (self.regs.Y - 1) & 0xFFFF
    
    def _op_xgdx(self, mode, ops):
        tmp = self.regs.D
        self.regs.D = self.regs.X
        self.regs.X = tmp
    
    def _op_xgdy(self, mode, ops):
        tmp = self.regs.D
        self.regs.D = self.regs.Y
        self.regs.Y = tmp
    
    def _op_inx(self, mode, ops):
        self.regs.X = (self.regs.X + 1) & 0xFFFF
        self.regs.set_Z(alu.CC_Z if self.regs.X == 0 else 0)
    
    def _op_dex(self, mode, ops):
        self.regs.X = (self.regs.X - 1) & 0xFFFF
        self.regs.set_Z(alu.CC_Z if self.regs.X == 0 else 0)
    
    def _op_iny(self, mode, ops):
        self.regs.Y = (self.regs.Y + 1) & 0xFFFF
        self.regs.set_Z(alu.CC_Z if self.regs.Y == 0 else 0)
    
    def _op_dey(self, mode, ops):
        self.regs.Y = (self.regs.Y - 1) & 0xFFFF
        self.regs.set_Z(alu.CC_Z if self.regs.Y == 0 else 0)
    
    def _op_ins(self, mode, ops):
        self.regs.SP = (self.regs.SP + 1) & 0xFFFF
    
    def _op_des(self, mode, ops):
        self.regs.SP = (self.regs.SP - 1) & 0xFFFF
    
    # ── Bit manipulation handlers ──
    
    def _op_bset(self, mode, ops):
        addr, mask = ops[0], ops[1]
        val = self.mem.read8(addr) | mask
        self.mem.write8(addr, val & 0xFF)
        self.regs.set_NZV(alu.test_nz8(val))
    
    def _op_bclr(self, mode, ops):
        addr, mask = ops[0], ops[1]
        val = self.mem.read8(addr) & (~mask & 0xFF)
        self.mem.write8(addr, val)
        self.regs.set_NZV(alu.test_nz8(val))
    
    def _op_brset(self, mode, ops):
        addr, mask, target = ops[0], ops[1], ops[2]
        val = self.mem.read8(addr)
        if (val & mask) == mask:
            self.regs.PC = target
    
    def _op_brclr(self, mode, ops):
        addr, mask, target = ops[0], ops[1], ops[2]
        val = self.mem.read8(addr)
        if (val & mask) == 0:
            self.regs.PC = target
    
    # ── CCR manipulation ──
    
    def _op_sei(self, mode, ops):
        self.regs.set_I(CC_I)
    
    def _op_cli(self, mode, ops):
        self.regs.set_I(0)
    
    def _op_sev(self, mode, ops):
        self.regs.set_V(alu.CC_V)
    
    def _op_clv(self, mode, ops):
        self.regs.set_V(0)
    
    def _op_sec(self, mode, ops):
        self.regs.set_C(alu.CC_C)
    
    def _op_clc(self, mode, ops):
        self.regs.set_C(0)
    
    # ── Control ──
    
    def _op_nop(self, mode, ops):
        pass
    
    def _op_wai(self, mode, ops):
        raise _HaltException("WAI")
    
    def _op_swi(self, mode, ops):
        """Software Interrupt — push all registers, jump to SWI vector.
        HC11 SWI push order: PC(hi,lo), Y(hi,lo), X(hi,lo), A, B, CCR
        Cross-ref: HC11 RM Section 6.4, EVBU PySim11/ops.py SWI handler.
        """
        self.regs.push16(self.mem, self.regs.PC)
        self.regs.push16(self.mem, self.regs.Y)
        self.regs.push16(self.mem, self.regs.X)
        self.regs.push8(self.mem, self.regs.A)
        self.regs.push8(self.mem, self.regs.B)
        self.regs.push8(self.mem, self.regs.CC)
        self.regs.set_I(CC_I)
        self.regs.PC = self.mem.read16(0xFFF6)  # SWI vector at $FFF6-$FFF7
    
    def _op_stop(self, mode, ops):
        raise _StopException("STOP")
    
    def _op_test(self, mode, ops):
        raise _HaltException("TEST")
    
    # ══════════════════════════════════════════════
    # Breakpoint API
    # ══════════════════════════════════════════════
    
    def add_breakpoint(self, addr: int):
        """Add a breakpoint at PC address. Execution stops when PC hits this."""
        self._breakpoints.add(addr & 0xFFFF)
    
    def remove_breakpoint(self, addr: int):
        self._breakpoints.discard(addr & 0xFFFF)
    
    def clear_breakpoints(self):
        self._breakpoints.clear()
    
    # ══════════════════════════════════════════════
    # Trace / Debug
    # ══════════════════════════════════════════════
    
    def enable_trace(self, enable: bool = True):
        """Enable instruction trace logging."""
        self._trace = enable
    
    def get_trace(self) -> str:
        return '\n'.join(self._trace_output)
    
    def clear_trace(self):
        self._trace_output.clear()
    
    def reset(self):
        """Full emulator reset."""
        self.regs.reset()
        self.sci.reset()
        self.adc.reset()
        self.ports.reset()
        self.timer.reset()
        self._breakpoints.clear()
        self._trace_output.clear()


# Internal exceptions for flow control
class _HaltException(Exception):
    pass

class _StopException(Exception):
    pass
