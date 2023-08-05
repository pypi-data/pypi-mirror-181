# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ayaka_games', 'ayaka_games.plugins']

package_data = \
{'': ['*'],
 'ayaka_games.plugins': ['data/*', 'data/calc_24/*', 'data/dragon/*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'nonebot-adapter-onebot>=2.1.3,<3.0.0',
 'nonebot-plugin-ayaka>=0.5.4b0,<0.6.0',
 'nonebot2>=2.0.0b5,<3.0.0',
 'pypinyin>=0.47.1,<0.48.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-ayaka-games',
    'version': '0.4.3b0',
    'description': 'a pack of textual game on QQ via nonebot-plugin-ayaka',
    'long_description': '<div align="center">\n\n# ayaka文字小游戏合集 v0.4.3b0\n\n基于[ayaka](https://github.com/bridgeL/nonebot-plugin-ayaka)开发的文字小游戏合集\n\n开发进度 8/10，还剩2个小游戏等待构思\n\n**特别感谢**  [@灯夜](https://github.com/lunexnocty/Meiri) 大佬的插件蛮好玩的~\n\n</div>\n\n## 文档\n\nhttps://bridgel.github.io/ayaka_doc/latest/games/\n',
    'author': 'Su',
    'author_email': 'wxlxy316@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bridgeL/nonebot-plugin-ayaka-games',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
