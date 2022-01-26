from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from os import PathLike
from pathlib import Path
from typing import Any, TextIO

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

    active_workspace: str = ""
    recent_workspaces: dict[str, int] = field(default_factory=dict)

    show_welcome: bool = True
    setup_completed: bool = False

    def load(self, reader: TextIO) -> None:
        """Update this config with the contents of the given reader."""
        self.update(**json.load(reader))

    def save(self, writer: TextIO) -> None:
        """Save the config contents to the given writer."""
        json.dump(asdict(self), writer, indent=4)

    def load_path(self, path: AnyPath = CONFIG_PATH) -> None:
        """Update this config with the contents of the given path."""
        self.load(open(path, mode="r"))

    def save_path(self, path: AnyPath = CONFIG_PATH) -> None:
        """Save the contents of this config to the given path.

        For safety, if a file already exists at the given path it will be
        renamed with a ".backup.json" suffix.
        """
        logger.info("Saving config: {}", path)
        self.create_backup(path)
        self.save(open(path, mode="w"))

    def update(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def reset(self) -> None:
        self.update(**asdict(Config()))

    @staticmethod
    def create_backup(path: AnyPath) -> None:
        path = Path(path)
        if path.exists():
            backup_path = path.with_suffix(".backup" + path.suffix)
            backup_path.unlink(missing_ok=True)
            try:
                path.rename(backup_path)
            except OSError as e:
                logger.warning("Failed to create backup: {} -> {}", path, backup_path)
                logger.warning("\t{}", e)
                raise e


config = Config()
try:
    config.load_path(CONFIG_PATH)
except FileNotFoundError:
    pass  # using default config
