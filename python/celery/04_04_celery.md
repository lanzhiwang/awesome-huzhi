# Celery-4.1 用户指南: Calling Tasks

## 基础

本文档描述 Celery 中任务实例和 Canvas 使用的统一 “Calling API”。

API 中定义了一个执行选项的标准集，以及三个方法：
- `apply_async(args[, kwargs[, ...]])` 发送任务消息
- `delay(*args, **kwargs)` 发送任务消息的简写，不支持执行选项
- `calling`(`__call__`) 直接调用任务对象，意味着任务不会被工作单元执行，而是在当前进程中执行（不会发送任务消息）

Quick Cheat Sheet

- T.delay(arg, kwarg=value) `.apply_async` 方法的参数简写方式。（`.delay(*args, **kwargs)` 会调用 `.apply_async(args, kwargs)`）

- `T.apply_async((arg,), {'kwarg': value})`

- `T.apply_async(countdown=10)` 从现在开始10秒后执行任务.

- `T.apply_async(eta=now+timedelta(seconds=10))` 从现在开始10秒后执行任务，这里使用 eta 声明

- `T.apply_async(countdown=60, expires=120)` 从现在开始1分钟后执行任务，任务过期时间为2分钟

- `T.apply_async(expires=now+timedelta(days=2))` 任务过期时间为2天，使用 datetime 设置

### 示例

使用 `delay` 方法很方便，就像使用一个常规函数：

```python
task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
```

使用 `apply_async()` 方法，你必须这样写：

```python
task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})
```

因此，`delay` 要方便得多，但是如果你想设置额外的执行选项，你不得不使用 `apply_async`。

本文档接下来将深入讲解执行选项。所有的例子都使用一个名为 `add` 的任务，它返回两个参数的和。

```python
@app.task
def add(x, y):
    return x + y
```

提示：如果任务没有在当前进程注册，你可以使用 `send_task()` 方法依据名称调用对应任务。

还有其他的方法…

当读到 Canvas 这一节时，你将会学习到关于启动任务的更多知识，`signature` 是用来传递函数调用签名的对象，（例如在网络上传输），并且他们还支持API调用：

```python
task.s(arg1, arg2, kwarg1='x', kwargs2='y').apply_async()
```

## Linking (callbacks/errbacks)

Celery 支持链接任务，这使得执行一个任务之后接着执行另一个任务。回调任务会将父任务的结果作为本任务函数的部分参数。

```python
add.apply_async((2, 2), link=add.s(16))
```

这里第一个任务 (4) 将会发送到另一个任务将 16 与前面结果相加，形成表达式 `(2 + 2) + 16 = 20`

如果任务抛出异常（`errback`），你也可以让回调函数执行，但是与常规的回调不同的是它将会传递父任务的 ID 而不是结果值。这是由于并不总是可以序列化抛出的异常，并且这种情况下，错误回调需要启用一个结果存储后端，另外任务需要自己获取父任务的结果。

下面是一个错误回调的例子：

```python
@app.task
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task {0} raised exception: {1!r}\n{2!r}'.format(uuid, exc, result.traceback))
```

它可以使用 `link_error` 执行选项添加进任务：

```python
add.apply_async((2, 2), link_error=error_handler.s())
```

除此之外，`link`和 `link_error` 执行选项可以在一个列表中声明：

```python
add.apply_async((2, 2), link=[add.s(16), other_task.s()])
```

`callback/errbacks` 将按顺序执行，并且所有回调函数调用时将使用父任务的返回值作为部分参数。

What’s s ?
这里使用的`add.s` 被称为一个签名。如果你不知道他们是什么，你可以看 `canvas guide` 这一节。从那里你还可以学习到 `chain`: 一个将任务串起来的简单方法。

实际操作中，`link` 执行选项被当做一个内部原语，你可能并不直接使用它，而是使用 `chain`。

## On message

Celery 通过设置 `setting_on_message` 回调支持捕获所有状态变更。

例如，对于长时间任务，你可以通过如下类似操作更新任务进度：

```python
@app.task(bind=True)
def hello(self, a, b):
    time.sleep(1)
    self.update_state(state="PROGRESS", meta={'progress': 50})
    time.sleep(1)
    self.update_state(state="PROGRESS", meta={'progress': 90})
    time.sleep(1)
    return 'hello world: %i' % (a+b)

def on_raw_message(body):
    print(body)

r = hello.apply_async()
print(r.get(on_message=on_raw_message, propagate=False))
```

将会产生如下输出：

