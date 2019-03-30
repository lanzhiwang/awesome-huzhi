## kubernetes master

### kubernetes master 节点安装配置步骤

1. 下载或者拷贝相关文件
2. kubelet 相关
	* 生成证书和私钥
	* 设置集群参数、认证参数、上下文等
	* 配置 cni
	* 创建 kubelet 的systemd unit文件
	* 启动服务

3. kube-proxy 相关
4. 设置 node 节点 role

### 相关配置说明如下

```bash
# 集群网络插件，可以支持calico, flannel, kube-router, cilium
CLUSTER_NETWORK="flannel"

# 服务网段 (Service CIDR），注意不要与内网已有网段冲突
SERVICE_CIDR="10.68.0.0/16"

# kubernetes 服务 IP (预分配，一般是 SERVICE_CIDR 中第一个IP)
CLUSTER_KUBERNETES_SVC_IP="10.68.0.1"

# 集群 DNS 服务 IP (从 SERVICE_CIDR 中预分配)
CLUSTER_DNS_SVC_IP="10.68.0.2"

# POD 网段 (Cluster CIDR），注意不要与内网已有网段冲突
CLUSTER_CIDR="172.20.0.0/16"

# 服务端口范围 (NodePort Range)
NODE_PORT_RANGE="20000-40000"

# 集群 DNS 域名
CLUSTER_DNS_DOMAIN="cluster.local."

# 需要说明的是集群的 apiserver 地址应该是负载均衡的地址
# MASTER_IP 为负载均衡主节点地址
MASTER_IP="192.168.1.12"
KUBE_APISERVER="https://192.168.1.12:8443"

# 集群 basic auth 使用的用户名和密码，用于 basic-auth.csv
BASIC_AUTH_USER="admin"
BASIC_AUTH_PASS="test1234"
```

### kubelet cni 配置选择

```bash
# "subnet": "{{ CLUSTER_CIDR }}"
"subnet": "172.20.0.0/16"
```

### kubelet cni 配置选择

```bash
--client-ca-file=/etc/kubernetes/ssl/ca.pem

--tls-cert-file=/etc/kubernetes/ssl/kubelet.pem
--tls-private-key-file=/etc/kubernetes/ssl/kubelet-key.pem

# --cluster-dns={{ CLUSTER_DNS_SVC_IP }}
--cluster-dns=10.68.0.2

# --cluster-domain={{ CLUSTER_DNS_DOMAIN }}
--cluster-domain=cluster.local.

```

### kube node 相关命令

