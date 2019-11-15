# Ceph Install

```
  +--------------+               +--------------+
  |              |               |              |
  |    ceph1     |_______________|     ceph2    |
  | MONITOR,OSD  |               |      OSD     |
  |              |               |              |
  +--------------+               +--------------+

```

### 为 ceph1 和 ceph2 安装 Ceph 和 ceph-deploy

```bash
root@ceph1:~# apt-get update
root@ceph1:~# apt-get install -y ceph ceph-deploy

root@ceph2:~# apt-get update
root@ceph2:~# apt-get install -y ceph ceph-deploy
```

### 为 ceph1 和 ceph2 创建文件夹

```bash
root@ceph1:~# mkdir -p /root/cluster 
root@ceph1:~# rm -f /root/cluster/*

root@ceph1:~# mkdir -p /osd1 & rm -rf /osd1/*
root@ceph1:~# chown ceph:ceph /osd1
root@ceph2:~# mkdir -p /osd2 & rm -rf /osd2/*
root@ceph2:~# chown ceph:ceph /osd2

root@ceph1:~# mkdir -p /var/run/ceph/
root@ceph1:~# chown ceph:ceph /var/run/ceph/
root@ceph2:~# mkdir -p /var/run/ceph/
root@ceph2:~# chown ceph:ceph /var/run/ceph/

```

### 在 ceph1 节点初始化 ceph

```bash
root@ceph1:~# cd /root/cluster
root@ceph1:~/cluster# ceph-deploy new ceph1
root@ceph1:~/cluster# ls
ceph-deploy-ceph.log  ceph.conf  ceph.mon.keyring
root@ceph1:~/cluster# ls /etc/ceph/
rbdmap
root@ceph1:~/cluster# ls /var/run/ceph/
root@ceph1:~/cluster# vim ceph.conf 
[global]
···
···
osd pool default size = 2
osd crush chooseleaf type = 0
osd max object name len = 256
osd journal size = 128

```

### 在 ceph1 激活 Monitor

```bash
root@ceph1:~/cluster# ceph-deploy mon create-initial
...
[ceph_deploy.gatherkeys][DEBUG ] Got ceph.bootstrap-rgw.keyring key from ceph1.

```

### 在 ceph1 为集群中两个节点创建 OSD

```bash
root@ceph1:~/cluster# ceph-deploy osd prepare ceph1:/osd1 ceph2:/osd2
...
[ceph_deploy.osd][DEBUG ] Host ceph1 is now ready for osd use.
...
[ceph_deploy.osd][DEBUG ] Host ceph2 is now ready for osd use.

root@ceph1:~/cluster# ceph-deploy osd activate ceph1:/osd1 ceph2:/osd2

```

### 拷贝配置到 ceph1 和 ceph2

```bash
root@ceph1:~/cluster# ceph-deploy admin ceph1 ceph2
root@ceph1:~/cluster# chmod +r /etc/ceph/ceph.client.admin.keyring
root@ceph2:~/cluster# chmod +r /etc/ceph/ceph.client.admin.keyring

```

### 验证安装结果

```bash
root@ceph1:~/cluster# ceph -v
ceph version 10.2.10 (5dc1e4c05cb68dbf62ae6fce3f0700e4654fdbbe)

root@ceph1:~/cluster# ceph -s

```


参考
* https://kubesphere.io/docs/v2.1/zh-CN/appendix/ceph-ks-install/
* https://docs.ceph.com/docs/master/start/quick-start-preflight/#create-a-ceph-deploy-user







| 编号 | hostname | ip | user/paswword | disk | process |
| ---- | ---- | ---- | ---- | ---- | ---- |
| 1 | ceph-01 | 10.0.10.21 | root/root | /dev/sdb | mon、mgr、osd |
| 2 | ceph-02 | 10.0.10.22 | root/root | /dev/sdb | mon、mgr、osd |
| 3 | ceph-03 | 10.0.10.23 | root/root | /dev/sdb | mon、mgr、osd |

### 准备工作
```bash
# 永久关闭 selinux
$ vim /etc/sysconfig/selinux
SELINUX=disabled
$ getenforce

# 关闭防火墙
$ systemctl stop firewalld.service
$ systemctl status firewalld.service

# 清除 iptable 规则

# 设置时区和同步时间
$ timedatectl set-timezone Asia/Shanghai
$ ntpdate ntp1.aliyun.com ntp2.aliyun.com ntp3.aliyun.com ntp4.aliyun.com

# 修改 hosts
$ cat /etc/hosts
10.0.10.21 ceph-01
10.0.10.22 ceph-02
10.0.10.23 ceph-03

# 添加 EPEL yum 源
$ yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
# 添加 ceph yum 源
$ yum install centos-release-ceph-nautilus.noarch
$ yum clean all; yum makecache fast

# 添加 ceph 用户
$ useradd -d /home/ceph -m ceph
$ echo 'ceph!@#$%^' | passwd --stdin ceph
$ echo "ceph ALL = (root) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/ceph
$ chmod 0440 /etc/sudoers.d/ceph

# root 用户免密
$ ssh-keygen
/root/.ssh/ceph
/root/.ssh/ceph.pub

$ ssh-copy-id -i /root/.ssh/ceph root@ceph-02
$ ssh-copy-id -i /root/.ssh/ceph root@ceph-03

$ ssh -i /root/.ssh/ceph root@ceph-02
$ ssh -i /root/.ssh/ceph root@ceph-03

# ceph 用户免密
$ su - ceph
$ ssh-keygen
/home/ceph/.ssh/ceph
/home/ceph/.ssh/ceph.pub

$ ssh-copy-id -i /home/ceph/.ssh/ceph ceph@ceph-02
$ ssh-copy-id -i /home/ceph/.ssh/ceph ceph@ceph-03

$ ssh -i /home/ceph/.ssh/ceph ceph@ceph-02
$ ssh -i /home/ceph/.ssh/ceph ceph@ceph-03

```

### 在管理节点(ceph-01)安装 ceph-deploy
```bash
$ su - root
$ yum install ceph-deploy ceph-common
$ ceph-deploy --version
2.0.1

```

### 部署 ceph 集群

