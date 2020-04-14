# Celery-4.1 用户指南: Concurrency

翻译[libing_thinking](https://me.csdn.net/u013148156) 最后发布于2017-11-22 17:40:44 阅读数 1644 收藏

展开

Release: 4.1
Date: 2017年8月18日

## 使用 Eventlet 实现并发

------

### 简介

------

`Eventlet` 的主页对它进行了描述；它是一个python的并发网络库，可以让你更改如何运行你的代码而不是怎么编写代码。

- 对高可扩展非阻塞IO操作，它使用 epoll或者libevent。
- `Coroutines` 使得开发者使用一个类似于线程的阻塞式编程风格，但是却能提供非阻塞IO的好处。
- 事件的分发是隐式的：意味着你可以很容易的从python解释器中使用Eventlet，或者作为一个大应用的一部分。

Celery 支持 Eventlet 作为一种可选的执行池实现。在有些情况下，它比 prefork 更优，但是你需要确保你的任务不会执行阻塞调用，因为这会阻塞工作单元中所有其他操作直到阻塞调用返回。

prefork 池能使用多个进程，但是通常每个CPU限制在少数几个进程。使用 Eventlet，你可以高效的开启成百上千个 green-thread。对一个消息源系统进行的一个非正式的测试显示 Eventlet 池可以每秒获取和处理数百个消息，而 prefork 池处理100个 消息源使用了14秒。注意这是异步IO优势明显的一个应用示例（异步http请求）。你可能想混合使用 Eventlet 和 prefork 工作单元，并且根据兼容性和哪个工作更佳来将任务路由到相应工作单元。

### 启用 Eventlet

------

你可以通过使用工作单元的 `celery worker -P` 选项启用 Eventlet 池：

```
$ celery -A proj worker -P eventlet -c 10001
```

### 示例

------

查看celery发布中的 `Eventlet example` 文件夹获取更多使用 Eventlet 的示例。

- [点赞](javascript:;)
- [收藏](javascript:;)
- [分享](javascript:;)



https://blog.csdn.net/u013148156/article/details/78606278

