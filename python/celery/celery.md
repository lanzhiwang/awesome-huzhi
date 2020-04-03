# celery

```
[root@isop216 bin]# ./celery --help
Usage: celery <command> [options]

Show help screen and exit.

Options:
  -A APP, --app=APP     app instance to use (e.g. module.attr_name)
  -b BROKER, --broker=BROKER
                        url to broker.  default is 'amqp://guest@localhost//'
  --loader=LOADER       name of custom loader class to use.
  --config=CONFIG       Name of the configuration module
  --workdir=WORKING_DIRECTORY
                        Optional directory to change to after detaching.
  -C, --no-color
  -q, --quiet
  --version             show program's version number and exit
  -h, --help            show this help message and exit

---- -- - - ---- Commands- -------------- --- ------------

+ Main:
|    celery worker
|    celery events
|    celery beat
|    celery shell
|    celery multi
|    celery amqp

+ Remote Control:
|    celery status

|    celery inspect --help
|    celery inspect active
|    celery inspect active_queues
|    celery inspect clock
|    celery inspect conf None
|    celery inspect memdump
|    celery inspect memsample
|    celery inspect objgraph None
|    celery inspect ping
|    celery inspect registered
|    celery inspect report
|    celery inspect reserved
|    celery inspect revoked
|    celery inspect scheduled
|    celery inspect stats

|    celery control --help
|    celery control add_consumer <queue> [exchange [type [routing_key]]]
|    celery control autoscale [max] [min]
|    celery control cancel_consumer <queue>
|    celery control disable_events
|    celery control enable_events
|    celery control pool_grow [N=1]
|    celery control pool_shrink [N=1]
|    celery control rate_limit <task_name> <rate_limit> (e.g. 5/s | 5/m | 5/h)>
|    celery control time_limit <task_name> <soft_secs> [hard_secs]

+ Utils:
|    celery purge
|    celery list
|    celery migrate
|    celery call
|    celery result
|    celery report
---- -- - - --------- -- - -------------- --- ------------

Type 'celery <command> --help' for help using a specific command.

[root@isop216 bin]#
您在 /var/spool/mail/root 中有邮件
[root@isop216 bin]#
[root@isop216 bin]# ./celery --version
3.1.19 (Cipater)
[root@isop216 bin]#
[root@isop216 bin]# ./celery worker --help
Usage: celery worker [options]

Start worker instance.

Examples::

    celery worker --app=proj -l info
    celery worker -A proj -l info -Q hipri,lopri

    celery worker -A proj --concurrency=4
    celery worker -A proj --concurrency=1000 -P eventlet

    celery worker --autoscale=10,0

Options:
  -A APP, --app=APP     app instance to use (e.g. module.attr_name)
  -b BROKER, --broker=BROKER
                        url to broker.  default is 'amqp://guest@localhost//'
  --loader=LOADER       name of custom loader class to use.
  --config=CONFIG       Name of the configuration module
  --workdir=WORKING_DIRECTORY
                        Optional directory to change to after detaching.
  -C, --no-color
  -q, --quiet
  -c CONCURRENCY, --concurrency=CONCURRENCY
                        Number of child processes processing the queue. The
                        default is the number of CPUs available on your
                        system.
  -P POOL_CLS, --pool=POOL_CLS
                        Pool implementation: prefork (default), eventlet,
                        gevent, solo or threads.
  --purge, --discard    Purges all waiting tasks before the daemon is started.
                        **WARNING**: This is unrecoverable, and the tasks will
                        be deleted from the messaging server.
  -l LOGLEVEL, --loglevel=LOGLEVEL
                        Logging level, choose between DEBUG, INFO, WARNING,
                        ERROR, CRITICAL, or FATAL.
  -n HOSTNAME, --hostname=HOSTNAME
                        Set custom hostname, e.g. 'w1.%h'. Expands: %h
                        (hostname), %n (name) and %d, (domain).
  -B, --beat            Also run the celery beat periodic task scheduler.
                        Please note that there must only be one instance of
                        this service.
  -s SCHEDULE_FILENAME, --schedule=SCHEDULE_FILENAME
                        Path to the schedule database if running with the -B
                        option. Defaults to celerybeat-schedule. The extension
                        ".db" may be appended to the filename. Apply
                        optimization profile.  Supported: default, fair
  --scheduler=SCHEDULER_CLS
                        Scheduler class to use. Default is
                        celery.beat.PersistentScheduler
  -S STATE_DB, --statedb=STATE_DB
                        Path to the state database. The extension '.db' may be
                        appended to the filename. Default: None
  -E, --events          Send events that can be captured by monitors like
                        celery events, celerymon, and others.
  --time-limit=TASK_TIME_LIMIT
                        Enables a hard time limit (in seconds int/float) for
                        tasks.
  --soft-time-limit=TASK_SOFT_TIME_LIMIT
                        Enables a soft time limit (in seconds int/float) for
                        tasks.
  --maxtasksperchild=MAX_TASKS_PER_CHILD
                        Maximum number of tasks a pool worker can execute
                        before it's terminated and replaced by a new worker.
  -Q QUEUES, --queues=QUEUES
                        List of queues to enable for this worker, separated by
                        comma. By default all configured queues are enabled.
                        Example: -Q video,image
  -X EXCLUDE_QUEUES, --exclude-queues=EXCLUDE_QUEUES
  -I INCLUDE, --include=INCLUDE
                        Comma separated list of additional modules to import.
                        Example: -I foo.tasks,bar.tasks
  --autoscale=AUTOSCALE
                        Enable autoscaling by providing max_concurrency,
                        min_concurrency. Example:: --autoscale=10,3 (always
                        keep 3 processes, but grow to 10 if necessary)
  --autoreload          Enable autoreloading.
  --no-execv            Don't do execv after multiprocessing child fork.
  --without-gossip      Do not subscribe to other workers events.
  --without-mingle      Do not synchronize with other workers at startup.
  --without-heartbeat   Do not send event heartbeats.
  --heartbeat-interval=HEARTBEAT_INTERVAL
                        Interval in seconds at which to send worker heartbeat
  -O OPTIMIZATION
  -D, --detach
  -f LOGFILE, --logfile=LOGFILE
                        Path to log file. If no logfile is specified, stderr
                        is used.
  --pidfile=PIDFILE     Optional file used to store the process pid. The
                        program will not start if this file already exists and
                        the pid is still alive.
  --uid=UID             User id, or user name of the user to run as after
                        detaching.
  --gid=GID             Group id, or group name of the main group to change to
                        after detaching.
  --umask=UMASK         Effective umask (in octal) of the process after
                        detaching.  Inherits the umask of the parent process
                        by default.
  --executable=EXECUTABLE
                        Executable to use for the detached process.
  --version             show program's version number and exit
  -h, --help            show this help message and exit
[root@isop216 bin]#



#### 示例

# addtask.pt
# Executing a simple task
from celery import Celery

app = Celery('addtask', broker='amqp://guest@localhost//')

@app.task
def add(x, y):
    return x + y


# addtaskmain.py
# RUN the AddTask example with
import addTask

if __name__ == '__main__':
    result = addTask.add.delay(5, 5)

celery --app=addtask worker -l info
python addtaskmain.py

```









[https://liang.readthedocs.io/en/latest/chapter/Celery%E6%95%99%E7%A8%8B.html](https://liang.readthedocs.io/en/latest/chapter/Celery教程.html)





