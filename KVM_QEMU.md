## kvm and qemu

kvm：kernel-level

qemu：user-level



#### Installing Virtualization Packages on an Existing Ubuntu Linux System

```bash
sudo apt-get install qemu-kvm libvirt-bin ubuntu-vm-builder bridge-utils
```


#### Installing Virtualization Packages on an Existing Red Hat Enterprise Linux System

```bash
## Installing the Virtualization Packages with yum
yum install qemu-kvm qemu-img libvirt
yum install libvirt-python virt-manager virt-install libvirt-client

## Installing Virtualization Package Groups
yum groupinstall "Virtualization Tools"
yum groupinstall "Virtualization Hypervisor"
yum groupinstall "Virtualization Platform"
yum groupinstall "Virtualization Client"
yum install qemu-img
```



#### 各软件包的作用

**yum install qemu-kvm qemu-img libvirt**

To use virtualization on Red Hat Enterprise Linux, you require at minimum the `qemu-kvm`, `qemu-img`, and `libvirt` packages. These packages provide the `user-level KVM emulator模拟器`, `disk image manager`, and `virtualization management tools` on the host Red Hat Enterprise Linux system.

The `libvirt` package provides the server and host-side libraries for interacting with hypervisors and host systems, and the libvirtd daemon that handles the library calls, manages virtual machines and controls the hypervisor.

**yum install libvirt-python virt-manager virt-install libvirt-client**

* libvirt-python

The `libvirt-python` package contains a module that permits允许 applications written in the Python programming language to use the interface supplied by the libvirt API.

* virt-manager

`virt-manager`, also known as Virtual Machine Manager, provides `a graphical tool` for administering virtual machines. It uses the libvirt-client library as the management API.

* virt-install

This package provides the virt-install command for `creating virtual machines` from the command line.

* libvirt-client

The `libvirt-client` spackage provides the client-side APIs and libraries for accessing libvirt servers. The libvirt-client package includes the virsh command-line tool to manage and control virtual machines and hypervisors from the command line or a special virtualization shell.



#### KVM虚拟机使用步骤

创建KVM虚拟机的步骤：

1. 创建虚拟机磁盘
2. 编写虚拟机配置文件

- 配置虚拟机使用的硬盘
- 配置cdrom设备
- 配置指定了虚拟机的网卡信息
- 配置虚拟机使用的图形设备的信息

3. 定义虚拟机

4. 启动虚拟机

此时启动有两种情况：

* 如果是全新的虚拟机，此时需要安装操作系统

* 如果虚拟机中已经存在操作系统，则可以直接连接虚拟机

安装操作系统的方法有两个：

* 纯命令行界面安装

* 图形界面安装
  * 在虚拟机配置文件中定义图形设备信息，使用 vnc clients
  * 在虚拟机配置文件中定义图形设备信息，使用 virt-manager
* 系统安装完成后需要修改 bios 引导顺序，启动网卡，修改网卡配置，启动 ssh server

5. 连接虚拟机

连接虚拟机的方法：

* virsh console <虚拟机名称>
* 图形界面连接
  * 在虚拟机配置文件中定义图形设备信息，使用 vnc clients
  * 在虚拟机配置文件中定义图形设备信息，使用 virt-manager



#### kvm虚拟机的命令行管理方式

1. 虚拟机磁盘的创建
   创建一个全新的kvm虚拟机，第一步应该是创建需要使用的虚拟机磁盘，qemu-img命令用于创建虚拟机磁盘：
   * 创建一个空间为40G的虚拟机磁盘文件disk.img，镜像格式为qcow2:
     ​    qemu-img create -f qcow2 ./disk.img 40G
     ​    注意，由于是松散文件，此时创建后的磁盘文件体积暂时还很小。
   * 基于已有的虚拟磁盘文件base.img来创建虚拟磁盘disk.img，相当于“克隆”的功能：
        qemu-img create -b base.img -f qcow2 ./disk.img 40G
        注意，此处使用-b参数来指定已有的磁盘文件，使用该方式生成的虚拟机磁盘文件虽然体积小，但已具有磁盘文件base.img的全部功能，且此时disk.img文件仅会存储与基础镜像的差异，是大规模部署相同业务时的首选方案。但在进行虚拟机迁移的时候，千万不要忘记将base.img文件也一并移走。

