# Celery-4.1 用户指南: Application

## Application

Celery 库在使用之前必须初始化，一个 Celery 实例被称为一个应用（或者缩写 app）。

Celery 应用是线程安全的，所以多个不同配置、不同组件、不同任务的应用可以在同一个进程空间里共存。

下面创建一个 celery 应用：

```python
>>> from celery import Celery
>>> app = Celery()
>>> app
<Celery __main__:0x100469fd0>
```

最后一行显示的是 celery 应用的文本表示： 包含应用类的名称（Celery），当前主模块的名称（**main**），以及应用对象的内存地址（0x100469fd0）。

## Main Name

上述文本表示中只有一部分是重要的，那就是主模块名称。下面分析下它为何重要。

当你发送一个消息给 Celery，消息中不会包含任何源码，而只有你想要执行的任务的名称。这就好像因特网上的域名映射原理一般：每个执行单元维护着一个任务名称到实际任务函数的映射，这个映射被称为`任务注册表`。

当你定义一个任务，这个任务就会被添加到本地注册表：

```python
>>> @app.task
... def add(x, y):
...     return x + y

>>> add
<@task: __main__.add>

>>> add.name
__main__.add

>>> app.tasks['__main__.add']
<@task: __main__.add>
```

现在，你又看到显示 `__main__` 模块名称；当 Celery 不能探查到这个任务函数属于哪个模块时，它将使用主模块名称来产生任务名称的前缀。

这在有些情况下会产生问题：

1. 定义任务的主模块作为一个程序运行。

2. 应用在python交互终端创建。

例如下面程序，定义任务的模块还调用 `app.worker_main()` 来启动一个工作单元：

**tasks.py**

```python
from celery import Celery
app = Celery()

@app.task
def add(x, y):
    return x + y


if __name__ == '__main__':
    app.worker_main()
```

当这个模块运行，任务将以前缀 `__main__` 命名，但是当该模块被其他进程引入来运行一个任务，这个任务的名称将以前缀 `tasks` 命名（即这个模块的真实名称）。

```python
>>> from tasks import add
>>> add.name
tasks.add
```

你可以给主模块声明另外一个名称：

```python
>>> app = Celery('tasks')
>>> app.main
'tasks'

>>> @app.task
... def add(x, y):
...     return x + y

>>> add.name
tasks.add
```

## 配置

你可以设置一些选项来改变 Celery 的工作方式。这些选项可以直接在 app 实例上进行设置，或者也可以使用一个指定的配置模块。

配置使用 `app.conf` 变量保存：

```python
>>> app.conf.timezone
'Europe/London'
```

你可以直接设置配置值：

```python
>>> app.conf.enable_utc = True
```

或者使用 `update` 方法同时更新多个配置项。

```python
>>> app.conf.update(
...     enable_utc=True,
...     timezone='Europe/London',
... )
```

实际的配置对象由多个字典决定，配置项按以下顺序查询：

1. 运行时的配置修改

2. 配置模块（如果声明）

3. 默认配置（celery.app.defaults）

你还可以使用 `app.add_defaults()` 方法添加新的默认配置源。

### config_from_object

`app.config_from_object()` 方法从一个配置对象加载配置。

它可以是一个配置模块，或者任意包含配置属性的对象。

注意任何前面设置的配置在调用 `config_from_object` 方法后都将被重置。如果你想设置附加的配置应该在调用这个方法之后。

示例1： 使用模块名

`app.config_from_object()` 方法的参数可以是一个 python 模块的全限定名称，或者一个 python 属性名，例如：`celeryconfig`，`myproj.config.celery`，或者 `myproj.config:CeleryConfig`

```python
from celery import Celery

app = Celery()
app.config_from_object('celeryconfig')
```

celeryconfig 模块内容如下形式：

**celeryconfig.py**

```python
enable_utc = True
timezone = 'Europe/London'
```

