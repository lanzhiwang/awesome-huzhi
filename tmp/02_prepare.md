## 集群所有节点的预配置

* 关闭或者卸载相关防火墙
* 关闭 selinux
* 安装基础软件包
* 禁用系统 swap
* 加载相关内核模块
* 设置系统参数
* 设置系统 ulimits

### 相关操作命令如下

```bash
# 删除 centos/redhat 默认安装的 firewalld、python-firewall、firewalld-filesystem

# 添加 EPEL 仓库

# 安装基础软件包
yum install conntrack-tools psmisc nfs-utils jq socat bash-completion rsync ipset ipvsadm

# 临时或者永久关闭 selinux
setenforce 0

/etc/selinux/config
"SELINUX=disabled"

# 禁用系统 swap
swapoff -a && sysctl -w vm.swappiness=0

# 注释 /etc/fstab 中的 swap 相关配置

# 加载相关内核模块
br_netfilter、ip_vs、ip_vs_rr、ip_vs_wrr、ip_vs_sh、nf_conntrack_ipv4、nf_conntrack

# 启用 systemd 自动加载模块服务

# 增加内核模块开机加载配置
cat /etc/modules-load.d/10-k8s-modules.conf
br_netfilter
ip_vs
ip_vs_rr
ip_vs_wrr
ip_vs_sh
nf_conntrack_ipv4
nf_conntrack

# 设置系统参数
cat /etc/sysctl.d/95-k8s-sysctl.conf
net.ipv4.ip_forward = 1
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-arptables = 1
# 
net.netfilter.nf_conntrack_max=1000000
vm.swappiness = 0
vm.max_map_count=655360
fs.file-max=655360

# 生效系统参数
sysctl -p /etc/sysctl.d/95-k8s-sysctl.conf

# 设置系统 ulimits
cat /etc/security/limits.d/30-k8s-ulimits.conf
* soft nofile 65536
* hard nofile 65536
* soft nproc 65536
* hard nproc 65536

mkdir -p /opt/kube/bin /etc/kubernetes/ssl

# 下载或者拷贝证书工具 CFSSL 到 /opt/kube/bin 目录

export PATH=/opt/kube/bin:$PATH

```

