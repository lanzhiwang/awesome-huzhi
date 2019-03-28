## nc 命令使用示例

### 基本使用说明
```
# To open a TCP connection to port 42 of host.example.com, using port 31337 as the source port, with a timeout of 5 seconds:
nc -p 31337 -w 5 host.example.com 42

# To open a UDP connection to port 53 of host.example.com:
nc -u host.example.com 53

# To open a TCP connection to port 42 of host.example.com using 10.1.2.3 as the IP for the local end of the connection:
nc -s 10.1.2.3 host.example.com 42

# To create and listen on a UNIX-domain stream socket:
# -l 选项用于指定 nc 处于侦听模式。指定该参数，则意味着 nc 被当作 server，侦听并接受连接，而非向其它地址发起连接
nc -lU /var/tmp/dsocket

# To connect to port 42 of host.example.com via an HTTP proxy at 10.2.3.4, port 8080. This example could also be used by ssh(1); see the ProxyCommand directive in ssh_config(5) for more information.
nc -x10.2.3.4:8080 -Xconnect host.example.com 42

# The same example again, this time enabling proxy authentication with username "ruser" if the proxy requires it:
nc -x10.2.3.4:8080 -Xconnect -Pruser host.example.com 42

# To choose the source IP for the testing using the -s option
# -v 选项输出交互或出错信息，新手调试时尤为有用
# -z 选项表示 zero，表示扫描时不发送任何数据
nc -zv -s source_IP target_IP Port

$
```

### 使用示例

#### nc 可以作为 server 端启动一个 tcp 的监听

```bash
# 在 192.168.49.244 机器上使用 nc 可以作为 server 端启动一个 tcp 的监听
$ nc -l 9999  # 或者 nc -l 9999 &
$ nc -l 9998 &

$ netstat -tulnp | grep 9999
tcp        0      0 0.0.0.0:9999                0.0.0.0:*                   LISTEN      10578/nc            

# 在 192.168.49.246 上使用各种方法测试端口连通性
$ telnet 192.168.49.244 9999
$ nmap 192.168.49.244 -p9999
$ nc -vz -w 2 192.168.49.244 9999
$ nc -vz -w 2 192.168.49.244 9998-9999

```

#### nc 可以作为 server 端启动一个 udp 的监听

```bash
# 在 192.168.49.244 机器上使用 nc 可以作为 server 端启动一个 udp 的监听
$ nc -lu 9999  # 或者 nc -lu 9999 &
$ nc -lu 9998 &

$ netstat -tulnp | grep 9999
udp        0      0 0.0.0.0:9999                0.0.0.0:*                               10728/nc            

# 在 192.168.49.246 上使用各种方法测试端口连通性
# 无法在客户端使用 telnet 测试，telnet 是运行于 tcp 协议的
$ nmap -sU 192.168.49.244 -p9999 -Pn  # 使用 nmap 命令会导致 9999 端口关闭
# -u 选项表示udp端口
$ nc -vz -w 2 -u 192.168.49.244 9999
$ nc -vz -w 2 -u 192.168.49.244 9998-9999

```

#### 使用 nc 传输文件

基本步骤：
1. 启动接收文件命令
2. 启动发送文件命令

note：也可以先启动发送命令，在启动接收命令

```bash
# 在 192.168.49.244 启动接收文件命令
$ nc -l 9995 > soft.zip

# 在 192.168.49.246 启动发送文件命令
$ nc 192.168.49.244 9995 < soft.zip
```

#### 使用 nc 传输多个文件，也就是传输打包后的目录

```bash
# 在 192.168.49.244 启动接收文件命令
# 管道后面最后必须是 - ，不能是其余自定义的文件名
$ nc -l 9995 | tar zxvf -

# 在 192.168.49.246 启动发送文件命令
# 必须将打包的文件命名为 -
$ tar -zcvf - a b c d e f | nc 192.168.49.244 9995
```

#### 测试网速

```bash
# 从 192.168.49.246 机器上向 192.168.49.244 发送数据，测试 192.168.49.246 的发送速度，192.168.49.244 的接收速度

# 在 192.168.49.244 启动接收命令
$ nc -l 9991 > /dev/null

# 在 192.168.49.244 测试接收速度
$ dstat
----total-cpu-usage---- -dsk/total- -net/total- ---paging-- ---system--
usr sys idl wai hiq siq| read  writ| recv  send|  in   out | int   csw 
  6   1  93   0   0   0|1571k 6026k|   0     0 |  10k 8940B|  19k   12k
  0   1  99   0   0   0|   0  1276k| 118M  586k|   0     0 |  15k   15k
  1   0  99   0   0   0|4096B    0 | 117M  540k|   0     0 |  15k   15k
  1   1  98   0   0   0|   0     0 | 117M  624k|   0     0 |  16k   16k
  0   1  99   0   0   0|4096B    0 | 117M  508k|   0     0 |  15k   15k
  5   1  94   0   0   0|4096B    0 | 117M  551k|   0     0 |  17k   16k
  1   1  99   0   0   0|   0  1224k| 117M  664k|   0     0 |  16k   16k
  1   1  99   0   0   0|   0     0 | 117M  578k|   0     0 |  15k   15k
  1   0  99   0   0   0|   0     0 | 117M  595k|   0     0 |  15k   15k
  0   1  99   0   0   0|   0     0 | 117M  550k|   0     0 |  15k   15k

# 192.168.49.244 接收速度大约是 117M/s

# 在 192.168.49.246 启动发送命令
$ nc 192.168.49.244 9991 < /dev/zero

# 在 192.168.49.246 测试发送速度
$ dstat
----total-cpu-usage---- -dsk/total- -net/total- ---paging-- ---system--
usr sys idl wai hiq siq| read  writ| recv  send|  in   out | int   csw 
  2   0  98   0   0   0| 439k 2131k|   0     0 |2530B 2322B|6781  6076 
  1   1  98   0   0   0|   0     0 |1046k  117M|   0     0 |  13k 5986 
  1   1  98   0   0   0|   0  1252k|1206k  117M|   0     0 |  15k 6895 
  1   0  99   0   0   0|   0  4096B|1195k  117M|   0     0 |  14k 6535 
  1   1  98   0   0   0|   0     0 |1188k  117M|   0     0 |  14k 6402 
  1   1  99   0   0   0|   0    12k|1072k  117M|   0     0 |  13k 5920 
  1   1  98   0   0   0|   0    12k|1256k  117M|   0     0 |  14k 6654 
  1   1  99   0   0   0|   0  1280k|1089k  117M|   0     0 |  14k 6107 
  5   1  95   0   0   0|   0    20k|1176k  117M|   0     0 |  16k 7409 
  1   1  98   0   0   0|   0     0 |1062k  117M|   0     0 |  14k 6198 
  1   1  98   0   0   0|   0  4096B|1155k  117M|   0     0 |  14k 6664 

# 192.168.49.246 发送速度大约是 117M/s
```