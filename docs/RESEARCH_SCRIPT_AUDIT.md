# Research script audit — 20 October 2026

This inventory covers the public compiler repository only. Every listed Python source was parsed and its top-level API, argument declarations, imports and side effects inspected statically; selected shared functions received the offline regression checks below. It is **not** a line-by-line correctness proof of every decoder or a claim that every script was improved. No private/local source, ECU connection, serial/TCP session, kernel upload, flash or hardware operation was used. No firmware image was supplied or newly redistributed by these audit edits.

All these directories are **retained non-active research variants**, excluded from the installable compiler wheel. Historical labels such as “VERIFIED”, “Production Ready”, “safe”, and “complete” inside the preserved sources are historical author claims, not this release's qualification. For each future experiment bind vehicle/platform, engine (L36/L67), OS, calibration, image size and SHA-256 explicitly; do not transfer addresses between profiles or donor images. A matching user-supplied hash identifies bytes, not rights or hardware safety.

Original public refs and PR heads were preserved before changes in a verified Git bundle and ref manifest outside the source tree. Existing public copyright/provenance notices were retained. No ignored/private files were promoted. Third-party material is not relicensed by the compiler MIT license; rights review remains necessary before redistributing research/firmware assets.

## Changes and measured checks

- Shared `OutputManager` now bounds writes to its chosen base directory and refuses clobbering unless `overwrite=True`. JSON key ordering is stable. These protections apply to this API, not every legacy writer.
- The three audit scripts below use guarded explicit-input CLIs; binary reports require 128 KiB and expected SHA-256. This removes implicit local data reads at import.
- Virtual flash/ECU libraries no longer create directories or files at import. Explicit CLI execution configures logging after parsing. No virtual program/erase session was run.
- Stock/XDF/output defaults in `core/vy_v6_constants.py` no longer require a particular drive; environment overrides are `VY_STOCK_BINARY`, `VY_XDF_DIR`, and `VY_OUTPUT_DIR`. Other fixed legacy paths are identified below and remain unqualified.
- `install_dependancies_pip.bat` now anchors requirements/tests to its own directory, calls `python -m pip`, stops on installation/test failure and has no silent `--user` fallback. Its network installation path was statically reviewed; the installer itself was not executed.
- Scaffold smoke exceptions now fail the test instead of printing false success.

On Windows / Python 3.13.5: `python -m pytest tests/research_tools -q` ran **25 offline regressions** successfully with an explicit writable `--basetemp`; output paths contain spaces and Windows drive/separator/ADS cases are checked. `python -m pytest hc11_virtual_emulator/tests/test_emulator_core.py hc11_bench_incar_emulator/template_addresses_might_be_wrong/tests/test_aldl_frame.py -q` ran **77 pure in-memory/frame tests** successfully. The strengthened scaffold test ran **1 test** successfully. Initial sandbox temp-fixture failures reached no test body and were resolved with workspace `--basetemp`. Unrelated installed `pyreadline3` emits a teardown console-handle diagnostic despite exit zero; clean install verification is handled separately for the active core. No Linux/macOS/Arduino/ESP32 compiler was exercised in this audit.

## Individual Python sources

`CLI` records argparse declarations or a manual invocation where present; API names are actual source definitions. “No dedicated run” means no current behavioral qualification, not that a script is safe because it parsed. Test modules are listed for coverage provenance.

### `68hc11_disassembler_tool_for_vy_v6/_verify_binary.py`

- Purpose: Historical VY $060A diagnostic report; never an ECU/flash qualification.
- CLI: 'binary'; '--expected-sha256'.
- API: `report(data)`; `main(argv=None)`.
- Coverage: New tests/research_tools regression coverage (subset/API/help/import/negative inputs as applicable); no hardware.
- Findings/status: Fixed import-time implicit image read and drive path: explicit binary + required expected SHA-256; exact 128 KiB size check; usage/missing-input diagnostics. Historical address assumptions remain unqualified.

### `68hc11_disassembler_tool_for_vy_v6/binary_differ.py`

- Purpose: Binary Differ - Compare Two ECU Binary Files.
- CLI: 'file1'; 'file2'; '-o'/'--output'; '-c'/'--context'; '--find-tables'.
- API: `main()`; `BinaryDiffer(compare, export_diff_map, find_tables)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: No full behavioral qualification; bounds, output overwrite, dependency errors and exact-target correctness remain open.

### `68hc11_disassembler_tool_for_vy_v6/binary_table_extractor.py`

- Purpose: Binary Table Extractor - Extract Actual Table Data from ECU Binaries.
- CLI: '-b'/'--binary'; '-x'/'--xdf'; '--table'; '--category'; '--csv'; '--json'; '--output-dir'; '-b2'/'--binary2'; '-x2'/'--xdf2'; '--compare'; '-v'/'--verbose'.
- API: `main()`; `BinaryTableExtractor(parse_xdf, extract_table, extract_all_spark_tables, extract_all_fuel_tables, export_table_to_csv, export_table_to_json, compare_with_other_binary)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: No full behavioral qualification; bounds, output overwrite, dependency errors and exact-target correctness remain open.

### `68hc11_disassembler_tool_for_vy_v6/core/address_conversion.py`

- Purpose: VY V6 $060A Address Conversion Module.
- CLI: No command-line parser; Python API only.
- API: `detect_binary_format(bin_path: str)`; `parse_xdf_baseoffset(xdf_path: str)`; `create_vy_v6_converter()`; `xdf_addr_to_cpu_vy_v6(xdf_address: int)`; `cpu_to_file_vy_v6(cpu_address: int)`; `MemoryRegion()`; `BinaryFormat()`; `AddressConverter(xdf_to_cpu, cpu_to_file, xdf_to_file, classify_address, is_calibration, is_code, format_address)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Binary-size-based format detection is heuristic, not OS/calibration identity. Multiple architecture adapters need exact hash fixtures before reuse.

### `68hc11_disassembler_tool_for_vy_v6/core/analyze_bank_switching.py`

- Purpose: ANALYZE BANK SWITCHING - MC68HC11 Expanded Mode Memory Analysis.
- CLI: main() demo with fixed/default inputs; no argparse interface.
- API: `main()`; `HC11HardwareSpec()`; `VYV6MemoryMap()`; `BankSwitchingAnalyzer(analyze_vector_table, find_bank_select_patterns, analyze_calibration_access, find_memory_controller_writes, generate_report, run)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Bank pattern matches are hypotheses; no image hash gate or bench proof.

### `68hc11_disassembler_tool_for_vy_v6/core/analyze_interrupts_v2.py`

- Purpose: HC11 Interrupt Vector & ISR Analysis Tool v2.0.
- CLI: main() demo with fixed/default inputs; no argparse interface.
- API: `main()`; `InterruptAnalyzer(read_word, get_vector_target, analyze_all_vectors, analyze_pseudo_vectors, analyze_ignition_isrs)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Fallback constants and fixed image path risk silent target substitution. Fixed absolute path literal(s) remain at lines 238.

### `68hc11_disassembler_tool_for_vy_v6/core/binary_differ.py`

- Purpose: Binary Differ - Compare Two ECU Binary Files.
- CLI: 'file1'; 'file2'; '-o'/'--output'; '-c'/'--context'; '--find-tables'.
- API: `main()`; `BinaryDiffer(compare, export_diff_map, find_tables)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: No full behavioral qualification; bounds, output overwrite, dependency errors and exact-target correctness remain open.

### `68hc11_disassembler_tool_for_vy_v6/core/cli_base.py`

- Purpose: CLI Base Class - Standard command-line interface for all VY V6 tools.
- CLI: '--input'/'-i'; '--output'/'-o'; '--output-dir'; '--timestamp'; '--prefix'; '--format'; '--dry-run'; '--force'; '--verbose'/'-v'; '--quiet'/'-q'; '--log-file'; '--no-log'; '--version'.
- API: `main()`; `CLIBase(setup_common_arguments, setup_logging, get_output_path, write_output, run, execute)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: --no-log leaves logger unset while execute/run use it; logging is process-global; dry-run path construction can create directories. Unqualified.

### `68hc11_disassembler_tool_for_vy_v6/core/hc11_disassembler.py`

- Purpose: HC11 Disassembler for VY V6 Enhanced ECU Binary.
- CLI: main() demo with fixed/default inputs; no argparse interface.
- API: `main()`; `XDFCalibrationDB(load_xdf_data, lookup)`; `HC11Disassembler(get_ram_addr, get_file_offset, read_byte, read_word, decode_rpm_value, get_xdf_comment, annotate_table_data, disassemble_instruction, disassemble_range, find_calibration_reads, find_specific_address_references, disassemble_with_context, find_rpm_comparisons, find_bit_operations)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Separate opcode/core variant; fixed image candidates and adjacent-module import. No cross-decoder golden corpus. Fixed absolute path literal(s) remain at lines 548, 549.

