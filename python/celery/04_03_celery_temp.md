# Celery-4.1 用户指南: Task

任务是构建 celery 应用的基础块。

任务是可以在任何除可调用对象外的地方创建的一个类。它扮演着双重角色，它定义了一个任务被调用时会发生什么（发送一个消息），以及一个工作单元获取到消息之后将会做什么。

每个任务都有不同的名称，发给 celery 的任务消息中会引用这个名称，工作单元就是根据这个名称找到正确的执行函数。

任务消息只有在被工作单元确认后才会从队列中删除。工作单元会预先保存许多任务消息，如果工作单元被杀死-由于断电或者其他原因-任务消息将会重新传递给其他工作单元。

理想的任务函数应该是具有幂等性的：这意味着即使一个任务函数以同样的参数被调用多次也不会导致不可预料的效果。因为工作单元无法探测任务是否是幂等的，所以默认的行为是在即将执行之前预先确认任务消息，这使得已经开始的任务不会再被执行。

如果你的任务函数是幂等的，你可以设置 `acks_late` 选项让工作单元在任务执行返回之后再确认任务消息。

注意：如果执行任务的子进程被终止（通过调用 sys.exit() 或者通过信号），即使 `acks_late` 选项被激活，工作单元也会确认当前处理的任务消息。这么做的理由是：

1. 对于会迫使内核发送 `SIGSEGV`（段错误）或者类似信号给进程的任务，我们不想再重新执行

2. 我们假设刻意终止任务的系统管理员不会想这个任务重新执行

3. 消耗过多内存的任务由触发内核内存溢出的危险，如果重复执行，同样的事情还会发生

4. 一直失败的任务再重新递送消息时会导致高频的消息循环影响到整个系统

如果你真的想在这些情况下重新递送任务消息，你应该考虑使能 `task_reject_on_worker_lost` 设置。

告警：一个无限期阻塞的任务会使得工作单元无法再做其他事情。

如果你的任务里有 I/O 操作，请确保给这些操作加上超时时间，例如使用 `requests` 库时给网络请求添加一个超时时间：

```python
connect_timeout, read_timeout = 5.0, 30.0
response = requests.get(URL, timeout=(connect_timeout, read_timeout))
```

时间限制对确保所有任务在规定的时间内返回很方便，但是一个超市事件将会强制终止进程，所以应该只有在没有手动设置超时时间的地方使用。

默认的 `prefork` 池调度器对长时间任务不是很友好，所以如果你的任务需要运行很长时间，确保在启动工作单元时使能了 `-ofair` 选项。

如果你的工作单元被挂起了，请先看看它运行的是什么任务，而不是先提交问题，因为大部分情况下挂起是由于一个或多个任务阻塞在网络操作上。

本章将学习定义任务的所有知识，以下是目录：
- Basic
- Names
- Task Request
- Logging
- Retrying
- List of Options
- States
- Semipredicates
- Custom task classes
- how it works
- Tips and Best Proctices
- Performance and Strategies
- Example

## 基础

通过使用 `task()` 装饰器，你可以很容易创建一个任务：

```python
from .models import User

@app.task
def create_user(username, password):
    User.objects.create(username=username, password=password)
```

任务上可以设置很多选项，这些选项作为参数传递给装饰器：

```python
@app.task(serializer='json')
def create_user(username, password):
    User.objects.create(username=username, password=password)
```

多个装饰器：

当使用多个装饰器装饰任务函数时，确保 `task` 装饰器最后应用（在 python 中，这意味它必须在第一个位置）：

```python
@app.task
@decorator2
@decorator1
def add(x, y):
    return x + y
```

应该如何导入任务装饰器？什么是 `app` ?

任务装饰器可以从 Celery 应用实例上获取，如果不理解，请先看 First Steps with Celery。

如果你使用 `Django` （请看 First steps with Django），或者你是一个库的作者，那么可能想使用 `shared_task（）` 装饰器：

```python
from celery import shared_task

@shared_task
def add(x, y):
    return x + y
```

### 绑定任务

一个绑定任务意味着任务函数的第一个参数总是任务实例本身(`self`)，就像 Python 绑定方法类似：

```python
logger = get_task_logger(__name__)

@task(bind=True)
def add(self, x, y):
    logger.info(self.request.id)
```

绑定任务在这些情况下是必须的：任务重试（使用 `app.Task.retry()` )，访问当前任务请求的信息，以及你添加到自定义任务基类的附加功能。

### 任务继承

任务装饰器的 `base` 参数可以声明任务的基类：

```python
import celery

class MyTask(celery.Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))

@task(base=MyTask)
def add(x, y):
    raise KeyError()
```

## 任务名称

每个任务必须有不同的名称。

如果没有显示提供名称，任务装饰器将会自动产生一个，产生的名称会基于这些信息：

1. 任务定义所在的模块
2. 任务函数的名称

显示设置任务名称的例子：

```python
>>> @app.task(name='sum-of-two-numbers')
>>> def add(x, y):
...     return x + y

>>> add.name
'sum-of-two-numbers'
```

最佳实践是使用模块名称作为命名空间，这样的话如果有一个同名任务函数定义在其他模块也不会产生冲突。

```python
>>> @app.task(name='tasks.add')
>>> def add(x, y):
...     return x + y
```

你可以通过任务函数的 `.name` 属性获取任务的名称：

```python
>>> add.name
'tasks.add'
```

`tasks.py` 模块中定义任务，其自动产生的名称就是上述这种形式。

```python
@app.task
def add(x, y):
    return x + y123
>>> from tasks import add
>>> add.name
'tasks.add'
```

### 自动命名与相对导入

绝对导入：

对于 python2，开发者的最佳实践是在每个模块前添加下面这句代码：

```python
from __future__ import absolute_import
```

这会总是强制使用绝对导入，所以使用相对导入的任务将不会出现相对导入相关的问题。

在 python3 中，默认就是绝对导入的，所以不需要再额外添加其他代码。

