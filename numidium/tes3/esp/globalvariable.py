from __future__ import annotations

from ..typing import *
from .object import TES3Object
from .enums import GlobalType


class GlobalVariable(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    kind: GlobalType | None
    value: f32 | None
    deleted: u32 | None
