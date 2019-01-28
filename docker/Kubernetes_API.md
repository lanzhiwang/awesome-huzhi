## Kubernetes API

### Workloads APIs

* Container 构建镜像

You create your Docker image and push it to a registry before referring to it in a Kubernetes pod.

The image property of a container supports the same syntax as the docker command does, including private registries and tags.

* CronJob 类似定时任务

A Cron Job creates Jobs on a time-based schedule.

One CronJob object is like one line of a crontab (cron table) file. It runs a job periodically on a given schedule, written in Cron format.

* DaemonSet 创建 pods 在所有的节点上运行（常驻守护进程、存储ceph、日志、监控），重点是描述 pods 和节点的关系

A DaemonSet ensures that all (or some) Nodes run a copy of a Pod. As nodes are added to the cluster, Pods are added to them. As nodes are removed from the cluster, those Pods are garbage collected. Deleting a DaemonSet will clean up the Pods it created.  DaemonSet确保所有（或某些）节点运行Pod的副本。 随着节点添加到群集中，将添加Pod。 随着节点从群集中删除，这些Pod将被垃圾收集。 删除DaemonSet将清除它创建的Pod。

* Deployment 声明 Pods 或者 ReplicaSets

A Deployment controller provides declarative updates for Pods and ReplicaSets.

You describe a desired state in a Deployment object, and the Deployment controller changes the actual state to the desired state at a controlled rate. You can define Deployments to create new ReplicaSets, or to remove existing Deployments and adopt all their resources with new Deployments.  您在Deployment对象中描述了所需的状态，Deployment控制器以受控速率将实际状态更改为所需状态。 您可以定义部署以创建新的ReplicaSet，或者删除现有的部署并使用新的部署采用所有资源。

	* Create a Deployment to rollout a ReplicaSet.
	* Declare the new state of the Pods
	* Rollback to an earlier Deployment revision
	* Scale up the Deployment to facilitate more load.
	* Pause the Deployment
	* Use the status of the Deployment
	* Clean up older ReplicaSets 

* Job 创建指定数量的 pods

A job creates one or more pods and ensures that a specified number of them successfully terminate. As pods successfully complete, the job tracks the successful completions. When a specified number of successful completions is reached, the job itself is complete. Deleting a Job will cleanup the pods it created.  作业创建一个或多个pod，并确保指定数量的pod成功终止。 随着pod成功完成，该作业跟踪成功完成。 达到指定数量的成功完成后，作业本身就完成了。 删除作业将清除它创建的pod。

A simple case is to create one Job object in order to reliably run one Pod to completion. The Job object will start a new Pod if the first pod fails or is deleted (for example due to a node hardware failure or a node reboot).  一个简单的例子是创建一个Job对象，以便可靠地运行一个Pod来完成。 如果第一个pod失败或被删除（例如由于节点硬件故障或节点重启），Job对象将启动一个新的Pod。

A Job can also be used to run multiple pods in parallel.

* Pod 

Pods are the smallest deployable units of computing that can be created and managed in Kubernetes

* ReplicaSet 

ReplicaSet is the next-generation Replication Controller. The only difference between a ReplicaSet and a Replication Controller right now is the selector support. ReplicaSet supports the new set-based selector requirements as described in the labels user guide whereas a Replication Controller only supports equality-based selector requirements.  ReplicaSet是下一代复制控制器。 现在ReplicaSet和Replication Controller之间的唯一区别是选择器支持。 ReplicaSet支持新的基于集合的选择器要求，如标签用户指南中所述，而Replication Controller仅支持基于等同的选择器要求。

* ReplicationController 

A ReplicationController ensures that a specified number of pod replicas are running at any one time. In other words, a ReplicationController makes sure that a pod or a homogeneous set of pods is always up and available.  ReplicationController确保一次运行指定数量的pod副本。 换句话说，ReplicationController确保一个pod或一组同类pod总是可用。

* StatefulSet 

StatefulSet is the workload API object used to manage stateful applications.

Manages the deployment and scaling of a set of Pods , and provides guarantees about the ordering and uniqueness of these Pods.  管理一组Pod的部署和扩展，并提供有关这些Pod的排序和唯一性的保证。

Like a Deployment , a StatefulSet manages Pods that are based on an identical container spec. Unlike a Deployment, a StatefulSet maintains a sticky identity for each of their Pods. These pods are created from the same spec, but are not interchangeable: each has a persistent identifier that it maintains across any rescheduling.  与部署类似，StatefulSet管理基于相同容器规范的Pod。 与部署不同，StatefulSet为其每个Pod维护一个粘性标识。 这些pod是根据相同的规范创建的，但不可互换：每个pod都有一个持久的标识符，它在任何重新安排时都会保留。

