# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ume']

package_data = \
{'': ['*']}

install_requires = \
['ImageHash>=4.3.0,<5.0.0',
 'pytesseract>=0.3.10,<0.4.0',
 'sewar>=0.4.4,<0.5.0',
 'wheel>=0.37.1,<0.38.0']

setup_kwargs = {
    'name': 'ume',
    'version': '0.1.1',
    'description': 'Unique Meme Engine.',
    'long_description': '# Unique Meme Engine',
    'author': 'isik-kaplan',
    'author_email': 'isik.kaplan@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wsd/ume',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
