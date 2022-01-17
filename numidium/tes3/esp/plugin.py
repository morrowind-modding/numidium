from __future__ import annotations

from .. import _tes3  # type: ignore
from .object import TES3Object


class Plugin:
    objects: list[TES3Object]

    @staticmethod
    def load(path: str) -> Plugin:
        plugin = Plugin()
        plugin.objects = []

        for obj in _tes3.load_objects(path):
            plugin.objects.append(TES3Object.wrap(obj))

        return plugin
