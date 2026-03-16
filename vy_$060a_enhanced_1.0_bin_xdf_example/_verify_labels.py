#!/usr/bin/env python3
"""Verify xdf_asm_labeler output against source JSON and binary."""
import json
import re
import struct

JSON_PATH = "Enhanced_v1.json"
BIN_PATH = "VX-VY_V6_$060A_Enhanced_v1.0a.bin"
LABELED_ASM = r"bin_splits_disasm\Enhanced_v1.0a_bank1_labeled.asm"
UNLABELED_ASM = r"bin_splits_disasm\Enhanced_v1.0a_bank1.asm"

# Load JSON
with open(JSON_PATH) as f:
    data = json.load(f)

# Load binary
with open(BIN_PATH, "rb") as f:
    bindata = f.read()

# Load labeled ASM into dict: addr -> line_text
asm_lines = {}
with open(LABELED_ASM, encoding='utf-8', errors='replace') as f:
    for line in f:
        m = re.match(r'^L([0-9A-Fa-f]{4}):', line)
        if m:
            addr = int(m.group(1), 16)
            asm_lines[addr] = line.rstrip()

# Load unlabeled ASM for comparison
orig_lines = {}
with open(UNLABELED_ASM, encoding='utf-8', errors='replace') as f:
    for line in f:
        m = re.match(r'^L([0-9A-Fa-f]{4}):', line)
        if m:
            addr = int(m.group(1), 16)
            orig_lines[addr] = line.rstrip()

print("=" * 80)
print("VERIFICATION REPORT - XDF ASM Labeler Output")
print("=" * 80)

errors = []
warnings = []

# ─── TEST 1: Scalar addresses exist in ASM and have correct label ───
print("\n--- TEST 1: Scalar address verification ---")
scalars = [s for s in data['scalars'] if s.get('address')]

# Build a map of all labeled ASM lines including the full text
# so we can search for titles that appear via multi-byte span (+N:$XXXX:)
all_labeled_text = "\n".join(asm_lines.values())

tested = 0
matched = 0
missing_addr = 0
wrong_label = 0
found_in_span = 0
for s in scalars:
    xdf_addr = int(s['address'], 16)
    cpu_addr = xdf_addr  # bank1: xdf_addr = cpu_addr
    title = s.get('title', '')
    value = s.get('value', '')
    
    if cpu_addr not in asm_lines:
        # Not a label line — look for it captured via multi-byte span
        # Search for $XXXX appearing in any label's multi-byte annotation
        addr_tag = f"${cpu_addr:04X}:"
        if addr_tag in all_labeled_text:
            found_in_span += 1
            continue
        missing_addr += 1
        if missing_addr <= 5:
            errors.append(f"MISSING: scalar ${cpu_addr:04X} '{title}' not in ASM at all")
        continue
    
    line = asm_lines[cpu_addr]
    tested += 1
    
    # Check that [XDF] annotation exists
    if '[XDF]' in line:
        # Check title appears (at least first 15 chars)
        title_check = title[:15] if len(title) > 15 else title
        if title_check in line:
            matched += 1
        else:
            wrong_label += 1
            if wrong_label <= 3:
                errors.append(f"WRONG LABEL at ${cpu_addr:04X}: expected '{title_check}' in: {line[-100:]}")
    else:
        wrong_label += 1
        if wrong_label <= 3:
            errors.append(f"NO [XDF] TAG at ${cpu_addr:04X}: {line[:80]}")

print(f"  Scalars with addresses: {len(scalars)}")
print(f"  Found at label line: {tested}")
print(f"  Found via multi-byte span: {found_in_span}")
print(f"  Missing entirely: {missing_addr}")
print(f"  Correctly labeled: {matched}")
print(f"  Wrong/missing label: {wrong_label}")

# ─── TEST 2: Code xref verification ───
print("\n--- TEST 2: Code xref spot-checks ---")
# Find lines in code region ($8000+) with [XDF] annotations
code_xrefs = []
for addr, line in asm_lines.items():
    if addr >= 0x8000 and '[XDF]' in line:
        code_xrefs.append((addr, line))

