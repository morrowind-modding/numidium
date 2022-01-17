from __future__ import annotations

from ..typing import *
from .object import TES3Object
from .enums import EffectId, EffectSchool


class MagicEffect(TES3Object):
    flags1: u32
    flags2: u32
    effect_id: EffectId
    data: MagicEffectData | None
    icon: str | None
    texture: str | None
    bolt_sound: str | None
    cast_sound: str | None
    hit_sound: str | None
    area_sound: str | None
    cast_visual: str | None
    bolt_visual: str | None
    hit_visual: str | None
    area_visual: str | None
    description: str | None
    deleted: u32 | None


class MagicEffectData(TES3Object):
    school: EffectSchool
    base_cost: f32
    flags: u32
    color: tuple[i32, i32, i32]
    speed: f32
    size: f32
    size_cap: f32
