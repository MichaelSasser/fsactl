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

import argparse

from argparse import _SubParsersAction as SubParsersAction
from logging import debug
from logging import warning
from typing import Callable
from typing import List

import coloredlogs

from fsactl import __version__

from .install import subparser_install
from .make import subparser_make
from .update import subparser_update


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enables debugging mode."
    )
    subparsers: SubParsersAction = parser.add_subparsers()

    # Subparsers
    subparsers_tuple: List[Callable[[SubParsersAction], None]] = [
        subparser_update,
        subparser_make,
        subparser_install,
    ]

    for subparser in subparsers_tuple:
        subparser(subparsers)

    return parser


def setup_logging(debug_mode: bool) -> None:
    coloredlogs.DEFAULT_LOG_FORMAT = (
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    coloredlogs.DEFAULT_LOG_LEVEL = 0 if debug_mode else 21
    coloredlogs.install()


def main() -> int:
    parser = setup_parser()

    args: argparse.Namespace = parser.parse_args()

    setup_logging(args.debug)

    debug(f"{args=}")

    if args.debug:
        debug("Disabing help on AttributeError")
        warning(
            "In debugging mode help is disabled! If you don't use any "
            "attibutes, the program will throw a AttributeError like: "
            "\"AttributeError: 'Namespace' object has no attribute 'func\".'"
            " This is perfectly normal and not a bug. If you want the help "
            'in debug mode, use the "--help" attribute.'
        )

        return int(args.func(args))

    try:
        return int(args.func(args))
    except AttributeError:
        parser.print_help()

        return 1


# vim: set ft=python :
