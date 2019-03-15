
zero-copy：减少IO操作步骤。

https://blog.csdn.net/lizhitao/article/details/39499283

https://blog.csdn.net/lizhitao/article/details/23743821

Kafka 性能测试和监控

Kafka 可以配置使用 **JMX** 进行运行状态的监控，既可以通过 JDK 自带 Jconsole 来观察结果，也可以通过Java API的方式来。也就是说 JMX 收集监控指标，Jconsole 展示监控指标。

开启JMX端口

修改bin/kafka-server-start.sh，添加JMX_PORT参数，添加后样子如下

if [ "x$KAFKA_HEAP_OPTS" = "x" ]; then
    export KAFKA_HEAP_OPTS="-Xmx1G -Xms1G"
    export JMX_PORT="9999"
fi

通过Jconsole测试时候可以连接 9999 端口

参考： https://www.linuxidc.com/Linux/2015-04/116177.htm

JMX 底层使用 Metrics 库

Metrics is a Java library which gives you unparalleled insight into what your code does in production.

使用 JConsole 的一个好处是不用安装额外的工具，缺点很明显，数据展示不够直观，数据组织形式不友好，更重要的是不能同时监控整个集群的Metrics。

通过 Kafka Manager 展示整个集群的指标，Kafka Manager 是 Yahoo 开源的 Kafka 管理工具。

Kafka性能测试脚本

$KAFKA_HOME/bin/kafka-producer-perf-test.sh

$KAFKA_HOME/bin/kafka-consumer-perf-test.sh

note：不带任何参数直接执行相关脚本可以看到所有的帮助信息




