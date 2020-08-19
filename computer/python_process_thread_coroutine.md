# python 下的进程、线程、协程

## 什么是进程

进程 - 操作系统提供的抽象概念，是**系统进行资源分配和调度的基本单位**，是操作系统结构的基础。程序是指令、数据及其组织形式的描述，进程是程序的实体。程序本身是没有生命周期的，它只是存在磁盘上的一些指令,程序一旦运行就是进程。

当程序需要运行时，操作系统将代码和所有静态数据加载到内存和进程的地址空间（每个进程都拥有唯一的地址空间，见下图所示）中，通过创建和初始化栈（局部变量，函数参数和返回地址)、分配堆内存以及与IO相关的任务，当前期准备工作完成，启动程序，OS将CPU的控制权转移到新创建的进程，进程开始运行。

![](./images/01.png)

操作系统对进程的控制和管理通过 PCB(Processing Control Block)，**PCB 通常是系统内存占用区中的一个连续存区，它存放着操作系统用于描述进程情况及控制进程运行所需的全部信息(进程标识号,进程状态,进程优先级,文件系统指针以及各个寄存器的内容等)**，进程的PCB是系统感知进程的唯一实体。

一个进程至少具有5种基本状态：初始态、执行状态、等待（阻塞）状态、就绪状态、终止状态

- 初始状态：进程刚被创建，由于其他进程正占有CPU所以得不到执行，只能处于初始状态。
- 执行状态：任意时刻处于执行状态的进程只能有一个。
- 就绪状态：只有处于就绪状态的经过调度才能到执行状态
- 等待状态：进程等待某件事件完成
- 停止状态：进程结束

### 进程间的切换

无论是在多核还是单核系统中，一个CPU看上去都像是在并发的执行多个进程，这是通过处理器在进程间切换来实现的。

操作系统对把CPU控制权在不同进程之间交换执行的机制成为上下文切换（context switch），即保存当前进程的上下文，恢复新进程的上下文，然后将CPU控制权转移到新进程，新进程就会从上次停止的地方开始。因此，进程是轮流使用CPU的，CPU被若干进程共享，使用某种调度算法来决定何时停止一个进程，并转而为另一个进程提供服务。

- 单核CPU双进程的情况

![img](./images/02.png)

> 进程只在特定的机制(CPU时间片用完)和遇到I/O中断的情况下，进行上下文切换，轮流使用CPU资源

- 双核CPU双进程的情况

![](./images/03.png)

> 每一个进程独占一个CPU核心资源，在处理I/O请求的时候，CPU处于阻塞状态

### 进程间数据共享

系统中的进程与其他进程共享CPU和主存资源，为了更好的管理主存，现在系统提供了一种对主存的抽象概念，即为虚拟存储器（VM）。它是一个抽象的概念，它为每一个进程提供了一个假象，即每个进程都在独占地使用主存。

虚拟存储器主要提供了三个能力：

1. 将主存看成是一个存储在磁盘上的高速缓存，在主存中只保存活动区域，并根据需要在磁盘和主存之间来回传送数据，通过这种方式，更高效地使用主存

2. 为每个进程提供了一致的地址空间，从而简化了存储器管理

3. **保护了每个进程的地址空间不被其他进程破坏**

> 由于进程拥有自己独占的虚拟地址空间，CPU通过地址翻译将虚拟地址转换成真实的物理地址，每个进程只能访问自己的地址空间。因此，在没有其他机制（进程间通信）的辅助下，进程之间是无法共享数据的

### 以 python 中 multiprocessing 为例

```python
import multiprocessing
import threading
import time

n = 0

def count(num):
    global n
    for i in range(100000):
        n += i
    print("Process {0}:n={1},id(n)={2}".format(num, n, id(n)))


if __name__ == '__main__':
    start_time = time.time()
    process = list()
    for i in range(5):
        # 测试多进程使用
        p = multiprocessing.Process(target=count, args=(i,))
        # 测试多线程使用
        # p = threading.Thread(target=count, args=(i,))
        process.append(p)

    for p in process:
        p.start()

    for p in process:
        p.join()

    print("Main:n={0},id(n)={1}".format(n, id(n)))

    end_time = time.time()
    print("Total time:{0}".format(end_time - start_time))

```

结果：

```
Process 0:n=4999950000,id(n)=140473326238856
Process 1:n=4999950000,id(n)=140473326460048
Process 2:n=4999950000,id(n)=140473326197144
Process 3:n=4999950000,id(n)=140473327245696
Process 4:n=4999950000,id(n)=140473326198088
Main:n=0,id(n)=140473304903600
Total time:0.0152850151062
```

> 变量 n 在进程 p{0,1,2,3,4} 和主进程（main）中均拥有唯一的地址空间

## 什么是线程

