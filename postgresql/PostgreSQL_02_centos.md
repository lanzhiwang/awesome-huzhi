# PostgreSQL In Centos

## 安装

```bash
# Install the repository RPM:
yum install https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm

# Install PostgreSQL:
yum install postgresql12-server

# Optionally initialize the database and enable automatic start:
/usr/pgsql-12/bin/postgresql-12-setup initdb
systemctl enable postgresql-12
systemctl start postgresql-12

############################################################

# 实际操作
# $ yum install postgresql12.x86_64 postgresql12-contrib.x86_64 postgresql12-devel.x86_64 postgresql12-libs.x86_64 postgresql12-server.x86_64

$ yum install postgresql12.x86_64 postgresql12-server.x86_64
# 安装的软件包如下
postgresql12
postgresql12-server
libicu
postgresql12-libs

$ rpm -ql postgresql12
/usr/pgsql-12/bin/clusterdb
/usr/pgsql-12/bin/createdb
/usr/pgsql-12/bin/createuser
/usr/pgsql-12/bin/dropdb
/usr/pgsql-12/bin/dropuser
/usr/pgsql-12/bin/pg_archivecleanup
/usr/pgsql-12/bin/pg_basebackup
/usr/pgsql-12/bin/pg_config
/usr/pgsql-12/bin/pg_dump
/usr/pgsql-12/bin/pg_dumpall
/usr/pgsql-12/bin/pg_isready
/usr/pgsql-12/bin/pg_receivewal
/usr/pgsql-12/bin/pg_restore
/usr/pgsql-12/bin/pg_rewind
/usr/pgsql-12/bin/pg_test_fsync
/usr/pgsql-12/bin/pg_test_timing
/usr/pgsql-12/bin/pg_upgrade
/usr/pgsql-12/bin/pg_waldump
/usr/pgsql-12/bin/pgbench
/usr/pgsql-12/bin/psql
/usr/pgsql-12/bin/reindexdb
/usr/pgsql-12/bin/vacuumdb
/usr/pgsql-12/lib/bitcode
...

$ rpm -ql postgresql12-server
/etc/pam.d/postgresql
/etc/sysconfig/pgsql
/usr/lib/systemd/system/postgresql-12.service
/usr/lib/tmpfiles.d/postgresql-12.conf
/usr/pgsql-12/bin/initdb
/usr/pgsql-12/bin/pg_checksums
/usr/pgsql-12/bin/pg_controldata
/usr/pgsql-12/bin/pg_ctl
/usr/pgsql-12/bin/pg_resetwal
/usr/pgsql-12/bin/postgres
/usr/pgsql-12/bin/postgresql-12-check-db-dir
/usr/pgsql-12/bin/postgresql-12-setup
/usr/pgsql-12/bin/postmaster
...
/var/lib/pgsql
/var/lib/pgsql/12
/var/lib/pgsql/12/backups
/var/lib/pgsql/12/data
/var/run/postgresql

$ /usr/pgsql-12/bin/postgresql-12-setup initdb
Initializing database ... OK

$ ll /var/lib/pgsql/12/
总用量 12
drwx------  2 postgres postgres 4096 6月  15 07:22 backups
drwx------ 20 postgres postgres 4096 8月   6 00:00 data
-rw-------  1 postgres postgres  921 8月   5 21:27 initdb.log
$ ll /var/lib/pgsql/12/data/
总用量 132
drwx------ 6 postgres postgres  4096 8月   6 07:58 base
-rw------- 1 postgres postgres    30 8月   6 00:00 current_logfiles
drwx------ 2 postgres postgres  4096 8月   5 21:32 global
drwx------ 2 postgres postgres  4096 8月   6 00:00 log
drwx------ 2 postgres postgres  4096 8月   5 21:27 pg_commit_ts
drwx------ 2 postgres postgres  4096 8月   5 21:27 pg_dynshmem
-rw------- 1 postgres postgres  4269 8月   5 21:27 pg_hba.conf
-rw------- 1 postgres postgres  1636 8月   5 21:27 pg_ident.conf
drwx------ 4 postgres postgres  4096 8月   6 08:03 pg_logical
drwx------ 4 postgres postgres  4096 8月   5 21:27 pg_multixact
drwx------ 2 postgres postgres  4096 8月   5 21:28 pg_notify
drwx------ 2 postgres postgres  4096 8月   5 21:27 pg_replslot
drwx------ 2 postgres postgres  4096 8月   5 21:27 pg_serial
drwx------ 2 postgres postgres  4096 8月   5 21:27 pg_snapshots
drwx------ 2 postgres postgres  4096 8月   5 21:27 pg_stat
drwx------ 2 postgres postgres  4096 8月   6 08:08 pg_stat_tmp
drwx------ 2 postgres postgres  4096 8月   5 21:27 pg_subtrans
drwx------ 2 postgres postgres  4096 8月   5 21:27 pg_tblspc
drwx------ 2 postgres postgres  4096 8月   5 21:27 pg_twophase
-rw------- 1 postgres postgres     3 8月   5 21:27 PG_VERSION
drwx------ 3 postgres postgres  4096 8月   5 21:27 pg_wal
drwx------ 2 postgres postgres  4096 8月   5 21:27 pg_xact
-rw------- 1 postgres postgres    88 8月   5 21:27 postgresql.auto.conf
-rw------- 1 postgres postgres 26632 8月   5 21:27 postgresql.conf
-rw------- 1 postgres postgres    58 8月   5 21:28 postmaster.opts
-rw------- 1 postgres postgres   103 8月   5 21:28 postmaster.pid

$ systemctl enable postgresql-12
$ systemctl start postgresql-12
$ systemctl status postgresql-12

$ ll /usr/bin/psql
/usr/bin/psql -> /etc/alternatives/pgsql-psql
$ ll /etc/alternatives/pgsql-psql
/etc/alternatives/pgsql-psql -> /usr/pgsql-12/bin/psql
$ ll /usr/pgsql-12/bin/psql
/usr/pgsql-12/bin/psql

# 验证新增的 postgres Linux 用户
$ cat /etc/passwd | grep postgres
postgres:x:26:26:PostgreSQL Server:/var/lib/pgsql:/bin/bash

```

