# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hanmatek']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['minimalmodbus>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['hanmatek-cli = hanmatek.__main__:main']}

setup_kwargs = {
    'name': 'hanmatek-psu',
    'version': '1.1.0',
    'description': 'Library and CLI for the Hanmatek Power supply units (PSU) of the HM3xxP series.',
    'long_description': '[![](https://img.shields.io/pypi/v/hanmatek-psu.svg?maxAge=3600)](https://pypi.org/project/hanmatek-psu/)\n[![Latest Release](https://gitlab.com/janoskut/hanmatek-psu/-/badges/release.svg)](https://gitlab.com/janoskut/hanmatek-psu/-/releases)\n[![pipeline status](https://gitlab.com/janoskut/hanmatek-psu/badges/main/pipeline.svg)](https://gitlab.com/janoskut/hanmatek-psu/-/commits/main)\n[![coverage report](https://gitlab.com/janoskut/hanmatek-psu/badges/main/coverage.svg)](https://gitlab.com/janoskut/hanmatek-psu/-/commits/main)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n\n\n# Hanmatek HM3xxP PSU control library and CLI\n\nUnifying library and CLI for the popular and low-cost digital lab power supplies `HM305P` and\n`HM310P`.\n\nThe library provides an (almost) complete, easy to use interface to all known functions of the\ndevice. This project is different to the below mentioned ones, in that it provides a minimal,\nbut complete interface to the device and also keeps the dependencies low.\n\nThis project is based on the work done in <https://github.com/notkevinjohn/HM310P>, which uses the\n`minimalmodbus` library for device communication. Other related projects were providing\nuseful register definition and hints:\n\n- <https://github.com/JackDoan/hm305_ctrl/tree/master/hm305>\n- <https://github.com/hobbyquaker/hanmatek-hm310p>\n- <https://sigrok.org/wiki/ETommens_eTM-xxxxP_Series#Protocol>\n\n\n## Installation\n\n```py\npip install hanmatek-psu\n```\n\nIf users are in the `plugdev` user group, Hanmatek devices are accessible via `/dev/ttyUSBx` without\nprivileges. Adding the following `udev` rule will create a symlink `/dev/ttyHM3xxP` when a Hanmatek\nPSU device is plugged in via USB. This symlink is used by default by the `hanmatek-cli` to find\ndevices:\n\n```sh\necho \'SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", SYMLINK+="ttyHM3xxP", MODE="0666", GROUP="plugdev"\' | sudo tee "/etc/udev/rules.d/99-hanmatek.rules" > /dev/null\n```\n\n## Usage\n\n### CLI Usage\n\n```sh\nhanmatek-cli -h\nhanmatek-cli --discover             # find devices\nhanmatek-cli                        # show default device info\nhanmatek-cli --device /dev/ttyUSB0  # specific device\nhanmatek-cli voltage:set 3.0        # set voltage\nhanmatek-cli current:set 0.1        # set current limit\nhanmatek-cli output on\nhanmatek-cli current                # read current\nhanmatek-cli power                  # read power\nhanmatek-cli output off\nhanmatek-cli --list                 # list all commands/registers\n```\n\n### Library Usage\n\n```py\nfrom hanmatek import HM3xxP\n\ndevice = HM3xxP("/dev/ttyHM3xxP")\nprint(device.info())\ndevice.write("voltage:set", 3.0)\ndevice.write("current:set", 3.0)\ndevice.write("output", True)\nprint(device.read("current"))\nprint(device.read("power"))\ndevice.write("output", False)\n```\n\n## Development\n\nThe following tools are used to provide clean and quality software, and made available through a\n`tox` configuration: `flake8` for linting, `black` for code formatting and checking, `mypy` for\ntype checking and `pytest` for unit tests. Use as:\n\n```sh\npip install "tox<=4" tox-poetry\n```\n\n(we\'re using [`tox-poetry`](https://pypi.org/project/tox-poetry/), so that `tox` reads dependencies\nfrom `pyproject.toml`)\n\n(note that `tox-poetry` requires `tox<4.x`, see <https://github.com/tkukushkin/tox-poetry/issues/15)>.\n\n```sh\ntox -a       # show test environments\ntox          # run all\ntox -e test  # run unit tests\ntox -e lint  # run lint\ntox -e type  # run type checker\n```\n\n(we\'re using [`pyproject-flake8`](https://pypi.org/project/pyproject-flake8), so that the `flake8`\nconfiguration can live in `pyproject.toml` - within `tox` we then run `pflake8` instead of\n`flake8`.)\n',
    'author': 'Janos',
    'author_email': 'janoskut@gmail.com',
    'maintainer': 'Janos',
    'maintainer_email': 'janoskut@gmail.com',
    'url': 'https://gitlab.com/janoskut/hanmatek-psu/-/tree/main',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
