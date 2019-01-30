## haproxy keepalived

### Introduction

High availability is a function of system design that allows an application to automatically restart or reroute work to another capable system in the event of a failure. In terms of servers, there are a few different technologies needed to set up a highly available system. There must be a component that can redirect the work and there must be a mechanism to monitor for failure and transition the system if an interruption is detected.  高可用性是系统设计的一个功能，允许应用程序在发生故障时自动重启或重新路由工作到另一个有能力的系统。 在服务器方面，建立高可用性系统需要一些不同的技术。 必须有一个可以重定向工作的组件，并且必须有一种机制来监视故障并在检测到中断时转换系统。

The `keepalived` daemon can be used to monitor services or systems and to automatically failover to a standby if problems occur. In this guide, we will demonstrate how to use keepalived to set up high availability for your load balancers. We will configure a floating IP address that can be moved between two capable load balancers. These will each be configured to split traffic between two backend web servers. If the primary load balancer goes down, the floating IP will be moved to the second load balancer automatically, allowing service to resume.  keepalived守护程序可用于监视服务或系统，并在出现问题时自动故障转移到备用数据库。 在本指南中，我们将演示如何使用keepalived为负载均衡器设置高可用性。 我们将配置一个可以在两个有能力的负载均衡器之间移动的浮动IP地址。 这些将被配置为在两个后端Web服务器之间分割流量。 如果主负载均衡器发生故障，浮动IP将自动移动到第二个负载均衡器，从而允许服务恢复。

![](./ha-diagram-animated.gif)

### Prerequisites

In order to complete this guide, you will need to create four Ubuntu 14.04 servers in your DigitalOcean account. All of the servers must be located within the same datacenter and should have private networking enabled.  要完成本指南，您需要在DigitalOcean帐户中创建四个Ubuntu 14.04服务器。 所有服务器必须位于同一数据中心内，并且应启用专用网络。

On each of these servers, you will need a non-root user configured with sudo access. You can follow our Ubuntu 14.04 initial server setup guide to learn how to set up these users.  在每个服务器上，您将需要一个配置了sudo访问权限的非root用户。 您可以按照我们的Ubuntu 14.04初始服务器设置指南来了解如何设置这些用户。

### Finding Server Network Information

Before we begin the actual configuration of our infrastructure components, it is best to gather some information about each of your servers.  在我们开始实际配置基础架构组件之前，最好收集有关每台服务器的一些信息。

To complete this guide, you will need to have the following information about your servers:

* web servers: Private IP address
* load balancers Private and Anchor IP addresses  负载均衡器专用和锚定IP地址

#### Finding Private IP Addresses
The easiest way to find your Droplet's private IP address is to use curl to grab the private IP address from the DigitalOcean metadata service. This command should be run from within your Droplets. On each Droplet, type:

```
$ curl 169.254.169.254/metadata/v1/interfaces/private/0/ipv4/address && echo
```

The correct IP address should be printed in the terminal window:

```
Output
10.132.20.236
```

#### Finding Anchor IP Addresses

The "anchor IP" is the local private IP address that the floating IP will bind to when attached to a DigitalOcean server. It is simply an alias for the regular eth0 address, implemented at the hypervisor level.

The easiest, least error-prone way of grabbing this value is straight from the DigitalOcean metadata service. Using curl, you can reach out to this endpoint on each of your servers by typing:

```
$ curl 169.254.169.254/metadata/v1/interfaces/public/0/anchor_ipv4/address && echo
```

The anchor IP will be printed on its own line:

```
Output
10.17.1.18
```

### Install and Configure the Web Server

After gathering the data above, we can move on to configuring our services.  收集上述数据后，我们可以继续配置我们的服务。

> Note
> In this setup, the software selected for the web server layer is fairly interchangeable. This guide will use Nginx because it is generic and rather easy to configure. If you are more comfortable with Apache or a (production-capable) language-specific web server, feel free to use that instead. HAProxy will simply pass client requests to the backend web servers which can handle the requests similarly to how it would handle direct client connections.  在此设置中，为Web服务器层选择的软件是可以互换的。 本指南将使用Nginx，因为它是通用的，而且相当容易配置。 如果您对Apache或（支持生产的）特定于语言的Web服务器更熟悉，请随意使用它。 HAProxy将简单地将客户端请求传递给后端Web服务器，后端Web服务器可以处理请求，类似于处理直接客户端连接的方式。

