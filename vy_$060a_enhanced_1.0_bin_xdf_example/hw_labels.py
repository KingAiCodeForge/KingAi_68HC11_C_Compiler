#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════
 HC11 Hardware / RAM / ISR / Vector Label Map
═══════════════════════════════════════════════════════════════════════
 STANDALONE module — no dependency on XDF data or JSON files.
 Everything here is from binary analysis + HC11 documentation.

 Sources:
   - vy_v6_constants.py (verified RAM addresses, HC11_REGISTERS)
   - split_and_disassemble.py (KNOWN_LABELS, VECTORS, HC11_VARIANT/COMMON)
   - NXP/Motorola 68HC11 Reference Manual (register map)
   - Chr0m3 Motorsport testing (RAM variable verification)
   - TIC3 ISR disassembly 2026-01-31 (ISR entry points)

 CORRECTIONS LOG — What We Got Wrong:
 ─────────────────────────────────────
 2026-01-16: HC11E9 @ 2MHz → CORRECTED to HC11FC0 @ 3.408MHz
             Source: DARC.BIN line 7, VL400 topic_982, Antus scope
 2026-01-16: MIN_DWELL 0xA2 → was from OSE12P (32KB), NOT VY V6
             VY actually uses 0x20 (32) for Delta Cylair/Dwell threshold
 2026-02-09: $017B "crank period" → CORRECTED to "dwell intermediate"
             Actual 24X crank period is at $194C (TIC3 ISR, bank2)
 2026-02-20: $00A2 "unknown RAM" → CONFIRMED as RPM (82 reads, 2 writes)
             v1 labeler had NO way to show this — ldaa $a2 was invisible

 Usage:
   from hw_labels import HWLabelMap

   hw = HWLabelMap()
   print(hw.lookup(0x00A2))  # [RAM] RPM — Engine RPM (82R, 2W)
   print(hw.lookup(0x1020))  # [HW] TCTL1 — Timer Control 1 — EST output mode
   print(hw.lookup(0x35FF))  # [ISR] ISR_TIC3_24X — 24X Crank Sensor ISR

═══════════════════════════════════════════════════════════════════════
 Author:  Jason King (KingAI)
 Version: 1.0 — February 2026
