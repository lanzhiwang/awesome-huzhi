## Ingress 

### 使用 ingress 资源的步骤

1. 安装 Ingress 控制器，使用 nginx-ingress 作为 ingress 控制器
2. 创建 ingress 资源
3. 获取 ingress 的 ip 地址
4. 访问对应的应用

### Ingress 原理

![](./ingress.png)

### 通过 ingress 暴露 es、sqlserver、gitlab 服务

```bash
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: ingress_es_sqlserver_gitlab
spec:
  rules:
  - host: test.es.com
    http:
      paths:
      - path: /
        backend:
          serviceName: elasticsearch
          servicePort: 9200
  - host: test.sqlserver.com
    http:
      paths:
      - path: /
        backend:
          serviceName: ag1-primary
          servicePort: 1433
  - host: test.gitlab.com
    http:
      paths:
      - path: /
        backend:
          serviceName: gitlab
          servicePort: 80

```
