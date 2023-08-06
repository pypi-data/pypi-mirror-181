# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ayaka',
 'ayaka.depend',
 'ayaka.driver',
 'ayaka.driver.ayakabot_driver',
 'ayaka.extension']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot>=2.1.3,<3.0.0', 'nonebot2>=2.0.0b5,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-ayaka',
    'version': '0.5.4b1',
    'description': 'a useful plugin providing convinient tools for the development of textual game on QQ',
    'long_description': '<div align="center">\n\n# Ayaka 0.5.4b1\n\n<img src="https://img.shields.io/pypi/pyversions/nonebot-plugin-ayaka">\n\n</div>\n\n## 文档\n\nhttps://bridgel.github.io/ayaka_doc/\n',
    'author': 'Su',
    'author_email': 'wxlxy316@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://bridgel.github.io/ayaka_doc/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
