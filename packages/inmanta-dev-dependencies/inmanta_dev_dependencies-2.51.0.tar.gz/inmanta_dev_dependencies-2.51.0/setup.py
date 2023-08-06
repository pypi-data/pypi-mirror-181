# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['inmanta_dev_dependencies']

package_data = \
{'': ['*']}

install_requires = \
['black==22.12.0',
 'flake8-black==0.3.5',
 'flake8-copyright==0.2.3',
 'flake8-isort==5.0.3',
 'flake8==3.9.2',
 'isort==5.11.2',
 'lxml==4.9.2',
 'mypy==0.991',
 'pep8-naming==0.13.2',
 'pyadr==0.19.0',
 'pytest==7.2.0']

extras_require = \
{'async': ['pytest-asyncio==0.20.3', 'pytest-timeout==2.1.0'],
 'core': ['pytest-env==0.8.1',
          'pytest-postgresql==4.1.1',
          'asyncpg>=0.21.0,<1.0.0',
          'tornado>=6.1,<7.0'],
 'extension': ['pytest-inmanta-extensions',
               'pytest-env==0.8.1',
               'pytest-postgresql==4.1.1',
               'asyncpg>=0.21.0,<1.0.0',
               'tornado>=6.1,<7.0'],
 'module': ['pytest-inmanta'],
 'pytest': ['pytest-env==0.8.1',
            'pytest-cover==3.0.0',
            'pytest-randomly==3.12.0',
            'pytest-xdist==3.1.0',
            'pytest-sugar==0.9.6',
            'pytest-sugar==0.9.6',
            'pytest-instafail==0.4.2',
            'pytest-instafail==0.4.2'],
 'sphinx': ['inmanta-sphinx==1.6.1',
            'sphinx-argparse==0.4.0',
            'sphinx-autodoc-annotation==1.0-1',
            'sphinx-tabs==3.4.1',
            'Sphinx==5.3.0',
            'sphinxcontrib-serializinghtml==1.1.5',
            'sphinxcontrib-redoc==1.6.0',
            'sphinx-click==4.4.0',
            'recommonmark==0.7.1',
            'myst_parser==0.18.1']}

setup_kwargs = {
    'name': 'inmanta-dev-dependencies',
    'version': '2.51.0',
    'description': 'Package collecting all common dev dependencies of inmanta modules and extensions to synchronize dependency versions.',
    'long_description': 'None',
    'author': 'Inmanta',
    'author_email': 'code@inmanta.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
