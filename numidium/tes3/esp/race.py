from __future__ import annotations

from ..typing import *
from .object import TES3Object
from .enums import SkillId


class Race(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    name: str | None
    data: RaceData | None
    spells: list[FixedString32]
    description: str | None
    deleted: u32 | None


class RaceData(TES3Object):
    skill_bonuses: list[tuple[SkillId, i32]]  # len = (7)
    strength: list[i32]  # size=2
    intelligence: list[i32]  # size=2
    willpower: list[i32]  # size=2
    agility: list[i32]  # size=2
    speed: list[i32]  # size=2
    endurance: list[i32]  # size=2
    personality: list[i32]  # size=2
    luck: list[i32]  # size=2
    height: list[f32]  # size=2
    weight: list[f32]  # size=2
    flags: u32
