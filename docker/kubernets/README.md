### k8s binary at:

```
https://dl.k8s.io/${K8S_VER}/kubernetes-server-linux-amd64.tar.gz
https://dl.k8s.io/v1.10.4/kubernetes-server-linux-amd64.tar.gz
https://storage.googleapis.com/kubernetes-release/release/v1.10.4/kubernetes-server-linux-amd64.tar.gz

$ ls
kubernetes-server-linux-amd64.tar.gz
$ 
$ tar -zxvf kubernetes-server-linux-amd64.tar.gz
$ 
$ ls
kubernetes  kubernetes-server-linux-amd64.tar.gz
$ 
$ tree -a kubernetes
kubernetes
├── addons
├── kubernetes-src.tar.gz
├── LICENSES
└── server
    └── bin
        ├── apiextensions-apiserver
        ├── cloud-controller-manager
        ├── cloud-controller-manager.docker_tag
        ├── cloud-controller-manager.tar
        ├── hyperkube
        ├── kubeadm
        ├── kube-aggregator
        ├── kube-aggregator.docker_tag
        ├── kube-aggregator.tar
        ├── kube-apiserver
        ├── kube-apiserver.docker_tag
        ├── kube-apiserver.tar
        ├── kube-controller-manager
        ├── kube-controller-manager.docker_tag
        ├── kube-controller-manager.tar
        ├── kubectl
        ├── kubelet
        ├── kube-proxy
        ├── kube-proxy.docker_tag
        ├── kube-proxy.tar
        ├── kube-scheduler
        ├── kube-scheduler.docker_tag
        ├── kube-scheduler.tar
        └── mounter

3 directories, 26 files
$ 

```


* [apiextensions-apiserver]()
* [cloud-controller-manager]()
* [hyperkube]()
* [kubeadm]()
* [kube-aggregator]()
* [kube-apiserver](./01_kube-apiserver.md)
* [kube-controller-manager](./02_kube-controller-manager.md)
* [kubectl](./03_kubectl.md)
* [kubelet](./04_kubelet.md)
* [kube-proxy]()
* [kube-scheduler]()
* [mounter]()

### etcd binary at:

```
https://github.com/coreos/etcd/releases/download/${ETCD_VER}/etcd-${ETCD_VER}-linux-amd64.tar.gz
https://github.com/coreos/etcd/releases/download/v3.3.8/etcd-v3.3.8-linux-amd64.tar.gz

https://storage.googleapis.com/etcd/${ETCD_VER}/etcd-${ETCD_VER}-linux-amd64.tar.gz
https://storage.googleapis.com/etcd/v3.3.8/etcd-v3.3.8-linux-amd64.tar.gz
```

### docker binary at:

```
https://download.docker.com/linux/static/stable/x86_64/docker-${DOCKER_VER}.tgz
https://download.docker.com/linux/static/stable/x86_64/docker-17.03.2-ce.tgz
```

### ca tools at:
```
https://pkg.cfssl.org/R1.2/cfssl_linux-amd64
https://pkg.cfssl.org/R1.2/cfssljson_linux-amd64
https://pkg.cfssl.org/R1.2/cfssl-certinfo_linux-amd64
```

### docker-compose at:

```
https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE}/docker-compose-Linux-x86_64
https://github.com/docker/compose/releases/download/1.18.0/docker-compose-Linux-x86_64
```

### harbor-offline-installer at:

```
https://github.com/vmware/harbor/releases/download/${HARBOR}/harbor-offline-installer-${HARBOR}.tgz
https://github.com/vmware/harbor/releases/download/v1.5.2/harbor-offline-installer-v1.5.2.tgz
```

### cni plugins at:
```
https://github.com/containernetworking/plugins/releases
```

### apiextensions-apiserver

