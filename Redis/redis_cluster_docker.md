## redis cluster docker

### 使用 Docker 容器构建 Redis 元素集群

* redis Cluster requires at least 3 master nodes.

* At least 6 nodes are required.


### 整个集群说明：

由于在测试环境上，所有在同一台机器上启动 6 个 redis-server 进程，端口号如下：

```
6379 6380 6381
6382 6383 6384
```

### 具体操作过程如下：

```bash
# 下载 redis 源码，后续编译安装，需要使用 redis-cli 命令创建和测试集群
$ wget http://download.redis.io/releases/redis-5.0.3.tar.gz

# pull 官方镜像
$ docker pull redis

########################################

# docker 容器启动命令
docker run -v /root/work/redis/config/redis_6379.conf:/usr/local/etc/redis/redis.conf -v /root/work/redis/data:/data --network host -d --name redis-6379 redis redis-server /usr/local/etc/redis/redis.conf

-v /root/work/redis/config/redis_6379.conf:/usr/local/etc/redis/redis.conf
# 对每个进程指定一个配置文件，使用端口号命名，通过挂载的方式挂载到容器

-v /root/work/redis/data:/data
# 挂载宿主机目录到容器中，存储 appendonly、dump、集群配置文件、日志文件等
# 相关文件需要在容器启动前创建好

--network host
# 为使用方便，直接使用宿主机的网络命名空间

redis-server /usr/local/etc/redis/redis.conf
# 在容器中使用配置文件启动 redis-server，需要注意不能将 daemonize 设置为 yes

########################################

# redis-server 的配置文件如下（以 redis-6379.conf 为例）
# redis-6379.conf
bind 0.0.0.0
port 6379

# 在 docker 中通过配置文件启动 redis-server时，要将 daemonize 设置为 no
daemonize no
pidfile /data/var/run/redis_6379.pid
loglevel notice
# 需要在挂载目录中提前创建
logfile "/data/var/log/redis_6379.log"

save 900 1
save 300 10
save 60 10000
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump_6379.rdb
dir /data/

appendonly yes
appendfilename "appendonly_6379.aof"

cluster-enabled yes
# 需要在挂载目录中提前创建
cluster-config-file /data/config/nodes-6379.conf
cluster-node-timeout 15000

requirepass Mysoftrdc@321
masterauth Mysoftrdc@321


# redis-6380.conf
# redis-6381.conf
# redis-6382.conf
# redis-6383conf
# redis-6384conf

# 整个目录结构如下
$ pwd
/root/work/redis
$ tree -a .
.
├── config
│   ├── redis_6379.conf
│   ├── redis_6380.conf
│   ├── redis_6381.conf
│   ├── redis_6382.conf
│   ├── redis_6383.conf
│   └── redis_6384.conf
└── data
    ├── appendonly_6379.aof
    ├── appendonly_6380.aof
    ├── appendonly_6381.aof
    ├── appendonly_6382.aof
    ├── appendonly_6383.aof
    ├── appendonly_6384.aof
    ├── config
    │   ├── nodes-6379.conf
    │   ├── nodes-6380.conf
    │   ├── nodes-6381.conf
    │   ├── nodes-6382.conf
    │   ├── nodes-6383.conf
    │   └── nodes-6384.conf
    ├── dump_6379.rdb
    ├── dump_6380.rdb
    ├── dump_6381.rdb
    ├── dump_6382.rdb
    ├── dump_6383.rdb
    ├── dump_6384.rdb
    └── var
        └── log
            ├── redis_6379.log
            ├── redis_6380.log
            ├── redis_6381.log
            ├── redis_6382.log
            ├── redis_6383.log
            └── redis_6384.log

5 directories, 30 files
$


########################################

# 创建集群
$ redis-cli -a Mysoftrdc@321 --cluster create 127.0.0.1:6379 127.0.0.1:6380 127.0.0.1:6381 127.0.0.1:6382 127.0.0.1:6383 127.0.0.1:6384 --cluster-replicas 1
>>> Performing hash slots allocation on 6 nodes...
Master[0] -> Slots 0 - 5460
Master[1] -> Slots 5461 - 10922
Master[2] -> Slots 10923 - 16383
Adding replica 127.0.0.1:6382 to 127.0.0.1:6379
Adding replica 127.0.0.1:6383 to 127.0.0.1:6380
Adding replica 127.0.0.1:6384 to 127.0.0.1:6381
>>> Trying to optimize slaves allocation for anti-affinity
[WARNING] Some slaves are in the same host as their master
M: d2361a18016c24fbfde940891634e777186f64b8 127.0.0.1:6379
   slots:[0-5460] (5461 slots) master
M: cf8c3995dcf966fe3a18c0d0cd5992ec068806bf 127.0.0.1:6380
   slots:[5461-10922] (5462 slots) master
M: 9ce56e43ff12003420d46d4ddf6477d988e58828 127.0.0.1:6381
   slots:[10923-16383] (5461 slots) master
S: 527059a8d5ded590c129a57f970d00c1deeb8f69 127.0.0.1:6382
   replicates 9ce56e43ff12003420d46d4ddf6477d988e58828
S: 3c32fb8638c8a2783b5aa445db08380592178fc3 127.0.0.1:6383
   replicates d2361a18016c24fbfde940891634e777186f64b8
S: 4271f3ccad48eea231abd5f2caf4ff7b575d5cf6 127.0.0.1:6384
   replicates cf8c3995dcf966fe3a18c0d0cd5992ec068806bf
Can I set the above configuration? (type 'yes' to accept): yes
>>> Nodes configuration updated
>>> Assign a different config epoch to each node
>>> Sending CLUSTER MEET messages to join the cluster
Waiting for the cluster to join
..
>>> Performing Cluster Check (using node 127.0.0.1:6379)
M: d2361a18016c24fbfde940891634e777186f64b8 127.0.0.1:6379
   slots:[0-5460] (5461 slots) master
   1 additional replica(s)
S: 3c32fb8638c8a2783b5aa445db08380592178fc3 127.0.0.1:6383
   slots: (0 slots) slave
   replicates d2361a18016c24fbfde940891634e777186f64b8
M: cf8c3995dcf966fe3a18c0d0cd5992ec068806bf 127.0.0.1:6380
   slots:[5461-10922] (5462 slots) master
   1 additional replica(s)
S: 527059a8d5ded590c129a57f970d00c1deeb8f69 127.0.0.1:6382
   slots: (0 slots) slave
   replicates 9ce56e43ff12003420d46d4ddf6477d988e58828
M: 9ce56e43ff12003420d46d4ddf6477d988e58828 127.0.0.1:6381
   slots:[10923-16383] (5461 slots) master
   1 additional replica(s)
S: 4271f3ccad48eea231abd5f2caf4ff7b575d5cf6 127.0.0.1:6384
   slots: (0 slots) slave
   replicates cf8c3995dcf966fe3a18c0d0cd5992ec068806bf
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
$

########################################

$ redis-cli -a Mysoftrdc@321 -c -h 127.0.0.1 -p 6379
127.0.0.1:6379> set name www.ymq.io
-> Redirected to slot [5798] located at 127.0.0.1:6380
OK
127.0.0.1:6380> get name 
"www.ymq.io"
127.0.0.1:6380> 
127.0.0.1:6380> 
127.0.0.1:6380> cluster info
cluster_state:ok
cluster_slots_assigned:16384
cluster_slots_ok:16384
cluster_slots_pfail:0
cluster_slots_fail:0
cluster_known_nodes:6
cluster_size:3
cluster_current_epoch:6
cluster_my_epoch:2
cluster_stats_messages_ping_sent:207
cluster_stats_messages_pong_sent:223
cluster_stats_messages_meet_sent:2
cluster_stats_messages_sent:432
cluster_stats_messages_ping_received:219
cluster_stats_messages_pong_received:209
cluster_stats_messages_meet_received:4
cluster_stats_messages_received:432
127.0.0.1:6380> 
127.0.0.1:6380> 
127.0.0.1:6380> 
127.0.0.1:6380> cluster nodes
4271f3ccad48eea231abd5f2caf4ff7b575d5cf6 127.0.0.1:6384@16384 slave cf8c3995dcf966fe3a18c0d0cd5992ec068806bf 0 1558073793088 6 connected
9ce56e43ff12003420d46d4ddf6477d988e58828 127.0.0.1:6381@16381 master - 0 1558073791000 3 connected 10923-16383
527059a8d5ded590c129a57f970d00c1deeb8f69 127.0.0.1:6382@16382 slave 9ce56e43ff12003420d46d4ddf6477d988e58828 0 1558073792000 3 connected
cf8c3995dcf966fe3a18c0d0cd5992ec068806bf 127.0.0.1:6380@16380 myself,master - 0 1558073790000 2 connected 5461-10922
3c32fb8638c8a2783b5aa445db08380592178fc3 127.0.0.1:6383@16383 slave d2361a18016c24fbfde940891634e777186f64b8 0 1558073790000 5 connected
d2361a18016c24fbfde940891634e777186f64b8 127.0.0.1:6379@16379 master - 0 1558073792034 1 connected 0-5460
127.0.0.1:6380> quit
$

```

