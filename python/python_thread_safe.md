# 什么是线程安全问题

在多线程环境下，每一个线程均可以使用**所属进程**的**全局变量**。如果一个线程对全局变量进行了修改，将会影响到其他所有的线程。为了避免多个线程同时对全局变量进行修改，引入了线程同步机制，通过互斥锁，条件变量或者读写锁等来控制对全局变量的访问。

只用全局变量并不能满足多线程环境的需求，很多时候线程还需要拥有自己的私有数据，这些数据对于其他线程来说不可见。因此线程中也可以使用**局部变量**，局部变量只有线程自身可以访问，同一个进程下的其他线程不可访问。

有时候使用局部变量不太方便，因此 python 还提供了 ThreadLocal 变量，它本身是一个全局变量，但是每个线程却可以利用它来保存属于自己的私有数据，这些私有数据对其他线程也是不可见的。

## 线程不安全示例

### 示例一：

```python
#!/usr/bin/env python3
# encoding: utf-8

import random
import threading
import logging
import time

def worker(data):
    logging.debug('data[\'value\']=%s', data['value'])
    temp = random.randint(1, 100)
    logging.debug('temp=%s', temp)
    data['value'] = temp
    time.sleep(1)
    logging.debug('data[\'value\']=%s', data['value'])
    local_data = 0
    for _ in range(100):
        local_data += 1
    logging.debug('local_data=%s', local_data)


logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)

data = {}
data['value'] = 1000
logging.debug('data[\'value\']=%s', data['value'])

local_data = 0
for _ in range(100):
    local_data += 1
logging.debug('local_data=%s', local_data)

for i in range(2):
    t = threading.Thread(target=worker, args=(data,))
    t.start()

logging.debug('data[\'value\']=%s', data['value'])
"""
(MainThread) data['value']=1000
(MainThread) local_data=100
(Thread-1  ) data['value']=1000
(Thread-1  ) temp=16
(Thread-2  ) data['value']=16
(Thread-2  ) temp=9
(MainThread) data['value']=9
(Thread-1  ) data['value']=9
(Thread-1  ) local_data=100
(Thread-2  ) data['value']=9
(Thread-2  ) local_data=100

"""

```

### 示例二：

```python
#!/usr/bin/env python3
# encoding: utf-8

import threading

global_num = 0

def thread_cal():
    global global_num
    for _ in range(1000):
        global_num += 1

# Get 10 threads, run them and wait them all finished.
threads = []
for i in range(10):
    threads.append(threading.Thread(target=thread_cal))
    threads[i].start()

for i in range(10):
    threads[i].join()

# Value of global variable can be confused.
print(global_num)

"""
% python 02.py
5774
% python 02.py
10000
% python 02.py
6243

% python3 02.py
10000
% python3 02.py
10000
% python3 02.py
10000

"""

```

### 示例三：

