# Celery-4.1 用户指南：Testing with Celery

翻译[libing_thinking](https://me.csdn.net/u013148156) 最后发布于2017-11-24 10:42:05 阅读数 1005 收藏

展开

## 任务与单元测试

------

在单元测试中测试任务行为的推荐方法是用`mocking`。

**Eager mode**:
`task_always_eager` 设置启用的 eager 模式不适用于单元测试。

当使用eager模式，你只是测试工作单元中发生的行为的一个模拟，而实际所发生的和模拟的有许多不同。

Celery 任务就像一个web视图，它只定义在任务被调用的上下文环境中怎样执行操作。

这意味着任务只处理如序列化、消息头、重试等，而真正的逻辑在其他地方实现。

假如我们有如下一个任务：

```
from .models import Product


@app.task(bind=True)
def send_order(self, product_pk, quantity, price):
    price = Decimal(price)  # json serializes this to string.

    # models are passed by id, not serialized.
    product = Product.objects.get(product_pk)

    try:
        product.order(quantity, price)
    except OperationalError as exc:
        raise self.retry(exc=exc)1234567891011121314
```

你可以使用如下类似的`mocking`给这个任务编写单元测试：

```
from pytest import raises

from celery.exceptions import Retry

# for python 2: use mock.patch from `pip install mock`.
from unittest.mock import patch

from proj.models import Product
from proj.tasks import send_order

class test_send_order:

    @patch('proj.tasks.Product.order')  # < patching Product in module above
    def test_success(self, product_order):
        product = Product.objects.create(
            name='Foo',
        )
        send_order(product.pk, 3, Decimal(30.3))
        product_order.assert_called_with(3, Decimal(30.3))

    @patch('proj.tasks.Product.order')
    @patch('proj.tasks.send_order.retry')
    def test_failure(self, send_order_retry, product_order):
        product = Product.objects.create(
            name='Foo',
        )

        # Set a side effect on the patched methods
        # so that they raise the errors we want.
        send_order_retry.side_effect = Retry()
        product_order.side_effect = OperationalError()

        with raises(Retry):
            send_order(product.pk, 3, Decimal(30.6))12345678910111213141516171819202122232425262728293031323334
```

## Py.test

------

4.0版本新特性。

Celery 也是一个 pytest 插件，它添加了一些特性，使得你可以在你的集成（单元）测试中使用。

### Marks

------

celery - 设置测试应用配置

celery mark 使得你可以覆盖为单个测试用例设置的配置：

```
@pytest.mark.celery(result_backend='redis://')
def test_something():
    ...123
```

或者为一个类中所有测试用例设置的配置：

```
@pytest.mark.celery(result_backend='redis://')
class test_something:

    def test_one(self):
        ...

    def test_two(self):
        ...12345678
```

## Fixtures

------

### 函数范围

------

- `celery_app` - 测试使用的 Celery 应用实例

这个 fixture 返回一个Celery测试实例，你可以用它来进行测试

示例：

```
def test_create_task(celery_app, celery_worker):
    @celery_app.task
    def mul(x, y):
        return x * y

    assert mul.delay(4, 4).get(timeout=10) == 16123456
```

- `celery_worker` - 嵌入到激活的工作单元中。

这个fixture 启动了一个 Celery 实例，你可以用来进行集成测试。这个工作单元将在一个单独的线程中运行，并且随着测试的返回而关闭。

示例：

```
# Put this in your conftest.py
@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'amqp://',
        'result_backend': 'redis://'
    }

def test_add(celery_worker):
    mytask.delay()


# If you wish to override some setting in one test cases
# only - you can use the ``celery`` mark:
@pytest.mark.celery(result_backend='rpc')
def test_other(celery_worker):
    ...1234567891011121314151617
```

### 会话范围

------

- `celery_config` - 覆盖 celery 这个测试应用可以设置实例的配置。

你可以重新定义这个 fixture 来配置测试应用实例。

你的 fixture 返回的配置将被用来配置 `celery_app()` 以及 `celery_session_app()` fixtures。

示例：

```
@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'amqp://',
        'result_backend': 'rpc',
    }123456
```

- `celery_parameters` - 覆盖这个函数可以设置celery测试应用的参数。

你可以重新定义这个fixture来修改celery测试应用实例的`__init__`函数参数。相对于 `celery_config()`，当初始化 Celery 时这些是直接传递的。

你的 fixture 返回的配置会被用来设置 `celery_app()`以及 `celery_session_app()` fixtures。

示例：

```
@pytest.fixture(scope='session')
def celery_parameters():
    return {
        'task_cls':  my.package.MyCustomTaskClass,
        'strict_typing': False,
    }123456
```

- `celery_worker_parameters` - 覆盖它可以设置工作单元参数

你可以重新定义这个 fixture 来修改 celery 测试工作单元的 `__init__`函数参数。当工作单元初始化时，这些是直接传递给 `WorkController`的。

你的fixture返回的配置会被用来配置 `celery_worker()` 以及 `celery_session_worker()`fixtures。

```
@pytest.fixture(scope='session')
def celery_worker_parameters():
    return {
        'queues':  ('high-prio', 'low-prio'),
        'exclude_queues': ('celery'),
    }123456
```

- `celery_enable_logging` - 覆盖它可以在嵌入的工作单元中启用日志

你可以通过覆盖这个 fixture 来在嵌入的工作单元中启用日志。

示例：

```
@pytest.fixture(scope='session')
def celery_enable_logging():
    return True123
```

- `celery_incudes` - 为嵌入的工作单元添加额外的导入

你可以通过覆盖这个 fixture 在嵌入的工作单元启动时包含一些模块。

你可以让它返回一个要导入的模块名称的列表，可以是任务模块、信号注册模块，等等。

实例：

```
@pytest.fixture(scope='session')
def celery_includes():
    return [
        'proj.tests.tasks',
        'proj.tests.celery_signal_handlers',
    ]123456
```

- `celery_worker_pool` - 覆盖嵌入的工作单元使用的池

你可以通过覆盖这个 fixture 配置嵌入的工作单元使用的执行池。

示例：

```
@pytest.fixture(scope='session')
def celery_worker_pool():
    return 'prefork'123
```

**告警**：
除非你的整个测试套件启用了 `monkeypatches`，否则你不能使用 `gevent/eventlet` 池。

- `celery_session_worker` - 在整个会话过程中使用的嵌入的工作单元

这个 fixture 启动了一个工作单元，它在整个会话期间都是激活状态（它不会针对每个测试用例开启和关闭）

示例：

```
# Add this to your conftest.py
@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'amqp://',
        'result_backend': 'rpc',
    }

# Do this in your tests.
def test_add_task(celery_session_worker):
    assert add.delay(2, 2) == 41234567891011
```

**告警**
混合使用会话工作单元和瞬态工作单元可能是一个糟糕的主意…

- **celery_session_app** - 测试使用的 celery 应用实例（会话范围）

当其他会话范围的 fixture 需要引用一个 Celery 应用实例时，它可以被引用

- **use_celery_app_trap** - 当回退到默认应用实例时抛出一个异常

你可以在你的`conftest.py`文件中覆盖这个 fixture 来覆盖启用 `app trap`: 如果有实体访问默认或者当前应用实例，将抛出一个异常。

示例：

```
@pytest.fixture(scope='session')
def use_celery_app_trap():
    return True123
```

如果一个测试用例要访问默认应用实例，你使用 `depends_on_current_app` fixture 标记它。

```
@pytest.mark.usefixtures('depends_on_current_app')
def test_something():
    something()123
```

- [点赞](javascript:;)
- [收藏](javascript:;)
- [分享](javascript:;)



https://blog.csdn.net/u013148156/article/details/78622170