print(f"  Total code xrefs found: {len(code_xrefs)}")

# Spot-check: extract the referenced address from the [XDF] tag and verify it exists in JSON
xref_verified = 0
xref_wrong = 0
for addr, line in code_xrefs[:50]:
    # Extract the $XXXX from the [XDF] comment
    m = re.search(r'\[XDF\] \$([0-9A-F]{4}):', line)
    if m:
        ref_addr = int(m.group(1), 16)
        # Verify this address exists in the operand
        # Get the instruction part (before the comment)
        instr_part = line.split(';')[0]
        ref_hex_lower = f"${ref_addr:04x}"
        ref_hex_upper = f"${ref_addr:04X}"
        if ref_hex_lower in instr_part or ref_hex_upper in instr_part:
            xref_verified += 1
        else:
            xref_wrong += 1
            if xref_wrong <= 3:
                errors.append(f"XREF MISMATCH at ${addr:04X}: comment says ${ref_addr:04X} but not in operand: {instr_part.strip()}")

print(f"  Spot-checked: {min(50, len(code_xrefs))}")
print(f"  Operand matches comment: {xref_verified}")
print(f"  Mismatches: {xref_wrong}")

# ─── TEST 3: Binary value cross-check ───
print("\n--- TEST 3: Binary byte value cross-check ---")
# For each scalar, check that the raw byte in the binary matches the hex bytes in the ASM line
byte_match = 0
byte_mismatch = 0
for s in scalars[:100]:
    xdf_addr = int(s['address'], 16)
    if xdf_addr >= len(bindata):
        continue
    bin_byte = bindata[xdf_addr]
    
    if xdf_addr in asm_lines:
        line = asm_lines[xdf_addr]
        # Extract hex bytes from the ASM line: "L752A:  9F 38  sts $38"
        m = re.match(r'^L[0-9A-Fa-f]{4}:\s+([0-9A-Fa-f]{2})', line)
        if m:
            asm_byte = int(m.group(1), 16)
            if asm_byte == bin_byte:
                byte_match += 1
            else:
                byte_mismatch += 1
                if byte_mismatch <= 3:
                    errors.append(f"BYTE MISMATCH at ${xdf_addr:04X}: bin=0x{bin_byte:02X} asm=0x{asm_byte:02X}")

print(f"  Tested: {byte_match + byte_mismatch}")
print(f"  Match: {byte_match}")
print(f"  Mismatch: {byte_mismatch}")

# ─── TEST 4: No original lines destroyed ───
print("\n--- TEST 4: Original line preservation ---")
destroyed = 0
for addr, orig_line in orig_lines.items():
    if addr in asm_lines:
        labeled_line = asm_lines[addr]
        # The labeled line should START with the original line (annotation appended)
        orig_stripped = orig_line.rstrip()
        if not labeled_line.startswith(orig_stripped):
            # Could be that an existing comment was there
            # Check instruction part matches
            orig_instr = orig_stripped.split(';')[0].rstrip()
            labeled_instr = labeled_line.split(';')[0].rstrip()
            if orig_instr != labeled_instr:
                destroyed += 1
                if destroyed <= 3:
                    errors.append(f"DESTROYED at ${addr:04X}:\n  orig: {orig_stripped[:80]}\n  new:  {labeled_line[:80]}")
    else:
        destroyed += 1

print(f"  Lines checked: {len(orig_lines)}")
print(f"  Preserved correctly: {len(orig_lines) - destroyed}")
print(f"  Destroyed/changed: {destroyed}")

