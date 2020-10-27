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

import re
import time

from pathlib import Path
from typing import List
from typing import Pattern

from .typing import YAML
from .workers.git import GitWorker
from .workers.worker import Worker


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


class Addons:
    VERSION_CHECK: Pattern[str] = re.compile(r"[0-9.]")

    # IGNORE_GIT: Callable = shutil.ignore_patterns(".git")

    def __init__(self, config: YAML) -> None:

        self.addon_dir = Path(config["msfs"]["addon_dir"])
        self.community_dir = Path(config["msfs"]["community_dir"])
        self.addons: YAML = config["msfs"]["addons"]

        self.workers: List[Worker] = []

        # Add an addon_path to the dict
        for addon in self.addons:
            if "github" in addon:  # Later use
                self.workers.append(
                    GitWorker(self.addon_dir, self.community_dir, addon)
                )

        # pprint(self.workers)
        # self.addons_vcs: list[Git] = []
        # print([addon["github"] for addon in self.addons])

        # self.__scan_for_vcs()

    # def __scan_for_vcs(self):
    #    if not self.addon_dir.is_dir():
    #        raise ValueError("The addon directory must be a directory.")
    #    directories: list[Path] = [addon for addon in
    #                               self.addon_dir.iterdir()
    #    ]
    #    for directory in directories:
    #        try:
    #            temp = Git(directory)
    #        except git.exc.InvalidGitRepositoryError:
    #            continue
    #        self.addons_vcs.append(temp)

    def download(self) -> None:  # NEW
        if len(self.workers) < 1:
            return  # Do nothing, if there are no addons configured
        print("\n\nDownloading...\n\n")
        for worker in self.workers:
            worker.download()

    def install(self, force: bool = True) -> None:
        print("\n\nInstalling...\n\n")
        for worker in self.workers:
            worker.install(force)

    # def update_tag(self, master: bool = False):
    #     def normalize(version: str):
    #         version = str(version).removeprefix("v").removeprefix("V")
    #         if self.__class__.VERSION_CHECK.fullmatch(version):
    #             return None
    #         if version.count(".") < 2:
    #             version = version + ".0"
    #         return version
    #
    #     print("\nChecking for newest stable release\n")
    #     for repo in self.addons_vcs:
    #         if master:
    #             repo.checkout("master")
    #             continue
    #
    #         newest: Optional[git.TagReference] = None
    #         for tag in sorted(repo.tags,
    #                           key=lambda t: t.commit.committed_date,
    #                           reverse=True):
    #             tag_str: str = normalize(str(tag))
    #             newest_str: str = normalize(str(newest))
    #
    #             # print(tag_str, end=" | ")
    #             try:
    #                 semver.VersionInfo.parse(
    #                     tag_str)  # Don't do anything with it
    #             except ValueError:
    #                 continue
    #             if newest is None:
    #                 newest = tag
    #                 continue
    #             try:
    #                 if semver.compare(tag_str, newest_str) > 0:
    #                     newest = tag
    #             except ValueError:
    #                 continue
    #         # print("Newest:", newest_str)
    #         if newest is not None:  # Found tags
    #             print(f"{repo.name:35} [{newest_str}]")
    #             repo.checkout(newest)  # TODO: else master
    #     # print(f"The new addon {repo.origin} does not use tags")
    #     # print(f"Found latest tag of the new addon {repo.origin}")

    def update(self) -> None:  # NEW
        print("\n\nUpdating...\n\n")
        for worker in self.workers:
            worker.update()
        # self, fetch: bool = False
        # print("Fetching updates")
        # for addon in self.addons_vcs:
        #    print(f"{addon.name:35}", end="")
        #    if fetch:
        #        addon.fetch()
        #    else:
        #        addon.pull()

    # def copy_updated(self, force: bool = False) -> None:
    #     copy_dirs: list[Copy] = []
    #     for addon in self.addons_vcs:
    #         src: Path = self.__find_dir_to_link(addon)
    #         dest: Path = self.community_dir / src.name
    #         # Only copy if updated or new
    #         if addon.has_updated or not dest.is_dir() or force:
    #             copy_dirs.append(Copy(src=src, dest=dest))
    #     # print(links)
    #     for copy_dir in copy_dirs:
    #
    #         shutil.rmtree(copy_dir.dest, ignore_errors=True)
    #
    #         try:
    #             # The git directory leaves behind linked files,
    #             # that can not be deleted by rmtree.
    #             # TODO: Maybe use the kernel.dll to unlink the file
    #             # that fails on rmtree and unlink it (should be noted
    #             # in 'e') and re-run the function.
    #             shutil.copytree(copy_dir.src,
    #                             copy_dir.dest,
    #                             ignore=self.__class__.IGNORE_GIT)
    #         except FileExistsError as e:
    #             # Should not happen, due to the prevention, that the git
    #             # directory is beeing copied.
    #             # Will happen, if copied manuelly.
    #             # print(f"{copy_dir.src=}, {copy_dir.dest=}, {e=}")
    #             raise FileExistsError(
    #                 "Maybe there is a linked file that coud not be deleted.")

    def make(self) -> None:
        failed: int = 0
        for worker in self.workers:
            if worker.make():
                failed += 1
                print("Failed... Continue in 5 seconds")
                time.sleep(5)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}({self.workers})"
        )

    def __str__(self) -> str:
        return self.__repr__()


# vim: set ft=python :
