## Redis Sentinel And Cluster

### 配置主从复制和哨兵

| 编号 | IP           | 角色 | port |
| :--: | :----------: | :--: | :--: |
| 1 | 192.168.0.31 | Master、Sentinel-1 | 6379、26379 |
| 2 | 192.168.0.32 | Slave-1、Sentinel-2 | 6379、26379 |
| 3 | 192.168.0.33 | Slave-2、Sentinel-3 | 6379、26379 |

```bash
## step 1：修改所有机器的配置文件 redis.conf 选项 bind
bind 0.0.0.0

## step 2：修改 Slave-1 和 Slave-1 上的配置文件 redis.conf 选项 slaveof
slaveof 192.168.0.31 6379

## step 3：在所有的机器上启动 redis 服务
$ redis-server redis.conf

## step 4：在所有的机器上拷贝 redis 源码中的 sentinel.conf 文件作为 sentinel 进程的配置文件，并且需要保证运行 sentinel 的进程的用户具有写入 sentinel.conf 文件的权限，sentinel 进程启动后会向配置文件中写入一些信息
$ cat sentinel.conf
port 26379
dir /tmp
sentinel monitor mymaster 192.168.0.31 6379 2
sentinel down-after-milliseconds mymaster 30000
sentinel parallel-syncs mymaster 1
sentinel failover-timeout mymaster 180000
sentinel deny-scripts-reconfig yes

## 在所有机器上启动 sentinel 进程
$ redis-server sentinel.conf --sentinel

## 观察日志和sentinel.conf文件，sentinel.conf文件会写入新的信息

## 管理 sentinel，无论连接那台机器的 26379 端口进程都可以
$ redis-cli -h 192.168.0.33 -p 26379
192.168.0.33:26379> sentinel 
```



### 配置 Redis Cluster





```bash
$ cat redis.conf
################################## INCLUDES ###################################
# include /path/to/local.conf
# include /path/to/other.conf

################################## MODULES #####################################
# loadmodule /path/to/my_module.so
# loadmodule /path/to/other_module.so

################################## NETWORK #####################################
bind 127.0.0.1
protected-mode yes
port 6379
tcp-backlog 511
timeout 0
tcp-keepalive 300

################################# GENERAL #####################################
daemonize no
supervised no
pidfile /var/run/redis_6379.pid
loglevel notice
logfile ""
# syslog-enabled no
# syslog-ident redis
# syslog-facility local0
databases 16
always-show-logo yes

################################ SNAPSHOTTING  ################################
save 900 1
save 300 10
save 60 10000
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir ./

################################# REPLICATION #################################
# slaveof <masterip> <masterport>
# masterauth <master-password>
slave-serve-stale-data yes
slave-read-only yes
repl-diskless-sync no
repl-diskless-sync-delay 5
# repl-ping-slave-period 10
# repl-timeout 60
repl-disable-tcp-nodelay no
# repl-backlog-size 1mb
# repl-backlog-ttl 3600
slave-priority 100
# min-slaves-to-write 3
# min-slaves-max-lag 10
# slave-announce-ip 5.5.5.5
# slave-announce-port 1234

################################## SECURITY ###################################
# requirepass foobared
# rename-command CONFIG ""

################################### CLIENTS ####################################
# maxclients 10000

############################## MEMORY MANAGEMENT ################################
# maxmemory <bytes>
# LRU means Least Recently Used
# LFU means Least Frequently Used
# maxmemory-policy noeviction
# maxmemory-samples 5

############################# LAZY FREEING ####################################
lazyfree-lazy-eviction no
lazyfree-lazy-expire no
lazyfree-lazy-server-del no
slave-lazy-flush no

############################## APPEND ONLY MODE ###############################
appendonly no
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
aof-load-truncated yes
aof-use-rdb-preamble no

################################ LUA SCRIPTING  ###############################
lua-time-limit 5000

################################ REDIS CLUSTER  ###############################
# cluster-enabled yes
# cluster-config-file nodes-6379.conf
# cluster-node-timeout 15000
# cluster-slave-validity-factor 10
# cluster-migration-barrier 1
# cluster-require-full-coverage yes
# cluster-slave-no-failover no

########################## CLUSTER DOCKER/NAT support  ########################
# cluster-announce-ip 10.1.1.5
# cluster-announce-port 6379
# cluster-announce-bus-port 6380

################################## SLOW LOG ###################################
slowlog-log-slower-than 10000
slowlog-max-len 128

################################ LATENCY MONITOR ##############################
latency-monitor-threshold 0

############################# EVENT NOTIFICATION ##############################
notify-keyspace-events ""

############################### ADVANCED CONFIG ###############################
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
list-max-ziplist-size -2
list-compress-depth 0
set-max-intset-entries 512
zset-max-ziplist-entries 128
zset-max-ziplist-value 64
hll-sparse-max-bytes 3000
activerehashing yes
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit slave 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
# client-query-buffer-limit 1gb
# proto-max-bulk-len 512mb
hz 10
aof-rewrite-incremental-fsync yes
# lfu-log-factor 10
# lfu-decay-time 1

########################### ACTIVE DEFRAGMENTATION #######################
# activedefrag yes
# active-defrag-ignore-bytes 100mb
# active-defrag-threshold-lower 10
# active-defrag-threshold-upper 100
# active-defrag-cycle-min 25
# active-defrag-cycle-max 75


```



```bash
$ cat sentinel.conf 
# bind 127.0.0.1 192.168.1.1
# protected-mode no
port 26379
# sentinel announce-ip <ip>
# sentinel announce-port <port>
dir /tmp
sentinel monitor mymaster 127.0.0.1 6379 2
# sentinel auth-pass mymaster MySUPER--secret-0123passw0rd
sentinel down-after-milliseconds mymaster 30000
sentinel parallel-syncs mymaster 1
sentinel failover-timeout mymaster 180000
# sentinel notification-script mymaster /var/redis/notify.sh
# sentinel client-reconfig-script mymaster /var/redis/reconfig.sh
sentinel deny-scripts-reconfig yes


```

