# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['structcheck']

package_data = \
{'': ['*']}

install_requires = \
['graphviz>=0.20.1,<0.21.0']

setup_kwargs = {
    'name': 'structcheck',
    'version': '1.0.41',
    'description': '',
    'long_description': '# structcheck\n[![Upload Python Package](https://github.com/vincentBenet/structcheck/actions/workflows/python-publish.yml/badge.svg)](https://github.com/vincentBenet/structcheck/actions/workflows/python-publish.yml)\n[![Python application](https://github.com/vincentBenet/structcheck/actions/workflows/python-app.yml/badge.svg)](https://github.com/vincentBenet/structcheck/actions/workflows/python-app.yml)\n[![Pylint](https://github.com/vincentBenet/structcheck/actions/workflows/pylint.yml/badge.svg)](https://github.com/vincentBenet/structcheck/actions/workflows/pylint.yml)\n\n\n## Installation\n### Pip installation\n\n\tpip install structcheck\n\t\n\n### Version check (linux)\n\n\tpip freeze | grep structcheck\n\n### Check installation\n\n\tpython -m structcheck --help\n\n## Usage\n\n### Shell command\n\n#### No arguments\n\n\tpython -m structcheck\n\t\nA popup windows will ask you for directory and config file\n\t\n#### Arguments\n\nPath to scan:\n\n\tpython -m structcheck -p "/path/to/scan"\n\t\nA popup windows will ask you for config file\n\n\tpython -m structcheck -p "/path/to/scan" -c "/path/to/config.json"\n\n### Python usage\n\n\timport structcheck\n\t\n\ttxt, reports, logs = structcheck.scan()  # Same as command \'python -m structcheck\'\n\t\nYou can add arguments with:\n\n\ttxt, reports, logs = structcheck.scan([\n\t\t"-p", "/path/to/scan",\n\t\t"-c", "/path/to/config.json",\n\t])',
    'author': 'vincentBenet',
    'author_email': 'vincent.benet@outlook.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
