# Docker 相关问题

### docker attach 和 docker exec 的区别？

docker attach 重新附着到容器的会话上，一般来说该容器运行了一个交互式的 Shell。

docker exec 在容器内部额外启动新的进程，一般来说该容器运行了一个后台任务，可以重新启动一个新的交互式 Shell。

参考 
* 《每天5分钟玩转Docker容器技术》4.1.2 进入容器的方法

### 如何确保容器的时间和时区时正确的？


### 容器资源限制

参考 
* 《每天5分钟玩转Docker容器技术》4.6

### 常用发行版基础镜像？

* alpine [使用示例](https://github.com/nicolaka/netshoot/blob/master/Dockerfile)
* debian
* ubuntu
* centos
* busybox

### docker 单机网络

1. docker 支持的单机网络模式
2. 自定义单机网络
3. 单机环境下的容器间通信
4. 容器与外部网络通信

参考
* 《每天5分钟玩转Docker容器技术》第五章
* 《Docker经典实例》第三章
* 《第一本Docker书》5.2.6 让 docker 容器互联
* 《深入浅出 Docker》第十一章，第十二章

### 跨主机间容器通信

1. overlay、VxLAN、VLAN、IPAM
2. MacVLAN、VLAN、交换机的 Access 和 Trunk 模式
3. flannel、VxLAN、host-gw
4. weave、Open vSwitch
5. calico

参考
* 《每天5分钟玩转Docker容器技术》第八章

### Libnetwork 和 CNM

1. Libnetwork 和 CNM 的关系
2. Libnetwork 实现的功能
3. docker 服务发现和负载均衡

参考
* 《深入浅出 Docker》第十一章，第十二章

### docker swarm
1. docker swarm
2. swarm 服务或者 docker 服务

参考
* 《深入浅出 Docker》第十章



### VxLAN 工作原理

参考

* 《深入浅出 Docker》第十二章


### 如何用 Dockerfile 构建镜像和常见的 Dockerfile 指令？

参考
* 《第一本 docker 书》4.5.3 节 用 Dockerfile 构建镜像


### 容器中卷的使用？

1. storage driver
2. copy-on-write
3. aufs、device mapper、btrfs、overlayfs、vfs、zfs
4. data volume
5. bind mount、docker managed volume
6. volume container、data-packed volume container

参考
* 《每天5分钟玩转Docker容器技术》第六章



### Docker Compose and Docker Stack

参考

* 《深入浅出 Docker》第九章，第十四章

