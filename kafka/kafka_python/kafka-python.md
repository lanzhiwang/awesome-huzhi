# kafka-python

Python client for the Apache Kafka distributed stream processing system. kafka-python is designed to function much like the official java client, with a sprinkling of pythonic interfaces (e.g., consumer iterators).  用于Apache Kafka分布式流处理系统的Python客户端。 kafka-python的功能与官方的Java客户端非常相似，带有一些pythonic接口（例如，消费者迭代器）。

kafka-python is best used with newer brokers (0.9+), but is backwards-compatible with older versions (to 0.8.0). Some features will only be enabled on newer brokers. For example, fully coordinated consumer groups – i.e., dynamic partition assignment to multiple consumers in the same group – requires use of 0.9 kafka brokers. Supporting this feature for earlier broker releases would require writing and maintaining custom leadership election and membership / health check code (perhaps using zookeeper or consul). For older brokers, you can achieve something similar by manually assigning different partitions to each consumer instance with config management tools like chef, ansible, etc. This approach will work fine, though it does not support rebalancing on failures. See Compatibility for more details.  kafka-python最适用于较新的代理（0.9+），但与旧版本（向0.8.0）向后兼容。 某些功能仅在较新的代理上启用。 例如，完全协调的消费者群体 - 即，向同一群组中的多个消费者分配动态分区 - 需要使用0.9 kafka经纪人。 为早期的代理发布支持此功能需要编写和维护自定义领导选举和成员/健康检查代码（可能使用zookeeper或consul）。 对于较旧的代理，您可以通过使用chef，ansible等配置管理工具为每个消费者实例手动分配不同的分区来实现类似的功能。这种方法可以正常工作，但它不支持故障时的重新平衡。

Please note that the master branch may contain unreleased features. For release documentation, please see readthedocs and/or python’s inline help.  请注意，主分支可能包含未发布的功能。 有关发布文档，请参阅readthedocs和/或python的内联帮助。

```bash
>>> pip install kafka-python
```

## KafkaConsumer

`KafkaConsumer` is a high-level message consumer, intended to operate as similarly as possible to the official java client. Full support for coordinated consumer groups requires use of kafka brokers that support the Group APIs: kafka v0.9+.  KafkaConsumer是一个高级消息使用者，旨在尽可能与官方Java客户端进行操作。 对协调的消费者群体的全面支持需要使用支持Group API的kafka代理：kafka v0.9 +。

See KafkaConsumer for API and configuration details.

The consumer iterator returns ConsumerRecords, which are simple namedtuples that expose basic message attributes: topic, partition, offset, key, and value:

```python
>>> from kafka import KafkaConsumer
>>> consumer = KafkaConsumer('my_favorite_topic')
>>> for msg in consumer:
...     print (msg)
```

```python
>>> # join a consumer group for dynamic partition assignment and offset commits
>>> from kafka import KafkaConsumer
>>> consumer = KafkaConsumer('my_favorite_topic', group_id='my_favorite_group')
>>> for msg in consumer:
...     print (msg)
```

```python
>>> # manually assign the partition list for the consumer
>>> from kafka import TopicPartition
>>> consumer = KafkaConsumer(bootstrap_servers='localhost:1234')
>>> consumer.assign([TopicPartition('foobar', 2)])
>>> msg = next(consumer)
```

```python
>>> # Deserialize msgpack-encoded values
>>> consumer = KafkaConsumer(value_deserializer=msgpack.loads)
>>> consumer.subscribe(['msgpackfoo'])
>>> for msg in consumer:
...     assert isinstance(msg.value, dict)
```

## KafkaProducer

`KafkaProducer` is a high-level, asynchronous message producer. The class is intended to operate as similarly as possible to the official java client. See KafkaProducer for more details.

```python
>>> from kafka import KafkaProducer
>>> producer = KafkaProducer(bootstrap_servers='localhost:1234')
>>> for _ in range(100):
...     producer.send('foobar', b'some_message_bytes')
```

```python
>>> # Block until a single message is sent (or timeout)
>>> future = producer.send('foobar', b'another_message')
>>> result = future.get(timeout=60)
```

```python
>>> # Block until all pending messages are at least put on the network
>>> # NOTE: This does not guarantee delivery or success! It is really
>>> # only useful if you configure internal batching using linger_ms
>>> producer.flush()
```

```python
>>> # Use a key for hashed-partitioning
>>> producer.send('foobar', key=b'foo', value=b'bar')
```

```python
>>> # Serialize json messages
>>> import json
>>> producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))
>>> producer.send('fizzbuzz', {'foo': 'bar'})
```

```python
>>> # Serialize string keys
>>> producer = KafkaProducer(key_serializer=str.encode)
>>> producer.send('flipflap', key='ping', value=b'1234')
```

```python
>>> # Compress messages
>>> producer = KafkaProducer(compression_type='gzip')
>>> for i in range(1000):
...     producer.send('foobar', b'msg %d' % i)
```

## Thread safety

The KafkaProducer can be used across threads without issue, unlike the KafkaConsumer which cannot.  KafkaProducer可以在没有问题的情况下跨线程使用，这与KafkaConsumer不同。

While it is possible to use the KafkaConsumer in a thread-local manner, multiprocessing is recommended.

## Compression

kafka-python supports gzip compression/decompression natively. To produce or consume lz4 compressed messages, you should install python-lz4 (pip install lz4). To enable snappy, install python-snappy (also requires snappy library). See Installation for more information.  kafka-python原生支持gzip压缩/解压缩。 要生成或使用lz4压缩消息，您应该安装python-lz4（pip install lz4）。 要启用snappy，请安装python-snappy（还需要snappy库）。 有关更多信息，请参阅安装

## Protocol

A secondary goal of kafka-python is to provide an easy-to-use protocol layer for interacting with kafka brokers via the python repl. This is useful for testing, probing, and general experimentation. The protocol support is leveraged to enable a check_version() method that probes a kafka broker and attempts to identify which version it is running (0.8.0 to 1.1+).

## Low-level

Legacy support is maintained for low-level consumer and producer classes, SimpleConsumer and SimpleProducer.


# Usage

## KafkaConsumer

```python
from kafka import KafkaConsumer

# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('my-topic',
                         group_id='my-group',
                         bootstrap_servers=['localhost:9092'])
for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))

# consume earliest available messages, don't commit offsets
KafkaConsumer(auto_offset_reset='earliest', enable_auto_commit=False)

# consume json messages
KafkaConsumer(value_deserializer=lambda m: json.loads(m.decode('ascii')))

# consume msgpack
KafkaConsumer(value_deserializer=msgpack.unpackb)

# StopIteration if no message after 1sec
KafkaConsumer(consumer_timeout_ms=1000)

# Subscribe to a regex topic pattern
consumer = KafkaConsumer()
consumer.subscribe(pattern='^awesome.*')

# Use multiple consumers in parallel w/ 0.9 kafka brokers
# typically you would run each on a different server / process / CPU
consumer1 = KafkaConsumer('my-topic',
                          group_id='my-group',
                          bootstrap_servers='my.server.com')
consumer2 = KafkaConsumer('my-topic',
                          group_id='my-group',
                          bootstrap_servers='my.server.com')
```

