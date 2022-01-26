from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from os import PathLike
from pathlib import Path
from typing import TextIO

from platformdirs import user_config_dir

from numidium.logger import logger

AnyPath = str | PathLike[str]

CONFIG_ROOT = Path(user_config_dir("numidium", appauthor=False))
CONFIG_PATH = CONFIG_ROOT / "config.json"

logger.info("CONFIG_ROOT: {}", CONFIG_ROOT)
logger.info("CONFIG_PATH: {}", CONFIG_PATH)


@dataclass
class Config:
    """Manages the application's configuration file.

    Use `load_path` to load changes from a file path.
    Use `save_path` to save changes into a file path.

    Attributes
    ----------
    active_extensions : list[str]
        The currently active extensions.
    """

    active_extensions: list[str] = field(default_factory=list)

    def load(self, reader: TextIO) -> None:
        """Update this config with the contents of the given reader."""
        try:
            contents = json.load(reader)
        except json.JSONDecodeError as e:
            logger.warning("Failed to load config: {}", reader)
            logger.warning("\t{}", e)
            raise e

        try:
            type(self).__init__(self, **contents)
        except TypeError as e:
            logger.warning("Invalid config contents: {}", contents)
            logger.warning(e)

    def save(self, writer: TextIO) -> None:
        """Save the config contents to the given writer."""
        try:
            json.dump(asdict(self), writer, separators=(",", ":"))
        except OSError as e:
            logger.warning("Failed to save config: {}", writer)
            logger.warning("\t{}", e)

    def load_path(self, path: AnyPath = CONFIG_PATH) -> None:
        """Update this config with the contents of the given path."""
        self.load(open(path, mode="r"))

    def save_path(self, path: AnyPath = CONFIG_PATH) -> None:
        """Save the contents of this config to the given path.

        For safety, if a file already exists at the given path it will be
        renamed with a ".backup.json" suffix.
        """
        logger.info("Saving config: {}", path)

        path = Path(path)
        if path.exists():
            backup_path = path.with_suffix(".backup.json")
            backup_path.unlink(missing_ok=True)
            try:
                path.rename(backup_path)
            except OSError as e:
                logger.warning("Failed to create backup: {} -> {}", path, backup_path)
                logger.warning("\t{}", e)
                raise e

        self.save(open(path, mode="w"))


config = Config()
try:
    config.load_path(CONFIG_PATH)
except FileNotFoundError:
    pass  # using default config
