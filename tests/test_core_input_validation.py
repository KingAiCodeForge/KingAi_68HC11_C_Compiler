"""Malformed object/resource inputs must fail before assembly or allocation."""
import copy
import pytest

from hc11_compiler import compile_object, compile_source, compile_asm_object, link_objects
from hc11_compiler.linker import LinkError
from hc11_compiler.objectfile import RelocatableObject, ObjectFormatError
from hc11_compiler.resource_map import ResourceMap, ResourceMapError, MemoryRegion
from hc11_compiler.lexer import Lexer
from hc11_compiler.lexer import LexerError, Preprocessor
from hc11_compiler.parser import Parser, ParseError
from hc11_compiler.assembler import Assembler, AssemblerError


@pytest.mark.parametrize("field,value", [
    ("version", True), ("module", "../escape"), ("module", None),
    ("assembly", 123), ("exports", {}), ("imports", None),
    ("resources", [{}]), ("source_sha256", "not a digest"),
    ("exports", [{"name": "f", "kind": "invalid"}]),
])
def test_malformed_k11o_rejected(field, value):
    data = compile_object("void f() {}", module_name="sample").to_dict()
    data[field] = value
    original = copy.deepcopy(data)
    with pytest.raises(ObjectFormatError):
        RelocatableObject.from_dict(data)
    assert data == original


@pytest.mark.parametrize("value", [True, 1.5, None, []])
def test_resource_size_has_no_lossy_coercion(value):
    data = ResourceMap.default_for_target("generic").to_dict()
    data["allocations"] = [{"name": "bad", "kind": "zp", "start": 0x40, "size": value}]
    with pytest.raises(ResourceMapError):
        ResourceMap.from_dict(data)


@pytest.mark.parametrize("alignment", [0, -1, True, 1.5])
def test_programmatic_alignment_rejected(alignment):
    with pytest.raises(ResourceMapError):
        ResourceMap.default_for_target("generic").find_free("zp", 1, alignment)


def test_grouped_scalar_and_array_declarations_keep_independent_types():
    source = "void f() { unsigned char a[3], b; b = 2; a[0] = b; }"
    program = Parser(Lexer(source).tokenize(), source).parse()
    group = program.declarations[0].body.statements[0]
    assert group.statements[0].ctype.array_len == 3
    assert group.statements[1].ctype.array_len is None
    assert compile_source(source, output="binary")


def test_ambiguous_pointer_group_fails_closed():
    with pytest.raises(ParseError, match="Separate pointer"):
        compile_source("void f() { int *a, b; }")


@pytest.mark.parametrize("directive", ['#include "missing.h"', '#if 0', '#ifdef FEATURE', '#pragma unknown', '#define F(x) (x)'])
def test_unsupported_preprocessor_directives_do_not_disappear(directive):
    with pytest.raises(LexerError, match="preprocessor"):
        compile_source(directive + "\nvoid f() {}")


def test_macro_expansion_preserves_quoted_literals_and_supports_undef():
    result = Preprocessor('#define A 7\n#define B A\nchar x = B;\nasm("A B");\n#undef A\nchar y = A;').process()
    assert "char x = 7;" in result
    assert 'asm("A B");' in result
    assert "char y = A;" in result


def test_all_requested_and_region_alignment_constraints_are_satisfied():
    resource_map = ResourceMap(regions=[MemoryRegion("r", "ram", 1, 100, 4)])
    address = resource_map.find_free("ram", 1, 3)
    assert address == 12 and address % 3 == address % 4 == 0


@pytest.mark.parametrize("value", [True, 1.9])
def test_programmatic_asm_resource_request_is_validated(value):
    with pytest.raises(ObjectFormatError, match="resource"):
        compile_asm_object("f: RTS", module_name="m", resources=[{"name": "buf", "kind": "ram", "size": value}])


def test_mutated_programmatic_object_cannot_bypass_link_admission():
    obj = compile_object("void f() {}", module_name="m")
    obj.resources = [{"name": "buf", "kind": "ram", "size": 1.9}]
    with pytest.raises(LinkError, match="Invalid object"):
        link_objects([obj])


@pytest.mark.parametrize("kwargs", [{"module_name": ""}, {"module_name": "m", "target": "unknown"}])
def test_programmatic_asm_module_contract_validated(kwargs):
    with pytest.raises(ObjectFormatError):
        compile_asm_object("f: RTS", **kwargs)


@pytest.mark.parametrize("field,value", [("reserved", "false"), ("name", None), ("kind", [])])
def test_resource_metadata_keeps_strict_types(field, value):
    data = ResourceMap.default_for_target("generic").to_dict()
    allocation = {"name": "ok", "kind": "zp", "start": 0x40, "size": 1}
    allocation[field] = value
    data["allocations"] = [allocation]
    with pytest.raises(ResourceMapError):
        ResourceMap.from_dict(data)


@pytest.mark.parametrize("source", ["        ORG $10000", "        ORG -1", "        ORG $FFFF\n        FDB 1", "        ORG $8000\n        FCB 1\n        ORG $8000\n        FCB 2"])
def test_assembler_rejects_address_wrap_and_overlapping_segments(source):
    with pytest.raises(AssemblerError):
        Assembler().assemble(source)


def test_last_address_single_byte_allowed_and_reused_assembler_clears_occupancy():
    assembler = Assembler()
    assert assembler.assemble("        ORG $FFFF\n        RTS") == bytes([0x39])
    assert assembler.assemble("        ORG $FFFF\n        NOP") == bytes([0x01])