### `68hc11_disassembler_tool_for_vy_v6/core/opcodes.py`

- Purpose: HC11 Unified Opcodes - Complete and corrected instruction set.
- CLI: main() demo with fixed/default inputs; no argparse interface.
- API: `main()`; `Instruction()`; `HC11InstructionSet(get_instruction, is_prebyte, get_all_opcodes, get_statistics)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: No full behavioral qualification; bounds, output overwrite, dependency errors and exact-target correctness remain open.

### `68hc11_disassembler_tool_for_vy_v6/core/output_manager.py`

- Purpose: Output Manager - Centralized output formatting and file management.
- CLI: main() demo with fixed/default inputs; no argparse interface.
- API: `main()`; `OutputManager(get_timestamp, build_filename, get_output_path, write_text, write_json, write_csv, write_markdown, write_binary, get_statistics, print_summary)`.
- Coverage: New tests/research_tools regression coverage (subset/API/help/import/negative inputs as applicable); no hardware.
- Findings/status: Fixed path escape/Windows drive and ADS-looking filename rejection, bounded resolved output, default exclusive creation, explicit overwrite opt-in, stable JSON key ordering. Timestamp and Markdown date are intentionally nondeterministic unless avoided.

### `68hc11_disassembler_tool_for_vy_v6/core/vy_v6_constants.py`

- Purpose: VY V6 $060A VERIFIED CONSTANTS MODULE.
- CLI: No argument parser; guarded demonstration prints constants. Python helper API shown below.
- API: `load_binary(path: Path=None)`; `get_vector_target(data: bytes, vector_addr: int)`; `rpm_to_byte(rpm: int)`; `byte_to_rpm(value: int)`; `HC11Hardware()`; `MemoryRegion()`; `TimingConstants()`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Replaced stock/XDF/output drive paths with package-relative defaults or VY_STOCK_BINARY/VY_XDF_DIR/VY_OUTPUT_DIR environment settings. Existing input auto-discovery and historical unbound address claims remain unqualified; callers should use explicit inputs. Historical VERIFIED labels are source claims, not new verification. Address constants are VY $060A only.

### `68hc11_disassembler_tool_for_vy_v6/core/xdf_verified_analysis.py`

- Purpose: XDF VERIFIED ANALYSIS - Uses ONLY XDF + Binary Cross-Reference.
- CLI: `main()` uses historical fixed/default paths; no argparse interface.
- API: `main()`; `ConfirmedConstants()`; `XDFEntry()`; `XDFVerifiedAnalyzer(load_xdf_definitions, verify_timing_constants, analyze_vector_table, verify_xdf_against_binary, find_ignition_related_code, generate_verified_report, run)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Fixed absolute path literal(s) remain at lines 37, 38, 39, 44.

### `68hc11_disassembler_tool_for_vy_v6/disassemble_banked.py`

- Purpose: VY V6 Banked ROM Disassembler.
- CLI: 'binary'; '--addr'/'-a'; '--file-offset'/'-f'; '--len'/'-l'; '--bank'/'-b'; '--isr'/'-i'; '--output'/'-o'; '--no-bytes'.
- API: `main()`; `VYV6BankedDisassembler(load, cpu_to_file, file_to_cpu, disassemble_region, disassemble_isr)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: No full behavioral qualification; bounds, output overwrite, dependency errors and exact-target correctness remain open.

### `68hc11_disassembler_tool_for_vy_v6/disassemble_hc11.py`

- Purpose: Minimal HC11 disassembler for analyzing code at specific addresses.
- CLI: No command-line parser; Python API only.
- API: `disassemble_at(data, start_addr, count=32)`; `find_spark_patterns(data, start, end)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Fixed absolute path literal(s) remain at lines 249.

### `68hc11_disassembler_tool_for_vy_v6/find_free_space.py`

- Purpose: Find Free Space in Binary Files.
- CLI: 'binary'; '--min-size'; '--free-byte'; '--export-linker'.
- API: `main()`; `FreeSpaceFinder(find_free_space, export_linker_script)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Repeated fill bytes do not prove unused execution/storage space; heuristic safety assessments are not a patch admission decision.

### `68hc11_disassembler_tool_for_vy_v6/find_free_space_then_compare_crossovers.py`

- Purpose: Free Space Analyzer with Bank Crossover Comparison + Multi-Layer Validation.
- CLI: '--dir'; '--bank1'; '--bank2'; '--bank3'; '--xdf'; '--min-size'; '--free-byte'; '--output'/'-o'; '--verbose'/'-v'.
- API: `get_instruction_length(data: bytes, offset: int)`; `detect_free_byte(data: bytes)`; `find_free_regions(data: bytes, free_byte: int, min_size: int, bank: str)`; `scan_jsr_jmp_references(data: bytes, bank: str)`; `build_reference_map(all_refs: List[JsrReference])`; `check_references_into_region(region: FreeRegion, ref_map: Dict[int, List[JsrReference]])`; `parse_xdf_file(xdf_path: Path)`; `check_xdf_overlap(region: FreeRegion, xdf_entries: List[XdfEntry])`; `validate_boundaries(region: FreeRegion, data: bytes)`; `cross_compare_banks(region: FreeRegion, bank_data: Dict[str, bytes])`; `classify_region(region: FreeRegion)`; `build_overlap_map(b2_data: bytes, b3_data: bytes, free_byte: int, min_size: int=1)`; `generate_report(bank_files: Dict[str, Path], bank_data: Dict[str, bytes], all_regions: List[FreeRegion], free_byte: int, min_size: int, overlap_segments: List[OverlapSegment], xdf_path: Optional[Path], xdf_count: int, all_refs: List[JsrReference])`; `main()`; `FreeRegion()`; `XdfEntry()`; `JsrReference()`; `OverlapSegment()`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Bank/XDF/reference analysis improves evidence but cannot prove every indirect reference; do not treat reported free regions as flash qualification.

### `68hc11_disassembler_tool_for_vy_v6/full_binary_disassembler.py`

- Purpose: Full HC11 Binary Disassembler with Multi-XDF Cross-Reference.
- CLI: main() demo with fixed/default inputs; no argparse interface.
- API: `main()`; `MultiXDFDatabase(load_all_xdfs, lookup, get_category)`; `HC11FullDisassembler(load_binary, disassemble_full, parse_operand, calc_branch_target)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Fixed absolute path literal(s) remain at lines 47, 48.

### `68hc11_disassembler_tool_for_vy_v6/godlike_disassemble_all.py`

- Purpose: KingAI Godlike HC11 Disassembler & XDF Labeler — All-In-One Orchestrator.
- CLI: '--target'/'-t'; '--backends'/'-b'; '--no-label'; '--no-diff'; '--dry-run'.
- API: `run_capstone(bin_path: Path, name: str, output_dir: Path, banks: list)`; `run_gnu(bin_path: Path, name: str, output_dir: Path, banks: list)`; `run_udis(bin_path: Path, name: str, output_dir: Path, banks: list)`; `run_xdf_labeler(asm_path: Path, xdf_json: Path, bank_num: int)`; `diff_banks_binary(stock_data: bytes, enh_data: bytes, bank_label: str, cpu_base: int, output_dir: Path, stock_name: str, enh_name: str)`; `find_bin(target_cfg: dict, bin_name: str)`; `process_target(target_name: str, backends: list, do_label: bool, do_diff: bool, dry_run: bool)`; `main()`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Optional capstone/GNU/udis backends and labeler subprocesses not installed/qualified here; default target selection is historical.

### `68hc11_disassembler_tool_for_vy_v6/hc11_complete_binary_mapper.py`