```bash
# ceph-01 ceph-02 ceph-03 ceph 集群节点
$ su - root
$ yum install ceph ceph-radosgw

# ceph-01 管理节点
$ su - ceph
$ mkdir -p /home/ceph/ceph-cluster
$ cd /home/ceph/ceph-cluster

# ceph-01 管理节点
# Start deploying a new cluster, and write a CLUSTER.conf and keyring for it.
$ ceph-deploy new ceph-01 --cluster-network 10.0.10.0/24 --public-network 10.0.10.0/24
[ceph_deploy.conf][DEBUG ] found configuration file at: /home/ceph/.cephdeploy.conf
[ceph_deploy.cli][INFO  ] Invoked (2.0.1): /bin/ceph-deploy new ceph-01 --cluster-network 10.0.10.0/24 --public-network 10.0.10.0/24
[ceph_deploy.cli][INFO  ] ceph-deploy options:
[ceph_deploy.cli][INFO  ]  username                      : None
[ceph_deploy.cli][INFO  ]  func                          : <function new at 0x7f9e09446de8>
[ceph_deploy.cli][INFO  ]  verbose                       : False
[ceph_deploy.cli][INFO  ]  overwrite_conf                : False
[ceph_deploy.cli][INFO  ]  quiet                         : False
[ceph_deploy.cli][INFO  ]  cd_conf                       : <ceph_deploy.conf.cephdeploy.Conf instance at 0x7f9e08bc4128>
[ceph_deploy.cli][INFO  ]  cluster                       : ceph
[ceph_deploy.cli][INFO  ]  ssh_copykey                   : True
[ceph_deploy.cli][INFO  ]  mon                           : ['ceph-01']
[ceph_deploy.cli][INFO  ]  public_network                : 10.0.10.0/24
[ceph_deploy.cli][INFO  ]  ceph_conf                     : None
[ceph_deploy.cli][INFO  ]  cluster_network               : 10.0.10.0/24
[ceph_deploy.cli][INFO  ]  default_release               : False
[ceph_deploy.cli][INFO  ]  fsid                          : None
[ceph_deploy.new][DEBUG ] Creating new cluster named ceph
[ceph_deploy.new][INFO  ] making sure passwordless SSH succeeds
[ceph-01][DEBUG ] connection detected need for sudo
[ceph-01][DEBUG ] connected to host: ceph-01
[ceph-01][DEBUG ] detect platform information from remote host
[ceph-01][DEBUG ] detect machine type
[ceph-01][DEBUG ] find the location of an executable
[ceph-01][INFO  ] Running command: sudo /usr/sbin/ip link show
[ceph-01][INFO  ] Running command: sudo /usr/sbin/ip addr show
[ceph-01][DEBUG ] IP addresses found: [u'10.0.10.21']
[ceph_deploy.new][DEBUG ] Resolving host ceph-01
[ceph_deploy.new][DEBUG ] Monitor ceph-01 at 10.0.10.21
[ceph_deploy.new][DEBUG ] Monitor initial members are ['ceph-01']
[ceph_deploy.new][DEBUG ] Monitor addrs are [u'10.0.10.21']
[ceph_deploy.new][DEBUG ] Creating a random mon key...
[ceph_deploy.new][DEBUG ] Writing monitor keyring to ceph.mon.keyring...
[ceph_deploy.new][DEBUG ] Writing initial config to ceph.conf...
$ ll
total 12
-rw-rw-r-- 1 ceph ceph  256 Nov 14 17:09 ceph.conf
-rw-rw-r-- 1 ceph ceph 3100 Nov 14 17:09 ceph-deploy-ceph.log
-rw------- 1 ceph ceph   73 Nov 14 17:09 ceph.mon.keyring
$ cat ceph.conf
[global]
fsid = 879b266e-2134-49f0-b097-c0468c45597b
public_network = 10.0.10.0/24
cluster_network = 10.0.10.0/24
mon_initial_members = ceph-01
mon_host = 10.0.10.21
auth_cluster_required = cephx
auth_service_required = cephx
auth_client_required = cephx

$ cat ceph.mon.keyring
[mon.]
key = AQDVGc1dAAAAABAANPEDZbc01d+YQCeR81CK6Q==
caps mon = allow *
$

# Install Ceph packages on remote hosts.
$ ceph-deploy install --no-adjust-repos ceph-01 ceph-02 ceph-03
[ceph_deploy.conf][DEBUG ] found configuration file at: /home/ceph/.cephdeploy.conf
[ceph_deploy.cli][INFO  ] Invoked (2.0.1): /bin/ceph-deploy install --no-adjust-repos ceph-01 ceph-02 ceph-03
[ceph_deploy.cli][INFO  ] ceph-deploy options:
[ceph_deploy.cli][INFO  ]  verbose                       : False
[ceph_deploy.cli][INFO  ]  testing                       : None
[ceph_deploy.cli][INFO  ]  cd_conf                       : <ceph_deploy.conf.cephdeploy.Conf instance at 0x7fafb379dcf8>
[ceph_deploy.cli][INFO  ]  cluster                       : ceph
[ceph_deploy.cli][INFO  ]  dev_commit                    : None
[ceph_deploy.cli][INFO  ]  install_mds                   : False
[ceph_deploy.cli][INFO  ]  stable                        : None
[ceph_deploy.cli][INFO  ]  default_release               : False
[ceph_deploy.cli][INFO  ]  username                      : None
[ceph_deploy.cli][INFO  ]  adjust_repos                  : False
[ceph_deploy.cli][INFO  ]  func                          : <function install at 0x7fafb42835f0>
[ceph_deploy.cli][INFO  ]  install_mgr                   : False
[ceph_deploy.cli][INFO  ]  install_all                   : False
[ceph_deploy.cli][INFO  ]  repo                          : False
[ceph_deploy.cli][INFO  ]  host                          : ['ceph-01', 'ceph-02', 'ceph-03']
[ceph_deploy.cli][INFO  ]  install_rgw                   : False
[ceph_deploy.cli][INFO  ]  install_tests                 : False
[ceph_deploy.cli][INFO  ]  repo_url                      : None
[ceph_deploy.cli][INFO  ]  ceph_conf                     : None
[ceph_deploy.cli][INFO  ]  install_osd                   : False
[ceph_deploy.cli][INFO  ]  version_kind                  : stable
[ceph_deploy.cli][INFO  ]  install_common                : False
[ceph_deploy.cli][INFO  ]  overwrite_conf                : False
[ceph_deploy.cli][INFO  ]  quiet                         : False
[ceph_deploy.cli][INFO  ]  dev                           : master
[ceph_deploy.cli][INFO  ]  nogpgcheck                    : False
[ceph_deploy.cli][INFO  ]  local_mirror                  : None
[ceph_deploy.cli][INFO  ]  release                       : None
[ceph_deploy.cli][INFO  ]  install_mon                   : False
[ceph_deploy.cli][INFO  ]  gpg_url                       : None
[ceph_deploy.install][DEBUG ] Installing stable version mimic on cluster ceph hosts ceph-01 ceph-02 ceph-03
[ceph_deploy.install][DEBUG ] Detecting platform for host ceph-01 ...
[ceph-01][DEBUG ] connection detected need for sudo
[ceph-01][DEBUG ] connected to host: ceph-01
[ceph-01][DEBUG ] detect platform information from remote host
[ceph-01][DEBUG ] detect machine type
[ceph_deploy.install][INFO  ] Distro info: CentOS Linux 7.7.1908 Core
[ceph-01][INFO  ] installing Ceph on ceph-01
[ceph-01][INFO  ] Running command: sudo yum clean all
[ceph-01][DEBUG ] Loaded plugins: fastestmirror
[ceph-01][DEBUG ] Cleaning repos: base centos-ceph-nautilus centos-nfs-ganesha28 ceph-noarch epel
[ceph-01][DEBUG ]               : extras updates
[ceph-01][DEBUG ] Cleaning up list of fastest mirrors
[ceph-01][INFO  ] Running command: sudo yum -y install ceph ceph-radosgw
[ceph-01][DEBUG ] Loaded plugins: fastestmirror
[ceph-01][DEBUG ] Determining fastest mirrors
[ceph-01][DEBUG ]  * base: mirrors.aliyun.com
[ceph-01][DEBUG ]  * centos-ceph-nautilus: mirrors.aliyun.com
[ceph-01][DEBUG ]  * centos-nfs-ganesha28: mirrors.aliyun.com
[ceph-01][DEBUG ]  * extras: mirrors.aliyun.com
[ceph-01][DEBUG ]  * updates: mirrors.163.com
[ceph-01][DEBUG ] Package 2:ceph-14.2.1-0.el7.x86_64 already installed and latest version
[ceph-01][DEBUG ] Package 2:ceph-radosgw-14.2.1-0.el7.x86_64 already installed and latest version
[ceph-01][DEBUG ] Nothing to do
[ceph-01][INFO  ] Running command: sudo ceph --version
[ceph-01][DEBUG ] ceph version 14.2.1 (d555a9489eb35f84f2e1ef49b77e19da9d113972) nautilus (stable)
[ceph_deploy.install][DEBUG ] Detecting platform for host ceph-02 ...
ceph@ceph-02's password:
Permission denied, please try again.
ceph@ceph-02's password:
[ceph-02][DEBUG ] connection detected need for sudo
ceph@ceph-02's password:
[ceph-02][DEBUG ] connected to host: ceph-02
[ceph-02][DEBUG ] detect platform information from remote host
[ceph-02][DEBUG ] detect machine type
[ceph_deploy.install][INFO  ] Distro info: CentOS Linux 7.7.1908 Core
[ceph-02][INFO  ] installing Ceph on ceph-02
[ceph-02][INFO  ] Running command: sudo yum clean all
[ceph-02][DEBUG ] Loaded plugins: fastestmirror
[ceph-02][DEBUG ] Cleaning repos: base centos-ceph-nautilus centos-nfs-ganesha28 epel extras
[ceph-02][DEBUG ]               : updates
[ceph-02][DEBUG ] Cleaning up everything
[ceph-02][DEBUG ] Cleaning up list of fastest mirrors
[ceph-02][INFO  ] Running command: sudo yum -y install ceph ceph-radosgw
[ceph-02][DEBUG ] Loaded plugins: fastestmirror
[ceph-02][DEBUG ] Determining fastest mirrors
[ceph-02][DEBUG ]  * base: mirrors.163.com
[ceph-02][DEBUG ]  * centos-ceph-nautilus: mirrors.cn99.com
[ceph-02][DEBUG ]  * centos-nfs-ganesha28: mirrors.cn99.com
[ceph-02][DEBUG ]  * extras: mirrors.cn99.com
[ceph-02][DEBUG ]  * updates: mirrors.163.com
[ceph-02][DEBUG ] Package 2:ceph-14.2.1-0.el7.x86_64 already installed and latest version
[ceph-02][DEBUG ] Package 2:ceph-radosgw-14.2.1-0.el7.x86_64 already installed and latest version
[ceph-02][DEBUG ] Nothing to do
[ceph-02][INFO  ] Running command: sudo ceph --version
[ceph-02][DEBUG ] ceph version 14.2.1 (d555a9489eb35f84f2e1ef49b77e19da9d113972) nautilus (stable)
[ceph_deploy.install][DEBUG ] Detecting platform for host ceph-03 ...
ceph@ceph-03's password:
[ceph-03][DEBUG ] connection detected need for sudo
ceph@ceph-03's password:
[ceph-03][DEBUG ] connected to host: ceph-03
[ceph-03][DEBUG ] detect platform information from remote host
[ceph-03][DEBUG ] detect machine type
[ceph_deploy.install][INFO  ] Distro info: CentOS Linux 7.7.1908 Core
[ceph-03][INFO  ] installing Ceph on ceph-03
[ceph-03][INFO  ] Running command: sudo yum clean all
[ceph-03][DEBUG ] Loaded plugins: fastestmirror
[ceph-03][DEBUG ] Cleaning repos: base centos-ceph-nautilus centos-nfs-ganesha28 epel extras
[ceph-03][DEBUG ]               : updates
[ceph-03][DEBUG ] Cleaning up everything
[ceph-03][DEBUG ] Cleaning up list of fastest mirrors
[ceph-03][INFO  ] Running command: sudo yum -y install ceph ceph-radosgw
[ceph-03][DEBUG ] Loaded plugins: fastestmirror
[ceph-03][DEBUG ] Determining fastest mirrors
[ceph-03][DEBUG ]  * base: mirrors.163.com
[ceph-03][DEBUG ]  * centos-ceph-nautilus: mirrors.cn99.com
[ceph-03][DEBUG ]  * centos-nfs-ganesha28: mirrors.cn99.com
[ceph-03][DEBUG ]  * extras: mirrors.cn99.com
[ceph-03][DEBUG ]  * updates: mirrors.163.com
[ceph-03][DEBUG ] Package 2:ceph-14.2.1-0.el7.x86_64 already installed and latest version
[ceph-03][DEBUG ] Package 2:ceph-radosgw-14.2.1-0.el7.x86_64 already installed and latest version
[ceph-03][DEBUG ] Nothing to do
[ceph-03][INFO  ] Running command: sudo ceph --version
[ceph-03][DEBUG ] ceph version 14.2.1 (d555a9489eb35f84f2e1ef49b77e19da9d113972) nautilus (stable)
# 本质就是执行 yum -y install ceph ceph-radosgw

# mon
$ ceph-deploy mon create-initial
[ceph_deploy.conf][DEBUG ] found configuration file at: /home/ceph/.cephdeploy.conf
[ceph_deploy.cli][INFO  ] Invoked (2.0.1): /bin/ceph-deploy mon create-initial
[ceph_deploy.cli][INFO  ] ceph-deploy options:
[ceph_deploy.cli][INFO  ]  username                      : None
[ceph_deploy.cli][INFO  ]  verbose                       : False
[ceph_deploy.cli][INFO  ]  overwrite_conf                : False
[ceph_deploy.cli][INFO  ]  subcommand                    : create-initial
[ceph_deploy.cli][INFO  ]  quiet                         : False
[ceph_deploy.cli][INFO  ]  cd_conf                       : <ceph_deploy.conf.cephdeploy.Conf instance at 0x7f8e73fd1e18>
[ceph_deploy.cli][INFO  ]  cluster                       : ceph
[ceph_deploy.cli][INFO  ]  func                          : <function mon at 0x7f8e74025410>
[ceph_deploy.cli][INFO  ]  ceph_conf                     : None
[ceph_deploy.cli][INFO  ]  default_release               : False
[ceph_deploy.cli][INFO  ]  keyrings                      : None
[ceph_deploy.mon][DEBUG ] Deploying mon, cluster ceph hosts ceph-01
[ceph_deploy.mon][DEBUG ] detecting platform for host ceph-01 ...
[ceph-01][DEBUG ] connection detected need for sudo
[ceph-01][DEBUG ] connected to host: ceph-01
[ceph-01][DEBUG ] detect platform information from remote host
[ceph-01][DEBUG ] detect machine type
[ceph-01][DEBUG ] find the location of an executable
[ceph_deploy.mon][INFO  ] distro info: CentOS Linux 7.7.1908 Core
[ceph-01][DEBUG ] determining if provided host has same hostname in remote
[ceph-01][DEBUG ] get remote short hostname
[ceph-01][DEBUG ] deploying mon to ceph-01
[ceph-01][DEBUG ] get remote short hostname
[ceph-01][DEBUG ] remote hostname: ceph-01
[ceph-01][DEBUG ] write cluster configuration to /etc/ceph/{cluster}.conf
[ceph-01][DEBUG ] create the mon path if it does not exist
[ceph-01][DEBUG ] checking for done path: /var/lib/ceph/mon/ceph-ceph-01/done
[ceph-01][DEBUG ] done path does not exist: /var/lib/ceph/mon/ceph-ceph-01/done
[ceph-01][INFO  ] creating keyring file: /var/lib/ceph/tmp/ceph-ceph-01.mon.keyring
[ceph-01][DEBUG ] create the monitor keyring file
[ceph-01][INFO  ] Running command: sudo ceph-mon --cluster ceph --mkfs -i ceph-01 --keyring /var/lib/ceph/tmp/ceph-ceph-01.mon.keyring --setuser 1000 --setgroup 1000
[ceph-01][INFO  ] unlinking keyring file /var/lib/ceph/tmp/ceph-ceph-01.mon.keyring
[ceph-01][DEBUG ] create a done file to avoid re-doing the mon deployment
[ceph-01][DEBUG ] create the init path if it does not exist
[ceph-01][INFO  ] Running command: sudo systemctl enable ceph.target
[ceph-01][INFO  ] Running command: sudo systemctl enable ceph-mon@ceph-01
[ceph-01][WARNIN] Created symlink from /etc/systemd/system/ceph-mon.target.wants/ceph-mon@ceph-01.service to /usr/lib/systemd/system/ceph-mon@.service.
[ceph-01][INFO  ] Running command: sudo systemctl start ceph-mon@ceph-01
[ceph-01][INFO  ] Running command: sudo ceph --cluster=ceph --admin-daemon /var/run/ceph/ceph-mon.ceph-01.asok mon_status
[ceph-01][DEBUG ] ********************************************************************************
[ceph-01][DEBUG ] status for monitor: mon.ceph-01
[ceph-01][DEBUG ] {
[ceph-01][DEBUG ]   "election_epoch": 3,
[ceph-01][DEBUG ]   "extra_probe_peers": [],
[ceph-01][DEBUG ]   "feature_map": {
[ceph-01][DEBUG ]     "mon": [
[ceph-01][DEBUG ]       {
[ceph-01][DEBUG ]         "features": "0x3ffddff8ffacffff",
[ceph-01][DEBUG ]         "num": 1,
[ceph-01][DEBUG ]         "release": "luminous"
[ceph-01][DEBUG ]       }
[ceph-01][DEBUG ]     ]
[ceph-01][DEBUG ]   },
[ceph-01][DEBUG ]   "features": {
[ceph-01][DEBUG ]     "quorum_con": "4611087854031667199",
[ceph-01][DEBUG ]     "quorum_mon": [
[ceph-01][DEBUG ]       "kraken",
[ceph-01][DEBUG ]       "luminous",
[ceph-01][DEBUG ]       "mimic",
[ceph-01][DEBUG ]       "osdmap-prune",
[ceph-01][DEBUG ]       "nautilus"
[ceph-01][DEBUG ]     ],
[ceph-01][DEBUG ]     "required_con": "2449958747315912708",
[ceph-01][DEBUG ]     "required_mon": [
[ceph-01][DEBUG ]       "kraken",
[ceph-01][DEBUG ]       "luminous",
[ceph-01][DEBUG ]       "mimic",
[ceph-01][DEBUG ]       "osdmap-prune",
[ceph-01][DEBUG ]       "nautilus"
[ceph-01][DEBUG ]     ]
[ceph-01][DEBUG ]   },
[ceph-01][DEBUG ]   "monmap": {
[ceph-01][DEBUG ]     "created": "2019-11-14 17:25:47.586563",
[ceph-01][DEBUG ]     "epoch": 1,
[ceph-01][DEBUG ]     "features": {
[ceph-01][DEBUG ]       "optional": [],
[ceph-01][DEBUG ]       "persistent": [
[ceph-01][DEBUG ]         "kraken",
[ceph-01][DEBUG ]         "luminous",
[ceph-01][DEBUG ]         "mimic",
[ceph-01][DEBUG ]         "osdmap-prune",
[ceph-01][DEBUG ]         "nautilus"
[ceph-01][DEBUG ]       ]
[ceph-01][DEBUG ]     },
[ceph-01][DEBUG ]     "fsid": "879b266e-2134-49f0-b097-c0468c45597b",
[ceph-01][DEBUG ]     "min_mon_release": 14,
[ceph-01][DEBUG ]     "min_mon_release_name": "nautilus",
[ceph-01][DEBUG ]     "modified": "2019-11-14 17:25:47.586563",
[ceph-01][DEBUG ]     "mons": [
[ceph-01][DEBUG ]       {
[ceph-01][DEBUG ]         "addr": "10.0.10.21:6789/0",
[ceph-01][DEBUG ]         "name": "ceph-01",
[ceph-01][DEBUG ]         "public_addr": "10.0.10.21:6789/0",
[ceph-01][DEBUG ]         "public_addrs": {
[ceph-01][DEBUG ]           "addrvec": [
[ceph-01][DEBUG ]             {
[ceph-01][DEBUG ]               "addr": "10.0.10.21:3300",
[ceph-01][DEBUG ]               "nonce": 0,
[ceph-01][DEBUG ]               "type": "v2"
[ceph-01][DEBUG ]             },
[ceph-01][DEBUG ]             {
[ceph-01][DEBUG ]               "addr": "10.0.10.21:6789",
[ceph-01][DEBUG ]               "nonce": 0,
[ceph-01][DEBUG ]               "type": "v1"
[ceph-01][DEBUG ]             }
[ceph-01][DEBUG ]           ]
[ceph-01][DEBUG ]         },
[ceph-01][DEBUG ]         "rank": 0
[ceph-01][DEBUG ]       }
[ceph-01][DEBUG ]     ]
[ceph-01][DEBUG ]   },
[ceph-01][DEBUG ]   "name": "ceph-01",
[ceph-01][DEBUG ]   "outside_quorum": [],
[ceph-01][DEBUG ]   "quorum": [
[ceph-01][DEBUG ]     0
[ceph-01][DEBUG ]   ],
[ceph-01][DEBUG ]   "quorum_age": 2,
[ceph-01][DEBUG ]   "rank": 0,
[ceph-01][DEBUG ]   "state": "leader",
[ceph-01][DEBUG ]   "sync_provider": []
[ceph-01][DEBUG ] }
[ceph-01][DEBUG ] ********************************************************************************
[ceph-01][INFO  ] monitor: mon.ceph-01 is running
[ceph-01][INFO  ] Running command: sudo ceph --cluster=ceph --admin-daemon /var/run/ceph/ceph-mon.ceph-01.asok mon_status
[ceph_deploy.mon][INFO  ] processing monitor mon.ceph-01
[ceph-01][DEBUG ] connection detected need for sudo
[ceph-01][DEBUG ] connected to host: ceph-01
[ceph-01][DEBUG ] detect platform information from remote host
[ceph-01][DEBUG ] detect machine type
[ceph-01][DEBUG ] find the location of an executable
[ceph-01][INFO  ] Running command: sudo ceph --cluster=ceph --admin-daemon /var/run/ceph/ceph-mon.ceph-01.asok mon_status
[ceph_deploy.mon][INFO  ] mon.ceph-01 monitor has reached quorum!
[ceph_deploy.mon][INFO  ] all initial monitors are running and have formed quorum
[ceph_deploy.mon][INFO  ] Running gatherkeys...
[ceph_deploy.gatherkeys][INFO  ] Storing keys in temp directory /tmp/tmpDaYi2Z
[ceph-01][DEBUG ] connection detected need for sudo
[ceph-01][DEBUG ] connected to host: ceph-01
[ceph-01][DEBUG ] detect platform information from remote host
[ceph-01][DEBUG ] detect machine type
[ceph-01][DEBUG ] get remote short hostname
[ceph-01][DEBUG ] fetch remote file
[ceph-01][INFO  ] Running command: sudo /usr/bin/ceph --connect-timeout=25 --cluster=ceph --admin-daemon=/var/run/ceph/ceph-mon.ceph-01.asok mon_status
[ceph-01][INFO  ] Running command: sudo /usr/bin/ceph --connect-timeout=25 --cluster=ceph --name mon. --keyring=/var/lib/ceph/mon/ceph-ceph-01/keyring auth get client.admin
[ceph-01][INFO  ] Running command: sudo /usr/bin/ceph --connect-timeout=25 --cluster=ceph --name mon. --keyring=/var/lib/ceph/mon/ceph-ceph-01/keyring auth get client.bootstrap-mds
[ceph-01][INFO  ] Running command: sudo /usr/bin/ceph --connect-timeout=25 --cluster=ceph --name mon. --keyring=/var/lib/ceph/mon/ceph-ceph-01/keyring auth get client.bootstrap-mgr
[ceph-01][INFO  ] Running command: sudo /usr/bin/ceph --connect-timeout=25 --cluster=ceph --name mon. --keyring=/var/lib/ceph/mon/ceph-ceph-01/keyring auth get client.bootstrap-osd
[ceph-01][INFO  ] Running command: sudo /usr/bin/ceph --connect-timeout=25 --cluster=ceph --name mon. --keyring=/var/lib/ceph/mon/ceph-ceph-01/keyring auth get client.bootstrap-rgw
[ceph_deploy.gatherkeys][INFO  ] Storing ceph.client.admin.keyring
[ceph_deploy.gatherkeys][INFO  ] Storing ceph.bootstrap-mds.keyring
[ceph_deploy.gatherkeys][INFO  ] Storing ceph.bootstrap-mgr.keyring
[ceph_deploy.gatherkeys][INFO  ] keyring 'ceph.mon.keyring' already exists
[ceph_deploy.gatherkeys][INFO  ] Storing ceph.bootstrap-osd.keyring
[ceph_deploy.gatherkeys][INFO  ] Storing ceph.bootstrap-rgw.keyring
[ceph_deploy.gatherkeys][INFO  ] Destroy temp directory /tmp/tmpDaYi2Z
$ ll
total 56
-rw------- 1 ceph ceph   113 Nov 14 17:25 ceph.bootstrap-mds.keyring
-rw------- 1 ceph ceph   113 Nov 14 17:25 ceph.bootstrap-mgr.keyring
-rw------- 1 ceph ceph   113 Nov 14 17:25 ceph.bootstrap-osd.keyring
-rw------- 1 ceph ceph   113 Nov 14 17:25 ceph.bootstrap-rgw.keyring
-rw------- 1 ceph ceph   151 Nov 14 17:25 ceph.client.admin.keyring
-rw-rw-r-- 1 ceph ceph   256 Nov 14 17:09 ceph.conf
-rw-rw-r-- 1 ceph ceph 25743 Nov 14 17:25 ceph-deploy-ceph.log
-rw------- 1 ceph ceph    73 Nov 14 17:09 ceph.mon.keyring
$

# Push configuration and client.admin key to a remote host.
$ ceph-deploy admin  ceph-01 ceph-02 ceph-03
[ceph_deploy.conf][DEBUG ] found configuration file at: /home/ceph/.cephdeploy.conf
[ceph_deploy.cli][INFO  ] Invoked (2.0.1): /bin/ceph-deploy admin ceph-01 ceph-02 ceph-03
[ceph_deploy.cli][INFO  ] ceph-deploy options:
[ceph_deploy.cli][INFO  ]  username                      : None
[ceph_deploy.cli][INFO  ]  verbose                       : False
[ceph_deploy.cli][INFO  ]  overwrite_conf                : False
[ceph_deploy.cli][INFO  ]  quiet                         : False
[ceph_deploy.cli][INFO  ]  cd_conf                       : <ceph_deploy.conf.cephdeploy.Conf instance at 0x7fcf6db952d8>
[ceph_deploy.cli][INFO  ]  cluster                       : ceph
[ceph_deploy.cli][INFO  ]  client                        : ['ceph-01', 'ceph-02', 'ceph-03']
[ceph_deploy.cli][INFO  ]  func                          : <function admin at 0x7fcf6e6a4230>
[ceph_deploy.cli][INFO  ]  ceph_conf                     : None
[ceph_deploy.cli][INFO  ]  default_release               : False
[ceph_deploy.admin][DEBUG ] Pushing admin keys and conf to ceph-01
[ceph-01][DEBUG ] connection detected need for sudo
[ceph-01][DEBUG ] connected to host: ceph-01
[ceph-01][DEBUG ] detect platform information from remote host
[ceph-01][DEBUG ] detect machine type
[ceph-01][DEBUG ] write cluster configuration to /etc/ceph/{cluster}.conf
[ceph_deploy.admin][DEBUG ] Pushing admin keys and conf to ceph-02
ceph@ceph-02's password:
[ceph-02][DEBUG ] connection detected need for sudo
ceph@ceph-02's password:
[ceph-02][DEBUG ] connected to host: ceph-02
[ceph-02][DEBUG ] detect platform information from remote host
[ceph-02][DEBUG ] detect machine type
[ceph-02][DEBUG ] write cluster configuration to /etc/ceph/{cluster}.conf
[ceph_deploy.admin][DEBUG ] Pushing admin keys and conf to ceph-03
ceph@ceph-03's password:
[ceph-03][DEBUG ] connection detected need for sudo
ceph@ceph-03's password:
[ceph-03][DEBUG ] connected to host: ceph-03
[ceph-03][DEBUG ] detect platform information from remote host
[ceph-03][DEBUG ] detect machine type
[ceph-03][DEBUG ] write cluster configuration to /etc/ceph/{cluster}.conf
$

$ ll /etc/ceph/
total 12
-rw------- 1 root root 151 Nov 14 17:29 ceph.client.admin.keyring
-rw-r--r-- 1 root root 256 Nov 14 17:29 ceph.conf
-rw-r--r-- 1 root root  92 Jun 20 20:59 rbdmap
-rw------- 1 root root   0 Nov 14 17:25 tmpRUnqDf
$

# ceph-01 ceph-02 ceph-03
$ su - root
$ setfacl -m u:ceph:r /etc/ceph/ceph.client.admin.keyring
$ ll /etc/ceph/
total 12
-rw-r-----+ 1 root root 151 Nov 14 17:29 ceph.client.admin.keyring
-rw-r--r--  1 root root 256 Nov 14 17:29 ceph.conf
-rw-r--r--  1 root root  92 Jun 20 20:59 rbdmap
-rw-------  1 root root   0 Nov 14 17:25 tmpRUnqDf

$ ceph -s
  cluster:
    id:     879b266e-2134-49f0-b097-c0468c45597b
    health: HEALTH_OK

  services:
    mon: 1 daemons, quorum ceph-01 (age 9m)
    mgr: no daemons active
    osd: 0 osds: 0 up, 0 in

  data:
    pools:   0 pools, 0 pgs
    objects: 0 objects, 0 B
    usage:   0 B used, 0 B / 0 B avail
    pgs:

$

# ceph-01 管理节点
$ su - ceph
$ cd /home/ceph/ceph-cluster
$ ceph-deploy mgr create ceph-01
[ceph_deploy.conf][DEBUG ] found configuration file at: /home/ceph/.cephdeploy.conf
[ceph_deploy.cli][INFO  ] Invoked (2.0.1): /bin/ceph-deploy mgr create ceph-01
[ceph_deploy.cli][INFO  ] ceph-deploy options:
[ceph_deploy.cli][INFO  ]  username                      : None
[ceph_deploy.cli][INFO  ]  verbose                       : False
[ceph_deploy.cli][INFO  ]  mgr                           : [('ceph-01', 'ceph-01')]
[ceph_deploy.cli][INFO  ]  overwrite_conf                : False
[ceph_deploy.cli][INFO  ]  subcommand                    : create
[ceph_deploy.cli][INFO  ]  quiet                         : False
[ceph_deploy.cli][INFO  ]  cd_conf                       : <ceph_deploy.conf.cephdeploy.Conf instance at 0x7fbc95f8d6c8>
[ceph_deploy.cli][INFO  ]  cluster                       : ceph
[ceph_deploy.cli][INFO  ]  func                          : <function mgr at 0x7fbc967f2140>
[ceph_deploy.cli][INFO  ]  ceph_conf                     : None
[ceph_deploy.cli][INFO  ]  default_release               : False
[ceph_deploy.mgr][DEBUG ] Deploying mgr, cluster ceph hosts ceph-01:ceph-01
[ceph-01][DEBUG ] connection detected need for sudo
[ceph-01][DEBUG ] connected to host: ceph-01
[ceph-01][DEBUG ] detect platform information from remote host
[ceph-01][DEBUG ] detect machine type
[ceph_deploy.mgr][INFO  ] Distro info: CentOS Linux 7.7.1908 Core
[ceph_deploy.mgr][DEBUG ] remote host will use systemd
[ceph_deploy.mgr][DEBUG ] deploying mgr bootstrap to ceph-01
[ceph-01][DEBUG ] write cluster configuration to /etc/ceph/{cluster}.conf
[ceph-01][WARNIN] mgr keyring does not exist yet, creating one
[ceph-01][DEBUG ] create a keyring file
[ceph-01][DEBUG ] create path recursively if it doesn't exist
[ceph-01][INFO  ] Running command: sudo ceph --cluster ceph --name client.bootstrap-mgr --keyring /var/lib/ceph/bootstrap-mgr/ceph.keyring auth get-or-create mgr.ceph-01 mon allow profile mgr osd allow * mds allow * -o /var/lib/ceph/mgr/ceph-ceph-01/keyring
[ceph-01][INFO  ] Running command: sudo systemctl enable ceph-mgr@ceph-01
[ceph-01][WARNIN] Created symlink from /etc/systemd/system/ceph-mgr.target.wants/ceph-mgr@ceph-01.service to /usr/lib/systemd/system/ceph-mgr@.service.
[ceph-01][INFO  ] Running command: sudo systemctl start ceph-mgr@ceph-01
[ceph-01][INFO  ] Running command: sudo systemctl enable ceph.target
$
$ ceph -s
  cluster:
    id:     879b266e-2134-49f0-b097-c0468c45597b
    health: HEALTH_OK

  services:
    mon: 1 daemons, quorum ceph-01 (age 11m)
    mgr: ceph-01(active, since 23s)
    osd: 0 osds: 0 up, 0 in

  data:
    pools:   0 pools, 0 pgs
    objects: 0 objects, 0 B
    usage:   0 B used, 0 B / 0 B avail
    pgs:

$

$ ceph-deploy disk list ceph-01 ceph-02 ceph-03
[ceph_deploy.conf][DEBUG ] found configuration file at: /home/ceph/.cephdeploy.conf
[ceph_deploy.cli][INFO  ] Invoked (2.0.1): /bin/ceph-deploy disk list ceph-01 ceph-02 ceph-03
[ceph_deploy.cli][INFO  ] ceph-deploy options:
[ceph_deploy.cli][INFO  ]  username                      : None
[ceph_deploy.cli][INFO  ]  verbose                       : False
[ceph_deploy.cli][INFO  ]  debug                         : False
[ceph_deploy.cli][INFO  ]  overwrite_conf                : False
[ceph_deploy.cli][INFO  ]  subcommand                    : list
[ceph_deploy.cli][INFO  ]  quiet                         : False
[ceph_deploy.cli][INFO  ]  cd_conf                       : <ceph_deploy.conf.cephdeploy.Conf instance at 0x7f0857d71200>
[ceph_deploy.cli][INFO  ]  cluster                       : ceph
[ceph_deploy.cli][INFO  ]  host                          : ['ceph-01', 'ceph-02', 'ceph-03']
[ceph_deploy.cli][INFO  ]  func                          : <function disk at 0x7f0857dab938>
[ceph_deploy.cli][INFO  ]  ceph_conf                     : None
[ceph_deploy.cli][INFO  ]  default_release               : False
[ceph-01][DEBUG ] connection detected need for sudo
[ceph-01][DEBUG ] connected to host: ceph-01
[ceph-01][DEBUG ] detect platform information from remote host
[ceph-01][DEBUG ] detect machine type
[ceph-01][DEBUG ] find the location of an executable
[ceph-01][INFO  ] Running command: sudo fdisk -l
[ceph-01][INFO  ] Disk /dev/sda: 64.4 GB, 64424509440 bytes, 125829120 sectors
[ceph-01][INFO  ] Disk /dev/sdb: 107.4 GB, 107374182400 bytes, 209715200 sectors
[ceph-01][INFO  ] Disk /dev/mapper/cl-root: 39.8 GB, 39766196224 bytes, 77668352 sectors
[ceph-01][INFO  ] Disk /dev/mapper/cl-swap: 4160 MB, 4160749568 bytes, 8126464 sectors
[ceph-01][INFO  ] Disk /dev/mapper/cl-home: 19.4 GB, 19415433216 bytes, 37920768 sectors
ceph@ceph-02's password:
[ceph-02][DEBUG ] connection detected need for sudo
ceph@ceph-02's password:
[ceph-02][DEBUG ] connected to host: ceph-02
[ceph-02][DEBUG ] detect platform information from remote host
[ceph-02][DEBUG ] detect machine type
[ceph-02][DEBUG ] find the location of an executable
[ceph-02][INFO  ] Running command: sudo fdisk -l
[ceph-02][INFO  ] Disk /dev/sdb: 107.4 GB, 107374182400 bytes, 209715200 sectors
[ceph-02][INFO  ] Disk /dev/sda: 64.4 GB, 64424509440 bytes, 125829120 sectors
[ceph-02][INFO  ] Disk /dev/mapper/cl-root: 39.8 GB, 39766196224 bytes, 77668352 sectors
[ceph-02][INFO  ] Disk /dev/mapper/cl-swap: 4160 MB, 4160749568 bytes, 8126464 sectors
[ceph-02][INFO  ] Disk /dev/mapper/cl-home: 19.4 GB, 19415433216 bytes, 37920768 sectors
ceph@ceph-03's password:
[ceph-03][DEBUG ] connection detected need for sudo
ceph@ceph-03's password:
[ceph-03][DEBUG ] connected to host: ceph-03
[ceph-03][DEBUG ] detect platform information from remote host
[ceph-03][DEBUG ] detect machine type
[ceph-03][DEBUG ] find the location of an executable
[ceph-03][INFO  ] Running command: sudo fdisk -l
[ceph-03][INFO  ] Disk /dev/sda: 64.4 GB, 64424509440 bytes, 125829120 sectors
[ceph-03][INFO  ] Disk /dev/sdb: 107.4 GB, 107374182400 bytes, 209715200 sectors
[ceph-03][INFO  ] Disk /dev/mapper/cl-root: 39.8 GB, 39766196224 bytes, 77668352 sectors
[ceph-03][INFO  ] Disk /dev/mapper/cl-swap: 4160 MB, 4160749568 bytes, 8126464 sectors
[ceph-03][INFO  ] Disk /dev/mapper/cl-home: 19.4 GB, 19415433216 bytes, 37920768 sectors
$

$ ceph-deploy disk zap ceph-01 /dev/sdb
[ceph_deploy.conf][DEBUG ] found configuration file at: /home/ceph/.cephdeploy.conf
[ceph_deploy.cli][INFO  ] Invoked (2.0.1): /bin/ceph-deploy disk zap ceph-01 /dev/sdb
[ceph_deploy.cli][INFO  ] ceph-deploy options:
[ceph_deploy.cli][INFO  ]  username                      : None
[ceph_deploy.cli][INFO  ]  verbose                       : False
[ceph_deploy.cli][INFO  ]  debug                         : False
[ceph_deploy.cli][INFO  ]  overwrite_conf                : False
[ceph_deploy.cli][INFO  ]  subcommand                    : zap
[ceph_deploy.cli][INFO  ]  quiet                         : False
[ceph_deploy.cli][INFO  ]  cd_conf                       : <ceph_deploy.conf.cephdeploy.Conf instance at 0x7ff1c2ac6200>
[ceph_deploy.cli][INFO  ]  cluster                       : ceph
[ceph_deploy.cli][INFO  ]  host                          : ceph-01
[ceph_deploy.cli][INFO  ]  func                          : <function disk at 0x7ff1c2b00938>
[ceph_deploy.cli][INFO  ]  ceph_conf                     : None
[ceph_deploy.cli][INFO  ]  default_release               : False
[ceph_deploy.cli][INFO  ]  disk                          : ['/dev/sdb']
[ceph_deploy.osd][DEBUG ] zapping /dev/sdb on ceph-01
[ceph-01][DEBUG ] connection detected need for sudo
[ceph-01][DEBUG ] connected to host: ceph-01
[ceph-01][DEBUG ] detect platform information from remote host
[ceph-01][DEBUG ] detect machine type
[ceph-01][DEBUG ] find the location of an executable
[ceph_deploy.osd][INFO  ] Distro info: CentOS Linux 7.7.1908 Core
[ceph-01][DEBUG ] zeroing last few blocks of device
[ceph-01][DEBUG ] find the location of an executable
[ceph-01][INFO  ] Running command: sudo /usr/sbin/ceph-volume lvm zap /dev/sdb
[ceph-01][DEBUG ] --> Zapping: /dev/sdb
[ceph-01][DEBUG ] --> --destroy was not specified, but zapping a whole device will remove the partition table
[ceph-01][DEBUG ] Running command: /usr/sbin/wipefs --all /dev/sdb
[ceph-01][DEBUG ] Running command: /bin/dd if=/dev/zero of=/dev/sdb bs=1M count=10
[ceph-01][DEBUG ]  stderr: 10+0 records in
[ceph-01][DEBUG ] 10+0 records out
[ceph-01][DEBUG ] 10485760 bytes (10 MB) copied
[ceph-01][DEBUG ]  stderr: , 0.00714173 s, 1.5 GB/s
[ceph-01][DEBUG ] --> Zapping successful for: <Raw Device: /dev/sdb>
$
$ ceph-deploy disk zap ceph-02 /dev/sdb
$ ceph-deploy disk zap ceph-03 /dev/sdb

$ ceph-deploy osd create ceph-01 --data /dev/sdb
[ceph_deploy.conf][DEBUG ] found configuration file at: /home/ceph/.cephdeploy.conf
[ceph_deploy.cli][INFO  ] Invoked (2.0.1): /bin/ceph-deploy osd create ceph-01 --data /dev/sdb
[ceph_deploy.cli][INFO  ] ceph-deploy options:
[ceph_deploy.cli][INFO  ]  verbose                       : False
[ceph_deploy.cli][INFO  ]  bluestore                     : None
[ceph_deploy.cli][INFO  ]  cd_conf                       : <ceph_deploy.conf.cephdeploy.Conf instance at 0x7f8a937ea320>
[ceph_deploy.cli][INFO  ]  cluster                       : ceph
[ceph_deploy.cli][INFO  ]  fs_type                       : xfs
[ceph_deploy.cli][INFO  ]  block_wal                     : None
[ceph_deploy.cli][INFO  ]  default_release               : False
[ceph_deploy.cli][INFO  ]  username                      : None
[ceph_deploy.cli][INFO  ]  journal                       : None
[ceph_deploy.cli][INFO  ]  subcommand                    : create
[ceph_deploy.cli][INFO  ]  host                          : ceph-01
[ceph_deploy.cli][INFO  ]  filestore                     : None
[ceph_deploy.cli][INFO  ]  func                          : <function osd at 0x7f8a9381e8c0>
[ceph_deploy.cli][INFO  ]  ceph_conf                     : None
[ceph_deploy.cli][INFO  ]  zap_disk                      : False
[ceph_deploy.cli][INFO  ]  data                          : /dev/sdb
[ceph_deploy.cli][INFO  ]  block_db                      : None
[ceph_deploy.cli][INFO  ]  dmcrypt                       : False
[ceph_deploy.cli][INFO  ]  overwrite_conf                : False
[ceph_deploy.cli][INFO  ]  dmcrypt_key_dir               : /etc/ceph/dmcrypt-keys
[ceph_deploy.cli][INFO  ]  quiet                         : False
[ceph_deploy.cli][INFO  ]  debug                         : False
[ceph_deploy.osd][DEBUG ] Creating OSD on cluster ceph with data device /dev/sdb
[ceph-01][DEBUG ] connection detected need for sudo
[ceph-01][DEBUG ] connected to host: ceph-01
[ceph-01][DEBUG ] detect platform information from remote host
[ceph-01][DEBUG ] detect machine type
[ceph-01][DEBUG ] find the location of an executable
[ceph_deploy.osd][INFO  ] Distro info: CentOS Linux 7.7.1908 Core
[ceph_deploy.osd][DEBUG ] Deploying osd to ceph-01
[ceph-01][DEBUG ] write cluster configuration to /etc/ceph/{cluster}.conf
[ceph-01][WARNIN] osd keyring does not exist yet, creating one
[ceph-01][DEBUG ] create a keyring file
[ceph-01][DEBUG ] find the location of an executable
[ceph-01][INFO  ] Running command: sudo /usr/sbin/ceph-volume --cluster ceph lvm create --bluestore --data /dev/sdb
[ceph-01][DEBUG ] Running command: /bin/ceph-authtool --gen-print-key
[ceph-01][DEBUG ] Running command: /bin/ceph --cluster ceph --name client.bootstrap-osd --keyring /var/lib/ceph/bootstrap-osd/ceph.keyring -i - osd new 93789138-8bcb-42b4-a592-772c82c92a25
[ceph-01][DEBUG ] Running command: /usr/sbin/vgcreate -s 1G --force --yes ceph-39befc06-e08b-4ee6-a6f8-4158ba190aee /dev/sdb
[ceph-01][DEBUG ]  stdout: Physical volume "/dev/sdb" successfully created.
[ceph-01][DEBUG ]  stdout: Volume group "ceph-39befc06-e08b-4ee6-a6f8-4158ba190aee" successfully created
[ceph-01][DEBUG ] Running command: /usr/sbin/lvcreate --yes -l 100%FREE -n osd-block-93789138-8bcb-42b4-a592-772c82c92a25 ceph-39befc06-e08b-4ee6-a6f8-4158ba190aee
[ceph-01][DEBUG ]  stdout: Logical volume "osd-block-93789138-8bcb-42b4-a592-772c82c92a25" created.
[ceph-01][DEBUG ] Running command: /bin/ceph-authtool --gen-print-key
[ceph-01][DEBUG ] Running command: /bin/mount -t tmpfs tmpfs /var/lib/ceph/osd/ceph-0
[ceph-01][DEBUG ] Running command: /usr/sbin/restorecon /var/lib/ceph/osd/ceph-0
[ceph-01][DEBUG ] Running command: /bin/chown -h ceph:ceph /dev/ceph-39befc06-e08b-4ee6-a6f8-4158ba190aee/osd-block-93789138-8bcb-42b4-a592-772c82c92a25
[ceph-01][DEBUG ] Running command: /bin/chown -R ceph:ceph /dev/dm-3
[ceph-01][DEBUG ] Running command: /bin/ln -s /dev/ceph-39befc06-e08b-4ee6-a6f8-4158ba190aee/osd-block-93789138-8bcb-42b4-a592-772c82c92a25 /var/lib/ceph/osd/ceph-0/block
[ceph-01][DEBUG ] Running command: /bin/ceph --cluster ceph --name client.bootstrap-osd --keyring /var/lib/ceph/bootstrap-osd/ceph.keyring mon getmap -o /var/lib/ceph/osd/ceph-0/activate.monmap
[ceph-01][DEBUG ]  stderr: 2019-11-14 17:44:55.907 7f0dba102700 -1 auth: unable to find a keyring on /etc/ceph/ceph.client.bootstrap-osd.keyring,/etc/ceph/ceph.keyring,/etc/ceph/keyring,/etc/ceph/keyring.bin,: (2) No such file or directory
[ceph-01][DEBUG ] 2019-11-14 17:44:55.907 7f0dba102700 -1 AuthRegistry(0x7f0db4063bc8) no keyring found at /etc/ceph/ceph.client.bootstrap-osd.keyring,/etc/ceph/ceph.keyring,/etc/ceph/keyring,/etc/ceph/keyring.bin,, disabling cephx
[ceph-01][DEBUG ]  stderr: got monmap epoch 1
[ceph-01][DEBUG ] Running command: /bin/ceph-authtool /var/lib/ceph/osd/ceph-0/keyring --create-keyring --name osd.0 --add-key AQAWIs1dywkPEBAAtZ33nxTem+5y5VY2bPyGiQ==
[ceph-01][DEBUG ]  stdout: creating /var/lib/ceph/osd/ceph-0/keyring
[ceph-01][DEBUG ] added entity osd.0 auth(key=AQAWIs1dywkPEBAAtZ33nxTem+5y5VY2bPyGiQ==)
[ceph-01][DEBUG ] Running command: /bin/chown -R ceph:ceph /var/lib/ceph/osd/ceph-0/keyring
[ceph-01][DEBUG ] Running command: /bin/chown -R ceph:ceph /var/lib/ceph/osd/ceph-0/
[ceph-01][DEBUG ] Running command: /bin/ceph-osd --cluster ceph --osd-objectstore bluestore --mkfs -i 0 --monmap /var/lib/ceph/osd/ceph-0/activate.monmap --keyfile - --osd-data /var/lib/ceph/osd/ceph-0/ --osd-uuid 93789138-8bcb-42b4-a592-772c82c92a25 --setuser ceph --setgroup ceph
[ceph-01][DEBUG ] --> ceph-volume lvm prepare successful for: /dev/sdb
[ceph-01][DEBUG ] Running command: /bin/chown -R ceph:ceph /var/lib/ceph/osd/ceph-0
[ceph-01][DEBUG ] Running command: /bin/ceph-bluestore-tool --cluster=ceph prime-osd-dir --dev /dev/ceph-39befc06-e08b-4ee6-a6f8-4158ba190aee/osd-block-93789138-8bcb-42b4-a592-772c82c92a25 --path /var/lib/ceph/osd/ceph-0 --no-mon-config
[ceph-01][DEBUG ] Running command: /bin/ln -snf /dev/ceph-39befc06-e08b-4ee6-a6f8-4158ba190aee/osd-block-93789138-8bcb-42b4-a592-772c82c92a25 /var/lib/ceph/osd/ceph-0/block
[ceph-01][DEBUG ] Running command: /bin/chown -h ceph:ceph /var/lib/ceph/osd/ceph-0/block
[ceph-01][DEBUG ] Running command: /bin/chown -R ceph:ceph /dev/dm-3
[ceph-01][DEBUG ] Running command: /bin/chown -R ceph:ceph /var/lib/ceph/osd/ceph-0
[ceph-01][DEBUG ] Running command: /bin/systemctl enable ceph-volume@lvm-0-93789138-8bcb-42b4-a592-772c82c92a25
[ceph-01][DEBUG ]  stderr: Created symlink from /etc/systemd/system/multi-user.target.wants/ceph-volume@lvm-0-93789138-8bcb-42b4-a592-772c82c92a25.service to /usr/lib/systemd/system/ceph-volume@.service.
[ceph-01][DEBUG ] Running command: /bin/systemctl enable --runtime ceph-osd@0
[ceph-01][DEBUG ]  stderr: Created symlink from /run/systemd/system/ceph-osd.target.wants/ceph-osd@0.service to /usr/lib/systemd/system/ceph-osd@.service.
[ceph-01][DEBUG ] Running command: /bin/systemctl start ceph-osd@0
[ceph-01][DEBUG ] --> ceph-volume lvm activate successful for osd ID: 0
[ceph-01][DEBUG ] --> ceph-volume lvm create successful for: /dev/sdb
[ceph-01][INFO  ] checking OSD status...
[ceph-01][DEBUG ] find the location of an executable
[ceph-01][INFO  ] Running command: sudo /bin/ceph --cluster=ceph osd stat --format=json
[ceph_deploy.osd][DEBUG ] Host ceph-01 is now ready for osd use.

$ ceph-deploy osd create ceph-02 --data /dev/sdb
$ ceph-deploy osd create ceph-03 --data /dev/sdb


$ ceph -s
  cluster:
    id:     879b266e-2134-49f0-b097-c0468c45597b
    health: HEALTH_OK

  services:
    mon: 1 daemons, quorum ceph-01 (age 22m)
    mgr: ceph-01(active, since 10m)
    osd: 3 osds: 3 up (since 110s), 3 in (since 110s)

  data:
    pools:   0 pools, 0 pgs
    objects: 0 objects, 0 B
    usage:   3.0 GiB used, 294 GiB / 297 GiB avail
    pgs:

$ ceph osd tree
ID CLASS WEIGHT  TYPE NAME        STATUS REWEIGHT PRI-AFF
-1       0.29008 root default
-3       0.09669     host ceph-01
 0   hdd 0.09669         osd.0        up  1.00000 1.00000
-5       0.09669     host ceph-02
 1   hdd 0.09669         osd.1        up  1.00000 1.00000
-7       0.09669     host ceph-03
 2   hdd 0.09669         osd.2        up  1.00000 1.00000
$

$ ceph-deploy mon add ceph-02
$ ceph-deploy mon add ceph-02
$ ceph -s
  cluster:
    id:     879b266e-2134-49f0-b097-c0468c45597b
    health: HEALTH_OK

  services:
    mon: 3 daemons, quorum ceph-01,ceph-02,ceph-03 (age 1.00253s)
    mgr: ceph-01(active, since 13m)
    osd: 3 osds: 3 up (since 4m), 3 in (since 4m)

  data:
    pools:   0 pools, 0 pgs
    objects: 0 objects, 0 B
    usage:   3.0 GiB used, 294 GiB / 297 GiB avail
    pgs:

$

$ ceph quorum_status --format json-pretty


$ ceph-deploy mgr create ceph-02
$ ceph-deploy mgr create ceph-03
$ ceph -s
  cluster:
    id:     879b266e-2134-49f0-b097-c0468c45597b
    health: HEALTH_OK

  services:
    mon: 3 daemons, quorum ceph-01,ceph-02,ceph-03 (age 2m)
    mgr: ceph-01(active, since 16m), standbys: ceph-02, ceph-03
    osd: 3 osds: 3 up (since 7m), 3 in (since 7m)

  data:
    pools:   0 pools, 0 pgs
    objects: 0 objects, 0 B
    usage:   3.0 GiB used, 294 GiB / 297 GiB avail
    pgs:

$


$ ceph osd pool create mypool 64 64
$ ceph osd pool create mypool1 64 64
$ ceph osd pool ls
mypool
mypool1
$ rados lspools
mypool
mypool1
$ ceph osd pool stats mypool
pool mypool id 1
  nothing is going on

$

$ rados put issue /etc/issue -p mypool
$ rados ls -p mypool
issue
$ rados get issue my_issue -p mypool
$ ll
-rw-r--r-- 1 ceph ceph     23 Nov 14 18:00 my_issue
$ ceph osd map mypool issue
osdmap e19 pool 'mypool' (1) object 'issue' -> pg 1.651f88da (1.1a) -> up ([1,0,2], p1) acting ([1,0,2], p1)
$ rados rm issue -p mypool
$ rados ls -p mypool





$ rbd create ceph-client-dce-worker-05-rbd1 --size 10240 -p mypool
$ rbd ls -p mypool
ceph-client-dce-worker-05-rbd1
$ rbd --image ceph-client-dce-worker-05-rbd1 info  -p mypool
rbd image 'ceph-client-dce-worker-05-rbd1':
	size 10 GiB in 2560 objects
	order 22 (4 MiB objects)
	snapshot_count: 0
	id: 11e2a619273e
	block_name_prefix: rbd_data.11e2a619273e
	format: 2
	features: layering, exclusive-lock, object-map, fast-diff, deep-flatten
	op_features:
	flags:
	create_timestamp: Thu Nov 14 18:26:35 2019
	access_timestamp: Thu Nov 14 18:26:35 2019
	modify_timestamp: Thu Nov 14 18:26:35 2019
$

$ uname -r
3.10.0-514.el7.x86_64
$ modprobe rbd



$ rbd map ceph-client-dce-worker-05-rbd1 -p mypool
rbd: sysfs write failed
RBD image feature set mismatch. Try disabling features unsupported by the kernel with "rbd feature disable".
In some cases useful info is found in syslog - try "dmesg | tail".
rbd: map failed: (6) No such device or address

$ rbd --image ceph-client-dce-worker-05-rbd1 info  -p mypool
rbd image 'ceph-client-dce-worker-05-rbd1':
	size 10 GiB in 2560 objects
	order 22 (4 MiB objects)
	snapshot_count: 0
	id: 11e2a619273e
	block_name_prefix: rbd_data.11e2a619273e
	format: 2
	features: layering, exclusive-lock, object-map, fast-diff, deep-flatten
	op_features:
	flags:
	create_timestamp: Thu Nov 14 18:26:35 2019
	access_timestamp: Thu Nov 14 18:26:35 2019
	modify_timestamp: Thu Nov 14 18:26:35 2019

$ rbd feature disable -p mypool ceph-client-dce-worker-05-rbd1 exclusive-lock object-map fast-diff deep-flatten

$ rbd --image ceph-client-dce-worker-05-rbd1 info  -p mypool
rbd image 'ceph-client-dce-worker-05-rbd1':
	size 10 GiB in 2560 objects
	order 22 (4 MiB objects)
	snapshot_count: 0
	id: 11e2a619273e
	block_name_prefix: rbd_data.11e2a619273e
	format: 2
	features: layering
	op_features:
	flags:
	create_timestamp: Thu Nov 14 18:26:35 2019
	access_timestamp: Thu Nov 14 18:26:35 2019
	modify_timestamp: Thu Nov 14 18:26:35 2019

$ rbd map ceph-client-dce-worker-05-rbd1 -p mypool
/dev/rbd0

$ rbd device list
id pool   namespace image                          snap device
0  mypool           ceph-client-dce-worker-05-rbd1 -    /dev/rbd0

$ rbd showmapped
id pool   namespace image                          snap device
0  mypool           ceph-client-dce-worker-05-rbd1 -    /dev/rbd0
$


$ fdisk -l /dev/rbd0

磁盘 /dev/rbd0：10.7 GB, 10737418240 字节，20971520 个扇区
Units = 扇区 of 1 * 512 = 512 bytes
扇区大小(逻辑/物理)：512 字节 / 512 字节
I/O 大小(最小/最佳)：4194304 字节 / 4194304 字节

$ mkfs.xfs /dev/rbd0
meta-data=/dev/rbd0              isize=512    agcount=17, agsize=162816 blks
         =                       sectsz=512   attr=2, projid32bit=1
         =                       crc=1        finobt=0, sparse=0
data     =                       bsize=4096   blocks=2621440, imaxpct=25
         =                       sunit=1024   swidth=1024 blks
naming   =version 2              bsize=4096   ascii-ci=0 ftype=1
log      =internal log           bsize=4096   blocks=2560, version=2
         =                       sectsz=512   sunit=8 blks, lazy-count=1
realtime =none                   extsz=4096   blocks=0, rtextents=0


$ mkdir -p /mnt/ceph-vol1
$ mount /dev/rbd0 /mnt/ceph-vol1
$ pwd
/mnt/ceph-vol1
$ echo 'qwe' > /mnt/ceph-vol1/file1
$ cat /mnt/ceph-vol1/file1
qwe
$ dd if=/dev/zero of=/mnt/ceph-vol1/file2 count=3 bs=1M
记录了3+0 的读入
记录了3+0 的写出
3145728字节(3.1 MB)已复制，0.00408281 秒，770 MB/秒
$ ll
总用量 3076
-rw-r--r-- 1 root root       4 11月 14 19:15 file1
-rw-r--r-- 1 root root 3145728 11月 14 19:16 file2




[root@ceph-01 ceph]# ceph -s
  cluster:
    id:     879b266e-2134-49f0-b097-c0468c45597b
    health: HEALTH_WARN
            application not enabled on 1 pool(s)

  services:
    mon: 3 daemons, quorum ceph-01,ceph-02,ceph-03 (age 21h)
    mgr: ceph-01(active, since 21h), standbys: ceph-02, ceph-03
    osd: 3 osds: 3 up (since 21h), 3 in (since 21h)

  data:
    pools:   2 pools, 128 pgs
    objects: 25 objects, 17 MiB
    usage:   3.1 GiB used, 294 GiB / 297 GiB avail
    pgs:     128 active+clean

[root@ceph-01 ceph]#
[root@ceph-01 ceph]# ceph osd pool ls
mypool
mypool1
[root@ceph-01 ceph]#
[root@ceph-01 ceph]# ceph health detail
HEALTH_WARN application not enabled on 1 pool(s)
POOL_APP_NOT_ENABLED application not enabled on 1 pool(s)
    application not enabled on pool 'mypool'
    use 'ceph osd pool application enable <pool-name> <app-name>', where <app-name> is 'cephfs', 'rbd', 'rgw', or freeform for custom applications.
[root@ceph-01 ceph]#
[root@ceph-01 ceph]# ceph osd pool application enable mypool rbd
enabled application 'rbd' on pool 'mypool'
[root@ceph-01 ceph]# ceph -s
  cluster:
    id:     879b266e-2134-49f0-b097-c0468c45597b
    health: HEALTH_OK

  services:
    mon: 3 daemons, quorum ceph-01,ceph-02,ceph-03 (age 21h)
    mgr: ceph-01(active, since 21h), standbys: ceph-02, ceph-03
    osd: 3 osds: 3 up (since 21h), 3 in (since 21h)

  data:
    pools:   2 pools, 128 pgs
    objects: 25 objects, 17 MiB
    usage:   3.1 GiB used, 294 GiB / 297 GiB avail
    pgs:     128 active+clean

[root@ceph-01 ceph]#



ceph-deploy mds create ceph-01
ceph-deploy mds create ceph-03
[ceph@ceph-01 ceph-cluster]$ ceph-deploy mds create ceph-02
[ceph_deploy.conf][DEBUG ] found configuration file at: /home/ceph/.cephdeploy.conf
[ceph_deploy.cli][INFO  ] Invoked (2.0.1): /bin/ceph-deploy mds create ceph-02
[ceph_deploy.cli][INFO  ] ceph-deploy options:
[ceph_deploy.cli][INFO  ]  username                      : None
[ceph_deploy.cli][INFO  ]  verbose                       : False
[ceph_deploy.cli][INFO  ]  overwrite_conf                : False
[ceph_deploy.cli][INFO  ]  subcommand                    : create
[ceph_deploy.cli][INFO  ]  quiet                         : False
[ceph_deploy.cli][INFO  ]  cd_conf                       : <ceph_deploy.conf.cephdeploy.Conf instance at 0x7fdc7a88f290>
[ceph_deploy.cli][INFO  ]  cluster                       : ceph
[ceph_deploy.cli][INFO  ]  func                          : <function mds at 0x7fdc7b17eed8>
[ceph_deploy.cli][INFO  ]  ceph_conf                     : None
[ceph_deploy.cli][INFO  ]  mds                           : [('ceph-02', 'ceph-02')]
[ceph_deploy.cli][INFO  ]  default_release               : False
[ceph_deploy.mds][DEBUG ] Deploying mds, cluster ceph hosts ceph-02:ceph-02
ceph@ceph-02's password:
[ceph-02][DEBUG ] connection detected need for sudo
ceph@ceph-02's password:
[ceph-02][DEBUG ] connected to host: ceph-02
[ceph-02][DEBUG ] detect platform information from remote host
[ceph-02][DEBUG ] detect machine type
[ceph_deploy.mds][INFO  ] Distro info: CentOS Linux 7.7.1908 Core
[ceph_deploy.mds][DEBUG ] remote host will use systemd
[ceph_deploy.mds][DEBUG ] deploying mds bootstrap to ceph-02
[ceph-02][DEBUG ] write cluster configuration to /etc/ceph/{cluster}.conf
[ceph-02][WARNIN] mds keyring does not exist yet, creating one
[ceph-02][DEBUG ] create a keyring file
[ceph-02][DEBUG ] create path if it doesn't exist
[ceph-02][INFO  ] Running command: sudo ceph --cluster ceph --name client.bootstrap-mds --keyring /var/lib/ceph/bootstrap-mds/ceph.keyring auth get-or-create mds.ceph-02 osd allow rwx mds allow mon allow profile mds -o /var/lib/ceph/mds/ceph-ceph-02/keyring
[ceph-02][INFO  ] Running command: sudo systemctl enable ceph-mds@ceph-02
[ceph-02][WARNIN] Created symlink from /etc/systemd/system/ceph-mds.target.wants/ceph-mds@ceph-02.service to /usr/lib/systemd/system/ceph-mds@.service.
[ceph-02][INFO  ] Running command: sudo systemctl start ceph-mds@ceph-02
[ceph-02][INFO  ] Running command: sudo systemctl enable ceph.target
[ceph@ceph-01 ceph-cluster]$


[ceph@ceph-01 ceph]$ ceph osd pool create cephfs_data 32 32
pool 'cephfs_data' created
[ceph@ceph-01 ceph]$ ceph osd pool create cephfs_metadata 32 32
pool 'cephfs_metadata' created
[ceph@ceph-01 ceph]$
[ceph@ceph-01 ceph]$ ceph osd pool ls
mypool
mypool1
cephfs_data
cephfs_metadata
[ceph@ceph-01 ceph]$
[ceph@ceph-01 ceph]$ ceph fs new mycephfs cephfs_metadata cephfs_data
new fs with metadata pool 4 and data pool 3
[ceph@ceph-01 ceph]$
[ceph@ceph-01 ceph]$ ceph fs ls
name: mycephfs, metadata pool: cephfs_metadata, data pools: [cephfs_data ]
[ceph@ceph-01 ceph]$


$ ceph-deploy rgw create ceph-01
$ ceph-deploy rgw create ceph-02
$ ceph-deploy rgw create ceph-03

管理节点操作 创建 S3 用户

[ceph@ceph-01 ceph-cluster]$ radosgw-admin user create --uid=daocloud --display-name="daocloud" --email=daocloud@example.com
{
    "user_id": "daocloud",
    "display_name": "daocloud",
    "email": "daocloud@example.com",
    "suspended": 0,
    "max_buckets": 1000,
    "subusers": [],
    "keys": [
        {
            "user": "daocloud",
            "access_key": "U7B35ZNAONZ1P574W4RB",
            "secret_key": "eDaW0aH4z0AaNbtwER73pn7h6jxR3YsBb4VvYQFp"
        }
    ],
    "swift_keys": [],
    "caps": [],
    "op_mask": "read, write, delete",
    "default_placement": "",
    "default_storage_class": "",
    "placement_tags": [],
    "bucket_quota": {
        "enabled": false,
        "check_on_raw": false,
        "max_size": -1,
        "max_size_kb": 0,
        "max_objects": -1
    },
    "user_quota": {
        "enabled": false,
        "check_on_raw": false,
        "max_size": -1,
        "max_size_kb": 0,
        "max_objects": -1
    },
    "temp_url_keys": [],
    "type": "rgw",
    "mfa_ids": []
}

[ceph@ceph-01 ceph-cluster]$

创建 Swift 子用户 (必须先创建S3用户才能创建Swift用户)
[ceph@ceph-01 ceph-cluster]$ radosgw-admin subuser create --uid=daocloud --subuser=daocloud:swift --access=full
{
    "user_id": "daocloud",
    "display_name": "daocloud",
    "email": "daocloud@example.com",
    "suspended": 0,
    "max_buckets": 1000,
    "subusers": [
        {
            "id": "daocloud:swift",
            "permissions": "full-control"
        }
    ],
    "keys": [
        {
            "user": "daocloud",
            "access_key": "U7B35ZNAONZ1P574W4RB",
            "secret_key": "eDaW0aH4z0AaNbtwER73pn7h6jxR3YsBb4VvYQFp"
        }
    ],
    "swift_keys": [
        {
            "user": "daocloud:swift",
            "secret_key": "e2NHT2xL8lW10BQzgaII30VxWC77KyW0m1KYWMNB"
        }
    ],
    "caps": [],
    "op_mask": "read, write, delete",
    "default_placement": "",
    "default_storage_class": "",
    "placement_tags": [],
    "bucket_quota": {
        "enabled": false,
        "check_on_raw": false,
        "max_size": -1,
        "max_size_kb": 0,
        "max_objects": -1
    },
    "user_quota": {
        "enabled": false,
        "check_on_raw": false,
        "max_size": -1,
        "max_size_kb": 0,
        "max_objects": -1
    },
    "temp_url_keys": [],
    "type": "rgw",
    "mfa_ids": []
}

[ceph@ceph-01 ceph-cluster]$

获取用户信息
[ceph@ceph-01 ceph-cluster]$ radosgw-admin user info --uid=daocloud
{
    "user_id": "daocloud",
    "display_name": "daocloud",
    "email": "daocloud@example.com",
    "suspended": 0,
    "max_buckets": 1000,
    "subusers": [
        {
            "id": "daocloud:swift",
            "permissions": "full-control"
        }
    ],
    "keys": [
        {
            "user": "daocloud",
            "access_key": "U7B35ZNAONZ1P574W4RB",
            "secret_key": "eDaW0aH4z0AaNbtwER73pn7h6jxR3YsBb4VvYQFp"
        }
    ],
    "swift_keys": [
        {
            "user": "daocloud:swift",
            "secret_key": "e2NHT2xL8lW10BQzgaII30VxWC77KyW0m1KYWMNB"
        }
    ],
    "caps": [],
    "op_mask": "read, write, delete",
    "default_placement": "",
    "default_storage_class": "",
    "placement_tags": [],
    "bucket_quota": {
        "enabled": false,
        "check_on_raw": false,
        "max_size": -1,
        "max_size_kb": 0,
        "max_objects": -1
    },
    "user_quota": {
        "enabled": false,
        "check_on_raw": false,
        "max_size": -1,
        "max_size_kb": 0,
        "max_objects": -1
    },
    "temp_url_keys": [],
    "type": "rgw",
    "mfa_ids": []
}

[ceph@ceph-01 ceph-cluster]$

新建 secret key
[ceph@ceph-01 ceph-cluster]$ radosgw-admin key create --subuser=daocloud:swift --key-type=swift --gen-secret
{
    "user_id": "daocloud",
    "display_name": "daocloud",
    "email": "daocloud@example.com",
    "suspended": 0,
    "max_buckets": 1000,
    "subusers": [
        {
            "id": "daocloud:swift",
            "permissions": "full-control"
        }
    ],
    "keys": [
        {
            "user": "daocloud",
            "access_key": "U7B35ZNAONZ1P574W4RB",
            "secret_key": "eDaW0aH4z0AaNbtwER73pn7h6jxR3YsBb4VvYQFp"
        }
    ],
    "swift_keys": [
        {
            "user": "daocloud:swift",
            "secret_key": "6MWmaoROz263JM75C1VyKjjx66MnB150ohOOBmnU"
        }
    ],
    "caps": [],
    "op_mask": "read, write, delete",
    "default_placement": "",
    "default_storage_class": "",
    "placement_tags": [],
    "bucket_quota": {
        "enabled": false,
        "check_on_raw": false,
        "max_size": -1,
        "max_size_kb": 0,
        "max_objects": -1
    },
    "user_quota": {
        "enabled": false,
        "check_on_raw": false,
        "max_size": -1,
        "max_size_kb": 0,
        "max_objects": -1
    },
    "temp_url_keys": [],
    "type": "rgw",
    "mfa_ids": []
}

[ceph@ceph-01 ceph-cluster]$

yum install s3cmd
[root@dce-worker-05 ~]# s3cmd --configure

Enter new values or accept defaults in brackets with Enter.
Refer to user manual for detailed description of all options.

Access key and Secret key are your identifiers for Amazon S3. Leave them empty for using the env variables.
Access Key: U7B35ZNAONZ1P574W4RB
Secret Key: eDaW0aH4z0AaNbtwER73pn7h6jxR3YsBb4VvYQFp
Default Region [US]: US

Use "s3.amazonaws.com" for S3 Endpoint and not modify it to the target Amazon S3.
S3 Endpoint [s3.amazonaws.com]: ceph-01:7480

Use "%(bucket)s.s3.amazonaws.com" to the target Amazon S3. "%(bucket)s" and "%(location)s" vars can be used
if the target S3 system supports dns based buckets.
DNS-style bucket+hostname:port template for accessing a bucket [%(bucket)s.s3.amazonaws.com]: %(bucket)s.ceph-01:7480

Encryption password is used to protect your files from reading
by unauthorized persons while in transfer to S3
Encryption password: ceph!@#$%^
Path to GPG program [/usr/bin/gpg]: /usr/bin/gpg

When using secure HTTPS protocol all communication with Amazon S3
servers is protected from 3rd party eavesdropping. This method is
slower than plain HTTP, and can only be proxied with Python 2.7 or newer
Use HTTPS protocol [Yes]: False

On some networks all internet access must go through a HTTP proxy.
Try setting it here if you can't connect to S3 directly
HTTP Proxy server name:

New settings:
  Access Key: U7B35ZNAONZ1P574W4RB
  Secret Key: eDaW0aH4z0AaNbtwER73pn7h6jxR3YsBb4VvYQFp
  Default Region: CN
  S3 Endpoint: ceph-01:7480
  DNS-style bucket+hostname:port template for accessing a bucket: %(bucket)s.ceph-01:7480
  Encryption password: ceph!@#$%^
  Path to GPG program: /usr/bin/gpg
  Use HTTPS protocol: False
  HTTP Proxy server name:
  HTTP Proxy server port: 0

Test access with supplied credentials? [Y/n] Y
Please wait, attempting to list all buckets...
Success. Your access key and secret key worked fine :-)

Now verifying that encryption works...
Success. Encryption and decryption worked fine :-)

Save settings? [y/N] y
Configuration saved to '/root/.s3cfg'
[root@dce-worker-05 ~]#

[root@dce-worker-05 ~]# cat .s3cfg
[default]
access_key = U7B35ZNAONZ1P574W4RB
access_token =
add_encoding_exts =
add_headers =
bucket_location = US
ca_certs_file =
cache_file =
check_ssl_certificate = True
check_ssl_hostname = True
cloudfront_host = cloudfront.amazonaws.com
content_disposition =
content_type =
default_mime_type = binary/octet-stream
delay_updates = False
delete_after = False
delete_after_fetch = False
delete_removed = False
dry_run = False
enable_multipart = True
encrypt = False
expiry_date =
expiry_days =
expiry_prefix =
follow_symlinks = False
force = False
get_continue = False
gpg_command = /usr/bin/gpg
gpg_decrypt = %(gpg_command)s -d --verbose --no-use-agent --batch --yes --passphrase-fd %(passphrase_fd)s -o %(output_file)s %(input_file)s
gpg_encrypt = %(gpg_command)s -c --verbose --no-use-agent --batch --yes --passphrase-fd %(passphrase_fd)s -o %(output_file)s %(input_file)s
gpg_passphrase = ceph!@#$%^
guess_mime_type = True
host_base = ceph-01:7480
host_bucket = %(bucket)s.ceph-01:7480
human_readable_sizes = False
invalidate_default_index_on_cf = False
invalidate_default_index_root_on_cf = True
invalidate_on_cf = False
kms_key =
limit = -1
limitrate = 0
list_md5 = False
log_target_prefix =
long_listing = False
max_delete = -1
mime_type =
multipart_chunk_size_mb = 15
multipart_max_chunks = 10000
preserve_attrs = True
progress_meter = True
proxy_host =
proxy_port = 0
put_continue = False
recursive = False
recv_chunk = 65536
reduced_redundancy = False
requester_pays = False
restore_days = 1
restore_priority = Standard
secret_key = eDaW0aH4z0AaNbtwER73pn7h6jxR3YsBb4VvYQFp
send_chunk = 65536
server_side_encryption = False
signature_v2 = False
signurl_use_https = False
simpledb_host = sdb.amazonaws.com
skip_existing = False
socket_timeout = 300
stats = False
stop_on_error = False
storage_class =
throttle_max = 100
upload_id =
urlencoding_mode = normal
use_http_expect = False
use_https = False
use_mime_magic = True
verbosity = WARNING
website_endpoint = http://%(bucket)s.s3-website-%(location)s.amazonaws.com/
website_error =
website_index = index.html
[root@dce-worker-05 ~]#





[root@dce-worker-05 ~]# s3cmd -d mb s3://first-buckets
ERROR: [Errno -2] Name or service not known
ERROR: Connection Error: Error resolving a server hostname.
Please check the servers address specified in 'host_base', 'host_bucket', 'cloudfront_host', 'website_endpoint'
[root@dce-worker-05 ~]#


修改 .s3cfg 文件中的 'host_base', 'host_bucket', 'cloudfront_host', 'website_endpoint'




[root@dce-worker-05 ~]# curl http://ceph-01:7480
<?xml version="1.0" encoding="UTF-8"?>
<ListAllMyBucketsResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
	<Owner>
		<ID>anonymous</ID>
		<DisplayName>
		</DisplayName>
	</Owner>
	<Buckets>
	</Buckets>
</ListAllMyBucketsResult>
[root@dce-worker-05 ~]#

pip install python-swiftclient
[root@dce-worker-05 ~]# swift -A http://ceph-01:7480/auth/v1.0 -U daocloud:swift -K '6MWmaoROz263JM75C1VyKjjx66MnB150ohOOBmnU' stat -v
                                 StorageURL: http://ceph-01:7480/swift/v1
                                 Auth Token: AUTH_rgwtk0e00000064616f636c6f75643a737769667445292ebcd1f6dc516ac8cf5d82660304a4bcd28113c7e5b7f551f2044025698c7b3bb3f9
                                    Account: v1
                                 Containers: 0
                                    Objects: 0
                                      Bytes: 0
Objects in policy "default-placement-bytes": 0
  Bytes in policy "default-placement-bytes": 0
   Containers in policy "default-placement": 0
      Objects in policy "default-placement": 0
        Bytes in policy "default-placement": 0
                     X-Openstack-Request-Id: tx000000000000000000003-005dce76ea-1578-default
                                 Connection: Keep-Alive
                X-Account-Bytes-Used-Actual: 0
                                 X-Trans-Id: tx000000000000000000003-005dce76ea-1578-default
                                X-Timestamp: 1573811946.07101
                               Content-Type: text/plain; charset=utf-8
                              Accept-Ranges: bytes
[root@dce-worker-05 ~]#

[root@dce-worker-05 ~]# swift -A http://ceph-01:7480/auth/v1.0 -U daocloud:swift -K '6MWmaoROz263JM75C1VyKjjx66MnB150ohOOBmnU' post example-bucket
[root@dce-worker-05 ~]# swift -A http://ceph-01:7480/auth/v1.0 -U daocloud:swift -K '6MWmaoROz263JM75C1VyKjjx66MnB150ohOOBmnU' list
example-bucket
[root@dce-worker-05 ~]#
[root@dce-worker-05 ~]# echo "Hello World" > ceph-swiftuser1-container1-object-1.txt
[root@dce-worker-05 ~]# swift -A http://ceph-01:7480/auth/v1.0 -U daocloud:swift -K '6MWmaoROz263JM75C1VyKjjx66MnB150ohOOBmnU' upload example-bucket ceph-swiftuser1-container1-object-1.txt
ceph-swiftuser1-container1-object-1.txt
[root@dce-worker-05 ~]#
[root@dce-worker-05 ~]# swift -A http://ceph-01:7480/auth/v1.0 -U daocloud:swift -K '6MWmaoROz263JM75C1VyKjjx66MnB150ohOOBmnU' list example-bucket
ceph-swiftuser1-container1-object-1.txt
[root@dce-worker-05 ~]#
[root@dce-worker-05 ~]# rm -rf  ceph-swiftuser1-container1-object-1.txt
[root@dce-worker-05 ~]#
[root@dce-worker-05 ~]# swift -A http://ceph-01:7480/auth/v1.0 -U daocloud:swift -K '6MWmaoROz263JM75C1VyKjjx66MnB150ohOOBmnU' download example-bucket ceph-swiftuser1-container1-object-1.txt
ceph-swiftuser1-container1-object-1.txt [auth 0.018s, headers 0.022s, total 0.022s, 0.003 MB/s]
[root@dce-worker-05 ~]#
[root@dce-worker-05 ~]# cat ceph-swiftuser1-container1-object-1.txt
Hello World
[root@dce-worker-05 ~]#

```



























