# 68HC11 legacy tooling: CLI preservation and XDF BASEOFFSET bounds

**22 October 2026.** Review-only software changes, no ECU firmware, read/write hardware, or flash operation. The main compiler ABI and assembler were not modified.

## Why this matters

- The legacy `core/cli_base.py` previously used `logging.disable(logging.CRITICAL)` for `--no-log` and returned before assigning `self.logger`; subsequent `execute()` logger calls could fail. It also changed the process-wide logging state for unrelated libraries.
- `--dry-run --output-dir` created the target directory during path planning, and a `--log-file` could be created even on a dry-run.
- The ordinary report writer opened destination files with `w` after an `exists()` check. A second process could create the same report between the check and open, and the tool would overwrite it. An explicitly forced output could alias the supplied input.
- The legacy `core/address_conversion.py::AddressConverter.xdf_to_file()` returned the *raw XDF address* when subtractive BASEOFFSET mapping produced a negative offset. This is a misleading fallthrough that could select a different byte of a firmware image. It also could not explicitly override a format's nonzero base to zero because zero was used as an implicit 'not provided' sentinel.

## Changes

1. **New standalone `core/safe_cli_output.py`**: render JSON/CSV/text before mutation; refuse NaN JSON, unsafe CSV formulas, input aliases and output symlinks; write a staged same-directory file; atomically publish by exclusive link/rename, or replace only with explicit `--force`. Existing-report overwrites are refused by default. Cleanup removes *only the tool's temporary file*.
2. **`core/cli_base.py` integration**: local null logger for `--no-log` without disabling process-wide logs; do not create log directories/files during `--dry-run`; keep `get_output_path()` pure; use the new writer; report fatal errors to stderr even with logging disabled.
3. **`core/address_conversion.py`**: fail-closed for negative/out-of-image file offsets, malformed numeric arguments and invalid subtract flags; `Optional[int]=None` means use format defaults, while an explicit zero correctly overrides. This changes only XDF→file-address admission, not banked CPU mapping, disassembly or runtime hardware addressing.

## Verification

Isolated Python 3.13.5 focused tests executed locally with **21 passed**:
- 7 synthetic report-writer tests covering alias/refusal, race, exclusive publication, output cleanup and formula-safe CSV.
- 14 synthetic BASEOFFSET tests covering VY, VT/V8 and BMW address arithmetic, explicit-zero overrides, invalid flags/types/negative/out-of-bounds results.

The exact new helper and both test-source Git blobs matched the locally executed files. The offset arithmetic was exercised in an **isolated method copy** matching the new implementation; running the exact full GitHub `address_conversion.py` and `cli_base.py` with all legacy consumers remains a separate integration gate.

## Reproduction

From a fresh source checkout, without GitHub Actions:

```sh
python -m pytest -q 68hc11_disassembler_tool_for_vy_v6/tests/test_safe_cli_output_v1.py 68hc11_disassembler_tool_for_vy_v6/tests/test_xdf_baseoffset_bounds_v1.py
python -m pytest -q tests/
```

Run a manual native Windows `--dry-run --no-log --log-file ... --output-dir ...` with a throwaway path to prove no destination changes, then verify that ordinary existing reports are preserved and `--force` never permits source aliases. Confirm any other callers that relied on unsafe raw XDF fallback; do not silently adapt negative addresses.

**Review status:** `SYNTHETIC_CHECKS_PASS / FULL_LEGACY_INTEGRATION_HOLD`. Keep existing PR #5 (binary differ) untouched. No GitHub Actions, no source firmware, no merge to main.

**Idea provenance:** The concrete CLI and BASEOFFSET fixes originate in an assistant-led audit of the GitHub-wide script inventory. This continuation is a **ChatGPTz idea 💡** informed by the earlier KingAI script-audit report, the user's request for broad reusable-script improvements, and preservation rules.
