# KingAI 68HC11 C Compiler

Experimental offline subset-C compiler, assembler and relocatable linker for
Motorola 68HC11 research. **0.4.0a1 is an alpha prerelease, with no hardware
qualification.** Software tests, assembly bytes, an image hash and Git mergeability
do not establish safe ECU execution.

The `generic`, `vy_v6`, `1227730` and `16197427` profiles select compiler memory
models. They do not identify an engine, OS, calibration or compatible donor image.
L36/L67, VS/VT/VX/VY and different enhanced revisions require separate contracts.
The VY split spark-table question is separate reverse-engineering work; selecting
a profile does not change its ownership or combine those tables.

## Install and offline use

Python 3.10 or newer is required. The installed compiler has no runtime dependency
outside Python's standard library. Use an isolated environment:

```sh
python -m venv .venv
# Activate .venv using your platform's standard activation command.
python -m pip install .
hc11cc --version
hc11cc examples/blink.c -o blink.asm --target generic
hc11cc examples/blink.c --format bin -o blink.bin --target generic
hc11kit asm example.asm -o example.s19
hc11kcos compile module.c -o module.k11o --target generic
hc11kcos build first.c second.c -o linked.bin --map-out resources.json
```

`python hc11cc.py`, `python hc11kit.py` and `python hc11kcos.py` remain usable from
a source checkout. The wheel installs the active package and these three entry
points; it excludes firmware, historical disassemblies and hardware scaffolds.
Source examples are illustrative and are not approved patches.

All writing CLIs reject output aliases of their source inputs, including existing
hard links and resolved symlinks. Default writes exclusively create new files;
`--force` replacements use a temporary file and atomic rename. Existing outputs require `--force`; the preserved
patch CLI alias `--overwrite` has the same meaning. Parent directories must exist.
`hc11kit checksum --fix` writes a separate `*_checksum` image by default. Preflight
is intended for a single local command; it is not a concurrent filesystem locking
or transactional multi-output API. The Python object `save()` API is an explicit
writer and can replace a requested file.

## Active tools and boundaries

| Tool | Actual interface |
| --- | --- |
| `hc11cc` | Input C file; assembly/stdout or `--format asm/bin/s19/listing`; `--target`, `--org`, `--stack`, tokens/AST debug modes |
| `hc11kit` | `asm`, `disasm`, `compile`, `patch`, `free`, `checksum`, `addr`, `xdf`, `info`; inspect each subcommand's `--help` |
| `hc11kcos` | `compile`, `asm-object`, `link`, `build`, `map`, `inspect`; inspect each subcommand's `--help` |
| Python package | `compile_source`, `compile_object`, `compile_asm_object`, `link_objects`, `link_sources`, `ResourceMap`, `Assembler` |

The implemented subset includes byte/word arithmetic, pointers, conditionals and
loops, selected arrays/structs, inline assembly, static translation-unit symbols,
and collision-checked relocatable objects. Unsupported code generation raises an
error. There is no libc, floating point, complete C preprocessor or general C
conformance. Includes, conditionals, function macros and pragmas must be
preprocessed externally; they are rejected rather than silently discarded.
The frame ABI is flat: local shadowing and oversized frames are
rejected; aggregate local initializers and relocatable vector ownership remain
unsupported. Comma-separated scalar declarations are supported; pointer groups
must be written as separate declarations. Resource maps prove only the declared
allocation constraints, not that an ECU's chosen bytes are unused.

## Offline image patching is unqualified research

`hc11kit patch` only manipulates files; it does not communicate with an ECU.
For `--target vy_v6`, it requires a 128 KiB image and `--expect-sha256`, plus
`--expect-hook-bytes` when installing a hook. Choose your own independently
identified image, reviewed hook and reserved range. No stock hash or recommended
hook is supplied by this release.

```sh
hc11kit patch input.bin candidate.bin --at <reviewed-file-offset> \
  --hook <reviewed-hook-offset>:<whole-instruction-size> \
  --expect-sha256 <exact-input-sha256> --expect-hook-bytes <original-bytes> \
  -o candidate-research.bin --verify
```

Default injection requires uniform 00/FF fill in the common window. Fill alone
does not prove free space or hook correctness. `--allow-banked-target` and
`--allow-nonfree` are explicit unqualified research overrides. Injection cannot
cross a memory-window boundary. Assembly/S19 origins must match the requested CPU
placement, and S19 checksums and contiguous addresses are checked.

The generic GM16 arithmetic is **not validated for VY $060A**. VY patch output
leaves checksum bytes unchanged unless `--force-generic-checksum` is requested.
`--verify` adds a disassembly view; written code/hook bytes are read back in all
cases. Neither operation proves runtime flow, complete instruction replacement,
bank state, stack/register preservation, timing or physical behavior. Size-based
`info` hints are not ECU identification. Banked CPU address/range conversion needs
an explicit bank. Bench, recovery and hardware qualification remain outstanding.

## Review and validation records

- [Active module audit](docs/ACTIVE_MODULE_AUDIT.md): interfaces, changes, coverage
  and unresolved limits for each active module/CLI.
- [Research script audit](docs/RESEARCH_SCRIPT_AUDIT.md): individual inventory of
  retained non-active variants and selected offline fixes. Many legacy scripts
  retain hard-coded paths and unsafe assumptions; they are not qualified tools.
- [Relocatable linker design](docs/KCOS_RELOCATABLE_LINKER.md): K11O ABI, resource
  maps, collision semantics and examples.
- [Release qualification](docs/RELEASE_QUALIFICATION.md): exact validation receipt,
  preserved refs and artifact boundaries.

The original public branches and local source variants are preserved outside the
integration checkout in verified bundles and SHA-256 manifests. Both remote fix
lines were reconciled: preloaded resource-map admission and independent fail-closed
codegen. Selected public local assembler/word-shift/guarded-patcher regressions
were adapted and rerun. Original dirty clones were not edited.

Research directories, including emulator/bench/Arduino/ESP32/Raspberry Pi tools,
remain identifiable in their existing paths. They are excluded from the wheel and
are not flash artifacts or proof of physical execution. Historical claims inside
those files do not override the audit's unqualified status. No hardware paths are
executed by the release checks.

## Tests and contribution

```sh
python -m pip install ".[test]"
python -m pytest tests -q
python -m pytest hc11_virtual_emulator/tests/test_emulator_core.py \
  hc11_virtual_emulator/tests/test_scaffold_imports.py \
  hc11_bench_incar_emulator/template_addresses_might_be_wrong/tests/test_aldl_frame.py -q
```

The workflow checks Windows/Linux and Python 3.10/3.12/3.13; consult the exact
commit's Actions results before claiming those combinations passed. Local
validation platforms and limitations are recorded in the receipt. Test counts
describe selected software checks, not production readiness.

Keep secrets, private research/customer firmware, machine configuration and
disposable outputs ignored. Audit/test source is eligible for public inclusion
only after individual sanitization. This release adds no private repository data.
MIT applies to the project's eligible original source; existing third-party
notices remain in force and firmware/reference redistribution rights are not
established by this license. See [LICENSE](LICENSE) and [CONTRIBUTING.md](CONTRIBUTING.md).
