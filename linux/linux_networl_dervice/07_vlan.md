# VLAN

```bash
ip link add link DEVICE name NAME type vlan [ protocol VLAN_PROTO ] id VLANID [ reorder_hdr { on | off } ] [ gvrp { on | off } ] [ mvrp { on | off } ] [ loose_binding { on | off } ] [ ingress-qos-map QOS-MAP ] [ egress-qos-map QOS-MAP ]


ip link add link enp0s5 name enp0s5.200 type vlan id 200


```