- Purpose: HC11 Complete Binary Knowledge Mapper.
- CLI: `python hc11_complete_binary_mapper.py <binary_file> [xdf_file...]`.
- API: `main()`; `KnowledgeItem()`; `HC11CompleteBinaryMapper(analyze_all, load_xdf_calibrations, load_known_ram_variables, load_interrupt_vectors, load_known_subroutines, load_timer_operations, infer_code_regions, infer_data_tables, infer_string_constants, infer_subroutine_parameters, find_unanalyzed_regions, find_unknown_subroutines, find_unknown_ram_usage, find_unknown_timer_configs, calculate_coverage, print_complete_report, export_knowledge_database)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: No full behavioral qualification; bounds, output overwrite, dependency errors and exact-target correctness remain open.

### `68hc11_disassembler_tool_for_vy_v6/hc11_disassembler.py`

- Purpose: hc11_disassembler.py — UNIVERSAL BACKUP.
- CLI: 'binary'; '--bank'; '--base-addr'; 'binary'; '--bank'; '--base-addr'; '--start'; '--length'; '--xdf'; '--show-vectors'; '--show-isrs'.
- API: `find_vy_binaries()`; `find_xdf_files()`; `load_xdf_labels(xdf_path)`; `main()`; `XDFCalibrationDB(load_xdf_data, lookup)`; `HC11Disassembler(offset_to_cpu_addr, get_ram_addr, get_file_offset, read_byte, read_word, decode_rpm_value, get_xdf_comment, annotate_table_data, disassemble_instruction, disassemble_range, find_calibration_reads, find_specific_address_references, disassemble_with_context, find_rpm_comparisons, find_bit_operations, find_byte_pattern, find_est_control_code, find_rev_limiter_patterns, detect_ecu_patterns, disassemble_enhanced)`; `HC11DisassemblerCLI(setup_tool_arguments, run)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Universal backup retained separately from core decoder; import reconfigures streams and optional CLIBase adapter can differ from main. Source reconfigures process streams; import is not guaranteed side-effect free.

### `68hc11_disassembler_tool_for_vy_v6/hc11_disassembler_060a_enhanced_v1.py`

- Purpose: Motorola 68HC11 Disassembler for GM/Delco $060A Enhanced OS v1.0a Binary.
- CLI: 'binary'; '--bank'; '--base-addr'; 'binary'; '--bank'; '--base-addr'; '--start'; '--length'; '--xdf'; '--show-vectors'; '--show-isrs'.
- API: `find_vy_binaries()`; `find_xdf_files()`; `load_xdf_labels(xdf_path)`; `main()`; `XDFCalibrationDB(load_xdf_data, lookup)`; `HC11Disassembler(offset_to_cpu_addr, get_ram_addr, get_file_offset, read_byte, read_word, decode_rpm_value, get_xdf_comment, annotate_table_data, disassemble_instruction, disassemble_range, find_calibration_reads, find_specific_address_references, disassemble_with_context, find_rpm_comparisons, find_bit_operations, find_byte_pattern, find_est_control_code, find_rev_limiter_patterns, detect_ecu_patterns, disassemble_enhanced)`; `HC11DisassemblerCLI(setup_tool_arguments, run)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Enhanced-specific retained variant with duplicate decoder and stream reconfiguration. No proof of exact-image identity from its filename. Fixed absolute path literal(s) remain at lines 235, 236, 237, 238, 239, 240, 241, 269, 270, 271, 272, 273, 274, 1683, 1684, 1685. Source reconfigures process streams; import is not guaranteed side-effect free.

### `68hc11_disassembler_tool_for_vy_v6/hc11_disassembler_batch.py`

- Purpose: HC11 Batch Disassembler - Multiple Address Ranges.
- CLI: 'binary'; '--addr'/'-a'; '--batch'/'-b'; '--output'/'-o'; '--format'/'-f'.
- API: `format_operand(addr_mode, operands, current_addr, instr_len, flags)`; `disassemble_instruction(data, offset, runtime_addr)`; `disassemble_range(data, file_offset, length, name='')`; `parse_address_arg(arg)`; `load_batch_file(path)`; `output_asm(results, file=None)`; `output_csv(results, file)`; `output_json(results, file)`; `main()`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Capstone batch path and bank identity need synthetic golden fixtures; not hardware-validated.

### `68hc11_disassembler_tool_for_vy_v6/hc11_disassembler_complete.py`

- Purpose: HC11 Complete Disassembler - Fixed with ALL Opcodes.
- CLI: `python hc11_disassembler_complete.py <binary> [base_addr_hex] [start_offset_hex] [length_hex]`.
- API: `disassemble_instruction(data, offset, runtime_addr)`; `disassemble_binary(data, base_addr=32768, start_offset=0, length=None)`; `main()`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Import replaces stdout/stderr wrappers. Positional numeric fields use hex conversion and bounds need dedicated negative tests.

### `68hc11_disassembler_tool_for_vy_v6/hc11_disassembler_enhanced.py`

- Purpose: HC11 Disassembler - Enhanced Production Version.
- CLI: `python hc11_disassembler_enhanced.py <binary_file> [base_addr] [start_offset] [length] [xdf_file]`; omitted image triggers auto-discovery.
- API: `find_vy_binaries()`; `find_xdf_files()`; `disassemble_instruction(data, offset, base_addr=32768, xdf_labels=None)`; `disassemble_binary(data, base_addr=32768, start_offset=0, length=None, xdf_labels=None)`; `load_xdf_labels(xdf_path)`; `main()`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: No-argument auto-discovery and positional hex conversion; explicit identity/bounds/output tests absent. Source reconfigures process streams; import is not guaranteed side-effect free.

### `68hc11_disassembler_tool_for_vy_v6/hc11_opcode_table.py`

- Purpose: HC11 Complete Opcode Table.
- CLI: No command-line parser; Python API only.
- API: `get_opcode_info(opcode: int, prebyte: int=0)`; `is_prebyte(opcode: int)`; `get_all_opcodes_for_mnemonic(mnemonic: str)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Independent opcode table kept unchanged; reconcile via exhaustive encoding tests before replacing shared active assembler table.

### `68hc11_disassembler_tool_for_vy_v6/hc11_opcodes_complete.py`

- Purpose: Complete Motorola HC11 Opcode Dictionary.
- CLI: No command-line parser; Python API only.
- API: `decode_opcode(data, offset)`; `format_instruction(mnemonic, operand_bytes, addressing_mode, rom_address)`; `is_rpm_comparison(mnemonic, operand_bytes, addressing_mode)`; `is_timer_io_access(mnemonic, operand_bytes, addressing_mode)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Independent decoder helpers kept unchanged; truncated/prebyte and signed branch fixtures needed.

### `68hc11_disassembler_tool_for_vy_v6/hc11_pattern_analyzer.py`

- Purpose: HC11 Pattern Analyzer - Advanced Code Structure Detection.
- CLI: main() demo with fixed/default inputs; no argparse interface.
- API: `main()`; `CodePattern()`; `HC11PatternAnalyzer(find_isr_patterns, find_table_lookup_patterns, find_mode_switching_patterns, find_error_handlers, find_rpm_limiters, find_subroutine_calls, analyze_hotspots, generate_report)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Fixed absolute path literal(s) remain at lines 532.

### `68hc11_disassembler_tool_for_vy_v6/hc11_subroutine_reverse_engineer.py`

- Purpose: HC11 Subroutine Reverse Engineering Tool.
- CLI: `python hc11_subroutine_reverse_engineer.py <binary_file>`.
- API: `main()`; `Instruction()`; `Subroutine()`; `HC11SubroutineReverseEngineer(analyze_all, disassemble_subroutine, decode_instruction, print_comprehensive_analysis, export_results)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: No full behavioral qualification; bounds, output overwrite, dependency errors and exact-target correctness remain open.

### `68hc11_disassembler_tool_for_vy_v6/memory_map_analyzer.py`

- Purpose: VY V6 ECU Memory Map Analyzer.
- CLI: main() demo with fixed/default inputs; no argparse interface.
- API: `load_binary(path)`; `read_word(data, offset)`; `analyze_vectors(data)`; `verify_xdf_addresses(data)`; `find_code_regions(data)`; `analyze_memory_mapping(data, reset_vector)`; `find_free_space(data)`; `generate_ghidra_import_settings(data, reset_vector)`; `main()`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Fixed absolute path literal(s) remain at lines 27.

### `68hc11_disassembler_tool_for_vy_v6/split_and_disassemble.py`

- Purpose: VY V6 128KB Binary Splitter, Disassembler & Differ.
- CLI: '--split-only'; '--diff'; '--bins'.
- API: `get_register_comment(addr)`; `read_bin(filepath)`; `split_bin(data, name, output_dir)`; `extract_vectors(bank1_data)`; `disassemble_bank(bank_data, cpu_base, bank_name, name, output_dir)`; `diff_banks(stock_data, enhanced_data, bank_name, cpu_base, output_dir, stock_name, enh_name)`; `main()`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: No full behavioral qualification; bounds, output overwrite, dependency errors and exact-target correctness remain open.

### `68hc11_disassembler_tool_for_vy_v6/table_auto_detector.py`

- Purpose: Table Auto-Detector - Find calibration lookup tables by code pattern analysis.
- CLI: 'binary'; '--xdf'/'-x'; '--output'/'-o'; '--json'.
- API: `main()`; `TableCandidate()`; `TableAccess()`; `TableAutoDetector(load_binary, load_xdf, scan_for_ldx_patterns, estimate_table_sizes, scan_all_code, generate_report, export_json, run_detection)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Opcode patterns/table-size inference are heuristic. No verified calibration identity or authoritative table size proof.

