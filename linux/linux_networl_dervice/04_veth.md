# veth

## veth设备的特点

* veth 和其它的网络设备都一样，一端连接的是内核协议栈。
* veth 设备是成对出现的，另一端两个设备彼此相连
* 一个设备收到协议栈的数据发送请求后，会将数据发送到另一个设备上去。

veth设备的特点如下图所示：

```

+----------------------------------------------------------------+
|                                                                |
|       +------------------------------------------------+       |
|       |             Newwork Protocol Stack             |       |
|       +------------------------------------------------+       |
|              ↑               ↑               ↑                 |
|..............|...............|...............|.................|
|              ↓               ↓               ↓                 |
|        +----------+    +-----------+   +-----------+           |
|        |   eth0   |    |   veth0   |   |   veth1   |           |
|        +----------+    +-----------+   +-----------+           |
|192.168.1.11  ↑               ↑               ↑                 |
|              |               +---------------+                 |
|              |         192.168.2.11     192.168.2.12           |
+--------------|-------------------------------------------------+
               ↓
         Physical Network

```

Newwork Protocol Stack 功能
* 根据目的 IP 查找路由表，找到应该由哪个设备处理数据包
* 根据需要和目的 IP 发送 ARP 数据包
* 将数据交给上层的应用处理


## 示例