```python
#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Keeping thread-local values
"""

#end_pymotw_header
import random
import threading
import logging
import time


def worker(foo):
    logging.debug('do_something before: %s' % foo)
    foo.do_something()
    logging.debug('do_something after: %s' % foo)

    local_foo = Foo(0)
    local_foo.do_something()
    logging.debug('local_foo: %s' % local_foo)


logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)


class Foo(object):
    class_val = 0

    def __init__(self, instance_val):
        self.instance_val = instance_val

    def do_something(self):
        for _ in range(100):
            self.instance_val += 1
            time.sleep(random.randint(0, 1))
            self.__class__.class_val += 1

    def __str__(self):
        return 'class_val: %s, instance_val: %s' % (self.instance_val, self.__class__.class_val)


foo = Foo(0)
logging.debug(foo)

local_foo = Foo(0)
logging.debug('local_foo: %s' % local_foo)

for i in range(10):
    t = threading.Thread(target=worker, args=(foo,))
    t.start()

foo.do_something()
logging.debug(foo)

local_foo.do_something()
logging.debug('local_foo: %s' % local_foo)
"""
(MainThread) class_val: 0, instance_val: 0
(MainThread) local_foo: class_val: 0, instance_val: 0
(Thread-1  ) do_something before: class_val: 0, instance_val: 0
(Thread-2  ) do_something before: class_val: 2, instance_val: 1
(Thread-3  ) do_something before: class_val: 3, instance_val: 1
(Thread-4  ) do_something before: class_val: 4, instance_val: 1
(Thread-5  ) do_something before: class_val: 10, instance_val: 6
(Thread-6  ) do_something before: class_val: 11, instance_val: 6
(Thread-7  ) do_something before: class_val: 11, instance_val: 6
(Thread-8  ) do_something before: class_val: 14, instance_val: 7
(Thread-9  ) do_something before: class_val: 17, instance_val: 9
(Thread-10 ) do_something before: class_val: 17, instance_val: 9
(Thread-7  ) do_something after: class_val: 942, instance_val: 932
(Thread-3  ) do_something after: class_val: 988, instance_val: 983
(Thread-9  ) do_something after: class_val: 1002, instance_val: 1001
(Thread-2  ) do_something after: class_val: 1012, instance_val: 1014
(MainThread) class_val: 1032, instance_val: 1057
(Thread-4  ) do_something after: class_val: 1042, instance_val: 1069
(Thread-10 ) do_something after: class_val: 1073, instance_val: 1128
(Thread-8  ) do_something after: class_val: 1076, instance_val: 1140
(Thread-6  ) do_something after: class_val: 1085, instance_val: 1179
(Thread-1  ) do_something after: class_val: 1090, instance_val: 1200
(Thread-5  ) do_something after: class_val: 1100, instance_val: 1320
(Thread-7  ) local_foo: class_val: 100, instance_val: 1941
(Thread-2  ) local_foo: class_val: 100, instance_val: 2041
(Thread-9  ) local_foo: class_val: 100, instance_val: 2067
(Thread-6  ) local_foo: class_val: 100, instance_val: 2106
(Thread-3  ) local_foo: class_val: 100, instance_val: 2128
(MainThread) local_foo: class_val: 100, instance_val: 2158
(Thread-10 ) local_foo: class_val: 100, instance_val: 2173
(Thread-8  ) local_foo: class_val: 100, instance_val: 2180
(Thread-1  ) local_foo: class_val: 100, instance_val: 2182
(Thread-4  ) local_foo: class_val: 100, instance_val: 2187
(Thread-5  ) local_foo: class_val: 100, instance_val: 2200

"""

```

## 全局变量 VS 局部变量

首先借助一个小程序来看看多线程环境下全局变量的同步问题。

```python
# -*- coding: utf-8 -*-

import threading

global_num = 0


def thread_cal():
    global global_num
    for _ in xrange(1000):
        global_num += 1

# Get 10 threads, run them and wait them all finished.
threads = []
for i in range(10):
    threads.append(threading.Thread(target=thread_cal))
    threads[i].start()

for i in range(10):
    threads[i].join()

# Value of global variable can be confused.
print global_num

"""
[root@huzhi-code]# python 11_test.py
7469
[root@huzhi-code]# python 11_test.py
8000
[root@huzhi-code]# python 11_test.py
6004
[root@huzhi-code]# python 11_test.py
10000
[root@huzhi-code]# python 11_test.py
9372
[root@huzhi-code]# python 11_test.py
8564
"""

```

这里我们创建了10个线程，每个线程均对全局变量 global_num 进行1000次的加1操作（循环1000次加1是为了延长单个线程执行时间，使线程执行时被中断切换），当10个线程执行完毕时，全局变量的值是多少呢？答案是不确定。简单来说是因为 `global_num += 1` 并不是一个原子操作，因此执行过程可能被其他线程中断，导致其他线程读到一个脏值。以两个线程执行 +1 为例，其中一个可能的执行序列如下（此情况下最后结果为1）：

![](../images/python_global_var.png)

多线程中使用全局变量时普遍存在这个问题，解决办法也很简单，可以使用互斥锁、条件变量或者是读写锁等。下面考虑用互斥锁来解决上面代码的问题，只需要在进行 +1 运算前加锁，运算完毕释放锁即可，这样就可以保证运算的原子性。

```python
# -*- coding: utf-8 -*-

import threading

global_num = 0
l = threading.Lock()

def thread_cal():
    global global_num
    for _ in xrange(1000):
        # 加锁和释放锁
        l.acquire()
        global_num += 1
        l.release()

# Get 10 threads, run them and wait them all finished.
threads = []
for i in range(10):
    threads.append(threading.Thread(target=thread_cal))
    threads[i].start()

for i in range(10):
    threads[i].join()

# Value of global variable can be confused.
print global_num

"""
[root@huzhi-code]# python 11_test.py
10000
[root@huzhi-code]# python 11_test.py
10000
[root@huzhi-code]# python 11_test.py
10000
[root@huzhi-code]# python 11_test.py
10000
[root@huzhi-code]#
"""

```

在线程中使用局部变量则不存在这个问题，因为每个线程的局部变量不能被其他线程访问。下面我们用10个线程分别对各自的局部变量进行1000次加1操作，每个线程结束时打印一共执行的操作次数（每个线程均为1000）：

