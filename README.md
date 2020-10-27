![GitHub](https://img.shields.io/github/license/MichaelSasser/fsactl?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fsactl?style=flat-square)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/fsactl?style=flat-square)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/michaelsasser/fsactl?style=flat-square)
![GitHub Release Date](https://img.shields.io/github/release-date/michaelsasser/fsactl?style=flat-square)
![PyPI - Status](https://img.shields.io/pypi/status/fsactl?style=flat-square)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/michaelsasser/fsactl?style=flat-square)

# MS FlightSimulator 2020 Addon Control

fsactl is a program to download, install, update, build and manage your FlightSimulator addons.

## Development

This program is currently under development.

## Installation

fsactl is written in Python. The installation is straight forward. Just run ``pip install fsactl``. fsactl will be installd from the [Python Package Index (PyPi)](https://pypi.org/project/fsactl/).

You will find more information in the documentation.

## Configuration File

Create a directory named fsactl in your My Documents directory and create a file called config.yaml in it
with a configuration like the following:

```yaml
---

# This is a comment

msfs:
  addon_dir: E:/MSFS-ADDONS  # A directory where your addons can be stored and managed
  community_dir: E:/MSFS/Community  # Your community folder
  addons:
    - github: pimarc/pms50-gns530   # A prebuild addon from github
    - github: lmk02/B787-XE  # A nother one
    - github: saltysimulations/salty-747  # This addon needs a build step
      build:
        - path: "{{ addon_path }}"  # build directory
          command: python build.py  # build command
    - github: r9r-dev/fs2020-vl3-rotax915  # This addon must be build in two steps
      build:
        - path: "{{ addon_path }}"  # first build directory
          command: update-layout.bat  # first build command
        - path: "{{ addon_path }}/community-vl3rotax915"  # second build directory
          command: "python {{ addon_path }}/build.py"  # second build command
```

Be sure to use slashs `/` instead of backslashs in all paths.

You will get a more detailed Documentation to this in the near future.

## Usage

```
$ fsactl
usage: fsactl [-h] [--version] [-d] {update,make,install} ...

positional arguments:
  {update,make,install}
    update              Update and build addons
    make                Force to rebuild the addons
    install             Install addons

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -d, --debug           Enables debugging mode.
```

## Semantic Versioning

This repository uses [SemVer](https://semver.org/) for its release
cycle.

## Branching Model

This repository uses the
[git-flow](https://danielkummer.github.io/git-flow-cheatsheet/index.html)
branching model by [Vincent Driessen](https://nvie.com/about/).
It has two branches with infinite lifetime:

* [master](https://github.com/MichaelSasser/fsactl/tree/master)
* [develop](https://github.com/MichaelSasser/fsactl/tree/develop)

The master branch gets updated on every release. The develop branch is the
merging branch.

## License
Copyright &copy; 2020 Michael Sasser <Info@MichaelSasser.org>. Released under
the GPLv3 license.
