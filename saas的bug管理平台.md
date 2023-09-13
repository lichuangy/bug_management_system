## Day01准备

## 今日概要

- 虚拟环境
- 项目框架
- git实战应用
- 通过python与腾讯sms发送短信

## 详解

### 1.虚拟环境 virtualenv&virtualenvwrapper-win

>  Python虚拟环境(Virtual Environment)的作用是创建一个独立的Python运行环境,用来隔离不同项目之间的依赖包管理。

#### 1.1安装

~~~ 
pip install virtualenv virtualenvwrapper-win -i https://pypi.tuna.tsinghua.edu.cn/simple
# -i 后面是指定镜像源
~~~

#### 1.2创建虚拟环境

~~~ 
mkvirtualenv -a 虚拟环境存放路径 虚拟环境就名称
mkvirtualenv -a F:\python_code\virtualenv\django_saas django_saas01

# 此时当前所在的目录就是创建环境变量的目录，可以提前新建一个目录然后在目录下面创建虚拟环境

# 也可以只通过virtualenv创建虚拟环境，只是virtualenvwrapper-win方便管理
	virtualenv env

~~~

~~~ 
1.打开终端
2.安装virtualenv  virtualenvwrapper-win
3.关闭终端，再重新打开
4.通过命令，进入指定目录
	win:
		D:
		cd xxx
	mac:
		cd xxx
5.创建虚拟环境
	mkvirtualenv 虚拟环境名
	mkvirtualenv py_django
~~~

#### 1.3虚拟环境管理操作

~~~ 
1. 创建虚拟环境
mkvirtualenv env_name

2. 激活虚拟环境
workon env_name

3. 离开虚拟环境
deactivate

4. 删除虚拟环境
rmvirtualenv env_name

5. 列出所有虚拟环境
lsvirtualenv
 
6. 快速切换虚拟环境
workon

7. 显示当前的虚拟环境
virtualenv_current_env_name

8. 在虚拟环境中安装包
pip install package_name

9. 将当前虚拟环境复制给其他用户
cpvirtualenv env_name /path/to/other/user

10. 显示虚拟环境的文件路径
cdvirtualenv

11. 重命名虚拟环境
mvvirtualenv old_env_name new_env_name
~~~

#### 1.4在虚拟环境中安装模块

- 激活虚拟环境
- 在激活的虚拟环境中安装模块

~~~~
pip3 install django==1.11.28 -i https://pypi.tuna.tsinghua.edu.cn/simple

# 注意： python3.7+django1.11.7 创建项目报错 使用 django1.11.28

~~~~





# day02

- 腾讯发送短信
- Djangod的ModeForm组件
- 注册逻辑
- redis



## 今日概要

## 详解

## 2.Django的ModelForm



## 3.注册逻辑

- 点击获取验证码
  - 获取手机号
  - 向后台发送ajax
    - 手机
    - tpl=register
  - 向手机发送验证码
  - 验证码失效处理120S

## 4.redis

### 4.1安装redis

- windows
- linux

**redis安装教程：[多端安装redis]([Installing Redis | Redis](https://redis.io/docs/getting-started/installation/))**

### 4.2python操作redis的模块

第一步：安装python操作redis模块

``` 
pip3 install redis
```

第二步：写代码操作redis

``` 
import redis

# 连接redis
conn = redis.Redis(host='',port=6379,passowrd='xxx',encoding='utf-8')

#设置键值：a=12 过期时间10秒
conn.set(a,12,ex=10)

#获取键值：如果存在返回值，不存在返回None
value = conn.get('a')
print(value)
```

使用redis-py实现redis连接池的主要步骤是:

1. 创建连接池ConnectionPool,指定redis服务器地址、端口、密码等参数,以及最大连接数max_connections。

```
python
import redis
pool = redis.ConnectionPool(
    host='localhost', 
    port=6379,
    password='foobared',
    max_connections=1000
)
```

2. 使用该连接池创建Redis实例:

```
python 
conn = redis.Redis(connection_pool=pool)
```

**django-redis** 模块

第一步：安装django-redis模块

```
pip3 install django-redis
```

第二部：配置

~~~
settings.py
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}:{}/{}".format(REDIS_HOST, REDIS_PORT, REDIS_DB),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
~~~



# day03

## 今日概要

## 详解

- 注册
- 短信验证码 
- 用户名密码登录

