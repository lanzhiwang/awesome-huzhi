# Awesome huzhi [![](https://github.com/lanzhiwang/awesome-huzhi/blob/master/images/awesome.svg)](https://github.com/lanzhiwang/awesome-huzhi)

学习心得，笔记，资源汇总等.

Author: `huzhi`


- [Awesome huzhi](#awesome-huzhi)

    - [Python](#python)

    - [Linux](#linux)

    - [MySQL](#mysql)

    - [Component](#component)

    - [分布式](#分布式)

    - [PHP](#php)

    - [go](#go)

    - [Android 逆向](#android)

    - [Computer-Base](#computer-base)

    - [JavaScript](#javascript)

    - [Internet Awesome](#internet-awesome)

    - [Other](#other)

    - [Book](#book)


## python

* [records](https://github.com/lanzhiwang/records) - 使用 UML 类图说明`records`设计架构

* [SQLAlchemy example](https://github.com/lanzhiwang/awesome-huzhi/wiki/SQLAlchemy-example) - `SQLAlchemy`示例说明 SQLAlchemy 的使用方法

* [pool](https://github.com/lanzhiwang/pool) - Python 进程池，线程池，连接池等的实现方法

* [thread_signal](https://github.com/lanzhiwang/Python/blob/master/thread_signal.py) - 线程响应`ctrl+c`信号退出

* [pyguide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md) - python代码规范

* [data_analysis](https://github.com/lanzhiwang/data_analysis) -`Numpy`、`Pandas`、`Scipy`、`Matplotlib`的使用方法([参考文档](https://github.com/donnemartin/data-science-ipython-notebooks))

* [learn_bottle](https://github.com/lanzhiwang/awesome-huzhi/wiki/learn_bottle) - `bottle`框架中常见类的UML图

* [python-patterns](https://github.com/lanzhiwang/python-patterns) - 常见设计模式UML类图说明-Python实现

* [learn-wsgiref](https://github.com/lanzhiwang/learn-wsgiref) - `wsgi`规范UML说明和相关实现

* [first-diy-framework](https://github.com/lanzhiwang/first-diy-framework) - 自定义 Python 框架和`asyncio`实现

* [lsbaws](https://github.com/rspivak/lsbaws) - 使用`socket`构建简单的`web`服务器

* Python并行编程方法

    1. 基于线程的并行 - `threading`

    2. 基于进程的并行 - `multiprocessing`

    3. 异步编程 - `async` `concurrent` `gevent`

    4. 分布式Python - `celery` `RPC`

* [Python 技巧](https://github.com/lanzhiwang/awesome-huzhi/wiki/Python_Tips)
	* [有趣实用的代码片段](https://github.com/satwikkansal/wtfPython)

* [布隆过滤器](https://github.com/jaybaird/python-bloomfilter)

* [Python 脚本到打包项目的标准化指南](http://veekaybee.github.io/2017/09/26/python-packaging/)

* [Python项目标准结构](https://www.kennethreitz.org/essays/repository-structure-and-python)

* 不太常见的包或者模块

	* Logbook 日志
    * maya 日期和时间
    * delegator 在Python中执行shell命令
	* Ansible 自动化运维

* 不太常见的Python语言特性
	* [exec-eval](https://anandology.com/python-practice-book/functional-programming.html#exec-eval)
	* [Mixins and Python](https://www.ianlewis.org/en/mixins-and-python)
	* [魔术方法](https://rszalski.github.io/magicmethods/)


## Linux

* shell 编程

	* [pure-bash-bible](https://github.com/dylanaraps/pure-bash-bible) - shell 字符串，变量，循环，文件处理等的高效处理方法

	* [shell](https://google.github.io/styleguide/shell.xml) - shell代码规范

* [free 命令输出详解](https://github.com/lanzhiwang/awesome-huzhi/wiki/free-output-explanation)

* [ uptime 命令输出 linux 负载说明](https://github.com/lanzhiwang/awesome-huzhi/wiki/linux-load-explanation)

* vim 常见操作

* Linux常见命令使用示例

	* [https://cheat.sh/](https://cheat.sh/)

	* [cheat.sh](https://github.com/chubin/cheat.sh)

	* [tldr](https://github.com/lanzhiwang/tldr)

* [Linux-Explore](https://github.com/lanzhiwang/awesome-huzhi/wiki/Linux-Explore) - 了解Linux服务器

* openssl、gpg

* firewall、iptables


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


## Component

* KVM

* ZooKeeper

* Etcd

* Redis

* MongoDB

* Elasticsearch

* RabbitMQ

* Kafka

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

* 分布式系统存在的问题

	* [拜占庭将军问题](https://github.com/lanzhiwang/awesome-huzhi/wiki/The_Byzantine_General_Problem)

* 分布式协议

	* Paxos

	* [Raft](https://www.cnblogs.com/mindwind/p/5231986.html)

* 分布式实现

	* 分布式文件系统

		* 分布式文件系统选型要考虑的问题

	* 一致性hash

	* 分布式 id 生成器

	* 分布式锁

	* 分布式配置管理

	* 分布式爬虫


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


## Android

* [AndroidViewClient](https://github.com/lanzhiwang/AndroidViewClient) - 获取安卓界面上的控件坐标用于沙箱运行

* [apk-Dynamic-Analysis](https://github.com/lanzhiwang/apk-Dynamic-Analysis) - 常见APK逆向分析工具使用方法

* [android-emulator](https://github.com/tracer0tong/android-emulator) - docker 运行安卓模拟器

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


## Computer-Base

* [tcp/ip](https://github.com/lanzhiwang/awesome-huzhi/wiki/tcp-ip-status) - tcp 连接和断开过程以及过程中进程的状态

* [system-design-primer](https://github.com/donnemartin/system-design-primer) - 设计可扩展系统


## JavaScript

* [jstips](https://github.com/loverajoel/jstips) - 常见 JavaScript 陷阱

* w3c school

* phantomjs、puppeteer、chromium

* 数据可视化

	* JavaScript数据可视化编程


## Internet-Awesome

* [awesome-python](https://github.com/vinta/awesome-python)

* [awesome-interview-questions](https://github.com/MaximAbramchuck/awesome-interview-questions)


## Other

* [Hack](https://github.com/source-foundry/Hack) - 写代码专用的字体


## Book

* Python

	* 图灵程序设计丛书:Python基础教程(第2版)

	* 流畅的Python (图灵程序设计丛书)

	* Effective Python:编写高质量Python代码的59个有效方法

	* Python 并行编程手册

	* Python 参考手册

	* Python核心编程(第3版)

	* Python网络编程攻略 (图灵程序设计丛书)

	* Python神经网络编程

	* Python极客项目编程

	* Flask Web开发 基于Python的Web应用开发实战 (图灵程序设计丛书)

	* Python Web开发 测试驱动方法 (图灵程序设计丛书)

	* Python数据分析基础教程：NumPy学习指南（第2版）

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

    * 大型网站技术架构:核心原理与案例分析

    * Wireshark网络分析的艺术

    * HTTP权威指南

    * 数学之美(第二版)

    * 啊哈!算法

    * 图解密码技术(第3版)

    * 深入理解计算机系统(原书第3版)

    * 从Paxos到Zookeeper:分布式一致性原理与实践

