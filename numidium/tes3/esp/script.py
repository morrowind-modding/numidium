from __future__ import annotations

from ..typing import *
from .object import TES3Object


class Script(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    header: ScriptHeader | None
    variables: BString | None
    bytecode: BString | None
    script_text: str | None
    deleted: u32 | None


class ScriptHeader(TES3Object):
    num_shorts: u32
    num_longs: u32
    num_floats: u32
    bytecode_length: u32
    variables_length: u32
