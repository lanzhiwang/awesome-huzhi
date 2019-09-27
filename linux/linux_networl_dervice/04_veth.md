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

## 示例

```bash
#########################################################
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
7: veth1@veth0: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 qdisc noop state DOWN qlen 1000
    link/ether 46:27:49:49:15:57 brd ff:ff:ff:ff:ff:ff
8: veth0@veth1: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 qdisc noop state DOWN qlen 1000
    link/ether 7e:08:71:f8:c8:1a brd ff:ff:ff:ff:ff:ff
[root@huzhi-code ~]#

#########################################################
[root@huzhi-code ~]# ip addr add 192.168.2.11/24 dev veth0
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
7: veth1@veth0: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 qdisc noop state DOWN qlen 1000
    link/ether 46:27:49:49:15:57 brd ff:ff:ff:ff:ff:ff
8: veth0@veth1: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 qdisc noop state DOWN qlen 1000
    link/ether 7e:08:71:f8:c8:1a brd ff:ff:ff:ff:ff:ff
    inet 192.168.2.11/24 scope global veth0
       valid_lft forever preferred_lft forever

#########################################################
[root@huzhi-code ~]# ip link set veth0 up
[root@huzhi-code ~]# ip link set veth1 up
[root@huzhi-code ~]# ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT qlen 1000
    link/ether 00:50:56:9b:35:0e brd ff:ff:ff:ff:ff:ff
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT
    link/ether 02:42:cf:09:1c:03 brd ff:ff:ff:ff:ff:ff
7: veth1@veth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT qlen 1000
    link/ether 46:27:49:49:15:57 brd ff:ff:ff:ff:ff:ff
8: veth0@veth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT qlen 1000
    link/ether 7e:08:71:f8:c8:1a brd ff:ff:ff:ff:ff:ff
[root@huzhi-code ~]# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         10.0.1.1        0.0.0.0         UG    100    0        0 ens192
10.0.1.1        0.0.0.0         255.255.255.255 UH    100    0        0 ens192
10.0.8.0        0.0.0.0         255.255.255.0   U     100    0        0 ens192
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
192.168.2.0     0.0.0.0         255.255.255.0   U     0      0        0 veth0
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
7: veth1@veth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP qlen 1000
    link/ether 46:27:49:49:15:57 brd ff:ff:ff:ff:ff:ff
    inet6 fe80::4427:49ff:fe49:1557/64 scope link
       valid_lft forever preferred_lft forever
8: veth0@veth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP qlen 1000
    link/ether 7e:08:71:f8:c8:1a brd ff:ff:ff:ff:ff:ff
    inet 192.168.2.11/24 scope global veth0
       valid_lft forever preferred_lft forever
    inet6 fe80::7c08:71ff:fef8:c81a/64 scope link
       valid_lft forever preferred_lft forever
[root@huzhi-code ~]#

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




[参考](https://segmentfault.com/a/1190000009251098)