相对导入和任务名称自动生成混合使用时会有些问题，所以如果你使用相对导入，你应该显示设置任务名称。

例如，客户端导入模块 `myapp.tasks` 时使用 `.tasks` ，而工作单元导入模块使用 `myapp.tasks`， 他们产生的名称会不匹配，任务调用时工作单元会报 `NotRegistered` 错误。

在使用 Django 和 include_apps 中应用 `project.myapp-` 形式的命名时也会出现同样的问题：

```python
INSTALLED_APPS = ['project.myapp']
```

如果你在命名空间 `project.myapp` 下安装应用时，任务模块将会被导入为 `project.myapp.tasks`， 所以你必须确保总是使用相同的名称导入任务：

```python
# GOOD
>>> from project.myapp.tasks import mytask

# BAD
>>> from myapp.tasks import mytask
```

第二个例子里任务的名称会不一样，因为工作单元与客户端在不同的名称空间下导入模块：

```python
>>> from project.myapp.tasks import mytask
>>> mytask.name
'project.myapp.tasks.mytask'

>>> from myapp.tasks import mytask
>>> mytask.name
'myapp.tasks.mytask'
```

基于这一点，你必须在导入模块时保持一致，这也是 python 的最佳实践。

同样的，你不应该使用老式的相对导入：

```python
# BAD
from module import foo

# GOOD
from proj.module import foo
```

新式的相对导入能够被正常使用：

```python
# GOOD
from .module import foo
```

如果你使用 celery 的项目里已经重度使用了这些模式，而且你没时间再去重构现有代码，那么你可以考虑现实声明任务名称而不是依赖于自动名称生成。

```python
@task(name='proj.tasks.add')
def add(x, y):
    return x + y
```

### 改变自动名称生成形式

4.0 版本新特性。

在有些情况，默认的自动名称生成规则并不合适。例如你在多个不同模块定义了多个任务：

```bash
project /
        / __init__.py
        / celery.py
        / moduleA /
                  / __init__.py
                  / tasks.py
        /moduleB /
                 / __init__.py
                 / tasks.py
```

使用默认的自动名称生成行为，每个任务都会有一个自动产生的名称如 `moduleA.tasks.taskA, moduleA.tasks.taskB, moduleB.tasks.test` 等等。你可能想去掉所有任务名称中的 tasks 字段。如上面已经指出的，你可以显示的给每个任务指定名称，或者你还可以通过覆盖 `app.gen_task_name()` 方法修改自动名称生成行为。继续以上这个例子，`celery.py` 可能包含：

```python
from celery import Celery

class MyCelery(Celery):
    def gen_task_name(self, name, module):
        if module.endswith('.tasks'):
            module = module[:-6]
        return super(MyCelery, self).gen_task_name(name, module)
```

此时，每个任务都一个这种形式的名称 `moduleA.taskA, moduleA.taskB, moduleB.test`。

告警：确保你的 `app.gen_task_name()` 函数是一个纯函数：意味着对于同样的输入它总是会返回相同的输出。

## 任务请求

`app.Task.request` 包含当前执行任务相关的信息与状态。

任务请求定义了以下属性：

* id：执行任务的唯一 id

* group：如果任务属于一个组，这个属性表示组 id

* chord: 任务所属 chord 的 id（如果任务是header的一部分）

* correlation_id：自定义 ID，用来处理类似重复删除操作

* args：位置参数

* kwargs：关键字参数

* origin：发送任务消息的主机名

* retries：当前任务已经重试的次数。它是一个从 0 开始的整数

* is_eager：如果任务是在客户端本地执行而不是通过工作单元执行，那么这个属性设置为 True

* eta：任务的原始 ETA（如果存在）。用 UTC 时间表示（依赖于 `enable_utc` 设置）

* expires：原始的过期时间（如果存在）。用 UTC 时间（依赖于 `enable_utc` 设置）

* hostname: 执行任务的工作单元的节点名称

* delivery_info：附加的消息传递消息。它是一个映射，包含用来递送任务消息的路由规则以及路由键。例如， `app.Task.retry()` 函数可以根据它来重新发送消息到相同的目标队列。该映射中的键的可用性取决于使用的消息中间件


* reply-to：回复发送的目的队列的名称（例如在 RPC 存储后端中使用）

* called_directly：如果任务不是由执行单元执行，这个属性设置为 `True`

* timelimit：它是一个元组，表示任务上当前激活的（软性，硬性）时间限制（如果存在）

* callbacks：如果任务执行成功，将被调用的函数签名的列表

* errback：如果任务还行失败，将被调用的函数签名的列表

* utc：如果调用者使能了 UTC（`enable_utc`），这个属性为`True`

3.1 版本新特性

* headers：与任务消息一起发送的消息头的映射（可以为 `None`）

* reply_to：回复发送的目的队列的名称

* correlation_id：通常与任务 id 相同，一般在 amqp 中用来跟踪回复是发送到哪里

4.0 新特性

* root_id：任务所属的工作流的第一个任务的唯一 id（如果存在）

* parent_id：调用任务的任务的唯一 id

* chain：组成一个任务链的预留任务的列表（如果存在）。列表中最后一项将是当前任务的下一个任务

示例：

下面是一个访问任务上下文信息的任务函数示例

```python
@app.task(bind=True)
def dump_context(self, x, y):
    print('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(self.request))
```

绑定参数说明这个函数是一个”绑定方法”，所以可以访问任务实例的属性和方法。

## 日志

任务工作单元会自动给你设置日志环境，当然你也可以手动配置日志。

celery 提供了一个特殊的日志句柄 “celery.task”，你可以通过继承这个句柄自动获取任务名称和唯一  id 作为日志的一部分。

最佳实践是在模块的开头创建一个所有任务公用的日志句柄：

```python
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@app.task
def add(x, y):
    logger.info('Adding {0} + {1}'.format(x, y))
    return x + y
```

celery 使用 python 标准日志库，可以在 python 官方文档中找到。

