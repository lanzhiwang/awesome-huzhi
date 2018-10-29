# Awesome huzhi [![](https://github.com/lanzhiwang/awesome-huzhi/blob/master/images/awesome.svg)](https://github.com/lanzhiwang/awesome-huzhi)

学习心得，笔记，资源汇总等.

Author: `huzhi`


- [Awesome huzhi](#awesome-huzhi)

    - [Python](#python)

    - [Linux](#linux)

    - [MySQL](#mysql)

    - [Docker/Kubernetes](#dockerkubernetes)

    - [Component](#component)

    - [分布式](#分布式)

    - [PHP](#php)

    - [go](#go)

    - [Android 逆向](#android)

    - [机器学习](#机器学习)

    - [计算机基础](#计算机基础)

    - [JavaScript](#javascript)

    - [Internet Awesome](#internet-awesome)

    - [Other](#other)

    - [Book](#book)


## python

* [pool](https://github.com/lanzhiwang/pool) - Python 进程池，线程池，连接池等的实现方法

* [Python并行编程](https://github.com/lanzhiwang/Python_Parallel_Programming)

    1. 基于线程的并行 - `threading`

    2. 基于进程的并行 - `multiprocessing`

    3. 异步编程 - `async` `concurrent` `gevent`

    4. 分布式Python - `celery` `RPC`

* Python 源码阅读

    * [Python 源码阅读最佳实践](https://github.com/lanzhiwang/awesome-huzhi/wiki/Source-reading)

    * Python 源码阅读列表
        * [bottle](https://github.com/bottlepy/bottle)
        * [records](https://github.com/kennethreitz/records)
        * [delegator.py](https://github.com/kennethreitz/delegator.py)
        * [maya](https://github.com/kennethreitz/maya)
        * [howdoi](https://github.com/gleitz/howdoi)
        * [Diamond](https://github.com/python-diamond/Diamond)
        * [tablib](https://github.com/kennethreitz/tablib)
        * [requests](https://github.com/requests/requests)
        * [werkzeug](https://github.com/pallets/werkzeug)
        * [flask](https://github.com/pallets/flask)
        * [fuqit](https://github.com/zedshaw/fuqit) - The FuqIt Web Framework

* 深入理解 Python ( 参考 [流畅的Python](https://github.com/fluentpython/example-code) )
    * [Python 数据模型](https://github.com/fluentpython/example-code/tree/master/01-data-model)
    * Python 数据结构
    	* [序列](https://github.com/fluentpython/example-code/tree/master/02-array-seq)
    	* [字典和集合](https://github.com/fluentpython/example-code/tree/master/03-dict-set)
    	* [文本和字节序列](https://github.com/fluentpython/example-code/tree/master/04-text-byte)
    * Python 函数
    * Python 面向对象
        * Python 风格的对象
        * [Python 抽象基类](https://github.com/fluentpython/example-code/tree/master/11-iface-abc)
        * [Python 多继承](https://github.com/fluentpython/example-code/tree/master/12-inheritance)
    * Python流程控制
    	* [可迭代对象、迭代器和生成器](https://github.com/fluentpython/example-code/tree/master/14-it-generator)
    	* 上下文管理器和else块
    	* 协程
    * 元编程
    	* [动态属性和特性](https://github.com/fluentpython/example-code/tree/master/19-dyn-attr-prop)
    	* [属性描述符](https://github.com/fluentpython/example-code/tree/master/20-descriptor)
    	* [类元编程](https://github.com/fluentpython/example-code/tree/master/21-class-metaprog)

* [python-patterns](https://github.com/lanzhiwang/python-patterns) - 常见设计模式UML类图说明-Python实现

* [learn-wsgiref](https://github.com/lanzhiwang/learn-wsgiref) - `wsgi`规范UML说明和相关实现

* [first-diy-framework](https://github.com/lanzhiwang/first-diy-framework) - 自定义 Python 框架和`asyncio`实现

* [lsbaws](https://github.com/rspivak/lsbaws) - 使用`socket`构建简单的`web`服务器

* [learn_bottle](https://github.com/lanzhiwang/awesome-huzhi/wiki/learn_bottle) - `bottle`框架中常见类的UML图

* [pyguide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md) - python代码规范

* [thread_signal](https://github.com/lanzhiwang/Python/blob/master/thread_signal.py) - 线程响应`ctrl+c`信号退出

* [data_analysis](https://github.com/lanzhiwang/data_analysis) -`Numpy`、`Pandas`、`Scipy`、`Matplotlib`的使用方法([参考文档](https://github.com/donnemartin/data-science-ipython-notebooks))

* [records](https://github.com/lanzhiwang/records) - 使用 UML 类图说明`records`设计架构

* [SQLAlchemy example](https://github.com/lanzhiwang/awesome-huzhi/wiki/SQLAlchemy-example) - `SQLAlchemy`示例说明 SQLAlchemy 的使用方法

* [Python 技巧](https://github.com/lanzhiwang/awesome-huzhi/wiki/Python_Tips)
	* [有趣实用的代码片段](https://github.com/satwikkansal/wtfPython)

* [布隆过滤器](https://github.com/jaybaird/python-bloomfilter)

* [Python 脚本到打包项目的标准化指南](http://veekaybee.github.io/2017/09/26/python-packaging/)

* [Python 项目标准结构](https://www.kennethreitz.org/essays/repository-structure-and-python)

* [Python 线程安全](https://github.com/lanzhiwang/awesome-huzhi/wiki/python-thread-safe)

* [Python 对象序列化](https://github.com/lanzhiwang/awesome-huzhi/wiki/Python-object-serialization)

* [Python 深复制和浅复制](https://github.com/fluentpython/example-code/blob/master/08-obj-ref/bus.py)

* [Python 弱引用](https://github.com/fluentpython/example-code/blob/master/08-obj-ref/cheese.py)

* [Python 对象可散列](https://github.com/lanzhiwang/awesome-huzhi/wiki/Python-object-hash)

* [Python 动态导入](https://github.com/lanzhiwang/awesome-huzhi/wiki/python-dynamic-import)

* [不太常见的包或者模块、函数](https://github.com/lanzhiwang/awesome-huzhi/wiki/Less-common-packages-or-modules-or-functions)

* 不太常见的Python语言特性
	* [exec-eval](https://anandology.com/python-practice-book/functional-programming.html#exec-eval)
	* [魔术方法](https://rszalski.github.io/magicmethods/)

* Python 虚拟环境
	* 解决依赖包问题: virtualenv
	* 解决 python 版本问题: pyenv

* [Python3 实例教程](https://github.com/jerry-git/learn-python3)

* [爬虫采集和调度框架](https://github.com/lanzhiwang/awesome-huzhi/blob/master/images/Reptile_frame.png)

* [httpie 使用说明](https://keelii.com/2018/09/03/HTTPie/)

* [将 python 源码编译成 exe 文件](https://www.ctolib.com/topics-119121.html)


## Linux

* shell 编程

	* [pure-bash-bible](https://github.com/dylanaraps/pure-bash-bible) - shell 字符串，变量，循环，文件处理等的高效处理方法

	* [shell](https://google.github.io/styleguide/shell.xml) - shell代码规范

* [Linux 使用技巧](https://github.com/jlevy/the-art-of-command-line)

* [unix/linux 命令列表及说明](https://github.com/lanzhiwang/awesome-huzhi/wiki/unix-linux-command-list)

* [free 命令输出详解](https://github.com/lanzhiwang/awesome-huzhi/wiki/free-output-explanation)

* [ uptime 命令输出 linux 负载说明](https://github.com/lanzhiwang/awesome-huzhi/wiki/linux-load-explanation)

* vim 常见操作

* Linux常见命令使用示例

	* [https://cheat.sh/](https://cheat.sh/)

	* [cheat.sh](https://github.com/chubin/cheat.sh)

	* [tldr](https://github.com/lanzhiwang/tldr)

* [Linux-Explore](https://github.com/lanzhiwang/awesome-huzhi/wiki/Linux-Explore) - 了解Linux服务器

* openssl、gpg

* firewall、[iptables](https://github.com/lanzhiwang/awesome-huzhi/blob/master/iptables.md)

* whiptail - 创建交互式shell脚本对话框

* [代理服务、翻墙](https://github.com/lanzhiwang/awesome-huzhi/wiki/%E4%BB%A3%E7%90%86%E6%9C%8D%E5%8A%A1)

* [nginx uwsgi flask](https://github.com/lanzhiwang/awesome-huzhi/blob/master/nginx_uwsgi_flask.md)


## MySQL

* 事务特性

	* [ACID](https://github.com/donnemartin/system-design-primer#relational-database-management-system-rdbms)

* 事务并发时的问题

    1. 脏读

    2. 不可重复读

    3. 幻读

* 事务隔离级别([事务隔离级别测试准备工作](https://github.com/lanzhiwang/awesome-huzhi/wiki/mysql-transaction-isolation#%E4%BA%8B%E5%8A%A1%E9%9A%94%E7%A6%BB%E7%BA%A7%E5%88%AB%E6%B5%8B%E8%AF%95%E5%87%86%E5%A4%87%E5%B7%A5%E4%BD%9C))

    1. [读未提交(read-uncommitted)](https://github.com/lanzhiwang/awesome-huzhi/wiki/mysql-transaction-isolation#%E8%AF%BB%E6%9C%AA%E6%8F%90%E4%BA%A4read-uncommitted)

    2. [不可重复读(read-committed)](https://github.com/lanzhiwang/awesome-huzhi/wiki/mysql-transaction-isolation#%E4%B8%8D%E5%8F%AF%E9%87%8D%E5%A4%8D%E8%AF%BBread-committed)

    3. [可重复读(repeatable-read)](https://github.com/lanzhiwang/awesome-huzhi/wiki/mysql-transaction-isolation#%E5%8F%AF%E9%87%8D%E5%A4%8D%E8%AF%BBrepeatable-read)

    4. [串行化(serializable)](https://github.com/lanzhiwang/awesome-huzhi/wiki/mysql-transaction-isolation#%E4%B8%B2%E8%A1%8C%E5%8C%96serializable)

* 锁表、锁数据行、异步处理

* [MySQL 表锁](https://github.com/lanzhiwang/awesome-huzhi/wiki/mysql-lock)

* [InnoDB记录存储结构、InnoDB数据页结构、MySQL的索引](https://github.com/lanzhiwang/awesome-huzhi/wiki/MySQL-index)

* 数据库分库分表方案

* [水平分表后页面分页处理办法](https://github.com/lanzhiwang/awesome-huzhi/wiki/mysql-sub-table)

* MySQL的压测工具 - mysqlslap


## Docker/Kubernetes

* [Docker 基础命令](https://github.com/lanzhiwang/awesome-huzhi/blob/master/docker/docker_base_operate.md)

* [docker compose](https://github.com/lanzhiwang/awesome-huzhi/blob/master/docker/docker_compose.md)

* [Docker 在单一主机上的网络原理](https://github.com/lanzhiwang/awesome-huzhi/blob/master/docker/docker_network.md)

* [Docker 跨主机访问原理](https://github.com/lanzhiwang/awesome-huzhi/blob/master/docker/multi-network.md)

* [docker swarm](https://github.com/lanzhiwang/awesome-huzhi/blob/master/docker/docker_swarm.md)

* [Docker 数据管理](https://github.com/lanzhiwang/awesome-huzhi/blob/master/docker/data_manager.md)

* [Docker/Kubernetes线路图](https://github.com/lanzhiwang/awesome-huzhi/wiki/docker-and-kubernetes)

* [Linux 容器技术基础](http://pierrchen.blogspot.com/2018/08/understand-container-index.html)


## Component

* KVM

* [ZooKeeper](https://github.com/lanzhiwang/awesome-huzhi/wiki/ZooKeeper-base)

* Etcd

* [Redis](https://github.com/lanzhiwang/awesome-huzhi/wiki/redis)

* MongoDB

* Elasticsearch

* [RabbitMQ](https://github.com/lanzhiwang/awesome-huzhi/wiki/RabbitMQ)

* [Kafka](https://github.com/lanzhiwang/awesome-huzhi/wiki/kafka-base)

* jenkins

* IMAP/POP3/STMP

* Hadoop生态
    * Hadoop
    * HDFS-文件系统
    * MapReduce-计算框架
    * Yarn-调度器
    * Zookeeper-类似于etcd
    * Hive-通过SQL简化MapReduce操作
    * Pig-通过pig语言简化MapReduce操作
    * Hue-通过web页面操作HDFS，MapReduce，hive等
    * Oozie-类似于Yarn
    * Sqoop-将关系型数据库数据导入Hadoop
    * Flume-将日志导入Hadoop
    * Kafka-队列
    * Hbase-数据库
    * Spark-流式计算框架

* Storm


## 分布式

* 分布式理论

	* [CAP theorem](https://github.com/donnemartin/system-design-primer#cap-theorem)

	* [分布式系统中的幂等性](https://www.cnblogs.com/vveiliang/p/6643874.html)

* [分布式系统介绍](https://hackernoon.com/a-thorough-introduction-to-distributed-systems-3b91562c9b3c)

* 分布式系统存在的问题

	* [拜占庭将军问题](https://github.com/lanzhiwang/awesome-huzhi/wiki/The_Byzantine_General_Problem)

* 分布式协议

	* Paxos

	* [Raft](https://github.com/lanzhiwang/awesome-huzhi/wiki/raft)

* 分布式实现

	* 分布式文件系统
		* [seaweedfs](https://github.com/chrislusf/seaweedfs)
		* [fastdfs](https://github.com/happyfish100/fastdfs)
		* [分布式文件系统选型要考虑的问题](https://github.com/lanzhiwang/awesome-huzhi/wiki/distributed-file-system)

	* [一致性hash](https://github.com/lanzhiwang/awesome-huzhi/wiki/Consistency-Hash)

	* [分布式 id 生成器](https://chai2010.cn/advanced-go-programming-book/ch6-cloud/ch6-01-dist-id.html)

	* [分布式锁](https://chai2010.cn/advanced-go-programming-book/ch6-cloud/ch6-02-lock.html)

	* [分布式配置管理](https://chai2010.cn/advanced-go-programming-book/ch6-cloud/ch6-06-config.html)

	* [分布式爬虫](https://chai2010.cn/advanced-go-programming-book/ch6-cloud/ch6-07-crawler.html)


## PHP

* [php_di](https://github.com/lanzhiwang/php_di) - 简单的 PHP 依赖注入示例

* [database_connection_pool](https://github.com/lanzhiwang/database_connection_pool) - 在 PHP 中使用 pdo 驱动和 gearman 实现的数据库连接池

* [FastRoute](https://github.com/lanzhiwang/FastRoute) - PHP 框架中的路由实现

* [curl_handle](https://github.com/lanzhiwang/curl_handle) - PHP 扩展`curl`封装

* [guzzle](https://github.com/lanzhiwang/guzzle) - PHP 中 `HTTP` 请求的客户端封装

* [firstFramework](https://github.com/lanzhiwang/firstFramework) - 自定义 PHP 框架


## go

* [go-example](https://github.com/lanzhiwang/go-example) - go example

* [go-design-patterns](https://github.com/lanzhiwang/go-design-patterns) - 常见设计模式UML类图说明-go实现

* [web 自定义框架](https://github.com/lanzhiwang/web)

* [go 模块介绍](https://roberto.selbach.ca/intro-to-go-modules/)

* [Go 与 Python 的比较, 介绍 Go 语言对比 Python 的优点](https://thinkfaster.co/2018/07/goodbye-python-hello-go/)

* [Go 语言的语法和各种细节的开源电子书，深入彻底地了解 Go](https://go101.org/article/101.html)

## Android

* [安卓基础](https://github.com/lanzhiwang/awesome-huzhi/blob/master/Android.md)

* [安卓应用攻击面](https://github.com/lanzhiwang/awesome-huzhi/blob/master/Android_application_attack_surface.md)

* [AndroidViewClient](https://github.com/lanzhiwang/AndroidViewClient) - 获取安卓界面上的控件坐标用于沙箱运行

* [apk-Dynamic-Analysis](https://github.com/lanzhiwang/apk-Dynamic-Analysis) - 常见APK逆向分析工具使用方法

* [android-emulator](https://github.com/tracer0tong/android-emulator) - docker 运行安卓模拟器

* [命令行构建 APK 文件](https://github.com/lanzhiwang/apk-Dynamic-Analysis/blob/master/apk_build.md)

* 安卓常见逆向工具列表
    * Android Studio

    * android-sdk

    * Apktool

    * Dex2jar/JD-GUI

    * Burp suite

    * Drozer

    * QARK

    * Droid Explorer

    * Cydia substrate/Introspy

    * Frida

    * Inspeckage

    * cuckoo

    * wifiphisher


## 机器学习

* [人工智能、机器学习、深度学习的关系](https://github.com/lanzhiwang/awesome-huzhi/blob/master/images/artificial_intelligence_Machine_learning_Deep_learning.png)

* [机器学习常见算法](https://github.com/lanzhiwang/awesome-huzhi/wiki/Machine-learning-common-algorithm)

* `线性回归模型`、`逻辑回归模型`、`卷积神经网络(CNN)`等模型的数学公式 :
  $$
  y = (wx + b) + noise
  $$

* `循环神经网络(RNN)`的数学公式常见算法 : 
  $$
  h_{t} = \tanh(W_{x}x_{t} + W_{h}h_{t-1}$ + b)
  $$

* [代码学习](https://github.com/lanzhiwang/awesome-huzhi/wiki/machine-learning-example)

* [fastText 使用示例](https://github.com/lanzhiwang/awesome-huzhi/blob/master/fastText.md)

* 《Python神经网络编程》

* [《TensorFlow学习指南:深度学习系统构建详解》](https://github.com/Hezi-Resheff/Oreilly-Learning-TensorFlow)

* [tensorflow_cookbook](https://github.com/nfmcclure/tensorflow_cookbook)

* 《深度学习入门 基于Python的理论与实现》

* [机器学习50个最佳免费数据集](https://gengo.ai/datasets/the-50-best-free-datasets-for-machine-learning/)



## 计算机基础

* [tcp/ip](https://github.com/lanzhiwang/awesome-huzhi/wiki/tcp-ip-status) - tcp 连接和断开过程以及过程中进程的状态
* [长连接和短连接](https://github.com/lanzhiwang/awesome-huzhi/blob/master/long_connection_and_short_connection.md)
* [nginx 支持长连接](https://github.com/lanzhiwang/awesome-huzhi/blob/master/nginx_keep_alive.md)
* [system-design-primer](https://github.com/donnemartin/system-design-primer) - 设计可扩展系统
* [代码整洁之道](https://github.com/lanzhiwang/awesome-huzhi/wiki/clean-code)
* [HTTPS图解](https://tls.ulfheim.net/)


## JavaScript

* [jstips](https://github.com/loverajoel/jstips) - 常见 JavaScript 陷阱

* w3c school

* 前端浏览器

	* [phantomjs](https://github.com/ariya/phantomjs)

	* [puppeteer](https://github.com/GoogleChrome/puppeteer)

	* [chromium](https://github.com/chromium/chromium)

* 数据可视化

	* JavaScript数据可视化编程

* [Puppeteer 的使用](https://docs.browserless.io/blog/2018/06/04/puppeteer-best-practices.html)


## Internet-Awesome

* [awesome-python](https://github.com/vinta/awesome-python)

* [awesome-interview-questions](https://github.com/MaximAbramchuck/awesome-interview-questions)


## Other

* [Hack](https://github.com/source-foundry/Hack) - 编程专用字体

* [ffmpeg](https://github.com/lanzhiwang/awesome-huzhi/blob/master/ffmpeg.md) - ffmpeg 是一个非常快速的视频和音频转换器，也可以从现场音频/视频源获取。 它还可以在任意采样率之间进行转换，并使用高质量的多相滤波器动态调整视频大小。

* [thumbor](https://github.com/thumbor/thumbor) - Thumbor是一种智能成像服务。 它支持按需裁剪，调整大小和翻转图像。

* [you-get](https://github.com/soimort/you-get) - 视频、音频、图片下载工具

* [asciify](https://github.com/RameshAditya/asciify) - Convert Images into ASCII Art with the power of Python

* [face_recognition](https://github.com/ageitgey/face_recognition) - 人脸识别

* Markdown

	* [haroopress](http://pad.haroopress.com/)、[typora](https://typora.io/)

	* [vnote](https://github.com/tamlok/vnote)

## Book

* Python

	* 图灵程序设计丛书:Python基础教程(第2版)

	* 流畅的Python (图灵程序设计丛书)

	* Effective Python:编写高质量Python代码的59个有效方法

	* Python 并行编程手册

	* Python 参考手册

	* Python核心编程(第3版)

	* Python编程之美(最佳实践指南)

	* Python网络编程攻略 (图灵程序设计丛书)

	* Python极客项目编程

	* Flask Web开发 基于Python的Web应用开发实战 (图灵程序设计丛书)

	* Python Web开发 测试驱动方法 (图灵程序设计丛书)

	* Python数据分析基础教程：NumPy学习指南（第2版）

	* Python数据可视化编程实战 第2版

	* Selenium自动化测试 基于 Python 语言

	* Python高手之路

* Linux

    * 鸟哥的Linux私房菜:基础学习篇(第3版)

    * 鸟哥的Linux私房菜:服务器架设篇

    * Linux Shell脚本攻略 第3版

    * Shell 从入门到精通

    * UNIXLinux系统管理技术手册 第4版

    * Linux Performance and Tuning Guidelines

* Docker

    * 第一本Docker书

    * Docker经典实例 (图灵程序设计丛书)

    * 每天5分钟玩转Docker容器技术

    * 每天5分钟玩转Kubernetes

* go

	* The Go Programming Language (英语)

	* Go并发编程实战(第2版)

	* Go语言入门经典

	* Go语言实战

	* Go Web编程

	* 微服务设计

	* [Go语言高级编程](https://github.com/chai2010/advanced-go-programming-book)

* MySQL

	* 高性能MySQL(第3版)

	* MySQL数据库入门

	* MySQL技术内幕(第5版)

	* 深入浅出MySQL:数据库开发、优化与管理维护(第2版)

* Android

	* Android安全攻防实践

	* Android恶意代码分析与渗透测试

* other

    * Kafka权威指南

    * Redis 4.x Cookbook中文版

    * 写给大忙人的Hadoop 2

    * 大型网站技术架构:核心原理与案例分析

    * Wireshark网络分析的艺术

    * HTTP权威指南

    * 数学之美(第二版)

    * 啊哈!算法

    * 图解密码技术(第3版)

    * 深入理解计算机系统(原书第3版)

    * 从Paxos到Zookeeper:分布式一致性原理与实践
