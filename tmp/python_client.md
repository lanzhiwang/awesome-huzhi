## kubernetes python client

### kubernetes python client 基本使用

1. 在 kubernetes 集群上创建管理员账号
2. 获取账号对应的 token
3. 获取 apiserver 地址 apiserver_url
4. 使用 token 和 apiserver_url 连接集群
5. 调用相关 api 进行操作

### 需要用到的接口

获取服务的相关信息
* GET /api/v1/namespaces/{namespace}/services/{name}

获取 ingress 的相关信息
* GET /apis/extensions/v1beta1/namespaces/{namespace}/ingresses/{name}


### 问题

* 连接数据库


```python
ret = v1.list_service_for_all_namespaces(watch=False)
for i in ret.items:
    print("%s \t%s \t%s \t%s \t%s \n" % (i.kind, i.metadata.namespace, i.metadata.name, i.spec.cluster_ip, i.spec.ports ))
```

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