你可以使用 `print()` 函数，因为任意写入到标准输出/标准错误输出的东西都会被重定向到日志系统（你可以禁用这个特性，请查看 `worker_redirect_stdouts` 这一节）。

注意：如果你在任务函数或者模块中创建一个日志句柄，任务工作单元不会更新这个重定向行为。如果你想重定向 `sys.stdout` 和 `sys.stderr` 到一个自定义日志句柄，你必须手动使能它。例如：

```python
import sys

logger = get_task_logger(__name__)

@app.task(bind=True)
def add(self, x, y):
    old_outs = sys.stdout, sys.stderr
    rlevel = self.app.conf.worker_redirect_stdouts_level
    try:
        self.app.log.redirect_stdouts_to_logger(logger, rlevel)
        print('Adding {0} + {1}'.format(x, y))
        return x + y
    finally:
        sys.stdout, sys.stderr = old_outs
```

### 参数检查

4.0 版本新特性

当你调用任务函数时，Celery 会验证传递的参数，就像调用一个普通函数时 Python 所做的检查。

```python
>>> @app.task
... def add(x, y):
...     return x + y

# Calling the task with two arguments works:
>>> add.delay(8, 8)
<AsyncResult: f59d71ca-1549-43e0-be41-4e8821a83c0c>

# Calling the task with only one argument fails:
>>> add.delay(8)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "celery/app/task.py", line 376, in delay
    return self.apply_async(args, kwargs)
  File "celery/app/task.py", line 485, in apply_async
    check_arguments(*(args or ()), **(kwargs or {}))
TypeError: add() takes exactly 2 arguments (1 given)
```

你可以通过设置任务的 `typing` 属性为 `False` 来禁用参数检查。

```python
>>> @app.task(typing=False)
... def add(x, y):
...     return x + y

# Works locally, but the worker reciving the task will raise an error.
>>> add.delay(8)
<AsyncResult: f59d71ca-1549-43e0-be41-4e8821a83c0c>
```

### 隐藏参数中的敏感信息

4.0 版本新特性。

当使用 `task_protocal 2` 或者更高版本（默认从 4.0 版本开始），你可以通过使用 `argsrepr` 和 `kwargsrepr` 参数来覆盖日志和监控事件中位置参数和关键字参数的显示：

```python
>>> add.apply_async((2, 3), argsrepr='(<secret-x>, <secret-y>)')
>>> charge.s(account, card='1234 5678 1234 5678').set(kwargsrepr=repr({'card': '**** **** **** 5678'})).delay()
```

告警：对于可以从任务中间件中读取任务消息或者可以截取到消息的人来说，敏感信息仍然是可以访问的。基于这个原因，如果你的消息中含有敏感信息，你应该加密信息，或者如上示例中带有信用卡号之类的信息可以将其加密存储到一个安全的存储，然后任务中从存储中获取并解密。

## 重试

`app.Task.retry()` 函数可以用来重新执行任务，例如在可恢复错误的事件中。

当你调用 `retry` 函数，它将发送一个新的消息，使用相同的任务 id，而且它会小心确保该消息投递到原始任务相同的队列。

一个任务被重试将记录为一个任务状态，因此你可以使用结果实例跟踪任务的进度（查看状态这一节）。

以下是一个使用 `retry` 函数的例子：

```python
@app.task(bind=True)
def send_twitter_status(self, oauth, tweet):
    try:
        twitter = Twitter(oauth)
        twitter.update_status(tweet)
    except (Twitter.FailWhaleError, Twitter.LoginError) as exc:
        raise self.retry(exc=exc)
```

注意：
`app.Task.retry()` 调用将会抛出一个异常使得任意 `retry` 后面的代码都不会被执行。这个异常就是 `Retry` 异常，它不是作为一个错误来处理而是作为一个semi-predicate 来告诉任务工作单元这个任务将被重试，从而当后端存储已经使能的情况下工作单元能将正确的状态存储到后端存储。

这是一个常规的操作，而且除非 `retry` 函数的 `throw` 参数设置为 `False`，这个异常将总是会抛出。

`exc` 参数是用来传递在日志中使用或者在后端结果中存储的异常信息。异常和堆栈回溯信息都可以在任务状态中看到（如果后端存储被使能）。

当任务带有 `max_retries` 值，如果已经达到最大尝试次数，当前异常会被重新被抛出，但是下列情况除外：
\- 没有给定 exc 参数
这种情况下，`MaxRetriesExceededError` 异常将会被抛出。
\- 当前没有异常
如果没有原始异常被重新抛出，`exc` 参数将会被使用，因此：

```
self.retry(exc=Twitter.LoginError())1
```

将会抛出 `exc` 给定的异常。

### 使用自定义重试延迟

------

当一个任务被重试，它在重试前会等待给定的时间，并且默认的延迟是由 `default_retry_delay` 属性定义。默认设置为 3 分钟。注意延迟设置的单位是秒（int 或者 float）。

你可以通过提供 `countdown` 参数覆盖这个默认值。

```
@app.task(bind=True, default_retry_delay=30 * 60)  # retry in 30 minutes.
def add(self, x, y):
    try:
        something_raising()
    except Exception as exc:
        # overrides the default delay to retry after 1 minute
        raise self.retry(exc=exc, countdown=60)1234567
```

### 对已知异常的自动尝试

------

4.0 版本新特性。

有时候，你只想在特定异常抛出时重试任务。

幸运的是，你可以通过使用任务装饰器中的 `autoretry_for` 参数让 Celery 自动尝试一个任务：

```
from twitter.exceptions import FailWhaleError

@app.task(autoretry_for=(FailWhaleError,))
def refresh_timeline(user):
    return twitter.refresh_timeline(user)12345
```

如果你想给内部调用的 `Task.retry` 函数传递自定义的参数，你可以传递 `retry_kwargs` 参数给任务装饰器：

```
@app.task(autoretry_for=(FailWhaleError,),
          retry_kwargs={'max_retries': 5})
def refresh_timeline(user):
    return twitter.refresh_timeline(user)1234
```

