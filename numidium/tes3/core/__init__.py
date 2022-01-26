from __future__ import annotations

from pathlib import Path

from numidium.config import config
from numidium.logger import logger
from numidium.tes3.ini import MorrowindIni

__all__ = ["MorrowindInstall"]


# TODO: Add unit tests.
class MorrowindInstall:
    """An in-memory representation of a Morrowind install.

    Attributes
    ----------
    """

    workspace: Path
    ini: MorrowindIni

    def load(self, workspace: str) -> None:
        # """Loads the Morrowind install within a given workspace into memory."""
        self.workspace = Path(workspace)
        self.ini = MorrowindIni()
        try:
            self.ini.load_path(self.ini_path)
        except Exception as e:
            logger.error("Morrowind.ini does not exist: %s", self.ini_path)
            raise e

    @property
    def exe_path(self) -> Path:
        return self.workspace / "Morrowind.exe"

    @property
    def ini_path(self) -> Path:
        return self.workspace / "Morrowind.ini"

    @property
    def data_files_path(self) -> Path:
        return self.workspace / "Data Files"

    @property
    def saves_path(self) -> Path:
        return self.workspace / "Saves"

    @property
    def screenshots_path(self) -> Path:
        return self.workspace / "Screenshots"
