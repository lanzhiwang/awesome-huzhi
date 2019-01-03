## Docker 的优点和缺点

### 优点

- Docker is a "packaging format" and a "process specification format".



### 缺点

- 容器化后经过多个虚拟网卡带来的性能损失
- 由于附加层而增加了复杂性。 这不仅影响部署，还影响开发和构建。
- 管理大量容器具有挑战性 - 特别是在集群容器方面。 像Google Kubernetes和Apache Mesos这样的工具可以在这里提供帮助。
- 容器共享相同的内核，因此与真实VM相比不那么孤立。 内核中的错误会影响每个容器。
- Docker基于Linux Containers（LXC），这是一种Linux技术。这对其他系统是不小的挑战
- 持久数据存储很复杂。
- 图形应用程序不能很好地工作。



#### 参考

* https://blog.philipphauer.de/discussing-docker-pros-and-cons/

* https://www.quora.com/What-are-some-disadvantages-of-using-Docker