这给手动处理异常提供了另一种方案，以上示例与在任务函数中使用 `try...except` 语句来重试任务有同样的效果：

```
@app.task
def refresh_timeline(user):
    try:
        twitter.refresh_timeline(user)
    except FailWhaleError as exc:
        raise div.retry(exc=exc, max_retries=5)123456
```

如果你想在发生任意错误时重试，可以这样：

```
@app.task(autoretry_for=(Exception,))
def x():
    ...123
```

4.1 版本新特性。

如果你的任务依赖于其他服务，例如给 API 发送请求，那么比较好的一个方式是使用指数退避来规避对服务造成冲击。幸运的是，Celery 的自动重试机制能非常简单实现这个。只要对声明 `retry_backoff` 参数，如下：

```
from requests.exceptions import RequestException

@app.task(autoretry_for=(RequestException,), retry_backoff=True)
def x():
    ...12345
```

默认情况下，指数退避还会引入一个随机 `jitter` 来避免所有任务统一时刻运行。指数退避的最大退避延迟默认是 10 分钟。所有的设置都可以通过选项自定义，如下选项：

`Task.autoretry_for`
一个异常类的列表或者元组。如果在任务执行期间任何一个其中异常抛出，任务将会被自动重试。默认情况下，没有异常会被重试。

`Task.retry_kwargs`
一个映射。使用这个属性可以自定义重试怎么执行。注意如果你使用下面所述的指数退避选项，那么任务的 `countdown` 选项将会由Celery的自动重试系统决定，而这个映射中的 `countdown` 将会被忽略。

`Task.retry_backoff`
布尔值，或者数字。如果这个选项设置为 True，重试将会按照指数退避规则延迟。第一次重试将延迟1秒，第二次重试将延迟2秒，第三次重试将延迟4秒，第四次重试将延迟8秒，以此类推。（但是，如果 `retry_jitter` 选项被启用，延迟值将依据它更新）。如果这个选项设置成数字，它将作为一个延迟因子。例如，如果设置成3，第一次重试延迟3秒，第二次重试延迟6秒，第三次重试延迟12秒，第四次重试延迟24秒，以此类推。默认情况下，这个选项设置成 `False`，此时重试不会有延迟。

`Task.retry_backoff_max`
数字。如果 `retry_backoff` 被启用，这个选项将设置两次重试之间的最大延迟。默认情况下，这个选项设置为 600 秒，即 10 分钟。

`Task.retry_jitter`
布尔值。`jitter` 用来在指数退避中引入随机性，从而避免队列中所有任务同时执行。如果这个选项被设置为 `True`，那么 `retry_backoff`j计算出的延迟值将认为是最大值，实际延迟值是0到最大值之间的一个随机值。默认情况下，这个选项设置为 `True`。

## 选项列表

------

任务装饰器有一系列选项可以用来修改任务的行为，例如可以通过 `rate_limit` 选项来设置任务的速率限制。

传递给任务装饰器的关键字参数将会设置为结果任务类的一个属性，下面是内建属性的列表。

General
`Task.name`
任务注册的名称

你可以手动设置任务名称，或者任务名称将依据模块名与类名自动生成。

另见任务名称这一节。

`Task.request`
如果任务将被执行，这个属性会包含当前请求的信息。会使用Thread local 存储。

另见任务请求这一节。

`Task.max_retries`
只有在任务函数中调用了 `self.retry` 函数或者给任务装饰器传递了 `autoretry_for` 参数时才有用。

放弃任务前的最大尝试次数。如果尝试次数超过这个值，`MaxRetriesExceededError` 异常将会被抛出。

注意：
你必须手动调用 `retry` 函数，否则发生异常时不会自动重试。

默认值是3。如果设置为 `None`，将禁用重试限制，任务将一直重试直到成功。

`Task.throws`
一个可选的预知错误类元组，不认为是真正的错误。

这个列表中的错误将作为一个失败记录到后端存储中，但是任务工作单元不会将这个时间记录成一个错误，并且不包含异常回溯信息。

示例：

```
@task(throws=(KeyError, HttpNotFound)):
def get_foo():
    something()123
```

错误类型：
\- 预知错误（在 `Task.throws` 中）
日志级别为 Info，堆栈回溯信息不包含在内
\- 非预知错误
日志级别为 Error，包含堆栈回溯信息

`Task.default_retry_delay`
任务重试前延迟的默认时间值，以秒为单位。可以是 int 或者 float。默认值是 3 分钟。

`Task.rate_limit`
设置任务类型的速率限制（限制给定时间内可以运行的任务数量）。当设置了速率限制后，已经开始的任务仍然会继续完成，但是任务开始前将等待一些时间。

如果这个属性设置成 `None`，速率限制将不生效。如果设置为整数或者浮点数，它将解释成”没秒任务数”。

速率限制可以以秒、分钟或者小时声明，只要值后面附加 “/s”, “/m”, “/h”。任务将在给定时间内平均分布。

实例：”100/m”（没分钟100个任务）。这将强制同一个任务工作单元启动两个任务的时间间隔为最小 600 毫秒。

默认值如 `task_default_rate_limit` 设置：如果没有声明说明默认情况下任务速率限制被禁用。

注意这里指的是每个任务工作单元的限制，不是全局速率限制。要实现全局速率限制（例如，对一个 API 的每秒请求数限制），你必须限定指定的任务队列。

注意：
如果任务请求带有 ETA，这个属性将被忽略。

`Task.time_limit`
任务的硬性时间限制，以秒为单位。如果没有设置，那么将使用任务工作单元的默认值。

`Task.soft_time_limit`
任务的软性时间限制。如果没有设置，那么将使用任务工作单元的默认值。

`Task.ignore_result`
不存储任务状态。注意这意味着你不能使用 `AsyncResult` 来检测任务是否完成，或者获取任务返回值。

`Task.store_errors_even_if_ignored`
如果设置为 `True`，即使任务被设置成忽略结果，错误也会也存储记录

