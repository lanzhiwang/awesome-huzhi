## redis-cli 常用命令

```bash
## 获取服务器信息
127.0.0.1:6379> info
127.0.0.1:6379> info Stats
# Stats
total_connections_received:1004501
total_commands_processed:893452995
instantaneous_ops_per_sec:446
total_net_input_bytes:280997502576
total_net_output_bytes:1056112833656
instantaneous_input_kbps:134.80
instantaneous_output_kbps:264.30
rejected_connections:0
sync_full:0
sync_partial_ok:0
sync_partial_err:0
expired_keys:581897
evicted_keys:0
keyspace_hits:294070814
keyspace_misses:150990542
pubsub_channels:0
pubsub_patterns:0
latest_fork_usec:87392
migrate_cached_sockets:0
127.0.0.1:6379> 

## 优雅地停止服务器
127.0.0.1:6379> SHUTDOWN [NOSAVE|SAVE]

## 选择数据库
127.0.0.1:6379> select 9
OK

## 判断 key 是否存在
127.0.0.1:6379[9]> exists "rhino:serv:media:running"
(integer) 1
127.0.0.1:6379[9]> exists "rhino:serv:media:waiting"
(integer) 0
127.0.0.1:6379[9]> 

## 查询 key 对应的类型
127.0.0.1:6379[9]> type "rhino:serv:media:running"
hash
127.0.0.1:6379[9]> 

## 查询 Redis 中 key 的个数
127.0.0.1:6379> DBSIZE
(integer) 1
127.0.0.1:6379> 

## 获取 Redis 中的所有的 key
127.0.0.1:6379> KEYS *
1) "mykey"
127.0.0.1:6379> 

127.0.0.1:6379> SCAN 0
1) "0"
2) 1) "mykey"
127.0.0.1:6379> 

## 删除 key
127.0.0.1:6379> help DEL 

  DEL key [key ...]
  summary: Delete a key
  since: 1.0.0
  group: generic

127.0.0.1:6379> 
127.0.0.1:6379> help UNLINK  # 异步删除 key

127.0.0.1:6379> 

## 重命名 key
127.0.0.1:6379> help RENAME

  RENAME key newkey
  summary: Rename a key
  since: 1.0.0
  group: generic

127.0.0.1:6379> 

## 序列化和反序列化
127.0.0.1:6379> help DUMP

  DUMP key
  summary: Return a serialized version of the value stored at the specified key.
  since: 2.6.0
  group: generic

127.0.0.1:6379> 
127.0.0.1:6379> help RESTORE

  RESTORE key ttl serialized-value [REPLACE]
  summary: Create a key using the provided serialized value, previously obtained using DUMP.
  since: 2.6.0
  group: generic

127.0.0.1:6379> 


```







```bash
$ redis-cli -h
redis-cli 3.2.9

Usage: redis-cli [OPTIONS] [cmd [arg [arg ...]]]
  -h <hostname>      Server hostname (default: 127.0.0.1).
  -p <port>          Server port (default: 6379).
  -s <socket>        Server socket (overrides hostname and port).
  -a <password>      Password to use when connecting to the server.
  -r <repeat>        Execute specified command N times.
  -i <interval>      When -r is used, waits <interval> seconds per command.
                     It is possible to specify sub-second times like -i 0.1.
  -n <db>            Database number.
  -x                 Read last argument from STDIN.
  -d <delimiter>     Multi-bulk delimiter in for raw formatting (default: \n).
  -c                 Enable cluster mode (follow -ASK and -MOVED redirections).
  --raw              Use raw formatting for replies (default when STDOUT is
                     not a tty).
  --no-raw           Force formatted output even when STDOUT is not a tty.
  --csv              Output in CSV format.
  --stat             Print rolling stats about server: mem, clients, ...
  --latency          Enter a special mode continuously sampling latency.
  --latency-history  Like --latency but tracking latency changes over time.
                     Default time interval is 15 sec. Change it using -i.
  --latency-dist     Shows latency as a spectrum, requires xterm 256 colors.
                     Default time interval is 1 sec. Change it using -i.
  --lru-test <keys>  Simulate a cache workload with an 80-20 distribution.
  --slave            Simulate a slave showing commands received from the master.
  --rdb <filename>   Transfer an RDB dump from remote server to local file.
  --pipe             Transfer raw Redis protocol from stdin to server.
  --pipe-timeout <n> In --pipe mode, abort with error if after sending all data.
                     no reply is received within <n> seconds.
                     Default timeout: 30. Use 0 to wait forever.
  --bigkeys          Sample Redis keys looking for big keys.
  --scan             List all keys using the SCAN command.
  --pattern <pat>    Useful with --scan to specify a SCAN pattern.
  --intrinsic-latency <sec> Run a test to measure intrinsic system latency.
                     The test will run for the specified amount of seconds.
  --eval <file>      Send an EVAL command using the Lua script at <file>.
  --ldb              Used with --eval enable the Redis Lua debugger.
  --ldb-sync-mode    Like --ldb but uses the synchronous Lua debugger, in
                     this mode the server is blocked and script changes are
                     are not rolled back from the server memory.
  --help             Output this help and exit.
  --version          Output version and exit.

Examples:
  cat /etc/passwd | redis-cli -x set mypasswd
  redis-cli get mypasswd
  redis-cli -r 100 lpush mylist x
  redis-cli -r 100 -i 1 info | grep used_memory_human:
  redis-cli --eval myscript.lua key1 key2 , arg1 arg2 arg3
  redis-cli --scan --pattern '*:12345*'

  (Note: when using --eval the comma separates KEYS[] from ARGV[] items)

When no command is given, redis-cli starts in interactive mode.
Type "help" in interactive mode for information on available commands
and settings.

$

```



