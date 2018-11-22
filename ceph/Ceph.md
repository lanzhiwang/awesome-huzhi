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
[root@app1 ~]# rpm -ql ceph-base
/etc/logrotate.d/ceph
/etc/sysconfig/ceph
/usr/bin/ceph-detect-init
/usr/bin/ceph-kvstore-tool
/usr/bin/ceph-run
/usr/bin/crushtool
/usr/bin/monmaptool
/usr/bin/osdmaptool
/usr/lib/ceph
/usr/lib/ceph/ceph_common.sh
/usr/lib/python2.7/site-packages/ceph_detect_init
/usr/lib/python2.7/site-packages/ceph_detect_init-1.0.1-py2.7.egg-info
/usr/lib/python2.7/site-packages/ceph_detect_init-1.0.1-py2.7.egg-info/PKG-INFO
/usr/lib/python2.7/site-packages/ceph_detect_init-1.0.1-py2.7.egg-info/SOURCES.txt
/usr/lib/python2.7/site-packages/ceph_detect_init-1.0.1-py2.7.egg-info/dependency_links.txt
/usr/lib/python2.7/site-packages/ceph_detect_init-1.0.1-py2.7.egg-info/entry_points.txt
/usr/lib/python2.7/site-packages/ceph_detect_init-1.0.1-py2.7.egg-info/requires.txt
/usr/lib/python2.7/site-packages/ceph_detect_init-1.0.1-py2.7.egg-info/top_level.txt
/usr/lib/python2.7/site-packages/ceph_detect_init/__init__.py
/usr/lib/python2.7/site-packages/ceph_detect_init/__init__.pyc
/usr/lib/python2.7/site-packages/ceph_detect_init/__init__.pyo
/usr/lib/python2.7/site-packages/ceph_detect_init/alpine
/usr/lib/python2.7/site-packages/ceph_detect_init/alpine/__init__.py
/usr/lib/python2.7/site-packages/ceph_detect_init/alpine/__init__.pyc
/usr/lib/python2.7/site-packages/ceph_detect_init/alpine/__init__.pyo
/usr/lib/python2.7/site-packages/ceph_detect_init/arch
/usr/lib/python2.7/site-packages/ceph_detect_init/arch/__init__.py
/usr/lib/python2.7/site-packages/ceph_detect_init/arch/__init__.pyc
/usr/lib/python2.7/site-packages/ceph_detect_init/arch/__init__.pyo
/usr/lib/python2.7/site-packages/ceph_detect_init/centos
/usr/lib/python2.7/site-packages/ceph_detect_init/centos/__init__.py
/usr/lib/python2.7/site-packages/ceph_detect_init/centos/__init__.pyc
/usr/lib/python2.7/site-packages/ceph_detect_init/centos/__init__.pyo
/usr/lib/python2.7/site-packages/ceph_detect_init/debian
/usr/lib/python2.7/site-packages/ceph_detect_init/debian/__init__.py
/usr/lib/python2.7/site-packages/ceph_detect_init/debian/__init__.pyc
/usr/lib/python2.7/site-packages/ceph_detect_init/debian/__init__.pyo
/usr/lib/python2.7/site-packages/ceph_detect_init/docker
/usr/lib/python2.7/site-packages/ceph_detect_init/docker/__init__.py
/usr/lib/python2.7/site-packages/ceph_detect_init/docker/__init__.pyc
/usr/lib/python2.7/site-packages/ceph_detect_init/docker/__init__.pyo
/usr/lib/python2.7/site-packages/ceph_detect_init/exc.py
/usr/lib/python2.7/site-packages/ceph_detect_init/exc.pyc
/usr/lib/python2.7/site-packages/ceph_detect_init/exc.pyo
/usr/lib/python2.7/site-packages/ceph_detect_init/fedora
/usr/lib/python2.7/site-packages/ceph_detect_init/fedora/__init__.py
/usr/lib/python2.7/site-packages/ceph_detect_init/fedora/__init__.pyc
/usr/lib/python2.7/site-packages/ceph_detect_init/fedora/__init__.pyo
/usr/lib/python2.7/site-packages/ceph_detect_init/freebsd
/usr/lib/python2.7/site-packages/ceph_detect_init/freebsd/__init__.py
/usr/lib/python2.7/site-packages/ceph_detect_init/freebsd/__init__.pyc
/usr/lib/python2.7/site-packages/ceph_detect_init/freebsd/__init__.pyo
/usr/lib/python2.7/site-packages/ceph_detect_init/gentoo
/usr/lib/python2.7/site-packages/ceph_detect_init/gentoo/__init__.py
/usr/lib/python2.7/site-packages/ceph_detect_init/gentoo/__init__.pyc
/usr/lib/python2.7/site-packages/ceph_detect_init/gentoo/__init__.pyo
/usr/lib/python2.7/site-packages/ceph_detect_init/main.py
/usr/lib/python2.7/site-packages/ceph_detect_init/main.pyc
/usr/lib/python2.7/site-packages/ceph_detect_init/main.pyo
/usr/lib/python2.7/site-packages/ceph_detect_init/oraclevms
/usr/lib/python2.7/site-packages/ceph_detect_init/oraclevms/__init__.py
/usr/lib/python2.7/site-packages/ceph_detect_init/oraclevms/__init__.pyc
/usr/lib/python2.7/site-packages/ceph_detect_init/oraclevms/__init__.pyo
/usr/lib/python2.7/site-packages/ceph_detect_init/rhel
/usr/lib/python2.7/site-packages/ceph_detect_init/rhel/__init__.py
/usr/lib/python2.7/site-packages/ceph_detect_init/rhel/__init__.pyc
/usr/lib/python2.7/site-packages/ceph_detect_init/rhel/__init__.pyo
/usr/lib/python2.7/site-packages/ceph_detect_init/suse
/usr/lib/python2.7/site-packages/ceph_detect_init/suse/__init__.py
/usr/lib/python2.7/site-packages/ceph_detect_init/suse/__init__.pyc
/usr/lib/python2.7/site-packages/ceph_detect_init/suse/__init__.pyo
/usr/lib/python2.7/site-packages/ceph_disk
/usr/lib/python2.7/site-packages/ceph_disk-1.0.0-py2.7.egg-info
/usr/lib/python2.7/site-packages/ceph_disk-1.0.0-py2.7.egg-info/PKG-INFO
/usr/lib/python2.7/site-packages/ceph_disk-1.0.0-py2.7.egg-info/SOURCES.txt
/usr/lib/python2.7/site-packages/ceph_disk-1.0.0-py2.7.egg-info/dependency_links.txt
/usr/lib/python2.7/site-packages/ceph_disk-1.0.0-py2.7.egg-info/entry_points.txt
/usr/lib/python2.7/site-packages/ceph_disk-1.0.0-py2.7.egg-info/requires.txt
/usr/lib/python2.7/site-packages/ceph_disk-1.0.0-py2.7.egg-info/top_level.txt
/usr/lib/python2.7/site-packages/ceph_disk/__init__.py
/usr/lib/python2.7/site-packages/ceph_disk/__init__.pyc
/usr/lib/python2.7/site-packages/ceph_disk/__init__.pyo
/usr/lib/python2.7/site-packages/ceph_disk/main.py
/usr/lib/python2.7/site-packages/ceph_disk/main.pyc
/usr/lib/python2.7/site-packages/ceph_disk/main.pyo
/usr/lib/python2.7/site-packages/ceph_volume
/usr/lib/python2.7/site-packages/ceph_volume-1.0.0-py2.7.egg-info
/usr/lib/python2.7/site-packages/ceph_volume-1.0.0-py2.7.egg-info/PKG-INFO
/usr/lib/python2.7/site-packages/ceph_volume-1.0.0-py2.7.egg-info/SOURCES.txt
/usr/lib/python2.7/site-packages/ceph_volume-1.0.0-py2.7.egg-info/dependency_links.txt
/usr/lib/python2.7/site-packages/ceph_volume-1.0.0-py2.7.egg-info/not-zip-safe
/usr/lib/python2.7/site-packages/ceph_volume-1.0.0-py2.7.egg-info/top_level.txt
/usr/lib/python2.7/site-packages/ceph_volume/__init__.py
/usr/lib/python2.7/site-packages/ceph_volume/__init__.pyc
/usr/lib/python2.7/site-packages/ceph_volume/__init__.pyo
/usr/lib/python2.7/site-packages/ceph_volume/api
/usr/lib/python2.7/site-packages/ceph_volume/api/__init__.py
/usr/lib/python2.7/site-packages/ceph_volume/api/__init__.pyc
/usr/lib/python2.7/site-packages/ceph_volume/api/__init__.pyo
/usr/lib/python2.7/site-packages/ceph_volume/api/lvm.py
/usr/lib/python2.7/site-packages/ceph_volume/api/lvm.pyc
/usr/lib/python2.7/site-packages/ceph_volume/api/lvm.pyo
/usr/lib/python2.7/site-packages/ceph_volume/configuration.py
/usr/lib/python2.7/site-packages/ceph_volume/configuration.pyc
/usr/lib/python2.7/site-packages/ceph_volume/configuration.pyo
/usr/lib/python2.7/site-packages/ceph_volume/decorators.py
/usr/lib/python2.7/site-packages/ceph_volume/decorators.pyc
/usr/lib/python2.7/site-packages/ceph_volume/decorators.pyo
/usr/lib/python2.7/site-packages/ceph_volume/devices
/usr/lib/python2.7/site-packages/ceph_volume/devices/__init__.py
/usr/lib/python2.7/site-packages/ceph_volume/devices/__init__.pyc
/usr/lib/python2.7/site-packages/ceph_volume/devices/__init__.pyo
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/__init__.py
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/__init__.pyc
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/__init__.pyo
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/activate.py
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/activate.pyc
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/activate.pyo
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/batch.py
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/batch.pyc
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/batch.pyo
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/common.py
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/common.pyc
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/common.pyo
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/create.py
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/create.pyc
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/create.pyo
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/listing.py
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/listing.pyc
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/listing.pyo
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/main.py
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/main.pyc
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/main.pyo
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/prepare.py
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/prepare.pyc
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/prepare.pyo
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/strategies
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/strategies/__init__.py
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/strategies/__init__.pyc
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/strategies/__init__.pyo
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/strategies/bluestore.py
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/strategies/bluestore.pyc
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/strategies/bluestore.pyo
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/strategies/filestore.py
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/strategies/filestore.pyc
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/strategies/filestore.pyo
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/strategies/validators.py
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/strategies/validators.pyc
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/strategies/validators.pyo
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/trigger.py
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/trigger.pyc
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/trigger.pyo
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/zap.py
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/zap.pyc
/usr/lib/python2.7/site-packages/ceph_volume/devices/lvm/zap.pyo
/usr/lib/python2.7/site-packages/ceph_volume/devices/simple
/usr/lib/python2.7/site-packages/ceph_volume/devices/simple/__init__.py
/usr/lib/python2.7/site-packages/ceph_volume/devices/simple/__init__.pyc
/usr/lib/python2.7/site-packages/ceph_volume/devices/simple/__init__.pyo
/usr/lib/python2.7/site-packages/ceph_volume/devices/simple/activate.py
/usr/lib/python2.7/site-packages/ceph_volume/devices/simple/activate.pyc
/usr/lib/python2.7/site-packages/ceph_volume/devices/simple/activate.pyo
/usr/lib/python2.7/site-packages/ceph_volume/devices/simple/main.py
/usr/lib/python2.7/site-packages/ceph_volume/devices/simple/main.pyc
/usr/lib/python2.7/site-packages/ceph_volume/devices/simple/main.pyo
/usr/lib/python2.7/site-packages/ceph_volume/devices/simple/scan.py
/usr/lib/python2.7/site-packages/ceph_volume/devices/simple/scan.pyc
/usr/lib/python2.7/site-packages/ceph_volume/devices/simple/scan.pyo
/usr/lib/python2.7/site-packages/ceph_volume/devices/simple/trigger.py
/usr/lib/python2.7/site-packages/ceph_volume/devices/simple/trigger.pyc
/usr/lib/python2.7/site-packages/ceph_volume/devices/simple/trigger.pyo
/usr/lib/python2.7/site-packages/ceph_volume/exceptions.py
/usr/lib/python2.7/site-packages/ceph_volume/exceptions.pyc
/usr/lib/python2.7/site-packages/ceph_volume/exceptions.pyo
/usr/lib/python2.7/site-packages/ceph_volume/log.py
/usr/lib/python2.7/site-packages/ceph_volume/log.pyc
/usr/lib/python2.7/site-packages/ceph_volume/log.pyo
/usr/lib/python2.7/site-packages/ceph_volume/main.py
/usr/lib/python2.7/site-packages/ceph_volume/main.pyc
/usr/lib/python2.7/site-packages/ceph_volume/main.pyo
/usr/lib/python2.7/site-packages/ceph_volume/process.py
/usr/lib/python2.7/site-packages/ceph_volume/process.pyc
/usr/lib/python2.7/site-packages/ceph_volume/process.pyo
/usr/lib/python2.7/site-packages/ceph_volume/systemd
/usr/lib/python2.7/site-packages/ceph_volume/systemd/__init__.py
/usr/lib/python2.7/site-packages/ceph_volume/systemd/__init__.pyc
/usr/lib/python2.7/site-packages/ceph_volume/systemd/__init__.pyo
/usr/lib/python2.7/site-packages/ceph_volume/systemd/main.py
/usr/lib/python2.7/site-packages/ceph_volume/systemd/main.pyc
/usr/lib/python2.7/site-packages/ceph_volume/systemd/main.pyo
/usr/lib/python2.7/site-packages/ceph_volume/systemd/systemctl.py
/usr/lib/python2.7/site-packages/ceph_volume/systemd/systemctl.pyc
/usr/lib/python2.7/site-packages/ceph_volume/systemd/systemctl.pyo
/usr/lib/python2.7/site-packages/ceph_volume/terminal.py
/usr/lib/python2.7/site-packages/ceph_volume/terminal.pyc
/usr/lib/python2.7/site-packages/ceph_volume/terminal.pyo
/usr/lib/python2.7/site-packages/ceph_volume/tests
/usr/lib/python2.7/site-packages/ceph_volume/tests/__init__.py
/usr/lib/python2.7/site-packages/ceph_volume/tests/__init__.pyc
/usr/lib/python2.7/site-packages/ceph_volume/tests/__init__.pyo
/usr/lib/python2.7/site-packages/ceph_volume/tests/conftest.py
/usr/lib/python2.7/site-packages/ceph_volume/tests/conftest.pyc
/usr/lib/python2.7/site-packages/ceph_volume/tests/conftest.pyo
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/__init__.py
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/__init__.pyc
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/__init__.pyo
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/__init__.py
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/__init__.pyc
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/__init__.pyo
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/strategies
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/strategies/__init__.py
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/strategies/__init__.pyc
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/strategies/__init__.pyo
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/strategies/test_bluestore.py
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/strategies/test_bluestore.pyc
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/strategies/test_bluestore.pyo
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/strategies/test_filestore.py
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/strategies/test_filestore.pyc
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/strategies/test_filestore.pyo
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/strategies/test_validate.py
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/strategies/test_validate.pyc
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/strategies/test_validate.pyo
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/test_activate.py
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/test_activate.pyc
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/test_activate.pyo
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/test_batch.py
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/test_batch.pyc
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/test_batch.pyo
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/test_create.py
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/test_create.pyc
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/test_create.pyo
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/test_listing.py
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/test_listing.pyc
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/test_listing.pyo
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/test_prepare.py
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/test_prepare.pyc
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/test_prepare.pyo
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/test_trigger.py
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/test_trigger.pyc
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/lvm/test_trigger.pyo
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/test_zap.py
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/test_zap.pyc
/usr/lib/python2.7/site-packages/ceph_volume/tests/devices/test_zap.pyo
/usr/lib/python2.7/site-packages/ceph_volume/tests/test_configuration.py
/usr/lib/python2.7/site-packages/ceph_volume/tests/test_configuration.pyc
/usr/lib/python2.7/site-packages/ceph_volume/tests/test_configuration.pyo
/usr/lib/python2.7/site-packages/ceph_volume/tests/test_decorators.py
/usr/lib/python2.7/site-packages/ceph_volume/tests/test_decorators.pyc
/usr/lib/python2.7/site-packages/ceph_volume/tests/test_decorators.pyo
/usr/lib/python2.7/site-packages/ceph_volume/tests/test_main.py
/usr/lib/python2.7/site-packages/ceph_volume/tests/test_main.pyc
/usr/lib/python2.7/site-packages/ceph_volume/tests/test_main.pyo
/usr/lib/python2.7/site-packages/ceph_volume/tests/test_process.py
/usr/lib/python2.7/site-packages/ceph_volume/tests/test_process.pyc
/usr/lib/python2.7/site-packages/ceph_volume/tests/test_process.pyo
/usr/lib/python2.7/site-packages/ceph_volume/tests/test_terminal.py
/usr/lib/python2.7/site-packages/ceph_volume/tests/test_terminal.pyc
/usr/lib/python2.7/site-packages/ceph_volume/tests/test_terminal.pyo
/usr/lib/python2.7/site-packages/ceph_volume/util
/usr/lib/python2.7/site-packages/ceph_volume/util/__init__.py
/usr/lib/python2.7/site-packages/ceph_volume/util/__init__.pyc
/usr/lib/python2.7/site-packages/ceph_volume/util/__init__.pyo
/usr/lib/python2.7/site-packages/ceph_volume/util/arg_validators.py
/usr/lib/python2.7/site-packages/ceph_volume/util/arg_validators.pyc
/usr/lib/python2.7/site-packages/ceph_volume/util/arg_validators.pyo
/usr/lib/python2.7/site-packages/ceph_volume/util/constants.py
/usr/lib/python2.7/site-packages/ceph_volume/util/constants.pyc
/usr/lib/python2.7/site-packages/ceph_volume/util/constants.pyo
/usr/lib/python2.7/site-packages/ceph_volume/util/device.py
/usr/lib/python2.7/site-packages/ceph_volume/util/device.pyc
/usr/lib/python2.7/site-packages/ceph_volume/util/device.pyo
/usr/lib/python2.7/site-packages/ceph_volume/util/disk.py
/usr/lib/python2.7/site-packages/ceph_volume/util/disk.pyc
/usr/lib/python2.7/site-packages/ceph_volume/util/disk.pyo
/usr/lib/python2.7/site-packages/ceph_volume/util/encryption.py
/usr/lib/python2.7/site-packages/ceph_volume/util/encryption.pyc
/usr/lib/python2.7/site-packages/ceph_volume/util/encryption.pyo
/usr/lib/python2.7/site-packages/ceph_volume/util/prepare.py
/usr/lib/python2.7/site-packages/ceph_volume/util/prepare.pyc
/usr/lib/python2.7/site-packages/ceph_volume/util/prepare.pyo
/usr/lib/python2.7/site-packages/ceph_volume/util/system.py
/usr/lib/python2.7/site-packages/ceph_volume/util/system.pyc
/usr/lib/python2.7/site-packages/ceph_volume/util/system.pyo
/usr/lib/python2.7/site-packages/ceph_volume/util/templates.py
/usr/lib/python2.7/site-packages/ceph_volume/util/templates.pyc
/usr/lib/python2.7/site-packages/ceph_volume/util/templates.pyo
/usr/lib/systemd/system-preset/50-ceph.preset
/usr/lib/systemd/system/ceph-disk@.service
/usr/lib/systemd/system/ceph.target
/usr/lib64/ceph
/usr/lib64/ceph/compressor
/usr/lib64/ceph/compressor/libceph_snappy.so
/usr/lib64/ceph/compressor/libceph_snappy.so.2
/usr/lib64/ceph/compressor/libceph_snappy.so.2.0.0
/usr/lib64/ceph/compressor/libceph_zlib.so
/usr/lib64/ceph/compressor/libceph_zlib.so.2
/usr/lib64/ceph/compressor/libceph_zlib.so.2.0.0
/usr/lib64/ceph/compressor/libceph_zstd.so
/usr/lib64/ceph/compressor/libceph_zstd.so.2
/usr/lib64/ceph/compressor/libceph_zstd.so.2.0.0
/usr/lib64/ceph/crypto
/usr/lib64/ceph/crypto/libceph_crypto_isal.so
/usr/lib64/ceph/crypto/libceph_crypto_isal.so.1
/usr/lib64/ceph/crypto/libceph_crypto_isal.so.1.0.0
/usr/lib64/ceph/erasure-code
/usr/lib64/ceph/erasure-code/libec_isa.so
/usr/lib64/ceph/erasure-code/libec_jerasure.so
/usr/lib64/ceph/erasure-code/libec_jerasure_generic.so
/usr/lib64/ceph/erasure-code/libec_jerasure_sse3.so
/usr/lib64/ceph/erasure-code/libec_jerasure_sse4.so
/usr/lib64/ceph/erasure-code/libec_lrc.so
/usr/lib64/ceph/erasure-code/libec_shec.so
/usr/lib64/ceph/erasure-code/libec_shec_generic.so
/usr/lib64/ceph/erasure-code/libec_shec_sse3.so
/usr/lib64/ceph/erasure-code/libec_shec_sse4.so
/usr/lib64/libos_tp.so
/usr/lib64/libos_tp.so.1
/usr/lib64/libos_tp.so.1.0.0
/usr/lib64/libosd_tp.so
/usr/lib64/libosd_tp.so.1
/usr/lib64/libosd_tp.so.1.0.0
/usr/lib64/rados-classes
/usr/lib64/rados-classes/libcls_cephfs.so
/usr/lib64/rados-classes/libcls_cephfs.so.1
/usr/lib64/rados-classes/libcls_cephfs.so.1.0.0
/usr/lib64/rados-classes/libcls_hello.so
/usr/lib64/rados-classes/libcls_hello.so.1
/usr/lib64/rados-classes/libcls_hello.so.1.0.0
/usr/lib64/rados-classes/libcls_journal.so
/usr/lib64/rados-classes/libcls_journal.so.1
/usr/lib64/rados-classes/libcls_journal.so.1.0.0
/usr/lib64/rados-classes/libcls_kvs.so
/usr/lib64/rados-classes/libcls_kvs.so.1
/usr/lib64/rados-classes/libcls_kvs.so.1.0.0
/usr/lib64/rados-classes/libcls_lock.so
/usr/lib64/rados-classes/libcls_lock.so.1
/usr/lib64/rados-classes/libcls_lock.so.1.0.0
/usr/lib64/rados-classes/libcls_log.so
/usr/lib64/rados-classes/libcls_log.so.1
/usr/lib64/rados-classes/libcls_log.so.1.0.0
/usr/lib64/rados-classes/libcls_lua.so
/usr/lib64/rados-classes/libcls_lua.so.1
/usr/lib64/rados-classes/libcls_lua.so.1.0.0
/usr/lib64/rados-classes/libcls_numops.so
/usr/lib64/rados-classes/libcls_numops.so.1
/usr/lib64/rados-classes/libcls_numops.so.1.0.0
/usr/lib64/rados-classes/libcls_rbd.so
/usr/lib64/rados-classes/libcls_rbd.so.1
/usr/lib64/rados-classes/libcls_rbd.so.1.0.0
/usr/lib64/rados-classes/libcls_refcount.so
/usr/lib64/rados-classes/libcls_refcount.so.1
/usr/lib64/rados-classes/libcls_refcount.so.1.0.0
/usr/lib64/rados-classes/libcls_replica_log.so
/usr/lib64/rados-classes/libcls_replica_log.so.1
/usr/lib64/rados-classes/libcls_replica_log.so.1.0.0
/usr/lib64/rados-classes/libcls_rgw.so
/usr/lib64/rados-classes/libcls_rgw.so.1
/usr/lib64/rados-classes/libcls_rgw.so.1.0.0
/usr/lib64/rados-classes/libcls_sdk.so
/usr/lib64/rados-classes/libcls_sdk.so.1
/usr/lib64/rados-classes/libcls_sdk.so.1.0.0
/usr/lib64/rados-classes/libcls_statelog.so
/usr/lib64/rados-classes/libcls_statelog.so.1
/usr/lib64/rados-classes/libcls_statelog.so.1.0.0
/usr/lib64/rados-classes/libcls_timeindex.so
/usr/lib64/rados-classes/libcls_timeindex.so.1
/usr/lib64/rados-classes/libcls_timeindex.so.1.0.0
/usr/lib64/rados-classes/libcls_user.so
/usr/lib64/rados-classes/libcls_user.so.1
/usr/lib64/rados-classes/libcls_user.so.1.0.0
/usr/lib64/rados-classes/libcls_version.so
/usr/lib64/rados-classes/libcls_version.so.1
/usr/lib64/rados-classes/libcls_version.so.1.0.0
/usr/sbin/ceph-create-keys
/usr/sbin/ceph-disk
/usr/sbin/rcceph
/usr/share/man/man8/ceph-create-keys.8.gz
/usr/share/man/man8/ceph-deploy.8.gz
/usr/share/man/man8/ceph-detect-init.8.gz
/usr/share/man/man8/ceph-disk.8.gz
/usr/share/man/man8/ceph-kvstore-tool.8.gz
/usr/share/man/man8/ceph-run.8.gz
/usr/share/man/man8/crushtool.8.gz
/usr/share/man/man8/monmaptool.8.gz
/usr/share/man/man8/osdmaptool.8.gz
/var/lib/ceph/bootstrap-mds
/var/lib/ceph/bootstrap-mgr
/var/lib/ceph/bootstrap-osd
/var/lib/ceph/bootstrap-rbd
/var/lib/ceph/bootstrap-rgw
/var/lib/ceph/tmp
[root@app1 ~]# 
[root@app1 ~]# rpm -ql ceph-common 
/etc/bash_completion.d/ceph
/etc/bash_completion.d/rados
/etc/bash_completion.d/radosgw-admin
/etc/bash_completion.d/rbd
/etc/ceph
/etc/ceph/rbdmap
/usr/bin/ceph
/usr/bin/ceph-authtool
/usr/bin/ceph-brag
/usr/bin/ceph-conf
/usr/bin/ceph-crush-location
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
/usr/lib/python2.7/site-packages/ceph_argparse.py
/usr/lib/python2.7/site-packages/ceph_argparse.pyc
/usr/lib/python2.7/site-packages/ceph_argparse.pyo
/usr/lib/python2.7/site-packages/ceph_daemon.py
/usr/lib/python2.7/site-packages/ceph_daemon.pyc
/usr/lib/python2.7/site-packages/ceph_daemon.pyo
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
/usr/share/doc/ceph/COPYING
/usr/share/doc/ceph/sample.ceph.conf
/usr/share/man/man8/ceph-authtool.8.gz
/usr/share/man/man8/ceph-conf.8.gz
/usr/share/man/man8/ceph-dencoder.8.gz
/usr/share/man/man8/ceph-post-file.8.gz
/usr/share/man/man8/ceph-rbdnamer.8.gz
/usr/share/man/man8/ceph-syn.8.gz
/usr/share/man/man8/ceph.8.gz
/usr/share/man/man8/mount.ceph.8.gz
/usr/share/man/man8/rados.8.gz
/usr/share/man/man8/radosgw-admin.8.gz
/usr/share/man/man8/rbd-replay-many.8.gz
/usr/share/man/man8/rbd-replay-prep.8.gz
/usr/share/man/man8/rbd-replay.8.gz
/usr/share/man/man8/rbd.8.gz
/usr/share/man/man8/rbdmap.8.gz
/var/lib/ceph
/var/log/ceph
[root@app1 ~]# 
[root@app1 ~]# rpm -ql ceph-mgr
/usr/bin/ceph-mgr
/usr/lib/systemd/system/ceph-mgr.target
/usr/lib/systemd/system/ceph-mgr@.service
/usr/lib64/ceph/mgr
/usr/lib64/ceph/mgr/.gitignore
/usr/lib64/ceph/mgr/balancer
/usr/lib64/ceph/mgr/balancer/__init__.py
/usr/lib64/ceph/mgr/balancer/__init__.pyc
/usr/lib64/ceph/mgr/balancer/__init__.pyo
/usr/lib64/ceph/mgr/balancer/module.py
/usr/lib64/ceph/mgr/balancer/module.pyc
/usr/lib64/ceph/mgr/balancer/module.pyo
/usr/lib64/ceph/mgr/dashboard
/usr/lib64/ceph/mgr/dashboard/HACKING.rst
/usr/lib64/ceph/mgr/dashboard/README.rst
/usr/lib64/ceph/mgr/dashboard/__init__.py
/usr/lib64/ceph/mgr/dashboard/__init__.pyc
/usr/lib64/ceph/mgr/dashboard/__init__.pyo
/usr/lib64/ceph/mgr/dashboard/base.html
/usr/lib64/ceph/mgr/dashboard/cephfs_clients.py
/usr/lib64/ceph/mgr/dashboard/cephfs_clients.pyc
/usr/lib64/ceph/mgr/dashboard/cephfs_clients.pyo
/usr/lib64/ceph/mgr/dashboard/clients.html
/usr/lib64/ceph/mgr/dashboard/config_options.html
/usr/lib64/ceph/mgr/dashboard/filesystem.html
/usr/lib64/ceph/mgr/dashboard/health.html
/usr/lib64/ceph/mgr/dashboard/module.py
/usr/lib64/ceph/mgr/dashboard/module.pyc
/usr/lib64/ceph/mgr/dashboard/module.pyo
/usr/lib64/ceph/mgr/dashboard/osd_perf.html
/usr/lib64/ceph/mgr/dashboard/osds.html
/usr/lib64/ceph/mgr/dashboard/rbd_iscsi.html
/usr/lib64/ceph/mgr/dashboard/rbd_iscsi.py
/usr/lib64/ceph/mgr/dashboard/rbd_iscsi.pyc
/usr/lib64/ceph/mgr/dashboard/rbd_iscsi.pyo
/usr/lib64/ceph/mgr/dashboard/rbd_ls.py
/usr/lib64/ceph/mgr/dashboard/rbd_ls.pyc
/usr/lib64/ceph/mgr/dashboard/rbd_ls.pyo
/usr/lib64/ceph/mgr/dashboard/rbd_mirroring.html
/usr/lib64/ceph/mgr/dashboard/rbd_mirroring.py
/usr/lib64/ceph/mgr/dashboard/rbd_mirroring.pyc
/usr/lib64/ceph/mgr/dashboard/rbd_mirroring.pyo
/usr/lib64/ceph/mgr/dashboard/rbd_pool.html
/usr/lib64/ceph/mgr/dashboard/remote_view_cache.py
/usr/lib64/ceph/mgr/dashboard/remote_view_cache.pyc
/usr/lib64/ceph/mgr/dashboard/remote_view_cache.pyo
/usr/lib64/ceph/mgr/dashboard/servers.html
/usr/lib64/ceph/mgr/dashboard/standby.html
/usr/lib64/ceph/mgr/dashboard/static
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/.gitignore
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/.jshintrc
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/LICENSE
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/README.md
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/bootstrap
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/bootstrap/css
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/bootstrap/css/bootstrap.min.css
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/bootstrap/css/bootstrap.min.css.map
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/bootstrap/fonts
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/bootstrap/fonts/glyphicons-halflings-regular.woff
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/bootstrap/fonts/glyphicons-halflings-regular.woff2
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/bootstrap/js
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/bootstrap/js/bootstrap.min.js
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/dist
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/dist/css
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/dist/css/AdminLTE.min.css
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/dist/css/skins
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/dist/css/skins/_all-skins.min.css
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/dist/css/skins/skin-black-light.min.css
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/dist/css/skins/skin-black.min.css
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/dist/css/skins/skin-blue-light.min.css
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/dist/css/skins/skin-blue.min.css
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/dist/css/skins/skin-green-light.min.css
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/dist/css/skins/skin-green.min.css
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/dist/css/skins/skin-purple-light.min.css
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/dist/css/skins/skin-purple.min.css
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/dist/css/skins/skin-red-light.min.css
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/dist/css/skins/skin-red.min.css
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/dist/css/skins/skin-yellow-light.min.css
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/dist/css/skins/skin-yellow.min.css
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/dist/img
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/dist/img/boxed-bg.jpg
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/dist/img/boxed-bg.png
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/dist/img/default-50x50.gif
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/dist/img/icons.png
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/dist/js
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/dist/js/app.min.js
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/plugins
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/plugins/chartjs
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/plugins/chartjs/Chart.js
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/plugins/chartjs/Chart.min.js
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/plugins/datatables
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/plugins/datatables/dataTables.bootstrap.min.js
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/plugins/datatables/images
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/plugins/datatables/images/sort_asc.png
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/plugins/datatables/images/sort_asc_disabled.png
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/plugins/datatables/images/sort_both.png
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/plugins/datatables/images/sort_desc.png
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/plugins/datatables/images/sort_desc_disabled.png
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/plugins/datatables/jquery.dataTables.min.css
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/plugins/datatables/jquery.dataTables.min.js
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/plugins/datatables/jquery.dataTables_themeroller.css
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/plugins/ionslider
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/plugins/ionslider/img
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/plugins/ionslider/img/sprite-skin-flat.png
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/plugins/ionslider/img/sprite-skin-nice.png
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/plugins/ionslider/ion.rangeSlider.css
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/plugins/ionslider/ion.rangeSlider.min.js
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/plugins/ionslider/ion.rangeSlider.skinFlat.css
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/plugins/ionslider/ion.rangeSlider.skinNice.css
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/plugins/jQuery
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/plugins/jQuery/jquery-2.2.3.min.js
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/plugins/sparkline
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/plugins/sparkline/jquery.sparkline.js
/usr/lib64/ceph/mgr/dashboard/static/AdminLTE-2.3.7/plugins/sparkline/jquery.sparkline.min.js
/usr/lib64/ceph/mgr/dashboard/static/Ceph_Logo_Standard_RGB_White_120411_fa.png
/usr/lib64/ceph/mgr/dashboard/static/favicon.ico
/usr/lib64/ceph/mgr/dashboard/static/libs
/usr/lib64/ceph/mgr/dashboard/static/libs/Chart.js
/usr/lib64/ceph/mgr/dashboard/static/libs/Chart.js/2.4.0
/usr/lib64/ceph/mgr/dashboard/static/libs/Chart.js/2.4.0/Chart.min.js
/usr/lib64/ceph/mgr/dashboard/static/libs/Chart.js/LICENSE.md
/usr/lib64/ceph/mgr/dashboard/static/libs/font-awesome
/usr/lib64/ceph/mgr/dashboard/static/libs/font-awesome/4.7.0
/usr/lib64/ceph/mgr/dashboard/static/libs/font-awesome/4.7.0/HELP-US-OUT.txt
/usr/lib64/ceph/mgr/dashboard/static/libs/font-awesome/4.7.0/css
/usr/lib64/ceph/mgr/dashboard/static/libs/font-awesome/4.7.0/css/font-awesome.min.css
/usr/lib64/ceph/mgr/dashboard/static/libs/font-awesome/4.7.0/fonts
/usr/lib64/ceph/mgr/dashboard/static/libs/font-awesome/4.7.0/fonts/fontawesome-webfont.woff
/usr/lib64/ceph/mgr/dashboard/static/libs/font-awesome/4.7.0/fonts/fontawesome-webfont.woff2
/usr/lib64/ceph/mgr/dashboard/static/libs/font-awesome/COPYING
/usr/lib64/ceph/mgr/dashboard/static/libs/moment.js
/usr/lib64/ceph/mgr/dashboard/static/libs/moment.js/2.17.1
/usr/lib64/ceph/mgr/dashboard/static/libs/moment.js/2.17.1/moment.min.js
/usr/lib64/ceph/mgr/dashboard/static/libs/rivets
/usr/lib64/ceph/mgr/dashboard/static/libs/rivets/0.9.6
/usr/lib64/ceph/mgr/dashboard/static/libs/rivets/0.9.6/rivets.bundled.min.js
/usr/lib64/ceph/mgr/dashboard/static/libs/underscore.js
/usr/lib64/ceph/mgr/dashboard/static/libs/underscore.js/1.8.3
/usr/lib64/ceph/mgr/dashboard/static/libs/underscore.js/1.8.3/underscore-min.js
/usr/lib64/ceph/mgr/dashboard/static/logo-mini.png
/usr/lib64/ceph/mgr/dashboard/types.py
/usr/lib64/ceph/mgr/dashboard/types.pyc
/usr/lib64/ceph/mgr/dashboard/types.pyo
/usr/lib64/ceph/mgr/influx
/usr/lib64/ceph/mgr/influx/__init__.py
/usr/lib64/ceph/mgr/influx/__init__.pyc
/usr/lib64/ceph/mgr/influx/__init__.pyo
/usr/lib64/ceph/mgr/influx/module.py
/usr/lib64/ceph/mgr/influx/module.pyc
/usr/lib64/ceph/mgr/influx/module.pyo
/usr/lib64/ceph/mgr/localpool
/usr/lib64/ceph/mgr/localpool/__init__.py
/usr/lib64/ceph/mgr/localpool/__init__.pyc
/usr/lib64/ceph/mgr/localpool/__init__.pyo
/usr/lib64/ceph/mgr/localpool/module.py
/usr/lib64/ceph/mgr/localpool/module.pyc
/usr/lib64/ceph/mgr/localpool/module.pyo
/usr/lib64/ceph/mgr/mgr_module.py
/usr/lib64/ceph/mgr/mgr_module.pyc
/usr/lib64/ceph/mgr/mgr_module.pyo
/usr/lib64/ceph/mgr/prometheus
/usr/lib64/ceph/mgr/prometheus/__init__.py
/usr/lib64/ceph/mgr/prometheus/__init__.pyc
/usr/lib64/ceph/mgr/prometheus/__init__.pyo
/usr/lib64/ceph/mgr/prometheus/module.py
/usr/lib64/ceph/mgr/prometheus/module.pyc
/usr/lib64/ceph/mgr/prometheus/module.pyo
/usr/lib64/ceph/mgr/restful
/usr/lib64/ceph/mgr/restful/__init__.py
/usr/lib64/ceph/mgr/restful/__init__.pyc
/usr/lib64/ceph/mgr/restful/__init__.pyo
/usr/lib64/ceph/mgr/restful/api
/usr/lib64/ceph/mgr/restful/api/__init__.py
/usr/lib64/ceph/mgr/restful/api/__init__.pyc
/usr/lib64/ceph/mgr/restful/api/__init__.pyo
/usr/lib64/ceph/mgr/restful/api/config.py
/usr/lib64/ceph/mgr/restful/api/config.pyc
/usr/lib64/ceph/mgr/restful/api/config.pyo
/usr/lib64/ceph/mgr/restful/api/crush.py
/usr/lib64/ceph/mgr/restful/api/crush.pyc
/usr/lib64/ceph/mgr/restful/api/crush.pyo
/usr/lib64/ceph/mgr/restful/api/doc.py
/usr/lib64/ceph/mgr/restful/api/doc.pyc
/usr/lib64/ceph/mgr/restful/api/doc.pyo
/usr/lib64/ceph/mgr/restful/api/mon.py
/usr/lib64/ceph/mgr/restful/api/mon.pyc
/usr/lib64/ceph/mgr/restful/api/mon.pyo
/usr/lib64/ceph/mgr/restful/api/osd.py
/usr/lib64/ceph/mgr/restful/api/osd.pyc
/usr/lib64/ceph/mgr/restful/api/osd.pyo
/usr/lib64/ceph/mgr/restful/api/pool.py
/usr/lib64/ceph/mgr/restful/api/pool.pyc
/usr/lib64/ceph/mgr/restful/api/pool.pyo
/usr/lib64/ceph/mgr/restful/api/request.py
/usr/lib64/ceph/mgr/restful/api/request.pyc
/usr/lib64/ceph/mgr/restful/api/request.pyo
/usr/lib64/ceph/mgr/restful/api/server.py
/usr/lib64/ceph/mgr/restful/api/server.pyc
/usr/lib64/ceph/mgr/restful/api/server.pyo
/usr/lib64/ceph/mgr/restful/common.py
/usr/lib64/ceph/mgr/restful/common.pyc
/usr/lib64/ceph/mgr/restful/common.pyo
/usr/lib64/ceph/mgr/restful/decorators.py
/usr/lib64/ceph/mgr/restful/decorators.pyc
/usr/lib64/ceph/mgr/restful/decorators.pyo
/usr/lib64/ceph/mgr/restful/hooks.py
/usr/lib64/ceph/mgr/restful/hooks.pyc
/usr/lib64/ceph/mgr/restful/hooks.pyo
/usr/lib64/ceph/mgr/restful/module.py
/usr/lib64/ceph/mgr/restful/module.pyc
/usr/lib64/ceph/mgr/restful/module.pyo
/usr/lib64/ceph/mgr/selftest
/usr/lib64/ceph/mgr/selftest/__init__.py
/usr/lib64/ceph/mgr/selftest/__init__.pyc
/usr/lib64/ceph/mgr/selftest/__init__.pyo
/usr/lib64/ceph/mgr/selftest/module.py
/usr/lib64/ceph/mgr/selftest/module.pyc
/usr/lib64/ceph/mgr/selftest/module.pyo
/usr/lib64/ceph/mgr/status
/usr/lib64/ceph/mgr/status/__init__.py
/usr/lib64/ceph/mgr/status/__init__.pyc
/usr/lib64/ceph/mgr/status/__init__.pyo
/usr/lib64/ceph/mgr/status/module.py
/usr/lib64/ceph/mgr/status/module.pyc
/usr/lib64/ceph/mgr/status/module.pyo
/usr/lib64/ceph/mgr/zabbix
/usr/lib64/ceph/mgr/zabbix/__init__.py
/usr/lib64/ceph/mgr/zabbix/__init__.pyc
/usr/lib64/ceph/mgr/zabbix/__init__.pyo
/usr/lib64/ceph/mgr/zabbix/module.py
/usr/lib64/ceph/mgr/zabbix/module.pyc
/usr/lib64/ceph/mgr/zabbix/module.pyo
/usr/lib64/ceph/mgr/zabbix/zabbix_template.xml
/var/lib/ceph/mgr
[root@app1 ~]# 
[root@app1 ~]# rpm -ql ceph-mon
/usr/bin/ceph-mon
/usr/bin/ceph-monstore-tool
/usr/bin/ceph-rest-api
/usr/lib/python2.7/site-packages/ceph_rest_api.py
/usr/lib/python2.7/site-packages/ceph_rest_api.pyc
/usr/lib/python2.7/site-packages/ceph_rest_api.pyo
/usr/lib/systemd/system/ceph-mon.target
/usr/lib/systemd/system/ceph-mon@.service
/usr/share/man/man8/ceph-mon.8.gz
/usr/share/man/man8/ceph-rest-api.8.gz
/var/lib/ceph/mon
[root@app1 ~]# 
[root@app1 ~]# rpm -ql ceph-osd
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
/usr/lib/udev/rules.d
/usr/lib/udev/rules.d/60-ceph-by-parttypeuuid.rules
/usr/lib/udev/rules.d/95-ceph-osd.rules
/usr/sbin/ceph-volume
/usr/sbin/ceph-volume-systemd
/usr/share/man/man8/ceph-bluestore-tool.8.gz
/usr/share/man/man8/ceph-clsinfo.8.gz
/usr/share/man/man8/ceph-osd.8.gz
/usr/share/man/man8/ceph-volume-systemd.8.gz
/usr/share/man/man8/ceph-volume.8.gz
/var/lib/ceph/osd
[root@app1 ~]# 
[root@app1 ~]# rpm -ql ceph-selinux
/usr/share/man/man8/ceph_selinux.8.gz
/usr/share/selinux/devel/include/contrib/ceph.if
/usr/share/selinux/packages/ceph.pp
[root@app1 ~]# 