2. 编写虚拟机配置文件origin.xml
   kvm虚拟机可以使用命令行的方式启动，但是需要带着众多参数，记忆麻烦，管理也困难，因此libvirtd这个服务在管理kvm虚拟机时，使用了xml文件来存储虚拟机的参数配置，一个标准的kvm虚拟机配置文件如下：

```
<domain type='kvm'>
    <!--此处标志着虚拟机的名称，该名称不能与当前系统中已有的虚拟机名称冲突-->
    <name>origin</name>

    <!--
    此处配置虚拟机的内存，分为两个参数，memory元素指定了虚拟机启动时占用的最大内存，
    currentMemory元素指定了虚拟机系统正常运行时占用的内存，参数unit指定了单位。
    两个参数可以设置为同一个值
    -->
    <memory unit='KiB'>4194304</memory>
    <currentMemory unit='KiB'>4194304</currentMemory>

    <vcpu placement='static'>1</vcpu>

    <os>
        <!--type指虚拟机的类型，hvm表示全虚拟化，一般不需要修改此处-->
        <type arch='x86_64'>hvm</type>

        <!--
        boot元素指定了启动虚拟机的设备及设备的启动顺序，示例中的配置指定了两个可用于启动的设备：cdrom和磁盘，
        由于需要全新安装一个操作系统，所以将cdrom放到了hd的前面，可以让虚拟机启动后先从光驱启动
        -->
        <boot dev='cdrom'/>
        <boot dev='hd'/>

    </os>

    <features>
        <acpi/>
        <apic/>
        <pae/>
    </features>

    <clock offset='localtime'/>

    <on_poweroff>destroy</on_poweroff>

    <on_reboot>restart</on_reboot>

    <on_crash>restart</on_crash>

    <devices>
        <!--
        此处指定了启动虚拟机使用的模拟器位置，确认此处配置的路径与系统中的qemu-kvm路径一致即可，
        在redhat系列的操作系统中使用yum来安装kvm的话，该选项一般不需要修改
        -->
        <emulator>/usr/libexec/qemu-kvm</emulator>

        <!--
        此处配置虚拟机使用的硬盘，需要注意已创建的虚拟机磁盘的格式与type参数指定的类型一致，
        source元素的file参数指定的路径即为已创建的虚拟机磁盘的路径。
        该配置项中的cache参数可修改为none、writethrough和writeback，三种参数各有利弊，
        但对于虚拟机中仅做少量文件写入的计算型业务来说，推荐使用writeback的模式，可以在少量数据写入时利用缓存达到较高的速度。
        该配置中的target元素指定了使用virtio驱动，可以提高虚拟机磁盘的性能，
        但是需要注意的是，非server版的windows系统对该驱动并非原生支持，
        当要创建全新的windows虚拟机时，可以先去掉该选项，或是再创建一个floppy设备来放置virtio驱动。
        -->
        <disk type='file' device='disk'>
            <driver name='qemu' type='qcow2' cache='writeback'/>
            <source file='/opt/dyn_vm/vmdk/origin.img'/>
            <target dev='vda' bus='virtio'/>
        </disk>

        <!--此处是对cdrom设备的配置，仅需要修改光盘镜像的路径即可-->
        <disk type='file' device='cdrom'>
            <driver name='qemu' type='raw'/>
            <source file='/opt/dyn_vm/iso/ubuntu-10.04.4-alternate-amd64.iso'/>
            <target dev='hdc' bus='ide'/>
            <readonly/>
        </disk>

        <!--该配置指定了虚拟机的网卡信息，
        libvirt默认提供了一个名为default的虚拟网络，创建的虚拟机使用该网络以NAT方式连接外网。
        在不使用桥接的情况下，该default虚拟网络可以支持使用，不必进行修改
        -->
        <interface type='network'>
            <source network='default'/>
            <model type='virtio'/>
        </interface>

        <input type='tablet' bus='usb'/>

        <input type='mouse' bus='ps2'/>

        <!--
        该配置为虚拟机使用的图形设备的信息，此处选择使用vnc作为外部连接虚拟机的图形方式，端口为5955，
        autoport参数可配置是否每次启动虚拟机时自动生成一个端口，listen参数指定了只能由哪些IP段的机器连接该vnc
        -->
        <graphics type='vnc' port='5955' autoport='no' listen='0.0.0.0'>

        </graphics>

    </devices>

</domain>
```