There are many configuration options for the consumer class. See KafkaConsumer API documentation for more details.

## KafkaProducer

```python
from kafka import KafkaProducer
from kafka.errors import KafkaError

producer = KafkaProducer(bootstrap_servers=['broker1:1234'])

# Asynchronous by default
future = producer.send('my-topic', b'raw_bytes')

# Block for 'synchronous' sends
try:
    record_metadata = future.get(timeout=10)
except KafkaError:
    # Decide what to do if produce request failed...
    log.exception()
    pass

# Successful result returns assigned partition and offset
print (record_metadata.topic)
print (record_metadata.partition)
print (record_metadata.offset)

# produce keyed messages to enable hashed partitioning
producer.send('my-topic', key=b'foo', value=b'bar')

# encode objects via msgpack
producer = KafkaProducer(value_serializer=msgpack.dumps)
producer.send('msgpack-topic', {'key': 'value'})

# produce json messages
producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'))
producer.send('json-topic', {'key': 'value'})

# produce asynchronously
for _ in range(100):
    producer.send('my-topic', b'msg')

def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)

def on_send_error(excp):
    log.error('I am an errback', exc_info=excp)
    # handle exception

# produce asynchronously with callbacks
producer.send('my-topic', b'raw_bytes').add_callback(on_send_success).add_errback(on_send_error)

# block until all async messages are sent
producer.flush()

# configure multiple retries
producer = KafkaProducer(retries=5)
```

# kafka-python API

## KafkaConsumer

## KafkaProducer

## KafkaAdminClient

## KafkaClient

## BrokerConnection

## ClusterMetadata

# KafkaConsumer

> class kafka.KafkaConsumer(*topics, **configs)

Consume records from a Kafka cluster.

The consumer will transparently handle the failure of servers in the Kafka cluster, and adapt as topic-partitions are created or migrate between brokers. It also interacts with the assigned kafka Group Coordinator node to allow multiple consumers to load balance consumption of topics (requires kafka >= 0.9.0.0).  消费者将透明地处理Kafka集群中服务器的故障，并在经纪人之间创建或迁移主题分区时进行调整。 它还与指定的kafka Group Coordinator节点交互，以允许多个消费者负载平衡主题消耗（需要kafka> = 0.9.0.0）。

The consumer is not thread safe and should not be shared across threads.

Parameters:	

*topics (str) – optional list of topics to subscribe to. If not set, call subscribe() or assign() before consuming records.

Keyword Arguments:

* bootstrap_servers – ‘host[:port]’ string (or list of ‘host[:port]’ strings) that the consumer should contact to bootstrap initial cluster metadata. This does not have to be the full node list. It just needs to have at least one broker that will respond to a Metadata API Request. Default port is 9092. If no servers are specified, will default to localhost:9092.

* client_id (str) – A name for this client. This string is passed in each request to servers and can be used to identify specific server-side log entries that correspond to this client. Also submitted to GroupCoordinator for logging with respect to consumer group administration. Default: ‘kafka-python-{version}’

* group_id (str or None) – The name of the consumer group to join for dynamic partition assignment (if enabled), and to use for fetching and committing offsets. If None, auto-partition assignment (via group coordinator) and offset commits are disabled. Default: None  s要为动态分区分配（如果已启用）加入的使用者组的名称，以及用于获取和提交偏移的名称。 如果为None，则禁用自动分区分配（通过组协调器）和偏移提交。 默认值：无

* key_deserializer (callable) – Any callable that takes a raw message key and returns a deserialized key.

* value_deserializer (callable) – Any callable that takes a raw message value and returns a deserialized value.

* fetch_min_bytes (int) – Minimum amount of data the server should return for a fetch request, otherwise wait up to fetch_max_wait_ms for more data to accumulate. Default: 1.

* fetch_max_wait_ms (int) – The maximum amount of time in milliseconds the server will block before answering the fetch request if there isn’t sufficient data to immediately satisfy the requirement given by fetch_min_bytes. Default: 500.

* fetch_max_bytes (int) – The maximum amount of data the server should return for a fetch request. This is not an absolute maximum, if the first message in the first non-empty partition of the fetch is larger than this value, the message will still be returned to ensure that the consumer can make progress. NOTE: consumer performs fetches to multiple brokers in parallel so memory usage will depend on the number of brokers containing partitions for the topic. Supported Kafka version >= 0.10.1.0. Default: 52428800 (50 MB).  服务器应为获取请求返回的最大数据量。 这不是绝对最大值，如果获取的第一个非空分区中的第一条消息大于此值，则仍将返回消息以确保消费者可以取得进展。 注意：使用者并行执行对多个代理的提取，因此内存使用将取决于包含该主题分区的代理的数量。 支持的Kafka版本> = 0.10.1.0。 默认值：52428800（50 MB）。

* max_partition_fetch_bytes (int) – The maximum amount of data per-partition the server will return. The maximum total memory used for a request = #partitions * max_partition_fetch_bytes. This size must be at least as large as the maximum message size the server allows or else it is possible for the producer to send messages larger than the consumer can fetch. If that happens, the consumer can get stuck trying to fetch a large message on a certain partition. Default: 1048576.  服务器将返回的每个分区的最大数据量。 用于请求的最大总内存= #partitions * max_partition_fetch_bytes。 此大小必须至少与服务器允许的最大消息大小一样大，否则生产者可以发送大于消费者可以获取的消息。 如果发生这种情况，消费者可能会遇到尝试在某个分区上获取大量消息的问题。 默认值：1048576。

* request_timeout_ms (int) – Client request timeout in milliseconds. Default: 305000.

* retry_backoff_ms (int) – Milliseconds to backoff when retrying on errors. Default: 100.

* reconnect_backoff_ms (int) – The amount of time in milliseconds to wait before attempting to reconnect to a given host. Default: 50.

* reconnect_backoff_max_ms (int) – The maximum amount of time in milliseconds to wait when reconnecting to a broker that has repeatedly failed to connect. If provided, the backoff per host will increase exponentially for each consecutive connection failure, up to this maximum. To avoid connection storms, a randomization factor of 0.2 will be applied to the backoff resulting in a random range between 20% below and 20% above the computed value. Default: 1000.  重新连接到反复无法连接的代理时等待的最长时间（以毫秒为单位）。 如果提供，每个主机的退避将在每次连续连接失败时呈指数增长，直至达到此最大值。 为了避免连接风暴，将对退避应用0.2的随机因子，导致在计算值之上20％至20％之间的随机范围。 默认值：1000。