[root@app1 yum.repos.d]# ceph-deploy install --release luminous app1 app2 app3
[ceph_deploy.conf][DEBUG ] found configuration file at: /root/.cephdeploy.conf
[ceph_deploy.cli][INFO  ] Invoked (2.0.1): /usr/bin/ceph-deploy install --release luminous app1 app2 app3
[ceph_deploy.cli][INFO  ] ceph-deploy options:
[ceph_deploy.cli][INFO  ]  verbose                       : False
[ceph_deploy.cli][INFO  ]  testing                       : None
[ceph_deploy.cli][INFO  ]  cd_conf                       : <ceph_deploy.conf.cephdeploy.Conf instance at 0x1d24e60>
[ceph_deploy.cli][INFO  ]  cluster                       : ceph
[ceph_deploy.cli][INFO  ]  dev_commit                    : None
[ceph_deploy.cli][INFO  ]  install_mds                   : False
[ceph_deploy.cli][INFO  ]  stable                        : None
[ceph_deploy.cli][INFO  ]  default_release               : False
[ceph_deploy.cli][INFO  ]  username                      : None
[ceph_deploy.cli][INFO  ]  adjust_repos                  : True
[ceph_deploy.cli][INFO  ]  func                          : <function install at 0x1ccf938>
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
[app1][DEBUG ] Cleaning repos: Ceph Ceph-noarch base ceph-source epel extras
[app1][DEBUG ]               : mysql-connectors-community mysql-tools-community
[app1][DEBUG ]               : mysql57-community updates
[app1][DEBUG ] Cleaning up everything
[app1][DEBUG ] Cleaning up list of fastest mirrors
[app1][INFO  ] Running command: yum -y install epel-release
[app1][DEBUG ] Loaded plugins: fastestmirror, priorities
[app1][WARNIN] http://sg.fedora.ipserverone.com/epel/7/x86_64/repodata/e97bc29265492560bd71be80663f2d85fa3192151c094a8d4ae6b1b4de6b5cd1-primary.xml.gz: [Errno 14] HTTP Error 404 - Not Found
[app1][WARNIN] Trying other mirror.
[app1][WARNIN] To address this issue please refer to the below knowledge base article 
[app1][WARNIN] 
[app1][WARNIN] https://access.redhat.com/articles/1320623
[app1][WARNIN] 
[app1][WARNIN] If above article doesn't help to resolve this issue please create a bug on https://bugs.centos.org/
[app1][WARNIN] 
[app1][DEBUG ] Determining fastest mirrors
[app1][DEBUG ]  * base: mirrors.aliyun.com
[app1][DEBUG ]  * epel: fedora.cs.nctu.edu.tw
[app1][DEBUG ]  * extras: mirror.bit.edu.cn
[app1][DEBUG ]  * updates: mirror.bit.edu.cn
[app1][DEBUG ] 8 packages excluded due to repository priority protections
[app1][DEBUG ] Package epel-release-7-11.noarch already installed and latest version
[app1][DEBUG ] Nothing to do
[app1][INFO  ] Running command: yum -y install yum-plugin-priorities
[app1][DEBUG ] Loaded plugins: fastestmirror, priorities
[app1][DEBUG ] Loading mirror speeds from cached hostfile
[app1][DEBUG ]  * base: mirrors.aliyun.com
[app1][DEBUG ]  * epel: fedora.cs.nctu.edu.tw
[app1][DEBUG ]  * extras: mirror.bit.edu.cn
[app1][DEBUG ]  * updates: mirror.bit.edu.cn
[app1][DEBUG ] 8 packages excluded due to repository priority protections
[app1][DEBUG ] Package yum-plugin-priorities-1.1.31-46.el7_5.noarch already installed and latest version
[app1][DEBUG ] Nothing to do
[app1][DEBUG ] Configure Yum priorities to include obsoletes
[app1][WARNIN] check_obsoletes has been enabled for Yum priorities plugin
[app1][INFO  ] Running command: rpm --import https://download.ceph.com/keys/release.asc
[app1][INFO  ] Running command: yum remove -y ceph-release
[app1][DEBUG ] Loaded plugins: fastestmirror, priorities
[app1][DEBUG ] Resolving Dependencies
[app1][DEBUG ] --> Running transaction check
[app1][DEBUG ] ---> Package ceph-release.noarch 0:1-1.el7 will be erased
[app1][DEBUG ] --> Finished Dependency Resolution
[app1][DEBUG ] 
[app1][DEBUG ] Dependencies Resolved
[app1][DEBUG ] 
[app1][DEBUG ] ================================================================================
[app1][DEBUG ]  Package              Arch           Version            Repository         Size
[app1][DEBUG ] ================================================================================
[app1][DEBUG ] Removing:
[app1][DEBUG ]  ceph-release         noarch         1-1.el7            installed         544  
[app1][DEBUG ] 
[app1][DEBUG ] Transaction Summary
[app1][DEBUG ] ================================================================================
[app1][DEBUG ] Remove  1 Package
[app1][DEBUG ] 
[app1][DEBUG ] Installed size: 544  
[app1][DEBUG ] Downloading packages:
[app1][DEBUG ] Running transaction check
[app1][DEBUG ] Running transaction test
[app1][DEBUG ] Transaction test succeeded
[app1][DEBUG ] Running transaction
[app1][DEBUG ]   Erasing    : ceph-release-1-1.el7.noarch                                  1/1 
[app1][DEBUG ] warning: /etc/yum.repos.d/ceph.repo saved as /etc/yum.repos.d/ceph.repo.rpmsave
[app1][DEBUG ]   Verifying  : ceph-release-1-1.el7.noarch                                  1/1 
[app1][DEBUG ] 
[app1][DEBUG ] Removed:
[app1][DEBUG ]   ceph-release.noarch 0:1-1.el7                                                 
[app1][DEBUG ] 
[app1][DEBUG ] Complete!
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
[app1][DEBUG ]  * updates: mirror.bit.edu.cn
[app1][DEBUG ] 8 packages excluded due to repository priority protections
[app1][DEBUG ] Package 2:ceph-12.2.9-0.el7.x86_64 already installed and latest version
[app1][DEBUG ] Package 2:ceph-radosgw-12.2.9-0.el7.x86_64 already installed and latest version
[app1][DEBUG ] Nothing to do
[app1][INFO  ] Running command: ceph --version
[app1][DEBUG ] ceph version 12.2.9 (9e300932ef8a8916fb3fda78c58691a6ab0f4217) luminous (stable)
[ceph_deploy.install][DEBUG ] Detecting platform for host app2 ...
[app2][DEBUG ] connected to host: app2 
[app2][DEBUG ] detect platform information from remote host
[app2][DEBUG ] detect machine type
[ceph_deploy.install][INFO  ] Distro info: CentOS Linux 7.5.1804 Core
[app2][INFO  ] installing Ceph on app2
[app2][INFO  ] Running command: yum clean all
[app2][DEBUG ] Loaded plugins: fastestmirror, priorities
[app2][DEBUG ] Cleaning repos: Ceph Ceph-noarch base ceph-source epel extras ius
[app2][DEBUG ]               : mysql-connectors-community mysql-tools-community
[app2][DEBUG ]               : mysql57-community updates
[app2][DEBUG ] Cleaning up everything
[app2][DEBUG ] Maybe you want: rm -rf /var/cache/yum, to also free up space taken by orphaned data from disabled or removed repos
[app2][DEBUG ] Cleaning up list of fastest mirrors
[app2][INFO  ] Running command: yum -y install epel-release
[app2][DEBUG ] Loaded plugins: fastestmirror, priorities
[app2][DEBUG ] Determining fastest mirrors
[app2][DEBUG ]  * base: mirrors.aliyun.com
[app2][DEBUG ]  * epel: mirror01.idc.hinet.net
[app2][DEBUG ]  * extras: mirrors.163.com
[app2][DEBUG ]  * ius: hkg.mirror.rackspace.com
[app2][DEBUG ]  * updates: mirrors.163.com
[app2][DEBUG ] 8 packages excluded due to repository priority protections
[app2][DEBUG ] Package epel-release-7-11.noarch already installed and latest version
[app2][DEBUG ] Nothing to do
[app2][INFO  ] Running command: yum -y install yum-plugin-priorities
[app2][DEBUG ] Loaded plugins: fastestmirror, priorities
[app2][DEBUG ] Loading mirror speeds from cached hostfile
[app2][DEBUG ]  * base: mirrors.aliyun.com
[app2][DEBUG ]  * epel: mirror01.idc.hinet.net
[app2][DEBUG ]  * extras: mirrors.163.com
[app2][DEBUG ]  * ius: hkg.mirror.rackspace.com
[app2][DEBUG ]  * updates: mirrors.163.com
[app2][DEBUG ] 8 packages excluded due to repository priority protections
[app2][DEBUG ] Package yum-plugin-priorities-1.1.31-46.el7_5.noarch already installed and latest version
[app2][DEBUG ] Nothing to do
[app2][DEBUG ] Configure Yum priorities to include obsoletes
[app2][WARNIN] check_obsoletes has been enabled for Yum priorities plugin
[app2][INFO  ] Running command: rpm --import https://download.ceph.com/keys/release.asc
[app2][INFO  ] Running command: yum remove -y ceph-release
[app2][DEBUG ] Loaded plugins: fastestmirror, priorities
[app2][DEBUG ] Resolving Dependencies
[app2][DEBUG ] --> Running transaction check
[app2][DEBUG ] ---> Package ceph-release.noarch 0:1-1.el7 will be erased
[app2][DEBUG ] --> Finished Dependency Resolution
[app2][DEBUG ] 
[app2][DEBUG ] Dependencies Resolved
[app2][DEBUG ] 
[app2][DEBUG ] ================================================================================
[app2][DEBUG ]  Package              Arch           Version            Repository         Size
[app2][DEBUG ] ================================================================================
[app2][DEBUG ] Removing:
[app2][DEBUG ]  ceph-release         noarch         1-1.el7            installed         544  
[app2][DEBUG ] 
[app2][DEBUG ] Transaction Summary
[app2][DEBUG ] ================================================================================
[app2][DEBUG ] Remove  1 Package
[app2][DEBUG ] 
[app2][DEBUG ] Installed size: 544  
[app2][DEBUG ] Downloading packages:
[app2][DEBUG ] Running transaction check
[app2][DEBUG ] Running transaction test
[app2][DEBUG ] Transaction test succeeded
[app2][DEBUG ] Running transaction
[app2][DEBUG ]   Erasing    : ceph-release-1-1.el7.noarch                                  1/1 
[app2][DEBUG ] warning: /etc/yum.repos.d/ceph.repo saved as /etc/yum.repos.d/ceph.repo.rpmsave
[app2][DEBUG ]   Verifying  : ceph-release-1-1.el7.noarch                                  1/1 
[app2][DEBUG ] 
[app2][DEBUG ] Removed:
[app2][DEBUG ]   ceph-release.noarch 0:1-1.el7                                                 
[app2][DEBUG ] 
[app2][DEBUG ] Complete!
[app2][INFO  ] Running command: yum install -y https://download.ceph.com/rpm-luminous/el7/noarch/ceph-release-1-0.el7.noarch.rpm
[app2][DEBUG ] Loaded plugins: fastestmirror, priorities
[app2][DEBUG ] Examining /var/tmp/yum-root-omvSj2/ceph-release-1-0.el7.noarch.rpm: ceph-release-1-1.el7.noarch
[app2][DEBUG ] Marking /var/tmp/yum-root-omvSj2/ceph-release-1-0.el7.noarch.rpm to be installed
[app2][DEBUG ] Resolving Dependencies
[app2][DEBUG ] --> Running transaction check
[app2][DEBUG ] ---> Package ceph-release.noarch 0:1-1.el7 will be installed
[app2][DEBUG ] --> Finished Dependency Resolution
[app2][DEBUG ] 
[app2][DEBUG ] Dependencies Resolved
[app2][DEBUG ] 
[app2][DEBUG ] ================================================================================
[app2][DEBUG ]  Package          Arch       Version     Repository                        Size
[app2][DEBUG ] ================================================================================
[app2][DEBUG ] Installing:
[app2][DEBUG ]  ceph-release     noarch     1-1.el7     /ceph-release-1-0.el7.noarch     544  
[app2][DEBUG ] 
[app2][DEBUG ] Transaction Summary
[app2][DEBUG ] ================================================================================
[app2][DEBUG ] Install  1 Package
[app2][DEBUG ] 
[app2][DEBUG ] Total size: 544  
[app2][DEBUG ] Installed size: 544  
[app2][DEBUG ] Downloading packages:
[app2][DEBUG ] Running transaction check
[app2][DEBUG ] Running transaction test
[app2][DEBUG ] Transaction test succeeded
[app2][DEBUG ] Running transaction
[app2][DEBUG ]   Installing : ceph-release-1-1.el7.noarch                                  1/1 
[app2][DEBUG ]   Verifying  : ceph-release-1-1.el7.noarch                                  1/1 
[app2][DEBUG ] 
[app2][DEBUG ] Installed:
[app2][DEBUG ]   ceph-release.noarch 0:1-1.el7                                                 
[app2][DEBUG ] 
[app2][DEBUG ] Complete!
[app2][WARNIN] ensuring that /etc/yum.repos.d/ceph.repo contains a high priority
[app2][WARNIN] altered ceph.repo priorities to contain: priority=1
[app2][INFO  ] Running command: yum -y install ceph ceph-radosgw
[app2][DEBUG ] Loaded plugins: fastestmirror, priorities
[app2][DEBUG ] Loading mirror speeds from cached hostfile
[app2][DEBUG ]  * base: mirrors.aliyun.com
[app2][DEBUG ]  * epel: mirror01.idc.hinet.net
[app2][DEBUG ]  * extras: mirrors.163.com
[app2][DEBUG ]  * ius: hkg.mirror.rackspace.com
[app2][DEBUG ]  * updates: mirrors.163.com
[app2][DEBUG ] 8 packages excluded due to repository priority protections
[app2][DEBUG ] Package 2:ceph-12.2.9-0.el7.x86_64 already installed and latest version
[app2][DEBUG ] Package 2:ceph-radosgw-12.2.9-0.el7.x86_64 already installed and latest version
[app2][DEBUG ] Nothing to do
[app2][INFO  ] Running command: ceph --version
[app2][DEBUG ] ceph version 12.2.9 (9e300932ef8a8916fb3fda78c58691a6ab0f4217) luminous (stable)
[ceph_deploy.install][DEBUG ] Detecting platform for host app3 ...
[app3][DEBUG ] connected to host: app3 
[app3][DEBUG ] detect platform information from remote host
[app3][DEBUG ] detect machine type
[ceph_deploy.install][INFO  ] Distro info: CentOS Linux 7.3.1611 Core
[app3][INFO  ] installing Ceph on app3
[app3][INFO  ] Running command: yum clean all
[app3][DEBUG ] Loaded plugins: fastestmirror, priorities
[app3][DEBUG ] Cleaning repos: Ceph Ceph-noarch base ceph-source epel extras
[app3][DEBUG ]               : mysql-connectors-community mysql-tools-community
[app3][DEBUG ]               : mysql57-community updates
[app3][DEBUG ] Cleaning up everything
[app3][DEBUG ] Cleaning up list of fastest mirrors
[app3][INFO  ] Running command: yum -y install epel-release
[app3][DEBUG ] Loaded plugins: fastestmirror, priorities
[app3][WARNIN] http://mirrors.cqu.edu.cn/CentOS/7.5.1804/os/x86_64/repodata/03d0a660eb33174331aee3e077e11d4c017412d761b7f2eaa8555e7898e701e0-primary.sqlite.bz2: [Errno 14] curl#56 - "Recv failure: Connection reset by peer"
[app3][WARNIN] Trying other mirror.
[app3][DEBUG ] Determining fastest mirrors
[app3][DEBUG ]  * base: mirrors.aliyun.com
[app3][DEBUG ]  * epel: mirror01.idc.hinet.net
[app3][DEBUG ]  * extras: mirrors.cn99.com
[app3][DEBUG ]  * updates: mirrors.163.com
[app3][DEBUG ] 8 packages excluded due to repository priority protections
[app3][DEBUG ] Package epel-release-7-11.noarch already installed and latest version
[app3][DEBUG ] Nothing to do
[app3][INFO  ] Running command: yum -y install yum-plugin-priorities
[app3][DEBUG ] Loaded plugins: fastestmirror, priorities
[app3][DEBUG ] Loading mirror speeds from cached hostfile
[app3][DEBUG ]  * base: mirrors.aliyun.com
[app3][DEBUG ]  * epel: mirror01.idc.hinet.net
[app3][DEBUG ]  * extras: mirrors.cn99.com
[app3][DEBUG ]  * updates: mirrors.163.com
[app3][DEBUG ] 8 packages excluded due to repository priority protections
[app3][DEBUG ] Package yum-plugin-priorities-1.1.31-46.el7_5.noarch already installed and latest version
[app3][DEBUG ] Nothing to do
[app3][DEBUG ] Configure Yum priorities to include obsoletes
[app3][WARNIN] check_obsoletes has been enabled for Yum priorities plugin
[app3][INFO  ] Running command: rpm --import https://download.ceph.com/keys/release.asc
[app3][INFO  ] Running command: yum remove -y ceph-release
[app3][DEBUG ] Loaded plugins: fastestmirror, priorities
[app3][DEBUG ] Resolving Dependencies
[app3][DEBUG ] --> Running transaction check
[app3][DEBUG ] ---> Package ceph-release.noarch 0:1-1.el7 will be erased
[app3][DEBUG ] --> Finished Dependency Resolution
[app3][DEBUG ] 
[app3][DEBUG ] Dependencies Resolved
[app3][DEBUG ] 
[app3][DEBUG ] ================================================================================
[app3][DEBUG ]  Package              Arch           Version            Repository         Size
[app3][DEBUG ] ================================================================================
[app3][DEBUG ] Removing:
[app3][DEBUG ]  ceph-release         noarch         1-1.el7            installed         544  
[app3][DEBUG ] 
[app3][DEBUG ] Transaction Summary
[app3][DEBUG ] ================================================================================
[app3][DEBUG ] Remove  1 Package
[app3][DEBUG ] 
[app3][DEBUG ] Installed size: 544  
[app3][DEBUG ] Downloading packages:
[app3][DEBUG ] Running transaction check
[app3][DEBUG ] Running transaction test
[app3][DEBUG ] Transaction test succeeded
[app3][DEBUG ] Running transaction
[app3][DEBUG ]   Erasing    : ceph-release-1-1.el7.noarch                                  1/1 
[app3][DEBUG ] warning: /etc/yum.repos.d/ceph.repo saved as /etc/yum.repos.d/ceph.repo.rpmsave
[app3][DEBUG ]   Verifying  : ceph-release-1-1.el7.noarch                                  1/1 
[app3][DEBUG ] 
[app3][DEBUG ] Removed:
[app3][DEBUG ]   ceph-release.noarch 0:1-1.el7                                                 
[app3][DEBUG ] 
[app3][DEBUG ] Complete!
[app3][INFO  ] Running command: yum install -y https://download.ceph.com/rpm-luminous/el7/noarch/ceph-release-1-0.el7.noarch.rpm
[app3][DEBUG ] Loaded plugins: fastestmirror, priorities
[app3][DEBUG ] Examining /var/tmp/yum-root-2cHImf/ceph-release-1-0.el7.noarch.rpm: ceph-release-1-1.el7.noarch
[app3][DEBUG ] Marking /var/tmp/yum-root-2cHImf/ceph-release-1-0.el7.noarch.rpm to be installed
[app3][DEBUG ] Resolving Dependencies
[app3][DEBUG ] --> Running transaction check
[app3][DEBUG ] ---> Package ceph-release.noarch 0:1-1.el7 will be installed
[app3][DEBUG ] --> Finished Dependency Resolution
[app3][DEBUG ] 
[app3][DEBUG ] Dependencies Resolved
[app3][DEBUG ] 
[app3][DEBUG ] ================================================================================
[app3][DEBUG ]  Package          Arch       Version     Repository                        Size
[app3][DEBUG ] ================================================================================
[app3][DEBUG ] Installing:
[app3][DEBUG ]  ceph-release     noarch     1-1.el7     /ceph-release-1-0.el7.noarch     544  
[app3][DEBUG ] 
[app3][DEBUG ] Transaction Summary
[app3][DEBUG ] ================================================================================
[app3][DEBUG ] Install  1 Package
[app3][DEBUG ] 
[app3][DEBUG ] Total size: 544  
[app3][DEBUG ] Installed size: 544  
[app3][DEBUG ] Downloading packages:
[app3][DEBUG ] Running transaction check
[app3][DEBUG ] Running transaction test
[app3][DEBUG ] Transaction test succeeded
[app3][DEBUG ] Running transaction
[app3][DEBUG ]   Installing : ceph-release-1-1.el7.noarch                                  1/1 
[app3][DEBUG ]   Verifying  : ceph-release-1-1.el7.noarch                                  1/1 
[app3][DEBUG ] 
[app3][DEBUG ] Installed:
[app3][DEBUG ]   ceph-release.noarch 0:1-1.el7                                                 
[app3][DEBUG ] 
[app3][DEBUG ] Complete!
[app3][WARNIN] ensuring that /etc/yum.repos.d/ceph.repo contains a high priority
[app3][WARNIN] altered ceph.repo priorities to contain: priority=1
[app3][INFO  ] Running command: yum -y install ceph ceph-radosgw
[app3][DEBUG ] Loaded plugins: fastestmirror, priorities
[app3][DEBUG ] Loading mirror speeds from cached hostfile
[app3][DEBUG ]  * base: mirrors.aliyun.com
[app3][DEBUG ]  * epel: mirror01.idc.hinet.net
[app3][DEBUG ]  * extras: mirrors.cn99.com
[app3][DEBUG ]  * updates: mirrors.163.com
[app3][DEBUG ] 8 packages excluded due to repository priority protections
[app3][DEBUG ] Package 2:ceph-12.2.9-0.el7.x86_64 already installed and latest version
[app3][DEBUG ] Package 2:ceph-radosgw-12.2.9-0.el7.x86_64 already installed and latest version
[app3][DEBUG ] Nothing to do
[app3][INFO  ] Running command: ceph --version
[app3][DEBUG ] ceph version 12.2.9 (9e300932ef8a8916fb3fda78c58691a6ab0f4217) luminous (stable)
[root@app1 yum.repos.d]# 







