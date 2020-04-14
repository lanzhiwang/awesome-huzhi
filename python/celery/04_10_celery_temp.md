# Celery-4.1 用户指南: Monitoring and Management Guide

翻译[libing_thinking](https://me.csdn.net/u013148156) 最后发布于2017-11-21 15:10:08 阅读数 3512 收藏

展开

## 简介

------

Celery 提供了监控和探查celery集群的工具。

这篇文档描述了一些工具，以及与监控相关的一些特性，例如事件和广播命令。

## 工作单元

------

### 命令行管理工具（inspect/control）

------

Celery 可以用来探查和管理工作单元节点（以及一定程度上对任务管理）。

列出所有可用的命令：

```
$ celery help1
```

或者对指定的命令获取帮助：

```
$ celery <command> --help1
```

#### 命令

------

- shell: 进入一个 Python shell
  本地环境将包含 `celery` 变量：这是当前的应用实例。另外，所有已知的任务会自动添加到本地环境中（除非 `--without-tasks` 标记被设置）。

celery 将按 `Ipython, bpython, 以及常规 python` 的顺序寻找交互式解释器。使用 `--ipython, --bpython, --python` 选项，你可以强制使用一中实现。

- status: 列出集群中的活动节点

```
$ celery -A proj status1
```

- result: 显示一个任务的结果

```
$ celery -A proj result -t tasks.add 4e196aa4-0141-4601-8138-7aa33db0f5771
```

注意只要任务没有使用一个自定义的存储后端，你可以忽略任务的名称。

- purge: 清除所有配置的任务队列的任务
  这个命令将清除在 `CELERY_QUEUES` 设置的队列中的所有消息

告警：
这个操作是无法取消的，消息将永久被删除！

```
$ celery -A proj purge1
```

你可以使用 `-Q` 选项声明要执行清除操作的队列：

```
$ celery -A proj purge -Q celery,foo,bar1
```

或者使用 `-X` 选项声明不会被清除的队列：

```
$ celery -A proj purge -X celery1
```

- inspect active: 列出活动任务

```
$ celery -A proj inspect active1
```

这是当前正在执行的所有任务。

- inspect scheduled: 列出被调度的ETA任务

这是当任务设置了 eta 或者 countdown 参数时工作单元预留的任务。

- inspect reserved: 列出预留的任务
  这是被工作单元获取并正在等待被执行的任务（不包含带有 ETA 设置的任务）。
- inspect revoked: 列出被取消的任务的历史

```
$ celery -A proj inspect revoked1
```

- inspect registered: 列出注册过的任务

```
$ celery -A proj inspect registered1
```

- inspect stats: 显示统计信息 (查看统计信息这一节)

```
$ celery -A proj inspect stats1
```

- inspect query_task: 根据任务 ID 显示任务信息

任何包含预留的或者正在执行的指定任务id的工作单元将回复任务状态和信息

```
$ celery -A proj inspect query_task e9f6c8f0-fec9-4ae8-a8c6-cf8c8451d4f81
```

你还可以一次询问多个任务：

```
$ celery -A proj inspect query_task id1 id2 ... idN1
```

- control enable_events: 启用事件

```
$ celery -A proj control enable_events1
```

- control disable_events: 禁用事件

```
$ celery -A proj control disable_events1
```

迁移：将任务从一个消息中间件迁移到另一个消息中间件（实验特性）

```
$ celery -A proj migrate redis://localhost amqp://localhost1
```

这个命令会将所有任务从一个消息中间件迁移到另一个消息中间件。因为这个命令是新的并且是实验性的，所以你在操作前确保数据有备份。

注意：
所有的 `inspect` 和 `control` 命令都支持 `--timeout` 参数，这表示等待回复的超时时间。如果由于延迟不能按时得到回复你可能需要增加超时时间。

#### 声明目的节点

------

默认情况下，`inspect` 和 `control` 命令将发送给所有工作单元。你可以通过 `--destination` 参数声明一个或者多个工作单元。

```
$ celery -A proj inspect -d w1@e.com,w2@e.com reserved

$ celery -A proj control -d w1@e.com,w2@e.com enable_events123
```

### Flower: Celery 实时web监控

------

Flower 是 celery 的一个基于 web 的实时监控和管理工具。它正在活跃的开发中，但是已经是一个必不可少的工具。作为 celery 推荐的监控工具，它废弃了 Django-Admin 监控、celerymon 以及基于 `ncurses` 的监控。

Flower 的发音就像 “flow”，但是如果你愿意你还可以使用植物版的flower。

#### 特性

------

- 使用 celery 事件实时监控
  - 任务进度和历史
  - 显示任务详细信息 (参数, 开始时间, 运行时间, 以及更多)
  - 图和统计信息
- 远程控制
  - 查看工作单元状态和统计信息
  - 关闭和重启工作单元实例
  - 控制工作单元池大小和自动扩展设置
  - 查看和修改工作单元获取消息的队列
  - 查看当前执行的任务
  - 查看被调度的任务(ETA/countdown)
  - 查看预留的任务和被取消的任务
  - 应用时间和速率限制
  - 配置查看器
  - 取消和中止任务
- HTTP API
  - 列出工作单元
  - 关闭工作单元
  - 重启工作单元池
  - 扩大工作单元池
  - 缩小工作单元池
  - 自动扩展工作单元池
  - 开始从一个队列消费
  - 停止从一个队列消费
  - 列出任务
  - 列出任务类型
  - 获取一个任务的信息
  - 执行一个任务
  - 根据名称执行一个任务
  - 获取任务结果
  - 获取一个任务的软时间限制和硬时间限制
  - 修改一个任务的速率
  - 取消一个任务
- OpenID 授权验证

屏幕截图
![这里写图片描述](http://docs.celeryproject.org/en/latest/_images/dashboard.png)
![这里写图片描述](http://docs.celeryproject.org/en/latest/_images/monitor.png)

#### 使用

------

你可以使用pip安装Flower:

```
$pip install flower1
```

运行flower命令会启动一个web服务器，你可以访问它：

```
$ celery -A proj flower1
```

默认的端口是 `http://localhost:5555`，但是你可以通过 `--port` 参数修改：

```
$ celery -A proj flower --port=55551
```

消息中间件可以通过 `--broker` 参数声明：

```
$ celery flower --broker=amqp://guest:guest@localhost:5672//
or
$ celery flower --broker=redis://guest:guest@localhost:6379/0123
```

此时，你可以在web浏览器中访问flower:

```
$ open http://localhost:55551
```

Flower 有比在这描述的更多的特性，包括授权认证选项。查看官方文档获取更多的信息。

### celery 事件：Curses 监控

------

2.0 版本新特性。

celery events 是一个显示任务和工作单元历史的字符界面监控。你可以查看任务的结果和跟踪信息，并且它还支持一些管理命令，如速率限制、关闭工作单元。这个监控是作为概念的验证开启的，并且你也许更想使用 flower。

启动：

```
$ celery -A proj events1
```

你应该可以看到类似如下的屏幕：
![这里写图片描述](http://docs.celeryproject.org/en/latest/_images/celeryevshotsm1.jpg)

celery events 还用来开启快照相机（查看 Snapshot 这一节）：

```
$ celery -A proj events --camera=<camera-class> --frequency=1.01
```

并且它还包含一个工具可以将事件dump到标准输出：

```
$ celery -A proj events --dump1
```

获取可用选项的完整列表，使用 `--help`:

```
$ celery events --help1
```

## RabbitMQ

------

要管理一个 Celery 集群，知道如果监控 RabbitMQ 非常重要。

RabbitMQ 带 `rabbitmqctl(1)` 命令，使用这个命令你可以列出队列、消息交换器、绑定、队列长度、每个队列使用的内存，以及管理用户、虚拟主机和他们的权限。

注意：
默认的虚拟主机（”/”）在这些示例中使用，如果你要使用一个定制化的虚拟主机，你应该添加 `-p`参数，例如： `rabbitmqctl list_queues -p my_vhost ...`

### Inspecting queues

------

查找队列中任务的数量：

```
$ rabbitmqctl list_queues name messages messages_ready \
                          messages_unacknowledged12
```

这里 `messages_ready` 是准备递送的消息的数量（已经发送但是还没有被接收），`messages_unacknowledged`是已经被工作单元接收但是还没有被确认的消息数量（意味它正在进行中，或者已经被预留）。`messages`是正在执行和没有确认消息总数。

查找从一个队列中消费消息的工作单元的数量：

```
$ rabbitmqctl list_queues name ，consumers1
```

查看为一个队列分配的总内存：

```
$ rabbitmqctl list_queues name memory1
```

提示：给 `rabbitmqctl` 命令添加 `-q` 选项使得输出更容易被解析。

## Redis

------

如果你使用 Redis 作为消息中间件，你可以使用 `redis-cli(1)` 命令监控 Celery 集群。

### Inspecting queues

------

查找队列中的任务数量：

```
$ redis-cli -h HOST -p PORT -n DATABASE_NUMBER llen QUEUE_NAME1
```

默认队列的名称是 celery。获取所有的可用队列，调用：

```
$ redis-cli -h HOST -p PORT -n DATABASE_NUMBER keys \*1
```

注意：
只有在队列中有任务时队列键才会存在，所以如果一个队列键不存在，这意味着这个队列中没有任何消息。这是因为在Redis中，如果一个列表中没有任何元素，这个列表将自动被删除，因此在命令行输出中不会有相应的键，并且这个列表的 `llen` 值返回 0。

另外，如果你还出于其他原因使用 Redis，`keys` 命令的输出将包含存储在数据库中的不相关的值。推荐的方式是为 Celery 指定一个专用的 `DATABASE_NUMBER`，你还可以使用数据库编号隔离不同的 celery 应用（虚拟主机），但是这不会影响到例如被Flower使用的监控事件，因为Redis pub/sub 命令是全局的而不是基于数据库的。

## Munin

------

下列是一些知名的能用来监控Celery集群的Munin插件：

- rabbitmq-munin: RabbitMQ 的 Munin 插件
  https://github.com/ask/rabbitmq-munin
- celery_tasks： 监控每种类型的任务被执行的次数（需要 celerymon）
  http://exchange.munin-monitoring.org/plugins/celery_tasks-2/details
- celery_task_states：监控在每个状态的任务的数量
  http://exchange.munin-monitoring.org/plugins/celery_tasks/details

## 事件

------

工作单元可以在一些事件发生时发送一个消息。这些事件之后被类似 Flower、celery events 的工具捕获到用来监控集群。

### 快照

------

2.1版本新特性。

即使是一个工作单元也能产生大量的事件，所以在硬盘上存储所有事件的历史是非常昂贵的。

快照是在一个时间段的一系列描述集群状态的事件，通过周期性的执行快照你可以保存所有的历史，但是只需要周期性的写到硬盘。

你需要一个照相机类来执行快照，在这个类中你可以定义每次状态被捕获时将发生什么；你可以将它写道一个数据库，通过邮件发送或者其他操作。

celery events 用来使用照相机进行快照，例如你想使用 `myapp.Camera` 照相机每2秒中获取一个状态快照，你可以使用如下参数运行 celery events：

```
$ celery -A proj events -c myapp.Camera --frequency=2.01
```

#### Custom Camera

------

如果你想捕获事件并且定时针对这些事件作一些操作，照相机将非常有用。对于实时事件处理，你可以直接使用 `app.events.Receiver`，就像实时处理这一节。

下面是一个照相机的示例，将快照dump到屏幕：

```
from pprint import pformat

from celery.events.snapshot import Polaroid

class DumpCam(Polaroid):
    clear_after = True  # clear after flush (incl, state.event_count).

    def on_shutter(self, state):
        if not state.event_count:
            # No new events since last snapshot.
            return
        print('Workers: {0}'.format(pformat(state.workers, indent=4)))
        print('Tasks: {0}'.format(pformat(state.tasks, indent=4)))
        print('Total: {0.event_count} events, {0.task_count} tasks'.format(
            state))123456789101112131415
```

查看 `celery.events.state` 的API获取更多关于状态对象的信息。

现在，你可以通过给 celery events 命令声明 `-c` 选项使用这个照相机：

```
$ celery -A proj events -c myapp.DumpCam --frequency=2.01
```

或者你可以在程序中如下使用：

```
from celery import Celery
from myapp import DumpCam

def main(app, freq=1.0):
    state = app.events.State()
    with app.connection() as connection:
        recv = app.events.Receiver(connection, handlers={'*': state.event})
        with DumpCam(state, freq=freq):
            recv.capture(limit=None, timeout=None)

if __name__ == '__main__':
    app = Celery(broker='amqp://guest@localhost//')
    main(app)12345678910111213
```

### 实时处理

------

实时处理事件，你需要：

- 一个事件消费者（这里是 `Receiver`）
- 当事件发生时将被调用的一个处理函数的集合
  对每个事件类型，你可以有不同的处理函数，后者捕获所有事件可以写成 `*`
- 状态（可选）
  `app.events.State` 是任务和工作单元内存中表示的一种方便的手段，它随着事件到来不断更新。

它为很多通用的东西包装了解决方案，如检查一个工作单元是否还活着（通过验证心跳），随着事件到来将事件字段合并，确保时间戳同步等等。

组合这些，你可以很容易实时处理事件：

```
from celery import Celery


def my_monitor(app):
    state = app.events.State()

    def announce_failed_tasks(event):
        state.event(event)
        # task name is sent only with -received event, and state
        # will keep track of this for us.
        task = state.tasks.get(event['uuid'])

        print('TASK FAILED: %s[%s] %s' % (
            task.name, task.uuid, task.info(),))

    with app.connection() as connection:
        recv = app.events.Receiver(connection, handlers={
                'task-failed': announce_failed_tasks,
                '*': state.event,
        })
        recv.capture(limit=None, timeout=None, wakeup=True)

if __name__ == '__main__':
    app = Celery(broker='amqp://guest@localhost//')
    my_monitor(app)12345678910111213141516171819202122232425
```

注意：
`capture`函数的`wakeup`参数使得强制让所有的工作单元发送一个心跳。当这个监控开始，你可以立马看到工作单元。

你可以通过声明处理函数来监听指定的事件：

```
from celery import Celery

def my_monitor(app):
    state = app.events.State()

    def announce_failed_tasks(event):
        state.event(event)
        # task name is sent only with -received event, and state
        # will keep track of this for us.
        task = state.tasks.get(event['uuid'])

        print('TASK FAILED: %s[%s] %s' % (
            task.name, task.uuid, task.info(),))

    with app.connection() as connection:
        recv = app.events.Receiver(connection, handlers={
                'task-failed': announce_failed_tasks,
        })
        recv.capture(limit=None, timeout=None, wakeup=True)

if __name__ == '__main__':
    app = Celery(broker='amqp://guest@localhost//')
    my_monitor(app)1234567891011121314151617181920212223
```

## Event Reference

------

这个列表包含工作单元发送的事件以及事件的参数

### 任务事件

------

#### task-sent

------

signature: task-sent(uuid, name, args, kwargs, retries, eta, expires, queue, exchange, routing_key, root_id, parent_id)
如果使能了 task_send_sent_event 设置，那么当有任务消息发布时发送该事件。

#### task-received

------

signature: task-received(uuid, name, args, kwargs, retries, eta, hostname, timestamp, root_id, parent_id)
当工作单元接收到一个任务时发送该事件。

#### task-started

------

signature: task-started(uuid, hostname, timestamp, pid)
工作单元将要执行任务之前

#### task-succeeded

------

signature: task-succeeded(uuid, result, runtime, hostname, timestamp)
任务执行成功

`Run-time` 是指使用池运行使用所花费的时间。（从任务发送到工作单元池，到池结果处理回调函数被调用）

#### task-failed

------

signature: task-failed(uuid, exception, traceback, hostname, timestamp)
任务执行失败时

#### task-rejected

------

signature: task-rejected(uuid, requeued)
任务被工作单元拒绝，可能被重新入队或者移除到死信队列

#### task-revoked

------

signature: task-revoked(uuid, terminated, signum, expired)
任务被取消时(注意这可能被多个工作单元发送).

如果任务进程被中止，将`terminated`设置为真，并且 `signum` 字段设置成使用的信号。如果任务过期， `expired`设置成真。

#### task-retried

------

signature: task-retried(uuid, exception, traceback, hostname, timestamp)
任务失败，但是将在将来重试

### 工作单元事件

------

#### worker-online

------

signature: worker-online(hostname, timestamp, freq, sw_ident, sw_ver, sw_sys)
工作单元已经连接到消息中间件，并且在线

hostname: 工作单元的节点名称
timestamp: 事件时间戳
freq: 心跳频率，以秒为单位 (float)
sw_ident: 工作单元软件名称 (例如, py-celery)
sw_ver: 软件版本 (例如, 2.2.0)
sw_sys: 操作系统 (例如, Linux/Darwin)

#### woker-heartbeat

------

signature: worker-heartbeat(hostname, timestamp, freq, sw_ident, sw_ver, sw_sys, active, processed)
每分钟发送一次，如果工作单元在两分钟内没有发送心跳，它将被认为离线。

hostname: 工作单元的节点名称
timestamp: 事件时间戳
freq: 心跳频率，以秒为单位 (float)
sw_ident: 工作单元软件名称 (例如, py-celery)
sw_ver: 软件版本 (例如, 2.2.0)
sw_sys: 操作系统 (例如, Linux/Darwin)
active: 当前执行的任务数量
processed: 被工作单元处理的总任务数量

#### woker-offline

------

signature: worker-offline(hostname, timestamp, freq, sw_ident, sw_ver, sw_sys)
工作单元与消息中间件断开连接。

- [点赞](javascript:;)
- [收藏](javascript:;)
- [分享](javascript:;)



[参考](https://blog.csdn.net/u013148156/article/details/78592801)

