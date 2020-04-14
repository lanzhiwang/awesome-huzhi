# Celery-4.1 用户指南: Configuration and defaults

这篇文档描述了可用的配置选项。

如果你使用默认的加载器，你必须创建 `celeryconfig.py` 模块并且保证它在 python 路径中。

## 配置文件示例

以下是配置示例，你可以从这个开始。它包括运行一个基本 Celery 应用的所有基础设置。

```python
## Broker settings.
broker_url = 'amqp://guest:guest@localhost:5672//'

## List of modules to import when the Celery worker starts.
imports = ('myapp.tasks',)

## Using the database to store task state and results.
result_backend = 'db+sqlite:///results.db'

task_annotations = {
    'tasks.add': {
        'rate_limit': '10/s'
    }
}
```

## 新的小写设置

4.0 版本引入了新的小写设置名称以及社会组织。

与以前版本的不同，除了设置项名称变为小写字母外，还有一个前缀的重命名，例如 `celerybeat_` 变为 `beat_`，`celeryd_` 变为 `worker`，以及很多顶级 `celery_` 设置重命名成了 `task_` 前缀。

Celery 仍然能读取老的配置文件，所以并不仓促迁移到新的设置格式。

| Setting name                      | Replace with                  |
| --------------------------------- | ----------------------------- |
| CELERY_ACCEPT_CONTENT             | accept_content                |
| CELERY_ENABLE_UTC                 | enable_utc                    |
| CELERY_IMPORTS                    | imports                       |
| CELERY_INCLUDE                    | include                       |
| CELERY_TIMEZONE                   | timezone                      |
| CELERYBEAT_MAX_LOOP_INTERVAL      | beat_max_loop_interval        |
| CELERYBEAT_SCHEDULE               | beat_schedule                 |
| CELERYBEAT_SCHEDULER              | beat_scheduler                |
| CELERYBEAT_SCHEDULE_FILENAME      | beat_schedule_filename        |
| CELERYBEAT_SYNC_EVERY             | beat_sync_every               |
| BROKER_URL                        | broker_url                    |
| BROKER_TRANSPORT                  | broker_transport              |
| BROKER_TRANSPORT_OPTIONS          | broker_transport_options      |
| BROKER_CONNECTION_TIMEOUT         | broker_connection_timeout     |
| BROKER_CONNECTION_RETRY           | broker_connection_retry       |
| BROKER_CONNECTION_MAX_RETRIES     | broker_connection_max_retries |
| BROKER_FAILOVER_STRATEGY          | broker_failover_strategy      |
| BROKER_HEARTBEAT                  | broker_heartbeat              |
| BROKER_LOGIN_METHOD               | broker_login_method           |
| BROKER_POOL_LIMIT                 | broker_pool_limit             |
| BROKER_USE_SSL                    | broker_use_ssl                |
| CELERY_CACHE_BACKEND              | cache_backend                 |
| CELERY_CACHE_BACKEND_OPTIONS      | cache_backend_options         |
| CASSANDRA_COLUMN_FAMILY           | cassandra_table               |
| CASSANDRA_ENTRY_TTL               | cassandra_entry_ttl           |
| CASSANDRA_KEYSPACE                | cassandra_keyspace            |
| CASSANDRA_PORT                    | cassandra_port                |
| CASSANDRA_READ_CONSISTENCY        | cassandra_read_consistency    |
| CASSANDRA_SERVERS                 | cassandra_servers             |
| CASSANDRA_WRITE_CONSISTENCY       | cassandra_write_consistency   |
| CELERY_COUCHBASE_BACKEND_SETTINGS | couchbase_backend_settings    |
| CELERY_MONGODB_BACKEND_SETTINGS   | mongodb_backend_settings      |
| CELERY_EVENT_QUEUE_EXPIRES        | event_queue_expires           |
| CELERY_EVENT_QUEUE_TTL            | event_queue_ttl               |
| CELERY_EVENT_QUEUE_PREFIX         | event_queue_prefix            |
| CELERY_EVENT_SERIALIZER           | event_serializer              |
| CELERY_REDIS_DB                   | redis_db                      |
| CELERY_REDIS_HOST                 | redis_host                    |
| CELERY_REDIS_MAX_CONNECTIONS      | redis_max_connections         |
| CELERY_REDIS_PASSWORD             | redis_password                |
| CELERY_REDIS_PORT                 | redis_port                    |
| CELERY_RESULT_BACKEND             | result_backend                |
| CELERY_MAX_CACHED_RESULTS         | result_cache_max              |
| CELERY_MESSAGE_COMPRESSION        | result_compression            |
| CELERY_RESULT_EXCHANGE            | result_exchange               |
| CELERY_RESULT_EXCHANGE_TYPE       | result_exchange_type          |
| CELERY_TASK_RESULT_EXPIRES        | result_expires                |
| CELERY_RESULT_PERSISTENT          | result_persistent             |
| CELERY_RESULT_SERIALIZER          | result_serializer             |
| CELERY_RESULT_DBURI               | Use result_backend instead.   |
| CELERY_RESULT_ENGINE_OPTIONS      | database_engine_options       |
| DB_SHORT_LIVED_SESSIONS           | database_short_lived_sessions |
| CELERY_RESULT_DB_TABLE_NAMES      | database_db_names             |
| CELERY_SECURITY_CERTIFICATE       | security_certificate          |
| CELERY_SECURITY_CERT_STORE        | security_cert_store           |
| CELERY_SECURITY_KEY               | security_key                  |
| CELERY_TASK_ACKS_LATE             | task_acks_late                |
| CELERY_TASK_ALWAYS_EAGER          | task_always_eager             |
| CELERY_TASK_ANNOTATIONS           | task_annotations              |
| CELERY_TASK_COMPRESSION           | task_compression              |
| CELERY_TASK_CREATE_MISSING_QUEUES | task_create_missing_queues    |
| CELERY_TASK_DEFAULT_DELIVERY_MODE | task_default_delivery_mode    |
| CELERY_TASK_DEFAULT_EXCHANGE      | task_default_exchange         |
| CELERY_TASK_DEFAULT_EXCHANGE_TYPE | task_default_exchange_type    |
| CELERY_TASK_DEFAULT_QUEUE         | task_default_queue            |
| CELERY_TASK_DEFAULT_RATE_LIMIT    | task_default_rate_limit       |
| CELERY_TASK_DEFAULT_ROUTING_KEY   | task_default_routing_key      |
| CELERY_TASK_EAGER_PROPAGATES      | task_eager_propagates         |
| CELERY_TASK_IGNORE_RESULT         | task_ignore_result            |
| CELERY_TASK_PUBLISH_RETRY         | task_publish_retry            |
| CELERY_TASK_PUBLISH_RETRY_POLICY  | task_publish_retry_policy     |
| CELERY_TASK_QUEUES                | task_queues                   |
| CELERY_TASK_ROUTES                | task_routes                   |
| CELERY_TASK_SEND_SENT_EVENT       | task_send_sent_event          |
| CELERY_TASK_SERIALIZER            | task_serializer               |
| CELERYD_TASK_SOFT_TIME_LIMIT      | task_soft_time_limit          |
| CELERYD_TASK_TIME_LIMIT           | task_time_limit               |
| CELERY_TRACK_STARTED              | task_track_started            |
| CELERYD_AGENT                     | worker_agent                  |
| CELERYD_AUTOSCALER                | worker_autoscaler             |
| CELERYD_CONCURRENCY               | worker_concurrency            |
| CELERYD_CONSUMER                  | worker_consumer               |
| CELERY_WORKER_DIRECT              | worker_direct                 |
| CELERY_DISABLE_RATE_LIMITS        | worker_disable_rate_limits    |
| CELERY_ENABLE_REMOTE_CONTROL      | worker_enable_remote_control  |
| CELERYD_HIJACK_ROOT_LOGGER        | worker_hijack_root_logger     |
| CELERYD_LOG_COLOR                 | worker_log_color              |
| CELERYD_LOG_FORMAT                | worker_log_format             |
| CELERYD_WORKER_LOST_WAIT          | worker_lost_wait              |
| CELERYD_MAX_TASKS_PER_CHILD       | worker_max_tasks_per_child    |
| CELERYD_POOL                      | worker_pool                   |
| CELERYD_POOL_PUTLOCKS             | worker_pool_putlocks          |
| CELERYD_POOL_RESTARTS             | worker_pool_restarts          |
| CELERYD_PREFETCH_MULTIPLIER       | worker_prefetch_multiplier    |
| CELERYD_REDIRECT_STDOUTS          | worker_redirect_stdouts       |
| CELERYD_REDIRECT_STDOUTS_LEVEL    | worker_redirect_stdouts_level |
| CELERYD_SEND_EVENTS               | worker_send_task_events       |
| CELERYD_STATE_DB                  | worker_state_db               |
| CELERYD_TASK_LOG_FORMAT           | worker_task_log_format        |
| CELERYD_TIMER                     | worker_timer                  |
| CELERYD_TIMER_PRECISION           | worker_timer_precision        |

