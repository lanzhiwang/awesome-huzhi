## Redis 通信协议

Redis服务器与客户端通过RESP（REdis Serialization Protocol `Redis 序列化协议`）协议通信

```bash
## 向服务器发送 PING 命令
$ echo -e "*1\r\n\$4\r\nPING\r\n" | nc 127.0.0.1 6379
+PONG

############################################
* 表示数组类型
1 表示数组大小，PING 命令只有一个字符串，数组大小为 1
\r\n 表示每个部分的终结符
\$4 \ 表示 $ 是转义字符，$4 表示后续四个字符 PING 表示字符串
PING 表示字符串本身
+PONG 表示命令的响应字符串，+ 表示响应是一个简单的字符串类型
############################################

## 向服务器发送 set mykey 1 命令
$ echo -e "*3\r\n\$3\r\nset\r\n\$5\r\nmykey\r\n\$1\r\n1\r\n" | nc 127.0.0.1 6379
+OK

############################################
* 表示数组类型
3 set mykey 1 有三个字符串，数组大小为 3
############################################

## 向服务器发送 get mykey 命令
$ echo -e "*2\r\n\$3\r\nget\r\n\$5\r\nmykey\r\n" | nc 127.0.0.1 6379
$1
1

## 向服务器发送 INCR mykey 命令
$ echo -e "*2\r\n\$4\r\nINCR\r\n\$5\r\nmykey\r\n" | nc 127.0.0.1 6379
:2

## 向服务器发送 get mykey 命令
$ echo -e "*2\r\n\$3\r\nget\r\n\$5\r\nmykey\r\n" | nc 127.0.0.1 6379
$1
2


## 向服务器发送错误命令 got mykey
$ echo -e "*2\r\n\$3\r\ngot\r\n\$5\r\nmykey\r\n" | nc 127.0.0.1 6379
-ERR unknown command 'got'


## 组合命令 set foo bar get foo
$ echo -e "*3\r\n\$3\r\nset\r\n\$3\r\nfoo\r\n\$3\r\nbar\r\n*2\r\n\$3\r\nget\r\n\$3\r\nfoo\r\n" | nc 127.0.0.1 6379
+OK
$3
bar

############################################
组合命令
数组的大小只要设置第一个命令 set foo bar 的大小，数组大小为 3
第二个命令之前需要有两个终结符 \r\n*2
############################################



```

