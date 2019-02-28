## SQLAlchemy — Python Tutorial

We often encounter data as Relational Databases. To work with them we generally would need to write raw SQL queries, pass them to the database engine and parse the returned results as a normal array of records.  我们经常将数据视为关系数据库。 要使用它们，我们通常需要编写原始SQL查询，将它们传递给数据库引擎并将返回的结果解析为正常的记录数组。

SQLAlchemy provides a nice “Pythonic” way of interacting with databases. So rather than dealing with the differences between specific dialects of traditional SQL such as MySQL or PostgreSQL or Oracle, you can leverage the Pythonic framework of SQLAlchemy to streamline your workflow and more efficiently query your data.  SQLAlchemy提供了一种与数据库交互的漂亮的“Pythonic”方式。 因此，您可以利用SQLAlchemy的Pythonic框架来简化工作流程并更有效地查询数据，而不是处理传统SQL（如MySQL或PostgreSQL或Oracle）的特定方言之间的差异。

### Installing The Package

```
pip install sqlalchemy
```

### Connecting to a database

To start interacting with the database we first we need to establish a connection.  要开始与数据库交互，我们首先需要建立连接。

```
import sqlalchemy as db
engine = db.create_engine('dialect+driver://user:pass@host:port/db')
```

### Viewing Table Details

SQLAlchemy can be used to automatically load tables from a database using something called reflection. Reflection is the process of reading the database and building the metadata based on that information.  SQLAlchemy可用于使用称为反射的东西从数据库自动加载表。 反射是读取数据库并基于该信息构建元数据的过程。
