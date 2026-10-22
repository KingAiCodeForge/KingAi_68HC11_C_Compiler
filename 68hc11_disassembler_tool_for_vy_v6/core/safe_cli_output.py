"""Fail-closed, atomic report publication for legacy HC11 research tools.

This module writes reports only. It never opens or edits an ECU BIN. A caller
must opt in to replacement; no-clobber mode uses an atomic exclusive publish.
"""
from __future__ import annotations

import csv
import io
import json
import os
from pathlib import Path
import tempfile
from typing import Any


def _formula_safe(value: Any) -> Any:
    if isinstance(value, str) and value.startswith(("=", "+", "-", "@", "\t", "\r", "\n")):
        return "'" + value
    return value


def render_output(data: Any, output_format: str) -> str:
    """Render completely before a filesystem mutation (never partial JSON/CSV)."""
    if output_format == "json":
        return json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False)
    if output_format == "csv":
        if isinstance(data, dict):
            rows = [data]
        elif isinstance(data, list):
            rows = data
        else:
            raise ValueError("CSV output requires a mapping or list of mappings")
        if not rows:
            return ""
        if any(not isinstance(row, dict) for row in rows):
            raise ValueError("CSV rows must all be mappings")
        fields = list(rows[0].keys())
        if any(not isinstance(k, str) for k in fields):
            raise ValueError("CSV field names must be text")
        buffer = io.StringIO(newline="")
        writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows([{key: _formula_safe(value) for key, value in row.items()}
                          for row in rows])
        return buffer.getvalue()
    if output_format in ("txt", "md"):
        return str(data)
    raise ValueError("Unsupported output format")


def publish_output(destination: str | Path, rendered_text: str, *, overwrite: bool = False,
                   source: str | Path | None = None) -> Path:
    """Atomically create a report, refusing aliases or existing files by default.

    An existing destination may be replaced only when overwrite=True, and
    never when its resolved path equals the declared source input. Temporary
    files are in the destination's own directory, so hardlink/rename is local.
    """
    if not isinstance(rendered_text, str):
        raise TypeError("Rendered report must be text")
    target = Path(destination)
    if source is not None and Path(source).resolve(strict=False) == target.resolve(strict=False):
        raise ValueError("Refusing report output that aliases the input")
    if target.is_symlink():
        raise ValueError("Refusing symlink output")
    if target.exists() and not overwrite:
        raise FileExistsError(f"Report already exists: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, staged_name = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".tmp", dir=target.parent)
    staged = Path(staged_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as stream:
            stream.write(rendered_text)
            stream.flush()
            os.fsync(stream.fileno())
        if overwrite:
            os.replace(staged, target)
        elif os.name == "nt":
            # Windows rename refuses a destination created since preflight.
            os.rename(staged, target)
        else:
            # Same-directory hardlink is atomic and refuses a destination race.
            os.link(staged, target)
        return target
    finally:
        staged.unlink(missing_ok=True)
