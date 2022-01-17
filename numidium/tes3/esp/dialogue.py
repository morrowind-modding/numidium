from __future__ import annotations

from ..typing import *
from .object import TES3Object
from .enums import DialogueType2


class Dialogue(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    kind: DialogueType2 | None
    deleted: u32 | None
