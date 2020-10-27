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

import sys
from logging import error
from pathlib import Path

import yaml

from fsactl.typing import YAML

__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


def load_config() -> YAML:
    config_path: Path = Path(__file__).parent / "updater.yaml"
    with config_path.open("r") as config_stream:
        try:
            # Environment(loader=BaseLoader())
            config: YAML = yaml.safe_load(config_stream)

        except yaml.YAMLError as e:
            error(
                f"There was a problem with your updater.yaml config file:\n\n{e}"
            )
            sys.exit(0)

# vim: set ft=python :
