# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sys_toolkit',
 'sys_toolkit.clipboard',
 'sys_toolkit.configuration',
 'sys_toolkit.system',
 'sys_toolkit.tests',
 'sys_toolkit.tmpdir']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'inflection>=0.5,<0.6']

entry_points = \
{'pytest11': ['sys_toolkit_fixtures = sys_toolkit.fixtures']}

setup_kwargs = {
    'name': 'sys-toolkit',
    'version': '2.3.0',
    'description': 'Classes for operating system utilities',
    'long_description': '![Unit Tests](https://github.com/hile/sys-toolkit/actions/workflows/unittest.yml/badge.svg)\n![Style Checks](https://github.com/hile/sys-toolkit/actions/workflows/lint.yml/badge.svg)\n\n# Python system utility toolkit\n\nThis module contains various small utility methods and common classes for working in python.\n\nThese classes have moved from *systematic* and *cli-toolkit* modules to this module.\n\n## Installing\n\nThis module has minimal dependencies (PyYAML) and should install with *pip* on any recent\npython version. The module has been tested with python 3.9 and python 3.10.\n\n## Running unit tests and linters\n\nAll tests are run with *tox*.\n\nRun unit tests, flake8 and pylint:\n\n```bash\nmake\n```\n\nRun unit tests:\n\n```bash\nmake test\n```\n\nRun flake8 and pylint:\n\n```bash\nmake lint\n```\n',
    'author': 'Ilkka Tuohela',
    'author_email': 'hile@iki.fi',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
