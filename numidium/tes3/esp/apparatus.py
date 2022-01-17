from __future__ import annotations

from ..typing import *
from .object import TES3Object
from .enums import ApparatusType


class Apparatus(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    data: ApparatusData | None
    name: str | None
    mesh: str | None
    icon: str | None
    script: str | None
    deleted: u32 | None


class ApparatusData(TES3Object):
    kind: ApparatusType
    quality: f32
    weight: f32
    value: u32
