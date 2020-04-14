# Celery-4.1 用户指南: Periodic Tasks

翻译[libing_thinking](https://me.csdn.net/u013148156) 最后发布于2017-11-21 11:00:21 阅读数 3998 收藏

展开

## 简介

------

`celery beat` 是一个调度器；它以常规的时间间隔开启任务，任务将会在集群中的可用节点上运行。

默认情况下，入口项是从 `beat_schedule` 设置中获取，但是自定义的存储也可以使用，例如在 SQL 数据库中存储入口项。

你必须保证一个调度一次只被一个调度器运行，否则将会形成重复任务。使用中央集权的方式意味着调度不需要被同步，并且服务可以在没有锁的情况下操作。

## 时区

------

默认情况下，周期性任务使用 UTC 时区，但是你可以使用 `timezone` 设置修改时区。

时区设置成 `Europe/London` 的示例：

```
timezone='Europe/London'1
```

这个设置必须添加到你的应用实例，或者通过直接配置(`app.conf.timezone = 'Europe/London'`)，或者如果你使用 `app.config_from_object`方法配置的话你可以将其添加到你的配置模块。查看配置这一节获取关于配置选项的跟多信息。

默认的调度器会自动探测时区的更改（调度器存储在 `celerybeat-schedule`文件中），并且会重置调度器，但是其他的调度器可能没有这么智能（例如：Django 数据库调度器，下面有讲到），这种情况下你必须自己重置调度器。

Django User:
Celery 建议并且兼容 Django1.4 中新引入的 `USE_TZ`设置。

对于DJango用户，`TIME_ZONE` 设置中声明的时区将会被应用，或者你可以通过 `timezone` 设置为 celery 声明一个自定义的时区。

当时区相关设置变更时数据库调度器不会自动重置，所以你必须自己重置：

```
$ python manage.py shell
>>> from djcelery.models import PeriodicTask
>>> PeriodicTask.objects.update(last_run_at=None)123
```

## Entries

------

想要周期性的调用一个任务，你必须在beat调度列表中添加一项。

```
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
    print(arg)12345678910111213141516171819202122
```

在 `on_after_configure` 句柄上设置这些意味着当使用 `test.s()` 时我们不会在模块级别对 app 求值。

`add_periodic_task()` 函数将会在 `beat_schedule` 设置中新增加一项，并且相同的设置也可以用来手动设置周期任务：

示例：每30秒运行一次 `tasks.add` 任务

```
app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tasks.add',
        'schedule': 30.0,
        'args': (16, 16)
    },
}
app.conf.timezone = 'UTC'12345678
```

注意：
如果你不清楚这些设置什么意思，请查看配置这一节。你可以直接在你的应用实例上设置这些选项，或者也可以使用一个单独的配置模块。

如果你给 args 提供一个单项的元组，别忘记构造器是逗号，不会一对括号。

为调度器使用 `timedelta` 意味着任务将以30秒为间隔发送（第一个任务将在 `celery beat` 启动后的30秒运行，以后每运行完一个任务，隔30秒再运行另一个）。

`Crontab` 类似的调度器也有，查看 `Crontab schedules` 这一节。

就像 `cron`，如果第一个任务在下一个任务到来之前没有完成，那么任务可能重叠。如果这是你所关注的，你应该使用一个锁策略来保证一次只有一个实例能运行（查看`Ensuring a task is only executed one at a time` 这一节）。

### Available Fields

------

- task
  要执行的任务的名称
- schedule
  执行的频率。

这可以是一个表示秒数的整数，一个 `timedelta` 或者一个 `crontab`。你还可以定义自己的调度器类型，只要扩展`schedule`接口。

- args
  位置参数(list 或者 tuple)
- kwargs
  关键字参数(dict)
- options
  执行选项（dict）
  这可以是 `apply_async()` 支持的任何参数 - `exchange, routing_key,expires` 等等。
- relative
  如果 `relative` 设置成真， `timedelta`调度器依据时钟调度。这意味着频率将根据`timedleta`的周期四舍五入到最近的秒，分，小时或者天。

默认情况下，`relative`值为假，频率没有四舍五入，而是相对于 `celery beat` 启动的时间。

## Crontab schedules

------

如果你想要对什么时候执行任务有更多的控制，例如，一天中某个特殊时间或者一周中某天，你可以使用`crontab`调度器类型：

```
from celery.schedules import crontab

app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'add-every-monday-morning': {
        'task': 'tasks.add',
        'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'args': (16, 16),
    },
}12345678910
```

Crontab 表达式的语法非常灵活。

一些示例：

| Example                                                      | Meaning                                                      |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| crontab()                                                    | 每分钟执行                                                   |
| crontab(minute=0, hour=0)                                    | 每天凌晨执行                                                 |
| crontab(minute=0, hour=’*/3’)                                | 每三个小时执行: midnight, 3am, 6am, 9am, noon, 3pm, 6pm, 9pm. |
| crontab(minute=0,hour=’0,3,6,9,12,15,18,21’)                 | 同上                                                         |
| crontab(minute=’*/15’)                                       | 每十五分钟执行                                               |
| crontab(day_of_week=’sunday’)                                | 星期天每分钟执行                                             |
| crontab(minute=’*‘,hour=’*‘, day_of_week=’sun’)              | 同上                                                         |
| crontab(minute=’*/10’,hour=’3,17,22’, day_of_week=’thu,fri’) | 每十分钟执行, 但是只在星期四、五的 3-4 am, 5-6 pm, and 10-11 pm |
| crontab(minute=0, hour=’*/2,*/3’)                            | 每两个小时及每三个小时执行，意思是: 除了下面时间的每个小时: 1am, 5am, 7am, 11am, 1pm, 5pm, 7pm, 11pm |
| crontab(minute=0, hour=’*/5’)                                | 每五个小时执行。这意味着将在 3pm 而不是 5pm 执行 (因为 3pm 等于 24 小时制的 15, 能被 5 整除) |
| crontab(minute=0, hour=’*/3,8-17’)                           | 每三个小时, 以及 (8am-5pm) 之间的小时执行                    |
| crontab(0, 0, day_of_month=’2’)                              | 每个月的第二天执行                                           |
| crontab(0, 0, day_of_month=’2-30/3’)                         | 每个月的偶数天执行                                           |
| crontab(0, 0,day_of_month=’1-7,15-21’)                       | 每个月的第一个和第三个星期执行                               |
| crontab(0, 0, day_of_month=’11’,month_of_year=’5’)           | 每年五月份的第十一天执行                                     |
| crontab(0, 0,month_of_year=’*/3’)                            | 每个季度的第一个月执行                                       |

查看 `celery.schedules.crontab` 这一节获取更多的信息。

## Solar schedules

------

如果你想任务依据日出、日落、黄昏、黎明时间来执行，你可以使用 `solar` 调度器类型：

```
from celery.schedules import solar

app.conf.beat_schedule = {
    # Executes at sunset in Melbourne
    'add-at-melbourne-sunset': {
        'task': 'tasks.add',
        'schedule': solar('sunset', -37.81753, 144.96715),
        'args': (16, 16),
    },
}12345678910
```

参数很简单： `solar(event, latitude, longitude)`

请确保为经度和纬度使用正确的符号：

| Sign | Argument   | Meaning |
| ---- | ---------- | ------- |
| +    | latitude   | North   |
| -    | latitude   | South   |
| +    | longtitude | East    |
| -    | longtitude | West    |

可能的事件类型有：

| Event             | Meaning                                                      |
| ----------------- | ------------------------------------------------------------ |
| dawn_astronomical | 天不完全黑的时候执行。 太阳在地平线下18度                    |
| dawn_nautical     | 地平线有充足的阳光并且可以看清一些事物; 形式化一点, 太阳在地平线下12度 |
| dawn_civil        | 有充足的阳光可以看清事物并且可以开始户外活动; 形式化一点, 太阳在地平线下6度 |
| sunrise           | 太阳的上边缘出现在东方地平线上时执行                         |
| solar_noon        | 一天中太阳距离地平线最高的位置时执行                         |
| sunset            | 傍晚太阳的上边缘消失在西方地平线上时执行                     |
| dusk_civil        | 黄昏的尽头, 事物仍然可见并且可以看到一些星星。形式化一点, 太阳在地平线下6度 |
| dusk_nautical     | 形式化一点, 太阳在地平线下12度。事物已经看不清，并且地平线也看不清了 |
| dusk_astronomical | 天完全黑时执行; 形式化一点, 太阳在地平线下18度               |

所有 `solar` 事件都使用 UTC 时间计算，因此不受你的 timezone 设置影响。

在极地区域，太阳可能不会每天都升起。这个调度器可以处理这种情况（即：当太阳没有升起，`sunrise` 事件不会触发）。只有 `solar_noon` 事件除外，这个事件是由太阳经过地球两极纵分地球的圆环的时刻定义的，即使太阳在地平线下它也会天天触发。

`Twilight` 定义为黎明到日出这段时间；以及日落到黄昏这段时间。依据你对 `twilight` 的定义（民用的、航海的或天文的），使用上述列表中的合适事件，你可以为你定义的`twilight` 触发一个事件，并且可以指定让事件在 `twilight` 开始还是结束的时刻触发。

查看 `celery.schedules.solar` 获取更多的信息。

## Starting the Scheduler

------

启动 `celery beat` 服务：

```
$ celery -A proj beat1
```

你可以通过使能工作单元的 `-B` 选项将 `beat` 嵌入到你的工作单元中，如果你不会启动多于一个工作单元，那么这是很便利的，但是这并不常用，并且也不推荐在生产环境使用：

```
$ celery -A proj worker -B1
```

Beat 需要在一个本地数据库文件（默认是 `celerybeat-schedule`文件 ）中保存任务的最后执行时间，所以需要有当前目录的写权限，或者你也可以为这个文件制定一个自定义的路径：

```
$ celery -A proj beat -s /home/celery/var/run/celerybeat-schedule1
```

注意：
使用 beat 守护进程，请查看相关文档。

### Using custom scheduler classes

------

自定义的调度器可以通过命令行中声明（使用 `--scheduler` 参数）。

默认的调度器是 `celery.beat.PersistentScheduler`，它将最后执行时间保存在本地一个 `shelve` 数据库文件中。

有一个 `django-celery-beat` 扩展可以将调度保存到Django数据库中，并且提供了一个方便的管理接口对运行的周期性任务进行管理。

安装和使用这个扩展：
\1. 使用 pip 安装这个包：

```
$ pip install django-celery-beat1
```

1. 在你 Django 项目的配置文件 `setting.py` 中将 `django_celery_beat` 添加到 `INSTALL_APPS` 中

```
INSTALLED_APPS = (
    ...,
    'django_celery_beat',
)1234
```

1. 应用 Django 数据迁移使得必要的数据库表被创建

```
$ python manage.py migrate1
```

1. 使用 `django_celery_beat.schedulers:DatabaseScheduler` 调度器：

```
$ celery -A proj beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler1
```

注意：
你也可以直接把他作为设置选项来添加

1. 访问 Django-Admin 接口，并设置一些周期性的任务

- [点赞 2](javascript:;)
- [收藏](javascript:;)
- [分享](javascript:;)





[参考](https://blog.csdn.net/u013148156/article/details/78582609)

