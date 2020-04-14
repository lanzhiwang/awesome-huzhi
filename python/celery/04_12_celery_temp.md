# Celery-4.1 用户指南: Optimizing

翻译[libing_thinking](https://me.csdn.net/u013148156) 最后发布于2017-11-22 13:37:48 阅读数 2394 收藏

展开

## 简介

------

默认的配置做了很多折中考虑。它不是针对某个情况优化的，但是大多数情况下都工作的非常好。

基于一个特殊的使用场景，有很多优化可以做。

优化可以应用到运行环境的不同属性，可以是任务执行的时间，使用的总内存数，或者是高负载时的响应时间。

## Ensuring操作

------

在`Programming Pearl`这本书中，Jon Bentley 通过 `一天有多少水从密西西比河流出?` 这个问题提出了`back-of-the-envelope` 的概念。

这个练习的重点是要说明一个系统能及时处理的数据量有一个极限。`Back of the envelope` 计算能够被用来预先做这个计划。

在 Celery 中；如果一个任务需要10分钟完成处理，并且有10个任务每分钟进来一个，那么队列将永远不会空。这就是为什么监控队列长度非常重要的原因！

有一种方案是使用`Munin`。你应该设置告警，使得一旦任意队列达到不可接受的长度你会收到告警。此时，你可以采取合理的措施，添加新的工作节点或者取消不必要的任务。

## 通用设置

------

### librabbitmq

------

如果你使用 RabbitMQ(AMQP) 作为消息中间件，那么你可以安装 `librabbitmq` 模块这个 C 实现的优化过的客户端。

```
$ pip install librabbitmq1
```

如果 `librabbitmq` 模块已经安装，`amqp` 传输将自动使用它，或者你也可以直接指定你想要的传输模块，使用 `pyamqp://` 或者 `librabbitmq://`前缀。

### 消息中间件连接池

------

从2.5版本开始，消息中间件连接池被自动启用。

你可调整 `broker_pool_limit` 设置来减少竞争，并且这个值应该基于使用消息中间件的激活状态的`thread/green-thread`数量。

### 使用临时队列

------

Celery 创建的队列默认是持久化的。这意味着即使消息中间会将消息写到硬盘使得即使重启任务也会被执行。

但是，一些情况下，消息丢失也没关系，所以并非所有的任务都需要持久化。你可以为这类任务消息创建一个临时队列来提高性能：

```
from kombu import Exchange, Queue

task_queues = (
    Queue('celery', routing_key='celery'),
    Queue('transient', Exchange('transient', delivery_mode=1),
          routing_key='transient', durable=False),
)1234567
```

或者可以配置 `task_routes`:

```
task_routes = {
    'proj.tasks.add': {'queue': 'celery', 'delivery_mode': 'transient'}
}123
```

`delivery_mode` 修改发送到队列的消息的递送方式。`one` 值代表消息不会写到硬盘，而`two`值（默认）代表消息可被写到硬盘。

将你的任务导向新的临时队列，你可以通过声明`queue`参数（或者使用`task_routes设置`）：

```
task.apply_async(args, queue='transient')1
```

获取更多的信息，请查看 `routing guide`。

## 工作单元设置

------

### Prefetch 限制

------

`Prefetch` 是一个继承自 AMQP 的术语，它经常被用户错误理解。

`prefetch` 限制是一个工作单元可以预留的任务的数量。如果他为0，工作单元将继续消费消息，并不是说可能存储其他可用节点能更快的处理任务，或者消息可能不适合保留在内容中。

工作单元的默认 `prefetch` 值是`worker_prefetch_multiplier`值乘以并行的数量（进程/线程/green-threads）。

如果你有许多长时间运行的任务，你可能会想将乘数值设置为1：意思是每个工作单元进程每次只预留一个任务。

但是 - 如果你有许多短时间运行任务，并且吞吐量/往返延迟对你又很重要，这个值应该大。如果消息已经被预先获取，且在内存中可用，工作单元每秒可以处理更多的任务。你可以通过实验来找到针对你场景的最佳值。值 50 或者 150 可能在这些环境中有意义。

如果你既有长时间任务又有短时间任务，最佳的方式是使用两个单独配置的工作单元节点，并且根据运行时间路由任务到相应的队列（查看路由任务这一节）。

### 每次预留一个任务

------

任务消息只有在被确认之后才会从队列中删除，所以如果工作单元在确认任务消息之前崩溃了，任务消息会重新递送到另一个工作单元（或者等当前工作单元恢复后又发送到这）

当使用默认的早确认机制，`prefetch` 乘数设置为 1，意味着每个工作单元将为每个进程最多预留一个额外的任务消息：或者，换而言之，如果工作单元使用 `-c 10` 参数启动，工作单元任意时刻最多预留20个任务（10个未确认的正在执行的任务，10个未确认的预留的任务）。

通常用户问禁用 `prefetching of tasks` 是否可能，但是他们实际意思是一个工作单元只预留工作单元进程数量的任务（对`-c 10`来说，10个未确认的任务）

这是能实现的，但是必须启用延迟确认。使用这个选项而不是默认行为意味着已经开始的任务在由于电源失败或者工作单元实例被意外杀死而失败时会被重试，所以这也要求任务的幂等的。
（感觉这里延迟确认和早确认说反了）

另见：
`Should I use retry or acks_late?`

你可以通过如下配置使能这个行为：

```
task_acks_late = True
worker_prefetch_multiplier = 112
```

### Prefork 池的 prefetch 设置

------

`prefork`池会异步发送尽可能多的任务给工作进程，从效果上，这意味着进程在预先获取任务。

这可以提高性能，不过它也意味着任务可能阻塞在等待长时间任务运行完成：

```
-> send task T1 to process A
# A executes T1
-> send task T2 to process B
# B executes T2
<- T2 complete sent by process B

-> send task T3 to process A
# A still executing T1, T3 stuck in local buffer and won't start until
# T1 returns, and other queued tasks won't be sent to idle processes
<- T1 complete sent by process A
# A executes T31234567891011
```

只要管道缓冲可写，工作单元将发送任务给工作进程。管道缓冲的大小与操作系统相关：一些可能只有 64K 大小，但是在近期的一些Linux发行版中这个缓冲大小是1MB（只能在系统层面上修改）。

你可以通过使用 `-0fair` 工作单元选项禁用这个预获取行为：

```
$ celery -A proj worker -l info -Ofair1
```

使用这个选项，工作单元将只给当前可用的进程发送任务，禁用预获取行为：

```
-> send task T1 to process A
# A executes T1
-> send task T2 to process B
# B executes T2
<- T2 complete sent by process B

-> send T3 to process B
# B executes T3

<- T3 complete sent by process B
<- T1 complete sent by process A1234567891011
```

### Footnotes

------

[*] 可以免费读这里: The back of the envelope. 这本书很经典，建议阅读。
[†] RabbitMQ 以及其他消息中间件轮询的方式发送消息，所以这对于一个激活的系统没有作用。如果没有 `prefetch` 限制并且你想重启集群，节点启动之间可能会有延迟。如果有3个离线节点和一个在线节点，所有的消息都会被递送到这个在线节点。
[‡] 这是一个并行设置； `worker_concurrency`设置或者 celery 工作单元的`-c`选项。

- [点赞](javascript:;)
- [收藏](javascript:;)
- [分享](javascript:;)





https://blog.csdn.net/u013148156/article/details/78602736



