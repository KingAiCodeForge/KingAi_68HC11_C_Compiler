# VY V6 $060A Enhanced v1.0a — Reference Binary & XDF

Reference material for the KingAI HC11 compiler and disassembler tools.
This folder contains the actual VY V6 Enhanced OS binary, XDF definition files,
bank-split outputs, and disassembly results.

## Using the Disassembler Tools on These Files

The Python scripts in `../68hc11_disassembler_tool_for_vy_v6/` can be used
directly on the binaries and XDF files here. See
[how_these_tools_work.md](../68hc11_disassembler_tool_for_vy_v6/how_these_tools_work.md)
for detailed workflows and examples.

### Quick Examples

```bash
# Disassemble bank 2 of the Enhanced binary
python ../68hc11_disassembler_tool_for_vy_v6/hc11_disassembler_060a_enhanced_v1.py \
  --bank bank2 --start 0x8000 --length 0x200

# Find free space for code injection
python ../68hc11_disassembler_tool_for_vy_v6/find_free_space.py \
  "VX-VY_V6_\$060A_Enhanced_v1.0a.bin" --min-size 64

# Extract tables using XDF definitions
python ../68hc11_disassembler_tool_for_vy_v6/binary_table_extractor.py \
  --binary "VX-VY_V6_\$060A_Enhanced_v1.0a.bin" --xdf "*.xdf"
```

## Contents

See [bin_splits_disasm/readme.md](bin_splits_disasm/readme.md) for the
bank-split binary layout and disassembly output details.