线程 - 也是操作系统提供的抽象概念，是程序执行中一个单一的顺序控制流程，是程序执行流的最小单元，是处理器调度和分派的基本单位。一个进程可以有一个或多个线程，**同一进程中的多个线程将共享该进程中的全部系统资源，如虚拟地址空间，文件描述符和信号处理等等。但同一进程中的多个线程有各自的调用栈和线程本地存储**（如下图所示)。

![](./images/04.png)

系统利用 PCB 来完成对进程的控制和管理。同样，系统为线程分配一个线程控制块 TCB（Thread Control Block）,将所有用于控制和管理线程的信息记录在线程的控制块中，TCB中通常包括：

- 线程标志符
- 一组寄存器
- 线程运行状态
- 优先级
- 线程专有存储区
- 信号屏蔽

和进程一样，线程同样有五种状态：初始态、执行状态、等待（阻塞）状态、就绪状态和终止状态,线程之间的切换和进程一样也需要上下文切换。

进程和线程之间有许多相似的地方，那它们之间到底有什么区别呢？

## 进程和线程的区别

- 进程是资源的分配和调度的独立单元。进程拥有完整的虚拟地址空间，当发生进程切换时，不同的进程拥有不同的虚拟地址空间。而同一进程的多个线程是可以共享同一地址空间
- 线程是CPU调度的基本单元，一个进程包含若干线程。
- 线程比进程小，基本上不拥有系统资源。线程的创建和销毁所需要的时间比进程小很多
- 由于线程之间能够共享地址空间，因此，需要考虑同步和互斥操作
- 一个线程的意外终止会影响整个进程的正常运行，但是一个进程的意外终止不会影响其他的进程的运行。因此，多进程程序安全性更高。

> 总之，多进程程序安全性高，进程切换开销大，效率低；多线程程序维护成本高，线程切换开销小，效率高。

## 什么是协程

协程（Coroutine，又称微线程）是一种比线程更加轻量级的存在，协程不是被操作系统内核所管理，而完全是由程序所控制。协程与线程以及进程的关系见下图所示。

- **协程可以比作子程序，但执行过程中，子程序内部可中断，然后转而执行别的子程序，在适当的时候再返回来接着执行。协程之间的切换不需要涉及任何系统调用或任何阻塞调用**
- 协程只在一个线程中执行，是子程序之间的切换，发生在用户态上。而且，线程的阻塞状态是由操作系统内核来完成，发生在内核态上，因此协程相比线程节省线程创建和切换的开销
- 协程中不存在同时写变量冲突，因此，也就不需要用来守卫关键区块的同步性原语，比如互斥锁、信号量等，并且不需要来自操作系统的支持。

协程适用于 IO 阻塞且需要大量并发的场景，当发生IO阻塞，由协程的调度器进行调度，通过将数据流 yield 掉，并且记录当前栈上的数据，阻塞完后立刻再通过协程恢复栈，并把阻塞的结果放到这个协程上去运行。

![](./images/05.png)

下面，将针对在不同的应用场景中如何选择使用 Python 中的进程，线程，协程进行分析。

## 如何选择

在针对不同的场景对比三者的区别之前，首先需要介绍一下python的多线程(一直被程序员所诟病，认为是"假的"多线程)。

> 那为什么认为 Python 中的多线程是“伪”多线程呢？

更换上面 multiprocessing 示例中， `p=multiprocessing.Process(target=count,args=(i,))`为 `p=threading.Thread(target=count,args=(i,))`,其他照旧，运行结果如下：

```
第一次运行结果：
Process 0:n=6499148696,id(n)=140353090180296
Process 3:n=10547326821,id(n)=140353090180296
Process 1:n=10648445612,id(n)=140353090180320
Process 2:n=10724850118,id(n)=140353076851968
Process 4:n=11034887213,id(n)=140353090180320
Main:n=11034887213,id(n)=140353090180320
Total time:0.0644900798798

第二次运行结果：
Process 0:n=5851416116,id(n)=140708530539408
Process 4:n=10648919229,id(n)=140708488153368
Process 2:n=10730514337,id(n)=140708530539360
Process 1:n=11067307242,id(n)=140708523967648
Process 3:n=11232321962,id(n)=140708523967648
Main:n=11232321962,id(n)=140708523967648
Total time:0.0649511814117
```

- n是全局变量，Main 的打印结果与线程相等，证明了线程之间是数据共享

> 但是，为什么多线程运行时间比多进程还要长？这与我们上面所说（线程的开销<<进程的开销）的严重不相符啊。这就是轮到Cpython（python默认的解释器）中GIL(Global Interpreter Lock,全局解释锁)登场了。

## 什么是GIL

GIL 来源于 Python 设计之初的考虑，为了数据安全(由于内存管理机制中采用引用计数)所做的决定。某个线程想要执行，必须先拿到 GIL。因此，可以把 GIL 看作是“通行证”,并且在一个 Python 进程中，GIL 只有一个,拿不到通行证的线程,就不允许进入 CPU 执行。

