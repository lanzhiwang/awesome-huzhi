## Python 生成器和协程

### 协程基本流程

```python
>>> def simple_coroutine():
...     print('-> coroutine started')
...     x = yield
...     print('-> coroutine received:', x)
... 
>>> my_coro = simple_coroutine()
>>> my_coro
<generator object simple_coroutine at 0x7ff7d22693b8>
>>> next(my_coro)  # my_coro.send(None)
-> coroutine started
>>> my_coro.send(42)
-> coroutine received: 42
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
# 控制权流动到协程定义体的末尾， 导致生成器像往常一样抛出 StopIteration 异常
>>> 

# 获取协程状态
>>> import inspect
>>> inspect.getgeneratorstate(my_coro)
'GEN_CLOSED'
>>> 

# 协程内部的一次如果未处理就会抛出
>>> my_coro = simple_coroutine()
>>> my_coro.send(1234)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: can't send non-None value to a just-started generator
>>> 

```



### 协程中的各种状态

```python
>>> def simple_coro2(a):
...     print('-> Started: a =', a)
...     b = yield a
...     print('-> Received: b =', b)
...     c = yield a + b
...     print('-> Received: c =', c)
... 
>>> 
>>> my_coro2 = simple_coro2(14)
>>> from inspect import getgeneratorstate
>>> getgeneratorstate(my_coro2)
'GEN_CREATED'
>>> next(my_coro2)
-> Started: a = 14
14
>>> getgeneratorstate(my_coro2)
'GEN_SUSPENDED'
>>> my_coro2.send(28)
-> Received: b = 28
42
>>> my_coro2.send(99)
-> Received: c = 99
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
>>> getgeneratorstate(my_coro2)
'GEN_CLOSED'
>>> 


```



### 协程与无限循环一起使用

```python
>>> def averager():
...     total = 0.0
...     count = 0
...     average = None
...     while True:  # 这个无限循环表明， 只要调用方不断把值发给这个协程， 它就会一直接收值， 然后生成结果。 仅当调用方在协程上调用 .close() 方法，或者没有对协程的引用而被垃圾回收程序回收时， 这个协程才会终止
...         term = yield average
...         total += term
...         count += 1
...         average = total/count
... 
>>> 
>>> coro_avg = averager()
>>> next(coro_avg)
>>> coro_avg.send(10)
10.0
>>> coro_avg.send(30)
20.0
>>> coro_avg.send(5)
15.0
>>> 
# 如何终止执行coro_avg

```



### 预激协程



```pyrhon
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps

def coroutine(func):
    """装饰器： 向前执行到第一个`yield`表达式， 预激`func`"""
    @wraps(func)
    def primer(*args, **kwargs):  # 把被装饰的生成器函数替换成这里的 primer 函数； 调用 primer 函数时， 返回预激后的生成器。
        gen = func(*args, **kwargs)  # 调用被装饰的函数， 获取生成器对象
        next(gen)  # 预激生成器
        return gen  # 返回生成器
    return primer

@coroutine
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average = total/count

>>> coro_avg = averager()
>>> from inspect import getgeneratorstate
>>> getgeneratorstate(coro_avg)
'GEN_SUSPENDED'
>>> coro_avg.send(10)
10.0
>>> coro_avg.send(30)
20.0
>>> coro_avg.send(5)
15.0
>>> 
# 发送的值不是数字， 导致协程内部有异常抛出
>>> coro_avg.send('spam')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/lanzhiwang/work/py_web/multimediaapi_lab/pukep.py", line 22, in averager
    total += term
TypeError: unsupported operand type(s) for +=: 'float' and 'str'
>>> 
>>> 
# 由于在协程内没有处理异常， 协程会终止。 如果试图重新激活协程， 会抛出 StopIteration 异常
>>> coro_avg.send(60)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
>>> 

# 示例暗示了终止协程的一种方式： 发送某个哨符值， 让协程退出。 内置的 None 和 Ellipsis 等常量经常用作哨符值。 Ellipsis 的优点是， 数据流中不太常有这个值。 我还见过有人把 StopIteration类（类本身， 而不是实例， 也不抛出） 作为哨符值； 也就是说， 是像这样使用的： my_coro.send(StopIteration)。


```