```bash
#########################################################
# 创建 veth0 和 veth1 设备对之前的 link、route、address
[root@huzhi-code ~]# ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT qlen 1000
    link/ether 00:50:56:9b:35:0e brd ff:ff:ff:ff:ff:ff
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT
    link/ether 02:42:cf:09:1c:03 brd ff:ff:ff:ff:ff:ff
[root@huzhi-code ~]# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         10.0.1.1        0.0.0.0         UG    100    0        0 ens192
10.0.1.1        0.0.0.0         255.255.255.255 UH    100    0        0 ens192
10.0.8.0        0.0.0.0         255.255.255.0   U     100    0        0 ens192
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
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

ip link add DEVICE type { veth | vxcan } [ peer name NAME ]

#########################################################
# 创建 veth0 和 veth1 设备对，影响 link
[root@huzhi-code ~]# ip link add veth0 type veth peer name veth1
[root@huzhi-code ~]# ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT qlen 1000
    link/ether 00:50:56:9b:35:0e brd ff:ff:ff:ff:ff:ff
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT
    link/ether 02:42:cf:09:1c:03 brd ff:ff:ff:ff:ff:ff
7: veth1@veth0: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 qdisc noop state DOWN mode DEFAULT qlen 1000
    link/ether 46:27:49:49:15:57 brd ff:ff:ff:ff:ff:ff
8: veth0@veth1: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 qdisc noop state DOWN mode DEFAULT qlen 1000
    link/ether 7e:08:71:f8:c8:1a brd ff:ff:ff:ff:ff:ff

#########################################################
# 为 veth0 设置 ip
[root@huzhi-code ~]# ip addr add 192.168.2.11/24 dev veth0
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
7: veth1@veth0: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 qdisc noop state DOWN qlen 1000
    link/ether 46:27:49:49:15:57 brd ff:ff:ff:ff:ff:ff
8: veth0@veth1: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 qdisc noop state DOWN qlen 1000
    link/ether 7e:08:71:f8:c8:1a brd ff:ff:ff:ff:ff:ff
    inet 192.168.2.11/24 scope global veth0
       valid_lft forever preferred_lft forever

#########################################################
# 启动 veth0 和 veth1
[root@huzhi-code ~]# ip link set veth0 up
[root@huzhi-code ~]# ip link set veth1 up
[root@huzhi-code ~]# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         10.0.1.1        0.0.0.0         UG    100    0        0 ens192
10.0.1.1        0.0.0.0         255.255.255.255 UH    100    0        0 ens192
10.0.8.0        0.0.0.0         255.255.255.0   U     100    0        0 ens192
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
192.168.2.0     0.0.0.0         255.255.255.0   U     0      0        0 veth0

#########################################################

[root@huzhi-code ~]# ip route get 192.168.2.11
local 192.168.2.11 dev lo  src 192.168.2.11
    cache <local>
[root@huzhi-code ~]#
[root@huzhi-code ~]# ip route get 192.168.2.12
192.168.2.12 dev veth0  src 192.168.2.11
    cache
[root@huzhi-code ~]#
[root@huzhi-code ~]# ip route get 192.168.2.1
192.168.2.1 dev veth0  src 192.168.2.11
    cache
[root@huzhi-code ~]#

#########################################################

[root@huzhi-code ~]# ping -c 4 192.168.2.11
PING 192.168.2.11 (192.168.2.11) 56(84) bytes of data.
64 bytes from 192.168.2.11: icmp_seq=1 ttl=64 time=0.066 ms
64 bytes from 192.168.2.11: icmp_seq=2 ttl=64 time=0.049 ms
64 bytes from 192.168.2.11: icmp_seq=3 ttl=64 time=0.052 ms
64 bytes from 192.168.2.11: icmp_seq=4 ttl=64 time=0.048 ms

--- 192.168.2.11 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 2999ms
rtt min/avg/max/mdev = 0.048/0.053/0.066/0.011 ms
[root@huzhi-code ~]#

[root@huzhi-code ~]# tcpdump -i lo -n
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on lo, link-type EN10MB (Ethernet), capture size 262144 bytes
15:00:13.420976 IP 192.168.2.11 > 192.168.2.11: ICMP echo request, id 16120, seq 1, length 64
15:00:13.420994 IP 192.168.2.11 > 192.168.2.11: ICMP echo reply, id 16120, seq 1, length 64
15:00:14.420834 IP 192.168.2.11 > 192.168.2.11: ICMP echo request, id 16120, seq 2, length 64
15:00:14.420847 IP 192.168.2.11 > 192.168.2.11: ICMP echo reply, id 16120, seq 2, length 64
15:00:15.420864 IP 192.168.2.11 > 192.168.2.11: ICMP echo request, id 16120, seq 3, length 64
15:00:15.420878 IP 192.168.2.11 > 192.168.2.11: ICMP echo reply, id 16120, seq 3, length 64
15:00:16.420831 IP 192.168.2.11 > 192.168.2.11: ICMP echo request, id 16120, seq 4, length 64
15:00:16.420845 IP 192.168.2.11 > 192.168.2.11: ICMP echo reply, id 16120, seq 4, length 64

[root@huzhi-code ~]#

[root@huzhi-code ~]# tcpdump -i veth0 -n
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on veth0, link-type EN10MB (Ethernet), capture size 262144 bytes

[root@huzhi-code ~]#

[root@huzhi-code ~]# tcpdump -i veth1 -n
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on veth1, link-type EN10MB (Ethernet), capture size 262144 bytes

[root@huzhi-code ~]#

#########################################################

[root@huzhi-code ~]# ping -c 4 192.168.2.12
PING 192.168.2.12 (192.168.2.12) 56(84) bytes of data.
From 192.168.2.11 icmp_seq=1 Destination Host Unreachable
From 192.168.2.11 icmp_seq=2 Destination Host Unreachable
From 192.168.2.11 icmp_seq=3 Destination Host Unreachable
From 192.168.2.11 icmp_seq=4 Destination Host Unreachable

--- 192.168.2.12 ping statistics ---
4 packets transmitted, 0 received, +4 errors, 100% packet loss, time 2999ms
pipe 4
[root@huzhi-code ~]#

[root@huzhi-code ~]# tcpdump -i veth0 -n
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on veth0, link-type EN10MB (Ethernet), capture size 262144 bytes
15:16:26.857171 ARP, Request who-has 192.168.2.12 tell 192.168.2.11, length 28
15:16:27.858786 ARP, Request who-has 192.168.2.12 tell 192.168.2.11, length 28
15:16:28.860772 ARP, Request who-has 192.168.2.12 tell 192.168.2.11, length 28


[root@huzhi-code ~]# tcpdump -i veth1 -n
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on veth1, link-type EN10MB (Ethernet), capture size 262144 bytes
15:16:26.857179 ARP, Request who-has 192.168.2.12 tell 192.168.2.11, length 28
15:16:27.858796 ARP, Request who-has 192.168.2.12 tell 192.168.2.11, length 28
15:16:28.860779 ARP, Request who-has 192.168.2.12 tell 192.168.2.11, length 28


[root@huzhi-code ~]# tcpdump -i lo -n
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on lo, link-type EN10MB (Ethernet), capture size 262144 bytes
15:16:29.862813 IP 192.168.2.11 > 192.168.2.11: ICMP host 192.168.2.12 unreachable, length 92
15:16:29.862823 IP 192.168.2.11 > 192.168.2.11: ICMP host 192.168.2.12 unreachable, length 92
15:16:29.862828 IP 192.168.2.11 > 192.168.2.11: ICMP host 192.168.2.12 unreachable, length 92
15:16:29.862832 IP 192.168.2.11 > 192.168.2.11: ICMP host 192.168.2.12 unreachable, length 92

```

