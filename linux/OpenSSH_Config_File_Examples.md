## OpenSSH Config File Examples

How do I create and setup an OpenSSH config file to create shortcuts for servers I frequently access under Linux or Unix desktop operating systems?  如何创建和设置OpenSSH配置文件以创建我经常在Linux或Unix桌面操作系统下访问的服务器的快捷方式？

A global or local configuration file for SSH client can create shortcuts for sshd server including advanced ssh client options. You can configure your OpenSSH ssh client using various files as follows to save time and typing frequently used ssh client command line options such as port, user, hostname, identity-file and much more:  SSH客户端的全局或本地配置文件可以为sshd服务器创建快捷方式，包括高级ssh客户端选项。 您可以使用以下各种文件配置OpenSSH ssh客户端，以节省时间并键入常用的ssh客户端命令行选项，如端口，用户，主机名，身份文件等等：

Let use see some common OpenSSH config file examples.

#### System-wide OpenSSH config file client configuration

1. **/etc/ssh/ssh_config** : This files set the default configuration for all users of OpenSSH clients on that desktop/laptop and it must be readable by all users on the system.

#### User-specific OpenSSH file client configuration

1. **~/.ssh/config** or **$HOME/.ssh/config** : This is user’s own configuration file which, overrides the settings in the global client configuration file, /etc/ssh/ssh_config.

### ~/.ssh/config file rules

The rules are as follows to create an ssh config file:

* You need to edit **~/.ssh/config** with a text editor such as vi.

* One config parameter per line is allowed in the configuration file with the parameter name followed by its value or values. The syntax is:  配置文件中允许每行一个配置参数，参数名称后跟其值或值。 语法是：
```
config value
config1 value1 value2
```

* You can use an equal sign (=) instead of whitespace between the parameter name and the values.
```
config=value
config1=value1 value2
```

* All empty lines are ignored.

