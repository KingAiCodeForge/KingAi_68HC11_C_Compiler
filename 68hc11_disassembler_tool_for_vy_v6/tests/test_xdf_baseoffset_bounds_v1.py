"""Synthetic-only XDF offset admission tests; not proof of ECU bank layout."""
import importlib.util
from pathlib import Path
import sys
import pytest

TARGET = Path(__file__).resolve().parents[1] / "core" / "address_conversion.py"
if not TARGET.exists():
    TARGET = Path(__file__).resolve().parents[1] / "core" / "address_contract_local.py"
spec = importlib.util.spec_from_file_location("address_conversion", TARGET)
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)


def converter(size=0x20000, base=0, subtract=0):
    if hasattr(m, "VY_V6_128KB"):
        return m.AddressConverter(m.BinaryFormat("test", size, 0, 0, 0, 0, base, subtract))
    return m.AddressConverter(m.BinaryFormat(size, base, subtract))


def test_unbased_vy_full_image_bounds():
    c=converter()
    assert c.xdf_to_file(0)==0
    assert c.xdf_to_file(0x77DE)==0x77DE
    assert c.xdf_to_file(0x1FFFF)==0x1FFFF
    with pytest.raises(ValueError,match="outside"):c.xdf_to_file(0x20000)


def test_negative_base_subtract_never_falls_back():
    c=converter(size=0x40000,base=0x30000,subtract=1)
    assert c.xdf_to_file(0x31000)==0x1000
    with pytest.raises(ValueError,match="outside"):c.xdf_to_file(0x77DE)


def test_explicit_zero_base_overrides_format():
    c=converter(size=0x40000,base=0x30000,subtract=1)
    assert c.xdf_to_file(0x77DE,xdf_base_offset=0,xdf_subtract=0)==0x77DE
    assert c.xdf_to_file(0x31000,xdf_base_offset=0,xdf_subtract=0)==0x31000


def test_bmw_additive_base():
    c=converter(size=0x80000,base=0x48000,subtract=0)
    assert c.xdf_to_file(0x1000)==0x49000
    with pytest.raises(ValueError,match="outside"):c.xdf_to_file(0x40000)


@pytest.mark.parametrize("args",[
    (-1,0,0),(0,-1,0),(0,0,2),(0,0,-1),(True,0,0),
    (0,True,0),(0,0,False),(0,0,1.2),('0x12',0,0)
])
def test_invalid_address_base_and_flag_rejected(args):
    with pytest.raises(ValueError):converter().xdf_to_file(*args)


def test_no_mutation_or_file_io_required(tmp_path):
    c=converter()
    assert c.xdf_to_file(0xFF)==0xFF
    assert not list(tmp_path.iterdir())
