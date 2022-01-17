from __future__ import annotations

from ..typing import *
from .object import TES3Object


class Door(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    name: str | None
    mesh: str | None
    script: str | None
    open_sound: str | None
    close_sound: str | None
    deleted: u32 | None
