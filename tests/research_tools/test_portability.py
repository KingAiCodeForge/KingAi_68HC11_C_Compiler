"""Offline regression checks; no serial, TCP, firmware or hardware operations."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / '68hc11_disassembler_tool_for_vy_v6/core/output_manager.py'
LABELS = ROOT / 'vy_$060a_enhanced_1.0_bin_xdf_example'
VERIFY_BINARY = ROOT / '68hc11_disassembler_tool_for_vy_v6/_verify_binary.py'


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize('filename', ['../outside.txt', '/outside.txt', '..\\outside.txt',
                                    'C:outside.txt', 'C:\\outside.txt', 'stream:ads', ''])
def test_output_rejects_non_leaf_filename(tmp_path, filename):
    manager = load(OUTPUT).OutputManager(tmp_path / 'directory with spaces')
    with pytest.raises(ValueError):
        manager.write_text('data', filename)


@pytest.mark.parametrize('subdir', ['../outside', '/outside', 'C:\\outside', '..\\outside'])
def test_output_stays_inside_base(tmp_path, subdir):
    manager = load(OUTPUT).OutputManager(tmp_path / 'reports')
    with pytest.raises(ValueError):
        manager.write_text('data', 'report.txt', subdir)
    assert not (tmp_path / 'outside').exists()


def test_output_overwrite_requires_explicit_choice(tmp_path):
    output = load(OUTPUT)
    manager = output.OutputManager(tmp_path / 'with spaces', timestamp=False)
    path = manager.write_text('original', 'report.txt', 'nested/folder')
    with pytest.raises(FileExistsError):
        manager.write_text('replacement', 'report.txt', 'nested/folder')
    assert path.read_text() == 'original'
    assert manager.files_written == 1
    output.OutputManager(manager.base_dir, overwrite=True).write_text('replacement', 'report.txt', 'nested/folder')
    assert path.read_text() == 'replacement'


def test_json_output_is_deterministic(tmp_path):
    manager = load(OUTPUT).OutputManager(tmp_path, timestamp=False)
    first = manager.write_json({'z': 1, 'a': 2}, 'first.json')
    second = manager.write_json({'a': 2, 'z': 1}, 'second.json')
    assert first.read_bytes() == second.read_bytes()


@pytest.mark.parametrize('path', [VERIFY_BINARY, LABELS / '_verify_labels.py', LABELS / '_check_dupes.py'])
def test_research_audits_import_without_io(path, tmp_path):
    # These previously opened implicit files at import. Import in an empty cwd
    # with bytecode disabled, where none of their historical inputs exist.
    result = subprocess.run([sys.executable, '-B', '-c',
        'import importlib.util,sys; s=importlib.util.spec_from_file_location("audit",sys.argv[1]); '
        'm=importlib.util.module_from_spec(s); s.loader.exec_module(m)', str(path)],
        cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert result.stdout == ''
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize('path', [VERIFY_BINARY, LABELS / '_verify_labels.py', LABELS / '_check_dupes.py'])
def test_research_audit_usage(path, tmp_path):
    result = subprocess.run([sys.executable, str(path), '--help'], cwd=tmp_path,
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert 'usage:' in result.stdout


def test_binary_audit_rejects_wrong_size_and_hash(tmp_path):
    binary = tmp_path / 'synthetic image.bin'
    binary.write_bytes(b'\xff')
    audit = load(VERIFY_BINARY)
    with pytest.raises(SystemExit) as exc:
        audit.main([str(binary), '--expected-sha256', hashlib.sha256(binary.read_bytes()).hexdigest()])
    assert exc.value.code == 2
    binary.write_bytes(b'\xff' * (128 * 1024))
    with pytest.raises(SystemExit) as exc:
        audit.main([str(binary), '--expected-sha256', '0' * 64])
    assert exc.value.code == 2


def test_duplicate_audit_validates_schema_and_reads_explicit_path(tmp_path, capsys):
    source = tmp_path / 'definitions with spaces.json'
    source.write_text(json.dumps({'scalars': [{'address': '0x42'}, {'address': '0x42'}]}))
    audit = load(LABELS / '_check_dupes.py')
    assert audit.main([str(source)]) == 0
    assert 'Duplicate scalar addresses: 1' in capsys.readouterr().out
    source.write_text('{"scalars": [null]}')
    with pytest.raises(SystemExit) as exc:
        audit.main([str(source)])
    assert exc.value.code == 2


def test_scaffold_smoke_assertion_reaches_failure_gate(monkeypatch):
    scaffold = load(ROOT / 'hc11_virtual_emulator/tests/test_scaffold_imports.py')
    import src.cpu.regs as regs

    def fail_register_construction():
        raise AssertionError('synthetic register smoke failure')

    monkeypatch.setattr(regs, 'Registers', fail_register_construction)
    with pytest.raises(AssertionError, match='scaffold import/smoke checks failed'):
        scaffold.test_imports()


def test_label_audit_rejects_negative_addresses(tmp_path):
    source = tmp_path / 'input.json'
    source.write_text(json.dumps({'scalars': [{'address': '-1'}], 'tables': []}))
    audit = load(LABELS / '_verify_labels.py')
    with pytest.raises(ValueError, match='bank-1 hex address'):
        audit.verify(source, tmp_path / 'absent.bin', tmp_path / 'absent.asm', tmp_path / 'absent-original.asm')


@pytest.mark.parametrize('filename', ['virtual_128kb_eeprom.py', 'virtual_aldl_frame_sender_and_vecu.py'])
def test_virtual_libraries_do_not_write_logs_on_import(filename, tmp_path):
    tools = ROOT / 'hc11_virtual_emulator/tools'
    script = ('import pathlib,logging,sys; sys.dont_write_bytecode=True; '
              'sys.path.insert(0,sys.argv[1]); '
              'pathlib.Path.mkdir=lambda *a,**k: (_ for _ in ()).throw(AssertionError("mkdir at import")); '
              'logging.FileHandler=lambda *a,**k: (_ for _ in ()).throw(AssertionError("log at import")); '
              '__import__(sys.argv[2])')
    result = subprocess.run([sys.executable, '-B', '-c', script, str(tools), filename[:-3]],
                            cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert list(tmp_path.iterdir()) == []
