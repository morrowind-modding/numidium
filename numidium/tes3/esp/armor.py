from __future__ import annotations

from ..typing import *
from .object import TES3Object
from .bipedobject import BipedObject
from .enums import ArmorType


class Armor(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    data: ArmorData | None
    name: str | None
    mesh: str | None
    icon: str | None
    script: str | None
    enchanting: str | None
    biped_objects: list[BipedObject]
    deleted: u32 | None


class ArmorData(TES3Object):
    kind: ArmorType
    weight: f32
    value: u32
    health: u32
    enchantment: u32
    armor_rating: u32
