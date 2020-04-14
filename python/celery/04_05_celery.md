# Celery-4.1 用户指南: Canvas-设计工作流

## 签名

2.0 版本新特性。

刚刚在 `calling` 这一节中学习了使用 `delay` 方法调用任务，并且通常这就是你所需要的，但是有时候你可能想将一个任务调用的签名传递给另外一个进程或者作为另外一个函数的参数。

任务签名包含了一次任务调用的参数、关键字参数以及执行选项信息，它可以传递给其他函数，甚至序列化后通过网络传输。

- 你使用 `add` 任务的名称创建一个签名，就像这样：

```python
>>> from celery import signature
>>> signature('tasks.add', args=(2, 2), countdown=10)
tasks.add(2, 2)
```

这个任务签名有两个参数：（2，2），并且 `countdown` 执行选项被设置成 10。

- 或者你也可以使用任务的 `signature` 方法创建任务签名：

```python
>>> add.signature((2, 2), countdown=10)
tasks.add(2, 2)
```

- 还有一个使用参数展开的快捷方式：

```python
>>> add.s(2, 2)
tasks.add(2, 2)
```

- 关键字参数也是支持的：

```python
>>> add.s(2, 2, debug=True)
tasks.add(2, 2, debug=True)
```

- 从任何签名实例，你都可以探查它的不同字段：

```python
>>> s = add.signature((2, 2), {'debug': True}, countdown=10)
>>> s.args
(2, 2)
>>> s.kwargs
{'debug': True}
>>> s.options
{'countdown': 10}
```

- 签名支持 “Calling API”，如 `delay`、`apply_async` 等等，包括直接调用（`__call__`）。

直接调用签名会在当前进程中执行任务：

```python
>>> add(2, 2)
4
>>> add.s(2, 2)()
4
```

`delay` 是 `apply_async` 函数的星号参数展开快捷方式：

```python
>>> result = add.delay(2, 2)
>>> result.get()
4
```

`apply_async` 方法与 `app.Task.apply_async()` 方法的参数相同：

```python
>>> add.apply_async(args, kwargs, **options)
>>> add.signature(args, kwargs, **options).apply_async()

>>> add.apply_async((2, 2), countdown=1)
>>> add.signature((2, 2), countdown=1).apply_async()
```

- 使用 `s()` 不能定义执行选项，但是提供了一个链式的 `set` 函数来处理这些：

```python
>>> add.s(2, 2).set(countdown=1)
proj.tasks.add(2, 2)
```

### Partials

使用签名，你可以在工作单元中执行任务：

```python
>>> add.s(2, 2).delay()
>>> add.s(2, 2).apply_async(countdown=1)
```

或者你可以在当前进程中直接调用任务：

```python
>>> add.s(2, 2)()
4
```

通过 `apply_async/delay` 声明额外的参数、关键字参数、执行选项来实现偏函数的功能：

- 任何新加的参数都会前置到签名的当前参数列表

```python
# incomplete signature
>>> partial = add.s(2)
# 4 + 2
>>> partial.delay(4)
# same
>>> partial.apply_async((4,))
```

- 任何新加的关键字参数都会与签名现有的关键字参数合并，优先选择新的关键字参数：

```python
>>> s = add.s(2, 2)
# add(2, 2, debug=True)
>>> s.delay(debug=True)
# same
>>> s.apply_async(kwargs={'debug': True})
```

- 任何新加的执行选项都会与签名的执行选项合并，优先选择新的执行选项：

```python
>>> s = add.signature((2, 2), countdown=10)
# countdown is now 1
>>> s.apply_async(countdown=1)
```

你还可以通过克隆任务来衍生出新任务：

```python
>>> s = add.s(2)
proj.tasks.add(2)

>>> s.clone(args=(4,), kwargs={'debug': True})
proj.tasks.add(4, 2, debug=True)
```

### Immutability

3.0 版本新特性。

便函数注定要和回调函数一起使用，任何链接任务、或者 `chord` 回调函数都会使用父任务的结果作为函数调用参数。有时候，你想声明一个不带任何附加参数的回调函数，此时你可以将签名设置成不可变的。

