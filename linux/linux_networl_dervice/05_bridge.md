# bridge

```bash
[root@huzhi-code ~]# ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT qlen 1000
    link/ether 00:50:56:9b:35:0e brd ff:ff:ff:ff:ff:ff
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT
    link/ether 02:42:cf:09:1c:03 brd ff:ff:ff:ff:ff:ff
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
[root@huzhi-code ~]# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         10.0.1.1        0.0.0.0         UG    100    0        0 ens192
10.0.1.1        0.0.0.0         255.255.255.255 UH    100    0        0 ens192
10.0.8.0        0.0.0.0         255.255.255.0   U     100    0        0 ens192
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
[root@huzhi-code ~]#

# 创建一个 bridge

+----------------------------------------------------------------+
|                                                                |
|       +------------------------------------------------+       |
|       |             Newwork Protocol Stack             |       |
|       +------------------------------------------------+       |
|              ↑                                ↑                |
|..............|................................|................|
|              ↓                                ↓                |
|        +----------+                     +------------+         |
|        |   eth0   |                     |     br0    |         |
|        +----------+                     +------------+         |
| 192.168.3.21 ↑                                                 |
|              |                                                 |
|              |                                                 |
+--------------|-------------------------------------------------+
               ↓
         Physical Network


[root@huzhi-code ~]# ip link add br0 type bridge
[root@huzhi-code ~]# ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT qlen 1000
    link/ether 00:50:56:9b:35:0e brd ff:ff:ff:ff:ff:ff
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT
    link/ether 02:42:cf:09:1c:03 brd ff:ff:ff:ff:ff:ff
10: br0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT qlen 1000
    link/ether 9e:bc:95:58:13:3d brd ff:ff:ff:ff:ff:ff
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
10: br0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN qlen 1000
    link/ether 9e:bc:95:58:13:3d brd ff:ff:ff:ff:ff:ff
[root@huzhi-code ~]#
[root@huzhi-code ~]# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         10.0.1.1        0.0.0.0         UG    100    0        0 ens192
10.0.1.1        0.0.0.0         255.255.255.255 UH    100    0        0 ens192
10.0.8.0        0.0.0.0         255.255.255.0   U     100    0        0 ens192
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
[root@huzhi-code ~]#

[root@huzhi-code ~]# ip link set br0 up
[root@huzhi-code ~]# ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT qlen 1000
    link/ether 00:50:56:9b:35:0e brd ff:ff:ff:ff:ff:ff
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT
    link/ether 02:42:cf:09:1c:03 brd ff:ff:ff:ff:ff:ff
10: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN mode DEFAULT qlen 1000
    link/ether 9e:bc:95:58:13:3d brd ff:ff:ff:ff:ff:ff
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
10: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN qlen 1000
    link/ether 9e:bc:95:58:13:3d brd ff:ff:ff:ff:ff:ff
    inet6 fe80::9cbc:95ff:fe58:133d/64 scope link
       valid_lft forever preferred_lft forever
[root@huzhi-code ~]# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         10.0.1.1        0.0.0.0         UG    100    0        0 ens192
10.0.1.1        0.0.0.0         255.255.255.255 UH    100    0        0 ens192
10.0.8.0        0.0.0.0         255.255.255.0   U     100    0        0 ens192
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
[root@huzhi-code ~]#

# 单独创建 br0 没有什么作用，即使为 br0 设置 IP 也没有作用
# 创建一对 veth 设备，并配置上 IP

+----------------------------------------------------------------+
|                                                                |
|       +------------------------------------------------+       |
|       |             Newwork Protocol Stack             |       |
|       +------------------------------------------------+       |
|            ↑            ↑              ↑            ↑          |
|............|............|..............|............|..........|
|            ↓            ↓              ↓            ↓          |
|        +------+     +--------+     +-------+    +-------+      |
|        | .3.21|     |        |     | .3.101|    | .3.102|      |
|        +------+     +--------+     +-------+    +-------+      |
|        | eth0 |     |   br0  |     | veth0 |    | veth1 |      |
|        +------+     +--------+     +-------+    +-------+      |
|            ↑                           ↑            ↑          |
|            |                           |            |          |
|            |                           +------------+          |
|            |                                                   |
+------------|---------------------------------------------------+
             ↓
     Physical Network

[root@huzhi-code ~]# ip link add veth0 type veth peer name veth1
[root@huzhi-code ~]# ip addr add 192.168.3.101/24 dev veth0
[root@huzhi-code ~]# ip addr add 192.168.3.102/24 dev veth1
[root@huzhi-code ~]# ip link set veth0 up
[root@huzhi-code ~]# ip link set veth1 up
[root@huzhi-code ~]# ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT qlen 1000
    link/ether 00:50:56:9b:35:0e brd ff:ff:ff:ff:ff:ff
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT
    link/ether 02:42:cf:09:1c:03 brd ff:ff:ff:ff:ff:ff
10: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN mode DEFAULT qlen 1000
    link/ether 9e:bc:95:58:13:3d brd ff:ff:ff:ff:ff:ff
11: veth1@veth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT qlen 1000
    link/ether 06:de:e7:d7:f7:dc brd ff:ff:ff:ff:ff:ff
12: veth0@veth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT qlen 1000
    link/ether ba:b2:8c:86:46:9b brd ff:ff:ff:ff:ff:ff
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
10: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN qlen 1000
    link/ether 9e:bc:95:58:13:3d brd ff:ff:ff:ff:ff:ff
    inet6 fe80::9cbc:95ff:fe58:133d/64 scope link
       valid_lft forever preferred_lft forever
11: veth1@veth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP qlen 1000
    link/ether 06:de:e7:d7:f7:dc brd ff:ff:ff:ff:ff:ff
    inet 192.168.3.102/24 scope global veth1
       valid_lft forever preferred_lft forever
    inet6 fe80::4de:e7ff:fed7:f7dc/64 scope link
       valid_lft forever preferred_lft forever
12: veth0@veth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP qlen 1000
    link/ether ba:b2:8c:86:46:9b brd ff:ff:ff:ff:ff:ff
    inet 192.168.3.101/24 scope global veth0
       valid_lft forever preferred_lft forever
    inet6 fe80::b8b2:8cff:fe86:469b/64 scope link
       valid_lft forever preferred_lft forever
[root@huzhi-code ~]# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         10.0.1.1        0.0.0.0         UG    100    0        0 ens192
10.0.1.1        0.0.0.0         255.255.255.255 UH    100    0        0 ens192
10.0.8.0        0.0.0.0         255.255.255.0   U     100    0        0 ens192
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
192.168.3.0     0.0.0.0         255.255.255.0   U     0      0        0 veth0
192.168.3.0     0.0.0.0         255.255.255.0   U     0      0        0 veth1
[root@huzhi-code ~]#

# 将 veth0 连上 br0

+----------------------------------------------------------------+
|                                                                |
|       +------------------------------------------------+       |
|       |             Newwork Protocol Stack             |       |
|       +------------------------------------------------+       |
|            ↑            ↑              |            ↑          |
|............|............|..............|............|..........|
|            ↓            ↓              ↓            ↓          |
|        +------+     +--------+     +-------+    +-------+      |
|        | .3.21|     |        |     | .3.101|    | .3.102|      |
|        +------+     +--------+     +-------+    +-------+      |
|        | eth0 |     |   br0  |<--->| veth0 |    | veth1 |      |
|        +------+     +--------+     +-------+    +-------+      |
|            ↑                           ↑            ↑          |
|            |                           |            |          |
|            |                           +------------+          |
|            |                                                   |
+------------|---------------------------------------------------+
             ↓
     Physical Network

[root@huzhi-code ~]# ip link set dev veth0 master br0
[root@huzhi-code ~]# bridge link
12: veth0 state UP @veth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 master br0 state forwarding priority 32 cost 2
[root@huzhi-code ~]#
[root@huzhi-code ~]# ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT qlen 1000
    link/ether 00:50:56:9b:35:0e brd ff:ff:ff:ff:ff:ff
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT
    link/ether 02:42:cf:09:1c:03 brd ff:ff:ff:ff:ff:ff
10: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT qlen 1000
    link/ether ba:b2:8c:86:46:9b brd ff:ff:ff:ff:ff:ff
11: veth1@veth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT qlen 1000
    link/ether 06:de:e7:d7:f7:dc brd ff:ff:ff:ff:ff:ff
12: veth0@veth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master br0 state UP mode DEFAULT qlen 1000
    link/ether ba:b2:8c:86:46:9b brd ff:ff:ff:ff:ff:ff
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
10: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP qlen 1000
    link/ether ba:b2:8c:86:46:9b brd ff:ff:ff:ff:ff:ff
    inet6 fe80::9cbc:95ff:fe58:133d/64 scope link
       valid_lft forever preferred_lft forever
11: veth1@veth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP qlen 1000
    link/ether 06:de:e7:d7:f7:dc brd ff:ff:ff:ff:ff:ff
    inet 192.168.3.102/24 scope global veth1
       valid_lft forever preferred_lft forever
    inet6 fe80::4de:e7ff:fed7:f7dc/64 scope link
       valid_lft forever preferred_lft forever
12: veth0@veth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master br0 state UP qlen 1000
    link/ether ba:b2:8c:86:46:9b brd ff:ff:ff:ff:ff:ff
    inet 192.168.3.101/24 scope global veth0
       valid_lft forever preferred_lft forever
    inet6 fe80::b8b2:8cff:fe86:469b/64 scope link
       valid_lft forever preferred_lft forever
[root@huzhi-code ~]# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         10.0.1.1        0.0.0.0         UG    100    0        0 ens192
10.0.1.1        0.0.0.0         255.255.255.255 UH    100    0        0 ens192
10.0.8.0        0.0.0.0         255.255.255.0   U     100    0        0 ens192
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
192.168.3.0     0.0.0.0         255.255.255.0   U     0      0        0 veth0
192.168.3.0     0.0.0.0         255.255.255.0   U     0      0        0 veth1
[root@huzhi-code ~]#

```