### 使用哨兵监控

```bash
# docker 容器启动命令
docker run -v /root/work/redis/config/sentinel_26379.conf:/data/config/sentinel_26379.conf -v /root/work/redis/data:/data --network host -d --name sentinel_26379 redis redis-server /data/config/sentinel_26379.conf --sentinel

-v /root/work/redis/config/sentinel_26379.conf:/data/config/sentinel_26379.conf 
# 使用初始的配置文件启动 sentinel 进程
# /data/config/sentinel_26379.conf 这个配置文件在 sentinel 进程启动后会自动修改

-v /root/work/redis/data:/data 
# 存储相关数据

redis-server /data/config/sentinel_26379.conf --sentinel
# 启动 sentinel 进程

########################################
# 启动 sentinel 进程的初始配置文件

# sentinel_26379.conf

bind 0.0.0.0
port 26379

# 需要在挂载目录中提前创建
logfile "/data/var/log/sentinel_26379.log"

# 需要在挂载目录中提前创建
dir /data/sentinel/tmp_26379

daemonize no
pidfile /data/var/run/sentinel_26379.pid

sentinel monitor master_6379 127.0.0.1 6379 2
sentinel down-after-milliseconds master_6379 30000
sentinel parallel-syncs master_6379 1
sentinel failover-timeout master_6379 180000

sentinel deny-scripts-reconfig yes

sentinel monitor master_6380 127.0.0.1 6380 2
sentinel down-after-milliseconds master_6380 30000
sentinel parallel-syncs master_6380 1
sentinel failover-timeout master_6380 180000

sentinel monitor master_6381 127.0.0.1 6381 2
sentinel down-after-milliseconds master_6381 30000
sentinel parallel-syncs master_6381 1
sentinel failover-timeout master_6381 180000

########################################

# sentinel_26380.conf

bind 0.0.0.0
port 26380

# 需要在挂载目录中提前创建
logfile "/data/var/log/sentinel_26380.log"

# 需要在挂载目录中提前创建
dir /data/sentinel/tmp_26380

daemonize no
pidfile /data/var/run/sentinel_26380.pid

sentinel monitor master_6379 127.0.0.1 6379 2
sentinel down-after-milliseconds master_6379 30000
sentinel parallel-syncs master_6379 1
sentinel failover-timeout master_6379 180000

sentinel deny-scripts-reconfig yes

sentinel monitor master_6380 127.0.0.1 6380 2
sentinel down-after-milliseconds master_6380 30000
sentinel parallel-syncs master_6380 1
sentinel failover-timeout master_6380 180000

sentinel monitor master_6381 127.0.0.1 6381 2
sentinel down-after-milliseconds master_6381 30000
sentinel parallel-syncs master_6381 1
sentinel failover-timeout master_6381 180000

########################################

# sentinel_26381.conf

bind 0.0.0.0
port 26381

# 需要在挂载目录中提前创建
logfile "/data/var/log/sentinel_26381.log"

# 需要在挂载目录中提前创建
dir /data/sentinel/tmp_26381

daemonize no
pidfile /data/var/run/sentinel_26381.pid

sentinel monitor master_6379 127.0.0.1 6379 2
sentinel down-after-milliseconds master_6379 30000
sentinel parallel-syncs master_6379 1
sentinel failover-timeout master_6379 180000

sentinel deny-scripts-reconfig yes

sentinel monitor master_6380 127.0.0.1 6380 2
sentinel down-after-milliseconds master_6380 30000
sentinel parallel-syncs master_6380 1
sentinel failover-timeout master_6380 180000

sentinel monitor master_6381 127.0.0.1 6381 2
sentinel down-after-milliseconds master_6381 30000
sentinel parallel-syncs master_6381 1
sentinel failover-timeout master_6381 180000

########################################

# 日志文件内容
[root@lanzhiwang-centos7 log]# cat sentinel_26379.log 
1:X 17 May 2019 09:29:31.804 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
1:X 17 May 2019 09:29:31.804 # Redis version=5.0.5, bits=64, commit=00000000, modified=0, pid=1, just started
1:X 17 May 2019 09:29:31.804 # Configuration loaded
1:X 17 May 2019 09:29:31.805 * Running mode=sentinel, port=26379.
1:X 17 May 2019 09:29:31.805 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
1:X 17 May 2019 09:29:31.808 # Sentinel ID is 6656add9bb1082f40edddfc086b729648fadfaf7
1:X 17 May 2019 09:29:31.808 # +monitor master master_6381 127.0.0.1 6381 quorum 2
1:X 17 May 2019 09:29:31.808 # +monitor master master_6379 127.0.0.1 6379 quorum 2
1:X 17 May 2019 09:29:31.808 # +monitor master master_6380 127.0.0.1 6380 quorum 2
1:X 17 May 2019 09:30:01.829 # +sdown master master_6381 127.0.0.1 6381
1:X 17 May 2019 09:30:01.829 # +sdown master master_6379 127.0.0.1 6379
1:X 17 May 2019 09:30:01.829 # +sdown master master_6380 127.0.0.1 6380
[root@lanzhiwang-centos7 log]# 
[root@lanzhiwang-centos7 log]# cat sentinel_26380.log 
1:X 17 May 2019 09:30:10.581 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
1:X 17 May 2019 09:30:10.581 # Redis version=5.0.5, bits=64, commit=00000000, modified=0, pid=1, just started
1:X 17 May 2019 09:30:10.581 # Configuration loaded
1:X 17 May 2019 09:30:10.582 * Running mode=sentinel, port=26380.
1:X 17 May 2019 09:30:10.582 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
1:X 17 May 2019 09:30:10.586 # Sentinel ID is 3debc3071cc55a1a6b388e6b2aede6ce19d3a526
1:X 17 May 2019 09:30:10.586 # +monitor master master_6380 127.0.0.1 6380 quorum 2
1:X 17 May 2019 09:30:10.586 # +monitor master master_6381 127.0.0.1 6381 quorum 2
1:X 17 May 2019 09:30:10.586 # +monitor master master_6379 127.0.0.1 6379 quorum 2
1:X 17 May 2019 09:30:40.629 # +sdown master master_6380 127.0.0.1 6380
1:X 17 May 2019 09:30:40.629 # +sdown master master_6381 127.0.0.1 6381
1:X 17 May 2019 09:30:40.629 # +sdown master master_6379 127.0.0.1 6379
[root@lanzhiwang-centos7 log]# 
[root@lanzhiwang-centos7 log]# cat sentinel_26381.log 
1:X 17 May 2019 09:30:45.781 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
1:X 17 May 2019 09:30:45.781 # Redis version=5.0.5, bits=64, commit=00000000, modified=0, pid=1, just started
1:X 17 May 2019 09:30:45.781 # Configuration loaded
1:X 17 May 2019 09:30:45.783 * Running mode=sentinel, port=26381.
1:X 17 May 2019 09:30:45.783 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
1:X 17 May 2019 09:30:45.787 # Sentinel ID is a0365de2c030201f6b9b889754cc901a66dca2e7
1:X 17 May 2019 09:30:45.787 # +monitor master master_6379 127.0.0.1 6379 quorum 2
1:X 17 May 2019 09:30:45.787 # +monitor master master_6381 127.0.0.1 6381 quorum 2
1:X 17 May 2019 09:30:45.787 # +monitor master master_6380 127.0.0.1 6380 quorum 2
1:X 17 May 2019 09:31:15.823 # +sdown master master_6379 127.0.0.1 6379
1:X 17 May 2019 09:31:15.824 # +sdown master master_6381 127.0.0.1 6381
1:X 17 May 2019 09:31:15.824 # +sdown master master_6380 127.0.0.1 6380
[root@lanzhiwang-centos7 log]# 

########################################

# 进程修改后的配置文件

[root@lanzhiwang-centos7 config]# cat sentinel_26379.conf 
bind 0.0.0.0
port 26379

# 需要在挂载目录中提前创建
logfile "/data/var/log/sentinel_26379.log"

# 需要在挂载目录中提前创建
dir "/data/sentinel/tmp_26379"

daemonize no
pidfile "/data/var/run/sentinel_26379.pid"

sentinel myid 6656add9bb1082f40edddfc086b729648fadfaf7

sentinel deny-scripts-reconfig yes

sentinel monitor master_6381 127.0.0.1 6381 2
sentinel config-epoch master_6381 0
sentinel leader-epoch master_6381 0

sentinel monitor master_6379 127.0.0.1 6379 2
sentinel config-epoch master_6379 0
sentinel leader-epoch master_6379 0

sentinel monitor master_6380 127.0.0.1 6380 2
sentinel config-epoch master_6380 0
sentinel leader-epoch master_6380 0

sentinel current-epoch 0

[root@lanzhiwang-centos7 config]# 

[root@lanzhiwang-centos7 config]# cat sentinel_26380.conf 
bind 0.0.0.0
port 26380

# 需要在挂载目录中提前创建
logfile "/data/var/log/sentinel_26380.log"

# 需要在挂载目录中提前创建
dir "/data/sentinel/tmp_26380"

daemonize no
pidfile "/data/var/run/sentinel_26380.pid"

sentinel myid 3debc3071cc55a1a6b388e6b2aede6ce19d3a526

sentinel deny-scripts-reconfig yes

sentinel monitor master_6380 127.0.0.1 6380 2
sentinel config-epoch master_6380 0
sentinel leader-epoch master_6380 0

sentinel monitor master_6381 127.0.0.1 6381 2
sentinel config-epoch master_6381 0
sentinel leader-epoch master_6381 0

sentinel monitor master_6379 127.0.0.1 6379 2
sentinel config-epoch master_6379 0
sentinel leader-epoch master_6379 0

sentinel current-epoch 0

[root@lanzhiwang-centos7 config]# 


[root@lanzhiwang-centos7 config]# cat sentinel_26381.conf 
bind 0.0.0.0
port 26381

# 需要在挂载目录中提前创建
logfile "/data/var/log/sentinel_26381.log"

# 需要在挂载目录中提前创建
dir "/data/sentinel/tmp_26381"

daemonize no
pidfile "/data/var/run/sentinel_26381.pid"

sentinel myid a0365de2c030201f6b9b889754cc901a66dca2e7

sentinel deny-scripts-reconfig yes

sentinel monitor master_6379 127.0.0.1 6379 2
sentinel config-epoch master_6379 0
sentinel leader-epoch master_6379 0

sentinel monitor master_6381 127.0.0.1 6381 2
sentinel config-epoch master_6381 0
sentinel leader-epoch master_6381 0

sentinel monitor master_6380 127.0.0.1 6380 2
sentinel config-epoch master_6380 0
sentinel leader-epoch master_6380 0

sentinel current-epoch 0

[root@lanzhiwang-centos7 config]# 

########################################

# 相关测试

# 哨兵集群整体状态
[root@lanzhiwang-centos7 config]# redis-cli -p 26379
127.0.0.1:26379> info Sentinel
# Sentinel
sentinel_masters:3
sentinel_tilt:0
sentinel_running_scripts:0
sentinel_scripts_queue_length:0
sentinel_simulate_failure_flags:0
master0:name=master_6381,status=sdown,address=127.0.0.1:6381,slaves=0,sentinels=1
master1:name=master_6379,status=sdown,address=127.0.0.1:6379,slaves=0,sentinels=1
master2:name=master_6380,status=sdown,address=127.0.0.1:6380,slaves=0,sentinels=1
127.0.0.1:26379> 

# redis 集群主从关系
# 6379->6382
# 6380->6383
# 6381->6384
[root@lanzhiwang-centos7 config]# redis-cli -p 6379.
127.0.0.1:6379> auth Mysoftrdc@321
OK
127.0.0.1:6379> info Replication
# Replication
role:master
connected_slaves:1
slave0:ip=127.0.0.1,port=6382,state=online,offset=11256,lag=1
master_replid:cbc28bb1bbc739e3a580db4ab48e57d8051b69e7
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:11270
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:11270
127.0.0.1:6379> 

[root@lanzhiwang-centos7 config]# redis-cli -a Mysoftrdc@321 -p 6380
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
127.0.0.1:6380> info Replication
# Replication
role:master
connected_slaves:1
slave0:ip=127.0.0.1,port=6383,state=online,offset=11571,lag=0
master_replid:055399bd0c8173152ca3bf0406f6ef19c787741f
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:11571
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:11571
127.0.0.1:6380> 

[root@lanzhiwang-centos7 config]# redis-cli -a Mysoftrdc@321 -p 6381
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
127.0.0.1:6381> info Replication
# Replication
role:master
connected_slaves:1
slave0:ip=127.0.0.1,port=6384,state=online,offset=11592,lag=0
master_replid:44e9f8045b4a1ea27302beec82dbd9a55f851257
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:11592
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:11592
127.0.0.1:6381> 

# 模拟 6379 下线，6379 下线方法是使用 shutdown 指令
[root@lanzhiwang-centos7 ~]# redis-cli -a Mysoftrdc@321 -p 6379
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
127.0.0.1:6379> info Replication
# Replication
role:master
connected_slaves:1
slave0:ip=127.0.0.1,port=6382,state=online,offset=12642,lag=1
master_replid:cbc28bb1bbc739e3a580db4ab48e57d8051b69e7
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:12642
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:12642
127.0.0.1:6379> shutdown
not connected> 

# 经过一段时间后，6382 变成了主节点
[root@lanzhiwang-centos7 ~]# redis-cli -a Mysoftrdc@321 -p 6382
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
127.0.0.1:6382> 
127.0.0.1:6382> info Replication
# Replication
role:slave
master_host:127.0.0.1
master_port:6379
master_link_status:up
master_last_io_seconds_ago:8
master_sync_in_progress:0
slave_repl_offset:12740
slave_priority:100
slave_read_only:1
connected_slaves:0
master_replid:cbc28bb1bbc739e3a580db4ab48e57d8051b69e7
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:12740
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:12740
127.0.0.1:6382> 
127.0.0.1:6382> 
127.0.0.1:6382> info Replication
# Replication
role:master
connected_slaves:0
master_replid:5cdc1a1746209db43df39bd59e5078df84ea81e2
master_replid2:cbc28bb1bbc739e3a580db4ab48e57d8051b69e7
master_repl_offset:12768
second_repl_offset:12769
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:12768
127.0.0.1:6382> 

```