* max_in_flight_requests_per_connection (int) – Requests are pipelined to kafka brokers up to this number of maximum requests per broker connection. Default: 5.

* auto_offset_reset (str) – A policy for resetting offsets on OffsetOutOfRange errors: ‘earliest’ will move to the oldest available message, ‘latest’ will move to the most recent. Any other value will raise the exception. Default: ‘latest’.

* enable_auto_commit (bool) – If True , the consumer’s offset will be periodically committed in the background. Default: True.

* auto_commit_interval_ms (int) – Number of milliseconds between automatic offset commits, if enable_auto_commit is True. Default: 5000.

* default_offset_commit_callback (callable) – Called as callback(offsets, response) response will be either an Exception or an OffsetCommitResponse struct. This callback can be used to trigger custom actions when a commit request completes.

* check_crcs (bool) – Automatically check the CRC32 of the records consumed. This ensures no on-the-wire or on-disk corruption to the messages occurred. This check adds some overhead, so it may be disabled in cases seeking extreme performance. Default: True

* metadata_max_age_ms (int) – The period of time in milliseconds after which we force a refresh of metadata, even if we haven’t seen any partition leadership changes to proactively discover any new brokers or partitions. Default: 300000

* partition_assignment_strategy (list) – List of objects to use to distribute partition ownership amongst consumer instances when group management is used. Default: [RangePartitionAssignor, RoundRobinPartitionAssignor]

* max_poll_records (int) – The maximum number of records returned in a single call to poll(). Default: 500

* max_poll_interval_ms (int) – The maximum delay between invocations of poll() when using consumer group management. This places an upper bound on the amount of time that the consumer can be idle before fetching more records. If poll() is not called before expiration of this timeout, then the consumer is considered failed and the group will rebalance in order to reassign the partitions to another member. Default 300000

* session_timeout_ms (int) – The timeout used to detect failures when using Kafka’s group management facilities. The consumer sends periodic heartbeats to indicate its liveness to the broker. If no heartbeats are received by the broker before the expiration of this session timeout, then the broker will remove this consumer from the group and initiate a rebalance. Note that the value must be in the allowable range as configured in the broker configuration by group.min.session.timeout.ms and group.max.session.timeout.ms. Default: 10000

* heartbeat_interval_ms (int) – The expected time in milliseconds between heartbeats to the consumer coordinator when using Kafka’s group management facilities. Heartbeats are used to ensure that the consumer’s session stays active and to facilitate rebalancing when new consumers join or leave the group. The value must be set lower than session_timeout_ms, but typically should be set no higher than 1/3 of that value. It can be adjusted even lower to control the expected time for normal rebalances. Default: 3000

* receive_buffer_bytes (int) – The size of the TCP receive buffer (SO_RCVBUF) to use when reading data. Default: None (relies on system defaults). The java client defaults to 32768.

* send_buffer_bytes (int) – The size of the TCP send buffer (SO_SNDBUF) to use when sending data. Default: None (relies on system defaults). The java client defaults to 131072.

* socket_options (list) – List of tuple-arguments to socket.setsockopt to apply to broker connection sockets. Default: [(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)]

* consumer_timeout_ms (int) – number of milliseconds to block during message iteration before raising StopIteration (i.e., ending the iterator). Default block forever [float(‘inf’)].  在提升StopIteration（即结束迭代器）之前，在消息迭代期间阻塞的毫秒数。 默认阻止永远[float（'inf'）]。

* skip_double_compressed_messages (bool) – A bug in KafkaProducer <= 1.2.4 caused some messages to be corrupted via double-compression. By default, the fetcher will return these messages as a compressed blob of bytes with a single offset, i.e. how the message was actually published to the cluster. If you prefer to have the fetcher automatically detect corrupt messages and skip them, set this option to True. Default: False.

* security_protocol (str) – Protocol used to communicate with brokers. Valid values are: PLAINTEXT, SSL. Default: PLAINTEXT.

* ssl_context (ssl.SSLContext) – Pre-configured SSLContext for wrapping socket connections. If provided, all other ssl_* configurations will be ignored. Default: None.

* ssl_check_hostname (bool) – Flag to configure whether ssl handshake should verify that the certificate matches the brokers hostname. Default: True.

* ssl_cafile (str) – Optional filename of ca file to use in certificate verification. Default: None.

* ssl_certfile (str) – Optional filename of file in pem format containing the client certificate, as well as any ca certificates needed to establish the certificate’s authenticity. Default: None.

* ssl_keyfile (str) – Optional filename containing the client private key. Default: None.

* ssl_password (str) – Optional password to be used when loading the certificate chain. Default: None.

* ssl_crlfile (str) – Optional filename containing the CRL to check for certificate expiration. By default, no CRL check is done. When providing a file, only the leaf certificate will be checked against this CRL. The CRL can only be checked with Python 3.4+ or 2.7.9+. Default: None.

* api_version (tuple) –
Specify which Kafka API version to use. If set to None, the client will attempt to infer the broker version by probing various APIs. Different versions enable different functionality.

Examples

**(0, 9) enables full group coordination features with automatic**

partition assignment and rebalancing,

**(0, 8, 2) enables kafka-storage offset commits with manual**

partition assignment only,

**(0, 8, 1) enables zookeeper-storage offset commits with manual**

partition assignment only,

**(0, 8, 0) enables basic functionality but requires manual**

partition assignment and offset management.

Default: None

* api_version_auto_timeout_ms (int) – number of milliseconds to throw a timeout exception from the constructor when checking the broker api version. Only applies if api_version set to ‘auto’  检查代理api版本时，从构造函数中抛出超时异常的毫秒数。 仅在api_version设置为“auto”时适用

* connections_max_idle_ms – Close idle connections after the number of milliseconds specified by this config. The broker closes idle connections after connections.max.idle.ms, so this avoids hitting unexpected socket disconnected errors on the client. Default: 540000  在此配置指定的毫秒数后关闭空闲连接。 代理在connections.max.idle.ms之后关闭空闲连接，因此这可以避免在客户端上遇到意外的套接字断开连接错误。 默认值：540000

* metric_reporters (list) – A list of classes to use as metrics reporters. Implementing the AbstractMetricsReporter interface allows plugging in classes that will be notified of new metric creation. Default: []  用作度量标准记录器的类列表。 实现AbstractMetricsReporter接口允许插入将通知新度量标准创建的类。 默认值：[]

* metrics_num_samples (int) – The number of samples maintained to compute metrics. Default: 2

* metrics_sample_window_ms (int) – The maximum age in milliseconds of samples used to compute metrics. Default: 30000

* selector (selectors.BaseSelector) – Provide a specific selector implementation to use for I/O multiplexing. Default: selectors.DefaultSelector

