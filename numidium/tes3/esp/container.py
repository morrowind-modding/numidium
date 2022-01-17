from __future__ import annotations

from ..typing import *
from .object import TES3Object


class Container(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    name: str | None
    mesh: str | None
    script: str | None
    encumbrance: f32 | None
    container_flags: u32 | None
    inventory: list[tuple[i32, FixedString32]]
    deleted: u32 | None
