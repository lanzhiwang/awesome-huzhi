## kubernetes python

### python 驱动相关组件

![](./python_client.png)

### kubernetes python client 基本使用

1. 在 kubernetes 集群上创建管理员账号
2. 获取账号对应的 token
3. 获取 apiserver 地址 apiserver_url
4. 使用 token 和 apiserver_url 连接集群
5. 调用相关 api 进行操作

### 服务发现方式

pod 访问集群内部的 pod

1. 通过环境变量发现服务（服务要早于 pod 创建）
2. 通过 DNS 发现服务（修改容器的 dnsPolicy 属性）
	* 使用 DNS 方法怎么发现 port

pod 连接外部的服务

1. endpoint
2. ExternalName

将服务暴露给外部客户端

1. NodePort
2. LoadBalancer
3. Ingress

* 由于 python 相关容器也运行在 pod 中，所以使用域名配置相关 ip，port 暂时写死。
* 账号密码统一用 secret 共享

### 问题

* SQL server、ES 等如果长时间无法返回结果或者在连接时pod被重新调度，应该如何重试？

### kubernetes python client 基本使用方法

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

from kubernetes import client, config

def main():
    # Define the barer token we are going to use to authenticate.
    # See here to create the token:
    # https://kubernetes.io/docs/tasks/access-application-cluster/access-cluster/
    Token = ''

    APISERVER = 'https://192.168.1.12:8443'

    # Create a configuration object
    configuration = client.Configuration()

    # Specify the endpoint of your Kube cluster
    configuration.host = APISERVER

    # Security part.
    # In this simple example we are not going to verify the SSL certificate of
    # the remote cluster (for simplicity reason)
    # Nevertheless if you want to do it you can with these 2 parameters
    # configuration.verify_ssl=True
    # ssl_ca_cert is the filepath to the file that contains the certificate.
    # configuration.ssl_ca_cert="certificate"
    # configuration.ssl_ca_cert = 'ca.crt'
    configuration.verify_ssl = False

    # configuration.api_key["authorization"] = "bearer " + Token
    # configuration.api_key_prefix['authorization'] = 'Bearer'
    configuration.api_key = {"authorization": "Bearer " + Token}

    # Create a ApiClient with our config
    client.Configuration.set_default(configuration)

    # Do calls
    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" %
              (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


if __name__ == '__main__':
    main()
    
```


```bash
cat CreateServiceAccount.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kube-system

cat RoleBinding.yaml
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kube-system

kubectl create -f CreateServiceAccount.yaml
kubectl create -f RoleBinding.yaml

# 获取 admin-user token
kubectl describe secret $(kubectl get secret -n kube-system | grep ^admin-user | awk '{print $1}') -n kube-system | grep -E '^token'| awk '{print $2}'

# 获取 apiserver 地址
kubectl config view --minify | grep server | cut -f 2- -d ":" | tr -d " "
```

### 参考

* https://github.com/kubernetes-client/python
* https://kubernetes.io/docs/reference/using-api/client-libraries/
