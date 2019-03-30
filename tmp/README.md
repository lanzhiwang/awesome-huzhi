## 容器云平台构建

### 需求

1. 基于kubernetes 1.14版本构建高可用集群
2. Worker节点需要支持linux与windows主机
3. 节点网络互通
4. 支持ES集群部署、更新、回滚
5. 部署高可用sqlserver集群
6. 部署gitlab高可用集群
7. 编写服务python服务，可通过ingress方式访问此服务，并且此服务可以与es/sqlserver/gitlab交互

### 具体构建

* [直接以运行二进制文件的方式搭建 kubernetes 集群](./kubernetes_install.md)
* [将 windows 主节加入到集群作为 node 节点](./Windows_Nodes.md)
* [ES 集群](./elasticsearch.md)
* [sqlserver 构建说明](./sqlserver.md)
* [gitlab 构建说明](./gitlab.md)
* [通过 ingress 暴露 es、sqlserver、gitlab 服务](./Ingress.md)
* [python 客户端访问 kubernetes 服务](./python_client.md)