3. 定义虚拟机
   虚拟机的配置文件origin.xml编写完成后，可以使用以下命令来定义该虚拟机：
   virsh define origin.xml

4. 启动虚拟机
   可以使用“start + 虚拟机名称”命令来启动已定义的虚拟机：
   virsh start origin

5. 查看虚拟机的vnc端口
   使用vncdisplay来查看虚拟机使用vnc端口
   virsh vncdisplay origin
   virt-manager
   WebVirtCloud
   arp -an 52:50:0c:7a:20:01 （这里只根据通信缓存记录的mac 、IP地址手段做排查。也有可能找不到。最好的办法是自己写一个脚本跟网段内的所有服务器都ping一次，记录下mac、ip地址以后再查找就没问题）
   grep 52:50:0c:7a:20:01 -rn /var/lib/libvirt/dnsmasq
   vncviewer port-id （ssh sk@192.168.225.22 -L 5900:127.0.0.1:5900）

6. 关闭虚拟机
   最正常的关闭虚拟机的方式就是在虚拟机系统中执行关机命令来关闭系统，如果虚拟机系统支持acpi，还可以使用以下的命令在外部优雅地关闭该虚拟机：
   virsh shutdown origin
   如果虚拟机已死机，或是该虚拟机不再重要，需要删除，则可以使用以下的命令来直接对虚拟机造成“拔电源”的效果：
   virsh destroy origin

7. 删除虚拟机
   如果需要删除虚拟机，则需要执行undefine命令来取消该虚拟机的定义：
   virsh undefine origin

kvm虚拟机默认XML文件存放位置
/etc/libvirt/qemu

kvm虚拟机默认镜像文件存放位置
/var/lib/libvirt/images/



#### kvm虚拟机使用桥接联网的配置方法

默认情况下kvm虚拟机使用NAT方式来联网，如果希望使用桥接方式来联网，则需要按照以下的方式来进行配置：

1. 配置桥接网络
   已redhat系列的操作系统为例，我们需要在实体机中创建一个桥接设备，让实体机网卡及kvm虚拟机的网卡直接连接到这个桥接设备上，可以在/etc/sysconfig/network-scripts目录下创建配置文件ifcfg-br0来创建一个网桥设备br0：
   vim /etc/sysconfig/network-scripts/ifcfg-br0 ，实际上该网桥设备的配置与当前实体机使用的物理网卡的配置内容相似，只是类型是网桥而已。
   该配置文件内容如下：

```
DEVICE="br0"
ONBOOT="yes"
TYPE=Bridge
NM_CONTROLLED=no
BOOTPROTO="none"
IPADDR=192.168.12.17
NETMASK=255.255.255.0
GATEWAY=192.168.12.1
```

2. 配置物理网卡
   创建网桥设备br0之后，需要将当前实体机使用的物理网卡连接到这个网桥上，如果当前实体机使用的网卡是eth0，则此时ifcfg-eth0配置文件的内容需要修改为以下的样子：

```
DEVICE="eth0"
ONBOOT="yes"
TYPE=Ethernet
NM_CONTROLLED=no
BRIDGE=br0
```

可以看到，此时eth0的配置文件不需要指定IP，只需要指定连接至br0这个网桥即可。

