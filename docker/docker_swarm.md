## docker swarm

### 初始化 Linux 系统

```bash
# 启动网络接口
$ ifup eth0

# 配置静态IP
$ ip address
$ vi /etc/sysconfig/network-scripts/ifcfg-eth0

# 关闭防火墙
$ service firewalld status
$ service firewalld stop

# 使用 aliyun 的 yum 镜像
$ curl -o /etc/yum.repos.d/CentOS-Aliyun.repo http://mirrors.aliyun.com/repo/Centos-7.repo

# 安装一般工具
$ yum makecache
$ yum install -y ntpdate wget vim net-tools unzip zip curl iptables

# 设置时区和同步时间
$ timedatectl
$ timedatectl set-timezone Asia/Shanghai
$ ntpdate ntp1.aliyun.com ntp2.aliyun.com ntp3.aliyun.com ntp4.aliyun.com
$ date

# 安装 docker
$ sudo yum install -y yum-utils device-mapper-persistent-data lvm2
$ sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
$ sudo yum makecache fast
$ sudo yum install -y docker-ce
$ systemctl daemon-reload
$ systemctl enable docker.service
$ systemctl start docker.service
$ systemctl status docker.service

# 检查 docker 的安装
$ docker info

# 安装docker-compose
$ curl -L https://github.com/docker/compose/releases/download/1.15.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
$ chmod +x /usr/local/bin/docker-compose
$ /usr/local/bin/docker-compose --version
$ docker-compose --version
$ ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
$ ln -s /usr/local/bin/docker-compose /usr/sbin/docker-compose

# 设置 hostname
$ hostnamectl set-hostname swarm-01
$ hostnamectl set-hostname swarm-02
$ hostnamectl set-hostname swarm-03
$ hostnamectl set-hostname swarm-04
$ hostnamectl set-hostname swarm-05
$ hostnamectl

# 设置 /etc/hosts
$ vim /etc/hosts
10.128.128.110  swarm-01
10.128.128.158  swarm-02
10.128.128.238  swarm-03
10.128.128.226  swarm-04
10.128.128.213  swarm-05

# 设置
$ vim /etc/resolv.conf
nameserver 114.114.114.114


```

### docker swarm 集群规划

| hostname | IP | role |
|--------|--------|--------|
| swarm-01 | 10.128.128.110 | manager 节点 |
| swarm-02 | 10.128.128.158 | worker 节点 |
| swarm-03 | 10.128.128.238 | worker 节点 |
| swarm-04 | 10.128.128.226 | worker 节点 |
| swarm-05 | 10.128.128.213 | worker 节点 |


### 相关命令帮助

```bash
[root@localhost ~]# docker swarm --help

Usage:	docker swarm COMMAND

Manage Swarm

Commands:
  ca          Display and rotate the root CA
  init        Initialize a swarm
  join        Join a swarm as a node and/or manager
  join-token  Manage join tokens
  leave       Leave the swarm
  unlock      Unlock swarm
  unlock-key  Manage the unlock key
  update      Update the swarm

Run 'docker swarm COMMAND --help' for more information on a command.
[root@localhost ~]#
[root@localhost ~]# docker node --help

Usage:	docker node COMMAND

Manage Swarm nodes

Commands:
  demote      Demote降级 one or more nodes from manager in the swarm
  inspect     Display detailed information on one or more nodes
  ls          List nodes in the swarm
  promote     Promote提升 one or more nodes to manager in the swarm
  ps          List tasks running on one or more nodes, defaults to current node
  rm          Remove one or more nodes from the swarm
  update      Update a node

Run 'docker node COMMAND --help' for more information on a command.
[root@localhost ~]#

[root@localhost ~]# docker service --help

Usage:	docker service COMMAND

Manage services

Commands:
  create      Create a new service
  inspect     Display detailed information on one or more services
  logs        Fetch the logs of a service or task
  ls          List services
  ps          List the tasks of one or more services
  rm          Remove one or more services
  rollback    Revert changes to a service's configuration
  scale       Scale one or multiple replicated services
  update      Update a service

Run 'docker service COMMAND --help' for more information on a command.
[root@localhost ~]#

```



