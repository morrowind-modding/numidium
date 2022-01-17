from __future__ import annotations

from ..typing import *
from .object import TES3Object
from .enums import AttributeId, SkillId


class Faction(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    name: str | None
    rank_names: list[FixedString32]
    data: FactionData | None
    reactions: list[FactionReaction]
    deleted: u32 | None


class FactionData(TES3Object):
    favored_attributes: list[AttributeId]  # size=2
    favored_skills: list[SkillId]  # size=7
    flags: u32


class FactionRequirement(TES3Object):
    attributes: list[i32]  # size=2
    primary_skill: i32
    favored_skill: i32
    reputation: i32


class FactionReaction(TES3Object):
    faction: str
    reaction: i32