We will start off by setting up our backend web servers. Both of these servers will serve exactly the same content. They will only accept web connections over their private IP addresses. This will help ensure that traffic is directed through one of the two HAProxy servers we will be configuring later.  我们将从设置后端Web服务器开始。 这两个服务器都将提供完全相同的内容。 他们只接受私人IP地址的网络连接。 这将有助于确保流量通过我们稍后将配置的两个HAProxy服务器之一进行定向。

Setting up web servers behind a load balancer allows us to distribute the request burden among some number identical web servers. As our traffic needs change, we can easily scale to meet the new demands by adding or removing web servers from this tier.  在负载均衡器后面设置Web服务器允许我们在一些数量相同的Web服务器之间分配请求负担。 随着我们的流量需求发生变化，我们可以通过在此层添加或删除Web服务器来轻松扩展以满足新需求。

#### Installing Nginx

We will be installing Nginx on our web serving machines to provide this functionality.

Start off by logging in with your sudo user to the two machines that you wish to use as the web servers. Update the local package index on each of your web servers and install Nginx by typing:

```
webserver$ sudo apt-get update
webserver$ sudo apt-get install nginx
```

#### Configure Nginx to Only Allow Requests from the Load Balancers

Next, we will configure our Nginx instances. We want to tell Nginx to only listen for requests on the private IP address of the server. Furthermore, we will only serve requests coming from the private IP addresses of our two load balancers.

To make these changes, open the default Nginx server block file on each of your web servers:

```
webserver$ sudo nano /etc/nginx/sites-available/default
```

To start, we will modify the listen directives. Change the listen directive to listen to the current web server's private IP address on port 80. Delete the extra listen line. It should look something like this:  首先，我们将修改listen指令。 更改listen指令以侦听端口80上当前Web服务器的专用IP地址。删除额外的监听行。 它应该看起来像这样：

```
# /etc/nginx/sites-available/default
server {
    listen web_server_private_IP:80;

    . . .
```

Afterwards, we will set up two allow directives to permit traffic originating from the private IP addresses of our two load balancers. We will follow this up with a deny all rule to forbid all other traffic:   之后，我们将设置两个允许指令，以允许来自两个负载均衡器的私有IP地址的流量。 我们将遵循拒绝所有规则以禁止所有其他流量：

```
# /etc/nginx/sites-available/default
server {
    listen web_server_private_IP:80;

    allow load_balancer_1_private_IP;
    allow load_balancer_2_private_IP;
    deny all;

    . . .
```

Save and close the files when you are finished.

Test that the changes that you made represent valid Nginx syntax by typing:

```
webserver$ sudo nginx -t
```

if no problems were reported, restart the Nginx daemon by typing:

```
webserver$ sudo service nginx restart
```

#### Testing the Changes

To test that your web servers are restricted correctly, you can make requests using curl from various locations.

On your web servers themselves, you can try a simple request of the local content by typing:

```
webserver$ curl 127.0.0.1
```

Because of the restrictions we set in place in our Nginx server block files, this request will actually be denied:

```
Output
curl: (7) Failed to connect to 127.0.0.1 port 80: Connection refused
```

This is expected and reflects the behavior that we were attempting to implement.

Now, from either of the load balancers, we can make a request for either of our web server's public IP address:

```
webserver$ curl web_server_public_IP
```

Once again, this should fail. The web servers are not listening on the public interface and furthermore, when using the public IP address, our web servers would not see the allowed private IP addresses in the request from our load balancers:

```
Output
curl: (7) Failed to connect to web_server_public_IP port 80: Connection refused
```

However, if we modify the call to make the request using the web server's private IP address, it should work correctly:

```
webserver$ curl web_server_private_IP
```

The default Nginx index.html page should be returned:

```
Output
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>

. . .
```

Test this from both load balancers to both web servers. Each request for the private IP address should succeed while each request made to the public addresses should fail.

Once the above behavior is demonstrated, we can move on. Our backend web server configuration is now complete.

### Install and Configure HAProxy

Next, we will set up the HAProxy load balancers. These will each sit in front of our web servers and split requests between the two backend servers. These load balancers are completely redundant. Only one will receive traffic at any given time.  接下来，我们将设置HAProxy负载平衡器。 这些将分别位于我们的Web服务器前面，并在两个后端服务器之间拆分请求。 这些负载平衡器完全是冗余的。 任何时候只有一个人会收到流量。

