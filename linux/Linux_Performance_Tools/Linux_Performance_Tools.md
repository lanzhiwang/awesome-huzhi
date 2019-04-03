## Linux Performance Tools

![](./02_linux_observability_tools.png)

### strace

```bash
# Basic stracing
strace <command>

# save the trace to a file
strace -o strace.out <other switches> <command>

# follow only the open() system call
strace -e trace=open <command>

# follow all the system calls which open a file
strace -e trace=file <command>

# follow all the system calls associated with process
# management
strace -e trace=process <command>

# follow child processes as they are created
strace -f <command>

# count time, calls and errors for each system call
strace -c <command>

# trace a running process (multiple PIDs can be specified)
strace -p <pid>

$
```

### ltrace

```bash
# 
# ltrace
# 
# Display dynamic library calls of a process.
# 
# Print (trace) library calls of a program binary:
  ltrace ./program
# 
# Count library calls. Print a handy summary at the bottom:
  ltrace -c /path/to/program
# 
# Trace calls to malloc and free, omit those done by libc:
  ltrace -e malloc+free-@libc.so* /path/to/program
# 
# Write to file instead of terminal:
  ltrace -o file /path/to/program
# 
# 

$
```

### ss

```bash
# Utility to investigate sockets
#
# Options:
#   -4/-6   list ipv4/ipv6 sockets
#   -n      numeric addresses instead of hostnames
#   -l      list listening sockets
#   -u/-t/-x list udp/tcp/unix sockets
#   -p      Show process(es) that using socket

# show all listening tcp sockets including the corresponding process
ss -tlp

# show all sockets connecting to 192.168.2.1 on port 80
ss -t dst 192.168.2.1:80

# show all ssh related connection
# documentation on the filter syntax: sudo apt-get install iproute2-doc
ss -t state established '( dport = :ssh or sport = :ssh )'

# Display timer information
ss -tn -o

# Filtering connections by tcp state
ss -t4 state established

$
```

### netstat

```bash
# WARNING ! netstat is deprecated. Look below.

# To view which users/processes are listening to which ports:
sudo netstat -lnptu

# To view routing table (use -n flag to disable DNS lookups):
netstat -r

# Which process is listening to port <port>
netstat -pln | grep <port> | awk '{print $NF}'

Example output: 1507/python

# Fast display of ipv4 tcp listening programs
sudo netstat -vtlnp --listening -4

# WARNING ! netstat is deprecated.
# Replace it by:
ss

# For netstat-r
ip route

# For netstat -i
ip -s link

# For netstat-g
ip maddr

$
```

* sysdig
### perf

```bash
# 
# perf
# 
# Framework for linux performance counter measurements.
# 
# Display basic performance counter stats for a command:
  perf stat gcc hello.c
# 
# Display system-wide real time performance counter profile:
  sudo perf top
# 
# Run a command and record its profile into "perf.data":
  sudo perf record command
# 
# Read "perf.data" (created by perf record) and display the profile:
  sudo perf report
# 
# 

$
```

### sar

```bash
# 
# sar
# 
# Monitor performance of various Linux subsystems.
# 
# Report I/O and transfer rate issued to physical devices, one per second (press CTRL+C to quit):
  sar -b 1
# 
# Report a total of 10 network device statistics, one per 2 seconds:
  sar -n DEV 2 10
# 
# Report CPU utilization, one per 2 seconds:
  sar -u ALL 2
# 
# Report a total of 20 memory utilization statistics, one per second:
  sar -r ALL 1 20
# 
# Report the run queue length and load averages, one per second:
  sar -q 1
# 
# Report paging statistics, one per 5 seconds:
  sar -B 5
# 
# 

$
```

* dstat
### dmesg

```bash
# Clear dmesg Buffer Logs
dmesg -c

# Display the local time and the delta in human-readable format. Conversion to the local time could be inaccurate
dmesg -e

# Print human-readable timestamps.
dmesg -T

# Human-readable output (color + reltime)
dmesg -H

$
```

* turbostat
* rdmsr
### mpstat

```bash
 
# mpstat
# 
# Report CPU statistics.
# 
# Display CPU statistics every 2 seconds:
  mpstat 2
# 
# Display 5 reports, one by one, at 2 second intervals:
  mpstat 2 5
# 
# Display 5 reports, one by one, from a given processor, at 2 second intervals:
  mpstat -P 0 2 5
# 
# 

$
```

### top

```bash
# Update every <interval> samples:
top -i <interval>

# Set the delay between updates to <delay> seconds:
top -s <delay>

# Set event counting to accumulative mode:
top -a

# Set event counting to delta mode:
top -d

# Set event counting to absolute mode:
top -e

# Do not calculate statistics on shared libraries, also known as frameworks:
top -F

# Calculate statistics on shared libraries, also known as frameworks (default):
top -f

# Print command line usage information and exit:
top -h

# Order the display by sorting on <key> in descending order
top -o <key>

$
```

### ps

```bash
# To list every process on the system:
ps aux

# To list a process tree
ps axjf

# To list every process owned by foouser:
ps -aufoouser

# To list every process with a user-defined format:
ps -eo pid,user,command

# Exclude grep from your grepped output of ps.
# Add [] to the first letter. Ex: sshd -> [s]shd
ps aux | grep '[h]ttpd'

$
```

* pidstat
* tiptop
* vmstat
* slabtop
### free

```bash
# 
# free
# 
# Display amount of free and used memory in the system.
# 
# Display system memory:
  free
# 
# Display memory in Bytes/KB/MB/GB:
  free -b|k|m|g
# 
# Display memory in human readable units:
  free -h
# 
# Refresh the output every 2 seconds:
  free -s 2
# 
# 

$
```