```python
>>> add.apply_async((2, 2), link=reset_buffers.signature(immutable=True))
```

可以使用 `.si()` 快捷方式创建不可变签名：

```python
>>> add.apply_async((2, 2), link=reset_buffers.si())
```

当任务签名是不可变的时，只有执行选项可以被设置，所以不能以部分参数/关键字参数调用签名。

### Callbacks

3.0 版本新特性。

回调函数可以通过使用 `apply_async` 函数的 `link` 参数添加到任何任务：

```python
add.apply_async((2, 2), link=other_task.s())
```

回调函数只有在任务成功退出才会调用，并且它会将父任务的返回结果作为参数。

如我签名所描述的，你给签名添加的任何参数，都会置于签名本身声明的参数之前！

如果你有如下签名：

```python
>>> sig = add.s(10)
```

那么，`sig.delay(result)` 变成：

```python
>>> add.apply_async(args=(result, 10))
```

现在，我们调用任务 `add`，设置回调函数并使用部分参数：

```python
>>> add.apply_async((2, 2), link=add.s(8))
```

如所预期的，它将首先启动一个任务计算 `2+2`，然后启动另一个任务计算 `4+8`。

## 原语

3.0 版本新特性。

概要

- group 组元语是一个签名，参数是要并发执行的任务的列表

- chain 链元语让我们可以将签名链接起来，使得一个任务调用后执行另外一个任务，本质上形成一个回调链

- chord 弦就像带有一个回调函数的组。弦由一个头部组和弦体组成，而弦体是头部组中所有任务都完成之后应该执行的任务

- map 映射元语就像内建的 map 函数，但是它还创建一个带有参数列表的临时任务。例如，`task.map([1, 2])` 将调用一个任务，参数被按序传给任务，所以结果是：

```python
res = [task(1), task(2)]
```

- starmap  除了参数被展开，其余都和 map 相同。例如，`add.starmap([(2,2), (4,4)])`将会生成如下任务调用：

```python
res = [add(2,2), add(4,4)]
```

- chunks 分块将一个长参数列表分解成，例如：

```python
# 1000 items
>>> items = zip(xrange(1000), xrange(1000))
>>> add.chunks(items, 10)
```

会将 10 个项为一块，分成 100 块，从而产生 100 个任务（每个任务处理 10 个项）

这些元语本身也是签名，所以他们可以任意组合，形成复杂的工组流。

下面是一些例子：

- 简单的链，这是一个简单的链，第一个任务执行完将它的返回结果传递给下一个任务，以此类推。

```python
>>> from celery import chain

>>> # 2 + 2 + 4 + 8
>>> res = chain(add.s(2, 2), add.s(4), add.s(8))()
>>> res.get()
16
```

这还可以使用管道符写：

```python
>>> (add.s(2, 2) | add.s(4) | add.s(8))().get()
16
```

- 不可变签名，签名可以是部分的，所以可以在现有参数基础上添加参数，但是有时候你可能并不想这样，例如你不想要链中前面任务的返回值。

这种情况下，你可以将签名标记为不可变的，则参数不能再改变：

```python
>>> add.signature((2, 2), immutable=True)
```

还有一个快捷方式 `si()`方法，并且这是创建签名的推荐方式：

```python
>>>add.si(2,2)
```

现在可以创建独立任务组成的链：

```python
>>> res = (add.si(2, 2) | add.si(4, 4) | add.si(8, 8))()
>>> res.get()
16

>>> res.parent.get()
8

>>> res.parent.parent.get()
4
```

- 简单的组，你可以很容易创建一个并发执行的任务：

```python
>>> from celery import group
>>> res = group(add.s(i, i) for i in xrange(10))()
>>> res.get(timeout=1)
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

- 简单的弦，弦使得我们可以添加一个回调函数，在组中所有任务都执行完成后，该回调函数将被调用。非易并行的算法常常需要这种方式：

```python
>>> from celery import chord
>>> res = chord((add.s(i, i) for i in xrange(10)), xsum.s())()
>>> res.get()
90
```

上面这个例子创建了并行执行的 10 个任务，当所有的任务执行完成，他们的返回值组成一个列表传递给 `xsum` 任务。

弦体也可以是不可变的，此时组任务的返回值不传递给回调函数：

```python
>>> chord((import_contact.s(c) for c in contacts), notify_complete.si(import_id)).apply_async()
```

注意上面使用的 `si`；创建了一个不可变的签名，意味着所有传递的新参数都被忽略（包括前面任务的返回值）。

- 组合，链也可以是部分的：

```python
>>> c1 = (add.s(4) | mul.s(8))

