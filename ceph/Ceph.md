## Ceph



### Ceph 架构

![](./ceph_architecture.png)





### 部署 Ceph 集群

#### 集群节点信息

| 编号 |       IP       |   hostname   |                   功能                   |
| :--: | :------------: | :----------: | :--------------------------------------: |
|  1   | 192.168.57.101 |  ceph-node1  |   ceph-deploy，monitor，OSD，RBD，MDS    |
|  2   | 192.168.57.102 |  ceph-node2  |               monitor，OSD               |
|  3   | 192.168.57.103 |  ceph-node3  |               monitor，OSD               |
|  4   | 192.168.57.200 | ceph-client1 |       RADOS 块设备客户端， CephFS        |
|  5   | 192.168.57.110 |   ceph-rgw   | RADOS GW，Amazon S3 客户端，Swift 客户端 |

#### 部署过程

1. 在 ceph-node1 节点上安装 `ceph-deploy` 工具

2. 使用 ceph-deploy 工具创建一个 ceph 集群 。 在 ceph-nodel 上执行下面的命令:

```bash
## Create a directory for ceph
# mkdir /etc/ceph
# cd /etc/ceph
# ceph-deploy new ceph-node1
```

ceph-deploy 工具的 new 命令会部署一个默认名称为 ceph 的新的 ceph 集群；它生成集群配置和keying 文件 。 如果你用 ls 命令查看当前工作目录，会发现生成的 `ceph.conf` 和 `ceph.mon.keyring` 文件 。

3. 用 ceph-deploy 工具将 Ceph 软件的二进制包安装到所有的节点上，在 ceph-node1 上执行以下命令:

```bash
# ceph-deploy install --release emperor ceph-node1 ceph-node2 ceph-node3
```
ceph-deploy 工具将首先安装 Ceph Emperor 二进制包的所有依赖库 。 一旦这个命令成功完成.就可以执行以下命令检查 Ceph 版本以及 Ceph 集群健康状况 。
```bash
# ceph -v
```

4. 在 ceph-node1 上创建第一个 `momtor`:

```bash
# ceph-deploy mon create-initial
```
一旦创建成功，执行以下命令检查集群状态 。 在这阶段集群不会处于健康状态 。
```bash
# ceph status
```

5. 执行下列步骤，在 ceph-node1 节点上创建一个对象存储设备( `OSD` )，并将其加入 Ceph 集群中

```bash
# ceph-deploy disk list ceph-node1 # 列出物理磁盘
# ceph-deploy disk zap ceph-node1:sdb ceph-node1:sdc cephnode1:sdd # 清除分区表和数据
# ceph-deploy osd create ceph-node1:sdb ceph-node1:sdc cephnode1:sdd # 创建 OSD 
# ceph status
```
6. 在 ceph-node1上执行下列命令在 ceph-node2 和 ceph-node3 上部署 `monitor` 和 `OSD` :

```bash
在 ceph-node2 和 ceph-node3 上部署 monitor:
# ceph-deploy mon create ceph-node2
# ceph-deploy mon create ceph-node3

在 ceph-node2 和 ceph-node3 上添加 Ceph OSD
# ceph-dep1oy disk 1ist ceph-node2 ceph-node3

# ceph-dep1oy disk zap ceph-node2:sdb ceph-node2:sdc ceph-node2:sdd
# ceph-dep1oy disk zap ceph-node3:sdb ceph-node3:sdc ceph-node3:sdd

# ceph-dep1oy osd create ceph-node2:sdb ceph-node2:sdc ceph-node2:sdd
# ceph-dep1oy osd create ceph-node3:sdb ceph-node3:sdc ceph-node3:sdd
# ceph status

```

7. Ceph 存储配置- 部署 `RADOS 块设备( Ceph 块设备 )`
```bash
## 登陆 ceph-node1 在 ceph-node1 上创建块设备
# rbd create ceph-c1ient1-rbd1 --size 10240 
# rbd ls
# rbd --image ceph-c1ient1-rbd1 info
# rbd --image ceph-c1ient1-rbd1 info -p rbd

## 在 ceph-node1 上安装为 ceph-client1 安装 Ceph 二进制包
# ceph-dep1oy inatall ceph-client1
# ceph-dep1oy admin ceph-client1 # 将 ceph.conf 和 ceph.mon.keyring 文件复制到 ceph-client1 上

## 登陆 ceph-client1，映射名为 ceph-c1ient1-rbd1 的 RBD 镜像到 ceph-client1 上
# rbd map --image ceph-c1ient1-rbd1
# rbd showmapped # 查找映射名，假设映射名为 /dev/rbd0

## 创建文件系统，挂载
# fdisk -l /dev/rbd0
# mkfs.xfs /dev/rbd0
# mkdir /mnt/ceph-vo11
# mount /dev/rbd0 /mnt/ceph-vo11

## 向 Ceph RBD 上存放数据
# dd if=/dev/zero of=/mnt/ceph-vo11/fi1e1 count=100 bs=lM

## 调整 Ceph RBD 的大小
## Ceph RBD 快照
## 复制 Ceph RBD
```

8. 部署 `CephFS` 和 `MDS`
```bash
## 在 ceph-node1 上部署 Ceph 元数据服务器( Ceph Metadata Server, MDS) 
# ceph-deploy mds create ceph-node1
# cat /etc/ceph/ceph.mon.keyring # 查看管理员密钥

## 方法一：使用内核驱动程序挂载 CephFS
# mkdir /mnt/kernel_cephfs
# mount -t ceph 192.168.57.101:6789:/ /mnt/kernel_cephfs -o name=admin,secret=QAinltT8AhAAS93FrXLrrnVp8/sQhjvTIg==

## 方法二：通过 FUSE 方式挂载 CephFS
# yum install ceph-fuse
# mkdir /mnt/kernel_cephfs
# ceph-fuse -m 192.168.57.101:6789 /mnt/kernel_cephfs

## 修改 /etc/fstab 文件确保开机挂载
```

9. 部署 `RADOS GW`
```bash
## 方法一：
# ceph-deploy rgw create ceph-rgw

## 方法二：也就是 ceph-deploy rgw create ceph-rgw 命令的具体过程

## 在 ceph-rgw 节点上安装下列软件
# yum install httpd mod_fastcgi ceph-radosgw ceph

## 配置 hostname
# cat /etc/hosts
192.168.57.110 ceph-rgw.objectstore.com ceph-rgw

## 编辑 /etc/httpd/conf/httpd.conf 文件以配置 Apache

## 创建 Ceph 对象网关脚本 s3gw.fcgi
# cat /var/www/html/s3gw.fcgi
#!/bin/sh
exec /usr/bin/radosgw -c /etc/ceph/ceph.conf -n client.radosgw.gateway

## 在 /etc/httpd/conf.d 目录下创建网关配置文件 rgw.conf

## 在任意一台 Ceph monitor 节点上为 Ceph 创建 RADOS 网关用户及密钥环






```







附加

```bash
/usr/bin/ceph-deploy
[root@app1 ~]# ceph-deploy --help
usage: ceph-deploy [-h] [-v | -q] [--version] [--username USERNAME]
                   [--overwrite-conf] [--ceph-conf CEPH_CONF]
                   COMMAND ...

Easy Ceph deployment

    -^-
   /   \
   |O o|  ceph-deploy v2.0.1
   ).-.(
  '/|||\`
  | '|` |
    '|`

Full documentation can be found at: http://ceph.com/ceph-deploy/docs

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         be more verbose
  -q, --quiet           be less verbose
  --version             the current installed version of ceph-deploy
  --username USERNAME   the username to connect to the remote host
  --overwrite-conf      overwrite an existing conf file on remote host (if
                        present)
  --ceph-conf CEPH_CONF
                        use (or reuse) a given ceph.conf file

