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

import ctypes.wintypes
import sys

from logging import fatal
from pathlib import Path

import yaml

from fsactl.typing import YAML


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


def load_config() -> YAML:

    # https://docs.microsoft.com/en-us/windows/win32/api/shlobj_core/nf-shlobj_core-shgetfolderpathw

    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)

    # Header "Shlobj.h":
    # SHFOLDERAPI SHGetFolderPathW(
    #     HWND   hwnd,     -> 0
    #     int    csidl,    -> 5 CSIDL_PERSONAL (My Documents folder)
    #     HANDLE hToken,   -> 0
    #     DWORD  dwFlags,  -> 0 SHGFP_TYPE_CURRENT (get the current value)
    #     LPWSTR pszPath   -> buf
    # );
    ctypes.windll.shell32.SHGetFolderPathW(0, 5, 0, 0, buf)  # type: ignore

    config_path: Path = Path(buf.value) / "fsactl/config.yaml"
    try:
        with config_path.open("r") as config_stream:
            try:
                return yaml.safe_load(config_stream)
            except yaml.YAMLError as e:
                fatal(
                    "There was a problem with your updater.yaml config file:"
                    f"\n\n{e}"
                )
                sys.exit(1)
    except FileNotFoundError:
        fatal("Could not find the config file.")
        sys.exit(1)


# vim: set ft=python :