```
$ ./apiextensions-apiserver -h
Launch an API extensions API server

Usage:
   [flags]

Flags:

--admission-control-config-file string
File with admission control configuration.

--alsologtostderr
log to standard error as well as files

--audit-log-batch-buffer-size int
The size of the buffer to store events before batching and writing. Only used in batch mode. (default 10000)

--audit-log-batch-max-size int
The maximum size of a batch. Only used in batch mode. (default 400)

--audit-log-batch-max-wait duration
The amount of time to wait before force writing the batch that hadn't reached the max size. Only used in batch mode. (default 30s)

--audit-log-batch-throttle-burst int
Maximum number of requests sent at the same moment if ThrottleQPS was not utilized before. Only used in batch mode. (default 15)

--audit-log-batch-throttle-enable
Whether batching throttling is enabled. Only used in batch mode.

--audit-log-batch-throttle-qps float32
Maximum average number of batches per second. Only used in batch mode. (default 10)

--audit-log-format string
Format of saved audits. "legacy" indicates 1-line text format for each event. "json" indicates structured json format. Requires the 'AdvancedAuditing' feature gate. Known formats are legacy,json. (default "json")

--audit-log-maxage int
The maximum number of days to retain old audit log files based on the timestamp encoded in their filename.

--audit-log-maxbackup int
The maximum number of old audit log files to retain.

--audit-log-maxsize int
The maximum size in megabytes of the audit log file before it gets rotated.

--audit-log-mode string
Strategy for sending audit events. Blocking indicates sending events should block server responses. Batch causes the backend to buffer and write events asynchronously. Known modes are batch,blocking. (default "blocking")

--audit-log-path string
If set, all requests coming to the apiserver will be logged to this file.  '-' means standard out.

--audit-log-truncate-enabled
Whether event and batch truncating is enabled.

--audit-log-truncate-max-batch-size int
Maximum size of the batch sent to the underlying backend. Actual serialized size can be several hundreds of bytes greater. If a batch exceeds this limit, it is split into several batches of smaller size. (default 10485760)

--audit-log-truncate-max-event-size int
Maximum size of the audit event sent to the underlying backend. If the size of an event is greater than this number, first request and response are removed, andif this doesn't reduce the size enough, event is discarded. (default 102400)

--audit-policy-file string
Path to the file that defines the audit policy configuration. Requires the 'AdvancedAuditing' feature gate. With AdvancedAuditing, a profile is required to enable auditing.

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

--authentication-kubeconfig string
kubeconfig file pointing at the 'core' kubernetes server with enough rights to create tokenaccessreviews.authentication.k8s.io.

--authentication-skip-lookup
If false, the authentication-kubeconfig will be used to lookup missing authentication configuration from the cluster.

--authentication-token-webhook-cache-ttl duration
The duration to cache responses from the webhook token authenticator. (default 10s)

--authorization-kubeconfig string
kubeconfig file pointing at the 'core' kubernetes server with enough rights to create  subjectaccessreviews.authorization.k8s.io.

--authorization-webhook-cache-authorized-ttl duration
The duration to cache 'authorized' responses from the webhook authorizer. (default 10s)

--authorization-webhook-cache-unauthorized-ttl duration
The duration to cache 'unauthorized' responses from the webhook authorizer. (default 10s)

--bind-address ip
The IP address on which to listen for the --secure-port port. The associated interface(s) must be reachable by the rest of the cluster, and by CLI/web clients. If blank, all interfaces will be used (0.0.0.0 for all IPv4 interfaces and :: for all IPv6 interfaces). (default 0.0.0.0)

--cert-dir string
The directory where the TLS certs are located. If --tls-cert-file and --tls-private-key-file are provided, this flag will be ignored. (default "apiserver.local.config/certificates")

--client-ca-file string
If set, any request presenting a client certificate signed by one of the authorities in the client-ca-file is authenticated with an identity corresponding to the CommonName of the client certificate.

--contention-profiling
Enable lock contention profiling, if profiling is enabled

--default-watch-cache-size int
Default watch cache size. If zero, watch cache will be disabled for resources that do not have a default watch size set. (default 100)

--delete-collection-workers int
Number of workers spawned for DeleteCollection call. These are used to speed up namespace cleanup. (default 1)

--deserialization-cache-size int
Number of deserialized json objects to cache in memory.

--disable-admission-plugins strings
admission plugins that should be disabled although they are in the default enabled plugins list. Comma-delimited list of admission plugins: Initializers, MutatingAdmissionWebhook, NamespaceLifecycle, ValidatingAdmissionWebhook. The order of plugins in this flag does not matter.

--enable-admission-plugins strings
admission plugins that should be enabled in addition to default enabled ones. Comma-delimited list of admission plugins: Initializers, MutatingAdmissionWebhook, NamespaceLifecycle, ValidatingAdmissionWebhook. The order of plugins in this flag does not matter.

--enable-garbage-collector
Enables the generic garbage collector. MUST be synced with the corresponding flag of the kube-controller-manager. (default true)

--enable-swagger-ui
Enables swagger ui on the apiserver at /swagger-ui

--etcd-cafile string
SSL Certificate Authority file used to secure etcd communication.

--etcd-certfile string
SSL certification file used to secure etcd communication.

--etcd-compaction-interval duration
The interval of compaction requests. If 0, the compaction request from apiserver is disabled. (default 5m0s)

--etcd-count-metric-poll-period duration
Frequency of polling etcd for number of resources per type. 0 disables the metric collection. (default 1m0s)

--etcd-keyfile string
SSL key file used to secure etcd communication.

--etcd-prefix string
The prefix to prepend to all resource paths in etcd. (default "/registry/apiextensions.kubernetes.io")

--etcd-servers strings
List of etcd servers to connect with (scheme://ip:port), comma separated.

--etcd-servers-overrides strings
Per-resource etcd servers overrides, comma separated. The individual override format: group/resource#servers, where servers are http://ip:port, semicolon separated.

--experimental-encryption-provider-config string
The file containing configuration for encryption providers to be used for storing secrets in etcd

-h, --help
help for this command

--http2-max-streams-per-connection int
The limit that the server gives to clients for the maximum number of streams in an HTTP/2 connection. Zero means to use golang's default. (default 1000)

--log-flush-frequency duration
Maximum number of seconds between log flushes (default 5s)

--log_backtrace_at traceLocation
when logging hits line file:N, emit a stack trace (default :0)

--log_dir string
If non-empty, write log files in this directory

--logtostderr
log to standard error instead of files (default true)

--profiling
Enable profiling via web interface host:port/debug/pprof/ (default true)

--requestheader-allowed-names strings
List of client certificate common names to allow to provide usernames in headers specified by --requestheader-username-headers. If empty, any client certificate validated by the authorities in --requestheader-client-ca-file is allowed.

--requestheader-client-ca-file string
Root certificate bundle to use to verify client certificates on incoming requests before trusting usernames in headers specified by --requestheader-username-headers

--requestheader-extra-headers-prefix strings
List of request header prefixes to inspect. X-Remote-Extra- is suggested. (default [x-remote-extra-])

--requestheader-group-headers strings
List of request headers to inspect for groups. X-Remote-Group is suggested. (default [x-remote-group])

--requestheader-username-headers strings
List of request headers to inspect for usernames. X-Remote-User is common. (default [x-remote-user])

--runtime-config mapStringString
A set of key=value pairs that describe runtime configuration that may be passed to apiserver. <group>/<version> (or <version> for the core group) key can be used to turn on/off specific api versions. api/all is special key to control all api versions, be careful setting it false, unless you know what you do. api/legacy is deprecated, we will remove it in the future, so stop using it.

--secure-port int
The port on which to serve HTTPS with authentication and authorization. If 0, don't serve HTTPS at all. (default 443)

--stderrthreshold severity
logs at or above this threshold go to stderr (default 2)

--storage-backend string
The storage backend for persistence. Options: 'etcd3' (default), 'etcd2'.

--storage-media-type string
The media type to use to store objects in storage. Some resources or storage backends may only support a specific media type and will ignore this setting. (default "application/json")

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

-v, --v Level
log level for V logs

--vmodule moduleSpec
comma-separated list of pattern=N settings for file-filtered logging

--watch-cache
Enable watch caching in the apiserver (default true)

--watch-cache-sizes strings
List of watch cache sizes for every resource (pods, nodes, etc.), comma separated. The individual override format: resource[.group]#size, where resource is lowercase plural (no version), group is optional, and size is a number. It takes effect when watch-cache is enabled. Some resources (replicationcontrollers, endpoints, nodes, pods, services, apiservices.apiregistration.k8s.io) have system defaults set by heuristics, others default to default-watch-cache-size

$ 

```

