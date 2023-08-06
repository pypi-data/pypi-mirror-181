# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rlbcore',
 'rlbcore.api',
 'rlbcore.cli',
 'rlbcore.external_utils',
 'rlbcore.memories',
 'rlbcore.memories.experience_replay',
 'rlbcore.uis']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.1.0,<23.0.0',
 'gymnasium>=0.27.0,<0.28.0',
 'mkdocs-macros-plugin>=0.7.0,<0.8.0',
 'mkdocs-material>=8.5.11,<9.0.0',
 'mkdocs>=1.4.2,<2.0.0',
 'mkdocstrings[python]>=0.19.0,<0.20.0',
 'omegaconf>=2.3.0,<3.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'rich>=12.6.0,<13.0.0',
 'typer[all]>=0.7.0,<0.8.0']

extras_require = \
{'all': ['autoflake>=1.4,<2.0',
         'black>=22.3.0,<23.0.0',
         'isort>=5.10.1,<6.0.0',
         'mlflow>=2.0.1,<3.0.0',
         'mypy>=0.961,<0.962',
         'pandas>=1.5.2,<2.0.0',
         'pytest>=7.2.0,<8.0.0',
         'pytest-vscodedebug>=0.1.0,<0.2.0',
         'pyupgrade>=2.37.3,<3.0.0',
         'toml>=0.10.2,<0.11.0',
         'wandb>=0.13.6,<0.14.0',
         'xdoctest[all]>=1.1.0,<2.0.0'],
 'mlflow': ['mlflow>=2.0.1,<3.0.0', 'pandas>=1.5.2,<2.0.0'],
 'test': ['autoflake>=1.4,<2.0',
          'black>=22.3.0,<23.0.0',
          'isort>=5.10.1,<6.0.0',
          'mypy>=0.961,<0.962',
          'pytest>=7.2.0,<8.0.0',
          'pytest-vscodedebug>=0.1.0,<0.2.0',
          'pyupgrade>=2.37.3,<3.0.0',
          'toml>=0.10.2,<0.11.0',
          'xdoctest[all]>=1.1.0,<2.0.0'],
 'wandb': ['wandb>=0.13.6,<0.14.0']}

entry_points = \
{'console_scripts': ['rlbcore = rlbcore.cli:app']}

setup_kwargs = {
    'name': 'rlbcore',
    'version': '0.2.5',
    'description': 'Common functionality for all rlbaselines projects',
    'long_description': '# RLB Core\n\nImplements functionality common among all RLBaselines projects.\n\nAll RLBaselines projects have `rlbcore` as a dependency.\n\n## Python environment\n\nCreate your python environment using `poetry install -E all`\n\n### Useful resources\n\n1. [Material for MkDocs](https://jamstackthemes.dev/demo/theme/mkdocs-material/)\n2. [MkDocs](https://www.mkdocs.org/)\n3. [Blog post](https://blog.elmah.io/creating-a-documentation-site-with-mkdocs/)\n',
    'author': 'Aditya Gudimella',
    'author_email': 'aditya.gudimella@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
