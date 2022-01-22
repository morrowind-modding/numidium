import os
import platform
import subprocess
from pathlib import Path


class OperatingSystemUtility:
    """
    Convenience class for operating system methods, such as platform-agnostic system interactions: opening a file in default application, opening explorer, etc.
    """

    def open_filepath_with_default_application(self, filepath: str) -> None:
        self._open_filepath_with_os(filepath)

    def open_filepath_with_explorer(self, filepath: str) -> None:
        directory: str = Path(filepath).parent
        self._open_filepath_with_os(directory)

    def _open_filepath_with_os(self, filepath: str) -> None:
        if platform.system() == "Darwin":  # macOS
            subprocess.call(("open", filepath))
        elif platform.system() == "Windows":  # Windows
            os.startfile(filepath)
        else:  # linux variants
            subprocess.call(("xdg-open", filepath))
