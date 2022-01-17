from __future__ import annotations

from ..typing import *
from .object import TES3Object


class GameSetting(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    value: str | f32 | i32 | None
