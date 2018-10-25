## Docker 网络


#### Docker 网络原理

用于容器的网络技术与用于虚拟机的网络技术非常类似。在同一台主机上的容器可以连接到一个软件交换机上，iptables 可以用来控制容器之间的网络流量，并将在容器中运行的进程的端口暴露到宿主机上。

在默认安装情况下， Docker 会在宿主机上创建一个名为 docker0 的 Linux 网桥设备。该网桥设备拥有一个私有网络地址及其所属子网。分配给 docker0 网桥的子网地址为 172.[17-31].42.1/16、 10.[0-255].42.1/16 和 192.168.[42-44].1/24 中第一个没有被占用的子网地址。因此，很多时候你的 docker0 网桥设备的地址都是 172.17.42.1。所有容器都会连接到该网桥设备上，并从中分配一个位于子网 172.17.42.0/24 中的 IP 地址。容器链接到网桥的网络接口会把 docker0 网络设备作为网关。创建新容器时， Docker 会创建一对网络设备接口，并将它们放到两个独立的网络命名空间：一个网络设备放到容器的网络命名空间（即 eth0）；另一个网络设备放到宿主机的网络命名空间，并连接到 docker0 网桥设备上。


#### Docker网络类型

* default: 桥接

* 无网络模式 --net=none

* 主机模式 --net=host

* 与其他容器共享网络的模式 --net=container:CONTAINER_NAME_OR_ID


#### 自定义桥接模式

桥接模式如下图所示

![]()


