import os
import platform
import subprocess
from pathlib import Path
from typing import Any, Callable, Generic, TypeVar


class OperatingSystemUtility:
    """
    Convenience class for operating system methods, such as platform-agnostic system interactions: opening a file in default application, opening explorer, etc.
    """

    def open_filepath_with_default_application(self, filepath: str) -> None:
        self._open_filepath_with_os(filepath)

    def open_filepath_with_explorer(self, filepath: str) -> None:
        directory: Path = Path(filepath).parent
        self._open_filepath_with_os(str(directory))

    def _open_filepath_with_os(self, filepath: str) -> None:
        if platform.system() == "Darwin":  # macOS
            subprocess.call(("open", filepath))
        elif platform.system() == "Windows":  # Windows
            os.startfile(filepath)
        else:  # linux variants
            subprocess.call(("xdg-open", filepath))


T = TypeVar("T")


class staticproperty(Generic[T]):
    __slots__ = ("func",)

    def __init__(self, func: Callable[[], T]) -> None:
        self.func = func

    def __get__(self, _obj: Any, _type: Any) -> T:
        return self.func()