3. 修改虚拟机配置文件
   此时在需要使用网桥来连接网络的虚拟机中配置网络如下即可：

```
<interface type='bridge'>
  <source bridge='br0'/>
  <model type='virtio'/>
</interface>
```

#### KVM使用NAT联网并为VM配置iptables端口转发
```bash
bro 10.128.128.6  # 物理网卡 
virbr0 192.168.122.1  # KVM NAT 网络设备 
vm 192.168.122.173  # 虚拟机IP

# 修改虚拟机网卡配置信息，使用固定IP
vim /etc/sysconfig/network-scripts/ifcfg-eth0
DEVICE="eth0"
ONBOOT="yes"
TYPE=Ethernet
NM_CONTROLLED=no
BOOTPROTO="none"
IPADDR=192.168.122.173
NETMASK=255.255.255.0
GATEWAY=192.168.122.1

# 在宿主机上开启主机路由
vi /etc/sysctl.conf
net.ipv4.ip_forward = 1

sysctl -p
#######################################################################################
查看宿主机iptables转发规则
iptables -vnL FORWARD --line-number

修改宿主机iptables转发规则，使虚拟机可以访问互联网 VM -> Internet(IP伪装)(SNAT)
# iptables -t nat -A POSTROUTING -o br0 -j MASQUERADE
or
# iptables -t nat -A POSTROUTING -o br0 -j SNAT --to-source 10.128.128.6
# iptables-save -t filter
# Generated by iptables-save v1.4.7 on Sun Aug 27 21:11:36 2017
*filter
:INPUT ACCEPT [32774:4290638]
:FORWARD ACCEPT [37:3108]
:OUTPUT ACCEPT [30753:6644732]
COMMIT
# Completed on Sun Aug 27 21:11:36 2017
#
# iptables-save -t nat
# Generated by iptables-save v1.4.7 on Sun Aug 27 21:11:40 2017
*nat
:PREROUTING ACCEPT [10:639]
:POSTROUTING ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
-A POSTROUTING -o br0 -j MASQUERADE
COMMIT
# Completed on Sun Aug 27 21:11:40 2017
#
#######################################################################################
修改宿主机iptables转发规则，以便可以从互联网访问虚拟机的固定端口 Internet -> VM
# iptables -t nat -A PREROUTING -i br0 -p tcp --dport 8283 -j DNAT --to-destination 192.168.122.173:22
# iptables-save -t nat
# Generated by iptables-save v1.4.7 on Sun Aug 27 21:43:20 2017
*nat
:PREROUTING ACCEPT [0:0]
:POSTROUTING ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
-A PREROUTING -i br0 -p tcp -m tcp --dport 8283 -j DNAT --to-destination 192.168.122.173:22
-A POSTROUTING -o br0 -j MASQUERADE
COMMIT
# Completed on Sun Aug 27 21:43:20 2017
#

# 测试从互联网访问虚拟机的固定端口
[root@server-1118 ~]# ssh root@10.128.128.6 -p 8283
The authenticity of host '[10.128.128.6]:8283 ([10.128.128.6]:8283)' can't be established.
ECDSA key fingerprint is 07:49:d2:5b:83:b3:a3:fa:6a:d1:03:b3:0a:b4:dc:a8.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '[10.128.128.6]:8283' (ECDSA) to the list of known hosts.
root@10.128.128.6's password:
Last login: Sun Aug 27 07:51:26 2017
[root@localhost ~]#
[root@localhost ~]# ifconfig -a
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.122.173  netmask 255.255.255.0  broadcast 192.168.122.255
        inet6 fe80::5054:ff:fe59:200c  prefixlen 64  scopeid 0x20<link>
        ether 52:54:00:59:20:0c  txqueuelen 1000  (Ethernet)
        RX packets 69534  bytes 133721222 (127.5 MiB)
        RX errors 0  dropped 10  overruns 0  frame 0
        TX packets 34272  bytes 2314362 (2.2 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1  (Local Loopback)
        RX packets 612  bytes 53052 (51.8 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 612  bytes 53052 (51.8 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
[root@localhost ~]#

```

