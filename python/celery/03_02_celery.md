# Celery 学习笔记（2）定时任务

## 定时任务

Celery 中启动定时任务有两种方式

1. 在配置文件中指定

2. 在程序中指定

```python
# cele.py
import celery

app = celery.Celery('cele', broker='redis://localhost:6379')

@app.task
def send(message):
    return message

app.conf.beat_schedule = {
    'send-every-10-seconds': {
        'task': 'cele.send',
        'schedule': 10.0,
        'args': ('Hello World', )
    }
}
```

可以通过在配置文件中编写 beat_schedule 属性，来配置周期性任务，上面的示例配置了一个每十秒执行一次的周期任务，任务为 cele.send，参数为 ‘Hello World’。当然你也可以将这个配置写到单独的配置文件中进行读取。这种配置的方式可以支持多个参数，

* task： 指定任务的名字

* schedule：设定任务的调度方式，可以是一个表示秒的整数，也可以是一个 timedelta 对象，或者是一个 crontab 对象，总之就是设定任务如何重复执行

* args： 任务的参数列表

* kwargs：任务的参数字典

* options：所有 apply_async 所支持的参数

同时官方文档中也指出，可以通过下面这种方式对定时任务进行设置。

```python
from celery import Celery
from celery.schedules import crontab

app = Celery()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )

@app.task
def test(arg):
    print(arg)
```

Celery 提供了一个 crontab 的对象，可以对于定时任务进行更为精确的时间设置，而不仅限于多少秒重复一次这种简单的任务。下面用例子的方式来说明一下。

```python
from celery.schedules import crontab

# 每分钟执行一次
c1 = crontab()

# 每天凌晨十二点执行
c2 = crontab(minute=0, hour=0)

# 每十五分钟执行一次
crontab(minute='*/15')

# 每周日的每一分钟执行一次
crontab(minute='*',hour='*', day_of_week='sun')

# 每周三，五的三点，七点和二十二点没十分钟执行一次
crontab(minute='*/10',hour='3,17,22', day_of_week='thu,fri')
```

到目前为止，只是对任务进行了配置，但是还没有实际运行任务，要支持周期任务，需要启动一个组件 beat，它用于对任务进行调度，我们以 cele.py 为例进行说明。

```bash
celery -A cele beat
```

这个命令会启动 cele 应用的 beat，当然也可以在启动 worker 的时候使用 -B 参数同时启动 beat 。

```bash
celery -A cele worker -l info -B
```

[参考](https://blog.csdn.net/preyta/article/details/54172961)
