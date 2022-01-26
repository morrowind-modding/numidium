from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import BinaryIO, Iterator

__all__ = ["MorrowindIni"]

PATTERN_SECTION_HEADER = re.compile(rb"^\[([^;]+)\]")
PATTERN_GAME_FILE = re.compile(rb"GameFile\d+=([^;]+)")
PATTERN_ARCHIVE = re.compile(rb"Archive \d+=([^;]+)")


class IniSection:
    """Represents a section of an ini file.

    Sections are the areas following a bracketed header. They include all
    the following lines until a new header is encountered or the file ends.

    Example:
    ```ini
        [Game Files]
        GameFile0=Morrowind.esm
        GameFile1=Tribunal.esm
        GameFile2=Bloodmoon.esm
    ```
    """

    lines: list[bytes]

    def __init__(self) -> None:
        self.lines = []

    def add_line(self, line: bytes) -> None:
        self.lines.append(line)

    def trim_trailing_lines(self) -> None:
        if any(self.lines):
            while not self.lines[-1].strip():
                self.lines.pop()


class IniFile:
    """Represents an entire ini file.

    Ini files contain various sections, annotated by bracketed headers.

    Attributes
    ----------
    sections : dict[str, IniSection]
        A dictionary of header strings and their associated sections.
    """

    sections: defaultdict[str, IniSection]

    def __init__(self) -> None:
        self.sections = defaultdict(IniSection)

    def load(self, reader: BinaryIO) -> None:
        """Load all sections from a readable object."""
        self.sections.clear()

        # initial section header (used for orphaned lines)
        header: str = ""

        # populate the sections dict with associated lines
        for line in reader.read().splitlines():
            if match := PATTERN_SECTION_HEADER.match(line):
                header = match.group(1).decode()
            else:
                self.sections[header].add_line(line)

        # trim any trailing white space after sections
        # required so that future appends look correct
        for section in self.sections.values():
            section.trim_trailing_lines()

    def save(self, writer: BinaryIO) -> None:
        """Write all sections to a writeable object."""
        last_section = self._get_last_section()
        for header, section in self.sections.items():
            if any(section.lines):
                # section header
                if header:
                    writer.write(f"[{header}]".encode())
                    writer.write(b"\r\n")
                # section lines
                for line in section.lines:
                    writer.write(line)
                    writer.write(b"\r\n")
                # section spacer
                if section is not last_section:
                    writer.write(b"\r\n")

    def load_path(self, path: Path | bytes | str) -> None:
        """Load all sections from the given path."""
        with open(path, mode="rb") as f:
            self.load(f)

    def save_path(self, path: Path | bytes | str) -> None:
        """Save all sections from the given path."""
        with open(path, mode="wb") as f:
            self.save(f)

    def _get_file_names(self, section_name: str, pattern: re.Pattern[bytes]) -> Iterator[str]:
        """Extract file names using the given regex pattern."""
        section = self.sections[section_name]
        for match in filter(None, map(pattern.match, section.lines)):
            try:
                yield match.group(1).decode("cp1252")
            except UnicodeDecodeError as e:
                raise e

    def _get_last_section(self) -> IniSection | None:
        """Get the last valid section in the file."""
        for section in reversed(self.sections.values()):
            if any(map(bytes.strip, section.lines)):
                return section
        return None

    def _get_commented_values(self, section: IniSection) -> dict[str, str]:
        result = {}
        for line in map(bytes.strip, section.lines):
            i, j = line.find(b"="), line.find(b";")
            if (i != -1) and (j != -1):
                value = line[i + 1 :].decode("cp1252")  # after "="
                key = value[: j - i - 1].lower()  # from "=" to ";"
                result[key] = value
        return result


class MorrowindIni(IniFile):
    """An in-memory representation of the `Morrowind.ini` file.

    Attributes
    ----------
    archives : list[str]
        The list of currently active (.bsa) archives.
    game_files : list[str]
        The list of currently active (.esp / .esm) files.
    """

    archives: list[str]
    game_files: list[str]

    def load(self, reader: BinaryIO) -> None:
        super().load(reader)
        self.archives = list(self._get_file_names("Archives", PATTERN_ARCHIVE))
        self.game_files = list(self._get_file_names("Game Files", PATTERN_GAME_FILE))

    def save(self, writer: BinaryIO) -> None:
        self._sync_archives()
        self._sync_game_files()
        super().save(writer)

    def _sync_archives(self) -> None:
        """Synchronize the 'Archives' section with our `archives` list."""
        section = self.sections["Archives"]
        values = self._get_commented_values(section)
        section.lines = [
            f"Archive {i}={values.get(v.lower(), v)}".encode("cp1252")
            for i, v in enumerate(self.archives)  # fmt: skip
        ]

    def _sync_game_files(self) -> None:
        """Synchronize the 'Game Files' section with our `game_files` list."""
        section = self.sections["Game Files"]
        values = self._get_commented_values(section)
        section.lines = [
            f"GameFile{i}={values.get(v.lower(), v)}".encode("cp1252")
            for i, v in enumerate(self.game_files)  # fmt: skip
        ]
