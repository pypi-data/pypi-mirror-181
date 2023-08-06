# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['makejinja']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=3.1.2,<4.0.0',
 'python-simpleconf[all]>=0.5.7,<0.6.0',
 'rich>=12.6.0,<13.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['makejinja = makejinja.cli:app']}

setup_kwargs = {
    'name': 'makejinja',
    'version': '0.5.1',
    'description': 'Automatically generate files based on Jinja templates. Use it to easily generate complex Home Assistant dashboards!',
    'long_description': '# MakeJinja\n',
    'author': 'Mirko Lenz',
    'author_email': 'mirko@mirkolenz.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mirkolenz/makejinja',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
