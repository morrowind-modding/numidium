from __future__ import annotations

from ..typing import *
from .object import TES3Object


class SoundGen(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    sound_flags: u32 | None
    creature: str | None
    sound: str | None
    deleted: u32 | None