#### KVM网络相关命令

```bash
##################### 默认网络设置 #####################
[root@localhost ~]# virsh net-list
Name                 State      Autostart     Persistent
----------------------------------------------------------
default              active     yes           yes
[root@localhost ~]#
[root@localhost ~]# virsh net-dumpxml default
<network connections='1'>
  <name>default</name>
  <uuid>51fd2ef1-9a3c-47f5-9b3c-dace21b0a21c</uuid>
  <forward mode='nat'>
    <nat>
      <port start='1024' end='65535'/>
    </nat>
  </forward>
  <bridge name='virbr0' stp='on' delay='0'/>
  <mac address='52:54:00:10:2b:fc'/>
  <ip address='192.168.122.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='192.168.122.2' end='192.168.122.254'/>
    </dhcp>
  </ip>
</network>
[root@localhost ~]#
[root@localhost ~]# cat /etc/libvirt/qemu/networks/default.xml
<!--
WARNING: THIS IS AN AUTO-GENERATED FILE. CHANGES TO IT ARE LIKELY TO BE
OVERWRITTEN AND LOST. Changes to this xml configuration should be made using:
  virsh net-edit default
or other application using the libvirt API.
-->
<network>
  <name>default</name>
  <uuid>51fd2ef1-9a3c-47f5-9b3c-dace21b0a21c</uuid>
  <forward mode='nat'/>
  <bridge name='virbr0' stp='on' delay='0'/>
  <mac address='52:54:00:10:2b:fc'/>
  <ip address='192.168.122.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='192.168.122.2' end='192.168.122.254'/>
    </dhcp>
  </ip>
</network>
[root@localhost ~]#
[root@localhost ~]# ifconfig -a
enp0s25: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.10.222  netmask 255.255.254.0  broadcast 192.168.11.255
        inet6 fe80::8668:3d77:497e:9025  prefixlen 64  scopeid 0x20<link>
        ether 28:d2:44:51:ac:67  txqueuelen 1000  (Ethernet)
        RX packets 115209  bytes 10252240 (9.7 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 196452  bytes 232895909 (222.1 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
        device interrupt 20  memory 0xf0600000-f0620000  
lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1  (Local Loopback)
        RX packets 156896  bytes 229075488 (218.4 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 156896  bytes 229075488 (218.4 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
virbr0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.122.1  netmask 255.255.255.0  broadcast 192.168.122.255
        ether 52:54:00:10:2b:fc  txqueuelen 1000  (Ethernet)
        RX packets 133  bytes 12033 (11.7 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 132  bytes 16986 (16.5 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
virbr0-nic: flags=4098<BROADCAST,MULTICAST>  mtu 1500
        ether 52:54:00:10:2b:fc  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
vnet0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet6 fe80::fc54:ff:fef9:e985  prefixlen 64  scopeid 0x20<link>
        ether fe:54:00:f9:e9:85  txqueuelen 1000  (Ethernet)
        RX packets 133  bytes 13895 (13.5 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 266  bytes 24186 (23.6 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
wlp3s0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        ether 5a:e6:fd:66:65:b5  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
[root@localhost ~]#
##################### 自定义NAT网络 #####################

# virsh net-destroy default  # destroy (stop) a network
Network default destroyed
# virsh net-undefine default  # undefine an inactive network
Network default has been undefined
# cat default_net.xml
<network connections='1'>
  <name>default</name>
  <forward mode='nat'>
    <nat>
      <port start='1024' end='65535'/>
    </nat>
  </forward>
  <bridge name='virbr0' stp='on' delay='0'/>
  <mac address='52:54:00:49:af:87'/>
  <ip address='192.168.122.1' netmask='255.255.255.0'>
    <dhcp>
        <range start='192.168.122.2' end='192.168.122.254'/>
        <host mac='52:50:0c:7a:20:01' name='rms01' ip='192.168.122.101'/>
            <host mac='52:50:0c:7a:20:02' name='rms02' ip='192.168.122.102'/>
            <host mac='52:50:0c:7a:20:03' name='rms03' ip='192.168.122.103'/>
            <host mac='52:50:0c:7a:20:04' name='rms04' ip='192.168.122.104'/>
            <host mac='52:50:0c:7a:20:05' name='rms05' ip='192.168.122.105'/>
            <host mac='52:50:0c:7a:20:06' name='rms06' ip='192.168.122.106'/>
            <host mac='52:50:0c:7a:20:07' name='rms07' ip='192.168.122.107'/>
            <host mac='52:50:0c:7a:20:08' name='rms08' ip='192.168.122.108'/>
            <host mac='52:50:0c:7a:20:09' name='rms09' ip='192.168.122.109'/>
            <host mac='52:50:0c:7a:20:0a' name='rms10' ip='192.168.122.110'/>
            <host mac='52:50:0c:7a:20:0b' name='rms11' ip='192.168.122.111'/>
            <host mac='52:50:0c:7a:20:0c' name='rms12' ip='192.168.122.112'/>
            <host mac='52:50:0c:7a:20:0d' name='rms13' ip='192.168.122.113'/>
            <host mac='52:50:0c:7a:20:0e' name='rms14' ip='192.168.122.114'/>
            <host mac='52:50:0c:7a:20:0f' name='rms15' ip='192.168.122.115'/>
            <host mac='52:50:0c:7a:20:10' name='rms16' ip='192.168.122.116'/>
            <host mac='52:50:0c:7a:20:11' name='rms17' ip='192.168.122.117'/>
            <host mac='52:50:0c:7a:20:12' name='rms18' ip='192.168.122.118'/>
            <host mac='52:50:0c:7a:20:13' name='rms19' ip='192.168.122.119'/>
            <host mac='52:50:0c:7a:20:14' name='rms20' ip='192.168.122.120'/>
    </dhcp>
  </ip>
</network>
#
# virsh net-define default_net.xml  # define (but don't start) a network from an XML file
Network default defined from default_net.xml
# virsh net-autostart default  # autostart a network
Network default marked as autostarted
#
# service libvirtd restart
#

##################### 自定义bridge网络 #####################

[root@server-1116 ~]# virsh net-dumpxml bridge
<network connections='1'>
  <name>bridge</name>
  <uuid>53236fab-521e-a095-6a22-89845bdea872</uuid>
  <forward mode='bridge'/>
  <bridge name='br0' />
</network>
[root@server-1116 ~]#
[root@server-1116 ~]# cat /etc/libvirt/qemu/networks/bridge.xml
<!--
WARNING: THIS IS AN AUTO-GENERATED FILE. CHANGES TO IT ARE LIKELY TO BE
OVERWRITTEN AND LOST. Changes to this xml configuration should be made using:
  virsh net-edit bridge
or other application using the libvirt API.
-->
<network>
  <name>bridge</name>
  <uuid>53236fab-521e-a095-6a22-89845bdea872</uuid>
  <forward mode='bridge'/>
  <bridge name='br0' />
</network>
[root@server-1116 ~]#

```

