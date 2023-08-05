# **otl 工具集**
---
# 安装方式
```shell script
pip install otl
```
---

### 封装企业微信接口
```python
from otl.wechat.wechat_api import WechatApi

GLOBAL_WECHAR_CONFIG = {
        'NAME': 'xxx',

        #企业的id，在管理端->"我的企业" 可以看到
        'CORP_ID': '',

        #应用列表 可以配置多个应用
        'APP_LIST': {
            'warning_robot': {           #报警机器人
                'APP_ID': '',           #APPID
                'APP_SECRET': '',       #APP密钥
                'switch': 'on',          #是否开启
            },
        }
    }

if __name__ == '__main__':
    we = WechatApi(GLOBAL_WECHAR_CONFIG)
    status, res = we.apps['warning_robot'].send(
        msg_type='text',
        to_users_list=['xxx'],
        msg_string='xxx'
    )
    if not status:
        print(res)
```
### 封装mysql方法
```python
from otl.db import MysqlDbBase


class Db1(MysqlDbBase):
    host = '1.1.1.1'
    port = 3306
    user = 'test_user'
    password = 'test_pwd'
    db = 'test_db'

# 实例化
db1 = Db1()
# 查询操作 -> 返回数据: list
db1.query("select ***")
# 写入操作 -> 返回影响行数: int
db1.insert("insert into ***")
# 更新操作 -> 返回影响行数: int
db1.update("update ***")
# 删除操作 -> 返回影响行数: int
db1.delete("delete ***")
```

### 发送邮件
```python
# -*- coding: utf-8 -*-
from otl.email import EmailApi
CONFIG = {
    # 组 支持多个组
    'team1': {
        'name': '',         # 组名 即邮件主题
        'user': '',         # 发件人
        'password': '',     # 发件人密码
        'smtp': '',         # smtp服务器
        'port': 25,
        'to_list': ['aaa@aa.com'],      # 收件人列表
        'cc_list': []       # 抄送列表
    }
}

if __name__ == '__main__':
    ea = EmailApi(CONFIG).team1    # 组名
    # 添加文本
    ea.add_str('lalala')
    # 添加图片
    ea.add_image("/a/b/123.jpg")
    # 添加表格
    ea.add_table([['姓名', '年龄', '性别'], ['aaa', 25, '男'], ['ccc', 25, '男']])
    # 添加附件
    ea.add_attr("/a/b/wechat.tgz")
    status, res = ea.send_email()
    if status:
        print('success')
    else:
        print('error: {}'.format(res))

```