## 配置指示

### 通用设置

- accept_content

  默认值: {‘json’} (set, list, or tuple).

  允许的内容类型/序列化器的白名单
  
  如果接收到一个消息，其内容类型不再上述列表中，它将会被丢弃并抛出一个错误。
  
  默认情况下，任意内容类型都是启用的，包括 pickle 以及 yaml，所以确保不受信任的第三方不能访问你的消息中间件。查看安全这一节获取更多信息。

示例：

```python
# using serializer name
accept_content = ['json']

# or the actual content-type (MIME)
accept_content = ['application/json']
```

### 时间与日期设置

- enable_utc

  2.5 版本新特性。

  默认值：从 3.0 版本开始默认启用
  
  一旦启用，消息中的日期和时间将会转化成 UTC 时区。
  
  注意2.5版本以下的工作单元将会认为所有消息都使用的本地时区，所以只有在所有的工作单元都升级了的情况下再启用这个特性。

- timezone

  2.5版本新特性

  默认值： “UTC”
  
  设置 Celery 使用一个自定义的时区。这个时区值可以是 pytz 库支持的任意时区。
  
  如果没有设置，UTC 时区将被使用。为了向后兼容，还提供了一个 enable_utc 设置，如果他设置成假，将使用系统本地时区。

### 任务设置

- task_annotations

  这个设置可以用来在配置文件中重写任意任务属性。这个设置可以是一个字典，获取一个annotation 对象的列表，这个列表对任务进行过滤，对匹配的任务名称起作用，并返回待更改属性的一个映射。

以下将更改 tasks.add 任务的 rate_limit 属性：

```python
task_annotations = {'tasks.add': {'rate_limit': '10/s'}}
```

或者对所有的任务更改：

```python
task_annotations = {'*': {'rate_limit': '10/s'}}
```

你还可以更改方法，例如 on_failure 处理函数：

```python
def my_on_failure(self, exc, task_id, args, kwargs, einfo):
    print('Oh no! Task failed: {0!r}'.format(exc))

task_annotations = {'*': {'on_failure': my_on_failure}}
```

如果你需要更灵活的控制，那么你可以使用对象而不是字典来选择任务来进行注解：

```python
class MyAnnotate(object):
    def annotate(self, task):
        if task.name.startswith('tasks.'):
            return {'rate_limit': '10/s'}

task_annotations = (MyAnnotate(), {other,})
```

- task_compression

  默认值： None

  任务消息的默认压缩算法。可以是 gzip、bzip2(如果可用)，或者任意在 Kombu 压缩模式注册表中注册的自定义压缩算法。
  
  默认发送未压缩的消息。

- task_protocol

  默认值：2（从 4.0 版本开始）
  
  设置默认的任务消息协议版本。支持的协议：1 和 2
  
  协议 2 在 3.1.24 以及 4.x+ 被支持

- task_serializer

  默认值：“json”（从 4.0 版本开始，更早: pickle ）

  一个表示使用的默认序列化方法的字符串。可以是 json(默认)、pickle、 yaml、msgpack，或者任意在 kombu.serialization.registry 中注册过的自定义序列化方法。
  
  另见：Serializers

- task_publish_retry

  2.2 版本新特性

  默认值：启用
  
  决定当连接丢失或者其他连接错误时任务消息的发布是否会重试，查看 `task_publish_retry_policy`。

- task_publish_retry_policy

  2.2版本新特性

  默认值：查看 Message Sending Retry。
  
  定义当连接丢失或者其他连接错误时任务消息的发布重试策略。

### 任务执行设置

- task_always_eager

  默认值：禁用
  
  如果设置成 True，所有的任务都将在本地执行直到任务返回。apply_async() 以及 Task.delay() 将返回一个 EagerResult 实例，模拟 AsyncResult 实例的 API 和行为，除了这个结果是已经计算过的之外。
  
  也就是说，任务将会在本地执行而不是发送到队列。

