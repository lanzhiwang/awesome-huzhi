### bitmap

```bash
SETBIT key offset value
GETBIT key offset
BITCOUNT key [start end]

BITOP operation destkey key [key ...]
  summary: Perform bitwise operations between strings
  operation: and or xor not
  since: 2.6.0
  
127.0.0.1:6379> help @string
```



### 过期时间

```bash
## 设置过期时间
127.0.0.1:6379> help EXPIRE

  EXPIRE key seconds
  summary: Set a key's time to live in seconds
  since: 1.0.0
  group: generic

127.0.0.1:6379> 
127.0.0.1:6379> help EXPIREAT

  EXPIREAT key timestamp
  summary: Set the expiration for a key as a UNIX timestamp
  since: 1.2.0
  group: generic

127.0.0.1:6379> 


## 查询过期时间
127.0.0.1:6379> help TTL

  TTL key
  summary: Get the time to live for a key
  since: 1.0.0
  group: generic

127.0.0.1:6379> 

## 删除过期时间，是 key 永久有效
127.0.0.1:6379> help PERSIST

  PERSIST key
  summary: Remove the expiration from a key
  since: 2.2.0
  group: generic

127.0.0.1:6379> 

```

删除已过期的 key 的方法:

* 通过访问过期的 key 被动过期
* 服务主动删除



### sort

```bash
127.0.0.1:6379> help SORT

  SORT key [BY pattern] [LIMIT offset count] [GET pattern [GET pattern ...]] [ASC|DESC] [ALPHA] [STORE destination]
  summary: Sort the elements in a list, set or sorted set
  since: 1.0.0
  group: generic

127.0.0.1:6379> 

sort key  ## 数值升序ASC
sort key ALPHA  ## 字符串按字典排序
sort key limit offset count alpha  ## 限制返回的元素个数，默认返回全部元素

```



### Redis 管道

```bash
$ cat pipeline.txt 
set mykey myvalue
sadd myset value1 value2
get mykey
scard myset

$ unix2dos pipeline.txt
$ cat pipeline.txt | redis-cli --pipe
All data transferred. Waiting for the last reply...
Last reply received from server.
errors: 0, replies: 4

## RESP 字符串中表示字符大小的$符号不需要转义
$ cat datapipe.txt
*3\r\n$3\r\nSET\r\n$5\r\nmykey\r\n$7\r\nmyvalue\r\n*4\r\n$4\r\nSADD\r\n$5\r\nmyset\r\n$6\r\nvalue1\r\n$6\r\nvalue2\r\n*2\r\n$3\r\nGET\r\n$5\r\nmykey\r\n*2\r\n$5\r\nSCARD\r\n$5\r\nmyset\r\n

$ unix2dos datapipe.txt
$ echo -e "$(cat datapipe.txt)" | redis-cli --pipe
All data transferred. Waiting for the last reply...
Last reply received from server.
errors: 0, replies: 4
$ 


```



### Redis 事务

```bash
## 基本事务处理
redis 127.0.0.1:6379> MULTI  # 标记事务开始
OK
 
redis 127.0.0.1:6379> INCR user_id  # 多条命令按顺序入队
QUEUED
 
redis 127.0.0.1:6379> INCR user_id
QUEUED
 
redis 127.0.0.1:6379> INCR user_id
QUEUED
 
redis 127.0.0.1:6379> PING
QUEUED
 
redis 127.0.0.1:6379> EXEC  # 执行
1) (integer) 1
2) (integer) 2
3) (integer) 3
4) PONG


## 监视 key，且事务成功执行
redis 127.0.0.1:6379> WATCH lock lock_times  # Unwatch 命令用于取消WATCH命令对所有key的监视
OK
 
redis 127.0.0.1:6379> MULTI
OK
 
redis 127.0.0.1:6379> SET lock "huangz"
QUEUED
 
redis 127.0.0.1:6379> INCR lock_times
QUEUED
 
redis 127.0.0.1:6379> EXEC
1) OK
2) (integer) 1
 
 
## 监视 key，且事务被打断
redis 127.0.0.1:6379> WATCH lock lock_times
OK
 
redis 127.0.0.1:6379> MULTI
OK
 
redis 127.0.0.1:6379> SET lock "joe"  # 就在这时，另一个客户端修改了 lock_times 的值
QUEUED
 
redis 127.0.0.1:6379> INCR lock_times
QUEUED
 
redis 127.0.0.1:6379> EXEC  # 因为 lock_times 被修改， joe 的事务执行失败
(nil)

## 取消事物
redis 127.0.0.1:6379> MULTI
OK
 
redis 127.0.0.1:6379> PING
QUEUED
 
redis 127.0.0.1:6379> SET greeting "hello"
QUEUED
 
redis 127.0.0.1:6379> DISCARD
OK


127.0.0.1:6379> help @transactions

  DISCARD -
  summary: Discard all commands issued after MULTI
  since: 2.0.0

  EXEC -
  summary: Execute all commands issued after MULTI
  since: 1.2.0

  MULTI -
  summary: Mark the start of a transaction block
  since: 1.2.0

  UNWATCH -
  summary: Forget about all watched keys
  since: 2.2.0

  WATCH key [key ...]
  summary: Watch the given keys to determine execution of the MULTI/EXEC block
  since: 2.2.0

127.0.0.1:6379> 

```



### Redis 发布订阅

```bash
## 首先订阅频道（channel）
SUBSCRIBE channel [channel ...]
PSUBSCRIBE pattern [pattern ...]

## 取消订阅
UNSUBSCRIBE [channel [channel ...]]
PUNSUBSCRIBE [pattern [pattern ...]]

## 其次向频道发布消息
PUBLISH channel message

## 管理频道
PUBSUB subcommand [argument [argument ...]]
$ PUBSUB CHANNELS


```



### 在 Redis 中使用 Lua 脚本

```bash


$ cat updatejson.lua 
local id = KEYS[1]
local data = ARGV[1]
local dataSource = cjson.decode(data)

local retJson = redis.call('get',  id)
if retJson == false then
    retJson = {}
else
    retJson = cjson.decode(retJson)
end
   
for k,v in pairs(dataSource) do 
    retJson[k] = v 
end
redis.call('set', id, cjson.encode(retJson))
return redis.call('get',id)

## 执行 lua 脚本
127.0.0.1:6379> help eval

  EVAL script numkeys key [key ...] arg [arg ...]
  summary: Execute a Lua script server side
  since: 2.6.0
  group: scripting

127.0.0.1:6379> 

redis-cli --eval myscript.lua key1 key2 , arg1 arg2 arg3
(Note: when using --eval the comma separates KEYS[] from ARGV[] items)

$ redis-cli --eval updatejson.lua 1 users:id:9925, '{"name": "Tina", "sex": "female", "grade": "A"}'


## 注册 Lua 脚本到 Redis 服务器中
127.0.0.1:6379> help SCRIPT LOAD

  SCRIPT LOAD script
  summary: Load the specified Lua script into the script cache.
  since: 2.6.0
  group: scripting

127.0.0.1:6379> 

$ redis-cli SCRIPT LOAD "`cat updatejson.lua`"
"6ac65d47b0795005b102929d81679f5c61310910"

## 执行注册后的脚本
127.0.0.1:6379> help evalsha

  EVALSHA sha1 numkeys key [key ...] arg [arg ...]
  summary: Execute a Lua script server side
  since: 2.6.0
  group: scripting

127.0.0.1:6379> 

$ redis-cli evalsha 6ac65d47b0795005b102929d81679f5c61310910 1 users:id:9925, '{"name": "Tina", "sex": "female", "grade": "A"}'

```