`Task.serializer`
表示默认使用的序列化方法的一个字符串。默认值是 `task_serializer` 设置。可以是 `pickle,json,yaml` 或者任意通过 `kombu.serialization.registry` 注册过的自定义序列化方法。

请查看序列化器这一节获取更多的信息。

`Task.compression`
表示默认压缩模式的一个字符串。

默认值如 `task_compression` 的设置值。可以是 `gzip, bzip2`，或者任意通过 `kombu.compression` 注册过的自定义压缩模式。

请查看压缩这一节获取更多的信息。

`Task.backend`
任务的结果后端存储。`celery.backends` 中的一个后端存储类的实例。默认是 `app.backend`，由 `result_backend` 定义。

`Task.acks_late`
如果设置为 `True`，任务消息将会在任务执行完成后确认，而不是刚开始时（默认行为）。

注意：由于任务工作单元可能在任务执行期间崩溃，所以任务可能会被执行多次。因此，需要确保任务是幂等的。

全局默认设置值可以被 `task_acks_late` 设置覆盖。

`Task.track_started`
当设置为 `True`，如果任务开始被一个工作单元执行，任务将报告它的状态为 “started”。默认值是 `False`，因为通常的行为是不报告到那种粒度级别。任务状态可以是 `pending, finished, waiting to be retried`。对于长时间运行的任务，如果需要知道任务的运行状态，”started” 状态会很有用。

工作执行单元的主机名和进程 id 会记录在任务状态的元信息中（即：`result.info['pid']`）

全局的默认值会被 `task_track_started` 设置值覆盖。

另见：任务的 API 引用文档。

## 状态

------

Celery 可以追踪任务的当前状态。状态信息包含成功执行的任务的结果值以及执行失败的任务的异常和堆栈回溯信息。

有几个可选的存储后端，他们各有优缺点。（见存储后端这一节）

在一个任务的生命周期中可以经历几个可能的状态，每个状态附加有一些元数据。当任务转变到一个新的状态，它以前的状态将被忘记，但是有一些转变是可以被推演到的，（即如果一个任务当前的状态是 `FAILED`， 那么它可定在某个时刻已经先转变成了 `STARTED` 状态）。

还有一些状态的集合，如 `FAILURE_STATES` 的集合，以及 `READY_STATE` 的集合。

客户端通过这些状态集的关系来确定异常是否需要重新抛出（`PROPAGATE_STATES`），或者状态是否能被缓存（如果任务已经 `ready`， 那么能被缓存）。

你还可以自定义任务状态。

## 结果存储后端

------

如果你需要跟踪任务状态或者需要任务返回值，那么 Celery 必须存储或者发送状态到他可以重新获取到的地方。有一些内建的存储后端可供选择： `SQLAlchemy/Django ORM， memcached, RabbitMQ/QPid(rpc), 以及 Redis` - 或者你也可以定义自己的存储后端。

没有一个存储后端使用所有的情况。你应该了解么个存储后端的优缺点，并选择最适合你需求的存储后端。

另见：任务结构存储后端设置

### RPC 存储后端（RabbitMQ/QPid）

------

RPC 结果存储后端（rpc://）比较特殊，他并不真正存储状态，而是将状态作为消息发送。这点区别很重要，因为它意味着结果只能被获取一次，并且只能被初始化该任务的客户端获取。两个不同的进程不能等待同一个结果。

即使有这个限制，如果你需要实时获取任务状态，它仍然是非常棒的一个选择。使用消息意味着客户端不需要主动去拉去状态。

消息默认是短暂的（非持久化），所以，如果消息中间件重新启动，结果值将不复存在。你可以通过 `result_persistent` 配置结果后端发送持久消息。

### 数据库存储后端

------

将状态存储到数据库在很多情况下会很方便，特别是对于已经含有数据库的网络应用，但是它也有一些不足。

- 向数据库询问新的状态的耗费很大，因此你应该增加调用`result.get()` 这类操作的时间间隔
- 一些使用默认事务隔离级别的数据库不合适轮询表的变动

在 MySQL 中，默认的事务隔离级别是 `REPEATABLE-READ`：意味着一个事务除非已经提交，否则不能看到其他事务做的更改。

建议更改为 `READ-COMMITED` 事务隔离级别。

### 内建状态

------

- PENGDING
  任务等待被执行或者状态未知。任何不知道的任务 id 都被认为在 pending 状态。
- STARTED
  任务已经开始。默认不记录此状态，如果要启用请查看 `app.Task.trace_started`。

meta-data: 执行当前任务的工作单元的进程 ID 和主机名。

- SUCCESS
  任务已经被成功执行。

meta-data: 结果包含任务的返回值
propagates: 是
ready: 是

-FAILURE
任务执行失败

meta-data: 结果包含抛出的异常，以及异常抛出时的堆栈回溯信息。
propagates: 是

-RETRY
任务被重试

meta-data: 结果包含导致重试的异常，以及异常抛出时的堆栈回溯信息。
propagates: 是

-REVOKED
任务被取消

propagates: 是

### 自定义状态

------

你可以自定义自己的状态，只需要提供一个唯一的状态名称。状态名称通常是大写的字符串。作为示例你可以查看下 `abortable_tasks`，它定义了一个 `ABORTED` 状态。

使用 `update_state()` 可以更新任务的状态：

```
@app.task(bind=True)
def upload_files(self, filenames):
    for i, file in enumerate(filenames):
        if not self.request.called_directly:
            self.update_state(state='PROGRESS',
                meta={'current': i, 'total': len(filenames)})123456
```

这里创建的了一个 `PROGRESS` 状态，它告诉应用这个任务正在进行中，并且它将 `current` 和 `total` 作为它的状态元信息。这可以用来创建任务进度条。

### 创建可被 pickle 序列化的异常

------

一个很少有人注意的python事实是异常定义必须符合一些简单规则使得它能被 `pickle` 模块序列化。

当使用 `pickle` 作为序列化器时，如果任务抛出的异常不能被 `pickle` 序列化就不能正常工作。

