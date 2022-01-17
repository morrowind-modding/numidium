from __future__ import annotations

from ..typing import *
from .object import TES3Object


class PathGrid(TES3Object):
    flags1: u32
    flags2: u32
    cell: str | None
    data: PathGridData | None
    points: list[PathGridPoint]
    connections: list[u32]
    deleted: u32 | None


class PathGridData(TES3Object):
    grid: tuple[i32, i32]
    granularity: u16
    point_count: u16


class PathGridPoint(TES3Object):
    location: list[i32]  # size=3
    auto_generated: u8
    connection_count: u8