- task_eager_propagates

  默认值：禁用
  
  如果设置成 True，本地执行的任务（使用 task.apply()，或者 task_always_eager 被启用）将传递异常。
  
  这与使用 apply() 带 throw=True 参数有同样的效果。

- task_remote_tracebacks

  默认值：禁用
  
  如果启用了，当重新抛出任务错误时，任务结果将会包括工作单元的堆栈信息。
  
  它需要 tblib 库，可以通过 pip 安装：

```bash
$ pip install celery[tblib]
```
查看 Bundles 获取关于组合多个扩展需求的信息。

- task_ignore_result

  默认值：禁用
  
  是否存储任务返回值（tombstones）。如果你只是想在发生错误的时候记录返回值，可以设置：task_store_errors_even_if_ignored

- task_store_errors_even_if_ignored

  默认值：禁用
  
  如果设置了，即使 task_ignore_result 启用了，工作单元也会在结果后端中存储所有的任务错误。

- task_track_started

  默认值：禁用
  
  如果设置成真，当任务被工作单元执行时，任务将报告它的状态为 started。默认值是假，因为通常行为是不做这种粒度级别的汇报。任务会处于 pending、finished 或者 waiting to be retried。当有长时间任务，并且需要知道当前正在运行什么任务时，有一个 started 状态将会很有用。

- task_time_limit

  默认值：没有时间限制
  
  任务的硬时间限制，以秒为单位。如果这个时间限制被超过，处理任务的工作单元进程将会被杀死并使用一个新的替代。
  
- task_soft_time_limit

  默认值：没有时间限制
  
  任务的软时间限制，以秒为单位
  
  当这个时间限制超过后，SoftTimeLimitExceeded 异常将会被抛出。例如，任务可以捕获这个异常在硬时间限制到达之前对环境进行清理：

```python
from celery.exceptions import SoftTimeLimitExceeded

@app.task
def mytask():
    try:
        return do_work()
    except SoftTimeLimitExceeded:
        cleanup_in_a_hurry()
```

- task_acks_late

  默认值：禁用
  
  延迟确认意味着任务消息将在任务执行完成之后再进行确认，而不是刚开始时（默认行为）。
  
  另见：FAQ： Shoud I use retry or acks_late

- task_reject_on_worker_lost

  默认值：禁用
  
  即使 task_acks_late 被启用，当处理任务的工作单元异常退出或者收到信号而退出时工作单元将会确认任务消息。
  
  将这个设置成真可以让消息重新入队，所以任务将会被再执行，在同一个工作单元或者另外一个工作单元。
  
  告警：启用这个可能导致消息循环；确保你知道你在做什么

- task_default_rate_limit

  默认值：没有速率限制
  
  任务的全局默认速率限制
  
  当任务没有一个自定义的速率限制时，这个值将被使用
  
  另见：worker_disable_rate_limits 设置可以禁用所有的速率限制

### 任务结果后端设置

- result_backend

  默认值：默认不启用结果后端
  
  用来存储结果的后端。可以是下列之一：
  
  1. rpc  以 AMQP 消息形式发送结果。查看 RPC 后端设置

  2. database  使用一个 SQLAlchemy 支持的结构化数据库。查看数据库后端设置

  3. redis  使用 Redis 存储结果。查看 Redis 后端设置

  4. cache  使用 Memcached 存储结果。查看 Cache 后端设置

  5. cassandra  使用 Cassandra 存储结果。查看 Cassandra 后端设置

  6. elasticsearch  使用 Elasticsearch 存储结果。查看 Elasticsearch 后端设置

  7. ironcache  使用 IronCache 存储结果。查看 IronCache 后端设置

  8. couchbase  使用 Couchbase 存储结果。查看 Couchbase 后端设置

  9. couchdb  使用 CouchDB 存储结果。查看 CouchDB 后端设置

  10. filesystem  使用共享文件夹存储结果。查看 File-system 后端设置

  11. consul  使用 Consul K/V 存储结果。查看 Consul K/V 后端设置

- result_serializer

  默认值：从 4.0 版本开始使用  json（更早：pickle）
  
  查看 Serializers 获取支持的序列化格式的信息。

- result_compression

  默认值：无压缩
  
  结果值得可选压缩方法。支持 task_seralizer 设置相同的选项。

- result_expires

  默认值：1 天后过期

  存储的结果被删除的时间（秒数，或者一个 timedelta 对象）
  
  有一个内建的周期性任务将删除过期的任务结果（celery.backend_cleanup），前提是 celery beat 已经被启用。这个任务每天上午 4 点运行。
  
  值 None 或者 0 意思是结果永不删除（取决于后端声明）
  
  注意：当前这个特性只支持 AMQP, database, cache, Redis 这些存储后端。当使用 database 存储后端，celery beat 必须执行使得过期结果被删除。

- result_cache_max

  默认值：默认禁用
  
  启用结果的客户端缓存。
  
  对于老的 amqp 后端，存储结果一旦被消费它将不再可用，此时这个特性将起到作用。
  
  这是老的结果被删除之前总的结果缓存的数量。值 0 或者 None 意味着没有限制，并且值 -1 将禁用缓存。

### Database 后端设置

Database URL 示例

使用一个数据库存储后端，你必须配置 result_backend 设置为一个连接的 URL，并且带 db+ 前缀：

```python
result_backend = 'db+scheme://user:password@host:port/dbname'
```

示例：

```python
# sqlite (filename)
result_backend = 'db+sqlite:///results.sqlite'

# mysql
result_backend = 'db+mysql://scott:tiger@localhost/foo'

# postgresql
result_backend = 'db+postgresql://scott:tiger@localhost/mydatabase'

# oracle
result_backend = 'db+oracle://scott:tiger@127.0.0.1:1521/sidname'
```

查看 Supported Databases 获取支持的数据库的一个表，查看 Connection String 获取相关的连接字符串（这是 db+ 前缀后带的URI的一部分）

- database_engine_options

  默认值：{} （空映射）
  
  你可以使用 sqlalchmey_engine_options 设置声明额外的 SQLAchemy 数据库引擎选项：

```python
# echo enables verbose logging from SQLAlchemy.
app.conf.database_engine_options = {'echo': True}
```