commands:
  COMMAND               description
    new                 Start deploying a new cluster, and write a
                        CLUSTER.conf and keyring for it.
    install             Install Ceph packages on remote hosts.
    rgw                 Ceph RGW daemon management
    mgr                 Ceph MGR daemon management
    mds                 Ceph MDS daemon management
    mon                 Ceph MON Daemon management
    gatherkeys          Gather authentication keys for provisioning new nodes.
    disk                Manage disks on a remote host.
    osd                 Prepare a data disk on remote host.
    repo                Repo definition management
    admin               Push configuration and client.admin key to a remote
                        host.
    config              Copy ceph.conf to/from remote host(s)
    uninstall           Remove Ceph packages from remote hosts.
    purgedata           Purge (delete, destroy, discard, shred) any Ceph data
                        from /var/lib/ceph
    purge               Remove Ceph packages from remote hosts and purge all
                        data.
    forgetkeys          Remove authentication keys from the local directory.
    pkg                 Manage packages on remote hosts.
    calamari            Install and configure Calamari nodes. Assumes that a
                        repository with Calamari packages is already
                        configured. Refer to the docs for examples
                        (http://ceph.com/ceph-deploy/docs/conf.html)

See 'ceph-deploy <command> --help' for help on a specific command
[root@app1 ~]# 
#############################################
[root@app1 ~]# mkdir /etc/ceph
[root@app1 ~]# cd /etc/ceph
[root@app1 ceph]# 
[root@app1 ceph]# ceph-deploy new app1
[ceph_deploy.conf][DEBUG ] found configuration file at: /root/.cephdeploy.conf
[ceph_deploy.cli][INFO  ] Invoked (2.0.1): /usr/bin/ceph-deploy new app1
[ceph_deploy.cli][INFO  ] ceph-deploy options:
[ceph_deploy.cli][INFO  ]  username                      : None
[ceph_deploy.cli][INFO  ]  func                          : <function new at 0x1e4b1b8>
[ceph_deploy.cli][INFO  ]  verbose                       : False
[ceph_deploy.cli][INFO  ]  overwrite_conf                : False
[ceph_deploy.cli][INFO  ]  quiet                         : False
[ceph_deploy.cli][INFO  ]  cd_conf                       : <ceph_deploy.conf.cephdeploy.Conf instance at 0x1e95cb0>
[ceph_deploy.cli][INFO  ]  cluster                       : ceph
[ceph_deploy.cli][INFO  ]  ssh_copykey                   : True
[ceph_deploy.cli][INFO  ]  mon                           : ['app1']
[ceph_deploy.cli][INFO  ]  public_network                : None
[ceph_deploy.cli][INFO  ]  ceph_conf                     : None
[ceph_deploy.cli][INFO  ]  cluster_network               : None
[ceph_deploy.cli][INFO  ]  default_release               : False
[ceph_deploy.cli][INFO  ]  fsid                          : None
[ceph_deploy.new][DEBUG ] Creating new cluster named ceph
[ceph_deploy.new][INFO  ] making sure passwordless SSH succeeds
[app1][DEBUG ] connected to host: app1 
[app1][DEBUG ] detect platform information from remote host
[app1][DEBUG ] detect machine type
[app1][DEBUG ] find the location of an executable
[app1][INFO  ] Running command: /usr/sbin/ip link show
[app1][INFO  ] Running command: /usr/sbin/ip addr show
[app1][DEBUG ] IP addresses found: [u'192.168.6.211']
[ceph_deploy.new][DEBUG ] Resolving host app1
[ceph_deploy.new][DEBUG ] Monitor app1 at 192.168.6.211
[ceph_deploy.new][DEBUG ] Monitor initial members are ['app1']
[ceph_deploy.new][DEBUG ] Monitor addrs are ['192.168.6.211']
[ceph_deploy.new][DEBUG ] Creating a random mon key...
[ceph_deploy.new][DEBUG ] Writing monitor keyring to ceph.mon.keyring...
[ceph_deploy.new][DEBUG ] Writing initial config to ceph.conf...
[root@app1 ceph]# ll
total 12
-rw-r--r-- 1 root root  195 Nov 21 14:35 ceph.conf
-rw-r--r-- 1 root root 2894 Nov 21 14:35 ceph-deploy-ceph.log
-rw------- 1 root root   73 Nov 21 14:35 ceph.mon.keyring
[root@app1 ceph]# 
[root@app1 ceph]# 
[root@app1 ceph]# cat ceph.conf 
[global]
fsid = c23d9371-3e7b-4276-bd77-0f21b4c1ad9b
mon_initial_members = app1
mon_host = 192.168.6.211
auth_cluster_required = cephx
auth_service_required = cephx
auth_client_required = cephx

[root@app1 ceph]# 
[root@app1 ceph]# cat ceph.mon.keyring 
[mon.]
key = AQCj/PRbAAAAABAAeaujHpx3iIm9dPqJoY5STA==
caps mon = allow *
[root@app1 ceph]# 
[root@app1 ceph]# cat ceph-deploy-ceph.log 
[2018-11-21 14:35:15,169][ceph_deploy.conf][DEBUG ] found configuration file at: /root/.cephdeploy.conf
[2018-11-21 14:35:15,170][ceph_deploy.cli][INFO  ] Invoked (2.0.1): /usr/bin/ceph-deploy new app1
[2018-11-21 14:35:15,170][ceph_deploy.cli][INFO  ] ceph-deploy options:
[2018-11-21 14:35:15,170][ceph_deploy.cli][INFO  ]  username                      : None
[2018-11-21 14:35:15,170][ceph_deploy.cli][INFO  ]  func                          : <function new at 0x1e4b1b8>
[2018-11-21 14:35:15,170][ceph_deploy.cli][INFO  ]  verbose                       : False
[2018-11-21 14:35:15,170][ceph_deploy.cli][INFO  ]  overwrite_conf                : False
[2018-11-21 14:35:15,170][ceph_deploy.cli][INFO  ]  quiet                         : False
[2018-11-21 14:35:15,170][ceph_deploy.cli][INFO  ]  cd_conf                       : <ceph_deploy.conf.cephdeploy.Conf instance at 0x1e95cb0>
[2018-11-21 14:35:15,171][ceph_deploy.cli][INFO  ]  cluster                       : ceph
[2018-11-21 14:35:15,171][ceph_deploy.cli][INFO  ]  ssh_copykey                   : True
[2018-11-21 14:35:15,171][ceph_deploy.cli][INFO  ]  mon                           : ['app1']
[2018-11-21 14:35:15,171][ceph_deploy.cli][INFO  ]  public_network                : None
[2018-11-21 14:35:15,171][ceph_deploy.cli][INFO  ]  ceph_conf                     : None
[2018-11-21 14:35:15,171][ceph_deploy.cli][INFO  ]  cluster_network               : None
[2018-11-21 14:35:15,171][ceph_deploy.cli][INFO  ]  default_release               : False
[2018-11-21 14:35:15,171][ceph_deploy.cli][INFO  ]  fsid                          : None
[2018-11-21 14:35:15,171][ceph_deploy.new][DEBUG ] Creating new cluster named ceph
[2018-11-21 14:35:15,171][ceph_deploy.new][INFO  ] making sure passwordless SSH succeeds
[2018-11-21 14:35:15,233][app1][DEBUG ] connected to host: app1 
[2018-11-21 14:35:15,234][app1][DEBUG ] detect platform information from remote host
[2018-11-21 14:35:15,266][app1][DEBUG ] detect machine type
[2018-11-21 14:35:15,272][app1][DEBUG ] find the location of an executable
[2018-11-21 14:35:15,290][app1][INFO  ] Running command: /usr/sbin/ip link show
[2018-11-21 14:35:15,335][app1][INFO  ] Running command: /usr/sbin/ip addr show
[2018-11-21 14:35:15,353][app1][DEBUG ] IP addresses found: [u'192.168.6.211']
[2018-11-21 14:35:15,354][ceph_deploy.new][DEBUG ] Resolving host app1
[2018-11-21 14:35:15,354][ceph_deploy.new][DEBUG ] Monitor app1 at 192.168.6.211
[2018-11-21 14:35:15,354][ceph_deploy.new][DEBUG ] Monitor initial members are ['app1']
[2018-11-21 14:35:15,354][ceph_deploy.new][DEBUG ] Monitor addrs are ['192.168.6.211']
[2018-11-21 14:35:15,354][ceph_deploy.new][DEBUG ] Creating a random mon key...
[2018-11-21 14:35:15,355][ceph_deploy.new][DEBUG ] Writing monitor keyring to ceph.mon.keyring...
[2018-11-21 14:35:15,355][ceph_deploy.new][DEBUG ] Writing initial config to ceph.conf...
[root@app1 ceph]# 
#############################################
[root@app1 ceph]# 
[root@app1 ceph]# ceph-deploy install --release luminous app1 app2 app3
[ceph_deploy.conf][DEBUG ] found configuration file at: /root/.cephdeploy.conf
[ceph_deploy.cli][INFO  ] Invoked (2.0.1): /usr/bin/ceph-deploy install --release luminous app1 app2 app3
[ceph_deploy.cli][INFO  ] ceph-deploy options:
[ceph_deploy.cli][INFO  ]  verbose                       : False
[ceph_deploy.cli][INFO  ]  testing                       : None
[ceph_deploy.cli][INFO  ]  cd_conf                       : <ceph_deploy.conf.cephdeploy.Conf instance at 0x1215cf8>
[ceph_deploy.cli][INFO  ]  cluster                       : ceph
[ceph_deploy.cli][INFO  ]  dev_commit                    : None
[ceph_deploy.cli][INFO  ]  install_mds                   : False
[ceph_deploy.cli][INFO  ]  stable                        : None
[ceph_deploy.cli][INFO  ]  default_release               : False
[ceph_deploy.cli][INFO  ]  username                      : None
[ceph_deploy.cli][INFO  ]  adjust_repos                  : True
[ceph_deploy.cli][INFO  ]  func                          : <function install at 0x11b4938>
[ceph_deploy.cli][INFO  ]  install_mgr                   : False
[ceph_deploy.cli][INFO  ]  install_all                   : False
[ceph_deploy.cli][INFO  ]  repo                          : False
[ceph_deploy.cli][INFO  ]  host                          : ['app1', 'app2', 'app3']
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
[ceph_deploy.cli][INFO  ]  release                       : luminous
[ceph_deploy.cli][INFO  ]  install_mon                   : False
[ceph_deploy.cli][INFO  ]  gpg_url                       : None
[ceph_deploy.install][DEBUG ] Installing stable version luminous on cluster ceph hosts app1 app2 app3
[ceph_deploy.install][DEBUG ] Detecting platform for host app1 ...
[app1][DEBUG ] connected to host: app1 
[app1][DEBUG ] detect platform information from remote host
[app1][DEBUG ] detect machine type
[ceph_deploy.install][INFO  ] Distro info: CentOS Linux 7.3.1611 Core
[app1][INFO  ] installing Ceph on app1
[app1][INFO  ] Running command: yum clean all
[app1][DEBUG ] Loaded plugins: fastestmirror
[app1][DEBUG ] Cleaning repos: base ceph-noarch epel extras mysql-connectors-community
[app1][DEBUG ]               : mysql-tools-community mysql57-community updates
[app1][DEBUG ] Cleaning up everything
[app1][DEBUG ] Cleaning up list of fastest mirrors
[app1][INFO  ] Running command: yum -y install epel-release
[app1][DEBUG ] Loaded plugins: fastestmirror
[app1][WARNIN] http://ftp.jaist.ac.jp/pub/Linux/Fedora/epel/7/x86_64/repodata/8bf3c67c445a16fc33ae55b855f5dc0c898f67dd71678be7af8efb3ae9e24a2d-updateinfo.xml.bz2: [Errno 14] curl#7 - "Failed to connect to 2001:df0:2ed:feed::feed: Network is unreachable"
[app1][WARNIN] Trying other mirror.
[app1][DEBUG ] Determining fastest mirrors
[app1][DEBUG ]  * base: mirrors.aliyun.com
[app1][DEBUG ]  * epel: mirror01.idc.hinet.net
[app1][DEBUG ]  * extras: mirrors.aliyun.com
[app1][DEBUG ]  * updates: mirrors.aliyun.com
[app1][DEBUG ] Package epel-release-7-11.noarch already installed and latest version
[app1][DEBUG ] Nothing to do
[app1][INFO  ] Running command: yum -y install yum-plugin-priorities
[app1][DEBUG ] Loaded plugins: fastestmirror
[app1][DEBUG ] Loading mirror speeds from cached hostfile
[app1][DEBUG ]  * base: mirrors.aliyun.com
[app1][DEBUG ]  * epel: mirror01.idc.hinet.net
[app1][DEBUG ]  * extras: mirrors.aliyun.com
[app1][DEBUG ]  * updates: mirrors.aliyun.com
[app1][DEBUG ] Resolving Dependencies
[app1][DEBUG ] --> Running transaction check
[app1][DEBUG ] ---> Package yum-plugin-priorities.noarch 0:1.1.31-46.el7_5 will be installed
[app1][DEBUG ] --> Finished Dependency Resolution
[app1][DEBUG ] 
[app1][DEBUG ] Dependencies Resolved
[app1][DEBUG ] 
[app1][DEBUG ] ================================================================================
[app1][DEBUG ]  Package                    Arch        Version              Repository    Size
[app1][DEBUG ] ================================================================================
[app1][DEBUG ] Installing:
[app1][DEBUG ]  yum-plugin-priorities      noarch      1.1.31-46.el7_5      updates       28 k
[app1][DEBUG ] 
[app1][DEBUG ] Transaction Summary
[app1][DEBUG ] ================================================================================
[app1][DEBUG ] Install  1 Package
[app1][DEBUG ] 
[app1][DEBUG ] Total download size: 28 k
[app1][DEBUG ] Installed size: 28 k
[app1][DEBUG ] Downloading packages:
[app1][DEBUG ] Running transaction check
[app1][DEBUG ] Running transaction test
[app1][DEBUG ] Transaction test succeeded
[app1][DEBUG ] Running transaction
[app1][DEBUG ]   Installing : yum-plugin-priorities-1.1.31-46.el7_5.noarch                 1/1 
[app1][DEBUG ]   Verifying  : yum-plugin-priorities-1.1.31-46.el7_5.noarch                 1/1 
[app1][DEBUG ] 
[app1][DEBUG ] Installed:
[app1][DEBUG ]   yum-plugin-priorities.noarch 0:1.1.31-46.el7_5                                
[app1][DEBUG ] 
[app1][DEBUG ] Complete!
[app1][DEBUG ] Configure Yum priorities to include obsoletes
[app1][WARNIN] check_obsoletes has been enabled for Yum priorities plugin
[app1][INFO  ] Running command: rpm --import https://download.ceph.com/keys/release.asc
[app1][INFO  ] Running command: yum remove -y ceph-release
[app1][DEBUG ] Loaded plugins: fastestmirror, priorities
[app1][WARNIN] No Match for argument: ceph-release
[app1][DEBUG ] No Packages marked for removal
[app1][INFO  ] Running command: yum install -y https://download.ceph.com/rpm-luminous/el7/noarch/ceph-release-1-0.el7.noarch.rpm
[app1][DEBUG ] Loaded plugins: fastestmirror, priorities
[app1][DEBUG ] Examining /var/tmp/yum-root-akaOKp/ceph-release-1-0.el7.noarch.rpm: ceph-release-1-1.el7.noarch
[app1][DEBUG ] Marking /var/tmp/yum-root-akaOKp/ceph-release-1-0.el7.noarch.rpm to be installed
[app1][DEBUG ] Resolving Dependencies
[app1][DEBUG ] --> Running transaction check
[app1][DEBUG ] ---> Package ceph-release.noarch 0:1-1.el7 will be installed
[app1][DEBUG ] --> Finished Dependency Resolution
[app1][DEBUG ] 
[app1][DEBUG ] Dependencies Resolved
[app1][DEBUG ] 
[app1][DEBUG ] ================================================================================
[app1][DEBUG ]  Package          Arch       Version     Repository                        Size
[app1][DEBUG ] ================================================================================
[app1][DEBUG ] Installing:
[app1][DEBUG ]  ceph-release     noarch     1-1.el7     /ceph-release-1-0.el7.noarch     544  
[app1][DEBUG ] 
[app1][DEBUG ] Transaction Summary
[app1][DEBUG ] ================================================================================
[app1][DEBUG ] Install  1 Package
[app1][DEBUG ] 
[app1][DEBUG ] Total size: 544  
[app1][DEBUG ] Installed size: 544  
[app1][DEBUG ] Downloading packages:
[app1][DEBUG ] Running transaction check
[app1][DEBUG ] Running transaction test
[app1][DEBUG ] Transaction test succeeded
[app1][DEBUG ] Running transaction
[app1][DEBUG ]   Installing : ceph-release-1-1.el7.noarch                                  1/1 
[app1][DEBUG ] warning: /etc/yum.repos.d/ceph.repo created as /etc/yum.repos.d/ceph.repo.rpmnew
[app1][DEBUG ]   Verifying  : ceph-release-1-1.el7.noarch                                  1/1 
[app1][DEBUG ] 
[app1][DEBUG ] Installed:
[app1][DEBUG ]   ceph-release.noarch 0:1-1.el7                                                 
[app1][DEBUG ] 
[app1][DEBUG ] Complete!
[app1][WARNIN] ensuring that /etc/yum.repos.d/ceph.repo contains a high priority
[ceph_deploy][ERROR ] RuntimeError: NoSectionError: No section: 'ceph'

[root@app1 ceph]# 
[root@app1 ceph]# 
[root@app1 ceph]# 
[root@app1 ceph]# rpm -ql ceph-release
/etc/yum.repos.d/ceph.repo
[root@app1 ceph]# 
[root@app1 ceph]# 
[root@app1 ceph]# ceph-deploy install --release luminous app1 app2 app3
[ceph_deploy.conf][DEBUG ] found configuration file at: /root/.cephdeploy.conf
[ceph_deploy.cli][INFO  ] Invoked (2.0.1): /usr/bin/ceph-deploy install --release luminous app1 app2 app3
[ceph_deploy.cli][INFO  ] ceph-deploy options:
[ceph_deploy.cli][INFO  ]  verbose                       : False
[ceph_deploy.cli][INFO  ]  testing                       : None
[ceph_deploy.cli][INFO  ]  cd_conf                       : <ceph_deploy.conf.cephdeploy.Conf instance at 0x24dccf8>
[ceph_deploy.cli][INFO  ]  cluster                       : ceph
[ceph_deploy.cli][INFO  ]  dev_commit                    : None
[ceph_deploy.cli][INFO  ]  install_mds                   : False
[ceph_deploy.cli][INFO  ]  stable                        : None
[ceph_deploy.cli][INFO  ]  default_release               : False
[ceph_deploy.cli][INFO  ]  username                      : None
[ceph_deploy.cli][INFO  ]  adjust_repos                  : True
[ceph_deploy.cli][INFO  ]  func                          : <function install at 0x247b938>
[ceph_deploy.cli][INFO  ]  install_mgr                   : False
[ceph_deploy.cli][INFO  ]  install_all                   : False
[ceph_deploy.cli][INFO  ]  repo                          : False
[ceph_deploy.cli][INFO  ]  host                          : ['app1', 'app2', 'app3']
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
[ceph_deploy.cli][INFO  ]  release                       : luminous
[ceph_deploy.cli][INFO  ]  install_mon                   : False
[ceph_deploy.cli][INFO  ]  gpg_url                       : None
[ceph_deploy.install][DEBUG ] Installing stable version luminous on cluster ceph hosts app1 app2 app3
[ceph_deploy.install][DEBUG ] Detecting platform for host app1 ...
[app1][DEBUG ] connected to host: app1 
[app1][DEBUG ] detect platform information from remote host
[app1][DEBUG ] detect machine type
[ceph_deploy.install][INFO  ] Distro info: CentOS Linux 7.3.1611 Core
[app1][INFO  ] installing Ceph on app1
[app1][INFO  ] Running command: yum clean all
[app1][DEBUG ] Loaded plugins: fastestmirror, priorities
[app1][DEBUG ] Cleaning repos: base epel extras mysql-connectors-community
[app1][DEBUG ]               : mysql-tools-community mysql57-community updates
[app1][DEBUG ] Cleaning up everything
[app1][DEBUG ] Cleaning up list of fastest mirrors
[app1][INFO  ] Running command: yum -y install epel-release
[app1][DEBUG ] Loaded plugins: fastestmirror, priorities
[app1][WARNIN] http://mirror.nes.co.id/epel/7/x86_64/repodata/repomd.xml: [Errno 14] curl#7 - "Failed connect to mirror.nes.co.id:80; No route to host"
[app1][WARNIN] Trying other mirror.
[app1][DEBUG ] Determining fastest mirrors
[app1][DEBUG ]  * base: mirrors.aliyun.com
[app1][DEBUG ]  * epel: fedora.cs.nctu.edu.tw
[app1][DEBUG ]  * extras: mirror.bit.edu.cn
[app1][DEBUG ]  * updates: mirrors.aliyun.com
[app1][DEBUG ] Package epel-release-7-11.noarch already installed and latest version
[app1][DEBUG ] Nothing to do
[app1][INFO  ] Running command: yum -y install yum-plugin-priorities
[app1][DEBUG ] Loaded plugins: fastestmirror, priorities
[app1][DEBUG ] Loading mirror speeds from cached hostfile
[app1][DEBUG ]  * base: mirrors.aliyun.com
[app1][DEBUG ]  * epel: fedora.cs.nctu.edu.tw
[app1][DEBUG ]  * extras: mirror.bit.edu.cn
[app1][DEBUG ]  * updates: mirrors.aliyun.com
[app1][DEBUG ] Package yum-plugin-priorities-1.1.31-46.el7_5.noarch already installed and latest version
[app1][DEBUG ] Nothing to do
[app1][DEBUG ] Configure Yum priorities to include obsoletes
[app1][WARNIN] check_obsoletes has been enabled for Yum priorities plugin
[app1][INFO  ] Running command: rpm --import https://download.ceph.com/keys/release.asc
[app1][INFO  ] Running command: yum remove -y ceph-release
[app1][DEBUG ] Loaded plugins: fastestmirror, priorities
[app1][WARNIN] No Match for argument: ceph-release
[app1][DEBUG ] No Packages marked for removal
[app1][INFO  ] Running command: yum install -y https://download.ceph.com/rpm-luminous/el7/noarch/ceph-release-1-0.el7.noarch.rpm
[app1][DEBUG ] Loaded plugins: fastestmirror, priorities
[app1][DEBUG ] Examining /var/tmp/yum-root-akaOKp/ceph-release-1-0.el7.noarch.rpm: ceph-release-1-1.el7.noarch
[app1][DEBUG ] Marking /var/tmp/yum-root-akaOKp/ceph-release-1-0.el7.noarch.rpm to be installed
[app1][DEBUG ] Resolving Dependencies
[app1][DEBUG ] --> Running transaction check
[app1][DEBUG ] ---> Package ceph-release.noarch 0:1-1.el7 will be installed
[app1][DEBUG ] --> Finished Dependency Resolution
[app1][DEBUG ] 
[app1][DEBUG ] Dependencies Resolved
[app1][DEBUG ] 
[app1][DEBUG ] ================================================================================
[app1][DEBUG ]  Package          Arch       Version     Repository                        Size
[app1][DEBUG ] ================================================================================
[app1][DEBUG ] Installing:
[app1][DEBUG ]  ceph-release     noarch     1-1.el7     /ceph-release-1-0.el7.noarch     544  
[app1][DEBUG ] 
[app1][DEBUG ] Transaction Summary
[app1][DEBUG ] ================================================================================
[app1][DEBUG ] Install  1 Package
[app1][DEBUG ] 
[app1][DEBUG ] Total size: 544  
[app1][DEBUG ] Installed size: 544  
[app1][DEBUG ] Downloading packages:
[app1][DEBUG ] Running transaction check
[app1][DEBUG ] Running transaction test
[app1][DEBUG ] Transaction test succeeded
[app1][DEBUG ] Running transaction
[app1][DEBUG ]   Installing : ceph-release-1-1.el7.noarch                                  1/1 
[app1][DEBUG ]   Verifying  : ceph-release-1-1.el7.noarch                                  1/1 
[app1][DEBUG ] 
[app1][DEBUG ] Installed:
[app1][DEBUG ]   ceph-release.noarch 0:1-1.el7                                                 
[app1][DEBUG ] 
[app1][DEBUG ] Complete!
[app1][WARNIN] ensuring that /etc/yum.repos.d/ceph.repo contains a high priority
[app1][WARNIN] altered ceph.repo priorities to contain: priority=1
[app1][INFO  ] Running command: yum -y install ceph ceph-radosgw
[app1][DEBUG ] Loaded plugins: fastestmirror, priorities
[app1][DEBUG ] Loading mirror speeds from cached hostfile
[app1][DEBUG ]  * base: mirrors.aliyun.com
[app1][DEBUG ]  * epel: fedora.cs.nctu.edu.tw
[app1][DEBUG ]  * extras: mirror.bit.edu.cn
[app1][DEBUG ]  * updates: mirrors.aliyun.com
[app1][DEBUG ] 8 packages excluded due to repository priority protections
[app1][DEBUG ] Resolving Dependencies
[app1][DEBUG ] --> Running transaction check
[app1][DEBUG ] ---> Package ceph.x86_64 2:12.2.9-0.el7 will be installed
[app1][DEBUG ] --> Processing Dependency: ceph-osd = 2:12.2.9-0.el7 for package: 2:ceph-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: ceph-mds = 2:12.2.9-0.el7 for package: 2:ceph-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: ceph-mon = 2:12.2.9-0.el7 for package: 2:ceph-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: ceph-mgr = 2:12.2.9-0.el7 for package: 2:ceph-12.2.9-0.el7.x86_64
[app1][DEBUG ] ---> Package ceph-radosgw.x86_64 2:12.2.9-0.el7 will be installed
[app1][DEBUG ] --> Processing Dependency: librados2 = 2:12.2.9-0.el7 for package: 2:ceph-radosgw-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: librgw2 = 2:12.2.9-0.el7 for package: 2:ceph-radosgw-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: ceph-common = 2:12.2.9-0.el7 for package: 2:ceph-radosgw-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: ceph-selinux = 2:12.2.9-0.el7 for package: 2:ceph-radosgw-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: libibverbs.so.1()(64bit) for package: 2:ceph-radosgw-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: librados.so.2()(64bit) for package: 2:ceph-radosgw-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: libceph-common.so.0()(64bit) for package: 2:ceph-radosgw-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Running transaction check
[app1][DEBUG ] ---> Package ceph-common.x86_64 2:12.2.9-0.el7 will be installed
[app1][DEBUG ] --> Processing Dependency: librbd1 = 2:12.2.9-0.el7 for package: 2:ceph-common-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: python-rados = 2:12.2.9-0.el7 for package: 2:ceph-common-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: python-rgw = 2:12.2.9-0.el7 for package: 2:ceph-common-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: python-cephfs = 2:12.2.9-0.el7 for package: 2:ceph-common-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: python-rbd = 2:12.2.9-0.el7 for package: 2:ceph-common-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: libcephfs2 = 2:12.2.9-0.el7 for package: 2:ceph-common-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: python-prettytable for package: 2:ceph-common-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: python-requests for package: 2:ceph-common-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: librbd.so.1()(64bit) for package: 2:ceph-common-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: libleveldb.so.1()(64bit) for package: 2:ceph-common-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: libfuse.so.2()(64bit) for package: 2:ceph-common-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: liblz4.so.1()(64bit) for package: 2:ceph-common-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: libradosstriper.so.1()(64bit) for package: 2:ceph-common-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: libbabeltrace.so.1()(64bit) for package: 2:ceph-common-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: libbabeltrace-ctf.so.1()(64bit) for package: 2:ceph-common-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: libcephfs.so.2()(64bit) for package: 2:ceph-common-12.2.9-0.el7.x86_64
[app1][DEBUG ] ---> Package ceph-mds.x86_64 2:12.2.9-0.el7 will be installed
[app1][DEBUG ] --> Processing Dependency: ceph-base = 2:12.2.9-0.el7 for package: 2:ceph-mds-12.2.9-0.el7.x86_64
[app1][DEBUG ] ---> Package ceph-mgr.x86_64 2:12.2.9-0.el7 will be installed
[app1][DEBUG ] --> Processing Dependency: python-jinja2 for package: 2:ceph-mgr-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: python-cherrypy for package: 2:ceph-mgr-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: python-six for package: 2:ceph-mgr-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: pyOpenSSL for package: 2:ceph-mgr-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: python-werkzeug for package: 2:ceph-mgr-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: python-pecan for package: 2:ceph-mgr-12.2.9-0.el7.x86_64
[app1][DEBUG ] ---> Package ceph-mon.x86_64 2:12.2.9-0.el7 will be installed
[app1][DEBUG ] --> Processing Dependency: python-flask for package: 2:ceph-mon-12.2.9-0.el7.x86_64
[app1][DEBUG ] ---> Package ceph-osd.x86_64 2:12.2.9-0.el7 will be installed
[app1][DEBUG ] --> Processing Dependency: gdisk for package: 2:ceph-osd-12.2.9-0.el7.x86_64
[app1][DEBUG ] ---> Package ceph-selinux.x86_64 2:12.2.9-0.el7 will be installed
[app1][DEBUG ] --> Processing Dependency: selinux-policy-base >= 3.13.1-166.el7_4.9 for package: 2:ceph-selinux-12.2.9-0.el7.x86_64
[app1][DEBUG ] ---> Package libibverbs.x86_64 0:15-7.el7_5 will be installed
[app1][DEBUG ] --> Processing Dependency: rdma-core(x86-64) = 15-7.el7_5 for package: libibverbs-15-7.el7_5.x86_64
[app1][DEBUG ] ---> Package librados2.x86_64 2:12.2.9-0.el7 will be installed
[app1][DEBUG ] --> Processing Dependency: liblttng-ust.so.0()(64bit) for package: 2:librados2-12.2.9-0.el7.x86_64
[app1][DEBUG ] ---> Package librgw2.x86_64 2:12.2.9-0.el7 will be installed
[app1][DEBUG ] --> Running transaction check
[app1][DEBUG ] ---> Package ceph-base.x86_64 2:12.2.9-0.el7 will be installed
[app1][DEBUG ] --> Processing Dependency: python-setuptools for package: 2:ceph-base-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: psmisc for package: 2:ceph-base-12.2.9-0.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: cryptsetup for package: 2:ceph-base-12.2.9-0.el7.x86_64
[app1][DEBUG ] ---> Package fuse-libs.x86_64 0:2.9.2-10.el7 will be installed
[app1][DEBUG ] ---> Package gdisk.x86_64 0:0.8.6-5.el7 will be installed
[app1][DEBUG ] ---> Package leveldb.x86_64 0:1.12.0-11.el7 will be installed
[app1][DEBUG ] ---> Package libbabeltrace.x86_64 0:1.2.4-3.el7 will be installed
[app1][DEBUG ] ---> Package libcephfs2.x86_64 2:12.2.9-0.el7 will be installed
[app1][DEBUG ] ---> Package libradosstriper1.x86_64 2:12.2.9-0.el7 will be installed
[app1][DEBUG ] ---> Package librbd1.x86_64 2:12.2.9-0.el7 will be installed
[app1][DEBUG ] ---> Package lttng-ust.x86_64 0:2.4.1-4.el7 will be installed
[app1][DEBUG ] --> Processing Dependency: liburcu-cds.so.1()(64bit) for package: lttng-ust-2.4.1-4.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: liburcu-bp.so.1()(64bit) for package: lttng-ust-2.4.1-4.el7.x86_64
[app1][DEBUG ] ---> Package lz4.x86_64 0:1.7.5-2.el7 will be installed
[app1][DEBUG ] ---> Package pyOpenSSL.x86_64 0:0.13.1-3.el7 will be installed
[app1][DEBUG ] ---> Package python-cephfs.x86_64 2:12.2.9-0.el7 will be installed
[app1][DEBUG ] ---> Package python-cherrypy.noarch 0:3.2.2-4.el7 will be installed
[app1][DEBUG ] ---> Package python-flask.noarch 1:0.10.1-4.el7 will be installed
[app1][DEBUG ] --> Processing Dependency: python-itsdangerous for package: 1:python-flask-0.10.1-4.el7.noarch
[app1][DEBUG ] ---> Package python-jinja2.noarch 0:2.7.2-2.el7 will be installed
[app1][DEBUG ] --> Processing Dependency: python-babel >= 0.8 for package: python-jinja2-2.7.2-2.el7.noarch
[app1][DEBUG ] --> Processing Dependency: python-markupsafe for package: python-jinja2-2.7.2-2.el7.noarch
[app1][DEBUG ] ---> Package python-pecan.noarch 0:0.4.5-2.el7 will be installed
[app1][DEBUG ] --> Processing Dependency: python-webtest >= 1.3.1 for package: python-pecan-0.4.5-2.el7.noarch
[app1][DEBUG ] --> Processing Dependency: python-webob >= 1.2 for package: python-pecan-0.4.5-2.el7.noarch
[app1][DEBUG ] --> Processing Dependency: python-simplegeneric >= 0.8 for package: python-pecan-0.4.5-2.el7.noarch
[app1][DEBUG ] --> Processing Dependency: python-mako >= 0.4.0 for package: python-pecan-0.4.5-2.el7.noarch
[app1][DEBUG ] --> Processing Dependency: python-singledispatch for package: python-pecan-0.4.5-2.el7.noarch
[app1][DEBUG ] ---> Package python-prettytable.noarch 0:0.7.2-3.el7 will be installed
[app1][DEBUG ] ---> Package python-rados.x86_64 2:12.2.9-0.el7 will be installed
[app1][DEBUG ] ---> Package python-rbd.x86_64 2:12.2.9-0.el7 will be installed
[app1][DEBUG ] ---> Package python-requests.noarch 0:2.6.0-1.el7_1 will be installed
[app1][DEBUG ] --> Processing Dependency: python-urllib3 >= 1.10.2-1 for package: python-requests-2.6.0-1.el7_1.noarch
[app1][DEBUG ] ---> Package python-rgw.x86_64 2:12.2.9-0.el7 will be installed
[app1][DEBUG ] ---> Package python-six.noarch 0:1.9.0-2.el7 will be installed
[app1][DEBUG ] ---> Package python-werkzeug.noarch 0:0.9.1-2.el7 will be installed
[app1][DEBUG ] ---> Package rdma.noarch 0:7.3_4.7_rc2-5.el7 will be obsoleted
[app1][DEBUG ] ---> Package rdma-core.i686 0:15-7.el7_5 will be obsoleting
[app1][DEBUG ] --> Processing Dependency: libudev.so.1(LIBUDEV_183) for package: rdma-core-15-7.el7_5.i686
[app1][DEBUG ] --> Processing Dependency: libudev.so.1 for package: rdma-core-15-7.el7_5.i686
[app1][DEBUG ] --> Processing Dependency: libsystemd.so.0(LIBSYSTEMD_209) for package: rdma-core-15-7.el7_5.i686
[app1][DEBUG ] --> Processing Dependency: libsystemd.so.0 for package: rdma-core-15-7.el7_5.i686
[app1][DEBUG ] ---> Package rdma-core.x86_64 0:15-7.el7_5 will be obsoleting
[app1][DEBUG ] ---> Package selinux-policy-targeted.noarch 0:3.13.1-102.el7 will be updated
[app1][DEBUG ] ---> Package selinux-policy-targeted.noarch 0:3.13.1-192.el7_5.6 will be an update
[app1][DEBUG ] --> Processing Dependency: selinux-policy = 3.13.1-192.el7_5.6 for package: selinux-policy-targeted-3.13.1-192.el7_5.6.noarch
[app1][DEBUG ] --> Processing Dependency: selinux-policy = 3.13.1-192.el7_5.6 for package: selinux-policy-targeted-3.13.1-192.el7_5.6.noarch
[app1][DEBUG ] --> Processing Dependency: policycoreutils >= 2.5-18 for package: selinux-policy-targeted-3.13.1-192.el7_5.6.noarch
[app1][DEBUG ] --> Running transaction check
[app1][DEBUG ] ---> Package cryptsetup.x86_64 0:1.7.4-4.el7 will be installed
[app1][DEBUG ] --> Processing Dependency: cryptsetup-libs(x86-64) = 1.7.4-4.el7 for package: cryptsetup-1.7.4-4.el7.x86_64
[app1][DEBUG ] ---> Package policycoreutils.x86_64 0:2.5-8.el7 will be updated
[app1][DEBUG ] ---> Package policycoreutils.x86_64 0:2.5-22.el7 will be an update
[app1][DEBUG ] ---> Package psmisc.x86_64 0:22.20-15.el7 will be installed
[app1][DEBUG ] ---> Package python-babel.noarch 0:0.9.6-8.el7 will be installed
[app1][DEBUG ] ---> Package python-itsdangerous.noarch 0:0.23-2.el7 will be installed
[app1][DEBUG ] ---> Package python-mako.noarch 0:0.8.1-2.el7 will be installed
[app1][DEBUG ] --> Processing Dependency: python-beaker for package: python-mako-0.8.1-2.el7.noarch
[app1][DEBUG ] ---> Package python-markupsafe.x86_64 0:0.11-10.el7 will be installed
[app1][DEBUG ] ---> Package python-setuptools.noarch 0:0.9.8-7.el7 will be installed
[app1][DEBUG ] --> Processing Dependency: python-backports-ssl_match_hostname for package: python-setuptools-0.9.8-7.el7.noarch
[app1][DEBUG ] ---> Package python-simplegeneric.noarch 0:0.8-7.el7 will be installed
[app1][DEBUG ] ---> Package python-singledispatch.noarch 0:3.4.0.2-2.el7 will be installed
[app1][DEBUG ] ---> Package python-urllib3.noarch 0:1.10.2-5.el7 will be installed
[app1][DEBUG ] --> Processing Dependency: python-ipaddress for package: python-urllib3-1.10.2-5.el7.noarch
[app1][DEBUG ] ---> Package python-webob.noarch 0:1.2.3-7.el7 will be installed
[app1][DEBUG ] ---> Package python-webtest.noarch 0:1.3.4-6.el7 will be installed
[app1][DEBUG ] ---> Package selinux-policy.noarch 0:3.13.1-102.el7 will be updated
[app1][DEBUG ] ---> Package selinux-policy.noarch 0:3.13.1-192.el7_5.6 will be an update
[app1][DEBUG ] ---> Package systemd-libs.x86_64 0:219-30.el7 will be updated
[app1][DEBUG ] --> Processing Dependency: systemd-libs = 219-30.el7 for package: systemd-219-30.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: systemd-libs = 219-30.el7 for package: libgudev1-219-30.el7.x86_64
[app1][DEBUG ] ---> Package systemd-libs.i686 0:219-57.el7_5.3 will be installed
[app1][DEBUG ] --> Processing Dependency: libselinux.so.1 for package: systemd-libs-219-57.el7_5.3.i686
[app1][DEBUG ] --> Processing Dependency: libpam_misc.so.0(LIBPAM_MISC_1.0) for package: systemd-libs-219-57.el7_5.3.i686
[app1][DEBUG ] --> Processing Dependency: libpam_misc.so.0 for package: systemd-libs-219-57.el7_5.3.i686
[app1][DEBUG ] --> Processing Dependency: libpam.so.0(LIBPAM_MODUTIL_1.0) for package: systemd-libs-219-57.el7_5.3.i686
[app1][DEBUG ] --> Processing Dependency: libpam.so.0(LIBPAM_EXTENSION_1.0) for package: systemd-libs-219-57.el7_5.3.i686
[app1][DEBUG ] --> Processing Dependency: libpam.so.0(LIBPAM_1.0) for package: systemd-libs-219-57.el7_5.3.i686
[app1][DEBUG ] --> Processing Dependency: libpam.so.0 for package: systemd-libs-219-57.el7_5.3.i686
[app1][DEBUG ] --> Processing Dependency: liblzma.so.5(XZ_5.0) for package: systemd-libs-219-57.el7_5.3.i686
[app1][DEBUG ] --> Processing Dependency: liblzma.so.5 for package: systemd-libs-219-57.el7_5.3.i686
[app1][DEBUG ] --> Processing Dependency: liblz4.so.1 for package: systemd-libs-219-57.el7_5.3.i686
[app1][DEBUG ] --> Processing Dependency: libgpg-error.so.0 for package: systemd-libs-219-57.el7_5.3.i686
[app1][DEBUG ] --> Processing Dependency: libgcrypt.so.11(GCRYPT_1.2) for package: systemd-libs-219-57.el7_5.3.i686
[app1][DEBUG ] --> Processing Dependency: libgcrypt.so.11 for package: systemd-libs-219-57.el7_5.3.i686
[app1][DEBUG ] --> Processing Dependency: libgcc_s.so.1(GCC_3.3.1) for package: systemd-libs-219-57.el7_5.3.i686
[app1][DEBUG ] --> Processing Dependency: libgcc_s.so.1(GCC_3.0) for package: systemd-libs-219-57.el7_5.3.i686
[app1][DEBUG ] --> Processing Dependency: libgcc_s.so.1 for package: systemd-libs-219-57.el7_5.3.i686
[app1][DEBUG ] --> Processing Dependency: libdw.so.1 for package: systemd-libs-219-57.el7_5.3.i686
[app1][DEBUG ] --> Processing Dependency: libcap.so.2 for package: systemd-libs-219-57.el7_5.3.i686
[app1][DEBUG ] ---> Package systemd-libs.x86_64 0:219-57.el7_5.3 will be an update
[app1][DEBUG ] ---> Package userspace-rcu.x86_64 0:0.7.16-1.el7 will be installed
[app1][DEBUG ] --> Running transaction check
[app1][DEBUG ] ---> Package cryptsetup-libs.x86_64 0:1.7.2-1.el7 will be updated
[app1][DEBUG ] ---> Package cryptsetup-libs.x86_64 0:1.7.4-4.el7 will be an update
[app1][DEBUG ] ---> Package elfutils-libs.x86_64 0:0.166-2.el7 will be updated
[app1][DEBUG ] ---> Package elfutils-libs.i686 0:0.170-4.el7 will be installed
[app1][DEBUG ] --> Processing Dependency: elfutils-libelf(x86-32) = 0.170-4.el7 for package: elfutils-libs-0.170-4.el7.i686
[app1][DEBUG ] --> Processing Dependency: libz.so.1(ZLIB_1.2.2.3) for package: elfutils-libs-0.170-4.el7.i686
[app1][DEBUG ] --> Processing Dependency: libz.so.1 for package: elfutils-libs-0.170-4.el7.i686
[app1][DEBUG ] --> Processing Dependency: libelf.so.1(ELFUTILS_1.7) for package: elfutils-libs-0.170-4.el7.i686
[app1][DEBUG ] --> Processing Dependency: libelf.so.1(ELFUTILS_1.6) for package: elfutils-libs-0.170-4.el7.i686
[app1][DEBUG ] --> Processing Dependency: libelf.so.1(ELFUTILS_1.5) for package: elfutils-libs-0.170-4.el7.i686
[app1][DEBUG ] --> Processing Dependency: libelf.so.1(ELFUTILS_1.4) for package: elfutils-libs-0.170-4.el7.i686
[app1][DEBUG ] --> Processing Dependency: libelf.so.1(ELFUTILS_1.3) for package: elfutils-libs-0.170-4.el7.i686
[app1][DEBUG ] --> Processing Dependency: libelf.so.1(ELFUTILS_1.1.1) for package: elfutils-libs-0.170-4.el7.i686
[app1][DEBUG ] --> Processing Dependency: libelf.so.1(ELFUTILS_1.0) for package: elfutils-libs-0.170-4.el7.i686
[app1][DEBUG ] --> Processing Dependency: libelf.so.1 for package: elfutils-libs-0.170-4.el7.i686
[app1][DEBUG ] --> Processing Dependency: libbz2.so.1 for package: elfutils-libs-0.170-4.el7.i686
[app1][DEBUG ] --> Processing Dependency: default-yama-scope for package: elfutils-libs-0.170-4.el7.i686
[app1][DEBUG ] ---> Package elfutils-libs.x86_64 0:0.170-4.el7 will be an update
[app1][DEBUG ] ---> Package libcap.x86_64 0:2.22-8.el7 will be updated
[app1][DEBUG ] ---> Package libcap.i686 0:2.22-9.el7 will be installed
[app1][DEBUG ] --> Processing Dependency: libattr.so.1(ATTR_1.0) for package: libcap-2.22-9.el7.i686
[app1][DEBUG ] --> Processing Dependency: libattr.so.1 for package: libcap-2.22-9.el7.i686
[app1][DEBUG ] ---> Package libcap.x86_64 0:2.22-9.el7 will be an update
[app1][DEBUG ] ---> Package libgcc.i686 0:4.8.5-28.el7_5.1 will be installed
[app1][DEBUG ] ---> Package libgcrypt.x86_64 0:1.5.3-12.el7_1.1 will be updated
[app1][DEBUG ] ---> Package libgcrypt.i686 0:1.5.3-14.el7 will be installed
[app1][DEBUG ] ---> Package libgcrypt.x86_64 0:1.5.3-14.el7 will be an update
[app1][DEBUG ] ---> Package libgpg-error.i686 0:1.12-3.el7 will be installed
[app1][DEBUG ] ---> Package libgudev1.x86_64 0:219-30.el7 will be updated
[app1][DEBUG ] ---> Package libgudev1.x86_64 0:219-57.el7_5.3 will be an update
[app1][DEBUG ] ---> Package libselinux.i686 0:2.5-12.el7 will be installed
[app1][DEBUG ] --> Processing Dependency: libsepol(x86-32) >= 2.5-6 for package: libselinux-2.5-12.el7.i686
[app1][DEBUG ] --> Processing Dependency: libsepol.so.1(LIBSEPOL_1.0) for package: libselinux-2.5-12.el7.i686
[app1][DEBUG ] --> Processing Dependency: libsepol.so.1 for package: libselinux-2.5-12.el7.i686
[app1][DEBUG ] --> Processing Dependency: libpcre.so.1 for package: libselinux-2.5-12.el7.i686
[app1][DEBUG ] ---> Package lz4.i686 0:1.7.5-2.el7 will be installed
[app1][DEBUG ] ---> Package pam.x86_64 0:1.1.8-18.el7 will be updated
[app1][DEBUG ] ---> Package pam.i686 0:1.1.8-22.el7 will be installed
[app1][DEBUG ] --> Processing Dependency: libdb-5.3.so for package: pam-1.1.8-22.el7.i686
[app1][DEBUG ] --> Processing Dependency: libcrack.so.2 for package: pam-1.1.8-22.el7.i686
[app1][DEBUG ] --> Processing Dependency: libaudit.so.1 for package: pam-1.1.8-22.el7.i686
[app1][DEBUG ] ---> Package pam.x86_64 0:1.1.8-22.el7 will be an update
[app1][DEBUG ] ---> Package python-backports-ssl_match_hostname.noarch 0:3.5.0.1-1.el7 will be installed
[app1][DEBUG ] --> Processing Dependency: python-backports for package: python-backports-ssl_match_hostname-3.5.0.1-1.el7.noarch
[app1][DEBUG ] ---> Package python-beaker.noarch 0:1.5.4-10.el7 will be installed
[app1][DEBUG ] --> Processing Dependency: python-paste for package: python-beaker-1.5.4-10.el7.noarch
[app1][DEBUG ] ---> Package python-ipaddress.noarch 0:1.0.16-2.el7 will be installed
[app1][DEBUG ] ---> Package systemd.x86_64 0:219-30.el7 will be updated
[app1][DEBUG ] --> Processing Dependency: systemd = 219-30.el7 for package: systemd-sysv-219-30.el7.x86_64
[app1][DEBUG ] ---> Package systemd.x86_64 0:219-57.el7_5.3 will be an update
[app1][DEBUG ] ---> Package xz-libs.i686 0:5.2.2-1.el7 will be installed
[app1][DEBUG ] --> Running transaction check
[app1][DEBUG ] ---> Package audit-libs.x86_64 0:2.6.5-3.el7 will be updated
[app1][DEBUG ] --> Processing Dependency: audit-libs(x86-64) = 2.6.5-3.el7 for package: audit-2.6.5-3.el7.x86_64
[app1][DEBUG ] ---> Package audit-libs.i686 0:2.8.1-3.el7_5.1 will be installed
[app1][DEBUG ] --> Processing Dependency: libcap-ng.so.0 for package: audit-libs-2.8.1-3.el7_5.1.i686
[app1][DEBUG ] ---> Package audit-libs.x86_64 0:2.8.1-3.el7_5.1 will be an update
[app1][DEBUG ] ---> Package bzip2-libs.i686 0:1.0.6-13.el7 will be installed
[app1][DEBUG ] ---> Package cracklib.i686 0:2.9.0-11.el7 will be installed
[app1][DEBUG ] ---> Package elfutils-default-yama-scope.noarch 0:0.170-4.el7 will be installed
[app1][DEBUG ] ---> Package elfutils-libelf.x86_64 0:0.166-2.el7 will be updated
[app1][DEBUG ] ---> Package elfutils-libelf.i686 0:0.170-4.el7 will be installed
[app1][DEBUG ] ---> Package elfutils-libelf.x86_64 0:0.170-4.el7 will be an update
[app1][DEBUG ] ---> Package libattr.x86_64 0:2.4.46-12.el7 will be updated
[app1][DEBUG ] ---> Package libattr.i686 0:2.4.46-13.el7 will be installed
[app1][DEBUG ] ---> Package libattr.x86_64 0:2.4.46-13.el7 will be an update
[app1][DEBUG ] ---> Package libdb.x86_64 0:5.3.21-19.el7 will be updated
[app1][DEBUG ] --> Processing Dependency: libdb(x86-64) = 5.3.21-19.el7 for package: libdb-devel-5.3.21-19.el7.x86_64
[app1][DEBUG ] --> Processing Dependency: libdb(x86-64) = 5.3.21-19.el7 for package: libdb-utils-5.3.21-19.el7.x86_64
[app1][DEBUG ] ---> Package libdb.i686 0:5.3.21-24.el7 will be installed
[app1][DEBUG ] ---> Package libdb.x86_64 0:5.3.21-24.el7 will be an update
[app1][DEBUG ] ---> Package libsepol.i686 0:2.5-8.1.el7 will be installed
[app1][DEBUG ] ---> Package pcre.x86_64 0:8.32-15.el7_2.1 will be updated
[app1][DEBUG ] --> Processing Dependency: pcre(x86-64) = 8.32-15.el7_2.1 for package: pcre-devel-8.32-15.el7_2.1.x86_64
[app1][DEBUG ] ---> Package pcre.i686 0:8.32-17.el7 will be installed
[app1][DEBUG ] --> Processing Dependency: libstdc++.so.6(GLIBCXX_3.4.9) for package: pcre-8.32-17.el7.i686
[app1][DEBUG ] --> Processing Dependency: libstdc++.so.6(GLIBCXX_3.4) for package: pcre-8.32-17.el7.i686
[app1][DEBUG ] --> Processing Dependency: libstdc++.so.6(CXXABI_1.3) for package: pcre-8.32-17.el7.i686
[app1][DEBUG ] --> Processing Dependency: libstdc++.so.6 for package: pcre-8.32-17.el7.i686
[app1][DEBUG ] ---> Package pcre.x86_64 0:8.32-17.el7 will be an update
[app1][DEBUG ] ---> Package python-backports.x86_64 0:1.0-8.el7 will be installed
[app1][DEBUG ] ---> Package python-paste.noarch 0:1.7.5.1-9.20111221hg1498.el7 will be installed
[app1][DEBUG ] --> Processing Dependency: python-tempita for package: python-paste-1.7.5.1-9.20111221hg1498.el7.noarch
[app1][DEBUG ] ---> Package systemd-sysv.x86_64 0:219-30.el7 will be updated
[app1][DEBUG ] ---> Package systemd-sysv.x86_64 0:219-57.el7_5.3 will be an update
[app1][DEBUG ] ---> Package zlib.i686 0:1.2.7-17.el7 will be installed
[app1][DEBUG ] --> Running transaction check
[app1][DEBUG ] ---> Package audit.x86_64 0:2.6.5-3.el7 will be updated
[app1][DEBUG ] ---> Package audit.x86_64 0:2.8.1-3.el7_5.1 will be an update
[app1][DEBUG ] ---> Package libcap-ng.i686 0:0.7.5-4.el7 will be installed
[app1][DEBUG ] ---> Package libdb-devel.x86_64 0:5.3.21-19.el7 will be updated
[app1][DEBUG ] ---> Package libdb-devel.x86_64 0:5.3.21-24.el7 will be an update
[app1][DEBUG ] ---> Package libdb-utils.x86_64 0:5.3.21-19.el7 will be updated
[app1][DEBUG ] ---> Package libdb-utils.x86_64 0:5.3.21-24.el7 will be an update
[app1][DEBUG ] ---> Package libstdc++.i686 0:4.8.5-28.el7_5.1 will be installed
[app1][DEBUG ] ---> Package pcre-devel.x86_64 0:8.32-15.el7_2.1 will be updated
[app1][DEBUG ] ---> Package pcre-devel.x86_64 0:8.32-17.el7 will be an update
[app1][DEBUG ] ---> Package python-tempita.noarch 0:0.5.1-6.el7 will be installed
[app1][DEBUG ] --> Finished Dependency Resolution
[app1][DEBUG ] 
[app1][DEBUG ] Dependencies Resolved
[app1][DEBUG ] 
[app1][DEBUG ] ================================================================================
[app1][DEBUG ]  Package                      Arch   Version                      Repository
[app1][DEBUG ]                                                                            Size
[app1][DEBUG ] ================================================================================
[app1][DEBUG ] Installing:
[app1][DEBUG ]  ceph                         x86_64 2:12.2.9-0.el7               Ceph    3.0 k
[app1][DEBUG ]  ceph-radosgw                 x86_64 2:12.2.9-0.el7               Ceph    3.8 M
[app1][DEBUG ]  rdma-core                    i686   15-7.el7_5                   updates  48 k
[app1][DEBUG ]      replacing  rdma.noarch 7.3_4.7_rc2-5.el7
[app1][DEBUG ]  rdma-core                    x86_64 15-7.el7_5                   updates  48 k
[app1][DEBUG ]      replacing  rdma.noarch 7.3_4.7_rc2-5.el7
[app1][DEBUG ] Installing for dependencies:
[app1][DEBUG ]  audit-libs                   i686   2.8.1-3.el7_5.1              updates 100 k
[app1][DEBUG ]  bzip2-libs                   i686   1.0.6-13.el7                 base     40 k
[app1][DEBUG ]  ceph-base                    x86_64 2:12.2.9-0.el7               Ceph    4.0 M
[app1][DEBUG ]  ceph-common                  x86_64 2:12.2.9-0.el7               Ceph     15 M
[app1][DEBUG ]  ceph-mds                     x86_64 2:12.2.9-0.el7               Ceph    3.6 M
[app1][DEBUG ]  ceph-mgr                     x86_64 2:12.2.9-0.el7               Ceph    3.6 M
[app1][DEBUG ]  ceph-mon                     x86_64 2:12.2.9-0.el7               Ceph    5.1 M
[app1][DEBUG ]  ceph-osd                     x86_64 2:12.2.9-0.el7               Ceph     13 M
[app1][DEBUG ]  ceph-selinux                 x86_64 2:12.2.9-0.el7               Ceph     20 k
[app1][DEBUG ]  cracklib                     i686   2.9.0-11.el7                 base     79 k
[app1][DEBUG ]  cryptsetup                   x86_64 1.7.4-4.el7                  base    128 k
[app1][DEBUG ]  elfutils-default-yama-scope  noarch 0.170-4.el7                  base     31 k
[app1][DEBUG ]  elfutils-libelf              i686   0.170-4.el7                  base    199 k
[app1][DEBUG ]  elfutils-libs                i686   0.170-4.el7                  base    288 k
[app1][DEBUG ]  fuse-libs                    x86_64 2.9.2-10.el7                 base     93 k
[app1][DEBUG ]  gdisk                        x86_64 0.8.6-5.el7                  base    187 k
[app1][DEBUG ]  leveldb                      x86_64 1.12.0-11.el7                epel    161 k
[app1][DEBUG ]  libattr                      i686   2.4.46-13.el7                base     18 k
[app1][DEBUG ]  libbabeltrace                x86_64 1.2.4-3.el7                  epel    147 k
[app1][DEBUG ]  libcap                       i686   2.22-9.el7                   base     48 k
[app1][DEBUG ]  libcap-ng                    i686   0.7.5-4.el7                  base     24 k
[app1][DEBUG ]  libcephfs2                   x86_64 2:12.2.9-0.el7               Ceph    435 k
[app1][DEBUG ]  libdb                        i686   5.3.21-24.el7                base    731 k
[app1][DEBUG ]  libgcc                       i686   4.8.5-28.el7_5.1             updates 108 k
[app1][DEBUG ]  libgcrypt                    i686   1.5.3-14.el7                 base    266 k
[app1][DEBUG ]  libgpg-error                 i686   1.12-3.el7                   base     87 k
[app1][DEBUG ]  libibverbs                   x86_64 15-7.el7_5                   updates 224 k
[app1][DEBUG ]  librados2                    x86_64 2:12.2.9-0.el7               Ceph    2.9 M
[app1][DEBUG ]  libradosstriper1             x86_64 2:12.2.9-0.el7               Ceph    330 k
[app1][DEBUG ]  librbd1                      x86_64 2:12.2.9-0.el7               Ceph    1.1 M
[app1][DEBUG ]  librgw2                      x86_64 2:12.2.9-0.el7               Ceph    1.7 M
[app1][DEBUG ]  libselinux                   i686   2.5-12.el7                   base    166 k
[app1][DEBUG ]  libsepol                     i686   2.5-8.1.el7                  base    293 k
[app1][DEBUG ]  libstdc++                    i686   4.8.5-28.el7_5.1             updates 317 k
[app1][DEBUG ]  lttng-ust                    x86_64 2.4.1-4.el7                  epel    176 k
[app1][DEBUG ]  lz4                          i686   1.7.5-2.el7                  base    111 k
[app1][DEBUG ]  lz4                          x86_64 1.7.5-2.el7                  base     98 k
[app1][DEBUG ]  pam                          i686   1.1.8-22.el7                 base    717 k
[app1][DEBUG ]  pcre                         i686   8.32-17.el7                  base    420 k
[app1][DEBUG ]  psmisc                       x86_64 22.20-15.el7                 base    141 k
[app1][DEBUG ]  pyOpenSSL                    x86_64 0.13.1-3.el7                 base    133 k
[app1][DEBUG ]  python-babel                 noarch 0.9.6-8.el7                  base    1.4 M
[app1][DEBUG ]  python-backports             x86_64 1.0-8.el7                    base    5.8 k
[app1][DEBUG ]  python-backports-ssl_match_hostname
[app1][DEBUG ]                               noarch 3.5.0.1-1.el7                base     13 k
[app1][DEBUG ]  python-beaker                noarch 1.5.4-10.el7                 base     80 k
[app1][DEBUG ]  python-cephfs                x86_64 2:12.2.9-0.el7               Ceph     83 k
[app1][DEBUG ]  python-cherrypy              noarch 3.2.2-4.el7                  base    422 k
[app1][DEBUG ]  python-flask                 noarch 1:0.10.1-4.el7               extras  204 k
[app1][DEBUG ]  python-ipaddress             noarch 1.0.16-2.el7                 base     34 k
[app1][DEBUG ]  python-itsdangerous          noarch 0.23-2.el7                   extras   24 k
[app1][DEBUG ]  python-jinja2                noarch 2.7.2-2.el7                  base    515 k
[app1][DEBUG ]  python-mako                  noarch 0.8.1-2.el7                  base    307 k
[app1][DEBUG ]  python-markupsafe            x86_64 0.11-10.el7                  base     25 k
[app1][DEBUG ]  python-paste                 noarch 1.7.5.1-9.20111221hg1498.el7 base    866 k
[app1][DEBUG ]  python-pecan                 noarch 0.4.5-2.el7                  epel    255 k
[app1][DEBUG ]  python-prettytable           noarch 0.7.2-3.el7                  base     37 k
[app1][DEBUG ]  python-rados                 x86_64 2:12.2.9-0.el7               Ceph    175 k
[app1][DEBUG ]  python-rbd                   x86_64 2:12.2.9-0.el7               Ceph    106 k
[app1][DEBUG ]  python-requests              noarch 2.6.0-1.el7_1                base     94 k
[app1][DEBUG ]  python-rgw                   x86_64 2:12.2.9-0.el7               Ceph     73 k
[app1][DEBUG ]  python-setuptools            noarch 0.9.8-7.el7                  base    397 k
[app1][DEBUG ]  python-simplegeneric         noarch 0.8-7.el7                    epel     12 k
[app1][DEBUG ]  python-singledispatch        noarch 3.4.0.2-2.el7                epel     18 k
[app1][DEBUG ]  python-six                   noarch 1.9.0-2.el7                  base     29 k
[app1][DEBUG ]  python-tempita               noarch 0.5.1-6.el7                  base     33 k
[app1][DEBUG ]  python-urllib3               noarch 1.10.2-5.el7                 base    102 k
[app1][DEBUG ]  python-webob                 noarch 1.2.3-7.el7                  base    202 k
[app1][DEBUG ]  python-webtest               noarch 1.3.4-6.el7                  base    102 k
[app1][DEBUG ]  python-werkzeug              noarch 0.9.1-2.el7                  extras  562 k
[app1][DEBUG ]  systemd-libs                 i686   219-57.el7_5.3               updates 408 k
[app1][DEBUG ]  userspace-rcu                x86_64 0.7.16-1.el7                 epel     73 k
[app1][DEBUG ]  xz-libs                      i686   5.2.2-1.el7                  base    109 k
[app1][DEBUG ]  zlib                         i686   1.2.7-17.el7                 base     91 k
[app1][DEBUG ] Updating for dependencies:
[app1][DEBUG ]  audit                        x86_64 2.8.1-3.el7_5.1              updates 247 k
[app1][DEBUG ]  audit-libs                   x86_64 2.8.1-3.el7_5.1              updates  99 k
[app1][DEBUG ]  cryptsetup-libs              x86_64 1.7.4-4.el7                  base    223 k
[app1][DEBUG ]  elfutils-libelf              x86_64 0.170-4.el7                  base    195 k
[app1][DEBUG ]  elfutils-libs                x86_64 0.170-4.el7                  base    267 k
[app1][DEBUG ]  libattr                      x86_64 2.4.46-13.el7                base     18 k
[app1][DEBUG ]  libcap                       x86_64 2.22-9.el7                   base     47 k
[app1][DEBUG ]  libdb                        x86_64 5.3.21-24.el7                base    720 k
[app1][DEBUG ]  libdb-devel                  x86_64 5.3.21-24.el7                base     38 k
[app1][DEBUG ]  libdb-utils                  x86_64 5.3.21-24.el7                base    132 k
[app1][DEBUG ]  libgcrypt                    x86_64 1.5.3-14.el7                 base    263 k
[app1][DEBUG ]  libgudev1                    x86_64 219-57.el7_5.3               updates  92 k
[app1][DEBUG ]  pam                          x86_64 1.1.8-22.el7                 base    720 k
[app1][DEBUG ]  pcre                         x86_64 8.32-17.el7                  base    422 k
[app1][DEBUG ]  pcre-devel                   x86_64 8.32-17.el7                  base    480 k
[app1][DEBUG ]  policycoreutils              x86_64 2.5-22.el7                   base    867 k
[app1][DEBUG ]  selinux-policy               noarch 3.13.1-192.el7_5.6           updates 453 k
[app1][DEBUG ]  selinux-policy-targeted      noarch 3.13.1-192.el7_5.6           updates 6.6 M
[app1][DEBUG ]  systemd                      x86_64 219-57.el7_5.3               updates 5.0 M
[app1][DEBUG ]  systemd-libs                 x86_64 219-57.el7_5.3               updates 402 k
[app1][DEBUG ]  systemd-sysv                 x86_64 219-57.el7_5.3               updates  80 k
[app1][DEBUG ] 
[app1][DEBUG ] Transaction Summary
[app1][DEBUG ] ================================================================================
[app1][DEBUG ] Install  4 Packages (+73 Dependent packages)
[app1][DEBUG ] Upgrade             ( 21 Dependent packages)
[app1][DEBUG ] 
[app1][DEBUG ] Total download size: 84 M
[app1][DEBUG ] Downloading packages:
[app1][DEBUG ] Delta RPMs disabled because /usr/bin/applydeltarpm not installed.
[app1][WARNIN] No data was received after 300 seconds, disconnecting...
[app1][INFO  ] Running command: ceph --version
[app1][ERROR ] Traceback (most recent call last):
[app1][ERROR ]   File "/usr/lib/python2.7/site-packages/ceph_deploy/lib/vendor/remoto/process.py", line 119, in run
[app1][ERROR ]     reporting(conn, result, timeout)
[app1][ERROR ]   File "/usr/lib/python2.7/site-packages/ceph_deploy/lib/vendor/remoto/log.py", line 13, in reporting
[app1][ERROR ]     received = result.receive(timeout)
[app1][ERROR ]   File "/usr/lib/python2.7/site-packages/ceph_deploy/lib/vendor/remoto/lib/vendor/execnet/gateway_base.py", line 704, in receive
[app1][ERROR ]     raise self._getremoteerror() or EOFError()
[app1][ERROR ] RemoteError: Traceback (most recent call last):
[app1][ERROR ]   File "/usr/lib/python2.7/site-packages/ceph_deploy/lib/vendor/remoto/lib/vendor/execnet/gateway_base.py", line 1036, in executetask
[app1][ERROR ]     function(channel, **kwargs)
[app1][ERROR ]   File "<remote exec>", line 12, in _remote_run
[app1][ERROR ]   File "/usr/lib64/python2.7/subprocess.py", line 711, in __init__
[app1][ERROR ]     errread, errwrite)
[app1][ERROR ]   File "/usr/lib64/python2.7/subprocess.py", line 1327, in _execute_child
[app1][ERROR ]     raise child_exception
[app1][ERROR ] OSError: [Errno 2] No such file or directory
[app1][ERROR ] 
[app1][ERROR ] 
[ceph_deploy][ERROR ] RuntimeError: Failed to execute command: ceph --version

