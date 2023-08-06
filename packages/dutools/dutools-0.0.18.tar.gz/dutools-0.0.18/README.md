# dutools

### python关系型数据库的自用轮子

### 轻量级 依赖 pymsql 与 psycopg2

### 新增 PostGreSql

### 新增 AsyncGoogle google_transl 采用 httpx 谷歌翻译

### 新增 RsaCrypto 非对称加密

# 安装包

```bash
pip install dutools
```

#### 使用 RsaCrypto

# 导入包
```text
from dutools.base_settings import EsSettings, BaseSettings
Windows 开发环境
Linux   生产环境
BaseSettings 一个通过(系统)自动判断生产与开发环境，在开发与生产环境中切换不同的打印颜色区别的 配置类

EsSettings 基于BaseSettings 
  4个内置函数
     cat()           查看配置信息, sta=True 时打印settings
    _create_index()  创建索引
    _delete_index()  删除索引
    __clear()        清空当前索引数据


conf.yml 文件示例
test:
  es:
    index: cards
    hosts:
      - http://127.0.0.1:9200
      - http://192.168.0.1:9200
    mapping_file: cards.json
  mysql:
    host: ...
    
env:
  es:
    index: cards
    hosts:
      - http://127.0.0.1:9200
      - http://192.168.0.1:9200
    mapping_file: cards.json
```

# from dutools import RsaCrypto
RsaCrypto 提供加解密与生成对应密钥

```python
import os
import json
from dutools.RSA import RsaCrypto  
# 使用场景： 用户登录 需要提供一个接口将加密文件传送给前端, 前端加密， 后端解密 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 自动获取路径或者手动给出都可
rsa = RsaCrypto(BASE_DIR)  # 实例化
rsa.create_rsa_key()  # 创建密钥

data = {"user": "195947454", "name": "H, DJ"}
a = rsa.encrypt(json.dumps(data))  # 加密 XtEtC...xE2nTKKLvUPWXeNTGsN5pI=
b = rsa.decrypt(a)  # 解密
print(a)
print(json.loads(b))


```

#### 使用 AsyncGoogle

# 导入包

# from dutools import AsyncGoogle

AsyncGoogle 提供一个直接使用的方法 google

```python
import asyncio
from dutools.translator import AsyncGoogle
from dutools.translator import google_transl  # 直接使用此方法亦可

google = AsyncGoogle(
    timeout=5,
    proxies=None,
    http2=False  # 是否启用HTTP2
)

data = [
    "For other COVID-19 related advisories for F&B establishments, see Safe Distancing Measures."
    "For information on VDS and ceasing of On-Arrival Testing at wholesale markets, see SMMs at wholesale markets.",
    "For information on food safety during this Covid-19 period, see COVID-19 and food safety.",
]

task_ist = []
for i in data:
    task = asyncio.create_task(google.translate(i, 'zh'))
    task_ist.append(task)
res = asyncio.gather(*task_ist)
print(res)


```

#### 使用 PostGreSql

# 导入包

# from dutools import PostGreSql

```python
# 构建一个PostGreSql配置
from dutools.pg_sql import PostGreSql

conf = {'database': "db",
        "user": "postgres",
        "password": "test",
        "host": "127.0.0.1",
        "port": "5432"}

# 例子
sql = 'SELECT DISTINCT * FROM "public"."test"  ORDER BY "userid" LIMIT 20'
conn = PostGreSql(conf)
# 单条数据
data = conn.fetchone(sql)  # 默认返回一个字典 {}
print(data)
# 多条数据
data = conn.fetchone(sql)  # 默认返回一个字典列表 [{},{}]
for row in data:
    print(row)  # {"name": "张三", "age": 25}

# 多数据查询
data = conn.fetchmany(sql, size=2000)  # 默认返回一个字典列表 [{},{}]
for row in data:
    print(row)  # {"name": "张三", "age": 25}

# 批量操作
# 1. 批量插入
sql = 'insert into public.user (id,name,age) VALUES %s'  # 批量操作时字段须保持一致 值用一个 %s 代替
data = [(1, "张三", 25), (2, "黄DJ", 25)]
conn.commit(sql, data)

# 1. 批量更新
sql = 'UPDATE public.user SET name = data.name, age = data.age FROM (VALUES %s) AS data (id, name, age) WHERE user.id = data.id'  # 此处应用psycopg2官方例子
data = [(1, "法外狂徒", 36), (2, "狗子哥", 27)]
conn.commit(sql, data)
```

## MYSQL

# 构建一个mysql配置

```python
from dutools.crud import Mysql, MysqlDB, mysql_ssd

conf = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": 'test',
    "password": 'test',
    "database": "users",
    "charset": "utf8mb4"
}
# 用法1
# 适合长时间保持连接状态的 MysqlDB
db = MysqlDB(conf)

# 插入数据
item = {"name": "张三", "age": 25}  # 注意字典key 需和数据库字段名称保持一致
sql = 'insert into user(%s) values(%s)'
db.commit(sql, data=item)
# 批量写入数据
item = [{"name": "张三", "age": 25}, {"name": "黄DJ", "age": 25}]  # 注意字典key 需和数据库字段名称保持一致
sql = 'insert into user(%s) values(%s)'
db.commit(sql, data_list=item)

# 更新数据
sql = 'update user set %s where name="黄DJ"'  # 请注意条件
db.commit(sql, data=item, up=True)  # 再做更新操作时，需要加上up=True

# 读取数据
sql = "select * from user"
data = db.fetchall(sql)  # 此方法返回一个 list
data = db.fetchone(sql)  # 此方法返回一个 默认字典 如不再 conf 中配置 cursorclass
```

#### Mysql 类 基本操作与 MysqlDB 一致

+ 比如需要关注数据库中是否有当天的数据，那么你可以使用他, 应为他适用短链接
+ 请使用 with

```python
# 导入包
from dutools.crud import Mysql, MysqlDB, mysql_ssd

# 构建一个mysql配置
conf = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": 'test',
    "password": 'test',
    "database": "users",
    "charset": "utf8mb4"
}
with Mysql(conf) as cur:
    # 插入数据
    item = {"name": "张三", "age": 25}  # 注意字典key 需和数据库字段名称保持一致
    sql = 'insert into user(%s) values(%s)'
    cur.commit(sql, data=item)

```

#### mysql_ssd

+ 用于超大数据读取

```python
# 导入包
from dutools.crud import mysql_ssd

# 构建一个mysql配置
conf = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": 'test',
    "password": 'test',
    "database": "users",
    "charset": "utf8mb4"
}

# 例子
sql = "select * from user"
with mysql_ssd(conf) as cur:
    cur.execute(sql)
    while True:
        row = cur.fetchone()
        if not row:
            break
        print(row)


```

