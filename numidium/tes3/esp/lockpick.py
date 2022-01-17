from __future__ import annotations

from ..typing import *
from .object import TES3Object


class Lockpick(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    data: LockpickData | None
    name: str | None
    mesh: str | None
    icon: str | None
    script: str | None
    deleted: u32 | None


class LockpickData(TES3Object):
    weight: f32
    value: u32
    uses: u32
    quality: f32