```python
# -*- coding: utf-8 -*-

import threading


def show(num):
    print threading.current_thread().getName(), num


def thread_cal():
    local_num = 0
    for _ in xrange(1000):
        local_num += 1
    show(local_num)


# Get 10 threads, run them and wait them all finished.
threads = []
for i in range(10):
    threads.append(threading.Thread(target=thread_cal))
    threads[i].start()

for i in range(10):
    threads[i].join()

"""
[root@huzhi-code]# python 11_test.py
Thread-2 1000
Thread-1 1000
Thread-3 1000
Thread-4 1000
Thread-5 1000
Thread-6 1000
Thread-7 1000
Thread-8 1000
Thread-10 1000
Thread-9 1000
"""
```

可以看出这里每个线程都有自己的 local_num，各个线程之间互不干涉。

## Thread-local 对象

上面程序中我们需要给 show 函数传递 local_num 局部变量，并没有什么不妥。不过考虑在实际生产环境中，我们可能会调用很多函数，每个函数都需要很多局部变量，这时候用传递参数的方法会很不友好。

为了解决这个问题，一个直观的的方法就是建立一个全局字典，保存线程 ID 到该线程局部变量的映射关系，运行中的线程可以根据自己的 ID 来获取本身拥有的数据。这样，就可以避免在函数调用中传递参数，如下示例：

```python
# -*- coding: utf-8 -*-

import threading

global_data = {}


def show():
    cur_thread = threading.current_thread()
    print cur_thread.getName(), global_data[cur_thread]


def thread_cal():
    cur_thread = threading.current_thread()
    global_data[cur_thread] = 0
    for _ in xrange(1000):
        global_data[cur_thread] += 1
    show()  # Need no local variable.  Looks good.


# Get 10 threads, run them and wait them all finished.
threads = []
for i in range(10):
    threads.append(threading.Thread(target=thread_cal))
    threads[i].start()

for i in range(10):
    threads[i].join()

"""
[root@huzhi-code]# python 11_test.py
Thread-2 1000
Thread-3 1000
Thread-1 1000
Thread-4 1000
Thread-5 1000
Thread-6 1000
Thread-8 1000
Thread-7 1000
Thread-9 1000
Thread-10 1000
[root@huzhi-code]#
"""
```

保存一个全局字典，然后将线程标识符作为key，相应线程的局部数据作为 value，这种做法并不完美。首先，每个函数在需要线程局部数据时，都需要先取得自己的线程ID，略显繁琐。更糟糕的是，这里并没有真正做到线程之间数据的隔离，因为每个线程都可以读取到全局的字典，每个线程都可以对字典内容进行更改。

为了更好解决这个问题，python 线程库实现了 ThreadLocal 变量（很多语言都有类似的实现，比如Java）。ThreadLocal 真正做到了线程之间的数据隔离，并且使用时不需要手动获取自己的线程 ID，如下示例：

```python
# -*- coding: utf-8 -*-

import threading

global_data = threading.local()


def show():
    print threading.current_thread().getName(), global_data.num


def thread_cal():
    global_data.num = 0
    for _ in xrange(1000):
        global_data.num += 1
    show()


# Get 10 threads, run them and wait them all finished.
threads = []
for i in range(10):
    threads.append(threading.Thread(target=thread_cal))
    threads[i].start()

for i in range(10):
    threads[i].join()

print "Main thread: ", global_data.__dict__

"""
[root@huzhi-code]# python 11_test.py
Thread-1 1000
Thread-2 1000
Thread-3 1000
Thread-4 1000
Thread-5 1000
Thread-9 1000
Thread-6 1000
Thread-8 1000
Thread-7 1000
Thread-10 1000
Main thread:  {}
"""
```

上面示例中每个线程都可以通过 global_data.num 获得自己独有的数据，并且每个线程读取到的 global_data 都不同，真正做到线程之间的隔离。


# 线程安全结论

`线程安全`就是多线程访问时，采用了加锁机制，当一个线程访问该类的某个数据时，进行保护，其他线程不能进行访问直到该线程读取完，其他线程才可使用。不会出现数据不一致或者数据污染。

`线程不安全`就是不提供数据访问保护，有可能出现多个线程先后更改数据造成所得到的数据是脏数据

Python实现线程安全的方法
1. Lock 对象
2. Rlock 对象
3. 信号量和有边界的信号量
4. 事件
5. queue 模块
6. threading.local()

要想实现线程安全不一定要使用锁机制，threading.local 就没有采用加锁机制，threading.local 在内部使用字典存储每个线程的相关数据。字典的key就是线程ID，值就是相关线程的数据。