# (16 + 4) * 8
>>> res = c1(16)
>>> res.get()
160
```

着意味着你可以组合链：

```python
# ((4 + 16) * 2 + 4) * 8
>>> c2 = (add.s(4, 16) | mul.s(2) | (add.s(4) | mul.s(8)))
>>> res = c2()
>>> res.get()
352
```

将组和另外一个任务链在一起将自动升级成弦:

```python
>>> c3 = (group(add.s(i, i) for i in xrange(10)) | xsum.s())
>>> res = c3()
>>> res.get()
90
```

组和弦也接收部分参数，所以在一个链中，前一个任务的返回值将传递给组中所有任务：

```python
>>> new_user_workflow = (create_user.s() | group(import_contacts.s(), send_welcome_email.s()))
>>> new_user_workflow.delay(username='artv', first='Art', last='Vandelay', email='art@vandelay.com')
```

如果你不想传递参数给组，那么让组中的签名不可变：

```python
>>> res = (add.s(4, 4) | group(add.si(i, i) for i in xrange(10)))()
>>> res.get()
<GroupResult: de44df8c-821d-4c84-9a6a-44769c738f98 [
    bc01831b-9486-4e51-b046-480d7c9b78de,
    2650a1b8-32bf-4771-a645-b0a35dcc791b,
    dcbee2a5-e92d-4b03-b6eb-7aec60fd30cf,
    59f92e0a-23ea-41ce-9fad-8645a0e7759c,
    26e1e707-eccf-4bf4-bbd8-1e1729c3cce3,
    2d10a5f4-37f0-41b2-96ac-a973b1df024d,
    e13d3bdb-7ae3-4101-81a4-6f17ee21df2d,
    104b2be0-7b75-44eb-ac8e-f9220bdfa140,
    c5c551a5-0386-4973-aa37-b65cbeb2624b,
    83f72d71-4b71-428e-b604-6f16599a9f37]>

>>> res.parent.get()
8
```

### Chains

3.0 版本新特性。

任务可以链在一起：如果当前任务成功执行，被链接的任务将会被启动：

```python
>>> res = add.apply_async((2, 2), link=mul.s(16))
>>> res.get()
4
```

被链接的任务将会用父任务的返回值作为它的第一个参数。上面这个例子当前任务返回值是 4，将会执行 `mul(4, 16)`。

结果将跟踪被原任务调用的任意子任务，而且这可以从结果实例中访问到：

```python
>>> res.children
[<AsyncResult: 8c350acf-519d-4553-8a53-4ad3a5c5aeb4>]

>>> res.children[0].get()
64
```

结果实例还有一个 `collect()` 方法，它将结果视作图，使得你可以在结果上迭代：

```python
>>> list(res.collect())
[(<AsyncResult: 7b720856-dc5f-4415-9134-5c89def5664e>, 4), (<AsyncResult: 8c350acf-519d-4553-8a53-4ad3a5c5aeb4>, 64)]
```

默认情况下，如果结果图没有完全形成，`collect()` 方法将会抛出一个 `IncompleteStream` 异常（至少有一个任务未完成），但是你可以获取结果图的一个中间表示形式：

```python
>>> for result, value in res.collect(intermediate=True)):
....
```

只要你愿意，你可以链接任意多的任务，并且签名也可以被链接：

```python
>>> s = add.s(2, 2)
>>> s.link(mul.s(4))
>>> s.link(log_result.s())
```

你还可以使用`on_error`方法添加错误回调函数：

```python
>>> add.s(2, 2).on_error(log_error.s()).delay()
```

当任务签名被应用，将导致下面调用发生：

```python
>>> add.apply_async((2, 2), link_error=log_error.s())
```

工作单元实际上不会将错误回调作为任务执行，而是会直接调用回调函数，这使得原始请求、异常、堆栈回溯对象都可以被传递给错误回调。

下面是一个错误回调的例子：

```python
from __future__ import print_function

