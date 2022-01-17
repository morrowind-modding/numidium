from __future__ import annotations

from ..typing import *
from .object import TES3Object
from .enums import FileType


class Header(TES3Object):
    flags1: u32
    flags2: u32
    version: f32
    file_type: FileType
    author: FixedString32
    description: FixedString256
    num_objects: u32
    masters: list[tuple[str, u64]]