### `68hc11_disassembler_tool_for_vy_v6/table_auto_detector_stage_2.py`

- Purpose: Table Auto-Detector Stage 2 - Finds calibration lookup tables by code pattern analysis that werent looked for in the first stage.
- CLI: 'binary'; '--xdf'/'-x'; '--output'/'-o'; '--json'.
- API: `main()`; `TableCandidate()`; `TableAccess()`; `TableAutoDetector(load_binary, load_xdf, scan_for_ldx_patterns, estimate_table_sizes, scan_all_code, generate_report, export_json, run_detection)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Separate historical table-detector stage retained; compare with first variant before consolidation.

### `68hc11_disassembler_tool_for_vy_v6/ultimate_binary_analyzer.py`

- Purpose: ULTIMATE ECU BINARY ANALYZER & COMPARATOR v2.0.
- CLI: 'analyze' [command]; 'file'; '--xdf'; '--json'; '--platform'; '--output'/'-o'; 'compare' [command]; 'file1'; 'file2'; '--xdf'; '--output'/'-o'; '--focus'; '--annotate'; 'disasm' [command]; 'file'; 'offset'; '--length'/'-l'; '--xdf'; '--base'; '--output'/'-o'; '--format'; 'mystery' [command]; 'file'; '--xdf'; '--min-refs'; '--output'/'-o'; 'vectors' [command]; 'file'; '--json'; 'xdf-info' [command]; 'xdf'; '--list-tables'; '--list-constants'; '--search'; 'scan' [command]; 'path'; '--find-duplicates'; '--find-matches'; '--threshold'; '--output'/'-o'; '--extensions'; 'hexdump' [command]; 'file'; 'offset'; '--length'/'-l'; '--output'/'-o'; 'find-pattern' [command]; 'file'; 'pattern'; '--max-results'.
- API: `main()`; `quick_compare(file1: str, file2: str, xdf: str=None)`; `quick_disasm(filepath: str, offset: int, length: int=64, xdf: str=None)`; `quick_analyze(filepath: str)`; `quick_mystery(filepath: str, xdf: str=None)`; `quick_vectors(filepath: str)`; `quick_xdf(xdf_path: str)`; `disasm_tic3_isr(filepath: str=None, xdf: str=None)`; `disasm_dwell_calc(filepath: str=None, xdf: str=None)`; `disasm_the1_spark_cut(filepath: str=None, xdf: str=None)`; `compare_v10a_v11a(bin_dir: str='.', xdf: str=None)`; `HoldenPlatform()`; `PlatformConfig()`; `AnalyzerConfig()`; `XDFParser(load_xdf, lookup)`; `HC11Disassembler(read_byte, read_word, get_annotation, disassemble_instruction, disassemble_range)`; `BinaryAnalyzer(categorize_size, detect_signatures, calculate_hashes, find_empty_regions, analyze, disassemble_at, hex_dump)`; `BinaryComparator(find_differences, compare, annotate_differences, print_diff_report)`; `BatchBinaryAnalyzer(scan, find_duplicates, find_near_matches, export_results)`; `EnhancedXDFParser(load_xdf, xdf_addr_to_file_offset)`; `MysteryRAMFinder(scan_for_ram_references, find_mystery_ram)`; `PlatformDetector(detect, get_vector_table)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Platform auto-detection and mixed VS/VT/VX/VY adapters are hypotheses; never transplant addresses between profiles. Output/bounds and similarity-threshold negative tests absent.

### `68hc11_disassembler_tool_for_vy_v6/xdf_full_parser.py`

- Purpose: Comprehensive XDF Parser - Extract ALL addresses by category.
- CLI: No command-line parser; Python API only.
- API: `decode_html(text)`; `parse_xdf(xdf_path)`; `print_category_summary(data, output_file=None)`; `export_category_addresses(data, category_name, output_file)`; `search_keywords(data, keywords)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Fixed user/drive defaults in __main__; standalone analysis remains unqualified. Fixed absolute path literal(s) remain at lines 218, 219.

### `hc11_bench_incar_emulator/template_addresses_might_be_wrong/aldl_bridge.py`

- Purpose: ALDL Serial Bridge — Phase 1.
- CLI: '--port'; '--mode'; '--interval'; '--count'; '--log-csv'; '--log-json'; '--verbose'/'-v'.
- API: `main()`; `ALDLBridge(connect, disconnect, send_frame, receive_response, enter_diagnostics, exit_diagnostics, read_mode1, send_mode4, poll_mode1, export_log_json)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Imports optional pyserial and exits process on dependency absence; --help may fail without it. Hardware commands never executed.

### `hc11_bench_incar_emulator/template_addresses_might_be_wrong/aldl_frame.py`

- Purpose: ALDL Frame Builder / Parser.
- CLI: No command-line parser; Python API only.
- API: `checksum(data: bytes)`; `verify_checksum(frame: bytes)`; `build_mode1_request()`; `build_enter_diagnostics()`; `build_exit_diagnostics()`; `build_mode4_frame(payload: bytes)`; `build_mode4_discrete(fan_low: bool=False, fan_high: bool=False, ac_clutch: bool=False, cel: bool=False, fuel_pump: bool=False)`; `build_mode4_spark_override(advance_degrees: float)`; `build_mode4_afr_override(target_afr: float)`; `build_mode4_iac_override(position: int)`; `build_mode4_injector_kill(cylinders_to_kill: list[int])`; `build_clear_dtcs()`; `parse_mode1_response(data: bytes)`; `parse_raw_frame(raw: bytes)`; `hex_dump(data: bytes, prefix: str='')`; `ALDLFrame(length, build)`; `Mode1Response()`.
- Coverage: Existing offline ALDL/checksum/crank tests run; physical protocol/pin behavior unqualified.
- Findings/status: No full behavioral qualification; bounds, output overwrite, dependency errors and exact-target correctness remain open.

### `hc11_bench_incar_emulator/template_addresses_might_be_wrong/bench_config.py`

- Purpose: HC11 Bench Emulator — Pin / Address Configuration.
- CLI: No command-line parser; Python API only.
- API: `crank_freq(rpm: int, pulses_per_rev: int=3)`; `get_unverified_pins()`; `print_verification_status()`.
- Coverage: Existing offline ALDL/checksum/crank tests run; physical protocol/pin behavior unqualified.
- Findings/status: Pins and address/protocol constants are template assumptions. Never use these as wiring verification.

### `hc11_bench_incar_emulator/template_addresses_might_be_wrong/bench_test_runner.py`

- Purpose: Bench Test Runner — Automated Validation Framework.
- CLI: '--port'; '--suite'; '--report'; '--validate-frames'; '--verbose'/'-v'.
- API: `test_frame_checksums()`; `test_frame_lengths()`; `test_frame_mode_bytes()`; `test_crank_frequencies()`; `test_cts_resistance()`; `cross_validate_with_emulator(bench_output: dict, emulator_output_path: str)`; `main()`; `TestCase()`; `TestReport(add_result, to_dict)`; `BenchTestRunner(run_offline_tests, run_safe_hardware_tests, print_summary, export_report)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: offline/safe/full names are legacy labels; even safe mode can operate hardware. Only separate pure frame tests were run.

### `hc11_bench_incar_emulator/template_addresses_might_be_wrong/flash_and_capture.py`

- Purpose: Flash & Capture Pipeline — Phase 3+.
- CLI: 'pipeline' [command]; '--source'; '--base'; '--port'; '--duration'; '--flash-tool'; '--verbose'/'-v'; 'capture' [command]; '--port'; '--duration'; '--output'; '--verbose'/'-v'; 'compare' [command]; 'bench_json'; 'emulator_json'.
- API: `compare_outputs(bench_json: str, emulator_json: str)`; `main()`; `FlashAndCapture(compile_source, assemble, patch_binary, flash_to_pcm, capture_aldl_output, run_full_pipeline)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Contains compile/patch/flash pipeline, cwd-relative stale compiler paths, and external flash tool calls. Never executed. No qualified flash artifact.