A StatefulSet operates under the same pattern as any other Controller. You define your desired state in a StatefulSet object, and the StatefulSet controller makes any necessary updates to get there from the current state.  StatefulSet以与任何其他Controller相同的模式运行。 您在StatefulSet对象中定义所需的状态，StatefulSet控制器进行任何必要的更新以从当前状态到达那里。

StatefulSets are valuable for applications that require one or more of the following.  有状态集对于需要以下一个或多个的应用程序非常有用。

	* Stable, unique network identifiers.  稳定，独特的网络标识符。
	* Stable, persistent storage.  稳定，持久的存储。
	* Ordered, graceful deployment and scaling.  有序，优雅的部署和扩展。
	* Ordered, automated rolling updates.  有序的自动滚动更新。

### Service APIs

* Endpoints

For Kubernetes-native applications, Kubernetes offers a simple Endpoints API that is updated whenever the set of Pods in a Service changes.   对于Kubernetes本机应用程序，Kubernetes提供了一个简单的Endpoints API，只要服务中的Pod集发生变化，它就会更新。

* Ingress 

An API object that manages external access to the services in a cluster, typically HTTP.  管理群集中服务的外部访问的API对象，通常是HTTP。

Ingress can provide load balancing, SSL termination and name-based virtual hosting.  Ingress可以提供负载平衡，SSL终止和基于名称的虚拟主机。

```
    internet
        |
   [ Ingress ]
   --|-----|--
   [ Services ]
```

* Service 

Kubernetes Pods are mortal. They are born and when they die, they are not resurrected. ReplicaSets in particular create and destroy Pods dynamically (e.g. when scaling out or in). While each Pod gets its own IP address, even those IP addresses cannot be relied upon to be stable over time. This leads to a problem: if some set of Pods (let’s call them backends) provides functionality to other Pods (let’s call them frontends) inside the Kubernetes cluster, how do those frontends find out and keep track of which backends are in that set?  Kubernetes Pods是致命的。 他们出生，死后，他们没有复活。 ReplicaSet特别是动态地创建和销毁Pod（例如，当向外扩展或在其中时）。 虽然每个Pod都有自己的IP地址，但即使是那些IP地址也不能依赖它们随时间变得稳定。 这会导致一个问题：如果某些Pod（让我们称之为后端）为Kubernetes集群内的其他Pod（让我们称之为前端）提供功能，那些前端如何找出并跟踪该集合中的哪些后端？

Enter Services.

A Kubernetes Service is an abstraction which defines a logical set of Pods and a policy by which to access them - sometimes called a micro-service. The set of Pods targeted by a Service is (usually) determined by a Label Selector (see below for why you might want a Service without a selector).  Kubernetes服务是一种抽象，它定义了一组逻辑Pod和一个访问它们的策略 - 有时称为微服务。 服务所针对的Pod集合（通常）由标签选择器确定（请参阅下文，了解您可能需要没有选择器的服务的原因）。

As an example, consider an image-processing backend which is running with 3 replicas. Those replicas are fungible - frontends do not care which backend they use. While the actual Pods that compose the backend set may change, the frontend clients should not need to be aware of that or keep track of the list of backends themselves. The Service abstraction enables this decoupling.  例如，考虑一个运行3个副本的图像处理后端。 那些复制品是可替代的 - 前端并不关心它们使用哪个后端。 虽然组成后端集的实际Pod可能会发生变化，但前端客户端不应该知道这一点或跟踪后端列表本身。 服务抽象实现了这种解耦。

For Kubernetes-native applications, Kubernetes offers a simple Endpoints API that is updated whenever the set of Pods in a Service changes. For non-native applications, Kubernetes offers a virtual-IP-based bridge to Services which redirects to the backend Pods.  对于Kubernetes本机应用程序，Kubernetes提供了一个简单的Endpoints API，只要服务中的Pod集发生变化，它就会更新。 对于非本机应用程序，Kubernetes提供基于虚拟IP的服务桥接，重定向到后端Pod。

### Config and Storage APIs

* ConfigMap

ConfigMaps allow you to decouple configuration artifacts from image content to keep containerized applications portable. This page provides a series of usage examples demonstrating how to create ConfigMaps and configure Pods using data stored in ConfigMaps.  ConfigMaps允许您将配置工件与图像内容分离，以使容器化应用程序可移植。 此页面提供了一系列用法示例，演示如何使用ConfigMaps中存储的数据创建ConfigMaps和配置Pod。

* Secret 

Objects of type secret are intended to hold sensitive information, such as passwords, OAuth tokens, and ssh keys. Putting this information in a secret is safer and more flexible than putting it verbatim in a pod definition or in a docker image.

* PersistentVolumeClaim

