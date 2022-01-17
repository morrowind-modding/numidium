from __future__ import annotations

from ..typing import *
from .object import TES3Object
from .enums import SkillId


class Book(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    data: BookData | None
    name: str | None
    mesh: str | None
    icon: str | None
    script: str | None
    enchanting: str | None
    text: str | None
    deleted: u32 | None


class BookData(TES3Object):
    weight: f32
    value: u32
    flags: u32
    skill: SkillId
    enchantment: u32
