from __future__ import annotations

from ..typing import *
from .object import TES3Object


class Activator(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    name: str | None
    mesh: str | None
    script: str | None
    deleted: u32 | None