* exclude_internal_topics (bool) – Whether records from internal topics (such as offsets) should be exposed to the consumer. If set to True the only way to receive records from an internal topic is subscribing to it. Requires 0.10+ Default: True  是否应将内部主题（如偏移）的记录暴露给消费者。 如果设置为True，则从内部主题接收记录的唯一方法是订阅它。 需要0.10+默认值：True

* sasl_mechanism (str) – String picking sasl mechanism when security_protocol is SASL_PLAINTEXT or SASL_SSL. Currently only PLAIN is supported. Default: None

* sasl_plain_username (str) – Username for sasl PLAIN authentication. Default: None

* sasl_plain_password (str) – Password for sasl PLAIN authentication. Default: None

* sasl_kerberos_service_name (str) – Service name to include in GSSAPI sasl mechanism handshake. Default: ‘kafka’

* sasl_kerberos_domain_name (str) – kerberos domain name to use in GSSAPI sasl mechanism handshake. Default: one of bootstrap servers

> assign(partitions)

Manually assign a list of TopicPartitions to this consumer.  手动将TopicPartitions列表分配给此使用者。

Parameters:	

partitions (list of TopicPartition) – Assignment for this instance.

Raises:	

* IllegalStateError – If consumer has already called
* subscribe().

Warning

It is not possible to use both manual partition assignment with assign() and group assignment with subscribe().

Note

* This interface does not support incremental assignment and will replace the previous assignment (if there was one).  此接口不支持增量分配，并将替换先前的分配（如果有）。

* Manual topic assignment through this method does not use the consumer’s group management functionality. As such, there will be no rebalance operation triggered when group membership or cluster and topic metadata change.  通过此方法分配手动主题不会使用使用者的组管理功能。 因此，当组成员身份或群集和主题元数据更改时，将不会触发重新平衡操作。

> assignment()

Get the TopicPartitions currently assigned to this consumer.

If partitions were directly assigned using assign(), then this will simply return the same partitions that were previously assigned. If topics were subscribed using subscribe(), then this will give the set of topic partitions currently assigned to the consumer (which may be None if the assignment hasn’t happened yet, or if the partitions are in the process of being reassigned).  如果使用assign() 直接分配分区，那么这将只返回先前分配的相同分区。 如果使用subscribe() 订阅主题，那么这将给出当前分配给使用者的主题分区集（如果尚未发生分配，则可以是None，或者如果分区正在被重新分配的过程中）。

Returns:	{TopicPartition, …}

Return type:	set

> beginning_offsets(partitions)

Get the first offset for the given partitions.

This method does not change the current consumer position of the partitions.

Note

This method may block indefinitely if the partition does not exist.

Parameters:	

partitions (list) – List of TopicPartition instances to fetch offsets for.

Returns:	
int:  The earliest available offsets for the given partitions.

Return type:	

TopicPartition

Raises:	
* UnsupportedVersionError – If the broker does not support looking up the offsets by timestamp.
* KafkaTimeoutError – If fetch failed in request_timeout_ms.

> close(autocommit=True)

Close the consumer, waiting indefinitely for any needed cleanup.

Keyword Arguments:

autocommit (bool) – If auto-commit is configured for this consumer, this optional flag causes the consumer to attempt to commit any pending consumed offsets prior to close. Default: True

> commit(offsets=None)

Commit offsets to kafka, blocking until success or error.

This commits offsets only to Kafka. The offsets committed using this API will be used on the first fetch after every rebalance and also on startup. As such, if you need to store offsets in anything other than Kafka, this API should not be used. To avoid re-processing the last message read if a consumer is restarted, the committed offset should be the next message your application should consume, i.e.: last_offset + 1.

Blocks until either the commit succeeds or an unrecoverable error is encountered (in which case it is thrown to the caller).

Currently only supports kafka-topic offset storage (not zookeeper).

Parameters:	

offsets (dict, optional) – {TopicPartition: OffsetAndMetadata} dict to commit with the configured group_id. Defaults to currently consumed offsets for all subscribed partitions.

> commit_async(offsets=None, callback=None)

Commit offsets to kafka asynchronously, optionally firing callback.

This commits offsets only to Kafka. The offsets committed using this API will be used on the first fetch after every rebalance and also on startup. As such, if you need to store offsets in anything other than Kafka, this API should not be used. To avoid re-processing the last message read if a consumer is restarted, the committed offset should be the next message your application should consume, i.e.: last_offset + 1.

This is an asynchronous call and will not block. Any errors encountered are either passed to the callback (if provided) or discarded.

Parameters:	

* offsets (dict, optional) – {TopicPartition: OffsetAndMetadata} dict to commit with the configured group_id. Defaults to currently consumed offsets for all subscribed partitions.

* callback (callable, optional) – Called as callback(offsets, response) with response as either an Exception or an OffsetCommitResponse struct. This callback can be used to trigger custom actions when a commit request completes.

Returns:	

kafka.future.Future

> committed(partition)

Get the last committed offset for the given partition.

This offset will be used as the position for the consumer in the event of a failure.

This call may block to do a remote call if the partition in question isn’t assigned to this consumer or if the consumer hasn’t yet initialized its cache of committed offsets.

Parameters:	partition (TopicPartition) – The partition to check.

Returns:	The last committed offset, or None if there was no prior commit.

> end_offsets(partitions)

Get the last offset for the given partitions. The last offset of a partition is the offset of the upcoming message, i.e. the offset of the last available message + 1.

This method does not change the current consumer position of the partitions.

Note

This method may block indefinitely if the partition does not exist.

Parameters:	

partitions (list) – List of TopicPartition instances to fetch offsets for.

Returns:	
int : The end offsets for the given partitions.

Return type:  TopicPartition

Raises:	
* UnsupportedVersionError – If the broker does not support looking up the offsets by timestamp.

* KafkaTimeoutError – If fetch failed in request_timeout_ms

> highwater(partition)

Last known highwater offset for a partition.

A highwater offset is the offset that will be assigned to the next message that is produced. It may be useful for calculating lag, by comparing with the reported position. Note that both position and highwater refer to the next offset – i.e., highwater offset is one greater than the newest available message.

Highwater offsets are returned in FetchResponse messages, so will not be available if no FetchRequests have been sent for this partition yet.

Parameters:	partition (TopicPartition) – Partition to check

Returns:	Offset if available

Return type:	int or None

> metrics(raw=False)

Get metrics on consumer performance.

> offsets_for_times(timestamps)

Look up the offsets for the given partitions by timestamp. The returned offset for each partition is the earliest offset whose timestamp is greater than or equal to the given timestamp in the corresponding partition.  按时间戳查找给定分区的偏移量。 每个分区的返回偏移量是最早的偏移量，其时间戳大于或等于相应分区中的给定时间戳。