br0 和 veth0 相连之后，发生了几个变化：

* br0 和 veth0 之间连接起来了，并且是双向的通道
* 协议栈和 veth0 之间变成了单通道，协议栈能发数据给 veth0，但 veth0 从外面收到的数据不会转发给协议栈
* **br0 的 mac 地址改变了，变成了 veth0 的 mac 地址**

相当于 bridge 在 veth0 和协议栈之间插了一脚，在 veth0 上面做了点小动作，将 veth0 本来要转发给协议栈的数据给拦截了，全部转发给 bridge 了，同时 bridge 也可以向 veth0 发数据。

```bash
[root@huzhi-code ~]# ping -c 4 192.168.3.101
PING 192.168.3.101 (192.168.3.101) 56(84) bytes of data.
64 bytes from 192.168.3.101: icmp_seq=1 ttl=64 time=0.057 ms
64 bytes from 192.168.3.101: icmp_seq=2 ttl=64 time=0.056 ms
64 bytes from 192.168.3.101: icmp_seq=3 ttl=64 time=0.054 ms
64 bytes from 192.168.3.101: icmp_seq=4 ttl=64 time=0.055 ms

--- 192.168.3.101 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3000ms
rtt min/avg/max/mdev = 0.054/0.055/0.057/0.007 ms
[root@huzhi-code ~]#
[root@huzhi-code ~]# tcpdump -n -i lo
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on lo, link-type EN10MB (Ethernet), capture size 262144 bytes
12:45:07.421808 IP 192.168.3.101 > 192.168.3.101: ICMP echo request, id 18211, seq 1, length 64
12:45:07.421823 IP 192.168.3.101 > 192.168.3.101: ICMP echo reply, id 18211, seq 1, length 64
12:45:08.421823 IP 192.168.3.101 > 192.168.3.101: ICMP echo request, id 18211, seq 2, length 64
12:45:08.421837 IP 192.168.3.101 > 192.168.3.101: ICMP echo reply, id 18211, seq 2, length 64
12:45:09.421820 IP 192.168.3.101 > 192.168.3.101: ICMP echo request, id 18211, seq 3, length 64
12:45:09.421835 IP 192.168.3.101 > 192.168.3.101: ICMP echo reply, id 18211, seq 3, length 64
12:45:10.421831 IP 192.168.3.101 > 192.168.3.101: ICMP echo request, id 18211, seq 4, length 64
12:45:10.421846 IP 192.168.3.101 > 192.168.3.101: ICMP echo reply, id 18211, seq 4, length 64


[root@huzhi-code ~]#
[root@huzhi-code ~]# ping -c 4 -I veth0 192.168.3.101
PING 192.168.3.101 (192.168.3.101) from 192.168.3.101 veth0: 56(84) bytes of data.

--- 192.168.3.101 ping statistics ---
4 packets transmitted, 0 received, 100% packet loss, time 2999ms

[root@huzhi-code ~]#
[root@huzhi-code ~]# tcpdump -n -i lo
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on lo, link-type EN10MB (Ethernet), capture size 262144 bytes
12:45:37.049901 IP 192.168.3.101 > 192.168.3.101: ICMP echo request, id 18212, seq 1, length 64
12:45:37.049914 IP 192.168.3.101 > 192.168.3.101: ICMP echo reply, id 18212, seq 1, length 64
12:45:38.049865 IP 192.168.3.101 > 192.168.3.101: ICMP echo request, id 18212, seq 2, length 64
12:45:38.049886 IP 192.168.3.101 > 192.168.3.101: ICMP echo reply, id 18212, seq 2, length 64
12:45:39.049878 IP 192.168.3.101 > 192.168.3.101: ICMP echo request, id 18212, seq 3, length 64
12:45:39.049894 IP 192.168.3.101 > 192.168.3.101: ICMP echo reply, id 18212, seq 3, length 64
12:45:40.049884 IP 192.168.3.101 > 192.168.3.101: ICMP echo request, id 18212, seq 4, length 64
12:45:40.049903 IP 192.168.3.101 > 192.168.3.101: ICMP echo reply, id 18212, seq 4, length 64



[root@huzhi-code ~]#
[root@huzhi-code ~]# ping -c 4 -I veth0 192.168.3.102
PING 192.168.3.102 (192.168.3.102) from 192.168.3.101 veth0: 56(84) bytes of data.

--- 192.168.3.102 ping statistics ---
4 packets transmitted, 0 received, 100% packet loss, time 2999ms

[root@huzhi-code ~]#
[root@huzhi-code ~]# tcpdump -n -i veth0
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on veth0, link-type EN10MB (Ethernet), capture size 262144 bytes
12:46:50.168840 ARP, Request who-has 192.168.3.102 tell 192.168.3.101, length 28
12:46:51.170761 ARP, Request who-has 192.168.3.102 tell 192.168.3.101, length 28
12:46:52.172761 ARP, Request who-has 192.168.3.102 tell 192.168.3.101, length 28
[root@huzhi-code ~]#
[root@huzhi-code ~]# tcpdump -n -i veth1
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on veth1, link-type EN10MB (Ethernet), capture size 262144 bytes
12:46:50.168850 ARP, Request who-has 192.168.3.102 tell 192.168.3.101, length 28
12:46:51.170766 ARP, Request who-has 192.168.3.102 tell 192.168.3.101, length 28
12:46:52.172767 ARP, Request who-has 192.168.3.102 tell 192.168.3.101, length 28
[root@huzhi-code ~]#
[root@huzhi-code ~]# tcpdump -n -i lo
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on lo, link-type EN10MB (Ethernet), capture size 262144 bytes
12:46:53.174790 IP 192.168.3.101 > 192.168.3.101: ICMP host 192.168.3.102 unreachable, length 92
12:46:53.174795 IP 192.168.3.101 > 192.168.3.101: ICMP host 192.168.3.102 unreachable, length 92
12:46:53.174797 IP 192.168.3.101 > 192.168.3.101: ICMP host 192.168.3.102 unreachable, length 92
12:46:53.174799 IP 192.168.3.101 > 192.168.3.101: ICMP host 192.168.3.102 unreachable, length 92
[root@huzhi-code ~]#


[root@huzhi-code ~]# echo 1 > /proc/sys/net/ipv4/conf/veth1/accept_local
[root@huzhi-code ~]# echo 1 > /proc/sys/net/ipv4/conf/veth0/accept_local
[root@huzhi-code ~]# echo 0 > /proc/sys/net/ipv4/conf/all/rp_filter
[root@huzhi-code ~]# echo 0 > /proc/sys/net/ipv4/conf/veth0/rp_filter
[root@huzhi-code ~]# echo 0 > /proc/sys/net/ipv4/conf/veth1/rp_filter
[root@huzhi-code ~]#

[root@huzhi-code ~]# ping -c 4 -I veth0 192.168.3.102
PING 192.168.3.102 (192.168.3.102) from 192.168.3.101 veth0: 56(84) bytes of data.

--- 192.168.3.102 ping statistics ---
4 packets transmitted, 0 received, 100% packet loss, time 2999ms

[root@huzhi-code ~]#
[root@huzhi-code ~]# tcpdump -n -i veth0
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on veth0, link-type EN10MB (Ethernet), capture size 262144 bytes
13:02:13.075932 ARP, Request who-has 192.168.3.102 tell 192.168.3.101, length 28
13:02:13.075954 ARP, Reply 192.168.3.102 is-at 06:de:e7:d7:f7:dc, length 28
13:02:14.076766 ARP, Request who-has 192.168.3.102 tell 192.168.3.101, length 28
13:02:14.076797 ARP, Reply 192.168.3.102 is-at 06:de:e7:d7:f7:dc, length 28
13:02:15.078763 ARP, Request who-has 192.168.3.102 tell 192.168.3.101, length 28
13:02:15.078791 ARP, Reply 192.168.3.102 is-at 06:de:e7:d7:f7:dc, length 28

[root@huzhi-code ~]#
[root@huzhi-code ~]# tcpdump -n -i veth1
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on veth1, link-type EN10MB (Ethernet), capture size 262144 bytes
13:02:13.075945 ARP, Request who-has 192.168.3.102 tell 192.168.3.101, length 28
13:02:13.075954 ARP, Reply 192.168.3.102 is-at 06:de:e7:d7:f7:dc, length 28
13:02:14.076774 ARP, Request who-has 192.168.3.102 tell 192.168.3.101, length 28
13:02:14.076797 ARP, Reply 192.168.3.102 is-at 06:de:e7:d7:f7:dc, length 28
13:02:15.078769 ARP, Request who-has 192.168.3.102 tell 192.168.3.101, length 28
13:02:15.078790 ARP, Reply 192.168.3.102 is-at 06:de:e7:d7:f7:dc, length 28

[root@huzhi-code ~]#
[root@huzhi-code ~]# tcpdump -n -i br0
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on br0, link-type EN10MB (Ethernet), capture size 262144 bytes
13:02:13.075954 ARP, Reply 192.168.3.102 is-at 06:de:e7:d7:f7:dc, length 28
13:02:14.076797 ARP, Reply 192.168.3.102 is-at 06:de:e7:d7:f7:dc, length 28
13:02:15.078791 ARP, Reply 192.168.3.102 is-at 06:de:e7:d7:f7:dc, length 28

[root@huzhi-code ~]#
[root@huzhi-code ~]# tcpdump -n -i lo
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on lo, link-type EN10MB (Ethernet), capture size 262144 bytes
13:02:16.080775 IP 192.168.3.101 > 192.168.3.101: ICMP host 192.168.3.102 unreachable, length 92
13:02:16.080780 IP 192.168.3.101 > 192.168.3.101: ICMP host 192.168.3.102 unreachable, length 92
13:02:16.080783 IP 192.168.3.101 > 192.168.3.101: ICMP host 192.168.3.102 unreachable, length 92
13:02:16.080785 IP 192.168.3.101 > 192.168.3.101: ICMP host 192.168.3.102 unreachable, length 92

[root@huzhi-code ~]#


ping -c 4 -I br0 192.168.3.102

```