The HAProxy configuration will pass requests to both of the web servers. The load balancers will listen for requests on their anchor IP address. As mentioned earlier, this is the IP address that the floating IP address will bind to when attached to the Droplet. This ensures that only traffic originating from the floating IP address will be forwarded.  HAProxy配置会将请求传递给两个Web服务器。 负载均衡器将监听其锚定IP地址上的请求。 如前所述，这是浮动IP地址在连接到Droplet时将绑定的IP地址。 这可确保仅转发源自浮动IP地址的流量。

#### Install HAProxy

The first step we need to take on our load balancers will be to install the haproxy package. We can find this in the default Ubuntu repositories. Update the local package index on your load balancers and install HAProxy by typing:

```
loadbalancer$ sudo apt-get update
loadbalancer$ sudo apt-get install haproxy
```

Configure HAProxy

The first item we need to modify when dealing with HAProxy is the `/etc/default/haproxy` file. Open that file now in your editor:

```
loadbalancer$ sudo nano /etc/default/haproxy
```

This file determines whether HAProxy will start at boot. Since we want the service to start automatically each time the server powers on, we need to change the value of ENABLED to "1":  此文件确定HAProxy是否将在引导时启动。 由于我们希望每次服务器启动时服务都会自动启动，因此我们需要将ENABLED的值更改为“1”：

```
# /etc/default/haproxy
# Set ENABLED to 1 if you want the init script to start haproxy.
ENABLED=1
# Add extra flags here.
#EXTRAOPTS="-de -m 16"
```

Save and close the file after making the above edit.

Next, we can open the main HAProxy configuration file:

```
loadbalancer$ sudo nano /etc/haproxy/haproxy.cfg
```

The first item that we need to adjust is the mode that HAProxy will be operating in. We want to configure TCP, or layer 4, load balancing. To do this, we need to alter the mode line in the default section. We should also change the option immediately following that deals with the log:  我们需要调整的第一个项目是HAProxy将要运行的模式。我们要配置TCP或第4层负载平衡。 为此，我们需要更改默认部分中的模式行。 我们还应该在处理日志之后立即更改选项：

```
# /etc/haproxy/haproxy.cfg
. . .

defaults
    log     global
    mode    tcp
    option  tcplog

. . .
```

At the end of the file, we need to define our front end configuration. This will dictate how HAProxy listens for incoming connections. We will bind HAProxy to the load balancer anchor IP address. This will allow it to listen for traffic originating from the floating IP address. We will call our front end "www" for simplicity. We will also specify a default backend to pass traffic to (which we will be configuring in a moment):

```
# /etc/haproxy/haproxy.cfg
. . .

defaults
    log     global
    mode    tcp
    option  tcplog

. . .

frontend www
    bind    load_balancer_anchor_IP:80
    default_backend nginx_pool
```

Next, we can configure our backend section. This will specify the downstream locations where HAProxy will pass the traffic it receives. In our case, this will be the private IP addresses of both of the Nginx web servers we configured. We will specify traditional round-robin balancing and will set the mode to "tcp" again:  接下来，我们可以配置我们的后端部分。 这将指定HAProxy将通过其接收的流量的下游位置。 在我们的例子中，这将是我们配置的两个Nginx Web服务器的私有IP地址。 我们将指定传统的循环平衡，并将模式再次设置为“tcp”：

```
# /etc/haproxy/haproxy.cfg
. . .

defaults
    log     global
    mode    tcp
    option  tcplog

. . .

frontend www
    bind load_balancer_anchor_IP:80
    default_backend nginx_pool

backend nginx_pool
    balance roundrobin
    mode tcp
    server web1 web_server_1_private_IP:80 check
    server web2 web_server_2_private_IP:80 check
```

When you are finished making the above changes, save and close the file.

Check that the configuration changes we made represent valid HAProxy syntax by typing:

```
loadbalancer$ sudo haproxy -f /etc/haproxy/haproxy.cfg -c
```

If no errors were reported, restart your service by typing:

```
loadbalancer$ sudo service haproxy restart
```

#### Testing the Changes

We can make sure our configuration is valid by testing with curl again.

From the load balancer servers, try to request the local host, the load balancer's own public IP address, or the server's own private IP address:

