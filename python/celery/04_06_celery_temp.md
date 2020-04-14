# Celery-4.1 用户指南: Workers Guide

## 启动工作单元

你可以通过执行以下命令在前台启动工作单元：

```bash
$ celery -A proj worker -l info
```

查看启动工作单元的可用命令行选项，可以执行：

```bash
$ celery worker --help
```

你可以在同一台机器上启动多个工作单元，只要确保给每个独立的工作单元使用 `--hostname` 参数声明一个节点名称。

```bash
$ celery -A proj worker --loglevel=INFO --concurrency=10 -n worker1@%h
$ celery -A proj worker --loglevel=INFO --concurrency=10 -n worker2@%h
$ celery -A proj worker --loglevel=INFO --concurrency=10 -n worker3@%h
```

`hostname` 参数可以使用以下变量扩展：

- %h: 主机名，包含域名
- %n: 主机名
- %d: 域名

如果单前主机名是 `george.example.com`，那么会扩展成：

| Variable | Template   | Result                     |
| -------- | ---------- | -------------------------- |
| %h       | worker1@%h | worker1@george.example.com |
| %n       | worker1@%n | worker1@george             |
| %d       | worker1@%d | worker1@example.com        |

注意对于 `supervisor` 用户：% 符号需要被转义： %%h

## 停止工作单元

停止可以通过使用 `TERM` 信号来实现。

当停止过程启动后，工作单元会在实际停止前完成当前所有的任务。如果任务很重要，你应该在做一些极端操作，例如发送 `KILL` 信号之前等待任务的完成。

如果工作单元在预期的时间里没有停止，进入了无限的循环或者类似的情景，那么你可以发送 `KILL` 信号强制关闭工作单元：但是你应该知道这样做会使当前正在执行的任务丢失（即，除非你的任务设置了 `acks_late` 选项）。

另外，进程不会覆盖 `KILL` 信号，所以工作单元进程不会干掉他的子进程；手动确保所有进程都终止了。以下命令通常能达到这个效果：

```bash
$ pkill -9 -f 'celery worker'
```

如果在你系统里没有 `pkill` 命令，你可以使用另外一个长些的命令版本：

```bash
$ ps auxww | grep 'celery worker' | awk '{print $2}' | xargs kill -9
```

## 重启工作单元

为了重启工作单元，你应该发送 `TERM` 信号，并且启动一个新的实例。在开发环境管理工作单元最简单的方式是使用 `celery multi`:

```bash
$ celery multi start 1 -A proj -l info -c4 --pidfile=/var/run/celery/%n.pid

$ celery multi restart 1 --pidfile=/var/run/celery/%n.pid
```

在生产环境中，你应该使用 `init-script` 或者一个进程管理系统（查看 `Daemonization` 这一节）。

除了停止工作单元，然后启动一个新的工作单元的方式重启外，你还可以使用 `HUP` 信号重启工作单元。注意工作单元将负责重启自己，所以容易产生问题，在生产环境还是不建议使用这种方式。

```bash
$ kill -HUP $pid
```

注意：

- 只有在工作单元在后台作为守护进程运行时发送 `HUP` 信号重启才有用（它没有控制终端）。
- 由于 macOS 平台的限制，`HUP` 信号在 macOS 中被禁用。

## 处理信号

工作单元主进程重写了如下信号处理方式：

| TERM | Warm shutdown, wait for tasks to complete. |
| ---- | ------------------------------------------ |
| QUIT | Cold shutdown, terminate ASAP              |
| USR1 | Dump traceback for all active threads.     |
| USR2 | Remote debug, see celery.contrib.rdb.      |

## 文件路径中的变量

文件路径参数 `--logfile, --pidfile, 以及 --statedb` 可以包含工作单元可以扩展的变量：

节点名称替换

- %p: 全节点名称
- %h: 主机名，包含域名
- %n: 主机名
- %d: 域名
- %i: `Prefork` 进程池的进程索引，如果是主进程索引为0
- %I: `Prefork` 带连接符的进程池索引

