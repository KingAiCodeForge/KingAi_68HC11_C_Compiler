# Combine Spark Tables POC — 0–4800 / 4800–6400 RPM Main Spark

> AI-generated research (Opus 4.6) using real source material and working tools.

## Goal

Use the C compiler → assembler → patcher pipeline (not standalone Python scripts)
to inject a combined spark table patch into the VY V6 Enhanced binary and verify
it still works after recent edits and enhancements.
Combine Spark Tables POC — 0–4800 / 4800–6400 RPM Main Spark
hook it up to where it needs to link/jump wire and follow flow.
do we do this in free space or over the stock lpg or petrol high and low octane maps. 

## Target Binaries

- `vy_$060a_enhanced_1.0_bin_xdf_example/bin_splits_disasm/` (split banks)
- `vy_$060a_enhanced_1.0_bin_xdf_example/bin_splits_disasm/Enhanced_v1.0a_bank1.bin`
- `vy_$060a_enhanced_1.0_bin_xdf_example/bin_splits_disasm/Enhanced_v1.0a_bank2.bin`
- `vy_$060a_enhanced_1.0_bin_xdf_example/bin_splits_disasm/Enhanced_v1.0a_bank3.bin`
- `vy_$060a_enhanced_1.0_bin_xdf_example/VX-VY_V6_$060A_Enhanced_v1.0a.bin`

## Approach

1. Patch a split bank binary, then recombine using the PowerShell script or
   the HC11 assembler toolchain.
2. Compare output against other tools (not just the Python scripts) for
   cross-validation.
3. Document results in a separate file under an `ignore/` folder.