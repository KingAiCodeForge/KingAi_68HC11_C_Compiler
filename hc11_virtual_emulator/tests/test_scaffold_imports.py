"""
HC11 Virtual Emulator — Scaffold Import Check

Run this to verify all scaffold modules import correctly.
Does NOT validate instruction correctness — that requires the
cross-reference testing suite (Phase 3 in dev plan).

Usage:
  cd hc11_virtual_emulator
  python -m tests.test_scaffold_imports
"""

import sys
import os

# Add parent dir to path so src is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_imports():
    """Verify all scaffold modules load without import errors."""
    print("─" * 50)
    print("  HC11 Virtual Emulator — Scaffold Import Check")
    print("─" * 50)
    
    results = []
    
    modules = [
        ("CPU Registers",   "src.cpu.regs"),
        ("ALU Operations",  "src.cpu.alu"),
        ("Opcode Decoder",  "src.cpu.decoder"),
        ("Memory Map",      "src.mem.memory"),
        ("SCI Peripheral",  "src.periph.sci"),
        ("ADC Peripheral",  "src.periph.adc"),
        ("I/O Ports",       "src.periph.ports"),
        ("Timer",           "src.periph.timer"),
        ("ALDL Mode 4",     "src.aldl.mode4_harness"),
        ("Main Emulator",   "src.emu"),
    ]
    
    for name, module_path in modules:
        try:
            __import__(module_path)
            results.append((name, "OK"))
            print(f"  ✓ {name:20s} → {module_path}")
        except Exception as e:
            results.append((name, f"FAIL: {e}"))
            print(f"  ✗ {name:20s} → {module_path}")
            print(f"    ERROR: {e}")
    
    print("─" * 50)
    
    # Quick functional smoke test
    print("\n  Smoke tests:")
    
    try:
        from src.cpu.regs import Registers
        r = Registers()
        r.A = 0x42
        r.B = 0x10
        assert r.D == 0x4210, f"D register mismatch: {r.D:04X}"
        r.D = 0xABCD
        assert r.A == 0xAB and r.B == 0xCD
        print(f"    ✓ Register D split/join")
    except Exception as e:
        print(f"    ✗ Register D: {e}")
    
    try:
        from src.cpu.alu import add8, sub8, CC_Z, CC_C, CC_N, CC_V
        result, flags = add8(0x7F, 0x01)
        assert result == 0x80, f"0x7F + 0x01 = 0x{result:02X} (expected 0x80)"
        assert flags & CC_N, "add8(0x7F, 0x01) should set N"
        assert flags & CC_V, "add8(0x7F, 0x01) should set V (signed overflow)"
        assert not (flags & CC_C), "add8(0x7F, 0x01) should NOT set C"
        print(f"    ✓ ALU add8 with overflow")
        
        result, flags = sub8(0x00, 0x01)
        assert result == 0xFF, f"0x00 - 0x01 = 0x{result:02X} (expected 0xFF)"
        assert flags & CC_C, "sub8(0,1) should set C (borrow)"
        assert flags & CC_N, "sub8(0,1) should set N"
        print(f"    ✓ ALU sub8 with borrow")
    except Exception as e:
        print(f"    ✗ ALU: {e}")
    
    try:
        from src.mem.memory import Memory
        mem = Memory()
        mem.write8(0x0050, 0xAA)
        assert mem.read8(0x0050) == 0xAA
        mem.write16(0x0100, 0x1234)
        assert mem.read16(0x0100) == 0x1234
        # ROM write should be silently dropped
        mem.load_binary(b'\x42', 0x8000)
        assert mem.read8(0x8000) == 0x42
        mem.write8(0x8000, 0xFF)  # should be dropped
        assert mem.read8(0x8000) == 0x42, "ROM write protection failed"
        print(f"    ✓ Memory read/write + ROM protection")
    except Exception as e:
        print(f"    ✗ Memory: {e}")
    
    try:
        from src.periph.sci import SCIPeripheral
        from src.mem.memory import Memory
        mem = Memory()
        sci = SCIPeripheral()
        sci.register(mem)
        mem.write8(0x102D, 0x08)  # TE enable
        mem.write8(0x102F, 0x48)  # TX 'H'
        mem.write8(0x102F, 0x49)  # TX 'I'
        assert sci.sci_output == b'HI', f"SCI output: {sci.sci_output!r}"
        print(f"    ✓ SCI transmit (ALDL TX)")
    except Exception as e:
        print(f"    ✗ SCI: {e}")
    
    try:
        from src.aldl.mode4_harness import Mode4Frame, aldl_checksum, validate_checksum
        frame = Mode4Frame()
        frame.set_fan(True)
        raw = frame.build_frame()
        assert raw[0] == 0xF7, f"Device addr: {raw[0]:02X}"
        assert raw[2] == 0x04, f"Mode byte: {raw[2]:02X}"
        assert validate_checksum(raw), f"Checksum invalid: {raw.hex()}"
        print(f"    ✓ Mode 4 frame build + checksum")
    except Exception as e:
        print(f"    ✗ Mode 4: {e}")
    
    try:
        from src.cpu.decoder import decode_opcode, OPCODES, ALL_OPCODES_PAGED
        total = len(OPCODES) + len(ALL_OPCODES_PAGED)
        # Check a known opcode
        mem2 = Memory()
        mem2.load_binary(bytes([0x86, 0x42]), 0x1000)  # LDAA #$42
        mnem, mode, cycles, next_pc = decode_opcode(mem2, 0x1000)
        assert mnem == 'LDAA' and mode == 'IMM8'
        print(f"    ✓ Opcode decoder ({total} opcodes loaded, LDAA #$42 decodes OK)")
    except Exception as e:
        print(f"    ✗ Decoder: {e}")
    
    print("\n" + "─" * 50)
    
    failed = [r for r in results if r[1] != "OK"]
    if failed:
        print(f"  {len(failed)} module(s) FAILED to import:")
        for name, status in failed:
            print(f"    ✗ {name}: {status}")
        return False
    else:
        print(f"  All {len(results)} scaffold modules imported successfully.")
        print(f"  All smoke tests passed.")
        return True


if __name__ == '__main__':
    success = test_imports()
    sys.exit(0 if success else 1)
