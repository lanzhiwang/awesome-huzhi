# 使用 Celery

Celery 是一个专注于实时处理和任务调度的分布式任务队列。所谓任务就是消息，消息中的有效载荷中包含要执行任务需要的全部数据。

使用 Celery 的常见场景如下：

1. Web 应用。当用户触发的一个操作需要较长时间才能执行完成时，可以把它作为任务交给 Celery 去异步执行，执行完再返回给用户。这段时间用户不需要等待，提高了网站的整体吞吐量和响应时间。

2. 定时任务。生产环境经常会跑一些定时任务。假如你有上千台的服务器、上千种任务，定时任务的管理很困难，Celery 可以帮助我们快速在不同的机器设定不同种任务。

3. 同步完成的附加工作都可以异步完成。比如发送短信/邮件、推送消息、清理/设置缓存等。

Celery 还提供了如下的特性：

1. 方便地查看定时任务的执行情况，比如执行是否成功、当前状态、执行任务花费的时间等。

2. 可以使用功能齐备的管理后台或者命令行添加、更新、删除任务。

3. 方便把任务和配置管理相关联。

4. 可选多进程、Eventlet 和 Gevent 三种模式并发执行。

5. 提供错误处理机制。

6. 提供多种任务原语，方便实现任务分组、拆分和调用链。

7. 支持多种消息代理和存储后端。

## Celery 的架构

Celery 包含如下组件：

1. Celery Beat：任务调度器，Beat 进程会读取配置文件的内容，周期性地将配置中到期需要执行的任务发送给任务队列。

2. Celery Worker：执行任务的消费者，通常会在多台服务器运行多个消费者来提高执行效率。

3. Broker：消息代理，或者叫作消息中间件，接受任务生产者发送过来的任务消息，存进队列再按序分发给任务消费方（通常是消息队列或者数据库）。

4. Producer：调用了 Celery 提供的 API、函数或者装饰器而产生任务并交给任务队列处理的都是任务生产者。

5. Result Backend：任务处理完后保存状态信息和结果，以供查询。Celery 默认已支持 Redis、RabbitMQ、MongoDB、Django ORM、SQLAlchemy 等方式。

Celery 的架构图如图所示：

![](./images/01.png)

## 选择消息代理

Celery 目前支持 RabbitMQ、Redis、MongoDB、Beanstalk、SQLAlchemy、Zookeeper 等作为消息代理，但适用于生产环境的只有 RabbitMQ 和 Redis，至于其他的方式，一是支持有限，二是可能得不到更好的技术支持。

Celery 官方推荐的是 RabbitMQ，Celery 的作者 Ask Solem Hoel 最初在 VMware 就是为 RabbitMQ 工作的，Celery 最初的设计就是基于 RabbitMQ，所以使用 RabbitMQ 会非常稳定，成功案例很多。如果使用 Redis，则需要能接受发生突然断电之类的问题造成 Redis 突然终止后的数据丢失等后果。

## Celery 序列化

在客户端和消费者之间传输数据需要序列化和反序列化，Celery 支持如下表所示的序列化方案：

![](./images/02.jpg)

为了提供更高的性能，我们选择如下方案：

1. 选择 RabbitMQ 作为消息代理。

2. RabbitMQ 的 Python 客户端选择 librabbitmq 这个 C 库。

3. 选择 Msgpack 做序列化。

4. 选择 Redis 做结果存储。

下面先安装它们。Celery 提供 bundles 的方式，也就是安装 Celery 的同时可以一起安装多种依赖：

```bash
pip install "celery[librabbitmq,redis,msgpack]"
```

注：bundles 的原理是在 setup.py 的 setup 函数中添加 extras_require。

## 从一个简单的例子开始

先演示一个简单的项目让 Celery 运行起来。项目的目录结构如下：

```bash
❯ tree chapter9/section3/proj

├── celeryconfig.py

├── celery.py

├── __init__.py

└── tasks.py
```

