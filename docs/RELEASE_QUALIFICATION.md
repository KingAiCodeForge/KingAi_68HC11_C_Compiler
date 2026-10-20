# 0.4.0a1 alpha qualification

This version integrates relocatable/aggregate compiler work, both independent
fix lines and selected preserved public-project local fixes. It is an
experimental **offline software** prerelease. No ECU, flash, serial/TCP device,
paid service or credential provisioning is involved. Hardware validation and
complete language/opcode conformance remain open.

The active and research audit ledgers identify inspected/changed/tested/static
only and unresolved paths individually. Research scaffolds are retained in the
Git tree, excluded from the installable wheel and not offered as flash assets.
Historical source/reference material has no newly established redistribution
rights. No private repository source or private calibration data was used.

## Reproducing the checks

Use an isolated Python environment with a writable temporary directory. On the
review host, Python 3.13.5/Windows and a path containing spaces were available;
Python 3.10/3.12 and Linux/macOS were unavailable locally. The GitHub workflow
declares Windows/Linux x Python 3.10/3.12/3.13. Read the exact commit's Actions
results before treating any CI platform as passed.

```sh
python -m pip install ".[test]" build
python -m compileall -q hc11_compiler hc11cc.py hc11kit.py hc11kcos.py
python -m pytest tests -q
python -m pytest hc11_virtual_emulator/tests/test_emulator_core.py \
  hc11_virtual_emulator/tests/test_scaffold_imports.py \
  hc11_bench_incar_emulator/template_addresses_might_be_wrong/tests/test_aldl_frame.py -q
python -m build --wheel --outdir <asset-directory>
```

For an environment with unrelated installed pytest plugins, set
`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`. If the host's default temporary directory is
unwritable, set `TEMP`/`TMP` and pytest `--basetemp` to a writable workspace
directory. The initial clean-venv ensurepip failure on this host was resolved
by that temporary-directory correction. No installed package or credential was
changed outside the isolated environment.

Final local source, wheel install, directory-with-spaces checks and hashes are
recorded in the machine-readable release receipt accompanying any published
assets. That receipt, not a historical test count, binds exact Git commit,
source tree, artifact SHA-256, interpreter, commands, outcomes and limitations.
The wheel must contain only the active package, three CLI modules and packaging
metadata. No firmware or hardware tool is a release asset.

## Publication gates

Integration is non-force, with original remote branches retained. Original
public refs and dirty local public-project variants have verified immutable
backup bundles/file manifests outside the integration checkout. No source file
is deleted. PR #1 is an ancestor of #2 and both are merged alongside the separate
fail-closed branch; the receipt records exact ancestry checks. Redundant PRs must
not be closed unless their actual content coverage is recorded.

Only a tested exact commit may advance main or receive the prerelease tag. Tags,
default branch, release flags and downloaded asset hashes must be checked after
publication. A package smoke check or clean Git merge does not make this a
stable release. Remaining target/hardware and non-active research work is
described in the audit ledgers.
