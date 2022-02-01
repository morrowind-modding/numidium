from __future__ import annotations

from .enums import BipedObjectType
from .object import TES3Object


class BipedObject(TES3Object):
    kind: BipedObjectType
    male_bodypart: str | None
    female_bodypart: str | None
