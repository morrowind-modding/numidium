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


class Creature(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    data: CreatureData | None
    name: str | None
    mesh: str | None
    script: str | None
    sound: str | None
    creature_flags: u32 | None
    scale: f32 | None
    inventory: list[tuple[i32, FixedString32]]
    spells: list[FixedString32]
    ai_data: AiData | None
    ai_packages: list[AiTravelPackage | AiWanderPackage | AiEscortPackage | AiFollowPackage | AiActivatePackage]
    travel_destinations: list[TravelDestination]
    deleted: u32 | None


class CreatureData(TES3Object):
    kind: u32
    level: u32
    strength: u32
    intelligence: u32
    willpower: u32
    agility: u32
    speed: u32
    endurance: u32
    personality: u32
    luck: u32
    health: u32
    magicka: u32
    fatigue: u32
    soul_points: u32
    combat: u32
    magic: u32
    steath: u32
    attack1: tuple[u32, u32]
    attack2: tuple[u32, u32]
    attack3: tuple[u32, u32]
    gold: u32