只要 `import celeryconfig` 能正常运行，应用实例就能加载它。

示例2：传递一个模块对象

你还可以传递一个已经加载的模块对象，但是不作为常规建议。

提示：建议使用模块名的方式加载，因为这种情况下当 prefork 池使用时，配置模块不必序列化。如果遇到配置问题或者序列化错误，可以尝试使用模块名的方式加载配置。

```python
import celeryconfig

from celery import Celery

app = Celery()
app.config_from_object(celeryconfig)
```

示例3：使用配置类/对象

```python
from celery import Celery

app = Celery()

class Config:
    enable_utc = True
    timezone = 'Europe/London'

app.config_from_object(Config)
# or using the fully qualified name of the object:
# app.config_from_object('module:Config')
```

### config_from_envvar

`app.config_from_envvar()` 从环境变量中获取配置模块名称。

例如，从环境变量 CELERY_CONFIG_MODULE 所声明的模块加载配置：

```python
import os
from celery import Celery

#: Set default configuration module name
os.environ.setdefault('CELERY_CONFIG_MODULE', 'celeryconfig')

app = Celery()
app.config_from_envvar('CELERY_CONFIG_MODULE')
```

你可以通过环境变量声明要使用的模块：

```bash
$ CELERY_CONFIG_MODULE="celeryconfig.prod" celery worker -l info
```

### 敏感配置

如果你想打印配置信息，作为调试信息或者类似，你也许不想暴露密码和API秘钥这类信息。

Celery 提供了一些有用的工具函数来展示这些配置信息，其中一个是 `humanize()` 函数：

```python
>>> app.conf.humanize(with_defaults=False, censored=True)
```

请注意 Celery 不会移除所有的敏感信息，因为它只是仅仅使用一个正则表达式来匹配配置项键名。如果你添加包含敏感信息的定制化配置，你应该使用 celery 能识别为敏感信息的键名。

如果一个配置项键名包含以下字符串，它将被看作是敏感的：
`API，TOKEN，KEY，SECRET，PASS，SIGNATURE，DATABASE`

## 延迟加载

一个应用实例是延迟加载的，意味着它只有在实际调用的时候才会被求值。

创建一个celery 实例只会做如下事情：

1. 创建一个用于事件的逻辑时钟实例

2. 创建一个任务注册表

3. 将自己设置为当前应用实例（如果 `set_as_current` 参数被禁用将不会做此设置）

4. 调用 `app.on_init()` 回调函数(默认不做任何事情)

`app.task()` 装饰器在任务定义时不会创建任务，而是延迟任务的创建到任务使用时，或者应用被终止时。

下面这个例子说明了直到你使用任务时或者访问任务对象的属性时（这里是 `repr()`）任务才会被创建:

```python
>>> @app.task
>>> def add(x, y):
...     return x + y

>>> type(add)
<class 'celery.local.PromiseProxy'>

>>> add.__evaluated__()
False

>>> add  # causes repr(add) to happen
<@task: __main__.add>

>>> add.__evaluated__()
True
```

应用的终止有两种情况，显示调用 `app.finalize()` 终止，或者通过访问 `app.tasks` 属性隐示终止。

终止应用对象将会执行：

1. 应用间必须共享的任务的拷贝，任务默认是被共享的，但是如果任务装饰器的共享参数被设置为禁用时任务会为被绑定的应用所私有。

2. 对所有未求值的任务求值

3. 确认所有任务都绑定到当前应用实例，任务绑定到了应用实例，所以可以读取配置的默认值。

note：

**默认应用实例**

celery 并不是一开始有应用实例这个概念，最早只有一个模块级别的 API，为了向后兼容老的 API，这个模块级别 API 会保留直到 celery 5.0 发布。

celery 会创建一个特殊的应用实例 - 默认应用实例，如果没有自定义的应用实例被初始化，这个默认应用实例将会被启用。

例如，老的任务基类使用了许多兼容特性，其中一些与新的特性不兼容，比如任务方法。