This is a blocking call. The consumer does not have to be assigned the partitions.

If the message format version in a partition is before 0.10.0, i.e. the messages do not have timestamps, None will be returned for that partition. None will also be returned for the partition if there are no messages in it.

Note

This method may block indefinitely if the partition does not exist.

Parameters:	

timestamps (dict) – {TopicPartition: int} mapping from partition to the timestamp to look up. Unit should be milliseconds since beginning of the epoch (midnight Jan 1, 1970 (UTC))

Returns:	

OffsetAndTimestamp: mapping from partition to the timestamp and offset of the first message with timestamp greater than or equal to the target timestamp.

Return type: TopicPartition

Raises:	
* ValueError – If the target timestamp is negative

* UnsupportedVersionError – If the broker does not support looking up the offsets by timestamp.

* KafkaTimeoutError – If fetch failed in request_timeout_ms

> partitions_for_topic(topic)

Get metadata about the partitions for a given topic.

Parameters:	topic (str) – Topic to check.

Returns:	Partition ids

Return type:	set

> pause(*partitions)

Suspend fetching from the requested partitions.   暂停从请求的分区中获取。

Future calls to poll() will not return any records from these partitions until they have been resumed using resume().

Note: This method does not affect partition subscription. In particular, it does not cause a group rebalance when automatic assignment is used.

Parameters:	*partitions (TopicPartition) – Partitions to pause.

> paused()

Get the partitions that were previously paused using pause().

Returns:	{partition (TopicPartition), …}

Return type:	set

> poll(timeout_ms=0, max_records=None)

Fetch data from assigned topics / partitions.

Records are fetched and returned in batches by topic-partition. On each poll, consumer will try to use the last consumed offset as the starting offset and fetch sequentially. The last consumed offset can be manually set through seek() or automatically set as the last committed offset for the subscribed list of partitions.

Incompatible with iterator interface – use one or the other, not both.

Parameters:	

* timeout_ms (int, optional) – Milliseconds spent waiting in poll if data is not available in the buffer. If 0, returns immediately with any records that are available currently in the buffer, else returns empty. Must not be negative. Default: 0

* max_records (int, optional) – The maximum number of records returned in a single call to poll(). Default: Inherit value from max_poll_records.

Returns:	
Topic to list of records since the last fetch for the
subscribed list of topics and partitions.

Return type: dict

> position(partition)

Get the offset of the next record that will be fetched

Parameters:	partition (TopicPartition) – Partition to check
Returns:	Offset
Return type:	int

> resume(*partitions)

Resume fetching from the specified (paused) partitions.

Parameters:	*partitions (TopicPartition) – Partitions to resume.

> seek(partition, offset)

Manually specify the fetch offset for a TopicPartition.

Overrides the fetch offsets that the consumer will use on the next poll(). If this API is invoked for the same partition more than once, the latest offset will be used on the next poll().

Note: You may lose data if this API is arbitrarily used in the middle of consumption to reset the fetch offsets.

Parameters:	
* partition (TopicPartition) – Partition for seek operation
* offset (int) – Message offset in partition

Raises:	
AssertionError – If offset is not an int >= 0; or if partition is not currently assigned.

> seek_to_beginning(*partitions)

Seek to the oldest available offset for partitions.

Parameters:	*partitions – Optionally provide specific TopicPartitions, otherwise default to all assigned partitions.

Raises:	AssertionError – If any partition is not currently assigned, or if no partitions are assigned.

> seek_to_end(*partitions)[source]

Seek to the most recent available offset for partitions.

Parameters:	*partitions – Optionally provide specific TopicPartitions, otherwise default to all assigned partitions.

Raises:	AssertionError – If any partition is not currently assigned, or if no partitions are assigned.

> subscribe(topics=(), pattern=None, listener=None)

Subscribe to a list of topics, or a topic regex pattern.

Partitions will be dynamically assigned via a group coordinator. Topic subscriptions are not incremental: this list will replace the current assignment (if there is one).

This method is incompatible with assign().

Parameters:	

* topics (list) – List of topics for subscription.

* pattern (str) – Pattern to match available topics. You must provide either topics or pattern, but not both.

* listener (ConsumerRebalanceListener) –
Optionally include listener callback, which will be called before and after each rebalance operation.

As part of group management, the consumer will keep track of the list of consumers that belong to a particular group and will trigger a rebalance operation if one of the following events trigger:

	* Number of partitions change for any of the subscribed topics
	* Topic is created or deleted
	* An existing member of the consumer group dies
	* A new member is added to the consumer group

When any of these events are triggered, the provided listener will be invoked first to indicate that the consumer’s assignment has been revoked, and then again when the new assignment has been received. Note that this listener will immediately override any listener set in a previous call to subscribe. It is guaranteed, however, that the partitions revoked/assigned through this interface are from topics subscribed in this call.

Raises:	
* IllegalStateError – If called after previously calling assign().
* AssertionError – If neither topics or pattern is provided.
* TypeError – If listener is not a ConsumerRebalanceListener.

> subscription()[source]

Get the current topic subscription.

Returns:	{topic, …}
Return type:	set

> topics()[source]

Get all topics the user is authorized to view.

Returns:	topics
Return type:	set

> unsubscribe()[source]

Unsubscribe from all topics and clear all assigned partitions.

# KafkaProducer

> class kafka.KafkaProducer(**configs)

A Kafka client that publishes records to the Kafka cluster.

The producer is thread safe and sharing a single producer instance across threads will generally be faster than having multiple instances.

The producer consists of a pool of buffer space that holds records that haven’t yet been transmitted to the server as well as a background I/O thread that is responsible for turning these records into requests and transmitting them to the cluster.  生成器包含一个缓冲区空间池，用于保存尚未传输到服务器的记录，以及一个后台I / O线程，负责将这些记录转换为请求并将它们传输到集群。

send() is asynchronous. When called it adds the record to a buffer of pending record sends and immediately returns. This allows the producer to batch together individual records for efficiency.  send() 是异步的。 调用时，它会将记录添加到待处理记录发送的缓冲区中并立即返回。 这允许生产者将各个记录一起批处理以提高效率。

The ‘acks’ config controls the criteria under which requests are considered complete. The “all” setting will result in blocking on the full commit of the record, the slowest but most durable setting.