### generator.throw

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time

'''
generator.throw(exc_type[, exc_value[, traceback]])
致使生成器在暂停的 yield 表达式处抛出指定的异常。 如果生成
器处理了抛出的异常， 代码会向前执行到下一个 yield 表达式， 而产
出的值会成为调用 generator.throw 方法得到的返回值。 如果生成器
没有处理抛出的异常， 异常会向上冒泡， 传到调用方的上下文中
'''

class DemoException(Exception):
    """为这次演示定义的异常类型。 """

def demo_exc_handling():
    print('-> coroutine started')
    while True:
        try:
            x = yield time()
        except DemoException:
            print('*** DemoException handled. Continuing...')
        else:
            print('-> coroutine received: {!r}'.format(x))

>>> exc_coro = demo_exc_handling()
>>> next(exc_coro)
-> coroutine started
1545205770.8204246
>>> exc_coro.send(11)
-> coroutine received: 11
1545205786.5895877
>>> exc_coro.throw(DemoException)
*** DemoException handled. Continuing...
1545205811.9567995
>>> from inspect import getgeneratorstate
>>> getgeneratorstate(exc_coro)
'GEN_SUSPENDED'
>>> exc_coro.throw(ZeroDivisionError)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/lanzhiwang/work/py_web/multimediaapi_lab/pukep.py", line 12, in demo_exc_handling
    x = yield time()
ZeroDivisionError
>>> getgeneratorstate(exc_coro)
'GEN_CLOSED'
>>> 


```



### generator.close()

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time

'''
generator.close()
致使生成器在暂停的 yield 表达式处抛出 GeneratorExit 异常。
如果生成器没有处理这个异常， 或者抛出了 StopIteration 异常（通
常是指运行到结尾）， 调用方不会报错
'''

class DemoException(Exception):
    """为这次演示定义的异常类型。 """

def demo_exc_handling():
    print('-> coroutine started')
    while True:
        try:
            x = yield time()
        except DemoException:
            print('*** DemoException handled. Continuing...')
        else:
            print('-> coroutine received: {!r}'.format(x))

>>> exc_coro = demo_exc_handling()
>>> next(exc_coro)
-> coroutine started
1545206169.8764915
>>> exc_coro.close()
>>> from inspect import getgeneratorstate
>>> getgeneratorstate(exc_coro)
'GEN_CLOSED'
>>> 

```



```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time

'''
generator.close()
致使生成器在暂停的 yield 表达式处抛出 GeneratorExit 异常。
如果生成器处理了这个异常， 并且生成器有产出值， 解释器会抛出 RuntimeError 异常。
生成器抛出的其他异常会向上冒泡， 传给调用方。
'''

class DemoException(Exception):
    """为这次演示定义的异常类型。 """

def demo_exc_handling():
    print('-> coroutine started')
    while True:
        try:
            x = yield time()
        except DemoException:
            print('*** DemoException handled. Continuing...')
        except GeneratorExit:
            print('*** GeneratorExit handled. Continuing...')
        else:
            print('-> coroutine received: {!r}'.format(x))

>>> exc_coro = demo_exc_handling()
>>> next(exc_coro)
-> coroutine started
1545206448.3586347
>>> exc_coro.send(11)
-> coroutine received: 11
1545206480.3637943
>>> exc_coro.close()
*** GeneratorExit handled. Continuing...
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
RuntimeError: generator ignored GeneratorExit
>>> 

```



### 协程返回值

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import namedtuple

Result = namedtuple('Result', 'count average')

def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total/count
    return Result(count, average)


>>> coro_avg = averager()
>>> next(coro_avg)
>>> coro_avg.send(10)
>>> coro_avg.send(30)
>>> coro_avg.send(5)
>>> coro_avg.send(None)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration: Result(count=3, average=15.0)
>>> 

