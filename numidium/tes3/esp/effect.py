from __future__ import annotations

from ..typing import *
from .object import TES3Object
from .enums import AttributeId2, EffectId2, SkillId2


class Effect(TES3Object):
    magic_effect: EffectId2
    skill: SkillId2
    attribute: AttributeId2
    range: u32
    area: u32
    duration: u32
    min_magnitude: u32
    max_magnitude: u32