```
{
    'task_id': '5660d3a3-92b8-40df-8ccc-33a5d1d680d7',
    'result': {'progress': 50},
    'children': [],
    'status': 'PROGRESS',
    'traceback': None
}
{
    'task_id': '5660d3a3-92b8-40df-8ccc-33a5d1d680d7',
    'result': {'progress': 90},
    'children': [],
    'status': 'PROGRESS',
    'traceback': None
}
{
    'task_id': '5660d3a3-92b8-40df-8ccc-33a5d1d680d7',
    'result': 'hello world: 10',
    'children': [],
    'status': 'SUCCESS',
    'traceback': None
}
hello world: 10
```

## ETA and Countdown

ETA（估计到达时间）使你可以声明任务将被执行的最早时间。以后，`countdown` 是设置 ETA 的快捷方式。

```python
>>> result = add.apply_async((2, 2), countdown=3)
# this takes at least 3 seconds to return
>>> result.get()
4
```

任务保证在声明的日期和时间后执行，当时不一定是所声明的准确时间。可能的原因是消息中间件的最后期限队列中可能包含多个等待执行的任务，或者是严重的网络延迟。为了保证你的任务能及时执行，你应该监控队列的阻塞情况。使用 `Munin` 或者类似的工具来获取报警，那么能采取恰当的措施来减轻负载。

`countdown` 是一个整数， 但是 `eta` 必须是一个 `datetime` 对象，用来声明一个精确的日期和时间（包含毫秒精度，以及时区信息）：

```python
>>> from datetime import datetime, timedelta
>>> tomorrow = datetime.utcnow() + timedelta(days=1)
>>> add.apply_async((2, 2), eta=tomorrow)
```

## Expiration

`expires` 参数定义了一个可选的过期时间，可以是任务发布后的秒数，或者使用 `datetime` 声明一个日期和时间。

```python
# Task expires after one minute from now.
>>> add.apply_async((10, 10), expires=60)

# Also supports datetime
>>> from datetime import datetime, timedelta
>>> add.apply_async((10, 10), kwargs, expires=datetime.now() + timedelta(days=1))
```

当工作单元接收到一个过期任务，它会将任务标记为 `REVOKED`（`TaskRevokeError`）。

## Message Sending Retry

当链接失败，celery 会重试发送任务消息，并且重试行为可以设置 - 比如重试的频率，或者最大重试次数 - 或者禁用所有。

禁用消息发送重试，你可以设置重试的执行选项为 `False`：

```python
add.apply_async((2, 2), retry=False)
```

相关设置：

* task_publish_retry
* task_publish_retry_policy

### 重试策略

重试策略是一个映射，用来控制重试怎样进行，包含如下键：

- `max_retries` 放弃重试前的最大重试次数，这种情况下导致重试的异常会被重新抛出。`None` 值意味着一直重试，默认重试3次

- `interval_start` 定义首次重试间隔的秒数（浮点数或者整数）。默认是0（首次重试会立即进行）

- `interval_step` 每进行一次重试，这个值会加到重试延迟里（浮点数或者整数）。默认是 0.2。

- `interval_max` 重试之间间隔的最大秒数（浮点数或者整数）。默认是 0.2。

例如，关联到默认的策略：

```python
add.apply_async((2, 2), retry=True, retry_policy={
    'max_retries': 3,
    'interval_start': 0,
    'interval_step': 0.2,
    'interval_max': 0.2
})
```

用于重试的最长时间会是 0.4 秒。时间默认设置得相对短是由于如果消息中间件断链接了会导致链接失败重试堆积效果 - 例如，许多 WEB 服务器会由于处理等待重试而阻塞其他的请求。

## Connection Error Handling

当你发送一个任务消息，而消息传输链接丢失了，或者链接不能被初始化了，一个 `OperationError` 错误将会被抛出：

```python
>>> from proj.tasks import add
>>> add.delay(2, 2)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "celery/app/task.py", line 388, in delay
        return self.apply_async(args, kwargs)
  File "celery/app/task.py", line 503, in apply_async
    **options
  File "celery/app/base.py", line 662, in send_task
    amqp.send_task_message(P, name, message, **options)
  File "celery/backends/rpc.py", line 275, in on_task_call
    maybe_declare(self.binding(producer.channel), retry=True)
  File "/opt/celery/kombu/kombu/messaging.py", line 204, in _get_channel
    channel = self._channel = channel()
  File "/opt/celery/py-amqp/amqp/connection.py", line 272, in connect
    self.transport.connect()
  File "/opt/celery/py-amqp/amqp/transport.py", line 100, in connect
    self._connect(self.host, self.port, self.connect_timeout)
  File "/opt/celery/py-amqp/amqp/transport.py", line 141, in _connect
    self.sock.connect(sa)
  kombu.exceptions.OperationalError: [Errno 61] Connection refused
```

