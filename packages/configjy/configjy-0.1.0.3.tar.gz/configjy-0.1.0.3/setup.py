# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['configjy']

package_data = \
{'': ['*']}

install_requires = \
['ruamel.yaml>=0.17.21,<0.18.0']

setup_kwargs = {
    'name': 'configjy',
    'version': '0.1.0.3',
    'description': 'Loads a json or yaml config file',
    'long_description': '# configjy\n\n> Loads variables from a .json, .yaml or .yml file\n\n[![PyPI version][pypi-image]][pypi-url]\n[![Build status][build-image]][build-url]\n[![GitHub stars][stars-image]][stars-url]\n[![Support Python versions][versions-image]][versions-url]\n\n\n\n## Getting started\n\nYou can [get `configjy` from PyPI](https://pypi.org/project/configjy),\nwhich means it\'s easily installable with `pip`:\n\n```bash\npython -m pip install configjy\n```\n\n\n## Example usage\n\n```python\n\nfrom configjy import ConfigFile\n\n# given this file:\n"""\n{\n    "key1": 10,\n    "key2": {\n        "key3": 20\n    },\n    "key4": "{{key1}}"\n}\n"""\n\n        \nfvar = ConfigFile(config_file_path)\nkey1 = fvar.get(\'key1\')\nprint(key1) # 10\n\nkey2 = fvar.get(\'key2\')\nprint(key2) # {"key3": 20}\n\nkey3 = fvar.get(\'key2.key3\')\nprint(key3) # 20\n\nkey4 = fvar.get(\'key4\')\nprint(key4) # str(key1) = "10"\n\nkey5 = fvar.get(\'key5\', default=1, print_when_not_exists=False)\nprint(key5) # 1\n\ntry:\n    key6 = fvar.get(\'key6\', raise_when_not_exists=True) # raises key error\nexcept KeyError:\n    pass\n\nkey6 = fvar.get(\'key6\') # print a warning abou non existent key\nprint(key6) # None\n\n\n```\n\n\n\n## Changelog\n\nRefer to the [CHANGELOG.md](https://github.com/henriquelino/configjy/blob/main/CHANGELOG.md) file.\n\n\n\n<!-- Badges -->\n\n[pypi-image]: https://img.shields.io/pypi/v/configjy\n[pypi-url]: https://pypi.org/project/configjy/\n\n[build-image]: https://github.com/henriquelino/configjy/actions/workflows/build.yaml/badge.svg\n[build-url]: https://github.com/henriquelino/configjy/actions/workflows/build.yaml\n\n[stars-image]: https://img.shields.io/github/stars/henriquelino/configjy\n[stars-url]: https://github.com/henriquelino/configjy\n\n[versions-image]: https://img.shields.io/pypi/pyversions/configjy\n[versions-url]: https://pypi.org/project/configjy/\n\n',
    'author': 'henrique lino',
    'author_email': 'henrique.lino97@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
