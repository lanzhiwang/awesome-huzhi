## kubernetes install

### 整体架构

![](./architecture.png)

* 所有节点以 centos7 为操作系统
* 整个集群包括 k8s 主节点、k8s node 节点、etcd、负载均衡节点
* 参照 ansible 的模式，设置一个工作节点，该工作节点不属于 kubernetes 集群
* 为了使部署过程快速完成，在部署之前将所有用到的二进制文件，docker 镜像等全部下载到工作节点，后续复制到集群的相关节点
* 架构的所有节点要求时间同步，所以需要 ntp 或者 chrony 服务
* 使用 harbor 作为私有镜像库，如果没有安装私有镜像库，就需要将 docker 镜像加载到 kubernetes 的 master 和 node 节点。
* 如图所示，客户端请求 haproxy 的 8443 端口，所以相关客户端（包括kubectl 和 kube-proxy）的配置文件中集群 apiserver 的地址应该使 192.168.1.12:8443 
* haproxy 对应的 80 和 443 端口用于向集群外部的客户端公开相关服务，用于 ingress ，此时该如何对应多个服务 ?
* kubernetes 主节点也可以安装 kube-proxy 和 kebuctl 等用于调度



[工作节点的准备工作](./01_deploy.md)
[所有节点的预配置](./02_prepare.md)
[haproxy + keepalived 安装配置](./03_lb.md)
[在 master 和 node 节点上安装 docker](./04_docker.md)
[etcd](./05_etcd.md)
[kubernetes 主节点安装配置](./06_kube_master.md)
[kubernetes node 节点安装配置](./07_kube_node.md)
[在主节点和 node 节点安装网络插件](./08_kube_network.md)
[安装 dns、metrics-server、dashboard、heapster、metallb、traefik、nginx-ingress](./09_kube_addon.md)











### 问题

* ntp 或者 chrony 服务的异同，该如何选择？
* kubernetes 是否需要知道镜像库的位置，还是只要在 docker 中指定？docker 配置文件可以指定
* haproxy + keepalived 部分配置参数的含义
* 在 systemd unit 文件中可以使用的相关变量有哪些？参见 haproxy + keepalived
* haproxy 对应的 80 和 443 端口用于向集群外部的客户端公开相关服务，用于 ingress ，此时该如何对应多个服务 ?
* 在主节点安装时的操作 `Making master nodes SchedulingDisabled` 和 `Setting master role name` 的作用？
* kubectl cordon 作用？







