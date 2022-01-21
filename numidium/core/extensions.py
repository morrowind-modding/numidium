from __future__ import annotations

import importlib
import sys
from dataclasses import dataclass
from operator import itemgetter
from pathlib import Path
from typing import Iterator, Protocol, cast

import tomlkit

from numidium.logger import logger

EXTENSIONS_DIR = Path.cwd() / "numidium" / "extensions"
GET_TOML_ITEMS = itemgetter("name", "version", "description", "authors")


class ExtensionProtocol(Protocol):
    """Interface that extension modules must conform to."""

    @staticmethod
    def register() -> None:
        pass

    @staticmethod
    def unregister() -> None:
        pass


@dataclass
class Extension:
    """An extension for the application.

    Attributes
    ----------
    path : Path
        The (absolute) path to the extension directory.
    name : str
        The extension name, which may differ from the directory name.
    version : str
        The extension version, semantic versioning recommended (e.g. '1.0.0').
    description : str
        The extension description.
    authors : list[str]
        The extension authors.
    active : bool = False
        Is the extension currently active.
    module : ExtensionProtocol | None = None
        The python module created from importing the extension.
        Expected to contain `register` and `unregister` methods.
    """

    path: Path
    name: str
    version: str
    description: str
    authors: list[str]

    icon: str = "icons:icon.ico"

    active: bool = False
    module: ExtensionProtocol | None = None

    def register(self) -> None:
        logger.info("Registering extension: {}", self.name)
        self.module = import_module(self.path.stem)
        self.active = True
        self.module.register()

    def unregister(self) -> None:
        logger.info("Unregistering extension: {}", self.name)
        self.active = False
        if self.module:
            self.module.unregister()

    @staticmethod
    def from_path(path: Path) -> Extension | None:
        if not path.is_dir():
            logger.warning("Extension is not packaged as a directory: {}", path.name)
            return None

        init_path = path / "__init__.py"
        if not init_path.is_file():
            logger.warning("Extension does not have a `__init__.py` file: {}", path.name)
            return None

        toml_path = path / "pyproject.toml"
        if not toml_path.is_file():
            logger.warning("Extension does not have a `pyproject.toml` file: {}", path.name)
            return None

        try:
            toml_data = tomlkit.parse(toml_path.read_text())
        except (UnicodeDecodeError, ValueError):
            logger.warning("Extension has invalid `pyproject.toml` file: {}", path.name)
            return None

        if not (
            isinstance(tool := toml_data.get("tool"), dict)
            and isinstance(table := tool.get("numidium"), dict)  # fmt: skip
        ):
            logger.warning("Could not find `tool.numidium` item: {}", toml_path)
            return None

        if not (
            isinstance(authors := table.get("authors"), list)
            and all(isinstance(author, str) for author in authors)  # fmt: skip
        ):
            logger.warning("Invalid author in `tool.numidium`: {}", toml_path)
            return None

        for key in "name", "version", "description":
            if not isinstance(value := table.get(key), str):
                logger.warning("Invalid {} in `tool.numidium`: {}", key, toml_path)
                return None

        return Extension(path, *GET_TOML_ITEMS(table))


def available_extensions() -> Iterator[Extension]:
    """Yields available extensions."""

    for path in EXTENSIONS_DIR.iterdir():
        if extension := Extension.from_path(path):
            yield extension


def import_module(path: str) -> ExtensionProtocol:
    importlib.invalidate_caches()

    module_name = f"numidium.extensions.{path}"  # TODO: dynamic packages
    try:
        module = sys.modules[module_name]
    except KeyError:
        module = importlib.import_module(module_name)
    else:
        importlib.reload(module)

    assert callable(module.register)
    assert callable(module.unregister)

    return cast(ExtensionProtocol, module)