先看一下主程序 celery.py：

```python
from __future__ import absolute_import

from celery import Celery

app = Celery('proj', include=['proj.tasks'])

app.config_from_object('proj.celeryconfig')


if __name__ == '__main__':
    app.start()

```

解析一下这个程序：

1. "from \_\_future\_\_ import absolute_import" 是拒绝隐式引入，因为 celery.py 的名字和 celery 的包名冲突，需要使用这条语句让程序正确地运行。

2. app 是 Celery 类的实例，创建的时候添加了 proj.tasks 这个模块，也就是包含了 proj/tasks.py 这个文件。

3. 把 Celery 配置存放进 proj/celeryconfig.py 文件，使用 app.config_from_object 加载配置。

看一下存放任务函数的文件 tasks.py：

```python
from __future__ import absolute_import

from proj.celery import app


@app.task
def add(x, y):
    return x + y

```

tasks.py 只有一个任务函数 add，让它生效的最直接的方法就是添加 app.task 这个装饰器。

看一下我们的配置文件 celeryconfig.py：

```python
# 使用 RabbitMQ 作为消息代理
BROKER_URL = 'amqp://dongwm:123456@localhost:5672/web_develop'

# 把任务结果存在了 Redis
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# 任务序列化和反序列化使用 msgpack 方案
CELERY_TASK_SERIALIZER = 'msgpack'

# 读取任务结果一般性能要求不高，所以使用了可读性更好的 JSON
CELERY_RESULT_SERIALIZER = 'json'

# 任务过期时间，不建议直接写 86400，应该让这样的 magic 数字表述更明显
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24

# 指定接受的内容类型
CELERY_ACCEPT_CONTENT = ['json', 'msgpack']

```

这个例子中没有任务调度相关的内容， 所以只需要启动消费者：

```bash
cd ~/web_develop/chapter9/section3

celery -A proj worker -l info

```

-A 参数默认会寻找 proj.celery 这个模块，其实使用 celery 作为模块文件名字不怎么合理。可以使用其他名字。举个例子，假如是 proj/app.py，可以使用如下命令启动：

```bash
celery -A proj.app worker -l info
```

上述信息提供了一些有帮助的内容，如消息代理和存储结果的地址、并发数量、任务列表、交换类型等。在对Celery 不熟悉的时候可以通过如上信息判断设置和修改是否已生效。

现在开启另外一个终端，用 IPython 调用 add 函数：

```python
In : from proj.tasks import add
In : r = add.delay(1, 3)
In : r
Out: <AsyncResult: 93288a00-94ee-4727-b815-53dc3474cf3f>

In : r.result
Out: 4

In : r.status
Out: u'SUCCESS'

In : r.successful()
Out: True

In : r.backend
Out: <celery.backends.redis.RedisBackend at 0x7fb2529500d0> # 保存在Redis中
```

可以看到 worker 的终端上显示执行了任务：

```python
[2016-06-03 13:34:40,749: INFO/MainProcess] Received task: proj.tasks.add[93288a00-94ee-4727-b815-53dc3474cf3f]

[2016-06-03 13:34:40,755: INFO/MainProcess] Task proj.tasks.add[93288a00-94ee-4727-b815-53dc3474cf3f] succeeded in 0.00511166098295s: 4
```

通过 IPython 触发的任务就完成了。任务的结果都需要根据上面提到的 task_id 获得，我们还可以用如下两种方式随时找到这个结果：

```python
task_id = '93288a00-94ee-4727-b815-53dc3474cf3f'

In : add.AsyncResult(task_id).get()

Out: 4
```

或者：

```python
In : from celery.result import AsyncResult

In : AsyncResult(task_id).get()

Out: 4
```

## 指定队列

Celery 非常容易设置和运行，通常它会使用默认的名为 celery 的队列（可以通过 CELERY_DEFAULT_QUEUE 修改）用来存放任务。我们可以使用优先级不同的队列来确保高优先级的任务不需要等待就得到响应。