为了确保异常是可以被 `pickle` 模块序列化的，你必须将异常初始化时的原始参数赋值给它的 `.args` 属性。确保这点最简单的方式是让异常调用 `Exception.__init__`。

下面我们看一些示例，有些是正确，有些是错误：

```
# OK:
class HttpError(Exception):
    pass

# BAD:
class HttpError(Exception):

    def __init__(self, status_code):
        self.status_code = status_code

# OK:
class HttpError(Exception):

    def __init__(self, status_code):
        self.status_code = status_code
        Exception.__init__(self, status_code)  # <-- REQUIRED12345678910111213141516
```

所以规则就是： 对于支持自定义参数 `*args` 的异常， `Exception.__init__(self, *args)` 必须被调用。

对于关键字参数没有特殊的支持，所以如果你想在异常反序列化时保留关键字参数，你必须将他们作为常规的参数传递。

```
class HttpError(Exception):

    def __init__(self, status_code, headers=None, body=None):
        self.status_code = status_code
        self.headers = headers
        self.body = body

        super(HttpError, self).__init__(status_code, headers, body)12345678
```

## Semipredicates

------

任务工作单元将任务包装在一个跟踪函数中以记录任务的最终状态。有一些异常可以用来发送信号给这个跟踪函数以改变它处理任务返回值的方式。

### Ignore

------

任务可以抛出 `Ignore` 异常强制使任务工作单元忽略这个任务。这意味着这个任务的任何状态都不会被保存，但是任务消息仍然被确认（从任务队列中删除）。

这可以被用来实现自定义的类似任务取消的功能，或者手动存储任务结果。

在 redis 中保存取消的任务的示例：

```
from celery.exceptions import Ignore

@app.task(bind=True)
def some_task(self):
    if redis.ismember('tasks.revoked', self.request.id):
        raise Ignore()123456
```

手动存储结果的示例：

```
from celery import states
from celery.exceptions import Ignore

@app.task(bind=True)
def get_tweets(self, user):
    timeline = twitter.get_timeline(user)
    if not self.request.called_directly:
        self.update_state(state=states.SUCCESS, meta=timeline)
    raise Ignore()123456789
```

### Reject

------

任务可以使用 `AMQP` 的`basic_reject` 方法抛出 `Reject` 异常来拒绝任务消息。如果 `Task.acks_late` 启用的话，拒绝消息将不生效。

拒绝一个消息与确认一个消息有同样的效果，但是一个消息中间件可能实现一些附加的功能。例如 RabbitMQ 支持 `Dead Letter Exchanges` 的概念，被拒绝的消息会递送到配置的死信队列。

拒绝可以用来重新入队任务消息，但是使用的时间要小心因为这很容易导致无限消息循环。

当任务导致内存溢出时使用拒绝的示例：

```
import errno
from celery.exceptions import Reject

@app.task(bind=True, acks_late=True)
def render_scene(self, path):
    file = get_file(path)
    try:
        renderer.render_scene(file)

    # if the file is too big to fit in memory
    # we reject it so that it's redelivered to the dead letter exchange
    # and we can manually inspect the situation.
    except MemoryError as exc:
        raise Reject(exc, requeue=False)
    except OSError as exc:
        if exc.errno == errno.ENOMEM:
            raise Reject(exc, requeue=False)

    # For any other error we retry after 10 seconds.
    except Exception as exc:
        raise self.retry(exc, countdown=10)123456789101112131415161718192021
```

任务消息重新入队的示例：

```
from celery.exceptions import Reject

@app.task(bind=True, acks_late=True)
def requeues(self):
    if not self.request.delivery_info['redelivered']:
        raise Reject('no reason', requeue=True)
    print('received two times')1234567
```

如果想了解更多的细节请查看消息中间件的 `basic_reject` 方法。

### Retry

------

`Retry` 异常是被 `Task.retry` 方法抛出用来告诉工作单元当前任务将被重试。

## 自定义任务类

------

所有的任务都继承自 `app.Task` 类。该类的 `run()` 方法就是任务的函数体。

如以下示例：

```
@app.task
def add(x, y):
    return x + y123
```

在 celery 内部将做如下包装：

```
class _AddTask(app.Task):

    def run(self, x, y):
        return x + y
add = app.tasks[_AddTask.name]12345
```

### 初始化

------

任务实例不是对每个请求都初始化一个，而是在任务注册表中作为一个全局实例。

这意味着 `__init__` 构造函数只会在每个进程调用一次，并且任务类语义上类似于 `Actor`。

假设你如下一个任务：

```
from celery import Task

class NaiveAuthenticateServer(Task):

    def __init__(self):
        self.users = {'george': 'password'}

    def run(self, username, password):
        try:
            return self.users[username] == password
        except KeyError:
            return False123456789101112
```

并且你将每个请求路由到同一个进程，此时它将在请求之间维护状态。

这也可以用来缓存资源，例如，下面这个任务基类缓存了一个数据库链接：

```
from celery import Task

class DatabaseTask(Task):
    _db = None

    @property
    def db(self):
        if self._db is None:
            self._db = Database.connect()
        return self._db12345678910
```

它可以这样加入到任务中：

```
@app.task(base=DatabaseTask)
def process_rows():
    for row in process_rows.db.table.all():
        process_row(row)1234
```

`process_rows` 任务的 `db` 属性在同一个进程中将总是保持相同。

### Handler

------

- `after_return(self, status, retval, task_id, args, kwargs, einfo)`
  任务返回后调用的处理函数。

参数：
\- status - 当前任务状态
\- retval - 任务返回值/异常
\- task_id - 任务的唯一ID
\- args - 任务的初始参数
\- kwargs - 任务的初始关键字参数

关键字参数：
\- einfo - `ExceptionInfo` 实例，包含异常堆栈回溯信息（如果存在）

这个处理函数的返回值被忽略。

- `on_failure(self, exc, task_id, args, kwargs, einfo)`
  当任务失败时调用。