例如，如果当前的主机名是 `george@goo.example.com`，那么将会扩展成：

- `--logfile-%p.log -> george@goo.example.com.log`
- `--logfile=%h.log -> goo.example.com.log`
- `--logfile=%n.log -> george.log`
- `--logfile=%d -> example.com.log`

#### Prefork 进程池索引

`Prefork` 进程池声明符将根据最终需要打开的文件的进程扩展成不同的文件名称。

这可以用来给每个子进程声明一个日志文件。

注意数字将保持进程限制，即使进程已经退出或者使用了`autoscale/maxtasksperchild/time` 限制。也就是说，数字是进程索引而不是进程计数或者进程ID。

- %i - 进程池中进程索引，如果是主进程则为0
  `-n worker1@example.com -c2 -f %n-%i.log` 命令将生成三个日志文件：
  - worker1-0.log (main process)
  - worker1-1.log (pool process 1)
  - worker1-2.log (pool process 2)

- %I - 带连接符号的进程池索引
  `-n worker1@example.com -c2 -f %n%I.log` 命令将生成三个日志文件：
  - worker1.log (main process)
  - worker1-1.log (pool process 1)
  - worker1-2.log (pool process 2)

## 并行

默认情况下，多进程被用来处理并发执行的任务，但是你可以使用 `Eventlet`。工作单元的进程/线程数可以使用 `--concurrency` 参数修改，默认是机器上可用的 CPU 核数。

进程的数量（multiprocessing/prefork pool）:
进程数越多通常效果会更好，但是也存在一个分隔点，超过这个数目添加更多的进程反而会影响性能。有些证据证明同时启动多个工作单元实例，可能比只启动一个工作单元实例性能更佳。例如：3个工作单元，每个工作单元10个进程。你需要通过实验找到对你最佳的进程数，因为影响的因素很多：应用、工作负载、任务执行时间以及其他因素。

## 远程控制

2.0 版本新特性。

Celery 命令
`celery` 程序用来从命令行执行远程控制命令。它支持所有下面列出的命令。查看`Manageemnt Command-line Utilities(inspect/control)`获取更多的信息。

池： prefork, eventlet, gevent
支持： blocking: solo(查看注意)
消息中间件： amqp, redis
支持：

工作单元可以使用一个高优先级的广播消息队列来执行远程控制。控制命令将会发送给所有工作单元，或者声明的一个工作单元的列表。

命令也有回复。客户端可以等待并收集这些回复。因为没有一个中央集权机构知道在集群中有多少个工作单元，也没法估计有多少个工作单元会发送回复，所以客户端可以配置一个超时时间 - 回复到达的最后时间期限。这个超时时间默认是1秒钟。如果工作单元没有在超时时间之前回复，并不意味着工作单元没有回复，或者更糟糕的是终止了，而是可能由于网络延迟或者工作单元处理命令比较慢，所以对于超时事件要做相应的处理。

除了超时时间，客户端还可以声明一个等待的最大回复数。如果目标节点已经声明，则这个限制就设置为目标节点的数量。

注意：
`sole` 池支持远程控制命令，但是任何任务执行都会阻塞远程控制命令，所以如果工作单元非常忙它在使用上会受到限制。在这种情况下，你必须增加等待命令回复的超时时间。

### `broadcast()` 函数

------

这是一个客户端发送命令给工作单元的函数。一些远程控制命令还有高级别的接口，他们在后台使用 `broadcast()` 函数，就像 `rate_limit()` 和 `ping()`。

发送 `rate_limit` 命令还相应的参数：

```
>>> app.control.broadcast('rate_limit',
...                          arguments={'task_name': 'myapp.mytask',
...                                     'rate_limit': '200/m'})123
```

这将异步发送命令，而不会等待回复。如果需要回复，你可以使用 `reply` 参数：