* 由于 veth0 的 arp 缓存里面没有 veth1 的 mac 地址，所以 ping 之前先发 arp 请求，从 veth1 上抓包来看，veth1 收到了 arp 请求，并且返回了 arp 应答
* 从 veth0 上抓包来看，arp 数据包也发出去了，并且也收到了 arp 返回
* br0 也收到了 arp 应答
* 之所以 ping 失败是因为在 veth0 收到  arp 应答包后没有给协议栈，而是给了 br0，又因为 br0  没有设置 IP，于是协议栈得不到 veth1 的 mac 地址，从而通信失败


给 br0 配置 IP 有两种方法：
1. 给 br0 配置 192.168.3.103/24
2. 删除 veth0 的IP，将 192.168.3.101/24 配置给 br0

```bash
[root@huzhi-code ~]# ip addr add 192.168.3.103/24 dev br0
[root@huzhi-code ~]# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         10.0.1.1        0.0.0.0         UG    100    0        0 ens192
10.0.1.1        0.0.0.0         255.255.255.255 UH    100    0        0 ens192
10.0.8.0        0.0.0.0         255.255.255.0   U     100    0        0 ens192
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
192.168.3.0     0.0.0.0         255.255.255.0   U     0      0        0 veth0
192.168.3.0     0.0.0.0         255.255.255.0   U     0      0        0 veth1
192.168.3.0     0.0.0.0         255.255.255.0   U     0      0        0 br0
[root@huzhi-code ~]#

+----------------------------------------------------------------+
|                                                                |
|       +------------------------------------------------+       |
|       |             Newwork Protocol Stack             |       |
|       +------------------------------------------------+       |
|            ↑            ↑              |            ↑          |
|............|............|..............|............|..........|
|            ↓            ↓              ↓            ↓          |
|        +------+     +--------+     +-------+    +-------+      |
|        | .3.21|     | .3.103 |     | .3.101|    | .3.102|      |
|        +------+     +--------+     +-------+    +-------+      |
|        | eth0 |     |   br0  |<--->| veth0 |    | veth1 |      |
|        +------+     +--------+     +-------+    +-------+      |
|            ↑                           ↑            ↑          |
|            |                           |            |          |
|            |                           +------------+          |
|            |                                                   |
+------------|---------------------------------------------------+
             ↓
     Physical Network

[root@huzhi-code ~]# ping -c 4 -I veth0 192.168.3.102
PING 192.168.3.102 (192.168.3.102) from 192.168.3.101 veth0: 56(84) bytes of data.

--- 192.168.3.102 ping statistics ---
4 packets transmitted, 0 received, 100% packet loss, time 2999ms

[root@huzhi-code ~]#
[root@huzhi-code ~]# tcpdump -n -i veth0
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on veth0, link-type EN10MB (Ethernet), capture size 262144 bytes
13:59:11.012931 ARP, Request who-has 192.168.3.102 tell 192.168.3.101, length 28
13:59:11.012952 ARP, Reply 192.168.3.102 is-at 5e:86:b7:d1:14:c3, length 28
13:59:12.014764 ARP, Request who-has 192.168.3.102 tell 192.168.3.101, length 28
13:59:12.014784 ARP, Reply 192.168.3.102 is-at 5e:86:b7:d1:14:c3, length 28
13:59:13.016761 ARP, Request who-has 192.168.3.102 tell 192.168.3.101, length 28
13:59:13.016778 ARP, Reply 192.168.3.102 is-at 5e:86:b7:d1:14:c3, length 28

[root@huzhi-code ~]#
[root@huzhi-code ~]# tcpdump -n -i veth1
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on veth1, link-type EN10MB (Ethernet), capture size 262144 bytes
13:59:11.012941 ARP, Request who-has 192.168.3.102 tell 192.168.3.101, length 28
13:59:11.012951 ARP, Reply 192.168.3.102 is-at 5e:86:b7:d1:14:c3, length 28
13:59:12.014770 ARP, Request who-has 192.168.3.102 tell 192.168.3.101, length 28
13:59:12.014783 ARP, Reply 192.168.3.102 is-at 5e:86:b7:d1:14:c3, length 28
13:59:13.016766 ARP, Request who-has 192.168.3.102 tell 192.168.3.101, length 28
13:59:13.016777 ARP, Reply 192.168.3.102 is-at 5e:86:b7:d1:14:c3, length 28

[root@huzhi-code ~]# tcpdump -n -i br0
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on br0, link-type EN10MB (Ethernet), capture size 262144 bytes
13:59:11.012952 ARP, Reply 192.168.3.102 is-at 5e:86:b7:d1:14:c3, length 28
13:59:12.014784 ARP, Reply 192.168.3.102 is-at 5e:86:b7:d1:14:c3, length 28
13:59:13.016778 ARP, Reply 192.168.3.102 is-at 5e:86:b7:d1:14:c3, length 28

[root@huzhi-code ~]# tcpdump -n -i lo
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on lo, link-type EN10MB (Ethernet), capture size 262144 bytes
13:59:14.018780 IP 192.168.3.101 > 192.168.3.101: ICMP host 192.168.3.102 unreachable, length 92
13:59:14.018785 IP 192.168.3.101 > 192.168.3.101: ICMP host 192.168.3.102 unreachable, length 92
13:59:14.018788 IP 192.168.3.101 > 192.168.3.101: ICMP host 192.168.3.102 unreachable, length 92
13:59:14.018790 IP 192.168.3.101 > 192.168.3.101: ICMP host 192.168.3.102 unreachable, length 92



+----------------------------------------------------------------+
|                                                                |
|       +------------------------------------------------+       |
|       |             Newwork Protocol Stack             |       |
|       +------------------------------------------------+       |
|            ↑            ↑              |            ↑          |
|............|............|..............|............|..........|
|            ↓            ↓              ↓            ↓          |
|        +------+     +--------+     +-------+    +-------+      |
|        | .3.21|     | .3.103 |     |       |    | .3.102|      |
|        +------+     +--------+     +-------+    +-------+      |
|        | eth0 |     |   br0  |<--->| veth0 |    | veth1 |      |
|        +------+     +--------+     +-------+    +-------+      |
|            ↑                           ↑            ↑          |
|            |                           |            |          |
|            |                           +------------+          |
|            |                                                   |
+------------|---------------------------------------------------+
             ↓
     Physical Network

[root@huzhi-code ~]# ip addr del 192.168.3.101/24 dev veth0
[root@huzhi-code ~]# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         10.0.1.1        0.0.0.0         UG    100    0        0 ens192
10.0.1.1        0.0.0.0         255.255.255.255 UH    100    0        0 ens192
10.0.8.0        0.0.0.0         255.255.255.0   U     100    0        0 ens192
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
192.168.3.0     0.0.0.0         255.255.255.0   U     0      0        0 veth1
192.168.3.0     0.0.0.0         255.255.255.0   U     0      0        0 br0
[root@huzhi-code ~]#

[root@huzhi-code ~]# ping -c 4 -I veth0 192.168.3.102
ping: Warning: source address might be selected on device other than veth0.
PING 192.168.3.102 (192.168.3.102) from 10.0.8.10 veth0: 56(84) bytes of data.

--- 192.168.3.102 ping statistics ---
4 packets transmitted, 0 received, 100% packet loss, time 2999ms

[root@huzhi-code ~]#
[root@huzhi-code ~]# tcpdump -n -i veth0
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on veth0, link-type EN10MB (Ethernet), capture size 262144 bytes
14:11:33.302326 ARP, Request who-has 192.168.3.102 tell 10.0.8.10, length 28
14:11:33.302339 ARP, Reply 192.168.3.102 is-at 5e:86:b7:d1:14:c3, length 28
14:11:34.304763 ARP, Request who-has 192.168.3.102 tell 10.0.8.10, length 28
14:11:34.304784 ARP, Reply 192.168.3.102 is-at 5e:86:b7:d1:14:c3, length 28
14:11:35.306773 ARP, Request who-has 192.168.3.102 tell 10.0.8.10, length 28
14:11:35.306796 ARP, Reply 192.168.3.102 is-at 5e:86:b7:d1:14:c3, length 28

[root@huzhi-code ~]# tcpdump -n -i veth1
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on veth1, link-type EN10MB (Ethernet), capture size 262144 bytes
14:11:33.302332 ARP, Request who-has 192.168.3.102 tell 10.0.8.10, length 28
14:11:33.302338 ARP, Reply 192.168.3.102 is-at 5e:86:b7:d1:14:c3, length 28
14:11:34.304769 ARP, Request who-has 192.168.3.102 tell 10.0.8.10, length 28
14:11:34.304783 ARP, Reply 192.168.3.102 is-at 5e:86:b7:d1:14:c3, length 28
14:11:35.306779 ARP, Request who-has 192.168.3.102 tell 10.0.8.10, length 28
14:11:35.306795 ARP, Reply 192.168.3.102 is-at 5e:86:b7:d1:14:c3, length 28

[root@huzhi-code ~]# tcpdump -n -i br0
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on br0, link-type EN10MB (Ethernet), capture size 262144 bytes
14:11:33.302339 ARP, Reply 192.168.3.102 is-at 5e:86:b7:d1:14:c3, length 28
14:11:34.304784 ARP, Reply 192.168.3.102 is-at 5e:86:b7:d1:14:c3, length 28
14:11:35.306796 ARP, Reply 192.168.3.102 is-at 5e:86:b7:d1:14:c3, length 28

[root@huzhi-code ~]# tcpdump -n -i lo
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on lo, link-type EN10MB (Ethernet), capture size 262144 bytes
14:11:36.308786 IP 10.0.8.10 > 10.0.8.10: ICMP host 192.168.3.102 unreachable, length 92
14:11:36.308806 IP 10.0.8.10 > 10.0.8.10: ICMP host 192.168.3.102 unreachable, length 92
14:11:36.308810 IP 10.0.8.10 > 10.0.8.10: ICMP host 192.168.3.102 unreachable, length 92
14:11:36.308812 IP 10.0.8.10 > 10.0.8.10: ICMP host 192.168.3.102 unreachable, length 92



[root@huzhi-code ~]# ping -c 4 -I br0 192.168.3.102
PING 192.168.3.102 (192.168.3.102) from 192.168.3.103 br0: 56(84) bytes of data.

--- 192.168.3.102 ping statistics ---
4 packets transmitted, 0 received, 100% packet loss, time 2999ms

[root@huzhi-code ~]#
[root@huzhi-code ~]# tcpdump -n -i veth0
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on veth0, link-type EN10MB (Ethernet), capture size 262144 bytes
14:16:21.003932 IP 192.168.3.103 > 192.168.3.102: ICMP echo request, id 18353, seq 1, length 64
14:16:22.003876 IP 192.168.3.103 > 192.168.3.102: ICMP echo request, id 18353, seq 2, length 64
14:16:23.003854 IP 192.168.3.103 > 192.168.3.102: ICMP echo request, id 18353, seq 3, length 64
14:16:24.003858 IP 192.168.3.103 > 192.168.3.102: ICMP echo request, id 18353, seq 4, length 64
14:16:26.016788 ARP, Request who-has 192.168.3.102 tell 192.168.3.103, length 28
14:16:26.016811 ARP, Reply 192.168.3.102 is-at 5e:86:b7:d1:14:c3, length 28

[root@huzhi-code ~]# tcpdump -n -i veth1
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on veth1, link-type EN10MB (Ethernet), capture size 262144 bytes
14:16:21.003941 IP 192.168.3.103 > 192.168.3.102: ICMP echo request, id 18353, seq 1, length 64
14:16:22.003881 IP 192.168.3.103 > 192.168.3.102: ICMP echo request, id 18353, seq 2, length 64
14:16:23.003859 IP 192.168.3.103 > 192.168.3.102: ICMP echo request, id 18353, seq 3, length 64
14:16:24.003862 IP 192.168.3.103 > 192.168.3.102: ICMP echo request, id 18353, seq 4, length 64
14:16:26.016792 ARP, Request who-has 192.168.3.102 tell 192.168.3.103, length 28
14:16:26.016810 ARP, Reply 192.168.3.102 is-at 5e:86:b7:d1:14:c3, length 28

[root@huzhi-code ~]# tcpdump -n -i br0
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on br0, link-type EN10MB (Ethernet), capture size 262144 bytes
14:16:21.003923 IP 192.168.3.103 > 192.168.3.102: ICMP echo request, id 18353, seq 1, length 64
14:16:22.003862 IP 192.168.3.103 > 192.168.3.102: ICMP echo request, id 18353, seq 2, length 64
14:16:23.003842 IP 192.168.3.103 > 192.168.3.102: ICMP echo request, id 18353, seq 3, length 64
14:16:24.003846 IP 192.168.3.103 > 192.168.3.102: ICMP echo request, id 18353, seq 4, length 64
14:16:26.016773 ARP, Request who-has 192.168.3.102 tell 192.168.3.103, length 28
14:16:26.016811 ARP, Reply 192.168.3.102 is-at 5e:86:b7:d1:14:c3, length 28

[root@huzhi-code ~]# tcpdump -n -i lo
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on lo, link-type EN10MB (Ethernet), capture size 262144 bytes
14:16:21.003963 IP 192.168.3.102 > 192.168.3.103: ICMP echo reply, id 18353, seq 1, length 64
14:16:22.003903 IP 192.168.3.102 > 192.168.3.103: ICMP echo reply, id 18353, seq 2, length 64
14:16:23.003878 IP 192.168.3.102 > 192.168.3.103: ICMP echo reply, id 18353, seq 3, length 64
14:16:24.003884 IP 192.168.3.102 > 192.168.3.103: ICMP echo reply, id 18353, seq 4, length 64

[root@huzhi-code ~]# cat /proc/sys/net/ipv4/ip_forward
1
[root@huzhi-code ~]#




```




