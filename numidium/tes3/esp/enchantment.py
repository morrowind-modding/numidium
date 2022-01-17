from __future__ import annotations

from ..typing import *
from .object import TES3Object
from .effect import Effect
from .enums import EnchantType


class Enchantment(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    data: EnchantmentData | None
    effects: list[Effect]
    deleted: u32 | None


class EnchantmentData(TES3Object):
    kind: EnchantType
    cost: u32
    max_charge: u32
    flags: u32
