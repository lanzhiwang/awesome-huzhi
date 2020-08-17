# Awesome huzhi [![](https://github.com/lanzhiwang/awesome-huzhi/blob/master/images/awesome.svg)](https://github.com/lanzhiwang/awesome-huzhi)

学习心得，笔记，资源汇总等.

Author: `huzhi`


- [Awesome huzhi](#awesome-huzhi)
    - [Python](#python)

    - [Linux](#linux)

    - [MySQL](#mysql)

    - [Docker/Kubernetes](#dockerkubernetes)

    - [常见数据结构和算法](#algorithm)

    - [邮件系统](#email)

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
* [python 多进程处理数据库操作](./python/DB_pool/pool.py)
* [python 数据库连接池实现--DBUtils](./python/DBUtils_User_Guide.md)
* [数据库 DB-API 2 标准实现](https://github.com/lanzhiwang/DBUtils-learn/blob/master/DBUtils/Tests/mock_db.py)
* [Python并行编程](https://github.com/lanzhiwang/Python_Parallel_Programming)（**如何选择并行编程的模型？？**）

* Python 源码阅读

    * [Python 源码阅读最佳实践](https://github.com/lanzhiwang/awesome-huzhi/wiki/Source-reading)

    * Python 源码阅读列表
        * [bottle](https://github.com/bottlepy/bottle)
        * [records](https://github.com/kennethreitz/records)
        * [delegator.py](https://github.com/kennethreitz/delegator.py)
        * [maya](https://github.com/kennethreitz/maya)
        * [flask](https://github.com/pallets/flask)
* [流畅的Python](https://github.com/fluentpython/example-code) 
* [python-patterns](https://github.com/lanzhiwang/python-patterns) - 常见设计模式UML类图说明-Python实现
* [gevent 用法示例](https://github.com/lanzhiwang/gevent_example/tree/master/examples)
* [learn-wsgiref](https://github.com/lanzhiwang/learn-wsgiref) - `wsgi`规范UML说明和相关实现
* [first-diy-framework](https://github.com/lanzhiwang/first-diy-framework) - 自定义 Python 框架和`asyncio`实现
* [lsbaws](https://github.com/rspivak/lsbaws) - 使用`socket`构建简单的`web`服务器
* [learn_bottle](https://github.com/lanzhiwang/awesome-huzhi/wiki/learn_bottle) - `bottle`框架中常见类的UML图
* [为什么 Flask 相对 Django 是一个轻量级框架](./python/Flask_microframework.md)
* [data_analysis](https://github.com/lanzhiwang/data_analysis) -`Numpy`、`Pandas`、`Scipy`、`Matplotlib`的使用方法([参考文档](https://github.com/donnemartin/data-science-ipython-notebooks))
* [records](https://github.com/lanzhiwang/records) - 使用 UML 类图说明`records`设计架构
* [SQLAlchemy example](./python/SQLAlchemy/SQLAlchemy.md) - `SQLAlchemy`示例说明 SQLAlchemy 的使用方法
* [Python 技巧](https://github.com/lanzhiwang/awesome-huzhi/wiki/Python_Tips)
  * [有趣实用的代码片段](https://github.com/satwikkansal/wtfPython)
* [布隆过滤器](./python/BloomFilter.md)
* [Python 脚本到打包项目的标准化指南](./python/packaging_standardization.md)
* [Python 项目标准结构](./python/Repository_Structure_and_Python.md)
* [Python 线程安全，全局变量，局部变量](https://github.com/lanzhiwang/awesome-huzhi/blob/master/python/python_thread_safe.md)
* [Python 对象序列化](https://github.com/lanzhiwang/awesome-huzhi/wiki/Python-object-serialization)
* [python logging 实践](https://github.com/lanzhiwang/awesome-huzhi/blob/master/python/python_logging.md)
* [Python 深复制和浅复制](./python/python_copy_deepcopy.md)
* [Python 弱引用](https://github.com/fluentpython/example-code/blob/master/08-obj-ref/cheese.py)
* [Python 动态导入](https://github.com/lanzhiwang/awesome-huzhi/wiki/python-dynamic-import)
* [Python 函数定义规则](./python/fun_def.md)
* [yield_and_yield_from](./python/Python_yield.md)
* [魔术方法](./python/Magic_Methods.md)
* [\_\_slots\_\_魔术方法说明](./python/__slots__%20.md)
* [new 和 init 代码示例](./python/new_init_example.md)、[\_\_new\_\_() and \_\_init\_\_()](./python/new_and_init.md)
* [getattr_and_getattribute](./python/getattr_and_getattribute.md)
* [Python 对象 hash](./python/Python_Hashes_and_Equality.md)
* [exec-eval](./python/exec_eval.md)
* [Python 函数重载](https://github.com/lanzhiwang/awesome-huzhi/blob/master/python/python_Overload.md)
* Python 虚拟环境
  * 解决依赖包问题: virtualenv
  * 解决 python 版本问题: pyenv
* [Python3 实例教程](https://github.com/jerry-git/learn-python3)
* [python 实现单例模式](https://github.com/lanzhiwang/awesome-huzhi/blob/master/python/Python_Singleton.md)
* [python 全局解释器锁和性能测试](python/GIL.md)
* [flask 启动脚本](./python/flask_manager.md)
* [python 常见面试问题](https://github.com/taizilongxu/interview_python)
* [常见正则表达式](https://github.com/lanzhiwang/common-regex)
* web请求参数验证
* 解析大的 XML 文件
    * [分段读取文件内容](https://python3-cookbook.readthedocs.io/zh_CN/latest/c06/p04_parse_huge_xml_files_incrementally.html)
    * 在文件内容中做数据冗余
* [爬虫相关问题](https://github.com/lanzhiwang/Anti-Anti-Spider)
* [Selenium](./python/Selenium.md)
* [Python 相关文章](./python/python-articles.md)
* [Python - Extension Programming with C](./python/Python-Extension-Programming-with-C.md)

##

* [problem](./problem.md)

##

## Linux

* shell 编程

  * [pure-bash-bible](https://github.com/dylanaraps/pure-bash-bible) - shell 字符串，变量，循环，文件处理等的高效处理方法

  * [shell](https://google.github.io/styleguide/shell.xml) - shell代码规范
* [Linux 使用技巧](https://github.com/jlevy/the-art-of-command-line)
* [linux 系统初始化](https://github.com/lanzhiwang/awesome-huzhi/wiki/linux-%E7%B3%BB%E7%BB%9F%E5%88%9D%E5%A7%8B%E5%8C%96)
* [Linux 网口相互绑定 bond](https://github.com/lanzhiwang/awesome-huzhi/wiki/Linux-%E7%BD%91%E5%8F%A3%E7%9B%B8%E4%BA%92%E7%BB%91%E5%AE%9A-bond)
* [磁盘分区](https://github.com/lanzhiwang/awesome-huzhi/wiki/disk-partition)
* [free 命令输出详解](https://github.com/lanzhiwang/awesome-huzhi/wiki/free-output-explanation)
* [ uptime 命令输出 linux 负载说明](https://github.com/lanzhiwang/awesome-huzhi/wiki/linux-load-explanation)
* [Linux常见命令使用示例](https://cheat.sh/)
* [Linux-Explore](https://github.com/lanzhiwang/awesome-huzhi/wiki/Linux-Explore) - 了解Linux服务器
* [OpenSSL](./linux/OpenSSL.md)、gpg（**gpg私钥免密码如何实现？？**）
* firewall、[iptables](./linux/iptables/iptables.md)
* [ip 指令常见用法](./linux/linux_networl_dervice/01_ip.md)
* [nginx uwsgi flask](./linux/nginx_uwsgi_flask.md)
* [监控系统 prometheus 基本原理以及客户端的使用](./linux/Prometheus.md)
  * [Prometheus操作指南](https://github.com/yunlzheng/prometheus-book)
* [epel](https://fedoraproject.org/wiki/EPEL)、[elrepo](http://elrepo.org/tiki/tiki-index.php)
* [http curl wget](./linux/HTTPie_and_Curl_Wget.md)
* [curl 帮助](https://curl.haxx.se/docs/httpscripting.html)
* [Linux 异步事件模型--以redis事件模型为例](https://github.com/lanzhiwang/awesome-huzhi/blob/master/Redis/Redis_Event_Model.md)
* [使用 nginx 作为 yum 代理](./linux/nginx_yum_proxy.md)
* [pcap 包示例](https://wiki.wireshark.org/SampleCaptures)
* [僵尸进程、清理僵尸进程的父进程](https://coolshell.cn/articles/656.html)
* [page cache && buffer cache](https://github.com/lanzhiwang/awesome-huzhi/blob/master/images/page_cache_and_buffer_cache.jpg)
* [select、poll、epoll 异同](https://github.com/lanzhiwang/IO)
* [C10K 问题](./linux/C10K.md)
* [不下载文件但获取下载文件的大小](./linux/download_file_size.md)
* [nginx 直接在配置文件中切割日志](./linux/nginx_log.md)
* [nginx 内置变量](./linux/nginx_built-in_variable.md)
* nginx **增量部署**添加新的模块（nginx -V）
* [进程间通信（IPC）：管道（包括无名管道和命名管道）、消息队列、信号量、共享存储、信号、Socket、Streams](./linux/ipc.md)
* [服务端和客户端 SSL 链路](./linux/SSL.md)
* [haproxy 和 keepalived](./linux/haproxy_keepalived/haproxy_keepalived.md)
* [获取 HTTP 响应时间](./linux/http_response_time.md)
* [OpenSSH Config File](./linux/OpenSSH_Config_File_Examples.md)
* [SSH ProxyCommand](./linux/SSH_ProxyCommand_example.md)
* [nc 命令示例](./linux/nc.md)
* [syslog](./linux/syslog/README.md)
* [网络性能测试工具 iperf3 工具使用方法](./linux/iperf.md)
* [利用perf剖析Linux应用程序](https://blog.gmem.cc/perf)
* [Linux网络知识集锦](https://blog.gmem.cc/network-faq)
* [makefile 相关](./linux/makefile.md)

## MySQL

* [MySQL 基础](./MySQL/MySQL_README.md)
* 事务特性
  * 原子性、一致性、隔离性、持久性（ACID）
  	* [参考1](https://github.com/donnemartin/system-design-primer#relational-database-management-system-rdbms)
  	* [参考2](https://mp.weixin.qq.com/s?__biz=MzIxNTQ3NDMzMw==&mid=2247484093&idx=1&sn=b6c607e7d7845ad963fe2b0e1fa771e6&chksm=97968b4fa0e102595cfee0ed4bd9ba83a938e49914163c94ed2d22659b083daea58040c62113&mpshare=1&scene=23&srcid=#rd)
* 事务并发时的问题

    1. 脏读

    2. 不可重复读

    3. 幻读
* 事务隔离级别([事务隔离级别测试准备工作](https://github.com/lanzhiwang/awesome-huzhi/wiki/mysql-transaction-isolation#%E4%BA%8B%E5%8A%A1%E9%9A%94%E7%A6%BB%E7%BA%A7%E5%88%AB%E6%B5%8B%E8%AF%95%E5%87%86%E5%A4%87%E5%B7%A5%E4%BD%9C)) （**为什么要有四种事务隔离级别？**）

    1. [读未提交(read-uncommitted)](https://github.com/lanzhiwang/awesome-huzhi/wiki/mysql-transaction-isolation#%E8%AF%BB%E6%9C%AA%E6%8F%90%E4%BA%A4read-uncommitted)

    2. [不可重复读(read-committed)](https://github.com/lanzhiwang/awesome-huzhi/wiki/mysql-transaction-isolation#%E4%B8%8D%E5%8F%AF%E9%87%8D%E5%A4%8D%E8%AF%BBread-committed)

    3. [可重复读(repeatable-read)](https://github.com/lanzhiwang/awesome-huzhi/wiki/mysql-transaction-isolation#%E5%8F%AF%E9%87%8D%E5%A4%8D%E8%AF%BBrepeatable-read)

    4. [串行化(serializable)](https://github.com/lanzhiwang/awesome-huzhi/wiki/mysql-transaction-isolation#%E4%B8%B2%E8%A1%8C%E5%8C%96serializable)
    
    5. [MVCC, ReadView, 版本链](https://mp.weixin.qq.com/s?__biz=MzIxNTQ3NDMzMw==&mid=2247484119&idx=1&sn=e3637553f3e813f1e2f7f6a3bcd270a9&scene=19#wechat_redirect)
* [buffer pool, change buffer, log buffer](https://mp.weixin.qq.com/s/_njwO8EJAYtqVuIOZCTwOQ)
* [MySQL 锁](https://github.com/lanzhiwang/awesome-huzhi/blob/master/MySQL/mysql_lock.md)
* 异步处理
* 错误日志、通用查询日志、慢查询日志、二进制日志、中继日志、DDL 日志
* [InnoDB记录存储结构、InnoDB数据页结构、MySQL的索引](https://github.com/lanzhiwang/awesome-huzhi/wiki/MySQL-index)
* 索引条件下推（Index Condition Pushdown)
* [MySQL 外键约束](./MySQL/mysql-FOREIGN-KEY.md)
* 数据库分库分表方案
* [水平分表后页面分页处理办法](https://github.com/lanzhiwang/awesome-huzhi/wiki/mysql-sub-table)
* MySQL的压测工具 - mysqlslap
* [MySQL 协议](https://github.com/lanzhiwang/awesome-huzhi/blob/master/MySQL/mysql_login_agreement.pdf)
* [MySQL 博客](https://mysqlserverteam.com/)
* [MySQL主从同步过程](https://github.com/lanzhiwang/awesome-huzhi/blob/master/MySQL/MySQL_master_slave.pdf)
* [MySQL IO 过程](https://github.com/lanzhiwang/awesome-huzhi/blob/master/MySQL/MySQL_IO.pdf)
* [MyISAM 和 InnoDB 的区别](./MySQL/MyISAM_InnoDB_diff.md)
* [安装 MySQL 5.7](https://github.com/lanzhiwang/awesome-huzhi/wiki/%E5%AE%89%E8%A3%85-MySQL-5.7)


## Docker/Kubernetes

* [docker 相关问题](./docker/docker_readme.md)
* [Docker 基础命令](https://github.com/lanzhiwang/awesome-huzhi/blob/master/docker/docker_base_operate.md)
* [Docker 在单一主机上的网络原理](https://github.com/lanzhiwang/awesome-huzhi/blob/master/docker/docker_network.md)
* [docker 网络追踪](https://tonybai.com/2017/11/06/explain-docker-single-host-network-using-iptables-trace-and-ebtables-log/)
* [Docker 跨主机访问原理](https://github.com/lanzhiwang/awesome-huzhi/blob/master/docker/multi-network.md)
* [Swarm mode 与 Docker Swarm 的差异及改进之处](https://www.ibm.com/developerworks/cn/opensource/os-cn-docker-selenium-grid-test/index.html)
* Linux 容器技术基础
  * [DOCKER基础技术：LINUX NAMESPACE（上）](https://coolshell.cn/articles/17010.html)
  * [DOCKER基础技术：LINUX NAMESPACE（下）](https://coolshell.cn/articles/17029.html)
  * [DOCKER基础技术：LINUX CGROUP](https://coolshell.cn/articles/17049.html)
  * [DOCKER基础技术：AUFS](https://coolshell.cn/articles/17061.html)
  * [DOCKER基础技术：DEVICEMAPPER](https://coolshell.cn/articles/17200.html)
  * [DOCKER基础技术：overlayfs](https://github.com/lanzhiwang/awesome-huzhi/blob/master/docker/overlayfs.pdf)
  * [understand-container-index](http://pierrchen.blogspot.com/2018/08/understand-container-index.html)
* [Docker 的 Image 文件是分层的，本文简单介绍怎么查看每一层的内容，它们又是怎么组合成一个可以运行的 Image 文件](https://cameronlonsdale.com/2018/11/26/whats-in-a-docker-image/)
* [通过控制分层来缩小 Image 文件尺寸](https://www.datawire.io/not-engineer-running-3-5gb-docker-images/)
* docker 的优点和缺点，反对声音
  * https://github.com/lanzhiwang/awesome-huzhi/blob/master/docker/Docker_Pros_and_Cons.md
  * http://apachebooster.com/kb/what-are-the-advantages-and-disadvantages-of-docker/
  * http://www.smashcompany.com/technology/why-would-anyone-choose-docker-over-fat-binaries
  * http://dockone.io/article/5520
  * http://www.smashcompany.com/technology/docker-is-a-dangerous-gamble-which-we-will-regret
  * https://thehftguy.com/2016/11/01/docker-in-production-an-history-of-failure/
* [dockerfile 最佳实践](https://blog.docker.com/2019/07/intro-guide-to-dockerfile-best-practices/)

* [kubernetes](https://github.com/lanzhiwang/k8s)

## algorithm

* [算法分类](./algorithm/README.md)
* [sort](./algorithm/Sort.md)
* [tree](./algorithm/Tree.md)
* [算法题](./algorithm/isStraight.md)


## email

* [IMAP/POP3/STMP 协议](./mail/mail_protocol.md)
* [邮件头信息解析规则和常见头字段](./mail/email_header.md)
  * 如何区分并不同的MUA和MTA添加的头信息？？
* [Python实现的简单邮件客户端实现获取邮件](./mail/email_client_python.md)
* [IMAP/POP3/STMP pacp 包](./mail/pcap/)
* [smtp 响应状态码](./mail/List_of_most_common_SMTP_responses.md)
* 实现高性能、安全邮件服务器？？
* 反爬虫？？
* [邮件服务器添加 SPF、DKIM、DMARC、PTR 提高送达率](http://lomu.me/post/SPF-DKIM-DMARC-PTR)
* [通过头信息识别垃圾邮件的方法](./mail/headers_Spam.md)


## Component

* Etcd
* Redis
    * [Redis 目标分类](https://github.com/lanzhiwang/awesome-huzhi/wiki/redis)
    * [Redis 客户端与服务端通信协议](https://github.com/lanzhiwang/awesome-huzhi/blob/master/Redis/Redis_Protocol.md)
    * [Redis 事件模型](https://github.com/lanzhiwang/awesome-huzhi/blob/master/Redis/Redis_Event_Model.md)
    * [redis-cli 常用命令](https://github.com/lanzhiwang/awesome-huzhi/blob/master/Redis/redis-cli.md)
    * [Redis 数据类型](https://github.com/lanzhiwang/awesome-huzhi/blob/master/Redis/Redis_Data_Type.md)
    * [bit 操作](https://github.com/lanzhiwang/awesome-huzhi/blob/master/Redis/redis_data_characteristic.md#bitmap)、[过期时间](https://github.com/lanzhiwang/awesome-huzhi/blob/master/Redis/redis_data_characteristic.md#%E8%BF%87%E6%9C%9F%E6%97%B6%E9%97%B4)、[sort](https://github.com/lanzhiwang/awesome-huzhi/blob/master/Redis/redis_data_characteristic.md#sort)、[管道操作](https://github.com/lanzhiwang/awesome-huzhi/blob/master/Redis/redis_data_characteristic.md#redis-%E7%AE%A1%E9%81%93)、[事务](https://github.com/lanzhiwang/awesome-huzhi/blob/master/Redis/redis_data_characteristic.md#redis-%E4%BA%8B%E5%8A%A1)、[发布订阅](https://github.com/lanzhiwang/awesome-huzhi/blob/master/Redis/redis_data_characteristic.md#redis-%E5%8F%91%E5%B8%83%E8%AE%A2%E9%98%85)、[在redis中使用lua脚本](https://github.com/lanzhiwang/awesome-huzhi/blob/master/Redis/redis_data_characteristic.md#%E5%9C%A8-redis-%E4%B8%AD%E4%BD%BF%E7%94%A8-lua-%E8%84%9A%E6%9C%AC)
    * [Redis 复制](https://github.com/lanzhiwang/awesome-huzhi/blob/master/Redis/Redis_Replication.md)
    * [Redis 持久化 RDB 和 AOF](https://github.com/lanzhiwang/awesome-huzhi/blob/master/Redis/Redis_Persistence.md)
    * [Redis 哨兵和集群](https://github.com/lanzhiwang/awesome-huzhi/blob/master/Redis/Redis_Sentinel_And_Cluster.md)
    * [Redis 数据分片解决方案对比](https://github.com/lanzhiwang/awesome-huzhi/blob/master/Redis/Redis_data_sharding.md)
    * [Redis在实践过程中需要考虑的问题以及解决方案](https://github.com/lanzhiwang/awesome-huzhi/blob/master/Redis/redis_practice.md)
    * redis 的缺点（主要是内存浪费、集群问题、Redis单线程对 CPU 的利用率不高）
    * [Redis 实现分布式锁](./Redis/Redis_lock.md)
    * [Redis 中的乐观锁和悲观锁](./Redis/Redis_optimistic_Pessimistic_lock.md)
    * [Redis 内存模型](./Redis/Redis_memory_model.md)
    * [Redis 中的写时复制机制](./Redis/Redis_cow.md)
    * [Redis 内存碎片化的原因](Redis/Memory_fragmentation.md)
    * [缓存穿透，缓存击穿，缓存雪崩](Redis/penetration_breakdown_avalanche.md)
    * [使用 docker 搭建 redis 集群和哨兵](./Redis/redis_cluster_docker.md)
	* Sentinel 进程是如何坚持到从服务器和其他哨兵实例的（毕竟我们只在配置文件中指定了主实例的信息）？
    
* [MongoDB](./MongoDB/MongoDB.md)
    * MongoDB 复制集的主从选举机制和主从同步机制？？
    * MongoDB 的分片机制？？
    * primary shard 是怎样选举的？？
    * MongoDB 的 balancer 机制？？
    * 分片的 chunks 功能是怎样实现的？？
    * mongos 元数据是怎样生成的？？
* Elasticsearch
	* [Elasticsearch 基础](./elasticsearch/elasticsearch_base.md)
  * [elasticsearch 分片索引](./elasticsearch/shard.md)
  * [elasticsearch 节点类型](./elasticsearch/elasticsearch_node.md)

* [RabbitMQ](https://github.com/lanzhiwang/awesome-huzhi/wiki/RabbitMQ)

* [Kafka](https://github.com/lanzhiwang/awesome-huzhi/wiki/kafka-base)
  * kafka 高性能的基本原因
    * 顺序读写磁盘，顺序读写磁盘效率比随机写内存还要高，这是Kafka高吞吐率的一个很重要的保证
    * partition 水平扩展
    * 仅仅元数据序列化和反序列号
    * 用户态和内核态交互少
    * Kafka提供两种策略去删除旧数据。一是基于时间，二是基于partition文件大小，减少磁盘IO
    * Kafka broker是无状态的，它不需要标记哪些消息被哪些consumer过，不需要通过broker去保证同一个consumer group只有一个consumer能消费某一条消息，因此也就不需要锁机制，这也为Kafka的高吞吐率提供了有力保障
    * 复制机制采用 "in sync" 机制，复制机制即不是同步复制，也不是单纯的异步复制



## 分布式

* 分布式理论

  * [一致性、可用性、分区容差 CAP theorem](https://github.com/donnemartin/system-design-primer#cap-theorem)
* [分布式系统介绍](https://hackernoon.com/a-thorough-introduction-to-distributed-systems-3b91562c9b3c)
* [分布式教程](https://github.com/feixiao/Distributed-Systems)



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


## Android

* [安卓基础](./android/Android.md)

* [安卓应用攻击面](./android/Android_application_attack_surface.md)

* [AndroidViewClient](https://github.com/lanzhiwang/AndroidViewClient) - 获取安卓界面上的控件坐标用于沙箱运行

* [apk-Dynamic-Analysis](https://github.com/lanzhiwang/apk-Dynamic-Analysis) - 常见APK逆向分析工具使用方法

* [android-emulator](https://github.com/tracer0tong/android-emulator) - docker 运行安卓模拟器

* [命令行构建 APK 文件](https://github.com/lanzhiwang/apk-Dynamic-Analysis/blob/master/apk_build.md)

## 计算机基础

* [tcp/ip](https://github.com/lanzhiwang/awesome-huzhi/wiki/tcp-ip-status) - tcp 连接和断开过程以及过程中进程的状态
* [TCP 协议基础](./computer/TCP_base.md)
* [tcp的半连接与完全连接队列](https://github.com/lanzhiwang/awesome-huzhi/wiki/tcp%E7%9A%84%E5%8D%8A%E8%BF%9E%E6%8E%A5%E4%B8%8E%E5%AE%8C%E5%85%A8%E8%BF%9E%E6%8E%A5%E9%98%9F%E5%88%97)
* [Linux SYNcookie 机制](https://github.com/lanzhiwang/awesome-huzhi/wiki/Linux-SYNcookie-%E6%9C%BA%E5%88%B6)
* [TCP IP协议中backlog参数](https://github.com/lanzhiwang/awesome-huzhi/wiki/TCP-IP%E5%8D%8F%E8%AE%AE%E4%B8%ADbacklog%E5%8F%82%E6%95%B0)
* [TCP状态转换图](https://github.com/lanzhiwang/awesome-huzhi/wiki/TCP%E7%8A%B6%E6%80%81%E8%BD%AC%E6%8D%A2%E5%9B%BE)
* [tcp/ip 主动断开连接为什么需要等到 2MSL 时长](https://github.com/lanzhiwang/awesome-huzhi/wiki/tcp-ip-status)
* [HTTP 包式处理和流式处理](./computer/http_packet_stream.md)
* [HTTP 连接管理 - 短连接、长连接、HTTP 流水线、域名分片、http2的多路复用](./computer/long_connection_and_short_connection.md)
* [HTTS 是如何工作的](./computer/https/README_01.md)
* [nginx 支持长连接](./computer/nginx_keep_alive.md)
* [HTTP 中 GET/POST 的区别](./computer/HTTP_GET_POST.md)
* [system-design-primer](https://github.com/donnemartin/system-design-primer) - 设计可扩展系统
* [代码整洁之道](https://github.com/lanzhiwang/awesome-huzhi/wiki/clean-code)
* [HTTPS图解](https://tls.ulfheim.net/)
* [HTTP Status Codes](./computer/HTTP_Status_Codes.md)
* [什么时候使用单例模式，为什么要使用单例模式](./computer/Singleton.md)
* [DNS 记录](./computer/DNS.md)
* [linux 内存分配](./c_language/README.md)


## JavaScript

* 前端浏览器（**各种浏览器的性能测量以及性能损耗问题？**）

	* [phantomjs](https://github.com/ariya/phantomjs)

	* [puppeteer](https://github.com/GoogleChrome/puppeteer)

	* [chromium](https://github.com/chromium/chromium)


## Internet-Awesome

* [awesome-python](https://github.com/vinta/awesome-python)

* [awesome-interview-questions](https://github.com/MaximAbramchuck/awesome-interview-questions)


## Other

* [Hack](https://github.com/source-foundry/Hack) - 编程专用字体

* [ffmpeg](./other/ffmpeg.md) - ffmpeg 是一个非常快速的视频和音频转换器，也可以从现场音频/视频源获取。 它还可以在任意采样率之间进行转换，并使用高质量的多相滤波器动态调整视频大小。

* [ffmpeg 操作示例](https://github.com/feixiao/ffmpeg)

* [thumbor](https://github.com/thumbor/thumbor) - Thumbor是一种智能成像服务。 它支持按需裁剪，调整大小和翻转图像。

* [you-get](https://github.com/soimort/you-get) - 视频、音频、图片下载工具

* [asciify](https://github.com/RameshAditya/asciify) - Convert Images into ASCII Art with the power of Python

* [face_recognition](https://github.com/ageitgey/face_recognition) - 人脸识别

* Markdown

	* [haroopress](http://pad.haroopress.com/)、[typora](https://typora.io/)

	* [vnote](https://github.com/tamlok/vnote)

## Book

* Python

  * 图灵程序设计丛书:Python基础教程(第3版)

  * Python 高级编程(第2版)

  * [python 学习手册](https://resources.oreilly.com/examples/9780596158071/tree/master)

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

    * 奔跑吧 Ansible

* Docker

    * 第一本Docker书
    * Docker经典实例 (图灵程序设计丛书)
    * 每天5分钟玩转Docker容器技术
    * 每天5分钟玩转Kubernetes
    * 容器即服务：从零构建企业级容器集群
    * Kubernetes权威指南：企业级容器云实战

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

    * Redis 深度历险 核心原理和应用实践

    * 写给大忙人的Hadoop 2

    * 大型网站技术架构:核心原理与案例分析

    * Wireshark网络分析就这么简单

    * HTTP权威指南

    * 数学之美(第二版)

    * 啊哈!算法

    * 图解密码技术(第3版)

    * 深入理解计算机系统(原书第3版)

    * 从Paxos到Zookeeper:分布式一致性原理与实践
