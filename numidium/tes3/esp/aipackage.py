from __future__ import annotations

from ..typing import *
from .object import TES3Object


class AiTravelPackage(TES3Object):
    location: list[f32]  # size=3
    reset: u8


class AiWanderPackage(TES3Object):
    distance: u16
    duration: u16
    game_hour: u8
    idle2: u8
    idle3: u8
    idle4: u8
    idle5: u8
    idle6: u8
    idle7: u8
    idle8: u8
    idle9: u8
    reset: i8


class AiEscortPackage(TES3Object):
    location: list[f32]  # size=3
    duration: u16
    target: FixedString32
    reset: u8
    cell: str | None


class AiFollowPackage(TES3Object):
    location: list[f32]  # size=3
    duration: u16
    target: FixedString32
    reset: u8
    cell: str | None


class AiActivatePackage(TES3Object):
    target: FixedString32
    reset: u8


class TravelDestination(TES3Object):
    translation: list[f32]  # size=3
    rotation: list[f32]  # size=3
    cell: str | None
