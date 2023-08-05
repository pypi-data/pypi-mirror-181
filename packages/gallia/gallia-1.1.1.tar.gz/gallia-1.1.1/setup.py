# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src',
 'cursed_hr': 'src/cursed_hr',
 'hr': 'src/hr',
 'opennetzteil': 'src/opennetzteil',
 'opennetzteil.devices': 'src/opennetzteil/devices',
 'opennetzteil.devices.http': 'src/opennetzteil/devices/http',
 'opennetzteil.devices.rnd': 'src/opennetzteil/devices/rnd',
 'opennetzteil.devices.rs': 'src/opennetzteil/devices/rs'}

packages = \
['cursed_hr',
 'gallia',
 'gallia.command',
 'gallia.commands',
 'gallia.commands.discover',
 'gallia.commands.discover.uds',
 'gallia.commands.fuzz',
 'gallia.commands.fuzz.uds',
 'gallia.commands.primitive',
 'gallia.commands.primitive.generic',
 'gallia.commands.primitive.uds',
 'gallia.commands.scan',
 'gallia.commands.scan.uds',
 'gallia.commands.script',
 'gallia.db',
 'gallia.services',
 'gallia.services.uds',
 'gallia.services.uds.core',
 'gallia.services.xcp',
 'gallia.transports',
 'hr',
 'opennetzteil',
 'opennetzteil.devices',
 'opennetzteil.devices.http',
 'opennetzteil.devices.rnd',
 'opennetzteil.devices.rs']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.8,<22.2',
 'aiohttp>=3.8,<4.0',
 'aiosqlite>=0.17,<0.18',
 'argcomplete>=2.0,<3.0',
 'construct>=2.10.67,<3.0.0',
 'msgspec>=0.8,<0.11',
 'pydantic>=1.10,<2.0',
 'pygit2>=1.10,<2.0',
 'python-can>=4.0,<5.0',
 'tabulate>=0.8.9,<0.10.0',
 'xdg>=5.1,<6.0',
 'zstandard>=0.17,<0.20']

extras_require = \
{':python_version < "3.11"': ['tomli>=2.0.1,<3.0.0']}

entry_points = \
{'console_scripts': ['cursed-hr = cursed_hr.cursed_hr:main',
                     'gallia = gallia.cli:main',
                     'hr = hr:main',
                     'netzteil = opennetzteil.cli:main']}

setup_kwargs = {
    'name': 'gallia',
    'version': '1.1.1',
    'description': 'Extendable Pentesting Framework',
    'long_description': '<!--\nSPDX-FileCopyrightText: AISEC Pentesting Team\n\nSPDX-License-Identifier: CC0-1.0\n-->\n\n# Gallia\n\n[![docs](https://img.shields.io/badge/-docs-green)](https://fraunhofer-aisec.github.io/gallia)\n[![docs](https://readthedocs.org/projects/docs/badge/?version=latest)](https://gallia.readthedocs.io/en/latest)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gallia)](https://pypi.python.org/pypi/gallia/)\n[![PyPI - License](https://img.shields.io/pypi/l/gallia)](https://www.apache.org/licenses/LICENSE-2.0.html)\n[![PyPI](https://img.shields.io/pypi/v/gallia)](https://pypi.python.org/pypi/gallia/)\n\nGallia is an extendable pentesting framework with the focus on the automotive domain.\nThe scope of the toolchain is conducting penetration tests from a single ECU up to whole cars.\nCurrently, the main focus lies on the [UDS](https://www.iso.org/standard/72439.html) interface.\nActing as a generic interface, the logging functionality implements reproducible tests and enables post-processing tasks.\nThe [rendered documentation](https://fraunhofer-aisec.github.io/gallia) is available via Github Pages.\nAlternatively, the documentation is hosted on [readthedocs](https://gallia.readthedocs.io/en/latest) as well.\nThe documentation for the current [stable](https://gallia.readthedocs.io/en/stable) realease is available on readthedocs.\n\nKeep in mind that this project is intended for research and development usage only!\nInappropriate usage might cause irreversible damage to the device under test.\nWe do not take any responsibility for damage caused by the usage of this tool.\n\n## Quickstart\n\nSee the [setup instructions](https://fraunhofer-aisec.github.io/gallia/setup.html).\n\nFirst create a config template with `--template`, store it to a file called [`gallia.toml`](https://fraunhofer-aisec.github.io/gallia/config.html), and adjust it to your needs.\n`gallia` reads this file to set the defaults of the command line flags.\nAll options correspond to a command line flag; the only required option for scans is `gallia.scanner.target`, for instance `isotp://can0?src_addr=0x123&dst_addr=0x312&tx_padding=0xaa&rx_padding=0xaa`.\n\n```\n$ gallia --template > gallia.toml\n```\n\nYou are all set to start your first scan, for instance read the diagnostic trouble codes:\n\n```\n$ gallia primitive uds dtc read\n```\n\nThe target can also be specified by the `--target` option on the command line.\nFor the format of the `--target` argument see the [transports documentation](https://fraunhofer-aisec.github.io/gallia/transports.html).\n\n## Acknowledgments\n\nThis work was partly funded by the German Federal Ministry of Education and Research (BMBF) as part of the [SecForCARs](https://www.secforcars.de/) project (grant no. 16KIS0790).\nA short presentation and demo video is available at this [page](https://www.secforcars.de/demos/10-automotive-scanning-framework.html).\n',
    'author': 'AISEC Pentesting Team',
    'author_email': 'None',
    'maintainer': 'Stefan Tatschner',
    'maintainer_email': 'stefan.tatschner@aisec.fraunhofer.de',
    'url': 'https://github.com/Fraunhofer-AISEC/gallia',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