#############################################
[root@app1 yum.repos.d]# ceph-deploy mon create-initial
[ceph_deploy.conf][DEBUG ] found configuration file at: /root/.cephdeploy.conf
[ceph_deploy.cli][INFO  ] Invoked (2.0.1): /usr/bin/ceph-deploy mon create-initial
[ceph_deploy.cli][INFO  ] ceph-deploy options:
[ceph_deploy.cli][INFO  ]  username                      : None
[ceph_deploy.cli][INFO  ]  verbose                       : False
[ceph_deploy.cli][INFO  ]  overwrite_conf                : False
[ceph_deploy.cli][INFO  ]  subcommand                    : create-initial
[ceph_deploy.cli][INFO  ]  quiet                         : False
[ceph_deploy.cli][INFO  ]  cd_conf                       : <ceph_deploy.conf.cephdeploy.Conf instance at 0x1154f38>
[ceph_deploy.cli][INFO  ]  cluster                       : ceph
[ceph_deploy.cli][INFO  ]  func                          : <function mon at 0x114a758>
[ceph_deploy.cli][INFO  ]  ceph_conf                     : None
[ceph_deploy.cli][INFO  ]  default_release               : False
[ceph_deploy.cli][INFO  ]  keyrings                      : None
[ceph_deploy][ERROR ] ConfigError: Cannot load config: [Errno 2] No such file or directory: 'ceph.conf'; has `ceph-deploy new` been run in this directory?
                 
