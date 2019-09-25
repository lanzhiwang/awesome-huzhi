# Linux 网络设备

## Linux 对常见网络设备的支持

[参考](https://www.systutorials.com/docs/linux/man/8-ip-link/)

### VLAN Type Support
```bash
ip link add link DEVICE name NAME type vlan [ protocol VLAN_PROTO ] id VLANID [ reorder_hdr { on | off } ] [ gvrp { on | off } ] [ mvrp { on | off } ] [ loose_binding { on | off } ] [ ingress-qos-map QOS-MAP ] [ egress-qos-map QOS-MAP ]

```

### VXLAN Type Support
```bash
ip link add DEVICE type vxlan id VNI [ dev PHYS_DEV ] [ { group | remote } IPADDR ] [ local { IPADDR | any } ] [ ttl TTL ] [ tos TOS ] [ flowlabel FLOWLABEL ] [ dstport PORT ] [ srcport MIN MAX ] [ [no]learning ] [ [no]proxy ] [ [no]rsc ] [ [no]l2miss ] [ [no]l3miss ] [ [no]udpcsum ] [ [no]udp6zerocsumtx ] [ [no]udp6zerocsumrx ] [ ageing SECONDS ] [ maxaddress NUMBER ] [ [no]external ] [ gbp ] [ gpe ]

```

### VETH, VXCAN Type Support
```bash
ip link add DEVICE type { veth | vxcan } [ peer name NAME ]

```

### GRE, IPIP, SIT, ERSPAN Type Support
```bash
ip link add DEVICE type { gre | ipip | sit | erspan } remote ADDR local ADDR [ encap { fou | gue | none } ] [ encap-sport { PORT | auto } ] [ encap-dport PORT ] [ [no]encap-csum ] [ [no]encap-remcsum ] [ mode { ip6ip | ipip | mplsip | any } ] [ erspan IDX ] [ external ]

```

### IP6GRE/IP6GRETAP Type Support
```bash
ip link add DEVICE type { ip6gre | ip6gretap } remote ADDR local ADDR [ [i|o]seq ] [ [i|o]key KEY ] [ [i|o]csum ] [ hoplimit TTL ] [ encaplimit ELIM ] [ tclass TCLASS ] [ flowlabel FLOWLABEL ] [ dscp inherit ] [ dev PHYS_DEV ]

```

### IPoIB Type Support
```bash
ip link add DEVICE name NAME type ipoib [ pkey PKEY ] [ mode MODE ]

```

### GENEVE Type Support
```bash
ip link add DEVICE type geneve id VNI remote IPADDR [ ttl TTL ] [ tos TOS ] [ flowlabel FLOWLABEL ] [ dstport PORT ] [ [no]external ] [ [no]udpcsum ] [ [no]udp6zerocsumtx ] [ [no]udp6zerocsumrx ]

```

### MACVLAN and MACVTAP Type Support
```bash
ip link add link DEVICE name NAME type { macvlan | macvtap } mode { private | vepa | bridge | passthru [ nopromisc ] | source }

```

### BRIDGE Type Support
```bash
ip link add DEVICE type bridge [ ageing_time AGEING_TIME ] [ group_fwd_mask MASK ] [ group_address ADDRESS ] [ forward_delay FORWARD_DELAY ] [ hello_time HELLO_TIME ] [ max_age MAX_AGE ] [ stp_state STP_STATE ] [ priority PRIORITY ] [ vlan_filtering VLAN_FILTERING ] [ vlan_protocol VLAN_PROTOCOL ] [ vlan_default_pvid VLAN_DEFAULT_PVID ] [ vlan_stats_enabled VLAN_STATS_ENABLED ] [ mcast_snooping MULTICAST_SNOOPING ] [ mcast_router MULTICAST_ROUTER ] [ mcast_query_use_ifaddr MCAST_QUERY_USE_IFADDR ] [ mcast_querier MULTICAST_QUERIER ] [ mcast_hash_elasticity HASH_ELASTICITY ] [ mcast_hash_max HASH_MAX ] [ mcast_last_member_count LAST_MEMBER_COUNT ] [ mcast_startup_query_count STARTUP_QUERY_COUNT ] [ mcast_last_member_interval LAST_MEMBER_INTERVAL ] [ mcast_membership_interval MEMBERSHIP_INTERVAL ] [ mcast_querier_interval QUERIER_INTERVAL ] [ mcast_query_interval QUERY_INTERVAL ] [ mcast_query_response_interval QUERY_RESPONSE_INTERVAL ] [ mcast_startup_query_interval STARTUP_QUERY_INTERVAL ] [ mcast_stats_enabled MCAST_STATS_ENABLED ] [ mcast_igmp_version IGMP_VERSION ] [ mcast_mld_version MLD_VERSION ] [ nf_call_iptables NF_CALL_IPTABLES ] [ nf_call_ip6tables NF_CALL_IP6TABLES ] [ nf_call_arptables NF_CALL_ARPTABLES ]

```

### MACsec Type Support
```bash
ip link add link DEVICE name NAME type macsec [ [ address <lladdr> ] port PORT | sci SCI ] [ cipher CIPHER_SUITE ] [ icvlen { 8..16 } ] [ encrypt { on | off } ] [ send_sci { on | off } ] [ end_station { on | off } ] [ scb { on | off } ] [ protect { on | off } ] [ replay { on | off } window { 0..2^32-1 } ] [ validate { strict | check | disabled } ] [ encodingsa { 0..3 } ]

```

### VRF Type Support
```bash
ip link add DEVICE type vrf table TABLE
```

## Linux 网络设备的说明

[参考](https://www.ibm.com/developerworks/cn/linux/1310_xiawc_networkdevice/index.html)

* Bridge
* VLAN ( Linux 里的 VLAN 设备是对 802.1.q 协议的一种内部软件实现 )
	* MACVLAN
	* 802.1.q VLAN
	* 802.1.qbg VLAN
	* 802.1.qbh VLAN
* TUN
* TAP
* VETH

## Linux 上配置网络设备命令举例

### Bridge

```bash
# 创建 Bridge
brctl addbr [BRIDGE NAME]

# 删除 Bridge
brctl delbr [BRIDGE NAME]

# attach 设备到 Bridge
brctl addif [BRIDGE NAME] [DEVICE NAME]

# 从 Bridge detach 设备
brctl delif [BRIDGE NAME] [DEVICE NAME]

# 查询 Bridge 情况
brctl show
```

### VLAN

```bash
# 创建 VLAN 设备
vconfig add [PARENT DEVICE NAME] [VLAN ID]

# 删除 VLAN 设备
vconfig rem [VLAN DEVICE NAME]

# 设置 VLAN 设备 flag
vconfig set_flag [VLAN DEVICE NAME] [FLAG] [VALUE]

# 设置 VLAN 设备 qos
vconfig set_egress_map [VLAN DEVICE NAME] [SKB_PRIORITY] [VLAN_QOS]
vconfig set_ingress_map [VLAN DEVICE NAME] [SKB_PRIORITY] [VLAN_QOS]

# 查询 VLAN 设备情况
cat /proc/net/vlan/[VLAN DEVICE NAME]
```

### VETH

```bash
# 创建 VETH 设备
ip link add link [DEVICE NAME] type veth
```

### TAP

```bash
# 创建 TAP 设备
tunctl -p [TAP DEVICE NAME]

# 删除 TAP 设备
tunctl -d [TAP DEVICE NAME]

# 查询系统里所有二层设备，包括 VETH/TAP 设备
ip link show

# 删除普通二层设备
ip link delete [DEVICE NAME] type [TYPE]
```

