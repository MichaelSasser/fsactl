#!/usr/bin/env python
# fsactl - install and manage your MSFS2020 addons
# Copyright (C) 2020  Michael Sasser <Michael@MichaelSasser.org>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any
from typing import Generator
from typing import Optional

from jinja2 import Template

from fsactl.typing import YAML

__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


class Worker:
    LN_PATH_HINTS: tuple[str, str, str, str, str, str] = (
        "ModelBehaviorDefs",
        "SimObjects",
        "html_ui",
        "effects",
        "layout.json",
        "manifest.json",
    )

    LN_FILE_EXT_HINTS: tuple[str, Any] = ("locPak",)

    def __init__(self, addon_dir: Path, community_dir: Path,
                 addon: YAML) -> None:
        self.addon = addon
        self.addon_dir: Path = addon_dir
        self.community_dir: Path = community_dir

        self.addon_path: Optional[Path] = None
        self.community_path: Optional[Path] = None

    def download(self) -> None:
        raise NotImplementedError()

    def update(self) -> None:
        raise NotImplementedError()

    def make(self) -> bool:  # generic

        if "build" in self.addon:
            for build in self.addon["build"]:

                # Render path  # TODO: try/except
                path: Path = Path(
                    Template(
                        build["path"]).render(addon_path=str(self.addon_path)))

                # Render command
                command: str = Template(
                    build["command"]).render(addon_path=str(self.addon_path))

                # print(f"{str(path)=:80} -> {command=}")

                try:
                    os.chdir(path)
                except (OSError, FileNotFoundError, PermissionError,
                        NotADirectoryError):
                    print(
                        f"There is something wrong with the directory: {str(path)}"
                    )
                print(f"\n\n{self.addon_path.name}\n")
                result = subprocess.run(command, shell=True, check=True)
                return True if result.returncode != 0 else False

    def install(self) -> None:
        # part generic
        raise NotImplementedError()

    def remove(self) -> None:
        # generic
        raise NotImplementedError()

    def _find_dir_to_install(
            self) -> Optional[Path]:  # If root return after --
        for hint in self.__class__.LN_PATH_HINTS:
            result = self.__hint_checker(hint)
            if result is not None:
                return result

        for hint in self.__class__.LN_FILE_EXT_HINTS:
            result = self.__hint_checker(f"*.{hint}")
            if result is not None:
                return result
        return None  # No path found

    def __hint_checker(self, hint: str) -> Optional[Path]:
        locations: Generator[Path, None,
                             None] = list(self.addon_path.rglob(hint))
        if len(locations) == 1:
            return locations[0].parent
        return None

    def __repr__(self) -> str:
        return f"{self.__class__.__module__}.{self.__class__.__qualname__}({self.addon})"

    def __str__(self) -> str:
        return self.__repr__()

# vim: set ft=python :