```
>>> app.control.broadcast('rate_limit', {
...     'task_name': 'myapp.mytask', 'rate_limit': '200/m'}, reply=True)
[{'worker1.example.com': 'New rate limit set successfully'},
 {'worker2.example.com': 'New rate limit set successfully'},
 {'worker3.example.com': 'New rate limit set successfully'}]12345
```

通过使用`destination` 参数，你可以声明接收命令的工作单元的列表：

```
>>> app.control.broadcast('rate_limit', {
...     'task_name': 'myapp.mytask',
...     'rate_limit': '200/m'}, reply=True,
...                             destination=['worker1@example.com'])
[{'worker1.example.com': 'New rate limit set successfully'}]12345
```

当然，使用高级别的接口来设置速率限制要更加便利，但是有些命令只能使用 `broadcast()` 发送请求。

## 命令

------

`revoke: Revoking tasks`
pool support: all, terminate only supported by prefork
broker support: amqp, redis
command: celery -A proj control revoke

所有的工作单元都保存了被取消的任务iD，在内存中或者持久化在硬盘里（查看 Persistent revoke 这一节）

当一个工作单元接收到一个任务取消请求，他将会放弃执行这个任务，但是它不会终止正在执行的任务，除非设置了 `terminate` 选项。

注意：
`terminate` 选项是当任务动不了时对管理员最后的求助。它不是用于终止任务，而是用来终止执行任务的进程，并且当信号发送时这个进程可能已经开始处理另外一个任务，所以你永远不应该在程序中使用它。

如果设置了 `terminate` 选项，执行任务的工作单元子进程将被终止。默认发送的信号是 `TERM`，但是你可以通过 `signal` 参数显示声明要发送的信号。信号可以是任意在python标准库 `signal` 模块中定义的信号，信号名称字符为大写。

终止一个任务也会取消它。

示例：

```
>>> result.revoke()

>>> AsyncResult(id).revoke()

>>> app.control.revoke('d9078da5-9915-40a0-bfa1-392c7bde42ed')

>>> app.control.revoke('d9078da5-9915-40a0-bfa1-392c7bde42ed',
...                    terminate=True)

>>> app.control.revoke('d9078da5-9915-40a0-bfa1-392c7bde42ed',
...                    terminate=True, signal='SIGKILL')1234567891011
```

### 取消多个任务

------

3.1版本新特性。

任务取消方法还接收一个列表参数，使得可以同时取消多个任务。

示例：

```
>>> app.control.revoke([
...    '7993b0aa-1f0b-4780-9af0-c47c0858b3f2',
...    'f565793e-b041-4b2b-9ca4-dca22762a55d',
...    'd9d35e03-2997-42d0-a13e-64a66b88a618',
])12345
```

从3.1版本开始，`GroupResult.revoke` 方法开始采用这一特性。

### 任务取消持久化

------

取消任务将发送一个广播消息给所有的工作单元，工作单元将在内存中记录一个被取消的任务的列表。当一个工作单元启动，它将与集群中其他工作单元同步被取消的任务。

被取消的任务保存在内存中，所以如果所有的工作单元都重启，那么被取消的任务的列表也将会消失。如果你想在重启后保留这个列表，你需要通过 `--statedb` 参数给工作单元声明一个文件来保存这些。

```
$ celery -A proj worker -l info --statedb=/var/run/celery/worker.state1
```

或者你可以使用 `celery multi` 命令为每一个工作单元实例创建一个文件，使用 `%n` 格式来扩展当前节点名称。

```
celery multi start 2 -l info --statedb=/var/run/celery/%n.state1
```

查看路径中的变量这一节。

注意远程控制命令必须能执行任务取消。远程命令当前只被 RabbitMQ（amqp） 和 Redis 支持。

## 时间限制

------

2.0 版本新特性。