```
loadbalancer$ curl 127.0.0.1
loadbalancer$ curl load_balancer_public_IP
loadbalancer$ curl load_balancer_private_IP
```

These should all fail with messages that look similar to this:

```
Output
curl: (7) Failed to connect to address port 80: Connection refused
```

However, if you make a request to the load balancer's anchor IP address, it should complete successfully:

```
loadbalancer$ curl load_balancer_anchor_IP
```

You should see the default Nginx index.html page, routed from one of the two backend web servers:

```
Output
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>

. . .
```

If this behavior matches that of your system, then your load balancers are configured correctly.

### Build and Install Keepalived

Our actual service is now up and running. However, our infrastructure is not highly available yet because we have no way of redirecting traffic if our active load balancer experiences problems. In order to rectify this, we will install the keepalived daemon on our load balancer servers. This is the component that will provide failover capabilities if our active load balancer becomes unavailable.  我们的实际服务现已开始运行。 但是，我们的基础架构尚未高度可用，因为如果我们的主动负载均衡器遇到问题，我们无法重定向流量。 为了纠正这个问题，我们将在负载均衡器服务器上安装keepalived守护进程。 如果我们的活动负载均衡器不可用，则该组件将提供故障转移功能。

There is a version of keepalived in Ubuntu's default repositories, but it is outdated and suffers from a few bugs that would prevent our configuration from working. Instead, we will install the latest version of keepalived from source.  在Ubuntu的默认存储库中有一个keepalived版本，但它已经过时并且有一些错误会阻止我们的配置工作。 相反，我们将从源代码安装最新版本的keepalived。

Before we begin, we should grab the dependencies we will need to build the software. The build-essential meta-package will provide the compilation tools we need, while the libssl-dev package contains the SSL development libraries that keepalived needs to build against:

```
loadbalancer$ sudo apt-get install build-essential libssl-dev
```

Once the dependencies are in place, we can download the tarball for keepalived. Visit this page to find the latest version of the software. Right-click on the latest version and copy the link address. Back on your servers, move to your home directory and use wget to grab the link you copied:

```
loadbalancer$ cd ~
loadbalancer$ wget http://www.keepalived.org/software/keepalived-1.2.19.tar.gz
```

Use the tar command to expand the archive. Move into the resulting directory:

```
loadbalancer$ tar xzvf keepalived*
loadbalancer$ cd keepalived*
```

Build and install the daemon by typing:

```
loadbalancer$ ./configure
loadbalancer$ make
loadbalancer$ sudo make install
```

The daemon should now be installed on both of the load balancer systems.

### Create a Keepalived Upstart Script

The keepalived installation moved all of the binaries and supporting files into place on our system. However, one piece that was not included was an Upstart script for our Ubuntu 14.04 systems.  keepalived安装将所有二进制文件和支持文件移动到我们的系统上。 但是，未包含的一件是我们的Ubuntu 14.04系统的Upstart脚本。

We can create a very simple Upstart script that can handle our keepalived service. Open a file called keepalived.conf within the /etc/init directory to get started:

```
loadbalancer$ sudo nano /etc/init/keepalived.conf
```

Inside, we can start with a simple description of the functionality keepalived provides. We'll use the description from the included man page. Next we will specify the runlevels in which the service should be started and stopped. We want this service to be active in all normal conditions (runlevels 2-5) and stopped for all other runlevels (when reboot, poweroff, or single-user mode is initiated, for instance):

```
# /etc/init/keepalived.conf
description "load-balancing and high-availability service"

start on runlevel [2345]
stop on runlevel [!2345]
```

Because this service is integral to ensuring our web service remains available, we want to restart this service in the event of a failure. We can then specify the actual exec line that will start the service. We need to add the --dont-fork option so that Upstart can track the pid correctly:  由于此服务对于确保我们的Web服务仍然可用是不可或缺的，因此我们希望在发生故障时重新启动此服务。 然后我们可以指定将启动服务的实际exec行。 我们需要添加--dont-fork选项，以便Upstart可以正确跟踪pid：

```
# /etc/init/keepalived.conf
description "load-balancing and high-availability service"

start on runlevel [2345]
stop on runlevel [!2345]

respawn

exec /usr/local/sbin/keepalived --dont-fork
```

Save and close the files when you are finished.

### Create the Keepalived Configuration File

With our Upstart files in place, we can now move on to configuring keepalived.

