from __future__ import annotations

import importlib
import sys
from dataclasses import dataclass
from functools import cached_property
from operator import itemgetter
from pathlib import Path
from typing import Iterator, Protocol, cast

import tomlkit

from numidium.config import config
from numidium.logger import logger

EXTENSIONS_DIR = Path.cwd() / "numidium" / "extensions"
GET_TOML_ITEMS = itemgetter("name", "version", "description", "authors")


def available_extensions() -> Iterator[Extension]:
    """Yields available extensions."""
    for path in EXTENSIONS_DIR.iterdir():
        if extension := Extension.from_path(path):
            yield extension


def reload_active_extensions() -> None:
    """Reload all active extensions."""
    for extension in available_extensions():
        if extension.name in config.active_extensions:
            extension.unregister()
            extension.register()


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
    """Represents an extension for the application.

    Creating an instance of this class does not automatically execute any of the
    associated extension's code. Its only purpose is to provide an interface for
    managing extensions. To actually execute/import the extension's code use the
    `register` method.

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
    icon : str
        The extension icon.
    """

    path: Path

    name: str
    version: str
    description: str
    authors: list[str]

    icon: str = "icons:icon.ico"

    def register(self) -> None:
        """Register the extension.

        If the extension module had not been previously imported, this function
        will import it. Otherwise, if the extension module was already imported,
        it will be reloaded as per the standard library `importlib.reload`
        function.

        After the module is imported (or reloaded) its `register` function will
        be called.
        """
        logger.debug("Registering extension: {}", self.name)
        if not self.module:
            module = self.import_module()
            module.register()
            if self.name not in config.active_extensions:
                config.active_extensions.append(self.name)
                config.save_path()

    def unregister(self) -> None:
        """Unregister the extension.

        This is equivilent to calling the extension module's `unregister`
        function and then removing it from `sys.modules`. Future code will no
        longer be able to import the module. Note that any existing references
        to the module will not be automatically invalidated.
        """
        logger.debug("Unregistering extension: {}", self.name)
        if self.module:
            self.module.unregister()
            del sys.modules[self.module_name]
            if self.name in config.active_extensions:
                config.active_extensions.remove(self.name)
                config.save_path()

    @property
    def module(self) -> ExtensionProtocol | None:
        """The python module created from importing this extension."""
        if module := sys.modules.get(self.module_name):
            return cast(ExtensionProtocol, module)
        return None

    @cached_property
    def module_name(self) -> str:
        """The name of the python module associated with this extension."""
        return f"numidium.extensions.{self.path.stem}"

    def import_module(self) -> ExtensionProtocol:
        importlib.invalidate_caches()

        try:
            module = sys.modules[self.module_name]
        except KeyError:
            module = importlib.import_module(self.module_name)
        else:
            importlib.reload(module)

        assert callable(module.register)
        assert callable(module.unregister)

        return cast(ExtensionProtocol, module)

    @staticmethod
    def from_path(path: Path) -> Extension | None:
        """Create a new extension from the given path, if it contains the required files."""
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
            if not isinstance(table.get(key), str):
                logger.warning("Invalid {} in `tool.numidium`: {}", key, toml_path)
                return None

        return Extension(path, *GET_TOML_ITEMS(table))
