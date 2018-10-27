## iptables

#### iptables 中的表

iptables 包含 5 张表（tables）:

* `raw` 用于配置数据包，raw 中的数据包不会被系统跟踪。

* `filter` 用于存放所有与防火墙相关操作的默认表。

* `nat` 用于 网络地址转换（例如：端口转发）。

* `mangle` 用于对特定数据包的修改（参考 损坏数据包）。

* `security` 用于强制访问控制网络规则（例如： SELinux）。

notes:

大部分情况仅需要使用 filter 和 nat。其他表用于更复杂的情况——包括多路由和路由判


#### iptables 常见用法

##### 查看规则

```bash
# 通过 -t 指定要查看的表
$ iptables-save -t filter
$ iptables-save -t nat
$ iptables-save

$ iptables -t filter -nvL --line-number
$ iptables -t nat -nvL --line-number

```

##### 添加规则

```bash
# 在位置 7 添加一条规则
$ iptables -t filter -I INPUT 7 -i eth0 -p tcp -m tcp --dport 80 -j ACCEPT
-t 指定要添加表
-I 添加操作
INPUT 指定要添加的链
7 添加的规则在链中的位置
-i eth0 -p tcp -m tcp --dport 80 -j ACCEPT 添加的规则

```

##### 删除规则

```bash
# 删除第一条规则
$ iptables -t filter -D INPUT 1
```

##### 修改规则（修改规则的最佳做法是先删除该条规则，在重新添加）

```bash
# 将第七条规则修改为 drop
$ iptables -t filter -R INPUT 7 -j DROP

# 将第七条规则修改为 accept
$ iptables -t filter -R INPUT 7 -j ACCEPT

```


##### 创建自定义链

```bash
# 在 filter 表中创建自定义的链 DOCKER
$ iptables -t filter -N DOCKER

```

##### 使用自定义链

使用方法：
1. 为自定义链添加规则
2. 在默认链中通过 `-j` 参数引用自定义链
3. 引用后会按照自定义链中的规则处理数据包

```bash
# 在 INPUT 链中引用自定义的 INPUT_direct 链
-A INPUT -j INPUT_direct

# 在 FORWARD 链中引用自定义的 DOCKER 链
-A FORWARD -o br-12f5421c9cfd -j DOCKER
```


##### 在 iptables 规则中插入日志

1. 在需要写入日志的位置添加规则
2. 开启系统日志或者开启iptables的独立日志

```bash
# 第一步添加日志规则，和添加普通规则的方法一样，只是-j参数不同
$ iptables -I INPUT 1 -j LOG --log-prefix "iptables"
$ iptables -I FORWARD 1 -j LOG --log-prefix "iptables"

# 开启系统日志或者开启iptables的独立日志
不同的Linux发行版操作方法不同

```

##### iptables debugging

[参考1](https://backreference.org/2010/06/11/iptables-debugging/)
[参考2](https://github.com/lanzhiwang/awesome-huzhi/blob/master/iptables_debugging.pdf)

#### ebtables 常见用法

```bash
# 查看规则
ebtables-save
ebtables --list

# 添加规则
$ ebtables -t broute -A BROUTING    -p ipv4 --ip-proto 1 --log-level 6 --log-ip --log-prefix "TRACE: eb:broute:BROUTING" -j ACCEPT
$ ebtables -t nat    -A OUTPUT      -p ipv4 --ip-proto 1 --log-level 6 --log-ip --log-prefix "TRACE: eb:nat:OUTPUT"  -j ACCEPT
$ ebtables -t nat    -A PREROUTING  -p ipv4 --ip-proto 1 --log-level 6 --log-ip --log-prefix "TRACE: eb:nat:PREROUTING" -j ACCEPT
$ ebtables -t filter -A INPUT       -p ipv4 --ip-proto 1 --log-level 6 --log-ip --log-prefix "TRACE: eb:filter:INPUT" -j ACCEPT
$ ebtables -t filter -A FORWARD     -p ipv4 --ip-proto 1 --log-level 6 --log-ip --log-prefix "TRACE: eb:filter:FORWARD" -j ACCEPT
$ ebtables -t filter -A OUTPUT      -p ipv4 --ip-proto 1 --log-level 6 --log-ip --log-prefix "TRACE: eb:filter:OUTPUT" -j ACCEPT
$ ebtables -t nat    -A POSTROUTING -p ipv4 --ip-proto 1 --log-level 6 --log-ip --log-prefix "TRACE: eb:nat:POSTROUTING" -j ACCEPT

```