软限制，或者硬限制？
时间限制通过两个值设置，软限制和硬限制。软限制允许任务在被杀死之前捕获一个异常来清理环境，硬限制超时时间是不可捕获的，它将强制终止任务。

pool support: prefork/gevent

一个任务可能永远运行，如果你又很多任务等待不可能发生的事件，你将阻塞工作单元处理其他的任务。不让这种情况发生的最佳方法就是设置时间限制。

时间限制（`--time-limit`）是一个任务终止前可以运行的最大时间秒数。你可以设置一个软时间限制(–soft-time-limit)，它将在硬时间限制到达强制杀死它之前抛出一个异常给任务，使得任务可以捕获到并清理任务环境：

```
from myapp import app
from celery.exceptions import SoftTimeLimitExceeded

@app.task
def mytask():
    try:
        do_work()
    except SoftTimeLimitExceeded:
        clean_up_in_a_hurry()123456789
```

时间限制还可以通过 `task_time_limit/task_soft_time_limit` 配置进行设置。

注意：
时间限制目前在不支持 `SIGUSR1` 信号的平台上不可用。

### 在运行时修改时间限制

------

2.3版本新特性。

broker support: amqp, redis

有一个远程控制命令可以修改一个任务的软限制和硬限制 - `time_limit`。

下面示例修改任务 `tasks.crawl_the_web` 的软限制为 1 分钟，硬限制为 2 分钟：

```
>>> app.control.time_limit('tasks.crawl_the_web',
                           soft=60, hard=120, reply=True)
[{'worker1.example.com': {'ok': 'time limits set successfully'}}]123
```

时间限制修改之后开始执行的任务才会被影响到。

## 速率限制

------

以下示例修改 `myapp.mytask` 任务的速率限制为每分钟最多执行 200 个该类型的任务。

```
>>> app.control.rate_limit('myapp.mytask', '200/m')1
```

以上示例没有声明目标节点名称，所以这个修改请求将会影响集群中所有的工作单元实例。如果你只想影响指定的工作单元，你可以包含 `destination` 参数：

```
>>> app.control.rate_limit('myapp.mytask', '200/m',
...            destination=['celery@worker1.example.com'])12
```

告警：
这个命令不会影响到使能了 `worker_disable_rate_limits` 的工作单元。

## 每个孩子的最大任务数

------

2.0版本新特性。

pool support: prefork

使用这个选项你可以配置工作单元子进程在被一个新进程取代之前可以执行的最打任务数量。

如果你任务中有无法控制的内存泄露，例如使用了已经不再维护的C扩展，这将是很有用的一个特性。

这个选项可以通过工作单元的 `--max-tasks-per-child` 参数或者 `worker_max_tasks_per_child` 配置进行设置。

## 每个孩子的最大内存

------

4.0版本新特性。

pool support: prefork

使用这个选项，你可以设置工作单元子进程被替换之前可以使用的最大内存。

如果你任务中有无法控制的内存泄露，例如使用了已经不再维护的C扩展，这将是很有用的一个特性。

这个选项可以通过工作单元的 `--max-memory-per-child` 参数或者 `worker_max_memory_per_child` 配置进行设置。

## 自动扩展

------

2.2版本新特性。

pool support: prefork, gevent

自动扩展组件用来基于负载动态调整池的大小：
\- 当负载高时增加池中的进程数
\- 当负载低时去除多余的进程

它可以通过 `--autoscale` 选项启用，需要两个数值：池的进程的最大数量和最小数量：

```
--autoscale=AUTOSCALE
     Enable autoscaling by providing
     max_concurrency,min_concurrency.  Example:
       --autoscale=10,3 (always keep 3 processes, but grow to
      10 if necessary).12345
```

你可以通过继承 `Autoscaler` 类来定义自己的扩展策略。一些依据的指标包括任务负载或者可用内存等。你可以通过 `worker_autoscaler` 设置声明一个自定义的自动扩展器。

## 队列

------

