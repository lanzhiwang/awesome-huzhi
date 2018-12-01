## Redis Replication

```bash
## 建立主从复制关系，在从服务器上使用命令行或者配置文件
127.0.0.1:6379> slaveof 127.0.0.1 6379

# 配置文件
slaveof 127.0.0.1 6379

127.0.0.1:6379> help SLAVEOF

  SLAVEOF host port
  summary: Make the server a slave of another instance, or promote it as master
  since: 1.0.0
  group: server

127.0.0.1:6379> 

## 检查主从复制关系
127.0.0.1:6379> info REPLICATION
```