- database_short_lived_sessions

  默认值：默认禁用

  默认禁用短会话。如果启用了，他们会急剧的降低性能，特别是对于处理很多任务的系统。当工作单元的流量很低，缓存的数据库连接会由于空闲而变为无用，进而会导致工作单元出错，这种情况下这个选项是有用的。例如：间歇性的错误如（OperationalError）（2006, ‘MySQL server has gone away’）通过启用短会话能解决。这个选项只影响数据库后端。

- database_table_names

  默认值：{} (空映射)
  当 SQLAlchemy 设置成结果后端， Celery 自动创建两个表来存储任务的元数据。这个设置允许你自定义表名称：

```python
# use custom table names for the database result backend.
database_table_names = {
    'task': 'myapp_taskmeta',
    'group': 'myapp_groupmeta',
}
```

### RPC 后端设置

- result_persistent

  默认值：默认被禁用（瞬态消息）
  
  如果设置成真，结果消息将被持久化。这意味着消息中间件重启后消息不会丢失。

配置示例：

```python
result_backend = 'rpc://'
result_persistent = False
```

### Cache 后端设置

注意：缓存后端支持 pylibmc 和 python-memcached 库。后者只有在 pylibmc 没有安装时才会被使用。

使用一个 Memcached 服务器：

```python
result_backend = 'cache+memcached://127.0.0.1:11211/'
```

使用多个 Memcached 服务器：

```python
result_backend = """
    cache+memcached://172.19.26.240:11211;172.19.26.242:11211/
""".strip()
```

“memory” 后端只在内存中存储缓存：

```python
result_backend = 'cache'
cache_backend = 'memory'
```

- cache_backend_options

  默认值：{} (空映射)
  
  你可以使用 cache_backend_options 设置 pylibmc 选项：

```python
cache_backend_options = {
    'binary': True,
    'behaviors': {'tcp_nodelay': True}
}
```

- cache_backend

  这个设置不再使用了，因为现在可以直接在 result_backend 中设置后端存储。

### Redis 后端设置

#### 配置后端 URL

注意：Redis 后端需要 Redis 库。

可以使用 pip 安装这个包：

```bash
$ pip install celery[redis]
```

查看 Bundles 获取组合多个扩展需求的信息

后端需要 result_backend 设置成一个 Redis URL:

```python
result_backend = 'redis://:password@host:port/db'
```

例如：

```python
result_backend = 'redis://localhost/0'
```

等同于：

```python
result_backend = 'redis://'
```

URL 的字段如下定义：

1. password  连接数据库的密码
2. host  Redis 服务器的主机名或者 IP 地址（例如：localhost）
3. port  Redis 服务器的端口。默认是 6379
4. db  使用的数据库编号。默认是0。db 可以包含一个可选的斜杠

- redis_backend_us_ssl

  默认值：禁用
  
  Redis后端支持 SSL。这个选项的合法值与 broker_use_ssl 相同

- redis_max_connections

  默认值：无显示
  
  Redis 连接池的最大可用连接数，这些连接用来发送和接收结果

- redis_socket_connect_timeout

  5.0.1 版本新特性

  默认值：None
  
  从存储后端连接到Redis服务器的连接的 Socket 超时时间（以秒为单位，int/float）

- redis_socket_timeout

  默认值：120 秒
  
  对 Redis 服务器的读写操作的 Socket 超时时间（以秒为单位，int/float），由存储后端使用

### Cassandra 后端设置

注意：Cassandra 后端驱动 cassandra-driver。

使用 pip 安装：

```bash
$ pip install celery[cassandra]
```

查看 Bundles 获取关于组合扩展需求的信息。

后端需要配置下列配置指令

- cassandra_servers

  默认值： [] (空列表)
  
  Cassandra 服务器列表。例如:

```python
cassandra_servers = ['localhost']
```

- cassandra_port

  默认值：9042
  
  连接到 Cassandra 服务器的端口

- cassandra_keyspace

  默认值: None
  
  存储结果的 key-space。例如:

```python
cassandra_keyspace = 'tasks_keyspace'
```

- cassandra_table

  默认值: None
  
  存储结果的表（列族）。例如:

```python
cassandra_table = 'tasks'
```

- cassandra_read_consistency

  默认值: None
  
  使用的读一致性。值可以是 ONE, TWO, THREE, QUORUM, ALL, LOCAL_QUORUM, EACH_QUORUM, LOCAL_ONE

- cassandra_write_consistency

  默认值: None
  
  使用的写一致性。值可以是 ONE, TWO, THREE, QUORUM, ALL, LOCAL_QUORUM, EACH_QUORUM, LOCAL_ONE

- cassandra_entry_ttl

  默认值: None
  
  状态项的 Time-to-live。添加过后一段时间他们将会过期并且被删除。值 None (默认) 意味着他们永不过期

- cassandra_auth_provider

  默认值: None
  
  使用的 cassandra.auth 模块中的 AuthProvider。 值可以是 PlainTextAuthProvider 或者 SaslAuthProvider

- cassandra_auth_kwargs
  默认值: {} (空映射)
  
  传递给 authentication provider 的命名参数。例如:

```python
cassandra_auth_kwargs = {
    username: 'cassandra',
    password: 'cassandra'
}
```

配置示例：

```python
cassandra_servers = ['localhost']
cassandra_keyspace = 'celery'
cassandra_table = 'tasks'
cassandra_read_consistency = 'ONE'
cassandra_write_consistency = 'ONE'
cassandra_entry_ttl = 86400
```

### Elasticsearch 后端设置

使用 Elasticsearch 作为结果后端，你只需要将 result_backend 设置成正确的 URL。

配置示例：

```python
result_backend = 'elasticsearch://example.com:9200/index_name/doc_type'
```

- elasticsearch_retry_on_timeout

  默认值: False
  
  超时后是否应该触发在另一个节点重试

- elasticsearch_max_retries

  默认值: 3
  
  异常被传递前的最大重试次数

- elasticsearch_timeout

  默认值: 10.0 秒
  
  elasticsearch 使用的全局超时时间

### Riak 后端设置

注意：Riak 后端需要 riak 库

使用 pip 进行安装：

```bash
$ pip install celery[riak]
```

查看 Bundles 获取组合多扩展需求的信息。

后端需要 result_backend 设置成一个 Riak URL:

```python
result_backend = 'riak://host:port/bucket'
```

例如：

```python
result_backend = 'riak://localhost/celery'
```

等同于：

```python
result_backend = 'riak://'
```