一个工作单元可以从任意数量的队列中消费任务消息。默认情况下，它会从所有定义在 `task_queues` 配置种的队列中消费消息（如果没有设置，它将从默认队列 `celery` 中消费消息）。

你可以在工作单元启动时声明从哪些队列中消费消息，通过 `-Q` 选项可以声明一个队列的列表：

```
$ celery -A proj worker -l info -Q foo,bar,baz1
```

如果队列的名称已经在 `task_queues` 中声明，它将使用这个配置，但是如果没有在队列列表中声明，那么Celery 将自动为你产生一个新的队列（依赖于 `task_create_missing_queues` 选项）。

你还可以通过远程控制命令 `add_consumer` 以及 `cancel_consumer` 让工作单元在运行时开始或者停止从一个队列中消费消息。

### Queues: Adding consumers

------

`add_consumer` 远程控制命令通知一个或多个工作单元从一个队列中消费消息。这个操作是幂等的。

让集群中的所有工作单元开始从队列`foo`中消费消息，你可以如下操作：

```
$ celery -A proj control add_consumer foo
-> worker1.local: OK
    started consuming from u'foo'123
```

如果你想声明一个指定的工作单元节点，可以使用 `--destination` 参数：

```
$ celery -A proj control add_consumer foo -d celery@worker1.local1
```

同样的效果可以通过 `app.control.add_consumer()` 方法动态实现：

```
>>> app.control.add_consumer('foo', reply=True)
[{u'worker1.local': {u'ok': u"already consuming from u'foo'"}}]

>>> app.control.add_consumer('foo', reply=True,
...                          destination=['worker1@example.com'])
[{u'worker1.local': {u'ok': u"already consuming from u'foo'"}}]123456
```

但现在为止，我们只列举了使用自动队列的示例，如果你想更多的控制，你可以声明 `exchange`、`routing_key` 甚至更多的选项：

```
>>> app.control.add_consumer(
...     queue='baz',
...     exchange='ex',
...     exchange_type='topic',
...     routing_key='media.*',
...     options={
...         'queue_durable': False,
...         'exchange_durable': False,
...     },
...     reply=True,
...     destination=['w1@example.com', 'w2@example.com'])1234567891011
```

### Queues: Canceling consumers

------

你可以通过 `cancel_consumer` 命令终止从一个队列中消费消息。

强制集群中所有的工作单元停止从一个队列中消费消息，你可以使用 `celery control` 程序：

```
$ celery -A proj control cancel_consumer foo1
```

如果你想声明一个指定的工作单元节点，可以使用 `--destination` 参数：

```
$ celery -A proj control cancel_consumer foo -d celery@worker1.local1
```

同样的效果可以通过 `app.control.cancel_consumer()` 方法动态实现：

```
>>> app.control.cancel_consumer('foo', reply=True)
[{u'worker1.local': {u'ok': u"no longer consuming from u'foo'"}}]12
```

### Queues: List of active queues

------

你可以使用 `active_queues` 控制命令获取工作单元消费的队列的列表：

```
$ celery -A proj inspect active_queues
[...]12
```

就像所有其他远程控制命令一样，它也支持 `--destination` 参数，用来声明应该回复请求的工作单元节点。

```
$ celery -A proj inspect active_queues -d celery@worker1.local
[...]12
```

这也可以通过 `app.control.inspect.active_queues()` 方法动态实现：

```
>>> app.control.inspect().active_queues()
[...]

>>> app.control.inspect(['worker1.local']).active_queues()
[...]12345
```

## 探查工作单元

------

`app.control.inspect` 可以用来探查正在运行的工作单元。在内部它使用远程控制命令来实现。

你也可以使用`celery`命令来探查工作单元，并且它支持与 `app.control` 接口相同的命令。

```
>>> # Inspect all nodes.
>>> i = app.control.inspect()

>>> # Specify multiple nodes to inspect.
>>> i = app.control.inspect(['worker1.example.com',
                            'worker2.example.com'])

>>> # Specify a single node to inspect.
>>> i = app.control.inspect('worker1.example.com')123456789
```

