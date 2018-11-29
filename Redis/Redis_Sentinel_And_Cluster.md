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

