# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_ikun_evolution',
 'nonebot_plugin_ikun_evolution.model',
 'nonebot_plugin_ikun_evolution.psql_db',
 'nonebot_plugin_ikun_evolution.service',
 'nonebot_plugin_ikun_evolution.xiaor_battle_system',
 'nonebot_plugin_ikun_evolution.xiaor_battle_system.src',
 'nonebot_plugin_ikun_evolution.xiaor_battle_system.src.tools']

package_data = \
{'': ['*'],
 'nonebot_plugin_ikun_evolution': ['gamedata/*',
                                   'gamedata/image/item/*',
                                   'gamedata/image/notice/*',
                                   'gamedata/json/*']}

install_requires = \
['gino>=1.0.1,<2.0.0', 'json5>=0.9.10,<0.10.0', 'lagom>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-ikun-evolution',
    'version': '1.0.0',
    'description': '移植自真寻的q群小游戏',
    'long_description': '# 只因进化录\n\n移植自真寻的[只因进化录](https://github.com/RShock/ikun_evolution)\n\n## 安装\n\n### 插件安装\n```\npip install nonebot_plugin_ikun_evolution\n```\n在 nonebot2 项目中设置 load_plugin()\n```\nnonebot.load_plugin(\'nonebot_plugin_ikun_evolution\')\n```\n\n### 数据库配置\n\n你需要安装一个[postgresql数据库](https://hibikier.github.io/zhenxun_bot/docs/installation_doc/install_postgresql.html)才能进行游戏\n\n安装完毕后，在`env.dev`里填上刚刚的数据库链接\n```\npsql = "postgresql://名字:密码@127.0.0.1:5432/数据库名字"\n```\n\n如果按真寻教程就是\n```\npsql = "postgresql://uname:zhenxun@127.0.0.1:5432/testdb"\n```\n\n这步有点困难，好处是再也不用担心误删数据库了。请加油罢\n',
    'author': '小r',
    'author_email': '418648118@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/RShock/nonebot_plugin_ikun_evolution',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
