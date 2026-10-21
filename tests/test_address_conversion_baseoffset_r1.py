"""Read-only, synthetic HC11/XDF base-offset regressions; no BIN writes."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


MODULE = (Path(__file__).resolve().parents[1]
          / "68hc11_disassembler_tool_for_vy_v6" / "core" / "address_conversion.py")
spec = importlib.util.spec_from_file_location("kingai_hc11_address_conversion", MODULE)
assert spec is not None and spec.loader is not None
import sys
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class XdfAddressOffsetRegression(unittest.TestCase):
    def test_vy_default_zero_remains_identity(self):
        converter = mod.AddressConverter(mod.VY_V6_128KB)
        self.assertEqual(converter.xdf_to_file(0x77DE), 0x77DE)
        self.assertEqual(converter.xdf_to_file(0x18000, xdf_base_offset=0), 0x18000)

    def test_explicit_zero_overrides_nonzero_bmw_default(self):
        converter = mod.AddressConverter(mod.BMW_512KB)
        self.assertEqual(converter.xdf_to_file(0x100), 0x48100)
        self.assertEqual(converter.xdf_to_file(0x100, xdf_base_offset=0), 0x100)

    def test_custom_instance_zero_overrides_factory_nonzero(self):
        converter = mod.AddressConverter(mod.BMW_512KB, custom_base_offset=0)
        self.assertEqual(converter.xdf_to_file(0x250), 0x250)

    def test_explicit_add_and_subtract_are_not_silently_reversed(self):
        converter = mod.AddressConverter(mod.VL_VN_32KB)
        self.assertEqual(converter.xdf_to_file(0x18000, xdf_base_offset=0x10000,
                                                xdf_subtract=1), 0x8000)
        self.assertEqual(converter.xdf_to_file(0x100, xdf_base_offset=0x20,
                                                xdf_subtract=0), 0x120)
        self.assertEqual(converter.xdf_to_file(0x100, xdf_subtract=0), 0x8100)

    def test_negative_translation_refuses_raw_fallback(self):
        converter = mod.AddressConverter(mod.VL_VN_32KB)
        with self.assertRaisesRegex(ValueError, "negative file offset"):
            converter.xdf_to_file(0x7000)
        with self.assertRaisesRegex(ValueError, "negative file offset"):
            converter.xdf_to_file(0x80, xdf_base_offset=0x100, xdf_subtract=1)

    def test_invalid_baseoffset_configuration_fails(self):
        converter = mod.AddressConverter(mod.VY_V6_128KB)
        with self.assertRaises(ValueError):
            converter.xdf_to_file(0x100, xdf_base_offset=-1)
        with self.assertRaises(ValueError):
            converter.xdf_to_file(0x100, xdf_base_offset=0x10, xdf_subtract=2)


if __name__ == "__main__":
    unittest.main()