### Dump of registered tasks

------

你可以使用 `registered()` 方法获取在工作单元中注册的任务：

```
>>> i.registered()
[{'worker1.example.com': ['tasks.add',
                          'tasks.sleeptask']}]123
```

### Dump of currently executing tasks

------

你可以通过 `active()` 方法获取激活任务的列表：

```
>>> i.active()
[{'worker1.example.com':
    [{'name': 'tasks.sleeptask',
      'id': '32666e9b-809c-41fa-8e93-5ae0c80afbbf',
      'args': '(8,)',
      'kwargs': '{}'}]}]123456
```

### Dump of scheduled(ETA) tasks

------

你可以通过 `scheduled()` 方法获取等待被调度的任务列表：

```
>>> i.scheduled()
[{'worker1.example.com':
    [{'eta': '2010-06-07 09:07:52', 'priority': 0,
      'request': {
        'name': 'tasks.sleeptask',
        'id': '1a7980ea-8b19-413e-91d2-0b74f3844c4d',
        'args': '[1]',
        'kwargs': '{}'}},
     {'eta': '2010-06-07 09:07:53', 'priority': 0,
      'request': {
        'name': 'tasks.sleeptask',
        'id': '49661b9a-aa22-4120-94b7-9ee8031d219d',
        'args': '[2]',
        'kwargs': '{}'}}]}]1234567891011121314
```

注意：
这些是带有 `ETA/countdown` 参数的任务，不是周期任务。

### Dump of reserved tasks

------

保留任务是已经被工作单元接收，但是还在等待被执行的任务。

你可以通过 `reserved()` 方法获取保留任务的列表：

```
>>> i.reserved()
[{'worker1.example.com':
    [{'name': 'tasks.sleeptask',
      'id': '32666e9b-809c-41fa-8e93-5ae0c80afbbf',
      'args': '(8,)',
      'kwargs': '{}'}]}]123456
```

### Statistics

------

远程控制命令 `inspect stats(或者 stats())` 将提供给你一个关于工作单元的有用的统计信息列表（或者可能对你无用）：

```
$ celery -A proj inspect stats1
```

输出将包含下列字段：
\- broker
消息中间件相关的信息。
\- connect_timeout
以秒为单位的建立一个新连接的超时时间

```
- heartbeat
当前心跳值（由客户端设置）

- hostname
远程消息中间件的节点名称

- insist
不再使用

- login_method
连接消息中间件的登录方法

- port
远程消息中间件的端口

- ssl
启用/禁用 SSL

- transport
使用的传输层

- transport_options
传输层选项

- uri_prefix
一些传输层需要hostname是URL的形式。
​```
redis+socket:///tmp/redis.sock
​```
这个例子中 URI-prefix 是 redis。

- userid
连接消息中间的用户 ID

- virtual_host
使用的虚拟主机
123456789101112131415161718192021222324252627282930313233343536
```

- clock
  工作单元的逻辑时钟值。这是一个正整数，每次你收到统计信息它的值会增加。
- pid
  工作单元实例的进程ID
- pool
  池相关的配置。
  - max-concurrency
    最大的进程/线程/green线程数量
  - max-tasks-per-child
    一个工作单元子线程/进程被回收前可以执行的最大任务数量
  - processes
    进程/线程id的列表
  - put-guarded-by-semaphore
    内部使用
  - timeouts
    时间限制的默认值
  - writes
    `prefork` 池的特殊配置，它显示当使用异步 I/O 时池中每个进程写操作的分布。
- prefetch_count
  任务消费者的当前 `prefetch` 计数。
- rusage
  系统使用统计信息。你系统平台的相关字段可能不同。

From getrusage(2):
\- stime
进程的内核态时间

