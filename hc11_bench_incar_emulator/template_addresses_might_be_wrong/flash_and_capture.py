"""
Flash & Capture Pipeline — Phase 3+
======================================

Automated pipeline:
  compile C source → assemble → patch into bin → flash to PCM → capture ALDL output

This is the integration script that ties together:
  - hc11kit.py (compiler)
  - S-record / binary tools
  - Flash tool (PCMHammer / OSEFlashTool via CLI)
  - ALDL bridge (aldl_bridge.py)

⚠ PINOUT NOTE: Flashing uses the same ALDL serial connection as Mode 4.
   No additional PCM pins needed beyond the ALDL bridge wiring.
   However, flash operations write to the PCM's EEPROM/Flash — this is
   irreversible (unless you reflash stock). Use with caution.

⚠ STATUS: This is a template/scaffold. The actual flash tool integration
   depends on which tool is available (PCMHammer, OSEFlashTool, or custom).

Usage:
  python flash_and_capture.py --source hello.c --port COM3
  python flash_and_capture.py --binary hello.bin --port COM3 --capture
  python flash_and_capture.py --compare bench_output.json emu_output.json
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from aldl_bridge import ALDLBridge
from aldl_frame import hex_dump


# =============================================================================
#  CONFIGURATION
# =============================================================================

# Path to the compiler toolkit (adjust for your setup)
# ⚠ These paths are placeholders — update to match your environment
COMPILER_PATH = Path("../../hc11_compiler/hc11kit.py")
ASSEMBLER_PATH = Path("../../hc11_compiler/assembler.py")

# Flash tool — one of these should be available
FLASH_TOOLS = {
    "pcmhammer": {
        "exe": "PCMHammer.exe",           # ⚠ PLACEHOLDER path
        "args_read": ["--read", "--port", "{port}", "--output", "{output}"],
        "args_write": ["--write", "--port", "{port}", "--input", "{input}"],
    },
    "oseflash": {
        "exe": "OSEFlashTool.exe",        # ⚠ PLACEHOLDER path
        "args_read": ["/r", "/p:{port}", "/o:{output}"],
        "args_write": ["/w", "/p:{port}", "/i:{input}"],
    },
    "custom": {
        "exe": "python",
        "args_read": ["flash_tool.py", "read", "--port", "{port}", "--output", "{output}"],
        "args_write": ["flash_tool.py", "write", "--port", "{port}", "--input", "{input}"],
    },
}

# Target addresses in the $060A binary
PATCH_BASE_ADDRESS = 0x5D00    # Start of free space for custom code
CALIBRATION_ID = "$060A"


# =============================================================================
#  PIPELINE STEPS
# =============================================================================

class FlashAndCapture:
    """Automated compile → flash → capture pipeline."""

    def __init__(self, port: str, flash_tool: str = "custom", verbose: bool = False):
        self.port = port
        self.flash_tool = flash_tool
        self.verbose = verbose
        self.log: list[dict] = []

    def _log_step(self, step: str, status: str, message: str = ""):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "step": step,
            "status": status,
            "message": message,
        }
        self.log.append(entry)
        icon = "✓" if status == "ok" else "✗" if status == "error" else "…"
        print(f"  {icon} [{step}] {message}")

    # -------------------------------------------------------------------------
    #  Step 1: Compile C source to assembly
    # -------------------------------------------------------------------------
    def compile_source(self, source_path: str, output_asm: Optional[str] = None) -> Optional[str]:
        """
        Compile C source to HC11 assembly using hc11kit.py.

        Returns path to generated .s file, or None on failure.
        """
        source = Path(source_path)
        if not source.exists():
            self._log_step("compile", "error", f"Source not found: {source}")
            return None

        if output_asm is None:
            output_asm = str(source.with_suffix(".s"))

        self._log_step("compile", "info", f"Compiling {source.name}...")

        try:
            cmd = [sys.executable, str(COMPILER_PATH), "compile", str(source),
                   "--output", output_asm]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                self._log_step("compile", "ok", f"Output: {output_asm}")
                return output_asm
            else:
                self._log_step("compile", "error", f"Compiler error:\n{result.stderr}")
                return None
        except FileNotFoundError:
            self._log_step("compile", "error",
                          f"Compiler not found at {COMPILER_PATH}. "
                          "Update COMPILER_PATH in flash_and_capture.py")
            return None
        except subprocess.TimeoutExpired:
            self._log_step("compile", "error", "Compilation timed out (30s)")
            return None

    # -------------------------------------------------------------------------
    #  Step 2: Assemble to binary
    # -------------------------------------------------------------------------
    def assemble(self, asm_path: str, output_bin: Optional[str] = None) -> Optional[str]:
        """
        Assemble HC11 assembly to binary.

        Returns path to generated .bin file, or None on failure.
        """
        asm = Path(asm_path)
        if not asm.exists():
            self._log_step("assemble", "error", f"Assembly file not found: {asm}")
            return None

        if output_bin is None:
            output_bin = str(asm.with_suffix(".bin"))

        self._log_step("assemble", "info", f"Assembling {asm.name}...")

        try:
            cmd = [sys.executable, str(ASSEMBLER_PATH), str(asm),
                   "--output", output_bin, "--format", "binary"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                size = Path(output_bin).stat().st_size
                self._log_step("assemble", "ok", f"Output: {output_bin} ({size} bytes)")
                return output_bin
            else:
                self._log_step("assemble", "error", f"Assembler error:\n{result.stderr}")
                return None
        except FileNotFoundError:
            self._log_step("assemble", "error",
                          f"Assembler not found at {ASSEMBLER_PATH}")
            return None
        except subprocess.TimeoutExpired:
            self._log_step("assemble", "error", "Assembly timed out (30s)")
            return None

    # -------------------------------------------------------------------------
    #  Step 3: Patch binary into calibration image
    # -------------------------------------------------------------------------
    def patch_binary(
        self,
        compiled_bin: str,
        base_image: str,
        output_image: str,
        patch_address: int = PATCH_BASE_ADDRESS,
    ) -> Optional[str]:
        """
        Patch compiled binary into a calibration image at the specified address.

        Args:
            compiled_bin: Path to compiled code binary
            base_image: Path to stock/base calibration binary ($060A)
            output_image: Path for the patched output image
            patch_address: Address in the image to insert compiled code

        Returns path to patched image, or None on failure.
        """
        self._log_step("patch", "info",
                       f"Patching {compiled_bin} into {base_image} at 0x{patch_address:04X}...")

        try:
            with open(base_image, "rb") as f:
                image = bytearray(f.read())

            with open(compiled_bin, "rb") as f:
                code = f.read()

            # Validate
            if patch_address + len(code) > len(image):
                self._log_step("patch", "error",
                              f"Code ({len(code)} bytes) doesn't fit at 0x{patch_address:04X} "
                              f"in image ({len(image)} bytes)")
                return None

            # Patch
            image[patch_address:patch_address + len(code)] = code

            # TODO: Recalculate checksum if needed
            # The $060A binary may have a checksum that needs updating after patching.
            # This is calibration-specific and needs to be implemented.

            with open(output_image, "wb") as f:
                f.write(image)

            self._log_step("patch", "ok",
                          f"Patched {len(code)} bytes at 0x{patch_address:04X} → {output_image}")
            return output_image

        except FileNotFoundError as e:
            self._log_step("patch", "error", f"File not found: {e}")
            return None
        except Exception as e:
            self._log_step("patch", "error", f"Patch failed: {e}")
            return None

    # -------------------------------------------------------------------------
    #  Step 4: Flash image to PCM
    # -------------------------------------------------------------------------
    def flash_to_pcm(self, image_path: str) -> bool:
        """
        Flash a binary image to the PCM.

        ⚠ THIS IS DESTRUCTIVE — the PCM's flash will be overwritten.
           Make sure you have a backup of the stock calibration!

        Returns True on success.
        """
        self._log_step("flash", "info", f"Flashing {image_path} to PCM on {self.port}...")

        if self.flash_tool not in FLASH_TOOLS:
            self._log_step("flash", "error", f"Unknown flash tool: {self.flash_tool}")
            return False

        tool = FLASH_TOOLS[self.flash_tool]

        # Build command
        args = [a.format(port=self.port, input=image_path) for a in tool["args_write"]]
        cmd = [tool["exe"]] + args

        self._log_step("flash", "info", f"Command: {' '.join(cmd)}")

        # ⚠ SAFETY CHECK
        print("\n  ⚠ ABOUT TO FLASH PCM — THIS OVERWRITES THE CALIBRATION!")
        print(f"    Image: {image_path}")
        print(f"    Port: {self.port}")
        confirm = input("    Type 'FLASH' to confirm: ").strip()

        if confirm != "FLASH":
            self._log_step("flash", "error", "Flash cancelled by user")
            return False

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                self._log_step("flash", "ok", "Flash complete")
                return True
            else:
                self._log_step("flash", "error", f"Flash failed:\n{result.stderr}")
                return False
        except FileNotFoundError:
            self._log_step("flash", "error", f"Flash tool not found: {tool['exe']}")
            return False
        except subprocess.TimeoutExpired:
            self._log_step("flash", "error", "Flash timed out (300s)")
            return False

    # -------------------------------------------------------------------------
    #  Step 5: Capture ALDL output
    # -------------------------------------------------------------------------
    def capture_aldl_output(
        self,
        duration_s: float = 10.0,
        output_file: Optional[str] = None,
    ) -> Optional[dict]:
        """
        Capture ALDL serial output from the PCM after flash.

        Args:
            duration_s: How long to capture (seconds)
            output_file: Optional JSON file to save captured data

        Returns dict with captured data, or None on failure.
        """
        self._log_step("capture", "info",
                       f"Capturing ALDL output for {duration_s}s on {self.port}...")

        bridge = ALDLBridge(port=self.port, verbose=self.verbose)
        if not bridge.connect():
            self._log_step("capture", "error", f"Cannot open {self.port}")
            return None

        captured = {
            "timestamp": datetime.now().isoformat(),
            "port": self.port,
            "duration_s": duration_s,
            "raw_bytes": [],
            "sci_output": "",
        }

        try:
            # Read raw bytes for the specified duration
            start = time.time()
            all_bytes = bytearray()

            while time.time() - start < duration_s:
                data = bridge.receive_response(max_bytes=256)
                if data:
                    all_bytes.extend(data)
                    # Try to decode as ASCII for SCI text output
                    try:
                        text = data.decode("ascii", errors="replace")
                        captured["sci_output"] += text
                    except Exception:
                        pass
                time.sleep(0.1)

            captured["raw_bytes"] = list(all_bytes)
            captured["byte_count"] = len(all_bytes)

            self._log_step("capture", "ok",
                          f"Captured {len(all_bytes)} bytes, "
                          f"SCI text: {captured['sci_output'][:80]!r}")

            if output_file:
                with open(output_file, "w") as f:
                    json.dump(captured, f, indent=2)
                self._log_step("capture", "ok", f"Saved to {output_file}")

            return captured

        finally:
            bridge.disconnect()

    # -------------------------------------------------------------------------
    #  Full pipeline
    # -------------------------------------------------------------------------
    def run_full_pipeline(
        self,
        source_path: str,
        base_image: str,
        capture_duration: float = 10.0,
    ) -> bool:
        """
        Run the complete compile → assemble → patch → flash → capture pipeline.

        Args:
            source_path: Path to C source file
            base_image: Path to stock $060A binary
            capture_duration: How long to capture ALDL output after flash

        Returns True if all steps succeed.
        """
        print(f"\n{'='*60}")
        print(f"Flash & Capture Pipeline")
        print(f"  Source: {source_path}")
        print(f"  Base:   {base_image}")
        print(f"  Port:   {self.port}")
        print(f"{'='*60}\n")

        stem = Path(source_path).stem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Step 1: Compile
        asm_path = self.compile_source(source_path)
        if not asm_path:
            return False

        # Step 2: Assemble
        bin_path = self.assemble(asm_path)
        if not bin_path:
            return False

        # Step 3: Patch
        output_image = f"{stem}_patched_{timestamp}.bin"
        patched = self.patch_binary(bin_path, base_image, output_image)
        if not patched:
            return False

        # Step 4: Flash
        if not self.flash_to_pcm(patched):
            return False

        # Step 5: Capture
        capture_file = f"{stem}_capture_{timestamp}.json"
        captured = self.capture_aldl_output(capture_duration, capture_file)
        if not captured:
            return False

        # Summary
        print(f"\n{'='*60}")
        print(f"Pipeline complete!")
        print(f"  Patched image: {output_image}")
        print(f"  Capture file:  {capture_file}")
        print(f"  SCI output:    {captured.get('sci_output', '')[:80]!r}")
        print(f"{'='*60}")

        # Export full pipeline log
        log_file = f"{stem}_pipeline_{timestamp}.json"
        with open(log_file, "w") as f:
            json.dump({
                "source": source_path,
                "base_image": base_image,
                "patched_image": output_image,
                "capture_file": capture_file,
                "steps": self.log,
                "captured": captured,
            }, f, indent=2)
        print(f"  Pipeline log:  {log_file}")

        return True


# =============================================================================
#  OUTPUT COMPARISON
# =============================================================================

def compare_outputs(bench_json: str, emulator_json: str) -> bool:
    """
    Compare bench capture against virtual emulator output.

    Loads both JSON files and checks for SCI output match.
    """
    print(f"\n=== Cross-Validation ===")
    print(f"  Bench:    {bench_json}")
    print(f"  Emulator: {emulator_json}\n")

    try:
        with open(bench_json) as f:
            bench = json.load(f)
        with open(emulator_json) as f:
            emu = json.load(f)
    except FileNotFoundError as e:
        print(f"  ✗ File not found: {e}")
        return False

    bench_sci = bench.get("sci_output", "")
    emu_sci = emu.get("sci_output", "")

    if bench_sci == emu_sci:
        print(f"  ✓ MATCH — SCI outputs are identical")
        print(f"    Output: {bench_sci[:80]!r}")
        return True
    else:
        print(f"  ✗ MISMATCH — outputs differ")
        print(f"    Bench:    {bench_sci[:80]!r}")
        print(f"    Emulator: {emu_sci[:80]!r}")

        # Show character-level diff
        min_len = min(len(bench_sci), len(emu_sci))
        for i in range(min_len):
            if bench_sci[i] != emu_sci[i]:
                print(f"    First difference at byte {i}: "
                      f"bench=0x{ord(bench_sci[i]):02X} vs emu=0x{ord(emu_sci[i]):02X}")
                break
        if len(bench_sci) != len(emu_sci):
            print(f"    Length difference: bench={len(bench_sci)} vs emu={len(emu_sci)}")

        return False


# =============================================================================
#  CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Flash & Capture Pipeline — compile → flash → verify",
        epilog="⚠ Flash operations are DESTRUCTIVE. Always keep a stock backup!"
    )

    sub = parser.add_subparsers(dest="command")

    # Full pipeline
    pipe = sub.add_parser("pipeline", help="Run full compile → flash → capture")
    pipe.add_argument("--source", required=True, help="C source file")
    pipe.add_argument("--base", required=True, help="Base calibration binary ($060A)")
    pipe.add_argument("--port", required=True, help="Serial port")
    pipe.add_argument("--duration", type=float, default=10.0, help="Capture duration (s)")
    pipe.add_argument("--flash-tool", default="custom", help="Flash tool to use")
    pipe.add_argument("--verbose", "-v", action="store_true")

    # Capture only
    cap = sub.add_parser("capture", help="Capture ALDL output only")
    cap.add_argument("--port", required=True, help="Serial port")
    cap.add_argument("--duration", type=float, default=10.0, help="Duration (s)")
    cap.add_argument("--output", type=str, default=None, help="Output JSON file")
    cap.add_argument("--verbose", "-v", action="store_true")

    # Compare outputs
    cmp = sub.add_parser("compare", help="Compare bench vs emulator output")
    cmp.add_argument("bench_json", help="Bench capture JSON")
    cmp.add_argument("emulator_json", help="Emulator output JSON")

    args = parser.parse_args()

    if args.command == "pipeline":
        fac = FlashAndCapture(port=args.port, flash_tool=args.flash_tool,
                              verbose=args.verbose)
        success = fac.run_full_pipeline(args.source, args.base, args.duration)
        sys.exit(0 if success else 1)

    elif args.command == "capture":
        fac = FlashAndCapture(port=args.port, verbose=args.verbose)
        result = fac.capture_aldl_output(args.duration, args.output)
        if result:
            print(f"\nCaptured {result['byte_count']} bytes")
            if result["sci_output"]:
                print(f"SCI output: {result['sci_output']}")
        sys.exit(0 if result else 1)

    elif args.command == "compare":
        match = compare_outputs(args.bench_json, args.emulator_json)
        sys.exit(0 if match else 1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
