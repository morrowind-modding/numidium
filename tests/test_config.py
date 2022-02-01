from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

from numidium.config import Config


def test_load_save() -> None:
    c = Config()

    with StringIO() as f:
        c.save(f)
        f.seek(0)

        c2 = Config()
        c2.load(f)
        assert c == c2


def test_backup_created() -> None:
    with TemporaryDirectory() as dir:
        config_path = Path(dir) / "config.json"
        backup_path = Path(dir) / "config.backup.json"

        config = Config()
        config.save_path(config_path)  # 1st call to create config file
        config.save_path(config_path)  # 2nd call should build a backup
        assert backup_path.exists()
