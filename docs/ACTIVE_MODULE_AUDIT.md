# Active module review - 20 October 2026

This is a bounded **alpha software** review. Each active module was inspected for
its interface, input/output path and relevant changed logic. Unchanged
lexer/parser/codegen/optimizer paths received no exhaustive semantic or
line-by-line correctness proof. Assembly/text tests do not establish complete C
semantics. Only the word-shift regression uses the small bounded byte executor;
it is not a whole-program emulator. Retained non-active tools have a separate
[per-file ledger](RESEARCH_SCRIPT_AUDIT.md) and are excluded from the wheel.

| Module/script | Purpose and actual API/CLI | Change/coverage | Remaining qualification |
| --- | --- | --- | --- |
| `hc11_compiler/__init__.py` | `compile_source`, assembler/object/resource exports, lazy `link_objects`/`link_sources` | Explicit source/output validation; alpha version; compile/API/link tests | No complete language conformance; direct APIs remain caller-controlled |
| `ast_nodes.py` | `CType` and AST dataclasses | Aggregate size/type interfaces inspected; PR #1 aggregate tests retained | General C type rules/layout compatibility unproven |
| `lexer.py` | `Preprocessor.process`, `Lexer.tokenize`, tokens, `LexerError` | Silent directive stripping and substitution inside strings fixed; unsupported directives error; bounded object macros preserve quoted literals; negative/literal tests | Includes/conditionals/function macros require external preprocessing; lexical edge cases not exhaustive |
| `parser.py` | `Parser(tokens, source).parse` | PR aggregates/static symbols retained; local comma-declaration idea adapted with independent array types; pointer groups rejected; parser/aggregate/negative tests | Flat frame rejects shadowing; incomplete C declarator/type grammar |
| `codegen.py` | `CodeGenerator.generate`, four `TARGET_PROFILES`, `CodeGenError` | Independent fail-closed branch retained; inherited header syntax repaired; strict 16-bit org/stack/target; unproven VY bank constants removed; word-left-shift D corruption repaired | Full codegen/ABI/optimizer semantics unproven; selected aggregates only; complex mutations/vector ownership unsupported |
| `optimizer.py` | `optimize(lines, max_passes=10)` | Pass boundary inspected; existing peephole/compile tests retained | No exhaustive flag/register/live-range equivalence proof |
| `assembler.py` | `Assembler.assemble/to_s19/get_listing`, `assemble`, `assemble_to_s19` | Preserved local public-project Y-bit prebytes and stable forward-reference sizes reconciled; address-wrap/overlapping output rejected; 27 independent byte/layout vectors plus bounds/smoke/link tests | Other opcode families/directives/expression grammar need more vectors |
| `objectfile.py` | `RelocatableObject` JSON load/save, `compile_object`, `compile_kcos_module`, `compile_asm_object` | PR ABI alternatives retained; malformed envelope/symbol/hash/resource types fail; negative/roundtrip tests | Assembly is assembler input; explicit save() can overwrite; not a hostile-input service |
| `resource_map.py` | `MemoryRegion`, `Allocation`, `ResourceMap.reserve/find_free/allocate/from_json` | PR #2 global preloaded collision/span checks retained across aliased pools; bool/float coercion rejected; alignment uses LCM to satisfy pool and request; metadata types strict; collision/clone/negative tests | Declared pools do not prove real ECU ownership; overlapping pools intentionally allowed while allocations cannot alias |
| `linker.py` | `link_objects`, `link_sources`, `LinkedImage` | Programmatically constructed/mutated objects use strict admission too; lossy resource int conversions removed; target/ABI/import/export/two-pass checks and both branch tests retained | No automatic OSID/bank/vector ownership, general relaxation or target proof |
| `cli.py` | `validate_outputs`, `validate_command_outputs`, `write_output`, `write_command_output` | Shared source/symlink/hardlink alias, duplicate/parent/strict overwrite and payload guards; exclusive no-clobber writes with descriptor-identity cleanup on I/O failure, explicit-force temporary replacement; race/write/close/filesystem negatives | No locking/transactional multi-output API; process/power loss or cleanup failure can leave a partial file; hardlink test skips where sandbox denies creation |
| `hc11cc.py` | C input, output/format, target/org/stack, tokens/AST, version | Explicit bin-format mismatch fixed; import-time stdout/path mutation removed; numeric/input diagnostics and shared output guards; space-path subprocess tests | Include-bearing examples now explicitly reject until externally preprocessed |
| `hc11kit.py` | `asm/disasm/compile/patch/free/checksum/addr/xdf/info` | Local guarded patcher adapted; shared output preflight; bounds/overlap, exact VY hash/hook, uniform fill, window limits, origin/S19 checks, full-image readback. Checksum writes copy; flat32 mapping repaired and banked CPU conversion explicit; synthetic tests | Hook whole-instruction boundaries/runtime bank/register state and GM16 applicability unproven; XDF remains partial; no hardware operations |
| `hc11kcos.py` | `compile/asm-object/link/build/map/inspect` | Import-safe commands; output/source/derived-object/map conflict guards; CLI/link negatives | Multi-output builds are not transactional; explicit resource contracts need target proof |

## Provenance and preservation

- Original public main: `f858bca4eac3ea281c096f48df241fa83491b386`.
- PR #1 `f63be13b7e5ccb9c734fe267d1565e56b6e62d36` is an ancestor of PR #2
  `3ceed9abf75772be9a5ea2546e94fda7ee723e8d`. Integration merges the latter,
  retaining both commits, resource/ABI alternatives and tests.
- Independent fail-closed line `22badaacf4952a97443025656a65bee507d78784` was merged
  separately. Its original header contained a mismatched `append(...]`; first
  exact integration test collection exposed it and this review repaired it.
- All original public refs are preserved in a verified complete Git bundle and
  manifest. Bundle SHA-256:
  `a3820d39451de3988fe1d261eb42651825ee51e2f67a3bb61677e8749989d6c6`.
- Two dirty **public-project** local clones were read only and preserved with
  byte-verified manifests/diffs/refs bundles before reconciliation. The second
  clone's 22 dirty/untracked/ignored source variants remain immutable in its
  snapshot. Selected sanitized assembler, guarded-patcher and word-shift
  changes/tests were adapted here. No private repository contents were inspected
  or promoted. Remaining local source/docs/scaffold alternatives stay in the
  snapshot, not silently overwritten or declared equivalent. Their original
  main-based compiler core cannot replace the aggregate/relocatable ABI wholesale.
- Assembler vectors cite NXP/Freescale M68HC11E Rev 2.1 Table 1, printed page 14.
  Word-shift tests retain local structural checks and run 768 synthetic
  value/count/profile cases in a bounded executor supporting only that sequence.

## Ignore and exposure review

The isolated checkout had default commented local excludes and no configured
global excludes. No applicable `.agents`, `.codex`, `AGENTS.md` or `SKILL.md` was
present. `tests/_*.py` filename exclusion was removed so reviewed audit/test source
can be public; no ignored source was promoted wholesale. Secret/private/customer
data, machine settings, firmware/binary and disposable build outputs remain
protected. Historical reference/media files remain in the original source tree,
not relicensed or copied into the wheel. Third-party redistribution rights remain
unqualified. No source file was deleted by this integration.

## Open work

Extend independent arithmetic/signedness/stack/call/branch/volatile/optimizer
execution vectors. Qualify complete target image/hash, engine/OS/calibration,
memory ownership, bank/hook contract and recovery separately. Finish or retire
each research variant using its ledger. A broad test count is not whole-tree
qualification or a recommended flash artifact.