import os

from proj.celery import app

@app.task
def log_error(request, exc, traceback):
    with open(os.path.join('/var/errors', request.id), 'a') as fh:
        print('--\n\n{0} {1} {2}'.format(task_id, exc, traceback), file=fh)
```

为了使链接任务更简便，有一个特殊的任务签名 `chain` 可以将任务链接到一起：

```python
>>> from celery import chain
>>> from proj.tasks import add, mul

>>> # (4 + 4) * 8 * 10
>>> res = chain(add.s(4, 4), mul.s(8), mul.s(10))
proj.tasks.add(4, 4) | proj.tasks.mul(8) | proj.tasks.mul(10)
```

调用任务链将在当前进程调用任务，并且返回链中最后一个任务的返回值：

```python
>>> res = chain(add.s(4, 4), mul.s(8), mul.s(10))()
>>> res.get()
640
```

它还将设置 `parent` 属性，这使得你可以以你自己的方式获取中间结果：

```python
>>> res.parent.get()
64

>>> res.parent.parent.get()
8

>>> res.parent.parent
<AsyncResult: eeaad925-6778-4ad1-88c8-b2a63d017933>
```

链还可以通过管道符创建：

```python
>>> (add.s(2, 2) | mul.s(8) | mul.s(10)).apply_async()
```

#### 图

除此之外，你还可以将结果图作为依赖图使用：

```python
>>> res = chain(add.s(4, 4), mul.s(8), mul.s(10))()

>>> res.parent.parent.graph
285fa253-fcf8-42ef-8b95-0078897e83e6(1)
    463afec2-5ed4-4036-b22d-ba067ec64f52(0)
872c3995-6fa0-46ca-98c2-5a19155afcf0(2)
    285fa253-fcf8-42ef-8b95-0078897e83e6(1)
        463afec2-5ed4-4036-b22d-ba067ec64f52(0)
```

你甚至可以将图转化为 `dot` 格式：

```python
>>> with open('graph.dot', 'w') as fh:
...     res.parent.parent.graph.to_dot(fh)
```

然后创建图片：

```bash
$ dot -Tpng graph.dot -o graph.png
```

### Groups

3.0版本新特性。

组可以用来执行并行任务。

组函数接收多个任务签名作为参数：

```python
>>> from celery import group
>>> from proj.tasks import add

>>> group(add.s(2, 2), add.s(4, 4))
(proj.tasks.add(2, 2), proj.tasks.add(4, 4))
```

如果你调用组，组中的任务将会在当前进程中一个接一个被启动，并且返回一个 `GroupResult` 实例，用来跟踪结果，或者告诉你有多少给任务已经成功执行等等：

```python
>>> g = group(add.s(2, 2), add.s(4, 4))
>>> res = g()
>>> res.get()
[4, 8]
```

组也支持迭代：

```python
>>> group(add.s(i, i) for i in xrange(100))()
```

组是一个签名，所以也可以和其他签名组合。

#### 组结果

组任务返回一个特殊的结果，这个结果就像普通任务一样使用，只不过它将组作为一个整体看待：

```python
>>> from celery import group
>>> from tasks import add

>>> job = group([
...             add.s(2, 2),
...             add.s(4, 4),
...             add.s(8, 8),
...             add.s(16, 16),
...             add.s(32, 32),
... ])

>>> result = job.apply_async()

# have all subtasks completed?
>>> result.ready()
True

# were all subtasks successful?
>>> result.successful()
True

