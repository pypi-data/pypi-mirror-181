# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_multi_chatgpt']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot>=2.1.5,<3.0.0',
 'nonebot-plugin-apscheduler>=0.2.0,<0.3.0',
 'nonebot-plugin-htmlrender>=0.2.0.1,<0.3.0.0',
 'nonebot2>=2.0.0rc2,<3.0.0',
 'pyyaml>=5.4.1,<6.0.0',
 'revchatgpt==0.0.43']

setup_kwargs = {
    'name': 'nonebot-plugin-multi-chatgpt',
    'version': '3.0.0',
    'description': '',
    'long_description': '# 多账户ChatGPT\n\n## 安装\n\n~~第一种方式~~（暂时不行，等待pr通过）\n\n```\nnb plugin install nonebot_plugin_multi_chatgpt\n```\n\n---\n\n第二种方式，使用一下命令安装\n\n```\npip3 install nonebot_plugin_multi_chatgpt --upgrade\n```\n\n随后在`bot.py`中加上如下代码，加载插件\n\n```\nnonebot.load_plugin(\'nonebot_plugin_multi_chatgpt\')\n```\n\n## 配置\n\n### token方式\n\n在`.env.dev`中配置自己的`chatgpt_session_token_list`即可\n\n多个token，请注意不能换行只能写成一排 例如\n\n```\nchatgpt_session_token_list = ["xxx", "yyy", "zzz"]\n```\n\n如果只有一个session也需要用数组的形式\n\n```\nchatgpt_session_token_list = ["xxxx"]\n```\n\n获取token得方法，打开Application选项卡 > Cookie，复制值`__Secure-next-auth.session-token`并将其粘贴到在`.env.dev`中`session_token`即可。不需要管Authorization的值。\n![](https://chrisyy-images.oss-cn-chengdu.aliyuncs.com/img/image-20221205094326498.png)\n\n### 密码方式\n\n密码登陆需要通过代理来配置，一般配置格式如下。\n\n```\nchatgpt_email_list = ["osyyjozylg@iubridge.com", "lgfo353p@linshiyouxiang.net"]\nchatgpt_passwd_list = ["yy123123", "yy123123"]\nchatgpt_proxy = "http://127.0.0.1:6152"\n```\n\n### 其他\n\n指令前缀，默认值为`chat`\n\n```\nchatgpt_command_prefix = "。"\n```\n\n## 图片相关\n\n### 配置\n\n采用命令进行配置，在此进行简单说明\n\n- 在 bot 连接时，将会在`机器人项目/`自动创建一个名为 `config_multi_chatgpt` 的文件夹（如果不存在），用于存放输出图片相关的配置文件\n- 配置文件名为 `img_out_config.yml`, 初始化时，将写入 `{"global":False}`，代表全局不开启图片输出\n- 在使用以下命令时，会分别在配置中加入`{"groups":[123456,45656,xxx]}` `{"users": [17960000,666,xxx]}` 其分别代表开启图片输出的**群**和**用户**\n\n### 指令\n\n\n| 操作       | 命令                 | 权限             | 备注                                               | 命令别名                   |\n|----------|--------------------| ---------------- |--------------------------------------------------|------------------------|\n| 全局图片输出   | 全局图片开<br />全局图片关   | SUPERUSER        | 开启后，在任何时候都返回图片                                   | gpt全局图片开<br />gpt全局图片关 |\n| 群图片输出    | 群图片开<br />群图片关     | 群主、管理员、SU | 需要在群内发送，开启后，在该群任何时候都返回图片                         | gpt群图片开<br />gpt群图片关   |\n| 用户输出     | 对我输出开<br />对我输出关   | /                | 开启后，对于该用户在任何时候都返回图片                              | 对我图片输出开<br />对我图片输出关   |\n| 某条消息输出   | -p 你好<br />你好 -p   | /                | 在某次请求时，在你要说的话前或者后加`-p` <br /> 则对此条消息，会返回图片       |                        |\n| 查看配置     | 查看输出               | SUPERUSER        | 返回一张图片，包含了图片输出的开关配置                              | 查看图片开关<br />查看图片输出     |\n| su删除某开启的群 | 图片输出删除 g 1111 2222 | SUPERUSER        | 关闭某几个开启图片输出的群，`g`作为参数,<br />不带参数默认为`g`，后跟群号用空格分隔 | 输出删除 g 1111 2222       |\n| su删除某开启的用户 | 图片输出删除 u 1111 2222 | SUPERUSER        | 对某几个人关闭输出，`u`作为参数,<br />不带参数默认为`g`，后跟QQ号用空格分隔    | 输出删除 u 1111 2222       |\n\n\n### 流程\n\n1. 机器人启动时，对配置文件进行检测，不存在则创建\n2. 消息预处理:\n   - 如果消息中包含`-p`，则对此条消息进行图片输出（无论全局、群、用户是否开启），将`-p`去除后，再进行chatGPT请求\n   - 如果消息中不包含`-p`则不处理\n3. 请求chatGPT，得到结果后，对结果进行处理：\n   - 如果消息中代码块符号` ``` `不完整，则补全（chatGPT有时返回不完整）\n   - 根据配置发送图片或者文本\n4. `-p` 或 全局开启，优先级最高，二者之一存在，则对此条消息进行图片输出\n5. 若非上述二者：\n   - 群聊\n     - 如果群开启图片输出，则返回图片\n     - 如果全局关闭但用户开启，则返回图片\n   - 私聊\n     - 如果用户开启图片输出，则返回图片\n\n# Todo\n\n- [X]  返回值渲染为图片\n- [ ]  完善密码登陆\n',
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