```bash
# 显示系统中的所有设备，如下所示，docker进程默认创建了网桥设备 docker0，启动容器后创建了网络接口设备 vetha27f235@if6
[root@app5 ~]# ip -d link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00 promiscuity 0 addrgenmode eui64 
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT qlen 1000
    link/ether 52:54:00:dd:52:c9 brd ff:ff:ff:ff:ff:ff promiscuity 0 addrgenmode eui64 
3: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT 
    link/ether 02:42:6d:57:39:a4 brd ff:ff:ff:ff:ff:ff promiscuity 0 
    bridge forward_delay 1500 hello_time 200 max_age 2000 addrgenmode eui64 
7: vetha27f235@if6: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT 
    link/ether 72:7e:1c:97:7d:e7 brd ff:ff:ff:ff:ff:ff link-netnsid 0 promiscuity 1 
    veth 
    bridge_slave addrgenmode eui64 
[root@app5 ~]# 
# 显示所有的网桥设备，并且显示网桥设备与网络接口设备的连接关系
[root@app5 ~]# brctl show
bridge name	bridge id		STP enabled	interfaces
docker0		8000.02426d5739a4	no		vetha27f235
[root@app5 ~]# 

# 增加一个桥接设备 br0
[root@app5 ~]# brctl addbr br0
[root@app5 ~]# ip -d link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00 promiscuity 0 addrgenmode eui64 
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT qlen 1000
    link/ether 52:54:00:dd:52:c9 brd ff:ff:ff:ff:ff:ff promiscuity 0 addrgenmode eui64 
3: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT 
    link/ether 02:42:6d:57:39:a4 brd ff:ff:ff:ff:ff:ff promiscuity 0 
    bridge forward_delay 1500 hello_time 200 max_age 2000 addrgenmode eui64 
7: vetha27f235@if6: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT 
    link/ether 72:7e:1c:97:7d:e7 brd ff:ff:ff:ff:ff:ff link-netnsid 0 promiscuity 1 
    veth 
    bridge_slave addrgenmode eui64 
8: br0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT qlen 1000
    link/ether c6:14:45:c7:b8:2c brd ff:ff:ff:ff:ff:ff promiscuity 0 
    bridge forward_delay 1500 hello_time 200 max_age 2000 addrgenmode eui64 
[root@app5 ~]# brctl show
bridge name	bridge id		STP enabled	interfaces
br0		8000.000000000000	no		
docker0		8000.02426d5739a4	no		vetha27f235
[root@app5 ~]# 
[root@app5 ~]# ifconfig br0
br0: flags=4098<BROADCAST,MULTICAST>  mtu 1500
        ether c6:14:45:c7:b8:2c  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

[root@app5 ~]# 
[root@app5 ~]# 
# 添加 IP 地址到网桥设备 br0
[root@app5 ~]# ip addr add 192.168.1.254/24 dev br0
[root@app5 ~]# 
[root@app5 ~]# ifconfig br0
br0: flags=4098<BROADCAST,MULTICAST>  mtu 1500
        inet 192.168.1.254  netmask 255.255.255.0  broadcast 0.0.0.0
        ether c6:14:45:c7:b8:2c  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

[root@app5 ~]# 
# 启动网桥设备
[root@app5 ~]# sudo ip link set dev br0 up
[root@app5 ~]# 
[root@app5 ~]# ip -d link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00 promiscuity 0 addrgenmode eui64 
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT qlen 1000
    link/ether 52:54:00:dd:52:c9 brd ff:ff:ff:ff:ff:ff promiscuity 0 addrgenmode eui64 
3: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT 
    link/ether 02:42:6d:57:39:a4 brd ff:ff:ff:ff:ff:ff promiscuity 0 
    bridge forward_delay 1500 hello_time 200 max_age 2000 addrgenmode eui64 
7: vetha27f235@if6: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT 
    link/ether 72:7e:1c:97:7d:e7 brd ff:ff:ff:ff:ff:ff link-netnsid 0 promiscuity 1 
    veth 
    bridge_slave addrgenmode eui64 
8: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN mode DEFAULT qlen 1000
    link/ether c6:14:45:c7:b8:2c brd ff:ff:ff:ff:ff:ff promiscuity 0 
    bridge forward_delay 1500 hello_time 200 max_age 2000 addrgenmode eui64 
[root@app5 ~]# 

##################################################################

# 显示系统中的所有设备
[root@app5 ~]# ip -d link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00 promiscuity 0 addrgenmode eui64 
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT qlen 1000
    link/ether 52:54:00:dd:52:c9 brd ff:ff:ff:ff:ff:ff promiscuity 0 addrgenmode eui64 
3: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT 
    link/ether 02:42:6d:57:39:a4 brd ff:ff:ff:ff:ff:ff promiscuity 0 
    bridge forward_delay 1500 hello_time 200 max_age 2000 addrgenmode eui64 
7: vetha27f235@if6: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT 
    link/ether 72:7e:1c:97:7d:e7 brd ff:ff:ff:ff:ff:ff link-netnsid 0 promiscuity 1 
    veth 
    bridge_slave addrgenmode eui64 
8: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN mode DEFAULT qlen 1000
    link/ether c6:14:45:c7:b8:2c brd ff:ff:ff:ff:ff:ff promiscuity 0 
    bridge forward_delay 1500 hello_time 200 max_age 2000 addrgenmode eui64 
[root@app5 ~]# 
[root@app5 ~]# 
[root@app5 ~]# brctl show
bridge name	bridge id		STP enabled	interfaces
br0		8000.000000000000	no		
docker0		8000.02426d5739a4	no		vetha27f235
[root@app5 ~]# 
[root@app5 ~]# ifconfig -a
br0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.254  netmask 255.255.255.0  broadcast 0.0.0.0
        inet6 fe80::c414:45ff:fec7:b82c  prefixlen 64  scopeid 0x20<link>
        ether c6:14:45:c7:b8:2c  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 10  bytes 732 (732.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

docker0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.17.0.1  netmask 255.255.0.0  broadcast 172.17.255.255
        inet6 fe80::42:6dff:fe57:39a4  prefixlen 64  scopeid 0x20<link>
        ether 02:42:6d:57:39:a4  txqueuelen 0  (Ethernet)
        RX packets 15818792  bytes 908364316 (866.2 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 19793989  bytes 28824165288 (26.8 GiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.6.215  netmask 255.255.255.0  broadcast 192.168.6.255
        inet6 fe80::5054:ff:fedd:52c9  prefixlen 64  scopeid 0x20<link>
        ether 52:54:00:dd:52:c9  txqueuelen 1000  (Ethernet)
        RX packets 34590857  bytes 49745846892 (46.3 GiB)
        RX errors 0  dropped 6074  overruns 0  frame 0
        TX packets 22166558  bytes 3315476708 (3.0 GiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1  (Local Loopback)
        RX packets 1948  bytes 105670 (103.1 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 1948  bytes 105670 (103.1 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

vetha27f235: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet6 fe80::707e:1cff:fe97:7de7  prefixlen 64  scopeid 0x20<link>
        ether 72:7e:1c:97:7d:e7  txqueuelen 0  (Ethernet)
        RX packets 15818450  bytes 1129793036 (1.0 GiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 19793698  bytes 28823990490 (26.8 GiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

[root@app5 ~]# 

##################################################################

# 创建网络接口设备对 foo、 bar
[root@app5 ~]# sudo ip link add foo type veth peer name bar
[root@app5 ~]# 
[root@app5 ~]# ip -d link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00 promiscuity 0 addrgenmode eui64 
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT qlen 1000
    link/ether 52:54:00:dd:52:c9 brd ff:ff:ff:ff:ff:ff promiscuity 0 addrgenmode eui64 
3: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT 
    link/ether 02:42:6d:57:39:a4 brd ff:ff:ff:ff:ff:ff promiscuity 0 
    bridge forward_delay 1500 hello_time 200 max_age 2000 addrgenmode eui64 
7: vetha27f235@if6: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT 
    link/ether 72:7e:1c:97:7d:e7 brd ff:ff:ff:ff:ff:ff link-netnsid 0 promiscuity 1 
    veth 
    bridge_slave addrgenmode eui64 
8: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN mode DEFAULT qlen 1000
    link/ether c6:14:45:c7:b8:2c brd ff:ff:ff:ff:ff:ff promiscuity 0 
    bridge forward_delay 1500 hello_time 200 max_age 2000 addrgenmode eui64 
9: bar@foo: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 qdisc noop state DOWN mode DEFAULT qlen 1000
    link/ether aa:b6:4f:d1:ab:69 brd ff:ff:ff:ff:ff:ff promiscuity 0 
    veth addrgenmode eui64 
10: foo@bar: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 qdisc noop state DOWN mode DEFAULT qlen 1000
    link/ether 56:5a:ea:6b:f1:67 brd ff:ff:ff:ff:ff:ff promiscuity 0 
    veth addrgenmode eui64 
[root@app5 ~]# 
[root@app5 ~]# brctl show
bridge name	bridge id		STP enabled	interfaces
br0		8000.000000000000	no		
docker0		8000.02426d5739a4	no		vetha27f235
[root@app5 ~]# 
[root@app5 ~]# ifconfig -a
bar: flags=4098<BROADCAST,MULTICAST>  mtu 1500
        ether aa:b6:4f:d1:ab:69  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

br0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.254  netmask 255.255.255.0  broadcast 0.0.0.0
        inet6 fe80::c414:45ff:fec7:b82c  prefixlen 64  scopeid 0x20<link>
        ether c6:14:45:c7:b8:2c  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 10  bytes 732 (732.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

docker0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.17.0.1  netmask 255.255.0.0  broadcast 172.17.255.255
        inet6 fe80::42:6dff:fe57:39a4  prefixlen 64  scopeid 0x20<link>
        ether 02:42:6d:57:39:a4  txqueuelen 0  (Ethernet)
        RX packets 15818792  bytes 908364316 (866.2 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 19793989  bytes 28824165288 (26.8 GiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.6.215  netmask 255.255.255.0  broadcast 192.168.6.255
        inet6 fe80::5054:ff:fedd:52c9  prefixlen 64  scopeid 0x20<link>
        ether 52:54:00:dd:52:c9  txqueuelen 1000  (Ethernet)
        RX packets 34591210  bytes 49745877755 (46.3 GiB)
        RX errors 0  dropped 6074  overruns 0  frame 0
        TX packets 22166637  bytes 3315490466 (3.0 GiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

foo: flags=4098<BROADCAST,MULTICAST>  mtu 1500
        ether 56:5a:ea:6b:f1:67  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1  (Local Loopback)
        RX packets 1948  bytes 105670 (103.1 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 1948  bytes 105670 (103.1 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

vetha27f235: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet6 fe80::707e:1cff:fe97:7de7  prefixlen 64  scopeid 0x20<link>
        ether 72:7e:1c:97:7d:e7  txqueuelen 0  (Ethernet)
        RX packets 15818450  bytes 1129793036 (1.0 GiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 19793698  bytes 28823990490 (26.8 GiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

[root@app5 ~]# 
# 将 foo 连接到网桥 br0 上
[root@app5 ~]# brctl addif br0 foo
[root@app5 ~]# 
[root@app5 ~]# ip -d link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00 promiscuity 0 addrgenmode eui64 
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT qlen 1000
    link/ether 52:54:00:dd:52:c9 brd ff:ff:ff:ff:ff:ff promiscuity 0 addrgenmode eui64 
3: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT 
    link/ether 02:42:6d:57:39:a4 brd ff:ff:ff:ff:ff:ff promiscuity 0 
    bridge forward_delay 1500 hello_time 200 max_age 2000 addrgenmode eui64 
7: vetha27f235@if6: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT 
    link/ether 72:7e:1c:97:7d:e7 brd ff:ff:ff:ff:ff:ff link-netnsid 0 promiscuity 1 
    veth 
    bridge_slave addrgenmode eui64 
8: br0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT qlen 1000
    link/ether 56:5a:ea:6b:f1:67 brd ff:ff:ff:ff:ff:ff promiscuity 0 
    bridge forward_delay 1500 hello_time 200 max_age 2000 addrgenmode eui64 
9: bar@foo: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 qdisc noop state DOWN mode DEFAULT qlen 1000
    link/ether aa:b6:4f:d1:ab:69 brd ff:ff:ff:ff:ff:ff promiscuity 0 
    veth addrgenmode eui64 
10: foo@bar: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 qdisc noop master br0 state DOWN mode DEFAULT qlen 1000
    link/ether 56:5a:ea:6b:f1:67 brd ff:ff:ff:ff:ff:ff promiscuity 1 
    veth 
    bridge_slave addrgenmode eui64 
[root@app5 ~]# 
[root@app5 ~]# brctl show
bridge name	bridge id		STP enabled	interfaces
br0		8000.565aea6bf167	no		foo
docker0		8000.02426d5739a4	no		vetha27f235
[root@app5 ~]# 
[root@app5 ~]# ifconfig -a
bar: flags=4098<BROADCAST,MULTICAST>  mtu 1500
        ether aa:b6:4f:d1:ab:69  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

br0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 192.168.1.254  netmask 255.255.255.0  broadcast 0.0.0.0
        inet6 fe80::c414:45ff:fec7:b82c  prefixlen 64  scopeid 0x20<link>
        ether 56:5a:ea:6b:f1:67  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 10  bytes 732 (732.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

docker0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.17.0.1  netmask 255.255.0.0  broadcast 172.17.255.255
        inet6 fe80::42:6dff:fe57:39a4  prefixlen 64  scopeid 0x20<link>
        ether 02:42:6d:57:39:a4  txqueuelen 0  (Ethernet)
        RX packets 15818792  bytes 908364316 (866.2 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 19793989  bytes 28824165288 (26.8 GiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.6.215  netmask 255.255.255.0  broadcast 192.168.6.255
        inet6 fe80::5054:ff:fedd:52c9  prefixlen 64  scopeid 0x20<link>
        ether 52:54:00:dd:52:c9  txqueuelen 1000  (Ethernet)
        RX packets 34591429  bytes 49745897905 (46.3 GiB)
        RX errors 0  dropped 6074  overruns 0  frame 0
        TX packets 22166688  bytes 3315501712 (3.0 GiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

foo: flags=4098<BROADCAST,MULTICAST>  mtu 1500
        ether 56:5a:ea:6b:f1:67  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1  (Local Loopback)
        RX packets 1948  bytes 105670 (103.1 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 1948  bytes 105670 (103.1 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

vetha27f235: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet6 fe80::707e:1cff:fe97:7de7  prefixlen 64  scopeid 0x20<link>
        ether 72:7e:1c:97:7d:e7  txqueuelen 0  (Ethernet)
        RX packets 15818450  bytes 1129793036 (1.0 GiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 19793698  bytes 28823990490 (26.8 GiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

[root@app5 ~]# 
# 启动网络设备 foo
[root@app5 ~]# ip link set foo up
[root@app5 ~]# 
[root@app5 ~]# ip -d link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00 promiscuity 0 addrgenmode eui64 
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT qlen 1000
    link/ether 52:54:00:dd:52:c9 brd ff:ff:ff:ff:ff:ff promiscuity 0 addrgenmode eui64 
3: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT 
    link/ether 02:42:6d:57:39:a4 brd ff:ff:ff:ff:ff:ff promiscuity 0 
    bridge forward_delay 1500 hello_time 200 max_age 2000 addrgenmode eui64 
7: vetha27f235@if6: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT 
    link/ether 72:7e:1c:97:7d:e7 brd ff:ff:ff:ff:ff:ff link-netnsid 0 promiscuity 1 
    veth 
    bridge_slave addrgenmode eui64 
8: br0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT qlen 1000
    link/ether 56:5a:ea:6b:f1:67 brd ff:ff:ff:ff:ff:ff promiscuity 0 
    bridge forward_delay 1500 hello_time 200 max_age 2000 addrgenmode eui64 
9: bar@foo: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT qlen 1000
    link/ether aa:b6:4f:d1:ab:69 brd ff:ff:ff:ff:ff:ff promiscuity 0 
    veth addrgenmode eui64 
10: foo@bar: <NO-CARRIER,BROADCAST,MULTICAST,UP,M-DOWN> mtu 1500 qdisc noqueue master br0 state LOWERLAYERDOWN mode DEFAULT qlen 1000
    link/ether 56:5a:ea:6b:f1:67 brd ff:ff:ff:ff:ff:ff promiscuity 1 
    veth 
    bridge_slave addrgenmode eui64 
[root@app5 ~]# 
[root@app5 ~]# brctl show
bridge name	bridge id		STP enabled	interfaces
br0		8000.565aea6bf167	no		foo
docker0		8000.02426d5739a4	no		vetha27f235
[root@app5 ~]# 
[root@app5 ~]# ifconfig -a
bar: flags=4098<BROADCAST,MULTICAST>  mtu 1500
        ether aa:b6:4f:d1:ab:69  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

br0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 192.168.1.254  netmask 255.255.255.0  broadcast 0.0.0.0
        inet6 fe80::c414:45ff:fec7:b82c  prefixlen 64  scopeid 0x20<link>
        ether 56:5a:ea:6b:f1:67  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 10  bytes 732 (732.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

docker0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.17.0.1  netmask 255.255.0.0  broadcast 172.17.255.255
        inet6 fe80::42:6dff:fe57:39a4  prefixlen 64  scopeid 0x20<link>
        ether 02:42:6d:57:39:a4  txqueuelen 0  (Ethernet)
        RX packets 15818792  bytes 908364316 (866.2 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 19793989  bytes 28824165288 (26.8 GiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.6.215  netmask 255.255.255.0  broadcast 192.168.6.255
        inet6 fe80::5054:ff:fedd:52c9  prefixlen 64  scopeid 0x20<link>
        ether 52:54:00:dd:52:c9  txqueuelen 1000  (Ethernet)
        RX packets 34591671  bytes 49745919566 (46.3 GiB)
        RX errors 0  dropped 6074  overruns 0  frame 0
        TX packets 22166735  bytes 3315512194 (3.0 GiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

foo: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        ether 56:5a:ea:6b:f1:67  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1  (Local Loopback)
        RX packets 1948  bytes 105670 (103.1 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 1948  bytes 105670 (103.1 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

vetha27f235: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet6 fe80::707e:1cff:fe97:7de7  prefixlen 64  scopeid 0x20<link>
        ether 72:7e:1c:97:7d:e7  txqueuelen 0  (Ethernet)
        RX packets 15818450  bytes 1129793036 (1.0 GiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 19793698  bytes 28823990490 (26.8 GiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

[root@app5 ~]# 

##################################################################

# 启动无网络的容器
[root@app5 ~]# docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS                    NAMES
0acee6d89d3f        guangdian:v0.0.2    "/bin/bash"         5 days ago          Up 5 days           0.0.0.0:8088->8088/tcp   gd-algo
[root@app5 ~]# 
[root@app5 ~]# ll /var/run/docker/netns
total 0
-r--r--r-- 1 root root 0 Oct 19 17:23 4ddace7f50ea
[root@app5 ~]# 

[root@app5 ~]# docker run -it --rm --net none --name cookbook ubuntu:14.04 bash
Unable to find image 'ubuntu:14.04' locally
14.04: Pulling from library/ubuntu
027274c8e111: Pull complete 
d3f9339a1359: Pull complete 
872f75707cf4: Pull complete 
dd5eed9f50d5: Pull complete 
Digest: sha256:e6e808ab8c62f1d9181817aea804ae4ba0897b8bd3661d36dbc329b5851b5637
Status: Downloaded newer image for ubuntu:14.04
root@d99498f7d4cd:/# 
# 容器中只有 lo 设备
root@d99498f7d4cd:/# ifconfig -a
lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

root@d99498f7d4cd:/# 


```

