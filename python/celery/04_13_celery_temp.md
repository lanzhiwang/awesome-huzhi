# Celery-4.1 用户指南: Debugging

翻译[libing_thinking](https://me.csdn.net/u013148156) 最后发布于2017-11-22 17:19:07 阅读数 1358 收藏

展开

## 远程调试任务（pdb）

------

### 基础

------

`celery.contrib.rdb` 是 pdb 的一个扩展版本，它支持不通过终端访问就可以远程调试进程。

示例：

```
from celery import task
from celery.contrib import rdb

@task()
def add(x, y):
    result = x + y
    rdb.set_trace()  # <- set break-point
    return result12345678
```

`set_trace()` 函数在当前位置设置一个断点，并且创建一个网络套接字使得你可以 telnet 上去进行远程调试你的任务。

调试器可能被多个进程同时启动，但调试器不是使用一个固定端口而是从基端口开始寻找一个可用的端口（默认从6900端口开始）。基端口可以通过环境变量 `CELERY_RDB_PORT` 进行修改。

默认情况下，调试器只在本机可用，要让它可以从外面访问需要设置环境变量 `CELERY_RDB_HOST`。

当工作单元执行到你的断点，它将打出日下日志信息：

```
[INFO/MainProcess] Received task:
    tasks.add[d7261c71-4962-47e5-b342-2448bedd20e8]
[WARNING/PoolWorker-1] Remote Debugger:6900:
    Please telnet 127.0.0.1 6900.  Type `exit` in session to continue.
[2011-01-18 14:25:44,119: WARNING/PoolWorker-1] Remote Debugger:6900:
    Waiting for client...123456
```

如果你 telnet 到你声明的端口，你将进入一个 pdb shell:

```
$ telnet localhost 6900
Connected to localhost.
Escape character is '^]'.
> /opt/devel/demoapp/tasks.py(128)add()
-> return result
(Pdb)123456
```

键入 help 或者可用命令的列表，如果你以前没有使用过 pdb，你最好先看看python 调试文档。

为了说明问题，我们读取 `result` 变量的值，修改它并且继续执行任务：

```
(Pdb) result
4
(Pdb) result = 'hello from rdb'
(Pdb) continue
Connection closed by foreign host.12345
```

我们捣乱的结果可以从工作单元日志看到：

```
[2011-01-18 14:35:36,599: INFO/MainProcess] Task
    tasks.add[d7261c71-4962-47e5-b342-2448bedd20e8] succeeded
    in 61.481s: 'hello from rdb'123
```

### 提示

------

#### 启用断点信号

------

如果设置了 `CELERY_RDBSIG` 环境变量，当 `SIGUSR2` 信号发送时，工作单元将启动一个rdb实例。对工作单元主进程或者工作进程这都适用。

例如开启一个工作单元：

```
$ CELERY_RDBSIG=1 celery worker -l info1
```

你可以通过给任何工作单元进程发送 `USR2` 信号启动一个 rdb 会话：

```
$ kill -USR2 <pid>1
```

- [点赞](javascript:;)
- [收藏](javascript:;)
- [分享](javascript:;)



https://blog.csdn.net/u013148156/article/details/78603252