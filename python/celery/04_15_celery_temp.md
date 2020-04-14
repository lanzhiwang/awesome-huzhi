# Celery-4.1 用户指南: Signals

翻译[libing_thinking](https://me.csdn.net/u013148156) 最后发布于2017-11-23 18:10:13 阅读数 1962 收藏

展开

## 基础

------

有多种类型的事件可以触发信号，你可以连接到这些信号，使得在他们触发的时候执行操作。

连接到 `after_task_publish` 信号的示例：

```
from celery.signals import after_task_publish

@after_task_publish.connect
def task_sent_handler(sender=None, headers=None, body=None, **kwargs):
    # information about task are located in headers for task messages
    # using the task protocol version 2.
    info = headers if 'task' in headers else body
    print('after_task_publish for task id {info[id]}'.format(
        info=info,
    ))12345678910
```

一些信号还带有发送者，你可以用来过滤信号。例如，`after_task_publish`信号使用任务名称作为发送者，所以通过给connect 方法提供 sender 参数，你可以使你的处理函数在每个名为 `proj.tasks.add`的任务发布的时候被回调：

```
@after_task_publish.connect(sender='proj.tasks.add')
def task_sent_handler(sender=None, headers=None, body=None, **kwargs):
    # information about task are located in headers for task messages
    # using the task protocol version 2.
    info = headers if 'task' in headers else body
    print('after_task_publish for task id {info[id]}'.format(
        info=info,
    ))12345678
```

信号的实现同 `django.core.dispatch`。所以默认情况下其他关键字参数（例如： signal）都被传递给所有信号处理函数。

信号处理的最佳实践是接收任意关键字参数（即：**kwargs）。这样的话当使用新的Celery 版本时只要添加新的参数而不需要更改你的代码。

## 信号

------

### 任务信号

------

- **before_task_publish**
  3.1版本新特性。

任务被发布之前分发的。注意它是在发送任务的进程中执行。
发送者是被发送的任务的名称。

提供的参数:

```
- body

任务消息体

这是一个包含任务消息字段的映射，查看 Version2 和 Version1 获取可以定义的可用字段的说明

- exchange

消息交换器的名称或者对象实例

- routing_key

发送消息时使用的路由键

- headers

应用头映射 (可以修改)

- properties

消息属性 (可以修改)

- declare

消息发布前声明的实体（消息交换器、队列或者绑定，可以修改）

- retry_policy

重试选项映射。可以是 `kombu.Connection.ensure()` 方法的任意参数，可以修改
1234567891011121314151617181920212223242526272829
```

- **after_task_publish**
  任务被分发到消息中间件之后。注意这是在发送任务的进程中执行。

提供的参数:

```
- headers
1
```

任务消息头，查看 Version2 和 Version1 获取可以定义的可用字段的说明

```
- body
1
```

任务消息体，查看 Version2 和 Version1 获取可以定义的可用字段的说明

```
- exchange

消息交换器名称或者消息交换器对象实例

- routing_key

使用的路由键
1234567
```

- **task_prerun**

任务执行前

发送者是将要执行的任务

提供的参数:

```
- task_id

被执行的任务的ID

- task

被执行的任务

- args

任务位置参数

- kwargs

任务关键字参数
123456789101112131415
```

- **task_postrun**

任务执行后分发

发送者是被执行的任务对象

提供的参数:

```
- task_id

被执行的任务的ID

- task

被执行的任务

- args

任务位置参数

- kwargs

任务关键字参数

- retval

任务的返回值

- state

结果状态的名称
1234567891011121314151617181920212223
```

- **task_retry**

当任务将被重试时分发

发送者是任务对象

提供的参数:

```
- request

当前任务请求

- reason

重试的理由 (通常是一个异常实例，但总是能表示成字符串)

- einfo

详细的异常信息，包括堆栈回溯信息（一个`billiard.einfo.ExceptionInfo` 对象）
1234567891011
```

- **task_success**

任务执行成功时分发

发送者是被执行的任务对象

提供的参数：

```
- result
任务的返回值
12
```

- **task_failure**

任务失败时分发

发送者是被执行的任务对象

提供的参数:

```
- task_id

任务的ID

- 异常

抛出的异常实例

- args

任务调用时传递的位置参数

- kwargs

任务调用时传递的关键字参数

- traceback

堆栈回溯对象

- einfo

`billiard.einfo.ExceptionInfo` 实例对象
1234567891011121314151617181920212223
```

- **task_revoked**

任务被工作单元取消或者中止时分发

提供的参数:

```
- request

这是一个 `Request` 实例，而不是 `task.request` 实例。当使用 prefork 池，这个信号由父进程分发，所以 `task.request` 是不可用的，也不应该使用。取而代之，我们可以使用这个对象，因为他们有很多相同的字段。

- terminated

如果任务被中止，设置为真

- signum

用来中止任务的信号数值。如果它的值为 None，且设置了 terminated 为真，那么它的值将设置成 TERM。

- expired

如果任务过期，设置成真
123456789101112131415
```

- **task_unknown**

当工作单元收到未注册的任务的消息

发送者是工作单元消费者

提供的参数:

```
- name

任务的名称

- id

消息中任务的id

- message

裸消息对象

- exc

发生的错误
123456789101112131415
```

- **task_rejected**

当工作单元从任务队列中收到未知类型的消息

发送者是工作单元消息者

提供的参数:

```
- message

裸消息对象

- exc

发生的错误（如果有）
1234567
```

## 应用信号

------

- **import_modules**

当程序（工作单元、beat、shell）导入 Include 中的模块，或者导入配置被导入时。

发送者是应用实例。

## 工作单元信号

------

- **celery_after_setup**
  工作单元启动但是在执行任务之前发送的信号。者意味着任意从 `celery worker -Q` 声明的队列都已经启用，日志环境已经设置好，等等。

它可以用来添加除 `celery worker -Q` 选项声明的队列之外的自定义队列，这些自定义队列应该始终被消费。下面是给每个工作单元创建一个直接队列的示例，这些队列可以用来路由任务给指定的工作单元：

```
from celery.signals import celeryd_after_setup

@celeryd_after_setup.connect
def setup_direct_queue(sender, instance, **kwargs):
    queue_name = '{0}.dq'.format(sender)  # sender is the nodename of the worker
    instance.app.amqp.queues.select_add(queue_name)123456
```

提供的参数：

- sender
  工作单元的节点名称
- instance
  这是要初始化的 `celery.apps.worker.Worker` 实例。注意，至今为止，只设置了 `app` 和 `hostname` 属性，并且 `__init__` 函数的余下部分还没有执行。
- conf
  当前应用实例的配置。
- **celeryd_init**

这是工作单元启动后发送的第一个信号。`sender`是工作单元的主机名，所以这个信号可以用来设置工作单元的特殊配置：

```
from celery.signals import celeryd_init

@celeryd_init.connect(sender='worker12@example.com')
def configure_worker12(conf=None, **kwargs):
    conf.task_default_rate_limit = '10/m'12345
```

或者如果你想给多个工作单元设置配置，你连接该信号的时候可以忽略 `sender` 参数：

```
from celery.signals import celeryd_init

@celeryd_init.connect
def configure_workers(sender=None, conf=None, **kwargs):
    if sender in ('worker1@example.com', 'worker2@example.com'):
        conf.task_default_rate_limit = '10/m'
    if sender == 'worker3@example.com':
        conf.worker_prefetch_multiplier = 012345678
```

提供的参数：
\- sender
工作单元的节点名称
\- instance
这是要初始化的 `celery.apps.worker.Worker` 实例。注意，至今为止，只设置了 `app` 和 `hostname` 属性，并且 `__init__` 函数的余下部分还没有执行。
\- conf
当前应用实例的配置。
\- options
从命令行传递给工作单元的选项

- **worker_init**
  任务开始前分发
- **worker_ready**
  工作单元准备接收任务时分发
- **worker_init**
  Celery 发送一个工作单元心跳时分发
  `sender` 是 `celery.worker.heartbeat.Heart` 实例
- **worker_shutting_down**
  工作单元准备关闭进程时分发

提供的参数：
\- sig
接收到的POSIX信号
\- how
关闭方法，热关闭或者冷关闭
\- exitcode
主进程退出时将使用的退出码

- **worker_process_init**
  在所有池进程开始时分发

注意这个信号绑定的处理函数不能阻塞多余4秒，否则进程会被认为开始失败而被杀死

- **worker_process_shutdown**
  在所有池进程将退出前分发

注意：不能保证这个信号一定能分发，类似于`finally` 块，不能保证处理函数会在关闭时进行调用，并且如果被调用也有可能中断。

提供的参数：
\- pid
将要关闭的子进程的进程ID
\- exitcode
子进程关闭时将使用的退出码

- **worker_shutdown**
  工作单元将要关闭前分发

## Beat 信号

------

- **beat_init**
  `celery beat`启动时分发 ( standalone 或者 embedded)

```
Sender` 是 `celery.beat.Service instance
```

- **beat_embedded_init**
  当celery beat 作为一个嵌入式进程启动时除发送 `beat_init`信号外还将发送的信号

```
Sender` 是 `celery.beat.Service instance
```

## Eventlet 信号

------

- **eventlet_pool_started**
  当 `eventlet pool` 启动时分发

`Sender` 是 `celery.concurrency.eventlet.TaskPool`实例

- **eventlet_pool_preshutdown**
  当工作单元关闭，`eventlet`池等待剩余工作进程时发送

`Sender` 是 `celery.concurrency.eventlet.TaskPool`实例

- **eventlet_pool_postshutdown**
  当池已经被`join`，并且工作单元将关闭时分发

`Sender` 是 `celery.concurrency.eventlet.TaskPool` 实例

- **eventlet_pool_apply**
  当任务应用到池时分发

`Sender` 是 `celery.concurrency.eventlet.TaskPool` 实例

提供的参数:

```
- target

目标函数

- args

位置参数

- kwargs

关键字参数
1234567891011
```

## 日志信号

------

- **setup_logging**
  如果这个信号被连接，celery不会配置日志器，所以你可以使用你自己的日志配置完全覆盖原来配置。

如果你想修改celery设置的配置，你可以使用 `after_setup_logger` 和 `after_setup_task_logger signals` 信号

提供的参数:

```
- loglevel

日志对象的级别

- logfile
日志文件的名称

- format

日志格式字符串

- colorize

声明日志消息是否标颜色
1234567891011121314
```

- **after_setup_logger**
  每个全局日志器设置后分发（不是任务日志器）。用来修改日志配置。

提供的参数:

```
- logger

日志器对象

- loglevel

日志对象的级别

- logfile

日志文件名称

- format

日志格式字符串

- colorize

声明日志是否标颜色
12345678910111213141516171819
```

- **after_setup_task_logger**
  每个任务日志器设置后分发。用来修改日志配置

提供的参数:

```
- logger

日志器对象

- loglevel

日志对象的级别

- logfile

日志文件名称

- format

日志格式字符串

- colorize

声明日志是否标颜色
12345678910111213141516171819
```

## 命令信号

------

- **user_preload_options**
  Celery 命令行程序完成解析预处理选项时该信号将被分发。

它可以用来给 celery 命令添加附加的命令行参数：

```
from celery import Celery
from celery import signals
from celery.bin.base import Option

app = Celery()
app.user_options['preload'].add(Option(
    '--monitoring', action='store_true',
    help='Enable our external monitoring utility, blahblah',
))

@signals.user_preload_options.connect
def handle_preload_options(options, **kwargs):
    if options['monitoring']:
        enable_monitoring()1234567891011121314
```

`Sender` 是`Command`实例，并且值依赖于调用的程序（例如： 对于总命令，他将是一个 `CeleryCommand` 对象）

提供的参数：
\- app
应用实例
\- options
被解析的预加载选项的映射（以及默认值）

## 废弃的信号

------

- **task_sent**
  这个信号已经被废弃，请使用 `after_task_publish`





https://blog.csdn.net/u013148156/article/details/78606458





