from __future__ import annotations

from ..typing import *
from .object import TES3Object


class Birthsign(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    name: str | None
    texture: str | None
    description: str | None
    spells: list[FixedString32]
    deleted: u32 | None
