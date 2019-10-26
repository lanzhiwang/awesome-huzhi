# python-articles

* [Python 消耗了太多的内存，如何减少内存使用量](https://habr.com/en/post/458518/)

* [Python GIL被杀了吗？](https://hackernoon.com/has-the-python-gil-been-slain-9440d28fa93d?utm_source=mybridge&utm_medium=blog&utm_campaign=read_more)

* [使用Python每秒百万个请求](https://www.freecodecamp.org/news/million-requests-per-second-with-python-95c137af319/?utm_source=mybridge&utm_medium=email&utm_campaign=read_more)


# 参考

* [Mybridge](https://github.com/Mybridge)




# Has the Python GIL been slain?  Python GIL被杀了吗？

In early 2003, Intel launched the new Pentium 4 “HT” processor. This processor was clocked at 3 GHz and had “Hyper-Threading” Technology.  2003年初，英特尔推出了新的Pentium 4“ HT”处理器。 该处理器的主频为3 GHz，并具有“超线程”技术。

Over the following years, Intel and AMD battled to achieve the best desktop computer performance by increasing bus-speed, L2 cache size and reducing die size to minimize latency. The 3Ghz HT was superseded in 2004 by the “Prescott” model 580, which clocked up to 4 GHz.  在接下来的几年中，英特尔和AMD一直在通过提高总线速度，L2缓存大小和减小裸片大小以最大程度地减少延迟来争取最佳台式计算机性能。 3Ghz HT于2004年被时钟频率高达4 GHz的“ Prescott”型号580取代。

It seemed like the path forward for better performance was higher clock speed, but CPUs were plagued by high power consumption and earth-warming heat output.  更高的时钟频率似乎是提高性能的前进方向，但是CPU受到高功耗和温暖地球的热量输出的困扰。

Do you have a 4Ghz CPU in your desktop? Unlikely, because the way forward for performance was higher-bus speed and multiple cores. The Intel Core 2 superseded the Pentium 4 in 2006, with clock speeds far lower.  台式机中是否有4Ghz CPU？ 不太可能，因为提高性能的方法是更高的总线速度和多核。 英特尔酷睿2在2006年取代了奔腾4，时钟速度大大降低。

Aside from the release of consumer multicore CPUs, something else happened in 2006, Python 2.5 was released! Python 2.5 came bundled with a beta version of the with statement that you know and love.  除了发布消费型多核CPU之外，2006年还发生了其他事情，Python 2.5也发布了！ Python 2.5附带了您熟悉和喜欢的with语句的beta版本。

Python 2.5 had one major limitation when it came to utilizing Intel’s Core 2 or AMD’s Athlon X2.  在使用Intel的Core 2或AMD的Athlon X2时，Python 2.5有一个主要限制。

The GIL.

## What is the GIL?

The GIL, or Global Interpreter Lock, is a boolean value in the Python interpreter, protected by a mutex. The lock is used by the core bytecode evaluation loop in CPython to set which thread is currently executing statements.  GIL或全局解释器锁是Python解释器中的一个布尔值，受互斥锁保护。 CPython中的核心字节码评估循环使用该锁来设置当前正在执行语句的线程。

CPython supports multiple threads within a single interpreter, but threads must request access to the GIL in order to execute Opcodes (low-level operations). This, in turn, means that Python developers can utilize async code, multi-threaded code and never have to worry about acquiring locks on any variables or having processes crash from deadlocks.  CPython在单个解释器中支持多个线程，但是线程必须请求访问GIL才能执行操作码（低级操作）。 反过来，这意味着Python开发人员可以利用异步代码，多线程代码，而不必担心获取任何变量的锁或使进程因死锁而崩溃。

The GIL makes multithreaded programming in Python simple.

The GIL also means that whilst CPython can be multi-threaded, only 1 thread can be executing at any given time. This means that your quad-core CPU is doing this — (minus the bluescreen, hopefully)  GIL还意味着，尽管CPython可以是多线程的，但在任何给定时间只能执行1个线程。 这意味着您的四核CPU正在执行此操作（希望减去蓝屏）

The current version of the GIL was written in 2009, to support async features and has survived relatively untouched even after many attempts to remove it or reduce the requirement for it.  当前版本的GIL写于2009年，以支持异步功能，即使在多次尝试删除或降低对GIL的要求之后，它仍未受到影响。

The requirement for any proposal to remove the GIL is that it should not degrade the performance of any single-threaded code. Anyone who ever enabled Hyper-Threading back in 2003 will appreciate why that is important.  任何删除GIL的建议的要求是，它不应降低任何单线程代码的性能。 早在2003年启用超线程的任何人都会欣赏为什么这很重要。

## Avoiding the GIL in CPython

If you want truly concurrent code in CPython, you have to use multiple processes.  如果要在CPython中使用真正的并发代码，则必须使用多个进程。

In CPython 2.6 the multiprocessing module was added to the standard library. Multiprocessing was a wrapper around the spawning of CPython processes (each with its own GIL) —  在CPython 2.6中，多处理模块已添加到标准库中。 多重处理是CPython进程（每个都有自己的GIL）的产生的包装器-

```python
from multiprocessing import Process

def f(name):
    print 'hello', name

if __name__ == '__main__':
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
```

Processes can be spawned, sent commands via compiled Python modules or functions and then rejoined into the master process.  可以生成进程，通过已编译的Python模块或函数发送命令，然后重新加入主进程。

Multiprocessing also supports sharing of variables via a Queue or a Pipe. It also has a Lock object, for locking objects in the master process for writing from other processes.  多重处理还支持通过队列或管道共享变量。 它还具有一个Lock对象，用于锁定主进程中的对象以从其他进程进行写入。

The multiprocessing has 1 major flaw. It has significant overhead, both in time and in memory usage. CPython startup times, even without no-site, are 100–200ms (see https://hackernoon.com/which-is-the-fastest-version-of-python-2ae7c61a6b2b).  多重处理有1个主要缺陷。 它在时间和内存使用上都有大量开销。 即使没有无站点，CPython的启动时间也为100-200ms（请参阅https://hackernoon.com/which-is-the-fastest-version-of-python-2ae7c61a6b2b）。

So you can have concurrent code in CPython, but you have to carefully plan it’s application for long-running processes that have little sharing of objects between them.  因此，您可以在CPython中使用并发代码，但是您必须仔细计划它的应用程序，以便长时间运行的进程之间几乎没有对象共享。

Another alternative is a third party package like Twisted.  另一种选择是第三方程序包，如Twisted。

## PEP554 and the death of the GIL?

> So to recap, multithreading in CPython is easy, but it’s not truly concurrent, and multiprocessing is concurrent but has a significant overhead.  综上所述，Python中的多线程很容易，但是它并不是真正的并发，多处理是并发的，但是开销却很大。

## What if there was a better way?

The clue in bypassing the GIL is in the name, the global interpreter lock is part of the global interpreter state. CPython processes can have multiple interpreters, and hence multiple locks, however, this feature is rarely used because it is only exposed via the C-API.  绕过GIL的线索就是名字，全局解释器锁是全局解释器状态的一部分。 CPython进程可以具有多个解释器，因此可以具有多个锁，但是，此功能很少使用，因为它仅通过C-API公开。

One of the features proposed for CPython 3.8 is PEP554, the implementation of sub-interpreters and an API with a new interpreters module in the standard library.  为CPython 3.8提议的功能之一是PEP554，子解释器的实现和标准库中带有新解释器模块的API。

This enables creating multiple interpreters, from Python within a single process. Another change for Python 3.8 is that interpreters will all have individual GILs —  这样一来，就可以从Python创建多个解释器。 Python 3.8的另一个变化是，解释器都将具有单独的GIL-

Because Interpreter state contains the memory allocation arena, a collection of all pointers to Python objects (local and global), sub-interpreters in PEP 554 cannot access the global variables of other interpreters.  由于解释器状态包含内存分配区域，所有指向Python对象的指针的集合（本地和全局），因此PEP 554中的子解释器无法访问其他解释器的全局变量。

Similar to multiprocessing, the way to share objects between interpreters would be to serialize them and use a form of IPC (network, disk or shared memory). There are many ways to serialize objects in Python, there’s the marshal module, the pickle module and more standardized methods like json and simplexml. Each of these has pro’s and con’s, all of them have an overhead.  与多处理类似，在解释器之间共享对象的方法是序列化它们并使用一种IPC形式（网络，磁盘或共享内存）。 使用Python序列化对象的方法有很多，其中有marshal模块，pickle模块以及更标准化的方法，例如json和simplexml。 这些每个都有优点和缺点，它们都有开销。

First prize would be to have a shared memory space that is mutable and controlled by the owning process. That way, objects could be sent from a master-interpreter and received by other interpreters. This would be a lookup managed-memory space of PyObject pointers that could be accessed by each interpreter, with the main process controlling the locks.  一等奖将是拥有一个共享的存储空间，该存储空间是可变的，并由拥有过程控制。 这样，对象可以从主解释器发送并由其他解释器接收。 这将是每个解释器可以访问的PyObject指针的查找管理内存空间，主要过程控制锁。

The API for this is still being worked out, but it will probably look like this:  API仍在制定中，但可能看起来像这样：

This example uses numpy and sends a numpy array over a channel by serializing it with the marshal module, the sub-interpreter then processes the data (on a separate GIL) so this could be a CPU-bound concurrency problem perfect for sub-interpreters.  此示例使用numpy并通过使用marshal模块对其进行序列化在通道上发送numpy数组，然后子解释器处理数据（在单独的GIL上），因此这可能是CPU绑定的并发问题，非常适合子解释器。

## That looks inefficient

The marshal module is fairly fast, but not as fast as sharing objects directly from memory.  封送模块相当快，但不如直接从内存中共享对象快。

PEP 574 proposes a new pickle protocol (v5) which has support for allowing memory buffers to be handled separately from the rest of the pickle stream. For large data objects, serializing them all in one go and deserializing from the sub-interpreter would add a lot of overhead.  PEP 574提出了一个新的pickle协议（v5），该协议支持允许将内存缓冲区与剩余的pickle流分开处理。 对于大型数据对象，一次性将它们全部序列化并从子解释器反序列化将增加很多开销。

The new API could be interfaced (hypothetically, neither have been merged yet) like this —  新的API可以像这样进行接口（假设还没有被合并）—

## That sure looks like a lot of boilerplate

Ok, so this example is using the low-level sub-interpreters API. If you’ve used the multiprocessing library you’ll recognize some of the problems. It’s not as simple as threading , you can’t just say run this function with this list of inputs in separate interpreters (yet).  好的，所以此示例使用低级子解释器API。 如果您使用了多处理库，您会发现一些问题。 它不像线程那样简单，您不能仅仅说在单独的解释器中使用此输入列表运行此功能。

Once this PEP is merged, I expect we’ll see some of the other APIs in PyPi adopt them.  合并此PEP后，我希望我们会看到PyPi中的其他一些API也采用了它们。

## How much overhead does a sub-interpreter have?

Short answer: More than a thread, less than a process.  简短的答案：多于一个线程，少于一个进程。

Long answer: The interpreter has its own state, so whilst PEP554 will make it easy to create sub-interpreters, it will need to clone and initialize the following:  长答案：解释器具有其自己的状态，因此尽管PEP554将使创建子解释器变得容易，但它需要克隆和初始化以下内容：

* modules in the __main__ namespace and importlib
* the sys dictionary containing
* builtin functions ( print() , assert etc)
* threads
* core configuration

The core configuration can be cloned easily from memory, but the imported modules are not so simple. Importing modules in Python is slow, so if creating a sub-interpreter means importing modules into another namespace each time, the benefits are diminished.  可以从内存中轻松克隆核心配置，但是导入的模块并不是那么简单。 在Python中导入模块的速度很慢，因此，如果创建子解释器意味着每次都将模块导入另一个名称空间，则收益会减少。

## What about asyncio?

The existing implementation of the asyncio event loop in the standard library creates frames to be evaluated but shares state within the main interpreter (and therefore shares the GIL).  标准库中asyncio事件循环的现有实现创建了要评估的帧，但在主解释器中共享状态（因此共享GIL）。

After PEP554 has been merged, and likely in Python 3.9, an alternate event loop implementation could be implemented (although nobody has done so yet) that runs async methods within sub interpreters, and hence, concurrently.  在PEP554合并之后（可能在Python 3.9中），可以实现一个替代的事件循环实现（尽管尚未有人这样做），该实现在子解释器中并因此在异步方法中运行。

## Sounds great, ship it!  听起来不错，请发货！

Well, not quite.  好吧，不完全是。

Because CPython has been implemented with a single interpreter for so long, many parts of the code base use the “Runtime State” instead of the “Interpreter State”, so if PEP554 were to be merged in it’s current form there would still be many issues.  由于CPython已经使用单个解释器实现了很长时间，因此代码库的许多部分使用“运行时状态”而不是“解释器状态”，因此，如果要以当前形式合并PEP554，仍然会有很多问题 。

For example, the Garbage Collector (in 3.7<) state belongs to the runtime.  例如，垃圾收集器（在3.7 <中）状态属于运行时。

During the PyCon sprints changes have started to move the garbage collector state to the interpreter, so that each sub interpreter will have it’s own GC (as it should).  在PyCon冲刺期间，更改已开始将垃圾收集器状态移至解释器，以便每个子解释器将拥有自己的GC（应有）。

Another issue is that there are some “global”, variables lingering around in the CPython codebase and many C extensions. So when people suddenly started writing properly concurrent code, we might start to see some problems.  另一个问题是CPython代码库和许多C扩展中存在一些“全局”变量。 因此，当人们突然开始编写正确的并发代码时，我们可能会开始看到一些问题。

Another issue is that file handles belong to the process, so if you have a file open for writing in one interpreter, the sub interpreter won’t be able to access the file (without further changes to CPython).  另一个问题是文件句柄属于该过程，因此，如果您打开了要在一个解释器中写入的文件，则子解释器将无法访问该文件（无需对CPython进行进一步更改）。

In short, there are many other things still to be worked out.  简而言之，还有许多其他事情需要解决。

## Conclusion: Is the GIL dead?

The GIL will still exist for single-threaded applications. So even when PEP554 is merged, if you have single-threaded code, it won’t suddenly be concurrent.  对于单线程应用程序，GIL将仍然存在。 因此，即使将PEP554合并，如果您具有单线程代码，也不会突然并发执行。

If you want concurrent code in Python 3.8, you have CPU-bound concurrency problems then this could be the ticket!  如果您想要Python 3.8中的并发代码，则遇到CPU约束的并发问题，那么这可能就是问题所在！

## When?

Pickle v5 and shared memory for multiprocessing will likely be Python 3.8 (October 2019) and sub-interpreters will be between 3.8 and 3.9.  Pickle v5和用于多处理的共享内存可能是Python 3.8（2019年10月），子解释器将在3.8和3.9之间。

If you want to play with my examples now, I’ve built a custom branch with all of the code required https://github.com/tonybaloney/cpython/tree/subinterpreters  如果您现在想使用我的示例，我已经建立了一个自定义分支，其中包含所有必需的代码https://github.com/tonybaloney/cpython/tree/subinterpreters
























