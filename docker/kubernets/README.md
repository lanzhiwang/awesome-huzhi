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

apiextensions-apiserver
cloud-controller-manager
hyperkube
kubeadm
kube-aggregator
kube-apiserver
kube-controller-manager
kubectl
kubelet
kube-proxy
kube-scheduler
mounter


```

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

### kube-apiserver

```
$ ./kube-apiserver -h
The Kubernetes API server validates and configures data for the api objects which include pods, services, replicationcontrollers, and
others. The API Server services REST operations and provides the frontend to the cluster's shared state through which all other components interact.

Usage:
  kube-apiserver [flags]

Flags:

--admission-control strings
Admission is divided into two phases. In the first phase, only mutating admission plugins run. In the second phase, only validating admission plugins run. The names in the below list may represent a validating plugin, a mutating plugin, or both. The order of plugins in which they are passed to this flag does not matter. Comma-delimited list of: AlwaysAdmit, AlwaysDeny, AlwaysPullImages, DefaultStorageClass, DefaultTolerationSeconds, DenyEscalatingExec, DenyExecOnPrivileged, EventRateLimit, ExtendedResourceToleration, ImagePolicyWebhook, InitialResources, Initializers, LimitPodHardAntiAffinityTopology, LimitRanger, MutatingAdmissionWebhook, NamespaceAutoProvision, NamespaceExists, NamespaceLifecycle, NodeRestriction, OwnerReferencesPermissionEnforcement, PersistentVolumeClaimResize, PersistentVolumeLabel, PodNodeSelector, PodPreset, PodSecurityPolicy, PodTolerationRestriction, Priority, ResourceQuota, SecurityContextDeny, ServiceAccount, StorageObjectInUseProtection, ValidatingAdmissionWebhook. (DEPRECATED: Use --enable-admission-plugins or --disable-admission-plugins instead. Will be removed in a future version.)

--admission-control-config-file string
File with admission control configuration.

--advertise-address ip
The IP address on which to advertise the apiserver to members of the cluster. This address must be reachable by the rest of the cluster. If blank, the --bind-address will be used. If --bind-address is unspecified, the host's default interface will be used.

--allow-privileged
If true, allow privileged containers. [default=false]

--alsologtostderr
log to standard error as well as files

--anonymous-auth
Enables anonymous requests to the secure port of the API server. Requests that are not rejected by another authentication method are treated as anonymous requests. Anonymous requests have a username of system:anonymous, and a group name of system:unauthenticated. (default true)

--apiserver-count int
The number of apiservers running in the cluster, must be a positive number. (default 1)

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

--authentication-token-webhook-cache-ttl duration
The duration to cache responses from the webhook token authenticator. (default 2m0s)

--authentication-token-webhook-config-file string
File with webhook configuration for token authentication in kubeconfig format. The API server will query the remote service to determine authentication for bearer tokens.

--authorization-mode string
Ordered list of plug-ins to do authorization on secure port. Comma-delimited list of: AlwaysAllow,AlwaysDeny,ABAC,Webhook,RBAC,Node. (default "AlwaysAllow")

--authorization-policy-file string
File with authorization policy in csv format, used with --authorization-mode=ABAC, on the secure port.

--authorization-webhook-cache-authorized-ttl duration
The duration to cache 'authorized' responses from the webhook authorizer. (default 5m0s)

--authorization-webhook-cache-unauthorized-ttl duration
The duration to cache 'unauthorized' responses from the webhook authorizer. (default 30s)

--authorization-webhook-config-file string
File with webhook configuration in kubeconfig format, used with --authorization-mode=Webhook. The API server will query the remote service to determine access on the API server's secure port.

--basic-auth-file string
If set, the file that will be used to admit requests to the secure port of the API server via http basic authentication.

--bind-address ip
The IP address on which to listen for the --secure-port port. The associated interface(s) must be reachable by the rest of the cluster, and by CLI/web clients. If blank, all interfaces will be used (0.0.0.0 for all IPv4 interfaces and :: for all IPv6 interfaces). (default 0.0.0.0)