```python
from celery.task import Task  # OLD Task base class.

from celery import Task  # NEW base class.
```

即使你使用老的模块级别的 API，也推荐使用新的基类。

## 打破链式操作

虽然可以依赖于当前设置的应用实例，但是将应用实例作为参数传递给所有需要它的对象仍然是最佳操作实践。

称这种操作为“应用实例链”的原因是因为它依赖所传递的应用实例创建了一个链。

下面这个例子被认为是差的实践：

```python
from celery import current_app

class Scheduler(object):
    def run(self):
        app = current_app
```

应该将 app 作为一个参数传递：

```python
class Scheduler(object):
    def __init__(self, app):
        self.app = app
```

在 celery 内部实现中，使用 `celery.app_or_default()` 函数使得模块级别的 API 也能正常使用。

```python
from celery.app import app_or_default

class Scheduler(object):
    def __init__(self, app=None):
        self.app = app_or_default(app)
```

在开发环境中，可以通过设置 `CELERY_TRACE_APP` 环境变量在应用实例链被打破时抛出一个异常：

```bash
$ CELERY_TRACE_APP=1 celery worker -l info
```

note：

**API 的演化**

Celery 项目从开始创建到现在的七年多时间里已经改变了很多。例如，最开始可以使用任何一个可调用对象作为一个任务：

```python
def hello(to):
    return 'hello {0}'.format(to)

>>> from celery.execute import apply_async
>>> apply_async(hello, ('world!',))
```

可以创建一个任务类，设置特定属性，或者覆盖其他行为

```python
from celery.task import Task
from celery.registry import tasks

class Hello(Task):
    queue = 'hipri'

    def run(self, to):
        return 'hello {0}'.format(to)

tasks.register(Hello)

>>> Hello.delay('world!')
```

后来，开发者觉得传递任意可调用对象是反模式，因为它使得很难使用除了 `pickle` 之外的序列化方案，因此这个特性在 2.0 就被踢除了，取而代之的是任务装饰器：

```python
from celery.task import task

@task(queue='hipri')
def hello(to):
    return 'hello {0}'.format(to)
```

## 抽象任务

所有使用 task() 装饰器创建的任务都会继承应用的基础 `Task` 类。

你可以使用装饰器的 base 参数给任务声明一个不同的基类：

```python
@app.task(base=OtherTask)
def add(x, y):
    return x + y
```

创建一个自定义的任务类，你应该继承这个中性类：`celery.Task`

```python
from celery import Task

class DebugTask(Task):
    def __call__(self, *args, **kwargs):
        print('TASK STARTING: {0.name}[{0.request.id}]'.format(self))
        return super(DebugTask, self).__call__(*args, **kwargs)
```

提示：
如果你覆盖了任务的 `__call__` 方法，那么非常重要的一点是你还需要调用父类的方法使得在任务被直接调用时基类call方法能设置好默认请求。

这个中性类比较特殊，因为它不会绑定到任意特殊应用实例。一旦任务绑定到一个应用实例，它将读取应用的配置信息来设置默认值等等。

使用一个基类，你需要使用 `app.task()` 装饰器创建一个任务：

```python
@app.task(base=DebugTask)
def add(x, y):
    return x + y
```

还可以通过修改 `app.Task` 属性来修改一个应用实例的默认基类：

```python
>>> from celery import Celery, Task

>>> app = Celery()

>>> class MyBaseTask(Task):
...     queue = 'hipri'

>>> app.Task = MyBaseTask
>>> app.Task
<unbound MyBaseTask>

>>> @app.task
... def add(x, y):
...     return x + y

>>> add
<@task: __main__.add>

>>> add.__class__.mro()
[<class add of <Celery __main__:0x1012b4410>>, <unbound MyBaseTask>, <unbound Task>, <type 'object'>]
```

[参考](https://blog.csdn.net/u013148156/article/details/78541171)
