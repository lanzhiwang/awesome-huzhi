## Redis Replication

```bash
127.0.0.1:6379> slaveof 127.0.0.1 6379

# 配置文件
slaveof 127.0.0.1 6379

127.0.0.1:6379> help SLAVEOF

  SLAVEOF host port
  summary: Make the server a slave of another instance, or promote it as master
  since: 1.0.0
  group: server

127.0.0.1:6379> 

```