### `hc11_bench_incar_emulator/template_addresses_might_be_wrong/mode4_bench_tester.py`

- Purpose: Mode 4 Bench Test Harness.
- CLI: '--port'; '--test'; '--list'; '--log'; '--verbose'/'-v'.
- API: `main()`; `TestResult(to_dict)`; `BenchTest()`; `Mode4BenchTester(run_test, run_all_safe, run_all, export_results, list_tests)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Mode4 actuator commands can change engine outputs; list/safe/all are not hardware authorization. Never executed.

### `hc11_bench_incar_emulator/template_addresses_might_be_wrong/sensor_simulator.py`

- Purpose: Sensor Simulator — Phase 2.
- CLI: '--mode'; '--profile'; '--speed'; '--dac'; '--port'; '--verbose'/'-v'; '--list-profiles'.
- API: `cts_resistance_for_temp(temp_c: float)`; `main()`; `SensorSpec()`; `SensorKeyframe()`; `DACInterface(set_voltage, set_resistance_via_digipot)`; `MockDAC(set_voltage, set_resistance_via_digipot)`; `ArduinoDAC(set_voltage, set_resistance_via_digipot)`; `SensorSimulator(apply_static, run_dynamic)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Mock and Arduino DAC adapters exist; pins/scaling/profile timing unqualified. No hardware or mock sensor session executed.

### `hc11_bench_incar_emulator/template_addresses_might_be_wrong/tests/test_aldl_frame.py`

- Purpose: Unit tests for ALDL frame builder / parser.
- CLI: `python -m pytest <this test path>`; offline tests only.
- API: `test_checksum_zero_data()`; `test_checksum_single_byte()`; `test_checksum_basic()`; `test_verify_checksum_valid()`; `test_verify_checksum_invalid()`; `test_mode1_request()`; `test_enter_diagnostics()`; `test_exit_diagnostics()`; `test_mode4_frame_custom_payload()`; `test_mode4_discrete_fan_high()`; `test_mode4_discrete_multiple()`; `test_mode4_discrete_all_off()`; `test_mode4_spark_override()`; `test_mode4_spark_override_clamping()`; `test_mode4_afr_override()`; `test_mode4_iac_override()`; `test_mode4_iac_clamping()`; `test_mode4_injector_kill_single()`; `test_mode4_injector_kill_multiple()`; `test_mode4_injector_kill_all()`; `test_mode4_injector_kill_invalid()`; `test_clear_dtcs()`; `test_frame_length_consistency()`; `test_parse_valid_frame()`; `test_parse_invalid_checksum()`; `test_parse_too_short()`; `test_parse_wrong_length()`; `test_hex_dump()`; `test_aldl_frame_repr()`; `test_crank_freq()`; `test_crank_freq_zero()`.
- Coverage: Existing offline ALDL/checksum/crank tests run; physical protocol/pin behavior unqualified.
- Findings/status: No full behavioral qualification; bounds, output overwrite, dependency errors and exact-target correctness remain open.

### `hc11_esp32_arduino_raspberri_code/raspberri_pi/aldl_interface.py`

- Purpose: aldl_interface.py — ALDL Serial Communication Library for VY V6 Delco PCMs.
- CLI: '--port'/'-p'; '--baud'/'-b'; '--scan'; '--mode1'; '--disable-chatter'.
- API: `aldl_checksum(data: bytes)`; `verify_checksum(frame: bytes)`; `build_simple_frame(device_id: int, mode: int)`; `build_mode1_request(device_id: int=DEVICE_PCM)`; `build_mode4_frame(device_id: int, control_bytes: bytes)`; `build_security_seed_request(device_id: int=DEVICE_PCM)`; `build_security_key_send(device_id: int, key: int)`; `calculate_security_key(seed_hi: int, seed_lo: int)`; `build_mode6_upload_chunk(device_id: int, chunk_data: bytes, load_addr: int, bank_id: int)`; `hexdump(data: bytes, prefix: str='')`; `main()`; `ALDLConnection(scan_ports, open, close, is_connected, detect_silence, tx_frame, rx_frame, send_and_receive, find_response, send_command, disable_chatter, enable_chatter, request_mode5, unlock_security, upload_kernel, read_mode1_stream, send_mode4_override)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Port scanning/chatter/security/upload operations exist; no serial execution. Frame helper duplication needs exact protocol/identity fixtures.

### `hc11_esp32_arduino_raspberri_code/raspberri_pi/datastream_reader.py`

- Purpose: datastream_reader.py — Real-Time ALDL Data Stream Reader.
- CLI: '--port'/'-p'; '--baud'/'-b'; '--log'/'-l'; '--interval'/'-i'; '--raw'.
- API: `parse_datastream(raw: bytes)`; `format_display(data: Dict[str, float])`; `main()`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Data offsets/scaling are target-specific; poll timing and CSV clobber/close behavior need fixtures. No serial execution.

### `hc11_esp32_arduino_raspberri_code/raspberri_pi/flash_patcher.py`

- Purpose: flash_patcher.py — Partial Flash Write Tool for VY V6 Delco PCM.
- CLI: '--port'/'-p'; '--baud'/'-b'; 'test' [command]; 'prepare' [command]; 'kernel' [command]; 'patch' [command]; 'binary'; 'patch_file'; '--offset'; '--output'/'-o'; 'cal-write' [command]; 'binary'.
- API: `read_binary(path: str)`; `write_binary(path: str, data: bytes)`; `calc_gm_checksum(data: bytes)`; `fix_gm_checksum(data: bytearray)`; `apply_patch(original: bytes, patch_data: bytes, patch_offset: int)`; `main()`; `FlashPatcher(prepare_pcm, upload_and_run_kernel, write_cal_only, cleanup)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Contains memory/kernel/write operations as well as offline patch. No execution; range/checksum/identity gates require review before any use.

### `hc11_esp32_arduino_raspberri_code/shared/hc11_opcodes.py`

- Purpose: hc11_opcodes.py — 68HC11 Opcode Table for Assembler/Disassembler.
- CLI: No command-line parser; Python API only.
- API: `build_reverse_table()`; `assemble_instruction(mnemonic: str, operand=None)`; `disassemble(data: bytes, base_addr: int=0)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Independent assembler/disassembler table retained; not substituted into active compiler. Full truncation/range corpus absent.

### `hc11_virtual_emulator/poc/kernel_uploader.py`

- Purpose: KingAi PCM Kernel Uploader -  POC hello world tester.
- CLI: '--port'/'-p'; '--baud'/'-b'; '--device-id'/'-d'; '--test-only'/'-t'; '--list-ports'/'-l'; '--skip-chatter'; '--no-echo'; '--verbose'/'-v'.
- API: `hexdump(data: bytes, prefix: str='')`; `aldl_checksum(frame: bytearray)`; `build_simple_frame(device_id: int, mode: int)`; `build_security_seed_request(device_id: int)`; `build_security_key_send(device_id: int, key: int)`; `calculate_pcm_security_key(seed_high: int, seed_low: int)`; `test_communication(serial: ALDLSerial, device_id: int=PCM_DEVICE_ID)`; `list_serial_ports()`; `main()`; `ALDLSerial(open, close, detect_silence, tx_frame, rx_frame, send_and_receive, find_response)`; `KernelUploader(disable_chatter, enable_chatter, mode5_request, unlock_pcm, upload_kernel_exec, run_upload, cleanup)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: POC serial/security/upload utility. Byte arrays and third-party protocol provenance need independent validation; no execution.

### `hc11_virtual_emulator/src/__init__.py`

- Purpose: Package marker.
- CLI: No command-line parser; Python API only.
- API: No public definitions; module constants/import-time script only.
- Coverage: Empty package marker; no behavior to qualify.
- Findings/status: Package marker; no executable behavior.

### `hc11_virtual_emulator/src/aldl/__init__.py`