The service looks for its configuration files in the /etc/keepalived directory. Create that directory now on both of your load balancers:

```
loadbalancer$ sudo mkdir -p /etc/keepalived
```

#### Creating the Primary Load Balancer's Configuration

Next, on the load balancer server that you wish to use as your primary server, create the main keepalived configuration file. The daemon looks for a file called keepalived.conf inside of the /etc/keepalived directory:  接下来，在要用作主服务器的负载平衡器服务器上，创建主keepalived配置文件。 守护进程在/etc/keepalived目录中查找名为keepalived.conf的文件：

```
primary$ sudo nano /etc/keepalived/keepalived.conf
```

Our check will be very simple. Every two seconds, we will check that a process called haproxy is still claiming a pid:  我们的检查非常简单。 每两秒钟，我们将检查一个名为haproxy的进程是否还在声明一个pid：

```
# Primary server's /etc/keepalived/keepalived.conf
vrrp_script chk_haproxy {
    script "pidof haproxy"
    interval 2
}
```

Next, we will open a block called vrrp_instance. This is the main configuration section that defines the way that keepalived will implement high availability.  接下来，我们将打开一个名为vrrp_instance的块。 这是主要配置部分，它定义了keepalived实现高可用性的方式。

We will start off by telling keepalived to communicate with its peers over eth1, our private interface. Since we are configuring our primary server, we will set the state configuration to "MASTER". This is the initial value that keepalived will use until the daemon can contact its peer and hold an election.  我们将首先告诉keepalived通过我们的私有接口eth1与其同行进行通信。 由于我们正在配置主服务器，因此我们将状态配置设置为“MASTER”。 这是keepalived将使用的初始值，直到守护程序可以联系其对等方并进行选举。

During the election, the priority option is used to decide which member is elected. The decision is simply based on which server has the highest number for this setting. We will use "200" for our primary server:   在选举期间，优先选项用于决定选出哪个成员。 该决定仅基于哪个服务器具有此设置的最大编号。 我们将使用“200”作为主服务器：

```
# Primary server's /etc/keepalived/keepalived.conf
vrrp_script chk_nginx {
    script "pidof nginx"
    interval 2
}

vrrp_instance VI_1 {
    interface eth1
    state MASTER
    priority 200


}
```

Next, we will assign an ID for this cluster group that will be shared by both nodes. We will use "33" for this example. We need to set unicast_src_ip to our primary load balancer's private IP address. We will set unicast_peer to our secondary load balancer's private IP address:

```
# Primary server's /etc/keepalived/keepalived.conf
vrrp_script chk_haproxy {
    script "pidof haproxy"
    interval 2
}

vrrp_instance VI_1 {
    interface eth1
    state MASTER
    priority 200

    virtual_router_id 33
    unicast_src_ip primary_private_IP
    unicast_peer {
        secondary_private_IP
    }


}
```

Next, we can set up some simple authentication for our keepalived daemons to communicate with one another. This is just a basic measure to ensure that the peer being contacted is legitimate. Create an authentication sub-block. Inside, specify password authentication by setting the auth_type. For the auth_pass parameter, set a shared secret that will be used by both nodes. Unfortunately, only the first eight characters are significant:

```
Primary server's /etc/keepalived/keepalived.conf
vrrp_script chk_haproxy {
    script "pidof haproxy"
    interval 2
}

vrrp_instance VI_1 {
    interface eth1
    state MASTER
    priority 200

    virtual_router_id 33
    unicast_src_ip primary_private_IP
    unicast_peer {
        secondary_private_IP
    }

    authentication {
        auth_type PASS
        auth_pass password
    }


}
```

Next, we will tell keepalived to use the check we created at the top of the file, labeled chk_haproxy, to determine the health of the local system. Finally, we will set a notify_master script, which is executed whenever this node becomes the "master" of the pair. This script will be responsible for triggering the floating IP address reassignment. We will create this script momentarily:  接下来，我们将告诉keepalived使用我们在文件顶部创建的标记为chk_haproxy的检查来确定本地系统的运行状况。 最后，我们将设置一个notify_master脚本，只要该节点成为该对的“主”，就会执行该脚本。 该脚本将负责触发浮动IP地址重新分配。 我们将暂时创建此脚本：

