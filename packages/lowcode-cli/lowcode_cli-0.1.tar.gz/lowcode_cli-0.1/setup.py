# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lowcode_cli',
 'lowcode_cli.common',
 'lowcode_cli.common.jinja2',
 'lowcode_cli.common.jinja2.filters',
 'lowcode_cli.common.jinja2.handles',
 'lowcode_cli.common.jsonschema',
 'lowcode_cli.conf',
 'lowcode_cli.core',
 'lowcode_cli.core.commands',
 'lowcode_cli.tools.doc',
 'lowcode_cli.utils']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'bs4>=0.0.1,<0.0.2',
 'case-convert>=1.1.0,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'convert-case>=1.1.1,<2.0.0',
 'dict-deep>=4.1.2,<5.0.0',
 'dynaconf>=3.1.11,<4.0.0',
 'jsonschema>=4.6.1,<5.0.0',
 'lxml>=4.9.1,<5.0.0',
 'pytest>=7.1.2,<8.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['lowcode = lowcode_cli.manage:cli']}

setup_kwargs = {
    'name': 'lowcode-cli',
    'version': '0.1',
    'description': 'Generate front-end code automatically',
    'long_description': None,
    'author': 'whc',
    'author_email': '249768447@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/status-521/lowcode-cli.git',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