### cloud-controller-manager
```
$ ./cloud-controller-manager -h
The Cloud controller manager is a daemon that embeds
the cloud specific control loops shipped with Kubernetes.

Usage:
  cloud-controller-manager [flags]

Flags:

--address ip
DEPRECATED: the IP address on which to listen for the --port port. See --bind-address instead. (default 0.0.0.0)

--allocate-node-cidrs
Should CIDRs for Pods be allocated and set on the cloud provider.

--alsologtostderr
log to standard error as well as files

--bind-address ip
The IP address on which to listen for the --secure-port port. The associated interface(s) must be reachable by the rest of the cluster, and by CLI/web clients. If blank, all interfaces will be used (0.0.0.0 for all IPv4 interfaces and :: for all IPv6 interfaces). (default 0.0.0.0)

--cert-dir string
The directory where the TLS certs are located. If --tls-cert-file and --tls-private-key-file are provided, this flag will be ignored. (default "/var/run/kubernetes")

--cidr-allocator-type string
Type of CIDR allocator to use (default "RangeAllocator")

--cloud-config string
The path to the cloud provider configuration file. Empty string for no configuration file.

--cloud-provider string
The provider of cloud services. Cannot be empty.

--cloud-provider-gce-lb-src-cidrs cidrs
CIDRs opened in GCE firewall for LB traffic proxy & health checks (default 130.211.0.0/22,209.85.152.0/22,209.85.204.0/22,35.191.0.0/16)

--cluster-cidr string
CIDR Range for Pods in cluster. Requires --allocate-node-cidrs to be true

--cluster-name string
The instance prefix for the cluster. (default "kubernetes")

--concurrent-service-syncs int32
The number of services that are allowed to sync concurrently. Larger number = more responsive service management, but more CPU (and network) load (default 1)

--configure-cloud-routes
hould CIDRs allocated by allocate-node-cidrs be configured on the cloud provider. (default true)

--contention-profiling
Enable lock contention profiling, if profiling is enabled.

--controller-start-interval duration
Interval between starting controller managers.

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
ExperimentalHostUserNamespaceDefaulting=true|false (BETA - efault=false)
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

-h, --help
help for cloud-controller-manager

--http2-max-streams-per-connection int
The limit that the server gives to clients for the maximum number of streams in an HTTP/2 connection. Zero means to use golang's default.

--kube-api-burst int32
Burst to use while talking with kubernetes apiserver. (default 30)

--kube-api-content-type string
Content type of requests sent to apiserver. (default "application/vnd.kubernetes.protobuf")

--kube-api-qps float32
QPS to use while talking with kubernetes apiserver. (default 20)

--kubeconfig string
Path to kubeconfig file with authorization and master location information.

--leader-elect
Start a leader election client and gain leadership before executing the main loop. Enable this when running replicated components for high availability. (default true)

--leader-elect-lease-duration duration
The duration that non-leader candidates will wait after observing a leadership renewal until attempting to acquire leadership of a led but unrenewed leader slot. This is effectively the maximum duration that a leader can be stopped before it is replaced by another candidate. This is only applicable if leader election is enabled. (default 15s)

--leader-elect-renew-deadline duration
The interval between attempts by the acting master to renew a leadership slot before it stops leading. This must be less than or equal to the lease duration. This is only applicable if leader election is enabled. (default 10s)

--leader-elect-resource-lock endpoints
The type of resource object that is used for locking during leader election. Supported options are endpoints (default) and `configmaps`. (default "endpoints")

--leader-elect-retry-period duration
The duration the clients should wait between attempting acquisition and renewal of a leadership. This is only applicable if leader election is enabled. (default 2s)

--log-backtrace-at traceLocation
when logging hits line file:N, emit a stack trace (default :0)

--log-dir string
If non-empty, write log files in this directory

--log-flush-frequency duration
Maximum number of seconds between log flushes (default 5s)

--loglevel int
Log level (0 = DEBUG, 5 = FATAL) (default 1)

--logtostderr
log to standard error instead of files (default true)

--master string
The address of the Kubernetes API server (overrides any value in kubeconfig).

--min-resync-period duration
The resync period in reflectors will be random between MinResyncPeriod and 2*MinResyncPeriod. (default 12h0m0s)

--node-monitor-period duration
The period for syncing NodeStatus in NodeController. (default 5s)

--node-status-update-frequency duration
Specifies how often the controller updates nodes' status. (default 5m0s)

--port int
DEPRECATED: the port on which to serve HTTP insecurely without authentication and authorization. If 0, don't serve HTTPS at all. See --secure-port instead. (default 10253)

--profiling
Enable profiling via web interface host:port/debug/pprof/ (default true)

--route-reconciliation-period duration
The period for reconciling routes created for Nodes by cloud provider. (default 10s)

--secure-port int
The port on which to serve HTTPS with authentication and authorization. If 0, don't serve HTTPS at all.

--stderrthreshold severity
logs at or above this threshold go to stderr (default 2)

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

--use-service-account-credentials
If true, use individual service account credentials for each controller.

-v, --v Level
log level for V logs

--version version[=true]
Print version information and quit

--vmodule moduleSpec
comma-separated list of pattern=N settings for file-filtered logging

$ 

```


