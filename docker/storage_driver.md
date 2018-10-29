

## storage driver



#### Docker 镜像和容器

Docker `镜像` 的分层结构如下图所示：

![](./storage_driver.jpg)

Docker `容器` 由最上面的一个可写的容器层，以及若干个自读的镜像层组成。容器的数据就存放在这些层中。

这样的分层结构的最大特性是 `Copy-on-Write` 。



#### 写时复制(Copy-on-Write)

* 新数据会直接存放在最上面的容器层。

* 修改现有数据（旧数据）会先从镜像层将数据复制容器层，修改后的数据直接保存在容器层中，镜像层保持不变。

* 如果多个层中有命名相同的文件，用户只能看到最上面那层中的文件。



#### storage_driver

分层结构使镜像和容器的创建、共享和分发变得非常高效。这些都要归功于与 Docker storage driver。正是 storage driver  `实现了多层数据的堆叠并为用户提供一个单一的合并之后的统一视图` 。

Docker 支持多种 storage driver 。`aufs`、`devicemapper`、`overlay`、`overlay2`、`btrfs`、`zfs`。他们都能实现分层的架构，同时又有各自的特性。









