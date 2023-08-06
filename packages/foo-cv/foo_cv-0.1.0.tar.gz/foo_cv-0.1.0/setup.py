# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['foo_cv']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=3.1.2,<4.0.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['foo-cv = foo_cv.cli:main']}

setup_kwargs = {
    'name': 'foo-cv',
    'version': '0.1.0',
    'description': 'Separate content and style for CV generation',
    'long_description': '# FOO CV\n\n> Separate content and design for CV\n\nWe provide two files:\n- Content given as JSON and\n- a Jinja2 LaTeX template.\n\nThe provided Python script merely connects the two and generates a TeX file that can then be processed using PDFLaTeX.\n\n[`json_resume`](https://github.com/prat0318/json_resume) is the main source of inspiration for this.\n\n## The profile picture\n\nThe picture was created using [Dalle](https://labs.openai.com/) given the description:\n\n> Create a portrait of Elrond mixed with Worf\n',
    'author': 'Dror Atariah',
    'author_email': 'drorata@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
