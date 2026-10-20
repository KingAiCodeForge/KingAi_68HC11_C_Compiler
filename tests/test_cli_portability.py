"""Offline CLI regression checks; synthetic data only, no device connection."""
from pathlib import Path
import os
import subprocess
import sys

import pytest

from hc11_compiler import compile_source
from hc11_compiler.cli import validate_outputs, write_output
from hc11_compiler.codegen import CodeGenError
from hc11kit import _s19_to_bytes

ROOT = Path(__file__).resolve().parents[1]


def run_cli(script, *args, cwd=None):
    return subprocess.run([sys.executable, str(ROOT / script), *map(str, args)],
                          cwd=cwd, capture_output=True, timeout=20)


def test_explicit_bin_format_and_space_paths(tmp_path):
    work = tmp_path / "directory with spaces"
    work.mkdir()
    source = work / "test source.c"
    source.write_text("void f() {}", encoding="utf-8")
    output = work / "result.dat"
    result = run_cli("hc11cc.py", source, "--format", "bin", "-o", output, cwd=work)
    assert result.returncode == 0, result.stderr
    assert output.read_bytes() == compile_source(source.read_text(), output="binary")


@pytest.mark.parametrize("script,command", [("hc11cc.py", ()), ("hc11kit.py", ("compile",)), ("hc11kcos.py", ("compile",))])
def test_source_alias_never_overwritten(tmp_path, script, command):
    source = tmp_path / "input.c"
    original = "void f() {}"
    source.write_text(original)
    result = run_cli(script, *command, source, "-o", source, "--force")
    assert result.returncode != 0
    assert b"aliases" in result.stderr
    assert source.read_text() == original


def test_output_requires_force_and_missing_parent_diagnostic(tmp_path):
    source = tmp_path / "input.c"
    source.write_text("void f() {}")
    output = tmp_path / "result.asm"
    output.write_text("keep")
    result = run_cli("hc11cc.py", source, "-o", output)
    assert result.returncode != 0 and output.read_text() == "keep"
    result = run_cli("hc11cc.py", source, "-o", tmp_path / "absent" / "out.asm")
    assert result.returncode != 0 and b"parent directory" in result.stderr


def test_cli_imports_have_no_stdout_or_sys_path_mutation():
    code = "import sys; before=list(sys.path); import hc11cc,hc11kit,hc11kcos; assert sys.path == before"
    result = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, timeout=20)
    assert result.returncode == 0, result.stderr
    assert result.stdout == b""


def test_hardlink_alias_protected(tmp_path):
    source = tmp_path / "source"
    source.write_bytes(b"original")
    alias = tmp_path / "alias"
    try:
        os.link(source, alias)
    except OSError:
        pytest.skip("Filesystem does not support hard links")
    with pytest.raises(ValueError, match="aliases"):
        validate_outputs([source], [alias], force=True)


@pytest.mark.parametrize("kwargs", [{"org": -1}, {"stack": 65536}, {"org": True}, {"target": "not-a-target"}])
def test_compile_address_and_target_fail_closed(kwargs):
    with pytest.raises(CodeGenError):
        compile_source("void f() {}", **kwargs)


def test_unknown_output_format_rejected():
    with pytest.raises(ValueError, match="output format"):
        compile_source("void f() {}", output="typo")


def test_bad_numeric_cli_input_has_no_traceback(tmp_path):
    source = tmp_path / "input.c"
    source.write_text("void f() {}")
    result = run_cli("hc11cc.py", source, "--org", "bogus")
    assert result.returncode != 0 and b"Traceback" not in result.stderr


@pytest.mark.parametrize("offset,hook", [("-1", None), ("0x10", "0x100:3"), ("0x10", "0x10:3"), ("0x10", "-1:3")])
def test_patch_bounds_reject_without_output(tmp_path, offset, hook):
    base = tmp_path / "base.bin"
    base.write_bytes(bytes([255]) * 64)
    code = tmp_path / "code.bin"
    code.write_bytes(bytes([0x39]))
    output = tmp_path / "output.bin"
    args = [base, code, "--at", offset, "-o", output, "--target", "generic", "--no-checksum"]
    if hook:
        args.extend(["--hook", hook])
    result = run_cli("hc11kit.py", "patch", *args)
    assert result.returncode != 0
    assert not output.exists() and base.read_bytes() == bytes([255]) * 64


