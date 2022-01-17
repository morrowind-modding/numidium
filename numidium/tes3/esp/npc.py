from __future__ import annotations

from ..typing import *
from .object import TES3Object
from .aidata import AiData
from .aipackage import (
    AiActivatePackage,
    AiEscortPackage,
    AiFollowPackage,
    AiTravelPackage,
    AiWanderPackage,
    TravelDestination,
)


class Npc(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    name: str | None
    mesh: str | None
    script: str | None
    race: str | None
    class_: str | None
    faction: str | None
    head: str | None
    hair: str | None
    npc_flags: u32 | None
    data: NpcData | None
    inventory: list[tuple[i32, FixedString32]]
    spells: list[FixedString32]
    ai_data: AiData | None
    ai_packages: list[AiTravelPackage | AiWanderPackage | AiEscortPackage | AiFollowPackage | AiActivatePackage]
    travel_destinations: list[TravelDestination]
    deleted: u32 | None


class NpcData(TES3Object):
    level: i16
    stats: NpcStats | None
    disposition: i8
    reputation: i8
    rank: i8
    gold: u32


class NpcStats(TES3Object):
    attributes: list[u8]  # size=8
    skills: list[u8]  # size=(27)
    health: u16
    magicka: u16
    fatigue: u16