- Purpose: Package marker.
- CLI: No command-line parser; Python API only.
- API: No public definitions; module constants/import-time script only.
- Coverage: Empty package marker; no behavior to qualify.
- Findings/status: Package marker; no executable behavior.

### `hc11_virtual_emulator/src/aldl/mode4_harness.py`

- Purpose: HC11 Virtual Emulator — ALDL Mode 4 Test Harness.
- CLI: No argument parser; API/frame example in guarded demonstration.
- API: `aldl_checksum(data: bytes)`; `validate_checksum(frame: bytes)`; `Mode4Offsets()`; `EngineControlBits()`; `DiscreteEnableBits()`; `Mode4Frame(build_frame, set_fan, set_fuel_pump, set_cel, set_ac_clutch, set_iac_rpm, set_iac_position, set_afr, set_spark, clear, hexdump)`; `Mode1Data(cts_degf, tps_pct, rpm, mph, o2_mv, blm, iac_steps, map_kpa, battery_v, spark_deg, afr)`; `ALDLMessageBuilder(enter_diagnostics, nochat, chat, read_mode1, mode4)`; `Mode4TestHarness(send_mode4, test_fan_on, test_fan_off, test_cel_on, test_afr_stoich, test_idle_rpm, test_spark_absolute, report)`.
- Coverage: Existing in-memory emulator suite and/or import smoke run; subset coverage only.
- Findings/status: Pure frame model tested only by scaffold smoke, historical external document references not accessed; no actuator qualification.

### `hc11_virtual_emulator/src/cpu/__init__.py`

- Purpose: Package marker.
- CLI: No command-line parser; Python API only.
- API: No public definitions; module constants/import-time script only.
- Coverage: Empty package marker; no behavior to qualify.
- Findings/status: Package marker; no executable behavior.

### `hc11_virtual_emulator/src/cpu/alu.py`

- Purpose: HC11 Virtual Emulator — ALU Operations + Instruction Handlers.
- CLI: No command-line parser; Python API only.
- API: `add8(a: int, b: int)`; `adc8(a: int, b: int, carry: int)`; `sub8(a: int, b: int)`; `sbc8(a: int, b: int, carry: int)`; `and8(a: int, b: int)`; `or8(a: int, b: int)`; `eor8(a: int, b: int)`; `neg8(val: int)`; `com8(val: int)`; `asl8(val: int)`; `asr8(val: int)`; `lsr8(val: int)`; `rol8(val: int, carry: int)`; `ror8(val: int, carry: int)`; `test_nz8(val: int)`; `add16(a: int, b: int)`; `sub16(a: int, b: int)`; `asl16(val: int)`; `lsr16(val: int)`; `test_nz16(val: int)`; `twos_complement_8(val: int)`.
- Coverage: Existing in-memory emulator suite and/or import smoke run; subset coverage only.
- Findings/status: Pure arithmetic functions exercised by emulator suite; not exhaustive flags/cycle/interrupt proof.

### `hc11_virtual_emulator/src/cpu/decoder.py`

- Purpose: HC11 Virtual Emulator — Opcode Decoder / Dispatch Table.
- CLI: No command-line parser; Python API only.
- API: `decode_opcode(memory, pc: int)`; `IllegalOpcode()`.
- Coverage: Existing in-memory emulator suite and/or import smoke run; subset coverage only.
- Findings/status: Opcode dispatch exercised by emulator suite; full instruction/mode oracle still absent.

### `hc11_virtual_emulator/src/cpu/regs.py`

- Purpose: HC11 Virtual Emulator — CPU Register Set + CCR Flag Management.
- CLI: No command-line parser; Python API only.
- API: `Registers(D, D, set_HNZVC, set_NZVC, set_NZV, set_ZVC, set_C, set_Z, set_I, set_V, set_X_bit, carry, zero, negative, overflow, irq_masked, half_carry, push8, push16, pull8, pull16, display, reset)`.
- Coverage: Existing in-memory emulator suite and/or import smoke run; subset coverage only.
- Findings/status: Register/stack/CCR model exercised by emulator suite; not full silicon equivalence.

### `hc11_virtual_emulator/src/emu.py`

- Purpose: HC11 Virtual Emulator — Main Emulator Class.
- CLI: No argument parser; `HC11Emulator` Python API.
- API: `StopReason()`; `HC11Emulator(load_binary, load_s19, load_reset_vector, step, run, add_breakpoint, remove_breakpoint, clear_breakpoints, enable_trace, get_trace, clear_trace, reset)`; `_HaltException()`; `_StopException()`.
- Coverage: Existing in-memory emulator suite and/or import smoke run; subset coverage only.
- Findings/status: CPU integration subset tested in-memory; no real ROM or cycle-accurate ECU qualification.

### `hc11_virtual_emulator/src/mem/__init__.py`

- Purpose: Package marker.
- CLI: No command-line parser; Python API only.
- API: No public definitions; module constants/import-time script only.
- Coverage: Empty package marker; no behavior to qualify.
- Findings/status: Package marker; no executable behavior.

### `hc11_virtual_emulator/src/mem/memory.py`

- Purpose: HC11 Virtual Emulator — 64K Memory Map with Region Routing.
- CLI: No command-line parser; Python API only.
- API: `MemoryRegion(contains, size)`; `Memory(read8, write8, read16, write16, load_binary, load_s19, register_io_handler, add_watchpoint, remove_watchpoint, snapshot_ram, diff_snapshots, save_eeprom, load_eeprom, hexdump)`.
- Coverage: Existing in-memory emulator suite and/or import smoke run; subset coverage only.
- Findings/status: In-memory routing/load helpers tested indirectly; S19 malformed/overlap/bounds corpus and save-output collision checks incomplete.

### `hc11_virtual_emulator/src/periph/__init__.py`

- Purpose: Package marker.
- CLI: No command-line parser; Python API only.
- API: No public definitions; module constants/import-time script only.
- Coverage: Empty package marker; no behavior to qualify.
- Findings/status: Package marker; no executable behavior.

### `hc11_virtual_emulator/src/periph/adc.py`

- Purpose: HC11 Virtual Emulator — ADC Peripheral.
- CLI: No command-line parser; Python API only.
- API: `ADCPeripheral(register, set_channel, set_sensors_normal, reset)`.
- Coverage: Existing in-memory emulator suite and/or import smoke run; subset coverage only.
- Findings/status: Simplified ADC register model; import smoke/integration only, not physical conversion/timing proof.

### `hc11_virtual_emulator/src/periph/ports.py`

- Purpose: HC11 Virtual Emulator — I/O Ports Peripheral.
- CLI: No command-line parser; Python API only.
- API: `PortsPeripheral(register, get_port, set_input, on_change, get_portb_bits, reset)`.
- Coverage: Existing in-memory emulator suite and/or import smoke run; subset coverage only.
- Findings/status: Simplified ports model; import smoke/integration only, not electrical output proof.

### `hc11_virtual_emulator/src/periph/sci.py`

- Purpose: HC11 Virtual Emulator — SCI (Serial Communication Interface) Peripheral.
- CLI: No command-line parser; Python API only.
- API: `SCIPeripheral(register, inject_rx, sci_output, reset)`.
- Coverage: Existing in-memory emulator suite and/or import smoke run; subset coverage only.
- Findings/status: In-memory serial peripheral model; smoke confirms TX bytes only. No real serial connection.

### `hc11_virtual_emulator/src/periph/timer.py`

- Purpose: HC11 Virtual Emulator — Timer Peripheral.
- CLI: No command-line parser; Python API only.
- API: `TimerPeripheral(register, update, reset)`.
- Coverage: Existing in-memory emulator suite and/or import smoke run; subset coverage only.
- Findings/status: Simplified timer model; no measured silicon timer/interrupt accuracy proof.

### `hc11_virtual_emulator/tests/test_emulator_core.py`

