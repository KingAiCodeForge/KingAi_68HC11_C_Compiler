"""Integration tests for conservative VY ROM patch preflight behavior."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
HC11KIT = REPO_ROOT / "hc11kit.py"
ROM_SIZE = 0x20000
HOOK_OFFSET = 0x101E1
CODE_OFFSET = 0x5D05


def _fixture(tmp_path: Path, code_byte: int = 0x00) -> tuple[Path, Path, Path, str]:
    data = bytearray(ROM_SIZE)
    data[6:8] = b"\xFF\xFF"
    data[HOOK_OFFSET:HOOK_OFFSET + 3] = bytes.fromhex("FD017B")
    data[CODE_OFFSET] = code_byte

    rom_path = tmp_path / "base.bin"
    code_path = tmp_path / "patch.bin"
    output_path = tmp_path / "patched.bin"
    rom_path.write_bytes(data)
    code_path.write_bytes(b"\x39")  # RTS
    digest = hashlib.sha256(data).hexdigest()
    return rom_path, code_path, output_path, digest


def _command(
    rom_path: Path,
    code_path: Path,
    output_path: Path,
    digest: str,
) -> list[str]:
    return [
        sys.executable,
        str(HC11KIT),
        "patch",
        str(rom_path),
        str(code_path),
        "--at",
        "0x5D05",
        "--hook",
        "0x101E1:3",
        "--expect-sha256",
        digest,
        "--expect-hook-bytes",
        "FD017B",
        "-o",
        str(output_path),
    ]


def _run(command: list[str]) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        command,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        check=False,
    )


def _remove_option(command: list[str], option: str) -> None:
    index = command.index(option)
    del command[index:index + 2]


def test_vy_patch_requires_expected_sha256(tmp_path: Path):
    rom_path, code_path, output_path, digest = _fixture(tmp_path)
    command = _command(rom_path, code_path, output_path, digest)
    _remove_option(command, "--expect-sha256")

    result = _run(command)

    assert result.returncode != 0
    assert "--expect-sha256 is required" in result.stderr
    assert not output_path.exists()


def test_vy_patch_rejects_sha256_mismatch(tmp_path: Path):
    rom_path, code_path, output_path, digest = _fixture(tmp_path)
    command = _command(rom_path, code_path, output_path, digest)
    command[command.index(digest)] = "0" * 64

    result = _run(command)

    assert result.returncode != 0
    assert "Input SHA256 mismatch" in result.stderr
    assert not output_path.exists()


def test_vy_hook_requires_expected_original_bytes(tmp_path: Path):
    rom_path, code_path, output_path, digest = _fixture(tmp_path)
    command = _command(rom_path, code_path, output_path, digest)
    _remove_option(command, "--expect-hook-bytes")

    result = _run(command)

    assert result.returncode != 0
    assert "--expect-hook-bytes is required" in result.stderr
    assert not output_path.exists()


def test_vy_patch_rejects_hook_byte_mismatch(tmp_path: Path):
    rom_path, code_path, output_path, digest = _fixture(tmp_path)
    command = _command(rom_path, code_path, output_path, digest)
    command[command.index("FD017B")] = "FFFFFF"

    result = _run(command)

    assert result.returncode != 0
    assert "Hook bytes mismatch" in result.stderr
    assert not output_path.exists()


def test_vy_patch_rejects_banked_injection_by_default(tmp_path: Path):
    rom_path, code_path, output_path, digest = _fixture(tmp_path)
    command = _command(rom_path, code_path, output_path, digest)
    command[command.index("0x5D05")] = "0xC468"

    result = _run(command)

    assert result.returncode != 0
    assert "resolves to bank1" in result.stderr
    assert "--allow-banked-target" in result.stderr
    assert not output_path.exists()


def test_vy_patch_rejects_occupied_target_region(tmp_path: Path):
    rom_path, code_path, output_path, digest = _fixture(tmp_path, code_byte=0x12)
    command = _command(rom_path, code_path, output_path, digest)

    result = _run(command)

    assert result.returncode != 0
    assert "is not uniform 00/FF fill" in result.stderr
    assert not output_path.exists()


def test_vy_patch_preserves_existing_output_without_overwrite(tmp_path: Path):
    rom_path, code_path, output_path, digest = _fixture(tmp_path)
    output_path.write_bytes(b"keep")

    result = _run(_command(rom_path, code_path, output_path, digest))

    assert result.returncode != 0
    assert "Output already exists" in result.stderr
    assert output_path.read_bytes() == b"keep"


def test_vy_patch_succeeds_with_guards_and_leaves_checksum_unchanged(tmp_path: Path):
    rom_path, code_path, output_path, digest = _fixture(tmp_path)

    result = _run(_command(rom_path, code_path, output_path, digest))

    assert result.returncode == 0, result.stderr
    patched = output_path.read_bytes()
    assert patched[CODE_OFFSET:CODE_OFFSET + 1] == b"\x39"
    assert patched[HOOK_OFFSET:HOOK_OFFSET + 3] == bytes.fromhex("BD5D05")
    assert patched[6:8] == b"\xFF\xFF"
    assert "Checksum left unchanged" in result.stdout
    assert "Output SHA256:" in result.stdout