给 veth0 配置 IP 没有意义，因为就算协议栈传数据包给 veth0，应答包也回不来。这里我们就将 veth0 的 IP 让给 bridge


```
ip addr del 192.168.3.101/24 dev veth0
ip addr add 192.168.3.101/24 dev br0

+----------------------------------------------------------------+
|                                                                |
|       +------------------------------------------------+       |
|       |             Newwork Protocol Stack             |       |
|       +------------------------------------------------+       |
|            ↑            ↑                           ↑          |
|............|............|...........................|..........|
|            ↓            ↓                           ↓          |
|        +------+     +--------+     +-------+    +-------+      |
|        | .3.21|     | .3.101 |     |       |    | .3.102|      |
|        +------+     +--------+     +-------+    +-------+      |
|        | eth0 |     |   br0  |<--->| veth0 |    | veth1 |      |
|        +------+     +--------+     +-------+    +-------+      |
|            ↑                           ↑            ↑          |
|            |                           |            |          |
|            |                           +------------+          |
|            |                                                   |
+------------|---------------------------------------------------+
             ↓
     Physical Network


# 将物理网卡 eth0 添加到 bridge
ip link set dev eth0 master br0
bridge link

# 将 eth0 上的 IP 删除掉
ip addr del 192.168.3.21/24 dev eth0

# 添加默认网关
ip route add default via 192.168.3.1

+----------------------------------------------------------------+
|                                                                |
|       +------------------------------------------------+       |
|       |             Newwork Protocol Stack             |       |
|       +------------------------------------------------+       |
|                         ↑                           ↑          |
|.........................|...........................|..........|
|                         ↓                           ↓          |
|        +------+     +--------+     +-------+    +-------+      |
|        |      |     | .3.101 |     |       |    | .3.102|      |
|        +------+     +--------+     +-------+    +-------+      |
|        | eth0 |<--->|   br0  |<--->| veth0 |    | veth1 |      |
|        +------+     +--------+     +-------+    +-------+      |
|            ↑                           ↑            ↑          |
|            |                           |            |          |
|            |                           +------------+          |
|            |                                                   |
+------------|---------------------------------------------------+
             ↓
     Physical Network

```





## 参考
* https://segmentfault.com/a/1190000009491002
* https://hechao.li/2017/12/13/linux-bridge-part1/