* All lines starting with the hash (#) are ignored.

* All values are case-sensitive, but parameter names are not.  所有值都区分大小写，但参数名称不区分大小写。

Tip : If this is a brand new Linux, Apple OS X/Unix box, or if you have never used ssh before create the ~/.ssh/ directory first using the following syntax:  如果这是一个全新的Linux，Apple OS X / Unix盒子，或者如果您在使用以下语法创建〜/ .ssh /目录之前从未使用过ssh：

```bash
mkdir -p $HOME/.ssh
chmod 0700 $HOME/.ssh

cat id_rsa.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### Examples

For demonstration purpose my sample setup is as follows:  出于演示目的，我的示例设置如下：

1. Local desktop client – Apple OS X or Ubuntu Linux.
2. Remote Unix server – OpenBSD server running latest OpenSSH server.
3. Remote OpenSSH server ip/host: 75.126.153.206 (server1.cyberciti.biz)
4. Remote OpenSSH server user: nixcraft
5. Remote OpenSSH port: 4242
6. Local ssh private key file path : /nfs/shared/users/nixcraft/keys/server1/id_rsa

Based upon the above information my ssh command is as follows:

```bash
$ ssh -i /nfs/shared/users/nixcraft/keys/server1/id_rsa -p 4242 nixcraft@server1.cyberciti.biz
```

OR

```bash
$ ssh -i /nfs/shared/users/nixcraft/keys/server1/id_rsa -p 4242 -l nixcraft server1.cyberciti.biz
```

You can avoid typing all of the ssh command parameters while logging into a remote machine and/or for executing commands on a remote machine. All you have to do is create an ssh config file. Open the Terminal application and create your config file by typing the following command:  您可以避免在登录远程计算机时键入所有ssh命令参数和/或在远程计算机上执行命令。 您所要做的就是创建一个ssh配置文件。 打开终端应用程序并键入以下命令创建配置文件：

```bash
vi ~/.ssh/config
```

Add/Append the following config option for a shortcut to server1 as per our sample setup:

```
Host server1
     HostName server1.cyberciti.biz
     User nixcraft
     Port 4242
     IdentityFile /nfs/shared/users/nixcraft/keys/server1/id_rsa
     
Host github.com
     HostName github.com
     User git
     IdentityFile ~/.ssh/github
```

Save and close the file. To open your new SSH session to server1.cyberciti.biz by typing the following command:

```bash
$ ssh server1
```

### Adding another host

Append the following to your **~/.ssh/config** file:

```
Host nas01
     HostName 192.168.1.100
     User root
     IdentityFile ~/.ssh/nas01.key
```

You can simply type:

```bash
$ ssh nas01
```

### Putting it all together

Here is my sample **~/.ssh/config** file that explains and create, design, and evaluate different needs for remote access using ssh client:  这是我的示例〜/ .ssh / config文件，它解释和创建，设计和评估使用ssh客户端进行远程访问的不同需求：

```
### default for all ##
Host *
     ForwardAgent no
     ForwardX11 no
     ForwardX11Trusted yes
     User nixcraft
     Port 22
     Protocol 2
     ServerAliveInterval 60
     ServerAliveCountMax 30
 
## override as per host ##
Host server1
     HostName server1.cyberciti.biz
     User nixcraft
     Port 4242
     IdentityFile /nfs/shared/users/nixcraft/keys/server1/id_rsa
 
## Home nas server ##
Host nas01
     HostName 192.168.1.100
     User root
     IdentityFile ~/.ssh/nas01.key
 
## Login AWS Cloud ##
Host aws.apache
     HostName 1.2.3.4
     User wwwdata
     IdentityFile ~/.ssh/aws.apache.key
 
## Login to internal lan server at 192.168.0.251 via our public uk office ssh based gateway using ##
## $ ssh uk.gw.lan ##
Host uk.gw.lan uk.lan
     HostName 192.168.0.251
     User nixcraft
     ProxyCommand  ssh nixcraft@gateway.uk.cyberciti.biz nc %h %p 2> /dev/null
 
## Our Us Proxy Server ##
## Forward all local port 3128 traffic to port 3128 on the remote vps1.cyberciti.biz server ## 
## $ ssh -f -N  proxyus ##
Host proxyus
    HostName vps1.cyberciti.biz
    User breakfree
    IdentityFile ~/.ssh/vps1.cyberciti.biz.key
    LocalForward 3128 127.0.0.1:3128
```

### Understanding ~/.ssh/config entries

* **Host** : Defines for which host or hosts the configuration section applies. The section ends with a new Host section or the end of the file. A single * as a pattern can be used to provide global defaults for all hosts.  定义配置部分适用的主机。 该部分以新的主机部分或文件末尾结束。 单个*作为模式可用于为所有主机提供全局默认值。

* **HostName** : Specifies the real host name to log into. Numeric IP addresses are also permitted.

* **User** : Defines the username for the SSH connection.

* **IdentityFile** : Specifies a file from which the user’s DSA, ECDSA or DSA authentication identity is read. The default is ~/.ssh/identity for protocol version 1, and ~/.ssh/id_dsa, ~/.ssh/id_ecdsa and ~/.ssh/id_rsa for protocol version 2.

* **ProxyCommand** : Specifies the command to use to connect to the server. The command string extends to the end of the line, and is executed with the user’s shell. In the command string, any occurrence of %h will be substituted by the host name to connect, %p by the port, and %r by the remote user name. The command can be basically anything, and should read from its standard input and write to its standard output. This directive is useful in conjunction with nc(1) and its proxy support. For example, the following directive would connect via an HTTP proxy at 192.1.0.253:
ProxyCommand /usr/bin/nc -X connect -x 192.1.0.253:3128 %h %p  
指定用于连接服务器的命令。 命令字符串扩展到行的末尾，并使用用户的shell执行。 在命令字符串中，任何出现的％h将由要连接的主机名替换，％p由端口替换，％r由远程用户名替换。 该命令基本上可以是任何东西，并且应该从其标准输入读取并写入其标准输出。 该指令与nc(1)及其代理支持结合使用非常有用。 例如，以下指令将通过192.1.0.253处的HTTP代理连接：
ProxyCommand /usr/bin/nc -X connect -x 192.1.0.253:3128 %h %p

* **LocalForward** : Specifies that a TCP port on the local machine be forwarded over the secure channel to the specified host and port from the remote machine. The first argument must be [bind_address:]port and the second argument must be host:hostport.  指定本地计算机上的TCP端口通过安全通道转发到远程计算机的指定主机和端口。 第一个参数必须是[bind_address：] port，第二个参数必须是host：hostport。

* **Port** : Specifies the port number to connect on the remote host.

* **Protocol** : Specifies the protocol versions ssh(1) should support in order of preference. The possible values are 1 and 2.

* **ServerAliveInterval** : Sets a timeout interval in seconds after which if no data has been received from the server, ssh(1) will send a message through the encrypted channel to request a response from the server. See blogpost “[Open SSH Server connection drops out after few or N minutes of inactivity](https://www.cyberciti.biz/tips/open-ssh-server-connection-drops-out-after-few-or-n-minutes-of-inactivity.html)” for more information.  设置超时间隔（以秒为单位），如果没有从服务器收到数据，ssh（1）将通过加密通道发送消息以请求服务器响应。 

* **ServerAliveCountMax** : Sets the number of server alive messages which may be sent without ssh(1) receiving any messages back from the server. If this threshold is reached while server alive messages are being sent, ssh will disconnect from the server, terminating the session.  设置可以在没有ssh（1）从服务器接收任何消息的情况下发送的服务器活动消息的数量。 如果在发送服务器活动消息时达到此阈值，则ssh将断开与服务器的连接，从而终止会话。

### Speed up ssh session  加快ssh会话

Multiplexing is nothing but send more than one ssh connection over a single connection. OpenSSH can reuse an existing TCP connection for multiple concurrent SSH sessions. This results into reduction of the overhead of creating new TCP connections. Update your ~/.ssh/config:  多路复用只不过是通过单个连接发送多个ssh连接。 OpenSSH可以为多个并发SSH会话重用现有的TCP连接。 这导致减少创建新TCP连接的开销。 更新你的〜/ .ssh / config：

```
Host server1
        HostName server1.cyberciti.biz
        ControlPath ~/.ssh/controlmasters/%r@%h:%p
        ControlMaster auto
```

See “[Linux / Unix: OpenSSH Multiplexer To Speed Up OpenSSH Connections](https://www.cyberciti.biz/faq/linux-unix-osx-bsd-ssh-multiplexing-to-speed-up-ssh-connections/)” for more info. In this example, I go [through one host to reach another server i.e. jump host using ProxyCommand](https://www.cyberciti.biz/faq/linux-unix-ssh-proxycommand-passing-through-one-host-gateway-server/):

```
## ~/.ssh/config ##
Host internal
  HostName 192.168.1.100
  User vivek
  ProxyCommand ssh vivek@vpn.nixcraft.net.in -W %h:%p
  ControlPath ~/.ssh/controlmasters/%r@%h:%p
  ControlMaster auto
```

[参考](https://www.cyberciti.biz/faq/create-ssh-config-file-on-linux-unix/)
