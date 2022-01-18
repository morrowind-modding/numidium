from pathlib import Path

from numidium.core.extensions import available_extensions


def test_available_extensions() -> None:
    for ext in available_extensions():
        assert ext.name == "example"
        assert ext.version == "0.1.0"
        assert ext.description == "An example plugin."
        assert ext.authors == ["Greatness7 <Greatness7@gmail.com>"]