#### KVM采用纯命令行界面安装
```bash
#创建guest所需的磁盘
qemu-img create -f qcow2 /img/os/rms-test.img 30G

# 命令行界面安装KVM虚拟机
virt-install --name=rms-test --ram=8192 --vcpus=4 --os-type=linux --location=/img/os/CentOS-7-x86_64-Minimal-1611.iso --disk path=/img/os/rms-test-05.img,format=qcow2 --network network=default --graphics none --extra-args='console=tty0 console=ttyS0,115200n8 serial'

virt-install --name Ubuntu-16.04 --ram=512 --vcpus=1 --cpu host --hvm --disk path=/var/lib/libvirt/images/ubuntu-16.04-vm1,size=8 --cdrom /var/lib/libvirt/boot/ubuntu-16.04-server-amd64.iso --graphics vnc

#连接虚拟机
virsh console rms-test
```



#### 连接远程 KVM 服务

```bash
root@jump:~/.ssh# virsh --connect=qemu+ssh://root@192.168.10.234:1116/system
Welcome to virsh, the virtualization interactive terminal.
Type:  'help' for help with commands
       'quit' to quit
virsh # list
Id    Name                           State
----------------------------------------------------
virsh # list --all
Id    Name                           State
----------------------------------------------------
-     agg-web-avi                    shut off
-     api-avl                        shut off
-     desktop                        shut off
-     docker-01                      shut off
-     docker-02                      shut off
-     docker-03                      shut off
-     es-data-01-avl                 shut off
-     es-data-02-avl                 shut off
-     es-data-04-avl                 shut off
-     es-master-01-a                 shut off
-     es-master-02                   shut off
-     es-test-wj                     shut off
-     horse_test                     shut off
-     k8s-m                          shut off
-     k8s-m-o                        shut off
-     k8s-w                          shut off
-     mongo-test-01                  shut off
-     operating-6001                 shut off
-     rms-test                       shut off
-     rms-test-01                    shut off
-     rms-test-other                 shut off
-     rms01                          shut off
-     rms02                          shut off
-     rms03                          shut off
-     rmsparse                       shut off
-     web-avi-test                   shut off
-     wordpress                      shut off
virsh #

## python连接远程KVM服务
root@huzhi-dev:/srv/webvirtcloud# python
Python 2.7.12 (default, Nov 20 2017, 18:23:56)
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import libvirt
>>> conn=libvirt.open("qemu+ssh://root@192.168.10.234:1116/system")
>>> names = conn.listDefinedDomains()
>>> print names
['es-data-02-avl', 'mongo-test-01', 'rms-test-other', 'es-test-wj', 'docker-01', 'desktop', 'es-master-01-a', 'k8s-w', 'rmsparse', 'es-data-04-avl', 'es-data-01-avl', 'es-master-02', 'rms-test', 'rms01', 'rms03', 'docker-02', 'k8s-m-o', 'web-avi-test', 'rms02', 'agg-web-avi', 'operating-6001', 'wordpress', 'k8s-m', 'horse_test', 'docker-03', 'api-avl', 'rms-test-01']
>>>
```