```
- utime
进程的用户态时间

- maxrss
进程使用的最大内存值（kilobytes计数）

- idrss
数据使用的非共享内存总数（执行的kilobytes次ticks计数）

- isrss
栈空间的非共享内存总数（执行的kilobytes次ticks计数）

- ixrss
与其他进程共享的内存总数（执行的kilobytes次ticks计数）

- inblock
文件系统为进程读硬盘的次数

- oublock
文件系统为进程写硬盘的次数

- majflt
进行 I/O 操作时出现的页错误计数

- minflt
没进程 I/O 操作时出现的页错误计数

- msgrcv
接收到的 IPC 消息

- msgsnd
发送的 IPC 消息

- nvcsw
进程主动进行上下文切换的次数

- nivcsw
非进程主动进行的上下文切换的次数

- nsignals
收到的信号数

- nswap
进程被交换除内存的次数
1234567891011121314151617181920212223242526272829303132333435363738394041424344
```

- total
  自从工作单元开始，任务名称与接收的该类型的任务数量的映射。

## 附加命令

------

### Remote shutdown

------

以下命令将远程优雅地关闭工作单元：

```
>>> app.control.broadcast('shutdown') # shutdown all workers
>>> app.control.broadcast('shutdown', destination='worker1@example.com')12
```

### Ping

------

这个命令像或者的工作单元发送一个 Ping 请求。工作单元将回复一个 `Pong`，而不做其他事情。如果你没有声明一个自定义的超时时间，它就使用默认的1秒超时时间：

```
>>> app.control.ping(timeout=0.5)
[{'worker1.example.com': 'pong'},
 {'worker2.example.com': 'pong'},
 {'worker3.example.com': 'pong'}]1234
```

`ping()` 方法还支持 `destination` 参数，所以你可以声明想要 `ping` 的工作单元：

```
>>> ping(['worker2.example.com', 'worker3.example.com'])
[{'worker2.example.com': 'pong'},
 {'worker3.example.com': 'pong'}]123
```

### Enable/disable events

------

你可以使用 `enable_events, disable_events` 命令启用/禁用事件。这对于临时监控一个使用 `celery events/celerymon` 的工作单元非常有用。

```
>>> app.control.enable_events()
>>> app.control.disable_events()12
```

## 编写自己的远程控制命令

------

有两种类型的远程控制命令：

- Inspect command
  没有副作用，将只是返回工作单元中找到的值，如已注册的任务的列表、激活的任务的列表，等等。
- Control command
  有副作用，如给工作单元添加一个消费队列。

远程控制命令在控制面板中注册，并且他们有一个参数：当前的 `ControlDispatch` 实例。在这里，如果你需要，你可以访问激活的 `Consumer`。

下面是一个控制命令的例子，它增加任务的 `prefetch` 计数：

```
from celery.worker.control import control_command

@control_command(
    args=[('n', int)],
    signature='[N=1]',  # <- used for help on the command-line.
)
def increase_prefetch_count(state, n=1):
    state.consumer.qos.increment_eventually(n)
    return {'ok': 'prefetch count incremented'}123456789
```

确保你将这段代码添加到一个模块中，并且该模块被工作单元导入：这可以在你定义 app 实例的模块定义，或者你也可以使用 imports 设置从其他模块导入。

重启工作单元使控制命令注册其中，现在你可以使用 `celery control` 工具执行你的命令：

```
$ celery -A proj control increase_prefetch_count 31
```

你还可以给 `celery inspect` 程序添加操作，例如读取当前的 `prefetch` 计数：

```
from celery.worker.control import inspect_command

@inspect_command
def current_prefetch_count(state):
    return {'prefetch_count': state.consumer.qos.value}12345
```

重启工作单元之后你可以通过 `celery inspect` 程序询问这个值：

```
$ celery -A proj inspect current_prefetch_count1
```

- [点赞](javascript:;)
- [收藏](javascript:;)
- [分享](javascript:;)

[参考](https://blog.csdn.net/u013148156/article/details/78579160)
