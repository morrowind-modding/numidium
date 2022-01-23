from __future__ import annotations

from pathlib import Path

from numidium.logger import logger
from numidium.tes3.ini import MorrowindIni

__all__ = ["MorrowindInstall"]


# TODO: Add unit tests.
class MorrowindInstall:
    """An in-memory representation of a Morrowind install.

    Attributes
    ----------
    """

    workspace: str

    path_morrowind_executable: Path
    path_morrowind_ini: Path

    directory_datafiles: Path
    directory_saves: Path
    directory_screenshots: Path

    ini: MorrowindIni

    def load(self, workspace: str) -> None:
        """Loads the Morrowind install within a given workspace into memory."""
        self.workspace = workspace

        # Load relative file paths.
        self.path_morrowind_executable = Path(self.workspace).joinpath("Morrowind").with_suffix(".exe")
        self.path_morrowind_ini = Path(self.workspace).joinpath("Morrowind").with_suffix(".ini")
        self.directory_datafiles = Path(self.workspace).joinpath("Data Files")
        self.directory_saves = Path(self.workspace).joinpath("Saves")
        self.directory_screenshots = Path(self.workspace).joinpath("Screenshots")

        # Check existence of files.
        for path in (self.path_morrowind_executable, self.path_morrowind_ini):
            if not path.exists():
                logger.error("File not found when loading Morrowind Install: %s", str(path))
                raise FileNotFoundError(path)
        logger.debug("Loaded Morrowind install filepaths and verified existence.")

        # Load INI file
        self.ini = MorrowindIni()
        self.ini.load_path(self.path_morrowind_ini)
        logger.debug("Loaded Morrowind INI into memory.")

        # TODO: Load other things
