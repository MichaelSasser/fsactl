#!/usr/bin/env python
# fsactl - install and manager your MSFS2020 addons
# Copyright (c) 2020  Michael Sasser <Michael@MichaelSasser.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


import sys

from fsactl.app import main


if __name__ == "__main__":
    sys.exit(main())

# vim: set ft=python :
