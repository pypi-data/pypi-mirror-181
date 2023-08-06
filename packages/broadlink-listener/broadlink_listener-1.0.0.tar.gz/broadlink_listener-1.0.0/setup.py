# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['broadlink_listener', 'broadlink_listener.cli_tools', 'tests']

package_data = \
{'': ['*'], 'tests': ['data/*']}

install_requires = \
['broadlink>=0.18.3,<0.19.0',
 'click==8.1.3',
 'cloup>=2.0.0,<3.0.0',
 'termcolor>=2.1.1,<3.0.0',
 'tqdm>=4.64.0,<5.0.0']

entry_points = \
{'console_scripts': ['broadlink-listener = '
                     'broadlink_listener.cli_tools.cli:main']}

setup_kwargs = {
    'name': 'broadlink-listener',
    'version': '1.0.0',
    'description': 'Broadlink IR codes listener and SmartIR json generator.',
    'long_description': '# Broadlink Listener\n\n\n[![pypi](https://img.shields.io/pypi/v/broadlink-listener.svg)](https://pypi.org/project/broadlink-listener/)\n[![python](https://img.shields.io/pypi/pyversions/broadlink-listener.svg)](https://pypi.org/project/broadlink-listener/)\n[![Build Status](https://github.com/gpongelli/broadlink-listener/actions/workflows/dev.yml/badge.svg)](https://github.com/gpongelli/broadlink-listener/actions/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/gpongelli/broadlink-listener/branch/main/graphs/badge.svg)](https://codecov.io/github/gpongelli/broadlink-listener)\n\n\n\nBroadlink IR codes listener and SmartIR json generator.\n\nThis project will install a `broadlink-listener` command line tool that can be used to generate a climate [SmartIR](https://github.com/smartHomeHub/SmartIR)\ncompatible json, starting from an initial structure that defines climate behavior, putting Broadlink IR remote to\nlistening state, until all IR code combination will being scan.\n\n\n* Documentation: <https://gpongelli.github.io/broadlink-listener>\n* GitHub: <https://github.com/gpongelli/broadlink-listener>\n* PyPI: <https://pypi.org/project/broadlink-listener/>\n* Free software: MIT\n\n\n## Features\n\n* Discover Broadlink IR remote\n* Starting from SmartIR json structure like\n```json\n{\n  "supportedController": "Broadlink",\n  "minTemperature": 16,\n  "maxTemperature": 31,\n  "precision": 1,\n  "operationModes": [\n    "op_a",\n    "op_b"\n  ],\n  "fanModes": [\n    "fan_a",\n    "fan_b"\n  ],\n  "swingModes": [\n    "swing_a",\n    "swing_b"\n  ]\n}\n```\n  it helps you listen all the defined IR codes to create a json like\n```json\n{\n  "supportedController": "Broadlink",\n  "minTemperature": 16,\n  "maxTemperature": 31,\n  "precision": 1,\n  "operationModes": [\n    "op_a",\n    "op_b"\n  ],\n  "fanModes": [\n    "fan_a",\n    "fan_b"\n  ],\n  "swingModes": [\n    "swing_a",\n    "swing_b"\n  ],\n  "commands": {\n    "off": "...",\n    "op_a": {\n        "fan_a": {\n            "swing_a": {\n                "16": "....",\n\n                "31": "...."\n            },\n            "swing_b": {\n                "16": "....",\n\n                "31": "...."\n            }\n        },\n        "fan_b": {\n            "swing_a": {\n                "16": "....",\n\n                "31": "...."\n            },\n            "swing_b": {\n                "16": "....",\n\n                "31": "...."\n            }\n        }\n    },\n    "op_b": {\n        "fan_a": {\n            "swing_a": {\n                "16": "....",\n\n                "31": "...."\n            },\n            "swing_b": {\n                "16": "....",\n\n                "31": "...."\n            }\n        },\n        "fan_b": {\n            "swing_a": {\n                "16": "....",\n\n                "31": "...."\n            },\n            "swing_b": {\n                "16": "....",\n\n                "31": "...."\n            }\n        }\n    }\n  }\n}\n```\n\n* Mandatory fields into starting json\n  * `supportedController`, `minTemperature`, `maxTemperature`, `precision`\n* Optional fields (at least one must be present or nothing will be listened):\n  * `operationModes`, `fanModes`,`swingModes`\n* Generated file can be used into SmartIR HomeAssistant component\n\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [gpongelli/cookiecutter-pypackage](https://github.com/gpongelli/cookiecutter-pypackage) project template.\n',
    'author': 'Gabriele Pongelli',
    'author_email': 'gabriele.pongelli@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/gpongelli/broadlink-listener',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0',
}


setup(**setup_kwargs)