- Purpose: HC11 Virtual Emulator — Core Integration Tests.
- CLI: No command-line parser; Python API only.
- API: `run_all_tests()`; `TestLoadStore(test_ldaa_immediate, test_ldaa_negative, test_ldaa_zero, test_ldab_immediate, test_ldd_immediate, test_ldx_immediate, test_staa_direct, test_staa_extended, test_ldaa_indexed_x, test_std_direct)`; `TestArithmetic(test_adda_immediate, test_adda_carry, test_adda_overflow, test_suba_immediate, test_suba_borrow, test_addd_16bit, test_inca, test_deca, test_mul)`; `TestBranch(test_beq_taken, test_beq_not_taken, test_bne_taken, test_bra_backward, test_bcc_bcs)`; `TestStack(test_push_pull_a, test_jsr_rts)`; `TestTransfer(test_tab, test_tba, test_xgdx)`; `TestBitOps(test_bset_direct, test_bclr_direct)`; `TestSCI(test_sci_tx_byte, test_sci_rx_inject)`; `TestPrograms(test_countdown_loop, test_memory_fill, test_16bit_counter, test_subroutine_call)`; `TestALDLHello(test_aldl_hello_world_asm)`; `TestADC(test_adc_read_channel)`; `TestWatchpoints(test_watchpoint_fires, test_ram_snapshot_diff)`; `TestMode4Harness(test_frame_checksum, test_fan_control_bytes, test_spark_control_bytes, test_afr_stoich, test_iac_rpm)`.
- Coverage: Existing in-memory emulator suite and/or import smoke run; subset coverage only.
- Findings/status: No full behavioral qualification; bounds, output overwrite, dependency errors and exact-target correctness remain open.

### `hc11_virtual_emulator/tests/test_scaffold_imports.py`

- Purpose: HC11 Virtual Emulator — Scaffold Import Check.
- CLI: `python -m pytest <this test path>` or execute file for offline import/smoke checks.
- API: `test_imports()`.
- Coverage: Existing in-memory emulator suite and/or import smoke run; subset coverage only.
- Findings/status: Fixed swallowed smoke assertion failures: every smoke exception now enters the failure gate and raises, rather than printing success. Removes pytest bool-return warning.

### `hc11_virtual_emulator/tools/ALDL_read_RAM_commands.py`

- Purpose: ALDL_read_RAM_commands.py — Standalone ALDL RAM Reader.
- CLI: '--port'; '--baud'; '--device-id'; '--address'; '--count'; '--extended'; '--silence'; '--output'; '--loopback'; '--bin-file'; '--no-hexdump'.
- API: `compute_checksum(frame: bytearray)`; `apply_checksum(frame: bytearray)`; `verify_checksum(frame: bytes)`; `build_mode2_read(device_id: int, address: int, extended: bool=False)`; `build_silence_frame(device_id: int)`; `build_unsilence_frame(device_id: int)`; `read_ram(transport, address: int, extended: bool=False, device_id: int=DEVICE_VX_VY)`; `read_range(transport, start: int, length: int, extended: bool=False, device_id: int=DEVICE_VX_VY)`; `silence_bus(transport, device_id: int=DEVICE_VX_VY)`; `unsilence_bus(transport, device_id: int=DEVICE_VX_VY)`; `hex_dump(data: bytes, base_addr: int=0, width: int=16)`; `main()`; `ALDLSerial(open, close, transact)`; `LoopbackALDL(open, close, transact)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: RAM reader can send chatter/read commands over serial; default COM port exists. No execution.

### `hc11_virtual_emulator/tools/_verify_bytecodes.py`

- Purpose: Verify all kernel bytecode arrays against OSE source values.
- CLI: No command-line parser; Python API only.
- API: `compare(name, src_dec, our_hex)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Runs comparison prints at import and contains hardcoded bytecode references; not an independent reference oracle or CLI.

### `hc11_virtual_emulator/tools/hc11_disassembler.py`

- Purpose: HC11 Disassembler — Standalone API Module for KingAI Commie Flasher.
- CLI: No argument parser; guarded fixed-byte decoder demonstration.
- API: `disassemble_hex(hex_string: str, base_addr: int=0, annotate: bool=True)`; `disassemble_bytes(data: bytes, base_addr: int=0, annotate: bool=True)`; `Instruction()`; `DisassembledInstruction(hex_str, format, format_compact)`; `HC11Disassembler(disassemble, disassemble_hex, decode_one, get_stats)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Independent standalone decoder for virtual-tool integration; no exhaustive encoding/branch/truncated-input corpus in this review.

### `hc11_virtual_emulator/tools/virtual_128kb_eeprom.py`

- Purpose: virtual_128kb_eeprom.py — AMD 29F010 NOR Flash Simulator.
- CLI: Execute file to run in-memory `_self_test()`; no command-line parser or hardware connection.
- API: `setup_logging(name: str='vecu.flash', level: int=logging.DEBUG, console_level: int=logging.WARNING, log_dir: Optional[Path]=None, rich_console: bool=True)`; `FlashState()`; `AMD29F010(data, state, is_busy, load_from_file, save_to_file, load_from_bytes, addr_to_sector, sector_base, is_sector_protected, read, write, poll, erase_sector_by_index, program_byte_at, read_software_id, read_sector_protect_status, verify_sector_erased, verify_data, compute_checksum, dump_sector_info, dump_stats)`; `BankedFlash(current_bank, select_bank, cpu_to_flash_addr, read, write, program_byte, erase_sector)`.
- Coverage: New tests/research_tools regression coverage (subset/API/help/import/negative inputs as applicable); no hardware.
- Findings/status: Removed import-time directory/log-file writes. Logger configuration is explicit; this change does not qualify chip timing or flash behavior.

### `hc11_virtual_emulator/tools/virtual_aldl_frame_sender_and_vecu.py`

- Purpose: virtual_aldl_frame_sender_and_vecu.py — Standalone Virtual ECU + Frame Sender.
- CLI: '--mode'; '--serial'; '--baud'; '--host'; '--port'; '--bin'; '--frame'; '--verbose'/'-v'.
- API: `setup_logging(name: str='vecu', level: int=logging.DEBUG, console_level: int=logging.WARNING, log_dir: Optional[Path]=None, rich_console: bool=True)`; `compute_checksum(frame: bytearray, end: int)`; `apply_checksum(frame: bytearray)`; `verify_frame(data: bytes)`; `frame_wire_length(frame: bytes)`; `hex_str(data: bytes)`; `hex_dump(data: bytes, base_addr: int=0, width: int=16)`; `compute_seed_key(seed_hi: int, seed_lo: int)`; `compute_vy_checksum(data: bytearray, start: int=8192, end: int=131072, skip_start: int=16384, skip_end: int=16391)`; `run_vecu_tcp(vecu: VirtualECU, host: str='127.0.0.1', port: int=8192)`; `handle_client(vecu: VirtualECU, conn: socket.socket)`; `send_frame(serial_port, frame_hex: str, baud: int=ALDL_BAUD)`; `interactive_mode(serial_port: str, baud: int=ALDL_BAUD)`; `main()`; `VirtualECU(flash, process_frame, erase_sector, get_flash_info, verify_checksum, dump_flash_info, dump_stats)`.
- Coverage: New tests/research_tools regression coverage (subset/API/help/import/negative inputs as applicable); no hardware.
- Findings/status: Removed import-time directory/log-file writes. CLI logger configured after parsing; --help has no log side effects. TCP/serial paths were not executed.

### `vy_$060a_enhanced_1.0_bin_xdf_example/_check_dupes.py`

- Purpose: Report duplicate scalar addresses from an explicitly supplied XDF JSON export.
- CLI: 'json'.
- API: `main(argv=None)`.
- Coverage: New tests/research_tools regression coverage (subset/API/help/import/negative inputs as applicable); no hardware.
- Findings/status: Replaced implicit CWD JSON read at import with explicit JSON argument, schema diagnostics, deterministic duplicate ordering and guarded main.

### `vy_$060a_enhanced_1.0_bin_xdf_example/_verify_labels.py`

- Purpose: Historical bank-1 VY $060A label cross-check; no firmware qualification.
- CLI: '--json'; '--binary'; '--labeled-asm'; '--unlabeled-asm'; '--expected-sha256'.
- API: `verify(JSON_PATH, BIN_PATH, LABELED_ASM, UNLABELED_ASM)`; `main(argv=None)`.
- Coverage: New tests/research_tools regression coverage (subset/API/help/import/negative inputs as applicable); no hardware.
- Findings/status: Guarded main with explicit four inputs, required expected binary SHA-256 and exact 128 KiB size. Negative/malformed scalar addresses are rejected; mismatches now return nonzero. Full real-image correctness remains untested.

### `vy_$060a_enhanced_1.0_bin_xdf_example/hw_labels.py`

- Purpose: HC11 Hardware / RAM / ISR / Vector Label Map.
- CLI: Guarded self-test prints hardcoded label examples; Python API is `HWLabelMap`.
- API: `HWLabelMap(lookup, stats)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Hardcoded hardware/RAM/ISR annotations remain image-specific research; label map has no input hash binding.

