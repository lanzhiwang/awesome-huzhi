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

# 实际操作
# $ yum install postgresql12.x86_64 postgresql12-contrib.x86_64 postgresql12-devel.x86_64 postgresql12-libs.x86_64 postgresql12-server.x86_64

$ yum install postgresql12.x86_64 postgresql12-server.x86_64
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
[root@lanzhiwang-centos7 ~]#











$ yum install postgresql.x86_64 postgresql-server.x86_64

# 安装的软件包如下
postgresql-libs-9.2.24-4.el7_8.x86_64.rpm
postgresql-9.2.24-4.el7_8.x86_64.rpm
postgresql-server-9.2.24-4.el7_8.x86_64.rpm

# 安装的常见文件如下
$ rpm -ql postgresql-9.2.24-4.el7_8.x86_64
/usr/bin/clusterdb
/usr/bin/createdb
/usr/bin/createlang
/usr/bin/createuser
/usr/bin/dropdb
/usr/bin/droplang
/usr/bin/dropuser
/usr/bin/pg_config
/usr/bin/pg_dump
/usr/bin/pg_dumpall
/usr/bin/pg_restore
/usr/bin/psql  #
/usr/bin/reindexdb
/usr/bin/vacuumdb
...


$ rpm -ql postgresql-server-9.2.24-4.el7_8.x86_64
/etc/pam.d/postgresql
/usr/bin/initdb
/usr/bin/pg_basebackup
/usr/bin/pg_controldata
/usr/bin/pg_ctl
/usr/bin/pg_receivexlog
/usr/bin/pg_resetxlog
/usr/bin/postgres
/usr/bin/postgresql-check-db-dir
/usr/bin/postgresql-setup
/usr/bin/postmaster
/usr/lib/systemd/system/postgresql.service  #
/usr/lib/tmpfiles.d/postgresql.conf  #
...
/var/lib/pgsql
/var/lib/pgsql/.bash_profile
/var/lib/pgsql/backups
/var/lib/pgsql/data
/var/run/postgresql

```


