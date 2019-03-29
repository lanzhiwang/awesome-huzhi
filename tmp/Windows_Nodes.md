## Kubernetes on Windows

- [将 windows 作为 kubernetes 的 node 节点](#为什么要将-windows-作为-kubernetes-的-node-节点)
- [准备工作](#准备工作)
	- [规划相关 ip使用默认值](#规划相关-ip使用默认值)
- [在 Linux 创建 kubernetes master 节点](#创建-kubernetes-master-节点)
- [修改节点标签使资源可以在 linux 或者 windows 上调度](#修改节点标签使资源可以在-linux-或者-windows-上调度)
- [确定网络模型](#确定网络模型)
- [将 windows server 加入集群](#将-windows-server-加入集群)
	- 安装 docker
	- 安装成功后重启系统
	- 启动 docker 服务
	- Create the "pause" (infrastructure) image（作用是什么？）
	- 拷贝相关证书和私钥
	- 下载 kubectl, kubelet, kube-proxy
	- 根据网络模型使用特定的脚本将 windows 加入集群

### 为什么要将 Windows 作为 Kubernetes 的 node 节点

将 Windows 作为 Kubernetes 的 node 节点的好处如下：

* overlay networking
* simplified network management
* scalability improvements
* hyper-v isolation (alpha)
* storage plugins

要想得到 overlay networking 好处需要满足如下条件：

* requires either Windows Server 2019 with KB4489899 installed or Windows Server vNext Insider Preview Build 18317+
* requires Kubernetes v1.14 (or above) with WinOverlay feature gate enabled
* requires Flannel v0.11.0 (or above)

### 准备工作

#### 规划相关 IP（使用默认值）

| Subnet / Address range    | Default Value |
| ------------------------- | ------------- |
| Service Subnet            | 10.96.0.0/12  |
| Cluster Subnet            | 10.244.0.0/16 |
| Kubernetes DNS Service IP | 10.96.0.10    |

### 创建 Kubernetes Master 节点

* Kubernetes v1.13  v1.14
* Ubuntu 16.04 

```bash
# 使用 root 用户执行下列命令
sudo –s

# 不使用交换分区
swapoff -a

# 更新
apt-get update -y && apt-get upgrade -y

# 安装 docker
apt-get install docker 

# 安装 kubeadm
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial main
EOF
apt-get update && apt-get install -y kubelet kubeadm kubectl

# Initialize master
kubeadm init --pod-network-cidr=10.244.0.0/16 --service-cidr=10.96.0.0/12

# 使 kubectl 可以访问集群
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

### 修改节点标签使资源可以在 Linux 或者 Windows 上调度

```bash
mkdir -p kube/yaml && cd kube/yaml

# Confirm that the update strategy of kube-proxy DaemonSet is set to RollingUpdate:
kubectl get ds/kube-proxy -o go-template='{{.spec.updateStrategy.type}}{{"\n"}}' --namespace=kube-system

# 下载 yaml 文件，修改 node 的标签
wget https://raw.githubusercontent.com/Microsoft/SDN/master/Kubernetes/flannel/l2bridge/manifests/node-selector-patch.yml
kubectl patch ds/kube-proxy --patch "$(cat node-selector-patch.yml)" -n=kube-system

kubectl get ds -n kube-system
```

### 确定网络模型

可选的网络模型有三种：

* Flannel in vxlan mode
* Flannel in host-gateway mode
* ToR switch

以 Flannel in vxlan mode 为例：

```bash
# enable bridged IPv4 traffic to iptables chains
sysctl net.bridge.bridge-nf-call-iptables=1

# download
wget https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml

# 应用 Flannel
kubectl apply -f kube-flannel.yml

```

### 将 Windows Server 加入集群

```PowerShell
# 安装 docker
Install-Module -Name DockerMsftProvider -Repository PSGallery -Force
Install-Package -Name Docker -ProviderName DockerMsftProvider
Restart-Computer -Force

# 安装成功后重启系统

# 启动 docker 服务
Start-Service docker

# Create the "pause" (infrastructure) image
docker pull mcr.microsoft.com/windows/nanoserver:1809
docker tag mcr.microsoft.com/windows/nanoserver:1809 microsoft/nanoserver:latest
docker run microsoft/nanoserver:latest


mkdir c:\k
# 将相关认证证书和私钥复制到 c:\k 目录

# 下载 kubectl, kubelet, kube-proxy

# 确认 kubectl 可以正常使用
kubectl config view

# 下载  Flannel start.ps1，使用该脚本将 windows 加入集群
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
wget https://raw.githubusercontent.com/Microsoft/SDN/master/Kubernetes/flannel/start.ps1 -o c:\k\start.ps1

cd c:\k
.\start.ps1 -ManagementIP <Windows Node IP> -NetworkMode <network mode>  -ClusterCIDR <Cluster CIDR> -ServiceCIDR <Service CIDR> -KubeDnsServiceIP <Kube-dns Service IP> -LogDir <Log directory>

```

[参考](https://docs.microsoft.com/en-us/virtualization/windowscontainers/kubernetes/getting-started-kubernetes-windows)