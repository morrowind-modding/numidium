from dataclasses import dataclass, field
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

from numidium.config import Config, ConfigBase


def test_load() -> None:
    config = ConfigBase()

    # ensure empty jsons do not error
    with StringIO(r"{}") as reader:
        config.load(reader)
        assert config.asdict() == {}


def test_save() -> None:
    config = ConfigBase()

    with StringIO() as stream:
        config.save(stream)
        assert stream.getvalue() == r"{}"


def test_update() -> None:
    config = ConfigBase()

    config.update({})
    assert config.asdict() == {}


def test_reset() -> None:
    config = ConfigBase()

    config.reset()
    assert config.asdict() == {}


def test_load_save() -> None:
    config = ConfigBase()

    with StringIO() as stream:
        config.save(stream)
        stream.seek(0)
        config.load(stream)
        assert config == ConfigBase()


def test_load_save_path() -> None:
    config = ConfigBase()

    with TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / "config.json"

        config.save_path(path)
        assert path.read_text() == r"{}"

        config.load_path(path)
        assert config == ConfigBase()


def test_backup_created() -> None:
    with TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir) / "config.json"
        backup_path = Path(temp_dir) / "config.backup.json"

        config = Config()
        config.save_path(config_path)  # 1st call to create config file
        config.save_path(config_path)  # 2nd call should build a backup
        assert backup_path.exists()


def test_subclass() -> None:
    import json

    test_obj = {"value": 1, "items": {"2": 3}}
    test_str = json.dumps(test_obj, indent=4)

    @dataclass
    class CustomConfig(ConfigBase):
        value: int = 0
        items: dict[str, int] = field(default_factory=dict)

    config = CustomConfig()

    config.update(test_obj)
    assert config.asdict() == test_obj

    config.reset()
    assert config == CustomConfig()

    with StringIO(test_str) as stream:
        config.load(stream)
        assert config.asdict() == test_obj

        stream.seek(0)
        config.save(stream)
        assert stream.getvalue() == test_str
