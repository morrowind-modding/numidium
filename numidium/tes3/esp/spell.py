from __future__ import annotations

from ..typing import *
from .object import TES3Object
from .effect import Effect
from .enums import SpellType


class Spell(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    name: str | None
    data: SpellData | None
    effects: list[Effect]
    deleted: u32 | None


class SpellData(TES3Object):
    kind: SpellType
    cost: u32
    flags: u32
