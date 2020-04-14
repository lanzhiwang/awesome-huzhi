# Celery-4.1 用户指南: Daemonization

翻译[libing_thinking](https://me.csdn.net/u013148156) 最后发布于2017-11-20 15:15:51 阅读数 3170 收藏

展开

## Generic init-scripts

------

查看Celery发布里的 `extra/generic-init.d/` 文件夹。

这个文件夹中包含了celery worker 程序的通用bash初始化脚本，可以运行在 Linux, FreeBSD, OpenBSD, 以及其他类Unix平台。

### Init-script: celeryd

Usage: /etc/init.d/celeryd {start|stop|restart|status}
Configuration file: /etc/default/celeryd

配置这个脚本来运行你的工作单元，你应该至少告诉它目录在哪什么时候开始（用来找到包含你应用的模块，或者你的配置模块）。

这个 `daemonization` 脚本是通过 `/etc/default/celeryd` 配置。这是一个 Shell 脚本，你可以下列配置选项等环境变量。添加影响工作单元的真正的环境变量，你还必须导出他们（e.g. export DISPLAY=”:0”）。

## 需要超级用户权限

这个初始化脚本只能被 root 用户使用，并且shell 配置文件的所有者也必须是 root。

没有权限的用户不必使用初始化脚本，他们可以使用 `celery multi` 工具（或者 `celery worker --detach`）：

```
$ celery multi start worker1 \
    -A proj \
    --pidfile="$HOME/run/celery/%n.pid" \
    --logfile="$HOME/log/celery/%n%I.log"

$ celery multi restart worker1 \
    -A proj \
    --logfile="$HOME/log/celery/%n%I.log" \
    --pidfile="$HOME/run/celery/%n.pid

$ celery multi stopwait worker1 --pidfile="$HOME/run/celery/%n.pid"1234567891011
```

#### 配置示例

------

这是一个python对象的配置示例：

/etc/default/celeryd:

```
# Names of nodes to start
#   most people will only start one node:
CELERYD_NODES="worker1"
#   but you can also start multiple and configure settings
#   for each in CELERYD_OPTS
#CELERYD_NODES="worker1 worker2 worker3"
#   alternatively, you can specify the number of nodes to start:
#CELERYD_NODES=10

# Absolute or relative path to the 'celery' command:
CELERY_BIN="/usr/local/bin/celery"
#CELERY_BIN="/virtualenvs/def/bin/celery"

# App instance to use
# comment out this line if you don't use an app
CELERY_APP="proj"
# or fully qualified:
#CELERY_APP="proj.tasks:app"

# Where to chdir at start.
CELERYD_CHDIR="/opt/Myproject/"

# Extra command-line arguments to the worker
CELERYD_OPTS="--time-limit=300 --concurrency=8"
# Configure node-specific settings by appending node name to arguments:
#CELERYD_OPTS="--time-limit=300 -c 8 -c:worker2 4 -c:worker3 2 -Ofair:worker1"

# Set logging level to DEBUG
#CELERYD_LOG_LEVEL="DEBUG"

# %n will be replaced with the first part of the nodename.
CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
CELERYD_PID_FILE="/var/run/celery/%n.pid"

# Workers should run as an unprivileged user.
#   You need to create this user manually (or you can choose
#   a user/group combination that already exists (e.g., nobody).
CELERYD_USER="celery"
CELERYD_GROUP="celery"

# If enabled pid and log directories will be created if missing,
# and owned by the userid/group configured.
CELERY_CREATE_DIRS=112345678910111213141516171819202122232425262728293031323334353637383940414243
```

#### 使用登录shell

------

你可以使用使用一个登录 shell 继承 `CELERY_USER` 的环境：

```
CELERYD_SU_ARGS="-l"1
```

注意不推荐这样做，而且你应该只有在绝对需要的时候才使用这个选项。

#### Django 配置示例

------

Django 用户现在使用与上述相同的模板，但是要确保定义你celery 应用实例的模块也给 `DJANGO_SETTINGS_MODULE` 设置了一个默认值，如`First steps with Django` 里的 Django 项目示例。

#### 可用的选项

------

- CELERY_APP
  使用的 app 应用实例
- CELERY_BIN
  celery 程序的绝对或者相对路径。例子：
  - celery
  - /usr/local/bin/celery
  - /virtualenvs/proj/bin/celery
  - /virtualenvs/proj/bin/python -m celery
- CELERY_NODES
  要启动的工作单元节点名称(空格分隔)
- CELERY_OPTS
  工作单元的附加命令行参数，查看 `celery worker --help` 可以获取到一个列表。它还支持 `multi` 使用的扩展语法来对每个节点单独配置。查看 `celery multi --help` 获取多节点配置示例。
- CELERY_CHDIR
  启动时路径修改到指定目录。默认情况下保持在当前目录。
- CELERY_PID_FILE
  PID 文件的绝对路径。默认是 `/var/run/celery/%n.pid`
- CELERY_LOG_FILE
  工作单元日志文件的绝对路径。默认是 `/var/log/celery/%n%I.log`。注意：当使用 prefork 池时，利用 `%I` 很重要，因为多个进程共享同一个日志文件时会产生竞态条件。
- CELERY_LOG_LEVEL
  日志单元日志文件。默认为 INFO。
- CELERY_USER
  运行工作单元的用户。默认是当前用户。
- CELERY_GROUP
  运行工作单元的用户组。默认是当前用户组。
- CELERY_CREATE_DIRS
  总是创建目录（日志目录以及PID文件目录）。默认只在木有自定义日志文件或者pid文件中创建目录。
- CELERY_CREATE_RUNDIR
  总是创建pid文件目录。当没有自定义pid文件时默认启用。
- CELERY_CREATE_LOGDIR
  总是创建日志文件目录。当没有自定义日志文件时默认启用。

### Init-script: celerybeat

Usage: /etc/init.d/celerybeat {start|stop|restart}
Configuration file: /etc/default/celerybeat or /etc/default/celeryd

#### 配置示例

------

这是一个python 对象的配置示例：

/etc/default/celerybeat:

```
# Absolute or relative path to the 'celery' command:
CELERY_BIN="/usr/local/bin/celery"
#CELERY_BIN="/virtualenvs/def/bin/celery"

# App instance to use
# comment out this line if you don't use an app
CELERY_APP="proj"
# or fully qualified:
#CELERY_APP="proj.tasks:app"

# Where to chdir at start.
CELERYBEAT_CHDIR="/opt/Myproject/"

# Extra arguments to celerybeat
CELERYBEAT_OPTS="--schedule=/var/run/celery/celerybeat-schedule"123456789101112131415
```

#### Django 配置示例

------

你可以使用上述相同的模板，但确保 `DJANGO_SETTINGS_MODULE` 变量被设置（并且被导出），并且 `CELERY_CHDIR` 设置成项目目录：

```
export DJANGO_SETTINGS_MODULE="settings"

CELERYD_CHDIR="/opt/MyProject"123
```

#### 可用的选项

------

- CELERY_APP
  使用的应用实例（`--app` 参数的值）
- CELERYBEAT_OPTS
  `celery beat` 的附加参数，查看 `celery beat --help`获取可用选项的列表。
- CELERYBEAT_PID_FILE
  PID文件的绝对路径。默认是 `/var/run/celeryd.pid`
- CELERYBEAT_LOG_FILE
  日志文件的绝对路径。默认是 `/var/log/celeryd.log`
- CELERYBEAT_LOG_LEVEL
  使用的日志级别。默认是 INFO。
- CELERYBEAT_USER
  运行 beat 的用户。默认是当前用户。
- CELERYBEAT_GROUP
  运行 beat 的用户组。默认是当前用户组。
- CELERY_CREATE_DIRS
  总是创建目录（日志目录以及PID文件目录）。默认只在木有自定义日志文件或者pid文件中创建目录。
- CELERY_CREATE_RUNDIR
  总是创建pid文件目录。当没有自定义pid文件时默认启用。
- CELERY_CREATE_LOGDIR
  总是创建日志文件目录。当没有自定义日志文件时默认启用。

#### Troubleshooting

------

如果你的初始化脚本不能工作，你应该在 `verbose` 模式运行它：

```
# sh -x /etc/init.d/celeryd start1
```

这能够为服务为何不能启动提供一些提示。

如果你的工作单元启动 `OK`，但是启动之后马上退出了，并且日志文件中没有任何证据可查，那么可能发生错误了，但是由于作为守护进程运行，标准输出已经关闭，你也不能再任何地方看到他们。这种情况下，你可以使用 `C_FAKEFORK` 环境变量来避免他称为守护进程：

```
# C_FAKEFORK=1 sh -x /etc/init.d/celeryd start1
```

这时，你应该能看到错误。

通常情况下，错误可能是由于文件读写权限不够导致的，也有可能是配置模块、用户模块、第三方库、甚至是celery 自己的语法错误（如果你发现bug，你应当报告）。

## 使用 systemd

------

extra/systemd/
Usage: systemctl {start|stop|restart|status} celery.service
Configuration file: /etc/conf.d/celery

### Service file: celery.service

这是一个`systemd` 服务配置的示例：
/etc/systemd/system/celery.service:

```
[Unit]
Description=Celery Service
After=network.target

[Service]
Type=forking
User=celery
Group=celery
EnvironmentFile=-/etc/conf.d/celery
WorkingDirectory=/opt/celery
ExecStart=/bin/sh -c '${CELERY_BIN} multi start ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
ExecStop=/bin/sh -c '${CELERY_BIN} multi stopwait ${CELERYD_NODES} \
  --pidfile=${CELERYD_PID_FILE}'
ExecReload=/bin/sh -c '${CELERY_BIN} multi restart ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'

[Install]
WantedBy=multi-user.target123456789101112131415161718192021
```

一旦你把这个文件放入 `/etc/systemd/system` 文件夹中，你应该运行 `systemctl daemon-reload` 命令来使得 Systemd 认识这个文件。每次你对该文件做完修改你都应该运行这个命令。

配置 user, group, chdir 设置：User, Group, 以及 WorkingDirectory 定义在 `/etc/systemd/system/celery.service`。

你还可以使用 `systemd-tmpfiles` 来创建工作目录（为日志文件及PID文件）。

file: `/etc/tmpfiles.d/celery.conf`

```
d /var/run/celery 0755 celery celery -
d /var/log/celery 0755 celery celery -12
```

#### 配置示例

------

下面是一个 python 对象的配置示例：
/etc/conf.d/celery:

```
# Name of nodes to start
# here we have a single node
CELERYD_NODES="w1"
# or we could have three nodes:
#CELERYD_NODES="w1 w2 w3"

# Absolute or relative path to the 'celery' command:
CELERY_BIN="/usr/local/bin/celery"
#CELERY_BIN="/virtualenvs/def/bin/celery"

# App instance to use
# comment out this line if you don't use an app
CELERY_APP="proj"
# or fully qualified:
#CELERY_APP="proj.tasks:app"

# How to call manage.py
CELERYD_MULTI="multi"

# Extra command-line arguments to the worker
CELERYD_OPTS="--time-limit=300 --concurrency=8"

# - %n will be replaced with the first part of the nodename.
# - %I will be replaced with the current child process index
#   and is important when using the prefork pool to avoid race conditions.
CELERYD_PID_FILE="/var/run/celery/%n.pid"
CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
CELERYD_LOG_LEVEL="INFO"12345678910111213141516171819202122232425262728
```

## 以超级权限运行工作单元

------

以超级权限运行一个工作单元在实际操作中是非常危险的事情。应该总是有些应急措施可以避免用root用户运行程序。Celery 可以运行使用消息中`pickle` 序列化的代码 - 这是危险的，特别是作为 root 用户运行。

默认情况下，celery 不会以 root 用户运行工作单元。相关的错误可能在日志文件中不可见，但是当 `C_FAKEFORK` 启用后可以看到。

强制 Celery 以 root 用户运行工作单元，可以使用 `C_FORCE_ROOT`。

当不设置 `C_FORCE_ROOT` 而使用 root 用户运行工作单元，工作单元会出现启动成功但是马上退出而没有明显的错误提示。

当在一个以root 用户使用的新的开发环境或者生产环境上运行项目时，这个问题就可能会出现。

## supervisor

------

- extra/supervisord in github

### launchd(macOS)

- extra/macOS in github







[参考](https://blog.csdn.net/u013148156/article/details/78581752)