>>> result.get()
[4, 8, 16, 32, 64]
```

`GroupResult` 包含一个 `AsyncResult` 实例的列表，并且就像单个任务一样操作。

组结果包含如下操作：

- `successful()` 如果所有的子任务都成功执行，那么返回 `True`（例如，没有抛出异常）。

- `failed()` 如果任意子任务失败，那么返回 `True`。

- `waiting()` 如果任意子任务没有执行完成，那么返回 `True`。

- `ready()` 如果所有的任务都执行完成，那么返回 `True`。

- `completed_count()` 返回完成的子任务数。

- `revoke()` 取消所有子任务。

- `join()` 收集所有子任务的返回值，并按照他们调用的顺序返回（作为一个列表）。

### Chords

2.3 版本新特性。

注意：在一个弦中应用的任务不能忽略任务的返回值。如果结果后端对弦中任何任务（弦头部或者弦体）禁用，你应该阅读“Important Notes”这一节。弦现在还不支持 RPC 存储后端。

弦是一个任务，只有弦头任务组中所有任务都执行完成，弦体任务才会执行。

我们来计算表达式 `1+1+2+2+3+3+...+n+n` 一直到100。

首先，你需要两个任务，`add()` 以及 `tsum()` (`sum()` 是一个标准函数)：

```python
@app.task
def add(x, y):
    return x + y

@app.task
def tsum(numbers):
    return sum(numbers)
```

现在，你可以使用弦来并行执行叠加步骤，然后计算所有叠加结果的和：

```python
>>> from celery import chord
>>> from tasks import add, tsum

>>> chord(add.s(i, i) for i in xrange(100))(tsum.s()).get()
9900
```

这明显是一个很勉强的例子，消息传递和同步的耗费使得它要比 python 里直接如下计算要慢得多：

```python
>>> sum(i + i for i in xrange(100))
```

同步的耗费非常大，所以你应该尽量避免使用弦。不过话又说回来，因为同步是许多并行算法所需要的，所以弦仍然是你工具箱里一个强大的元语。

我们一步步来定义弦：

```python
>>> callback = tsum.s()
>>> header = [add.s(i, i) for i in range(100)]
>>> result = chord(header)(callback)
>>> result.get()
9900
```

记住，回调函数只有在弦头任务组中所有任务都返回后才执行。头任务组中的每步都作为一个任务执行，可能在不同的节点上执行。回调函数将应用每个任务的返回值作为参数。`chord()` 返回的任务 ID 是回调函数的 ID，所以你可以等待它完成并拿到它的返回值（但是记住永远不要让一个任务等待其他任务）。

#### 错误处理

如果其中一个任务抛出异常将会发生什么呢？

弦的回调函数结果将转化为 `failure` 状态， 并且错误被设置成 `ChordError` 异常：

```python
>>> c = chord([add.s(4, 4), raising_task.s(), add.s(8, 8)])
>>> result = c()
>>> result.get()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "*/celery/result.py", line 120, in get
    interval=interval)
  File "*/celery/backends/amqp.py", line 150, in wait_for
    raise meta['result']
celery.exceptions.ChordError: Dependency 97de6f3f-ea67-4517-a21c-d867c61fcb47
    raised ValueError('something something',)
```

根据结果存储后端的不同，堆栈回溯信息也不一样，可以查看错误描述，这包括失败任务的 ID 和原异常的字符串表示。你还可以在 `result.traceback` 中找到原异常堆栈回溯信息。

注意余下的任务仍然会继续执行，所以即使中间这个任务失败，第三个任务（`add.s(8,8)`）依旧执行。另外，`ChordError` 只显示首先失败的任务（实时）：它不关心任务组中的顺序。

当弦失败时执行一个操作，你可以给弦回调添加一个错误回调函数：

```python
@app.task
def on_chord_error(request, exc, traceback):
    print('Task {0!r} raised error: {1!r}'.format(request.id, exc))

>>> c = (group(add.s(i, i) for i in range(10)) | xsum.s().on_error(on_chord_error.s()))).delay()
```

Important Notes
弦中的任务不可以忽略返回值。实际操作中，这意味着为了使用弦你必须启用  `result_backend`。另外，如果你的配置中 `task_ignore_result` 设置成真，请确保弦中使用的每个任务定义时都设置了 `ignore_result=False`。应用到任务子类和装饰类都管用。

任务子类示例：

```python
class MyTask(Task):
    ignore_result = False
```

装饰类示例：

```python
@app.task(ignore_result=False)
def another_task(project):
    do_something()
```

默认情况下，同步步骤是由一个周期性任务实现，它每秒轮训组的完成状态，当完成后调用回调函数。

实现示例：

```python
from celery import maybe_signature