```bash
# 容器 cookbook 网络命名空间的 ID
[root@app5 ~]# docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS                    NAMES
d99498f7d4cd        ubuntu:14.04        "bash"              36 seconds ago      Up 34 seconds                                cookbook
0acee6d89d3f        guangdian:v0.0.2    "/bin/bash"         5 days ago          Up 5 days           0.0.0.0:8088->8088/tcp   gd-algo
[root@app5 ~]# 
[root@app5 ~]# ll /var/run/docker/netns
total 0
-r--r--r-- 1 root root 0 Oct 19 17:23 4ddace7f50ea
-r--r--r-- 1 root root 0 Oct 25 15:44 cc0d7ac3ded1
[root@app5 ~]# 
[root@app5 ~]# docker inspect -f '{{.NetworkSettings.SandboxKey}}' cookbook
/var/run/docker/netns/cc0d7ac3ded1
[root@app5 ~]# 
[root@app5 ~]# docker inspect cookbook | grep SandboxKey
            "SandboxKey": "/var/run/docker/netns/cc0d7ac3ded1",
[root@app5 ~]# 
# 为了使用 ip 命令需要创建一个软连接
[root@app5 ~]# cd /var/run
[root@app5 run]# pwd
/var/run
[root@app5 run]# ip netns
[root@app5 run]# ln -s /var/run/docker/netns netns
[root@app5 run]# ip netns
cc0d7ac3ded1
4ddace7f50ea (id: 0)
[root@app5 run]# 
# 将容器 cookbook 网络命名空间的 ID设置为变量
[root@app5 run]# NID=cc0d7ac3ded1
[root@app5 run]# echo ${NID}
cc0d7ac3ded1
[root@app5 run]# 

```


