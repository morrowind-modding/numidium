from __future__ import annotations

from ..typing import *
from .object import TES3Object
from .effect import Effect


class Alchemy(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    data: AlchemyData | None
    name: str | None
    mesh: str | None
    icon: str | None
    script: str | None
    effects: list[Effect]
    deleted: u32 | None


class AlchemyData(TES3Object):
    weight: f32
    value: u32
    flags: u32
