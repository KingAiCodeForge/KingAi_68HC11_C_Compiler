"""Regression for both retained byte-identical binary-differ entry points."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = (
    ROOT / '68hc11_disassembler_tool_for_vy_v6' / 'binary_differ.py',
    ROOT / '68hc11_disassembler_tool_for_vy_v6' / 'core' / 'binary_differ.py',
)


class BinaryDiffSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = [path.read_bytes() for path in SCRIPTS]
        if cls.sources[0] != cls.sources[1]:
            raise AssertionError('Both legacy binary_differ copies must stay byte-identical')
        cls.modules = []
        for i, path in enumerate(SCRIPTS):
            spec = importlib.util.spec_from_file_location(f'binary_differ_test_{i}', path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            cls.modules.append(module)

    def compare(self, module, left, right):
        with tempfile.TemporaryDirectory() as td:
            first, second = Path(td)/'a.bin', Path(td)/'b.bin'
            first.write_bytes(left)
            second.write_bytes(right)
            return module.BinaryDiffer(str(first), str(second)).compare(verbose=False)

    def test_identical_including_two_empty_files(self):
        for module in self.modules:
            for payload in (b'', b'abc', b'\x00\xff'*80):
                result = self.compare(module, payload, payload)
                self.assertTrue(result['identical'])
                self.assertEqual(result['total_diff_bytes'], 0)
                self.assertEqual(result['diff_regions'], [])
                self.assertEqual(result['percent_different'], 0)

    def test_only_trailing_bytes_are_not_equal(self):
        for module in self.modules:
            for x, y, kind in ((b'abc', b'abcZZ', 'only_in_file2'),
                               (b'abcZZ', b'abc', 'only_in_file1'),
                               (b'', b'\x01\x02', 'only_in_file2')):
                with self.subTest(module=module.__name__, kind=kind):
                    result = self.compare(module, x, y)
                    self.assertFalse(result['identical'])
                    self.assertEqual(result['total_diff_bytes'], abs(len(x)-len(y)))
                    self.assertEqual(result['trailing_diff_bytes'], abs(len(x)-len(y)))
                    self.assertEqual(result['diff_regions'][-1]['kind'], kind)
                    self.assertAlmostEqual(result['percent_different'],
                                           100 * abs(len(x)-len(y)) / max(len(x),len(y)))

    def test_changed_common_and_unmatched_tail_counted_once(self):
        for module in self.modules:
            r = self.compare(module, b'abcde', b'aZcdeXX')
            self.assertEqual(r['common_changed_bytes'], 1)
            self.assertEqual(r['trailing_diff_bytes'], 2)
            self.assertEqual(r['total_diff_bytes'], 3)
            self.assertEqual([(x['start'],x['end']) for x in r['diff_regions']], [(1,1),(5,6)])

    def test_header_geometry_preserved_in_json(self):
        for module in self.modules:
            r = self.compare(module, b'abc', b'aXc')
            for key in ('file1','file2','size1','size2','total_diff_bytes','percent_different','diff_regions'):
                self.assertIn(key,r)
            self.assertEqual(r['sha256_file1'], hashlib.sha256(b'abc').hexdigest())

    def test_existing_report_and_both_inputs_preserved(self):
        for module in self.modules:
            with tempfile.TemporaryDirectory() as td:
                a,b,report=[Path(td)/x for x in ('old.bin','new.bin','report.json')]
                a.write_bytes(b'abc');b.write_bytes(b'abc\x00');report.write_text('PRESERVE')
                differ=module.BinaryDiffer(str(a),str(b))
                for dest in (a,b,report):
                    before=dest.read_bytes()
                    with self.assertRaises((ValueError, FileExistsError)):
                        differ.export_diff_map(str(dest))
                    self.assertEqual(dest.read_bytes(), before)
                self.assertEqual(a.read_bytes(),b'abc')

    def test_symlink_and_hardlink_alias_rejected(self):
        for module in self.modules:
            with tempfile.TemporaryDirectory() as td:
                a,b,linked=[Path(td)/x for x in ('a.bin','b.bin','linked.bin')]
                a.write_bytes(b'abc');b.write_bytes(b'abc')
                try:
                    linked.hardlink_to(a)
                except OSError:
                    self.skipTest('hardlink not supported in this local filesystem')
                with self.assertRaises(ValueError):
                    module.BinaryDiffer(str(a),str(b)).export_diff_map(str(linked))
                self.assertEqual(a.read_bytes(), b'abc')

    def test_json_written_once_and_rejected_second_time(self):
        for module in self.modules:
            with tempfile.TemporaryDirectory() as td:
                a,b,out=[Path(td)/x for x in ('a.bin','b.bin','report.json')]
                a.write_bytes(b'abc');b.write_bytes(b'abcZZ')
                diff=module.BinaryDiffer(str(a),str(b))
                diff.export_diff_map(str(out))
                content=out.read_bytes()
                self.assertEqual(json.loads(content)['trailing_diff_bytes'], 2)
                with self.assertRaises(FileExistsError):diff.export_diff_map(str(out))
                self.assertEqual(out.read_bytes(),content)

    def test_invalid_context_and_table_minimum_rejected(self):
        for module in self.modules:
            with tempfile.TemporaryDirectory() as td:
                a,b=[Path(td)/x for x in ('a.bin','b.bin')]
                a.write_bytes(b'a');b.write_bytes(b'b')
                differ=module.BinaryDiffer(str(a),str(b))
                for v in (-1, 4097,True):
                    with self.assertRaises(ValueError):differ.compare(context_bytes=v,verbose=False)
                for v in (0,-1,True):
                    with self.assertRaises(ValueError):differ.find_tables(min_size=v)

    def test_unmatched_tail_never_claimed_a_table(self):
        for module in self.modules:
            with tempfile.TemporaryDirectory() as td:
                a,b=[Path(td)/x for x in ('a.bin','b.bin')]
                a.write_bytes(b'hello');b.write_bytes(b'hello'+b'x'*500)
                self.assertEqual(module.BinaryDiffer(str(a),str(b)).find_tables(min_size=16),[])

    def test_cli_compares_readonly_and_json(self):
        with tempfile.TemporaryDirectory() as td:
            a,b,report=[Path(td)/x for x in ('a.bin','b.bin','report.json')]
            a.write_bytes(b'abc');b.write_bytes(b'abczz')
            result = subprocess.run([sys.executable,str(SCRIPTS[0]),str(a),str(b),'--output',str(report)],
                                    capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(json.loads(report.read_text())['total_diff_bytes'],2)
            self.assertEqual(a.read_bytes(),b'abc')


if __name__ == '__main__':unittest.main()
