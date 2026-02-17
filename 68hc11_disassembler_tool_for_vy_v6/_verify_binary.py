#!/usr/bin/env python3
"""Quick binary verification script - checks key addresses against known values"""
import sys

BIN_PATH = r"A:\kingai_c_compiler_v0.1\vy_$060a_enhanced_1.0_bin_xdf_example\VX-VY_V6_$060A_Enhanced_v1.0a.bin"

with open(BIN_PATH, "rb") as f:
    data = f.read()

print(f"Binary size: {len(data)} bytes ({len(data)//1024}KB)")
print()

# 1. Vector table at $FFD6-$FFFF (file offset same for bank1)
print("=== VECTOR TABLE ($FFD6-$FFFF) — should be ADDRESS WORDS, not code ===")
VECTOR_NAMES = [
    "SCI", "SPI", "PAI_Edge", "PA_Overflow", "Timer_Overflow",
    "OC5", "OC4", "OC3", "OC2", "OC1", "IC3", "IC2", "IC1",
    "RTI", "IRQ", "XIRQ", "SWI", "Illegal_Opcode", "COP_Watchdog",
    "Clock_Monitor", "RESET"
]
vec_start = 0xFFD6
for i, name in enumerate(VECTOR_NAMES):
    addr = vec_start + i * 2
    hi = data[addr]
    lo = data[addr + 1]
    target = (hi << 8) | lo
    print(f"  ${addr:04X}: ${hi:02X} ${lo:02X}  -> ${target:04X}  ({name})")

print()

# 2. Pseudo-ISR Jump Table at $2000
print("=== PSEUDO-ISR JUMP TABLE ($2000-$202F) ===")
for off in range(0x2000, 0x2030, 3):
    op = data[off]
    hi = data[off + 1]
    lo = data[off + 2]
    target = (hi << 8) | lo
    if op == 0x7E:
        print(f"  ${off:04X}: ${op:02X} ${hi:02X} ${lo:02X}  JMP ${target:04X}")
    else:
        print(f"  ${off:04X}: ${op:02X} ${hi:02X} ${lo:02X}  NOT JMP! opcode=${op:02X}")

print()

# 3. Code/Free space boundary
print("=== CODE/FREE BOUNDARY (around $C467-$C470) ===")
for off in range(0xC460, 0xC478):
    b = data[off]
    if off == 0xC460 or off == 0xC468:
        print()
    if off % 16 == 0:
        print(f"  ${off:04X}: ", end="")
    print(f"{b:02X} ", end="")
print()
print(f"  Last code byte at $C467: ${data[0xC467]:02X}")
print(f"  First free byte at $C468: ${data[0xC468]:02X}")

print()

# 4. Hook point verification
print("=== HOOK POINT at file 0x101E1 (bank2 CPU $81E1) ===")
off = 0x101E1
print(f"  0x{off:05X}: {data[off]:02X} {data[off+1]:02X} {data[off+2]:02X}  "
      f"{'CORRECT (FD 01 7B = STD $017B)' if data[off]==0xFD and data[off+1]==0x01 and data[off+2]==0x7B else 'WRONG!'}")

print()

# 5. Bank2 first instruction verification
print("=== BANK2 FIRST BYTES at file 0x10000 (CPU $8000) ===")
off = 0x10000
print(f"  0x{off:05X}: ", end="")
for i in range(32):
    print(f"{data[off+i]:02X} ", end="")
    if (i+1) % 16 == 0:
        print(f"\n  0x{off+i+1:05X}: ", end="")
print()

# 6. Bank3 first instruction verification  
print("=== BANK3 FIRST BYTES at file 0x18000 (CPU $8000) ===")
off = 0x18000
print(f"  0x{off:05X}: ", end="")
for i in range(32):
    print(f"{data[off+i]:02X} ", end="")
    if (i+1) % 16 == 0:
        print(f"\n  0x{off+i+1:05X}: ", end="")
print()

# 7. Verify vector targets point into jump table
print("=== VECTOR TARGET VALIDATION ===")
errors = 0
for i, name in enumerate(VECTOR_NAMES):
    addr = vec_start + i * 2
    hi = data[addr]
    lo = data[addr + 1]
    target = (hi << 8) | lo
    # All vectors should point into $2000-$202F range
    if 0x2000 <= target <= 0x202F:
        # Check that target address contains JMP ($7E)
        if data[target] == 0x7E:
            pass  # OK
        else:
            print(f"  WARNING: {name} -> ${target:04X} does NOT contain JMP (found ${data[target]:02X})")
            errors += 1
    else:
        print(f"  WARNING: {name} -> ${target:04X} is OUTSIDE jump table range $2000-$202F")
        errors += 1

if errors == 0:
    print("  ALL vectors correctly point into jump table and targets contain JMP")
else:
    print(f"  {errors} vector target issues found!")

print()

# 8. Spot-check bank2 disassembly at $8000
# Expected from .asm: L8000: 13 29 80 1D  brclr $29, #$80, $8021
print("=== SPOT-CHECK: Bank2 $8000 instruction decode ===")
off = 0x10000
b0, b1, b2, b3 = data[off], data[off+1], data[off+2], data[off+3]
print(f"  Bytes: ${b0:02X} ${b1:02X} ${b2:02X} ${b3:02X}")
if b0 == 0x13:
    # BRCLR direct: opcode, addr, mask, rel_offset (4 bytes total)
    target_addr = off + 4 + (b3 if b3 < 128 else b3 - 256)
    cpu_target = 0x8000 + (target_addr - 0x10000)
    print(f"  BRCLR ${b1:02X}, #${b2:02X}, ${cpu_target:04X}  (4 bytes)")
    # The .asm says: brclr $29, #-128, $8021
    # #-128 = #$80 — this is a SIGNED display issue
    print(f"  .asm shows mask as signed: #{b2-256 if b2>127 else b2}")
    print(f"  Correct unsigned mask: #${b2:02X}")
else:
    print(f"  Expected BRCLR ($13) but got ${b0:02X}")

# 9. bank3 first instruction
print()
print("=== SPOT-CHECK: Bank3 $8000 instruction decode ===")
off = 0x18000
b0, b1, b2 = data[off], data[off+1], data[off+2]
print(f"  Bytes: ${b0:02X} ${b1:02X} ${b2:02X}")
if b0 == 0xCC:
    val = (b1 << 8) | b2
    print(f"  LDD #${val:04X} ({val})  (3 bytes) — CORRECT per .asm")
else:
    print(f"  Expected LDD ($CC) but got ${b0:02X}")

# 10. Check the pcmhacking.net string at $3FE2
print()
print("=== PCMHACKING.NET STRING at $3FE2 ===")
s = data[0x3FE2:0x4000]
try:
    txt = s.decode('ascii', errors='replace')
    print(f"  {repr(txt)}")
except:
    print(f"  Raw: {s.hex()}")