#### 相关文件列表

```bash
## kvm模拟器
# rpm -ql qemu-kvm
/etc/ksmtuned.conf
/etc/modprobe.d/blacklist-kvm.conf
/etc/rc.d/init.d/ksm
/etc/rc.d/init.d/ksmtuned
/etc/sasl2/qemu-kvm.conf
/etc/sysconfig/ksm
/etc/sysconfig/modules/kvm.modules
/etc/udev/rules.d/80-kvm.rules
/usr/libexec/qemu-kvm  ## 模拟器，虚拟机需要使用该路径定义模拟器位置
/usr/sbin/ksmtuned

## kvm磁盘管理
# rpm -ql qemu-img
/usr/bin/qemu-img
/usr/bin/qemu-io

## kvm server
# rpm -ql libvirt
/etc/libvirt
/etc/libvirt/libvirtd.conf
/etc/libvirt/lxc.conf
/etc/libvirt/nwfilter
/etc/libvirt/nwfilter/allow-arp.xml
/etc/libvirt/nwfilter/allow-dhcp-server.xml
/etc/libvirt/nwfilter/allow-dhcp.xml
/etc/libvirt/nwfilter/allow-incoming-ipv4.xml
/etc/libvirt/nwfilter/allow-ipv4.xml
/etc/libvirt/nwfilter/clean-traffic.xml
/etc/libvirt/nwfilter/no-arp-ip-spoofing.xml
/etc/libvirt/nwfilter/no-arp-mac-spoofing.xml
/etc/libvirt/nwfilter/no-arp-spoofing.xml
/etc/libvirt/nwfilter/no-ip-multicast.xml
/etc/libvirt/nwfilter/no-ip-spoofing.xml
/etc/libvirt/nwfilter/no-mac-broadcast.xml
/etc/libvirt/nwfilter/no-mac-spoofing.xml
/etc/libvirt/nwfilter/no-other-l2-traffic.xml
/etc/libvirt/nwfilter/no-other-rarp-traffic.xml
/etc/libvirt/nwfilter/qemu-announce-self-rarp.xml
/etc/libvirt/nwfilter/qemu-announce-self.xml
/etc/libvirt/qemu ## kvm虚拟机的xml文件存放地址
/etc/libvirt/qemu.conf
/etc/libvirt/qemu/networks
/etc/libvirt/qemu/networks/autostart
/etc/logrotate.d/libvirtd
/etc/logrotate.d/libvirtd.lxc
/etc/logrotate.d/libvirtd.qemu
/etc/rc.d/init.d/libvirtd ## kvm虚拟机常驻进程
/etc/sysconfig/libvirtd
/etc/sysctl.d/libvirtd
/usr/libexec/libvirt_iohelper
/usr/libexec/libvirt_lxc
/usr/libexec/libvirt_parthelper
/usr/sbin/libvirtd
/var/cache/libvirt
/var/cache/libvirt/qemu
/var/lib/libvirt/boot
/var/lib/libvirt/dnsmasq
/var/lib/libvirt/filesystems
/var/lib/libvirt/images
/var/lib/libvirt/lxc
/var/lib/libvirt/network
/var/lib/libvirt/qemu
/var/log/libvirt
/var/log/libvirt/lxc
/var/log/libvirt/qemu
/var/log/libvirt/uml
/var/run/libvirt
/var/run/libvirt/lxc
/var/run/libvirt/network
/var/run/libvirt/qemu

## kvm命令行管理虚拟机
# rpm -ql libvirt-client
/etc/libvirt/libvirt.conf
/etc/rc.d/init.d/libvirt-guests
/etc/sasl2/libvirt.conf
/etc/sysconfig/libvirt-guests
/usr/bin/virsh
/usr/bin/virt-host-validate
/usr/bin/virt-pki-validate
/usr/bin/virt-xml-validate
/var/lib/libvirt

## kvm命令行安装虚拟机
# rpm -ql virt-install
/usr/bin/virt-clone
/usr/bin/virt-install
/usr/bin/virt-xml

# rpm -ql python-virtinst-0.600.0-31.el6.noarch ( 替换virt-install )
/usr/bin/virt-clone
/usr/bin/virt-convert
/usr/bin/virt-image
/usr/bin/virt-install
/usr/sbin/virt-install

## libvirt API的Python接口封装, libvirt是kvm常驻进程
# rpm -ql libvirt-python

## libvirt-client图形界面，libvirt-client是kvm命令行管理虚拟机
# rpm -ql virt-manager
/etc/gconf/schemas/virt-manager.schemas
/usr/bin/virt-manager
/usr/libexec/virt-manager-launch

qemu-img
/usr/bin/qemu-img
/usr/bin/qemu-io

libvirt-client
/usr/bin/virsh
/usr/bin/virt-host-validate
/usr/bin/virt-pki-validate
/usr/bin/virt-xml-validate

virt-install(python-virtinst-0.600.0-31.el6.noarch)
/usr/bin/virt-clone
/usr/bin/virt-convert
/usr/bin/virt-image
/usr/bin/virt-install

virt-manager
/usr/bin/virt-manager
```



参考：

[在 Ubuntu 18.04 LTS 上使用 KVM 配置无头虚拟化服务器](https://linux.cn/article-10121-1.html)

[Setup Headless Virtualization Server Using KVM In Ubuntu 18.04 LTS](https://www.ostechnix.com/setup-headless-virtualization-server-using-kvm-ubuntu/)

[qemu 用户空间](https://www.linux-kvm.org/page/Documents)

[Ubuntu上使用kvm](https://help.ubuntu.com/community/KVM)

[CentOS上使用kvm](https://wiki.centos.org/HowTos/KVM)

