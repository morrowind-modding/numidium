from __future__ import annotations

from ..typing import *
from .object import TES3Object


class Sound(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    sound_path: str | None
    data: SoundData | None
    deleted: u32 | None


class SoundData(TES3Object):
    volume: u8
    range: tuple[u8, u8]
