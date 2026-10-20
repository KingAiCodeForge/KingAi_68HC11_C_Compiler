"""Synthetic fail-closed resource-map admission regression tests.

No ECU memory layouts, factory ROM holes or KCOS interrupts are claimed proven
by these synthetic input fixtures.
"""
import copy
import pytest

from hc11_compiler.resource_map import (
    ResourceMap, ResourceMapError, ResourceCollisionError
)

def baseline():
    return {
        "format":"k11-resource-map", "version":1,
        "regions":[
            {"name":"zero","kind":"zp","start":"0x40","end":"0x4F","alignment":1},
            {"name":"shared","kind":"ram","start":"0x40","end":"0x5F","alignment":1},
            {"name":"program","kind":"rom","start":"0x8000","end":"0x8FFF","alignment":2},
        ],
        "allocations":[
            {"name":"factory","kind":"zp","start":"0x40","size":8,"reserved":True}
        ],
    }

def test_valid_overlapping_pool_regions_allowed_but_reservations_unique():
    obj=ResourceMap.from_dict(baseline())
    next_ram=obj.allocate("ram",8,1,"new")
    assert next_ram.start==0x48

@pytest.mark.parametrize("candidate",[
    {"name":"overlap","kind":"ram","start":"0x47","size":3},
    {"name":"same","kind":"zp","start":"0x40","size":8},
])
def test_preloaded_cross_kind_and_same_kind_collisions_refused(candidate):
    data=baseline()
    data["allocations"].append(candidate)
    with pytest.raises(ResourceCollisionError,match="collides"):
        ResourceMap.from_dict(data)

def test_allocation_outside_all_matching_kinds_refused():
    data=baseline()
    data["allocations"]=[{"name":"wrong_kind","kind":"zp","start":"0x55","size":2}]
    with pytest.raises(ResourceMapError,match="matching region"):
        ResourceMap.from_dict(data)

@pytest.mark.parametrize("start,size",[
    ("0x40",0), ("0x40",-1), ("0xFFFF",2), (-1,1),
])
def test_invalid_allocation_span_refused(start,size):
    data=baseline()
    data["allocations"]=[{"name":"bad","kind":"ram","start":start,"size":size}]
    with pytest.raises(ResourceMapError):
        ResourceMap.from_dict(data)

@pytest.mark.parametrize("change",[
    {"start":"0x80","end":"0x40"},
    {"start":-1},
    {"end":"0x10000"},
    {"alignment":0},
    {"name":""},
    {"kind":""},
])
def test_invalid_region_shapes_refused(change):
    data=baseline()
    data["regions"][0].update(change)
    with pytest.raises(ResourceMapError):
        ResourceMap.from_dict(data)

@pytest.mark.parametrize("key,value",[
    ("regions",{}),("allocations",None),("version",2),("version",True),
    ("format","arbitrary"),("regions",["bad"]),
])
def test_invalid_resource_envelope_refused(key,value):
    data=baseline()
    data[key]=value
    with pytest.raises(ResourceMapError):
        ResourceMap.from_dict(data)

def test_reservation_collision_still_checks_loaded_factories():
    obj=ResourceMap.from_dict(baseline())
    with pytest.raises(ResourceCollisionError):
        obj.reserve("ram",0x44,2,"danger")
    assert obj.to_dict()["allocations"][0]["name"]=="factory"

def test_bad_map_not_mutated_on_refusal():
    data=baseline()
    data["allocations"].append(
        {"name":"overlap","kind":"ram","start":"0x42","size":1})
    before=copy.deepcopy(data)
    with pytest.raises(ResourceCollisionError):
        ResourceMap.from_dict(data)
    assert data==before

def test_linker_map_clone_does_not_drop_preloaded_protection():
    obj=ResourceMap.from_dict(baseline())
    copy_map=obj.clone()
    assert copy_map.allocations==obj.allocations
    with pytest.raises(ResourceCollisionError):
        copy_map.reserve("ram",0x46,1,"collision")

