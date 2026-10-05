"""Collision-checked ROM/RAM resource maps for HC11 linking."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


class ResourceMapError(Exception):
    pass


class ResourceCollisionError(ResourceMapError):
    pass


def _as_int(value) -> int:
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        text = value.strip()
        if text.startswith("$"):
            return int(text[1:], 16)
        return int(text, 0)
    raise TypeError(f"Expected integer address, got {type(value).__name__}")


def _align_up(value: int, alignment: int) -> int:
    if alignment <= 0:
        raise ValueError("alignment must be positive")
    return ((value + alignment - 1) // alignment) * alignment


@dataclass(frozen=True)
class MemoryRegion:
    name: str
    kind: str
    start: int
    end: int                  # inclusive
    alignment: int = 1

    @property
    def size(self) -> int:
        return self.end - self.start + 1

    def contains(self, start: int, size: int) -> bool:
        if size <= 0:
            return False
        end = start + size - 1
        return self.start <= start and end <= self.end

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "kind": self.kind,
            "start": self.start,
            "end": self.end,
            "alignment": self.alignment,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MemoryRegion":
        return cls(
            name=str(data["name"]),
            kind=str(data["kind"]),
            start=_as_int(data["start"]),
            end=_as_int(data["end"]),
            alignment=int(data.get("alignment", 1)),
        )


@dataclass(frozen=True)
class Allocation:
    name: str
    kind: str
    start: int
    size: int
    module: str = ""
    reserved: bool = False

    @property
    def end(self) -> int:
        return self.start + self.size - 1

    def overlaps(self, other_start: int, other_size: int) -> bool:
        other_end = other_start + other_size - 1
        return not (self.end < other_start or other_end < self.start)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "kind": self.kind,
            "start": self.start,
            "size": self.size,
            "module": self.module,
            "reserved": self.reserved,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Allocation":
        return cls(
            name=str(data["name"]),
            kind=str(data["kind"]),
            start=_as_int(data["start"]),
            size=int(data["size"]),
            module=str(data.get("module", "")),
            reserved=bool(data.get("reserved", False)),
        )


@dataclass
class ResourceMap:
    """A set of allocatable regions plus committed allocations.

    Regions may overlap (for example, a generic RAM pool and a zero-page pool).
    Allocation collision checks are global, so the same bytes can never be
    assigned twice even when two region classes cover them.
    """

    regions: List[MemoryRegion] = field(default_factory=list)
    allocations: List[Allocation] = field(default_factory=list)

    def clone(self) -> "ResourceMap":
        return ResourceMap.from_dict(self.to_dict())

    def regions_for(self, kind: str) -> List[MemoryRegion]:
        return sorted(
            (r for r in self.regions if r.kind == kind),
            key=lambda r: (r.start, r.end, r.name),
        )

    def _collision(self, start: int, size: int) -> Optional[Allocation]:
        for alloc in self.allocations:
            if alloc.overlaps(start, size):
                return alloc
        return None

    def _region_for_range(self, kind: str, start: int, size: int) -> Optional[MemoryRegion]:
        for region in self.regions_for(kind):
            if region.contains(start, size):
                return region
        return None

    def reserve(self, kind: str, start: int, size: int, name: str,
                module: str = "", *, reserved: bool = True) -> Allocation:
        start = _as_int(start)
        size = int(size)
        if size <= 0:
            raise ResourceMapError(f"{name}: size must be positive")
        region = self._region_for_range(kind, start, size)
        if region is None:
            raise ResourceMapError(
                f"{name}: ${start:04X}-${start + size - 1:04X} is outside all {kind} regions"
            )
        hit = self._collision(start, size)
        if hit is not None:
            raise ResourceCollisionError(
                f"{name}: ${start:04X}-${start + size - 1:04X} collides with "
                f"{hit.module + ':' if hit.module else ''}{hit.name} "
                f"(${hit.start:04X}-${hit.end:04X})"
            )
        alloc = Allocation(
            name=name, kind=kind, start=start, size=size,
            module=module, reserved=reserved,
        )
        self.allocations.append(alloc)
        return alloc

    def find_free(self, kind: str, size: int, alignment: int = 1) -> int:
        size = int(size)
        if size <= 0:
            raise ResourceMapError("allocation size must be positive")
        for region in self.regions_for(kind):
            effective_alignment = max(int(alignment), int(region.alignment), 1)
            candidate = _align_up(region.start, effective_alignment)
            while candidate + size - 1 <= region.end:
                hit = self._collision(candidate, size)
                if hit is None:
                    return candidate
                candidate = _align_up(hit.end + 1, effective_alignment)
        raise ResourceMapError(
            f"No {kind} region can fit {size} bytes aligned to {alignment}"
        )

    def allocate(self, kind: str, size: int, alignment: int, name: str,
                 module: str = "") -> Allocation:
        start = self.find_free(kind, size, alignment)
        return self.reserve(kind, start, size, name, module, reserved=False)

    def usage(self, kind: Optional[str] = None) -> int:
        return sum(
            a.size for a in self.allocations
            if kind is None or a.kind == kind
        )

    def to_dict(self) -> dict:
        return {
            "format": "k11-resource-map",
            "version": 1,
            "regions": [r.to_dict() for r in self.regions],
            "allocations": [a.to_dict() for a in self.allocations],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ResourceMap":
        if data.get("format") not in (None, "k11-resource-map"):
            raise ResourceMapError("Unsupported resource-map format")
        return cls(
            regions=[MemoryRegion.from_dict(x) for x in data.get("regions", [])],
            allocations=[Allocation.from_dict(x) for x in data.get("allocations", [])],
        )

    @classmethod
    def default_for_target(cls, target: str) -> "ResourceMap":
        from .codegen import TARGET_PROFILES

        profile = TARGET_PROFILES.get(target)
        if profile is None:
            raise ResourceMapError(f"Unknown target profile: {target}")

        ram_start = int(profile.get("ram_start", 0x0000))
        ram_end = int(profile.get("ram_end", 0x00FF))
        rom_start = int(profile.get("org", 0x8000))
        vectors = int(profile.get("vectors", 0xFFD6))

        regions: List[MemoryRegion] = []
        zp_start = max(ram_start, 0x0040)
        zp_end = min(ram_end, 0x00FF)
        if zp_start <= zp_end:
            regions.append(MemoryRegion("zero_page", "zp", zp_start, zp_end, 1))

        if ram_end >= 0x0100:
            regions.append(MemoryRegion("extended_ram", "ram",
                                        max(ram_start, 0x0100), ram_end, 1))
        elif zp_start <= zp_end:
            regions.append(MemoryRegion("general_ram", "ram", zp_start, zp_end, 1))

        if rom_start < vectors:
            regions.append(MemoryRegion("program_rom", "rom",
                                        rom_start, vectors - 1, 2))

        return cls(regions=regions)

    @classmethod
    def from_json(cls, text: str) -> "ResourceMap":
        import json
        return cls.from_dict(json.loads(text))

    def to_json(self, *, indent: int = 2) -> str:
        import json
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True)
