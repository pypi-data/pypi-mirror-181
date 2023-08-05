# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nonebot_plugin_majsoul',
 'nonebot_plugin_majsoul.interceptors',
 'nonebot_plugin_majsoul.network',
 'nonebot_plugin_majsoul.paifuya',
 'nonebot_plugin_majsoul.paifuya.data',
 'nonebot_plugin_majsoul.paifuya.data.models',
 'nonebot_plugin_majsoul.paifuya.mappers',
 'nonebot_plugin_majsoul.paifuya.parsers',
 'nonebot_plugin_majsoul.res',
 'nonebot_plugin_majsoul.utils']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0',
 'icmplib>=3.0.3,<4.0.0',
 'matplotlib>=3.6.2,<4.0.0',
 'monthdelta>=0.9.1,<0.10.0',
 'nonebot-adapter-onebot>=2.1.5,<3.0.0',
 'nonebot2>=2.0.0rc1,<3.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'typing-extensions>=4.4.0,<5.0.0',
 'tzlocal>=4.2,<5.0']

setup_kwargs = {
    'name': 'nonebot-plugin-majsoul',
    'version': '0.1.2',
    'description': '',
    'long_description': '<!-- markdownlint-disable MD033 MD036 MD041 -->\n\n<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>\n</p>\n\n<div align="center">\n\nnonebot-plugin-majsoul\n============\n\n_✨ 雀魂信息查询插件 ✨_\n\n</div>\n\n\n<p align="center">\n  <a href="https://raw.githubusercontent.com/ssttkkl/nonebot-plugin-majsoul/master/LICENSE">\n    <img src="https://img.shields.io/github/license/ssttkkl/nonebot-plugin-majsoul.svg" alt="license">\n  </a>\n  <a href="https://pypi.python.org/pypi/nonebot-plugin-majsoul">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-majsoul.svg" alt="pypi">\n  </a>\n  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">\n</p>\n\n受[DaiShengSheng/Majsoul_bot](https://github.com/DaiShengSheng/Majsoul_bot)启发而写的雀魂信息查询 Bot 插件。\n\n支持适配器：Onebot V11\n\n## 功能\n\n### 雀魂牌谱屋\n\n#### 查询个人数据（可按照时间、按照场数、按照房间类型查询）\n\n指令：`/雀魂(三麻)信息 <雀魂账号> [<房间类型>] [最近<数量>场] [最近<数量>{天|周|个月|年}]`\n\n![雀魂信息](img/majsoul_info.png)\n\n![雀魂信息2](img/majsoul_info_2.png)\n\n#### 查询个人最近对局（可按照房间类型查询）\n\n指令：`/雀魂(三麻)对局 <雀魂账号> [<房间类型>]`\n\n![最近对局](img/records.png)\n\n![最近对局（消息）](img/records_forward.png)\n\n#### 绘制个人PT推移图\n\n指令：`/雀魂(三麻)PT图 <雀魂账号> [最近<数量>场] [最近<数量>{天|周|个月|年}]`\n\n![雀魂PT推移图](img/pt_plot.png)\n\n![雀魂PT推移图（图）](img/pt_plot_img.png)\n\n## See Also\n\n- [nonebot-plugin-mahjong-utils](https://github.com/ssttkkl/nonebot-plugin-mahjong-utils)：日麻小工具插件。支持手牌分析、番符点数查询。\n- [nonebot-plugin-mahjong-scoreboard](https://github.com/ssttkkl/nonebot-plugin-mahjong-scoreboard)\n  ：日麻计分器。为面麻群友提供日麻对局分数记录。根据马点进行PT精算，统计PT增减，支持对局与榜单查询与导出。\n\n## LICENSE\n\nAGPLv3\n',
    'author': 'ssttkkl',
    'author_email': 'huang.wen.long@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
