
# tun/tap

tun/tap 设备最常用的场景是 VPN，包括 tunnel 以及应用层的 IPSec 等

```

+----------------------------------------------------------------+
|                                                                |
|  +--------------------+      +--------------------+            |
|  | User Application A |      | User Application B |<-----+     |
|  +--------------------+      +--------------------+      |     |
|               | 1                    | 5                 |     |
|...............|......................|...................|.....|
|               ↓                      ↓                   |     |
|         +----------+           +----------+              |     |
|         | socket A |           | socket B |              |     |
|         +----------+           +----------+              |     |
|                 | 2               | 6                    |     |
|.................|.................|......................|.....|
|                 ↓                 ↓                      |     |
|             +------------------------+                 4 |     |
|             | Newwork Protocol Stack |                   |     |
|             +------------------------+                   |     |
|                | 7                 | 3                   |     |
|................|...................|.....................|.....|
|                ↓                   ↓                     |     |
|        +----------------+    +----------------+          |     |
|        |      eth0      |    |      tun0      |          |     |
|        +----------------+    +----------------+          |     |
|    10.32.0.11  |                   |   192.168.3.11      |     |
|                | 8                 +---------------------+     |
|                |                                               |
+----------------|-----------------------------------------------+
                 ↓
         Physical Network

# ip tuntap help
Usage: ip tuntap { add | del } [ dev PHYS_DEV ] 
          [ mode { tun | tap } ] [ user USER ] [ group GROUP ]
          [ one_queue ] [ pi ] [ vnet_hdr ]

Where: USER  := { STRING | NUMBER }
       GROUP := { STRING | NUMBER }

ip tuntap add dev tun0 mode 

```

如图所示：
* 当一个 TUN 设备被创建时，在 Linux 设备文件目录下将会生成一个对应 char 设备，用户程序可以像打开普通文件一样打开这个文件进行读写。
* 当执行 write() 操作时，数据进入 TUN 设备，此时对于 Linux 网络层来说，相当于 TUN 设备收到了一包数据，请求内核接受它，如同普通的物理网卡从外界收到一包数据一样，不同的是其实数据来自 Linux 上的一个用户程序。Linux 收到此数据后将根据**网络配置**进行后续处理，从而完成了用户程序向 Linux 内核网络层注入数据的功能。
* 当用户程序执行 read() 请求时，相当于向内核查询 TUN 设备上是否有需要被发送出去的数据，有的话取出到用户程序里，完成 TUN 设备的发送数据功能。
* 针对 TUN 设备的一个形象的比喻是：使用 TUN 设备的应用程序相当于另外一台计算机，TUN 设备是本机的一个网卡，他们之间相互连接。应用程序通过 read()/write()操作，和本机网络核心进行通讯。

note:
1. 创建 TUN 设备，相当于 fd = touch()
2. User Application A 调用 write(fd) 写入数据
3. Newwork Protocol Stack 发现有新的数据写入
4. Newwork Protocol Stack 查找路由表，确定该数据交由 TUN 设备处理
5. TUN 设备缓存数据，等待 User Application B 进行 read() 调用

因为给 tun0 设备设置 IP（192.168.3.11）后会新增一条 192.168.3.0/24 网段，接口是 tun0 的路由信息，所以当 Newwork Protocol Stack 接收或者发送数据时都会查找路由表，当匹配 192.168.3.0/24 网段时，会将数据交给 tun0 设备处理。例如 **ping 192.168.3.12**，此时 Newwork Protocol Stack 会将 ICMP 包交给 tun0 设备处理，但此时 tun0 设备无法处理。而当 **ping 192.168.3.11** 时，Newwork Protocol Stack 会将 ICMP 包交给 lo 设备处理，这也是与想象中的不一样。

Newwork Protocol Stack 功能
* 根据目的 IP 查找路由表，找到应该由哪个设备处理数据包
* 根据需要和目的 IP 发送 ARP 数据包
* 将数据交给上层的应用处理

## 实践

1. 创建 tun0 设备后需要检查该设备是否有 MAC 地址，因为二层的 ARP 协议需要使用到 MAC 地址
2. 创建 tun0 设备后需要为 tun0 设置 IP 地址，否则 tun0 无法连接到 Newwork Protocol Stack，也就不能使用路由表等功能

