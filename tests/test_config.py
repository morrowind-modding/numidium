from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from numidium.config import Config

test_case_args = ["json_str", "config"]
test_vase_vals = [
    ('{"active_extensions":[]}', Config(active_extensions=[])),
    ('{"active_extensions":["a"]}', Config(active_extensions=["a"])),
    ('{"active_extensions":["a","b"]}', Config(active_extensions=["a", "b"])),
]


@pytest.mark.parametrize(test_case_args, test_vase_vals)
def test_load(json_str: str, config: Config) -> None:
    c = Config()
    c.load(StringIO(json_str))
    assert c == config


@pytest.mark.parametrize(test_case_args, test_vase_vals)
def test_save(json_str: str, config: Config) -> None:
    with StringIO() as f:
        config.save(f)
        assert f.getvalue() == json_str


@pytest.mark.parametrize(test_case_args, test_vase_vals)
def test_load_save(json_str: str, config: Config) -> None:
    c = Config()

    with StringIO() as f:
        c.save(f)
        f.seek(0)
        config.load(f)
        assert c == config


def test_backup_created() -> None:
    with TemporaryDirectory() as dir:
        config_path = Path(dir) / "config.json"
        backup_path = Path(dir) / "config.backup.json"

        config = Config()
        config.save_path(config_path)  # 1st call to create config file
        config.save_path(config_path)  # 2nd call should build a backup
        assert backup_path.exists()
