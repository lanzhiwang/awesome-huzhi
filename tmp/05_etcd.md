## 安装 etcd

```bash

192.168.1.1 NODE_NAME=etcd1
192.168.1.2 NODE_NAME=etcd2
192.168.1.3 NODE_NAME=etcd3

mkdir -p /opt/kube/bin /etc/kubernetes/ssl /etc/etcd/ssl /var/lib/etcd

# 从工作节点拷贝 etcd 二进制文件
scp /etc/ansible/bin/etcd /opt/kube/bin/etcd
scp /etc/ansible/bin/etcdctl /opt/kube/bin/etcdctl

# 从工作节点拷贝 CA 证书和私钥
scp /etc/kubernetes/ssl/ca.pem /etc/kubernetes/ssl/ca.pem
scp /etc/kubernetes/ssl/ca-key.pem /etc/kubernetes/ssl/ca-key.pem
scp /etc/kubernetes/ssl/ca.csr /etc/kubernetes/ssl/ca.csr
scp /etc/kubernetes/ssl/ca-config.json /etc/kubernetes/ssl/ca-config.json

# 创建 etcd 证书请求文件，以 192.168.1.1 为例
cat /etc/etcd/ssl/etcd-csr.json
{
  "CN": "etcd",
  "hosts": [
    "127.0.0.1",
    "192.168.1.1"
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

# 创建 etcd 证书和私钥
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