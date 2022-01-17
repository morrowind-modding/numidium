from __future__ import annotations

from ..typing import *
from .object import TES3Object


class RepairTool(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    data: RepairToolData | None
    name: str | None
    mesh: str | None
    icon: str | None
    script: str | None
    deleted: u32 | None


class RepairToolData(TES3Object):
    weight: f32
    value: u32
    uses: u32
    quality: f32