# threading.local 对象基本性质

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" threading.local 对象基本性质
"""

from threading import Thread
from threading import local

# 在全局命名空间中实例化 local 对象
mydata = local()

# 为 local 对象上的属性赋值，该属性属于全局进程的相关数据
mydata.number = 42
print mydata.number  # 42
print mydata.__dict__  # {'number': 42}

# 为 local 对象上的属性赋值的另一种方式
mydata.__dict__.setdefault('widgets', [])
print mydata.widgets  # []

log = []

def f():
    # 在线程内部使用全局命名空间中的 local 对象 mydata
    # 但是该对象不会携带全局进程中的相关数据
    print mydata.__dict__  # {}
    items = mydata.__dict__.items()
    print items  # []
    items.sort()
    # 在线程中向 local 对象添加数据
    log.append(items)
    mydata.number = 11
    log.append(mydata.number)

# 启动线程
thread = Thread(target=f)
thread.start()
thread.join()
print log  # [[], 11]

# 在线程中添加的数据不会影响全局进程中的数据，实现线程安全
print mydata.number  # 42

```

# 继承 local 对象实现自定义类

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 继承 local 对象实现自定义类
"""

from threading import Thread
from threading import local

class MyLocal(local):
    number = 2

    def __init__(self, **kw):
        # 这里会执行两次，在全局进程中执行一次，当该对象应用在线程中也要执行一次
        print "MyLocal init"
        self.__dict__.update(kw)
        print self.__dict__  # {'color': 'red'}

    def squared(self):
        return self.number ** 2

# 在全局命名空间中实例化 MyLocal 对象，MyLocal 对象继承自 local 对象
mydata = MyLocal(color='red')

# mydata 在全局进程中的地址和在线程中的地址一样，为什么会两次执行初始化方法 __init__??
print id(mydata)  # 140319450666808

# 实例化 MyLocal 对象后，添加相关属性，这些属性属于全局进程中的相关数据
# 其中 color 是实例化时添加的属性，number 是类变量，other 是动态添加的
# 所以 color 和 number 可以在线程中访问到，other 在线程中不能访问
print mydata.number  # 2
print mydata.color  # red

mydata.other = 5
print mydata.other  # 5

del mydata.color
print mydata.squared()  # 4








def f():
    print id(mydata)  # 140319450666808
    print mydata.__dict__  # {'color': 'red'}
    items = mydata.__dict__.items()
    print items  # [('color', 'red')]
    items.sort()
    log.append(items)
    print mydata.number  # 2
    # print mydata.other  # AttributeError: 'MyLocal' object has no attribute 'other'
    mydata.number = 11
    log.append(mydata.number)




log = []
thread = Thread(target=f)
thread.start()
thread.join()
print log  # [[('color', 'red')], 11]
print mydata.number  # 2
# print mydata.color  # AttributeError: 'MyLocal' object has no attribute 'color'

```

### 继承 local 对象实现自定义类时的限制

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread
from threading import local

def f():
    print mydata.__dict__  # {}
    items = mydata.__dict__.items()
    print items  # []
    items.sort()
    log.append(items)
    mydata.number = 11
    log.append(mydata.number)


class MyLocal(local):
    __slots__ = 'number'

mydata = MyLocal()
mydata.number = 52
mydata.color = 'blue'  # __slots__ 的行为和普通对象中的 __slots__ 行为不一致，普通对象此时不能额外添加属性
print mydata.number  # 52
print mydata.color  # blue

log = []
thread = Thread(target=f)
thread.start()
thread.join()
print mydata.number  # 11
del mydata
```

### werkzeug.local.Local 对象基本性质

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread
from werkzeug.local import Local

request_global = '123'
request_local = '456'

locals = Local()
locals.request = '789'

class MyThread(Thread):
    def run(self):
        global request_global
        request_global = 'abc'

        request_local = 'def'

        locals.request = 'ghi'

        print 'child thread request: ', request_global  # child thread request:  abc
        print 'child thread request: ', request_local  # child thread request:  def
        print 'child thread request: ', locals.request  # child thread request:  ghi

mythread = MyThread()
mythread.start()
mythread.join()

print 'main thread request: ', request_global  # main thread request:  abc
print 'main thread request: ', request_local  # main thread request:  456
print 'main thread request: ', locals.request  # main thread request:  789

```

参考：

* https://selfboot.cn/2016/08/22/threadlocal_overview/
* https://learnku.com/docs/pymotw/threading-manage-concurrent-operations-within-a-process/3421