``` bash
# 创建 tun0 设备前的 route、IP、link
[root@huzhi-code ~]# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         10.0.1.1        0.0.0.0         UG    100    0        0 ens192
10.0.1.1        0.0.0.0         255.255.255.255 UH    100    0        0 ens192
10.0.8.0        0.0.0.0         255.255.255.0   U     100    0        0 ens192
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
[root@huzhi-code ~]#
[root@huzhi-code ~]# ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT qlen 1000
    link/ether 00:50:56:9b:35:0e brd ff:ff:ff:ff:ff:ff
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT
    link/ether 02:42:cf:09:1c:03 brd ff:ff:ff:ff:ff:ff
[root@huzhi-code ~]#
[root@huzhi-code ~]# ip address show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP qlen 1000
    link/ether 00:50:56:9b:35:0e brd ff:ff:ff:ff:ff:ff
    inet 10.0.8.10/24 brd 10.0.8.255 scope global ens192
       valid_lft forever preferred_lft forever
    inet6 fe80::98e0:1851:d89b:6fae/64 scope link tentative dadfailed
       valid_lft forever preferred_lft forever
    inet6 fe80::9d85:ff3a:61fc:fb77/64 scope link tentative dadfailed
       valid_lft forever preferred_lft forever
    inet6 fe80::f109:5dec:37bb:2842/64 scope link tentative dadfailed
       valid_lft forever preferred_lft forever
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN
    link/ether 02:42:cf:09:1c:03 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
       valid_lft forever preferred_lft forever
[root@huzhi-code ~]#

# 创建 tun0 设备
[root@huzhi-code ~]# ip tuntap add dev tun0 mode tun
[root@huzhi-code ~]# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         10.0.1.1        0.0.0.0         UG    100    0        0 ens192
10.0.1.1        0.0.0.0         255.255.255.255 UH    100    0        0 ens192
10.0.8.0        0.0.0.0         255.255.255.0   U     100    0        0 ens192
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
[root@huzhi-code ~]# ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT qlen 1000
    link/ether 00:50:56:9b:35:0e brd ff:ff:ff:ff:ff:ff
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT
    link/ether 02:42:cf:09:1c:03 brd ff:ff:ff:ff:ff:ff
6: tun0: <POINTOPOINT,MULTICAST,NOARP> mtu 1500 qdisc noop state DOWN mode DEFAULT qlen 500
    link/none
[root@huzhi-code ~]# ip address show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP qlen 1000
    link/ether 00:50:56:9b:35:0e brd ff:ff:ff:ff:ff:ff
    inet 10.0.8.10/24 brd 10.0.8.255 scope global ens192
       valid_lft forever preferred_lft forever
    inet6 fe80::98e0:1851:d89b:6fae/64 scope link tentative dadfailed
       valid_lft forever preferred_lft forever
    inet6 fe80::9d85:ff3a:61fc:fb77/64 scope link tentative dadfailed
       valid_lft forever preferred_lft forever
    inet6 fe80::f109:5dec:37bb:2842/64 scope link tentative dadfailed
       valid_lft forever preferred_lft forever
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN
    link/ether 02:42:cf:09:1c:03 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
       valid_lft forever preferred_lft forever
6: tun0: <POINTOPOINT,MULTICAST,NOARP> mtu 1500 qdisc noop state DOWN qlen 500
    link/none
[root@huzhi-code ~]#

# 为 tun0 设置 IP
[root@huzhi-code ~]# ip addr add 192.168.3.11/24 dev tun0
[root@huzhi-code ~]# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         10.0.1.1        0.0.0.0         UG    100    0        0 ens192
10.0.1.1        0.0.0.0         255.255.255.255 UH    100    0        0 ens192
10.0.8.0        0.0.0.0         255.255.255.0   U     100    0        0 ens192
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
[root@huzhi-code ~]# ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT qlen 1000
    link/ether 00:50:56:9b:35:0e brd ff:ff:ff:ff:ff:ff
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT
    link/ether 02:42:cf:09:1c:03 brd ff:ff:ff:ff:ff:ff
6: tun0: <POINTOPOINT,MULTICAST,NOARP> mtu 1500 qdisc noop state DOWN mode DEFAULT qlen 500
    link/none
[root@huzhi-code ~]# ip address show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP qlen 1000
    link/ether 00:50:56:9b:35:0e brd ff:ff:ff:ff:ff:ff
    inet 10.0.8.10/24 brd 10.0.8.255 scope global ens192
       valid_lft forever preferred_lft forever
    inet6 fe80::98e0:1851:d89b:6fae/64 scope link tentative dadfailed
       valid_lft forever preferred_lft forever
    inet6 fe80::9d85:ff3a:61fc:fb77/64 scope link tentative dadfailed
       valid_lft forever preferred_lft forever
    inet6 fe80::f109:5dec:37bb:2842/64 scope link tentative dadfailed
       valid_lft forever preferred_lft forever
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN
    link/ether 02:42:cf:09:1c:03 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
       valid_lft forever preferred_lft forever
6: tun0: <POINTOPOINT,MULTICAST,NOARP> mtu 1500 qdisc noop state DOWN qlen 500
    link/none
    inet 192.168.3.11/24 scope global tun0
       valid_lft forever preferred_lft forever
[root@huzhi-code ~]#

# 启动 tun0
[root@huzhi-code ~]# ip link set tun0 up
[root@huzhi-code ~]# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         10.0.1.1        0.0.0.0         UG    100    0        0 ens192
10.0.1.1        0.0.0.0         255.255.255.255 UH    100    0        0 ens192
10.0.8.0        0.0.0.0         255.255.255.0   U     100    0        0 ens192
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
192.168.3.0     0.0.0.0         255.255.255.0   U     0      0        0 tun0
[root@huzhi-code ~]# ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT qlen 1000
    link/ether 00:50:56:9b:35:0e brd ff:ff:ff:ff:ff:ff
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT
    link/ether 02:42:cf:09:1c:03 brd ff:ff:ff:ff:ff:ff
6: tun0: <NO-CARRIER,POINTOPOINT,MULTICAST,NOARP,UP> mtu 1500 qdisc pfifo_fast state DOWN mode DEFAULT qlen 500
    link/none
[root@huzhi-code ~]# ip address show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP qlen 1000
    link/ether 00:50:56:9b:35:0e brd ff:ff:ff:ff:ff:ff
    inet 10.0.8.10/24 brd 10.0.8.255 scope global ens192
       valid_lft forever preferred_lft forever
    inet6 fe80::98e0:1851:d89b:6fae/64 scope link tentative dadfailed
       valid_lft forever preferred_lft forever
    inet6 fe80::9d85:ff3a:61fc:fb77/64 scope link tentative dadfailed
       valid_lft forever preferred_lft forever
    inet6 fe80::f109:5dec:37bb:2842/64 scope link tentative dadfailed
       valid_lft forever preferred_lft forever
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN
    link/ether 02:42:cf:09:1c:03 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
       valid_lft forever preferred_lft forever
6: tun0: <NO-CARRIER,POINTOPOINT,MULTICAST,NOARP,UP> mtu 1500 qdisc pfifo_fast state DOWN qlen 500
    link/none
    inet 192.168.3.11/24 scope global tun0
       valid_lft forever preferred_lft forever
[root@huzhi-code ~]#

# 测试连通性
[root@huzhi-code ~]# ping -c 4 192.168.3.11
PING 192.168.3.11 (192.168.3.11) 56(84) bytes of data.
64 bytes from 192.168.3.11: icmp_seq=1 ttl=64 time=0.044 ms
64 bytes from 192.168.3.11: icmp_seq=2 ttl=64 time=0.058 ms
64 bytes from 192.168.3.11: icmp_seq=3 ttl=64 time=0.062 ms
64 bytes from 192.168.3.11: icmp_seq=4 ttl=64 time=0.061 ms

--- 192.168.3.11 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 2999ms
rtt min/avg/max/mdev = 0.044/0.056/0.062/0.009 ms
[root@huzhi-code ~]#
[root@huzhi-code ~]# ping -c 4 192.168.3.12
PING 192.168.3.12 (192.168.3.12) 56(84) bytes of data.

--- 192.168.3.12 ping statistics ---
4 packets transmitted, 0 received, 100% packet loss, time 2999ms

[root@huzhi-code ~]#
[root@huzhi-code ~]# ping -c 4 192.168.3.1
PING 192.168.3.1 (192.168.3.1) 56(84) bytes of data.

--- 192.168.3.1 ping statistics ---
4 packets transmitted, 0 received, 100% packet loss, time 3015ms

[root@huzhi-code ~]#


# 测试不同的 IP 选择的路由
[root@huzhi-code ~]# ip route get 192.168.3.11
local 192.168.3.11 dev lo  src 192.168.3.11
    cache <local>
[root@huzhi-code ~]#
[root@huzhi-code ~]# ip route get 192.168.3.12
192.168.3.12 dev tun0  src 192.168.3.11
    cache
[root@huzhi-code ~]#
[root@huzhi-code ~]# ip route get 192.168.3.1
192.168.3.1 dev tun0  src 192.168.3.11
    cache
[root@huzhi-code ~]#


```