参数：
\- exc - 任务抛出的异常
\- task_id - 失败任务的唯一ID
\- args - 失败任务的原始参数
\- kwargs - 失败任务的原始关键字参数

关键字参数：
\- einfo - `ExceptionInfo` 实例，包含异常堆栈回溯信息

这个处理函数的返回值被忽略

- `on_retry(self, exc, task_id, args, kwargs, einfo)`
  任务重试时由工作单元调用

参数：
\- exc - 发送给 `retry()` 函数的异常
\- task_id - 被重试任务的唯一 ID
\- args - 被重试任务的原始参数
\- kwargs - 被重试任务的原始关键字参数

关键字参数：
\- einfo - `ExceptionInfo` 实例，包含异常堆栈回溯信息

这个处理函数的返回值被忽略

- `on_success(self, retval, task_id, args, kwargs)`
  任务成功执行完由工作单元调用的处理函数。

参数：
\- retval - 任务的返回值
\- task_id - 任务的唯一 ID
\- args - 任务的原始参数
\- kwargs - 任务的原始关键字参数

这个处理函数的返回值被忽略。

## How it works

------

这里是一些技术细节。这部分内容不是必须知道的，但是你可能会感兴趣。

所有定义的任务都可以从任务注册表中列出来。任务注册表包含所有任务名称到对应任务类的映射。你可以通过任务注册表查看：

```
>>> from proj.celery import app
>>> app.tasks
{'celery.chord_unlock':
    <@task: celery.chord_unlock>,
 'celery.backend_cleanup':
    <@task: celery.backend_cleanup>,
 'celery.chord':
    <@task: celery.chord>}12345678
```

这是 celery 内建的一些任务。注意任务只有在定义他们的模块被导入时才会被注册。

默认的加载器会导入 `imports` 设置中的所有模块。

`app.task()` 装饰器在你的应用任务注册表中注册你的任务。

但任务被发送，实际的任务代码并不随之发送，只携带当前任务的名称。当工作单元接收到任务，它会根据任务名称从任务注册表中找到实际要执行的代码。

这意味着你应该总是保持工作单元和客户端代码的一致性。这是个缺陷，但是另外的解决方案是一个需要被解决的技术挑战。

## 提示与最佳实践

------

### 忽略不想要的结果

------

如果你不在意任务的返回结果，可以设置 `ignore_result` 选项，因为存储结果耗费时间和资源。

```
@app.task(ignore_result=True)
def mytask():
    something()123
```

可以通过 `task_ignore_result` 设置全局忽略任务结果。

### 更多优化提示

------

可以在优化指南一节找到附加的优化建议。

### 避免启动同步子任务

------

让一个任务等待另外一个任务的返回结果是很低效的，并且如果工作单元池被耗尽的话这将会导致死锁。

尽量让你的任务异步，例如使用回调函数：
Bad:

```
@app.task
def update_page_info(url):
    page = fetch_page.delay(url).get()
    info = parse_page.delay(url, page).get()
    store_page_info.delay(url, info)

@app.task
def fetch_page(url):
    return myhttplib.get(url)

@app.task
def parse_page(url, page):
    return myparser.parse_document(page)

@app.task
def store_page_info(url, info):
    return PageInfo.objects.create(url, info)1234567891011121314151617
```

Good:

```
def update_page_info(url):
    # fetch_page -> parse_page -> store_page
    chain = fetch_page.s(url) | parse_page.s() | store_page_info.s(url)
    chain()

@app.task()
def fetch_page(url):
    return myhttplib.get(url)

@app.task()
def parse_page(page):
    return myparser.parse_document(page)

@app.task(ignore_result=True)
def store_page_info(info, url):
    PageInfo.objects.create(url=url, info=info)12345678910111213141516
```

这里，我们将不同的任务签名链接起来创建一个任务链。你可以通过 `Canvas: Designing Work-flows` 这一节了解任务链和其他有用的方案。

默认情况下，celery 不会让你在一个任务里同步执行其他任务，很少或者极端情况下，你可能不得不这么做。告警：不建议同步执行子任务！

```
@app.task
def update_page_info(url):
    page = fetch_page.delay(url).get(disable_sync_subtasks=False)
    info = parse_page.delay(url, page).get(disable_sync_subtasks=False)
    store_page_info.delay(url, info)

@app.task
def fetch_page(url):
    return myhttplib.get(url)

@app.task
def parse_page(url, page):
    return myparser.parse_document(page)

@app.task
def store_page_info(url, info):
    return PageInfo.objects.create(url, info)1234567891011121314151617
```

## 性能与策略

------

- 粒度
  任务粒度是每个子任务需要的总计算量。通常情况下，将任务分解成多个小任务比保持少量长时间任务要更好。

任务越小你可以并行处理的任务就越多，而且不会由于任务长时间运行妨碍工作单元处理其他等待的任务。

但是，执行任何任务都是由花销的。需要发送任务消息，数据可能不是本地的，等等。所以如果任务的粒度太细，增加的耗费可能会大于这样做带来的好处。

另见：`Art of Concurrency` 这本书有一节专门讲述任务粒度这个主题。

[AOC1] Breshears, Clay. Section 2.2.1, “The Art of Concurrency”. O’Reilly Media, Inc. May 15, 2009. ISBN-13 978-0-596-52153-0.

### Data locality

------

处理任务的工作单元应该离待处理的数据越近越好。最好是在内存中有一份拷贝，最坏的情况是从其他地方全量传输。

如果数据距离很远，你可以在特定区域运行另外一个任务，或者如果不可能 - 缓存常用的数据，又或者预先加载将要使用的数据。

最简单的在工作单元之间共享数据的方法是使用一个分布式缓存系统，例如 memcached。

另见：Jim Gray 写的 `Distributed Computing Economics` 这篇论文对数据本地化有详细的介绍。

### 状态

------

因为 celery 是一个分布式系统，你不知道任务在哪个进程或者哪台服务器上运行。你甚至不知道任务是否会在有限的时间里完成。