### 配置 SSH 免密登录
```bash
ceph-01

ssh-keygen
/root/.ssh/ceph
/root/.ssh/ceph.pub

ssh-copy-id -i /root/.ssh/ceph root@ceph-02
ssh-copy-id -i /root/.ssh/ceph root@ceph-03

ssh -i /root/.ssh/ceph root@ceph-02
ssh -i /root/.ssh/ceph root@ceph-03

useradd -d /home/ceph -m ceph
passwd ceph
ceph!@#$%^

echo "ceph ALL = (root) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/ceph
chmod 0440 /etc/sudoers.d/ceph

mkdir -p /root/cluster 
rm -f /root/cluster/*

mkdir -p /osd1 & rm -rf /osd1/*
chown ceph:ceph /osd1

mkdir -p /var/run/ceph/
chown ceph:ceph /var/run/ceph/

```

### osd 磁盘准备
```bash
ceph-01
ceph-02
ceph-03

fdisk -l /dev/sdb

磁盘 /dev/sdb：107.4 GB, 107374182400 字节，209715200 个扇区
Units = 扇区 of 1 * 512 = 512 bytes
扇区大小(逻辑/物理)：512 字节 / 512 字节
I/O 大小(最小/最佳)：512 字节 / 512 字节

```

### 安装相关文件