>>> coro_avg = averager()
>>> next(coro_avg)
>>> coro_avg.send(10)
>>> coro_avg.send(30)
>>> coro_avg.send(5)
>>> try:
...     coro_avg.send(None)
... except StopIteration as exc:
...     result = exc.value
... 
>>> result
Result(count=3, average=15.0)
>>> 

```



### yield from

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

def gen():
    for c in 'AB':
        yield c
    for i in range(1, 3):
        yield i

print(list(gen()))  # ['A', 'B', 1, 2]

def gen_and_yield():
    yield from 'AB'
    yield from range(1, 3)

print(list(gen_and_yield()))  # ['A', 'B', 1, 2]

```



```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

Result = namedtuple('Result', 'count average')

# 作为子生成器使用
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total/count
    return Result(count, average)


# 作为委派生成器使用
def grouper(results, key):
    while True:
        results[key] = yield from averager()


# 委托生成器客户端
def main(data):
    results = {}
    """1、外层 for 循环每次迭代会新建一个 grouper 实例，
    赋值给 group 变量； group 是委派生成器

    6、外层 for 循环重新迭代时会新建一个 grouper 实例， 然后绑定到 group 变量上。
    前一个 grouper 实例（以及它创建的尚未终止的averager 子生成器实例）
    被垃圾回收程序回收
    """
    for key, values in data.items():
        group = grouper(results, key)

        """2、调用 next(group)， 预激委派生成器 grouper，
        此时进入 while True 循环， 调用子生成器 averager 后，
        在 yield from 表达式处暂停
        """
        next(group)

        """3、内层 for 循环调用 group.send(value)， 直接把值传给子生成器averager。
        同时， 当前的 grouper 实例（group） 在 yield from 表达式处暂停
        """
        for value in values:
            group.send(value)

        """4、内层循环结束后， group 实例依旧在 yield from 表达式处暂停，
        因此， grouper 函数定义体中为 results[key] 赋值的语句还没有执行

        5、如果外层 for 循环的末尾没有 group.send(None)，
        那么 averager 子生成器永远不会终止，
        委派生成器 group 永远不会再次激活， 因此永远不会为 results[key] 赋值
        """
        group.send(None)  # important!

    # print(results)  # {'girls;m': Result(count=10, average=1.4279999999999997), 'boys;m': Result(count=9, average=1.3888888888888888), 'boys;kg': Result(count=9, average=40.422222222222224), 'girls;kg': Result(count=10, average=42.040000000000006)}
    report(results)


# output report
def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(
              result.count, group, result.average, unit))


data = {
    'girls;kg':
        [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m':
        [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg':
        [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'boys;m':
        [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
}


if __name__ == '__main__':
    main(data)

```



### yield from  结论



```python
yield from EXPR 表达式对 EXPR 对象所做的第一件事是， 调用 iter(EXPR)， 从
中获取迭代器。 因此， EXPR 可以是任何可迭代的对象

RESULT = yield from EXPR

_i = iter(EXPR)
try:
    _y = next(_i)
except StopIteration as _e:
    _r = _e.value
else:
    while 1:
        _s = yield _y
        try:
            _y = _i.send(_s)
        except StopIteration as _e:
            _r = _e.value
            break

RESULT = _r


_i = iter(EXPR)
"""
i（迭代器）子生成器
EXPR 可以是任何可迭代的对象， 因为获取迭代器 _i（这是子生成
器） 使用的是 iter() 函数
"""
try:
    _y = next(_i)
    """
    _y（产出的值）子生成器产出的值
    预激子生成器； 结果保存在 _y 中， 作为产出的第一个值
    """
except StopIteration as _e:
    _r = _e.value
    """
    _r（结果）最终的结果（即子生成器运行结束后 yield from 表达式的值）
    如果抛出 StopIteration 异常， 获取异常对象的 value 属性， 赋值
    给 _r——这是最简单情况下的返回值（RESULT）
    """
else:
    while 1:  # 运行这个循环时， 委派生成器会阻塞， 只作为调用方和子生成器之间的通道
        _s = yield _y
        """
        预激子生成器的结果保存在 _y 中， 作为产出的第一个值
        _s（发送的值）调用方发给委派生成器的值， 这个值会转发给子生成器
        产出子生成器当前产出的元素； 等待调用方发送 _s 中保存的值。 注
        意， 这个代码清单中只有这一个 yield 表达式。
        """
        try:
            _y = _i.send(_s)  
            """
            _s（发送的值）调用方发给委派生成器的值， 这个值会转发给子生成器
            _y（产出的值）子生成器产出的值
            尝试让子生成器向前执行， 转发调用方发送的 _s
            """
        except StopIteration as _e:
            """如果子生成器抛出 StopIteration 异常， 获取 value 属性的值， 赋
            值给 _r， 然后退出循环， 让委派生成器恢复运行
            """
            _r = _e.value
            break

RESULT = _r  # 返回的结果（RESULT） 是 _r， 即整个 yield from 表达式的值

```



