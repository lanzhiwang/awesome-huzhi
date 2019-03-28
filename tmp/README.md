容器云平台构建
需求：
1、基于kubernetes 1.14版本构建高可用集群
2、Worker节点需要支持linux与windows主机
3、节点网络互通
4、[支持ES集群部署、更新、回滚](https://blog.csdn.net/chenleiking/article/details/79453460)
5、部署高可用sqlserver集群
6、部署gitlab高可用集群
7、编写服务python服务，可通过ingress方式访问此服务，并且此服务可以与es/sqlserver/gitlab交互，通过 gitlab 接口访问
将以上要求具体步骤与结构汇聚成文档，如果条件允许最好有实际演示环境



* kubernetes worker 节点怎样使用 windows
* 私有镜像库，怎样配置 kubernetes 使用 公有镜像库，将镜像导入私库或者你的所有k8s节点上的docker内。
* 怎样做到高可用
* https://dl.k8s.io/v1.14.0/kubernetes-server-linux-amd64.tar.gz

###

* 集群确保各节点时区设置一致、时间同步
* 配置基础网络、更新源、SSH登陆等



### 节点规划

```
[deploy]
192.168.1.1 NTP_ENABLED=no

# etcd集群请提供如下NODE_NAME，注意etcd集群必须是1,3,5,7...奇数个节点
[etcd]
192.168.1.1 NODE_NAME=etcd1
192.168.1.2 NODE_NAME=etcd2
192.168.1.3 NODE_NAME=etcd3

[kube-master]
192.168.1.1
192.168.1.2

[kube-node]
192.168.1.3
192.168.1.4

# 参数 NEW_INSTALL：yes表示新建，no表示使用已有harbor服务器
# 如果不使用域名，可以设置 HARBOR_DOMAIN=""
[harbor]
#192.168.1.8 HARBOR_DOMAIN="harbor.yourdomain.com" NEW_INSTALL=no

# 负载均衡(目前已支持多于2节点，一般2节点就够了) 安装 haproxy+keepalived
[lb]
192.168.1.1 LB_ROLE=backup
192.168.1.2 LB_ROLE=master
```



1. 在节点上安装 chrony 服务，启动服务端和客户端
2. 关闭 selinux 和 防火墙，安装 conntrack-tools、psmisc、nfs-utils、jq、socat、bash-completion、rsync、ipset、ipvsadm
3. 安装 haproxy、keepalived
   - name: 安装 keepalived

```bash
yum install epel-release -y
yum update

ssh-keygen -t rsa -b 2048 回车 回车 回车
ssh-copy-id $IPs #$IPs为所有节点地址包括自身，按照提示输入yes 和root密码

lanzhiwang@lanzhiwang-desktop:~$ ll /etc/ansible
total 32
drwxr-xr-x   2 root root  4096 2月  11 14:19 ./
drwxr-xr-x 140 root root 12288 3月  27 09:39 ../
-rw-r--r--   1 root root 10301 1月  15  2016 ansible.cfg
-rw-r--r--   1 root root   982 8月  21  2018 hosts
lanzhiwang@lanzhiwang-desktop:~$ 

lanzhiwang@lanzhiwang-desktop:~$ ll /etc/ansible
total 132
drwxr-xr-x  11 root       root        4096 3月  28 22:45 ./
drwxr-xr-x 140 root       root       12288 3月  27 09:39 ../
-rw-rw-r--   1 lanzhiwang lanzhiwang   499 3月  28 22:43 01.prepare.yml
-rw-rw-r--   1 lanzhiwang lanzhiwang    58 3月  28 22:43 02.etcd.yml
-rw-rw-r--   1 lanzhiwang lanzhiwang    87 3月  28 22:43 03.docker.yml
-rw-rw-r--   1 lanzhiwang lanzhiwang   532 3月  28 22:43 04.kube-master.yml
-rw-rw-r--   1 lanzhiwang lanzhiwang    72 3月  28 22:43 05.kube-node.yml
-rw-rw-r--   1 lanzhiwang lanzhiwang   346 3月  28 22:43 06.network.yml
-rw-rw-r--   1 lanzhiwang lanzhiwang    77 3月  28 22:43 07.cluster-addon.yml
-rw-rw-r--   1 lanzhiwang lanzhiwang  1521 3月  28 22:43 11.harbor.yml
-rw-rw-r--   1 lanzhiwang lanzhiwang   411 3月  28 22:43 22.upgrade.yml
-rw-rw-r--   1 lanzhiwang lanzhiwang  1394 3月  28 22:43 23.backup.yml
-rw-rw-r--   1 lanzhiwang lanzhiwang  1391 3月  28 22:43 24.restore.yml
-rw-rw-r--   1 lanzhiwang lanzhiwang  1723 3月  28 22:43 90.setup.yml
-rw-rw-r--   1 lanzhiwang lanzhiwang  5941 3月  28 22:43 99.clean.yml
-rw-rw-r--   1 lanzhiwang lanzhiwang 10283 3月  28 22:43 ansible.cfg
drwxrwxr-x   2 lanzhiwang lanzhiwang  4096 3月  28 22:43 bin/
drwxrwxr-x   4 lanzhiwang lanzhiwang  4096 3月  28 22:43 dockerfiles/
drwxrwxr-x   8 lanzhiwang lanzhiwang  4096 3月  28 22:43 docs/
drwxrwxr-x   2 lanzhiwang lanzhiwang  4096 3月  28 22:43 down/
drwxrwxr-x   2 lanzhiwang lanzhiwang  4096 3月  28 22:43 example/
-rw-r--r--   1 root       root         982 8月  21  2018 hosts
drwxrwxr-x  14 lanzhiwang lanzhiwang  4096 3月  28 22:43 manifests/
drwxrwxr-x   2 lanzhiwang lanzhiwang  4096 3月  28 22:43 pics/
-rw-rw-r--   1 lanzhiwang lanzhiwang  5056 3月  28 22:43 README.md
drwxrwxr-x  22 lanzhiwang lanzhiwang  4096 3月  28 22:43 roles/
drwxrwxr-x   2 lanzhiwang lanzhiwang  4096 3月  28 22:43 tools/
lanzhiwang@lanzhiwang-desktop:~$ 

lanzhiwang@lanzhiwang-desktop:~$ ll /etc/ansible/bin
total 1569764
drwxrwxr-x  2 lanzhiwang lanzhiwang      4096 3月  28 23:01 ./
drwxr-xr-x 11 root       root            4096 3月  28 22:45 ../
-rwxr-xr-x  1 lanzhiwang lanzhiwang  42785408 3月  28 23:00 apiextensions-apiserver*
-rwxr-xr-x  1 lanzhiwang lanzhiwang 100320960 3月  28 23:00 cloud-controller-manager*
-rw-r--r--  1 lanzhiwang lanzhiwang         8 3月  28 23:00 cloud-controller-manager.docker_tag
-rw-r--r--  1 lanzhiwang lanzhiwang 144212480 3月  28 23:00 cloud-controller-manager.tar
-rwxr-xr-x  1 lanzhiwang lanzhiwang 211089600 3月  28 23:00 hyperkube*
-rwxr-xr-x  1 lanzhiwang lanzhiwang  39574816 3月  28 23:00 kubeadm*
-rwxr-xr-x  1 lanzhiwang lanzhiwang 167464288 3月  28 23:00 kube-apiserver*
-rw-r--r--  1 lanzhiwang lanzhiwang         8 3月  28 23:00 kube-apiserver.docker_tag
-rw-r--r--  1 lanzhiwang lanzhiwang 211355648 3月  28 23:00 kube-apiserver.tar
-rwxr-xr-x  1 lanzhiwang lanzhiwang 115497504 3月  28 23:00 kube-controller-manager*
-rw-r--r--  1 lanzhiwang lanzhiwang         8 3月  28 23:00 kube-controller-manager.docker_tag
-rw-r--r--  1 lanzhiwang lanzhiwang 159389184 3月  28 23:00 kube-controller-manager.tar
-rwxr-xr-x  1 lanzhiwang lanzhiwang  43103040 3月  28 23:00 kubectl*
-rwxr-xr-x  1 lanzhiwang lanzhiwang 127850432 3月  28 23:01 kubelet*
-rwxr-xr-x  1 lanzhiwang lanzhiwang  36681344 3月  28 23:01 kube-proxy*
-rw-r--r--  1 lanzhiwang lanzhiwang         8 3月  28 23:01 kube-proxy.docker_tag
-rw-r--r--  1 lanzhiwang lanzhiwang  83978752 3月  28 23:01 kube-proxy.tar
-rwxr-xr-x  1 lanzhiwang lanzhiwang  39254208 3月  28 23:01 kube-scheduler*
-rw-r--r--  1 lanzhiwang lanzhiwang         8 3月  28 23:01 kube-scheduler.docker_tag
-rw-r--r--  1 lanzhiwang lanzhiwang  83145728 3月  28 23:01 kube-scheduler.tar
-rwxr-xr-x  1 lanzhiwang lanzhiwang   1648224 3月  28 23:01 mounter*
-rwxrwxr-x  1 lanzhiwang lanzhiwang       171 3月  28 22:43 readme.md*
lanzhiwang@lanzhiwang-desktop:~$ 



# 集群部署节点：一般为运行ansible 脚本的节点
# 变量 NTP_ENABLED (=yes/no) 设置集群是否安装 chrony 时间同步
[deploy]
192.168.1.1 NTP_ENABLED=no

# etcd集群请提供如下NODE_NAME，注意etcd集群必须是1,3,5,7...奇数个节点
[etcd]
192.168.1.1 NODE_NAME=etcd1
192.168.1.2 NODE_NAME=etcd2
192.168.1.3 NODE_NAME=etcd3

[kube-master]
192.168.1.1
192.168.1.2

[kube-node]
192.168.1.3
192.168.1.4

# 参数 NEW_INSTALL：yes表示新建，no表示使用已有harbor服务器
# 如果不使用域名，可以设置 HARBOR_DOMAIN=""
[harbor]
#192.168.1.8 HARBOR_DOMAIN="harbor.yourdomain.com" NEW_INSTALL=no

# 负载均衡(目前已支持多于2节点，一般2节点就够了) 安装 haproxy+keepalived
[lb]
192.168.1.1 LB_ROLE=backup
192.168.1.2 LB_ROLE=master

#【可选】外部负载均衡，用于自有环境负载转发 NodePort 暴露的服务等
[ex-lb]
#192.168.1.6 LB_ROLE=backup EX_VIP=192.168.1.250
#192.168.1.7 LB_ROLE=master EX_VIP=192.168.1.250

[all:vars]
# ---------集群主要参数---------------
#集群部署模式：allinone, single-master, multi-master
DEPLOY_MODE=multi-master

# 集群 MASTER IP即 LB节点VIP地址，为区别与默认apiserver端口，设置VIP监听的服务端口8443
# 公有云上请使用云负载均衡内网地址和监听端口
MASTER_IP="192.168.1.10"
KUBE_APISERVER="https://{{ MASTER_IP }}:8443"

# 集群网络插件，目前支持calico, flannel, kube-router, cilium
CLUSTER_NETWORK="flannel"

# 服务网段 (Service CIDR），注意不要与内网已有网段冲突
SERVICE_CIDR="10.68.0.0/16"

# POD 网段 (Cluster CIDR），注意不要与内网已有网段冲突
CLUSTER_CIDR="172.20.0.0/16"

# 服务端口范围 (NodePort Range)
NODE_PORT_RANGE="20000-40000"

# kubernetes 服务 IP (预分配，一般是 SERVICE_CIDR 中第一个IP)
CLUSTER_KUBERNETES_SVC_IP="10.68.0.1"

# 集群 DNS 服务 IP (从 SERVICE_CIDR 中预分配)
CLUSTER_DNS_SVC_IP="10.68.0.2"

# 集群 DNS 域名
CLUSTER_DNS_DOMAIN="cluster.local."

# ---------附加参数--------------------
#默认二进制文件目录
bin_dir="/opt/kube/bin"

#证书目录
ca_dir="/etc/kubernetes/ssl"

#部署目录，即 ansible 工作目录，建议不要修改
base_dir="/etc/ansible"


```



#### 生成CA 证书和私钥

* cfssl 和 cfssljson 命令安装
```
$ cat ca-config.json
{
  "signing": {
    "default": {
      "expiry": "87600h"
    },
    "profiles": {
      "kubernetes": {
        "usages": [
            "signing",
            "key encipherment",
            "server auth",
            "client auth"
        ],
        "expiry": "87600h"
      }
    }
  }
}

$ cat ca-csr.json
{
  "CN": "kubernetes",
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "WH",
      "L": "XS",
      "O": "k8s",
      "OU": "System"
    }
  ],
  "ca": {
    "expiry": "131400h"
  }
}

cfssl gencert -initca ca-csr.json | cfssljson -bare ca
ca.pem 
ca-key.pem
```



```bash
$ cat admin-csr.json
{
  "CN": "admin",
  "hosts": [],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "WH",
      "L": "XS",
      "O": "system:masters",
      "OU": "System"
    }
  ]
}

cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=kubernetes admin-csr.json | cfssljson -bare admin
admin.pem
admin-key.pem
```



使用`kubectl config` 生成kubeconfig 自动保存到 ~/.kube/config，生成后 `cat ~/.kube/config`可以验证配置文件包含 kube-apiserver 地址、证书、用户名等信息。

```bash
kubectl config set-cluster kubernetes --certificate-authority=ca.pem --embed-certs=true --server=127.0.0.1:8443
kubectl config set-credentials admin --client-certificate=admin.pem --embed-certs=true --client-key=admin-key.pem
kubectl config set-context kubernetes --cluster=kubernetes --user=admin
kubectl config use-context kubernetes
```



```bash
$ cat kube-proxy-csr.json
{
  "CN": "system:kube-proxy",
  "hosts": [],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "WH",
      "L": "XS",
      "O": "k8s",
      "OU": "System"
    }
  ]
}

cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=kubernetes kube-proxy-csr.json | cfssljson -bare kube-proxy
kube-proxy.pem
kube-key.pem

生成 kube-proxy.kubeconfig
使用kubectl config 生成kubeconfig 自动保存到 kube-proxy.kubeconfig

kubectl config set-cluster kubernetes --certificate-authority=ca.pem --embed-certs=true --server=127.0.0.1:8443 --kubeconfig=kube-proxy.kubeconfig

kubectl config set-credentials kube-proxy --client-certificate=kube-proxy.pem --embed-certs=true --client-key=kube-proxy-key.pem --kubeconfig=kube-proxy.kubeconfig

kubectl config set-context default --cluster=kubernetes --user=kube-proxy --kubeconfig=kube-proxy.kubeconfig

kubectl config use-context default --kubeconfig=kube-proxy.kubeconfig
```


### haproxy + keepalived

```bash
192.168.1.11 LB_ROLE=backup
192.168.1.12 LB_ROLE=master

# 安装 haproxy
yum install haproxy -y

# 创建 haproxy 配置目录
mkdir /etc/haproxy

# 修改 centos 的 haproxy.service
cat /usr/lib/systemd/system/haproxy.service
[Unit]
Description=HAProxy Load Balancer
After=syslog.target network.target

[Service]
EnvironmentFile=/etc/sysconfig/haproxy
ExecStartPre=/usr/bin/mkdir -p /run/haproxy
ExecStart=/usr/sbin/haproxy-systemd-wrapper -f /etc/haproxy/haproxy.cfg -p /run/haproxy.pid $OPTIONS
ExecReload=/bin/kill -USR2 $MAINPID
KillMode=mixed

[Install]
WantedBy=multi-user.target

# 配置 haproxy
cat /etc/haproxy/haproxy.cfg
global
        log /dev/log    local0
        log /dev/log    local1 notice
        chroot /var/lib/haproxy
        stats socket /run/haproxy/admin.sock mode 660 level admin
        stats timeout 30s
        user haproxy
        group haproxy
        daemon
        nbproc 1

defaults
        log     global
        timeout connect 5000
        timeout client  10m
        timeout server  10m

listen kube-master
        bind 0.0.0.0:8443
        mode tcp
        option tcplog
        balance roundrobin
        server 192.168.1.1 192.168.1.1:6443 check inter 2000 fall 2 rise 2 weight 1
        server 192.168.1.2 192.168.1.2:6443 check inter 2000 fall 2 rise 2 weight 1

listen ingress-node
	bind 0.0.0.0:80
	mode tcp
        option tcplog
        balance roundrobin
        server 192.168.1.3 192.168.1.3:23456 check inter 2000 fall 2 rise 2 weight 1
        server 192.168.1.4 192.168.1.4:23456 check inter 2000 fall 2 rise 2 weight 1
        server 192.168.1.5 192.168.1.5:23456 check inter 2000 fall 2 rise 2 weight 1

listen ingress-node-tls
	bind 0.0.0.0:443
	mode tcp
        option tcplog
        balance {{ BALANCE_ALG }}
        server 192.168.1.3 192.168.1.3:23457 check inter 2000 fall 2 rise 2 weight 1
        server 192.168.1.4 192.168.1.4:23457 check inter 2000 fall 2 rise 2 weight 1
        server 192.168.1.5 192.168.1.5:23457 check inter 2000 fall 2 rise 2 weight 1

# 安装 keepalived
yum install keepalived

# 创建keepalived配置目录
mkdir /etc/keepalived

# 配置 keepalived 主节点 192.168.1.12
cat /etc/keepalived/keepalived.conf
global_defs {
    router_id lb-master-192.168.1.12
}

vrrp_script check-haproxy {
    script "killall -0 haproxy"
    interval 5
    weight -60
}

vrrp_instance VI-kube-master {
    state MASTER
    priority 120
    unicast_src_ip 192.168.1.12
    unicast_peer {
        192.168.1.11
    }
    dont_track_primary
    interface 192.168.1.12
    virtual_router_id 111
    advert_int 3
    track_script {
        check-haproxy
    }
    virtual_ipaddress {
        192.168.1.12
    }
}

# 配置 keepalived 备节点 192.168.1.11
cat /etc/keepalived/keepalived.conf 
global_defs {
    router_id lb-backup-192.168.1.11
}

vrrp_script check-haproxy {
    script "killall -0 haproxy"
    interval 5
    weight -60
}

vrrp_instance VI-kube-master {
    state BACKUP
    priority {{ 119 | random(61, 1) }}
    unicast_src_ip 192.168.1.11
    unicast_peer {
        192.168.1.12
    }
    dont_track_primary
    interface 192.168.1.11
    virtual_router_id 111
    advert_int 3
    track_script {
        check-haproxy
    }
    virtual_ipaddress {
       192.168.1.12
    }
}

# 
systemctl daemon-reload
systemctl enable haproxy
systemctl restart haproxy

systemctl enable keepalived
systemctl restart keepalived

```


### 安装 etcd

```bash

192.168.1.1 NODE_NAME=etcd1
192.168.1.2 NODE_NAME=etcd2
192.168.1.3 NODE_NAME=etcd3

# 下载etcd二进制文件
cp /etc/ansible/bin/etcd /opt/kube/bin/etcd
cp /etc/ansible/bin/etcdctl /opt/kube/bin/etcdctl

# 分发CA证书和私钥
scp /etc/kubernetes/ssl/ca.pem /etc/kubernetes/ssl/ca.pem
scp /etc/kubernetes/ssl/ca-key.pem /etc/kubernetes/ssl/ca-key.pem
scp /etc/kubernetes/ssl/ca.csr /etc/kubernetes/ssl/ca.csr
scp /etc/kubernetes/ssl/ca-config.json /etc/kubernetes/ssl/ca-config.json

# 创建etcd证书请求
cat /etc/etcd/ssl/etcd-csr.json
cd /etc/etcd/ssl && /opt/kube/bin/cfssl gencert \
        -ca=/etc/kubernetes/ssl/ca.pem \
        -ca-key=/etc/kubernetes/ssl/ca-key.pem \
        -config=/etc/kubernetes/ssl/ca-config.json \
        -profile=kubernetes etcd-csr.json | \  
        /opt/kube/bin/cfssl/cfssljson -bare etcd
        
# 创建etcd的 systemd unit 文件，以 192.168.1.1 NODE_NAME=etcd1 为例
cat /etc/systemd/system/etcd.service
[Unit]
Description=Etcd Server
After=network.target
After=network-online.target
Wants=network-online.target
Documentation=https://github.com/coreos

[Service]
Type=notify
WorkingDirectory=/var/lib/etcd/
ExecStart=/opt/kube/bin/etcd \
  --name=etcd1 \
  --cert-file=/etc/etcd/ssl/etcd.pem \
  --key-file=/etc/etcd/ssl/etcd-key.pem \
  --peer-cert-file=/etc/etcd/ssl/etcd.pem \
  --peer-key-file=/etc/etcd/ssl/etcd-key.pem \
  --trusted-ca-file=/etc/kubernetes/ssl/ca.pem \
  --peer-trusted-ca-file=/etc/kubernetes/ssl/ca.pem \
  --initial-advertise-peer-urls=https://192.168.1.1:2380 \
  --listen-peer-urls=https://192.168.1.1:2380 \
  --listen-client-urls=https://192.168.1.1:2379,http://127.0.0.1:2379 \
  --advertise-client-urls=https://192.168.1.1:2379 \
  --initial-cluster-token=etcd-cluster-0 \
  --initial-cluster=etcd1=https://192.168.1.1:2380,etcd02=http://192.168.1.2:2380,etcd03=http://192.168.13:2380 \
  --initial-cluster-state=new \
  --data-dir=/var/lib/etcd
Restart=on-failure
RestartSec=5
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target

# 开机启用etcd服务
systemctl enable etcd
# 开启etcd服务
systemctl daemon-reload
systemctl restart etcd
systemctl status etcd.service
```

### 安装 docker 

```bash
[kube-master]
192.168.1.1
192.168.1.2

[kube-node]
192.168.1.3
192.168.1.4
192.168.1.5

# 下载 docker 二进制文件，也可以直接 yum 安装
cp /etc/ansible/bin/docker-containerd /opt/kube/bin/docker-containerd
cp /etc/ansible/bin/docker-containerd-shim /opt/kube/bin/docker-containerd-shim
cp /etc/ansible/bin/docker-init /opt/kube/bin/docker-init
cp /etc/ansible/bin/docker-runc /opt/kube/bin/docker-runc
cp /etc/ansible/bin/docker /opt/kube/bin/docker
cp /etc/ansible/bin/docker-containerd-ctr /opt/kube/bin/docker-containerd-ctr
cp /etc/ansible/bin/dockerd /opt/kube/bin/dockerd
cp /etc/ansible/bin/docker-proxy /opt/kube/bin/docker-proxy

# docker命令自动补全???

# docker配置
cat /etc/docker/daemon.json
{
  "registry-mirrors": ["https://registry.docker-cn.com", "https://docker.mirrors.ustc.edu.cn"], 
  "max-concurrent-downloads": 10,
  "log-driver": "json-file",
  "log-level": "warn",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
    },
  "data-root": "/var/lib/docker"
}

# 清理 iptables 统计
iptables -P INPUT ACCEPT \
&& iptables -F && iptables -X \
&& iptables -F -t nat && iptables -X -t nat \
&& iptables -F -t raw && iptables -X -t raw \
&& iptables -F -t mangle && iptables -X -t mangle

# 创建docker的systemd unit文件
cat /etc/systemd/system/docker.service
[Unit]
Description=Docker Application Container Engine
Documentation=http://docs.docker.io

[Service]
Environment="PATH=/opt/kube/bin:/bin:/sbin:/usr/bin:/usr/sbin"
ExecStart=/opt/kube/bin/dockerd 
ExecStartPost=/sbin/iptables -I FORWARD -s 0.0.0.0/0 -j ACCEPT
ExecReload=/bin/kill -s HUP $MAINPID
Restart=on-failure
RestartSec=5
LimitNOFILE=infinity
LimitNPROC=infinity
LimitCORE=infinity
Delegate=yes
KillMode=process

[Install]
WantedBy=multi-user.target

# 安装docker查询镜像tag的小工具
```

### kube master

```bash
192.168.1.1
192.168.1.2

# 下载 kube-master 二进制
cp /etc/ansible/bin/kube-apiserver /opt/kube/bin/kube-apiserver
cp /etc/ansible/bin/kube-controller-manager /opt/kube/bin/kube-controller-manager
cp /etc/ansible/bin/kube-scheduler /opt/kube/bin/kube-scheduler

# 分发相关证书
scp /etc/kubernetes/ssl/ca.pem /etc/kubernetes/ssl/ca.pem
scp /etc/kubernetes/ssl/ca-key.pem /etc/kubernetes/ssl/ca-key.pem
scp /etc/kubernetes/ssl/ca.csr /etc/kubernetes/ssl/ca.csr
scp /etc/kubernetes/ssl/ca-config.json /etc/kubernetes/ssl/ca-config.json
scp /etc/kubernetes/ssl/admin.pem /etc/kubernetes/ssl/admin.pem
scp /etc/kubernetes/ssl/admin-key.pem /etc/kubernetes/ssl/admin-key.pem

# 创建 kubernetes 证书签名请求，以 192.168.1.1 为例
cat /etc/kubernetes/ssl/kubernetes-csr.json
{
  "CN": "kubernetes",
  "hosts": [
    "127.0.0.1",
    "192.168.1.1",
    "192.168.1.11",
    "192.168.1.12",
    "10.68.0.1",
    "kubernetes",
    "kubernetes.default",
    "kubernetes.default.svc",
    "kubernetes.default.svc.cluster",
    "kubernetes.default.svc.cluster.local"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "WH",
      "L": "XS",
      "O": "k8s",
      "OU": "System"
    }
  ]
}

# 创建 kubernetes 证书和私钥
cd /etc/kubernetes/ssl && /opt/kube/bin/cfssl gencert \
        -ca=/etc/kubernetes/ssl/ca.pem \
        -ca-key=/etc/kubernetes/ssl/ca-key.pem \
        -config=/etc/kubernetes/ssl/ca-config.json \
        -profile=kubernetes kubernetes-csr.json | /opt/kube/bin/cfssljson -bare kubernetes

# 创建 aggregator proxy证书签名请求
cat {{ ca_dir }}/aggregator-proxy-csr.json
{
  "CN": "aggregator",
  "hosts": [],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "WH",
      "L": "XS",
      "O": "k8s",
      "OU": "System"
    }
  ]
}

# 创建 aggregator-proxy证书和私钥
cd /etc/kubernetes/ssl && /opt/kube/bin/cfssl gencert \
        -ca=/etc/kubernetes/ssl/ca.pem \
        -ca-key=/etc/kubernetes/ssl/ca-key.pem \
        -config=/etc/kubernetes/ssl/ca-config.json \
        -profile=kubernetes aggregator-proxy-csr.json | /opt/kube/bin/cfssljson -bare aggregator-proxy
        
# 创建 basic-auth.csv
cat /etc/kubernetes/ssl/basic-auth.csv
test1234,admin,1
readonly,readonly,2

# 创建kube-apiserver的systemd unit文件，以 192.168.1.1 为例
cat /etc/systemd/system/kube-apiserver.service
[Unit]
Description=Kubernetes API Server
Documentation=https://github.com/GoogleCloudPlatform/kubernetes
After=network.target

[Service]
ExecStart=/opt/kube/bin/kube-apiserver \
  --admission-control=NamespaceLifecycle,LimitRanger,ServiceAccount,DefaultStorageClass,ResourceQuota,NodeRestriction,MutatingAdmissionWebhook,ValidatingAdmissionWebhook \
  --bind-address=192.168.1.1 \
  --insecure-bind-address=127.0.0.1 \
  --authorization-mode=Node,RBAC \
  --kubelet-https=true \
  --kubelet-client-certificate=/etc/kubernetes/ssl/admin.pem \
  --kubelet-client-key=/etc/kubernetes/ssl/admin-key.pem \
  --anonymous-auth=false \
  --basic-auth-file=/etc/kubernetes/ssl/basic-auth.csv \
  --service-cluster-ip-range=10.68.0.0/16 \
  --service-node-port-range=20000-40000 \
  --tls-cert-file=/etc/kubernetes/ssl/kubernetes.pem \
  --tls-private-key-file=/etc/kubernetes/ssl/kubernetes-key.pem \
  --client-ca-file=/etc/kubernetes/ssl/ca.pem \
  --service-account-key-file=/etc/kubernetes/ssl/ca-key.pem \
  --etcd-cafile=/etc/kubernetes/ssl/ca.pem \
  --etcd-certfile=/etc/kubernetes/ssl/kubernetes.pem \
  --etcd-keyfile=/etc/kubernetes/ssl/kubernetes-key.pem \
  --etcd-servers=https://192.168.1.1:2379,https://192.168.1.2:2379,https://192.168.1.2:2379 \
  --enable-swagger-ui=true \
  --endpoint-reconciler-type=lease \
  --allow-privileged=true \
  --audit-log-maxage=30 \
  --audit-log-maxbackup=3 \
  --audit-log-maxsize=100 \
  --audit-log-path=/var/lib/audit.log \
  --event-ttl=1h \
  --requestheader-client-ca-file=/etc/kubernetes/ssl/ca.pem \
  --requestheader-allowed-names= \
  --requestheader-extra-headers-prefix=X-Remote-Extra- \
  --requestheader-group-headers=X-Remote-Group \
  --requestheader-username-headers=X-Remote-User \
  --proxy-client-cert-file=/etc/kubernetes/ssl/aggregator-proxy.pem \
  --proxy-client-key-file=/etc/kubernetes/ssl/aggregator-proxy-key.pem \
  --enable-aggregator-routing=true \
  --runtime-config=batch/v2alpha1=true \
  --v=2
Restart=on-failure
RestartSec=5
Type=notify
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target

# 创建kube-controller-manager的systemd unit文件
cat /etc/systemd/system/kube-controller-manager.service
[Unit]
Description=Kubernetes Controller Manager
Documentation=https://github.com/GoogleCloudPlatform/kubernetes

[Service]
ExecStart=/opt/kube/bin/kube-controller-manager \
  --address=127.0.0.1 \
  --master=http://127.0.0.1:8080 \
  --allocate-node-cidrs=true \
  --service-cluster-ip-range=10.68.0.0/16 \
  --cluster-cidr=172.20.0.0/16 \
  --cluster-name=kubernetes \
  --cluster-signing-cert-file=/etc/kubernetes/ssl/ca.pem \
  --cluster-signing-key-file=/etc/kubernetes/ssl/ca-key.pem \
  --service-account-private-key-file=/etc/kubernetes/ssl/ca-key.pem \
  --root-ca-file=/etc/kubernetes/ssl/ca.pem \
  --horizontal-pod-autoscaler-use-rest-clients=true \
  --leader-elect=true \
  --v=2
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target

# 创建kube-scheduler的systemd unit文件
cat /etc/systemd/system/kube-scheduler.service
[Unit]
Description=Kubernetes Scheduler
Documentation=https://github.com/GoogleCloudPlatform/kubernetes

[Service]
ExecStart=/opt/kube/bin/kube-scheduler \
  --address=127.0.0.1 \
  --master=http://127.0.0.1:8080 \
  --leader-elect=true \
  --v=2
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target

systemctl enable kube-apiserver kube-controller-manager kube-scheduler
systemctl daemon-reload
systemctl restart kube-apiserver
systemctl restart kube-controller-manager
systemctl restart kube-scheduler

kubectl get node

```

### kube node

```bash
192.168.1.3
192.168.1.4
192.168.1.5

# 相关目录
mkdir /var/lib/kubelet
mkdir /var/lib/kube-proxy
mkdir /etc/cni/net.d
mkdir /root/.kube

# 下载 kubelet,kube-proxy 二进制和基础 cni plugins
cp /etc/ansible/bin/kubectl /opt/kube/bin/kubectl
cp /etc/ansible/bin/kubelet /opt/kube/bin/kubelet
cp /etc/ansible/bin/kube-proxy /opt/kube/bin/kube-proxy
cp /etc/ansible/bin/bridge /opt/kube/bin/bridge
cp /etc/ansible/bin/host-local /opt/kube/bin/host-local
cp /etc/ansible/bin/loopback /opt/kube/bin/loopback

# 分发 kubeconfig 配置文件
scp /root/.kube/config /root/.kube/config

# 添加 kubectl 命令自动补全

# 分发证书相关
cp /etc/kubernetes/ssl/ca.pem /etc/kubernetes/ssl/ca.pem
cp /etc/kubernetes/ssl/ca-key.pem /etc/kubernetes/ssl/ca-key.pem
cp /etc/kubernetes/ssl/ca.csr /etc/kubernetes/ssl/ca.csr
cp /etc/kubernetes/ssl/ca-config.json /etc/kubernetes/ssl/ca-config.json

# 准备kubelet 证书签名请求，以 192.168.1.3 为例
cat /etc/kubernetes/ssl/kubelet-csr.json
{
  "CN": "system:node:192.168.1.3",
  "hosts": [
    "127.0.0.1",
    "192.168.1.3"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "WH",
      "L": "XS",
      "O": "system:nodes",
      "OU": "System"
    }
  ]
}

# 创建 kubelet 证书与私钥
cd /etc/kubernetes/ssl && /opt/kube/bin/cfssl gencert \
        -ca=/etc/kubernetes/ssl/ca.pem \
        -ca-key=/etc/kubernetes/ssl/ca-key.pem \
        -config=/etc/kubernetes/ssl/ca-config.json \
        -profile=kubernetes kubelet-csr.json | /opt/kube/bin/cfssljson -bare kubelet

# 设置集群参数
/opt/kube/bin/kubectl config set-cluster kubernetes \
        --certificate-authority=/etc/kubernetes/ca.pem \
        --embed-certs=true \
        --server=https://192.168.1.12:8443 \
	--kubeconfig=kubelet.kubeconfig
```