--cert-dir string
The directory where the TLS certs are located. If --tls-cert-file and --tls-private-key-file are provided, this flag will be ignored. (default "/var/run/kubernetes")

--client-ca-file string
If set, any request presenting a client certificate signed by one of the authorities in the client-ca-file is authenticated with an identity corresponding to the CommonName of the client certificate.

--cloud-config string
The path to the cloud provider configuration file. Empty string for no configuration file.

--cloud-provider string
The provider for cloud services. Empty string for no provider.

--cloud-provider-gce-lb-src-cidrs cidrs
CIDRs opened in GCE firewall for LB traffic proxy & health checks (default 130.211.0.0/22,209.85.152.0/22,209.85.204.0/22,35.191.0.0/16)

--contention-profiling
Enable lock contention profiling, if profiling is enabled

--cors-allowed-origins strings
List of allowed origins for CORS, comma separated.  An allowed origin can be a regular expression to support subdomain matching. If this list is empty CORS will not be enabled.

--default-not-ready-toleration-seconds int
Indicates the tolerationSeconds of the toleration for notReady:NoExecute that is added by default to every pod that does not already have such a toleration. (default 300)

--default-unreachable-toleration-seconds int
Indicates the tolerationSeconds of the toleration for unreachable:NoExecute that is added by default to every pod that does not already have such a toleration. (default 300)

--default-watch-cache-size int
Default watch cache size. If zero, watch cache will be disabled for resources that do not have a default watch size set. (default 100)

--delete-collection-workers int
Number of workers spawned for DeleteCollection call. These are used to speed up namespace cleanup. (default 1)

--deserialization-cache-size int
Number of deserialized json objects to cache in memory.

--disable-admission-plugins strings
admission plugins that should be disabled although they are in the default enabled plugins list. Comma-delimited list of admission plugins: AlwaysAdmit, AlwaysDeny, AlwaysPullImages, DefaultStorageClass, DefaultTolerationSeconds, DenyEscalatingExec, DenyExecOnPrivileged, EventRateLimit, ExtendedResourceToleration, ImagePolicyWebhook, InitialResources, Initializers, LimitPodHardAntiAffinityTopology, LimitRanger, MutatingAdmissionWebhook, NamespaceAutoProvision, NamespaceExists, NamespaceLifecycle, NodeRestriction, OwnerReferencesPermissionEnforcement, PersistentVolumeClaimResize, PersistentVolumeLabel, PodNodeSelector, PodPreset, PodSecurityPolicy, PodTolerationRestriction, Priority, ResourceQuota, SecurityContextDeny, ServiceAccount, StorageObjectInUseProtection, ValidatingAdmissionWebhook. The order of plugins in this flag does not matter.

--enable-admission-plugins strings
admission plugins that should be enabled in addition to default enabled ones. Comma-delimited list of admission plugins: AlwaysAdmit, AlwaysDeny, AlwaysPullImages, DefaultStorageClass, DefaultTolerationSeconds, DenyEscalatingExec, DenyExecOnPrivileged, EventRateLimit, ExtendedResourceToleration, ImagePolicyWebhook, InitialResources, Initializers, LimitPodHardAntiAffinityTopology, LimitRanger, MutatingAdmissionWebhook, NamespaceAutoProvision, NamespaceExists, NamespaceLifecycle, NodeRestriction, OwnerReferencesPermissionEnforcement, PersistentVolumeClaimResize, PersistentVolumeLabel, PodNodeSelector, PodPreset, PodSecurityPolicy, PodTolerationRestriction, Priority, ResourceQuota, SecurityContextDeny, ServiceAccount, StorageObjectInUseProtection, ValidatingAdmissionWebhook. The order of plugins in this flag does not matter.

--enable-aggregator-routing
Turns on aggregator routing requests to endoints IP rather than cluster IP.