If the request fails, the producer can automatically retry, unless ‘retries’ is configured to 0. Enabling retries also opens up the possibility of duplicates (see the documentation on message delivery semantics for details: https://kafka.apache.org/documentation.html#semantics ).

The producer maintains buffers of unsent records for each partition. These buffers are of a size specified by the ‘batch_size’ config. Making this larger can result in more batching, but requires more memory (since we will generally have one of these buffers for each active partition).

By default a buffer is available to send immediately even if there is additional unused space in the buffer. However if you want to reduce the number of requests you can set ‘linger_ms’ to something greater than 0. This will instruct the producer to wait up to that number of milliseconds before sending a request in hope that more records will arrive to fill up the same batch. This is analogous to Nagle’s algorithm in TCP. Note that records that arrive close together in time will generally batch together even with linger_ms=0 so under heavy load batching will occur regardless of the linger configuration; however setting this to something larger than 0 can lead to fewer, more efficient requests when not under maximal load at the cost of a small amount of latency.  默认情况下，即使缓冲区中有其他未使用的空间，也可以立即发送缓冲区。 但是，如果您想减少请求数量，可以将“linger_ms”设置为大于0的值。这将指示生产者在发送请求之前等待该毫秒数，希望有更多记录到达以填满 同一批次。 这类似于TCP中的Nagle算法。 请注意，即使在linger_ms = 0的情况下，及时到达的记录通常也会一起批处理，因此在重负载下，无论是否存在延迟配置，都会发生批处理; 但是，将此设置为大于0的值可以在不受最大负载影响的情况下以较少的延迟为代价导致更少，更有效的请求。

The buffer_memory controls the total amount of memory available to the producer for buffering. If records are sent faster than they can be transmitted to the server then this buffer space will be exhausted. When the buffer space is exhausted additional send calls will block.

The key_serializer and value_serializer instruct how to turn the key and value objects the user provides into bytes.

Keyword Arguments:

* bootstrap_servers – ‘host[:port]’ string (or list of ‘host[:port]’ strings) that the producer should contact to bootstrap initial cluster metadata. This does not have to be the full node list. It just needs to have at least one broker that will respond to a Metadata API Request. Default port is 9092. If no servers are specified, will default to localhost:9092.

* client_id (str) – a name for this client. This string is passed in each request to servers and can be used to identify specific server-side log entries that correspond to this client. Default: ‘kafka-python-producer-#’ (appended with a unique number per instance)

* key_serializer (callable) – used to convert user-supplied keys to bytes If not None, called as f(key), should return bytes. Default: None.

* value_serializer (callable) – used to convert user-supplied message values to bytes. If not None, called as f(value), should return bytes. Default: None.

* acks (0, 1, 'all') –
The number of acknowledgments the producer requires the leader to have received before considering a request complete. This controls the durability of records that are sent. The following settings are common:

>> 0: Producer will not wait for any acknowledgment from the server.

The message will immediately be added to the socket buffer and considered sent. No guarantee can be made that the server has received the record in this case, and the retries configuration will not take effect (as the client won’t generally know of any failures). The offset given back for each record will always be set to -1.

>> 1: Wait for leader to write the record to its local log only.

Broker will respond without awaiting full acknowledgement from all followers. In this case should the leader fail immediately after acknowledging the record but before the followers have replicated it then the record will be lost.

>> all: Wait for the full set of in-sync replicas to write the record.

This guarantees that the record will not be lost as long as at least one in-sync replica remains alive. This is the strongest available guarantee.

If unset, defaults to acks=1.

* compression_type (str) – The compression type for all data generated by the producer. Valid values are ‘gzip’, ‘snappy’, ‘lz4’, or None. Compression is of full batches of data, so the efficacy of batching will also impact the compression ratio (more batching means better compression). Default: None.

* retries (int) – Setting a value greater than zero will cause the client to resend any record whose send fails with a potentially transient error. Note that this retry is no different than if the client resent the record upon receiving the error. Allowing retries without setting max_in_flight_requests_per_connection to 1 will potentially change the ordering of records because if two batches are sent to a single partition, and the first fails and is retried but the second succeeds, then the records in the second batch may appear first. Default: 0.

* batch_size (int) – Requests sent to brokers will contain multiple batches, one for each partition with data available to be sent. A small batch size will make batching less common and may reduce throughput (a batch size of zero will disable batching entirely). Default: 16384

* linger_ms (int) – The producer groups together any records that arrive in between request transmissions into a single batched request. Normally this occurs only under load when records arrive faster than they can be sent out. However in some circumstances the client may want to reduce the number of requests even under moderate load. This setting accomplishes this by adding a small amount of artificial delay; that is, rather than immediately sending out a record the producer will wait for up to the given delay to allow other records to be sent so that the sends can be batched together. This can be thought of as analogous to Nagle’s algorithm in TCP. This setting gives the upper bound on the delay for batching: once we get batch_size worth of records for a partition it will be sent immediately regardless of this setting, however if we have fewer than this many bytes accumulated for this partition we will ‘linger’ for the specified time waiting for more records to show up. This setting defaults to 0 (i.e. no delay). Setting linger_ms=5 would have the effect of reducing the number of requests sent but would add up to 5ms of latency to records sent in the absense of load. Default: 0.

* partitioner (callable) – Callable used to determine which partition each message is assigned to. Called (after key serialization): partitioner(key_bytes, all_partitions, available_partitions). The default partitioner implementation hashes each non-None key using the same murmur2 algorithm as the java client so that messages with the same key are assigned to the same partition. When a key is None, the message is delivered to a random partition (filtered to partitions with available leaders only, if possible).

* buffer_memory (int) – The total bytes of memory the producer should use to buffer records waiting to be sent to the server. If records are sent faster than they can be delivered to the server the producer will block up to max_block_ms, raising an exception on timeout. In the current implementation, this setting is an approximation. Default: 33554432 (32MB)

* connections_max_idle_ms – Close idle connections after the number of milliseconds specified by this config. The broker closes idle connections after connections.max.idle.ms, so this avoids hitting unexpected socket disconnected errors on the client. Default: 540000

* max_block_ms (int) – Number of milliseconds to block during send() and partitions_for(). These methods can be blocked either because the buffer is full or metadata unavailable. Blocking in the user-supplied serializers or partitioner will not be counted against this timeout. Default: 60000.

* max_request_size (int) – The maximum size of a request. This is also effectively a cap on the maximum record size. Note that the server has its own cap on record size which may be different from this. This setting will limit the number of record batches the producer will send in a single request to avoid sending huge requests. Default: 1048576.

* metadata_max_age_ms (int) – The period of time in milliseconds after which we force a refresh of metadata even if we haven’t seen any partition leadership changes to proactively discover any new brokers or partitions. Default: 300000

* retry_backoff_ms (int) – Milliseconds to backoff when retrying on errors. Default: 100.

* request_timeout_ms (int) – Client request timeout in milliseconds. Default: 30000.

* receive_buffer_bytes (int) – The size of the TCP receive buffer (SO_RCVBUF) to use when reading data. Default: None (relies on system defaults). Java client defaults to 32768.

* send_buffer_bytes (int) – The size of the TCP send buffer (SO_SNDBUF) to use when sending data. Default: None (relies on system defaults). Java client defaults to 131072.

* socket_options (list) – List of tuple-arguments to socket.setsockopt to apply to broker connection sockets. Default: [(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)]

* reconnect_backoff_ms (int) – The amount of time in milliseconds to wait before attempting to reconnect to a given host. Default: 50.

* reconnect_backoff_max_ms (int) – The maximum amount of time in milliseconds to wait when reconnecting to a broker that has repeatedly failed to connect. If provided, the backoff per host will increase exponentially for each consecutive connection failure, up to this maximum. To avoid connection storms, a randomization factor of 0.2 will be applied to the backoff resulting in a random range between 20% below and 20% above the computed value. Default: 1000.

* max_in_flight_requests_per_connection (int) – Requests are pipelined to kafka brokers up to this number of maximum requests per broker connection. Note that if this setting is set to be greater than 1 and there are failed sends, there is a risk of message re-ordering due to retries (i.e., if retries are enabled). Default: 5.

* security_protocol (str) – Protocol used to communicate with brokers. Valid values are: PLAINTEXT, SSL, SASL_PLAINTEXT, SASL_SSL. Default: PLAINTEXT.

* ssl_context (ssl.SSLContext) – pre-configured SSLContext for wrapping socket connections. If provided, all other ssl_* configurations will be ignored. Default: None.

* ssl_check_hostname (bool) – flag to configure whether ssl handshake should verify that the certificate matches the brokers hostname. default: true.

* ssl_cafile (str) – optional filename of ca file to use in certificate veriication. default: none.

* ssl_certfile (str) – optional filename of file in pem format containing the client certificate, as well as any ca certificates needed to establish the certificate’s authenticity. default: none.

* ssl_keyfile (str) – optional filename containing the client private key. default: none.

* ssl_password (str) – optional password to be used when loading the certificate chain. default: none.

* ssl_crlfile (str) – optional filename containing the CRL to check for certificate expiration. By default, no CRL check is done. When providing a file, only the leaf certificate will be checked against this CRL. The CRL can only be checked with Python 3.4+ or 2.7.9+. default: none.

* api_version (tuple) – Specify which Kafka API version to use. If set to None, the client will attempt to infer the broker version by probing various APIs. Example: (0, 10, 2). Default: None

* api_version_auto_timeout_ms (int) – number of milliseconds to throw a timeout exception from the constructor when checking the broker api version. Only applies if api_version set to ‘auto’

* metric_reporters (list) – A list of classes to use as metrics reporters. Implementing the AbstractMetricsReporter interface allows plugging in classes that will be notified of new metric creation. Default: []

* metrics_num_samples (int) – The number of samples maintained to compute metrics. Default: 2

* metrics_sample_window_ms (int) – The maximum age in milliseconds of samples used to compute metrics. Default: 30000

* selector (selectors.BaseSelector) – Provide a specific selector implementation to use for I/O multiplexing. Default: selectors.DefaultSelector

* sasl_mechanism (str) – string picking sasl mechanism when security_protocol is SASL_PLAINTEXT or SASL_SSL. Currently only PLAIN is supported. Default: None

* sasl_plain_username (str) – username for sasl PLAIN authentication. Default: None

* sasl_plain_password (str) – password for sasl PLAIN authentication. Default: None

* sasl_kerberos_service_name (str) – Service name to include in GSSAPI sasl mechanism handshake. Default: ‘kafka’

* sasl_kerberos_domain_name (str) – kerberos domain name to use in GSSAPI sasl mechanism handshake. Default: one of bootstrap servers

> close(timeout=None)

Close this producer.

Parameters:	timeout (float, optional) – timeout in seconds to wait for completion.

> flush(timeout=None)

Invoking this method makes all buffered records immediately available to send (even if linger_ms is greater than 0) and blocks on the completion of the requests associated with these records. The post-condition of flush() is that any previously sent record will have completed (e.g. Future.is_done() == True). A request is considered completed when either it is successfully acknowledged according to the ‘acks’ configuration for the producer, or it results in an error.

Other threads can continue sending messages while one thread is blocked waiting for a flush call to complete; however, no guarantee is made about the completion of messages sent after the flush call begins.

Parameters:	timeout (float, optional) – timeout in seconds to wait for completion.

Raises:	KafkaTimeoutError – failure to flush buffered records within the provided timeout

> metrics(raw=False)

Get metrics on producer performance.

> partitions_for(topic)

Returns set of all known partitions for the topic.

> send(topic, value=None, key=None, headers=None, partition=None, timestamp_ms=None)

Publish a message to a topic.

Parameters:

* topic (str) – topic where the message will be published

* value (optional) – message value. Must be type bytes, or be serializable to bytes via configured value_serializer. If value is None, key is required and message acts as a ‘delete’. See kafka compaction documentation for more details: https://kafka.apache.org/documentation.html#compaction (compaction requires kafka >= 0.8.1)

* partition (int, optional) – optionally specify a partition. If not set, the partition will be selected using the configured ‘partitioner’.

* key (optional) – a key to associate with the message. Can be used to determine which partition to send the message to. If partition is None (and producer’s partitioner config is left as default), then messages with the same key will be delivered to the same partition (but if key is None, partition is chosen randomly). Must be type bytes, or be serializable to bytes via configured key_serializer.

* headers (optional) – a list of header key value pairs. List items are tuples of str key and bytes value.

* timestamp_ms (int, optional) – epoch milliseconds (from Jan 1 1970 UTC) to use as the message timestamp. Defaults to current time.

Returns: resolves to RecordMetadata

Return type: FutureRecordMetadata

Raises:	
* KafkaTimeoutError – if unable to fetch topic metadata, or unable to obtain memory buffer prior to configured max_block_ms

# KafkaAdminClient

> class kafka.admin.KafkaAdminClient(**configs)

A class for administering the Kafka cluster.

Warning

This is an unstable interface that was recently added and is subject to change without warning. In particular, many methods currently return raw protocol tuples. In future releases, we plan to make these into nicer, more pythonic objects. Unfortunately, this will likely break those interfaces.  这是一个最近添加的不稳定界面，如有更改，恕不另行通知。 特别是，许多方法目前返回原始协议元组。 在未来的版本中，我们计划将这些变成更好，更pythonic的对象。 不幸的是，这可能会破坏这些接口。

The KafkaAdminClient class will negotiate for the latest version of each message protocol format supported by both the kafka-python client library and the Kafka broker. Usage of optional fields from protocol versions that are not supported by the broker will result in IncompatibleBrokerVersion exceptions.  KafkaAdminClient类将协商kafka-python客户端库和Kafka代理支持的每种消息协议格式的最新版本。 使用代理不支持的协议版本中的可选字段将导致IncompatibleBrokerVersion异常。

Use of this class requires a minimum broker version >= 0.10.0.0.

Keyword Arguments:

* bootstrap_servers – ‘host[:port]’ string (or list of ‘host[:port]’ strings) that the consumer should contact to bootstrap initial cluster metadata. This does not have to be the full node list. It just needs to have at least one broker that will respond to a Metadata API Request. Default port is 9092. If no servers are specified, will default to localhost:9092.

* client_id (str) – a name for this client. This string is passed in each request to servers and can be used to identify specific server-side log entries that correspond to this client. Also submitted to GroupCoordinator for logging with respect to consumer group administration. Default: ‘kafka-python-{version}’

* reconnect_backoff_ms (int) – The amount of time in milliseconds to wait before attempting to reconnect to a given host. Default: 50.

* reconnect_backoff_max_ms (int) – The maximum amount of time in milliseconds to wait when reconnecting to a broker that has repeatedly failed to connect. If provided, the backoff per host will increase exponentially for each consecutive connection failure, up to this maximum. To avoid connection storms, a randomization factor of 0.2 will be applied to the backoff resulting in a random range between 20% below and 20% above the computed value. Default: 1000.

* request_timeout_ms (int) – Client request timeout in milliseconds. Default: 30000.

* connections_max_idle_ms – Close idle connections after the number of milliseconds specified by this config. The broker closes idle connections after connections.max.idle.ms, so this avoids hitting unexpected socket disconnected errors on the client. Default: 540000

* retry_backoff_ms (int) – Milliseconds to backoff when retrying on errors. Default: 100.

* max_in_flight_requests_per_connection (int) – Requests are pipelined to kafka brokers up to this number of maximum requests per broker connection. Default: 5.

* receive_buffer_bytes (int) – The size of the TCP receive buffer (SO_RCVBUF) to use when reading data. Default: None (relies on system defaults). Java client defaults to 32768.

* send_buffer_bytes (int) – The size of the TCP send buffer (SO_SNDBUF) to use when sending data. Default: None (relies on system defaults). Java client defaults to 131072.

* socket_options (list) – List of tuple-arguments to socket.setsockopt to apply to broker connection sockets. Default: [(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)]

* metadata_max_age_ms (int) – The period of time in milliseconds after which we force a refresh of metadata even if we haven’t seen any partition leadership changes to proactively discover any new brokers or partitions. Default: 300000

* security_protocol (str) – Protocol used to communicate with brokers. Valid values are: PLAINTEXT, SSL. Default: PLAINTEXT.

* ssl_context (ssl.SSLContext) – Pre-configured SSLContext for wrapping socket connections. If provided, all other ssl_* configurations will be ignored. Default: None.

* ssl_check_hostname (bool) – Flag to configure whether SSL handshake should verify that the certificate matches the broker’s hostname. Default: True.

* ssl_cafile (str) – Optional filename of CA file to use in certificate veriication. Default: None.

* ssl_certfile (str) – Optional filename of file in PEM format containing the client certificate, as well as any CA certificates needed to establish the certificate’s authenticity. Default: None.

* ssl_keyfile (str) – Optional filename containing the client private key. Default: None.

* ssl_password (str) – Optional password to be used when loading the certificate chain. Default: None.

* ssl_crlfile (str) – Optional filename containing the CRL to check for certificate expiration. By default, no CRL check is done. When providing a file, only the leaf certificate will be checked against this CRL. The CRL can only be checked with Python 3.4+ or 2.7.9+. Default: None.

* api_version (tuple) – Specify which Kafka API version to use. If set to None, KafkaClient will attempt to infer the broker version by probing various APIs. Example: (0, 10, 2). Default: None

* api_version_auto_timeout_ms (int) – number of milliseconds to throw a timeout exception from the constructor when checking the broker api version. Only applies if api_version is None

* selector (selectors.BaseSelector) – Provide a specific selector implementation to use for I/O multiplexing. Default: selectors.DefaultSelector

* metrics (kafka.metrics.Metrics) – Optionally provide a metrics instance for capturing network IO stats. Default: None.

* metric_group_prefix (str) – Prefix for metric names. Default: ‘’

* sasl_mechanism (str) – string picking sasl mechanism when security_protocol is SASL_PLAINTEXT or SASL_SSL. Currently only PLAIN is supported. Default: None

* sasl_plain_username (str) – username for sasl PLAIN authentication. Default: None

* sasl_plain_password (str) – password for sasl PLAIN authentication. Default: None

* sasl_kerberos_service_name (str) – Service name to include in GSSAPI sasl mechanism handshake. Default: ‘kafka’

> alter_configs(config_resources)
> close()
> create_partitions(topic_partitions, timeout_ms=None, validate_only=False)
> create_topics(new_topics, timeout_ms=None, validate_only=False)
> delete_topics(topics, timeout_ms=None)
> describe_configs(config_resources, include_synonyms=False)
> describe_consumer_groups(group_ids, group_coordinator_id=None)
> list_consumer_group_offsets(group_id, group_coordinator_id=None, partitions=None)
> list_consumer_groups(broker_ids=None)

# KafkaClient

> class kafka.client.KafkaClient(**configs)

A network client for asynchronous request/response network I/O.

This is an internal class used to implement the user-facing producer and consumer clients.  这是一个内部类，用于实现面向用户的生产者和消费者客户端。

This class is not thread-safe!

cluster

ClusterMetadata – Local cache of cluster metadata, retrieved via MetadataRequests during poll().

> add_topic(topic)
> check_version(node_id=None, timeout=2, strict=False)
> close(node_id=None)
> connected(node_id)
> connection_delay(node_id)
> get_api_versions()
> in_flight_request_count(node_id=None)
> is_disconnected(node_id)
> is_ready(node_id, metadata_priority=True)
> least_loaded_node()
> poll(timeout_ms=None, future=None)
> ready(node_id, metadata_priority=True)
> send(node_id, request)
> set_topics(topics)

# BrokerConnection

> class kafka.BrokerConnection(host, port, afi, **configs)

Initialize a Kafka broker connection

> blacked_out()
> can_send_more()
> check_version(timeout=2, strict=False, topics=[])
> close(error=None)
> connect()
> connected()
> connecting()
> connection_delay()
> disconnected()
> recv()
> send(request)

# ClusterMetadata

> class kafka.cluster.ClusterMetadata(**configs)

A class to manage kafka cluster metadata.

This class does not perform any IO. It simply updates internal state given API responses (MetadataResponse, GroupCoordinatorResponse).

> add_group_coordinator(group, response)
> add_listener(listener)
> available_partitions_for_topic(topic)
> broker_metadata(broker_id)
> brokers()
> coordinator_for_group(group)
> failed_update(exception)
> leader_for_partition(partition)
> partitions_for_broker(broker_id)
> partitions_for_topic(topic)
> refresh_backoff()
> remove_listener(listener)
> request_update()
> topics(exclude_internal_topics=True)
> ttl()
> update_metadata(metadata)
> with_partitions(partitions_to_add)

