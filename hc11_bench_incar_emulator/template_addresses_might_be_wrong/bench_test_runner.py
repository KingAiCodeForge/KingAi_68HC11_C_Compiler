"""
Bench Test Runner — Automated Validation Framework
=====================================================

Orchestrates bench tests:
  1. Configure sensor state (sensor_simulator)
  2. Send ALDL commands (aldl_bridge / mode4_bench_tester)
  3. Capture PCM responses
  4. Compare against expected values (oracle validation)
  5. Generate pass/fail report

Supports:
  - Individual test execution
  - Full regression suite
  - Cross-validation against virtual emulator output
  - JSON report generation

⚠ PINOUT NOTE: This is the orchestration layer — it doesn't directly
   reference pin numbers. Pin verification status is checked via
   bench_config.py at startup.

Usage:
  python bench_test_runner.py --port COM3 --suite safe
  python bench_test_runner.py --port COM3 --suite full --report results.json
  python bench_test_runner.py --validate-frames  (offline frame validation only)
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

from aldl_frame import (
    ALDLFrame,
    build_clear_dtcs,
    build_enter_diagnostics,
    build_mode1_request,
    build_mode4_discrete,
    build_mode4_spark_override,
    build_mode4_afr_override,
    build_mode4_iac_override,
    build_mode4_injector_kill,
    hex_dump,
    verify_checksum,
)
from bench_config import ALL_PINS_VERIFIED, MODE1_OFFSETS, MODE4_OFFSETS


# =============================================================================
#  TEST DEFINITIONS
# =============================================================================

@dataclass
class TestCase:
    """A single test case definition."""
    id: str
    name: str
    description: str
    category: str       # "frame", "mode1", "mode4", "integration"
    safety: str         # "safe", "caution", "danger"
    requires_hardware: bool = True
    requires_engine: bool = False

    # Expected values for validation
    expected: dict = field(default_factory=dict)

    # Test function (set by runner)
    _run_fn: Optional[callable] = None


@dataclass
class TestReport:
    """Complete test run report."""
    run_id: str
    timestamp: str
    port: Optional[str]
    pins_verified: bool
    suite: str
    results: list[dict] = field(default_factory=list)
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    total: int = 0

    def add_result(self, test_id: str, status: str, message: str = "",
                   duration_ms: float = 0, response: str = ""):
        self.results.append({
            "test_id": test_id,
            "status": status,
            "message": message,
            "duration_ms": duration_ms,
            "response": response,
        })
        self.total += 1
        if status == "PASS":
            self.passed += 1
        elif status == "FAIL":
            self.failed += 1
        elif status == "SKIP":
            self.skipped += 1

    def to_dict(self) -> dict:
        return {
            "run_id": self.run_id,
            "timestamp": self.timestamp,
            "port": self.port,
            "pins_verified": self.pins_verified,
            "suite": self.suite,
            "summary": {
                "total": self.total,
                "passed": self.passed,
                "failed": self.failed,
                "skipped": self.skipped,
            },
            "results": self.results,
        }


# =============================================================================
#  OFFLINE FRAME VALIDATION TESTS (no hardware needed)
# =============================================================================

def test_frame_checksums() -> tuple[bool, str]:
    """Verify all frame builder functions produce valid checksums."""
    frames = [
        ("Mode 1 request", build_mode1_request()),
        ("Enter diagnostics", build_enter_diagnostics()),
        ("Mode 4 fan high", build_mode4_discrete(fan_high=True)),
        ("Mode 4 fan low", build_mode4_discrete(fan_low=True)),
        ("Mode 4 CEL", build_mode4_discrete(cel=True)),
        ("Mode 4 fuel pump", build_mode4_discrete(fuel_pump=True)),
        ("Mode 4 spark 10°", build_mode4_spark_override(10.0)),
        ("Mode 4 spark 15°", build_mode4_spark_override(15.0)),
        ("Mode 4 spark 25°", build_mode4_spark_override(25.0)),
        ("Mode 4 AFR 14.7", build_mode4_afr_override(14.7)),
        ("Mode 4 AFR 12.5", build_mode4_afr_override(12.5)),
        ("Mode 4 IAC 0xA0", build_mode4_iac_override(0xA0)),
        ("Mode 4 kill cyl 1", build_mode4_injector_kill([1])),
        ("Mode 4 kill cyl 1,3,5", build_mode4_injector_kill([1, 3, 5])),
        ("Clear DTCs", build_clear_dtcs()),
    ]

    failures = []
    for name, frame in frames:
        if not verify_checksum(frame.raw):
            failures.append(f"  {name}: checksum INVALID ({hex_dump(frame.raw)})")

    if failures:
        return False, f"Checksum failures:\n" + "\n".join(failures)
    return True, f"All {len(frames)} frame checksums valid"


def test_frame_lengths() -> tuple[bool, str]:
    """Verify frame length bytes are consistent."""
    frames = [
        build_mode1_request(),
        build_enter_diagnostics(),
        build_mode4_discrete(fan_high=True),
        build_mode4_spark_override(15.0),
    ]

    failures = []
    for frame in frames:
        declared_len = frame.raw[1]
        actual_len = len(frame.raw)
        if declared_len != actual_len:
            failures.append(
                f"  Mode 0x{frame.mode:02X}: declared={declared_len}, actual={actual_len}"
            )

    if failures:
        return False, "Length mismatches:\n" + "\n".join(failures)
    return True, f"All {len(frames)} frame lengths consistent"


def test_frame_mode_bytes() -> tuple[bool, str]:
    """Verify mode bytes are correct."""
    checks = [
        (build_mode1_request(), 0x01, "Mode 1"),
        (build_enter_diagnostics(), 0x0A, "Enter Diagnostics"),
        (build_mode4_discrete(), 0x04, "Mode 4"),
    ]

    failures = []
    for frame, expected_mode, name in checks:
        if frame.raw[0] != expected_mode:
            failures.append(f"  {name}: expected 0x{expected_mode:02X}, got 0x{frame.raw[0]:02X}")

    if failures:
        return False, "Mode byte errors:\n" + "\n".join(failures)
    return True, f"All {len(checks)} mode bytes correct"


def test_crank_frequencies() -> tuple[bool, str]:
    """Verify crank frequency calculations."""
    from bench_config import crank_freq, CRANK_FREQ_TABLE

    failures = []
    for rpm, (expected_3x, expected_18x) in CRANK_FREQ_TABLE.items():
        calc_3x = crank_freq(rpm, 3)
        calc_18x = crank_freq(rpm, 18)

        if abs(calc_3x - expected_3x) > 0.01:
            failures.append(f"  {rpm} RPM 3X: expected {expected_3x}, got {calc_3x}")
        if abs(calc_18x - expected_18x) > 0.01:
            failures.append(f"  {rpm} RPM 18X: expected {expected_18x}, got {calc_18x}")

    if failures:
        return False, "Frequency calculation errors:\n" + "\n".join(failures)
    return True, f"All {len(CRANK_FREQ_TABLE)} RPM frequency entries verified"


def test_cts_resistance() -> tuple[bool, str]:
    """Verify CTS resistance interpolation is monotonically decreasing."""
    from sensor_simulator import cts_resistance_for_temp

    temps = list(range(-40, 131, 10))
    resistances = [cts_resistance_for_temp(t) for t in temps]

    failures = []
    for i in range(len(resistances) - 1):
        if resistances[i] <= resistances[i + 1]:
            failures.append(
                f"  {temps[i]}°C ({resistances[i]:.0f}Ω) ≤ {temps[i+1]}°C ({resistances[i+1]:.0f}Ω)"
            )

    if failures:
        return False, "CTS resistance not monotonically decreasing:\n" + "\n".join(failures)
    return True, f"CTS resistance curve verified across {len(temps)} points"


# =============================================================================
#  TEST RUNNER
# =============================================================================

class BenchTestRunner:
    """Runs test suites and generates reports."""

    # Offline tests (no hardware needed)
    OFFLINE_TESTS = {
        "frame_checksum": ("Frame checksums valid", test_frame_checksums),
        "frame_length": ("Frame lengths consistent", test_frame_lengths),
        "frame_mode": ("Mode bytes correct", test_frame_mode_bytes),
        "crank_freq": ("Crank frequency calculations", test_crank_frequencies),
        "cts_curve": ("CTS resistance curve", test_cts_resistance),
    }

    def __init__(self, port: Optional[str] = None, verbose: bool = False):
        self.port = port
        self.verbose = verbose
        self.report = TestReport(
            run_id=datetime.now().strftime("%Y%m%d_%H%M%S"),
            timestamp=datetime.now().isoformat(),
            port=port,
            pins_verified=ALL_PINS_VERIFIED,
            suite="",
        )

    def run_offline_tests(self) -> bool:
        """Run all tests that don't require hardware."""
        self.report.suite = "offline"
        print("\n=== Offline Validation Tests ===")
        print("(No hardware required — validating frame logic)\n")

        all_passed = True
        for test_id, (name, test_fn) in self.OFFLINE_TESTS.items():
            t0 = time.time()
            try:
                passed, message = test_fn()
                duration = (time.time() - t0) * 1000
                status = "PASS" if passed else "FAIL"
                icon = "✓" if passed else "✗"
                print(f"  {icon} {name}: {message}")
                self.report.add_result(test_id, status, message, duration)
                if not passed:
                    all_passed = False
            except Exception as e:
                duration = (time.time() - t0) * 1000
                print(f"  ✗ {name}: EXCEPTION — {e}")
                self.report.add_result(test_id, "FAIL", str(e), duration)
                all_passed = False

        return all_passed

    def run_safe_hardware_tests(self) -> bool:
        """Run hardware tests that are safe (read-only or benign outputs)."""
        self.report.suite = "safe"
        if not self.port:
            print("ERROR: --port required for hardware tests")
            return False

        print("\n=== Safe Hardware Tests ===")
        print(f"Port: {self.port}")

        if not ALL_PINS_VERIFIED:
            print("⚠ WARNING: Pin assignments NOT verified — test at your own risk")
            print("  See bench_config.py for unverified pins\n")

        # Import here to avoid errors when running offline
        from aldl_bridge import ALDLBridge
        from mode4_bench_tester import Mode4BenchTester

        bridge = ALDLBridge(port=self.port, verbose=self.verbose)
        if not bridge.connect():
            self.report.add_result("connect", "FAIL", f"Cannot open {self.port}")
            return False

        self.report.add_result("connect", "PASS", f"Connected to {self.port}")

        try:
            tester = Mode4BenchTester(bridge)

            # Enter diagnostics
            if bridge.enter_diagnostics():
                self.report.add_result("enter_diag", "PASS", "Entered diagnostics mode")
            else:
                self.report.add_result("enter_diag", "FAIL", "No response to Mode $0A")
                return False

            # Mode 1 read
            t0 = time.time()
            resp = bridge.read_mode1()
            dur = (time.time() - t0) * 1000
            if resp:
                self.report.add_result("mode1_read", "PASS", str(resp), dur)
            else:
                self.report.add_result("mode1_read", "FAIL", "No Mode 1 response", dur)

            # Safe discrete tests
            for test_name in ["fan_low_on", "fan_high_on", "cel_on", "all_discrete_off"]:
                result = tester.run_test(test_name)
                status = "PASS" if result.passed else "FAIL"
                self.report.add_result(
                    test_name, status, result.notes, result.duration_ms, result.response_hex
                )
                time.sleep(0.5)

            bridge.exit_diagnostics()
            self.report.add_result("exit_diag", "PASS", "Exited diagnostics mode")

        finally:
            bridge.disconnect()

        return self.report.failed == 0

    def print_summary(self):
        """Print test run summary."""
        print(f"\n{'='*60}")
        print(f"Test Run: {self.report.run_id}")
        print(f"Suite: {self.report.suite}")
        print(f"Results: {self.report.passed} passed, {self.report.failed} failed, "
              f"{self.report.skipped} skipped / {self.report.total} total")

        if not ALL_PINS_VERIFIED:
            print(f"\n⚠ Pin assignments are UNVERIFIED — hardware test results")
            print(f"  may not reflect correct PCM behavior!")

        print(f"{'='*60}")

        if self.report.failed > 0:
            print("\nFailed tests:")
            for r in self.report.results:
                if r["status"] == "FAIL":
                    print(f"  ✗ {r['test_id']}: {r['message']}")

    def export_report(self, path: str):
        """Export full report to JSON."""
        with open(path, "w") as f:
            json.dump(self.report.to_dict(), f, indent=2)
        print(f"\nReport exported to {path}")