# ─── TEST 5: Table region coverage ───
print("\n--- TEST 5: Table region coverage ---")
tables = [t for t in data['tables'] if t.get('axes', {}).get('z', {}).get('address')]
table_starts_found = 0
table_starts_in_span = 0
table_starts_missing = 0
for t in tables:
    z_addr = int(t['axes']['z']['address'], 16)
    title = t.get('title', '')[:40]
    if z_addr in asm_lines and '[XDF]' in asm_lines[z_addr]:
        table_starts_found += 1
    elif f"${z_addr:04X}:" in all_labeled_text:
        table_starts_in_span += 1
    else:
        table_starts_missing += 1
        if table_starts_missing <= 3:
            warnings.append(f"TABLE START not labeled: ${z_addr:04X} '{title}'")

print(f"  Tables with z-axis addresses: {len(tables)}")
print(f"  Start at label line: {table_starts_found}")
print(f"  Start in multi-byte span: {table_starts_in_span}")
print(f"  Start address missing: {table_starts_missing}")

# ─── TEST 6: Check for false positive xrefs ───
print("\n--- TEST 6: False positive check (branch targets labeled as xrefs) ---")
false_positives = 0
branch_mnemonics = {'bra', 'brn', 'bhi', 'bls', 'bcc', 'bcs', 'bne', 'beq',
                    'bvc', 'bvs', 'bpl', 'bmi', 'bge', 'blt', 'bgt', 'ble', 'jmp'}
for addr, line in asm_lines.items():
    if addr >= 0x8000 and '[XDF]' in line:
        # Extract mnemonic
        m = re.match(r'^L[0-9A-Fa-f]{4}:\s+[0-9A-Fa-f ]+\s+(\S+)', line)
        if m:
            mnemonic = m.group(1).lower()
            if mnemonic in branch_mnemonics:
                false_positives += 1
                if false_positives <= 3:
                    errors.append(f"FALSE POSITIVE: branch {mnemonic} at ${addr:04X} has [XDF] tag: {line[:100]}")

print(f"  Branch instructions with [XDF] labels: {false_positives}")

# ─── TEST 7: Check JSR/LDX/LDD xrefs to RAM ($0000-$1FFF) aren't tagged ───
print("\n--- TEST 7: RAM address xref check ---")
ram_xrefs = 0
for addr, line in asm_lines.items():
    if addr >= 0x8000 and '[XDF]' in line:
        m = re.search(r'\[XDF\] \$([0-9A-F]{4}):', line)
        if m:
            ref = int(m.group(1), 16)
            if ref < 0x2000:
                ram_xrefs += 1
                if ram_xrefs <= 2:
                    warnings.append(f"RAM xref at ${addr:04X} → ${ref:04X}: {line[:100]}")

print(f"  XDF labels pointing to RAM ($0000-$1FFF): {ram_xrefs}")

# ─── TEST 8: Annotation count consistency ───
print("\n--- TEST 8: Annotation count ─")
total_xdf_tags = sum(1 for line in asm_lines.values() if '[XDF]' in line)
print(f"  Total lines with [XDF] tag: {total_xdf_tags}")

# Expected: header says 8401
# Also check that the INNER calibration region addresses not matching ANY XDF entry 
# remain unlabeled
cal_region_lines = {a: l for a, l in asm_lines.items() if 0x4000 <= a < 0x8000}
cal_labeled = sum(1 for l in cal_region_lines.values() if '[XDF]' in l)
cal_unlabeled = len(cal_region_lines) - cal_labeled
print(f"  Cal region ($4000-$7FFF) lines: {len(cal_region_lines)}")
print(f"  Cal labeled: {cal_labeled}")
print(f"  Cal unlabeled: {cal_unlabeled}")

# ─── SUMMARY ───
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
if errors:
    print(f"\n  ERRORS ({len(errors)}):")
    for e in errors:
        print(f"    ❌ {e}")
if warnings:
    print(f"\n  WARNINGS ({len(warnings)}):")
    for w in warnings:
        print(f"    ⚠️  {w}")
if not errors and not warnings:
    print("  ✅ ALL CHECKS PASSED")
elif not errors:
    print(f"\n  ✅ No errors, {len(warnings)} warnings")
else:
    print(f"\n  ❌ {len(errors)} errors, {len(warnings)} warnings")
