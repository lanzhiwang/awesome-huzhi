## TRACING PYTHON MEMORY LEAKS

While I was writing a python daemon, I noticed that my application process memory usage is growing over time. The data wasn’t increasing so there must have been some memory leak.  当我编写python守护程序时，我注意到我的应用程序进程的内存使用量随时间增长。 数据没有增加，因此一定存在内存泄漏。

It’s not so easy for a Python application to leak memory. Usually there are three scenarios:  Python应用程序泄漏内存并非易事。 通常有以下三种情况：

1. some low level C library is leaking
2. your Python code have global lists or dicts that grow over time, and you forgot to remove the objects after use  您的Python代码具有随时间增长的全局列表或字典，并且您在使用后忘记删除对象
3. there are some [reference cycles](http://en.wikipedia.org/wiki/Reference_counting#Dealing_with_reference_cycles) in your app

I remembered the [post from Marius Gedminas](http://mg.pov.lt/blog/hunting-python-memleaks), in which he traced his memory leaks, but I haven’t noticed before that [he published](http://mg.pov.lt/blog/python-object-graphs.html) his [tools](http://mg.pov.lt/objgraph.py).  我记得马里乌斯·盖德米纳斯（Marius Gedminas）的帖子，他在其中追踪了他的内存泄漏，但是在他发布工具之前我还没有注意到。
The tools are awesome. Just take a look at my session:  工具很棒。

```
$ pdb ./myserver.py
> /server.py(12)()
-> import sys
(Pdb) r
2008-11-13 23:15:36,619 server.py      INFO   Running with verbosity 10 (>=DEBUG)
2008-11-13 23:15:36,620 server.py      INFO   Main dir='./server', args=[]
```

After some time, when my application collected some garbages I pressed Ctrl+C:

```
2008-11-13 18:41:40,136 server.py      INFO   Quitting
(Pdb) import gc
(Pdb) gc.collect()
58
(Pdb) gc.collect()
0
```

Let’s see some statistics of object types in memory:

```
(Pdb) import objgraph
(Pdb) objgraph.show_most_common_types(limit=20)
dict                       378631
list                       184791
builtin_function_or_method 57542
tuple                      55478
Message                    48129
function                   45575
instancemethod             31949
NonBlockingSocket          31876
NonBlockingConnection      31876
_socketobject              31876
_Condition                 28320
AMQPReader                 14900
cell                       9678
```

Message objects definitely shouldn’t be in the memory. Let’s see where are they referenced:

```
(Pdb) objgraph.by_type('Message')[1]
<amqplib.client_0_8.Message object at 0x8a5b7ac>
(Pdb) import random
(Pdb) obj = objgraph.by_type('Message')[random.randint(0,48000)]
(Pdb) objgraph.show_backrefs([obj], max_depth=10)
Graph written to objects.dot (15 nodes)
Image generated as objects.png
```

This is what I saw:

![Message object references](https://www.lshift.net/~majek/objects-message-5.png)

Ok. A Channelobject still has references to our Message. Let’s move on to see why Channel is not freed:

```
(Pdb) obj = objgraph.by_type('Channel')[random.randint(0,31000)]
(Pdb) objgraph.show_backrefs([obj], max_depth=10)
Graph written to objects.dot (35 nodes)
Image generated as objects.png
```

Channel object references are much more interesting – we just caught a reference cycle here!

[![Channel object references](https://www.lshift.net/~majek/objects-message-6-500.png)](https://www.lshift.net/~majek/objects-message-6.png)

There is also one other class that’s not being freed – NonBlockingConnection:

```
(Pdb) obj = objgraph.by_type('NonBlockingConnection')[random.randint(0,31000)]
(Pdb) objgraph.show_backrefs([obj], max_depth=10)
Graph written to objects.dot (135 nodes)
Image generated as objects.png
```

Here’s the cycle we’re looking for:

![img](https://tech.labs.oliverwyman.com/wp-content/uploads/2008/11/objects-message-3.png)

To fix this issue it’s enough to break the reference loops in one place. This is the code that fixes the reference loops:

```
        # we don't need channel and connection any more
        channel.close()
        connection.close()
        # remove the reference cycles:
        del channel.callbacks
        del connection.channels
        del connonection.connection
```

[参考](http://tech.labs.oliverwyman.com/blog/2008/11/14/tracing-python-memory-leaks/)