```bash
ceph-01


$ su - root
$ yum install centos-release-ceph-nautilus.noarch
$ yum makecache fast



# 添加 ceph yum 源
yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm

cat << EOM > /etc/yum.repos.d/ceph.repo
[ceph-noarch]
name=Ceph noarch packages
baseurl=https://download.ceph.com/rpm-nautilus/el7/noarch
enabled=1
gpgcheck=1
type=rpm-md
gpgkey=https://download.ceph.com/keys/release.asc
EOM

yum install centos-release-ceph-nautilus.noarch
centos-release-ceph-nautilus.noarch
centos-release-nfs-ganesha28.noarch
centos-release-storage-common.noarch

rpm -ql centos-release-ceph-nautilus.noarch
/etc/yum.repos.d/CentOS-Ceph-Nautilus.repo

rpm -ql centos-release-nfs-ganesha28.noarch
/etc/yum.repos.d/CentOS-NFS-Ganesha-28.repo

rpm -ql centos-release-storage-common.noarch
/etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-SIG-Storage
/etc/yum.repos.d/CentOS-Storage-common.repo


yum update

yum install ceph-deploy
rpm -ql ceph-deploy
/usr/bin/ceph-deploy

yum install ceph
已安装:
ceph.x86_64 2:14.2.1-0.el7

作为依赖被安装:
ceph-base.x86_64 2:14.2.1-0.el7
ceph-common.x86_64 2:14.2.1-0.el7
ceph-mds.x86_64 2:14.2.1-0.el7
ceph-mgr.x86_64 2:14.2.1-0.el7
ceph-mon.x86_64 2:14.2.1-0.el7
ceph-osd.x86_64 2:14.2.1-0.el7
ceph-selinux.x86_64 2:14.2.1-0.el7
cryptsetup.x86_64 0:2.0.3-5.el7
fuse-libs.x86_64 0:2.9.2-11.el7
leveldb.x86_64 0:1.12.0-11.el7
libbabeltrace.x86_64 0:1.2.4-3.1.el7
libcephfs2.x86_64 2:14.2.1-0.el7
libconfig.x86_64 0:1.4.9-5.el7
libibverbs.x86_64 0:22.1-3.el7
liboath.x86_64 0:2.6.2-1.el7
librabbitmq.x86_64 0:0.8.0-2.el7
librados2.x86_64 2:14.2.1-0.el7
libradosstriper1.x86_64 2:14.2.1-0.el7
librbd1.x86_64 2:14.2.1-0.el7
librdmacm.x86_64 0:22.1-3.el7
librgw2.x86_64 2:14.2.1-0.el7
libstoragemgmt.x86_64 0:1.7.3-3.el7
libstoragemgmt-python.noarch 0:1.7.3-3.el7
libstoragemgmt-python-clibs.x86_64 0:1.7.3-3.el7
lttng-ust.x86_64 0:2.10.0-1.el7
psmisc.x86_64 0:22.20-16.el7
pyOpenSSL.x86_64 0:0.13.1-4.el7
python-beaker.noarch 0:1.5.4-10.el7
python-ceph-argparse.x86_64 2:14.2.1-0.el7
python-cephfs.x86_64 2:14.2.1-0.el7
python-cffi.x86_64 0:1.6.0-5.el7
python-chardet.noarch 0:2.2.1-3.el7
python-cherrypy.noarch 0:3.2.2-4.el7
python-logutils.noarch 0:0.3.3-3.el7
python-mako.noarch 0:0.8.1-2.el7
python-markupsafe.x86_64 0:0.11-10.el7
python-paste.noarch 0:1.7.5.1-9.20111221hg1498.el7
python-ply.noarch 0:3.4-11.el7
python-pycparser.noarch 0:2.14-1.el7
python-rados.x86_64 2:14.2.1-0.el7
python-rbd.x86_64 2:14.2.1-0.el7
python-requests.noarch 0:2.6.0-7.el7_7
python-rgw.x86_64 2:14.2.1-0.el7
python-simplegeneric.noarch 0:0.8-7.el7
python-tempita.noarch 0:0.5.1-6.el7
python-urllib3.noarch 0:1.10.2-7.el7
python-webtest.noarch 0:1.3.4-6.el7
python-werkzeug.noarch 0:0.9.1-2.el7
python2-bcrypt.x86_64 0:3.1.6-2.el7
python2-pecan.noarch 0:1.3.2-1.el7
python2-prettytable.noarch 0:0.7.2-12.el7
python2-singledispatch.noarch 0:3.4.0.3-4.el7
python2-six.noarch 0:1.12.0-1.el7
python2-webob.noarch 0:1.8.5-1.el7
userspace-rcu.x86_64 0:0.10.0-3.el7
yajl.x86_64 0:2.0.4-4.el7


[root@ceph-01 cluster]# rpm -ql ceph.x86_64
(没有包含文件)
[root@ceph-01 cluster]#

[root@ceph-01 cluster]# rpm -ql ceph-base.x86_64
/etc/logrotate.d/ceph
/etc/sysconfig/ceph
/usr/bin/ceph-crash
/usr/bin/ceph-kvstore-tool
/usr/bin/ceph-run
/usr/bin/crushtool
/usr/bin/monmaptool
/usr/bin/osdmaptool
/usr/lib/ceph
/usr/lib/ceph/ceph_common.sh
/usr/lib/python2.7/site-packages/ceph_volume

/usr/lib/systemd/system-preset/50-ceph.preset
/usr/lib/systemd/system/ceph-crash.service
/usr/lib/systemd/system/ceph.target
/usr/lib64/ceph

/usr/lib64/libos_tp.so
/usr/lib64/libos_tp.so.1
/usr/lib64/libos_tp.so.1.0.0
/usr/lib64/libosd_tp.so
/usr/lib64/libosd_tp.so.1
/usr/lib64/libosd_tp.so.1.0.0
/usr/lib64/rados-classes

/usr/sbin/ceph-create-keys

/var/lib/ceph/bootstrap-mds
/var/lib/ceph/bootstrap-mgr
/var/lib/ceph/bootstrap-osd
/var/lib/ceph/bootstrap-rbd
/var/lib/ceph/bootstrap-rbd-mirror
/var/lib/ceph/bootstrap-rgw
/var/lib/ceph/crash
/var/lib/ceph/crash/posted
/var/lib/ceph/tmp
[root@ceph-01 cluster]#

[root@ceph-01 cluster]# rpm -ql ceph-common.x86_64
/etc/bash_completion.d/ceph
/etc/bash_completion.d/rados
/etc/bash_completion.d/radosgw-admin
/etc/bash_completion.d/rbd
/etc/ceph
/etc/ceph/rbdmap
/usr/bin/ceph
/usr/bin/ceph-authtool
/usr/bin/ceph-conf
/usr/bin/ceph-dencoder
/usr/bin/ceph-post-file
/usr/bin/ceph-rbdnamer
/usr/bin/ceph-syn
/usr/bin/cephfs-data-scan
/usr/bin/cephfs-journal-tool
/usr/bin/cephfs-table-tool
/usr/bin/rados
/usr/bin/radosgw-admin
/usr/bin/rbd
/usr/bin/rbd-replay
/usr/bin/rbd-replay-many
/usr/bin/rbd-replay-prep
/usr/bin/rbdmap

/usr/lib/systemd/system/rbdmap.service
/usr/lib/tmpfiles.d/ceph-common.conf
/usr/lib/udev/rules.d
/usr/lib/udev/rules.d/50-rbd.rules
/usr/sbin/mount.ceph
/usr/share/ceph
/usr/share/ceph/id_rsa_drop.ceph.com
/usr/share/ceph/id_rsa_drop.ceph.com.pub
/usr/share/ceph/known_hosts_drop.ceph.com
/usr/share/doc/ceph

/var/lib/ceph
/var/log/ceph
[root@ceph-01 cluster]#

[root@ceph-01 cluster]# rpm -ql ceph-mds.x86_64
/usr/bin/ceph-mds
/usr/lib/systemd/system/ceph-mds.target
/usr/lib/systemd/system/ceph-mds@.service
/usr/share/man/man8/ceph-mds.8.gz
/var/lib/ceph/mds
[root@ceph-01 cluster]#


[root@ceph-01 cluster]# rpm -ql ceph-mgr.x86_64
/usr/bin/ceph-mgr
/usr/lib/systemd/system/ceph-mgr.target
/usr/lib/systemd/system/ceph-mgr@.service
/usr/share/ceph/mgr
/var/lib/ceph/mgr
[root@ceph-01 cluster]#

[root@ceph-01 cluster]# rpm -ql ceph-mon.x86_64
/usr/bin/ceph-mon
/usr/bin/ceph-monstore-tool
/usr/lib/systemd/system/ceph-mon.target
/usr/lib/systemd/system/ceph-mon@.service
/usr/share/man/man8/ceph-mon.8.gz
/var/lib/ceph/mon
[root@ceph-01 cluster]#


[root@ceph-01 cluster]# rpm -ql ceph-mon.x86_64
/usr/bin/ceph-mon
/usr/bin/ceph-monstore-tool
/usr/lib/systemd/system/ceph-mon.target
/usr/lib/systemd/system/ceph-mon@.service
/usr/share/man/man8/ceph-mon.8.gz
/var/lib/ceph/mon


[root@ceph-01 cluster]# rpm -ql ceph-osd.x86_64
/etc/sudoers.d/ceph-osd-smartctl
/usr/bin/ceph-bluestore-tool
/usr/bin/ceph-clsinfo
/usr/bin/ceph-objectstore-tool
/usr/bin/ceph-osd
/usr/bin/ceph-osdomap-tool
/usr/lib/ceph/ceph-osd-prestart.sh
/usr/lib/sysctl.d/90-ceph-osd.conf
/usr/lib/systemd/system/ceph-osd.target
/usr/lib/systemd/system/ceph-osd@.service
/usr/lib/systemd/system/ceph-volume@.service
/usr/sbin/ceph-volume
/usr/sbin/ceph-volume-systemd
/usr/share/man/man8/ceph-bluestore-tool.8.gz
/usr/share/man/man8/ceph-clsinfo.8.gz
/usr/share/man/man8/ceph-osd.8.gz
/usr/share/man/man8/ceph-volume-systemd.8.gz
/usr/share/man/man8/ceph-volume.8.gz
/var/lib/ceph/osd
[root@ceph-01 cluster]#


[root@ceph-01 cluster]# rpm -ql ceph-selinux.x86_64
/usr/share/man/man8/ceph_selinux.8.gz
/usr/share/selinux/devel/include/contrib/ceph.if
/usr/share/selinux/packages/ceph.pp
[root@ceph-01 cluster]#


[root@ceph-01 cluster]# ceph-deploy new ceph-01
[ceph_deploy.conf][DEBUG ] found configuration file at: /root/.cephdeploy.conf
[ceph_deploy.cli][INFO  ] Invoked (2.0.1): /usr/bin/ceph-deploy new ceph-01
[ceph_deploy.cli][INFO  ] ceph-deploy options:
[ceph_deploy.cli][INFO  ]  username                      : None
[ceph_deploy.cli][INFO  ]  func                          : <function new at 0x7f75a35aade8>
[ceph_deploy.cli][INFO  ]  verbose                       : False
[ceph_deploy.cli][INFO  ]  overwrite_conf                : False
[ceph_deploy.cli][INFO  ]  quiet                         : False
[ceph_deploy.cli][INFO  ]  cd_conf                       : <ceph_deploy.conf.cephdeploy.Conf instance at 0x7f75a2d25518>
[ceph_deploy.cli][INFO  ]  cluster                       : ceph
[ceph_deploy.cli][INFO  ]  ssh_copykey                   : True
[ceph_deploy.cli][INFO  ]  mon                           : ['ceph-01']
[ceph_deploy.cli][INFO  ]  public_network                : None
[ceph_deploy.cli][INFO  ]  ceph_conf                     : None
[ceph_deploy.cli][INFO  ]  cluster_network               : None
[ceph_deploy.cli][INFO  ]  default_release               : False
[ceph_deploy.cli][INFO  ]  fsid                          : None
[ceph_deploy.new][DEBUG ] Creating new cluster named ceph
[ceph_deploy.new][INFO  ] making sure passwordless SSH succeeds
[ceph-01][DEBUG ] connected to host: ceph-01
[ceph-01][DEBUG ] detect platform information from remote host
[ceph-01][DEBUG ] detect machine type
[ceph-01][DEBUG ] find the location of an executable
[ceph-01][INFO  ] Running command: /usr/sbin/ip link show
[ceph-01][INFO  ] Running command: /usr/sbin/ip addr show
[ceph-01][DEBUG ] IP addresses found: [u'10.0.10.21']
[ceph_deploy.new][DEBUG ] Resolving host ceph-01
[ceph_deploy.new][DEBUG ] Monitor ceph-01 at 10.0.10.21
[ceph_deploy.new][DEBUG ] Monitor initial members are ['ceph-01']
[ceph_deploy.new][DEBUG ] Monitor addrs are ['10.0.10.21']
[ceph_deploy.new][DEBUG ] Creating a random mon key...
[ceph_deploy.new][DEBUG ] Writing monitor keyring to ceph.mon.keyring...
[ceph_deploy.new][DEBUG ] Writing initial config to ceph.conf...
[root@ceph-01 cluster]#
[root@ceph-01 cluster]# ll
总用量 12
-rw-r--r-- 1 root root  195 11月 14 10:42 ceph.conf
-rw-r--r-- 1 root root 2934 11月 14 10:42 ceph-deploy-ceph.log
-rw------- 1 root root   73 11月 14 10:42 ceph.mon.keyring
[root@ceph-01 cluster]#


[root@ceph-01 cluster]# cat ceph.conf
[global]
fsid = d6e82b39-5f95-460b-bdea-0a1f17c70f90
mon_initial_members = ceph-01
mon_host = 10.0.10.21
auth_cluster_required = cephx
auth_service_required = cephx
auth_client_required = cephx

[root@ceph-01 cluster]#
[root@ceph-01 cluster]# cat ceph-deploy-ceph.log
[2019-11-14 10:42:33,329][ceph_deploy.conf][DEBUG ] found configuration file at: /root/.cephdeploy.conf
[2019-11-14 10:42:33,330][ceph_deploy.cli][INFO  ] Invoked (2.0.1): /usr/bin/ceph-deploy new ceph-01
[2019-11-14 10:42:33,330][ceph_deploy.cli][INFO  ] ceph-deploy options:
[2019-11-14 10:42:33,330][ceph_deploy.cli][INFO  ]  username                      : None
[2019-11-14 10:42:33,330][ceph_deploy.cli][INFO  ]  func                          : <function new at 0x7f75a35aade8>
[2019-11-14 10:42:33,330][ceph_deploy.cli][INFO  ]  verbose                       : False
[2019-11-14 10:42:33,330][ceph_deploy.cli][INFO  ]  overwrite_conf                : False
[2019-11-14 10:42:33,330][ceph_deploy.cli][INFO  ]  quiet                         : False
[2019-11-14 10:42:33,330][ceph_deploy.cli][INFO  ]  cd_conf                       : <ceph_deploy.conf.cephdeploy.Conf instance at 0x7f75a2d25518>
[2019-11-14 10:42:33,330][ceph_deploy.cli][INFO  ]  cluster                       : ceph
[2019-11-14 10:42:33,331][ceph_deploy.cli][INFO  ]  ssh_copykey                   : True
[2019-11-14 10:42:33,331][ceph_deploy.cli][INFO  ]  mon                           : ['ceph-01']
[2019-11-14 10:42:33,331][ceph_deploy.cli][INFO  ]  public_network                : None
[2019-11-14 10:42:33,331][ceph_deploy.cli][INFO  ]  ceph_conf                     : None
[2019-11-14 10:42:33,331][ceph_deploy.cli][INFO  ]  cluster_network               : None
[2019-11-14 10:42:33,331][ceph_deploy.cli][INFO  ]  default_release               : False
[2019-11-14 10:42:33,332][ceph_deploy.cli][INFO  ]  fsid                          : None
[2019-11-14 10:42:33,332][ceph_deploy.new][DEBUG ] Creating new cluster named ceph
[2019-11-14 10:42:33,332][ceph_deploy.new][INFO  ] making sure passwordless SSH succeeds
[2019-11-14 10:42:33,531][ceph-01][DEBUG ] connected to host: ceph-01
[2019-11-14 10:42:33,532][ceph-01][DEBUG ] detect platform information from remote host
[2019-11-14 10:42:33,563][ceph-01][DEBUG ] detect machine type
[2019-11-14 10:42:33,569][ceph-01][DEBUG ] find the location of an executable
[2019-11-14 10:42:33,571][ceph-01][INFO  ] Running command: /usr/sbin/ip link show
[2019-11-14 10:42:33,595][ceph-01][INFO  ] Running command: /usr/sbin/ip addr show
[2019-11-14 10:42:33,606][ceph-01][DEBUG ] IP addresses found: [u'10.0.10.21']
[2019-11-14 10:42:33,606][ceph_deploy.new][DEBUG ] Resolving host ceph-01
[2019-11-14 10:42:33,627][ceph_deploy.new][DEBUG ] Monitor ceph-01 at 10.0.10.21
[2019-11-14 10:42:33,628][ceph_deploy.new][DEBUG ] Monitor initial members are ['ceph-01']
[2019-11-14 10:42:33,628][ceph_deploy.new][DEBUG ] Monitor addrs are ['10.0.10.21']
[2019-11-14 10:42:33,628][ceph_deploy.new][DEBUG ] Creating a random mon key...
[2019-11-14 10:42:33,628][ceph_deploy.new][DEBUG ] Writing monitor keyring to ceph.mon.keyring...
[2019-11-14 10:42:33,628][ceph_deploy.new][DEBUG ] Writing initial config to ceph.conf...
[root@ceph-01 cluster]#
[root@ceph-01 cluster]# cat ceph.mon.keyring
[mon.]
key = AQAZv8xdAAAAABAAZxvMy7KyWbiELWVu/GGVmw==
caps mon = allow *
[root@ceph-01 cluster]#

[root@ceph-01 cluster]# ls /etc/ceph/
ls: 无法访问/etc/ceph/: 没有那个文件或目录
[root@ceph-01 cluster]#
[root@ceph-01 cluster]# ls /var/run/ceph/
[root@ceph-01 cluster]#



```