```
# Primary server's /etc/keepalived/keepalived.conf
vrrp_script chk_haproxy {
    script "pidof haproxy"
    interval 2
}

vrrp_instance VI_1 {
    interface eth1
    state MASTER
    priority 200

    virtual_router_id 33
    unicast_src_ip primary_private_IP
    unicast_peer {
        secondary_private_IP
    }

    authentication {
        auth_type PASS
        auth_pass password
    }

    track_script {
        chk_haproxy
    }

    notify_master /etc/keepalived/master.sh
}
```

Once you've set up the information above, save and close the file.

#### Creating the Secondary Load Balancer's Configuration

Next, we will create the companion script on our secondary load balancer. Open a file at /etc/keepalived/keepalived.conf on your secondary server:

```
secondary$ sudo nano /etc/keepalived/keepalived.conf
```

Inside, the script that we will use will be largely equivalent to the primary server's script. The items that we need to change are:

* state: This should be changed to "BACKUP" on the secondary server so that the node initializes to the backup state before elections occur.
* priority: This should be set to a lower value than the primary server. We will use the value "100" in this guide.
* unicast_src_ip: This should be the private IP address of the secondary server.
* unicast_peer: This should contain the private IP address of the primary server.

When you change those values, the script for the secondary server should look like this:

```
# Secondary server's /etc/keepalived/keepalived.conf
vrrp_script chk_haproxy {
    script "pidof haproxy"
    interval 2
}

vrrp_instance VI_1 {
    interface eth1
    state BACKUP
    priority 100

    virtual_router_id 33
    unicast_src_ip secondary_private_IP
    unicast_peer {
        primary_private_IP
    }

    authentication {
        auth_type PASS
        auth_pass password
    }

    track_script {
        chk_haproxy
    }

    notify_master /etc/keepalived/master.sh
}

```

Once you've entered the script and changed the appropriate values, save and close the file.

#### Create the Wrapper Script

```
# /etc/keepalived/master.sh
export DO_TOKEN='digitalocean_api_token'
IP='floating_ip_addr'
ID=$(curl -s http://169.254.169.254/metadata/v1/id)
HAS_FLOATING_IP=$(curl -s http://169.254.169.254/metadata/v1/floating_ip/ipv4/active)

if [ $HAS_FLOATING_IP = "false" ]; then
    n=0
    while [ $n -lt 10 ]
    do
        python /usr/local/bin/assign-ip $IP $ID && break
        n=$((n+1))
        sleep 3
    done
fi
```

Save and close the file when you are finished.

### Start Up the Keepalived Service and Test Failover

The `keepalived` daemon and all of its companion scripts should now be completely configured. We can start the service on both of our load balancers by typing:

```
loadbalancer$ sudo start keepalived
```

The service should start up on each server and contact its peer, authenticating with the shared secret we configured. Each daemon will monitor the local HAProxy process, and will listen to signals from the remote keepalived process.  该服务应该在每个服务器上启动并联系其对等方，使用我们配置的共享密钥进行身份验证。 每个守护进程都将监视本地HAProxy进程，并将侦听来自远程keepalived进程的信号。

Your primary load balancer, which should have the floating IP address assigned to it currently, will direct requests to each of the backend Nginx servers in turn. There is some simple session stickiness that is usually applied, making it more likely that you will get the same backend when making requests through a web browser.  您的主要负载均衡器（当前应为其分配了浮动IP地址）将依次将请求定向到每个后端Nginx服务器。 通常会应用一些简单的会话粘性，使您在通过Web浏览器发出请求时更有可能获得相同的后端。

We can test failover in a simple way by simply turning off HAProxy on our primary load balancer:

```
primary$ sudo service haproxy stop
```

If we visit our floating IP address in our browser, we might momentarily get an error indicating the page could not be found:

```
http://floating_IP_addr
```

If we refresh the page a few times, in a moment, our default Nginx page will come back:

### Visualizing the Transition

#### Tail the Logs on the Web Servers

```
webserver$ sudo tail -f /var/log/nginx/access.log | awk '{print $1;}'
```

#### Configure Nginx to Log Actual Client IP Address

```
webserver$ sudo nano /etc/nginx/nginx.conf
```

```
# add to /etc/nginx/nginx.conf
log_format haproxy_log 'ProxyIP: $remote_addr - ClientIP: $http_x_forwarded_for - $remote_user [$time_local] ' '"$request" $status $body_bytes_sent "$http_referer" ' '"$http_user_agent"';
```
