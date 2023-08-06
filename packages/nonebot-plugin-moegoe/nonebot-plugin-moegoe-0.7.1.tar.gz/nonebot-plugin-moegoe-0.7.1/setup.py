# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_moegoe']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0', 'nonebot2>=2.0.0-beta.4,<3.0.0', 'rtoml>=0.9.0,<0.10.0']

extras_require = \
{'onebot': ['nonebot-adapter-onebot>=2.0.0-beta.4,<3.0.0']}

setup_kwargs = {
    'name': 'nonebot-plugin-moegoe',
    'version': '0.7.1',
    'description': '日韩中 VITS 模型拟声',
    'long_description': '<!--\n * @Author         : yiyuiii\n * @Date           : 2022-10-11 20:00:00\n * @LastEditors    : yiyuiii\n * @LastEditTime   : 2022-11-29 20:00:00\n * @Description    : None\n * @GitHub         : https://github.com/yiyuiii\n-->\n\n<!-- markdownlint-disable MD033 MD036 MD041 -->\n\n<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>\n</p>\n\n<div align="center">\n\n# nonebot-plugin-moegoe\n\n_✨ 日韩中 VITS 模型拟声 by fumiama✨_\n\n搬运自ZeroBot-Plugin仓库：https://github.com/FloatTech/ZeroBot-Plugin/tree/master/plugin/moegoe\n\n</div>\n\n<p align="center">\n  <a href="https://raw.githubusercontent.com/Yiyuiii/nonebot-plugin-moegoe/master/LICENSE">\n    <img src="https://img.shields.io/github/license/Yiyuiii/nonebot-plugin-moegoe.svg" alt="license">\n  </a>\n  <a href="https://pypi.python.org/pypi/nonebot-plugin-moegoe">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-moegoe.svg" alt="pypi">\n  </a>\n  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">\n</p>\n\n## :gear: 安装方法\n\n`nb plugin install nonebot_plugin_moegoe`\n或 `pip install nonebot_plugin_moegoe`\n\n## :rocket: 使用方式\n\n**在聊天中输入:**\n\n- **让**[派蒙|凯亚|安柏|丽莎|琴|香菱|枫原万叶|迪卢克|温迪|可莉|早柚|托马|芭芭拉|优菈|云堇|钟离|魈|凝光|雷电将军|北斗|甘雨|七七|刻晴|神里绫华|雷泽|神里绫人|罗莎莉亚|阿贝多|八重神子|宵宫|荒泷一斗|九条裟罗|夜兰|珊瑚宫心海|五郎|达达利亚|莫娜|班尼特|申鹤|行秋|烟绯|久岐忍|辛焱|砂糖|胡桃|重云|菲谢尔|诺艾尔|迪奥娜|鹿野院平藏]**说**(中文)\n- **让**[宁宁|爱瑠|芳乃|茉子|丛雨|小春|七海|妃爱|华乃|亚澄|诗樱|天梨|里|广梦|莉莉子]**说日语：**(日语)\n- **让**[Sua|Mimiru|Arin|Yeonhwa|Yuhwa|Seonbae]**说韩语：**(韩语)\n\n例：\n\n- [让派蒙说你好！旅行者。](https://genshin.azurewebsites.net/api/speak?format=mp3&text=你好！旅行者。&id=0)\n- [让宁宁说日语：hello.](https://moegoe.azurewebsites.net/api/speak?text=hello!&id=0)\n- [让Sua说韩语：hello.](https://moegoe.azurewebsites.net/api/speakkr?text=hello!&id=0)\n\n**Bot返回语音**\n\n<!-- <p align="center">\n  <audio src="https://genshin.azurewebsites.net/api/speak?format=mp3&text=你好！旅行者。&id=0"></audio>\n\n<audio src="https://moegoe.azurewebsites.net/api/speak?text=hello!&id=0"></audio>\n\n<audio src="https://moegoe.azurewebsites.net/api/speakkr?text=hello!&id=0"></audio>\n</p> -->\n\n## :gear: 配置方法\n\n在插件初次联网成功运行后，可以发现 BOTROOT/data/moegoe/ 路径下有profile.toml文件，其中可以配置\n\n- 插件优先级 priority\n- 触发正则语句 regex\n\n等等。 修改后保存，重启生效。\n\n**注意：**\n因使用人数过多，目前中文API设置了秘钥限制。在自行获取APIKey后，在配置文件的cnapi url末尾加上\'&code=你的APIKey\'，即可使用。参考[Issue 17](https://github.com/Yiyuiii/nonebot-plugin-moegoe/issues/17#issuecomment-1336317427)\n\n日文和韩文的API目前正常。\n\n当插件版本更新时新配置将覆盖旧配置，如果不希望被覆盖可以在profile.toml中把版本调高。\n\n## :speech_balloon: 常见问题\n\n<details>\n<summary>报错 ERROR: No matching distribution found for nonebot-plugin-moegoe</summary>\n\n[Issue 1](https://github.com/Yiyuiii/nonebot-plugin-moegoe/issues/1)\n\n - 注意安装的包名是带**下划线**的：nonebot_plugin_moegoe\n</details>\n\n<details>\n<summary>API不能正确生成语音</summary>\n\n[Issue 2](https://github.com/Yiyuiii/nonebot-plugin-moegoe/issues/2) | [Issue 4](https://github.com/Yiyuiii/nonebot-plugin-moegoe/issues/4)\n\n- 第一种情况：**中文语音api对输入要求很严**，只支持中文字符和几个标点符号，输入如果包含api无法处理的字符就会无法生成语音，包括英文、叠词、奇怪标点符号等就大概率不行。\n- 第二种情况：当后台在报`encode silk failed: convert pcm file error: exec: "ffmpeg": executable file not found in %PATH% `错误时，表示go-cqhttp编码音频所依赖的ffmpeg包没有被安装，所以不能发送音频。**请自行安装ffmpeg**。*（不过ffmpeg可能不是必须的。如果有人在不安装ffmpeg时能正常使用，请向我反馈，这一点还没有经过测试。）*\n- 第三种情况：**本插件默认优先级为5**，若有其它的插件优先级比5强，且该插件有block截断，则本插件可能无法收到并处理消息。目前需要自行调整插件的优先级。\n</details>\n\n<details>\n<summary>API不能生成较长语音</summary>\n\n目前API生成较长语音的速度很慢（从数十秒到数分钟），为避免该类请求的并发造成资源阻塞，代码中限制了请求时长，可自行修改。\n\n`resp = await client.get(url, timeout=120)`\n</details>\n\n<details>\n<summary>API挂了</summary>\n\n[Issue 7](https://github.com/Yiyuiii/nonebot-plugin-moegoe/issues/7) | [Issue 15](https://github.com/Yiyuiii/nonebot-plugin-moegoe/issues/15)\n\n</details>\n\n\n## :clipboard: 更新日志\n\n#### 2022.11.29 > v0.7.1 :fire:\n- 修复安装失败的BUG。profile.toml的位置改变，之前版本的配置可能无法自动更新profile.toml配置文件。\n\n#### 2022.11.29 > v0.7.0\n- 从__init__.py抽离一些配置组成profile.toml配置文件，现在可以自动从github上抓取url等配置的更新了。\n\n#### 2022.10.11 > v0.6.0\n- 同步更新中文原神语音api\n\n#### 2022.10.03 > v0.5.2\n- 增加包依赖的nonebot版本限制（仅此而已）\n\n#### 2022.08.24 > v0.5.1\n- 在`让xx说xx：`正则式中添加冒号的全角半角匹配`(：|:)`（此外，之前版本已经添加形如`(日语|日文|日本语)`的正则匹配）\n\n#### 2022.08.24 > v0.5.0\n- 添加日语speaker2的API，增加8名可选语音人物\n- 换用httpx以修正requests阻塞多协程的BUG\n- 在中文语音中，将输入文字中的英文符号和0-9数字预处理为中文\n- 优化报错提示\n- 整理代码\n',
    'author': 'yiyuiii',
    'author_email': 'yiyuiii@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yiyuiii/nonebot-plugin-moegoe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
