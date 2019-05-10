## iperf3 工具使用方法

### 安装

```bash
# 安装
$ wget https://iperf.fr/download/fedora/iperf3-3.1.3-1.fc24.x86_64.rpm
$ rpm -ivh iperf3-3.1.3-1.fc24.x86_64.rpm 
$ rpm -qa | grep iperf
iperf3-3.1.3-1.fc24.x86_64
$ rpm -ql iperf3-3.1.3-1.fc24.x86_64
/usr/bin/iperf3
/usr/lib64/libiperf.so.0
/usr/lib64/libiperf.so.0.0.0
/usr/share/doc/iperf3
/usr/share/doc/iperf3/LICENSE
/usr/share/doc/iperf3/README.md
/usr/share/doc/iperf3/RELEASE_NOTES
/usr/share/man/man1/iperf3.1.gz
/usr/share/man/man3/libiperf.3.gz
```

### iperf3 使用方法

```bash
# iperf3 使用方法
$ iperf3 -h
Usage: iperf [-s|-c host] [options]
       iperf [-h|--help] [-v|--version]

# iperf 采用 client/server 模式

Server or Client:  # 服务端和客户端都可以使用的选项
  -p, --port      #         server port to listen on/connect to  # 设置客户端和服务端的端口
  -f, --format    [kmgKMG]  format to report: Kbits, Mbits, KBytes, MBytes  # 设置格式，格式化带宽数输出
  -i, --interval  #         seconds between periodic bandwidth reports  # 设置每次报告之间的时间间隔，单位为秒。如果设置为非零值，就会按照此时间间隔输出测试报告。默认值为零。
  -F, --file name           xmit/recv the specified file  # xmit / recv 指定的文件
  -A, --affinity n/n,m      set CPU affinity  # 设置 CPU 亲和性
  -B, --bind      <host>    bind to a specific interface  # 绑定到主机的多个地址中的一个。对于客户端来说，这个参数设置了出栈接口。对于服务器端来说，这个参数设置入栈接口。这个参数只用于具有多网络接口的主机。在 Iperf 的 UDP 模式下，此参数用于绑定和加入一个多播组。使用范围在224.0.0.0 至 239.255.255.255 的多播地址。
  -V, --verbose             more detailed output  # 更多的输出
  -J, --json                output in JSON format  # 输出为 json 格式
  --logfile f               send output to a log file  # 输出到指定文件中
  -d, --debug               emit debugging output
  -v, --version             show version information and quit
  -h, --help                show this message and quit
Server specific:
  -s, --server              run in server mode  # 运行服务端
  -D, --daemon              run the server as a daemon
  -I, --pidfile file        write PID file
  -1, --one-off             handle one client connection then exit
Client specific:
  -c, --client    <host>    run in client mode, connecting to <host>  # 运行客户端，指定服务端 IP
  -u, --udp                 use UDP rather than TCP  # 使用 UDP 代替 TCP，默认是 TCP
  -b, --bandwidth #[KMG][/#] target bandwidth in bits/sec (0 for unlimited)
                            (default 1 Mbit/sec for UDP, unlimited for TCP)
                            (optional slash and packet count for burst mode)
  -t, --time      #         time in seconds to transmit for (default 10 secs)
  -n, --bytes     #[KMG]    number of bytes to transmit (instead of -t)
  -k, --blockcount #[KMG]   number of blocks (packets) to transmit (instead of -t or -n)
  -l, --len       #[KMG]    length of buffer to read or write  # 设置读写缓冲区的长度。
                            (default 128 KB for TCP, 8 KB for UDP)
  --cport         <port>    bind to a specific client port (TCP and UDP, default: ephemeral port)
  -P, --parallel  #         number of parallel client streams to run  # 客户端并行运行的连接数
  -R, --reverse             run in reverse mode (server sends, client receives)  # 默认 iperf3 使用上传模式：Client 负责发送数据，Server 负责接收。如果需要测试下载速度，则使用 -R 参数 Client 负责接收数据，Server 负责发送数据。
  -w, --window    #[KMG]    set window size / socket buffer size  # 设置套接字缓冲区为指定大小。对于 TCP 方式，此设置为 TCP 窗口大小。对于 UDP 方式，此设置为接受 UDP 数据包的缓冲区大小，限制可以接受数据包的最大值。
  -C, --congestion <algo>   set TCP congestion control algorithm (Linux and FreeBSD only)
  -M, --set-mss   #         set TCP/SCTP maximum segment size (MTU - 40 bytes)  # 通过 TCP_MAXSEG 选项尝试设置 TCP 最大信息段的值。MSS 值的大小通常是 TCP/IP 头减去40字节。在以太网中，MSS 值为 1460 字节（MTU 1500 字节）
  -N, --no-delay            set TCP/SCTP no delay, disabling Nagle's Algorithm  # 设置 TCP 无延迟选项，禁用 Nagle's 算法。通常情况此选项对于交互程序，例如 telnet，是禁用的。
  -4, --version4            only use IPv4
  -6, --version6            only use IPv6
  -S, --tos N               set the IP 'type of service'
  -L, --flowlabel N         set the IPv6 flow label (only supported on Linux)
  -Z, --zerocopy            use a 'zero copy' method of sending data
  -O, --omit N              omit the first n seconds
  -T, --title str           prefix every output line with this string
  --get-server-output       get results from server
  --udp-counters-64bit      use 64-bit counters in UDP test packets
  --no-fq-socket-pacing     disable fair-queuing based socket pacing
                            (Linux only)

[KMG] indicates options that support a K/M/G suffix for kilo-, mega-, or giga-

iperf3 homepage at: http://software.es.net/iperf/
Report bugs to:     https://github.com/esnet/iperf
$
```