URL 的字段定义如下：
1. host  Riak 服务器的主机名或者 IP 地址（例如 localhost）
2. port  使用 protobuf 协议的 Riak 服务器端口，默认是 8087
3. bucket  使用的 Bucket 名称。默认是 celery。bucket 名称需要是一个只包含 ASCII 字符的字符串。

另外，这个后端可以使用如下配置指令进行配置：

- riak_backend_settings

  默认值: {} (空映射)
  
  这是一个支持如下键的映射:
  1. host  Riak 服务器的主机名或者 IP 地址（例如 localhost）
  2. port  Riak 服务器端口。默认是 8087
  3. bucket  使用的 Bucket 名称。默认是 celery。bucket 名称需要是一个只包含 ASCII 字符的字符串
  4. protocol  连接到 Riak 服务器使用的协议。这不可以通过 result_backend 配置

### AWS DynamoDB 后端设置

注意：Dynamodb 后端需要 boto3 库

使用 pip 进行安装：

```bash
$ pip install celery[dynamodb]
```

查看 Bundles 获取组合多扩展需求的信息。

后端需要 result_backend 设置成一个 DynamoDB URL：

```python
result_backend = 'dynamodb://aws_access_key_id:aws_secret_access_key@region:port/table?read=n&write=m'
```

例如，声明 AWS 区域以及表名称：

```python
result_backend = 'dynamodb://@us-east-1/celery_results
```

或者从环境中获取 AWS 配置参数，使用默认表名称（celery）以及声明读写吞吐量：

```python
result_backend = 'dynamodb://@/?read=5&write=5'
```

或者在本地使用 DynamoDB 的可下载版本：

```python
result_backend = 'dynamodb://@localhost:8000
```

URL 中的字段如下定义：

1. aws_access_key_id & aws_secret_access_key
   访问 AWS API 资源的认证信息。这可以通过 boto3 从不同的源获取到
2. region
   AWS 区域，例如： us-east-1 或者本地版本的 localhost。查看 boto3 库文档获取更多的信息。
3. port
   如果你使用的本地版本，这是本地 DynamoDB 示例监听的端口。如果你没有把区域设置成 localhost，这个设置选项将无效
4. table
   使用的表名。默认是 celery。查看 DynamoDB 命名规则获取允许的字符以及表名长度的信息。
5. read & write
   所创建的 DynamoBD 表的读写能力单元。默认的读写值都是 1。更多的细节可以从 Provisioned Throughput documentation 中获取到。

### IronCache 后端设置

注意：IronCache 后端需要 iron_celery 库：

使用 pip 进行安装：

```bash
$ pip install iron_celery
```

IronCache 通过在 result_backend 中配置的 URL 进行声明，例如：

```python
result_backend = 'ironcache://project_id:token@'
```

或者更改缓存名称：

```python
ironcache:://project_id:token@/awesomecache
```

### Couchbase 后端设置

注意：Couchbase 后端需要 couchbase 库

使用 pip 进行安装：

```bash
$ pip install celery[couchbase]
```

查看 Bundle 获取组合多扩展需求的步骤。

后端可以通过 result_backend 设置成一个 Couchbase URL：

```python
result_backend = 'couchbase://username:password@host:port/bucket'
```

- couchbase_backend_settings

  默认值：{} （空映射）
  
  这是一个支持如下键的映射：

1. host  Couchbase 服务器的主机名。默认是 localhost
2. port  Couchbase 服务器监听的端口。默认是 8091
3. bucket  Couchbase 服务器默认写入的桶。默认是 default
4. username  Couchbase 服务器认证的用户名（可选）
5. password  Couchbase 服务器认证的密码（可选）

### CouchDB 后端设置

注意：CouchDB 后端需要 pycouchdb 库

使用 pip 安装这个包：

```bash
$ pip install celery[couchdb]
```

查看 Bundles 获取更多关于组合多扩展需求的信息

后端可以通过 result_backend 配置成一个 CouchDB URL:

```python
result_backend = 'couchdb://username:password@host:port/container'
```

URL 由以下部分组成：

1. username  Couchbase 服务器认证的用户名（可选）
2. password  Couchbase 服务器认证的密码（可选）
3. host  Couchbase 服务器的主机名。默认是 localhost
4. port  Couchbase 服务器监听的端口。默认是 8091
5. container  CouchDB 服务器写入的默认容器。默认是 default

### File-system 后端设置

后端可以通过一个文件 URL 配置，例如：

```python
CELERY_RESULT_BACKEND = 'file:///var/celery/results'
```

配置的目录需要被共享，并且所有使用该后端的服务器都可写。

如果你在单独的一个系统上使用 Celery，你不需要任何进一步的配置就可以简单的使用这个后端。
对于大型的集群，你可以使用 NFS、GlusterFS、CIFS、HDFS(使用FUSE)，或者其他文件系统。

### Consul K/V 存储后端设置

Consul 后端可以通过 URL 配置：

```python
CELERY_RESULT_BACKEND = 'consul://localhost:8500/'
```

后端将在 Consul K/V 存储中作为单独键存储结果

后端使用Consul 中的 TTLs 支持结果的自动过期

### 消息路由

- task_queues

  默认值： None （默认队列的配置）
  
  多数用户不愿声明这个配置，而是使用 automatic routing facilites。
  
  如果你真的需要配置高级路由，这个设置应该是一个 kombu.Queue 对象的列表，工作单元可以从中消费。
  
  注意工作单元可以通过 `-Q` 选项覆盖这个设置，或者这个列表中的单独队列可以通过 `-X` 选项进行排除。
  
  查看 Basics 获取更多的信息。
  
  默认值是 celery 队列的一个队列/消息交换器/绑定的键，消息交互类型是direct。

- task_routes

  默认值： None
  
  一个路由器的列表，或者单个路路由，用来路由任务到相应的队列。当决定一个任务的最终目的，路由器将按声明顺序进行轮询。
  
  一个路由器可以通过如下方式声明：
  
  1. 函数，签名格式为 `(name, args, kwargs, options, task=None, **kwargs)`
  2. 字符串，提供到路由函数的路径
  3. 字典，包含路由声明，它将会转化成一个 `celery.routes.MapRoute` 实例
  4. 一个 `(pattern, route)` 元组的列表，它将会转化成一个 `celery.routes.MapRoute` 实例

示例：

