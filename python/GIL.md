# 全局解释器锁

GIL 是由 CPython 解释器所引入的锁机制。GIL 会在解释器中防止**多线程**的并行执行。在执行前，每个线程都必须等待 GIL 释放正在运行的线程。实际上，在访问解释器中的任何作为栈和 Python 对象实例前，解释器会强制执行中的线程获取到 GIL。这正是 GIL 的目的所在，它会防止不同线程并发访问 Python 对象。GIL 会保护解释器的内存，并确保垃圾收集以正确的方式进行。实际上，如果开发者想以并行执行线程的方式来达到提升性能的目的，那么 GIL 会阻止这样做。如果从CPython 解释器中删除GIL，那么线程就能并行执行了。GIL 并不会阻止一个进程在不同的处理器上执行，同一时刻它只允许唯一的线程出现在解释器中。

以下是**串行执行**，**多线程执行**，**多进程执行**分别在**计算密集型**和**IO密集型**应用下的性能测试数据：

```
# 计算密集型
non (1 iters)           0.001860 seconds
threaded (1 threads)    0.001796 seconds
process (1 process)     0.004290 seconds
non (2 iters)           0.003355 seconds
threaded (2 threads)    0.003513 seconds
process (2 process)     0.005005 seconds
non (4 iters)           0.006698 seconds
threaded (4 threads)    0.007105 seconds
process (4 process)     0.006100 seconds
non (8 iters)           0.013766 seconds
threaded (8 threads)    0.014240 seconds
process (8 process)     0.009060 seconds

# IO密集型
non (1 iters)           0.051190 seconds
threaded (1 threads)    0.048204 seconds
process (1 process)     0.052165 seconds
non (2 iters)           0.100434 seconds
threaded (2 threads)    0.054724 seconds
process (2 process)     0.060189 seconds
non (4 iters)           0.200313 seconds
threaded (4 threads)    0.057347 seconds
process (4 process)     0.062610 seconds
non (8 iters)           0.411077 seconds
threaded (8 threads)    0.084225 seconds
process (8 process)     0.097673 seconds

```

根据结果可以看到线程调用的成本要比不使用线程调用的成本高多少。特别的，我们还会发现增加线程的开销与线程数之间的比例关系。这说明 GIL 对多线程并行有很大影响，增加线程数并未带来什么好处。函数是在 Python 中执行的，由于创建线程与 GIL 的成本，多线程示例永远不可能比非线程示例更快。另外，要记住，在同一时刻，GIL 只允许一个线程访问解释器。

在 I/O 过程中，GIL 会被释放。多线程执行要比单线程执行快。由于很多应用会在 I/O 中执行一定数量的工作，因此 GIL 并不会阻止程序员创建多线程任务来并发执行以加快执行速度。

所以，对于**IO密集型应用**来说，使用多线程会提高程序性能，对于**计算密集型应用**来说，使用多进程会提高程序性能

## 测试脚本

```python
from threading import Thread
import multiprocessing


def show_results(func_name, results):
    print("%-23s %4.6f seconds" % (func_name, results))


class process_object(multiprocessing.Process):
    def __init__(self, func):
        multiprocessing.Process.__init__(self)
        self.func = func

    def run(self):
        self.func()


def process(num_process, func):
    funcs = []
    for i in range(int(num_process)):
        funcs.append(process_object(func))
    for i in funcs:
        i.start()
    for i in funcs:
        i.join()


class threads_object(Thread):
    def __init__(self,
                 group=None,
                 target=None,
                 name=None,
                 args=(),
                 kwargs=None,
                 *,
                 daemon=None):
        super().__init__(group=group, target=target, name=name, daemon=daemon)
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.args[0]()


def threaded(num_threads, func):
    funcs = []
    for i in range(int(num_threads)):
        funcs.append(threads_object(args=(func, )))
    for i in funcs:
        i.start()
    for i in funcs:
        i.join()


class non_object(object):
    def __init__(self, func):
        self.func = func

    def run(self):
        self.func()


def non(num_iter, func):
    funcs = []
    for i in range(int(num_iter)):
        funcs.append(non_object(func))
    for i in funcs:
        i.run()


def function_to_run1():
    pass


def function_to_run2():
    a, b = 1, 1
    for _ in range(10000):
        a, b = b, a + b


def function_to_run3():
    from urllib import request
    response = request.urlopen('http://www.baidu.com/')
    response.read(1024)


if __name__ == "__main__":
    import sys
    from timeit import Timer

    repeat = 10
    number = 1
    num = [1, 2, 4, 8]

    for func in [function_to_run1, function_to_run2, function_to_run3]:
        for i in num:
            t = Timer("non(%s, %s)" % (i, func.__name__),
                      "from __main__ import non",
                      globals=globals())
            best_result = min(t.repeat(repeat=repeat, number=number))
            show_results("non (%s iters)" % i, best_result)

            t = Timer("threaded(%s, %s)" % (i, func.__name__),
                      "from __main__ import threaded",
                      globals=globals())
            best_result = min(t.repeat(repeat=repeat, number=number))
            show_results("threaded (%s threads)" % i, best_result)

            t = Timer("process(%s, %s)" % (i, func.__name__),
                      "from __main__ import process",
                      globals=globals())
            best_result = min(t.repeat(repeat=repeat, number=number))
            show_results("process (%s process)" % i, best_result)
        print('Iterations complete')
"""
non (1 iters)           0.000001 seconds
threaded (1 threads)    0.000069 seconds
process (1 process)     0.002885 seconds
non (2 iters)           0.000001 seconds
threaded (2 threads)    0.000115 seconds
process (2 process)     0.003724 seconds
non (4 iters)           0.000002 seconds
threaded (4 threads)    0.000189 seconds
process (4 process)     0.004960 seconds
non (8 iters)           0.000003 seconds
threaded (8 threads)    0.000364 seconds
process (8 process)     0.007469 seconds

"""

```

[参考](https://github.com/lanzhiwang/python3-standard-library-example/blob/master/source/05_threading/evaluating_performances.py)