古代谚语告诉我们”断言世界是任务的责任”。它的意思是发起任务后世界观可以已经改变，所以任务负责确保世界是它应该保持的样子；如果你有一个任务是对一个搜索引擎重新编索引，并且搜索引擎应该最多每隔5分钟重新编索引，那么应该是任务的职责来断言这一点，而不是调用者。

另外一个例子是 Django 的模型对象。他们不应该作为参数传递给任务。几乎总是在任务运行时从数据库获取对象是最好的，因为老的数据会导致竞态条件。

假象有这样一个场景，你有一篇文章，以及自动展开文章中缩写的任务：

```
class Article(models.Model):
    title = models.CharField()
    body = models.TextField()

@app.task
def expand_abbreviations(article):
    article.body.replace('MyCorp', 'My Corporation')
    article.save()12345678
```

首先，作者创建一篇文章并保存，这时作者点击一个按钮初始化一个缩写展开任务：

```
>>> article = Article.objects.get(id=102)
>>> expand_abbreviations.delay(article)12
```

现在，队列非常忙，所以任务在2分钟内都不会运行。与此同时，另一个作者修改了这篇文章，当这个任务最终运行，因为老版本的文章作为参数传递给了这个任务，所以这篇文章会回滚到老的版本。

修复这个竞态条件很简单，只要参数传递文章的 id 即可，此时可以在任务中重新获取这篇文章：

```
@app.task
def expand_abbreviations(article_id):
    article = Article.objects.get(id=article_id)
    article.body.replace('MyCorp', 'My Corporation')
    article.save()12345
>>> expand_abbreviations.delay(article_id)1
```

因为发送打消息可能耗费资源，所以这样修改甚至可能带来性能的提升。

### 数据库事物

------

我们看另外一个例子：

```
from django.db import transaction

@transaction.commit_on_success
def create_article(request):
    article = Article.objects.create()
    expand_abbreviations.delay(article.pk)123456
```

这是在数据库中创建一个文章对象的 Django 视图，此时传递主键给任务。它使用 `commit_on_success` 装饰器，当视图返回时该事务会被提交，当视图抛出异常时会进行回滚。

如果在事务提交之前任务已经开始执行会产生一个竞态条件；数据库对象还不存在。

解决方案是使用 `on_commit` 回调函数来在所有事务提交成功后启动任务。

```
from django.db.transaction import on_commit

def create_article(request):
    article = Article.objects.create()
    on_commit(lambda: expand_abbreviations.delay(article.pk))12345
```

注意：
`on_commit` 函数只在 Django 1.9 以上版本才可用，如果你使用以前的版本，那么可以使用 `django-transaction-hooks` 库添加相关支持。

## 例子

------

让我们看一个真实的例子：博客中用户提交的评论要做垃圾过滤。当评论创建后，垃圾过滤任务在后台运行，所以用户无需等待它完成。

我有一个Django博客应用，允许访客对发表的博客进行评论。这里描述下这个应用的部分模型/视图以及任务。

blog/models.py
评论模型如下：

```
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Comment(models.Model):
    name = models.CharField(_('name'), max_length=64)
    email_address = models.EmailField(_('email address'))
    homepage = models.URLField(_('home page'),
                               blank=True, verify_exists=False)
    comment = models.TextField(_('comment'))
    pub_date = models.DateTimeField(_('Published date'),
                                    editable=False, auto_add_now=True)
    is_spam = models.BooleanField(_('spam?'),
                                  default=False, editable=False)

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')123456789101112131415161718
```

在评论发表的视图中，我首先将评论写到数据库，然后在后台发起垃圾过滤任务。

blog/views.py

```
from django import forms
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.shortcuts import get_object_or_404, render_to_response

from blog import tasks
from blog.models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment


def add_comment(request, slug, template_name='comments/create.html'):
    post = get_object_or_404(Entry, slug=slug)
    remote_addr = request.META.get('REMOTE_ADDR')

    if request.method == 'post':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save()
            # Check spam asynchronously.
            tasks.spam_filter.delay(comment_id=comment.id,
                                    remote_addr=remote_addr)
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = CommentForm()

    context = RequestContext(request, {'form': form})
    return render_to_response(template_name, context_instance=context)1234567891011121314151617181920212223242526272829303132
```

过滤垃圾评论我使用 `Akismet`，这个服务在开源博客平台 Wordpress 中用来过滤垃圾评论。`Akismet` 对个人使用是免费的，但是对于商业用途需要收费。你需要先注册并获取到 API 秘钥。

发送 API 请求给 `Akismet` 我使用 `akismet.py` 这个库，它是由 Michael Foord 写的。

blog/tasks.py

```
from celery import Celery

from akismet import Akismet

from django.core.exceptions import ImproperlyConfigured
from django.contrib.sites.models import Site

from blog.models import Comment


app = Celery(broker='amqp://')


@app.task
def spam_filter(comment_id, remote_addr=None):
    logger = spam_filter.get_logger()
    logger.info('Running spam filter for comment %s', comment_id)

    comment = Comment.objects.get(pk=comment_id)
    current_domain = Site.objects.get_current().domain
    akismet = Akismet(settings.AKISMET_KEY, 'http://{0}'.format(domain))
    if not akismet.verify_key():
        raise ImproperlyConfigured('Invalid AKISMET_KEY')


    is_spam = akismet.comment_check(user_ip=remote_addr,
                        comment_content=comment.comment,
                        comment_author=comment.name,
                        comment_author_email=comment.email_address)
    if is_spam:
        comment.is_spam = True
        comment.save()

    return is_spam
12345678910111213141516171819202122232425262728293031323334
```

- [点赞 2](javascript:;)
- [收藏](javascript:;)
- [分享](javascript:;)
- 

[![img](https://profile.csdnimg.cn/7/F/F/3_u013148156)![img](https://g.csdnimg.cn/static/user-reg-year/2x/6.png)](https://blog.csdn.net/u013148156)

[libing_thinking](https://blog.csdn.net/u013148156)