```python
task_routes = {
    'celery.ping': 'default',
    'mytasks.add': 'cpu-bound',
    'feed.tasks.*': 'feeds',  # <-- glob pattern
    re.compile(r'(image|video)\.tasks\..*'): 'media',  # <-- regex
    'video.encode': {
        'queue': 'video',
        'exchange': 'media',
        'routing_key': 'media.video.encode'
    }
}

task_routes = ('myapp.tasks.route_task', {'celery.ping': 'default'})  # 其中，myapp.tasks.route_task 可以是


def route_task(self, name, args, kwargs, options, task=None, **kw):
    if task == 'celery.ping':
        return {'queue': 'default'}
```

route_task 可以返回一个字符串或者一个字典。一个字符串表示 task_queues 中的一个队列名，而字典表示一个自定义的路由。

当发送消息，路由被按顺序询问。第一个返回非 None 值的路由将被使用。消息选项此时将与找到的路由设置合并，其中路由器的设置要优先。

例如： apply_async() 有这些参数：

```python
Task.apply_async(immediate=False, exchange='video', routing_key='video.compress')
```

并且有一个路由器返回：

```python
{'immediate': True, 'exchange': 'urgent'}
```

那么最终的消息选项将是：

```python
immediate=True, exchange='urgent', routing_key='video.compress'
```

（以及Task类中定义的任意默认消息选项）

当进行合并时，task_routes 中定义的值会优先于 task_queues 中定义的值。

对于如下设置：

```python
task_queues = {
    'cpubound': {
        'exchange': 'cpubound',
        'routing_key': 'cpubound'
    }
}

task_routes = {
    'tasks.add': {
        'queue': 'cpubound',
        'routing_key': 'tasks.add',
        'serializer': 'json',
    },
}
```

tasks.add 的最终路由选项将变为：

```python
{
    'exchange': 'cpubound',
    'routing_key': 'tasks.add',
    'serializer': 'json'
}
```

- task_queue_ha_policy

  消息中间件： RabbitMQ
  
  默认值：None
  
  这将设置一个队列的HA策略，并且值可以是一个字符串（通常是 all）

```python
task_queue_ha_policy = 'all'
```

使用 all 将复制队列到所有的当前节点，或者你指定一个节点的列表：

```python
task_queue_ha_policy = ['rabbit@host1', 'rabbit@host2']
```

使用一个列表将隐示设置 `x-ha-policy`为 `nodes`，`x-ha-policy-params` 为给定的节点列表

- task_queue_max_priority

  消息中间件： RabbitMQ
  
  默认值： None
  
  查看 RabbitMQ Message Priorities

- worker_direct

  默认值： 禁用
  
  这个选项使得每个工作单元有一个专门的队列，所以任务可以路由到指定的工作单元。
  
  每个工作单元的队列名称是基于工作单元主机名和一个 `.dq` 后缀自动产生的，使用 `C.dq` 消息交换机。
  
  例如：节点名称为 `w1@example.com` 的工作单元的队列名称为：

```python
w1@example.com.dq
```

此时，你可以通过指定主机名为路由键并且使用 C.dq 消息交互器来将任务路由到指定的节点。

```python
task_routes = {
    'tasks.add': {
        'exchange': 'C.dq',
        'routing_key': 'w1@example.com'
    }
}
```

- task_create_missing_queues

  默认值：启用
  
  如果启用（默认），任何声明的未在 task_queues 中未定义的队列都将自动被创建。查看 Automaci routing。

- task_default_queue

  默认值： celery
  
  如果消息没有声明路由或者自定义的队列，apply_async 默认使用的队列名称。
  
  这个队列必须在 task_queues 中。如果 task_queues 没有声明，那么他将自动创建一个队列项，而这个设置值就作为队列的名称。

- task_default_exchange

  默认值：celery
  
  当 task_queues 设置中指定键没有声明自定义的消息交换机，那么这个默认的消息交互器将被使用。

- task_default_exchange_type

  默认值：direct
  
  当 task_queues 设置中指定键没有声明自定义的消息交互器类型，那么这个默认的消息交互器类型将被使用。

- task_default_routing_key

  默认值：celery
  
  当 task_queues 设置中指定键没有声明自定义的路由键，那么这个默认的路由键将被使用。

- task_default_delivery_mode

  默认值：presistent
  
  可以是瞬态的（消息不写硬盘），或者持久的（写硬盘）

### 消息中间件设置

- broker_url

  默认值：amqp://
  
  默认的消息中间件 URL。这必须是一个如下形式的 URL：

```python
transport://userid:password@hostname:port/virtual_host
```

其中只有模式部分是必须的，其余部分都是可选的，默认会设置为对应传输中间件的默认值。

传输部分是使用的消息中间件的实现，默认是 `amqp`，（如果安装了 `librabbitmq` 会使用这个库，否则使用 `pyamqp`）。还有其他可用的选择，包括 `redis://`、 `sqs://`、 `qpid://`。

模式部分可以是你自己的传输中间件实现的全限定路径：

```python
broker_url = 'proj.transports.MyTransport://localhost'
```

可以配置多个消息中间件，使用相同的传输协议也行。消息中间件可以通过当个字符串声明，不同的消息中间件URL之间用冒号分隔：

```python
broker_url = 'transport://userid:password@hostname:port//;transport://userid:password@hostname:port//'
```

或者作为一个列表：

```python
broker_url = [
    'transport://userid:password@localhost:port//',
    'transport://userid:password@hostname:port//'
]
```

这些消息中间件将被用于 broker_failover_strategy

查看 Kombu 文档中的 URLs 章节获取更多的信息。

- broker_read_url / broker_write_url

  默认值：broker_url 的设置值
  
  这些设置可以配置而不用 broker_url 的设置，可以为消息中间件声明不同的连接参数，用来消费和生成消息。

示例：

```python
broker_read_url = 'amqp://user:pass@broker.example.com:56721'
broker_write_url = 'amqp://user:pass@broker.example.com:56722'
```

所有选项都可以声明成一个列表，作为故障恢复的可选值，查看 broker_url 获取更多的信息

- broker_failover_strategy

  默认值：round-robin
  消息中间件连接对象的默认故障恢复策略。如果提供了，将映射到 `kombu.connection.failover_strategies` 中的一个键，或者引用任何方法，从给定的列表中产生一个项。

示例：

```python
# Random failover strategy
def random_failover_strategy(servers):
    it = list(servers)  # don't modify callers list
    shuffle = random.shuffle
    for _ in repeat(None):
        shuffle(it)
        yield it[0]

broker_failover_strategy = random_failover_strategy
```

