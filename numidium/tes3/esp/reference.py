from __future__ import annotations

from ..typing import *
from .object import TES3Object


class Reference(TES3Object):
    mast_index: u32
    refr_index: u32
    id: str
    temporary: bool
    translation: list[f32]  # size=3
    rotation: list[f32]  # size=3
    scale: f32 | None
    moved_cell: tuple[i32, i32] | None
    blocked: u8 | None
    owner: str | None
    owner_global: str | None
    owner_faction: str | None
    owner_faction_rank: u32 | None
    charge_left: u32 | None
    health_left: u32 | None
    stack_size: u32 | None
    door_destination_coords: list[f32] | None  # size=6
    door_destination_cell: str | None
    lock_level: u32 | None
    key: str | None
    trap: str | None
    soul: str | None
    deleted: u32 | None