### hyperkube

```
$ ./hyperkube -h
Request a new project

Usage:
  hyperkube [flags]
  hyperkube [command]

Available Commands:
  cloud-controller-manager 
  help    Help about any command
  kube-apiserver           
  kube-controller-manager  
  kube-proxy               
  kube-scheduler           
  kubectl    kubectl controls the Kubernetes cluster manager
  kubelet                  

Flags:

--allow-verification-with-non-compliant-keys
Allow a SignatureVerifier to use keys which are technically non-compliant with RFC6962.

--alsologtostderr
log to standard error as well as files

--application-metrics-count-limit int
Max number of application metrics to store (per container) (default 100)

--azure-container-registry-config string
Path to the file containing Azure container registry configuration information.

--boot-id-file string
Comma-separated list of files to check for boot-id. Use the first one that exists. (default "/proc/sys/kernel/random/boot_id")

--cloud-provider-gce-lb-src-cidrs cidrs
CIDRs opened in GCE firewall for LB traffic proxy & health checks (default 130.211.0.0/22,209.85.152.0/22,209.85.204.0/22,35.191.0.0/16)

--container-hints string
location of the container hints file (default "/etc/cadvisor/container_hints.json")

--containerd string
containerd endpoint (default "unix:///var/run/containerd.sock")

--default-not-ready-toleration-seconds int
Indicates the tolerationSeconds of the toleration for notReady:NoExecute that is added by default to every pod that does not already have such a toleration. (default 300)

--default-unreachable-toleration-seconds int
Indicates the tolerationSeconds of the toleration for unreachable:NoExecute that is added by default to every pod that does not already have such a toleration. (default 300)

--docker string
docker endpoint (default "unix:///var/run/docker.sock")

--docker-env-metadata-whitelist string
a comma-separated list of environment variable keys that needs to be collected for docker containers

--docker-only
Only report docker containers in addition to root stats

--docker-root string
DEPRECATED: docker root is read from docker info (this is a fallback, default: /var/lib/docker) (default "/var/lib/docker")

--docker-tls
use TLS to connect to docker

--docker-tls-ca string
path to trusted CA (default "ca.pem")

--docker-tls-cert string
path to client certificate (default "cert.pem")

--docker-tls-key string
path to private key (default "key.pem")

--enable-load-reader
Whether to enable cpu load reader

--event-storage-age-limit string
Max length of time for which to store events (per type). Value is a comma separated list of key values, where the keys are event types (e.g.: creation, oom) or "default" and the value is a duration. Default is applied to all non-specified event types (default "default=0")

--event-storage-event-limit string
Max number of events to store (per type). Value is a comma separated list of key values, where the keys are event types (e.g.: creation, oom) or "default" and the value is an integer. Default is applied to all non-specified event types (default "default=0")

--global-housekeeping-interval duration
Interval between global housekeepings (default 1m0s)

-h, --help
help for hyperkube

--housekeeping-interval duration
Interval between container housekeepings (default 10s)

--ir-data-source string
Data source used by InitialResources. Supported options: influxdb, gcm. (default "influxdb")

--ir-dbname string
InfluxDB database name which contains metrics required by InitialResources (default "k8s")

--ir-hawkular string
Hawkular configuration URL

--ir-influxdb-host string
Address of InfluxDB which contains metrics required by InitialResources (default "localhost:8080/api/v1/namespaces/kube-system/services/monitoring-influxdb:api/proxy")

--ir-namespace-only
Whether the estimation should be made only based on data from the same namespace.

--ir-password string
Password used for connecting to InfluxDB (default "root")

--ir-percentile int
Which percentile of samples should InitialResources use when estimating resources. For experiment purposes. (default 90)

--ir-user string
User used for connecting to InfluxDB (default "root")

--log-backtrace-at traceLocation
when logging hits line file:N, emit a stack trace (default :0)

--log-cadvisor-usage
Whether to log the usage of the cAdvisor container

--log-dir string
If non-empty, write log files in this directory

--log-flush-frequency duration
Maximum number of seconds between log flushes (default 5s)

--loglevel int
Log level (0 = DEBUG, 5 = FATAL) (default 1)

--logtostderr
log to standard error instead of files (default true)

--machine-id-file string
Comma-separated list of files to check for machine-id. Use the first one that exists. (default "/etc/machine-id,/var/lib/dbus/machine-id")

--stderrthreshold severity
logs at or above this threshold go to stderr (default 2)

--storage-driver-buffer-duration duration
Writes in the storage driver will be buffered for this duration, and committed to the non memory backends as a single transaction (default 1m0s)

--storage-driver-db string
database name (default "cadvisor")

--storage-driver-host string
database host:port (default "localhost:8086")

--storage-driver-password string
database password (default "root")

--storage-driver-secure
use secure connection with database

--storage-driver-table string
table name (default "stats")

--storage-driver-user string
database username (default "root")

-v, --v Level
log level for V logs

--version version[=true]
Print version information and quit

--vmodule moduleSpec
comma-separated list of pattern=N settings for file-filtered logging

Use "hyperkube [command] --help" for more information about a command.

$ 

```