═══════════════════════════════════════════════════════════════════════
"""

from typing import Dict, Optional
from collections import defaultdict


# ─────────────────────────────────────────────────────────────────────
#  HC11 REGISTERS $1000-$100D: VARIANT-DEPENDENT
# ─────────────────────────────────────────────────────────────────────
# The exact HC11 derivative in the VY V6 Delco P04 is UNCONFIRMED.
# DARC disassembly (VT V6 SC — DIFFERENT ECU) claims HC11FC0.
# For $1000-$100D where variants disagree, we show HC11F (most likely)
# with alternatives noted. $100E+ is same on all HC11 variants.
# ─────────────────────────────────────────────────────────────────────

HC11_VARIANT_REGISTERS = {
    0x1000: ("PORTA", "Port A data (all variants)"),
    0x1001: ("DDRA", "Port A DDR (HC11F/G/K) | Reserved (HC11E)"),
    0x1002: ("PORTG", "Port G / bank switch (HC11F/K) | PIOC (HC11E/G)"),
    0x1003: ("DDRG", "Port G DDR (HC11F/K) | PORTC (HC11E/G)"),
    0x1004: ("PORTB", "Port B data (all variants)"),
    0x1005: ("PORTF", "Port F (HC11F/K) | PORTCL (HC11E/G)"),
    0x1006: ("PORTC", "Port C data (HC11F/K) | Reserved (HC11E/G)"),
    0x1007: ("DDRC", "Port C DDR (all variants)"),
    0x1008: ("PORTD", "Port D data PD5-PD0 (all variants)"),
    0x1009: ("DDRD", "Port D DDR (all variants)"),
    0x100A: ("PORTE", "Port E data — ADC inputs (all variants)"),
    0x100B: ("CFORC", "Timer Compare Force (all variants)"),
    0x100C: ("OC1M", "OC1 Action Mask Register (all variants)"),
    0x100D: ("OC1D", "OC1 Action Data Register (all variants)"),
}

# ─────────────────────────────────────────────────────────────────────
#  HC11 REGISTERS $100E-$103F: IDENTICAL across all variants
# ─────────────────────────────────────────────────────────────────────

HC11_COMMON_REGISTERS = {
    0x100E: ("TCNT_H", "Timer Counter high byte"),
    0x100F: ("TCNT_L", "Timer Counter low byte"),
    0x1010: ("TIC1_H", "Input Capture 1 high"),
    0x1011: ("TIC1_L", "Input Capture 1 low"),
    0x1012: ("TIC2_H", "Input Capture 2 high — CAM"),
    0x1013: ("TIC2_L", "Input Capture 2 low — CAM"),
    0x1014: ("TIC3_H", "Input Capture 3 high — 24X Crank"),
    0x1015: ("TIC3_L", "Input Capture 3 low — 24X Crank"),
    0x1016: ("TOC1_H", "Output Compare 1 high"),
    0x1017: ("TOC1_L", "Output Compare 1 low"),
    0x1018: ("TOC2_H", "Output Compare 2 high — Dwell"),
    0x1019: ("TOC2_L", "Output Compare 2 low — Dwell"),
    0x101A: ("TOC3_H", "Output Compare 3 high — EST Spark"),
    0x101B: ("TOC3_L", "Output Compare 3 low — EST Spark"),
    0x101C: ("TOC4_H", "Output Compare 4 high"),
    0x101D: ("TOC4_L", "Output Compare 4 low"),
    0x101E: ("TOC5_H", "Output Compare 5 high"),
    0x101F: ("TOC5_L", "Output Compare 5 low"),
    0x1020: ("TCTL1", "Timer Control 1 — EST output mode"),
    0x1021: ("TCTL2", "Timer Control 2 — IC edge config"),
    0x1022: ("TMSK1", "Timer Interrupt Mask 1"),
    0x1023: ("TFLG1", "Timer Interrupt Flag 1"),
    0x1024: ("TMSK2", "Timer Interrupt Mask 2"),
    0x1025: ("TFLG2", "Timer Interrupt Flag 2"),
    0x1026: ("PACTL", "Pulse Accumulator Control"),
    0x1027: ("PACNT", "Pulse Accumulator Count"),
    0x1028: ("SPCR", "SPI Control Register"),
    0x1029: ("SPSR", "SPI Status Register"),
    0x102A: ("SPDR", "SPI Data Register"),
    0x102B: ("BAUD", "SCI Baud Rate"),
    0x102C: ("SCCR1", "SCI Control Register 1"),
    0x102D: ("SCCR2", "SCI Control Register 2"),
    0x102E: ("SCSR", "SCI Status Register"),
    0x102F: ("SCDR", "SCI Data Register — ALDL"),
    0x1030: ("ADCTL", "ADC Control/Status"),
    0x1031: ("ADR1", "ADC Result 1"),
    0x1032: ("ADR2", "ADC Result 2"),
    0x1033: ("ADR3", "ADC Result 3"),
    0x1034: ("ADR4", "ADC Result 4"),
    0x1035: ("BPROT", "Block Protect"),
    0x1039: ("OPTION", "System Configuration Options"),
    0x103A: ("COPRST", "COP Watchdog Reset"),
    0x103B: ("PPROG", "EEPROM Programming"),
    0x103C: ("HPRIO", "Highest Priority I-Bit"),
    0x103D: ("INIT", "RAM/IO Mapping Register"),
    0x103F: ("CONFIG", "System Configuration"),
}

# ─────────────────────────────────────────────────────────────────────
#  CONFIRMED RAM ADDRESSES
# ─────────────────────────────────────────────────────────────────────
# Verified by binary analysis + XDF cross-reference + TIC3 ISR disasm.
#
# BEFORE v2:  ldaa $a2  → no annotation (invisible, unknown)
# AFTER v2:   ldaa $a2  ; [RAM] RPM — Engine RPM (82R, 2W)
#
# BEFORE v2:  std $0199 → no annotation
# AFTER v2:   std $0199 ; [RAM] DWELL_RAM — Dwell time (3 STD, 1 LDD)
#
# CORRECTED 2026-02-09: $017B was labeled "crank_period" in early docs.
#   Actual: DWELL_INTERMEDIATE (dwell calc working variable).
#   Actual 24X crank period → $194C (stored in TIC3 ISR, bank2 only).
# ─────────────────────────────────────────────────────────────────────

RAM_ADDRESSES = {
    # Engine parameters — VERIFIED (72+ reads in code)
    0x0080: ("ENGINE_STATUS", "Engine status flags"),
    0x00A2: ("RPM", "Engine RPM (82R, 2W)"),
    0x00A3: ("RPM_HIGH", "RPM high byte — rev limiter"),

    # Timing — VERIFIED (TIC3 ISR disassembly 2026-01-31)
    0x017B: ("DWELL_INTERMEDIATE", "Dwell intermediate calc (was mislabeled crank_period)"),
    0x0199: ("DWELL_RAM", "Dwell time (3 STD, 1 LDD)"),
    0x194C: ("CRANK_PERIOD_24X", "24X crank period (bank2 CCP/purge logic at $B30A+, NOT in TIC3 ISR)"),
}

# ─────────────────────────────────────────────────────────────────────
#  ISR HANDLERS & SUBROUTINE NAMES
# ─────────────────────────────────────────────────────────────────────
# From split_and_disassemble.py KNOWN_LABELS + vector table analysis.
# These are ALL in bank1 COMMON area ($2000-$3FFF) so visible from
# any bank's code via JMP/JSR.
# ─────────────────────────────────────────────────────────────────────

ISR_AND_CODE_LABELS = {
    # Pseudo-vector JMP table ($2000-$2021)
    # HC11 vectors → here → JMP to actual ISR handler
    0x2000: ("JMP_Default", "SPI/PAIE/PAO/TOF/TOC5/TOC2/RTI handler"),
    0x2003: ("JMP_SCI", "SCI serial (ALDL) redirect"),
    0x2006: ("JMP_TOC4", "Output Compare 4 redirect"),
    0x2009: ("JMP_TOC3_EST", "EST spark control redirect"),
    0x200C: ("JMP_TOC1", "Output Compare 1 redirect"),
    0x200F: ("JMP_TIC3_24X", "24X crank sensor redirect"),
    0x2012: ("JMP_TIC2_CAM", "CAM sensor redirect"),
    0x2015: ("JMP_TIC1", "Input Capture 1 redirect"),
    0x2018: ("JMP_IRQ", "Main interrupt redirect"),
    0x201B: ("JMP_XIRQ", "Non-maskable interrupt redirect"),
    0x201E: ("JMP_SWI", "Software interrupt redirect"),
    0x2021: ("JMP_ILLOP", "Illegal opcode trap redirect"),

    # Actual ISR handler entry points
    0x29D3: ("ISR_SCI", "Serial Communications ISR (ALDL)"),
    0x2BA0: ("ISR_SWI", "Software Interrupt handler"),
    0x2BA6: ("ISR_ILLOP", "Illegal Opcode Trap handler"),
    0x2BAC: ("ISR_XIRQ", "Non-Maskable Interrupt handler"),
    0x2BAF: ("ISR_Default_RTI", "Default RTI handler"),
    0x301F: ("ISR_TIC1", "Input Capture 1 ISR"),
    0x30BA: ("ISR_IRQ", "Main IRQ handler"),
    0x358A: ("ISR_TIC2_CAM", "CAM Sensor ISR"),
    0x35BD: ("ISR_TOC3_EST", "EST Spark Control ISR"),
    0x35DE: ("ISR_TOC4", "Output Compare 4 ISR"),
    0x35FF: ("ISR_TIC3_24X", "24X Crank Sensor ISR — CRITICAL"),
    0x3719: ("ISR_TIC3_RTS", "TIC3 ISR return point"),
    0x371A: ("Dwell_Calc", "Dwell calculation subroutine"),
    0x37A6: ("ISR_TOC1", "Output Compare 1 ISR"),

    # TIC3 ISR computed jump table (cylinder sync cases)
    0x361C: ("TIC3_Cyl_Sync", "TIC3 cylinder sync entry"),
    0x365C: ("TIC3_Cyl_0", "TIC3 cylinder 0"),
    0x3667: ("TIC3_Cyl_1", "TIC3 cylinder 1"),
    0x367D: ("TIC3_Cyl_2", "TIC3 cylinder 2"),
    0x368F: ("TIC3_Cyl_3", "TIC3 cylinder 3"),
    0x36A0: ("TIC3_Cyl_4", "TIC3 cylinder 4"),
    0x36AB: ("TIC3_Cyl_5", "TIC3 cylinder 5"),
    0x36E6: ("TIC3_Period_Calc", "TIC3 period calculation"),
    0x37B8: ("TOC1_Continue", "TOC1 ISR continuation"),
}

# ─────────────────────────────────────────────────────────────────────
#  INTERRUPT VECTOR TABLE ($FFD6-$FFFE)
# ─────────────────────────────────────────────────────────────────────
# Bank1 only. Each 16-bit entry points to the pseudo-vector JMP table
# at $2000-$2021, which then JMPs to the actual ISR code.
# ─────────────────────────────────────────────────────────────────────

VECTOR_TABLE = {
    0xFFD6: ("VEC_SCI", "Serial (ALDL) → $2003"),
    0xFFD8: ("VEC_SPI", "SPI → $2000"),
    0xFFDA: ("VEC_PAIE", "Pulse Accum Input Edge → $2000"),
    0xFFDC: ("VEC_PAO", "Pulse Accum Overflow → $2000"),
    0xFFDE: ("VEC_TOF", "Timer Overflow → $2000"),
    0xFFE0: ("VEC_TOC5", "Output Compare 5 → $2000"),
    0xFFE2: ("VEC_TOC4", "Output Compare 4 → $2006"),
    0xFFE4: ("VEC_TOC3", "EST Spark Control → $2009"),
    0xFFE6: ("VEC_TOC2", "Dwell Start → $2000"),
    0xFFE8: ("VEC_TOC1", "Output Compare 1 → $200C"),
    0xFFEA: ("VEC_TIC3", "24X Crank → $200F — CRITICAL"),
    0xFFEC: ("VEC_TIC2", "CAM Sensor → $2012"),
    0xFFEE: ("VEC_TIC1", "Input Capture 1 → $2015"),
    0xFFF0: ("VEC_RTI", "Real Time Interrupt → $2000"),
    0xFFF2: ("VEC_IRQ", "Main Interrupt → $2018"),
    0xFFF4: ("VEC_XIRQ", "Non-Maskable → $201B"),
    0xFFF6: ("VEC_SWI", "Software Interrupt → $201E"),
    0xFFF8: ("VEC_ILLOP", "Illegal Opcode → $2021"),
    0xFFFA: ("VEC_COP", "COP Watchdog — bank1/2: BRA $2024 (∞ loop), bank3: $C015"),
    0xFFFC: ("VEC_CME", "Clock Monitor — bank1/2: BRA $2027 (∞ loop), bank3: $C019"),
    0xFFFE: ("VEC_RESET", "Reset — bank1/2: BRA $202A (∞ loop), bank3: $C011"),
}

# ─────────────────────────────────────────────────────────────────────
#  MISCELLANEOUS KNOWN ADDRESSES
# ─────────────────────────────────────────────────────────────────────

MISC_LABELS = {
    0x0E00: ("EEPROM_VIN", "VIN stored in EEPROM"),
    0x0F00: ("EEPROM_End", "End of EEPROM region"),
    0x4000: ("FlashCalStart", "Start of flash calibration"),
    0x4006: ("Checksum_HI", "Calibration checksum high"),
    0x4007: ("Checksum_LO", "Calibration checksum low"),
    0x7FF0: ("CalID", "Calibration ID"),
    0x8000: ("ProgROM_Start", "Start of program ROM"),
    0xFF80: ("ProgID", "Program identification"),
    0xC011: ("RESET_Handler", "Bank 0 reset entry"),
    0xC015: ("COP_Handler", "Bank 0 COP watchdog"),
    0xC019: ("CME_Handler", "Bank 0 clock monitor"),
}


# ─────────────────────────────────────────────────────────────────────
#  HWLabelMap CLASS — builds one merged lookup from all sources above
# ─────────────────────────────────────────────────────────────────────

class HWLabelMap:
    """
    Hardware / RAM / ISR / Vector label lookup.

    100% independent of XDF — no JSON file needed.
    Built entirely from HC11 documentation + verified binary analysis.

    Tags in output:
      [HW]   HC11 hardware register ($1000-$103F)
      [RAM]  Confirmed RAM variable
      [ISR]  ISR entry point / subroutine
      [JMP]  Pseudo-vector jump table entry ($2000-$2021)
      [VEC]  Interrupt vector table ($FFD6-$FFFE)
      [CODE] Other known code/data addresses
    """

    def __init__(self):
        self.labels: Dict[int, str] = {}
        self._build()

    def _build(self):
        # HC11 variant-dependent registers
        for addr, (name, desc) in HC11_VARIANT_REGISTERS.items():
            self.labels[addr] = f"[HW] {name} — {desc}"

        # HC11 common registers
        for addr, (name, desc) in HC11_COMMON_REGISTERS.items():
            self.labels[addr] = f"[HW] {name} — {desc}"

        # RAM addresses
        for addr, (name, desc) in RAM_ADDRESSES.items():
            self.labels[addr] = f"[RAM] {name} — {desc}"

        # ISR / subroutine names
        for addr, (name, desc) in ISR_AND_CODE_LABELS.items():
            tag = "[JMP]" if addr < 0x2030 else "[ISR]"
            self.labels[addr] = f"{tag} {name} — {desc}"

        # Vector table
        for addr, (name, desc) in VECTOR_TABLE.items():
            self.labels[addr] = f"[VEC] {name} — {desc}"

        # Misc (only if not already claimed by a more specific source)
        for addr, (name, desc) in MISC_LABELS.items():
            if addr not in self.labels:
                self.labels[addr] = f"[CODE] {name} — {desc}"

    def lookup(self, cpu_addr: int) -> Optional[str]:
        """Get HW/RAM/ISR annotation for a CPU address, or None."""
        return self.labels.get(cpu_addr)

    def stats(self) -> dict:
        """Count labels by tag type."""
        tags = defaultdict(int)
        for v in self.labels.values():
            tag = v.split(']')[0] + ']' if ']' in v else '?'
            tags[tag] += 1
        return dict(tags)

    def __len__(self):
        return len(self.labels)

    def __contains__(self, addr):
        return addr in self.labels


# ─────────────────────────────────────────────────────────────────────
#  Self-test
# ─────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    hw = HWLabelMap()
    stats = hw.stats()
    total = sum(stats.values())
    print(f"HWLabelMap: {total} labels")
    for tag, count in sorted(stats.items()):
        print(f"  {tag}: {count}")
    print()
    print("Sample lookups:")
    for addr in [0x00A2, 0x0199, 0x017B, 0x1020, 0x1023, 0x103A,
                 0x35FF, 0x371A, 0x2009, 0xFFEA, 0xFFFE, 0x0080]:
        ann = hw.lookup(addr)
        print(f"  ${addr:04X}: {ann}")
