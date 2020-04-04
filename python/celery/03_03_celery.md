# Celery 学习笔记（3）任务和任务执行

## 任务

任务是 Celery 里不可缺少的一部分，它可以是任何可调用对象。每一个任务通过一个唯一的名称进行标识， worker 通过这个名称对任务进行检索。任务可以通过 app.task 装饰器进行注册，需要注意的一点是，当函数有多个装饰器时，为了保证 Celery 的正常运行，app.task 装饰器需要在最外层。

```python
# 装饰器示例
@app.task
@decorator2
@decorator1
def add(x, y):
    return x + y
```

同时，app.task 装饰器也接受多种参数对任务进行配置。例如，可以通过 name 显式的设定任务的名字，serializer 设定任务的序列化方式。

```python
@app.task(name='task.add', serializer='json')
def add(x, y):
    return x + y
```

还有一个比较重要的是 bind 参数，当设置了 bind 参数，则会为这个任务绑定一个 Task 实例，通过第一个 self 参数传入，可以通过这个 self 参数访问到 Task 对象的所有属性。

```python
logger = get_task_logger(__name__)

@task(bind=True)
def add(self, x, y):
    logger.info(self.request.id)
```

## 任务执行

前面介绍到，可以通过 delay 使用 Celery 执行一个任务，实际上 delay 是 apply_async 的一个快捷方式，而相较于 delay，apply_aysnc 支持对于任务执行过程的更精确的控制。比如下面这个例子的 countdown 参数表示在接收到任务 10 秒后开始执行。

```python
>>> add.apply_async((1, 2), countdown=10)
>>> <AsyncResult: 16af1a5f-b546-4f7c-b113-0e861c175144>
```

函数原型如下：

```python
task.apply_async(args[, kwargs[, …]])
```

其中 args 和 kwargs 分别是 task 接收的参数，当然它也接受额外的参数对任务进行控制。除此 countdown 之外，可以通过 expires 设置任务过期时间，当 worker 接收到一个过期任务，它的状态会标记为 REVOKE；也可以通过设置 retry=True，在任务执行失败时进行重试。

对于未注册的函数，可以调用 Task 对象的 send_task 方法向任务队列添加一个任务，通过 name 参数设定任务名进行标识，和 apply_aysnc 一样返回一个 AsyncResult 对象。

所以总结一下，在 Celery 中执行任务的方法一共有三种：

1. delay， 用来进行最简单便捷的任务执行

2. apply_async， 对于任务的执行附加额外的参数，对任务进行控制

3. app.send_task， 可以执行未在 Celery 中进行注册的任务

## 链式执行

在 Celery 中，可以通过调用 `apply_async` 时传递 `link` 参数设置任务执行完成后的后续任务，当然这个任务也会由 Celery 交给 worker 执行。这里有一点需要注意，任务执行的返回值将会以参数的形式传递给这个后续任务，而这里的后续任务需要是一个 signature 对象（关于 signature 对象在下一节详细的介绍，这里只需要知道 `add.s(1)` 语句将会创建一个 signature 对象，功能上类似于偏函数 functools.patial(add，1））。下面的例子等价于 `add(add(1, 2), 3)`

```python
>>> add.apply_async((1, 2), link=add.s(3))
```

同样的对于失败的任务，可以用 `linkerr` 参数来指定回调函数。同时 `link` 和 `linkerr` 也支持将列表作为参数，任务执行之后列表中的任务都会被加入队列中继续执行。使用 `link` 和 `linkerr` 可以更好的规划任务流程，在下一节可以看到使用 chain 函数可以更好的实现这个功能。

## 自定义 Task

可以通过继承 `celery.Task` 的方式来定义自己的 Task 类，并为你的 Task 类添加额外的功能。

```python
import celery

class MyTask(celery.Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))

@task(base=MyTask)
def add(x, y):
    raise KeyError()
```

和上面的 `on_failure` 类似，Task 对象中有一系列方法来控制任务的执行，也可以通过重写这些方法来为任务添加回调函数，通过 base 参数来指定任务的基类。

- `after_return`：在任务执行返回后交给 worker 执行

- `on_failure`：在任务执行失败后交给 worker 执行

- `on_retry`：在任务进行重试是交给 worker 执行

- `on_success`：在任务执行成功后交给 worker 执行

```python
import celery

class CountTask(celery.Task):
    count = 0
    def on_success(self, retval, task_id, args, kwargs):
        self.count += 1
        return self.count

@app.task(base=CountTask)
def send():
    if send.count <= 10:
        return 'Hello World'
    else:
        return 'end'
```

除此之外还可以通过自定义的 Task 类在多个任务间共享状态，例如可以通过类属性 count 来保存任务的成功执行次数，在任务中可以直接在函数上调用对应属性来获得 Task 类的属性。

[参考](https://blog.csdn.net/preyta/article/details/54288870)
