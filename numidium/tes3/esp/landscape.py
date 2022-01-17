from __future__ import annotations

from ..typing import *
from .object import TES3Object


class Landscape(TES3Object):
    flags1: u32
    flags2: u32
    grid: tuple[i32, i32] | None
    landscape_flags: u32 | None
    vertex_normals: VertexNormals | None
    vertex_heights: VertexHeights | None
    world_map_data: WorldMapData | None
    vertex_colors: VertexColors | None
    texture_indices: TextureIndices | None
    deleted: u32 | None


class VertexNormals(TES3Object):
    data: list[i8]  # size=(3 * 65 * 65)


class VertexHeights(TES3Object):
    offset: f32
    data: list[i8]  # size=(65 * 65)


class WorldMapData(TES3Object):
    data: list[i8]  # size=(9 * 9)


class VertexColors(TES3Object):
    data: list[u8]  # size=(3 * 65 * 65)


class TextureIndices(TES3Object):
    data: list[u16]  # size=(16 * 16)
