### kube-apiserver

* admission 是什么？
* batch mode 是什么？
* ThrottleQPS 是什么？
* webhook ?
* CORS ？
* inflight ？

```
$ ./kube-apiserver -h
The Kubernetes API server validates and configures data for the api objects which include pods, services, replicationcontrollers, and
others. The API Server services REST operations and provides the frontend to the cluster's shared state through which all other components interact.

Usage:
  kube-apiserver [flags]

Flags:

--admission-control strings
Admission is divided into two phases. In the first phase, only mutating admission plugins run. In the second phase, only validating admission plugins run. The names in the below list may represent a validating plugin, a mutating plugin, or both. The order of plugins in which they are passed to this flag does not matter. Comma-delimited list of: AlwaysAdmit, AlwaysDeny, AlwaysPullImages, DefaultStorageClass, DefaultTolerationSeconds, DenyEscalatingExec, DenyExecOnPrivileged, EventRateLimit, ExtendedResourceToleration, ImagePolicyWebhook, InitialResources, Initializers, LimitPodHardAntiAffinityTopology, LimitRanger, MutatingAdmissionWebhook, NamespaceAutoProvision, NamespaceExists, NamespaceLifecycle, NodeRestriction, OwnerReferencesPermissionEnforcement, PersistentVolumeClaimResize, PersistentVolumeLabel, PodNodeSelector, PodPreset, PodSecurityPolicy, PodTolerationRestriction, Priority, ResourceQuota, SecurityContextDeny, ServiceAccount, StorageObjectInUseProtection, ValidatingAdmissionWebhook. (DEPRECATED: Use --enable-admission-plugins or --disable-admission-plugins instead. Will be removed in a future version.)  入学分为两个阶段。在第一阶段，只运行变异插入插件。在第二阶段，仅运行验证许可插件。以下列表中的名称可能代表验证插件，变异插件或两者。它们传递给此标志的插件顺序无关紧要。逗号分隔的列表：
（已弃用：请改用--enable-admission-plugins或--disable-admission-plugins。将来的版本将删除。）

--admission-control-config-file string
File with admission control configuration.

--advertise-address ip
The IP address on which to advertise the apiserver to members of the cluster. This address must be reachable by the rest of the cluster. If blank, the --bind-address will be used. If --bind-address is unspecified, the host's default interface will be used.  用于向群集成员通告apiserver的IP地址。 该地址必须可由群集的其余部分访问。 如果为空，则使用--bind-address。 如果未指定--bind-address，将使用主机的默认接口。

--allow-privileged
If true, allow privileged containers. [default=false]  如果为true，则允许特权容器。[默认= FALSE]

--alsologtostderr
log to standard error as well as files  记录标准错误以及文件

--anonymous-auth
Enables anonymous requests to the secure port of the API server. Requests that are not rejected by another authentication method are treated as anonymous requests. Anonymous requests have a username of system:anonymous, and a group name of system:unauthenticated. (default true)  启用对API服务器的安全端口的匿名请求。 未被其他身份验证方法拒绝的请求将被视为匿名请求。 匿名请求的用户名为system：anonymous，组名为system：unauthenticated。 （默认为true）

--apiserver-count int
The number of apiservers running in the cluster, must be a positive number. (default 1)  群集中运行的备用数量必须为正数。 （默认1）

--audit-log-batch-buffer-size int
The size of the buffer to store events before batching and writing. Only used in batch mode. (default 10000)  在批处理和写入之前存储事件的缓冲区的大小。 仅用于批处理模式。 （默认10000）

--audit-log-batch-max-size int
The maximum size of a batch. Only used in batch mode. (default 400)  批次的最大大小。 仅用于批处理模式。 （默认400）

--audit-log-batch-max-wait duration
The amount of time to wait before force writing the batch that hadn't reached the max size. Only used in batch mode. (default 30s)  强制写入未达到最大大小的批处理之前等待的时间。 仅用于批处理模式。 （默认30秒）

--audit-log-batch-throttle-burst int
Maximum number of requests sent at the same moment if ThrottleQPS was not utilized before. Only used in batch mode. (default 15)  如果之前未使用ThrottleQPS，则在同一时刻发送的最大请求数。 仅用于批处理模式。 （默认15）

--audit-log-batch-throttle-enable
Whether batching throttling is enabled. Only used in batch mode.  是否启用批量限制。 仅用于批处理模式。

--audit-log-batch-throttle-qps float32
Maximum average number of batches per second. Only used in batch mode. (default 10)  每秒最大平均批次数。 仅用于批处理模式。 （默认10）

--audit-log-format string
Format of saved audits. "legacy" indicates 1-line text format for each event. "json" indicates structured json format. Requires the 'AdvancedAuditing' feature gate. Known formats are legacy,json. (default "json")  已保存审核的格式。 “legacy”表示每个事件的1行文本格式。 “json”表示结构化的json格式。 需要“AdvancedAuditing”功能门。 已知的格式是legacy，json。 （默认“json”）

--audit-log-maxage int
The maximum number of days to retain old audit log files based on the timestamp encoded in their filename.  根据文件名中编码的时间戳保留旧审核日志文件的最大天数。

--audit-log-maxbackup int
The maximum number of old audit log files to retain.  要保留的最大旧审核日志文件数。

--audit-log-maxsize int
The maximum size in megabytes of the audit log file before it gets rotated.  审计日志文件旋转之前的最大大小（兆字节）。

--audit-log-mode string
Strategy for sending audit events. Blocking indicates sending events should block server responses. Batch causes the backend to buffer and write events asynchronously. Known modes are batch,blocking. (default "blocking")  发送审计事件的策略。 阻止表示发送事件应阻止服务器响应。 批处理导致后端缓冲并异步写入事件。 已知模式是批量，阻止。 （默认“阻止”）

--audit-log-path string
If set, all requests coming to the apiserver will be logged to this file.  '-' means standard out.

--audit-log-truncate-enabled
Whether event and batch truncating is enabled.

--audit-log-truncate-max-batch-size int
Maximum size of the batch sent to the underlying backend. Actual serialized size can be several hundreds of bytes greater. If a batch exceeds this limit, it is split into several batches of smaller size. (default 10485760)  发送到底层后端的批处理的最大大小。 实际的序列化大小可以大几百个字节。 如果批次超过此限制，则将其拆分为几个较小的批次。 （默认10485760）

--audit-log-truncate-max-event-size int
Maximum size of the audit event sent to the underlying backend. If the size of an event is greater than this number, first request and response are removed, andif this doesn't reduce the size enough, event is discarded. (default 102400) 发送到底层后端的审计事件的最大大小。 如果事件的大小大于此数字，则会删除第一个请求和响应，如果这不会减小足够的大小，则会丢弃事件。 （默认102400）

--audit-policy-file string
Path to the file that defines the audit policy configuration. Requires the 'AdvancedAuditing' feature gate. With AdvancedAuditing, a profile is required to enable auditing.  定义审核策略配置的文件的路径。 需要“AdvancedAuditing”功能门。 使用AdvancedAuditing时，需要配置文件才能启用审核。

--audit-webhook-batch-buffer-size int
The size of the buffer to store events before batching and writing. Only used in batch mode. (default 10000)

--audit-webhook-batch-max-size int
The maximum size of a batch. Only used in batch mode. (default 400)

--audit-webhook-batch-max-wait duration
The amount of time to wait before force writing the batch that hadn't reached the max size. Only used in batch mode. (default 30s)

--audit-webhook-batch-throttle-burst int
Maximum number of requests sent at the same moment if ThrottleQPS was not utilized before. Only used in batch mode. (default 15)

--audit-webhook-batch-throttle-enable
Whether batching throttling is enabled. Only used in batch mode. (default true)

--audit-webhook-batch-throttle-qps float32
Maximum average number of batches per second. Only used in batch mode. (default 10)

--audit-webhook-config-file string
Path to a kubeconfig formatted file that defines the audit webhook configuration. Requires the 'AdvancedAuditing' feature gate.

--audit-webhook-initial-backoff duration
The amount of time to wait before retrying the first failed request. (default 10s)

--audit-webhook-mode string
Strategy for sending audit events. Blocking indicates sending events should block server responses. Batch causes the backend to buffer and write events asynchronously. Known modes are batch,blocking. (default "batch")

--audit-webhook-truncate-enabled
Whether event and batch truncating is enabled.

--audit-webhook-truncate-max-batch-size int
Maximum size of the batch sent to the underlying backend. Actual serialized size can be several hundreds of bytes greater. If a batch exceeds this limit, it is split into several batches of smaller size. (default 10485760)

--audit-webhook-truncate-max-event-size int
Maximum size of the audit event sent to the underlying backend. If the size of an event is greater than this number, first request and response are removed, andif this doesn't reduce the size enough, event is discarded. (default 102400)

--authentication-token-webhook-cache-ttl duration
The duration to cache responses from the webhook token authenticator. (default 2m0s)  缓存来自webhook令牌身份验证器的响应的持续时间。 （默认2m0s）

--authentication-token-webhook-config-file string
File with webhook configuration for token authentication in kubeconfig format. The API server will query the remote service to determine authentication for bearer tokens.  具有webhook配置的文件，用于以kubeconfig格式进行令牌认证。 API服务器将查询远程服务以确定对承载令牌的认证。

--authorization-mode string
Ordered list of plug-ins to do authorization on secure port. Comma-delimited list of: AlwaysAllow,AlwaysDeny,ABAC,Webhook,RBAC,Node. (default "AlwaysAllow")  在安全端口上执行授权的有序插件列表。 以逗号分隔的列表：AlwaysAllow，AlwaysDeny，ABAC，Webhook，RBAC，Node。 （默认为“AlwaysAllow”）

--authorization-policy-file string
File with authorization policy in csv format, used with --authorization-mode=ABAC, on the secure port.  文件带有csv格式的授权策略，与安全端口上的--authorization-mode = ABAC一起使用。

--authorization-webhook-cache-authorized-ttl duration
The duration to cache 'authorized' responses from the webhook authorizer. (default 5m0s)  从webhook授权程序缓存“已授权”响应的持续时间。 （默认5m0s）

--authorization-webhook-cache-unauthorized-ttl duration
The duration to cache 'unauthorized' responses from the webhook authorizer. (default 30s)  从webhook授权程序缓存“未授权”响应的持续时间。 （默认30秒）

--authorization-webhook-config-file string
File with webhook configuration in kubeconfig format, used with --authorization-mode=Webhook. The API server will query the remote service to determine access on the API server's secure port.

--basic-auth-file string
If set, the file that will be used to admit requests to the secure port of the API server via http basic authentication.  如果设置，将用于通过http基本身份验证向API服务器的安全端口发出请求的文件。

--bind-address ip
The IP address on which to listen for the --secure-port port. The associated interface(s) must be reachable by the rest of the cluster, and by CLI/web clients. If blank, all interfaces will be used (0.0.0.0 for all IPv4 interfaces and :: for all IPv6 interfaces). (default 0.0.0.0)  要监听--secure-port端口的IP地址。 关联的接口必须可由群集的其余部分以及CLI / Web客户端访问。 如果为空，将使用所有接口（所有IPv4接口均为0.0.0.0，所有IPv6接口为::）。 （默认0.0.0.0）

--cert-dir string
The directory where the TLS certs are located. If --tls-cert-file and --tls-private-key-file are provided, this flag will be ignored. (default "/var/run/kubernetes")

--client-ca-file string
If set, any request presenting a client certificate signed by one of the authorities in the client-ca-file is authenticated with an identity corresponding to the CommonName of the client certificate.  如果设置，则表示由client-ca文件中的某个权限签名的客户端证书的任何请求都将使用与客户端证书的CommonName对应的标识进行身份验证。

--cloud-config string
The path to the cloud provider configuration file. Empty string for no configuration file.

--cloud-provider string
The provider for cloud services. Empty string for no provider.

--cloud-provider-gce-lb-src-cidrs cidrs
CIDRs opened in GCE firewall for LB traffic proxy & health checks (default 130.211.0.0/22,209.85.152.0/22,209.85.204.0/22,35.191.0.0/16)

--contention-profiling
Enable lock contention profiling, if profiling is enabled  如果启用了性能分析，则启用锁争用性分析

--cors-allowed-origins strings
List of allowed origins for CORS, comma separated.  An allowed origin can be a regular expression to support subdomain matching. If this list is empty CORS will not be enabled.  CORS允许的来源列表，以逗号分隔。 允许的原点可以是支持子域匹配的正则表达式。 如果此列表为空，则不会启用CORS。

--default-not-ready-toleration-seconds int
Indicates the tolerationSeconds of the toleration for notReady:NoExecute that is added by default to every pod that does not already have such a toleration. (default 300)  表示notReady的容忍度的绝对值：NoExecute默认情况下添加到尚未具有此类容差的每个容器中。 （默认300）

--default-unreachable-toleration-seconds int
Indicates the tolerationSeconds of the toleration for unreachable:NoExecute that is added by default to every pod that does not already have such a toleration. (default 300)  表示容忍无法访问的容忍度：默认情况下，NoExecute添加到尚未具有此容忍度的每个容器中。 （默认300）

--default-watch-cache-size int
Default watch cache size. If zero, watch cache will be disabled for resources that do not have a default watch size set. (default 100)  默认监视缓存大小。 如果为零，则对于未设置默认监视大小的资源，将禁用监视缓存。 （默认为100）

--delete-collection-workers int
Number of workers spawned for DeleteCollection call. These are used to speed up namespace cleanup. (default 1)  为DeleteCollection调用生成的worker数。 这些用于加速命名空间清理。 （默认1）

--deserialization-cache-size int
Number of deserialized json objects to cache in memory.  要在内存中缓存的反序列化json对象的数量。

--disable-admission-plugins strings
admission plugins that should be disabled although they are in the default enabled plugins list. Comma-delimited list of admission plugins: AlwaysAdmit, AlwaysDeny, AlwaysPullImages, DefaultStorageClass, DefaultTolerationSeconds, DenyEscalatingExec, DenyExecOnPrivileged, EventRateLimit, ExtendedResourceToleration, ImagePolicyWebhook, InitialResources, Initializers, LimitPodHardAntiAffinityTopology, LimitRanger, MutatingAdmissionWebhook, NamespaceAutoProvision, NamespaceExists, NamespaceLifecycle, NodeRestriction, OwnerReferencesPermissionEnforcement, PersistentVolumeClaimResize, PersistentVolumeLabel, PodNodeSelector, PodPreset, PodSecurityPolicy, PodTolerationRestriction, Priority, ResourceQuota, SecurityContextDeny, ServiceAccount, StorageObjectInUseProtection, ValidatingAdmissionWebhook. The order of plugins in this flag does not matter.

--enable-admission-plugins strings
admission plugins that should be enabled in addition to default enabled ones. Comma-delimited list of admission plugins: AlwaysAdmit, AlwaysDeny, AlwaysPullImages, DefaultStorageClass, DefaultTolerationSeconds, DenyEscalatingExec, DenyExecOnPrivileged, EventRateLimit, ExtendedResourceToleration, ImagePolicyWebhook, InitialResources, Initializers, LimitPodHardAntiAffinityTopology, LimitRanger, MutatingAdmissionWebhook, NamespaceAutoProvision, NamespaceExists, NamespaceLifecycle, NodeRestriction, OwnerReferencesPermissionEnforcement, PersistentVolumeClaimResize, PersistentVolumeLabel, PodNodeSelector, PodPreset, PodSecurityPolicy, PodTolerationRestriction, Priority, ResourceQuota, SecurityContextDeny, ServiceAccount, StorageObjectInUseProtection, ValidatingAdmissionWebhook. The order of plugins in this flag does not matter.

--enable-aggregator-routing
Turns on aggregator routing requests to endoints IP rather than cluster IP.  将聚合器路由请求打开到端点IP而不是群集IP。

--enable-bootstrap-token-auth
Enable to allow secrets of type 'bootstrap.kubernetes.io/token' in the 'kube-system' namespace to be used for TLS bootstrapping authentication.  允许在'kube-system'命名空间中允许类型为'bootstrap.kubernetes.io/token'的机密用于TLS引导认证。

--enable-garbage-collector
Enables the generic garbage collector. MUST be synced with the corresponding flag of the kube-controller-manager. (default true)  启用通用垃圾收集器。 必须与kube-controller-manager的相应标志同步。 （默认为true）

--enable-logs-handler
If true, install a /logs handler for the apiserver logs. (default true)

--enable-swagger-ui
Enables swagger ui on the apiserver at /swagger-ui

--endpoint-reconciler-type string
Use an endpoint reconciler (master-count, lease, none) (default "master-count")  使用端点协调程序（主计数，租用，无）（默认为“主计数”）

--etcd-cafile string
SSL Certificate Authority file used to secure etcd communication.  用于保护etcd通信的SSL证书颁发机构文件。

--etcd-certfile string
SSL certification file used to secure etcd communication.  用于保护etcd通信的SSL认证文件。

--etcd-compaction-interval duration
The interval of compaction requests. If 0, the compaction request from apiserver is disabled. (default 5m0s)  压缩请求的间隔。 如果为0，则禁用来自apiserver的压缩请求。 （默认5m0s）

--etcd-count-metric-poll-period duration
Frequency of polling etcd for number of resources per type. 0 disables the metric collection. (default 1m0s)  每种类型的资源数量的轮询频率等。 0禁用度量标准集合。 （默认1m0s）

--etcd-keyfile string
SSL key file used to secure etcd communication.  用于保护etcd通信的SSL密钥文件。

--etcd-prefix string
The prefix to prepend to all resource paths in etcd. (default "/registry")

--etcd-servers strings
List of etcd servers to connect with (scheme://ip:port), comma separated.  要连接的etcd服务器列表（scheme：// ip：port），逗号分隔。

--etcd-servers-overrides strings
Per-resource etcd servers overrides, comma separated. The individual override format: group/resource#servers, where servers are http://ip:port, semicolon separated.  每个资源的etcd服务器覆盖，逗号分隔。 单个覆盖格式：group / resource＃servers，其中服务器是http：// ip：port，分号分隔。

--event-ttl duration
Amount of time to retain events. (default 1h0m0s)  保留事件的时间量。 （默认1h0m0s）

--experimental-encryption-provider-config string
The file containing configuration for encryption providers to be used for storing secrets in etcd  包含用于在etcd中存储机密的加密提供程序的配置的文件

--external-hostname string
The hostname to use when generating externalized URLs for this master (e.g. Swagger API Docs).

--feature-gates mapStringBool
A set of key=value pairs that describe feature gates for alpha/experimental features. Options are:
APIListChunking=true|false (BETA - default=true)
APIResponseCompression=true|false (ALPHA - default=false)
Accelerators=true|false (ALPHA - default=false)
AdvancedAuditing=true|false (BETA - default=true)
AllAlpha=true|false (ALPHA - default=false)
AppArmor=true|false (BETA - default=true)
BlockVolume=true|false (ALPHA - default=false)
CPUManager=true|false (BETA - default=true)
CRIContainerLogRotation=true|false (ALPHA - default=false)
CSIPersistentVolume=true|false (BETA - default=true)
CustomPodDNS=true|false (BETA - default=true)
CustomResourceSubresources=true|false (ALPHA - default=false)
CustomResourceValidation=true|false (BETA - default=true)
DebugContainers=true|false (ALPHA - default=false)
DevicePlugins=true|false (BETA - default=true)
DynamicKubeletConfig=true|false (ALPHA - default=false)
EnableEquivalenceClassCache=true|false (ALPHA - default=false)
ExpandPersistentVolumes=true|false (ALPHA - default=false)
ExperimentalCriticalPodAnnotation=true|false (ALPHA - default=false)
ExperimentalHostUserNamespaceDefaulting=true|false (BETA -default=false)
GCERegionalPersistentDisk=true|false (BETA - default=true)
HugePages=true|false (BETA - default=true)
HyperVContainer=true|false (ALPHA - default=false)
Initializers=true|false (ALPHA - default=false)
LocalStorageCapacityIsolation=true|false (BETA - default=true)
MountContainers=true|false (ALPHA - default=false)
MountPropagation=true|false (BETA - default=true)
PersistentLocalVolumes=true|false (BETA - default=true)
PodPriority=true|false (ALPHA - default=false)
PodShareProcessNamespace=true|false (ALPHA - default=false)
ReadOnlyAPIDataVolumes=true|false (DEPRECATED - default=true)
ResourceLimitsPriorityFunction=true|false (ALPHA - default=false)
RotateKubeletClientCertificate=true|false (BETA - default=true)
RotateKubeletServerCertificate=true|false (ALPHA - default=false)
RunAsGroup=true|false (ALPHA - default=false)
ScheduleDaemonSetPods=true|false (ALPHA - default=false)
ServiceNodeExclusion=true|false (ALPHA - default=false)
ServiceProxyAllowExternalIPs=true|false (DEPRECATED - default=false)
StorageObjectInUseProtection=true|false (BETA - default=true)
StreamingProxyRedirects=true|false (BETA - default=true)
SupportIPVSProxyMode=true|false (BETA - default=true)
SupportPodPidsLimit=true|false (ALPHA - default=false)
TaintBasedEvictions=true|false (ALPHA - default=false)
TaintNodesByCondition=true|false (ALPHA - default=false)
TokenRequest=true|false (ALPHA - default=false)
VolumeScheduling=true|false (BETA - default=true)
VolumeSubpath=true|false (default=true)
一组key = value对，用于描述alpha / experimental特征的特征门。 选项包括：

-h, --help
help for kube-apiserver

--http2-max-streams-per-connection int
The limit that the server gives to clients for the maximum number of streams in an HTTP/2 connection. Zero means to use golang's default.  服务器为HTTP / 2连接中的最大流数量提供给客户端的限制。 零表示使用golang的默认值。

--insecure-bind-address ip
The IP address on which to serve the --insecure-port (set to 0.0.0.0 for all IPv4 interfaces and :: for all IPv6 interfaces). (default 127.0.0.1) (DEPRECATED: This flag will be removed in a future version.)  为--insecure-port提供服务的IP地址（对于所有IPv4接口设置为0.0.0.0，对于所有IPv6接口设置为::）。 （默认为127.0.0.1）（已弃用：此标志将在以后的版本中删除。）

--insecure-port int
The port on which to serve unsecured, unauthenticated access. It is assumed that firewall rules are set up such that this port is not reachable from outside of the cluster and that port 443 on the cluster's public address is proxied to this port. This is performed by nginx in the default setup. Set to zero to disable. (default 8080) (DEPRECATED: This flag will be removed in a future version.)  用于提供不安全，未经身份验证的访问的端口。 假设设置了防火墙规则，使得无法从群集外部访问此端口，并且群集的公共地址上的端口443代理到此端口。 这是由默认设置中的nginx执行的。 设置为零以禁用。 （默认为8080）（已弃用：此标志将在以后的版本中删除。）

--ir-data-source string
Data source used by InitialResources. Supported options: influxdb, gcm. (default "influxdb")  InitialResources使用的数据源。 支持的选项：Influxdb，gcm。 （默认“influxdb”）

--ir-dbname string
InfluxDB database name which contains metrics required by InitialResources (default "k8s")

--ir-hawkular string
Hawkular configuration URL

--ir-influxdb-host string
Address of InfluxDB which contains metrics required by InitialResources (default "localhost:8080/api/v1/namespaces/kube-system/services/monitoring-influxdb:api/proxy")

--ir-namespace-only
Whether the estimation should be made only based on data from the same namespace.  是否应仅基于来自相同命名空间的数据进行估计。

--ir-password string
Password used for connecting to InfluxDB (default "root")

--ir-percentile int
Which percentile of samples should InitialResources use when estimating resources. For experiment purposes. (default 90)  nitialResources在估算资源时应使用哪个样本百分比。 用于实验目的。 （默认90）

--ir-user string
User used for connecting to InfluxDB (default "root")

--kubelet-certificate-authority string
Path to a cert file for the certificate authority.

--kubelet-client-certificate string
Path to a client cert file for TLS.

--kubelet-client-key string
Path to a client key file for TLS.

--kubelet-https
Use https for kubelet connections. (default true)

--kubelet-preferred-address-types strings
List of the preferred NodeAddressTypes to use for kubelet connections. (default [Hostname,InternalDNS,InternalIP,ExternalDNS,ExternalIP])  用于kubelet连接的首选NodeAddressType的列表。 （默认[Hostname，InternalDNS，InternalIP，ExternalDNS，ExternalIP]）

--kubelet-read-only-port uint
DEPRECATED: kubelet port. (default 10255)

--kubelet-timeout duration
Timeout for kubelet operations. (default 5s)

--kubernetes-service-node-port int
If non-zero, the Kubernetes master service (which apiserver creates/maintains) will be of type NodePort, using this as the value of the port. If zero, the Kubernetes master service will be of type ClusterIP.  如果非零，则Kubernetes主服务（apiserver创建/维护）将是NodePort类型，使用此作为端口的值。 如果为零，则Kubernetes主服务将为ClusterIP类型。

--log-backtrace-at traceLocation
when logging hits line file:N, emit a stack trace (default :0)

--log-dir string
If non-empty, write log files in this directory

--log-flush-frequency duration
Maximum number of seconds between log flushes (default 5s)

--logtostderr
log to standard error instead of files (default true)

--master-service-namespace string
DEPRECATED: the namespace from which the kubernetes master services should be injected into pods. (default "default")  DEPRECATED：应该将kubernetes主服务注入pod的命名空间。 （默认为“默认”）

--max-connection-bytes-per-sec int
If non-zero, throttle each user connection to this number of bytes/sec. Currently only applies to long-running requests.  如果非零，则将每个用户连接限制为此字节数/秒。 目前仅适用于长时间运行的请求。

--max-mutating-requests-inflight int
The maximum number of mutating requests in flight at a given time. When the server exceeds this, it rejects requests. Zero for no limit. (default 200)  在给定时间内飞行中的最大变异请求数。 当服务器超过此值时，它会拒绝请求。 零无限制。 （默认200）

--max-requests-inflight int
The maximum number of non-mutating requests in flight at a given time. When the server exceeds this, it rejects requests. Zero for no limit. (default 400)

--min-request-timeout int
An optional field indicating the minimum number of seconds a handler must keep a request open before timing it out. Currently only honored by the watch request handler, which picks a randomized value above this number as the connection timeout, to spread out load. (default 1800)  一个可选字段，指示处理程序在计时之前必须保持请求打开的最小秒数。 目前仅受到监视请求处理程序的支持，该处理程序选择高于此数字的随机值作为连接超时，以分散负载。 （默认1800）

--oidc-ca-file string
If set, the OpenID server's certificate will be verified by one of the authorities in the oidc-ca-file, otherwise the host's root CA set will be used.  如果设置，则将由oidc-ca文件中的某个权限验证OpenID服务器的证书，否则将使用主机的根CA集。

--oidc-client-id string
The client ID for the OpenID Connect client, must be set if oidc-issuer-url is set.

--oidc-groups-claim string
If provided, the name of a custom OpenID Connect claim for specifying user groups. The claim value is expected to be a string or array of strings. This flag is experimental, please see the authentication documentation for further details.

--oidc-groups-prefix string
If provided, all groups will be prefixed with this value to prevent conflicts with other authentication strategies.

--oidc-issuer-url string
The URL of the OpenID issuer, only HTTPS scheme will be accepted. If set, it will be used to verify the OIDC JSON Web Token (JWT).

--oidc-signing-algs strings
Comma-separated list of allowed JOSE asymmetric signing algorithms. JWTs with a 'alg' header value not in this list will be rejected. Values are defined by RFC 7518 https://tools.ietf.org/html/rfc7518#section-3.1. (default [RS256])

--oidc-username-claim string
The OpenID claim to use as the user name. Note that claims other than the default ('sub') is not guaranteed to be unique and immutable. This flag is experimental, please see the authentication documentation for further details. (default "sub")

--oidc-username-prefix string
If provided, all usernames will be prefixed with this value. If not provided, username claims other than 'email' are prefixed by the issuer URL to avoid clashes. To skip any prefixing, provide the value '-'.

--profiling
Enable profiling via web interface host:port/debug/pprof/ (default true)  通过Web界面主机启用性能分析：port / debug / pprof /（默认为true）

--proxy-client-cert-file string
Client certificate used to prove the identity of the aggregator or kube-apiserver when it must call out during a request. This includes proxying requests to a user api-server and calling out to webhook admission plugins. It is expected that this cert includes a signature from the CA in the --requestheader-client-ca-file flag. That CA is published in the 'extension-apiserver-authentication' configmap in the kube-system namespace. Components receiving calls from kube-aggregator should use that CA to perform their half of the mutual TLS verification.

--proxy-client-key-file string
Private key for the client certificate used to prove the identity of the aggregator or kube-apiserver when it must call out during a request. This includes proxying requests to a user api-server and calling out to webhook admission plugins.

--repair-malformed-updates
If true, server will do its best to fix the update request to pass the validation, e.g., setting empty UID in update request to its existing value. This flag can be turned off after we fix all the clients that send malformed updates. (default true)  如果为true，则服务器将尽力修复更新请求以通过验证，例如，将更新请求中的空UID设置为其现有值。 修复发送格式错误更新的所有客户端后，可以关闭此标志。 （默认为true）

--request-timeout duration
An optional field indicating the duration a handler must keep a request open before timing it out. This is the default request timeout for requests but may be overridden by flags such as --min-request-timeout for specific types of requests. (default 1m0s)  一个可选字段，指示处理程序在计时之前必须保持请求打开的持续时间。 这是请求的默认请求超时，但可能会被特定类型的请求的标志（例如--min-request-timeout）覆盖。 （默认1m0s）

--requestheader-allowed-names strings
List of client certificate common names to allow to provide usernames in headers specified by --requestheader-username-headers. If empty, any client certificate validated by the authorities in --requestheader-client-ca-file is allowed.  允许在--requestheader-username-headers指定的标头中提供用户名的客户端证书通用名称列表。 如果为空，则允许由--requestheader-client-ca-file中的权限验证的任何客户端证书。

--requestheader-client-ca-file string
Root certificate bundle to use to verify client certificates on incoming requests before trusting usernames in headers specified by --requestheader-username-headers  根据--requestheader-username-headers指定的标头中的用户名信任之前用于验证传入请求的客户端证书的根证书包

--requestheader-extra-headers-prefix strings
List of request header prefixes to inspect. X-Remote-Extra- is suggested.  要检查的请求标头前缀列表。 建议使用X-Remote-Extra-。

--requestheader-group-headers strings
List of request headers to inspect for groups. X-Remote-Group is suggested.  要检查组的请求标头列表。 建议使用X-Remote-Group。

--requestheader-username-headers strings
List of request headers to inspect for usernames. X-Remote-User is common.

--runtime-config mapStringString
A set of key=value pairs that describe runtime configuration that may be passed to apiserver. <group>/<version> (or <version> for the core group) key can be used to turn on/off specific api versions. api/all is special key to control all api versions, be careful setting it false, unless you know what you do. api/legacy is deprecated, we will remove it in the future, so stop using it.  一组key = value对，描述可以传递给apiserver的运行时配置。 <group> / <version>（或核心组的<version>）键可用于打开/关闭特定的api版本。 api / all是控制所有api版本的特殊键，小心设置为false，除非你知道你做了什么。 api / legacy已弃用，我们将来会将其删除，因此请停止使用它。

--secure-port int
The port on which to serve HTTPS with authentication and authorization. If 0, don't serve HTTPS at all. (default 6443)  通过身份验证和授权为HTTPS提供服务的端口。 如果为0，则根本不提供HTTPS。 （默认6443）

--service-account-api-audiences strings
Identifiers of the API. The service account token authenticator will validate that tokens used against the API are bound to at least one of these audiences.  API的标识符。 服务帐户令牌验证器将验证针对API使用的令牌是否绑定到这些受众中的至少一个。

--service-account-issuer string
Identifier of the service account token issuer. The issuer will assert this identifier in "iss" claim of issued tokens. This value is a string or URI.  服务帐户令牌颁发者的标识符。 发行人将在发行的令牌的“iss”声明中声明该标识符。 该值是字符串或URI。

--service-account-key-file stringArray
File containing PEM-encoded x509 RSA or ECDSA private or public keys, used to verify ServiceAccount tokens. The specified file can contain multiple keys, and the flag can be specified multiple times with different files. If unspecified, --tls-private-key-file is used. Must be specified when --service-account-signing-key is provided  包含PEM编码的x509 RSA或ECDSA私钥或公钥的文件，用于验证ServiceAccount令牌。 指定的文件可以包含多个键，并且可以使用不同的文件多次指定该标志。 如果未指定，则使用--tls-private-key-file。 必须在提供--service-account-signing-key时指定

--service-account-lookup
If true, validate ServiceAccount tokens exist in etcd as part of authentication. (default true)  如果为true，则验证ServiceAccount令牌作为身份验证的一部分存在于etcd中。 （默认为true）

--service-account-signing-key-file string
Path to the file that contains the current private key of the service account token issuer. The issuer will sign issued ID tokens with this private key. (Ignored unless alpha TokenRequest is enabled)  包含服务帐户令牌颁发者的当前私钥的文件的路径。 发行人将使用此私钥签署已发行的ID令牌。 （忽略除非启用了Alpha TokenRequest)

--service-cluster-ip-range ipNet
A CIDR notation IP range from which to assign service cluster IPs. This must not overlap with any IP ranges assigned to nodes for pods. (default 10.0.0.0/24)  CIDR表示法IP范围，用于分配服务群集IP。 这不得与分配给pod节点的任何IP范围重叠。 （默认10.0.0.0/24）

--service-node-port-range portRange
A port range to reserve for services with NodePort visibility. Example: '30000-32767'. Inclusive at both ends of the range. (default 30000-32767)  为NodePort可见性的服务保留的端口范围。 示例：'30000-32767'。 包括在范围的两端。 （默认30000-32767）

--stderrthreshold severity
logs at or above this threshold go to stderr (default 2)

--storage-backend string
The storage backend for persistence. Options: 'etcd3' (default), 'etcd2'.

--storage-media-type string
The media type to use to store objects in storage. Some resources or storage backends may only support a specific media type and will ignore this setting. (default "application/vnd.kubernetes.protobuf")  用于在存储中存储对象的媒体类型。 某些资源或存储后端可能仅支持特定媒体类型，并将忽略此设置。 （默认“application / vnd.kubernetes.protobuf”）

--storage-versions string
The per-group version to store resources in. Specified in the format "group1/version1,group2/version2,...". In the case where objects are moved from one group to the other, you may specify the format "group1=group2/v1beta1,group3/v1beta1,...". You only need to pass the groups you wish to change from the defaults. It defaults to a list of preferred versions of all registered groups, which is derived from the KUBE_API_VERSIONS environment variable. (default "admission.k8s.io/v1beta1,admissionregistration.k8s.io/v1beta1,apps/v1,authentication.k8s.io/v1,authorization.k8s.io/v1,autoscaling/v1,batch/v1,certificates.k8s.io/v1beta1,componentconfig/v1alpha1,events.k8s.io/v1beta1,extensions/v1beta1,imagepolicy.k8s.io/v1alpha1,networking.k8s.io/v1,policy/v1beta1,rbac.authorization.k8s.io/v1,scheduling.k8s.io/v1alpha1,settings.k8s.io/v1alpha1,storage.k8s.io/v1,v1")

--target-ram-mb int
Memory limit for apiserver in MB (used to configure sizes of caches, etc.)  apiserver的内存限制（MB）（用于配置缓存大小等）

--tls-cert-file string
File containing the default x509 Certificate for HTTPS. (CA cert, if any, concatenated after server cert). If HTTPS serving is enabled, and --tls-cert-file and --tls-private-key-file are not provided, a self-signed certificate and key are generated for the public address and saved to the directory specified by --cert-dir.

--tls-cipher-suites strings
Comma-separated list of cipher suites for the server. Values are from tls package constants (https://golang.org/pkg/crypto/tls/#pkg-constants). If omitted, the default Go cipher suites will be used

--tls-min-version string
Minimum TLS version supported. Value must match version names from https://golang.org/pkg/crypto/tls/#pkg-constants.

--tls-private-key-file string
File containing the default x509 private key matching --tls-cert-file.

--tls-sni-cert-key namedCertKey
A pair of x509 certificate and private key file paths, optionally suffixed with a list of domain patterns which are fully qualified domain names, possibly with prefixed wildcard segments. If no domain patterns are provided, the names of the certificate are extracted. Non-wildcard matches trump over wildcard matches, explicit domain patterns trump over extracted names. For multiple key/certificate pairs, use the --tls-sni-cert-key multiple times. Examples: "example.crt,example.key" or "foo.crt,foo.key:*.foo.com,foo.com". (default [])

--token-auth-file string
If set, the file that will be used to secure the secure port of the API server via token authentication.

-v, --v Level
log level for V logs

--version version[=true]
Print version information and quit

--vmodule moduleSpec
comma-separated list of pattern=N settings for file-filtered logging

--watch-cache
Enable watch caching in the apiserver (default true)

--watch-cache-sizes strings
List of watch cache sizes for every resource (pods, nodes, etc.), comma separated. The individual override format: resource[.group]#size, where resource is lowercase plural (no version), group is optional, and size is a number. It takes effect when watch-cache is enabled. Some resources (replicationcontrollers, endpoints, nodes, pods, services, apiservices.apiregistration.k8s.io) have system defaults set by heuristics, others default to default-watch-cache-size

$ 

```