```bash
# 将网络接口设备 bar 放入到容器的命名空间中
[root@app5 run]# ip link set bar netns ${NID}
[root@app5 run]# 
# 启动 bar 设备
[root@app5 run]# ip link set foo up
[root@app5 run]# 
[root@app5 run]# 
# 在主机中没有了 bar 设备
[root@app5 run]# ip -d link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00 promiscuity 0 addrgenmode eui64 
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT qlen 1000
    link/ether 52:54:00:dd:52:c9 brd ff:ff:ff:ff:ff:ff promiscuity 0 addrgenmode eui64 
3: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT 
    link/ether 02:42:6d:57:39:a4 brd ff:ff:ff:ff:ff:ff promiscuity 0 
    bridge forward_delay 1500 hello_time 200 max_age 2000 addrgenmode eui64 
7: vetha27f235@if6: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT 
    link/ether 72:7e:1c:97:7d:e7 brd ff:ff:ff:ff:ff:ff link-netnsid 0 promiscuity 1 
    veth 
    bridge_slave addrgenmode eui64 
8: br0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT qlen 1000
    link/ether 56:5a:ea:6b:f1:67 brd ff:ff:ff:ff:ff:ff promiscuity 0 
    bridge forward_delay 1500 hello_time 200 max_age 2000 addrgenmode eui64 
10: foo@if9: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue master br0 state LOWERLAYERDOWN mode DEFAULT qlen 1000
    link/ether 56:5a:ea:6b:f1:67 brd ff:ff:ff:ff:ff:ff link-netnsid 1 promiscuity 1 
    veth 
    bridge_slave addrgenmode eui64 
[root@app5 run]# 
[root@app5 run]# brctl show
bridge name	bridge id		STP enabled	interfaces
br0		8000.565aea6bf167	no		foo
docker0		8000.02426d5739a4	no		vetha27f235
[root@app5 run]# 
[root@app5 run]# ifconfig -a
br0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 192.168.1.254  netmask 255.255.255.0  broadcast 0.0.0.0
        inet6 fe80::c414:45ff:fec7:b82c  prefixlen 64  scopeid 0x20<link>
        ether 56:5a:ea:6b:f1:67  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 10  bytes 732 (732.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

docker0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.17.0.1  netmask 255.255.0.0  broadcast 172.17.255.255
        inet6 fe80::42:6dff:fe57:39a4  prefixlen 64  scopeid 0x20<link>
        ether 02:42:6d:57:39:a4  txqueuelen 0  (Ethernet)
        RX packets 15818792  bytes 908364316 (866.2 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 19793989  bytes 28824165288 (26.8 GiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.6.215  netmask 255.255.255.0  broadcast 192.168.6.255
        inet6 fe80::5054:ff:fedd:52c9  prefixlen 64  scopeid 0x20<link>
        ether 52:54:00:dd:52:c9  txqueuelen 1000  (Ethernet)
        RX packets 34649792  bytes 49817309991 (46.3 GiB)
        RX errors 0  dropped 6074  overruns 0  frame 0
        TX packets 22198937  bytes 3317753983 (3.0 GiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

foo: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        ether 56:5a:ea:6b:f1:67  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1  (Local Loopback)
        RX packets 1952  bytes 105886 (103.4 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 1952  bytes 105886 (103.4 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

vetha27f235: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet6 fe80::707e:1cff:fe97:7de7  prefixlen 64  scopeid 0x20<link>
        ether 72:7e:1c:97:7d:e7  txqueuelen 0  (Ethernet)
        RX packets 15818450  bytes 1129793036 (1.0 GiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 19793698  bytes 28823990490 (26.8 GiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

[root@app5 run]# 

# 在容器中出现 bar 设备
root@d99498f7d4cd:/# ifconfig -a
bar       Link encap:Ethernet  HWaddr aa:b6:4f:d1:ab:69  
          BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

root@d99498f7d4cd:/# 

# 将容器中的 bar 设备重命名为 eth1
[root@app5 run]# ip netns exec ${NID} ip link set dev bar name eth1
[root@app5 run]# 
root@d99498f7d4cd:/# ifconfig -a
eth1      Link encap:Ethernet  HWaddr aa:b6:4f:d1:ab:69  
          BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

root@d99498f7d4cd:/# ip address
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
9: eth1@if10: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether aa:b6:4f:d1:ab:69 brd ff:ff:ff:ff:ff:ff
root@d99498f7d4cd:/# 

# 设置容器中 eth1 设备的 MAC 地址
[root@app5 run]# ip netns exec ${NID} ip link set eth1 address 12:34:56:78:9a:bc
[root@app5 run]# 
root@d99498f7d4cd:/# ifconfig -a
eth1      Link encap:Ethernet  HWaddr 12:34:56:78:9a:bc  
          BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

root@d99498f7d4cd:/# ip address
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
9: eth1@if10: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 12:34:56:78:9a:bc brd ff:ff:ff:ff:ff:ff
root@d99498f7d4cd:/# 

# 启动容器中的 eth1 设备
[root@app5 run]# ip netns exec ${NID} ip link set eth1 up
[root@app5 run]# 
root@d99498f7d4cd:/# ifconfig -a
eth1      Link encap:Ethernet  HWaddr 12:34:56:78:9a:bc  
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:7 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:578 (578.0 B)  TX bytes:0 (0.0 B)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

root@d99498f7d4cd:/# ip address
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
9: eth1@if10: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 12:34:56:78:9a:bc brd ff:ff:ff:ff:ff:ff
root@d99498f7d4cd:/# 

# 设置容器中 eth1 的 IP 地址
[root@app5 run]# ip netns exec ${NID} ip addr add 192.168.1.1/24 dev eth1
[root@app5 run]# 
root@d99498f7d4cd:/# ifconfig -a
eth1      Link encap:Ethernet  HWaddr 12:34:56:78:9a:bc  
          inet addr:192.168.1.1  Bcast:0.0.0.0  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:8 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:648 (648.0 B)  TX bytes:0 (0.0 B)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

root@d99498f7d4cd:/# ip address
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
9: eth1@if10: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 12:34:56:78:9a:bc brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.1/24 scope global eth1
       valid_lft forever preferred_lft forever
root@d99498f7d4cd:/# 

# 设置容器中 eth1 的路由
[root@app5 run]# ip netns exec ${NID} ip route add default via 192.168.1.254
[root@app5 run]# 
root@d99498f7d4cd:/# ifconfig -a
eth1      Link encap:Ethernet  HWaddr 12:34:56:78:9a:bc  
          inet addr:192.168.1.1  Bcast:0.0.0.0  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:8 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:648 (648.0 B)  TX bytes:0 (0.0 B)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

root@d99498f7d4cd:/# ip address
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
9: eth1@if10: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 12:34:56:78:9a:bc brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.1/24 scope global eth1
       valid_lft forever preferred_lft forever
root@d99498f7d4cd:/# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.1.254   0.0.0.0         UG    0      0        0 eth1
192.168.1.0     0.0.0.0         255.255.255.0   U     0      0        0 eth1
root@d99498f7d4cd:/# 

# 为了使容器访问外网，在主机中设置 iptables 的 nat 规则
[root@app5 run]# iptables-save -t nat
# Generated by iptables-save v1.4.21 on Thu Oct 25 16:22:44 2018
*nat
:PREROUTING ACCEPT [1054888:65681248]
:INPUT ACCEPT [8764:767596]
:OUTPUT ACCEPT [2566:179244]
:POSTROUTING ACCEPT [14276:881556]
:DOCKER - [0:0]
-A PREROUTING -m addrtype --dst-type LOCAL -j DOCKER
-A OUTPUT ! -d 127.0.0.0/8 -m addrtype --dst-type LOCAL -j DOCKER
-A POSTROUTING -s 172.17.0.0/16 ! -o docker0 -j MASQUERADE
-A POSTROUTING -s 172.17.0.2/32 -d 172.17.0.2/32 -p tcp -m tcp --dport 8088 -j MASQUERADE
-A DOCKER -i docker0 -j RETURN
-A DOCKER ! -i docker0 -p tcp -m tcp --dport 8088 -j DNAT --to-destination 172.17.0.2:8088
COMMIT
# Completed on Thu Oct 25 16:22:44 2018
[root@app5 run]# 
[root@app5 run]# iptables -t nat -A POSTROUTING -s 192.168.0.0/24 -j MASQUERADE
[root@app5 run]# iptables-save -t nat
# Generated by iptables-save v1.4.21 on Thu Oct 25 16:35:30 2018
*nat
:PREROUTING ACCEPT [12:1276]
:INPUT ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
:POSTROUTING ACCEPT [0:0]
:DOCKER - [0:0]
-A PREROUTING -m addrtype --dst-type LOCAL -j DOCKER
-A OUTPUT ! -d 127.0.0.0/8 -m addrtype --dst-type LOCAL -j DOCKER
-A POSTROUTING -s 172.17.0.0/16 ! -o docker0 -j MASQUERADE
-A POSTROUTING -s 172.17.0.2/32 -d 172.17.0.2/32 -p tcp -m tcp --dport 8088 -j MASQUERADE
-A POSTROUTING -s 192.168.0.0/24 -j MASQUERADE
-A DOCKER -i docker0 -j RETURN
-A DOCKER ! -i docker0 -p tcp -m tcp --dport 8088 -j DNAT --to-destination 172.17.0.2:8088
COMMIT
# Completed on Thu Oct 25 16:35:30 2018
[root@app5 run]# 


```