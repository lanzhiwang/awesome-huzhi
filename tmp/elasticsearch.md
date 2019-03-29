## 在 Kubernetes 集群上部署 ElasticSearch

[TOC]



### 整体部署说明

![](./elasticsearch.png)

* 整个 ES 集群有 3 个主节点，2 个数据节点， 2 个 ignest 节点
* 每个 pod 中运行一个容器
* 使用 三个 deployment 管理相关 pod
* 部署 3 个 service 分别对于三种节点的服务
* 节点之间的发现使用 service/elasticsearch-discovery 服务，不需要容器之间的直接通信
* 客户端访问 service/elasticsearch 服务后转发到数据节点
* 因为有 3 个主节点，为防止网络原因产生脑裂，设置 minimum_master_nodes 为 2
* 数据持久化暂时使用本地目录，后续要改成 pv 和 pvc
* 为了保证集群的高可用，在对集群进行升级、更新、回滚时需要有最低限度的 pod 可用，使用 PodDisruptionBudget 资源保障最低限度的 pod 可用


### 部署过程

1. 构建 ElasticSearch 镜像，构建镜像的过程参考 [docker-elasticsearch-kubernetes](https://github.com/pires/docker-elasticsearch-kubernetes)

2. 由于没有私有镜像库，将构建好的镜像上传到 Kubernetes 的所有节点上

3. 编写相关的 yaml 文件在 Kubernetes 集群上创建资源

### 相关 yaml 文件（[参考](https://github.com/pires/kubernetes-elasticsearch-cluster)）

```bash
$ tree -a .
.
├── es-curator-config.yaml # curator 的 ConfigMap
├── es-curator.yaml # 使用 curator 计划任务定期管理集群中的所有
├── es-data-pdb.yaml # 使用 PodDisruptionBudget 资源保证数据 pod 最小可用
├── es-data.yaml # 数据节点 Deployment
├── es-discovery-svc.yaml # master 节点 Service
├── es-ingest-svc.yaml # ingest 节点 Service
├── es-ingest.yaml # ingest 节点 Deployment
├── es-master-pdb.yaml # 使用 PodDisruptionBudget 资源保证主节点 pod 最小可用
├── es-master.yaml # master 节点 Deployment
├── es-svc.yaml # 数据节点 Service
├── kibana-cm.yaml # kibana 相关
├── kibana-svc.yaml
├── kibana.yaml
├── LICENSE
├── README.md
└── stateful
    ├── es-data-stateful.yaml # 数据节点 StatefulSet
    ├── es-data-svc.yaml # 数据节点 Service
    ├── es-master-stateful.yaml # 主节点 StatefulSet
    ├── es-master-svc.yaml # 数据节点 Service
    └── README.md

17 directories, 44 files
$ 

```

### ElasticSearch 配置文件 elasticsearch.yml

ElasticSearch 的配置文件中使用了很多环境变量来配置相关选项，因此在相关的 Deployment 或者 StatefulSet 中要提供必要的环境变量。ElasticSearch 配置文件如下：

* 其中 ${DISCOVERY_SERVICE} 和 ${MEMORY_LOCK} 两个环境变量在 Dockerfile 中已经初始化了。${DISCOVERY_SERVICE} = elasticsearch-discovery 知道节点之间通过 elasticsearch-discovery 服务互相发现。
* 如果没有提供相应的环境变量，则配置选项使用默认值

```
cluster:
  name: ${CLUSTER_NAME}

node:
  master: ${NODE_MASTER}
  data: ${NODE_DATA}
  name: ${NODE_NAME}
  ingest: ${NODE_INGEST}
  max_local_storage_nodes: ${MAX_LOCAL_STORAGE_NODES}

processors: ${PROCESSORS:1}

network.host: ${NETWORK_HOST}

path:
  data: /data/data
  logs: /data/log
  repo: ${REPO_LOCATIONS}

bootstrap:
  memory_lock: ${MEMORY_LOCK}  # 在 Dockerfile 中定义 MEMORY_LOCK false

http:
  enabled: ${HTTP_ENABLE}
  compression: true
  cors:
    enabled: ${HTTP_CORS_ENABLE}
    allow-origin: ${HTTP_CORS_ALLOW_ORIGIN}

discovery:
  zen:
    ping.unicast.hosts: ${DISCOVERY_SERVICE}  # 在 Dockerfile 中定义 DISCOVERY_SERVICE elasticsearch-discovery，通过 elasticsearch-discovery 服务发现其他节点
    minimum_master_nodes: ${NUMBER_OF_MASTERS}

xpack.ml.enabled: false
```

### master 节点相关服务和 deployment

```
apiVersion: v1
kind: Service
metadata:
  name: elasticsearch-discovery
  labels:
    component: elasticsearch  # 用于筛选与 elasticsearch 有关的资源
    role: master
spec:
  selector:
    component: elasticsearch
    role: master
  ports:
  - name: transport
    port: 9300
    protocol: TCP
  clusterIP: None

# 使用 component 和 role = master 管理主节点 pod
# 服务监听 9300 端口
# 将 clusterIP 设置为 None，创建 headless 服务连接到所有的主节点 pod

---

apiVersion: apps/v1beta1
kind: Deployment
metadata:
  name: es-master
  labels:
    component: elasticsearch
    role: master
spec:
  replicas: 3
  template:
    metadata:
      labels:
        component: elasticsearch
        role: master
    spec:
      initContainers:
      - name: init-sysctl
        image: busybox:1.27.2
        command:
        - sysctl
        - -w
        - vm.max_map_count=262144
        securityContext:
          privileged: true
      containers:
      - name: es-master
        image: quay.io/pires/docker-elasticsearch-kubernetes:6.3.2
        env:
        - name: NAMESPACE  # 该环境变量暂时没有用到
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: NODE_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: CLUSTER_NAME
          value: myesdb
        - name: NUMBER_OF_MASTERS
          value: "2"
        - name: NODE_MASTER
          value: "true"
        - name: NODE_INGEST
          value: "false"
        - name: NODE_DATA
          value: "false"
        - name: HTTP_ENABLE
          value: "false"
        - name: ES_JAVA_OPTS  # 该环境变量暂时没有用到
          value: -Xms256m -Xmx256m
        - name: PROCESSORS
          valueFrom:
            resourceFieldRef:
              resource: limits.cpu
        resources:
          requests:
            cpu: 0.25
          limits:
            cpu: 1
        ports:
        - containerPort: 9300
          name: transport
        livenessProbe:
          tcpSocket:
            port: transport
          initialDelaySeconds: 20
          periodSeconds: 10
        volumeMounts:
        - name: storage
          mountPath: /data
      volumes:  # 需要提供持久化处理
          - emptyDir:
              medium: ""
            name: "storage"

# 在 Deployment 设置了相关标签
# 启动容器之前调整了内核参数
# 设置了相关环境变量
# 使用 tcp 套接字存活探针检测容器是否在运行
# 使用本地文件系统存储数据，需要改成持久化存储

#######################################
# 使用环境变量填充的配置文件如下：
# 该节点作为主节点

cluster:
  name: ${CLUSTER_NAME}  # myesdb

node:
  master: ${NODE_MASTER}  # true
  data: ${NODE_DATA}  # false
  name: ${NODE_NAME}  # es-master
  ingest: ${NODE_INGEST}  # false
  max_local_storage_nodes: ${MAX_LOCAL_STORAGE_NODES}

processors: ${PROCESSORS:1}  # 1

network.host: ${NETWORK_HOST}

path:
  data: /data/data
  logs: /data/log
  repo: ${REPO_LOCATIONS}

bootstrap:
  memory_lock: ${MEMORY_LOCK}  # 在 Dockerfile 中定义 MEMORY_LOCK false

http:
  enabled: ${HTTP_ENABLE}  # false
  compression: true
  cors:
    enabled: ${HTTP_CORS_ENABLE}
    allow-origin: ${HTTP_CORS_ALLOW_ORIGIN}

discovery:
  zen:
    ping.unicast.hosts: ${DISCOVERY_SERVICE}  # 在 Dockerfile 中定义 DISCOVERY_SERVICE = elasticsearch-discovery，通过 elasticsearch-discovery 服务发现其他节点
    minimum_master_nodes: ${NUMBER_OF_MASTERS}  # 2

xpack.ml.enabled: false

```

### data 节点服务和 deployment

```
apiVersion: v1
kind: Service
metadata:
  name: elasticsearch
  labels:
    component: elasticsearch
    role: data
spec:
  selector:
    component: elasticsearch
    role: data
  ports:
  - name: http
    port: 9200
#type: LoadBalancer

# 服务监听 9200 端口，将请求转发到后端的数据节点

---

apiVersion: apps/v1beta1
kind: Deployment
metadata:
  name: es-data
  labels:
    component: elasticsearch
    role: data
spec:
  replicas: 2
  template:
    metadata:
      labels:
        component: elasticsearch
        role: data
    spec:
      initContainers:
      - name: init-sysctl
        image: busybox:1.27.2
        command:
        - sysctl
        - -w
        - vm.max_map_count=262144
        securityContext:
          privileged: true
      containers:
      - name: es-data
        image: quay.io/pires/docker-elasticsearch-kubernetes:6.3.2
        env:
        - name: NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: NODE_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: CLUSTER_NAME
          value: myesdb
        - name: NODE_MASTER
          value: "false"
        - name: NODE_INGEST
          value: "false"
        - name: HTTP_ENABLE
          value: "true"
        - name: ES_JAVA_OPTS
          value: -Xms256m -Xmx256m
        - name: PROCESSORS
          valueFrom:
            resourceFieldRef:
              resource: limits.cpu
        resources:
          requests:
            cpu: 0.25
          limits:
            cpu: 1
        ports:
        - containerPort: 9200
          name: http
        - containerPort: 9300
          name: transport
        livenessProbe:
          tcpSocket:
            port: transport
          initialDelaySeconds: 20
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /_cluster/health
            port: http
          initialDelaySeconds: 20
          timeoutSeconds: 5
        volumeMounts:
        - name: storage
          mountPath: /data
      volumes:
          - emptyDir:
              medium: ""
            name: storage

# 在 Deployment 中使用  http get 就绪探针检测容器是否可以正常提供服务

###########################################

# 使用环境变量填充的配置文件如下：

cluster:
  name: ${CLUSTER_NAME}  # myesdb

node:
  master: ${NODE_MASTER}  # false
  data: ${NODE_DATA}
  name: ${NODE_NAME}  # es-data
  ingest: ${NODE_INGEST}  # false
  max_local_storage_nodes: ${MAX_LOCAL_STORAGE_NODES}

processors: ${PROCESSORS:1}  # 1

network.host: ${NETWORK_HOST}

path:
  data: /data/data
  logs: /data/log
  repo: ${REPO_LOCATIONS}

bootstrap:
  memory_lock: ${MEMORY_LOCK}  # 在 Dockerfile 中定义 MEMORY_LOCK false

http:
  enabled: ${HTTP_ENABLE}  # true
  compression: true
  cors:
    enabled: ${HTTP_CORS_ENABLE}
    allow-origin: ${HTTP_CORS_ALLOW_ORIGIN}

discovery:
  zen:
    ping.unicast.hosts: ${DISCOVERY_SERVICE}  # 在 Dockerfile 中定义 DISCOVERY_SERVICE elasticsearch-discovery，通过 elasticsearch-discovery 服务发现其他节点
    minimum_master_nodes: ${NUMBER_OF_MASTERS}

xpack.ml.enabled: false

```

### ingest 节点服务和 Deployment

```
apiVersion: v1
kind: Service
metadata:
  name: elasticsearch-ingest
  labels:
    component: elasticsearch
    role: ingest
spec:
  selector:
    component: elasticsearch
    role: ingest
  ports:
  - name: http
    port: 9200
#type: LoadBalancer

---

apiVersion: apps/v1beta1
kind: Deployment
metadata:
  name: es-ingest
  labels:
    component: elasticsearch
    role: ingest
spec:
  replicas: 2
  template:
    metadata:
      labels:
        component: elasticsearch
        role: ingest
    spec:
      initContainers:
      - name: init-sysctl
        image: busybox:1.27.2
        command:
        - sysctl
        - -w
        - vm.max_map_count=262144
        securityContext:
          privileged: true
      containers:
      - name: es-ingest
        image: quay.io/pires/docker-elasticsearch-kubernetes:6.3.2
        env:
        - name: NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: NODE_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: CLUSTER_NAME
          value: myesdb
        - name: NODE_MASTER
          value: "false"
        - name: NODE_DATA
          value: "false"
        - name: HTTP_ENABLE
          value: "true"
        - name: ES_JAVA_OPTS
          value: -Xms256m -Xmx256m
        - name: NETWORK_HOST
          value: _site_,_lo_
        - name: PROCESSORS
          valueFrom:
            resourceFieldRef:
              resource: limits.cpu
        resources:
          requests:
            cpu: 0.25
          limits:
            cpu: 1
        ports:
        - containerPort: 9200
          name: http
        - containerPort: 9300
          name: transport
        livenessProbe:
          tcpSocket:
            port: transport
          initialDelaySeconds: 20
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /_cluster/health
            port: http
          initialDelaySeconds: 20
          timeoutSeconds: 5
        volumeMounts:
        - name: storage
          mountPath: /data
      volumes:
          - emptyDir:
              medium: ""
            name: storage

###############################################

cluster:
  name: ${CLUSTER_NAME}  # myesdb

node:
  master: ${NODE_MASTER}  # false
  data: ${NODE_DATA}  # false
  name: ${NODE_NAME}  # es-ingest
  ingest: ${NODE_INGEST}
  max_local_storage_nodes: ${MAX_LOCAL_STORAGE_NODES}

processors: ${PROCESSORS:1}  # 1

network.host: ${NETWORK_HOST}  # NETWORK_HOST = _site_,_lo_

path:
  data: /data/data
  logs: /data/log
  repo: ${REPO_LOCATIONS}

bootstrap:
  memory_lock: ${MEMORY_LOCK}  # 在 Dockerfile 中定义 MEMORY_LOCK false

http:
  enabled: ${HTTP_ENABLE}  # true
  compression: true
  cors:
    enabled: ${HTTP_CORS_ENABLE}
    allow-origin: ${HTTP_CORS_ALLOW_ORIGIN}

discovery:
  zen:
    ping.unicast.hosts: ${DISCOVERY_SERVICE}  # 在 Dockerfile 中定义 DISCOVERY_SERVICE elasticsearch-discovery，通过 elasticsearch-discovery 服务发现其他节点
    minimum_master_nodes: ${NUMBER_OF_MASTERS}

xpack.ml.enabled: false

```

### StatefulSet 资源使用说明

1. 为每个 StatefulSet 创建相关的 Service 和持久化存储
2. 直接使用 volumeClaimTemplates 创建持久化存储
3. 其他配置和 Deployment 差不多

volumeClaimTemplates 使用方法如下：

```
.....
        volumeMounts:
        - name: storage
          mountPath: /data
  volumeClaimTemplates:
  - metadata:
      name: storage
    spec:
      storageClassName: standard
      accessModes: [ ReadWriteOnce ]
      resources:
        requests:
          storage: 12Gi
```

* [参考1](https://github.com/pires/kubernetes-elasticsearch-cluster)
* [参考2](https://github.com/pires/docker-elasticsearch-kubernetes)