Cpython 解释器在内存管理中采用引用计数，当对象的引用次数为0时，会将对象当作垃圾进行回收。设想这样一种场景：

> 一个进程中含有两个线程，分别为线程0和线程1，两个线程全都引用对象a。当两个线程同时对a发生引用（并未修改，不需要使用同步性原语），就会发生同时修改对象a的引用计数器，造成计数器引用少于实质性的引用，当进行垃圾回收时，造成错误异常。因此，需要一把全局锁（即为GIL）来保证对象引用计数的正确性和安全性。

无论是单核还是多核,一个进程永远只能同时执行一个线程(拿到 GIL 的线程才能执行，如下图所示)，这就是为什么在多核 CPU 上，Python 的多线程效率并不高的根本原因。

![](./images/06.png)

> 那是不是在 Python 中遇到并发的需求就使用多进程就万事大吉了呢？其实不然，软件工程中有一句名言：**没有银弹！**

## 何时用？

常见的应用场景不外乎三种：

1. CPU 密集型：程序需要占用 CPU 进行大量的运算和数据处理；
2. I/O 密集型：程序中需要频繁的进行 I/O 操作；例如网络中 socket 数据传输和读取等；
3. CPU 密集 + I/O 密集：以上两种的结合

> CPU密集型的情况可以对比以上multiprocessing和threading的例子，多进程的性能 > 多线程的性能。

下面主要解释一下 I/O 密集型的情况。与 I/O 设备交互，目前最常用的解决方案就是**DMA**。

### 什么是 DMA

DMA(Direct Memory Access) 是系统中的一个特殊设备，它可以协调完成内存到设备间的数据传输，中间过程不需要 CPU 介入。

以文件写入为例：

1. 进程 p1 发出数据写入磁盘文件的请求
2. CPU 处理写入请求，通过编程告诉 DMA 引擎数据在内存的位置，要写入数据的大小以及目标设备等信息
3. CPU 处理其他进程 p2 的请求，DMA 负责将内存数据写入到设备中
4. DMA 完成数据传输，中断 CPU
5. CPU 从 p2 上下文切换到 p1 , 继续执行 p1

![](./images/07.png)

#### Python多线程的表现（I/O密集型）

1. 线程 Thread0 首先执行，线程 Thread1 等待（GIL的存在）
2. Thread0 收到 I/O 请求，将请求转发给 DMA, DMA 执行请求
3. Thread1 占用 CPU 资源，继续执行
4. CPU 收到 DMA 的中断请求，切换到 Thread0 继续执行

![](./images/08.png)

> 与进程的执行模式相似，弥补了GIL带来的不足，又由于线程的开销远远小于进程的开销，因此，在 IO 密集型场景中，多线程的性能更高

实践是检验真理的唯一标准，下面将针对 I/O 密集型场景进行测试。

#### 测试

- 执行代码

```python
import multiprocessing
import threading
import time

def count(num):
    time.sleep(1)  # 模拟IO操作
    print("Process {0} End".format(num))


if __name__ == '__main__':
    start_time = time.time()
    process = list()
    for i in range(5):
        # p = multiprocessing.Process(target=count, args=(i,))
        p = threading.Thread(target=count, args=(i,))
        process.append(p)
    for p in process:
        p.start()
    for p in process:
        p.join()
    end_time = time.time()
    print("Total time:{0}".format(end_time - start_time))

```

- 结果

```
## 多进程
Process 0 End
Process 3 End
Process 4 End
Process 2 End
Process 1 End
Total time:1.383193016052246
## 多线程
Process 0 End
Process 4 End
Process 3 End
Process 1 End
Process 2 End
Total time:1.003425121307373

```

- 多线程的执行效性能高于多进程

> 是不是认为这就结束了？远还没有呢。针对 I/O 密集型的程序，协程的执行效率更高，因为它是程序自身所控制的，这样将节省线程创建和切换所带来的开销。

以 Python 中 asyncio 应用为依赖，使用 async/await 语法进行协程的创建和使用。

- 程序代码

```python
import time
import asyncio

async def coroutine():
    await asyncio.sleep(1)  # 模拟IO操作

if __name__ == "__main__":
    start_time = time.time()
    loop = asyncio.get_event_loop()
    tasks = []
    for i in range(5):
        task = loop.create_task(coroutine())
        tasks.append(task)
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    end_time = time.time()
    print("total time:", end_time - start_time)

```

- 结果

```
total time: 1.001854419708252
```

- 协程的执行效性能高于多线程

## 总结

本文从操作系统原理出发结合代码实践讲解了进程，线程和协程以及他们之间的关系。并且，总结和整理了Python实践中针对不同的场景如何选择对应的方案，如下：

- CPU密集型：多进程
- IO密集型：多线程（协程维护成本较高,而且在读写文件方面效率没有显著提升）
- CPU密集和IO密集：多进程+协程