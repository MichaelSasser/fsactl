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

import shutil

from pathlib import Path
from typing import Any
from typing import Callable
from typing import List
from typing import Optional
from typing import Set

from fsactl.handlers.git import Git
from fsactl.typing import YAML

from .worker import Worker


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


class GitWorker(Worker):
    IGNORE_COPY: Callable[[Any, List[str]], Set[str]] = shutil.ignore_patterns(
        ".git"
    )

    def __init__(
        self, addon_dir: Path, community_dir: Path, addon: YAML
    ) -> None:
        super().__init__(addon_dir, community_dir, addon)

        self.addon_path = self.addon_dir / self.addon["github"].replace(
            "/", "--"
        )

        self.origin: str = f"https://github.com/{self.addon['github']}.git"
        self.vcs: Optional[Git] = None

    def download(self) -> None:
        if not self.addon_path.is_dir():  # If dir not already exists
            # Clone the new addon to the addon directory

            print(f"Downloading new addon {self.origin} to {self.addon_path}")
            self.vcs = Git.clone(self.origin, self.addon_path)

    def update(self) -> None:
        # TODO: mechanisem branch/status something:
        #   - fetch and checkout newest tag
        #   - just pull
        #   - switch to "master" and pull (Not all have a master)
        # currently: just update whatever
        if not self.vcs:
            self.vcs = Git(self.addon_path)

        print(f"{self.addon_path.name:60}", end="")
        self.vcs.pull()

    def install(self, force: bool = True) -> None:
        if not self.vcs:
            self.vcs = Git(self.addon_path)

        print(f"\n{self.addon_path.name}")

        # print(self)
        copy_dir: Optional[Path] = self._find_dir_to_install()
        if copy_dir is None:  # TODO: Do something, when None
            return
        # print(f"{copy_dir=}")
        self.community_path = self.community_dir / copy_dir.name
        # print(f"{self.community_path=}")

        if self.vcs.has_updated or not self.community_path.is_dir() or force:
            shutil.rmtree(self.community_path, ignore_errors=True)

            try:
                # The git directory leaves behind linked files,
                # that can not be deleted by rmtree.
                # TODO: Maybe use the kernel.dll to unlink the file
                # that fails on rmtree and unlink it (should be noted
                # in 'e') and re-run the function.
                shutil.copytree(
                    self.addon_path,
                    self.community_path,
                    ignore=self.__class__.IGNORE_COPY,
                )
            except FileExistsError:
                # Should not happen, due to the prevention, that the git
                # directory is beeing copied.
                # Will happen, if copied manuelly.
                # print(f"{self.addon_path=} -> {self.community_path}, {e=}")
                # sys.exit(1)
                raise FileExistsError(
                    "Maybe there is a linked file that coud not be deleted."
                )


# vim: set ft=python :
