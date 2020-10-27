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

import datetime

from pathlib import Path
from shutil import get_terminal_size
from textwrap import TextWrapper
from types import TracebackType
from typing import Any
from typing import List
from typing import Optional
from typing import Type
from typing import Union

import git

from tabulate import tabulate


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


class Git:
    def __init__(self, path: Union[Path, str]) -> None:
        self.path: Path = Path(path)
        self.repo = git.Repo(self.path)
        assert not self.repo.bare

        self.git = git.cmd.Git(self.path)
        self.heads = self.repo.heads

        self.has_updated: Optional[bool] = None  # None, if not checked

    @classmethod
    def clone(cls, origin: str, dest: Path) -> Git:
        git.Repo.clone_from(origin, dest.name)
        return cls(dest)

    def checkout(self, ref: git.TagReference) -> None:
        self.git.checkout(str(ref))

    @property
    def datetime_last_pulled_commit(self) -> datetime.datetime:
        log = self.repo.active_branch.log()

        return datetime.datetime.fromtimestamp(log[-1].time[0])

    def log(self, since: Optional[datetime.datetime] = None) -> None:
        cmd = ["--pretty=%as\t%an\t%s"]

        if since:
            cmd.append(f"--since={str(since)}")

        terminal_size_x, _ = get_terminal_size()
        # debug(f"Terminal width = {terminal_size_x}")

        ######################################################################
        #                          Terminal width                            #
        #                          ^^^^^^^^^^^^^^                            #
        #                                                                    #
        # |<-------------------------------(121)-------------------------->| #
        # |<--------------------------(119)------------------------->|     | #
        # |<----------------------(34)--------------------->|        |     | #
        # |<------------------(32)----------------->|       |        |     | #
        # |<---------------(30)-------------->|     |       |        |     | #
        # |<-------------16------------>|     |     |       |        |     | #
        # |<---------14--------->|      |     |     |       |        |     | #
        # |<----12----->|        |      |     |     |       |        |     | #
        # |<--3-->|     |        |      |     |     |       |        |     | #
        # |_______d a t e________|______u s e r_____|_______commit_msg_____| #
        #                               |<--->|            |<------>|        #
        #                                 15                 x - 35          #
        #                                                                    #
        ######################################################################

        wrapper_user = TextWrapper(
            width=15, drop_whitespace=True, break_long_words=True
        )
        wrapper_comment = TextWrapper(
            width=terminal_size_x - 35,
            drop_whitespace=True,
            break_long_words=True,
        )

        log: List[List[str]] = [
            line.split("\t") for line in self.git.log(cmd).split("\n")
        ]

        if log[0][0]:  # Has updated
            self.has_updated = True
            print("")  # Newline
        else:
            self.has_updated = False
            print("[up-to-date]")
            return

        for line in log:
            line[1] = wrapper_user.fill(text=line[1])
            line[2] = wrapper_comment.fill(text=line[2])

        print(
            tabulate(
                log,
                headers=("Date", "User", "Commit Message"),
                tablefmt="psql",
            )
        )

    def pull(self) -> None:
        # Get the last pulled datetime
        since = self.datetime_last_pulled_commit

        retries: int = 3
        while retries:
            retries -= 1
            try:
                self.git.pull()
            except git.exc.GitCommandError:
                self.hard_reset()
            except git.GitCommandError:
                raise ConnectionError(
                    "The updater was not able to connect to remote repository "
                    "on GitHub. Are you connected to the internet?"
                )

        self.log(since)

    def fetch(self) -> None:
        # Get the last pulled datetime
        since = self.datetime_last_pulled_commit

        try:
            self.git.fetch()
        except git.GitCommandError:
            raise ConnectionError(
                "The updater was not able to connect to remote repository "
                "on GitHub. Are you connected to the internet?"
            )

        self.log(since)

    def hard_reset(self) -> None:
        self.repo.git.reset("--hard")
        self.repo.git.clean("-xdf")

    @property
    def tags(self) -> Any:
        return self.repo.tags

    def __enter__(self) -> Git:
        """Use the class with the ``with`` statement`` statement.

        This is currently not really needed, but unifies the way handlers are
        used.
        """

        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Use the class with the ``with`` statement`` statement.

        This is currently not really needed, but unifies the way handlers are
        used.
        """

        return

    @property
    def name(self) -> str:
        return self.path.name

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}({self.path.name})"
        )

    def __str__(self) -> str:
        return self.__repr__()


# vim: set ft=python :
