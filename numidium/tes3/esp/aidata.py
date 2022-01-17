from __future__ import annotations

from ..typing import *
from .object import TES3Object


class AiData(TES3Object):
    hello: i16
    fight: i8
    flee: i8
    alarm: i8
    services: u32
