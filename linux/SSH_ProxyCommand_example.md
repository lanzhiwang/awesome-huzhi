## SSH ProxyCommand example: Going through one host to reach another server

How do I use and jump through one server to reach another using ssh on a Linux or Unix-like systems? Is it possible to connect to another host via an intermediary so that the client can act as if the connection were direct using ssh?  如何在Linux或类Unix系统上使用ssh使用和跳过一台服务器到达另一台服务器？ 是否可以通过中介连接到另一台主机，以便客户端可以像使用ssh直接连接一样？

You can jump host using ProxyCommand. Some times you can only access a remote server via ssh by first login into an intermediary server (or firewall/jump host). So you first login into to the intermediary server and then ssh to another server. You need to authenticate twice and the chain can be long and is not limited to just two hosts.  您可以使用ProxyCommand跳转主机。 有时您只能通过首先登录中间服务器（或防火墙/跳转主机）通过ssh访问远程服务器。 所以你首先登录到中间服务器，然后ssh到另一台服务器。 您需要进行两次身份验证，并且链可能很长，并且不仅限于两个主机。

### Sample setup
```
     +-------+       +----------+      +-----------+
     | Laptop| <---> | Jumphost | <--> | FooServer |
     +-------+       +----------+      +-----------+
               OR
     +-------+       +----------+      +-----------+
     | Laptop| <---> | Firewall | <--> | FooServer |
     +-------+       +----------+      +-----------+
	192.168.1.5      121.1.2.3         10.10.29.68
```

I can only access a remote server named ‘FooServer’ via ssh by first login into an intermediary server called ‘Jumphost’. First, login to Jumphost:

```bash
$ ssh vivek@Jumphost
```

Next, I must ssh through the intermediary system as follows:

```bash
$ ssh vivek@FooServer
```

### Passing through a gateway or two  通过一两个网关

Instead of typing two ssh command, I can type the following all-in-one command. This is useful for connecting to FooServer via firewall called ‘Jumphost’ as the jump host:

```bash
$ ssh -tt Jumphost ssh -tt FooServer
$ ssh -tt vivek@Jumphost ssh -tt vivek@FooServer
$ ssh -tt vivek@Jumphost ssh -tt vivek@FooServer command1 arg1 arg2
$ ssh -tt vivek@Jumphost ssh -tt vivek@FooServer htop
$ ssh -tt vivek@Jumphost ssh -tt vivek@FooServer screen -dR
```

Where,

* The -t option passed to the ssh command force pseudo-tty allocation. This can be used to execute arbitrary screen-based programs on a remote machine. Multiple -tt options force tty allocation, even if ssh has no local tty.  -t选项传递给ssh命令强制伪tty分配。 这可用于在远程计算机上执行任意基于屏幕的程序。 多个-tt选项强制tty分配，即使ssh没有本地tty。

### Say hello to the ProxyCommand

The syntax is:

```bash
$ ssh -o ProxyCommand='ssh firewall nc remote_server1 22' remote_server1
$ ssh -o ProxyCommand='ssh vivek@Jumphost nc FooServer 22' vivek@FooServer
##########################################
## -t option is needed to run commands ###
##########################################
$ ssh -t -o ProxyCommand='ssh vivek@Jumphost nc FooServer 22' vivek@FooServer htop
```

The netcat (nc) command is needed to set and establish a TCP pipe between Jumphost (or firewall) and FooServer. Now, my laptop (local system) is connected to Jumphost it now connected FooServer. In this example, the utility netcat (nc) is for reading and writing network connections directly. It can be used to pass connections to a 2nd server such as FooServer.  需要 netcat(nc) 命令来设置和建立 Jumphost（或防火墙）和 FooServer之间的TCP管道。 现在，我的笔记本电脑（本地系统）连接到 Jumphost 它现在连接到 FooServer。 在此示例中，实用程序netcat（nc）用于直接读写网络连接。 它可用于将连接传递给第二台服务器，例如FooServer。

[参考](https://www.cyberciti.biz/faq/linux-unix-ssh-proxycommand-passing-through-one-host-gateway-server/)
