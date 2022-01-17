from __future__ import annotations

from ..typing import *
from .object import TES3Object
from .enums import WeaponType


class Weapon(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    data: WeaponData | None
    mesh: str | None
    name: str | None
    icon: str | None
    script: str | None
    enchanting: str | None
    deleted: u32 | None


class WeaponData(TES3Object):
    weight: f32
    value: u32
    kind: WeaponType
    health: u16
    speed: f32
    reach: f32
    enchantment: u16
    chop_min: u8
    chop_max: u8
    slash_min: u8
    slash_max: u8
    thrust_min: u8
    thrust_max: u8
    flags: u32
