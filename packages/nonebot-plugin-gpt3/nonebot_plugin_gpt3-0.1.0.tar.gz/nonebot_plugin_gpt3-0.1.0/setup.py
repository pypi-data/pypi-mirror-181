# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_gpt3']

package_data = \
{'': ['*']}

install_requires = \
['openai>=0.25.0,<0.26.0']

setup_kwargs = {
    'name': 'nonebot-plugin-gpt3',
    'version': '0.1.0',
    'description': '',
    'long_description': '# nonebot-plugin-gpt3\n\n',
    'author': 'chrisyy',
    'author_email': '1017975501@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
