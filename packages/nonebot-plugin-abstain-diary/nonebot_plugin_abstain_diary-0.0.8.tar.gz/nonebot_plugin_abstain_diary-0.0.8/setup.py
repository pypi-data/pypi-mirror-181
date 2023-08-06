# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_abstain_diary']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0',
 'nonebot-adapter-onebot>=2.1.3,<3.0.0',
 'nonebot2>=2.0.0b5,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-abstain-diary',
    'version': '0.0.8',
    'description': '适用于nonebot2 v11的戒色打卡日记插件',
    'long_description': '<div align="center">\n  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>\n  <br>\n  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>\n</div>\n\n<div align="center">\n\n# nonebot_plugin_abstain_diary\n  \n_✨ NoneBot 戒色打卡日记 插件 ✨_\n  \n<a href="https://github.com/Ikaros-521/nonebot_plugin_abstain_diary/stargazers">\n    <img alt="GitHub stars" src="https://img.shields.io/github/stars/Ikaros-521/nonebot_plugin_abstain_diary?color=%09%2300BFFF&style=flat-square">\n</a>\n<a href="https://github.com/Ikaros-521/nonebot_plugin_abstain_diary/issues">\n    <img alt="GitHub issues" src="https://img.shields.io/github/issues/Ikaros-521/nonebot_plugin_abstain_diary?color=Emerald%20green&style=flat-square">\n</a>\n<a href="https://github.com/Ikaros-521/nonebot_plugin_abstain_diary/network">\n    <img alt="GitHub forks" src="https://img.shields.io/github/forks/Ikaros-521/nonebot_plugin_abstain_diary?color=%2300BFFF&style=flat-square">\n</a>\n<a href="./LICENSE">\n    <img src="https://img.shields.io/github/license/Ikaros-521/nonebot_plugin_abstain_diary.svg" alt="license">\n</a>\n<a href="https://pypi.python.org/pypi/nonebot_plugin_abstain_diary">\n    <img src="https://img.shields.io/pypi/v/nonebot_plugin_abstain_diary.svg" alt="pypi">\n</a>\n<a href="https://www.python.org">\n    <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">\n</a>\n\n</div>\n\n适用于nonebot2 v11的戒色打卡日记插件    \n\n## 🔧 开发环境\nNonebot2：2.0.0b5  \npython：3.8.13  \n操作系统：Windows10（Linux兼容性问题不大）  \n编辑器：VS Code  \n\n## 💿 安装\n\n### 1. nb-cli安装（推荐）\n在你bot工程的文件夹下，运行cmd（运行路径要对啊），执行nb命令安装插件，插件配置会自动添加至配置文件  \n```\nnb plugin install nonebot_plugin_abstain_diary\n```\n\n### 2. 本地安装\n将项目clone到你的机器人插件下的对应插件目录内（一般为机器人文件夹下的`src/plugins`），然后把`nonebot_plugin_abstain_diary`文件夹里的内容拷贝至上一级目录即可。  \nclone命令参考（得先装`git`，懂的都懂）：\n```\ngit clone https://github.com/Ikaros-521/nonebot_plugin_abstain_diary.git\n``` \n也可以直接下载压缩包到插件目录解压，然后同样提取`nonebot_plugin_abstain_diary`至上一级目录。  \n目录结构： ```你的bot/src/plugins/nonebot_plugin_abstain_diary/__init__.py```  \n\n\n### 3. pip安装\n```\npip install nonebot_plugin_abstain_diary\n```  \n打开 nonebot2 项目的 ```bot.py``` 文件, 在其中写入  \n```nonebot.load_plugin(\'nonebot_plugin_abstain_diary\')```  \n当然，如果是默认nb-cli创建的nonebot2的话，在bot路径```pyproject.toml```的```[tool.nonebot]```的```plugins```中添加```nonebot_plugin_abstain_diary```即可  \npyproject.toml配置例如：  \n``` \n[tool.nonebot]\nplugin_dirs = ["src/plugins"]\nplugins = ["nonebot_plugin_abstain_diary"]\n``` \n\n### 更新版本\n```\nnb plugin update nonebot_plugin_abstain_diary\n```\n\n## 🔧 配置  \n暂无，感觉没必要自定义了，先不开放。  \n\n## 🎉 功能\n戒色打卡（群聊内使用）。将用户期望戒色天数，用户群，用户QQ昵称，用户当前戒色天数等信息记录于本地bot的data/data.json文件中，方便用户对自己戒色信息的相关查询。  \n*财能使人贪，色能使人嗜，名能使人矜，潜能使人倚，四患既都去，岂在浮尘里。*  \n\n## 👉 命令\n\n以下命令使用时记得加上自己的命令前缀哦~（一般为/）  \n\n### 1、戒色帮助\n命令结构：```/戒色帮助``` 或 ```/戒色说明``` 或 ```/戒色命令```  \n例如：```/戒色帮助```  \nbot返回内容：  \n```\n戒色命令如下(【】中的才是命令哦，记得加命令前缀)：\n【戒色目标】【设置戒色目标】，后面追加戒色目标天数。例如：/戒色目标 30\n\n【戒色】【戒色打卡】，每日打卡，请勿中断喵。例如：/戒色\n\n【群戒色】【戒色情况】【群友戒色情况】，查看本群所有戒色情况。例如：/群戒色\n\n【放弃戒色】【取消戒色】【不戒色了】，删除戒色目标。例如：/放弃戒色\n\n【群戒色】【戒色情况】【群友戒色情况】，查看本群所有戒色情况\n\n财能使人贪，色能使人嗜，名能使人矜，潜能使人倚，四患既都去，岂在浮尘里。\n```\n\n### 2、戒色目标\n命令结构：```/戒色目标``` 或 ```/设置戒色目标``` 后面追加 戒色目标天数  \n例如：```/戒色目标 30```  \nbot返回内容：  \n```\n戒色目标天数：30，设置成功！今天是打卡第一天，加油！你我都有美好的未来！\n```\n\n### 3、戒色\n命令结构：```/戒色``` 或 ```/戒色打卡```  \n例如：```/戒色```  \nbot返回内容：  \n```\n戒色打卡成功！您已打卡1天！\n```\n\n### 4、群戒色\n命令结构：```/群戒色``` 或 ```/戒色情况``` 或 ```/戒色情况```  \n例如：```/群戒色```  \nbot返回内容：  \n```\n🥵🥵🥵群戒色信息\n打卡数    群昵称    目标数\n——————————————\n1    只因    3\n3    霓    7\n```\n\n### 4、放弃戒色\n命令结构：```/放弃戒色``` 或 ```/取消戒色``` 或 ```/不戒色了```  \n例如：```/放弃戒色```  \nbot返回内容：  \n```\n戒色打卡已取消，您可以开冲啦！！！\n```\n\n## 📝 更新日志\n\n<details>\n<summary>展开/收起</summary>\n\n### 0.0.1\n\n- 插件初次发布  \n  \n### 0.0.2\n\n- 修复首次运行数据文件加载失败bug\n- 优化功能逻辑，设置目标即为开始打开第一天\n- 优化文字描述\n\n### 0.0.3\n\n- 新增取消戒色功能\n- 优化戒色目标天数校验\n- 修复文件第二次加载时的数据异常bug\n\n### 0.0.4\n\n- 修复文件json数据加载bug\n- 优化文档\n\n### 0.0.5\n\n- bug也太多了，绷\n\n### 0.0.6\n\n- 优化输出文字排版和描述\n\n### 0.0.7\n\n- 优化日志打印\n\n### 0.0.8\n\n- 添加插件元信息，标准化\n- 文档描述优化\n\n\n</details>\n\n## 项目打包上传至pypi\n\n官网：https://pypi.org，注册账号，在系统用户根目录下创建`.pypirc`，配置  \n``` \n[distutils] \nindex-servers=pypi \n \n[pypi] repository = https://upload.pypi.org/legacy/ \nusername = 用户名 \npassword = 密码\n```\n\n### poetry\n\n```\n# 参考 https://www.freesion.com/article/58051228882/\n# poetry config pypi-token.pypi\n\n# 1、安装poetry\npip install poetry\n\n# 2、初始化配置文件（根据提示填写）\npoetry init\n\n# 3、微调配置文件pyproject.toml\n\n# 4、运行 poetry install, 可生成 “poetry.lock” 文件（可跳过）\npoetry install\n\n# 5、编译，生成dist\npoetry build\n\n# 6、发布(poetry config pypi-token.pypi 配置token)\npoetry publish\n\n```\n\n### twine\n\n```\n# 参考 https://www.cnblogs.com/danhuai/p/14915042.html\n#创建setup.py文件 填写相关信息\n\n# 1、可以先升级打包工具\npip install --upgrade setuptools wheel twine\n\n# 2、打包\npython setup.py sdist bdist_wheel\n\n# 3、可以先检查一下包\ntwine check dist/*\n\n# 4、上传包到pypi（需输入用户名、密码）\ntwine upload dist/*\n```',
    'author': 'Ikaros',
    'author_email': '327209194@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Ikaros-521/nonebot_plugin_abstain_diary',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
