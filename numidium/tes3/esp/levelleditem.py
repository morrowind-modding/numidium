from __future__ import annotations

from ..typing import *
from .object import TES3Object


class LevelledItem(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    list_flags: u32 | None
    chance_none: u8 | None
    items: list[tuple[str, u16]]
    deleted: u32 | None
