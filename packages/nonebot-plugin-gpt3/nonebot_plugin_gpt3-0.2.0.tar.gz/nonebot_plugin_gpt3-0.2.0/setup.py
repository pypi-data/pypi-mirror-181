# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_gpt3']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot>=2.1.5,<3.0.0',
 'nonebot2>=2.0.0rc2,<3.0.0',
 'openai>=0.25.0,<0.26.0']

setup_kwargs = {
    'name': 'nonebot-plugin-gpt3',
    'version': '0.2.0',
    'description': '',
    'long_description': '<div align="center">\n  <a href="https://v2.nonebot.dev/store"><img src="https://s2.loli.net/2022/06/16/opBDE8Swad5rU3n.png" width="180" height="180" alt="NoneBotPluginLogo"></a>\n  <br>\n  <p><img src="https://s2.loli.net/2022/06/16/xsVUGRrkbn1ljTD.png" width="240" alt="NoneBotPluginText"></p>\n</div>\n\n<div align="center">\n\n# Nnonebot-plugin-gpt3\n\n_✨ 基于openai GPT3官方API的对话插件 ✨_\n\n<p align="center">\n  <img src="https://img.shields.io/github/license/EtherLeaF/nonebot-plugin-colab-novelai" alt="license">\n  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python">\n  <img src="https://img.shields.io/badge/nonebot-2.0.0r4+-red.svg" alt="NoneBot">\n  <a href="https://pypi.python.org/pypi/nonebot-plugin-gpt3">\n      <img src="https://img.shields.io/pypi/dm/nonebot-plugin-gpt3" alt="pypi download">\n  </a>\n</p>\n\n\n</div>\n\n## 功能\n\n- [x] 上下文\n- [x] 会话导出\n- [x] 返回文字图片渲染\n- [x] 每个人单独会话\n- [ ] 更多配置\n\n## 安装\n\n1.  使用 nb-cli\n\n```\nnb plugin install nonebot_plugin_gpt3\n```\n\n2.   通过包管理器安装，可以通过nb，pip3，或者poetry等方式安装，以pip为例\n\n```\npip install nonebot_plugin_gpt3\n```\n\n随后在`bot.py`中加上如下代码，加载插件\n\n```\nnonebot.load_plugin(\'nonebot_plugin_gpt3\')\n```\n\n## 配置\n\n对于官方openai接口只需配置API Keys即可，所以请填写API在您配置的`chatgpt_token_path`下面，默认路径是`config/chatgpt_img_config.yml`\n\n文件内格式如下，有多个Key请按照如下格式配置。\n\n```\napi_keys:\n  - XXX\n  - YYY\n```\n\n之后是一些自定义配置，根据注释可以自行修改，如果需要配置请在`env.dev`下进行配置。\n\n```\nchatgpt_api_key_path = "config/chatgpt_api.yml" # api文件\nchatgpt_command_prefix = "chat"\t\t\t\t\t\t\t\t\t# 触发聊天的前缀\nchatgpt_need_at = False\t\t\t\t\t\t\t\t\t\t\t\t\t# 是否需要@\nchatgpt_image_render = False\t\t\t\t\t\t\t\t\t\t# 是否需要图片渲染\n```\n\n\n## 如何使用？\n\n',
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
