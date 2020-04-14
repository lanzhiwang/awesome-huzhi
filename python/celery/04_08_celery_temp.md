# Celery-4.1 用户指南: Routing Tasks

翻译[libing_thinking](https://me.csdn.net/u013148156) 最后发布于2017-11-20 22:49:17 阅读数 2665 收藏

展开

注意：
像主题和扇出之类的路由概念并不对所有传输介质都可用，请翻阅”传输比较表”。

## 基础

------

### 自动路由

------

路由最简单的方式是使用 `task_create_missing_queues` 设置（默认启用）。

使用这个设置，一个还没有在 `task_queues` 中定义的有名队列将会自动被创建。这使得进行简单的路由任务非常容易。

假如你有两台服务器，x 和 y 处理常规任务，还有一台服务器 z，只处理`feed`消息源相关的任务。你可以使用这个配置：

```
task_routes = {'feed.tasks.import_feed': {'queue': 'feeds'}}1
```

使用这个路由使得导入消息源任务被路由到`feeds`队列，而所有其他任务都将路由到默认队列(由于历史原因默认队列名为 `celery`)。

或者，你可以使用`glob`模式匹配，甚至可以用正则表达式，来匹配`feed.tasks`命名空间里的所有任务：

```
app.conf.task_routes = {'feed.tasks.*': {'queue': 'feeds'}}1
```

如果匹配模式的顺序很重要，你应该以项列表的格式声明路由：

```
task_routes = ([
    ('feed.tasks.*', {'queue': 'feeds'}),
    ('web.tasks.*', {'queue': 'web'}),
    (re.compile(r'(video|image)\.tasks\..*'), {'queue': 'media'}),
],)12345
```

注意：
`task_routes` 设置可以是一个字典，或者一个路由对象的列表，所以在上述情况下，你需要以一个包含列表的元组的方式声明 `task_routes`。

安装好路由器后，你可以启动服务器 z 用来专门处理 `feeds` 消息源队列：

```
user@z:/$ celery -A proj worker -Q feeds1
```

你可以声明你需要的多个队列，所以你也可以让你的服务器处理默认队列的消息：

```
user@z:/$ celery -A proj worker -Q feeds,celery1
```

#### 修改默认队列的名称

你可以使用下列配置修改默认队列的名称：

```
app.conf.task_default_queue = 'default'1
```

#### 队列是如何被定义的

这个特性的重点在于为只有基本需求的用户隐藏了复杂的 `AMQP` 协议。但是 - 你可能对队列是如何声明的仍然感兴趣。

一个名为 `video` 的队列将使用下列配置创建：
`{'exchange': 'video','exchange_type': 'direct','routing_key': 'video'}`

非 `AMQP` 后端如 Redis 或者 SQS 不支持消息交换器，所以他们需要消息交换器与队列同名。使用这种设计使得它可以在不会吃消息交换器的后端也能正常工作。

### 手动路由

假如你又两台服务器 x 和 y 处理常规任务，另外一台服务器 z，用来专门处理消息源相关的任务，你可以使用如下配置：

```
from kombu import Queue

app.conf.task_default_queue = 'default'
app.conf.task_queues = (
    Queue('default',    routing_key='task.#'),
    Queue('feed_tasks', routing_key='feed.#'),
)
task_default_exchange = 'tasks'
task_default_exchange_type = 'topic'
task_default_routing_key = 'task.default'12345678910
```

`task_queue` 是一个队列实例的列表。如果你没有为一个 key 设置消息交换器或者交换器类型，这些信息将从 `task_default_exchange` 和 `task_default_exchange_type` 配置中获取。

路由一个任务到 `feed_tasks` 队列，你可以在 `task_routes` 配置种添加一个项：

```
task_routes = {
        'feeds.tasks.import_feed': {
            'queue': 'feed_tasks',
            'routing_key': 'feed.import',
        },
}123456
```

你可以使用`Task.apply_async()`方法或者 `send_task()` 方法的 `routing_key` 参数覆盖这个路由行为：

```
>>> from feeds.tasks import import_feed
>>> import_feed.apply_async(args=['http://cnn.com/rss'],
...                         queue='feed_tasks',
...                         routing_key='feed.import')1234
```

使服务器 z 只从 `feed_tasks` 队列获取消息，你可以启动工作单元时使用 `-Q` 选项：

```
user@z:/$ celery -A proj worker -Q feed_tasks --hostname=z@%h1
```

服务器 x 和 y 必须配置成从`default`队列获取消息：

```
user@x:/$ celery -A proj worker -Q default --hostname=x@%h
user@y:/$ celery -A proj worker -Q default --hostname=y@%h12
```

如果你愿意，你甚至可以让的消息源处理工作单元也处理常规任务，也许在有许多常规任务的时候：

```
user@z:/$ celery -A proj worker -Q feed_tasks,default --hostname=z@%h1
```

如果你想添加在另外一个消息交换器上一个队列，只要声明自定义消息交换器及它的类型即可。

```
from kombu import Exchange, Queue

app.conf.task_queues = (
    Queue('feed_tasks',    routing_key='feed.#'),
    Queue('regular_tasks', routing_key='task.#'),
    Queue('image_tasks',   exchange=Exchange('mediatasks', type='direct'),
                           routing_key='image.compress'),
)12345678
```

如果你对这些术语有不清楚的地方，你应该去看看 `AMQP`。

另见：
处理下面的 `AMQP Primer`，还有 `Rabbits and Warrens` 这个讲述队列和消息交换的优秀的博客。另外，还有一个 `CloudAMQP tutorial`，对于 `RabbitMQ` 用户来说， `RabbitMQ FAQ` 将是非常有用的。

## 特殊的路由选项

------

### RabbitMQ 消息优先级

------

supported transports:
RabbitMQ

4.0版本新特性。

队列可以通过设置 `x-max-priority` 参数支持优先级：

```
from kombu import Exchange, Queue

app.conf.task_queues = [
    Queue('tasks', Exchange('tasks'), routing_key='tasks',
          queue_arguments={'x-max-priority': 10},
]123456
```

所有队列的优先级默认值使用 `task_queue_max_priority` 设置：

```
app.conf.task_queue_max_priority = 101
```

## AMQP Primer

------

### 消息

------

消息包含消息头和消息体。Celery 使用消息头存储消息的内容类型和内容编码。内容类型通常是消息使用的序列化格式。消息体包含要执行的任务的名称，任务的id(UUID)，任务函数的参数以及一个附加的元信息 - 如重试次数或者 ETA。

下面是一个使用 python 字典表示的任务消息的示例：

```
{'task': 'myapp.tasks.add',
 'id': '54086c5e-6193-4575-8308-dbab76798756',
 'args': [4, 4],
 'kwargs': {}}1234
```

### 生产者，消费者，消息中间件

------

发送消息的客户端通常被称为发布者，或者生产者，而接收消息的实体被称为消费者。

消息中间件是一个消息服务器，它将消息从生产者路由到消费者。

下面这些术语在 `AMQP` 相关的文档里经常能看到。

### Exchanges, 队列, 路由键

------

1. 消息是发送给消息交换器
2. 消息交换器将消息路由到一个或者多个队列。有几种不同的消息交换器类型，他们提供不同的路由方式，或者实现不同的消息场景
3. 消息在队列中等待指导有人消费它
4. 当消息被确认它将从队列中删除

收发消息的必要步骤包括：
\1. 创建一个消息交换器
\2. 创建一个队列
\3. 将队列绑定到消息交换器

Celery 自动创建 `task_queues` 中定义的队列所需要的实体（除非队列的 `auto_declare` 设置为 `False`）。

下面是队列配置示例包含三个队列；Video 处理一个，images 处理一个，以及其他处理的 default 队列：

```
from kombu import Exchange, Queue

app.conf.task_queues = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('videos',  Exchange('media'),   routing_key='media.video'),
    Queue('images',  Exchange('media'),   routing_key='media.image'),
)
app.conf.task_default_queue = 'default'
app.conf.task_default_exchange_type = 'direct'
app.conf.task_default_routing_key = 'default'12345678910
```

### Exchange 类型

------

消息交换器类型定义了消息怎样通过消息交换器路由。标准的消息交换器类型有 `direct,topic,fanout以及headers`。另外，非标准的消息交换器类型可以通过 `RabbitMQ` 插件的方式使用，例如 Michael Bridgen 写的 `last-value-cache plugin`。

#### Direct exchanges

------

直接消息交换类型通过精确的路由键匹配实现路由，所以一个被路由键 `video` 绑定的队列只能收到这个带这个路由键的消息。

#### Topic exchanges

------

主题消息交换类型使用 . 分隔单词，`wild-card` 字符 *（匹配整个词），字符#（匹配零个或多个词） 的方式匹配路由键。

对于类似 `usa.news, usa.weather, norway.news, 以及 norway.weather` 的路由键，绑定可以是 `*.news`(all news)，usa.# (all items in the USA)，or usa.weather (all USA weather items)

### 相关 API 命令

------

- exchange.declare(exchange_name, type, passive,
  durable, auto_delete, internal)

使用名称声明一个消息交换器。

查看 amqp:Channel.exchange_声明。

关键字参数:

passive – 被动意味着消息交换器不会被自动创建，你可以使用它来检测消息交换器是否存在。
durable – Durable 消息交换器是持久的 (即, 消息中间件重启他们还存在)。
auto_delete – 这意味着如果没有队列使用它，消息中间件将会自动删除它。

- queue.declare(queue_name, passive, durable, exclusive, auto_delete)
  使用名称声明一个队列。

查看 amqp:Channel.queue_声明。

专用队列只能在当前连接中被消费。专用也意味着 `auto_delete`。

- queue.bind(queue_name, exchange_name, routing_key)
  使用路由键将一个队列绑定到一个消息交换器。

未绑定的队列不会收到消息，所以这是必须的。

查看 amqp:Channel.queue_bind。

- queue.delete(name, if_unused=False, if_empty=False)
  Deletes a queue and its binding.

查看 amqp:Channel.queue_delete

exchange.delete(name, if_unused=False)
Deletes an exchange.

查看 amqp:Channel.exchange_delete

注意：
声明并不意味着“创建”。当你声明，你只是断言这个实体存在并且是可操作的。没有规定说谁应该创建 `exchange/queue/binding`,不论是消费者或者生产者。通常谁先需要它谁就创建它。

### API 动手实践

------

Celery 有一个工具 `celery amqp` 用来从命令行访问 `AMQP` API，使得可以访问管理员的任务如创建/删除队列以及消息交换器，删除队列消息或者发送消息。对于非 `AMQP` 消息中间件它也可以使用，但是不同的实现可能没有实现所有的命令。

你可以直接在 `celery amqp` 的命令行参数中编写命令，或者不带任何参数启动进入到交互模式：

```
$ celery -A proj amqp
-> connecting to amqp://guest@localhost:5672/.
-> connected.
1>1234
```

这里 1> 是一个提示符。数字 1 表示你当前已经执行的命令。键入 help 获取可用命令的列表，它还支持自动补全，所以你可以开始键入命令，然后按tab键显示可用的匹配。

下面创建一个队列，你可以发送消息给它：

```repl
$ celery -A proj amqp
1> exchange.declare testexchange direct
ok.
2> queue.declare testqueue
ok. queue:testqueue messages:0 consumers:0.
3> queue.bind testqueue testexchange testkey
ok.1234567
```

这里创建了一个直接类型的消息交互器 `testexchange`，以及一个名为 `testqueue` 的队列。这个队列使用路由键 `testkey` 绑定到消息交换器。

从此以后，所有带路由键 `testkey`发送到消息交换器 `testexchange` 的消息都将递送到这个队列。你可以使用 `basic.publish` 命令发送一个消息：

```repl
4> basic.publish 'This is a message!' testexchange testkey
ok.12
```

现在消息已经发送，你可以获取它。你可以使用 `basic.get` 命令，它将以异步的方式从队列中获取消息（对于维护任务这是可行的，但是对于服务，你应该使用 `basic.consume`）。

从队列中取出一个消息：

```
5> basic.get testqueue
{'body': 'This is a message!',
 'delivery_info': {'delivery_tag': 1,
                   'exchange': u'testexchange',
                   'message_count': 0,
                   'redelivered': False,
                   'routing_key': u'testkey'},
 'properties': {}}12345678
```

`AMQP` 使用确认机制来表示一个消息已经收到并且被成功处理。如果消息没有被确认并且消费者通道关闭，那么消息将重新递送到另一个消费者。

注意上述结构中的 `delivery_tag`， 在一个连接通道中，每个接收到的消息都有唯一的一个 `delivery_tag`，这个标记是用来确认消息的。另外，注意 `delivery_tag` 在不同连接通道中不是唯一的，所以在另一个客户端，递送标记 1 可能指向不同于这个通道的另一个消息。

你可以使用 `basic.ack` 确认你收到的消息：

```repl
6> basic.ack 1
ok.12
```

清理我们测试会话的环境，你应该删除掉你创建的实体：

```repl
7> queue.delete testqueue
ok. 0 messages deleted.
8> exchange.delete testexchange
ok.1234
```

## 路由任务

------

### 定义队列

------

在 Celery 中，可用的队列是通过 `task_queue` 设置的。

下面是队列配置示例包含三个队列；Video 处理一个，images 处理一个，以及其他处理的 default 队列：

```
default_exchange = Exchange('default', type='direct')
media_exchange = Exchange('media', type='direct')

app.conf.task_queues = (
    Queue('default', default_exchange, routing_key='default'),
    Queue('videos', media_exchange, routing_key='media.video'),
    Queue('images', media_exchange, routing_key='media.image')
)
app.conf.task_default_queue = 'default'
app.conf.task_default_exchange = 'default'
app.conf.task_default_routing_key = 'default'1234567891011
```

这里，`task_default_queue` 将会被用来路由没有显示路由的任务。

默认消息交互器、消息交换类型以及路由键将会用作任务的默认路由值，并且作为 `task_queues` 中定义的队列的默认配置值。

一个队列多个绑定也是支持的。下面示例中两个路由键都绑定到了同一个队列：

```
from kombu import Exchange, Queue, binding

media_exchange = Exchange('media', type='direct')

CELERY_QUEUES = (
    Queue('media', [
        binding(media_exchange, routing_key='media.video'),
        binding(media_exchange, routing_key='media.image'),
    ]),
)12345678910
```

### 声明任务目的地

------

任务的目的是由下列因素决定（按顺序）
\1. `task_routes` 中定义的路由
\2. `Task.apply_async()` 方法的路由参数
\3. `Task` 本身定义的路由相关属性

最佳实践是不写硬编码这些设置，而是通过 `Routers` 将它作为配置选项；这是最灵活的方式，但是合理的默认值仍然可以设置称任务属性。

### 路由器

------

路由器是一个决定任务路由选项的函数。

定义一个路由器，你只需要定义签名未 `(name, args, kwargs, options, task=None, **kw)` 的函数：

```
def route_task(name, args, kwargs, options, task=None, **kw):
        if name == 'myapp.tasks.compress_video':
            return {'exchange': 'video',
                    'exchange_type': 'topic',
                    'routing_key': 'video.compress'}12345
```

如果你返回队列键，它将使用 ·`task_queue` 中该队列的设置扩展：

```
{'queue': 'video', 'routing_key': 'video.compress'}1
```

扩展为 ->

```
{'queue': 'video',
 'exchange': 'video',
 'exchange_type': 'topic',
 'routing_key': 'video.compress'}1234
```

你可以通过将路由添加到 `task_routes` 设置中来安装路由类：

```
task_routes = (route_task,)1
```

路由函数还可以通过名称来添加：

```
task_routes = ('myapp.routers.route_task',)1
```

对于上述这种简单的任务名称->路由的映射，你可以在 `task_routes` 设置中使用一个字典来达到同样的效果：

```
task_routes = {
    'myapp.tasks.compress_video': {
        'queue': 'video',
        'routing_key': 'video.compress',
    },
}123456
```

路由器将按顺序被遍历，直到遇到第一个返回真值的路由器，并使用它作为任务的最终路由。

你可以在一个序列中定义多个路由器：

```
task_routes = [
    route_task,
    {
        'myapp.tasks.compress_video': {
            'queue': 'video',
            'routing_key': 'video.compress',
    },
]12345678
```

路由器将被按顺序访问，首先返回值的将被选中。

### 广播

------

Celery 还支持广播路由。下列消息交换器 `broadcast_task` 将任务的拷贝递送到连接它的所有工作单元：

```
from kombu.common import Broadcast

app.conf.task_queues = (Broadcast('broadcast_tasks'),)
app.conf.task_routes = {
    'tasks.reload_cache': {
        'queue': 'broadcast_tasks',
        'exchange': 'broadcast_tasks'
    }
}123456789
```

现在，`tasks.reload_cache` 任务将递送到所有从这个队列消费的工作单元。

下面是另一个广播路由的示例，这次使用的是 `celery beat` 调度器：

```
from kombu.common import Broadcast
from celery.schedules import crontab

app.conf.task_queues = (Broadcast('broadcast_tasks'),)

app.conf.beat_schedule = {
    'test-task': {
        'task': 'tasks.reload_cache',
        'schedule': crontab(minute=0, hour='*/3'),
        'options': {'exchange': 'broadcast_tasks'}
    },
}123456789101112
```

#### 广播结果：

------

注意 Celery 结果没有定义如果两个任务有相同的任务 ID 将发生什么。如果相同的任务分发到多于一个工作单元，那么状态历史可能不会保留。

这种情况下，设置 `task.ignore_result` 属性是一个不错的注意。

- [点赞](javascript:;)
- [收藏](javascript:;)
- [分享](javascript:;)



[参考](https://blog.csdn.net/u013148156/article/details/78587375)



