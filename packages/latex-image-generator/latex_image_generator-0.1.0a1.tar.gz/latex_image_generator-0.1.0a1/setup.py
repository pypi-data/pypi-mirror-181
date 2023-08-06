# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['latex_image_generator']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['generate-latex-image = latex_image_generator.main:main']}

setup_kwargs = {
    'name': 'latex-image-generator',
    'version': '0.1.0a1',
    'description': 'Tool to generate images using LaTeX.',
    'long_description': '# latex-image-generator\n\nTool to generate images using LaTeX.\n',
    'author': 'Kenta Kabashima',
    'author_email': 'kenta_program37@hotmail.co.jp',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/MusicScience37Projects/tools/latex-image-generator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
