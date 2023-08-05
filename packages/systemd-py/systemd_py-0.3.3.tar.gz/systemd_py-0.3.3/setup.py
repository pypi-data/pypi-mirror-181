# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['systemd_py',
 'systemd_py.builders',
 'systemd_py.commands',
 'systemd_py.commands.cli',
 'systemd_py.commands.interactive',
 'systemd_py.core',
 'systemd_py.core.enums',
 'systemd_py.core.models',
 'systemd_py.core.types',
 'systemd_py.interactive',
 'systemd_py.utils',
 'systemd_py.utils.terminal']

package_data = \
{'': ['*']}

install_requires = \
['mkdocs-gen-files>=0.4.0,<0.5.0',
 'mkdocs-git-committers-plugin-2>=1.1.1,<2.0.0',
 'mkdocs-git-revision-date-localized-plugin>=1.1.0,<2.0.0',
 'mkdocs-literate-nav>=0.5.0,<0.6.0',
 'mkdocs-material>=8.5.11,<9.0.0',
 'mkdocs-section-index>=0.3.4,<0.4.0',
 'mkdocs>=1.4.2,<2.0.0',
 'mkdocstrings[python]>=0.19.0,<0.20.0',
 'pydantic>=1.10.2,<2.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['systemd-py = systemd_py.commands.main:app']}

setup_kwargs = {
    'name': 'systemd-py',
    'version': '0.3.3',
    'description': 'systemd-py is a library which helps you to create systemd services in python.',
    'long_description': '# Systemd-py\n`systemd-py` is a library which helps you to create systemd services in python.\n\n\n## Installation\n### Install from PyPI\n    pip install systemd-py\n\n### Install from source (build using poetry)\n    git clone\n    cd systemd-py\n    poetry build\n    pip install dist/systemd-py-<version>-py3-none-any.whl\n\n### Install from GitHub\n    pip install git+hhttps://github.com/amiwrprez/systemd-py.git\n\n\n## Documentation\n### Online\nSee [documentation](https://amiwrpremium.github.io/systemd-py/).\n\n### Offline\nYou can generate documentation locally using `mkdocs`:\n    mkdocs build\n\n\n## Examples\n### From docs\nSee [Documentation Examples](https://amiwrpremium.github.io/systemd-py/examples/)\n### Example Folder\nSee [examples](https://github.com/amiwrpremium/systemd-py/tree/master/examples) for examples.\n',
    'author': 'amiwrpremium',
    'author_email': 'amiwrpremium@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://amiwrpremium.github.io/systemd-py/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