--enable-bootstrap-token-auth
Enable to allow secrets of type 'bootstrap.kubernetes.io/token' in the 'kube-system' namespace to be used for TLS bootstrapping authentication.

--enable-garbage-collector
Enables the generic garbage collector. MUST be synced with the corresponding flag of the kube-controller-manager. (default true)

--enable-logs-handler
If true, install a /logs handler for the apiserver logs. (default true)

--enable-swagger-ui
Enables swagger ui on the apiserver at /swagger-ui

--endpoint-reconciler-type string
Use an endpoint reconciler (master-count, lease, none) (default "master-count")

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
The prefix to prepend to all resource paths in etcd. (default "/registry")

--etcd-servers strings
List of etcd servers to connect with (scheme://ip:port), comma separated.

--etcd-servers-overrides strings
Per-resource etcd servers overrides, comma separated. The individual override format: group/resource#servers, where servers are http://ip:port, semicolon separated.

--event-ttl duration
Amount of time to retain events. (default 1h0m0s)

--experimental-encryption-provider-config string
The file containing configuration for encryption providers to be used for storing secrets in etcd

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

-h, --help
help for kube-apiserver

--http2-max-streams-per-connection int
The limit that the server gives to clients for the maximum number of streams in an HTTP/2 connection. Zero means to use golang's default.

--insecure-bind-address ip
The IP address on which to serve the --insecure-port (set to 0.0.0.0 for all IPv4 interfaces and :: for all IPv6 interfaces). (default 127.0.0.1) (DEPRECATED: This flag will be removed in a future version.)

--insecure-port int
The port on which to serve unsecured, unauthenticated access. It is assumed that firewall rules are set up such that this port is not reachable from outside of the cluster and that port 443 on the cluster's public address is proxied to this port. This is performed by nginx in the default setup. Set to zero to disable. (default 8080) (DEPRECATED: This flag will be removed in a future version.)

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

--kubelet-certificate-authority string
Path to a cert file for the certificate authority.

--kubelet-client-certificate string
Path to a client cert file for TLS.

--kubelet-client-key string
Path to a client key file for TLS.

--kubelet-https
Use https for kubelet connections. (default true)

--kubelet-preferred-address-types strings
List of the preferred NodeAddressTypes to use for kubelet connections. (default [Hostname,InternalDNS,InternalIP,ExternalDNS,ExternalIP])

--kubelet-read-only-port uint
DEPRECATED: kubelet port. (default 10255)

--kubelet-timeout duration
Timeout for kubelet operations. (default 5s)

--kubernetes-service-node-port int
If non-zero, the Kubernetes master service (which apiserver creates/maintains) will be of type NodePort, using this as the value of the port. If zero, the Kubernetes master service will be of type ClusterIP.

--log-backtrace-at traceLocation
when logging hits line file:N, emit a stack trace (default :0)

--log-dir string
If non-empty, write log files in this directory

--log-flush-frequency duration
Maximum number of seconds between log flushes (default 5s)

--logtostderr
log to standard error instead of files (default true)

--master-service-namespace string
DEPRECATED: the namespace from which the kubernetes master services should be injected into pods. (default "default")

--max-connection-bytes-per-sec int
If non-zero, throttle each user connection to this number of bytes/sec. Currently only applies to long-running requests.

--max-mutating-requests-inflight int
The maximum number of mutating requests in flight at a given time. When the server exceeds this, it rejects requests. Zero for no limit. (default 200)

--max-requests-inflight int
The maximum number of non-mutating requests in flight at a given time. When the server exceeds this, it rejects requests. Zero for no limit. (default 400)

--min-request-timeout int
An optional field indicating the minimum number of seconds a handler must keep a request open before timing it out. Currently only honored by the watch request handler, which picks a randomized value above this number as the connection timeout, to spread out load. (default 1800)

--oidc-ca-file string
If set, the OpenID server's certificate will be verified by one of the authorities in the oidc-ca-file, otherwise the host's root CA set will be used.

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
Enable profiling via web interface host:port/debug/pprof/ (default true)

--proxy-client-cert-file string
Client certificate used to prove the identity of the aggregator or kube-apiserver when it must call out during a request. This includes proxying requests to a user api-server and calling out to webhook admission plugins. It is expected that this cert includes a signature from the CA in the --requestheader-client-ca-file flag. That CA is published in the 'extension-apiserver-authentication' configmap in the kube-system namespace. Components receiving calls from kube-aggregator should use that CA to perform their half of the mutual TLS verification.

--proxy-client-key-file string
Private key for the client certificate used to prove the identity of the aggregator or kube-apiserver when it must call out during a request. This includes proxying requests to a user api-server and calling out to webhook admission plugins.

--repair-malformed-updates
If true, server will do its best to fix the update request to pass the validation, e.g., setting empty UID in update request to its existing value. This flag can be turned off after we fix all the clients that send malformed updates. (default true)

--request-timeout duration
An optional field indicating the duration a handler must keep a request open before timing it out. This is the default request timeout for requests but may be overridden by flags such as --min-request-timeout for specific types of requests. (default 1m0s)

--requestheader-allowed-names strings
List of client certificate common names to allow to provide usernames in headers specified by --requestheader-username-headers. If empty, any client certificate validated by the authorities in --requestheader-client-ca-file is allowed.

--requestheader-client-ca-file string
Root certificate bundle to use to verify client certificates on incoming requests before trusting usernames in headers specified by --requestheader-username-headers

--requestheader-extra-headers-prefix strings
List of request header prefixes to inspect. X-Remote-Extra- is suggested.

--requestheader-group-headers strings
List of request headers to inspect for groups. X-Remote-Group is suggested.

--requestheader-username-headers strings
List of request headers to inspect for usernames. X-Remote-User is common.

--runtime-config mapStringString
A set of key=value pairs that describe runtime configuration that may be passed to apiserver. <group>/<version> (or <version> for the core group) key can be used to turn on/off specific api versions. api/all is special key to control all api versions, be careful setting it false, unless you know what you do. api/legacy is deprecated, we will remove it in the future, so stop using it.

--secure-port int
The port on which to serve HTTPS with authentication and authorization. If 0, don't serve HTTPS at all. (default 6443)

--service-account-api-audiences strings
Identifiers of the API. The service account token authenticator will validate that tokens used against the API are bound to at least one of these audiences.

--service-account-issuer string
Identifier of the service account token issuer. The issuer will assert this identifier in "iss" claim of issued tokens. This value is a string or URI.

--service-account-key-file stringArray
File containing PEM-encoded x509 RSA or ECDSA private or public keys, used to verify ServiceAccount tokens. The specified file can contain multiple keys, and the flag can be specified multiple times with different files. If unspecified, --tls-private-key-file is used. Must be specified when --service-account-signing-key is provided

--service-account-lookup
If true, validate ServiceAccount tokens exist in etcd as part of authentication. (default true)

--service-account-signing-key-file string
Path to the file that contains the current private key of the service account token issuer. The issuer will sign issued ID tokens with this private key. (Ignored unless alpha TokenRequest is enabled

--service-cluster-ip-range ipNet
A CIDR notation IP range from which to assign service cluster IPs. This must not overlap with any IP ranges assigned to nodes for pods. (default 10.0.0.0/24)

--service-node-port-range portRange
A port range to reserve for services with NodePort visibility. Example: '30000-32767'. Inclusive at both ends of the range. (default 30000-32767)

--stderrthreshold severity
logs at or above this threshold go to stderr (default 2)

--storage-backend string
The storage backend for persistence. Options: 'etcd3' (default), 'etcd2'.

--storage-media-type string
The media type to use to store objects in storage. Some resources or storage backends may only support a specific media type and will ignore this setting. (default "application/vnd.kubernetes.protobuf")

--storage-versions string
The per-group version to store resources in. Specified in the format "group1/version1,group2/version2,...". In the case where objects are moved from one group to the other, you may specify the format "group1=group2/v1beta1,group3/v1beta1,...". You only need to pass the groups you wish to change from the defaults. It defaults to a list of preferred versions of all registered groups, which is derived from the KUBE_API_VERSIONS environment variable. (default "admission.k8s.io/v1beta1,admissionregistration.k8s.io/v1beta1,apps/v1,authentication.k8s.io/v1,authorization.k8s.io/v1,autoscaling/v1,batch/v1,certificates.k8s.io/v1beta1,componentconfig/v1alpha1,events.k8s.io/v1beta1,extensions/v1beta1,imagepolicy.k8s.io/v1alpha1,networking.k8s.io/v1,policy/v1beta1,rbac.authorization.k8s.io/v1,scheduling.k8s.io/v1alpha1,settings.k8s.io/v1alpha1,storage.k8s.io/v1,v1")

--target-ram-mb int
Memory limit for apiserver in MB (used to configure sizes of caches, etc.)

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

### kube-controller-manager

```
$ ./kube-controller-manager -h
The Kubernetes controller manager is a daemon that embeds the core control loops shipped with Kubernetes. In applications of robotics and
automation, a control loop is a non-terminating loop that regulates the state of the system. In Kubernetes, a controller is a control loop that watches the shared state of the cluster through the apiserver and makes changes attempting to move the current state towards the desired state. Examples of controllers that ship with Kubernetes today are the replication controller, endpoints controller, namespace controller, and serviceaccounts controller.

Usage:
  kube-controller-manager [flags]

Flags:

--address ip                                                        
DEPRECATED: the IP address on which to listen for the --port port. See --bind-address instead. (default 0.0.0.0)

--allocate-node-cidrs                                               
Should CIDRs for Pods be allocated and set on the cloud provider.

--allow-verification-with-non-compliant-keys                        Allow a SignatureVerifier to use keys which are technically non-compliant with RFC6962.

--alsologtostderr
log to standard error as well as files

--attach-detach-reconcile-sync-period duration
The reconciler sync wait time between volume attach detach. This duration must be larger than one second, and increasing this value from the default may allow for volumes to be mismatched with pods. (default 1m0s)

--bind-address ip
The IP address on which to listen for the --secure-port port. The associated interface(s) must be reachable by the rest of the cluster, and by CLI/web clients. If blank, all interfaces will be used (0.0.0.0 for all IPv4 interfaces and :: for all IPv6 interfaces). (default 0.0.0.0)

--cert-dir string
The directory where the TLS certs are located. If --tls-cert-file and --tls-private-key-file are provided, this flag will be ignored. (default "/var/run/kubernetes")

--cidr-allocator-type string
Type of CIDR allocator to use (default "RangeAllocator")

--cloud-config string
The path to the cloud provider configuration file. Empty string for no configuration file.

--cloud-provider string
The provider for cloud services.  Empty string for no provider.

--cloud-provider-gce-lb-src-cidrs cidrs                             CIDRs opened in GCE firewall for LB traffic proxy & health checks (default 130.211.0.0/22,209.85.152.0/22,209.85.204.0/22,35.191.0.0/16)

--cluster-cidr string
CIDR Range for Pods in cluster. Requires --allocate-node-cidrs to be true

--cluster-name string
The instance prefix for the cluster. (default "kubernetes")

--cluster-signing-cert-file string                                  Filename containing a PEM-encoded X509 CA certificate used to issue cluster-scoped certificates (default "/etc/kubernetes/ca/ca.pem")

--cluster-signing-key-file string                                   Filename containing a PEM-encoded RSA or ECDSA private key used to sign cluster-scoped certificates (default "/etc/kubernetes/ca/ca.key")

--concurrent-deployment-syncs int32
The number of deployment objects that are allowed to sync concurrently. Larger number = more responsive deployments, but more CPU (and network) load (default 5)

--concurrent-endpoint-syncs int32
The number of endpoint syncing operations that will be done concurrently. Larger number = faster endpoint updating, but more CPU (and network) load (default 5)

--concurrent-gc-syncs int32
The number of garbage collector workers that are allowed to sync concurrently. (default 20)

--concurrent-namespace-syncs int32
The number of namespace objects that are allowed to sync concurrently. Larger number = more responsive namespace termination, but more CPU (and network) load (default 10)

--concurrent-replicaset-syncs int32
The number of replica sets that are allowed to sync concurrently. Larger number = more responsive replica management, but more CPU (and network) load (default 5)

--concurrent-resource-quota-syncs int32
The number of resource quotas that are allowed to sync concurrently. Larger number = more responsive quota management, but more CPU (and network) load (default 5)

--concurrent-service-syncs int32
The number of services that are allowed to sync concurrently. Larger number = more responsive service management, but more CPU (and network) load (default 1)

--concurrent-serviceaccount-token-syncs int32
The number of service account token objects that are allowed to sync concurrently. Larger number = more responsive token generation, but more CPU (and network) load (default 5)

--concurrent_rc_syncs int32
The number of replication controllers that are allowed to sync concurrently. Larger number = more responsive replica management, but more CPU (and network) load (default 5)

--configure-cloud-routes                                            Should CIDRs allocated by allocate-node-cidrs be configured on the cloud provider. (default true)

--contention-profiling                                              Enable lock contention profiling, if profiling is enabled.

--controller-start-interval duration                                Interval between starting controller managers.

--controllers strings                                               A list of controllers to enable.  '*' enables all on-by-default controllers, 'foo' enables the controller named 'foo', '-foo' disables the controller named 'foo'.

All controllers: attachdetach, bootstrapsigner, clusterrole-aggregation, cronjob, csrapproving, csrcleaner, csrsigning, daemonset, deployment, disruption, endpoint, garbagecollector, horizontalpodautoscaling, job, namespace, nodeipam, nodelifecycle, persistentvolume-binder, persistentvolume-expander, podgc, pv-protection, pvc-protection, replicaset, replicationcontroller, resourcequota, route, service, serviceaccount, serviceaccount-token, statefulset, tokencleaner, ttl Disabled-by-default controllers: bootstrapsigner, tokencleaner (default [*])

--deployment-controller-sync-period duration                        Period for syncing the deployments. (default 30s)

--disable-attach-detach-reconcile-sync                              Disable volume attach detach reconciler sync. Disabling this may cause volumes to be mismatched with pods. Use wisely.

--enable-dynamic-provisioning                                       Enable dynamic provisioning for environments that support it. (default true)

--enable-garbage-collector                                          Enables the generic garbage collector. MUST be synced with the corresponding flag of the kube-apiserver. (default true)

--enable-hostpath-provisioner                                       Enable HostPath PV provisioning when running without a cloud provider. This allows testing and development of provisioning features.  HostPath provisioning is not supported in any way, won't work in a multi-node cluster, and should not be used for anything other than testing or development.

--enable-taint-manager                                              WARNING: Beta feature. If set to true enables NoExecute Taints and will evict all not-tolerating Pod running on Nodes tainted with this kind of Taints. (default true)

--experimental-cluster-signing-duration duration
The length of duration signed certificates will be given. (default 8760h0m0s)

--external-cloud-volume-plugin string
The plugin to use when cloud provider is set to external. Can be empty, should only be set when cloud-provider is external. Currently used to allow node and volume controllers to work for in tree cloud providers.

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

--flex-volume-plugin-dir string
Full path of the directory in which the flex volume plugin should search for additional third party volume plugins. (default "/usr/libexec/kubernetes/kubelet-plugins/volume/exec/")

-h, --help                                                              help for kube-controller-manager

--horizontal-pod-autoscaler-downscale-delay duration
The period since last downscale, before another downscale can be performed in horizontal pod autoscaler. (default 5m0s)

--horizontal-pod-autoscaler-sync-period duration
The period for syncing the number of pods in horizontal pod autoscaler. (default 30s)

--horizontal-pod-autoscaler-tolerance float
The minimum change (from 1.0) in the desired-to-actual metrics ratio for the horizontal pod autoscaler to consider scaling. (default 0.1)

--horizontal-pod-autoscaler-upscale-delay duration
The period since last upscale, before another upscale can be performed in horizontal pod autoscaler. (default 3m0s)

--horizontal-pod-autoscaler-use-rest-clients                        WARNING: alpha feature.  If set to true, causes the horizontal pod autoscaler controller to use REST clients through the kube-aggregator, instead of using the legacy metrics client through the API server proxy.  This is required for custom metrics support in the horizontal pod autoscaler. (default true)

--http2-max-streams-per-connection int
The limit that the server gives to clients for the maximum number of streams in an HTTP/2 connection. Zero means to use golang's default.

--insecure-experimental-approve-all-kubelet-csrs-for-group string
This flag does nothing.

--kube-api-burst int32                                              Burst to use while talking with kubernetes apiserver. (default 30)

--kube-api-content-type string                                      Content type of requests sent to apiserver. (default "application/vnd.kubernetes.protobuf")

--kube-api-qps float32
QPS to use while talking with kubernetes apiserver. (default 20)

--kubeconfig string
Path to kubeconfig file with authorization and master location information.

--large-cluster-size-threshold int32                                Number of nodes from which NodeController treats the cluster as large for the eviction logic purposes. --secondary-node-eviction-rate is implicitly overridden to 0 for clusters this size or smaller. (default 50)

--leader-elect                                                      Start a leader election client and gain leadership before executing the main loop. Enable this when running replicated components for high availability. (default true)

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

--log-flush-frequency duration                                      Maximum number of seconds between log flushes (default 5s)

--loglevel int
Log level (0 = DEBUG, 5 = FATAL) (default 1)

--logtostderr
log to standard error instead of files (default true)

--master string
The address of the Kubernetes API server (overrides any value in kubeconfig).

--min-resync-period duration
The resync period in reflectors will be random between MinResyncPeriod and 2*MinResyncPeriod. (default 12h0m0s)

--namespace-sync-period duration
The period for syncing namespace life-cycle updates (default 5m0s)

--node-cidr-mask-size int32
Mask size for node cidr in cluster. (default 24)

--node-eviction-rate float32                                        Number of nodes per second on which pods are deleted in case of node failure when a zone is healthy (see --unhealthy-zone-threshold for definition of healthy/unhealthy). Zone refers to entire cluster in non-multizone clusters. (default 0.1)

--node-monitor-grace-period duration                                Amount of time which we allow running Node to be unresponsive before marking it unhealthy. Must be N times more than kubelet's nodeStatusUpdateFrequency, where N means number of retries allowed for kubelet to post node status. (default 40s)

--node-monitor-period duration
The period for syncing NodeStatus in NodeController. (default 5s)

--node-startup-grace-period duration                                Amount of time which we allow starting Node to be unresponsive before marking it unhealthy. (default 1m0s)

--pod-eviction-timeout duration
The grace period for deleting pods on failed nodes. (default 5m0s)

--port int                                                          DEPRECATED: the port on which to serve HTTP insecurely without authentication and authorization. If 0, don't serve HTTPS at all. See --secure-port instead. (default 10252)

--profiling                                                         Enable profiling via web interface host:port/debug/pprof/ (default true)

--pv-recycler-increment-timeout-nfs int32
the increment of time added per Gi to ActiveDeadlineSeconds for an NFS scrubber pod (default 30)

--pv-recycler-minimum-timeout-hostpath int32
The minimum ActiveDeadlineSeconds to use for a HostPath Recycler pod.  This is for development and testing only and will not work in a multi-node cluster. (default 60)

--pv-recycler-minimum-timeout-nfs int32
The minimum ActiveDeadlineSeconds to use for an NFS Recycler pod (default 300)

--pv-recycler-pod-template-filepath-hostpath string
The file path to a pod definition used as a template for HostPath persistent volume recycling. This is for development and testing only and will not work in a multi-node cluster.

--pv-recycler-pod-template-filepath-nfs string
The file path to a pod definition used as a template for NFS persistent volume recycling

--pv-recycler-timeout-increment-hostpath int32
the increment of time added per Gi to ActiveDeadlineSeconds for a HostPath scrubber pod.  This is for development and testing only and will not work in a multi-node cluster. (default 30)

--pvclaimbinder-sync-period duration
The period for syncing persistent volumes and persistent volume claims (default 15s)

--resource-quota-sync-period duration
The period for syncing quota usage status in the system (default 5m0s)

--root-ca-file string
If set, this root certificate authority will be included in service account's token secret. This must be a valid PEM-encoded CA bundle.

--route-reconciliation-period duration
The period for reconciling routes created for Nodes by cloud provider. (default 10s)

--secondary-node-eviction-rate float32                              Number of nodes per second on which pods are deleted in case of node failure when a zone is unhealthy (see --unhealthy-zone-threshold for definition of healthy/unhealthy). Zone refers to entire cluster in non-multizone clusters. This value is implicitly overridden to 0 if the cluster size is smaller than --large-cluster-size-threshold. (default 0.01)

--secure-port int
The port on which to serve HTTPS with authentication and authorization. If 0, don't serve HTTPS at all.

--service-account-private-key-file string                           Filename containing a PEM-encoded private RSA or ECDSA key used to sign service account tokens.

--service-cluster-ip-range string
CIDR Range for Services in cluster. Requires --allocate-node-cidrs to be true

--stderrthreshold severity
logs at or above this threshold go to stderr (default 2)

--terminated-pod-gc-threshold int32                                 Number of terminated pods that can exist before the terminated pod garbage collector starts deleting terminated pods. If <= 0, the terminated pod garbage collector is disabled. (default 12500)

--tls-cert-file string
File containing the default x509 Certificate for HTTPS. (CA cert, if any, concatenated after server cert). If HTTPS serving is enabled, and --tls-cert-file and --tls-private-key-file are not provided, a self-signed certificate and key are generated for the public address and saved to the directory specified by --cert-dir.

--tls-cipher-suites strings                                         Comma-separated list of cipher suites for the server. Values are from tls package constants (https://golang.org/pkg/crypto/tls/#pkg-constants). If omitted, the default Go cipher suites will be used

--tls-min-version string                                            Minimum TLS version supported. Value must match version names from https://golang.org/pkg/crypto/tls/#pkg-constants.

--tls-private-key-file string
File containing the default x509 private key matching --tls-cert-file.

--tls-sni-cert-key namedCertKey
A pair of x509 certificate and private key file paths, optionally suffixed with a list of domain patterns which are fully qualified domain names, possibly with prefixed wildcard segments. If no domain patterns are provided, the names of the certificate are extracted. Non-wildcard matches trump over wildcard matches, explicit domain patterns trump over extracted names. For multiple key/certificate pairs, use the --tls-sni-cert-key multiple times. Examples: "example.crt,example.key" or "foo.crt,foo.key:*.foo.com,foo.com". (default [])

--unhealthy-zone-threshold float32                                  Fraction of Nodes in a zone which needs to be not Ready (minimum 3) for zone to be treated as unhealthy.  (default 0.55)

--use-service-account-credentials
If true, use individual service account credentials for each controller.

-v, --v Level                                                           log level for V logs

--version version[=true]                                            Print version information and quit

--vmodule moduleSpec                                                comma-separated list of pattern=N settings for file-filtered logging

$ 

```

### kubectl
### kubelet
### kube-proxy
### kube-scheduler
### mounter