1. ping 进程构造 ICMP echo 请求包，并通过 socket 发给协议栈
2. 协议栈根据目的 IP 地址和系统路由表，知道去 192.168.2.12 的数据包应该要由 veth0 口出去
3. 由于是第一次访问 192.168.2.12，且目的 IP 和本地 IP 在同一个网段，所以协议栈会先发送 ARP 出去，询问 192.168.2.12 的 mac 地址
4. 协议栈将 ARP 包交给 veth0，让它发出去
5. 由于 veth0 的另一端连的是 veth1，所以 ARP 请求包就转发给了 veth1
6. veth1 收到 ARP 包后，转交给另一端的协议栈
7. 协议栈一看自己的设备列表，发现本地没有 192.168.2.12 这个 IP，于是就丢弃了该 ARP 请求包，这就是为什么只能看到 ARP 请求包，看不到应答包的原因
8. 同时，veth0 收到 ARP 包后，转交给另一端的协议栈，协议栈一看自己的设备列表，发现本地没有 192.168.2.12 这个 IP，于是就丢弃了该 ARP 请求包，这就是为什么只能看到 ARP 请求包，看不到应答包的原因
9. 当协议栈找不到 192.168.2.12 的 MAC 地址时，协议栈会向ICMP包中的原地址（此时是192.168.2.11）发送一个 host unreachable 的响应包，这就是在 lo 接口可以抓到数据的原因，也可以得出结论，ICMP 的响应包都在 lo 接口处理

