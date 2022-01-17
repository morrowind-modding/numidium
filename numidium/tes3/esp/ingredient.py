from __future__ import annotations

from ..typing import *
from .object import TES3Object
from .enums import AttributeId, EffectId, SkillId


class Ingredient(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    data: IngredientData | None
    name: str | None
    mesh: str | None
    icon: str | None
    script: str | None
    deleted: u32 | None


class IngredientData(TES3Object):
    weight: f32
    value: u32
    effects: list[EffectId]  # size=4
    skills: list[SkillId]  # size=4
    attributes: list[AttributeId]  # size=4
