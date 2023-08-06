# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autofac']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.1.0,<23.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'rich>=12.6.0,<13.0.0',
 'typer[all]>=0.7.0,<0.8.0']

extras_require = \
{'all': ['autoflake>=1.4,<2.0',
         'black>=22.3.0,<23.0.0',
         'isort>=5.10.1,<6.0.0',
         'mkdocs>=1.4.2,<2.0.0',
         'mkdocs-material>=8.5.11,<9.0.0',
         'mypy>=0.961,<0.962',
         'pytest>=7.2.0,<8.0.0',
         'pytest-vscodedebug>=0.1.0,<0.2.0',
         'pyupgrade>=2.37.3,<3.0.0',
         'toml>=0.10.2,<0.11.0',
         'xdoctest[all]>=1.1.0,<2.0.0'],
 'test': ['autoflake>=1.4,<2.0',
          'black>=22.3.0,<23.0.0',
          'isort>=5.10.1,<6.0.0',
          'mkdocs>=1.4.2,<2.0.0',
          'mkdocs-material>=8.5.11,<9.0.0',
          'mypy>=0.961,<0.962',
          'pytest>=7.2.0,<8.0.0',
          'pytest-vscodedebug>=0.1.0,<0.2.0',
          'pyupgrade>=2.37.3,<3.0.0',
          'toml>=0.10.2,<0.11.0',
          'xdoctest[all]>=1.1.0,<2.0.0']}

setup_kwargs = {
    'name': 'autofac',
    'version': '0.1.0',
    'description': 'AutoFac is a library for using Dependency Inversion Principle in Python',
    'long_description': '# AutoFac\n\nAutoFac is a library that allows you to use Dependency Inversion Principle in Python.\n\n## Python environment\n\nCreate your python environment using `poetry install -E all`\n\n## Adding documentation\n\n1. Run `mkdocs new .` to create the documentation structure (after customizing template)\n2. Change theme in `mkdocs.yml` to `material`\n\n### Useful resources\n\n1. [Material for MkDocs](https://jamstackthemes.dev/demo/theme/mkdocs-material/)\n2. [MkDocs](https://www.mkdocs.org/)\n3. [Blog post](https://blog.elmah.io/creating-a-documentation-site-with-mkdocs/)\n',
    'author': 'Aditya Gudimella',
    'author_email': 'aditya.gudimella@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
