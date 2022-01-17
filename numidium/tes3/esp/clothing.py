from __future__ import annotations

from ..typing import *
from .object import TES3Object
from .bipedobject import BipedObject
from .enums import ClothingType


class Clothing(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    data: ClothingData | None
    name: str | None
    mesh: str | None
    icon: str | None
    script: str | None
    enchanting: str | None
    biped_objects: list[BipedObject]
    deleted: u32 | None


class ClothingData(TES3Object):
    kind: ClothingType
    value: u16
    weight: f32
    enchantment: u16
