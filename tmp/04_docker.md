## docker 

安装方式：

* 二进制文件安装
* 包管理

### 二进制文件安装示例

```bash
[kube-master]
192.168.1.1
192.168.1.2

[kube-node]
192.168.1.3
192.168.1.4
192.168.1.5

mkdir -p /opt/kube/bin /etc/kubernetes/ssl

# 从工作节点拷贝 docker 二进制文件，也可以直接 yum 安装
scp /etc/ansible/bin/docker-containerd /opt/kube/bin/docker-containerd
scp /etc/ansible/bin/docker-containerd-shim /opt/kube/bin/docker-containerd-shim
scp /etc/ansible/bin/docker-init /opt/kube/bin/docker-init
scp /etc/ansible/bin/docker-runc /opt/kube/bin/docker-runc
scp /etc/ansible/bin/docker /opt/kube/bin/docker
scp /etc/ansible/bin/docker-containerd-ctr /opt/kube/bin/docker-containerd-ctr
scp /etc/ansible/bin/dockerd /opt/kube/bin/dockerd
scp /etc/ansible/bin/docker-proxy /opt/kube/bin/docker-proxy

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