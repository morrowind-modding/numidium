from pathlib import Path

from . import _dds  # type: ignore


def decompress(path: Path | str) -> tuple[bytes, int, int]:
    output = _dds.decompress(str(path))
    return output.data, output.width, output.height
