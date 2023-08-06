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
    'version': '0.7.3',
    'description': 'Automatically generate files based on Jinja templates. Use it to easily generate complex Home Assistant dashboards!',
    'long_description': '# MakeJinja\n\n## Installation\n\nMakeJinja is available via `pip` and can be installed via\n\n`pip install makejinja`\n\nBeware that depending on other packages installed on your system via pip, there may be incompatibilities.\nThus, we advise leveraging [`pipx`](https://github.com/pypa/pipx) instead:\n\n`pipx install makejinja`\n\n## Usage\n\nIn its default configuration, MakeJinja searches the input folder recursively for files ending in `.jinja`.\nAlso, we copy all contents (except raw template files) of the input folder to the output folder and remove the `.jinja` ending during the render process.\nTo get an overview of the remaining options, we advise you to run `makejinja --help`:\n\n<!-- Regenerate: COLUMNS=120 py makejinja --help | pbcopy -->\n',
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