```python
_i = iter(EXPR)
try:
    _y = next(_i)
except StopIteration as _e:
    _r = _e.value
else:
    while 1:
        try:
            _s = yield _y
        except GeneratorExit as _e:
            try:
                _m = _i.close
            except AttributeError:
                pass
            else:
                _m()
            raise _e
        except BaseException as _e:
            _x = sys.exc_info()
            try:
                _m = _i.throw
            except AttributeError:
                raise _e
            else:
                try:
                    _y = _m(*_x)
                except StopIteration as _e:
                    _r = _e.value
                    break
        else:
            try:
                if _s is None:
                    _y = next(_i)
                else:
                    _y = _i.send(_s)
            except StopIteration as _e:
                _r = _e.value
                break

RESULT = _r


_i = iter(EXPR)
"""EXPR 可以是任何可迭代的对象， 因为获取迭代器 _i（这是子生成
器） 使用的是 iter() 函数
"""
try:
    _y = next(_i)
    """预激子生成器； 结果保存在 _y 中， 作为产出的第一个值
    """
except StopIteration as _e:
    """如果抛出 StopIteration 异常， 获取异常对象的 value 属性， 赋值
    给 _r——这是最简单情况下的返回值（RESULT）
    """
    _r = _e.value
else:
    while 1:  # 运行这个循环时， 委派生成器会阻塞， 只作为调用方和子生成器之间的通道
        try:
            _s = yield _y
            """产出子生成器当前产出的元素； 等待调用方发送 _s 中保存的值。 这
            个代码清单中只有这一个 yield 表达式
            """
        except GeneratorExit as _e:
            """这一部分用于关闭委派生成器和子生成器。 因为子生成器可以是任
            何可迭代的对象， 所以可能没有 close 方法
            """
            try:
                _m = _i.close
            except AttributeError:
                pass
            else:
                _m()
            raise _e
        except BaseException as _e:
            """这一部分处理调用方通过 .throw(...) 方法传入的异常。 同样，
            子生成器可以是迭代器， 从而没有 throw 方法可调用——这种情况会导致委派生成器抛出异常。
            """
            _x = sys.exc_info()
            try:
                _m = _i.throw
            except AttributeError:
                raise _e
            else:
                """如果子生成器有 throw 方法， 调用它并传入调用方发来的异常。 子
                生成器可能会处理传入的异常（然后继续循环） ； 可能抛出
                StopIteration 异常（从中获取结果， 赋值给 _r， 循环结束） ； 还可
                能不处理， 而是抛出相同的或不同的异常， 向上冒泡， 传给委派生成器。
                """
                try:
                    _y = _m(*_x)
                except StopIteration as _e:
                    _r = _e.value
                    break
        else:
            try:
                if _s is None:
                    """如果调用方最后发送的值是 None， 在子生成器上调用 next 函数，
                    否则调用 send 方法
                    """
                    _y = next(_i)
                else:
                    _y = _i.send(_s)
            except StopIteration as _e:
                """如果子生成器抛出 StopIteration 异常， 获取 value 属性的值， 赋
                值给 _r， 然后退出循环， 让委派生成器恢复运行
                """
                _r = _e.value
                break

RESULT = _r

```

