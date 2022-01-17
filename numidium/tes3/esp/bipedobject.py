from __future__ import annotations

from ..typing import *
from .object import TES3Object
from .enums import BipedObjectType


class BipedObject(TES3Object):
    kind: BipedObjectType
    male_bodypart: str | None
    female_bodypart: str | None
