"""Synthetic-only preservation tests; no ECU firmware or hardware required."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import sys
from unittest.mock import patch
import pytest

MODULE = Path(__file__).resolve().parents[1] / "core" / "safe_cli_output.py"
spec = importlib.util.spec_from_file_location("safe_cli_output", MODULE)
output = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = output
spec.loader.exec_module(output)


def test_atomic_new_and_no_clobber(tmp_path):
    dest = tmp_path / "folder" / "report.json"
    assert output.publish_output(dest, output.render_output({"value": 2}, "json")) == dest
    assert json.loads(dest.read_text()) == {"value": 2}
    with pytest.raises(FileExistsError):
        output.publish_output(dest, "ALTERNATE")
    assert json.loads(dest.read_text()) == {"value": 2}
    assert not list(dest.parent.glob("*.tmp"))


def test_force_only_replaces_report_not_source(tmp_path):
    source = tmp_path / "original.bin"
    source.write_bytes(b"ECU_ORIGINAL_BYTES")
    dest = tmp_path / "analysis.txt"
    dest.write_text("OLD")
    output.publish_output(dest, "NEW", overwrite=True, source=source)
    assert dest.read_text() == "NEW" and source.read_bytes() == b"ECU_ORIGINAL_BYTES"
    with pytest.raises(ValueError, match="aliases the input"):
        output.publish_output(source, "DANGEROUS", overwrite=True, source=source)
    assert source.read_bytes() == b"ECU_ORIGINAL_BYTES"


def test_symlink_to_source_rejected(tmp_path):
    src = tmp_path / "source.bin"
    src.write_bytes(b"LEAVE_ALONE")
    alias = tmp_path / "output.json"
    try:alias.symlink_to(src)
    except OSError:pytest.skip("Symlinks not permitted")
    with pytest.raises(ValueError):output.publish_output(alias, "garbage", overwrite=True, source=src)
    assert src.read_bytes() == b"LEAVE_ALONE"


def test_csv_formula_escape_and_nonfinite_json(tmp_path):
    rendered = output.render_output([{"name": "=HYPERLINK('bad')", "n": 9}, {"name": "plain", "n": 10}], "csv")
    assert "'=HYPERLINK" in rendered
    with pytest.raises(ValueError):output.render_output({"bad": float("nan")}, "json")
    assert not list(tmp_path.iterdir())


def test_writer_failure_cleans_partial_temp(tmp_path):
    dest = tmp_path / "report.txt"
    with patch.object(output.os, "link", side_effect=PermissionError("hardlink denied")):
        if output.os.name != "nt":
            with pytest.raises(PermissionError):output.publish_output(dest, "NEW")
            assert not dest.exists() and not list(tmp_path.glob(".*.tmp"))


def test_racing_writer_is_never_overwritten(tmp_path):
    dest = tmp_path / "report.json"
    original = output.os.link
    def competitor(temp, target):
        Path(target).write_text("OTHER PROCESS")
        return original(temp, target)
    if output.os.name == "nt":pytest.skip("POSIX link race regression")
    with patch.object(output.os, "link", side_effect=competitor):
        with pytest.raises(FileExistsError):output.publish_output(dest, "MY PROCESS")
    assert dest.read_text() == "OTHER PROCESS"
    assert not list(tmp_path.glob(".*.tmp"))


def test_unsupported_csv_type_and_mismatched_row_rejected():
    with pytest.raises(ValueError):output.render_output([1, 2], "csv")
    with pytest.raises(ValueError):output.render_output([{"a": 1}, {"unknown": 2}], "csv")
    with pytest.raises(ValueError):output.render_output("hi", "pdf")