如果有设置了重试配置，这种错误只有在达到最大重试次数，或者立即关闭的情况下才会发生。

你也可以这样处理这种错误：

```python
>>> from celery.utils.log import get_logger
>>> logger = get_logger(__name__)
>>> try:
...     add.delay(2, 2)
... except add.OperationalError as exc:
...     logger.exception('Sending task raised: %r', exc)
```

## Serializers

客户端和工作单元之间的数据传输需要序列化，所以每个 celery 的消息都有一个  `content_type` 请求头用来描述编码使用的序列化方法。

默认的序列化器是 `json`，但是你可以通过 `task_serializer` 设置修改序列化器，或者针对单个任务，甚至单个消息设置序列化器。

内建的序列化器有 `JSON, pickle, YAML` 以及 `msgpack`，你还可以将自定义的序列化器注册到 Kombu 序列化器注册表。

另见：Kombu 用户指南中的消息序列化。

每个选项都有优点和缺点。

- json
	* JSON 在许多语言中都有支持，现在是 python 标准的一部分（从2.6开始），而且通过使用现代化的 python 库，例如 simplejson，可以非常快的编码。
	* JSON 的主要缺点是它限制了你只能使用如下数据类型：strings, Unicode, floats, Boolean, dictionaries, and lists. Decimals 与 dates 明显都没有。
	* 二进制数据会使用 Base64 编码传输，比原生支持二进制数据类型的序列化方法增加了 34% 的数据传输量。
	* 但是，如果你的数据满足以上限制，并且你需要跨语言支持，那么默认的 JSON 序列化可能是你最佳的选择。

- pickle
	* 如果你不想支持除 python 外的其他语言，那么 pickle 编码将使你获得所有 python 数据类型的支持（除了类实例），发送二进制文件时消息更小，并且比 JSON 处理稍快。

- yaml
	* YAML 有许多与 json 相似的特性，但是它原生支持更多的数据类型（包括日期，递归引用，等等）。
	* 但是，YAML 的python库比 JSON 库要慢一些。
	* 如果你需要一个更富有表达性的数据类型的集合，并且需要保持跨语言兼容，那么 YAML 会是比上述其他序列化更好的选择。

- msgpack
	* msgpack 是一个特性上与 JSON 类似的一个二进制序列化格式。但是应用时间还比较短，在这个时间点对它的支持是实验性的。

使用的编码方式在消息头中可查看到，所以工作单元知道怎么反序列化任何任务。如果你使用一个自定义的序列化器，那么它必须也在工作单元可用。

下列顺序用来确定在发送消息时使用什么序列化器：

1. 执行选项 `serializer`
2. `Task.serializer` 属性
3. `task_serializer` 设置

为单个任务调用设置自定义的序列化器的示例：

```python
>>> add.apply_async((10, 10), serializer='json')1
```

## Compression

Celery 使用 gzip 或者 bzip2 压缩消息。你也可以创建自己的压缩模式，并注册到 Kombu 压缩模式注册表。

下列顺序用来确定当发送消息时使用什么压缩模式：

1. 执行选项 `compression`
2. `Task.compression` 属性
3. `task_compression` 设置

当调用一个任务时声明压缩模式的示例：

```python
>>> add.apply_async((2, 2), compression='zlib')1
```

## Connections

**Automatic Pool Support**

从 2.3 版本开始支持自动连接池，所以你没有必要手动处理连接与发布者来重用这些连接。

从 2.5 版本开始，连接池默认被启用。

你可以通过创建一个发布者来手动处理连接：

```python
results = []
with add.app.pool.acquire(block=True) as connection:
    with add.get_publisher(connection) as publisher:
        try:
            for args in numbers:
                res = add.apply_async((2, 2), publisher=publisher)
                results.append(res)

print([res.get() for res in results])
```

当然，这个特殊的例子用 group 更更好的表达：

```python
>>> from celery import group

>>> numbers = [(2, 2), (4, 4), (8, 8), (16, 16)]
>>> res = group(add.s(i, j) for i, j in numbers).apply_async()

>>> res.get()
[4, 8, 16, 32]
```

## Routing options

Celery 可以路由任务到不同的队列。

简单的路由（name <-> name）是通过 queue 选项来实现:

```python
add.apply_async(queue='priority.high')
```

你可以使用 -Q 命令行参数将工作单元分配到 `priority.high` 队列：

```bash
$ celery -A proj worker -l info -Q celery,priority.high
```

[参考](https://blog.csdn.net/u013148156/article/details/78563222)
