from __future__ import annotations

from ..typing import *
from .object import TES3Object


class LandscapeTexture(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    index: u32 | None
    texture: str | None
    deleted: u32 | None
