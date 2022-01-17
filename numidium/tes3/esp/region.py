from __future__ import annotations

from ..typing import *
from .object import TES3Object


class Region(TES3Object):
    flags1: u32
    flags2: u32
    id: str
    name: str | None
    weather_chances: WeatherChances | None
    sleep_creature: str | None
    map_color: list[u8] | None  # size=4
    sounds: list[tuple[FixedString32, u8]]
    deleted: u32 | None


class WeatherChances(TES3Object):
    clear: u8
    cloudy: u8
    foggy: u8
    overcast: u8
    rain: u8
    thunder: u8
    ash: u8
    blight: u8
    snow: u8
    blizzard: u8