* numastat
### tcpdump

```bash
# TCPDump is a packet analyzer. It allows the user to intercept and display TCP/IP
# and other packets being transmitted or received over a network. (cf Wikipedia).
# Note: 173.194.40.120 => google.com

# Intercepts all packets on eth0
tcpdump -i eth0

# Intercepts all packets from/to 173.194.40.120
tcpdump host 173.194.40.120

# Intercepts all packets on all interfaces from / to 173.194.40.120 port 80
# -nn => Disables name resolution for IP addresses and port numbers.
tcpdump -nn -i any host 173.194.40.120 and port 80

# Make a grep on tcpdump (ASCII)
# -A  => Show only ASCII in packets.
# -s0 => By default, tcpdump only captures 68 bytes.
tcpdump -i -A any host 173.194.40.120 and port 80 | grep 'User-Agent'

# With ngrep
# -d eth0 => To force eth0 (else ngrep work on all interfaces)
# -s0 => force ngrep to look at the entire packet. (Default snaplen: 65536 bytes)
ngrep 'User-Agent' host 173.194.40.120 and port 80

# Intercepts all packets on all interfaces from / to 8.8.8.8 or 173.194.40.127 on port 80
tcpdump 'host ( 8.8.8.8 or 173.194.40.127 ) and port 80' -i any

# Intercepts all packets SYN and FIN of each TCP session.
tcpdump 'tcp[tcpflags] & (tcp-syn|tcp-fin) != 0'

# To display SYN and FIN packets of each TCP session to a host that is not on our network
tcpdump 'tcp[tcpflags] & (tcp-syn|tcp-fin) != 0 and not src and dst net local_addr'

# To display all IPv4 HTTP packets that come or arrive on port 80 and that contain only data (no SYN, FIN no, no packet containing an ACK)
tcpdump 'tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'

# Saving captured data
tcpdump -w file.cap

# Reading from capture file
tcpdump -r file.cap

# Show content in hexa
# Change -x to -xx => show extra header (ethernet).
tcpdump -x

# Show content in hexa and ASCII
# Change -X to -XX => show extra header (ethernet).
tcpdump -X

# Note on packet maching:
# Port matching:
# - portrange 22-23
# - not port 22
# - port ssh
# - dst port 22
# - src port 22
#
# Host matching:
# - dst host 8.8.8.8
# - not dst host 8.8.8.8
# - src net 67.207.148.0 mask 255.255.255.0
# - src net 67.207.148.0/24

$
```

* nicstat
### ip

```bash
# Display all interfaces with addresses
ip addr

# Take down / up the wireless adapter
ip link set dev wlan0 {up|down}

# Set a static IP and netmask
ip addr add 192.168.1.100/32 dev eth0

# Remove a IP from an interface
ip addr del 192.168.1.100/32 dev eth0

# Remove all IPs from an interface
ip address flush dev eth0

# Display all routes
ip route

# Display all routes for IPv6
ip -6 route

# Add default route via gateway IP
ip route add default via 192.168.1.1

# Add route via interface
ip route add 192.168.0.0/24 dev eth0

# Change your mac address 
ip link set dev eth0 address aa:bb:cc:dd:ee:ff

# View neighbors (using ARP and NDP) 
ip neighbor show

$
```

* lldptool
* snmpget
* iptraf
* ethtool
### swapon

```bash
# 
# swapon
# 
# Enables device or file for swapping.
# 
# Get swap information:
  swapon -s
# 
# Enable a given swap partition:
  swapon /dev/sdb7
# 
# Enable a given swap file:
  swapon path/to/file
# 
# Enable all swap areas:
  swapon -a
# 
# Enable swap by label of a device or file:
  swapon -L swap1
# 
# 

$
```

### blktrace

```bash
# blktrace
# blktrace is a block layer IO tracing mechanism which provides detailed information about request queue operations up to user space

# trace PC (non-filesystem requests, PC) on the /dev/sdb disk.
# blkparse generates human-readable formatting
blktrace /dev/sdb -a PC -o - | blkparse -i -

$
```

* iotop
### iostat

```bash
# 
# iostat
# 
# Report statistics for devices and partitions.
# 
# Display a report of CPU and disk statistics since system startup:
  iostat
# 
# Display a report of CPU and disk statistics with units converted to megabytes:
  iostat -m
# 
# Display CPU statistics:
  iostat -c
# 
# Display disk statistics with disk names (including LVM):
  iostat -N
# 
# Display extended disk statistics with disk names for device "sda":
  iostat -xN sda
# 
# Display incremental reports of CPU and disk statistics every 2 seconds:
  iostat 2
# 
# 

$
```

* bpftrace
* bcc
* lttng
* stap
* ftrace
* pcstat
### lsof

```bash
# List all IPv4 network files
sudo lsof -i4

# List all IPv6 network files
sudo lsof -i6

# List all open sockets
lsof -i

# List all listening ports
lsof -Pnl +M -i4

# Find which program is using the port 80
lsof -i TCP:80

# List all connections to a specific host
lsof -i@192.168.1.5

# List all processes accessing a particular file/directory
lsof </path/to/file>

# List all files open for a particular user
lsof -u <username>

# List all files/network connections a command is using
lsof -c <command-name>

# List all files a process has open
lsof -p <pid>

# List all files open mounted at /mount/point.
# Particularly useful for finding which process(es) are using a
# mounted USB stick or CD/DVD.
lsof +f -- </mount/point>

# See this primer: http://www.danielmiessler.com/study/lsof/
# for a number of other useful lsof tips

$
```