### 创建 docker swarm 集群

manager 节点

```bash
# 初始化 docker swarm 集群
[root@localhost ~]# docker swarm init --advertise-addr 10.128.128.110
Swarm initialized: current node (2s6b4q4j9fi80bdu0sek2l8xj) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join --token SWMTKN-1-00r7shqn93w0o8wjs613tmfjym3x5k634jv3zryhljvo4yapct-4wonogbaovtgaezwn7la8aq3k 10.128.128.110:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.

[root@localhost ~]#
# 打印增加 worker 节点的命令
[root@localhost ~]# docker swarm join-token worker
To add a worker to this swarm, run the following command:

    docker swarm join --token SWMTKN-1-00r7shqn93w0o8wjs613tmfjym3x5k634jv3zryhljvo4yapct-4wonogbaovtgaezwn7la8aq3k 10.128.128.110:2377

[root@localhost ~]#
# docker info 说明 Swarm 信息
[root@localhost ~]# docker info
Containers: 1
 Running: 1
 Paused: 0
 Stopped: 0
Images: 1
Server Version: 17.06.1-ce
Storage Driver: overlay
 Backing Filesystem: xfs
 Supports d_type: true
Logging Driver: json-file
Cgroup Driver: cgroupfs
Plugins:
 Volume: local
 Network: bridge host macvlan null overlay
 Log: awslogs fluentd gcplogs gelf journald json-file logentries splunk syslog
Swarm: active
 NodeID: 2s6b4q4j9fi80bdu0sek2l8xj
 Is Manager: true
 ClusterID: 00sa0s0lwwrpw6bunt0pqc740
 Managers: 1
 Nodes: 5
 Orchestration:
  Task History Retention Limit: 5
 Raft:
  Snapshot Interval: 10000
  Number of Old Snapshots to Retain: 0
  Heartbeat Tick: 1
  Election Tick: 3
 Dispatcher:
  Heartbeat Period: 5 seconds
 CA Configuration:
  Expiry Duration: 3 months
  Force Rotate: 0
 Root Rotation In Progress: false
 Node Address: 10.128.128.110
 Manager Addresses:
  10.128.128.110:2377
Runtimes: runc
Default Runtime: runc
Init Binary: docker-init
containerd version: 6e23458c129b551d5c9871e5174f6b1b7f6d1170
runc version: 810190ceaa507aa2727d7ae6f4790c76ec150bd2
init version: 949e6fa
Security Options:
 seccomp
  Profile: default
Kernel Version: 3.10.0-514.el7.x86_64
Operating System: CentOS Linux 7 (Core)
OSType: linux
Architecture: x86_64
CPUs: 2
Total Memory: 1.796GiB
Name: swarm-01
ID: LA5B:5L7N:J46U:P2JU:LAKL:UUVM:LA3D:JPSX:RIUB:CPZK:EPZA:FXZ6
Docker Root Dir: /var/lib/docker
Debug Mode (client): false
Debug Mode (server): false
Registry: https://index.docker.io/v1/
Experimental: false
Insecure Registries:
 127.0.0.0/8
Live Restore Enabled: false

[root@localhost ~]#
# 显示集群中的节点
[root@localhost ~]# docker node ls
ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS
2s6b4q4j9fi80bdu0sek2l8xj *   swarm-01            Ready               Active              Leader
###################################################################################################################################
[root@localhost ~]#
# 在 worker 节点机器上执行加入集群的命令
[root@localhost ~]# docker node ls
ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS
2s6b4q4j9fi80bdu0sek2l8xj *   swarm-01            Ready               Active              Leader
3w3014he63242togyeyb35k1w     swarm-02            Ready               Active             
fivl9s8cvlrweptjjacu8zqv8     swarm-04            Ready               Active             
jqher5t38yyir31it3b6dxfry     swarm-05            Ready               Active             
pzuezfs7ykegw0dvslpznwssa     swarm-03            Ready               Active             
[root@localhost ~]#
# 显示一个节点的详细信息
[root@localhost ~]# docker node inspect --pretty 2s6b4q4j9fi80bdu0sek2l8xj
ID:            2s6b4q4j9fi80bdu0sek2l8xj
Hostname:                  swarm-01
Joined at:                 2017-08-25 13:22:32.575640702 +0000 utc
Status:
 State:            Ready
 Availability:             Active
 Address:        10.128.128.110
Manager Status:
 Address:        10.128.128.110:2377
 Raft Status:        Reachable
 Leader:        Yes
Platform:
 Operating System:    linux
 Architecture:        x86_64
Resources:
 CPUs:            2
 Memory:        1.796GiB
Plugins:
 Log:        awslogs, fluentd, gcplogs, gelf, journald, json-file, logentries, splunk, syslog
 Network:        bridge, host, macvlan, null, overlay
 Volume:        local
Engine Version:        17.06.1-ce
TLS Info:
 TrustRoot:
-----BEGIN CERTIFICATE-----
MIIBazCCARCgAwIBAgIUV9+lhfN8rnixxKO/Z81b0NIJ3vcwCgYIKoZIzj0EAwIw
EzERMA8GA1UEAxMIc3dhcm0tY2EwHhcNMTcwODI1MTMxODAwWhcNMzcwODIwMTMx
ODAwWjATMREwDwYDVQQDEwhzd2FybS1jYTBZMBMGByqGSM49AgEGCCqGSM49AwEH
A0IABFWoY4MMErx4kVSvdvALpnpI2aVh1gyUdY64UaGXJrac1EuswgrQ+mdInRdi
SUK+gryTH8HbvFgLDKGN1x+u6K+jQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMB
Af8EBTADAQH/MB0GA1UdDgQWBBRpRcbjYujVrgM/KZJjhv6XxAU2mjAKBggqhkjO
PQQDAgNJADBGAiEA4R+o0nX2mfmjnWdIOF1+HUjeF0Z2NPnOIDFDV/dH0V4CIQDV
Dv509/AhNKyx35VpCeE478upV6Ghd4TGPx5nh53U6A==
-----END CERTIFICATE-----

 Issuer Subject:    MBMxETAPBgNVBAMTCHN3YXJtLWNh
 Issuer Public Key:    MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEVahjgwwSvHiRVK928AumekjZpWHWDJR1jrhRoZcmtpzUS6zCCtD6Z0idF2JJQr6CvJMfwdu8WAsMoY3XH67orw==
[root@localhost ~]#
[root@localhost ~]# docker node inspect --pretty 3w3014he63242togyeyb35k1w
ID:            3w3014he63242togyeyb35k1w
Hostname:                  swarm-02
Joined at:                 2017-08-25 13:24:33.36440352 +0000 utc
Status:
 State:            Ready
 Availability:             Active
 Address:        10.128.128.158
Platform:
 Operating System:    linux
 Architecture:        x86_64
Resources:
 CPUs:            2
 Memory:        1.796GiB
Plugins:
 Log:        awslogs, fluentd, gcplogs, gelf, journald, json-file, logentries, splunk, syslog
 Network:        bridge, host, macvlan, null, overlay
 Volume:        local
Engine Version:        17.06.1-ce
TLS Info:
 TrustRoot:
-----BEGIN CERTIFICATE-----
MIIBazCCARCgAwIBAgIUV9+lhfN8rnixxKO/Z81b0NIJ3vcwCgYIKoZIzj0EAwIw
EzERMA8GA1UEAxMIc3dhcm0tY2EwHhcNMTcwODI1MTMxODAwWhcNMzcwODIwMTMx
ODAwWjATMREwDwYDVQQDEwhzd2FybS1jYTBZMBMGByqGSM49AgEGCCqGSM49AwEH
A0IABFWoY4MMErx4kVSvdvALpnpI2aVh1gyUdY64UaGXJrac1EuswgrQ+mdInRdi
SUK+gryTH8HbvFgLDKGN1x+u6K+jQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMB
Af8EBTADAQH/MB0GA1UdDgQWBBRpRcbjYujVrgM/KZJjhv6XxAU2mjAKBggqhkjO
PQQDAgNJADBGAiEA4R+o0nX2mfmjnWdIOF1+HUjeF0Z2NPnOIDFDV/dH0V4CIQDV
Dv509/AhNKyx35VpCeE478upV6Ghd4TGPx5nh53U6A==
-----END CERTIFICATE-----

 Issuer Subject:    MBMxETAPBgNVBAMTCHN3YXJtLWNh
 Issuer Public Key:    MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEVahjgwwSvHiRVK928AumekjZpWHWDJR1jrhRoZcmtpzUS6zCCtD6Z0idF2JJQr6CvJMfwdu8WAsMoY3XH67orw==
###################################################################################################################################
[root@localhost ~]#

# 创建服务
[root@localhost ~]# docker service create --replicas 1 --name helloworld alpine ping docker.com
74kpf3mryfg3p3r5cii4pd6fa
Since --detach=false was not specified, tasks will be created in the background.
In a future release, --detach=false will become the default.
[root@localhost ~]#
[root@localhost ~]# docker service ls
ID                  NAME                MODE                REPLICAS            IMAGE               PORTS
74kpf3mryfg3        helloworld          replicated          1/1                 alpine:latest       
[root@localhost ~]#
[root@localhost ~]# docker service inspect --pretty helloworld
ID:        74kpf3mryfg3p3r5cii4pd6fa
Name:        helloworld
Service Mode:    Replicated
 Replicas:    1
Placement:
UpdateConfig:
 Parallelism:    1
 On failure:    pause
 Monitoring Period: 5s
 Max failure ratio: 0
 Update order:      stop-first
RollbackConfig:
 Parallelism:    1
 On failure:    pause
 Monitoring Period: 5s
 Max failure ratio: 0
 Rollback order:    stop-first
ContainerSpec:
 Image:        alpine:latest@sha256:1072e499f3f655a032e88542330cf75b02e7bdf673278f701d7ba61629ee3ebe
 Args:        ping docker.com
Resources:
Endpoint Mode:    vip
[root@localhost ~]#
[root@localhost ~]# docker service inspect helloworld
[
    {
        "ID": "74kpf3mryfg3p3r5cii4pd6fa",
        "Version": {
            "Index": 31
        },
        "CreatedAt": "2017-08-25T13:27:05.486683242Z",
        "UpdatedAt": "2017-08-25T13:27:05.486683242Z",
        "Spec": {
            "Name": "helloworld",
            "Labels": {},
            "TaskTemplate": {
                "ContainerSpec": {
                    "Image": "alpine:latest@sha256:1072e499f3f655a032e88542330cf75b02e7bdf673278f701d7ba61629ee3ebe",
                    "Args": [
                        "ping",
                        "docker.com"
                    ],
                    "StopGracePeriod": 10000000000,
                    "DNSConfig": {}
                },
                "Resources": {
                    "Limits": {},
                    "Reservations": {}
                },
                "RestartPolicy": {
                    "Condition": "any",
                    "Delay": 5000000000,
                    "MaxAttempts": 0
                },
                "Placement": {
                    "Platforms": [
                        {
                            "Architecture": "amd64",
                            "OS": "linux"
                        }
                    ]
                },
                "ForceUpdate": 0,
                "Runtime": "container"
            },
            "Mode": {
                "Replicated": {
                    "Replicas": 1
                }
            },
            "UpdateConfig": {
                "Parallelism": 1,
                "FailureAction": "pause",
                "Monitor": 5000000000,
                "MaxFailureRatio": 0,
                "Order": "stop-first"
            },
            "RollbackConfig": {
                "Parallelism": 1,
                "FailureAction": "pause",
                "Monitor": 5000000000,
                "MaxFailureRatio": 0,
                "Order": "stop-first"
            },
            "EndpointSpec": {
                "Mode": "vip"
            }
        },
        "Endpoint": {
            "Spec": {}
        }
    }
]
[root@localhost ~]#
# 显示服务中的任务
[root@localhost ~]# docker service ps helloworld
ID                  NAME                IMAGE               NODE                    DESIRED STATE       CURRENT STATE           ERROR               PORTS
v78a07w97t0q        helloworld.1        alpine:latest       localhost.localdomain   Running             Running 2 minutes ago                       
[root@localhost ~]#
# 将服务扩展到6个
[root@localhost ~]# docker service scale helloworld=6
helloworld scaled to 6
[root@localhost ~]#
[root@localhost ~]# docker service ls
ID                  NAME                MODE                REPLICAS            IMAGE               PORTS
74kpf3mryfg3        helloworld          replicated          6/6                 alpine:latest       
[root@localhost ~]#  
[root@localhost ~]# docker service ps helloworld
ID                  NAME                IMAGE               NODE                DESIRED STATE       CURRENT STATE            ERROR               PORTS
v78a07w97t0q        helloworld.1        alpine:latest       swarm-03            Running             Running 15 minutes ago                       
6avxiczbv6n0        helloworld.2        alpine:latest       swarm-01            Running             Running 11 minutes ago                       
1ix19nu0x9bt        helloworld.3        alpine:latest       swarm-04            Running             Running 11 minutes ago                       
oxomkt9dir1z        helloworld.4        alpine:latest       swarm-05            Running             Running 11 minutes ago                       
ukgwhf3guhjr        helloworld.5        alpine:latest       swarm-05            Running             Running 11 minutes ago                       
sczweh2s46e0        helloworld.6        alpine:latest       swarm-02            Running             Running 11 minutes ago                       
[root@localhost ~]#
###################################################################################################################################
[root@localhost ~]# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
alpine              <none>              7328f6f8b418        8 weeks ago         3.96MB
[root@localhost ~]# docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
4156abcaaa3c        alpine:latest       "ping docker.com"   13 minutes ago      Up 13 minutes                           helloworld.2.6avxiczbv6n0wqslicbgx51ix
[root@localhost ~]# docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
f21efc3c068d        bridge              bridge              local
a2ba5c4f0fd2        docker_gwbridge     bridge              local
b833743707da        host                host                local
tvd8r3ej0emx        ingress             overlay             swarm
1f571176f955        none                null                local
[root@localhost ~]#
###################################################################################################################################
[root@localhost ~]# docker service rm helloworld
helloworld
[root@localhost ~]#
[root@localhost ~]# docker service ls
ID                  NAME                MODE                REPLICAS            IMAGE               PORTS
[root@localhost ~]#
[root@localhost ~]# docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
[root@localhost ~]#
[root@localhost ~]# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
alpine              <none>              7328f6f8b418        8 weeks ago         3.96MB
[root@localhost ~]#
###################################################################################################################################
[root@swarm-01 ~]# docker node ls
ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS
2s6b4q4j9fi80bdu0sek2l8xj *   swarm-01            Ready               Active              Leader
3w3014he63242togyeyb35k1w     swarm-02            Ready               Active             
fivl9s8cvlrweptjjacu8zqv8     swarm-04            Ready               Active             
jqher5t38yyir31it3b6dxfry     swarm-05            Ready               Active             
pzuezfs7ykegw0dvslpznwssa     swarm-03            Ready               Active             
[root@swarm-01 ~]#
[root@swarm-01 ~]# docker node promote 3w3014he63242togyeyb35k1w
Node 3w3014he63242togyeyb35k1w promoted to a manager in the swarm.
[root@swarm-01 ~]# docker node ls
ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS
2s6b4q4j9fi80bdu0sek2l8xj *   swarm-01            Ready               Active              Leader
3w3014he63242togyeyb35k1w     swarm-02            Ready               Active              Reachable
fivl9s8cvlrweptjjacu8zqv8     swarm-04            Ready               Active             
jqher5t38yyir31it3b6dxfry     swarm-05            Ready               Active             
pzuezfs7ykegw0dvslpznwssa     swarm-03            Ready               Active             
[root@swarm-01 ~]#
[root@swarm-01 ~]# docker node promote pzuezfs7ykegw0dvslpznwssa
Node pzuezfs7ykegw0dvslpznwssa promoted to a manager in the swarm.
[root@swarm-01 ~]#
[root@swarm-01 ~]# docker node ls
ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS
2s6b4q4j9fi80bdu0sek2l8xj *   swarm-01            Ready               Active              Leader
3w3014he63242togyeyb35k1w     swarm-02            Ready               Active              Reachable
fivl9s8cvlrweptjjacu8zqv8     swarm-04            Ready               Active             
jqher5t38yyir31it3b6dxfry     swarm-05            Ready               Active             
pzuezfs7ykegw0dvslpznwssa     swarm-03            Ready               Active              Reachable
[root@swarm-01 ~]#
[root@swarm-01 ~]# docker node promote fivl9s8cvlrweptjjacu8zqv8
Node fivl9s8cvlrweptjjacu8zqv8 promoted to a manager in the swarm.
[root@swarm-01 ~]# docker node ls
ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS
2s6b4q4j9fi80bdu0sek2l8xj *   swarm-01            Ready               Active              Leader
3w3014he63242togyeyb35k1w     swarm-02            Ready               Active              Reachable
fivl9s8cvlrweptjjacu8zqv8     swarm-04            Ready               Active              Reachable
jqher5t38yyir31it3b6dxfry     swarm-05            Ready               Active             
pzuezfs7ykegw0dvslpznwssa     swarm-03            Ready               Active              Reachable
[root@swarm-01 ~]#

[root@swarm-01 ~]# docker node demote fivl9s8cvlrweptjjacu8zqv8
Manager fivl9s8cvlrweptjjacu8zqv8 demoted in the swarm.
[root@swarm-01 ~]# docker node ls
ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS
2s6b4q4j9fi80bdu0sek2l8xj *   swarm-01            Ready               Active              Leader
3w3014he63242togyeyb35k1w     swarm-02            Ready               Active              Reachable
fivl9s8cvlrweptjjacu8zqv8     swarm-04            Ready               Active             
jqher5t38yyir31it3b6dxfry     swarm-05            Ready               Active             
pzuezfs7ykegw0dvslpznwssa     swarm-03            Ready               Active              Reachable
[root@swarm-01 ~]#

```