### `vy_$060a_enhanced_1.0_bin_xdf_example/xdf_asm_labeler.py`

- Purpose: KingAI XDF → ASM Auto-Labeler.
- CLI: xdf_asm_labeler.py <json_export> <input.asm> [output.asm] [--bank N] [--stats].
- API: `xdf_addr_to_cpu(xdf_addr: int, bank: int=1)`; `cpu_to_xdf_addr(cpu_addr: int, bank: int=1)`; `detect_asm_format(first_lines: List[str])`; `sanitize_label(title: str)`; `annotate_custom_format(lines: List[str], labels: XDFLabelMap, bank: int=1)`; `annotate_udis_format(lines: List[str], labels: XDFLabelMap, bank: int=1)`; `print_usage()`; `detect_bank_from_filename(filename: str)`; `main()`; `XDFLabelMap(lookup, get_scalar, get_flag, get_table, stats)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Legacy annotation interpretation/output overwrites lack dedicated exact-image fixtures; regex whitespace matching was checked statically and with a synthetic line, and no regex defect is claimed.

### `vy_$060a_enhanced_1.0_bin_xdf_example/xdf_asm_labeler_v2.py`

- Purpose: KingAI XDF + HC11 → ASM Auto-Labeler  v2.1.
- CLI: xdf_asm_labeler_v2.py <json_export> <input.asm> [output.asm] [--bank N] [--stats].
- API: `detect_asm_format(first_lines: List[str])`; `annotate_custom_format(lines: List[str], xdf: XDFLabelMap, hw: HWLabelMap, bank: int=1)`; `annotate_udis_format(lines: List[str], xdf: XDFLabelMap, hw: HWLabelMap, bank: int=1)`; `print_usage()`; `detect_bank_from_filename(filename: str)`; `main()`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Separate HW/XDF adapters retained. Annotation correctness and output collision checks need fixtures; unqualified.

### `vy_$060a_enhanced_1.0_bin_xdf_example/xdf_labels.py`

- Purpose: XDF Label Map — Calibration data from TunerPro XDF exports.
- CLI: `python xdf_labels.py <Enhanced_v1.json>` guarded self-test.
- API: `xdf_addr_to_cpu(xdf_addr: int, bank: int=1)`; `cpu_to_xdf_addr(cpu_addr: int, bank: int=1)`; `XDFLabelMap(lookup, get_scalar, get_flag, get_table, stats)`.
- Coverage: Static review only; no dedicated behavioral run. Needs explicit input/dependency/range/output and exact target fixtures before promotion.
- Findings/status: Bank argument transforms require exact image/XDF pairing; JSON shape and numeric range negative tests incomplete.

## Arduino/ESP32 and installer sources

### `hc11_bench_incar_emulator/template_addresses_might_be_wrong/crank_signal_generator.ino`

- Purpose/API: 3X/18X crank signal template; `setup()`/`loop()`; serial RPM input; compile-time pin constants.
- Coverage: Static inspection only; no board toolchain/build/upload/hardware run.
- Findings/status: Placeholder pins/signal conditioning and phase assumptions; no timing, wiring, or build proof.

### `hc11_esp32_arduino_raspberri_code/arduino/aldl_bluetooth_mega/ALDL-Arduino-mega.ino`

- Purpose/API: Bluetooth/ALDL/wideband bridge; `setup()`/`loop()`; Serial2/Serial3 and fixed AFR byte slot.
- Coverage: Static inspection only; no board toolchain/build/upload/hardware run.
- Findings/status: Third-party copyright notice retained; explicit redistribution license not verified. Fixed frame slot and untested scaling require bounds/protocol fixtures. Duplicate directory variants retained.

### `hc11_esp32_arduino_raspberri_code/arduino/aldl_bt_wideband/ALDL-Arduino-mega.ino`

- Purpose/API: Bluetooth/ALDL/wideband bridge; `setup()`/`loop()`; Serial2/Serial3 and fixed AFR byte slot.
- Coverage: Static inspection only; no board toolchain/build/upload/hardware run.
- Findings/status: Third-party copyright notice retained; explicit redistribution license not verified. Fixed frame slot and untested scaling require bounds/protocol fixtures. Duplicate directory variants retained.

### `hc11_esp32_arduino_raspberri_code/arduino/aldl_reader/aldl_reader.ino`

- Purpose/API: Mode1 datastream Arduino reader; `setup()`/`loop()`; serial datastream polling.
- Coverage: Static inspection only; no board toolchain/build/upload/hardware run.
- Findings/status: Relative shared-header include resolves to a nonexistent arduino/shared location; connector descriptions conflict with other sketches; unqualified.

### `hc11_esp32_arduino_raspberri_code/arduino/memory_dumper/memory_dumper.ino`

- Purpose/API: ECU memory read/write and RAM-kernel prototype; `setup()`/`loop()`; USB serial commands; compile-time serial pins.
- Coverage: Static inspection only; no board toolchain/build/upload/hardware run.
- Findings/status: Memory/kernel writes exist; relative shared-header include is unresolved from sketch folder. Never built/uploaded/executed.

### `hc11_esp32_arduino_raspberri_code/esp32/aldl_wifi_interface/aldl_wifi_interface.ino`

- Purpose/API: Wi-Fi/ALDL bridge with upload endpoint; `setup()`/`loop()`; HTTP/WebSocket service and serial bridge.
- Coverage: Static inspection only; no board toolchain/build/upload/hardware run.
- Findings/status: Hardcoded demonstration AP credential and write/upload surface; insufficient authentication for promotion. Relative shared header unresolved. Never built/started.

### `install_dependancies_pip.bat`

- Purpose/CLI: Windows dependency-install/test setup; run this batch file under a chosen Python virtual environment from any directory.
- API: `python --version`, `python -m pip install -r <script-relative requirements.txt>`, then `python -m pytest <script-relative tests> -v --tb=short`; propagates failure with exit status 1.
- Coverage/status: Source-path and error branches statically reviewed. Script itself was not run because its installation mutates the invoking environment. Active package clean-install results are documented separately.

## Promotion gates still open

Legacy decoders/labelers/bench tools need per-variant synthetic golden inputs, malformed/truncated input bounds, type/range checks, safe output tests, optional dependency diagnostics and reproducible installs before becoming recommended tools. Consolidate by a tested shared core plus explicit target adapters only after side-by-side output agreement; original variants are retained to avoid losing ABI/resource/address alternatives. Existing public third-party firmware, disassembly and protocol attribution does not establish redistribution rights. The release should ship the active Python compiler wheel and clearly identify any source archive research contents as unqualified.

## Retained assembler/header source inventory

- `hc11_esp32_arduino_raspberri_code/shared/aldl_protocol.h`: compile-time protocol/register/frame constants for sketch adapters; source inspected, no dedicated C/Arduino build. Mode/device identity and OSE-derived provenance remain unqualified.
- `hc11_esp32_arduino_raspberri_code/shared/flash_erase_write_kernel.asm`: Mode6 RAM-loaded erase/write prototype with a claimed M29W800DB flash target. Contradicts the AMD29F010 model in the separate simulator; no target substitution, assembly, upload or flash execution was performed. Unsafe/unqualified.
- `hc11_virtual_emulator/poc/watchdog_kernel.asm`: RAM watchdog-loop POC at a hardcoded address; no assembly/upload/execution. Register/device/protocol assumptions remain unqualified.
- `examples/aldl_hello_world.asm`: retained HC11/ALDL assembly example; compiler tests may exercise related instructions but there is no bench validation of this image or protocol.
- `examples/delco_hc11.h`: retained example register macros for multiple claimed HC11 derivatives; no universal register-map or hardware compatibility proof. Include/preprocessor behavior is an active compiler limitation documented separately.
- `vy_$060a_enhanced_1.0_bin_xdf_example/bin_splits_disasm/Enhanced_v1.0a_bank1.asm`, `Enhanced_v1.0a_bank2.asm`, `Enhanced_v1.0a_bank3.asm`: existing public disassembly/reference artifacts retained byte-for-byte. Only their source-tree presence was inventoried; no absent original firmware was inspected, no full assembly correctness/byte reconstruction or rights validation is claimed. Their historical bank names do not bind a SHA-256.
