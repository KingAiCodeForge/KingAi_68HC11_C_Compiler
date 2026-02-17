"""
Mode 4 Bench Test Harness
==========================

Structured test suite for Mode 4 actuator commands over ALDL.
Each test sends a specific Mode 4 frame and validates the PCM's response.

Test categories:
  - Discrete outputs (fan, CEL, fuel pump, A/C)
  - Engine overrides (spark, AFR, IAC)
  - Injector kill (power balance)
  - DTC clear
  - Extended actuator tests (Mode $6F)

⚠ PINOUT NOTE: Mode 4 byte offsets and bit assignments are from the
   VX-VY Mode 4 definition (pcmhacking.net topic 2460) and may need
   verification against the actual $060A calibration. See bench_config.py.

⚠ SAFETY: Mode 4 commands actuate real relays and override engine functions.
   Only run on bench or with engine off unless you understand the risks.

Usage:
  python mode4_bench_tester.py --port COM3 --test fan_high_on
  python mode4_bench_tester.py --port COM3 --test all --log results.json
  python mode4_bench_tester.py --port COM3 --list
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Optional

from aldl_bridge import ALDLBridge
from aldl_frame import (
    build_clear_dtcs,
    build_mode4_afr_override,
    build_mode4_discrete,
    build_mode4_iac_override,
    build_mode4_injector_kill,
    build_mode4_spark_override,
    hex_dump,
)


@dataclass
class TestResult:
    """Result of a single bench test."""
    name: str
    description: str
    passed: Optional[bool] = None  # None = not yet run
    response_hex: str = ""
    notes: str = ""
    timestamp: str = ""
    duration_ms: float = 0.0

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "passed": self.passed,
            "response_hex": self.response_hex,
            "notes": self.notes,
            "timestamp": self.timestamp,
            "duration_ms": self.duration_ms,
        }


@dataclass
class BenchTest:
    """Definition of a bench test case."""
    name: str
    description: str
    category: str
    safety: str  # "safe", "caution", "danger"
    run: Callable  # Function that executes the test
    requires_engine: bool = False


class Mode4BenchTester:
    """Runs structured Mode 4 tests against a real PCM over ALDL."""

    def __init__(self, bridge: ALDLBridge):
        self.bridge = bridge
        self.results: list[TestResult] = []
        self.tests: dict[str, BenchTest] = {}
        self._register_tests()

    def _register_tests(self):
        """Register all available test cases."""

        # --- Discrete output tests ---
        self.tests["fan_low_on"] = BenchTest(
            name="fan_low_on",
            description="Turn fan low relay ON via Mode 4",
            category="discrete",
            safety="safe",
            run=lambda: self._test_discrete(fan_low=True),
        )
        self.tests["fan_high_on"] = BenchTest(
            name="fan_high_on",
            description="Turn fan high relay ON via Mode 4",
            category="discrete",
            safety="safe",
            run=lambda: self._test_discrete(fan_high=True),
        )
        self.tests["cel_on"] = BenchTest(
            name="cel_on",
            description="Turn check engine lamp ON via Mode 4",
            category="discrete",
            safety="safe",
            run=lambda: self._test_discrete(cel=True),
        )
        self.tests["fuel_pump_on"] = BenchTest(
            name="fuel_pump_on",
            description="Turn fuel pump relay ON via Mode 4",
            category="discrete",
            safety="safe",
            run=lambda: self._test_discrete(fuel_pump=True),
        )
        self.tests["ac_clutch_on"] = BenchTest(
            name="ac_clutch_on",
            description="Turn A/C compressor clutch relay ON via Mode 4",
            category="discrete",
            safety="safe",
            run=lambda: self._test_discrete(ac_clutch=True),
        )
        self.tests["all_discrete_off"] = BenchTest(
            name="all_discrete_off",
            description="All discrete outputs OFF (baseline)",
            category="discrete",
            safety="safe",
            run=lambda: self._test_discrete(),
        )

        # --- Engine override tests ---
        self.tests["spark_15"] = BenchTest(
            name="spark_15",
            description="Override spark advance to 15° BTDC",
            category="engine",
            safety="caution",
            run=lambda: self._test_spark(15.0),
            requires_engine=True,
        )
        self.tests["spark_10"] = BenchTest(
            name="spark_10",
            description="Override spark advance to 10° BTDC",
            category="engine",
            safety="caution",
            run=lambda: self._test_spark(10.0),
            requires_engine=True,
        )
        self.tests["afr_stoich"] = BenchTest(
            name="afr_stoich",
            description="Override AFR to stoich (14.7:1)",
            category="engine",
            safety="caution",
            run=lambda: self._test_afr(14.7),
            requires_engine=True,
        )
        self.tests["iac_1000"] = BenchTest(
            name="iac_1000",
            description="Override IAC to ~1000 RPM position (0xA0)",
            category="engine",
            safety="caution",
            run=lambda: self._test_iac(0xA0),
            requires_engine=True,
        )

        # --- Injector kill tests ---
        self.tests["kill_cyl1"] = BenchTest(
            name="kill_cyl1",
            description="Kill injector 1 (power balance test)",
            category="injector",
            safety="caution",
            run=lambda: self._test_injector_kill([1]),
            requires_engine=True,
        )
        self.tests["kill_cyl1_3"] = BenchTest(
            name="kill_cyl1_3",
            description="Kill injectors 1 and 3",
            category="injector",
            safety="caution",
            run=lambda: self._test_injector_kill([1, 3]),
            requires_engine=True,
        )

        # --- DTC tests ---
        self.tests["clear_dtcs"] = BenchTest(
            name="clear_dtcs",
            description="Clear all diagnostic trouble codes",
            category="dtc",
            safety="safe",
            run=self._test_clear_dtcs,
        )

        # --- Read-only tests ---
        self.tests["mode1_read"] = BenchTest(
            name="mode1_read",
            description="Read Mode 1 data stream (read-only, safe)",
            category="read",
            safety="safe",
            run=self._test_mode1_read,
        )

    # =========================================================================
    #  TEST IMPLEMENTATIONS
    # =========================================================================

    def _test_discrete(self, **kwargs) -> TestResult:
        """Test discrete output control."""
        frame = build_mode4_discrete(**kwargs)
        enabled = [k for k, v in kwargs.items() if v]
        desc = f"Discrete: {', '.join(enabled) if enabled else 'all OFF'}"

        result = TestResult(
            name=f"discrete_{'+'.join(enabled) if enabled else 'off'}",
            description=desc,
            timestamp=datetime.now().isoformat(),
        )

        t0 = time.time()
        if self.bridge.send_frame(frame):
            resp = self.bridge.receive_response()
            result.duration_ms = (time.time() - t0) * 1000
            if resp:
                result.response_hex = hex_dump(resp)
                result.passed = True
                result.notes = "Response received — verify relay state manually"
            else:
                result.passed = False
                result.notes = "No response from PCM"
        else:
            result.passed = False
            result.notes = "Failed to send frame"

        return result

    def _test_spark(self, degrees: float) -> TestResult:
        """Test spark advance override."""
        frame = build_mode4_spark_override(degrees)

        result = TestResult(
            name=f"spark_{degrees:.0f}",
            description=f"Spark override to {degrees}° BTDC",
            timestamp=datetime.now().isoformat(),
        )

        t0 = time.time()
        if self.bridge.send_frame(frame):
            resp = self.bridge.receive_response()
            result.duration_ms = (time.time() - t0) * 1000
            if resp:
                result.response_hex = hex_dump(resp)
                result.passed = True
                result.notes = f"⚠ Verify spark advance reads {degrees}° on scan tool"
            else:
                result.passed = False
                result.notes = "No response from PCM"
        else:
            result.passed = False
            result.notes = "Failed to send frame"

        return result

    def _test_afr(self, afr: float) -> TestResult:
        """Test AFR override."""
        frame = build_mode4_afr_override(afr)

        result = TestResult(
            name=f"afr_{afr:.1f}",
            description=f"AFR override to {afr:.1f}:1",
            timestamp=datetime.now().isoformat(),
        )

        t0 = time.time()
        if self.bridge.send_frame(frame):
            resp = self.bridge.receive_response()
            result.duration_ms = (time.time() - t0) * 1000
            if resp:
                result.response_hex = hex_dump(resp)
                result.passed = True
                result.notes = f"⚠ Verify AFR on wideband reads ~{afr:.1f}"
            else:
                result.passed = False
                result.notes = "No response from PCM"
        else:
            result.passed = False
            result.notes = "Failed to send frame"

        return result

    def _test_iac(self, position: int) -> TestResult:
        """Test IAC position override."""
        frame = build_mode4_iac_override(position)

        result = TestResult(
            name=f"iac_{position:02X}",
            description=f"IAC override to position 0x{position:02X}",
            timestamp=datetime.now().isoformat(),
        )

        t0 = time.time()
        if self.bridge.send_frame(frame):
            resp = self.bridge.receive_response()
            result.duration_ms = (time.time() - t0) * 1000
            if resp:
                result.response_hex = hex_dump(resp)
                result.passed = True
                result.notes = "⚠ Verify idle RPM changes accordingly"
            else:
                result.passed = False
                result.notes = "No response from PCM"
        else:
            result.passed = False
            result.notes = "Failed to send frame"

        return result

    def _test_injector_kill(self, cylinders: list[int]) -> TestResult:
        """Test injector kill."""
        frame = build_mode4_injector_kill(cylinders)
        cyl_str = ",".join(str(c) for c in cylinders)

        result = TestResult(
            name=f"kill_cyl_{cyl_str}",
            description=f"Kill injector(s) for cylinder(s) {cyl_str}",
            timestamp=datetime.now().isoformat(),
        )

        t0 = time.time()
        if self.bridge.send_frame(frame):
            resp = self.bridge.receive_response()
            result.duration_ms = (time.time() - t0) * 1000
            if resp:
                result.response_hex = hex_dump(resp)
                result.passed = True
                result.notes = f"⚠ CAUTION: Cylinders {cyl_str} disabled — expect rough running"
            else:
                result.passed = False
                result.notes = "No response from PCM"
        else:
            result.passed = False
            result.notes = "Failed to send frame"

        return result

    def _test_clear_dtcs(self) -> TestResult:
        """Test DTC clearing."""
        frame = build_clear_dtcs()

        result = TestResult(
            name="clear_dtcs",
            description="Clear all DTCs",
            timestamp=datetime.now().isoformat(),
        )

        t0 = time.time()
        if self.bridge.send_frame(frame):
            resp = self.bridge.receive_response()
            result.duration_ms = (time.time() - t0) * 1000
            if resp:
                result.response_hex = hex_dump(resp)
                result.passed = True
                result.notes = "Verify DTCs cleared on subsequent Mode 1 read"
            else:
                result.passed = False
                result.notes = "No response from PCM"
        else:
            result.passed = False
            result.notes = "Failed to send frame"

        return result

    def _test_mode1_read(self) -> TestResult:
        """Test Mode 1 data stream read (safe, read-only)."""
        result = TestResult(
            name="mode1_read",
            description="Mode 1 data stream read",
            timestamp=datetime.now().isoformat(),
        )

        t0 = time.time()
        resp = self.bridge.read_mode1()
        result.duration_ms = (time.time() - t0) * 1000

        if resp:
            result.passed = True
            result.response_hex = resp.raw.hex(" ").upper() if resp.raw else ""
            result.notes = str(resp)
        else:
            result.passed = False
            result.notes = "No Mode 1 response"

        return result

    # =========================================================================
    #  TEST RUNNER
    # =========================================================================

    def run_test(self, name: str) -> TestResult:
        """Run a single named test."""
        if name not in self.tests:
            print(f"ERROR: Unknown test '{name}'. Use --list to see available tests.")
            return TestResult(name=name, description="Unknown test", passed=False)

        test = self.tests[name]
        print(f"\n[{test.safety.upper()}] {test.name}: {test.description}")

        if test.requires_engine:
            print("  ⚠ This test requires a running engine or simulated crank signals")

        result = test.run()
        self.results.append(result)

        status = "PASS" if result.passed else "FAIL" if result.passed is False else "SKIP"
        print(f"  → {status} ({result.duration_ms:.0f}ms) {result.notes}")

        return result

    def run_all_safe(self):
        """Run all tests marked as 'safe' (no engine required)."""
        safe_tests = [t for t in self.tests.values() if t.safety == "safe"]
        print(f"\n=== Running {len(safe_tests)} safe tests ===\n")

        for test_def in safe_tests:
            self.run_test(test_def.name)
            time.sleep(0.5)  # Brief pause between tests

        self._print_summary()

    def run_all(self):
        """Run ALL tests (including those requiring engine)."""
        print(f"\n=== Running ALL {len(self.tests)} tests ===")
        print("⚠ WARNING: Some tests actuate relays and override engine parameters!\n")

        for name in self.tests:
            self.run_test(name)
            time.sleep(0.5)

        self._print_summary()

    def _print_summary(self):
        """Print test results summary."""
        passed = sum(1 for r in self.results if r.passed is True)
        failed = sum(1 for r in self.results if r.passed is False)
        total = len(self.results)

        print(f"\n{'='*60}")
        print(f"Results: {passed}/{total} passed, {failed} failed")
        print(f"{'='*60}")

        if failed > 0:
            print("\nFailed tests:")
            for r in self.results:
                if r.passed is False:
                    print(f"  ✗ {r.name}: {r.notes}")

    def export_results(self, path: str):
        """Export test results to JSON."""
        data = {
            "run_date": datetime.now().isoformat(),
            "port": self.bridge.port,
            "total_tests": len(self.results),
            "passed": sum(1 for r in self.results if r.passed is True),
            "failed": sum(1 for r in self.results if r.passed is False),
            "results": [r.to_dict() for r in self.results],
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Results exported to {path}")

    def list_tests(self):
        """Print all available tests."""
        print("\nAvailable bench tests:\n")
        categories = {}
        for test in self.tests.values():
            categories.setdefault(test.category, []).append(test)

        for cat, tests in sorted(categories.items()):
            print(f"  [{cat.upper()}]")
            for t in tests:
                engine = " (needs engine)" if t.requires_engine else ""
                print(f"    {t.name:20s} [{t.safety:>7s}] {t.description}{engine}")
            print()


# =============================================================================
#  CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Mode 4 Bench Test Harness — VY V6 Delco PCM",
        epilog="⚠ Verify pinout and Mode 4 byte offsets before running actuator tests!"
    )
    parser.add_argument("--port", help="Serial port (e.g. COM3)")
    parser.add_argument("--test", type=str, default=None,
                        help="Test name to run (or 'all', 'safe')")
    parser.add_argument("--list", action="store_true",
                        help="List all available tests")
    parser.add_argument("--log", type=str, default=None,
                        help="Export results to JSON file")
    parser.add_argument("--verbose", "-v", action="store_true")

    args = parser.parse_args()

    if args.list:
        # Can list tests without a port
        bridge = ALDLBridge(port="dummy", verbose=False)
        tester = Mode4BenchTester(bridge)
        tester.list_tests()
        return

    if not args.port:
        print("ERROR: --port required (e.g. --port COM3)")
        sys.exit(1)

    bridge = ALDLBridge(port=args.port, verbose=args.verbose)
    if not bridge.connect():
        sys.exit(1)

    tester = Mode4BenchTester(bridge)

    try:
        if not bridge.enter_diagnostics():
            print("Cannot enter diagnostics mode. Check cable and PCM power.")
            sys.exit(1)

        if args.test == "all":
            tester.run_all()
        elif args.test == "safe":
            tester.run_all_safe()
        elif args.test:
            tester.run_test(args.test)
        else:
            print("No test specified. Use --test <name>, --test safe, --test all, or --list")

        if args.log and tester.results:
            tester.export_results(args.log)

    finally:
        bridge.disconnect()


if __name__ == "__main__":
    main()
