# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_idiom']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot>=2.1.3,<3.0.0', 'nonebot2>=2.0.0b5,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-idiom',
    'version': '0.1.3',
    'description': '',
    'long_description': '# nonebot_plugin_idiom\nnonebot_plugin_idiom\n#改写于\nhttps://github.com/xuhaoShaw/QRobot\n# 感谢！！！\n## 安装方式\n- #### 使用pip\n```\npip install nonebot_plugin_idiom\n```\n- ### 指令:\n```\n指令： < 成语接龙 | 成语接龙 + 一个成语 >\n```\n\n- ### 叠甲:\n```\n第一次发插件，轻喷！\nbug: 如果发现插件有BUG或有建议，欢迎提*Issue*\n```\n',
    'author': 'Your dxn',
    'author_email': '1684193123@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
