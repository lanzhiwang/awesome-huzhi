## Docker 数据管理

### 概述

从数据的角度看，容器可以分为两类：`无状态(stateless)容器`和`有状态(stateful)容器`。

`无状态容器`是指容器在运行过程中不需要保存数据，每次访问的结果不依赖上次的访问。典型的应用是提供静态页面的web服务器。

`有状态容器`是指容器运行过程中需要保存数据，而且数据会发生变化，访问的结果依赖之前请求处理的结果。典型的应用是数据库。

对于有状态的容器，如何保存数据？

* data volume(Docker主机本地目录)

* 使用专门的 Storage Provider，也就是跨主机管理 data volume

不论是使用Docker主机本地的 data volume，还是使用跨主机的 data volume，都需要 `volume driver`。每一个 data volume 都是由 volume driver 管理的。

创建 volume 时如果不特别指定，将使用 local 类型的 driver，既从 Docker Host的本地目录中分配存储空间。如果要支持跨主机的 volume，则需要使用第三方的 driver。

```bash
[root@hz18 bin]# docker info | grep Volume
 Volume: local
[root@hz18 bin]#
```

![](./data_manager.svg)


### data volume(Docker主机本地目录)


### 跨主机管理 data volume

以 `Rex-Ray` 作为driver，以 `Virtual Media` 作为数据存储系统为例

```
Step 1: Download REX-Ray
$ curl -sSL https://rexray.io/install | sh

Step 2: Create the configuration
libstorage:
  service: virtualbox  # 使用 Virtual Media 作为存储系统
virtualbox:
  endpoint: http://192.168.99.1:18083  # Virtual Media 的访问地址
  volumePath: /Users/<your-name>/VirtualBox/Volumes
  controllerName: SATA

Step 3: Place the file at
/etc/rexray/config.yml

Step 4: Run as a service
$ rexray start

Step 5: 配置 VirtualBoBox 使 Virtual Media 可用

Step 6: 重启 rexray 服务

Step 7: rexray volume ls

Step 8: 创建 volume
docker volume create --driver rexray --name=mysqldata --opt=size=2

Step 9: 启动容器
docker run -v mysqldata:/var/lib/mysql

```

