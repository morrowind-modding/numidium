from __future__ import annotations

import pathlib
from os import PathLike
from typing import Protocol

import tomlkit


class ExtensionProtocol(Protocol):
    """Interface that extensions must conform to."""

    @staticmethod
    def register() -> None:
        pass

    @staticmethod
    def unregister() -> None:
        pass


class Extension:
    path: pathlib.Path
    toml: tomlkit.TOMLDocument

    def __init__(self, path: PathLike[str]) -> None:
        with open(path, "rb") as file:
            self.path = pathlib.Path(path)
            self.toml = tomlkit.load(file)