[root@app1 yum.repos.d]# cd /etc/ceph/
[root@app1 ceph]# 
[root@app1 ceph]# pwd
/etc/ceph
[root@app1 ceph]# 
[root@app1 ceph]# 
[root@app1 ceph]# 
[root@app1 ceph]# ceph-deploy mon create-initial
[ceph_deploy.conf][DEBUG ] found configuration file at: /root/.cephdeploy.conf
[ceph_deploy.cli][INFO  ] Invoked (2.0.1): /usr/bin/ceph-deploy mon create-initial
[ceph_deploy.cli][INFO  ] ceph-deploy options:
[ceph_deploy.cli][INFO  ]  username                      : None
[ceph_deploy.cli][INFO  ]  verbose                       : False
[ceph_deploy.cli][INFO  ]  overwrite_conf                : False
[ceph_deploy.cli][INFO  ]  subcommand                    : create-initial
[ceph_deploy.cli][INFO  ]  quiet                         : False
[ceph_deploy.cli][INFO  ]  cd_conf                       : <ceph_deploy.conf.cephdeploy.Conf instance at 0x2139f38>
[ceph_deploy.cli][INFO  ]  cluster                       : ceph
[ceph_deploy.cli][INFO  ]  func                          : <function mon at 0x212f758>
[ceph_deploy.cli][INFO  ]  ceph_conf                     : None
[ceph_deploy.cli][INFO  ]  default_release               : False
[ceph_deploy.cli][INFO  ]  keyrings                      : None
[ceph_deploy.mon][DEBUG ] Deploying mon, cluster ceph hosts app1
[ceph_deploy.mon][DEBUG ] detecting platform for host app1 ...
[app1][DEBUG ] connected to host: app1 
[app1][DEBUG ] detect platform information from remote host
[app1][DEBUG ] detect machine type
[app1][DEBUG ] find the location of an executable
[ceph_deploy.mon][INFO  ] distro info: CentOS Linux 7.3.1611 Core
[app1][DEBUG ] determining if provided host has same hostname in remote
[app1][DEBUG ] get remote short hostname
[app1][DEBUG ] deploying mon to app1
[app1][DEBUG ] get remote short hostname
[app1][DEBUG ] remote hostname: app1
[app1][DEBUG ] write cluster configuration to /etc/ceph/{cluster}.conf
[app1][DEBUG ] create the mon path if it does not exist
[app1][DEBUG ] checking for done path: /var/lib/ceph/mon/ceph-app1/done
[app1][DEBUG ] done path does not exist: /var/lib/ceph/mon/ceph-app1/done
[app1][INFO  ] creating keyring file: /var/lib/ceph/tmp/ceph-app1.mon.keyring
[app1][DEBUG ] create the monitor keyring file
[app1][INFO  ] Running command: ceph-mon --cluster ceph --mkfs -i app1 --keyring /var/lib/ceph/tmp/ceph-app1.mon.keyring --setuser 167 --setgroup 167
[app1][INFO  ] unlinking keyring file /var/lib/ceph/tmp/ceph-app1.mon.keyring
[app1][DEBUG ] create a done file to avoid re-doing the mon deployment
[app1][DEBUG ] create the init path if it does not exist
[app1][INFO  ] Running command: systemctl enable ceph.target
[app1][INFO  ] Running command: systemctl enable ceph-mon@app1
[app1][WARNIN] Created symlink from /etc/systemd/system/ceph-mon.target.wants/ceph-mon@app1.service to /usr/lib/systemd/system/ceph-mon@.service.
[app1][INFO  ] Running command: systemctl start ceph-mon@app1
[app1][INFO  ] Running command: ceph --cluster=ceph --admin-daemon /var/run/ceph/ceph-mon.app1.asok mon_status
[app1][DEBUG ] ********************************************************************************
[app1][DEBUG ] status for monitor: mon.app1
[app1][DEBUG ] {
[app1][DEBUG ]   "election_epoch": 3, 
[app1][DEBUG ]   "extra_probe_peers": [], 
[app1][DEBUG ]   "feature_map": {
[app1][DEBUG ]     "mon": {
[app1][DEBUG ]       "group": {
[app1][DEBUG ]         "features": "0x3ffddff8eea4fffb", 
[app1][DEBUG ]         "num": 1, 
[app1][DEBUG ]         "release": "luminous"
[app1][DEBUG ]       }
[app1][DEBUG ]     }
[app1][DEBUG ]   }, 
[app1][DEBUG ]   "features": {
[app1][DEBUG ]     "quorum_con": "4611087853745930235", 
[app1][DEBUG ]     "quorum_mon": [
[app1][DEBUG ]       "kraken", 
[app1][DEBUG ]       "luminous"
[app1][DEBUG ]     ], 
[app1][DEBUG ]     "required_con": "153140804152475648", 
[app1][DEBUG ]     "required_mon": [
[app1][DEBUG ]       "kraken", 
[app1][DEBUG ]       "luminous"
[app1][DEBUG ]     ]
[app1][DEBUG ]   }, 
[app1][DEBUG ]   "monmap": {
[app1][DEBUG ]     "created": "2018-11-21 16:57:49.992274", 
[app1][DEBUG ]     "epoch": 1, 
[app1][DEBUG ]     "features": {
[app1][DEBUG ]       "optional": [], 
[app1][DEBUG ]       "persistent": [
[app1][DEBUG ]         "kraken", 
[app1][DEBUG ]         "luminous"
[app1][DEBUG ]       ]
[app1][DEBUG ]     }, 
[app1][DEBUG ]     "fsid": "c23d9371-3e7b-4276-bd77-0f21b4c1ad9b", 
[app1][DEBUG ]     "modified": "2018-11-21 16:57:49.992274", 
[app1][DEBUG ]     "mons": [
[app1][DEBUG ]       {
[app1][DEBUG ]         "addr": "192.168.6.211:6789/0", 
[app1][DEBUG ]         "name": "app1", 
[app1][DEBUG ]         "public_addr": "192.168.6.211:6789/0", 
[app1][DEBUG ]         "rank": 0
[app1][DEBUG ]       }
[app1][DEBUG ]     ]
[app1][DEBUG ]   }, 
[app1][DEBUG ]   "name": "app1", 
[app1][DEBUG ]   "outside_quorum": [], 
[app1][DEBUG ]   "quorum": [
[app1][DEBUG ]     0
[app1][DEBUG ]   ], 
[app1][DEBUG ]   "rank": 0, 
[app1][DEBUG ]   "state": "leader", 
[app1][DEBUG ]   "sync_provider": []
[app1][DEBUG ] }
[app1][DEBUG ] ********************************************************************************
[app1][INFO  ] monitor: mon.app1 is running
[app1][INFO  ] Running command: ceph --cluster=ceph --admin-daemon /var/run/ceph/ceph-mon.app1.asok mon_status
[ceph_deploy.mon][INFO  ] processing monitor mon.app1
[app1][DEBUG ] connected to host: app1 
[app1][DEBUG ] detect platform information from remote host
[app1][DEBUG ] detect machine type
[app1][DEBUG ] find the location of an executable
[app1][INFO  ] Running command: ceph --cluster=ceph --admin-daemon /var/run/ceph/ceph-mon.app1.asok mon_status
[ceph_deploy.mon][INFO  ] mon.app1 monitor has reached quorum!
[ceph_deploy.mon][INFO  ] all initial monitors are running and have formed quorum
[ceph_deploy.mon][INFO  ] Running gatherkeys...
[ceph_deploy.gatherkeys][INFO  ] Storing keys in temp directory /tmp/tmpbimlel
[app1][DEBUG ] connected to host: app1 
[app1][DEBUG ] detect platform information from remote host
[app1][DEBUG ] detect machine type
[app1][DEBUG ] get remote short hostname
[app1][DEBUG ] fetch remote file
[app1][INFO  ] Running command: /usr/bin/ceph --connect-timeout=25 --cluster=ceph --admin-daemon=/var/run/ceph/ceph-mon.app1.asok mon_status
[app1][INFO  ] Running command: /usr/bin/ceph --connect-timeout=25 --cluster=ceph --name mon. --keyring=/var/lib/ceph/mon/ceph-app1/keyring auth get client.admin
[app1][INFO  ] Running command: /usr/bin/ceph --connect-timeout=25 --cluster=ceph --name mon. --keyring=/var/lib/ceph/mon/ceph-app1/keyring auth get-or-create client.admin osd allow * mds allow * mon allow * mgr allow *
[app1][INFO  ] Running command: /usr/bin/ceph --connect-timeout=25 --cluster=ceph --name mon. --keyring=/var/lib/ceph/mon/ceph-app1/keyring auth get client.bootstrap-mds
[app1][INFO  ] Running command: /usr/bin/ceph --connect-timeout=25 --cluster=ceph --name mon. --keyring=/var/lib/ceph/mon/ceph-app1/keyring auth get-or-create client.bootstrap-mds mon allow profile bootstrap-mds
[app1][INFO  ] Running command: /usr/bin/ceph --connect-timeout=25 --cluster=ceph --name mon. --keyring=/var/lib/ceph/mon/ceph-app1/keyring auth get client.bootstrap-mgr
[app1][INFO  ] Running command: /usr/bin/ceph --connect-timeout=25 --cluster=ceph --name mon. --keyring=/var/lib/ceph/mon/ceph-app1/keyring auth get-or-create client.bootstrap-mgr mon allow profile bootstrap-mgr
[app1][INFO  ] Running command: /usr/bin/ceph --connect-timeout=25 --cluster=ceph --name mon. --keyring=/var/lib/ceph/mon/ceph-app1/keyring auth get client.bootstrap-osd
[app1][INFO  ] Running command: /usr/bin/ceph --connect-timeout=25 --cluster=ceph --name mon. --keyring=/var/lib/ceph/mon/ceph-app1/keyring auth get-or-create client.bootstrap-osd mon allow profile bootstrap-osd
[app1][INFO  ] Running command: /usr/bin/ceph --connect-timeout=25 --cluster=ceph --name mon. --keyring=/var/lib/ceph/mon/ceph-app1/keyring auth get client.bootstrap-rgw
[app1][INFO  ] Running command: /usr/bin/ceph --connect-timeout=25 --cluster=ceph --name mon. --keyring=/var/lib/ceph/mon/ceph-app1/keyring auth get-or-create client.bootstrap-rgw mon allow profile bootstrap-rgw
[ceph_deploy.gatherkeys][INFO  ] Storing ceph.client.admin.keyring
[ceph_deploy.gatherkeys][INFO  ] Storing ceph.bootstrap-mds.keyring
[ceph_deploy.gatherkeys][INFO  ] Storing ceph.bootstrap-mgr.keyring
[ceph_deploy.gatherkeys][INFO  ] keyring 'ceph.mon.keyring' already exists
[ceph_deploy.gatherkeys][INFO  ] Storing ceph.bootstrap-osd.keyring
[ceph_deploy.gatherkeys][INFO  ] Storing ceph.bootstrap-rgw.keyring
[ceph_deploy.gatherkeys][INFO  ] Destroy temp directory /tmp/tmpbimlel
[root@app1 ceph]# 
[root@app1 ceph]# ceph status
  cluster:
    id:     c23d9371-3e7b-4276-bd77-0f21b4c1ad9b
    health: HEALTH_OK
 
  services:
    mon: 1 daemons, quorum app1
    mgr: no daemons active
    osd: 0 osds: 0 up, 0 in
 
  data:
    pools:   0 pools, 0 pgs
    objects: 0 objects, 0B
    usage:   0B used, 0B / 0B avail
    pgs:     
 
