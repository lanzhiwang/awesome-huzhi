# VLAN

## 基础知识

### 交换机端口类型

* access
* trunk

### 网卡模式

* 广播模式
* 多播传送
* 直接模式
* 混杂模式

## 配置 VLAN

配置 VLAN 方法：
1. 网卡配置文件
2. 使用 vconfig 命令
3. 使用 ip 命令

### 使用 vconfig 命令

```bash
# 增加 vlan
$ vconfig add eth0 100
$ vconfig add eth0 200

# 对 vlan100 和 vlan200 配置 ip
$ ifconfig eth0 up
$ ifconfig eth0.100 xx.xx.xx.xx netmask xx.xx.xx.xx

# 删除
$ vconfig rem vlan100
$ vconfig rem vlan200

```

### 使用 ip 命令

```bash
ip link add link DEVICE name NAME type vlan [ protocol VLAN_PROTO ] id VLANID [ reorder_hdr { on | off } ] [ gvrp { on | off } ] [ mvrp { on | off } ] [ loose_binding { on | off } ] [ ingress-qos-map QOS-MAP ] [ egress-qos-map QOS-MAP ]

ip link add link enp0s5 name enp0s5.200 type vlan id 200

```
