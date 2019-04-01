## Deploy a SQL Server Always On availability group on a Kubernetes cluster

### 前提条件

* SQL Server 2019

### 整体部署说明

![](./sqlserver.png)

### 部署 sqlserver 使用到的 Kubernetes资源

![](./sqlserver_Kubernetes.png)

### 部署步骤

1. Create the Kubernetes cluster
2. Deploy the operator
3. Configure the storage
4. Deploy the StatefulSet
5. Create the databases and attach them to the availability group

### 问题

* sqlserver operator 注册了 sqlserver 资源，也创建了 sqlserver 实例，是怎样做到的？
* sqlserver 资源的作用？
* 怎样构建在 windows 上运行的 docker 镜像??
* sqlserver 在 Windows 节点和 Linux 节点上运行有没有区别，是否要选择只在 Windows 上运行？

### 参考

* https://docs.microsoft.com/en-us/sql/linux/sql-server-ag-kubernetes?view=sqlallproducts-allversions

### 相关文件

#### operator.yaml

```
apiVersion: v1
kind: Namespace
metadata: {name: ag1}
---
apiVersion: v1
kind: ServiceAccount
metadata: {name: mssql-operator, namespace: ag1}
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata: {name: mssql-operator-ag1}
rules:
- apiGroups: ['']
  resources: [serviceaccounts, services]
  verbs: [create, get, update, delete]
- apiGroups: [batch]
  resources: [jobs]
  verbs: [create, get, update, delete]
- apiGroups: [rbac.authorization.k8s.io]
  resources: [roles, rolebindings]
  verbs: [create, get, update, delete]
- apiGroups: [apps]
  resources: [statefulsets]
  verbs: [create, delete, get, update]
- apiGroups: ['']
  resources: [configmaps, endpoints, secrets]
  verbs: [create, get, update, watch, delete]
- apiGroups: ['']
  resources: [pods]
  verbs: [get, list, update]
- apiGroups: [apiextensions.k8s.io]
  resources: [customresourcedefinitions]
  verbs: [create]
- apiGroups: [apiextensions.k8s.io]
  resourceNames: [sqlservers.mssql.microsoft.com]
  resources: [customresourcedefinitions]
  verbs: [delete, get, update]
- apiGroups: [mssql.microsoft.com]
  resources: [sqlservers]
  verbs: [get, list, watch]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata: {name: mssql-operator-ag1}
roleRef: {apiGroup: rbac.authorization.k8s.io, kind: ClusterRole, name: mssql-operator-ag1}
subjects:
- {kind: ServiceAccount, name: mssql-operator, namespace: ag1}
---
apiVersion: apps/v1beta2
kind: Deployment
metadata: {name: mssql-operator, namespace: ag1}
spec:
  replicas: 1
  selector:
    matchLabels: {app: mssql-operator}
  template:
    metadata:
      labels: {app: mssql-operator}
    spec:
      containers:
      - command: [/mssql-server-k8s-operator]
        env:
        - name: MSSQL_K8S_NAMESPACE
          valueFrom:
            fieldRef: {fieldPath: metadata.namespace}
        image: mcr.microsoft.com/mssql/ha:2019-CTP2.1-ubuntu
        name: mssql-operator
      serviceAccount: mssql-operator
```
### Create a secret

```
kubectl create secret generic sql-secrets --from-literal=sapassword="<>" --from-literal=masterkeypassword="<>"  --namespace ag1
```

### sqlserver.yaml

```
apiVersion: mssql.microsoft.com/v1
kind: SqlServer
metadata:
  labels: {name: mssql1, type: sqlservr}
  name: mssql1
  namespace: ag1
spec:
  acceptEula: true
  agentsContainerImage: mcr.microsoft.com/mssql/ha:2019-CTP2.1-ubuntu
  availabilityGroups: [ag1]
  instanceRootVolumeClaimTemplate:
    accessModes: [ReadWriteOnce]
    resources:
      requests: {storage: 5Gi}
    storageClass: default
  saPassword:
    secretKeyRef: {key: sapassword, name: sql-secrets}
  sqlServerContainer: {image: 'mcr.microsoft.com/mssql/server:2019-CTP2.1-ubuntu'}
---
apiVersion: v1
kind: Service
metadata: {name: mssql1, namespace: ag1}
spec:
  ports:
  - {name: tds, port: 1433}
  selector: {name: mssql1, type: sqlservr}
  type: LoadBalancer
---
apiVersion: mssql.microsoft.com/v1
kind: SqlServer
metadata:
  labels: {name: mssql2, type: sqlservr}
  name: mssql2
  namespace: ag1
spec:
  acceptEula: true
  agentsContainerImage: mcr.microsoft.com/mssql/ha:2019-CTP2.1-ubuntu
  availabilityGroups: [ag1]
  instanceRootVolumeClaimTemplate:
    accessModes: [ReadWriteOnce]
    resources:
      requests: {storage: 5Gi}
    storageClass: default
  saPassword:
    secretKeyRef: {key: sapassword, name: sql-secrets}
  sqlServerContainer: {image: 'mcr.microsoft.com/mssql/server:2019-CTP2.1-ubuntu'}
---
apiVersion: v1
kind: Service
metadata: {name: mssql2, namespace: ag1}
spec:
  ports:
  - {name: tds, port: 1433}
  selector: {name: mssql2, type: sqlservr}
  type: LoadBalancer
---
apiVersion: mssql.microsoft.com/v1
kind: SqlServer
metadata:
  labels: {name: mssql3, type: sqlservr}
  name: mssql3
  namespace: ag1
spec:
  acceptEula: true
  agentsContainerImage: mcr.microsoft.com/mssql/ha:2019-CTP2.1-ubuntu
  availabilityGroups: [ag1]
  instanceRootVolumeClaimTemplate:
    accessModes: [ReadWriteOnce]
    resources:
      requests: {storage: 5Gi}
    storageClass: default
  saPassword:
    secretKeyRef: {key: sapassword, name: sql-secrets}
  sqlServerContainer: {image: 'mcr.microsoft.com/mssql/server:2019-CTP2.1-ubuntu'}
---
apiVersion: v1
kind: Service
metadata: {name: mssql3, namespace: ag1}
spec:
  ports:
  - {name: tds, port: 1433}
  selector: {name: mssql3, type: sqlservr}
  type: LoadBalancer
```

### ag-services.yaml

```
apiVersion: v1
kind: Service
metadata: {annotations: null, name: ag1-primary, namespace: ag1}
spec:
  ports:
  - {name: tds, port: 1433, targetPort: 1433}
  selector: {role.ag.mssql.microsoft.com/ag1: primary, type: sqlservr}
  type: LoadBalancer
---
apiVersion: v1
kind: Service
metadata: {annotations: null, name: ag1-secondary, namespace: ag1}
spec:
  ports:
  - {name: tds, port: 1433}
  selector: {role.ag.mssql.microsoft.com/ag1: secondary,
    type: sqlservr}
  type: LoadBalancer
---
```