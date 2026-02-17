"""
Unit tests for ALDL frame builder / parser.

These tests validate the protocol layer (framing, checksums, encoding)
without any hardware dependency. Run offline at any time.

Usage:
  python -m pytest tests/test_aldl_frame.py -v
  # or
  python tests/test_aldl_frame.py
"""

import sys
import os

# Add parent directory to path so we can import aldl_frame
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aldl_frame import (
    ALDLFrame,
    checksum,
    verify_checksum,
    build_mode1_request,
    build_enter_diagnostics,
    build_exit_diagnostics,
    build_mode4_frame,
    build_mode4_discrete,
    build_mode4_spark_override,
    build_mode4_afr_override,
    build_mode4_iac_override,
    build_mode4_injector_kill,
    build_clear_dtcs,
    parse_raw_frame,
    hex_dump,
)


# =============================================================================
#  CHECKSUM TESTS
# =============================================================================

def test_checksum_zero_data():
    """Checksum of empty payload is 0."""
    assert checksum(b"\x00") == 0

def test_checksum_single_byte():
    """Checksum of 0xFF should be 0x01."""
    assert checksum(b"\xFF") == 1

def test_checksum_basic():
    """Basic checksum calculation."""
    data = bytes([0x01, 0x03])  # Mode 1, length 3
    chk = checksum(data)
    assert (sum(data) + chk) & 0xFF == 0

def test_verify_checksum_valid():
    """Valid frame should pass verification."""
    frame = build_mode1_request()
    assert verify_checksum(frame.raw)

def test_verify_checksum_invalid():
    """Corrupted frame should fail verification."""
    frame = build_mode1_request()
    corrupted = bytearray(frame.raw)
    corrupted[-1] ^= 0xFF  # Flip checksum bits
    assert not verify_checksum(bytes(corrupted))


# =============================================================================
#  FRAME BUILDER TESTS
# =============================================================================

def test_mode1_request():
    """Mode 1 request frame structure."""
    frame = build_mode1_request()
    assert frame.mode == 0x01
    assert frame.raw[0] == 0x01  # Mode byte
    assert len(frame.raw) == frame.raw[1]  # Length consistency
    assert verify_checksum(frame.raw)

def test_enter_diagnostics():
    """Enter diagnostics frame structure."""
    frame = build_enter_diagnostics()
    assert frame.mode == 0x0A
    assert frame.raw[0] == 0x0A
    assert verify_checksum(frame.raw)

def test_exit_diagnostics():
    """Exit diagnostics frame structure."""
    frame = build_exit_diagnostics()
    assert frame.mode == 0x0F
    assert verify_checksum(frame.raw)

def test_mode4_frame_custom_payload():
    """Mode 4 with arbitrary payload."""
    payload = bytes([0x01, 0x02, 0x03, 0x04])
    frame = build_mode4_frame(payload)
    assert frame.mode == 0x04
    assert frame.raw[0] == 0x04
    assert frame.data == payload
    assert verify_checksum(frame.raw)

def test_mode4_discrete_fan_high():
    """Mode 4 fan high discrete control."""
    frame = build_mode4_discrete(fan_high=True)
    assert frame.mode == 0x04
    assert verify_checksum(frame.raw)
    # Data should contain non-zero byte for fan control
    assert len(frame.data) >= 5

def test_mode4_discrete_multiple():
    """Mode 4 multiple discrete outputs."""
    frame = build_mode4_discrete(fan_low=True, cel=True, fuel_pump=True)
    assert verify_checksum(frame.raw)

def test_mode4_discrete_all_off():
    """Mode 4 all discrete outputs off."""
    frame = build_mode4_discrete()
    assert verify_checksum(frame.raw)

def test_mode4_spark_override():
    """Mode 4 spark advance override."""
    for degrees in [0, 5, 10, 15, 20, 25, 30, 40]:
        frame = build_mode4_spark_override(float(degrees))
        assert verify_checksum(frame.raw), f"Checksum failed at {degrees}°"

def test_mode4_spark_override_clamping():
    """Spark override should clamp to valid byte range."""
    # Very large advance shouldn't crash
    frame = build_mode4_spark_override(100.0)
    assert verify_checksum(frame.raw)
    # Very retarded timing
    frame = build_mode4_spark_override(-50.0)
    assert verify_checksum(frame.raw)

def test_mode4_afr_override():
    """Mode 4 AFR override."""
    for afr in [10.0, 12.5, 14.7, 16.0]:
        frame = build_mode4_afr_override(afr)
        assert verify_checksum(frame.raw), f"Checksum failed at AFR {afr}"

def test_mode4_iac_override():
    """Mode 4 IAC position override."""
    for pos in [0, 64, 128, 160, 200, 255]:
        frame = build_mode4_iac_override(pos)
        assert verify_checksum(frame.raw), f"Checksum failed at IAC {pos}"

