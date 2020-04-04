# Celery 学习笔记（4）Workflow

## Signature 对象

前面介绍了可以通过 delay 和 apply_async 来执行一个任务，多数情况下这已经足够使用，但是有时候你希望能够将任务及其参数传递给其它函数时，现有的方法就不够用了。

在 Celery 中，提供了 signature 方法将函数和参数打包起来成为一个 signature 对象，在这个对象中可以保存函数的参数以及任务执行的参数。

```python
>>> from celery import signature
>>> signature('cele.add', args=(2, 2), countdown=10)
cele.add(2, 2)
```

或者你可以直接在 task 对象上调用 signature 方法，生成一个 signature 对象，或者直接调用 s 这个快捷方法。

```python
>>> add.signature((2, 2), countdown=10)
cele.add(2, 2)
>>> add.s(2, 2)
cele.add(2, 2)
```

和普通的 task 对象一样，你可以直接在 signarture 对象上调用 delay 或者 apply_async 方法，向 Celery 队列提交一个任务。

```python
>>> add.s(2, 2).delay()
<AsyncResult: fa8f326d-9e10-48f6-97c9-b33a33381231>
>>> add.s(2, 2).apply_async()
<AsyncResult: 6595e01e-ef73-4787-9f0e-5f2d5c35b103>
```

除了可以包含所有的参数之外，你也可以通过部分赋值的方式，产生一个偏函数对象，其效果就跟 partial 类似。当你调用时，只需要提供剩余参数就可以了。这样生成的偏函数和普通的 signature 对象功能上没有差别，只是相当于有了绑定的参数。

```python
>>> partial_s = add.s(1)
>>> partial_s(2)
3
```

前面有提到可以通过 apply_aysnc 的 link 参数指定任务的后续任务，但是有一点不太令人满意，就是默认情况下会将前一个任务的返回值以第一个参数的形式传递给后一个任务，也就是说，如果我不是要创建这种传递返回值的任务，但是函数定义却需要额外多一个参数，否则在任务执行时会出错。所以 Celery 也提供了一个机制使得取消掉这种默认的返回值传递，那就是将 signature 声明为 immutable。也可以直接使用 si 这个快捷方法创建 immutable signature。

```python
@app.task
def no_argument():
    return 'No Argument'

>>> add.apply_async((2, 2), link=no_argument.signature(immutable=True))
>>> add.apply_async((2, 2), link=no_argument.si())
```


## 工作流

实际使用过程中，可能需要处理大量有关或无关的任务，所以 Celery 提供了一组函数，用来对任务执行流程进行控制。而其中的基本任务单元就是前面提到的 signature 对象。

### chain - 任务的链式执行

chain 函数接受一个任务的列表，Celery 保证一个 chain 里的子任务会依次执行，在 AsynResult 上执行 get 会得到最后一个任务的返回值。和 link 功能类似，每一个任务执行结果会当作参数传入下一个任务，所以如果你不需要这种特性，采用 immutable signature 来取消。

```python
>>> from celery import chain
>>> result = chain(add.s(1, 2), add.s(3), add.s(4))  # 1+2+3+4
>>> result().get()
10
```

### group - 任务的并发执行

group 函数也接受一个任务列表，这些任务会同时加入到任务队列中，且执行顺序没有任何保证。在 AsynResult 上执行 get 会得到一个包含了所有返回值的列表。

```python
>>> from celery import group
>>> group(add.s(1, 2), add.s(3,4), add.s(5,6))().get()
[3, 7, 11]
```

### chord - 带回调的 group

chord 基本功能和 group 类似，只是有一个额外的回调函数。回调函数会在前面的任务全部结束时执行，其参数是一个包含了所有任务返回值的列表。在 AsynResult 上执行 get 会得到回调函数的返回值。

```python
@app.task
def xsum(values):
    return sum(values)

>>> from celery import chord
>>> chord((add.s(i, i) for i in xrange(4)), xsum.s())().get()  # xsum 收到 [0, 2, 4, 6]
12
```

### chunks - 将大量任务分解为小块任务

和前面三个函数不同， chunks 是在 app.task 对象上的方法，它将多个任务分成几块执行，每一块是一个单独的任务由一个 worker 执行。

```python
>>> add.chunks(zip(range(100), range(100)), 10)().get()
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

[参考](https://blog.csdn.net/preyta/article/details/54313047)
