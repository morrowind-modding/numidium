from __future__ import annotations

from ..typing import *
from .object import TES3Object
from .enums import AttributeId, SkillId, Specialization


class Class(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    name: str | None
    data: ClassData | None
    description: str | None
    deleted: u32 | None


class ClassData(TES3Object):
    attribute1: AttributeId
    attribute2: AttributeId
    specialization: Specialization
    minor1: SkillId
    major1: SkillId
    minor2: SkillId
    major2: SkillId
    minor3: SkillId
    major3: SkillId
    minor4: SkillId
    major4: SkillId
    minor5: SkillId
    major5: SkillId
    flags: u32
    auto_calc_flags: u32
