# Copyright Contributors to the Packit project.
# SPDX-License-Identifier: MIT

import collections
import re
from typing import List, Optional, SupportsIndex, Union, cast, overload

from specfile.constants import SECTION_NAMES

# name for the implicit "preamble" section
PREAMBLE = "package"


class Section(collections.UserList):
    """
    Class that represents a spec file section.

    Attributes:
        name: Name of the section (without the leading '%').
        data: List of lines forming the content of the section, not including newline characters.
    """

    def __init__(self, name: str, data: Optional[List[str]] = None) -> None:
        super().__init__()
        if not name or name.split()[0].lower() not in SECTION_NAMES:
            raise ValueError(f"Invalid section name: '{name}'")
        self.name = name
        if data is not None:
            self.data = data.copy()

    def __str__(self) -> str:
        data = "".join(f"{i}\n" for i in self.data)
        if self.name == PREAMBLE:
            return data
        return f"%{self.name}\n{data}"

    def __repr__(self) -> str:
        data = repr(self.data)
        return f"Section('{self.name}', {data})"

    def __copy__(self) -> "Section":
        return Section(self.name, self.data)

    @overload
    def __getitem__(self, i: SupportsIndex) -> str:
        pass

    @overload
    def __getitem__(self, i: slice) -> "Section":
        pass

    def __getitem__(self, i):
        if isinstance(i, slice):
            return Section(self.name, self.data[i])
        else:
            return self.data[i]

    @property
    def normalized_name(self) -> str:
        """Normalized name of the section. All characters are lowercased."""
        return self.name.lower()

    def copy(self) -> "Section":
        return Section(self.name, self.data)

    def get_raw_data(self) -> List[str]:
        if self.name == PREAMBLE:
            return self.data
        return [f"%{self.name}"] + self.data


class Sections(collections.UserList):
    """
    Class that represents all spec file sections, hence the entire spec file.

    Sections can be accessed by index or conveniently by name as attributes:
    ```
    # print the third line of the first section
    print(sections[0][2])

    # remove the last line of %prep section
    del sections.prep[-1]

    # replace the entire %prep section
    sections.prep = ['line 1', 'line 2']

    # delete %changelog
    del sections.changelog
    ```

    Attributes:
        data: List of individual sections. Preamble is expected to always be the first.
    """

    def __str__(self) -> str:
        return "".join(str(i) for i in self.data)

    def __repr__(self) -> str:
        data = repr(self.data)
        return f"Sections({data})"

    def __copy__(self) -> "Sections":
        return Sections(self.data)

    def __contains__(self, name: object) -> bool:
        try:
            # use parent's __getattribute__() so this method can be called from __getattr__()
            data = super().__getattribute__("data")
        except AttributeError:
            return False
        return any(s.name.lower() == cast(str, name).split()[0].lower() for s in data)

    def __getattr__(self, name: str) -> Section:
        if name not in self:
            return super().__getattribute__(name)
        try:
            return self.get(name)
        except ValueError:
            raise AttributeError(name)

    def __setattr__(self, name: str, value: Union[Section, List[str]]) -> None:
        if name not in self:
            return super().__setattr__(name, value)
        try:
            if isinstance(value, Section):
                self.data[self.find(name)] = value
            else:
                self.data[self.find(name)].data = value
        except ValueError:
            raise AttributeError(name)

    def __delattr__(self, name: str) -> None:
        if name not in self:
            return super().__delattr__(name)
        try:
            del self.data[self.find(name)]
        except ValueError:
            raise AttributeError(name)

    def get(self, name: str) -> Section:
        return self.data[self.find(name)]

    def find(self, name: str) -> int:
        name = name.lower()
        for i, section in enumerate(self.data):
            if section.name.lower() == name:
                return i
        raise ValueError

    @classmethod
    def parse(cls, lines: List[str]) -> "Sections":
        """
        Parses given lines into sections.

        Args:
            lines: Lines to parse.

        Returns:
            Constructed instance of `Sections` class.
        """
        section_name_regexes = [
            re.compile(rf"^%{re.escape(n)}(\s+.*$|$)", re.IGNORECASE)
            for n in SECTION_NAMES
        ]
        section_starts = []
        for i, line in enumerate(lines):
            if line.startswith("%"):
                for r in section_name_regexes:
                    if r.match(line):
                        section_starts.append(i)
                        break
        section_starts.append(len(lines))
        data = [Section(PREAMBLE, lines[: section_starts[0]])]
        for start, end in zip(section_starts, section_starts[1:]):
            data.append(Section(lines[start][1:], lines[start + 1 : end]))
        return cls(data)

    def get_raw_data(self) -> List[str]:
        result = []
        for section in self.data:
            result.extend(section.get_raw_data())
        return result
