## Redis Persistence

### RDB

```bash
127.0.0.1:6379> CONFIG SET SAVE "900 1 300 10 60 10000"

# 配置文件
save 900 1 
save 300 10
save 60 10000

127.0.0.1:6379> help CONFIG SET

  CONFIG SET parameter value
  summary: Set a configuration parameter to the given value
  since: 2.0.0
  group: server

127.0.0.1:6379> 

127.0.0.1:6379> help SAVE

  SAVE -
  summary: Synchronously save the dataset to disk
  since: 1.0.0
  group: server

127.0.0.1:6379> 

```

### AOF

```bash
127.0.0.1:6379> CONFIG SET appendonly yes

# 配置文件
appendonly yes
```

