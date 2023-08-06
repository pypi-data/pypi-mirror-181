# 导入方法
```cmd
pip install mongodb_to_other
```

## 一.mongodb转xls

### 1.1注意事项
请确保自己的mongodb为此格式

_加粗的可以自行更改_

>**testdb**
>>collections
>>>**userdb**

### 1.2 导入

```python
    from mongodb_to_other import mongodb_to_xls
```
### 1.3使用

```python
    from mongodb_to_other import mongodb_to_xls
    #倒库
    mongodb_to_xls("数据名","集合名","xls文件路径",port=int('数据库端口(默认为27017)'),ip="mongodb数据库所在的ip地址(默认为127.0.0.1)",name="数据库用户名(默认为None)",password="数据库密码(默认为None)")
```
在上面代码中 *mongodb_to_xls* 函数有三个必要值，**第一个值**为数据库的名称，**第二个值**为数据库中collections文件夹下要转换的集合，**第三个值**为要输出的文件地址

## 二.mongodb转json

### 2.1简介
**注意事项与*mongodb转xls*一样**
这一个模块主要是为了*windows*用户设计
因为*windows*用户无法使用*mongodb的导出工具*

### 2.2导入


```python
    from mongodb_to_other import mongodb_to_json
```

### 2.3使用

```python
    from mongodb_to_other import mongodb_to_json
    #倒库
    mongodb_to_json("数据名","集合名","xls文件路径",port=int('数据库端口(默认为27017)'),ip="mongodb数据库所在的ip地址(默认为127.0.0.1)",name="数据库用户名(默认为None)",password="数据库密码(默认为None)")
```
在上面代码中 *mongodb_to_xls* 函数有三个必要值，**第一个值**为数据库的名称，**第二个值**为数据库中collections文件夹下要转换的集合，**第三个值**为要输出的文件地址

## 三.mongodb转my_sql

### 3.1注意事项
- 转换后mysql会变为如下
```
表名: mongodb中的set_name
--------------------------------------
| _id(mongodb中的id) |  key  |  key  |
--------------------------------------
| xxxxxxxxxxxxxxxxx  | value | value |(第一条)
--------------------------------------
| xxxxxxxxxxxxxxxxx  | value | value |(第二条)
--------------------------------------
```
- 请注意**mysql**数据库中**没有**与mongodb中的set_name相同的表,如果有**重复**会报错

- 请注意**mysql**默认为3306端口**无法改变**

- 请注意**mysql必须**要有用户

### 3.2导入

```python
    from mongodb_to_other import mongodb_to_mysql
```

### 3.3使用


```python
    from mongodb_to_other import mongodb_to_mysql
    #倒库
    mongodb_to_json("mongodb数据名","mongodb集合名","mysql数据库名","mysql用户名","mysql用户密码",s_ip="你的mysql数据库ip(默认为127.0.0.1）",port=int('mongodb数据库端口(默认为27017)'),ip="mongodb数据库所在的ip地址(默认为127.0.0.1)",name="mongodb数据库用户名(默认为None)",password="mongodb数据库密码(默认为None)")
```


给个星星吧