@app.task(bind=True)
def unlock_chord(self, group, callback, interval=1, max_retries=None):
    if group.ready():
        return maybe_signature(callback).delay(group.join())
    raise self.retry(countdown=interval, max_retries=max_retries)
```

这被所有结果存储后端使用，除了 Redis 和 Memcached：他们定义了一个计数器，每执行完一个任务加 1，当计数器超过组中任务数时调用回调函数。

Redis 和 Memcached 方式是更好的选择，但是在其他存储后端中不容易被实现（欢迎建议！）。

注意：弦在Redis 2.2 以下版本不能正常工作；你需要升级到至少redis-server 2.2。

注意：如果你使用了弦，并且使用 Redis 存储后端，同时又覆盖了 `Task.after_return()` 方法，那么你需要确保调用 super 方法，否则弦的回调函数不会执行。

```python
def after_return(self, *args, **kwargs):
    do_something()
    super(MyTask, self).after_return(*args, **kwargs)
```

### Map & Starmap

`map` 和 `starmap` 是内建的任务，他们对序列中每个元素调用任务。

他们与任务组不同在于：

- 只有一个任务消息被发送

- 操作是按次序的

例如使用 `map`：

```python
>>> from proj.tasks import add
>>> ~xsum.map([range(10), range(100)])
[45, 4950]
```

与下列任务等价：

```python
@app.task
def temp():
    return [xsum(range(10)), xsum(range(100))]
```

使用 `starmap`：

```python
>>> ~add.starmap(zip(range(10), range(10)))
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

与下面任务等价：

```python
@app.task
def temp():
    return [add(i, i) for i in range(10)]
```

`map` 和 `starmap` 都是签名对象，所以他们都可以用作其他签名，或者组合到任务组等等，例如十秒钟后调用 `starmap`:

```python
>>> add.starmap(zip(range(10), range(10))).apply_async(countdown=10)
```

### Chunks

分块可以让你将迭代的工作片段化，使得如果你有 100万个对象处理，那么你可以创建 10 个任务，每个任务处理 10万个对象。

有人也许会担心分块任务会导致并行度的降低，但是对于一个繁忙的集群来说一般是不会的，实践中，因为你避免了消息的耗费，结果可能还会提高性能。

你可以使用 `app.Task.chunks()` 创建一个分块签名:

```python
>>> add.chunks(zip(range(100), range(100)), 10)
```

在任务组中，为块发送任务消息将在调用时在当前进程中进行：

```python
>>> from proj.tasks import add

>>> res = add.chunks(zip(range(100), range(100)), 10)()
>>> res.get()
[[0, 2, 4, 6, 8, 10, 12, 14, 16, 18],
 [20, 22, 24, 26, 28, 30, 32, 34, 36, 38],
 [40, 42, 44, 46, 48, 50, 52, 54, 56, 58],
 [60, 62, 64, 66, 68, 70, 72, 74, 76, 78],
 [80, 82, 84, 86, 88, 90, 92, 94, 96, 98],
 [100, 102, 104, 106, 108, 110, 112, 114, 116, 118],
 [120, 122, 124, 126, 128, 130, 132, 134, 136, 138],
 [140, 142, 144, 146, 148, 150, 152, 154, 156, 158],
 [160, 162, 164, 166, 168, 170, 172, 174, 176, 178],
 [180, 182, 184, 186, 188, 190, 192, 194, 196, 198]]
```

当调用`.apply_async`方法，将创建一个专门的任务使得独立子任务在一个工作单元中执行：

```python
>>> add.chunks(zip(range(100), range(100)), 10).apply_async()
```

你还可以将分块转化成组：

```python
>>> group = add.chunks(zip(range(100), range(100)), 10).group()
```

在任务组中，你可以通过递增延迟调整每个任务的 `countdown` 时间：

```python
>>> group.skew(start=1, stop=10)()
```

这意味着第一个任务 `countdown` 时间为1秒，第二个任务 `countdown` 时间为 2 秒，以此类推。

[参考](https://blog.csdn.net/u013148156/article/details/78566208)
