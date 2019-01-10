## ulogd

#### ulogd安装以及基础概念

```bash
# ulogd 相关软件包
# 参考 https://pkgs.org/download/ulogd
$ yum search ulogd
ulogd-libdbi.x86_64 : Libdbi framework output plugin for ulogd
ulogd-mysql.x86_64 : MySQL output plugin for ulogd
ulogd-pcap.x86_64 : PCAP output plugin for ulogd
ulogd-pgsql.x86_64 : PostgreSQL output plugin for ulogd
ulogd-sqlite.x86_64 : SQLITE output plugin for ulogd
ulogd.x86_64 : Userspace logging daemon for netfilter

# 安装
$ yum install ulogd.x86_64

# 相关文件
$ rpm -ql ulogd.x86_64
/etc/logrotate.d/ulogd
/etc/rc.d/init.d/ulogd  ## systemctl status ulogd
/etc/ulogd.conf  ## 配置文件
/usr/lib64/ulogd  ## ulogd 使用的插件
/usr/lib64/ulogd/ulogd_filter_HWHDR.so
/usr/lib64/ulogd/ulogd_filter_IFINDEX.so
/usr/lib64/ulogd/ulogd_filter_IP2BIN.so
/usr/lib64/ulogd/ulogd_filter_IP2HBIN.so
/usr/lib64/ulogd/ulogd_filter_IP2STR.so
/usr/lib64/ulogd/ulogd_filter_MARK.so
/usr/lib64/ulogd/ulogd_filter_PRINTFLOW.so
/usr/lib64/ulogd/ulogd_filter_PRINTPKT.so
/usr/lib64/ulogd/ulogd_filter_PWSNIFF.so
/usr/lib64/ulogd/ulogd_inpflow_NFACCT.so
/usr/lib64/ulogd/ulogd_inpflow_NFCT.so
/usr/lib64/ulogd/ulogd_inppkt_NFLOG.so
/usr/lib64/ulogd/ulogd_inppkt_ULOG.so
/usr/lib64/ulogd/ulogd_inppkt_UNIXSOCK.so
/usr/lib64/ulogd/ulogd_output_GPRINT.so
/usr/lib64/ulogd/ulogd_output_GRAPHITE.so
/usr/lib64/ulogd/ulogd_output_LOGEMU.so
/usr/lib64/ulogd/ulogd_output_NACCT.so
/usr/lib64/ulogd/ulogd_output_OPRINT.so
/usr/lib64/ulogd/ulogd_output_SYSLOG.so
/usr/lib64/ulogd/ulogd_output_XML.so
/usr/lib64/ulogd/ulogd_raw2packet_BASE.so
/usr/sbin/ulogd  ## ulogd 可执行文件
/usr/share/doc/ulogd-2.0.5
/usr/share/doc/ulogd-2.0.5/AUTHORS
/usr/share/doc/ulogd-2.0.5/COPYING
/usr/share/doc/ulogd-2.0.5/README
/usr/share/doc/ulogd-2.0.5/ulogd.html  ## ulogd 详细介绍文件
/usr/share/doc/ulogd-2.0.5/ulogd.ps
/usr/share/doc/ulogd-2.0.5/ulogd.txt
/usr/share/man/man8/ulogd.8.gz
/var/log/ulogd

# 配置文件详细内容
# 参考 ulogd 详细介绍文件 /usr/share/doc/ulogd-2.0.5/ulogd.html
$ cat /etc/ulogd.conf
# Example configuration for ulogd
# Adapted to Debian by Achilleas Kotsis <achille@debian.gr>

[global]
######################################################################
# GLOBAL OPTIONS
######################################################################


# logfile for status messages
logfile="/var/log/ulogd/ulogd.log"

# loglevel: debug(1), info(3), notice(5), error(7) or fatal(8) (default 5)
# loglevel=1

######################################################################
# PLUGIN OPTIONS
######################################################################

# We have to configure and load all the plugins we want to use

# general rules:
# 1. load the plugins _first_ from the global section
# 2. options for each plugin in seperate section below

# 此选项后跟一个ulogd插件的文件名，ulogd应在初始化时加载。 此选项可能会出现多次。
# 插件包含 'Input Plugins'、'Filter Plugins'、'Output Plugins'
plugin="/usr/lib64/ulogd/ulogd_inppkt_NFLOG.so"
#plugin="/usr/lib64/ulogd/ulogd_inppkt_ULOG.so"
#plugin="/usr/lib64/ulogd/ulogd_inppkt_UNIXSOCK.so"
plugin="/usr/lib64/ulogd/ulogd_inpflow_NFCT.so"
plugin="/usr/lib64/ulogd/ulogd_filter_IFINDEX.so"
plugin="/usr/lib64/ulogd/ulogd_filter_IP2STR.so"
plugin="/usr/lib64/ulogd/ulogd_filter_IP2BIN.so"
#plugin="/usr/lib64/ulogd/ulogd_filter_IP2HBIN.so"
plugin="/usr/lib64/ulogd/ulogd_filter_PRINTPKT.so"
plugin="/usr/lib64/ulogd/ulogd_filter_HWHDR.so"
plugin="/usr/lib64/ulogd/ulogd_filter_PRINTFLOW.so"
#plugin="/usr/lib64/ulogd/ulogd_filter_MARK.so"
plugin="/usr/lib64/ulogd/ulogd_output_LOGEMU.so"
plugin="/usr/lib64/ulogd/ulogd_output_SYSLOG.so"
plugin="/usr/lib64/ulogd/ulogd_output_XML.so"
#plugin="/usr/lib64/ulogd/ulogd_output_SQLITE3.so"
plugin="/usr/lib64/ulogd/ulogd_output_GPRINT.so"
#plugin="/usr/lib64/ulogd/ulogd_output_NACCT.so"
#plugin="/usr/lib64/ulogd/ulogd_output_PCAP.so"
#plugin="/usr/lib64/ulogd/ulogd_output_PGSQL.so"
#plugin="/usr/lib64/ulogd/ulogd_output_MYSQL.so"
#plugin="/usr/lib64/ulogd/ulogd_output_DBI.so"
plugin="/usr/lib64/ulogd/ulogd_raw2packet_BASE.so"
plugin="/usr/lib64/ulogd/ulogd_inpflow_NFACCT.so"
plugin="/usr/lib64/ulogd/ulogd_output_GRAPHITE.so"
#plugin="/usr/lib64/ulogd/ulogd_output_JSON.so"

# 此选项后面是一个插件实例列表，它将以输入插件开头，包含可选的过滤插件并由输出插件完成。 此选项可能会出现多次。
# 通过 input 插件获取获取网络包，通过 filter 插件处理网络包，最后通过 output 插件存储数据包
# stack 定义要使用的插件，并且定义插件的顺序
# this is a stack for logging packet send by system via LOGEMU
#stack=log1:NFLOG,base1:BASE,ifi1:IFINDEX,ip2str1:IP2STR,print1:PRINTPKT,emu1:LOGEMU

# this is a stack for packet-based logging via LOGEMU
#stack=log2:NFLOG,base1:BASE,ifi1:IFINDEX,ip2str1:IP2STR,print1:PRINTPKT,emu1:LOGEMU

# this is a stack for ULOG packet-based logging via LOGEMU
#stack=ulog1:ULOG,base1:BASE,ip2str1:IP2STR,print1:PRINTPKT,emu1:LOGEMU

# this is a stack for packet-based logging via LOGEMU with filtering on MARK
#stack=log2:NFLOG,mark1:MARK,base1:BASE,ifi1:IFINDEX,ip2str1:IP2STR,print1:PRINTPKT,emu1:LOGEMU

# this is a stack for packet-based logging via GPRINT
#stack=log1:NFLOG,gp1:GPRINT

# this is a stack for flow-based logging via LOGEMU
#stack=ct1:NFCT,ip2str1:IP2STR,print1:PRINTFLOW,emu1:LOGEMU

# this is a stack for flow-based logging via GPRINT
#stack=ct1:NFCT,gp1:GPRINT

# this is a stack for flow-based logging via XML
#stack=ct1:NFCT,xml1:XML

# this is a stack for logging in XML
#stack=log1:NFLOG,xml1:XML

# this is a stack for accounting-based logging via XML
#stack=acct1:NFACCT,xml1:XML

# this is a stack for accounting-based logging to a Graphite server
#stack=acct1:NFACCT,graphite1:GRAPHITE

# this is a stack for NFLOG packet-based logging to PCAP
#stack=log2:NFLOG,base1:BASE,pcap1:PCAP

# this is a stack for logging packet to MySQL
#stack=log2:NFLOG,base1:BASE,ifi1:IFINDEX,ip2bin1:IP2BIN,mac2str1:HWHDR,mysql1:MYSQL

# this is a stack for logging packet to PGsql after a collect via NFLOG
#stack=log2:NFLOG,base1:BASE,ifi1:IFINDEX,ip2str1:IP2STR,mac2str1:HWHDR,pgsql1:PGSQL

# this is a stack for logging packet to JSON formatted file after a collect via NFLOG
#stack=log2:NFLOG,base1:BASE,ifi1:IFINDEX,ip2str1:IP2STR,mac2str1:HWHDR,json1:JSON

# this is a stack for logging packets to syslog after a collect via NFLOG
#stack=log3:NFLOG,base1:BASE,ifi1:IFINDEX,ip2str1:IP2STR,print1:PRINTPKT,sys1:SYSLOG

# this is a stack for logging packets to syslog after a collect via NuFW
#stack=nuauth1:UNIXSOCK,base1:BASE,ip2str1:IP2STR,print1:PRINTPKT,sys1:SYSLOG

# this is a stack for flow-based logging to MySQL
#stack=ct1:NFCT,ip2bin1:IP2BIN,mysql2:MYSQL

# this is a stack for flow-based logging to PGSQL
#stack=ct1:NFCT,ip2str1:IP2STR,pgsql2:PGSQL

# this is a stack for flow-based logging to PGSQL without local hash
#stack=ct1:NFCT,ip2str1:IP2STR,pgsql3:PGSQL

# this is a stack for flow-based logging to SQLITE3
#stack=ct1:NFCT,sqlite3_ct:SQLITE3

# this is a stack for logging packet to SQLITE3
#stack=log1:NFLOG,sqlite3_pkt:SQLITE3

# this is a stack for flow-based logging in NACCT compatible format
#stack=ct1:NFCT,ip2str1:IP2STR,nacct1:NACCT

# this is a stack for accounting-based logging via GPRINT
#stack=acct1:NFACCT,gp1:GPRINT

# 每个插件的配置
[ct1]
#netlink_socket_buffer_size=217088
#netlink_socket_buffer_maxsize=1085440
#netlink_resync_timeout=60 # seconds to wait to perform resynchronization
#pollinterval=10 # use poll-based logging instead of event-driven
# If pollinterval is not set, NFCT plugin will work in event mode
# In this case, you can use the following filters on events:
#accept_src_filter=192.168.1.0/24,1:2::/64 # source ip of connection must belong to these networks
#accept_dst_filter=192.168.1.0/24 # destination ip of connection must belong to these networks
#accept_proto_filter=tcp,sctp # layer 4 proto of connections

[ct2]
#netlink_socket_buffer_size=217088
#netlink_socket_buffer_maxsize=1085440
#reliable=1 # enable reliable flow-based logging (may drop packets)
hash_enable=0

# Logging of system packet through NFLOG
[log1]
# netlink multicast group (the same as the iptables --nflog-group param)
# Group O is used by the kernel to log connection tracking invalid message
group=0
#netlink_socket_buffer_size=217088
#netlink_socket_buffer_maxsize=1085440
# set number of packet to queue inside kernel
#netlink_qthreshold=1
# set the delay before flushing packet in the queue inside kernel (in 10ms)
#netlink_qtimeout=100

# packet logging through NFLOG for group 1
[log2]
# netlink multicast group (the same as the iptables --nflog-group param)
group=1 # Group has to be different from the one use in log1
#netlink_socket_buffer_size=217088
#netlink_socket_buffer_maxsize=1085440
# If your kernel is older than 2.6.29 and if a NFLOG input plugin with
# group 0 is not used by any stack, you need to have at least one NFLOG
# input plugin with bind set to 1. If you don't do that you may not
# receive any message from the kernel.
#bind=1

# packet logging through NFLOG for group 2, numeric_label is
# set to 1
[log3]
# netlink multicast group (the same as the iptables --nflog-group param)
group=2 # Group has to be different from the one use in log1/log2
numeric_label=1 # you can label the log info based on the packet verdict
#netlink_socket_buffer_size=217088
#netlink_socket_buffer_maxsize=1085440
#bind=1

[ulog1]
# netlink multicast group (the same as the iptables --ulog-nlgroup param)
nlgroup=1
#numeric_label=0 # optional argument

[nuauth1]
socket_path="/tmp/nuauth_ulogd2.sock"

[emu1]
file="/var/log/ulogd/ulogd_syslogemu.log"
sync=1

[op1]
file="/var/log/ulogd/ulogd_oprint.log"
sync=1

[gp1]
file="/var/log/ulogd/ulogd_gprint.log"
sync=1
timestamp=1

[xml1]
directory="/var/log/ulogd/"
sync=1

[json1]
sync=1
#file="/var/log/ulogd/ulogd.json"
#timestamp=0
# device name to be used in JSON message
#device="My awesome Netfilter firewall"
# If boolean_label is set to 1 then the numeric_label put on packet
# by the input plugin is coding the action on packet: if 0, then
# packet has been blocked and if non null it has been accepted.
#boolean_label=1

[pcap1]
#default file is /var/log/ulogd/ulogd.pcap
#file="/var/log/ulogd/ulogd.pcap"
sync=1

[mysql1]
db="nulog"
host="localhost"
user="nupik"
table="ulog"
pass="changeme"
procedure="INSERT_PACKET_FULL"
# backlog configuration:
# set backlog_memcap to the size of memory that will be
# allocated to store events in memory if data is temporary down
# and insert them when the database came back.
#backlog_memcap=1000000
# number of events to insert at once when backlog is not empty
#backlog_oneshot_requests=10

[mysql2]
db="nulog"
host="localhost"
user="nupik"
table="conntrack"
pass="changeme"
procedure="INSERT_CT"

[pgsql1]
db="nulog"
host="localhost"
user="nupik"
table="ulog"
#schema="public"
pass="changeme"
procedure="INSERT_PACKET_FULL"
# connstring can be used to define PostgreSQL connection string which
# contains all parameters of the connection. If set, this value has
# precedence on other variables used to build the connection string.
# See http://www.postgresql.org/docs/9.2/static/libpq-connect.html#LIBPQ-CONNSTRING
# for a complete description of options.
#connstring="host=localhost port=4321 dbname=nulog user=nupik password=changeme"
#backlog_memcap=1000000
#backlog_oneshot_requests=10
# If superior to 1 a thread dedicated to SQL request execution
# is created. The value stores the number of SQL request to keep
# in the ring buffer
#ring_buffer_size=1000

[pgsql2]
db="nulog"
host="localhost"
user="nupik"
table="ulog2_ct"
#schema="public"
pass="changeme"
procedure="INSERT_CT"

[pgsql3]
db="nulog"
host="localhost"
user="nupik"
table="ulog2_ct"
#schema="public"
pass="changeme"
procedure="INSERT_OR_REPLACE_CT"

[pgsql4]
db="nulog"
host="localhost"
user="nupik"
table="nfacct"
#schema="public"
pass="changeme"
procedure="INSERT_NFACCT"

[dbi1]
db="ulog2"
dbtype="pgsql"
host="localhost"
user="ulog2"
table="ulog"
pass="ulog2"
procedure="INSERT_PACKET_FULL"

[sqlite3_ct]
table="ulog_ct"
db="/var/log/ulogd/ulogd.sqlite3db"
buffer=200

[sqlite3_pkt]
table="ulog_pkt"
db="/var/log/ulogd/ulogd.sqlite3db"
buffer=200

[sys2]
facility=LOG_LOCAL2

[nacct1]
sync = 1
#file = /var/log/ulogd/ulogd_nacct.log

[mark1]
mark = 1

[acct1]
pollinterval = 2
# If set to 0, we don't reset the counters for each polling (default is 1).
#zerocounter = 0
# Set timestamp (default is 0, which means not set). This timestamp can be
# interpreted by the output plugin.
#timestamp = 1

[graphite1]
host="127.0.0.1"
port="2003"
# Prefix of data name sent to graphite server
prefix="netfilter.nfacct"

# 安装 mysql 插件，mysql 插件属于 Output Plugins
$ yum install ulogd-mysql.x86_64
$ rpm -ql ulogd-mysql.x86_64 
/usr/lib64/ulogd/ulogd_output_MYSQL.so
/usr/share/doc/ulogd-mysql-2.0.5
/usr/share/doc/ulogd-mysql-2.0.5/COPYING

# 要使用数据库作为最后的存储，需要对数据库做一些初始化操作

```



#### ulogd 使用方法

```bash
# 在每个 iptables 规则前加上日志
# 日志规则的目标是 -j NFLOG
# To use the NFCT or NFLOG input plugin, you will need a 2.6.14 or later kernel. 
# For old-style ULOG logging, you need a kernel >= 2.4.18.
# 定义日志规则就是使用 ulogd 的 input 插件
$ iptables -A FORWARD --nflog-group 32 --nflog-prefix foo -j NFLOG
$ iptables -A FORWARD -j ACCEPT
$ iptables -A FORWARD --nflog-group 32 --nflog-prefix foo -j ULOG

```