def test_mode4_iac_clamping():
    """IAC override should clamp to 0-255."""
    frame = build_mode4_iac_override(300)
    assert verify_checksum(frame.raw)
    frame = build_mode4_iac_override(-10)
    assert verify_checksum(frame.raw)

def test_mode4_injector_kill_single():
    """Kill single injector."""
    frame = build_mode4_injector_kill([1])
    assert verify_checksum(frame.raw)

def test_mode4_injector_kill_multiple():
    """Kill multiple injectors."""
    frame = build_mode4_injector_kill([1, 3, 5])
    assert verify_checksum(frame.raw)

def test_mode4_injector_kill_all():
    """Kill all 6 injectors."""
    frame = build_mode4_injector_kill([1, 2, 3, 4, 5, 6])
    assert verify_checksum(frame.raw)

def test_mode4_injector_kill_invalid():
    """Invalid cylinder numbers should be ignored."""
    frame = build_mode4_injector_kill([0, 7, 8])
    assert verify_checksum(frame.raw)

def test_clear_dtcs():
    """Clear DTCs frame."""
    frame = build_clear_dtcs()
    assert frame.mode == 0x04
    assert verify_checksum(frame.raw)


# =============================================================================
#  FRAME LENGTH TESTS
# =============================================================================

def test_frame_length_consistency():
    """All frames should have consistent length byte."""
    frames = [
        build_mode1_request(),
        build_enter_diagnostics(),
        build_exit_diagnostics(),
        build_mode4_discrete(fan_high=True),
        build_mode4_spark_override(15.0),
        build_mode4_afr_override(14.7),
        build_clear_dtcs(),
    ]
    for frame in frames:
        declared_len = frame.raw[1]
        actual_len = len(frame.raw)
        assert declared_len == actual_len, (
            f"Mode 0x{frame.mode:02X}: declared={declared_len}, actual={actual_len}"
        )


# =============================================================================
#  FRAME PARSER TESTS
# =============================================================================

def test_parse_valid_frame():
    """Parser should accept a valid frame."""
    original = build_mode1_request()
    parsed = parse_raw_frame(original.raw)
    assert parsed is not None
    assert parsed.mode == 0x01

def test_parse_invalid_checksum():
    """Parser should reject frame with bad checksum."""
    frame = build_mode1_request()
    corrupted = bytearray(frame.raw)
    corrupted[-1] ^= 0xFF
    parsed = parse_raw_frame(bytes(corrupted))
    assert parsed is None

def test_parse_too_short():
    """Parser should reject frames shorter than 3 bytes."""
    assert parse_raw_frame(b"\x01") is None
    assert parse_raw_frame(b"\x01\x02") is None

def test_parse_wrong_length():
    """Parser should reject frame with mismatched length byte."""
    frame = build_mode1_request()
    bad = bytearray(frame.raw)
    bad[1] = 99  # Wrong length
    # Recalculate checksum for the corrupted frame
    bad[-1] = checksum(bytes(bad[:-1]))
    parsed = parse_raw_frame(bytes(bad))
    assert parsed is None  # Length mismatch


# =============================================================================
#  UTILITY TESTS
# =============================================================================

def test_hex_dump():
    """Hex dump formatting."""
    result = hex_dump(b"\x01\x02\x03", prefix="TX: ")
    assert "01 02 03" in result
    assert "TX: " in result
    assert "[3 bytes]" in result

def test_aldl_frame_repr():
    """Frame repr should be readable."""
    frame = build_mode1_request()
    r = repr(frame)
    assert "0x01" in r
    assert "ALDLFrame" in r


# =============================================================================
#  CRANK FREQUENCY TESTS (from bench_config)
# =============================================================================

def test_crank_freq():
    """Crank frequency calculation."""
    from bench_config import crank_freq
    assert abs(crank_freq(800, 3) - 40.0) < 0.01
    assert abs(crank_freq(800, 18) - 240.0) < 0.01
    assert abs(crank_freq(1000, 3) - 50.0) < 0.01
    assert abs(crank_freq(6000, 18) - 1800.0) < 0.01

def test_crank_freq_zero():
    """Zero RPM should give zero frequency."""
    from bench_config import crank_freq
    assert crank_freq(0, 3) == 0.0


# =============================================================================
#  RUN
# =============================================================================

if __name__ == "__main__":
    # Simple test runner for running without pytest
    import inspect

    tests = [(name, obj) for name, obj in globals().items()
             if name.startswith("test_") and callable(obj)]

    passed = 0
    failed = 0

    print(f"\nRunning {len(tests)} tests...\n")

    for name, test_fn in sorted(tests):
        try:
            test_fn()
            print(f"  ✓ {name}")
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ {name}: EXCEPTION — {e}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed / {len(tests)} total")
    print(f"{'='*50}")

    sys.exit(1 if failed > 0 else 0)