```bash
[root@huzhi-code ~]# ip addr add 192.168.2.12/24 dev veth1
[root@huzhi-code ~]# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         10.0.1.1        0.0.0.0         UG    100    0        0 ens192
10.0.1.1        0.0.0.0         255.255.255.255 UH    100    0        0 ens192
10.0.8.0        0.0.0.0         255.255.255.0   U     100    0        0 ens192
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
192.168.2.0     0.0.0.0         255.255.255.0   U     0      0        0 veth0
192.168.2.0     0.0.0.0         255.255.255.0   U     0      0        0 veth1
[root@huzhi-code ~]#

[root@huzhi-code ~]# ip route get 192.168.2.11
local 192.168.2.11 dev lo  src 192.168.2.11
    cache <local>
[root@huzhi-code ~]# ip route get 192.168.2.12
local 192.168.2.12 dev lo  src 192.168.2.12
    cache <local>
[root@huzhi-code ~]# ip route get 192.168.2.13
192.168.2.13 dev veth0  src 192.168.2.11
    cache
[root@huzhi-code ~]#


[root@huzhi-code ~]# ping -c 4 192.168.2.12
PING 192.168.2.12 (192.168.2.12) 56(84) bytes of data.
64 bytes from 192.168.2.12: icmp_seq=1 ttl=64 time=0.074 ms
64 bytes from 192.168.2.12: icmp_seq=2 ttl=64 time=0.046 ms
64 bytes from 192.168.2.12: icmp_seq=3 ttl=64 time=0.049 ms
64 bytes from 192.168.2.12: icmp_seq=4 ttl=64 time=0.048 ms

--- 192.168.2.12 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 2999ms
rtt min/avg/max/mdev = 0.046/0.054/0.074/0.012 ms
[root@huzhi-code ~]#

[root@huzhi-code ~]# tcpdump -i lo -n
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on lo, link-type EN10MB (Ethernet), capture size 262144 bytes
19:45:19.786979 IP 192.168.2.12 > 192.168.2.12: ICMP echo request, id 16570, seq 1, length 64
19:45:19.786991 IP 192.168.2.12 > 192.168.2.12: ICMP echo reply, id 16570, seq 1, length 64
19:45:20.786797 IP 192.168.2.12 > 192.168.2.12: ICMP echo request, id 16570, seq 2, length 64
19:45:20.786810 IP 192.168.2.12 > 192.168.2.12: ICMP echo reply, id 16570, seq 2, length 64
19:45:21.786813 IP 192.168.2.12 > 192.168.2.12: ICMP echo request, id 16570, seq 3, length 64
19:45:21.786826 IP 192.168.2.12 > 192.168.2.12: ICMP echo reply, id 16570, seq 3, length 64
19:45:22.786819 IP 192.168.2.12 > 192.168.2.12: ICMP echo request, id 16570, seq 4, length 64
19:45:22.786832 IP 192.168.2.12 > 192.168.2.12: ICMP echo reply, id 16570, seq 4, length 64





[root@huzhi-code ~]# ping -c 4 -I veth0 192.168.2.12
PING 192.168.2.12 (192.168.2.12) from 192.168.2.11 veth0: 56(84) bytes of data.

--- 192.168.2.12 ping statistics ---
4 packets transmitted, 0 received, 100% packet loss, time 2999ms

[root@huzhi-code ~]#

[root@huzhi-code ~]# tcpdump -i veth0 -n
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on veth0, link-type EN10MB (Ethernet), capture size 262144 bytes
19:46:32.304288 ARP, Request who-has 192.168.2.12 tell 192.168.2.11, length 28
19:46:33.304772 ARP, Request who-has 192.168.2.12 tell 192.168.2.11, length 28
19:46:34.306770 ARP, Request who-has 192.168.2.12 tell 192.168.2.11, length 28

[root@huzhi-code ~]# tcpdump -i veth1 -n
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on veth1, link-type EN10MB (Ethernet), capture size 262144 bytes
19:46:32.304298 ARP, Request who-has 192.168.2.12 tell 192.168.2.11, length 28
19:46:33.304778 ARP, Request who-has 192.168.2.12 tell 192.168.2.11, length 28
19:46:34.306776 ARP, Request who-has 192.168.2.12 tell 192.168.2.11, length 28

[root@huzhi-code ~]# tcpdump -i lo -n
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on lo, link-type EN10MB (Ethernet), capture size 262144 bytes
19:46:35.308806 IP 192.168.2.11 > 192.168.2.11: ICMP host 192.168.2.12 unreachable, length 92
19:46:35.308815 IP 192.168.2.11 > 192.168.2.11: ICMP host 192.168.2.12 unreachable, length 92
19:46:35.308818 IP 192.168.2.11 > 192.168.2.11: ICMP host 192.168.2.12 unreachable, length 92
19:46:35.308829 IP 192.168.2.11 > 192.168.2.11: ICMP host 192.168.2.12 unreachable, length 92

```