结论：
由于 tun0 的 ip 地址是 192.168.3.11，所以 `ping -c 4 192.168.3.11` 走的是 lo 接口。
而 `ping -c 4 192.168.3.11` 和 `ping -c 4 192.168.3.11` 会走 tun0 接口。


```bash
# ping 192.168.3.11 的同时在 lo 接口上抓包
[root@huzhi-code ~]# ping -c 4 192.168.3.11
PING 192.168.3.11 (192.168.3.11) 56(84) bytes of data.
64 bytes from 192.168.3.11: icmp_seq=1 ttl=64 time=0.051 ms
64 bytes from 192.168.3.11: icmp_seq=2 ttl=64 time=0.051 ms
64 bytes from 192.168.3.11: icmp_seq=3 ttl=64 time=0.045 ms
64 bytes from 192.168.3.11: icmp_seq=4 ttl=64 time=0.041 ms

--- 192.168.3.11 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 2999ms
rtt min/avg/max/mdev = 0.041/0.047/0.051/0.004 ms
[root@huzhi-code ~]#

[root@huzhi-code ~]# tcpdump -n icmp -i lo
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on lo, link-type EN10MB (Ethernet), capture size 262144 bytes
14:16:42.087617 IP 192.168.3.11 > 192.168.3.11: ICMP echo request, id 15962, seq 1, length 64
14:16:42.087633 IP 192.168.3.11 > 192.168.3.11: ICMP echo reply, id 15962, seq 1, length 64
14:16:43.086901 IP 192.168.3.11 > 192.168.3.11: ICMP echo request, id 15962, seq 2, length 64
14:16:43.086921 IP 192.168.3.11 > 192.168.3.11: ICMP echo reply, id 15962, seq 2, length 64
14:16:44.086963 IP 192.168.3.11 > 192.168.3.11: ICMP echo request, id 15962, seq 3, length 64
14:16:44.086989 IP 192.168.3.11 > 192.168.3.11: ICMP echo reply, id 15962, seq 3, length 64
14:16:45.086893 IP 192.168.3.11 > 192.168.3.11: ICMP echo request, id 15962, seq 4, length 64
14:16:45.086912 IP 192.168.3.11 > 192.168.3.11: ICMP echo reply, id 15962, seq 4, length 64


# ping 192.168.3.12 和 192.168.3.1 的同时在 tun0 接口上抓包
[root@huzhi-code ~]# ping -c 4 192.168.3.12
PING 192.168.3.12 (192.168.3.12) 56(84) bytes of data.

--- 192.168.3.12 ping statistics ---
4 packets transmitted, 0 received, 100% packet loss, time 2999ms

[root@huzhi-code ~]#
[root@huzhi-code ~]# ping -c 4 192.168.3.1
PING 192.168.3.1 (192.168.3.1) 56(84) bytes of data.

--- 192.168.3.1 ping statistics ---
4 packets transmitted, 0 received, 100% packet loss, time 2999ms

[root@huzhi-code ~]#


[root@huzhi-code ~]# tcpdump -i tun0
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on tun0, link-type RAW (Raw IP), capture size 262144 bytes

因为 tun0 接口收到数据包后没有上层的应用处理数据包，所以是 ping 不通的，并且不能抓包。

```

[参考](https://segmentfault.com/a/1190000009249039)
