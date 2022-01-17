from __future__ import annotations

from ..typing import *
from .object import TES3Object
from .enums import BodypartId, BodypartType


class Bodypart(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    data: BodypartData | None
    name: str | None
    mesh: str | None
    deleted: u32 | None


class BodypartData(TES3Object):
    part: BodypartId
    vampire: u8
    female: u8
    kind: BodypartType
