## redis cluster docker

使用 Docker 容器构建 Redis 元素集群

* redis Cluster requires at least 3 master nodes.

* At least 6 nodes are required.


整个集群说明：

由于在测试环境上，所有在同一台机器上启动 6 个 redis-server 进程，端口号如下：

```
6379 6380 6381
6382 6383 6384
```

具体操作过程如下：

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
