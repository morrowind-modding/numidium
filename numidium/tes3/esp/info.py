from __future__ import annotations

from ..typing import *
from .enums import (
    DialogueType,
    FilterComparison,
    FilterFunction,
    FilterSlot,
    FilterType,
    Sex,
)
from .object import TES3Object


class Info(TES3Object):
    flags1: u32
    flags2: u32
    info_id: str
    prev_id: str | None
    next_id: str | None
    data: InfoData | None
    speaker_id: str | None
    speaker_rank: str | None
    speaker_class: str | None
    speaker_faction: str | None
    speaker_cell: str | None
    player_faction: str | None
    text: str | None
    sound_path: str | None
    quest_name: u8 | None
    quest_finish: u8 | None
    quest_restart: u8 | None
    filters: list[Filter]
    script_text: str | None
    deleted: u32 | None


class InfoData(TES3Object):
    kind: DialogueType
    disposition: i32
    speaker_rank: i8
    speaker_sex: Sex
    player_rank: i8


class Filter(TES3Object):
    slot: FilterSlot
    kind: FilterType
    function: FilterFunction
    comparison: FilterComparison
    id: str
    value: f32 | i32 | None