基于 proj 目录下的源码，我们创建一个 projq 目录，并对 projq/celeryconfig.py 添加如下配置：

```python
from kombu import Queue

# 定义任务队列
CELERY_QUEUES = (
    # 路由键以 "task." 开头的消息都进 default 队列
    Queue('default', routing_key='task.#'),

    # 路由键以 "web." 开头的消息都进 web_tasks 队列
    Queue('web_tasks', routing_key='web.#')
)

# 默认的交换机名字为 tasks
CELERY_DEFAULT_EXCHANGE = 'tasks'

# 默认的交换类型是 topic
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'

# 默认的路由键是 task.default，这个路由键符合上面的 default 队列
CELERY_DEFAULT_ROUTING_KEY = 'task.default'

CELERY_ROUTES = {
    # tasks.add 的消息会进入 web_tasks 队列
    'projq.tasks.add': {
        'queue': 'web_tasks',
        'routing_key': 'web.add'
    }
}

```

现在用指定队列的方式启动消费者进程：

```bash
celery -A projq worker -Q web_tasks -l info
```

上述 worker 只会执行 web_tasks 中的任务，我们可以合理安排消费者数量，让 web_tasks 中任务的优先级更高。

## 使用任务调度

之前的例子都是由发布者触发的，本节展示一下使用 Celery 的 Beat 进程自动生成任务。基于 proj 目录下的源码，创建一个 projb 目录，对 projb/celeryconfig.py 添加如下配置：

```python
CELERYBEAT_SCHEDULE = {
    'add': {
        'task': 'projb.tasks.add',
        'schedule': timedelta(seconds=10),
        'args': (16, 16)
    }
}
```

CELERYBEAT_SCHEDULE 中指定了 tasks.add 这个任务每 10 秒跑一次，执行的时候的参数是 16 和 16。

启动 Beat 程序：

```bash
celery beat -A projb
```

然后启动 Worker 进程：

```bash
celery -A projb worker -l info
```

之后可以看到每 10 秒都会自动执行一次 tasks.add。

注：Beat 和 Worker 进程可以一并启动：

```bash
celery -B -A projb worker -l info
```

使用 Django 可以通过 django-celery 实现在管理后台创建、删除、更新任务，是因为它使用了自定义的调度类djcelery.schedulers.DatabaseScheduler，我们可以参考它实现 Flask 或者其他 Web 框架的管理后台来完成同样的功能。使用自定义调度类还可以实现动态添加任务。

## 任务绑定、记录日志和重试

任务绑定、记录日志和重试是 Celery 常用的 3 个高级属性。现在修改 proj/tasks.py 文件，添加 div 函数用于演示：

```python
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@app.task(bind=True)
def div(self, x, y):
    logger.info(('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}').format(self.request))
    try:
        result = x / y
    except ZeroDivisionError as e:
        raise self.retry(exc=e, countdown=5, max_retries=3)
    return result

```

当使用 bind = True 后，函数的参数发生变化，多出了参数 self（第一个参数），相当于把 div 变成了一个已绑定的方法，通过 self 可以获得任务的上下文。

在 IPython 中调用 div ：

```python
In : from proj.tasks import div

In : r = div.delay(2, 1)
```

可以看到如下执行信息：

```python
[2016-06-03 15:50:31,853: INFO/Worker-1] proj.tasks.div[1da82fb8-20de-4d5a-9b48-045da6db0cda]: Executing task id 1da82fb8-20de-4d5a-9b48-045da6db0cda, args: [2, 1] kwargs: {}
```

换成能造成异常的参数：

```python
In : r = div.delay(2, 0)
```

可以发现每 5 秒就会重试一次，一共重试 3 次（默认重复 3 次），然后抛出异常。

[参考](https://zhuanlan.zhihu.com/p/22304455)