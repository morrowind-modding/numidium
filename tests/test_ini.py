from io import BytesIO
from pathlib import Path

from numidium.tes3 import MorrowindIni

BASE_INI_PATH = Path(__file__) / "../assets/Morrowind.ini"


def test_morrowind_ini() -> None:
    ini = MorrowindIni()
    ini.load_path(BASE_INI_PATH)

    assert ini.game_files == ["Morrowind.esm", "Tribunal.esm", "Bloodmoon.esm"]
    assert ini.archives == ["Tribunal.bsa", "Bloodmoon.bsa"]


def test_load_save() -> None:
    ini = MorrowindIni()
    ini.load_path(BASE_INI_PATH)

    with BytesIO() as f:
        ini.save(f)
        result = f.getvalue()
        expect = BASE_INI_PATH.read_bytes()
        assert result == expect


def test_append_archive() -> None:
    # fmt: off
    setup = (
        b"[Archives]\r\n"
        b"Archive 0=A.bsa\r\n"
        b"Archive 1=B.bsa\r\n"
    )
    expect = (
        b"[Archives]\r\n"
        b"Archive 0=A.bsa\r\n"
        b"Archive 1=B.bsa\r\n"
        b"Archive 2=C.bsa\r\n"
    )
    # fmt: on

    ini = MorrowindIni()
    ini.load(BytesIO(setup))

    # ensure append works
    ini.archives.append("C.bsa")
    assert ini.archives == ["A.bsa", "B.bsa", "C.bsa"]
    assert ini.game_files == []

    # ensure saving works
    with BytesIO() as f:
        ini.save(f)
        result = f.getvalue()
        assert result == expect


def test_append_game_file() -> None:
    # fmt: off
    setup = (
        b"[Game Files]\r\n"
        b"GameFile0=A.esm\r\n"
        b"GameFile1=B.esm\r\n"
        b"GameFile2=C.esm\r\n"
    )
    expect = (
        b"[Game Files]\r\n"
        b"GameFile0=A.esm\r\n"
        b"GameFile1=B.esm\r\n"
        b"GameFile2=C.esm\r\n"
        b"GameFile3=D.esm\r\n"
    )
    # fmt: on

    ini = MorrowindIni()
    ini.load(BytesIO(setup))

    # ensure append works
    ini.game_files.append("D.esm")
    assert ini.game_files == ["A.esm", "B.esm", "C.esm", "D.esm"]

    # ensure saving works
    with BytesIO() as f:
        ini.save(f)
        result = f.getvalue()
        assert result == expect


def test_section_comments_preserved() -> None:
    # fmt: off
    setup = (
        b"[Archives]\r\n"
        b"Archive 0=A.bsa;A\r\n"
        b"Archive 1=B.bsa; B\r\n"
        b"Archive 2=C.bsa ;C\r\n"
    )
    expect = (
        b"[Archives]\r\n"
        b"Archive 0=A.bsa;A\r\n"
        b"Archive 1=B.bsa; B\r\n"
        b"Archive 2=C.bsa ;C\r\n"
    )
    # fmt: on

    with BytesIO() as f:
        ini = MorrowindIni()
        ini.load(BytesIO(setup))
        ini.save(f)

        result = f.getvalue()
        assert result == expect