[root@app1 ceph]# 

#############################################

[root@app1 ceph]# ceph-deploy disk list app1
[ceph_deploy.conf][DEBUG ] found configuration file at: /root/.cephdeploy.conf
[ceph_deploy.cli][INFO  ] Invoked (2.0.1): /usr/bin/ceph-deploy disk list app1
[ceph_deploy.cli][INFO  ] ceph-deploy options:
[ceph_deploy.cli][INFO  ]  username                      : None
[ceph_deploy.cli][INFO  ]  verbose                       : False
[ceph_deploy.cli][INFO  ]  debug                         : False
[ceph_deploy.cli][INFO  ]  overwrite_conf                : False
[ceph_deploy.cli][INFO  ]  subcommand                    : list
[ceph_deploy.cli][INFO  ]  quiet                         : False
[ceph_deploy.cli][INFO  ]  cd_conf                       : <ceph_deploy.conf.cephdeploy.Conf instance at 0xf7bd88>
[ceph_deploy.cli][INFO  ]  cluster                       : ceph
[ceph_deploy.cli][INFO  ]  host                          : ['app1']
[ceph_deploy.cli][INFO  ]  func                          : <function disk at 0xf1ac80>
[ceph_deploy.cli][INFO  ]  ceph_conf                     : None
[ceph_deploy.cli][INFO  ]  default_release               : False
[app1][DEBUG ] connected to host: app1 
[app1][DEBUG ] detect platform information from remote host
[app1][DEBUG ] detect machine type
[app1][DEBUG ] find the location of an executable
[app1][INFO  ] Running command: fdisk -l
[app1][INFO  ] Disk /dev/vda: 107.4 GB, 107374182400 bytes, 209715200 sectors
[app1][INFO  ] Disk /dev/mapper/cl-root: 2142.8 GB, 2142760861696 bytes, 4185079808 sectors
[app1][INFO  ] Disk /dev/mapper/cl-swap: 8455 MB, 8455716864 bytes, 16515072 sectors
[app1][INFO  ] Disk /dev/mapper/cl-home: 44.1 GB, 44149243904 bytes, 86228992 sectors
[app1][INFO  ] Disk /dev/vdb: 2199.0 GB, 2199023255552 bytes, 4294967296 sectors
[root@app1 ceph]# 


#############################################
#############################################
#############################################
#############################################

```