worker节点

```bash
# worker 节点加入集群
[root@localhost ~]# docker swarm join --token SWMTKN-1-00r7shqn93w0o8wjs613tmfjym3x5k634jv3zryhljvo4yapct-4wonogbaovtgaezwn7la8aq3k 10.128.128.110:2377
This node joined a swarm as a worker.
[root@localhost ~]#
###################################################################################################################################
[root@localhost ~]# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
alpine              <none>              7328f6f8b418        8 weeks ago         3.96MB
[root@localhost ~]# docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
aaedd7e53004        alpine:latest       "ping docker.com"   13 minutes ago      Up 13 minutes                           helloworld.6.sczweh2s46e02bilpkisqgve0
[root@localhost ~]# docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
b31b40b4cd67        bridge              bridge              local
75813f588c32        docker_gwbridge     bridge              local
d4f7b6d58414        host                host                local
tvd8r3ej0emx        ingress             overlay             swarm
60aeefc1a055        none                null                local
[root@localhost ~]#
###################################################################################################################################
[root@localhost ~]# docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
[root@localhost ~]# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
alpine              <none>              7328f6f8b418        8 weeks ago         3.96MB
[root@localhost ~]#

[root@localhost ~]# docker node ls
Error response from daemon: This node is not a swarm manager. Worker nodes can't be used to view or modify cluster state. Please run this command on a manager node or promote the current node to a manager.
[root@localhost ~]#
```

