"""Software-only tests for arrays/structs, K11O objects and KCOS linking."""

import pytest

from hc11_compiler import (
    ResourceMap,
    compile_object,
    compile_source,
    link_objects,
)
from hc11_compiler.linker import LinkError
from hc11_compiler.objectfile import RelocatableObject
from hc11_compiler.parser import ParseError
from hc11_compiler.resource_map import MemoryRegion


def test_array_and_struct_codegen_assembles():
    src = r"""
struct Pair {
    unsigned char flag;
    unsigned int value;
};

unsigned char samples[8];
struct Pair state;

unsigned char update(unsigned char i) {
    samples[i] = 7;
    state.flag = samples[i];
    state.value = 0x1234;
    return state.flag;
}
"""
    asm = compile_source(src, target="vy_v6", output="asm")
    assert "ABX" in asm
    assert "STAA    0,X" in asm
    assert "STD     0,X" in asm

    binary = compile_source(src, target="vy_v6", output="binary")
    assert len(binary) > 0


def test_local_array_and_struct_pointer_codegen():
    src = r"""
struct Pair {
    unsigned char flag;
    unsigned int value;
};

unsigned char read_pair(struct Pair *p, unsigned char i) {
    unsigned char scratch[4];
    scratch[i] = p->flag;
    return scratch[i];
}
"""
    asm = compile_source(src, target="vy_v6", output="asm")
    assert "PSHY" in asm
    assert "TSY" in asm
    assert ",Y" in asm
    assert "XGDX" in asm
    assert len(compile_source(src, target="vy_v6", output="binary")) > 0


def test_sizeof_arrays_and_structs_is_compile_time():
    src = r"""
struct Pair {
    unsigned char flag;
    unsigned int value;
};
unsigned char data[8];

unsigned int size_pair(void) { return sizeof(struct Pair); }
unsigned int size_data(void) { return sizeof(data); }
"""
    asm = compile_source(src, target="vy_v6", output="asm")
    assert "#$03" in asm
    assert "#$08" in asm


def test_arrays_over_255_elements_fail_explicitly():
    with pytest.raises(ParseError, match="255"):
        compile_source("unsigned char huge[256];", target="vy_v6")


def test_stable_y_frame_replaces_moving_x_frame_for_locals():
    src = r"""
unsigned char f(unsigned char a) {
    unsigned char x;
    unsigned char y;
    x = a;
    y = x;
    return y;
}
"""
    asm = compile_source(src, target="vy_v6", output="asm")
    assert "PSHY" in asm
    assert "TSY" in asm
    assert "0,Y" in asm
    assert "1,Y" in asm
    assert "TSX" not in asm


def test_k11o_round_trip():
    obj = compile_object(
        "unsigned char helper(unsigned char x) { return x + 1; }",
        module_name="math",
        target="vy_v6",
    )
    restored = RelocatableObject.loads(obj.dumps())
    assert restored.module == "math"
    assert restored.target == "vy_v6"
    assert [x.name for x in restored.exports] == ["helper"]
    assert restored.imports == []
    assert restored.source_sha256 == obj.source_sha256
    assert "ORG" not in restored.assembly


def test_multifile_link_resolves_function_import():
    helper = compile_object(
        "unsigned char helper(unsigned char x) { return x + 1; }",
        module_name="helper",
        target="vy_v6",
    )
    app = compile_object(
        r"""
extern unsigned char helper(unsigned char x);
unsigned char main(void) { return helper(4); }
""",
        module_name="app",
        target="vy_v6",
    )

    image = link_objects([helper, app])
    assert image.size > 0
    assert image.base_addr >= 0x8000
    assert "helper" in image.symbols
    assert "main" in image.symbols
    assert image.s19.startswith("S0")


def test_linker_allocates_global_ram_without_overlap():
    a = compile_object(
        r"""
unsigned char a_buf[8];
unsigned char a(void) { return a_buf[0]; }
""",
        module_name="a",
        target="vy_v6",
    )
    b = compile_object(
        r"""
__zeropage unsigned char fast;
unsigned int b_buf[3];
unsigned char b(void) { fast = 1; return fast; }
""",
        module_name="b",
        target="vy_v6",
    )

    image = link_objects([a, b])
    allocations = [
        x for x in image.resource_map.allocations
        if x.kind in ("ram", "zp")
    ]
    assert len(allocations) == 3
    for i, left in enumerate(allocations):
        for right in allocations[i + 1:]:
            assert left.end < right.start or right.end < left.start


def test_duplicate_exports_are_rejected():
    one = compile_object(
        "unsigned char collide(void) { return 1; }",
        module_name="one",
        target="vy_v6",
    )
    two = compile_object(
        "unsigned char collide(void) { return 2; }",
        module_name="two",
        target="vy_v6",
    )
    with pytest.raises(LinkError, match="Duplicate export"):
        link_objects([one, two])


def test_unresolved_import_is_rejected():
    app = compile_object(
        "unsigned char main(void) { return missing(); }",
        module_name="app",
        target="vy_v6",
    )
    with pytest.raises(LinkError, match="Unresolved imports"):
        link_objects([app])


def test_ram_exhaustion_is_reported_before_image_is_emitted():
    obj = compile_object(
        "unsigned char too_big[8]; unsigned char main(void) { return 1; }",
        module_name="big",
        target="vy_v6",
    )
    rmap = ResourceMap(regions=[
        MemoryRegion("tiny_ram", "ram", 0x0100, 0x0103),
        MemoryRegion("rom", "rom", 0x8000, 0x8FFF, 2),
    ])
    with pytest.raises(LinkError, match="fit 8 bytes"):
        link_objects([obj], resource_map=rmap)


def test_reserved_rom_hole_is_skipped_and_linked_code_is_collision_checked():
    obj = compile_object(
        "unsigned char main(void) { return 1; }",
        module_name="app",
        target="vy_v6",
    )
    rmap = ResourceMap(regions=[
        MemoryRegion("ram", "ram", 0x0100, 0x03FF),
        MemoryRegion("rom", "rom", 0x8000, 0x8FFF, 2),
    ])
    rmap.reserve("rom", 0x8000, 0x0100, "factory_owned")
    image = link_objects([obj], resource_map=rmap)
    assert image.base_addr >= 0x8100
    code = next(x for x in image.resource_map.allocations if x.name == "__linked_code__")
    assert code.start >= 0x8100
