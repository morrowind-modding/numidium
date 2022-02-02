from __future__ import annotations

import dataclasses
import json
from dataclasses import MISSING, dataclass, field
from datetime import datetime
from os import PathLike
from pathlib import Path
from typing import Any, TextIO

from platformdirs import user_config_dir

AnyPath = str | PathLike[str]

CONFIG_ROOT = Path(user_config_dir("numidium", appauthor=False))
CONFIG_ROOT.mkdir(parents=True, exist_ok=True)

CONFIG_PATH = CONFIG_ROOT / "config.json"


@dataclass
class ConfigBase:
    """Base class for managing json-backed configuration files."""

    __slots__ = ()

    def load(self, reader: TextIO) -> None:
        """Update the config with contents from the given reader."""
        self.update(json.load(reader))

    def save(self, writer: TextIO) -> None:
        """Save the config contents to the given writer."""
        json.dump(self.asdict(), writer, indent=4)

    def load_path(self, path: AnyPath) -> None:
        """Update this config with the contents of the given path."""
        self.load(open(path, mode="r"))

    def save_path(self, path: AnyPath) -> None:
        """Save the contents of this config to the given path."""
        self.save(open(path, mode="w"))

    def update(self, obj: dict[str, Any]) -> None:
        """Update the config with contents from the given dict."""
        for f in dataclasses.fields(self):
            if f.name in obj:
                setattr(self, f.name, obj[f.name])

    def reset(self) -> None:
        """Reset the config's values back to their defaults.

        An exception will be raised if any attributes had no default specified.
        """
        for f in dataclasses.fields(self):
            setattr(self, f.name, f.default_factory() if (v := f.default) is MISSING else v)

    def asdict(self) -> dict[str, Any]:
        """Convert the config into a regular dict object."""
        return dataclasses.asdict(self)


@dataclass
class Config(ConfigBase):
    """Manages the application's configuration file.

    Use `load_path` to load changes from a file path.
    Use `save_path` to save changes into a file path.

    Attributes
    ----------
    show_welcome : bool
        Show the welcome screen on startup.
    active_extensions : list[str]
        The currently active extensions.
    recent_workspaces : dict[str int]
        A mapping of workspaces and the timestamps of when they were last opened.
    """

    show_welcome: bool = True

    active_extensions: list[str] = field(default_factory=list)
    recent_workspaces: dict[str, int] = field(default_factory=dict)

    def load_path(self, path: AnyPath = CONFIG_PATH) -> None:
        super().load_path(path)

    def save_path(self, path: AnyPath = CONFIG_PATH) -> None:
        self.create_backup(path)
        super().save_path(path)

    @staticmethod
    def create_backup(path: AnyPath) -> None:
        path = Path(path)
        if path.exists():
            backup_path = path.with_suffix(".backup" + path.suffix)
            backup_path.unlink(missing_ok=True)
            path.rename(backup_path)

    @property
    def active_workspace(self) -> str:
        return next(iter(self.recent_workspaces), "")

    @active_workspace.setter
    def active_workspace(self, workspace: str) -> None:
        self.recent_workspaces[workspace] = int(datetime.now().timestamp())
        items = list(self.recent_workspaces.items())
        items.sort(key=lambda x: x[1], reverse=True)
        self.recent_workspaces.clear()
        self.recent_workspaces.update(items)
        self.save_path()


config = Config()
try:
    config.load_path(CONFIG_PATH)
except (FileNotFoundError, json.JSONDecodeError):
    config.save_path(CONFIG_PATH)
