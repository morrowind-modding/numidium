from __future__ import annotations

from ..typing import *
from .object import TES3Object


class Light(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    data: LightData | None
    name: str | None
    mesh: str | None
    icon: str | None
    script: str | None
    sound: str | None
    deleted: u32 | None


class LightData(TES3Object):
    weight: f32
    value: u32
    time: i32
    radius: u32
    color: list[u8]  # size=4
    flags: u32
