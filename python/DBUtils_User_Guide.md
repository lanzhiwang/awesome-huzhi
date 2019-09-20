# DBUtils User's Guide

- Version             1.3

- Released          08/03/18

- Translations    English | [German](https://cito.github.io/DBUtils/UsersGuide.de.html)

Contents

- [Synopsis](https://cito.github.io/DBUtils/UsersGuide.html#synopsis)
- [Modules](https://cito.github.io/DBUtils/UsersGuide.html#modules)
- [Download](https://cito.github.io/DBUtils/UsersGuide.html#download)
- [Installation](https://cito.github.io/DBUtils/UsersGuide.html#installation)
  - [Installation as a standalone (top-level) package](https://cito.github.io/DBUtils/UsersGuide.html#installation-as-a-standalone-top-level-package)
  - [Installation as a Webware for Python subpackage (plug-in)](https://cito.github.io/DBUtils/UsersGuide.html#installation-as-a-webware-for-python-subpackage-plug-in)
- [Requirements](https://cito.github.io/DBUtils/UsersGuide.html#requirements)
- [Functionality](https://cito.github.io/DBUtils/UsersGuide.html#functionality)
  - [SimplePooledDB](https://cito.github.io/DBUtils/UsersGuide.html#simplepooleddb)
  - [SteadyDB](https://cito.github.io/DBUtils/UsersGuide.html#steadydb)
  - [PersistentDB](https://cito.github.io/DBUtils/UsersGuide.html#persistentdb)
  - [PooledDB](https://cito.github.io/DBUtils/UsersGuide.html#pooleddb)
  - [Which one to use?](https://cito.github.io/DBUtils/UsersGuide.html#which-one-to-use)
- [Usage](https://cito.github.io/DBUtils/UsersGuide.html#usage)
  - [PersistentDB](https://cito.github.io/DBUtils/UsersGuide.html#id1)
  - [PooledDB](https://cito.github.io/DBUtils/UsersGuide.html#id2)
  - [Usage in Webware for Python](https://cito.github.io/DBUtils/UsersGuide.html#usage-in-webware-for-python)
- [Notes](https://cito.github.io/DBUtils/UsersGuide.html#notes)
- [Future](https://cito.github.io/DBUtils/UsersGuide.html#future)
- [Bug reports and feedback](https://cito.github.io/DBUtils/UsersGuide.html#bug-reports-and-feedback)
- [Links](https://cito.github.io/DBUtils/UsersGuide.html#links)
- [Credits](https://cito.github.io/DBUtils/UsersGuide.html#credits)
- [Copyright and License](https://cito.github.io/DBUtils/UsersGuide.html#copyright-and-license)

# Synopsis  概要

[DBUtils](https://github.com/Cito/DBUtils) is a suite of Python modules allowing to connect in a safe and efficient way between a threaded [Python](https://www.python.org/) application and a database. DBUtils has been written in view of [Webware for Python](https://cito.github.io/w4py/) as the application and [PyGreSQL](http://www.pygresql.org/) as the adapter to a [PostgreSQL](https://www.postgresql.org/) database, but it can be used for any other Python application and [DB-API 2](https://www.python.org/dev/peps/pep-0249/) conformant database adapter.  DBUtils是一套Python模块，允许在线程Python应用程序和数据库之间以安全有效的方式连接。 DBUtils是针对作为应用程序的Python的Webware和作为PostgreSQL数据库的适配器的PyGreSQL编写的，但它可以用于任何其他Python应用程序和符合DB-API 2的数据库适配器。

# Modules

The DBUtils suite is realized as a Python package containing two subsets of modules, one for use with arbitrary DB-API 2 modules, the other one for use with the classic PyGreSQL module.  DBUtils套件实现为包含两个模块子集的Python包，一个用于任意DB-API 2模块，另一个用于经典PyGreSQL模块。

| Universal 普遍 DB-API 2 variant 变种 |                                  |
| -------------------------- | -------------------------------- |
| SteadyDB.py                | Hardened DB-API 2 connections    |
| PooledDB.py                | Pooling for DB-API 2 connections |
| PersistentDB.py            | Persistent DB-API 2 connections  |
| SimplePooledDB.py          | Simple pooling for DB-API 2      |

| Classic PyGreSQL variant 变种 |                                          |
| ------------------------ | ---------------------------------------- |
| SteadyPg.py              | Hardened classic PyGreSQL connections    |
| PooledPg.py              | Pooling for classic PyGreSQL connections |
| PersistentPg.py          | Persistent classic PyGreSQL connections  |
| SimplePooledPg.py        | Simple pooling for classic PyGreSQL      |

The dependencies of the modules in the universal DB-API 2 variant are as indicated in the following diagram:  通用DB-API 2变体中模块的依赖关系如下图所示：

![dbdep.gif](https://cito.github.io/DBUtils/dbdep.gif)

The dependencies of the modules in the classic PyGreSQL variant are similar:  经典PyGreSQL变体中模块的依赖关系是类似的：

![pgdep.gif](https://cito.github.io/DBUtils/pgdep.gif)

# Download

You can download the actual version of DBUtils from the Python Package Index at:

```
https://pypi.python.org/pypi/DBUtils
```

The source code repository can be found here on GitHub:

```
https://github.com/Cito/DBUtils
```

# Installation

## Installation as a standalone (top-level) package

If you intend to use DBUtils from other applications than Webware for Python, it is recommended to install the package in the usual way:

```
python setup.py install
```

You can also use [pip](https://pip.pypa.io/) for download and installation:

```
pip install DBUtils
```

## Installation as a Webware for Python subpackage (plug-in)

If you want to use DBUtils as a supplement for the Webware for Python framework only, you should install it as a Webware plug-in:

```
python setup.py install --install-lib=/path/to/Webware
```

Replace /path/to/Webware with the path to the root directory of your Webware for Python installation. You will also need to run the Webware installer if this has not been done already or if you want to integrate the DBUtils documentation into the Webware documentation:

```
cd path/to/Webware
python install.py
```

# Requirements

DBUtils requires at least [Python](https://www.python.org/) version 2.6. The modules in the classic PyGreSQL variant need [PyGreSQL](http://www.pygresql.org/) version 3.4 or above, while the modules in the universal DB-API 2 variant run with any Python [DB-API 2](https://www.python.org/dev/peps/pep-0249/) compliant database interface module.  DBUtils至少需要Python 2.6版。 经典PyGreSQL变体中的模块需要PyGreSQL 3.4或更高版本，而通用DB-API 2变体中的模块可以与任何符合Python DB-API 2的数据库接口模块一起运行。

# Functionality

This section will refer to the names in the DB-API 2 variant only, but the same applies to the classic PyGreSQL variant.  本节仅涉及DB-API 2变体中的名称，但同样适用于经典的PyGreSQL变体。

## SimplePooledDB

DBUtils.SimplePooledDB is a very basic reference implementation of a pooled database connection. It is much less sophisticated than the regular PooledDB module and is particularly lacking the failover functionality. DBUtils.SimplePooledDB is essentially the same as the MiscUtils.DBPool module that is part of Webware for Python. You should consider it a demonstration of concept rather than something that should go into production.  DBUtils.SimplePooledDB是池化数据库连接的一个非常基本的参考实现。 它比普通的PooledDB模块简单得多，并且特别缺乏故障转移功能。 DBUtils.SimplePooledDB与MiscUtils.DBPool模块基本相同，后者是Webware for Python的一部分。 您应该将其视为概念的演示，而不是应该投入生产的东西。

## SteadyDB

DBUtils.SteadyDB is a module implementing "hardened" connections to a database, based on ordinary connections made by any DB-API 2 database module. A "hardened" connection will transparently reopen upon access when it has been closed or the database connection has been lost or when it is used more often than an optional usage limit.  DBUtils.SteadyDB是一个模块，它基于任何DB-API 2数据库模块的普通连接，实现与数据库的“强化”连接。 当一个“硬化”连接关闭或数据库连接丢失或者使用频率高于可选使用限制时，它将在访问时透明地重新打开。

A typical example where this is needed is when the database has been restarted while your application is still running and has open connections to the database, or when your application accesses a remote database in a network that is separated by a firewall and the firewall has been restarted and lost its state.  需要执行此操作的典型示例是，在应用程序仍在运行时重新启动数据库并且与数据库建立了打开的连接，或者当您的应用程序访问由防火墙隔开的网络中的远程数据库时 重新启动并失去了状态。

Usually, you will not use the SteadyDB module directly; it merely serves as a basis for the next two modules, PersistentDB and PooledDB.  通常，您不会直接使用SteadyDB模块; 它只是作为下两个模块PersistentDB和PooledDB的基础。

## PersistentDB

DBUtils.PersistentDB implements steady, thread-affine, persistent connections to a database, using any DB-API 2 database module.  DBUtils.PersistentDB使用任何DB-API 2数据库模块实现与数据库的稳定，线程仿射，持久连接。

The following diagram shows the connection layers involved when you are using PersistentDB connections:  下图显示了使用PersistentDB连接时涉及的连接层：

![persist.gif](https://cito.github.io/DBUtils/persist.gif)

Whenever a thread opens a database connection for the first time, a new connection to the database will be opened that will be used from now on for this specific thread. When the thread closes the database connection, it will still be kept open so that the next time when a connection is requested by the same thread, this already opened connection can be used. The connection will be closed automatically when the thread dies.  每当线程第一次打开数据库连接时，将打开一个新的数据库连接，从现在开始将用于此特定线程。 当线程关闭数据库连接时，它仍将保持打开状态，以便下次同一线程请求连接时，可以使用此已打开的连接。 当线程死亡时，连接将自动关闭。

In short: PersistentDB tries to recycle database connections to increase the overall database access performance of your threaded application, but it makes sure that connections are never shared between threads.  简而言之：PersistentDB尝试回收数据库连接以提高线程应用程序的整体数据库访问性能，但它确保连接永远不会在线程之间共享。

Therefore, PersistentDB will work perfectly even if the underlying DB-API module is not thread-safe at the connection level, and it will avoid problems when other threads change the database session or perform transactions spreading over more than one SQL command.  因此，即使底层DB-API模块在连接级别不是线程安全的，PersistentDB也能正常工作，并且当其他线程更改数据库会话或执行跨多个SQL命令传播的事务时，它将避免出现问题。

## PooledDB

DBUtils.PooledDB implements a pool of steady, thread-safe cached connections to a database which are transparently reused, using any DB-API 2 database module.  BUtils.PooledDB使用任何DB-API 2数据库模块实现了一个稳定，线程安全的缓存连接池，这些连接是透明地重用的数据库。

The following diagram shows the connection layers involved when you are using PooledDB connections:

![pool.gif](https://cito.github.io/DBUtils/pool.gif)

As the diagram indicates, PooledDB can share opened database connections between different threads. This will happen by default if you set up the connection pool with a positive value of **maxshared** and the underlying DB-API 2 is thread-safe at the connection level, but you can also request dedicated database connections that will not be shared between threads. Besides the pool of shared connections, you can also set up a pool of at least **mincached** and at the most **maxcached** idle connections that will be used whenever a thread is requesting a dedicated database connection or the pool of shared connections is not yet full. When a thread closes a connection that is not shared any more, it is returned back to the pool of idle connections so that it can be recycled again.  如图所示，PooledDB可以在不同线程之间共享打开的数据库连接。 如果您将连接池设置为正值maxshared且底层DB-API 2在连接级别是线程安全的，则默认情况下会发生这种情况，但您也可以请求不在线程之间共享的专用数据库连接。 除了共享连接池之外，您还可以设置至少mincached和最多maxcached空闲连接的池，每当线程请求专用数据库连接或共享连接池尚未满时，将使用这些连接。 当线程关闭不再共享的连接时，它将返回到空闲连接池，以便可以再次回收它。

If the underlying DB-API module is not thread-safe, thread locks will be used to ensure that the PooledDB connections are thread-safe. So you don't need to worry about that, but you should be careful to use dedicated connections whenever you change the database session or perform transactions spreading over more than one SQL command.  如果底层DB-API模块不是线程安全的，则将使用线程锁来确保PooledDB连接是线程安全的。 因此，您无需担心这一点，但每当您更改数据库会话或执行跨多个SQL命令传播的事务时，您都应该小心使用专用连接。

## Which one to use?

Both PersistentDB and PooledDB serve the same purpose to improve the database access performance by recycling database connections, while preserving stability even if database connection will be disrupted.  PersistentDB和PooledDB通过回收数据库连接来提高数据库访问性能，同时保持稳定性，即使数据库连接中断也是如此。

So which of these two modules should you use? From the above explanations it is clear that PersistentDB will make more sense if your application keeps a constant number of threads which frequently use the database. In this case, you will always have the same amount of open database connections. However, if your application frequently starts and ends threads, then it will be better to use PooledDB. The latter will also allow more fine-tuning, particularly if you are using a thread-safe DB-API 2 module.  那么你应该使用这两个模块中的哪一个？ 从上面的解释可以清楚地看出，如果您的应用程序保持经常使用数据库的常量线程数，则PersistentDB会更有意义。 在这种情况下，您将始终具有相同数量的打开数据库连接。 但是，如果您的应用程序经常启动和结束线程，那么最好使用PooledDB。 后者还允许更多微调，特别是如果您使用的是线程安全的DB-API 2模块。

Since the interface of both modules is similar, you can easily switch from one to the other and check which one will suit better.   由于两个模块的接口相似，因此您可以轻松地从一个模块切换到另一个模块，并检查哪个模块更适合。

# Usage

The usage of all the modules is similar, but there are also some differences in the initialization between the "Pooled" and "Persistent" variants and also between the universal DB-API 2 and the classic PyGreSQL variants.  所有模块的使用情况类似，但“Pooled”和“Persistent”变体之间以及通用DB-API 2和经典PyGreSQL变体之间的初始化也存在一些差异。

We will cover here only the PersistentDB module and the more complex PooledDB module. For the details of the other modules, have a look at their module docstrings. Using the Python interpreter console, you can display the documentation of the PooledDB module as follows (this works analogously for the other modules):  我们这里仅介绍PersistentDB模块和更复杂的PooledDB模块。 有关其他模块的详细信息，请查看其模块文档字符串。 使用Python解释器控制台，您可以按如下方式显示PooledDB模块的文档（这与其他模块类似）：

```
help(PooledDB)
```

## PersistentDB

In order to make use of the PersistentDB module, you first need to set up a generator for your kind of database connections by creating an instance of PersistentDB, passing the following parameters:  为了使用PersistentDB模块，首先需要通过创建PersistentDB实例为您的数据库连接类型设置生成器，并传递以下参数：

- creator: either an arbitrary function returning new DB-API 2 connection objects or a DB-API 2 compliant database module  返回新的DB-API 2连接对象的任意函数或符合DB-API 2的数据库模块

- maxusage: the maximum number of reuses of a single connection (the default of 0 or None means unlimited reuse)  单个连接的最大重用次数（默认值为0或None表示无限次重用）

  Whenever the limit is reached, the connection will be reset.  只要达到限制，连接就会重置。

- setsession: an optional list of SQL commands that may serve to prepare the session, e.g. ["set datestyle to german", ...]  可用于准备会话的SQL命令的可选列表

- failures: an optional exception class or a tuple of exception classes for which the connection failover mechanism shall be applied, if the default (OperationalError, InternalError) is not adequate  如果缺省值（OperationalError，InternalError）不足，则应该应用连接故障转移机制的可选异常类或异常类元组

- ping: an optional flag controlling when connections are checked with the ping() method if such a method is available (0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always, and all other bit combinations of these values)  一个可选标志，控制何时使用ping（）方法检查连接（如果有这样的方法）

- closeable: if this is set to true, then closing connections will be allowed, but by default this will be silently ignored  如果将其设置为true，则允许关闭连接，但默认情况下将自动忽略

- threadlocal: an optional class for representing thread-local data that will be used instead of our Python implementation (threading.local is faster, but cannot be used in all cases)  一个可选的类，用于表示将用于代替我们的Python实现的线程局部数据（threading.local更快，但不能在所有情况下使用）

- The creator function or the connect function of the DB-API 2 compliant database module specified as the creator will receive any additional parameters such as the host, database, user, password etc. You may choose some or all of these parameters in your own creator function, allowing for sophisticated failover and load-balancing mechanisms.  指定为创建者的DB-API 2兼容数据库模块的创建者函数或连接函数将接收任何其他参数，例如主机，数据库，用户，密码等。您可以在自己的创建者中选择部分或全部这些参数 功能，允许复杂的故障转移和负载平衡机制。

For instance, if you are using pgdb as your DB-API 2 database module and want every connection to your local database mydb to be reused 1000 times:

```
import pgdb  # import used DB-API 2 module
from DBUtils.PersistentDB import PersistentDB
persist = PersistentDB(pgdb, 1000, database='mydb')
```

Once you have set up the generator with these parameters, you can request database connections of that kind:

```
db = persist.connection()
```

You can use these connections just as if they were ordinary DB-API 2 connections. Actually what you get is the hardened SteadyDB version of the underlying DB-API 2 connection.  您可以像使用普通的DB-API 2连接一样使用这些连接。 实际上你得到的是底层DB-API 2连接的强化SteadyDB版本。

Closing a persistent connection with db.close() will be silently ignored since it would be reopened at the next usage anyway and contrary to the intent of having persistent connections. Instead, the connection will be automatically closed when the thread dies. You can change this behavior be setting the closeable parameter.  关闭与db.close（）的持久连接将被忽略，因为无论如何它将在下次使用时重新打开，这与持久连接的意图相反。 相反，当线程死亡时，连接将自动关闭。 您可以通过设置closeable参数来更改此行为。

Note that you need to explicitly start transactions by calling the begin() method. This ensures that the transparent reopening will be suspended until the end of the transaction, and that the connection will be rolled back before being reused by the same thread.  请注意，您需要通过调用begin（）方法显式启动事务。 这可确保透明重新打开将暂停直到事务结束，并且连接将在被同一线程重用之前回滚。

By setting the threadlocal parameter to threading.local, getting connections may become a bit faster, but this may not work in all environments (for instance, mod_wsgi is known to cause problems since it clears the threading.local data between requests).  通过将threadlocal参数设置为threading.local，获取连接可能会变得更快，但这可能不适用于所有环境（例如，已知mod_wsgi会导致问题，因为它会清除请求之间的threading.local数据）。

## PooledDB

In order to make use of the PooledDB module, you first need to set up the database connection pool by creating an instance of PooledDB, passing the following parameters:

- creator: either an arbitrary function returning new DB-API 2 connection objects or a DB-API 2 compliant database module  返回新的DB-API 2连接对象的任意函数或符合DB-API 2的数据库模块

- mincached : the initial number of idle connections in the pool (the default of 0 means no connections are made at startup)  池中的初始空闲连接数（默认值为0表示启动时没有建立连接）

- maxcached: the maximum number of idle connections in the pool (the default value of 0 or None means unlimited pool size)

- maxshared: maximum number of shared connections allowed (the default value of 0 or None means all connections are dedicated专用)

  When this maximum number is reached, connections are shared if they have been requested as shareable.  达到此最大数量时，如果已将连接请求为可共享，则会共享连接。

- maxconnections: maximum number of connections generally allowed (the default value of 0 or None means any number of connections)  通常允许的最大连接数（默认值0或None表示任意数量的连接）

- blocking: determines behavior when exceeding the maximum  超过最大值时确定行为

  If this is set to true, block and wait until the number of connections decreases, but by default an error will be reported.  如果将此值设置为true，则阻塞并等待，直到连接数减少，但默认情况下将报告错误。

- maxusage: maximum number of reuses of a single connection (the default of 0 or None means unlimited reuse)

  When this maximum usage number of the connection is reached, the connection is automatically reset (closed and reopened).

- setsession: an optional list of SQL commands that may serve to prepare the session, e.g. ["set datestyle to german", ...]  可用于准备会话的SQL命令的可选列表

- reset: how connections should be reset when returned to the pool (False or None to rollback transcations started with begin(), the default value True always issues a rollback for safety's sake)  如何在返回池时重置连接（False或None以使用begin（）开始回滚转码，默认值True始终为安全起见而发出回滚）

- failures: an optional exception class or a tuple of exception classes for which the connection failover mechanism shall be applied, if the default (OperationalError, InternalError) is not adequate  如果缺省值（OperationalError，InternalError）不足，则应该应用连接故障转移机制的可选异常类或异常类元组

- ping: an optional flag controlling when connections are checked with the ping() method if such a method is available (0 = None = never, 1 = default = whenever fetched from the pool, 2 = when a cursor is created, 4 = when a query is executed, 7 = always, and all other bit combinations of these values)  一个可选标志，控制何时使用ping（）方法检查连接（如果有这样的方法）

- The creator function or the connect function of the DB-API 2 compliant database module specified as the creator will receive any additional parameters such as the host, database, user, password etc. You may choose some or all of these parameters in your own creator function, allowing for sophisticated failover and load-balancing mechanisms.  指定为创建者的DB-API 2兼容数据库模块的创建者函数或连接函数将接收任何其他参数，例如主机，数据库，用户，密码等。您可以在自己的创建者中选择部分或全部这些参数 功能，允许复杂的故障转移和负载平衡机制。

For instance, if you are using pgdb as your DB-API 2 database module and want a pool of at least five connections to your local database mydb:

```
import pgdb  # import used DB-API 2 module
from DBUtils.PooledDB import PooledDB
pool = PooledDB(pgdb, 5, database='mydb')
```

Once you have set up the connection pool you can request database connections from that pool:

```
db = pool.connection()
```

You can use these connections just as if they were ordinary DB-API 2 connections. Actually what you get is the hardened SteadyDB version of the underlying DB-API 2 connection.

Please note that the connection may be shared with other threads by default if you set a non-zero maxshared parameter and the DB-API 2 module allows this. If you want to have a dedicated connection, use:

```
db = pool.connection(shareable=False)
```

Instead of this, you can also get a dedicated connection as follows:

```
db = pool.dedicated_connection()
```

If you don't need it any more, you should immediately return it to the pool with db.close(). You can get another connection in the same way.

*Warning:* In a threaded environment, never do the following:

```
pool.connection().cursor().execute(...)
```

This would release the connection too early for reuse which may be fatal if the connections are not thread-safe. Make sure that the connection object stays alive as long as you are using it, like that:

```
db = pool.connection()
cur = db.cursor()
cur.execute(...)
res = cur.fetchone()
cur.close()  # or del cur
db.close()  # or del db
```

Note that you need to explicitly start transactions by calling the begin() method. This ensures that the connection will not be shared with other threads, that the transparent reopening will be suspended until the end of the transaction, and that the connection will be rolled back before being given back to the connection pool.

## Usage in Webware for Python

If you are using DBUtils in order to access a database from [Webware for Python](https://cito.github.io/w4py/) servlets, you need to make sure that you set up your database connection generators only once when the application starts, and not every time a servlet instance is created. For this purpose, you can add the necessary code to the module or class initialization code of your base servlet class, or you can use the contextInitialize() function in the __init__.py script of your application context.  如果您使用DBUtils从Webware for Python servlet访问数据库，则需要确保在应用程序启动时仅设置一次数据库连接生成器，而不是每次都创建servlet实例。 为此，您可以将必要的代码添加到基本servlet类的模块或类初始化代码中，或者可以在应用程序上下文的__init__.py脚本中使用contextInitialize（）函数。

The directory Examples that is part of the DButils distribution contains an example context for Webware for Python that uses a small demo database designed to track the attendees for a series of seminars (the idea for this example has been taken from the article "[The Python DB-API](http://www.linuxjournal.com/article/2605)" by Andrew Kuchling).  作为DButils发行版的一部分的目录Examples包含一个Webware for Python的示例上下文，它使用一个小型演示数据库来跟踪一系列研讨会的与会者（这个例子的想法来自文章“The Python DB” -API“by Andrew Kuchling）。

The example context can be configured by either creating a config file Configs/Database.config or by directly changing the default parameters in the example servlet Examples/DBUtilsExample.py. This way you can set an appropriate database user and password, and you can choose the underlying database module (PyGreSQL classic or any DB-API 2 module). If the setting maxcached is present, then the example servlet will use the "Pooled" variant, otherwise it will use the "Persistent" variant.  可以通过创建配置文件Configs / Database.config或直接更改示例servlet Examples / DBUtilsExample.py中的缺省参数来配置示例上下文。 这样您就可以设置适当的数据库用户和密码，并且可以选择底层数据库模块（PyGreSQL classic或任何DB-API 2模块）。 如果存在设置maxcached，则示例servlet将使用“Pooled”变体，否则它将使用“Persistent”变体。

# Notes

If you are using one of the popular object-relational mappers [SQLObject](http://www.sqlobject.org/) or [SQLAlchemy](http://www.sqlalchemy.org/), you won't need DBUtils, since they come with their own connection pools. SQLObject 2 (SQL-API) is actually borrowing some code from DBUtils to split the pooling out into a separate layer.  如果您使用的是流行的对象关系映射器SQLObject或SQLAlchemy之一，则不需要DBUtils，因为它们带有自己的连接池。 SQLObject 2（SQL-API）实际上是从DBUtils借用一些代码将池分割成一个单独的层。

Also note that when you are using a solution like the Apache webserver with [mod_python](http://modpython.org/) or [mod_wsgi](https://github.com/GrahamDumpleton/mod_wsgi), then your Python code will be usually run in the context of the webserver's child processes. So if you are using the PooledDB module, and several of these child processes are running, you will have as much database connection pools. If these processes are running many threads, this may still be a reasonable approach, but if these processes don't spawn more than one worker thread, as in the case of Apache's "prefork" multi-processing module, this approach does not make sense. If you're running such a configuration, you should resort to a middleware for connection pooling that supports multi-processing, such as [pgpool](http://www.pgpool.net/) or [pgbouncer](https://pgbouncer.github.io/) for the PostgreSQL database.  另请注意，当您使用带有mod_python或mod_wsgi的Apache webserver等解决方案时，您的Python代码通常会在Web服务器的子进程的上下文中运行。 因此，如果您正在使用PooledDB模块，并且其中一些子进程正在运行，那么您将拥有尽可能多的数据库连接池。 如果这些进程运行多个线程，这可能仍然是一种合理的方法，但如果这些进程不会产生多个工作线程，就像Apache的“prefork”多处理模块一样，这种方法没有意义。 如果您正在运行这样的配置，则应该使用支持多处理的连接池的中间件，例如PostgreSQL数据库的pgpool或pgbouncer。

# Future

Some ideas for future improvements:

- Alternatively to the maximum number of uses of a connection, implement a maximum time to live for connections.
- Create modules MonitorDB and MonitorPg that will run in a separate thread, monitoring the pool of the idle connections and maybe also the shared connections respectively the thread-affine connections. If a disrupted connection is detected, then it will be reestablished automatically by the monitoring thread. This will be useful in a scenario where a database powering a website is restarted during the night. Without the monitoring thread, the users would experience a slight delay in the next morning, because only then, the disrupted database connections will be detected and the pool will be rebuilt. With the monitoring thread, this will already happen during the night, shortly after the disruption. The monitoring thread could also be configured to generally recreate the connection pool every day shortly before the users arrive.
- Optionally log usage, bad connections and exceeding of limits.

# Bug reports and feedback

Please send bug reports, patches and feedback directly to the author (using the email address given below).

If there are Webware related problems, these can also be discussed in the [Webware for Python mailing list](https://lists.sourceforge.net/lists/listinfo/webware-discuss).

# Links

Some links to related and alternative software:

- [DBUtils](https://github.com/Cito/DBUtils)
- [Python](https://www.python.org/)
- [Webware for Python](https://cito.github.io/w4py/) framework
- Python [DB-API 2](https://www.python.org/dev/peps/pep-0249/)
- [PostgreSQL](https://www.postgresql.org/) database
- [PyGreSQL](http://www.pygresql.org/) Python adapter for PostgreSQL
- [pgpool](http://www.pgpool.net/) middleware for PostgreSQL connection pooling
- [pgbouncer](https://pgbouncer.github.io/) lightweight PostgreSQL connection pooling
- [SQLObject](http://www.sqlobject.org/) object-relational mapper
- [SQLAlchemy](http://www.sqlalchemy.org/) object-relational mapper

# Credits

- Author

  Christoph Zwerschke <[cito@online.de](mailto:cito@online.de)>

- Contributions

  DBUtils uses code, input and suggestions made by Ian Bicking, Chuck Esterbrook (Webware for Python), Dan Green (DBTools), Jay Love, Michael Palmer, Tom Schwaller, Geoffrey Talvola, Warren Smith (DbConnectionPool), Ezio Vernacotola, Jehiah Czebotar, Matthew Harriger, Gregory Piñero and Josef van Eenbergen.

# Copyright and License

Copyright © 2005-2018 by Christoph Zwerschke. All Rights Reserved.

DBUtils is free and open source software, licensed under the [MIT license](https://opensource.org/licenses/MIT).

# 参考

* [阅读原文](https://cito.github.io/DBUtils/UsersGuide.html)
* [source code](https://github.com/Cito/DBUtils)