- broker_heartbeat

  支持的传输层协议：pyamqp
  
  默认值：120.0（与服务器协商）
  
  注意：这个值只被工作单元使用，客户端此时不使用心跳。
  
  因为单纯使用 TCP/IP 并不总是及时探测到连接丢失，所以 AMQP 定义了心跳，客户端和消息中间件用来检测连接是否关闭。
  
  心跳会被监控，如果心跳值是 10 秒，那么检测心跳的时间间隔是 10 除以 broker_heartbeat_checkrate （默认情况下，这个值是心跳值的两倍，所以对于 10 秒心跳，心跳每隔5秒检测一次）

- broker_heartbeat_checkrate

  支持的传输层协议：pyamqp
  
  默认值：2.0
  
  工作单元会间隔监控消息中间件没有丢失过多的心跳。这个检测的速率是用 broker_heartbeat 值除以这个设置值得到的，所以如果心跳是 10.0 并且这个设置值是默认的 2.0，那么这个监控将每隔 5 秒钟执行一次（心跳发送速率的两倍）

- broker_use_ssl

  支持的传输层协议： pyamqp, redis
  
  默认值: 禁用
  
  在消息中间件连接上使用 SSL
  
  这个选项的合法值依据使用的传输协议的不同而不同

- pyamqp

  如果设置成 True，连接将依据默认的 SSL 设置启用 SSL。如果设置成一个字典，将依据给定的策略配置 SSL 连接。使用的格式是 python 的 ssl.wrap_socket() 选项。
  
  注意 SSL 套接字一般会在消息中间件的一个单独的端口上服务。

以下示例提供了客户端证书，并且使用一个自定义的认证授权来验证服务器证书：

```python
import ssl
broker_use_ssl = {
    'keyfile': '/var/ssl/private/worker-key.pem',
    'certfile': '/var/ssl/amqp-server-cert.pem',
    'ca_certs': '/var/ssl/myca.pem',
    'cert_reqs': ssl.CERT_REQUIRED
}
```

告警：使用 broker_use_ssl=True 时请小心。可能你的默认配置根本不会验证服务器证书。请阅读python 的 ssl module security considerations。

- redis

  设置必须是一个字典，包括如下键：

  * ssl_cert_reqs (required): one of the SSLContext.verify_mode values: 
    * ssl.CERT_NONE
    * ssl.CERT_OPTIONAL
    * ssl.CERT_REQUIRED
  * ssl_ca_certs (optional): path to the CA certificate
  * ssl_certfile (optional): path to the client certificate
  * ssl_keyfile (optional): path to the client key

- broker_pool_limit

  2.3 版本新特性
  
  默认值：10
  
  连接池中可以打开最大连接数。
  
  从 2.5 版本开始连接池被默认启用，默认限制是 10 个连接。这个数值可以依据使用一个连接的 threads/green-threads (eventlet/gevent) 数量进行更改。例如：运行 eventlet 启动 1000 个 greenlets，他们使用一个连接到消息中间件，如果发生竞态条件，那么你应该开始增加这个限制。
  
  如果设置成 None 或者 0，连接池将会被禁用，并且每次使用连接都会重新建立连接并关闭。

- broker_connection_timeout

  默认值：4.0
  
  放弃与 AMQP 服务器建立连接之前默认等待的超时时间。当使用 gevent 时该设置被禁用。

- broker_connection_retry

  默认值：启用
  
  如果与 AMQP 消息中间件的连接断开，将自动重新建立连接
  
  每次重试中间等待的时间会递增，并且在 broker_connection_max_retries 未达到之前会一直重试

- broker_connection_max_retries

  默认值：100
  
  放弃与 AMQP 服务器重新建立连接之前的最大重试次数
  
  如果设置成 0 或者 None，将一只重试

- broker_login_method

  默认值：AMQPLAIN
  
  设置自定义的 amqp 登陆方法

- broker_transport_options

  2.2 版本新特性

  默认值：{} （空映射）
  
  传递给底层传输中间件的一个附加选项的字典
  
  设置可见超时时间的示例如下（Redis 与 SQS 传输中间件支持）：

```python
broker_transport_options = {'visibility_timeout': 18000}  # 5 hours
```

### 工作单元

- imports

  默认值：[] （空列表）
  
  当工作单元启动时导入的一系列模块
  
  这用来声明要导入的模块，但是它还可用来导入信号处理函数和附加的远程控制命令，等等。
  
  这些模块将会以原来声明的顺序导入

- include

  默认值：[] （空列表）
  
  语义上与 imports 相同，但是可以作为将不同导入分类的一种手段
  
  这个设置中的模块是在 imports 设置中的模块导入之后才导入

- worker_concurrency

  默认值：CPU核数
  
  执行任务的并发工作单元 process/threads/green 数量
  
  如果你大部分操作是 I/O 操作，你可以设置更多的进程（线程），但是大部分情况下都是以 CPU 数作为定界，尝试让这个值接近你机器的 CPU 核数。如果没有设置，当前机器的 CPU 核数将会被使用

- worker_prefetch_multiplier

  默认值：4
  
  工作单元一次预获取多少个消息是这个设置值乘以并发进程的数量。默认值是 4（每个进程 4 条消息）。但是，默认设置通常是好的选择 - 如果你有长时间任务等待在队列中，并且你必须启动工作单元，注意第一个工作单元初始时将收到 4 倍的消息量。因此任务可能在工作单元间不会平均分布
  
  禁用这个选项，只要将 worker_prefetch_multiplier 设置成 1。设置成 0 将允许工作单元持续消费它想要的尽可能多的消息。

更详细的信息，请阅读 Prefetch Limits

注意：带 ETA/countdown 的任务不会受 prefetch 限制的影响

- worker_lost_wait

  默认值：10.0 秒
  
  有些情况下，工作单元可能在没有适当清理的情况下就被杀死，并且工作单元可能在终止前已经发布了一个结果。这个值声明了在抛出 WorkerLostError 异常之前我们会在丢失的结果值上等待多久

- worker_max_tasks_per_child

  一个工作单元进程在被一个新的进程替代之前可以执行的最大任务数

- worker_max_memory_per_child

  默认值：没有限制。类型：int(kilobytes)
  
  一个工作单元进程在被一个新的进程替代之前可以消耗的最大预留内存（单位KB）。如果单独一个任务就导致工作单元超过这个限制，当前的任务会执行完成，并且之后这个进程将会被更新替代。
  
  示例：

