#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════
 XDF Label Map — Calibration data from TunerPro XDF exports
═══════════════════════════════════════════════════════════════════════
 Loads the JSON export produced by tunerpro_exporter.py and builds a
 lookup table of all XDF-defined addresses: scalars, flags, tables,
 and axis breakpoints.

 This module is COMPLETELY INDEPENDENT of hw_labels.py.
 It knows nothing about HC11 registers, RAM, ISRs, or vectors.
 Its only data source is the XDF JSON file.

 REQUIRES: Enhanced_v1.json (or equivalent XDF export)
   This file is NOT auto-generated — it comes from running
   tunerpro_exporter.py against the .xdf definition file.
   It MUST be kept in the repo or regenerated from the .xdf.

 Usage:
   from xdf_labels import XDFLabelMap

   xdf = XDFLabelMap("Enhanced_v1.json", bank=1)
   print(xdf.lookup(0x77DE))  # Rev Limit High = 236 RPM * 25
   print(xdf.stats())

═══════════════════════════════════════════════════════════════════════
 Author:  Jason King (KingAI)
 Version: 1.0 — February 2026
═══════════════════════════════════════════════════════════════════════
"""

import json
from typing import Dict, Optional


# ─────────────────────────────────────────────────────────────────────
#  ADDRESS TRANSLATION
# ─────────────────────────────────────────────────────────────────────
# XDF addresses are file offsets in the 128KB binary (BASEOFFSET=0).
# CPU addresses are what the HC11 sees after bank switching.
#
# Bank1: file[0x00000:0x10000] → CPU $0000-$FFFF  (64KB, cal + code)
# Bank2: file[0x10000:0x18000] → CPU $8000-$FFFF  (32KB, code only)
# Bank3: file[0x18000:0x20000] → CPU $8000-$FFFF  (32KB, code only)
#
# Calibration data: XDF $4000-$7FFC → Bank1 CPU $4000-$7FFC
# COMMON area $2000-$7FFF is visible from ALL banks (no bank switch).
# ─────────────────────────────────────────────────────────────────────

BANK_MAP = {
    1: (0x00000, 0x10000, 0x0000),  # 64KB: CPU $0000-$FFFF
    2: (0x10000, 0x18000, 0x8000),  # 32KB: CPU $8000-$FFFF
    3: (0x18000, 0x20000, 0x8000),  # 32KB: CPU $8000-$FFFF
}

CAL_RANGE = (0x2000, 0x8000)  # $2000-$7FFF calibration data


def xdf_addr_to_cpu(xdf_addr: int, bank: int = 1) -> Optional[int]:
    """Convert XDF file offset to CPU address for a given bank."""
    file_start, file_end, cpu_base = BANK_MAP[bank]
    if file_start <= xdf_addr < file_end:
        return cpu_base + (xdf_addr - file_start)
    return None


def cpu_to_xdf_addr(cpu_addr: int, bank: int = 1) -> int:
    """Convert CPU address back to XDF file offset."""
    file_start, _, cpu_base = BANK_MAP[bank]
    return file_start + (cpu_addr - cpu_base)


# ─────────────────────────────────────────────────────────────────────
#  XDFLabelMap CLASS
# ─────────────────────────────────────────────────────────────────────

class XDFLabelMap:
    """
    Loads XDF export JSON and builds lookup tables for calibration
    addresses (scalars, flags, tables, axis breakpoints).

    All 1655 addresses live in the $4000-$7FFC calibration region.
    Code in ANY bank can reference these via extended addressing
    (e.g. ldaa $77DE → Rev Limit High).
    """

    def __init__(self, json_path: str, bank: int = 1):
        self.bank = bank
        self.scalars: Dict[int, dict] = {}
        self.flags: Dict[int, dict] = {}
        self.tables: Dict[int, dict] = {}
        self.table_axes: Dict[int, dict] = {}
        self.all_addrs: Dict[int, str] = {}
        self.definition_name = "Unknown"
        self.bin_name = "Unknown"
        # Always load as bank1 — calibration is in bank1 file region
        self._load(json_path, load_bank=1)

    def _load(self, json_path: str, load_bank: int = 1):
        with open(json_path, 'r') as f:
            data = json.load(f)

        meta = data.get('metadata', {})
        self.definition_name = meta.get(
            'source_definition', 'Unknown'
        )
        self.bin_name = meta.get('source_file', 'Unknown')

        # ── Scalars ──
        for s in data.get('scalars', []):
            addr_str = s.get('address')
            if not addr_str:
                continue
            xdf_addr = int(addr_str, 16)
            cpu_addr = xdf_addr_to_cpu(xdf_addr, load_bank)
            if cpu_addr is not None:
                self.scalars[cpu_addr] = s
                title = s.get('title', '')
                val = s.get('value', '')
                unit = s.get('unit', '')
                entry = f"{title} = {val} {unit}".strip()
                if cpu_addr in self.all_addrs:
                    self.all_addrs[cpu_addr] += f" | {entry}"
                else:
                    self.all_addrs[cpu_addr] = entry

        # ── Flags ──
        for f_entry in data.get('flags', []):
            addr_str = f_entry.get('address')
            if not addr_str:
                continue
            xdf_addr = int(addr_str, 16)
            cpu_addr = xdf_addr_to_cpu(xdf_addr, load_bank)
            if cpu_addr is not None:
                self.flags[cpu_addr] = f_entry
                title = f_entry.get('title', '')
                mask = f_entry.get('mask', '')
                is_set = f_entry.get('is_set', False)
                state = "SET" if is_set else "NOT SET"
                tag = f"[FLAG] {title} mask={mask} ({state})"
                if cpu_addr not in self.all_addrs:
                    self.all_addrs[cpu_addr] = tag
                else:
                    self.all_addrs[cpu_addr] += (
                        f" | [FLAG] {title} ({state})"
                    )

        # ── Tables (z-axis = data start) ──
        for t in data.get('tables', []):
            axes = t.get('axes', {})
            z = axes.get('z', {})
            z_addr_str = z.get('address')
            if z_addr_str:
                xdf_addr = int(z_addr_str, 16)
                cpu_addr = xdf_addr_to_cpu(xdf_addr, load_bank)
                if cpu_addr is not None:
                    self.tables[cpu_addr] = t
                    dims = t.get('dimensions', {})
                    rows = dims.get('rows', 0)
                    cols = dims.get('cols', 0)
                    title = t.get('title', '')
                    if cpu_addr not in self.all_addrs:
                        self.all_addrs[cpu_addr] = (
                            f"[TABLE {rows}x{cols}] {title}"
                        )

            # X/Y axis addresses
            for axis_id in ('x', 'y'):
                ax = axes.get(axis_id, {})
                ax_addr_str = ax.get('address')
                if ax_addr_str:
                    xdf_addr = int(ax_addr_str, 16)
                    cpu_addr = xdf_addr_to_cpu(
                        xdf_addr, load_bank
                    )
                    if cpu_addr is not None:
                        title = t.get('title', '')
                        ax_unit = ax.get('unit', '')
                        count = ax.get('count', 0)
                        self.table_axes[cpu_addr] = {
                            'table_title': title,
                            'axis': axis_id.upper(),
                            'unit': ax_unit,
                            'count': count,
                        }
                        if cpu_addr not in self.all_addrs:
                            aid = axis_id.upper()
                            self.all_addrs[cpu_addr] = (
                                f"[{aid}-AXIS of {title}]"
                                f" {count} pts, {ax_unit}"
                            )

    def lookup(self, cpu_addr: int) -> Optional[str]:
        """Get the XDF annotation for a CPU address, or None."""
        return self.all_addrs.get(cpu_addr)

    def get_scalar(self, cpu_addr: int) -> Optional[dict]:
        return self.scalars.get(cpu_addr)

    def get_flag(self, cpu_addr: int) -> Optional[dict]:
        return self.flags.get(cpu_addr)

    def get_table(self, cpu_addr: int) -> Optional[dict]:
        return self.tables.get(cpu_addr)

    def stats(self) -> dict:
        return {
            'scalars': len(self.scalars),
            'flags': len(self.flags),
            'tables': len(self.tables),
            'table_axes': len(self.table_axes),
            'total_unique': len(self.all_addrs),
            'addr_range': (
                f"${min(self.all_addrs):04X}"
                if self.all_addrs else "N/A",
                f"${max(self.all_addrs):04X}"
                if self.all_addrs else "N/A",
            ),
        }

    def __len__(self):
        return len(self.all_addrs)

    def __contains__(self, addr):
        return addr in self.all_addrs


# ─────────────────────────────────────────────────────────────────────
#  Self-test
# ─────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python xdf_labels.py <Enhanced_v1.json>")
        sys.exit(1)

    xdf = XDFLabelMap(sys.argv[1])
    s = xdf.stats()
    print(f"XDFLabelMap: {s['total_unique']} addresses")
    print(f"  {s['scalars']} scalars, {s['flags']} flags, "
          f"{s['tables']} tables, {s['table_axes']} axes")
    print(f"  Range: {s['addr_range'][0]} - {s['addr_range'][1]}")
    print(f"  Definition: {xdf.definition_name}")
    print(f"  Binary: {xdf.bin_name}")
    print()
    print("Sample lookups:")
    for addr in [0x4000, 0x77DE, 0x77DD, 0x77E0, 0x7FF0]:
        ann = xdf.lookup(addr)
        if ann:
            print(f"  ${addr:04X}: {ann}")