Managing storage is a distinct problem from managing compute. The PersistentVolume subsystem provides an API for users and administrators that abstracts details of how storage is provided from how it is consumed. To do this we introduce two new API resources: PersistentVolume and PersistentVolumeClaim.  管理存储是管理计算的一个明显问题。 PersistentVolume子系统为用户和管理员提供了一个API，它提供了如何根据消费方式提供存储的详细信息。 为此，我们引入了两个新的API资源：PersistentVolume和PersistentVolumeClaim。

A PersistentVolume (PV) is a piece of storage in the cluster that has been provisioned by an administrator. It is a resource in the cluster just like a node is a cluster resource. PVs are volume plugins like Volumes, but have a lifecycle independent of any individual pod that uses the PV. This API object captures the details of the implementation of the storage, be that NFS, iSCSI, or a cloud-provider-specific storage system.  PersistentVolume（PV）是群集中由管理员配置的一块存储。 它是集群中的资源，就像节点是集群资源一样。 PV是容量插件，如Volumes，但其生命周期独立于使用PV的任何单个pod。 此API对象捕获存储实现的详细信息，包括NFS，iSCSI或特定于云提供程序的存储系统。

A PersistentVolumeClaim (PVC) is a request for storage by a user. It is similar to a pod. Pods consume node resources and PVCs consume PV resources. Pods can request specific levels of resources (CPU and Memory). Claims can request specific size and access modes (e.g., can be mounted once read/write or many times read-only).  PersistentVolumeClaim（PVC）是用户存储的请求。 它类似于一个吊舱。 Pod消耗节点资源，PVC消耗PV资源。 Pod可以请求特定级别的资源（CPU和内存）。 声明可以请求特定的大小和访问模式（例如，可以一次读/写或多次只读）。

While PersistentVolumeClaims allow a user to consume abstract storage resources, it is common that users need PersistentVolumes with varying properties, such as performance, for different problems. Cluster administrators need to be able to offer a variety of PersistentVolumes that differ in more ways than just size and access modes, without exposing users to the details of how those volumes are implemented. For these needs there is the StorageClass resource.  虽然PersistentVolumeClaims允许用户使用抽象存储资源，但是对于不同的问题，用户需要具有不同属性（如性能）的PersistentVolumes。 群集管理员需要能够提供各种PersistentVolume，这些PersistentVolume在多种方式上不仅仅是大小和访问模式，而不会让用户了解这些卷的实现方式。 对于这些需求，存在StorageClass资源。

* StorageClass

A StorageClass provides a way for administrators to describe the “classes” of storage they offer. Different classes might map to quality-of-service levels, or to backup policies, or to arbitrary policies determined by the cluster administrators. Kubernetes itself is unopinionated about what classes represent. This concept is sometimes called “profiles” in other storage systems.  StorageClass为管理员提供了一种描述他们提供的“存储类”的方法。 不同的类可能映射到服务质量级别，或备份策略，或者由集群管理员确定的任意策略。 Kubernetes本身对于什么类代表是不受任何影响的。 这个概念有时在其他存储系统中称为“配置文件”。

* Volume 

On-disk files in a Container are ephemeral, which presents some problems for non-trivial applications when running in Containers. First, when a Container crashes, kubelet will restart it, but the files will be lost - the Container starts with a clean state. Second, when running Containers together in a Pod it is often necessary to share files between those Containers. The Kubernetes Volume abstraction solves both of these problems.  Container中的磁盘文件是短暂的，这在容器中运行时会给非平凡的应用程序带来一些问题。 首先，当容器崩溃时，kubelet将重新启动它，但文件将丢失 -  Container以干净状态启动。 其次，在Pod中一起运行Container时，通常需要在这些容器之间共享文件。 Kubernetes Volume抽象解决了这两个问题。

* VolumeAttachment 

### Metadata APIs

* ControllerRevision

* CustomResourceDefinition

* Event 

* LimitRange 

* HorizontalPodAutoscaler 

* InitializerConfiguration 

* MutatingWebhookConfiguration 

* ValidatingWebhookConfiguration 

* PodTemplate 

* PodDisruptionBudget 

* PriorityClass 

* PodPreset 

* PodSecurityPolicy 

### Cluster APIs

* APIService

* Binding 

* CertificateSigningRequest 

* ClusterRole

* ClusterRoleBinding 

* ComponentStatus 

* LocalSubjectAccessReview 

* Namespace 

* Node 

* PersistentVolume 

* ResourceQuota 

* Role 

* RoleBinding 

* SelfSubjectAccessReview 

* SelfSubjectRulesReview 

* ServiceAccount 

* SubjectAccessReview 

* TokenReview 

* NetworkPolicy 