```bash
192.168.1.3
192.168.1.4
192.168.1.5

# 相关目录
mkdir -p /opt/kube/bin /etc/kubernetes/ssl
mkdir -p /var/lib/kubelet /var/lib/kube-proxy /etc/cni/net.d /root/.kube

# 从工作节点拷贝 kubelet,kube-proxy 二进制和基础 cni plugins
scp /etc/ansible/bin/kubectl /opt/kube/bin/kubectl
scp /etc/ansible/bin/kubelet /opt/kube/bin/kubelet
scp /etc/ansible/bin/kube-proxy /opt/kube/bin/kube-proxy
scp /etc/ansible/bin/bridge /opt/kube/bin/bridge
scp /etc/ansible/bin/host-local /opt/kube/bin/host-local
scp /etc/ansible/bin/loopback /opt/kube/bin/loopback

# 从工作节点拷贝 kubectl 的配置文件
scp /root/.kube/config /root/.kube/config

# 添加 kubectl 命令自动补全

# 从工作节点拷贝证书
scp /etc/kubernetes/ssl/ca.pem /etc/kubernetes/ssl/ca.pem
scp /etc/kubernetes/ssl/ca-key.pem /etc/kubernetes/ssl/ca-key.pem
scp /etc/kubernetes/ssl/ca.csr /etc/kubernetes/ssl/ca.csr
scp /etc/kubernetes/ssl/ca-config.json /etc/kubernetes/ssl/ca-config.json

##### kubelet 相关 ##### 

# 准备 kubelet 证书签名请求，以 192.168.1.3 为例
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

# 设置 kubelet 集群参数
/opt/kube/bin/kubectl config set-cluster kubernetes \
        --certificate-authority=/etc/kubernetes/ssl/ca.pem \
        --embed-certs=true \
        --server=https://192.168.1.12:8443 \
	--kubeconfig=kubelet.kubeconfig

# 设置 kubelet 客户端认证参数
/opt/kube/bin/kubectl config set-credentials system:node:192.168.1.3 \
        --client-certificate=/etc/kubernetes/ssl/kubelet.pem \
        --embed-certs=true \
        --client-key=/etc/kubernetes/ssl/kubelet-key.pem \
	--kubeconfig=kubelet.kubeconfig

# 设置 kubelet 上下文参数
/opt/kube/bin/kubectl config set-context default \
        --cluster=kubernetes \
	--user=system:node:192.168.1.3 \
	--kubeconfig=kubelet.kubeconfig"

# 选择默认上下文
/opt/kube/bin/kubectl config use-context default \
	--kubeconfig=kubelet.kubeconfig

# 移动 kubelet.kubeconfig
mv /root/kubelet.kubeconfig /etc/kubernetes/

# cni 配置文件
cat /etc/cni/net.d/10-default.conf
{
	"name": "mynet",
	"type": "bridge",
	"bridge": "mynet0",
	"isDefaultGateway": true,
	"ipMasq": true,
	"hairpinMode": true,
	"ipam": {
		"type": "host-local",
		"subnet": "172.20.0.0/16"
	}
}

# 创建 kubelet 的systemd unit文件，以 192.168.1.3 为例
cat /etc/systemd/system/kubelet.service
[Unit]
Description=Kubernetes Kubelet
Documentation=https://github.com/GoogleCloudPlatform/kubernetes
After=docker.service
Requires=docker.service

[Service]
WorkingDirectory=/var/lib/kubelet
ExecStart=/opt/kube/bin/kubelet \
  --address=192.168.1.3 \
  --allow-privileged=true \
  --anonymous-auth=false \
  --authentication-token-webhook \
  --authorization-mode=Webhook \
  --client-ca-file=/etc/kubernetes/ssl/ca.pem \
  --cluster-dns=10.68.0.2 \
  --cluster-domain=cluster.local. \
  --cni-bin-dir=/opt/kube/bin \
  --cni-conf-dir=/etc/cni/net.d \
  --fail-swap-on=false \
  --hairpin-mode hairpin-veth \
  --hostname-override=192.168.1.3 \
  --kubeconfig=/etc/kubernetes/kubelet.kubeconfig \
  --max-pods=110 \
  --network-plugin=cni \
  --pod-infra-container-image=mirrorgooglecontainers/pause-amd64:3.1 \
  --register-node=true \
  --root-dir=/var/lib/kubelet \
  --tls-cert-file=/etc/kubernetes/ssl/kubelet.pem \
  --tls-private-key-file=/etc/kubernetes/ssl/kubelet-key.pem \
  --v=2
#kubelet cAdvisor 默认在所有接口监听 4194 端口的请求, 以下iptables限制内网访问
ExecStartPost=/sbin/iptables -A INPUT -s 10.0.0.0/8 -p tcp --dport 4194 -j ACCEPT
ExecStartPost=/sbin/iptables -A INPUT -s 172.16.0.0/12 -p tcp --dport 4194 -j ACCEPT
ExecStartPost=/sbin/iptables -A INPUT -s 192.168.0.0/16 -p tcp --dport 4194 -j ACCEPT
ExecStartPost=/sbin/iptables -A INPUT -p tcp --dport 4194 -j DROP
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target

systemctl enable kubelet
systemctl daemon-reload && systemctl restart kubelet

##### kube-proxy 相关 #####

# 从工作节点拷贝 kube-proxy.kubeconfig 配置文件
cp /etc/kubernetes/kube-proxy.kubeconfig /etc/kubernetes/kube-proxy.kubeconfig

# 创建 kube-proxy 服务文件，以 192.168.1.3 为例
cat /etc/systemd/system/kube-proxy.service
[Unit]
Description=Kubernetes Kube-Proxy Server
Documentation=https://github.com/GoogleCloudPlatform/kubernetes
After=network.target

[Service]
# kube-proxy 根据 --cluster-cidr 判断集群内部和外部流量，指定 --cluster-cidr 或 --masquerade-all 选项后
# kube-proxy 会对访问 Service IP 的请求做 SNAT，这个特性与calico 实现 network policy冲突，因此禁用
WorkingDirectory=/var/lib/kube-proxy
ExecStart=/opt/kube/bin/kube-proxy \
  --bind-address=192.168.1.3 \
  --hostname-override=192.168.1.3 \
  --kubeconfig=/etc/kubernetes/kube-proxy.kubeconfig \
  --logtostderr=true \
  --proxy-mode=iptables
Restart=on-failure
RestartSec=5
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target

systemctl enable kube-proxy
systemctl daemon-reload && systemctl restart kube-proxy

# 设置 node 节点 role，以 192.168.1.3 为例
/opt/kube/bin/kubectl label node 192.168.1.3 kubernetes.io/role=node --overwrite

```