```python
worker_max_memory_per_child = 12000  # 12MB
```

- worker_disable_rate_limits

  默认值：禁用（启用速率限制）
  
  即使任务显示设置了速率，仍然禁用所有速率限制
  

- worker_state_db

  默认值：None
  
  存储工作单元状态的文件名称（如取消的任务）。可以是相对或者绝对路径，但是注意后缀.db 可能会被添加到文件名后（依赖于python 的版本）
  
  也可以通过 celery worker –statedb 参数设置

- worker_timer_precision

  默认值：1.0 秒
  
  设置重新检测调度器之前 ETA 调度器可以休息的最大秒数
  
  设置成1意味着调度器精度将为1秒。如果你需要毫秒精度，你可以设置成 0.1

- worker_enable_remote_control

  默认值：默认启用
  
  声明工作单元的远程控制是否启用

### 事件

- worker_send_task_events

  默认值：默认禁用
  
  发送任务相关的事件，使得任务可以使用类似 flower 的工作监控到。为工作单元的 `-E` 参数设置默认值

- task_send_sent_event

  2.2 版本新特性

  默认值：默认禁用
  
  如果启用，对于每个任务都将有一个 task-sent 事件被发送，因此任务在被消费前就能被追踪。

- event_queue_ttl

  支持的传输中间件: amqp
  
  默认值：5.0 秒
  
  发送到一个监控客户端事件队列的消息的过期时间（x-message-ttl），以秒为单位（int/float)。
  
  例如：如果这个值设置为10，被递送到这个队列的消息将会在 10 秒后被删除

- event_queue_expires

  支持的传输中间件: amqp
  
  默认值：60.0 秒
  
  一个监控客户端事件队列被删除前的过期时间（x-expires）。

- event_queue_prefix

  默认值： celeryev
  
  事件接收队列名称的前缀

- event_serializer

  默认值： json
  
  当发送事件消息时使用的消息序列化格式

### 远程控制命令

- control_queue_ttl

  默认值： 300.0
  
  远程控制命令队列中的消息到期之前的时间（以秒为单位）。
  
  如果使用默认的300秒，则意味着如果发送了远程控制命令并且在300秒内没有工作人员接听，则该命令将被丢弃。
  
  此设置也适用于远程控制答复队列。

- control_queue_expires

  默认值： 10.0
  
  从代理中删除未使用的远程控制命令队列之前的时间（以秒为单位）。
  
  此设置也适用于远程控制答复队列。

### 日志

- worker_hijack_root_logger

  2.2 版本新特性

  默认值： 默认启用 (hijack root logger).
  
  默认情况下，任意前面配置的根日志器的处理函数都将被移除。如果你想自定义日志处理函数，那么你可以通过设置 worker_hijack_root_logger = False 来禁用这个行为
  
  注意：日志可以通过连接到 celery.signals.setup_logging 进行定制化

- worker_log_color

  默认值： 如果应用实例日志输出到一个终端，这个将启用
  
  启用/禁用Celery 应用日志输出的颜色

- worker_log_format

  默认值：[%(asctime)s: %(levelname)s/%(processName)s] %(message)s
  
  日志信息的格式

- worker_task_log_format

  默认值：

```python
[%(asctime)s: %(levelname)s/%(processName)s]
    [%(task_name)s(%(task_id)s)] %(message)s
```

  任务中记录日志使用的格式

- worker_redirect_stdouts

  默认值： 默认启用
  
  如果启用，标准输出和标准错误输出将重定向到当前日志器
  
  工作单元和 beat 将使用到

- worker_redirect_stdouts_level

  默认值：WARNING
  
  标准输出和标准错误输出的日志级别。可以是DEBUG, INFO, WARNING, ERROR, or CRITICAL

### 安全

- security_key

  默认值： None
  
  2.5 版本新特性
  
  包含私钥的文件的相对或者绝对路径，私钥用来在使用消息签名时对消息进行签名。

- security_certificate

  默认值：None
  
  2.5 版本新特性
  
  包含 X.509 认证的文件的相对或者绝对路径，认证用来在使用消息签名时对消息进行签名。

- security_cert_store

  默认值：None
  
  2.5 版本新特性
  
  包含用来进行消息签名的X.509认证的目录。可以使用文件名模式匹配（例如：/etc/certs/*.pem）

### 自定义组件类 （高级）

- worker_pool

  默认值：prefork（celery.concurrency.prefork:TaskPool）
  
  工作单元使用的池类的名称

- Eventlet/Gevent

  永远不要使用这个选项来选择用 eventlet 还是 gevent。你必须对工作单元使用 -P 选项，确保应急补丁不会应用过迟，导致出现奇怪的现象。

- worker_pool_restarts

  默认值：默认禁用
  
  如果启用，工作单元池可以使用 pool_restart 远程控制命令进行重启

- worker_autoscaler

  2.2 版本新特性

  默认值： celery.worker.autoscale:Autoscaler
  
  使用的自动扩展类的名称

- worker_consumer

  默认值：celery.worker.consumer:Consumer
  
  工作单元使用的消费类的名称
  
- worker_timer

  默认值：kombu.async.hub.timer:Timer
  
  工作单元使用的 ETA 调度器类的名称。默认值是被池具体实现设置。

### Beat 设置 （celery beat）

- beat_schedule

  默认值： {} (空映射)
  
  beat 调度的周期性任务。查看 Entries

- beat_scheduler

  默认值：celery.beat:PersistentScheduler
  
  默认的调度器类。如果同时使用 django-celery-beat 扩展，可以设置成 `django_celery_beat.schedulers:DatabaseScheduler`
  
  也可以通过celery beat 的 -S 参数进行设置

- beat_schedule_filename

  默认值：celerybeat-schedule
  
  存储周期性任务最后运行时间的文件的名称，这个文件被 PersistentScheduler 使用。可以是相对或者绝对路径，但是注意后缀.db可能添加到文件名后（依赖于python版本）
  
  也可以通过 celery beat 的 –schedule 参数进行设置

- beat_sync_every

  默认值：0
  
  另一个数据库同步发起前可以执行的周期性任务的数量。值 0（默认）表示基于时间同步 - 默认是3 分钟，由 scheduler.sync_every 确定。如果设置成1，beat 将在每个任务消息发送后发起同步。

- beat_max_loop_interval

  默认值： 0

[参考](https://blog.csdn.net/u013148156/article/details/78812472)