注意：对于非 debian 系统，这里有可能 ping 不通，主要是因为内核中的一些 ARP 相关配置导致veth1 不返回 ARP 应答包，如 ubuntu 和 centos 上就会出现这种情况，解决办法如下：
```bash
$ echo 1 > /proc/sys/net/ipv4/conf/veth1/accept_local
$ echo 1 > /proc/sys/net/ipv4/conf/veth0/accept_local
$ echo 0 > /proc/sys/net/ipv4/conf/all/rp_filter
$ echo 0 > /proc/sys/net/ipv4/conf/veth0/rp_filter
$ echo 0 > /proc/sys/net/ipv4/conf/veth1/rp_filter

[root@huzhi-code ~]# ping -c 4 -I veth0 192.168.2.12
PING 192.168.2.12 (192.168.2.12) from 192.168.2.11 veth0: 56(84) bytes of data.

--- 192.168.2.12 ping statistics ---
4 packets transmitted, 0 received, 100% packet loss, time 2999ms

[root@huzhi-code ~]#

[root@huzhi-code ~]# tcpdump -i veth0 -n
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on veth0, link-type EN10MB (Ethernet), capture size 262144 bytes
19:54:59.869615 IP 192.168.2.11 > 192.168.2.12: ICMP echo request, id 16583, seq 1, length 64
19:55:00.868837 IP 192.168.2.11 > 192.168.2.12: ICMP echo request, id 16583, seq 2, length 64
19:55:01.868863 IP 192.168.2.11 > 192.168.2.12: ICMP echo request, id 16583, seq 3, length 64
19:55:02.868883 IP 192.168.2.11 > 192.168.2.12: ICMP echo request, id 16583, seq 4, length 64
19:55:04.880775 ARP, Request who-has 192.168.2.12 tell 192.168.2.11, length 28
19:55:04.880802 ARP, Reply 192.168.2.12 is-at 46:27:49:49:15:57, length 28

[root@huzhi-code ~]# tcpdump -i veth1 -n
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on veth1, link-type EN10MB (Ethernet), capture size 262144 bytes
19:54:59.869622 IP 192.168.2.11 > 192.168.2.12: ICMP echo request, id 16583, seq 1, length 64
19:55:00.868847 IP 192.168.2.11 > 192.168.2.12: ICMP echo request, id 16583, seq 2, length 64
19:55:01.868871 IP 192.168.2.11 > 192.168.2.12: ICMP echo request, id 16583, seq 3, length 64
19:55:02.868894 IP 192.168.2.11 > 192.168.2.12: ICMP echo request, id 16583, seq 4, length 64
19:55:04.880782 ARP, Request who-has 192.168.2.12 tell 192.168.2.11, length 28
19:55:04.880802 ARP, Reply 192.168.2.12 is-at 46:27:49:49:15:57, length 28

[root@huzhi-code ~]# tcpdump -i lo -n
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on lo, link-type EN10MB (Ethernet), capture size 262144 bytes
19:54:59.869642 IP 192.168.2.12 > 192.168.2.11: ICMP echo reply, id 16583, seq 1, length 64
19:55:00.868873 IP 192.168.2.12 > 192.168.2.11: ICMP echo reply, id 16583, seq 2, length 64
19:55:01.868892 IP 192.168.2.12 > 192.168.2.11: ICMP echo reply, id 16583, seq 3, length 64
19:55:02.868926 IP 192.168.2.12 > 192.168.2.11: ICMP echo reply, id 16583, seq 4, length 64

```

数据包的流程如下：

1. ping 进程构造 ICMP echo 请求包，并通过 socket 发给协议栈
2. 由于 ping 程序指定了走 veth0 接口，协议栈做相应的路由和 ARP 处理后，直接将该数据包交给了 veth0
3. 由于 veth0 的另一端连的是 veth1，所以 ICMP echo 请求包就转发给了 veth1，也就是 veth0 和 veth1 都接收到 ICMP echo 请求包，但 veth0 不发送响应包
4. veth1 收到 ICMP echo 请求包后，转交给另一端的协议栈
5. 协议栈一看自己的设备列表，发现本地有 192.168.2.12 这个 IP，于是构造 ICMP echo 应答包返回，此时返回不在屋里网络，直接在协议栈中处理返回包
6. 协议栈查看自己的路由表，发现回给 192.168.2.11 的数据包应该走 lo 口，于是将应答包交给 lo设备
7. lo 接到协议栈的应答包后，又把数据包还给了协议栈
8. 协议栈收到应答包后，发现有 socket 需要该包，于是交给了相应的 socket，这个 socket 正好是 ping 进程创建的 socket，于是 ping 进程收到了应答包
9. 所以在 lo 设备上可以看到应答包

## 参考
* https://segmentfault.com/a/1190000009251098
* https://www.ibm.com/developerworks/cn/linux/1310_xiawc_networkdevice/index.html

