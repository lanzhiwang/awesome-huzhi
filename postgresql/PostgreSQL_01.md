# PostgreSQL 新手入门

## 安装

首先，安装 PostgreSQL 客户端。

```bash
$ sudo apt-get install postgresql-client
```

然后，安装 PostgreSQL 服务器。

```bash
$ sudo apt-get install postgresql
```

正常情况下，安装完成后，PostgreSQL 服务器会自动在本机的 5432 端口开启。

如果还想安装图形管理界面，可以运行下面命令，但是本文不涉及这方面内容。

```bash
$ sudo apt-get install pgadmin3
```

## 添加新用户和新数据库

初次安装后，默认生成一个名为 **postgres的数据库** 和一个名为 **postgres的数据库用户**。这里需要注意的是，同时还生成了一个名为 **postgres的Linux系统用户**。

下面，我们使用 postgres 用户，来生成其他用户和新数据库。好几种方法可以达到这个目的，这里介绍两种。

### 第一种方法，使用 PostgreSQL 控制台

首先，新建一个 Linux 新用户，可以取你想要的名字，这里为 dbuser。

```bash
$ sudo adduser dbuser
```

然后，切换到 postgres 用户。

```bash
sudo su - postgres
```

下一步，使用 psql 命令登录 PostgreSQL 控制台。

```bash
$ psql
```

这时相当于系统用户 postgres 以同名数据库用户的身份，登录数据库，这是不用输入密码的。如果一切正常，系统提示符会变为 "postgres=#"，表示这时已经进入了数据库控制台。以下的命令都在控制台内完成。

第一件事是使用 \password 命令，为 postgres 用户设置一个密码。

```bash
> \password postgres
```

第二件事是创建数据库用户 dbuser（刚才创建的是 Linux 系统用户），并设置密码。

```bash
> CREATE USER dbuser WITH PASSWORD 'password';
```

第三件事是创建用户数据库，这里为 exampledb，并指定所有者为 dbuser。

```bash
> CREATE DATABASE exampledb OWNER dbuser;
```

第四件事是将 exampledb 数据库的所有权限都赋予 dbuser，否则 dbuser 只能登录控制台，没有任何数据库操作权限。

```bash
> GRANT ALL PRIVILEGES ON DATABASE exampledb to dbuser;
```

最后，使用 \q 命令退出控制台（也可以直接按ctrl+D）。

```bash
> \q
```

### 第二种方法，使用shell命令行

添加新用户和新数据库，除了在 PostgreSQL 控制台内，还可以在 shell 命令行下完成。这是因为PostgreSQL 提供了命令行程序 createuser 和 createdb。还是以新建用户 dbuser 和数据库exampledb 为例。

首先，创建数据库用户 dbuser，并指定其为超级用户。

```bash
$ sudo -u postgres createuser --superuser dbuser
```

然后，登录数据库控制台，设置 dbuser 用户的密码，完成后退出控制台。

```bash
> sudo -u postgres psql
>
> \password dbuser
>
> \q
```

接着，在 shell 命令行下，创建数据库 exampledb，并指定所有者为 dbuser。

```bash
$ sudo -u postgres createdb -O dbuser exampledb
```

## 登录数据库

添加新用户和新数据库以后，就要以新用户的名义登录数据库，这时使用的是 psql 命令。

```bash
$ psql -U dbuser -d exampledb -h 127.0.0.1 -p 5432
```

上面命令的参数含义如下：-U指定用户，-d指定数据库，-h指定服务器，-p指定端口。

输入上面命令以后，系统会提示输入 dbuser 用户的密码。输入正确，就可以登录控制台了。

psql 命令存在简写形式。如果当前 Linux 系统用户，同时也是 PostgreSQL 用户，则可以省略用户名（-U参数的部分）。举例来说，我的 Linux 系统用户名为ruanyf，且 PostgreSQL 数据库存在同名用户，则我以 ruanyf 身份登录Linux系统后，可以直接使用下面的命令登录数据库，且不需要密码。

```bash
$ psql exampledb
```

此时，如果 PostgreSQL 内部还存在与当前系统用户同名的数据库，则连数据库名都可以省略。比如，假定存在一个叫做 ruanyf 的数据库，则直接键入 psql 就可以登录该数据库。

```bash
$ psql
```

另外，如果要恢复外部数据，可以使用下面的命令。

```bash
$ psql exampledb < exampledb.sql
```

## 控制台命令

除了前面已经用到的 \password 命令（设置密码）和 \q 命令（退出）以外，控制台还提供一系列其他命令。

> - \h：查看 SQL 命令的解释，比如 \h select。
> - \?：查看 psql 命令列表。
> - \l：列出所有数据库。
> - \c [database_name]：连接其他数据库。
> - \d：列出当前数据库的所有表格。
> - \d [table_name]：列出某一张表格的结构。
> - \du：列出所有用户。
> - \e：打开文本编辑器。
> - \conninfo：列出当前数据库和连接的信息。

## 数据库操作

基本的数据库操作，就是使用一般的SQL语言。

> \# 创建新表
> CREATE TABLE user_tbl(name VARCHAR(20), signup_date DATE);
>
> \# 插入数据
> INSERT INTO user_tbl(name, signup_date) VALUES('张三', '2013-12-22');
>
> \# 选择记录
> SELECT * FROM user_tbl;
>
> \# 更新数据
> UPDATE user_tbl set name = '李四' WHERE name = '张三';
>
> \# 删除记录
> DELETE FROM user_tbl WHERE name = '李四' ;
>
> \# 添加栏位
> ALTER TABLE user_tbl ADD email VARCHAR(40);
>
> \# 更新结构
> ALTER TABLE user_tbl ALTER COLUMN signup_date SET NOT NULL;
>
> \# 更名栏位
> ALTER TABLE user_tbl RENAME COLUMN signup_date TO signup;
>
> \# 删除栏位
> ALTER TABLE user_tbl DROP COLUMN email;
>
> \# 表格更名
> ALTER TABLE user_tbl RENAME TO backup_tbl;
>
> \# 删除表格
> DROP TABLE IF EXISTS backup_tbl;

[阮一峰的网络日志 - PostgreSQL新手入门](https://www.ruanyifeng.com/blog/2013/12/getting_started_with_postgresql.html)
