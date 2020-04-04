# Celery 浅析

Celery 是用 python 实现的一个分布式的任务处理系统，对于需要高可用异步处理的系统来说它是一个不错的选择。本来想实现一个分布式任务处理系统，当看到 celery 后感觉没有必要再自己写，需要的功能都已经实现，系统的各方面都考虑的比较周全，官方文档也很完善，而且社区活跃度也很高，据官网描述已经有一些公司在生产环境应用。本文对 Celery 的基础知识进行一个简单介绍。

## 主要组件

* broker 消息中间件，用来在客户端和任务执行单元之间传递消息

* worker 任务执行单元，从 broker 中获取任务消息，并执行异步任务

* backend 存储后端，保存任务中间状态及最终结果

broker 和 worker 必须配置，对于结果和任务当前状态不敏感的应用可不配置backend。

## 安装

```bash
pip install celery
```

## 示例

这里 broker 和 backend 均配置为 redis，且都在本机上运行。

### 单模块示例

* code

```python
#!/usr/bin/env python
# coding: utf-8

"""
tasks.py
"""

from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/1', backend='redis://localhost:6379/2')

@app.task
def fib(n):
    if n in [1, 2]:
        return 1
    elif n > 2:
        return fib(n-1) + fib(n-2)
    else:
        raise Exception('input n invalid')
```

* 运行

1. 启动任务执行单元

```bash
celery -A tasks -l info worker
```

2. 客户端发送任务

```python
from tasks import fib
res = fib.delay(10)
print(res.state)  # 获取任务执行状态
print(res.result)  # 获取任务执行结果
```

### 包示例

更加工程化的方式是用包进行包装。

* 包目录结构

```bash
mypro
    / __init__.py
    / tasks.py
    / celery.py
    / celeryconfig.py
```

* code

```python
#!/usr/bin/env python
# coding: utf-8

"""
celery.py
"""

from celery import Celery

app = Celery('mypro', include=['mypro.tasks'])
app.config_from_object('mypro.celeryconfig')
```

```python
#!/usr/bin/env python
# coding: utf-8

"""
tasks.py
"""

from mypro import app

@app.task
def fib(n):
    if n in [1,2]:
        return 1
    elif n>2:
        return fib(n-1) + fib(n-2)
    else:
        raise Exception('input n invalid')
```

```python
"""
celeryconfig.py
"""

broker_url = 'redis://127.0.0.1/1'
backend_result = 'redis://127.0.0.1/2'
```

* 运行

1. 启动任务执行单元

```bash
celery -A mypro -l info worker
```

2. 客户端发送任务

```python
from tasks import fib

res = fib.delay(10)
print(res.state)
print(res.result)
```

## WEB UI

安装

```bash
pip install flower
```

运行

```bash
celery flower --address 0.0.0.0 --port 9999 --broker=redis://localhost:6379/1
```

## 问题

* 相对路径导入问题

上述包示例在 python3 下可以正常运行，但在 python2 下会报不能导入 Celery 的错误，这是由于我们包中 celery.py 文件与我们安装的 celery 包名称冲突，导致先找到的是我们包中的 celery.py，此时可以在文件前面加上 `from __future__ import absolute_path`。而 python3 中默认就是绝对路径导入，所以没有这个问题。

* celery 实例名称

创建 celery 实例时，第一个参数是实例名称，主要作用是用来在自动生成任务名称时作为任务名称前缀，每个任务执行单元里都有一个任务名称与任务函数之间的映射表。客户端发送过来的消息中只描述任务名称，工作进程收到后根据映射表映射到具体函数。如果不给这个参数，默认会用当前模块名填充，所以当你的任务执行单元作为一个程序启动时，会填充 `__main__`，而在客户端模块引入任务模块时会填充为任务模块的名称，此时客户端调用时会出现任务未注册的错误。所以，我们一般直接将这个参数写成当前模块或包的名称。当然，如果你直接指定任务名称时可以忽略这些。

[参考](https://blog.csdn.net/u013148156/article/details/78528685)