### kubeadm

```
$ ./kubeadm -h

kubeadm: easily bootstrap a secure Kubernetes cluster.

    ┌──────────────────────────────────────────────────────────┐
    │ KUBEADM IS CURRENTLY IN BETA                             │
    │                                                          │
    │ But please, try it out and give us feedback at:          │
    │ https://github.com/kubernetes/kubeadm/issues             │
    │ and at-mention @kubernetes/sig-cluster-lifecycle-bugs    │
    │ or @kubernetes/sig-cluster-lifecycle-feature-requests    │
    └──────────────────────────────────────────────────────────┘

Example usage:

    Create a two-machine cluster with one master (which controls the cluster), and one node (where your workloads, like Pods and Deployments run).

    ┌──────────────────────────────────────────────────────────┐
    │ On the first machine:                                    │
    ├──────────────────────────────────────────────────────────┤
    │ master# kubeadm init                                     │
    └──────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────┐
    │ On the second machine:                                   │
    ├──────────────────────────────────────────────────────────┤
    │ node# kubeadm join <arguments-returned-from-init>        │
    └──────────────────────────────────────────────────────────┘

    You can then repeat the second step on as many other machines as you like.

Usage:
  kubeadm [command]

Available Commands:
  alpha       Experimental sub-commands not yet fully functional.
  completion  Output shell completion code for the specified shell (bash or zsh).
  config      Manage configuration for a kubeadm cluster persisted in a ConfigMap in the cluster.
  help        Help about any command
  init        Run this command in order to set up the Kubernetes master.
  join        Run this on any machine you wish to join an existing cluster
  reset       Run this to revert any changes made to this host by 'kubeadm init' or 'kubeadm join'.
  token       Manage bootstrap tokens.
  upgrade     Upgrade your cluster smoothly to a newer version with this command.
  version     Print the version of kubeadm

Flags:
  -h, --help   help for kubeadm

Use "kubeadm [command] --help" for more information about a command.

$ 
```