def test_checksum_fix_preserves_source_by_default(tmp_path):
    source = tmp_path / "base.bin"
    original = bytes(range(32))
    source.write_bytes(original)
    result = run_cli("hc11kit.py", "checksum", source, "--fix")
    assert result.returncode == 0, result.stderr
    assert source.read_bytes() == original
    assert source.with_name("base_checksum.bin").is_file()


def test_s19_validates_checksum_and_address(tmp_path):
    source = tmp_path / "image.s19"
    source.write_text("S10480003942\n")
    assert _s19_to_bytes(source, expected_origin=0x8000) == b"9"
    with pytest.raises(ValueError, match="address"):
        _s19_to_bytes(source, expected_origin=0x9000)
    source.write_text("S10480003900\n")
    with pytest.raises(ValueError, match="checksum"):
        _s19_to_bytes(source)


def test_banked_address_conversion_requires_bank_and_flat32_converts():
    result = run_cli("hc11kit.py", "addr", "0x8000", "--from", "cpu")
    assert result.returncode != 0 and b"explicit" not in result.stdout
    assert b"require --bank" in result.stderr
    result = run_cli("hc11kit.py", "addr", "0x20", "--format", "flat_32k")
    assert result.returncode == 0 and b"0x8020" in result.stdout


def test_flat32_disassembly_maps_cpu_to_file(tmp_path):
    source = tmp_path / "image.bin"
    source.write_bytes(bytes([0x39]) + bytes(31))
    result = run_cli("hc11kit.py", "disasm", source, "--format", "flat_32k", "--range", "0x8000-0x8001")
    assert result.returncode == 0, result.stderr
    assert b"8000" in result.stdout and b"RTS" in result.stdout


def test_invalid_hook_byte_text_is_not_silently_filtered():
    from hc11kit import _parse_expected_bytes
    with pytest.raises(ValueError):
        _parse_expected_bytes("zzFD017B")


def test_kcos_conflicting_outputs_leave_sources_unchanged(tmp_path):
    source = tmp_path / "module.c"
    source.write_text("void f() {}")
    output = tmp_path / "result.bin"
    result = run_cli("hc11kcos.py", "build", source, "-o", output, "--map-out", output)
    assert result.returncode != 0 and not output.exists()


def test_output_created_during_compilation_is_not_overwritten(tmp_path, monkeypatch):
    import hc11cc
    source = tmp_path / "source.c"
    source.write_text("void f() {}")
    output = tmp_path / "out.asm"
    def racing_compile(*args, **kwargs):
        output.write_text("other process output")
        return "assembly"
    monkeypatch.setattr(hc11cc, "compile_source", racing_compile)
    monkeypatch.setattr(sys, "argv", ["hc11cc", str(source), "-o", str(output)])
    with pytest.raises(SystemExit):
        hc11cc.main()
    assert output.read_text() == "other process output"


def test_exclusive_writer_cannot_clobber_racing_destination(tmp_path, monkeypatch):
    import builtins
    output = tmp_path / "out.asm"
    original_open = builtins.open
    def racing_open(path, mode="r", *args, **kwargs):
        if mode == "xb" and Path(path) == output:
            with original_open(output, "wb") as other:
                other.write(b"racing output")
        return original_open(path, mode, *args, **kwargs)
    monkeypatch.setattr(builtins, "open", racing_open)
    with pytest.raises(FileExistsError):
        write_output(output, "candidate")
    assert output.read_bytes() == b"racing output"


def test_force_flag_requires_real_boolean(tmp_path):
    output = tmp_path / "out"
    output.write_bytes(b"keep")
    with pytest.raises(TypeError, match="boolean"):
        write_output(output, b"candidate", force="false")
    assert output.read_bytes() == b"keep"


def test_force_output_replaces_file_without_touching_source(tmp_path):
    source = tmp_path / "source"
    source.write_bytes(b"original")
    output = tmp_path / "output"
    output.write_bytes(b"old")
    write_output(output, "candidate", inputs=[source], force=True)
    assert output.read_bytes() == b"candidate"
    assert source.read_bytes() == b"original"
