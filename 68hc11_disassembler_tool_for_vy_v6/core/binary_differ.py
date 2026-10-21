#!/usr/bin/env python3
"""Read-only binary comparison for offline ECU research.

Reports changed bytes in the common region AND unmatched trailing bytes. A
same-prefix/different-size pair is never described as equal. Difference spans
are byte offsets, not calibrated tables or evidence of ECU compatibility.
JSON output is exclusive-create; original files and existing reports are never
replaced. This remains a legacy research utility, not a flash verifier.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
from typing import Dict, List


def _aliases(a: Path, b: Path) -> bool:
    """Detect path, symlink and hardlink aliases before writing a report."""
    if os.path.normcase(str(a.resolve())) == os.path.normcase(str(b.resolve())):
        return True
    try:
        return a.samefile(b)
    except OSError:
        return False


class BinaryDiffer:
    """Byte-level comparison. No ECU hardware communication or file patching."""

    def __init__(self, file1: str, file2: str):
        self.file1, self.file2 = Path(file1), Path(file2)
        for path in (self.file1, self.file2):
            if not path.is_file():
                raise FileNotFoundError(f"Regular input file not found: {path}")
        self.data1, self.data2 = self.file1.read_bytes(), self.file2.read_bytes()
        self.size1, self.size2 = len(self.data1), len(self.data2)

    def _regions(self) -> list[dict]:
        """List maximal changed common spans plus a distinct unmatched tail."""
        length = min(self.size1, self.size2)
        regions: list[dict] = []
        start: int | None = None
        for position in range(length):
            different = self.data1[position] != self.data2[position]
            if different and start is None:
                start = position
            elif not different and start is not None:
                regions.append({'start': start, 'end': position - 1,
                                'length': position - start, 'kind': 'changed'})
                start = None
        if start is not None:
            regions.append({'start': start, 'end': length - 1,
                            'length': length - start, 'kind': 'changed'})
        if self.size1 != self.size2:
            regions.append({'start': length, 'end': max(self.size1, self.size2) - 1,
                            'length': abs(self.size1 - self.size2),
                            'kind': 'only_in_file1' if self.size1 > self.size2 else 'only_in_file2'})
        return regions

    def compare(self, context_bytes: int = 16, *, verbose: bool = True) -> Dict:
        if type(context_bytes) is not int or not 0 <= context_bytes <= 4096:
            raise ValueError('context_bytes must be an integer from 0 to 4096')
        regions = self._regions()
        common_changed = sum(r['length'] for r in regions if r['kind'] == 'changed')
        trailing = abs(self.size1 - self.size2)
        total = common_changed + trailing
        longest = max(self.size1, self.size2)
        report = {
            'file1': str(self.file1), 'file2': str(self.file2),
            'size1': self.size1, 'size2': self.size2,
            'sha256_file1': hashlib.sha256(self.data1).hexdigest(),
            'sha256_file2': hashlib.sha256(self.data2).hexdigest(),
            'identical': total == 0,
            'common_changed_bytes': common_changed,
            'trailing_diff_bytes': trailing,
            'total_diff_bytes': total,
            'percent_different': (total / longest * 100) if longest else 0.0,
            'diff_regions': regions,
            'warning': 'Byte differences do not identify tuning tables, ECU compatibility or flash safety.',
        }
        if verbose:
            print(f'BINARY COMPARISON\nFile 1: {self.file1.name} ({self.size1:,} bytes)'
                  f'\nFile 2: {self.file2.name} ({self.size2:,} bytes)')
            if trailing:
                print(f'WARNING: image lengths differ by {trailing:,} bytes.')
            print(f'Different/unmatched bytes: {total:,} ({report["percent_different"]:.2f}%)'
                  f'\nCommon-region changes: {common_changed:,}; unmatched trailing: {trailing:,}'
                  f'\nDifference regions: {len(regions)}')
            for index, region in enumerate(regions[:20], 1):
                print(f'  #{index}: 0x{region["start"]:06X}-0x{region["end"]:06X}'
                      f' ({region["length"]} bytes; {region["kind"]})')
                if region['length'] <= 64:
                    self._print_hex_diff(region['start'], region['end'], context_bytes)
            if len(regions) > 20:
                print(f'... {len(regions)-20} more regions (all retained in JSON report)')
        return report

    def _print_hex_diff(self, start: int, end: int, context: int):
        first = max(0, start - context)
        last = min(max(self.size1, self.size2), end + context + 1)
        for offset in range(first, last, 16):
            boundary = min(offset + 16, last)
            left = ' '.join(f'{v:02X}' for v in self.data1[offset:boundary])
            right = ' '.join(f'{v:02X}' for v in self.data2[offset:boundary])
            marker = '>>>' if offset <= end and boundary > start else '   '
            print(f'{marker} {offset:06X} | {left:<47} | {right}')

    def export_diff_map(self, output_file: str):
        """Create a report without replacing any existing path, even an input alias."""
        path = Path(output_file)
        for source in (self.file1, self.file2):
            if _aliases(path, source):
                raise ValueError(f'Report output aliases an input: {path}')
        if path.exists() or path.is_symlink():
            raise FileExistsError(f'Refusing to overwrite an existing report: {path}')
        if not path.parent.is_dir():
            raise FileNotFoundError(f'Report parent directory does not exist: {path.parent}')
        payload = json.dumps(self.compare(verbose=False), indent=2, allow_nan=False) + '\n'
        # Exclusive-create is atomic with respect to competing creators.
        # Clean up only if *this invocation* actually opened the new file.
        created = False
        try:
            with path.open('x', encoding='utf-8') as handle:
                created = True
                handle.write(payload)
        except BaseException:
            if created:
                path.unlink(missing_ok=True)
            raise
        print(f'Difference map created: {path}')

    def find_tables(self, min_size: int = 16) -> List[Dict]:
        """Return size-filtered *candidates*, never claimed ECU tuning maps."""
        if type(min_size) is not int or min_size <= 0:
            raise ValueError('min_size must be a positive integer')
        candidates = []
        for region in self._regions():
            if region['kind'] != 'changed' or region['length'] < min_size:
                continue  # Missing trailing data cannot safely be classified as a table.
            s, e = region['start'], region['end']
            candidates.append({'address': f'0x{s:06X}', 'size': region['length'],
                               'potential_type': self._guess_table_type(self.data1[s:e+1],
                                                                         self.data2[s:e+1])})
        print(f'Continuous changed-region candidates: {len(candidates)} (heuristic only)')
        return candidates

    def _guess_table_type(self, data1: bytes, data2: bytes) -> str:
        if data1 and len(data1) % 2 == 0:
            values = [int.from_bytes(data1[i:i+2], 'big') for i in range(0, len(data1), 2)]
            if all(0 <= v <= 100 for v in values):
                return 'Percentage/Factor Table (heuristic)'
            if all(500 <= v <= 8000 for v in values):
                return 'RPM Table (heuristic)'
            if all(0 <= v <= 255 for v in values):
                return 'Scalar/Byte Table (heuristic)'
        return 'Unknown Table Type'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file1', help='Original read-only BIN/image')
    parser.add_argument('file2', help='Comparison read-only BIN/image')
    parser.add_argument('-o', '--output', help='Create JSON receipt at an unused path')
    parser.add_argument('-c', '--context', type=int, default=16)
    parser.add_argument('--find-tables', action='store_true', help='Heuristic candidates only')
    args = parser.parse_args(argv)
    try:
        differ = BinaryDiffer(args.file1, args.file2)
        differ.compare(context_bytes=args.context)
        if args.find_tables:
            differ.find_tables()
        if args.output:
            differ.export_diff_map(args.output)
    except (OSError, ValueError) as exc:
        parser.exit(2, f'error: {exc}\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