### kube-aggregator

```
$ ./kube-aggregator -h
Launch a API aggregator and proxy server

Usage:
   [flags]

Flags:

--admission-control-config-file string
File with admission control configuration.

--alsologtostderr
log to standard error as well as files

--audit-log-batch-buffer-size int
The size of the buffer to store events before batching and writing. Only used in batch mode. (default 10000)

--audit-log-batch-max-size int
The maximum size of a batch. Only used in batch mode. (default 400)

--audit-log-batch-max-wait duration
The amount of time to wait before force writing the batch that hadn't reached the max size. Only used in batch mode. (default 30s)

--audit-log-batch-throttle-burst int
Maximum number of requests sent at the same moment if ThrottleQPS was not utilized before. Only used in batch mode. (default 15)

--audit-log-batch-throttle-enable
Whether batching throttling is enabled. Only used in batch mode.

--audit-log-batch-throttle-qps float32
Maximum average number of batches per second. Only used in batch mode. (default 10)

--audit-log-format string
Format of saved audits. "legacy" indicates 1-line text format for each event. "json" indicates structured json format. Requires the 'AdvancedAuditing' feature gate. Known formats are legacy,json. (default "json")

--audit-log-maxage int
The maximum number of days to retain old audit log files based on the timestamp encoded in their filename.

--audit-log-maxbackup int
The maximum number of old audit log files to retain.

--audit-log-maxsize int
The maximum size in megabytes of the audit log file before it gets rotated.

--audit-log-mode string
Strategy for sending audit events. Blocking indicates sending events should block server responses. Batch causes the backend to buffer and write events asynchronously. Known modes are batch,blocking. (default "blocking")

--audit-log-path string
If set, all requests coming to the apiserver will be logged to this file.  '-' means standard out.

--audit-log-truncate-enabled
Whether event and batch truncating is enabled.

--audit-log-truncate-max-batch-size int
Maximum size of the batch sent to the underlying backend. Actual serialized size can be several hundreds of bytes greater. If a batch exceeds this limit, it is split into several batches of smaller size. (default 10485760)

--audit-log-truncate-max-event-size int
Maximum size of the audit event sent to the underlying backend. If the size of an event is greater than this number, first request and response are removed, andif this doesn't reduce the size enough, event is discarded. (default 102400)

--audit-policy-file string
Path to the file that defines the audit policy configuration. Requires the 'AdvancedAuditing' feature gate. With AdvancedAuditing, a profile is required to enable auditing.

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

--authentication-kubeconfig string
kubeconfig file pointing at the 'core' kubernetes server with enough rights to create tokenaccessreviews.authentication.k8s.io.

--authentication-skip-lookup
If false, the authentication-kubeconfig will be used to lookup missing authentication configuration from the cluster.

--authentication-token-webhook-cache-ttl duration
The duration to cache responses from the webhook token authenticator. (default 10s)

--authorization-kubeconfig string
kubeconfig file pointing at the 'core' kubernetes server with enough rights to create  subjectaccessreviews.authorization.k8s.io.

--authorization-webhook-cache-authorized-ttl duration
The duration to cache 'authorized' responses from the webhook authorizer. (default 10s)

--authorization-webhook-cache-unauthorized-ttl duration
The duration to cache 'unauthorized' responses from the webhook authorizer. (default 10s)

--bind-address ip
The IP address on which to listen for the --secure-port port. The associated interface(s) must be reachable by the rest of the cluster, and by CLI/web clients. If blank, all interfaces will be used (0.0.0.0 for all IPv4 interfaces and :: for all IPv6 interfaces). (default 0.0.0.0)

--cert-dir string
The directory where the TLS certs are located. If --tls-cert-file and --tls-private-key-file are provided, this flag will be ignored. (default "apiserver.local.config/certificates")

--client-ca-file string
If set, any request presenting a client certificate signed by one of the authorities in the client-ca-file is authenticated with an identity corresponding to the CommonName of the client certificate.

--contention-profiling
Enable lock contention profiling, if profiling is enabled

--default-watch-cache-size int
Default watch cache size. If zero, watch cache will be disabled for resources that do not have a default watch size set. (default 100)

--delete-collection-workers int
Number of workers spawned for DeleteCollection call. These are used to speed up namespace cleanup. (default 1)

--deserialization-cache-size int
Number of deserialized json objects to cache in memory.

--disable-admission-plugins strings
admission plugins that should be disabled although they are in the default enabled plugins list. Comma-delimited list of admission plugins: Initializers, MutatingAdmissionWebhook, NamespaceLifecycle, ValidatingAdmissionWebhook. The order of plugins in this flag does not matter.

--enable-admission-plugins strings
admission plugins that should be enabled in addition to default enabled ones. Comma-delimited list of admission plugins: Initializers, MutatingAdmissionWebhook, NamespaceLifecycle, ValidatingAdmissionWebhook. The order of plugins in this flag does not matter.

--enable-garbage-collector
Enables the generic garbage collector. MUST be synced with the corresponding flag of the kube-controller-manager. (default true)

--enable-swagger-ui
Enables swagger ui on the apiserver at /swagger-ui

--etcd-cafile string
SSL Certificate Authority file used to secure etcd communication.

--etcd-certfile string
SSL certification file used to secure etcd communication.

--etcd-compaction-interval duration
The interval of compaction requests. If 0, the compaction request from apiserver is disabled. (default 5m0s)

--etcd-count-metric-poll-period duration
Frequency of polling etcd for number of resources per type. 0 disables the metric collection. (default 1m0s)

--etcd-keyfile string
SSL key file used to secure etcd communication.

--etcd-prefix string
The prefix to prepend to all resource paths in etcd. (default "/registry/kube-aggregator.kubernetes.io/")

--etcd-servers strings
List of etcd servers to connect with (scheme://ip:port), comma separated.

--etcd-servers-overrides strings
Per-resource etcd servers overrides, comma separated. The individual override format: group/resource#servers, where servers are http://ip:port, semicolon separated.

--experimental-encryption-provider-config string
The file containing configuration for encryption providers to be used for storing secrets in etcd

-h, --help
help for this command

--http2-max-streams-per-connection int
The limit that the server gives to clients for the maximum number of streams in an HTTP/2 connection. Zero means to use golang's default. (default 1000)

--kubeconfig string
kubeconfig file pointing at the 'core' kubernetes server.

--log-flush-frequency duration
Maximum number of seconds between log flushes (default 5s)

--log_backtrace_at traceLocation
when logging hits line file:N, emit a stack trace (default :0)

--log_dir string
If non-empty, write log files in this directory

--logtostderr
log to standard error instead of files (default true)

--profiling
Enable profiling via web interface host:port/debug/pprof/ (default true)

--proxy-client-cert-file string
client certificate used identify the proxy to the API server

--proxy-client-key-file string
client certificate key used identify the proxy to the API server

--requestheader-allowed-names strings
List of client certificate common names to allow to provide usernames in headers specified by --requestheader-username-headers. If empty, any client certificate validated by the authorities in --requestheader-client-ca-file is allowed.

--requestheader-client-ca-file string
Root certificate bundle to use to verify client certificates on incoming requests before trusting usernames in headers specified by --requestheader-username-headers

--requestheader-extra-headers-prefix strings
List of request header prefixes to inspect. X-Remote-Extra- is suggested. (default [x-remote-extra-])

--requestheader-group-headers strings
List of request headers to inspect for groups. X-Remote-Group is suggested. (default [x-remote-group])

--requestheader-username-headers strings
List of request headers to inspect for usernames. X-Remote-User is common. (default [x-remote-user])

--runtime-config mapStringString
A set of key=value pairs that describe runtime configuration that may be passed to apiserver. <group>/<version> (or <version> for the core group) key can be used to turn on/off specific api versions. api/all is special key to control all api versions, be careful setting it false, unless you know what you do. api/legacy is deprecated, we will remove it in the future, so stop using it.

--secure-port int
The port on which to serve HTTPS with authentication and authorization. If 0, don't serve HTTPS at all. (default 443)

--stderrthreshold severity
logs at or above this threshold go to stderr (default 2)

--storage-backend string
The storage backend for persistence. Options: 'etcd3' (default), 'etcd2'.

--storage-media-type string
The media type to use to store objects in storage. Some resources or storage backends may only support a specific media type and will ignore this setting. (default "application/json")

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

-v, --v Level
log level for V logs

--vmodule moduleSpec
comma-separated list of pattern=N settings for file-filtered logging

--watch-cache
Enable watch caching in the apiserver (default true)

--watch-cache-sizes strings
List of watch cache sizes for every resource (pods, nodes, etc.), comma separated. The individual override format: resource[.group]#size, where resource is lowercase plural (no version), group is optional, and size is a number. It takes effect when watch-cache is enabled. Some resources (replicationcontrollers, endpoints, nodes, pods, services, apiservices.apiregistration.k8s.io) have system defaults set by heuristics, others default to default-watch-cache-size

$ 

```





### kube-proxy
### kube-scheduler
### mounter
