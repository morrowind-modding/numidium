from __future__ import annotations

from ..typing import *
from .object import TES3Object
from .enums import SkillId


class Skill(TES3Object):
    flags1: u32
    flags2: u32
    skill_id: SkillId
    data: SkillData | None
    description: str | None
    deleted: u32 | None


class SkillData(TES3Object):
    governing_attribute: i32
    specialization: i32
    actions: list[f32]  # size=4
