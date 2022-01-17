from __future__ import annotations

from ..typing import *
from .object import TES3Object
from .reference import Reference


class Cell(TES3Object):
    flags1: u32
    flags2: u32
    name: str | None
    data: CellData | None
    region: str | None
    map_color: list[u8] | None  # size=4
    water_height: f32 | None
    atmosphere_data: AtmosphereData | None
    references: dict[tuple[u32, u32], Reference]
    deleted: u32 | None


class CellData(TES3Object):
    flags: u32
    grid: tuple[i32, i32]


class AtmosphereData(TES3Object):
    ambient_color: list[u8]  # size=4
    sunlight_color: list[u8]  # size=4
    fog_color: list[u8]  # size=4
    fog_density: f32
