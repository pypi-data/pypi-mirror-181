# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['omicron',
 'omicron.config',
 'omicron.core',
 'omicron.dal',
 'omicron.dal.influx',
 'omicron.extensions',
 'omicron.models',
 'omicron.notify',
 'omicron.plotting',
 'omicron.talib']

package_data = \
{'': ['*'], 'omicron.config': ['sql/*']}

install_requires = \
['Bottleneck>=1.3.4,<2.0.0',
 'aiohttp>=3.8.0,<4.0.0',
 'aioredis>=2.0.1,<3.0.0',
 'aiosmtplib>=1.1.6,<2.0.0',
 'arrow>=1.2,<2.0',
 'cfg4py>=0.9',
 'ciso8601>=2.2.0,<3.0.0',
 'ckwrap>=0.1.10,<0.2.0',
 'deprecation>=2.1.0,<3.0.0',
 'empyrical-reloaded>=0.5.8,<0.6.0',
 'httpx>=0.23.0,<0.24.0',
 'numpy>=1.22,<2.0',
 'pandas>=1.3.5,<2.0.0',
 'plotly>=5.10.0,<6.0.0',
 'retry>=0.9.2,<0.10.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'sh==1.14.1',
 'zigzag>=0.3,<0.4',
 'zillionare-core-types>=0.5.2,<0.6.0']

extras_require = \
{':sys_platform == "linux"': ['TA-Lib>=0.4.25,<0.5.0'],
 'dev': ['pre-commit>=2.17.0,<3.0.0',
         'tox>=3.24.5,<4.0.0',
         'pip>=22.0.3,<23.0.0',
         'toml>=0.10.2,<0.11.0',
         'twine>=3.8.0,<4.0.0'],
 'doc': ['mkdocs>=1.3.0,<2.0.0',
         'mkdocs-include-markdown-plugin>=3.2.3,<4.0.0',
         'mkdocs-material>=8.1.11,<9.0.0',
         'mkdocstrings>=0.18.0,<0.19.0',
         'mkdocs-autorefs>=0.3.1,<0.4.0',
         'livereload>=2.6.3,<3.0.0',
         'mike>=1.1.2,<2.0.0'],
 'test': ['black>=22.3.0,<23.0.0',
          'isort==5.10.1',
          'flake8==4.0.1',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'pytest>=7.0.1,<8.0.0',
          'pytest-cov>=3.0.0,<4.0.0',
          'psutil>=5.7.3,<6.0.0',
          'freezegun>=1.2.1,<2.0.0']}

setup_kwargs = {
    'name': 'zillionare-omicron',
    'version': '2.0.0a65',
    'description': 'Core Library for Zillionare',
    'long_description': '\n![](http://images.jieyu.ai/images/hot/zillionbanner.jpg)\n\n<h1 align="center">Omicron - Core Library for Zillionare</h1>\n\n\n[![Version](http://img.shields.io/pypi/v/zillionare-omicron?color=brightgreen)](https://pypi.python.org/pypi/zillionare-omicron)\n[![CI Status](https://github.com/zillionare/omicron/actions/workflows/release.yml/badge.svg)](https://github.com/zillionare/omicron)\n[![Code Coverage](https://img.shields.io/codecov/c/github/zillionare/omicron)](https://app.codecov.io/gh/zillionare/omicron)\n<<<<<<< HEAD\n=======\n[![ReadtheDos](https://readthedocs.org/projects/omicron/badge/?version=latest)](https://omicron.readthedocs.io/en/latest/?badge=latest)\n>>>>>>> master\n[![Downloads](https://pepy.tech/badge/zillionare-omicron)](https://pepy.tech/project/zillionare-omicron)\n[![License](https://img.shields.io/badge/License-MIT.svg)](https://opensource.org/licenses/MIT)\n[![Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n# Contents\n\n## 简介\n\nOmicron是Zillionare的核心公共模块，向其它模块提供行情数据、交易日历、证券列表、时间操作及Trigger等功能。\n\nOmicron是大富翁量化框架的一部分。您必须至少安装并运行[Omega](https://zillionare.github.io/omega)，然后才能利用omicron来访问上述数据。\n\n[使用文档](https://zillionare.github.io/omicron)\n\n## Credits\n\n<<<<<<< HEAD\nZillionare-Omicron采用[Python Project Wizard](https://zillionare.github.io/python-project-wizard)构建。\n=======\n* [Cookiecutter](https://github.com/audreyr/cookiecutter)\n* [Cookiecutter-pypackage](https://github.com/zillionare/cookiecutter-pypackage)\n* ![JetBrains Black Box Logo logo](https://resources.jetbrains.com/storage/products/company/brand/logos/jb_square.svg) [Pycharm开源项目支持计划](https://www.jetbrains.com/?from=zillionare-omega)\n>>>>>>> master\n',
    'author': 'jieyu',
    'author_email': 'code@jieyu.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://zillionare-omicron.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