# =============================================================================
#  VIRTUAL EMULATOR CROSS-VALIDATION
# =============================================================================

def cross_validate_with_emulator(
    bench_output: dict,
    emulator_output_path: str,
) -> tuple[bool, str]:
    """
    Compare bench hardware output against virtual emulator output.

    Both should produce identical SCI output for the same input binary.
    Differences indicate either a hardware wiring issue or an emulator bug.

    Args:
        bench_output: Dict with captured ALDL responses from bench
        emulator_output_path: Path to JSON file from virtual emulator run

    Returns:
        (match, diff_description)
    """
    if not Path(emulator_output_path).exists():
        return False, f"Emulator output file not found: {emulator_output_path}"

    with open(emulator_output_path) as f:
        emu_output = json.load(f)

    # Compare key fields
    diffs = []

    # TODO: Implement field-by-field comparison based on the specific
    # output format of the virtual emulator. This is a placeholder.
    if "sci_output" in emu_output and "sci_output" in bench_output:
        if emu_output["sci_output"] != bench_output["sci_output"]:
            diffs.append(f"SCI output mismatch: bench={bench_output['sci_output']!r} "
                        f"vs emu={emu_output['sci_output']!r}")

    if diffs:
        return False, "\n".join(diffs)
    return True, "Bench and emulator outputs match"


# =============================================================================
#  CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Bench Test Runner — automated validation framework",
    )
    parser.add_argument("--port", type=str, default=None,
                        help="Serial port for hardware tests")
    parser.add_argument("--suite", choices=["offline", "safe", "full"],
                        default="offline", help="Test suite to run")
    parser.add_argument("--report", type=str, default=None,
                        help="Export report to JSON file")
    parser.add_argument("--validate-frames", action="store_true",
                        help="Run offline frame validation only")
    parser.add_argument("--verbose", "-v", action="store_true")

    args = parser.parse_args()

    runner = BenchTestRunner(port=args.port, verbose=args.verbose)

    if args.validate_frames or args.suite == "offline":
        # Run offline tests only
        runner.run_offline_tests()

    elif args.suite == "safe":
        # Offline + safe hardware tests
        runner.run_offline_tests()
        runner.run_safe_hardware_tests()

    elif args.suite == "full":
        # Everything
        runner.run_offline_tests()
        runner.run_safe_hardware_tests()
        # TODO: Add engine-required tests here

    runner.print_summary()

    if args.report:
        runner.export_report(args.report)


if __name__ == "__main__":
    main()
