# Python tools

[yourtools](https://pypi.org/project/yourtools/)

## Installation
```shell
pip3 uninstall yourtools
pip3 install yourtools
```

## Table of Contents

- WeChat
  - send_msg 发送应用消息
  - upload_media 上传临时素材文件到企微，并返回media_id
- MySQL
  - query 执行普通查询SQL
  - execute 执行DML SQL
- Hive
  - query 执行普通查询SQL
  - exec_ddl_sql 执行DML SQL

## Example

### 1、MySQL

```python
from yourtools import MySQL

def test_mysql():
    dbconfg = {
        'host': '172.0.0.1',
        'port': 3306,
        'username': 'root',
        'password': '123456',
        'db': 'test',
        'charset': 'utf8'
    }
    mysql = MySQL(dbconfg)
    # query data
    result = mysql.query("select * from users")
    print(result)
    # dml sql 
    result = mysql.execute("insert into users(name,birthday,ts) values('灭霸2','2022-11-01 16:00:00','2022-11-01 16:00:00') ")
```

### 2、Hive
```python
from yourtools import Hive

hive_connection = {
    'host': '127.0.0.1',
    'port': 10000,
    'db': 'ods',
    'username': '',
    'auth': 'NOSASL'
}
hive = Hive(hive_connection)
hive_sql="""
select * from ods.ods_user
"""
rows = hive.query(hive_sql)
print(rows)

```

### 3、WeChat
```python
from yourtools import WeChat

# WeChat(corpid，Secret，AgentId)
qw = WeChat("asdg234234", "OINFSokasdIOKflsafdaOOKFD", 1000000)
data = {
    "touser": "198297694527839423",
    "toparty": "",
    "totag": "",
    "msgtype": "text",
    "agentid": 1000000,
    "text": {
        "content": "你的快递已到，请携带工卡前往邮件中心领取。\n出发前可查看<a href=\"http://work.weixin.qq.com\">邮件中心视频实况</a>，聪明避开排队。"
    },
    "safe": 0,
    "enable_id_trans": 0,
    "enable_duplicate_check": 0,
    "duplicate_check_interval": 1800
}
send_statu = qw.send_msg(data)
print(send_statu)
```