## 初始化操作

```bash
# 基本操作
# 切换到 postgres 用户
$ su - postgres
# 登录控制台
-bash-4.2$ /usr/pgsql-12/bin/psql
psql (12.3)
Type "help" for help.

# 为 postgres 用户设置一个密码
postgres=# \password postgres
Enter new password:
Enter it again:
# 列出所有的数据库
postgres=# \l
                                  List of databases
   Name    |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges
-----------+----------+----------+-------------+-------------+-----------------------
 postgres  | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 template0 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
           |          |          |             |             | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
           |          |          |             |             | postgres=CTc/postgres
(3 rows)

postgres=#
# 列出所有的数据表
postgres=# \d
Did not find any relations.
# 列出所有的用户
postgres=# \du
                                   List of roles
 Role name |                         Attributes                         | Member of
-----------+------------------------------------------------------------+-----------
 postgres  | Superuser, Create role, Create DB, Replication, Bypass RLS | {}

postgres=#
# 退出
postgres=# \q
-bash-4.2$
-bash-4.2$ exit
logout

# 修改配置文件
sed -i "s#local   all             all                                     peer#local   all             all                                     trust#g" /var/lib/pgsql/12/data/pg_hba.conf

sed -i "s#host    all             all             127.0.0.1/32            ident#host    all             all             127.0.0.1/32            trust#g" /var/lib/pgsql/12/data/pg_hba.conf

$ systemctl restart postgresql-12
$ systemctl status postgresql-12

```

## 创建数据库

```bash
$ adduser dbuser
$ cat /etc/passwd | grep dbuser
dbuser:x:1000:1000::/home/dbuser:/bin/bash

$  su - postgres
上一次登录：三 8月  5 21:31:46 CST 2020pts/1 上
-bash-4.2$ psql
psql (12.3)
Type "help" for help.

postgres=# \du
                                   List of roles
 Role name |                         Attributes                         | Member of
-----------+------------------------------------------------------------+-----------
 postgres  | Superuser, Create role, Create DB, Replication, Bypass RLS | {}

postgres=# \l
                                  List of databases
   Name    |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges
-----------+----------+----------+-------------+-------------+-----------------------
 postgres  | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 template0 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
           |          |          |             |             | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
           |          |          |             |             | postgres=CTc/postgres
(3 rows)

postgres=# CREATE USER dbuser WITH PASSWORD 'password';
CREATE ROLE
postgres=# CREATE DATABASE exampledb OWNER dbuser;
CREATE DATABASE
postgres=# GRANT ALL PRIVILEGES ON DATABASE exampledb to dbuser;
GRANT
postgres=# \du
                                   List of roles
 Role name |                         Attributes                         | Member of
-----------+------------------------------------------------------------+-----------
 dbuser    |                                                            | {}
 postgres  | Superuser, Create role, Create DB, Replication, Bypass RLS | {}

postgres=#
postgres=# \l
                                  List of databases
   Name    |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges
-----------+----------+----------+-------------+-------------+-----------------------
 exampledb | dbuser   | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =Tc/dbuser           +
           |          |          |             |             | dbuser=CTc/dbuser
 postgres  | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 template0 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
           |          |          |             |             | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
           |          |          |             |             | postgres=CTc/postgres
(4 rows)

postgres=#
postgres=# \q
-bash-4.2$ exit
logout
$
$ psql -U postgres -d postgres -h 127.0.0.1 -p 5432
psql (12.3)
输入 "help" 来获取帮助信息.

postgres=# \l
                                     数据库列表
   名称    |  拥有者  | 字元编码 |  校对规则   |    Ctype    |       存取权限
-----------+----------+----------+-------------+-------------+-----------------------
 exampledb | dbuser   | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =Tc/dbuser           +
           |          |          |             |             | dbuser=CTc/dbuser
 postgres  | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 template0 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
           |          |          |             |             | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
           |          |          |             |             | postgres=CTc/postgres
(4 行记录)

postgres=# \c exampledb
您现在已经连接到数据库 "exampledb",用户 "postgres".
exampledb=# \q

$ psql -U dbuser -d exampledb -h 127.0.0.1 -p 5432
psql (12.3)
输入 "help" 来获取帮助信息.

exampledb=> \l
                                     数据库列表
   名称    |  拥有者  | 字元编码 |  校对规则   |    Ctype    |       存取权限
-----------+----------+----------+-------------+-------------+-----------------------
 exampledb | dbuser   | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =Tc/dbuser           +
           |          |          |             |             | dbuser=CTc/dbuser
 postgres  | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 template0 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
           |          |          |             |             | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
           |          |          |             |             | postgres=CTc/postgres
(4 行记录)

exampledb=> \d
没有找到任何关系.
exampledb=> \q
$

```