[root@app1 ceph]# ceph --version
ceph version 12.2.9 (9e300932ef8a8916fb3fda78c58691a6ab0f4217) luminous (stable)
You have new mail in /var/spool/mail/root
[root@app1 ceph]# 
[root@app1 ceph]# 
[root@app1 ceph]# ceph -v
ceph version 12.2.9 (9e300932ef8a8916fb3fda78c58691a6ab0f4217) luminous (stable)
[root@app1 ceph]# 
[root@app1 ceph]# rpm -ql ceph
(contains no files)
[root@app1 ceph]# 
[root@app1 ceph]# 
[root@app1 ceph]# 
[root@app1 ceph]# rpm -ql ceph-radosgw
/usr/bin/radosgw
/usr/bin/radosgw-es
/usr/bin/radosgw-object-expirer
/usr/bin/radosgw-token
/usr/lib/systemd/system/ceph-radosgw.target
/usr/lib/systemd/system/ceph-radosgw@.service
/usr/share/man/man8/radosgw.8.gz
/var/lib/ceph/radosgw
[root@app1 ceph]# 
[root@app1 ceph]# rpm -ql rdma-core
/etc/modprobe.d/mlx4.conf
/etc/modprobe.d/truescale.conf
/etc/rdma
/etc/rdma/ibacm_opts.cfg
/etc/rdma/mlx4.conf
/etc/rdma/modules
/etc/rdma/modules/infiniband.conf
/etc/rdma/modules/iwarp.conf
/etc/rdma/modules/iwpmd.conf
/etc/rdma/modules/opa.conf
/etc/rdma/modules/rdma.conf
/etc/rdma/modules/roce.conf
/etc/rdma/modules/srp_daemon.conf
/etc/rdma/rdma.conf
/etc/rdma/sriov-vfs
/etc/sysconfig/network-scripts/ifdown-ib
/etc/sysconfig/network-scripts/ifup-ib
/etc/udev/rules.d/70-persistent-ipoib.rules
/usr/lib/dracut/modules.d/05rdma
/usr/lib/dracut/modules.d/05rdma/module-setup.sh
/usr/lib/modprobe.d/libmlx4.conf
/usr/lib/systemd/system/rdma-hw.target
/usr/lib/systemd/system/rdma-load-modules@.service
/usr/lib/systemd/system/rdma-ndd.service
/usr/lib/systemd/system/rdma.service
/usr/lib/udev/rules.d/60-rdma-ndd.rules
/usr/lib/udev/rules.d/60-srp_daemon.rules
/usr/lib/udev/rules.d/75-rdma-description.rules
/usr/lib/udev/rules.d/90-iwpmd.rules
/usr/lib/udev/rules.d/90-rdma-hw-modules.rules
/usr/lib/udev/rules.d/90-rdma-ulp-modules.rules
/usr/lib/udev/rules.d/90-rdma-umad.rules
/usr/lib/udev/rules.d/98-rdma.rules
/usr/libexec/mlx4-setup.sh
/usr/libexec/rdma-init-kernel
/usr/libexec/rdma-set-sriov-vf
/usr/libexec/truescale-serdes.cmds
/usr/sbin/rdma-ndd
/usr/share/doc/rdma-core-15
/usr/share/doc/rdma-core-15/README.md
/usr/share/doc/rdma-core-15/udev.md
/usr/share/licenses/rdma-core-15
/usr/share/licenses/rdma-core-15/COPYING.BSD_FB
/usr/share/licenses/rdma-core-15/COPYING.BSD_MIT
/usr/share/licenses/rdma-core-15/COPYING.GPL2
/usr/share/licenses/rdma-core-15/COPYING.md
/usr/share/man/man8/rdma-ndd.8.gz
/etc/modprobe.d/mlx4.conf
/etc/modprobe.d/truescale.conf
/etc/rdma
/etc/rdma/ibacm_opts.cfg
/etc/rdma/mlx4.conf
/etc/rdma/modules
/etc/rdma/modules/infiniband.conf
/etc/rdma/modules/iwarp.conf
/etc/rdma/modules/iwpmd.conf
/etc/rdma/modules/opa.conf
/etc/rdma/modules/rdma.conf
/etc/rdma/modules/roce.conf
/etc/rdma/modules/srp_daemon.conf
/etc/rdma/rdma.conf
/etc/rdma/sriov-vfs
/etc/sysconfig/network-scripts/ifdown-ib
/etc/sysconfig/network-scripts/ifup-ib
/etc/udev/rules.d/70-persistent-ipoib.rules
/usr/lib/dracut/modules.d/05rdma
/usr/lib/dracut/modules.d/05rdma/module-setup.sh
/usr/lib/modprobe.d/libmlx4.conf
/usr/lib/systemd/system/rdma-hw.target
/usr/lib/systemd/system/rdma-load-modules@.service
/usr/lib/systemd/system/rdma-ndd.service
/usr/lib/systemd/system/rdma.service
/usr/lib/udev/rules.d/60-rdma-ndd.rules
/usr/lib/udev/rules.d/60-srp_daemon.rules
/usr/lib/udev/rules.d/75-rdma-description.rules
/usr/lib/udev/rules.d/90-iwpmd.rules
/usr/lib/udev/rules.d/90-rdma-hw-modules.rules
/usr/lib/udev/rules.d/90-rdma-ulp-modules.rules
/usr/lib/udev/rules.d/90-rdma-umad.rules
/usr/lib/udev/rules.d/98-rdma.rules
/usr/libexec/mlx4-setup.sh
/usr/libexec/rdma-init-kernel
/usr/libexec/rdma-set-sriov-vf
/usr/libexec/truescale-serdes.cmds
/usr/sbin/rdma-ndd
/usr/share/doc/rdma-core-15
/usr/share/doc/rdma-core-15/README.md
/usr/share/doc/rdma-core-15/udev.md
/usr/share/licenses/rdma-core-15
/usr/share/licenses/rdma-core-15/COPYING.BSD_FB
/usr/share/licenses/rdma-core-15/COPYING.BSD_MIT
/usr/share/licenses/rdma-core-15/COPYING.GPL2
/usr/share/licenses/rdma-core-15/COPYING.md
/usr/share/man/man8/rdma-ndd.8.gz
[root@app1 ceph]# 

#############################################
#############################################
#############################################
#############################################
#############################################
#############################################

```

