[参考](https://blog.csdn.net/hxpjava1/article/details/79676794)


```

---
apiVersion: v1
kind: Namespace
metadata:
  name: ns-elasticsearch
  labels:
    name: ns-elasticsearch
 
---
apiVersion: v1
kind: ServiceAccount
metadata:
  labels:
    elastic-app: elasticsearch
  name: elasticsearch-admin
  namespace: ns-elasticsearch
 
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: elasticsearch-admin
  labels:
    elastic-app: elasticsearch
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
  - kind: ServiceAccount
    name: elasticsearch-admin
    namespace: ns-elasticsearch
 
---
kind: Deployment
apiVersion: apps/v1beta2
metadata:
  labels:
    elastic-app: elasticsearch
    role: master
  name: elasticsearch-master
  namespace: ns-elasticsearch
spec:
  replicas: 3
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      elastic-app: elasticsearch
      role: master
  template:
    metadata:
      labels:
        elastic-app: elasticsearch
        role: master
    spec:
      containers:
        - name: elasticsearch-master
          image: docker.elastic.co/elasticsearch/elasticsearch:6.2.2-1
          lifecycle:
            postStart:
              exec:
                command: ["/bin/bash", "-c", "sysctl -w vm.max_map_count=262144; ulimit -l unlimited;"]
          ports:
            - containerPort: 9200
              protocol: TCP
            - containerPort: 9300
              protocol: TCP
          env:
            - name: "cluster.name"
              value: "elasticsearch-cluster"
            - name: "bootstrap.memory_lock"
              value: "true"
            - name: "discovery.zen.ping.unicast.hosts"
              value: "elasticsearch-discovery"
            - name: "discovery.zen.minimum_master_nodes"
              value: "2"
            - name: "discovery.zen.ping_timeout"
              value: "5s"
            - name: "node.master"
              value: "true"
            - name: "node.data"
              value: "false"
            - name: "node.ingest"
              value: "false"
            - name: "ES_JAVA_OPTS"
              value: "-Xms256m -Xmx256m"
          securityContext:
            privileged: true
      serviceAccountName: elasticsearch-admin
      tolerations:
        - key: node-role.kubernetes.io/master
          effect: NoSchedule
 
---
kind: Service
apiVersion: v1
metadata:
  labels:
    elastic-app: elasticsearch
  name: elasticsearch-discovery
  namespace: ns-elasticsearch
spec:
  ports:
    - port: 9300
      targetPort: 9300
  selector:
    elastic-app: elasticsearch
    role: master
 
---
kind: Deployment
apiVersion: apps/v1beta2
metadata:
  labels:
    elastic-app: elasticsearch
    role: data
  name: elasticsearch-data
  namespace: ns-elasticsearch
spec:
  replicas: 2
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      elastic-app: elasticsearch
  template:
    metadata:
      labels:
        elastic-app: elasticsearch
        role: data
    spec:
      containers:
        - name: elasticsearch-data
          image: docker.elastic.co/elasticsearch/elasticsearch:6.2.2-1
          lifecycle:
            postStart:
              exec:
                command: ["/bin/bash", "-c", "sysctl -w vm.max_map_count=262144; ulimit -l unlimited;"]
          ports:
            - containerPort: 9200
              protocol: TCP
            - containerPort: 9300
              protocol: TCP
          volumeMounts:
            - name: esdata
              mountPath: /usr/share/elasticsearch/data
          env:
            - name: "cluster.name"
              value: "elasticsearch-cluster"
            - name: "bootstrap.memory_lock"
              value: "true"
            - name: "discovery.zen.ping.unicast.hosts"
              value: "elasticsearch-discovery"
            - name: "node.master"
              value: "false"
            - name: "node.data"
              value: "true"
            - name: "ES_JAVA_OPTS"
              value: "-Xms256m -Xmx256m"
          securityContext:
            privileged: true
      volumes:
        - name: esdata
          emptyDir: {}
      serviceAccountName: elasticsearch-admin
      tolerations:
        - key: node-role.kubernetes.io/master
          effect: NoSchedule
 
---
kind: Service
apiVersion: v1
metadata:
  labels:
    elastic-app: elasticsearch-service
  name: elasticsearch-service
  namespace: ns-elasticsearch
spec:
  ports:
    - port: 9200
      targetPort: 9200
  selector:
    elastic-app: elasticsearch

```