### iperf3 使用示例和输出说明

```bash
# 默认测试
[root@wh-libinghua work]# iperf3 -s
-----------------------------------------------------------
Server listening on 5201
-----------------------------------------------------------
Accepted connection from 10.5.106.252, port 46460
[  5] local 10.5.106.253 port 5201 connected to 10.5.106.252 port 46462
[ ID] Interval           Transfer     Bandwidth  # Interval 表示时间间隔。Transfer 表示时间间隔里面转输的数据量。Bandwidth 是时间间隔里的传输速率。
[  5]   0.00-1.00   sec   347 MBytes  2.91 Gbits/sec                  
[  5]   1.00-2.00   sec   334 MBytes  2.80 Gbits/sec                  
[  5]   2.00-3.00   sec   304 MBytes  2.55 Gbits/sec                  
[  5]   3.00-4.00   sec   331 MBytes  2.78 Gbits/sec                  
[  5]   4.00-5.00   sec   358 MBytes  3.01 Gbits/sec                  
[  5]   5.00-6.00   sec   367 MBytes  3.08 Gbits/sec                  
[  5]   6.00-7.00   sec   328 MBytes  2.75 Gbits/sec                  
[  5]   7.00-8.00   sec   356 MBytes  2.99 Gbits/sec                  
[  5]   8.00-9.00   sec   348 MBytes  2.92 Gbits/sec                  
[  5]   9.00-10.00  sec   360 MBytes  3.02 Gbits/sec                  
[  5]  10.00-10.04  sec  12.2 MBytes  2.79 Gbits/sec                  
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bandwidth
[  5]   0.00-10.04  sec  0.00 Bytes  0.00 bits/sec                  sender  # 本次测试的发送数据量统计。
[  5]   0.00-10.04  sec  3.36 GBytes  2.88 Gbits/sec                  receiver  # 本次测试的接收数据量统计。
-----------------------------------------------------------
Server listening on 5201
-----------------------------------------------------------


[root@localhost work]# iperf3 -c 10.5.106.253
Connecting to host 10.5.106.253, port 5201
[  4] local 10.5.106.252 port 46462 connected to 10.5.106.253 port 5201
[ ID] Interval           Transfer     Bandwidth       Retr  Cwnd  # Interval 表示时间间隔。Transfer 表示时间间隔里面转输的数据量。Bandwidth 是时间间隔里的传输速率。时间间隔内出现报文重传的次数。时间间隔内拥塞窗口（Congestion Window）大小。
[  4]   0.00-1.00   sec   363 MBytes  3.04 Gbits/sec  765    182 KBytes       
[  4]   1.00-2.00   sec   331 MBytes  2.78 Gbits/sec  675    189 KBytes       
[  4]   2.00-3.00   sec   306 MBytes  2.56 Gbits/sec  630    232 KBytes       
[  4]   3.00-4.00   sec   332 MBytes  2.78 Gbits/sec  720    170 KBytes       
[  4]   4.00-5.00   sec   357 MBytes  2.99 Gbits/sec  810    182 KBytes       
[  4]   5.00-6.00   sec   370 MBytes  3.11 Gbits/sec  855    216 KBytes       
[  4]   6.00-7.00   sec   319 MBytes  2.67 Gbits/sec  675    192 KBytes       
[  4]   7.00-8.00   sec   363 MBytes  3.05 Gbits/sec  810    164 KBytes       
[  4]   8.00-9.00   sec   346 MBytes  2.91 Gbits/sec  720    218 KBytes       
[  4]   9.00-10.00  sec   359 MBytes  3.01 Gbits/sec  810    184 KBytes       
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bandwidth       Retr
[  4]   0.00-10.00  sec  3.37 GBytes  2.89 Gbits/sec  7470             sender
[  4]   0.00-10.00  sec  3.36 GBytes  2.89 Gbits/sec                  receiver

iperf Done.
[root@localhost work]# 



# 客户端并行运行测试
[root@wh-libinghua work]# iperf3 -s
-----------------------------------------------------------
Server listening on 5201
-----------------------------------------------------------
Accepted connection from 10.5.106.252, port 46464
[  5] local 10.5.106.253 port 5201 connected to 10.5.106.252 port 46466
[  7] local 10.5.106.253 port 5201 connected to 10.5.106.252 port 46468
[ ID] Interval           Transfer     Bandwidth
[  5]   0.00-1.00   sec   235 MBytes  1.97 Gbits/sec                  
[  7]   0.00-1.00   sec   153 MBytes  1.28 Gbits/sec                  
[SUM]   0.00-1.00   sec   388 MBytes  3.26 Gbits/sec                  
- - - - - - - - - - - - - - - - - - - - - - - - -
[  5]   1.00-2.00   sec   248 MBytes  2.08 Gbits/sec                  
[  7]   1.00-2.00   sec   193 MBytes  1.62 Gbits/sec                  
[SUM]   1.00-2.00   sec   441 MBytes  3.70 Gbits/sec                  
- - - - - - - - - - - - - - - - - - - - - - - - -
[  5]   2.00-3.00   sec   221 MBytes  1.86 Gbits/sec                  
[  7]   2.00-3.00   sec   161 MBytes  1.36 Gbits/sec                  
[SUM]   2.00-3.00   sec   383 MBytes  3.21 Gbits/sec                  
- - - - - - - - - - - - - - - - - - - - - - - - -
[  5]   3.00-4.00   sec   247 MBytes  2.08 Gbits/sec                  
[  7]   3.00-4.00   sec   171 MBytes  1.43 Gbits/sec                  
[SUM]   3.00-4.00   sec   418 MBytes  3.51 Gbits/sec                  
- - - - - - - - - - - - - - - - - - - - - - - - -
[  5]   4.00-5.00   sec   246 MBytes  2.06 Gbits/sec                  
[  7]   4.00-5.00   sec   150 MBytes  1.26 Gbits/sec                  
[SUM]   4.00-5.00   sec   396 MBytes  3.32 Gbits/sec                  
- - - - - - - - - - - - - - - - - - - - - - - - -
[  5]   5.00-6.00   sec   222 MBytes  1.86 Gbits/sec                  
[  7]   5.00-6.00   sec   204 MBytes  1.71 Gbits/sec                  
[SUM]   5.00-6.00   sec   427 MBytes  3.58 Gbits/sec                  
- - - - - - - - - - - - - - - - - - - - - - - - -
[  5]   6.00-7.00   sec   255 MBytes  2.14 Gbits/sec                  
[  7]   6.00-7.00   sec   149 MBytes  1.25 Gbits/sec                  
[SUM]   6.00-7.00   sec   404 MBytes  3.39 Gbits/sec                  
- - - - - - - - - - - - - - - - - - - - - - - - -
[  5]   7.00-8.00   sec   258 MBytes  2.16 Gbits/sec                  
[  7]   7.00-8.00   sec   136 MBytes  1.14 Gbits/sec                  
[SUM]   7.00-8.00   sec   394 MBytes  3.30 Gbits/sec                  
- - - - - - - - - - - - - - - - - - - - - - - - -
[  5]   8.00-9.00   sec   262 MBytes  2.20 Gbits/sec                  
[  7]   8.00-9.00   sec   132 MBytes  1.10 Gbits/sec                  
[SUM]   8.00-9.00   sec   394 MBytes  3.30 Gbits/sec                  
- - - - - - - - - - - - - - - - - - - - - - - - -
[  5]   9.00-10.00  sec   213 MBytes  1.79 Gbits/sec                  
[  7]   9.00-10.00  sec   173 MBytes  1.45 Gbits/sec                  
[SUM]   9.00-10.00  sec   386 MBytes  3.24 Gbits/sec                  
- - - - - - - - - - - - - - - - - - - - - - - - -
[  5]  10.00-10.03  sec  10.6 MBytes  2.62 Gbits/sec                  
[  7]  10.00-10.03  sec  2.63 MBytes   648 Mbits/sec                  
[SUM]  10.00-10.03  sec  13.3 MBytes  3.27 Gbits/sec                  
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bandwidth
[  5]   0.00-10.03  sec  0.00 Bytes  0.00 bits/sec                  sender
[  5]   0.00-10.03  sec  2.36 GBytes  2.02 Gbits/sec                  receiver
[  7]   0.00-10.03  sec  0.00 Bytes  0.00 bits/sec                  sender
[  7]   0.00-10.03  sec  1.59 GBytes  1.36 Gbits/sec                  receiver
[SUM]   0.00-10.03  sec  0.00 Bytes  0.00 bits/sec                  sender
[SUM]   0.00-10.03  sec  3.95 GBytes  3.38 Gbits/sec                  receiver
-----------------------------------------------------------
Server listening on 5201
-----------------------------------------------------------


[root@localhost work]# iperf3 -c 10.5.106.253 -P 2
Connecting to host 10.5.106.253, port 5201
[  4] local 10.5.106.252 port 46466 connected to 10.5.106.253 port 5201
[  6] local 10.5.106.252 port 46468 connected to 10.5.106.253 port 5201
[ ID] Interval           Transfer     Bandwidth       Retr  Cwnd
[  4]   0.00-1.00   sec   245 MBytes  2.06 Gbits/sec  748    156 KBytes       
[  6]   0.00-1.00   sec   159 MBytes  1.33 Gbits/sec  778   91.9 KBytes       
[SUM]   0.00-1.00   sec   404 MBytes  3.39 Gbits/sec  1526             
- - - - - - - - - - - - - - - - - - - - - - - - -
[  4]   1.00-2.00   sec   246 MBytes  2.07 Gbits/sec  734    180 KBytes       
[  6]   1.00-2.00   sec   196 MBytes  1.64 Gbits/sec  899    113 KBytes       
[SUM]   1.00-2.00   sec   442 MBytes  3.71 Gbits/sec  1633             
- - - - - - - - - - - - - - - - - - - - - - - - -
[  4]   2.00-3.00   sec   223 MBytes  1.87 Gbits/sec  619    204 KBytes       
[  6]   2.00-3.00   sec   159 MBytes  1.34 Gbits/sec  809   52.3 KBytes       
[SUM]   2.00-3.00   sec   383 MBytes  3.21 Gbits/sec  1428             
- - - - - - - - - - - - - - - - - - - - - - - - -
[  4]   3.00-4.00   sec   240 MBytes  2.02 Gbits/sec  721   62.2 KBytes       
[  6]   3.00-4.00   sec   171 MBytes  1.44 Gbits/sec  721    225 KBytes       
[SUM]   3.00-4.00   sec   412 MBytes  3.46 Gbits/sec  1442             
- - - - - - - - - - - - - - - - - - - - - - - - -
[  4]   4.00-5.00   sec   250 MBytes  2.10 Gbits/sec  610    147 KBytes       
[  6]   4.00-5.00   sec   151 MBytes  1.27 Gbits/sec  809   96.2 KBytes       
[SUM]   4.00-5.00   sec   401 MBytes  3.37 Gbits/sec  1419             
- - - - - - - - - - - - - - - - - - - - - - - - -
[  4]   5.00-6.00   sec   224 MBytes  1.88 Gbits/sec  773    165 KBytes       
[  6]   5.00-6.00   sec   205 MBytes  1.72 Gbits/sec  858   96.2 KBytes       
[SUM]   5.00-6.00   sec   429 MBytes  3.60 Gbits/sec  1631             
- - - - - - - - - - - - - - - - - - - - - - - - -
[  4]   6.00-7.00   sec   254 MBytes  2.13 Gbits/sec  615    148 KBytes       
[  6]   6.00-7.00   sec   147 MBytes  1.23 Gbits/sec  780   91.9 KBytes       
[SUM]   6.00-7.00   sec   401 MBytes  3.36 Gbits/sec  1395             
- - - - - - - - - - - - - - - - - - - - - - - - -
[  4]   7.00-8.00   sec   264 MBytes  2.21 Gbits/sec  732    230 KBytes       
[  6]   7.00-8.00   sec   131 MBytes  1.10 Gbits/sec  690   41.0 KBytes       
[SUM]   7.00-8.00   sec   394 MBytes  3.31 Gbits/sec  1422             
- - - - - - - - - - - - - - - - - - - - - - - - -
[  4]   8.00-9.00   sec   256 MBytes  2.15 Gbits/sec  774   94.7 KBytes       
[  6]   8.00-9.00   sec   139 MBytes  1.17 Gbits/sec  779    160 KBytes       
[SUM]   8.00-9.00   sec   395 MBytes  3.32 Gbits/sec  1553             
- - - - - - - - - - - - - - - - - - - - - - - - -
[  4]   9.00-10.00  sec   218 MBytes  1.83 Gbits/sec  624    174 KBytes       
[  6]   9.00-10.00  sec   168 MBytes  1.41 Gbits/sec  821   55.1 KBytes       
[SUM]   9.00-10.00  sec   386 MBytes  3.23 Gbits/sec  1445             
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bandwidth       Retr
[  4]   0.00-10.00  sec  2.36 GBytes  2.03 Gbits/sec  6950             sender
[  4]   0.00-10.00  sec  2.36 GBytes  2.03 Gbits/sec                  receiver
[  6]   0.00-10.00  sec  1.59 GBytes  1.36 Gbits/sec  7944             sender
[  6]   0.00-10.00  sec  1.59 GBytes  1.36 Gbits/sec                  receiver
[SUM]   0.00-10.00  sec  3.95 GBytes  3.39 Gbits/sec  14894             sender
[SUM]   0.00-10.00  sec  3.95 GBytes  3.39 Gbits/sec                  receiver

iperf Done.
[root@localhost work]# 

```
