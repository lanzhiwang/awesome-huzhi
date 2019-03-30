## gitlab

### gitlab 集群需要解决的问题

* 由于 git 是分布式系统，所以 gitlab 在一定意义上允许在其上托管的代码丢失
* 如果 gitlab 集群崩溃，用户的认证信息可能丢失，需要重新认证，这是不合理的，所以需要做持久化处理
* 做 CI/CD 时需要在 gitlab 上做相关设置，所以也需要把设置参数做持久化处理


[参考](https://github.com/IBM/Kubernetes-container-service-GitLab-sample)
