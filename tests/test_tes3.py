from numidium import tes3


def test_load() -> None:
    plugin = tes3.Plugin.load("tests/assets/OAAB_Data.esm")
    header = plugin.objects[0]

    assert type(header) is tes3.Header
    assert header.flags1 == 0
    assert header.flags2 == 0
    assert header.version <= 1.3
    assert header.file_type == tes3.FileType.Esm
    assert header.author == ""
    assert header.description == ""
    assert header.num_objects == 3656
    assert header.masters == [("Morrowind.esm", 79837557), ("Tribunal.esm", 4565686), ("Bloodmoon.esm", 9631798)]
