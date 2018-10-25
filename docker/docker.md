## Docker

### Install Docker in Ubuntu

```bash
$ sudo apt-get update
$ sudo apt-get install linux-image-extra-$(uname -r) linux-image-extra-virtual
$ sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
$ sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
$ sudo apt-get install docker-ce
$ dpkg -L docker-ce
$ docker info

```

### Install docker in CentOS

```bash
# install docker
$ yum install -y yum-utils device-mapper-persistent-data lvm2
$ yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
$ yum makecache fast
$ yum install -y docker-ce
$ systemctl daemon-reload
$ systemctl enable docker.service
$ systemctl start docker.service
$ systemctl status docker.service
$ docker info

# install docker compose
$ curl -L https://github.com/docker/compose/releases/download/1.15.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
$ chmod +x /usr/local/bin/docker-compose
$ /usr/local/bin/docker-compose --version
docker-compose version 1.15.0, build e12f3b9
$ docker-compose --version
docker-compose version 1.15.0, build e12f3b9
$ ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
$ ln -s /usr/local/bin/docker-compose /usr/sbin/docker-compose

```


### 配置文件

```bash
# 对应于 docker 1.12.6
$ cat /etc/sysconfig/docker
OPTIONS='--selinux-enabled --log-driver=journald --insecure-registry docker-registry.innovation.os'

# 对应于 docker 17.06.2-ce
$ cat /etc/docker/daemon.json
{
    "log-driver": "journald",
    "insecure-registries": ["docker-registry.innovation.os"]
}

```


### Docker 操作

```bash
# docker 进程相关信息
$ sudo docker info

$ sudo service docker status
docker start/running, process 25144

$ systemctl status docker.service

$ ps -ef | grep docker
root     25144     1  0 05:54 ?        00:00:00 /usr/bin/dockerd --raw-logs
root     25155 25144  0 05:54 ?        00:00:00 docker-containerd -l unix:///var/run/docker/libcontainerd/docker-containerd.sock --metrics-interval=0 --start-timeout 2m --state-dir /var/run/docker/libcontainerd/containerd --shim docker-containerd-shim --runtime docker-runc
$

# 运行容器
$ sudo docker run -i -t ubuntu /bin/bash
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
aafe6b5e13de: Pull complete
0a2b43a72660: Pull complete
18bdd1e546d2: Pull complete
8198342c3e05: Pull complete
f56970a44fd4: Pull complete
Digest: sha256:f3a61450ae43896c4332bda5e78b453f4a93179045f20c8181043b26b5e79028
Status: Downloaded newer image for ubuntu:latest

root@a68cc7370822:/# hostname
a68cc7370822

root@a68cc7370822:/# cat /etc/hosts
127.0.0.1    localhost
::1    localhost ip6-localhost ip6-loopback
fe00::0    ip6-localnet
ff00::0    ip6-mcastprefix
ff02::1    ip6-allnodes
ff02::2    ip6-allrouters
172.18.0.2    a68cc7370822

root@a68cc7370822:/# ps -aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0  18232  1996 ?        Ss   06:12   0:00 /bin/bash
root        13  0.0  0.0  34416  1468 ?        R+   06:16   0:00 ps -aux

root@a68cc7370822:/# apt-get update

root@a68cc7370822:/#

root@a68cc7370822:/# apt-get install vim

root@a68cc7370822:/#

root@a68cc7370822:/# exit
exit

$ sudo docker ps -al
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                          PORTS               NAMES
a68cc7370822        ubuntu              "/bin/bash"         26 minutes ago      Exited (0) About a minute ago                       stoic_knuth

# 增加 name 参数
$ sudo docker run --name huzhi_first_container -i -t ubuntu /bin/bash

root@52150991084b:/# whereis vim
vim:

root@52150991084b:/# exit
exit

$ sudo docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                      PORTS               NAMES
52150991084b        ubuntu              "/bin/bash"         51 seconds ago      Exited (0) 30 seconds ago                       huzhi_first_container
a68cc7370822        ubuntu              "/bin/bash"         27 minutes ago      Exited (0) 2 minutes ago                        stoic_knuth

# 启动容器
$ sudo docker start huzhi_first_container
huzhi_first_container

# 进入容器
$ sudo docker attach huzhi_first_container

root@52150991084b:/# whereis vim
vim:

root@52150991084b:/#

# -d 常驻进程
$ sudo docker run --name daemon_dave -d ubuntu /bin/sh -c "while true; do echo hello world; sleep 1; done"
e5c656e1e1e1c56c0dd29e450bb5a9527266d867a3c45f7fa9de6a1e4f1ceb01

$ sudo docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                      PORTS               NAMES
e5c656e1e1e1        ubuntu              "/bin/sh -c 'while..."   21 seconds ago      Up 19 seconds                                   daemon_dave
52150991084b        ubuntu              "/bin/bash"              8 minutes ago       Exited (0) 2 minutes ago                        huzhi_first_container
a68cc7370822        ubuntu              "/bin/bash"              35 minutes ago      Exited (0) 10 minutes ago                       stoic_knuth

# 打印日志
$ sudo docker logs daemon_dave
hello world
hello world
hello world
hello world

$ sudo docker logs -ft daemon_dave
2017-05-08T06:47:14.073738615Z hello world
2017-05-08T06:47:20.082663499Z hello world
2017-05-08T06:49:56.325945219Z hello world

# 查看容器中的进程信息
$ sudo docker top daemon_dave
UID                 PID                 PPID                C                   STIME               TTY                 TIME                CMD
root                26668               26652               0                   06:47               ?                   00:00:00            /bin/sh -c while true; do echo hello world; sleep 1; done
root                26942               26668               0                   06:51               ?                   00:00:00            sleep 1

# 在容器中执行shell命令
$ sudo docker exec -d daemon_dave touch /etc/new_config_file

$ sudo docker exec -t -i daemon_dave /bin/bash

root@e5c656e1e1e1:/# ll /etc/new_config_file
-rw-r--r-- 1 root root 0 May  8 06:53 /etc/new_config_file

root@e5c656e1e1e1:/# exit
exit

$ sudo docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                      PORTS               NAMES
e5c656e1e1e1        ubuntu              "/bin/sh -c 'while..."   9 minutes ago       Up 9 minutes                                    daemon_dave
52150991084b        ubuntu              "/bin/bash"              16 minutes ago      Exited (0) 11 minutes ago                       huzhi_first_container
a68cc7370822        ubuntu              "/bin/bash"              43 minutes ago      Exited (0) 18 minutes ago                       stoic_knuth

# 停止容器
$ sudo docker stop daemon_dave
daemon_dave

$ sudo docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                       PORTS               NAMES
e5c656e1e1e1        ubuntu              "/bin/sh -c 'while..."   10 minutes ago      Exited (137) 5 seconds ago                       daemon_dave
52150991084b        ubuntu              "/bin/bash"              18 minutes ago      Exited (0) 12 minutes ago                        huzhi_first_container
a68cc7370822        ubuntu              "/bin/bash"              45 minutes ago      Exited (0) 20 minutes ago                        stoic_knuth

# --restart 参数
$ sudo docker run --restart=always --name daemon_dave -d ubuntu /bin/sh -c "while true; do echo hello world; sleep 1; done"
$ sudo docker run --restart=on-failure --name daemon_dave -d ubuntu /bin/sh -c "while true; do echo hello world; sleep 1; done"
$ sudo docker run --restart=on-failure:5 --name daemon_dave -d ubuntu /bin/sh -c "while true; do echo hello world; sleep 1; done"

$ sudo docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                       PORTS               NAMES
e5c656e1e1e1        ubuntu              "/bin/sh -c 'while..."   13 minutes ago      Exited (137) 3 minutes ago                       daemon_dave
52150991084b        ubuntu              "/bin/bash"              21 minutes ago      Exited (0) 15 minutes ago                        huzhi_first_container
a68cc7370822        ubuntu              "/bin/bash"              48 minutes ago      Exited (0) 23 minutes ago                        stoic_knuth

# 查看容器信息
$ sudo docker inspect daemon_dave

$ sudo docker inspect --format='{{ .State.Running }}' daemon_dave
false

$ sudo docker inspect --format='{{ .Image }}' daemon_dave
sha256:f7b3f317ec734a73deca91b34c2b1e3dd7454650da9c8ef3047d29a873865178

$ sudo docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                        PORTS               NAMES
e5c656e1e1e1        ubuntu              "/bin/sh -c 'while..."   21 minutes ago      Exited (137) 11 minutes ago                       daemon_dave
52150991084b        ubuntu              "/bin/bash"              29 minutes ago      Exited (0) 23 minutes ago                         huzhi_first_container
a68cc7370822        ubuntu              "/bin/bash"              56 minutes ago      Exited (0) 31 minutes ago                         stoic_knuth

# 删除容器
$ sudo docker rm stoic_knuth
stoic_knuth

$ sudo docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                        PORTS               NAMES
e5c656e1e1e1        ubuntu              "/bin/sh -c 'while..."   22 minutes ago      Exited (137) 11 minutes ago                       daemon_dave
52150991084b        ubuntu              "/bin/bash"              29 minutes ago      Exited (0) 24 minutes ago                         huzhi_first_container

$ sudo docker ps -a -q

$ sudo docker stop
$ sudo docker kill
$ sudo docker rm `sudo docker ps -a -q`

# 获取镜像
$ sudo docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              latest              f7b3f317ec73        13 days ago         117 MB

$ sudo docker pull ubuntu
Using default tag: latest
latest: Pulling from library/ubuntu
Digest: sha256:f3a61450ae43896c4332bda5e78b453f4a93179045f20c8181043b26b5e79028
Status: Image is up to date for ubuntu:latest

$ sudo docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              latest              f7b3f317ec73        13 days ago         117 MB

$ sudo docker pull -a ubuntu
10.04: Pulling from library/ubuntu
a3ed95caeb02: Pull complete
86b54f4b6a4e: Pull complete
Digest: sha256:f6695b2d24dd2e1da0a79fa72459e33505da79939c13ce50e90675c32988ab64
12.04.5: Pulling from library/ubuntu
d8868e50ac4c: Pull complete
83251ac64627: Pull complete
589bba2f1b36: Pull complete
d62ecaceda39: Pull complete
6d93b41cfc6b: Pull complete
Digest: sha256:18305429afa14ea462f810146ba44d4363ae76e4c8dfc38288cf73aa07485005
12.04: Pulling from library/ubuntu
Digest: sha256:18305429afa14ea462f810146ba44d4363ae76e4c8dfc38288cf73aa07485005
Get https://registry-1.docker.io/v2/library/ubuntu/manifests/12.10: net/http: TLS handshake timeout

$ sudo docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              latest              f7b3f317ec73        13 days ago         117 MB
ubuntu              12.04               5b117edd0b76        3 weeks ago         104 MB
ubuntu              12.04.5             5b117edd0b76        3 weeks ago         104 MB
ubuntu              10.04               e21dbcc7c9de        3 years ago         183 MB

# 使用带标签的镜像
$ sudo docker run --name huzhi_first_container -i -t ubuntu:12.04 /bin/bash

$ sudo docker pull fedora
Using default tag: latest
latest: Pulling from library/fedora
691bc14ee274: Pull complete
Digest: sha256:69281ddd7b2600e5f2b17f1e12d7fba25207f459204fb2d15884f8432c479136
Status: Downloaded newer image for fedora:latest

$ sudo docker images fedora
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
fedora              latest              15895ef0b3b2        2 weeks ago         231 MB

$ sudo docker pull fedora:20

$ sudo docker search puppet

$ sudo docker pull devopsil/puppet

$ sudo docker run -i -t devopsil/puppet /bin/bash

# 修改容器后提交保存
$ sudo docker run -i -t ubuntu /bin/bash

root@3ad7ccaa4145:/# pwd
/

root@3ad7ccaa4145:/# ll
total 72
drwxr-xr-x  36 root root 4096 May  8 07:36 ./
drwxr-xr-x  36 root root 4096 May  8 07:36 ../
-rwxr-xr-x   1 root root    0 May  8 07:35 .dockerenv*
drwxr-xr-x   2 root root 4096 Apr 17 20:31 bin/
drwxr-xr-x   2 root root 4096 Apr 12  2016 boot/
drwxr-xr-x   5 root root  360 May  8 07:35 dev/
drwxr-xr-x  45 root root 4096 May  8 07:35 etc/
drwxr-xr-x   2 root root 4096 Apr 12  2016 home/
drwxr-xr-x   8 root root 4096 Sep 13  2015 lib/
drwxr-xr-x   2 root root 4096 Apr 17 20:30 lib64/
drwxr-xr-x   2 root root 4096 Apr 17 20:30 media/
drwxr-xr-x   2 root root 4096 Apr 17 20:30 mnt/
drwxr-xr-x   2 root root 4096 Apr 17 20:30 opt/
dr-xr-xr-x 124 root root    0 May  8 07:35 proc/
drwx------   2 root root 4096 Apr 17 20:31 root/
drwxr-xr-x   6 root root 4096 Apr 24 22:57 run/
drwxr-xr-x   2 root root 4096 Apr 24 22:57 sbin/
drwxr-xr-x   2 root root 4096 Apr 17 20:30 srv/
dr-xr-xr-x  13 root root    0 May  8 07:35 sys/
drwxrwxrwt   2 root root 4096 May  8 07:36 tmp/
drwxr-xr-x  11 root root 4096 Apr 24 22:57 usr/
drwxr-xr-x  14 root root 4096 May  8 07:36 var/

root@3ad7ccaa4145:/# cd /root

root@3ad7ccaa4145:~# ll -a
total 16
drwx------  2 root root 4096 Apr 17 20:31 ./
drwxr-xr-x 36 root root 4096 May  8 07:36 ../
-rw-r--r--  1 root root 3106 Oct 22  2015 .bashrc
-rw-r--r--  1 root root  148 Aug 17  2015 .profile

root@3ad7ccaa4145:~# touch test.txt

root@3ad7ccaa4145:~# ll
total 16
drwx------  2 root root 4096 May  8 07:39 ./
drwxr-xr-x 37 root root 4096 May  8 07:39 ../
-rw-r--r--  1 root root 3106 Oct 22  2015 .bashrc
-rw-r--r--  1 root root  148 Aug 17  2015 .profile
-rw-r--r--  1 root root    0 May  8 07:39 test.txt

root@3ad7ccaa4145:~# exit
exit

$ sudo docker ps -l -q
3ad7ccaa4145

$ sudo docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                        PORTS               NAMES
3ad7ccaa4145        ubuntu              "/bin/bash"              6 minutes ago       Exited (0) 55 seconds ago                         keen_wright
e5c656e1e1e1        ubuntu              "/bin/sh -c 'while..."   54 minutes ago      Exited (137) 44 minutes ago                       daemon_dave
52150991084b        ubuntu              "/bin/bash"              About an hour ago   Exited (0) 56 minutes ago                         huzhi_first_container

$ sudo docker commit 3ad7ccaa4145 huzhi/test
sha256:11cd92767a6104362dac0cf7a542faa0ca209bea3078ba1c973cfccf4a01ee22

$ sudo docker images huzhi/test
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
huzhi/test          latest              11cd92767a61        24 seconds ago      124 MB

$ sudo docker commit -m="test" --author="huzhi" 3ad7ccaa4145 huzhi/test:test

$ sudo docker inspect huzhi/test

$ sudo docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
huzhi/test          latest              11cd92767a61        5 minutes ago       124 MB
ubuntu              latest              f7b3f317ec73        13 days ago         117 MB
fedora              latest              15895ef0b3b2        2 weeks ago         231 MB
ubuntu              12.04               5b117edd0b76        3 weeks ago         104 MB
ubuntu              12.04.5             5b117edd0b76        3 weeks ago         104 MB
ubuntu              10.04               e21dbcc7c9de        3 years ago         183 MB
```


### 通过 dockerfile 构建镜像

```bash
$ mkdir static_web

$ cd static_web

$ pwd
/home/ubuntu/static_web

$ ls -a
.  ..

$ touch Dockerfile

$ vim Dockerfile

$ cat Dockerfile
# Version: 0.0.1
FROM ubuntu:latest
MAINTAINER James Turnbull "james@example.com"
RUN apt-get update
# /bin/sh -c "apt-get update"
RUN apt-get install -y nginx
# RUN [ "apt-get", " install", " -y", " nginx" ]
RUN echo 'Hi, I am in your container' > /var/www/html/index.html
EXPOSE 80

$ sudo docker build -t="huzhi/static_web" .
Sending build context to Docker daemon 2.048 kB
Step 1/6 : FROM ubuntu:latest
---> f7b3f317ec73
Step 2/6 : MAINTAINER James Turnbull "james@example.com"
---> Running in 1402dbd45502
---> ecd0ed3a265d
Removing intermediate container 1402dbd45502
Step 3/6 : RUN apt-get update
---> Running in 31964fe2d3d7
Get:1 http://security.ubuntu.com/ubuntu xenial-security InRelease [102 kB]
Fetched 23.9 MB in 1min 42s (234 kB/s)
Reading package lists...
---> dec44e1329e3
Removing intermediate container 31964fe2d3d7
Step 4/6 : RUN apt-get install -y nginx
---> Running in e01a0e0621a2
Reading package lists...
Processing triggers for systemd (229-4ubuntu16) ...
---> dac4f060368e
Removing intermediate container e01a0e0621a2
Step 5/6 : RUN echo 'Hi, I am in your container' > /var/www/html/index.html
---> Running in d87185324f0e
---> 6255901b6e9f
Removing intermediate container d87185324f0e
Step 6/6 : EXPOSE 80
---> Running in 1f600e39491f
---> 85792be42dc2
Removing intermediate container 1f600e39491f
Successfully built 85792be42dc2

$ ls -a
.  ..  Dockerfile

$ sudo docker build -t="huzhi/static_web:v1" .

$ sudo docker build -t="huzhi/static_web:v1" git@github.com:jam/docker-static_web

$ touch .dockerignore

$ ll -a
total 12
drwxrwxr-x  2 ubuntu ubuntu 4096 May  8 08:19 ./
drwxr-xr-x 20 ubuntu ubuntu 4096 May  8 08:04 ../
-rw-rw-r--  1 ubuntu ubuntu  285 May  8 08:04 Dockerfile
-rw-rw-r--  1 ubuntu ubuntu    0 May  8 08:19 .dockerignore

$ sudo docker build --no-cache -t="huzhi/static_web" .

$ sudo docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
huzhi/static_web    latest              85792be42dc2        8 minutes ago       212 MB
huzhi/test          latest              11cd92767a61        39 minutes ago      124 MB
ubuntu              latest              f7b3f317ec73        13 days ago         117 MB
fedora              latest              15895ef0b3b2        2 weeks ago         231 MB
ubuntu              12.04               5b117edd0b76        3 weeks ago         104 MB
ubuntu              12.04.5             5b117edd0b76        3 weeks ago         104 MB
ubuntu              10.04               e21dbcc7c9de        3 years ago         183 MB

$ sudo docker images huzhi/static_web
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
huzhi/static_web    latest              85792be42dc2        9 minutes ago       212 MB

$ sudo docker history huzhi/static_web
IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
85792be42dc2        10 minutes ago      /bin/sh -c #(nop)  EXPOSE 80/tcp                0 B                 
6255901b6e9f        10 minutes ago      /bin/sh -c echo 'Hi, I am in your containe...   27 B               
dac4f060368e        10 minutes ago      /bin/sh -c apt-get install -y nginx             56.5 MB             
dec44e1329e3        16 minutes ago      /bin/sh -c apt-get update                       38.2 MB             
ecd0ed3a265d        18 minutes ago      /bin/sh -c #(nop)  MAINTAINER James Turnbu...   0 B                 
f7b3f317ec73        13 days ago         /bin/sh -c #(nop)  CMD ["/bin/bash"]            0 B                 
<missing>           13 days ago         /bin/sh -c mkdir -p /run/systemd && echo '...   7 B                 
<missing>           13 days ago         /bin/sh -c sed -i 's/^#\s*\(deb.*universe\...   2.76 kB             
<missing>           13 days ago         /bin/sh -c rm -rf /var/lib/apt/lists/*          0 B                 
<missing>           13 days ago         /bin/sh -c set -xe   && echo '#!/bin/sh' >...   745 B               
<missing>           13 days ago         /bin/sh -c #(nop) ADD file:141408db9037263...   117 MB             


$ sudo docker history 85792be42dc2
IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
85792be42dc2        10 minutes ago      /bin/sh -c #(nop)  EXPOSE 80/tcp                0 B                 
6255901b6e9f        10 minutes ago      /bin/sh -c echo 'Hi, I am in your containe...   27 B               
dac4f060368e        10 minutes ago      /bin/sh -c apt-get install -y nginx             56.5 MB             
dec44e1329e3        17 minutes ago      /bin/sh -c apt-get update                       38.2 MB             
ecd0ed3a265d        18 minutes ago      /bin/sh -c #(nop)  MAINTAINER James Turnbu...   0 B                 
f7b3f317ec73        13 days ago         /bin/sh -c #(nop)  CMD ["/bin/bash"]            0 B                 
<missing>           13 days ago         /bin/sh -c mkdir -p /run/systemd && echo '...   7 B                 
<missing>           13 days ago         /bin/sh -c sed -i 's/^#\s*\(deb.*universe\...   2.76 kB             
<missing>           13 days ago         /bin/sh -c rm -rf /var/lib/apt/lists/*          0 B                 
<missing>           13 days ago         /bin/sh -c set -xe   && echo '#!/bin/sh' >...   745 B               
<missing>           13 days ago         /bin/sh -c #(nop) ADD file:141408db9037263...   117 MB             

$ sudo docker run -d -p 80 --name static_web huzhi/static_web nginx -g "daemon off;"
cf5e2539a79321650661d2ac33abee53057f557fe122e7417357d817533b333e

$ sudo docker ps -l
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                   NAMES
cf5e2539a793        huzhi/static_web    "nginx -g 'daemon ..."   57 seconds ago      Up 56 seconds       0.0.0.0:32768->80/tcp   static_web

$ sudo docker port cf5e2539a793 80
0.0.0.0:32768

$ sudo docker port static_web 80
0.0.0.0:32768

$ sudo docker run -d -p 80:80 --name static_web huzhi/static_web nginx -g "daemon off;"

$ sudo docker run -d -p 8080:80 --name static_web huzhi/static_web nginx -g "daemon off;"

$ sudo docker run -d -p 127.0.0.1:80:80 --name static_web huzhi/static_web nginx -g "daemon off;"

$ sudo docker run -d -p 127.0.0.1::80 --name static_web huzhi/static_web nginx -g "daemon off;"

$ sudo docker run -d -P --name static_web huzhi/static_web nginx -g "daemon off;"

$ curl localhost:32768
Hi, I am in your container
```


### 常见Dockerfile指令和示例

```bash
参考
https://docs.docker.com/engine/reference/builder/

####################################################################################

FROM
MAINTAINER
RUN
EXPOSE
CMD
ENTRYPOINT WORKDIR
USERcd
VOLUME
ADD
COPY
ONBUILD

####################################################################################

# Version: 0.0.1
FROM ubuntu:16.04
MAINTAINER James Turnbull "james@example.com"
ENV REFRESHED_AT 2016-06-01
RUN apt-get -qq update

####################################################################################

FROM ubuntu:14.04
MAINTAINER James Turnbull "james@example.com"
RUN apt-get update
# /bin/sh -c "apt-get update"
RUN apt-get install -y nginx
# RUN [ "apt-get", " install", " -y", " nginx" ]
RUN echo 'Hi, I am in your container' > /var/www/html/index.html
EXPOSE 80

####################################################################################

FROM ubuntu:16.04
MAINTAINER James Turnbull "james@example.com"
ENV REFRESHED_AT 2013-07-28
RUN apt-get update
RUN apt-get install -y apache2
ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2
ONBUILD ADD . /var/www/
EXPOSE 80
ENTRYPOINT ["/usr/sbin/apache2"]
CMD ["-D", "FOREGROUND"]

####################################################################################

FROM ubuntu:16.04
MAINTAINER James Turnbull "james@example.com"
ENV REFRESHED_AT 2016-06-01
RUN apt-get update
RUN apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN echo "root:password" | chpasswd
EXPOSE 22

####################################################################################

FROM jamtur01/apache2
MAINTAINER James Turnbull "james@example.com"
ENV APPLICATION_NAME webapp
ENV ENVIRONMENT development

####################################################################################

```

### 目录挂载
```bash
-v $PWD/webapp:/opt/webapp
-v :/opt/webapp # 容器作为数据盘
```

### 容器 link

```bash

# 宿主机网络，默认安装 docker0 网卡
$ ifconfig -a
docker0   Link encap:Ethernet  HWaddr 02:42:24:77:fa:22
          inet addr:172.18.0.1  Bcast:0.0.0.0  Mask:255.255.0.0
          inet6 addr: fe80::42:24ff:fe77:fa22/64 Scope:Link
          UP BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:149249 errors:0 dropped:0 overruns:0 frame:0
          TX packets:210154 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:8692217 (8.6 MB)  TX bytes:283872701 (283.8 MB)
eth0      Link encap:Ethernet  HWaddr fa:16:3e:81:7e:e4
          inet addr:172.17.2.15  Bcast:172.17.2.255  Mask:255.255.255.0
          inet6 addr: fe80::f816:3eff:fe81:7ee4/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:65470  Metric:1
          RX packets:16058983 errors:0 dropped:0 overruns:0 frame:0
          TX packets:20887904 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:9130973317 (9.1 GB)  TX bytes:5612731152 (5.6 GB)
lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:8106777 errors:0 dropped:0 overruns:0 frame:0
          TX packets:8106777 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:657193214 (657.1 MB)  TX bytes:657193214 (657.1 MB)

$ sudo docker run -ti ubuntu /bin/bash

# 容器中分配 docker0 的子网 IP
root@d5067c81c703:/# ifconfig -a
eth0      Link encap:Ethernet  HWaddr 02:42:ac:12:00:02
          inet addr:172.18.0.2  Bcast:0.0.0.0  Mask:255.255.0.0
          inet6 addr: fe80::42:acff:fe12:2/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:18755 errors:0 dropped:0 overruns:0 frame:0
          TX packets:12038 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:25335378 (25.3 MB)  TX bytes:866216 (866.2 KB)
lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

root@d5067c81c703:/#

root@34db29f846be:/# traceroute www.baidu.com
traceroute to www.baidu.com (61.135.169.125), 30 hops max, 60 byte packets
# 通过宿主机 docker0
1  172.18.0.1 (172.18.0.1)  0.137 ms  0.028 ms  0.046 ms
# 通过宿主机 eth0
2  172.17.2.1 (172.17.2.1)  0.229 ms  0.154 ms  0.225 ms
3  192-168-14-1.avlyun.org (192.168.14.1)  2.684 ms  2.957 ms  3.317 ms
4  192.168.55.3 (192.168.55.3)  0.591 ms  0.496 ms  0.522 ms
5  171.113.252.1 (171.113.252.1)  2.071 ms  2.431 ms  2.014 ms
6  111.175.208.170 (111.175.208.170)  4.874 ms  5.454 ms  5.355 ms
7  111.175.209.49 (111.175.209.49)  1.727 ms  1.671 ms  1.588 ms
8  * * *
9  202.97.57.102 (202.97.57.102)  24.902 ms * *
10  * 219.158.39.61 (219.158.39.61)  28.307 ms *
11  * * *
12  124.65.194.78 (124.65.194.78)  22.472 ms * *
13  124.65.58.66 (124.65.58.66)  25.958 ms 124.65.59.198 (124.65.59.198)  22.781 ms 124.65.59.114 (124.65.59.114)  22.544 ms
14  61.49.168.82 (61.49.168.82)  25.375 ms 202.106.43.30 (202.106.43.30)  22.391 ms 123.125.248.126 (123.125.248.126)  26.513 ms
15  * * *
16  * * *
17  * * *
18  * * *
19  * * *
20  * * *
21  * * *
22  * * *
23  * * *
24  * * *
25  * * *
26  * * *
27  * * *
28  * * *
29  * * *
30  * * *
root@34db29f846be:/#

# 启动容器后，默认宿主机会产生一个网卡
$ ifconfig -a
docker0   Link encap:Ethernet  HWaddr 02:42:24:77:fa:22
          inet addr:172.18.0.1  Bcast:0.0.0.0  Mask:255.255.0.0
          inet6 addr: fe80::42:24ff:fe77:fa22/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:149257 errors:0 dropped:0 overruns:0 frame:0
          TX packets:210154 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:8692753 (8.6 MB)  TX bytes:283872701 (283.8 MB)
eth0      Link encap:Ethernet  HWaddr fa:16:3e:81:7e:e4
          inet addr:172.17.2.15  Bcast:172.17.2.255  Mask:255.255.255.0
          inet6 addr: fe80::f816:3eff:fe81:7ee4/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:65470  Metric:1
          RX packets:16076367 errors:0 dropped:0 overruns:0 frame:0
          TX packets:20932872 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:9132815016 (9.1 GB)  TX bytes:5618288512 (5.6 GB)
lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:8106785 errors:0 dropped:0 overruns:0 frame:0
          TX packets:8106785 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:657193614 (657.1 MB)  TX bytes:657193614 (657.1 MB)
vethe4e9530 Link encap:Ethernet  HWaddr 12:5c:77:2d:96:0b
          inet6 addr: fe80::105c:77ff:fe2d:960b/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:8 errors:0 dropped:0 overruns:0 frame:0
          TX packets:8 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:648 (648.0 B)  TX bytes:648 (648.0 B)

# 宿主机启动 dockerd 进程后也会修改防火墙 iptables
$ sudo iptables -t nat -L -n
Chain PREROUTING (policy ACCEPT)
target     prot opt source               destination         
DOCKER     all  --  0.0.0.0/0            0.0.0.0/0            ADDRTYPE match dst-type LOCAL

Chain INPUT (policy ACCEPT)
target     prot opt source               destination         

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination         
DOCKER     all  --  0.0.0.0/0           !127.0.0.0/8          ADDRTYPE match dst-type LOCAL

Chain POSTROUTING (policy ACCEPT)
target     prot opt source               destination         
MASQUERADE  all  --  172.18.0.0/16        0.0.0.0/0           

Chain DOCKER (2 references)
target     prot opt source               destination         
RETURN     all  --  0.0.0.0/0            0.0.0.0/0

# 通过 --link 参数连接另一个容器
$ sudo docker run -p 4567 --name webapp --link redis:db -ti -v $PWD/webapp:/opt/webapp huzhi/sinatra /bin/bash

root@cf280bb8b575:/#
# 通过 --link 参数启动的容器会修改 /etc/hosts 和 env
root@cf280bb8b575:/# cat /etc/hosts
127.0.0.1    localhost
::1    localhost ip6-localhost ip6-loopback
fe00::0    ip6-localnet
ff00::0    ip6-mcastprefix
ff02::1    ip6-allnodes
ff02::2    ip6-allrouters
172.18.0.3    db 12a11f176856 redis
172.18.0.2    cf280bb8b575

root@cf280bb8b575:/#

root@cf280bb8b575:/# env
HOSTNAME=cf280bb8b575
DB_NAME=/webapp/db
DB_PORT_6379_TCP_PORT=6379
TERM=xterm
DB_PORT=tcp://172.18.0.3:6379
DB_PORT_6379_TCP=tcp://172.18.0.3:6379
LS_COLORS=rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.jpg=01;35:*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.oga=00;36:*.opus=00;36:*.spx=00;36:*.xspf=00;36:
DB_ENV_REFRESHED_AT=2014-06-01
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
REFRESHED_AT=2014-06-01
PWD=/
DB_PORT_6379_TCP_ADDR=172.18.0.3
DB_PORT_6379_TCP_PROTO=tcp
SHLVL=1
HOME=/root
_=/usr/bin/env

root@cf280bb8b575:/#

root@cf280bb8b575:/# exit
exit

```


### Docker网络

```bash
# 宿主机网络
ubuntu@huzhi-ubuntu3:~/docker/docbook$ ifconfig -a
docker0   Link encap:Ethernet  HWaddr 02:42:24:77:fa:22 
          inet addr:172.18.0.1  Bcast:0.0.0.0  Mask:255.255.0.0
          inet6 addr: fe80::42:24ff:fe77:fa22/64 Scope:Link
          UP BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:285866 errors:0 dropped:0 overruns:0 frame:0
          TX packets:374854 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:16876068 (16.8 MB)  TX bytes:508925014 (508.9 MB)

eth0      Link encap:Ethernet  HWaddr fa:16:3e:81:7e:e4 
          inet addr:172.17.2.15  Bcast:172.17.2.255  Mask:255.255.255.0
          inet6 addr: fe80::f816:3eff:fe81:7ee4/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:65470  Metric:1
          RX packets:37499145 errors:0 dropped:0 overruns:0 frame:0
          TX packets:58821757 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:20850063223 (20.8 GB)  TX bytes:14821928460 (14.8 GB)

lo        Link encap:Local Loopback 
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:9763316 errors:0 dropped:0 overruns:0 frame:0
          TX packets:9763316 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:906707772 (906.7 MB)  TX bytes:906707772 (906.7 MB)

ubuntu@huzhi-ubuntu3:~/docker/docbook$
ubuntu@huzhi-ubuntu3:~$ ip -d link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00 promiscuity 0
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 65470 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether fa:16:3e:81:7e:e4 brd ff:ff:ff:ff:ff:ff promiscuity 0
3: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default
    link/ether 02:42:24:77:fa:22 brd ff:ff:ff:ff:ff:ff promiscuity 0
    bridge
99: veth633680d: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT group default
    link/ether e2:81:85:aa:83:62 brd ff:ff:ff:ff:ff:ff promiscuity 1
    veth
107: vethd87c6b8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT group default
    link/ether 12:e8:56:2b:8f:1c brd ff:ff:ff:ff:ff:ff promiscuity 1
    veth
ubuntu@huzhi-ubuntu3:~$ brctl show
bridge name    bridge id        STP enabled    interfaces
docker0        8000.02422477fa22    no        veth633680d
                                              vethd87c6b8
ubuntu@huzhi-ubuntu3:~$

# 增加桥接接口
ubuntu@huzhi-ubuntu3:~$ sudo brctl addbr br0
ubuntu@huzhi-ubuntu3:~$ brctl show
bridge name    bridge id        STP enabled    interfaces
br0        8000.000000000000    no       
docker0        8000.02422477fa22    no        veth633680d
                                              vethd87c6b8
ubuntu@huzhi-ubuntu3:~$ ip -d link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00 promiscuity 0
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 65470 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether fa:16:3e:81:7e:e4 brd ff:ff:ff:ff:ff:ff promiscuity 0
3: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default
    link/ether 02:42:24:77:fa:22 brd ff:ff:ff:ff:ff:ff promiscuity 0
    bridge
99: veth633680d: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT group default
    link/ether e2:81:85:aa:83:62 brd ff:ff:ff:ff:ff:ff promiscuity 1
    veth
107: vethd87c6b8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT group default
    link/ether 12:e8:56:2b:8f:1c brd ff:ff:ff:ff:ff:ff promiscuity 1
    veth
108: br0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default
    link/ether 6a:7d:5b:09:9d:d4 brd ff:ff:ff:ff:ff:ff promiscuity 0
    bridge
ubuntu@huzhi-ubuntu3:~$ sudo ip addr add 192.168.1.254/24 dev br0
ubuntu@huzhi-ubuntu3:~$ ip address
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 65470 qdisc pfifo_fast state UP group default qlen 1000
    link/ether fa:16:3e:81:7e:e4 brd ff:ff:ff:ff:ff:ff
    inet 172.17.2.15/24 brd 172.17.2.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::f816:3eff:fe81:7ee4/64 scope link
       valid_lft forever preferred_lft forever
3: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:24:77:fa:22 brd ff:ff:ff:ff:ff:ff
    inet 172.18.0.1/16 scope global docker0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:24ff:fe77:fa22/64 scope link
       valid_lft forever preferred_lft forever
99: veth633680d: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP group default
    link/ether e2:81:85:aa:83:62 brd ff:ff:ff:ff:ff:ff
    inet6 fe80::e081:85ff:feaa:8362/64 scope link
       valid_lft forever preferred_lft forever
107: vethd87c6b8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP group default
    link/ether 12:e8:56:2b:8f:1c brd ff:ff:ff:ff:ff:ff
    inet6 fe80::10e8:56ff:fe2b:8f1c/64 scope link
       valid_lft forever preferred_lft forever
108: br0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default
    link/ether 6a:7d:5b:09:9d:d4 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.254/24 scope global br0
       valid_lft forever preferred_lft forever
ubuntu@huzhi-ubuntu3:~$ sudo ip link set dev br0 up
ubuntu@huzhi-ubuntu3:~$ ip address
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 65470 qdisc pfifo_fast state UP group default qlen 1000
    link/ether fa:16:3e:81:7e:e4 brd ff:ff:ff:ff:ff:ff
    inet 172.17.2.15/24 brd 172.17.2.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::f816:3eff:fe81:7ee4/64 scope link
       valid_lft forever preferred_lft forever
3: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:24:77:fa:22 brd ff:ff:ff:ff:ff:ff
    inet 172.18.0.1/16 scope global docker0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:24ff:fe77:fa22/64 scope link
       valid_lft forever preferred_lft forever
99: veth633680d: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP group default
    link/ether e2:81:85:aa:83:62 brd ff:ff:ff:ff:ff:ff
    inet6 fe80::e081:85ff:feaa:8362/64 scope link
       valid_lft forever preferred_lft forever
107: vethd87c6b8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP group default
    link/ether 12:e8:56:2b:8f:1c brd ff:ff:ff:ff:ff:ff
    inet6 fe80::10e8:56ff:fe2b:8f1c/64 scope link
       valid_lft forever preferred_lft forever
108: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN group default
    link/ether 6a:7d:5b:09:9d:d4 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.254/24 scope global br0
       valid_lft forever preferred_lft forever
    inet6 fe80::687d:5bff:fe09:9dd4/64 scope link
       valid_lft forever preferred_lft forever
ubuntu@huzhi-ubuntu3:~$
ubuntu@huzhi-ubuntu3:~$ brctl show
bridge name    bridge id        STP enabled    interfaces
br0        8000.000000000000    no       
docker0        8000.02422477fa22    no        veth633680d
                                                                    vethd87c6b8
ubuntu@huzhi-ubuntu3:~$
ubuntu@huzhi-ubuntu3:~$ sudo ip link add foo type veth peer name bar
ubuntu@huzhi-ubuntu3:~$ ip -d link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00 promiscuity 0
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 65470 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether fa:16:3e:81:7e:e4 brd ff:ff:ff:ff:ff:ff promiscuity 0
3: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default
    link/ether 02:42:24:77:fa:22 brd ff:ff:ff:ff:ff:ff promiscuity 0
    bridge
99: veth633680d: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT group default
    link/ether e2:81:85:aa:83:62 brd ff:ff:ff:ff:ff:ff promiscuity 1
    veth
107: vethd87c6b8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT group default
    link/ether 12:e8:56:2b:8f:1c brd ff:ff:ff:ff:ff:ff promiscuity 1
    veth
113: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN mode DEFAULT group default
    link/ether 1a:2d:fb:d4:0b:0d brd ff:ff:ff:ff:ff:ff promiscuity 0
    bridge
114: bar: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/ether 4a:e3:1e:a3:0d:dc brd ff:ff:ff:ff:ff:ff promiscuity 0
    veth
115: foo: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/ether d2:dc:88:2c:5e:72 brd ff:ff:ff:ff:ff:ff promiscuity 0
    veth
ubuntu@huzhi-ubuntu3:~$ brctl show
bridge name    bridge id        STP enabled    interfaces
br0        8000.000000000000    no       
docker0        8000.02422477fa22    no        veth633680d
                                              vethd87c6b8
ubuntu@huzhi-ubuntu3:~$ ifconfig -a
bar       Link encap:Ethernet  HWaddr 4a:e3:1e:a3:0d:dc 
          BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

br0       Link encap:Ethernet  HWaddr 1a:2d:fb:d4:0b:0d 
          inet addr:192.168.1.254  Bcast:0.0.0.0  Mask:255.255.255.0
          inet6 addr: fe80::182d:fbff:fed4:b0d/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:8 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:0 (0.0 B)  TX bytes:648 (648.0 B)

docker0   Link encap:Ethernet  HWaddr 02:42:24:77:fa:22 
          inet addr:172.18.0.1  Bcast:0.0.0.0  Mask:255.255.0.0
          inet6 addr: fe80::42:24ff:fe77:fa22/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:288895 errors:0 dropped:0 overruns:0 frame:0
          TX packets:378972 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:18108677 (18.1 MB)  TX bytes:513368037 (513.3 MB)

eth0      Link encap:Ethernet  HWaddr fa:16:3e:81:7e:e4 
          inet addr:172.17.2.15  Bcast:172.17.2.255  Mask:255.255.255.0
          inet6 addr: fe80::f816:3eff:fe81:7ee4/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:65470  Metric:1
          RX packets:46572198 errors:0 dropped:0 overruns:0 frame:0
          TX packets:71908475 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:25029259970 (25.0 GB)  TX bytes:18940854588 (18.9 GB)

foo       Link encap:Ethernet  HWaddr d2:dc:88:2c:5e:72 
          BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

lo        Link encap:Local Loopback 
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:10570707 errors:0 dropped:0 overruns:0 frame:0
          TX packets:10570707 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:971532402 (971.5 MB)  TX bytes:971532402 (971.5 MB)

veth633680d Link encap:Ethernet  HWaddr e2:81:85:aa:83:62 
          inet6 addr: fe80::e081:85ff:feaa:8362/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:1664 errors:0 dropped:0 overruns:0 frame:0
          TX packets:1840 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:693975 (693.9 KB)  TX bytes:1084319 (1.0 MB)

vethd87c6b8 Link encap:Ethernet  HWaddr 12:e8:56:2b:8f:1c 
          inet6 addr: fe80::10e8:56ff:fe2b:8f1c/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:69 errors:0 dropped:0 overruns:0 frame:0
          TX packets:74 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:27603 (27.6 KB)  TX bytes:32798 (32.7 KB)

ubuntu@huzhi-ubuntu3:~$


$ docker run -ti --net=none ubuntu bash
$ docker run -ti --net=host ubuntu bash
$ docker run -ti --net=container:cf5e2539a793 ubuntu bash

ubuntu@huzhi-ubuntu3:~/docker/docbook/ch03/simple$ sudo docker run -t -i --net none --name cookbook huzhi/ubuntu bash
root@ced902c1f11f:/# ip -d link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00 promiscuity 0
root@ced902c1f11f:/#
root@ced902c1f11f:/# ip address
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
root@ced902c1f11f:/#
ubuntu@huzhi-ubuntu3:~$ sudo brctl addif br0 foo
ubuntu@huzhi-ubuntu3:~$ ip -d link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00 promiscuity 0
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 65470 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether fa:16:3e:81:7e:e4 brd ff:ff:ff:ff:ff:ff promiscuity 0
3: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default
    link/ether 02:42:24:77:fa:22 brd ff:ff:ff:ff:ff:ff promiscuity 0
    bridge
99: veth633680d: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT group default
    link/ether e2:81:85:aa:83:62 brd ff:ff:ff:ff:ff:ff promiscuity 1
    veth
107: vethd87c6b8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT group default
    link/ether 12:e8:56:2b:8f:1c brd ff:ff:ff:ff:ff:ff promiscuity 1
    veth
113: br0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default
    link/ether d2:dc:88:2c:5e:72 brd ff:ff:ff:ff:ff:ff promiscuity 0
    bridge
114: bar: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/ether 4a:e3:1e:a3:0d:dc brd ff:ff:ff:ff:ff:ff promiscuity 0
    veth
115: foo: <BROADCAST,MULTICAST> mtu 1500 qdisc noop master br0 state DOWN mode DEFAULT group default qlen 1000
    link/ether d2:dc:88:2c:5e:72 brd ff:ff:ff:ff:ff:ff promiscuity 1
    veth
ubuntu@huzhi-ubuntu3:~$ brctl show
bridge name    bridge id        STP enabled    interfaces
br0        8000.d2dc882c5e72    no              foo
docker0        8000.02422477fa22    no        veth633680d
                            vethd87c6b8
ubuntu@huzhi-ubuntu3:~$ ifconfig -a
bar       Link encap:Ethernet  HWaddr 4a:e3:1e:a3:0d:dc 
          BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

br0       Link encap:Ethernet  HWaddr d2:dc:88:2c:5e:72 
          inet addr:192.168.1.254  Bcast:0.0.0.0  Mask:255.255.255.0
          inet6 addr: fe80::182d:fbff:fed4:b0d/64 Scope:Link
          UP BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:8 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:0 (0.0 B)  TX bytes:648 (648.0 B)

docker0   Link encap:Ethernet  HWaddr 02:42:24:77:fa:22 
          inet addr:172.18.0.1  Bcast:0.0.0.0  Mask:255.255.0.0
          inet6 addr: fe80::42:24ff:fe77:fa22/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:288895 errors:0 dropped:0 overruns:0 frame:0
          TX packets:378972 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:18108677 (18.1 MB)  TX bytes:513368037 (513.3 MB)

eth0      Link encap:Ethernet  HWaddr fa:16:3e:81:7e:e4 
          inet addr:172.17.2.15  Bcast:172.17.2.255  Mask:255.255.255.0
          inet6 addr: fe80::f816:3eff:fe81:7ee4/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:65470  Metric:1
          RX packets:46572322 errors:0 dropped:0 overruns:0 frame:0
          TX packets:71908599 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:25029270146 (25.0 GB)  TX bytes:18940873860 (18.9 GB)

foo       Link encap:Ethernet  HWaddr d2:dc:88:2c:5e:72 
          BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

lo        Link encap:Local Loopback 
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:10570725 errors:0 dropped:0 overruns:0 frame:0
          TX packets:10570725 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:971533302 (971.5 MB)  TX bytes:971533302 (971.5 MB)

veth633680d Link encap:Ethernet  HWaddr e2:81:85:aa:83:62 
          inet6 addr: fe80::e081:85ff:feaa:8362/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:1664 errors:0 dropped:0 overruns:0 frame:0
          TX packets:1840 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:693975 (693.9 KB)  TX bytes:1084319 (1.0 MB)

vethd87c6b8 Link encap:Ethernet  HWaddr 12:e8:56:2b:8f:1c 
          inet6 addr: fe80::10e8:56ff:fe2b:8f1c/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:69 errors:0 dropped:0 overruns:0 frame:0
          TX packets:74 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:27603 (27.6 KB)  TX bytes:32798 (32.7 KB)

ubuntu@huzhi-ubuntu3:~$
ubuntu@huzhi-ubuntu3:~$ sudo ip link set foo up
ubuntu@huzhi-ubuntu3:~$ ip -d link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00 promiscuity 0
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 65470 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether fa:16:3e:81:7e:e4 brd ff:ff:ff:ff:ff:ff promiscuity 0
3: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default
    link/ether 02:42:24:77:fa:22 brd ff:ff:ff:ff:ff:ff promiscuity 0
    bridge
99: veth633680d: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT group default
    link/ether e2:81:85:aa:83:62 brd ff:ff:ff:ff:ff:ff promiscuity 1
    veth
107: vethd87c6b8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT group default
    link/ether 12:e8:56:2b:8f:1c brd ff:ff:ff:ff:ff:ff promiscuity 1
    veth
113: br0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default
    link/ether d2:dc:88:2c:5e:72 brd ff:ff:ff:ff:ff:ff promiscuity 0
    bridge
114: bar: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/ether 4a:e3:1e:a3:0d:dc brd ff:ff:ff:ff:ff:ff promiscuity 0
    veth
115: foo: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc pfifo_fast master br0 state DOWN mode DEFAULT group default qlen 1000
    link/ether d2:dc:88:2c:5e:72 brd ff:ff:ff:ff:ff:ff promiscuity 1
    veth
ubuntu@huzhi-ubuntu3:~$ brctl show
bridge name    bridge id        STP enabled    interfaces
br0        8000.d2dc882c5e72    no        foo
docker0        8000.02422477fa22    no        veth633680d
                                                                    vethd87c6b8
ubuntu@huzhi-ubuntu3:~$ ifconfig -a
bar       Link encap:Ethernet  HWaddr 4a:e3:1e:a3:0d:dc 
          BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

br0       Link encap:Ethernet  HWaddr d2:dc:88:2c:5e:72 
          inet addr:192.168.1.254  Bcast:0.0.0.0  Mask:255.255.255.0
          inet6 addr: fe80::182d:fbff:fed4:b0d/64 Scope:Link
          UP BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:8 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:0 (0.0 B)  TX bytes:648 (648.0 B)

docker0   Link encap:Ethernet  HWaddr 02:42:24:77:fa:22 
          inet addr:172.18.0.1  Bcast:0.0.0.0  Mask:255.255.0.0
          inet6 addr: fe80::42:24ff:fe77:fa22/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:288895 errors:0 dropped:0 overruns:0 frame:0
          TX packets:378972 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:18108677 (18.1 MB)  TX bytes:513368037 (513.3 MB)

eth0      Link encap:Ethernet  HWaddr fa:16:3e:81:7e:e4 
          inet addr:172.17.2.15  Bcast:172.17.2.255  Mask:255.255.255.0
          inet6 addr: fe80::f816:3eff:fe81:7ee4/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:65470  Metric:1
          RX packets:46572448 errors:0 dropped:0 overruns:0 frame:0
          TX packets:71908717 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:25029280498 (25.0 GB)  TX bytes:18940892848 (18.9 GB)

foo       Link encap:Ethernet  HWaddr d2:dc:88:2c:5e:72 
          UP BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

lo        Link encap:Local Loopback 
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:10570735 errors:0 dropped:0 overruns:0 frame:0
          TX packets:10570735 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:971533802 (971.5 MB)  TX bytes:971533802 (971.5 MB)

veth633680d Link encap:Ethernet  HWaddr e2:81:85:aa:83:62 
          inet6 addr: fe80::e081:85ff:feaa:8362/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:1664 errors:0 dropped:0 overruns:0 frame:0
          TX packets:1840 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:693975 (693.9 KB)  TX bytes:1084319 (1.0 MB)

vethd87c6b8 Link encap:Ethernet  HWaddr 12:e8:56:2b:8f:1c 
          inet6 addr: fe80::10e8:56ff:fe2b:8f1c/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:69 errors:0 dropped:0 overruns:0 frame:0
          TX packets:74 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:27603 (27.6 KB)  TX bytes:32798 (32.7 KB)

ubuntu@huzhi-ubuntu3:~$
root@huzhi-ubuntu3:/var/run/docker/netns# pwd
/var/run/docker/netns
root@huzhi-ubuntu3:/var/run/docker/netns# ll
total 0
drwxr-xr-x 2 root root 100 Jun 11 05:59 ./
drwx------ 7 root root 140 May  8 06:12 ../
-r--r--r-- 1 root root   0 Jun 11 05:30 5cda50bb96a1
-r--r--r-- 1 root root   0 Jun 11 05:43 abfc292d54a6
-r--r--r-- 1 root root   0 Jun 11 05:59 ce46d1411530
root@huzhi-ubuntu3:/var/run/docker/netns# docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                  NAMES
ced902c1f11f        huzhi/ubuntu        "bash"                   48 minutes ago      Up 48 minutes                              cookbook
6e63ce488220        wordpress           "docker-entrypoint..."   About an hour ago   Up About an hour    0.0.0.0:8080->80/tcp   compose_wordpress_1
f3c1832fb299        mysql               "docker-entrypoint..."   About an hour ago   Up About an hour    3306/tcp               compose_mysql_1
root@huzhi-ubuntu3:/var/run# exit
exit
ubuntu@huzhi-ubuntu3:~$
ubuntu@huzhi-ubuntu3:~$ cd /var/run/
ubuntu@huzhi-ubuntu3:/var/run$ sudo ln -s /var/run/docker/netns netns
ubuntu@huzhi-ubuntu3:/var/run$ sudo ip netns
ce46d1411530
abfc292d54a6
5cda50bb96a1
ubuntu@huzhi-ubuntu3:/var/run$
ubuntu@huzhi-ubuntu3:~$ sudo docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                  NAMES
ced902c1f11f        huzhi/ubuntu        "bash"                   52 minutes ago      Up 52 minutes                              cookbook
6e63ce488220        wordpress           "docker-entrypoint..."   About an hour ago   Up About an hour    0.0.0.0:8080->80/tcp   compose_wordpress_1
f3c1832fb299        mysql               "docker-entrypoint..."   About an hour ago   Up About an hour    3306/tcp               compose_mysql_1
ubuntu@huzhi-ubuntu3:~$
ubuntu@huzhi-ubuntu3:~$ sudo docker stop compose_wordpress_1
compose_wordpress_1
ubuntu@huzhi-ubuntu3:~$ sudo docker stop compose_mysql_1
compose_mysql_1
ubuntu@huzhi-ubuntu3:~$ sudo docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                      PORTS               NAMES
ced902c1f11f        huzhi/ubuntu        "bash"                   54 minutes ago      Up 54 minutes                                   cookbook
6e63ce488220        wordpress           "docker-entrypoint..."   About an hour ago   Exited (0) 15 seconds ago                       compose_wordpress_1
f3c1832fb299        mysql               "docker-entrypoint..."   About an hour ago   Exited (0) 3 seconds ago                        compose_mysql_1
ubuntu@huzhi-ubuntu3:~$ sudo docker rm 6e63ce488220
6e63ce488220
ubuntu@huzhi-ubuntu3:~$ sudo docker rm f3c1832fb299
f3c1832fb299
ubuntu@huzhi-ubuntu3:~$
ubuntu@huzhi-ubuntu3:~$ sudo docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
ced902c1f11f        huzhi/ubuntu        "bash"              54 minutes ago      Up 54 minutes                           cookbook
ubuntu@huzhi-ubuntu3:~$
ubuntu@huzhi-ubuntu3:/var/run$ sudo ip netns
ce46d1411530
ubuntu@huzhi-ubuntu3:/var/run$
ubuntu@huzhi-ubuntu3:/var/run$ NIC=$(sudo ip netns)
ubuntu@huzhi-ubuntu3:/var/run$ echo $NIC
ce46d1411530
ubuntu@huzhi-ubuntu3:/var/run$
ubuntu@huzhi-ubuntu3:/var/run$ sudo ip link set bar netns $NIC
ubuntu@huzhi-ubuntu3:/var/run$ brctl show
bridge name    bridge id        STP enabled    interfaces
br0        8000.d2dc882c5e72    no        foo
docker0        8000.02422477fa22    no       
ubuntu@huzhi-ubuntu3:/var/run$ ip -d link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00 promiscuity 0
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 65470 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether fa:16:3e:81:7e:e4 brd ff:ff:ff:ff:ff:ff promiscuity 0
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default
    link/ether 02:42:24:77:fa:22 brd ff:ff:ff:ff:ff:ff promiscuity 0
    bridge
113: br0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default
    link/ether d2:dc:88:2c:5e:72 brd ff:ff:ff:ff:ff:ff promiscuity 0
    bridge
115: foo: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc pfifo_fast master br0 state DOWN mode DEFAULT group default qlen 1000
    link/ether d2:dc:88:2c:5e:72 brd ff:ff:ff:ff:ff:ff promiscuity 1
    veth
ubuntu@huzhi-ubuntu3:/var/run$ ifconfig -a
br0       Link encap:Ethernet  HWaddr d2:dc:88:2c:5e:72 
          inet addr:192.168.1.254  Bcast:0.0.0.0  Mask:255.255.255.0
          inet6 addr: fe80::182d:fbff:fed4:b0d/64 Scope:Link
          UP BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:8 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:0 (0.0 B)  TX bytes:648 (648.0 B)

docker0   Link encap:Ethernet  HWaddr 02:42:24:77:fa:22 
          inet addr:172.18.0.1  Bcast:0.0.0.0  Mask:255.255.0.0
          inet6 addr: fe80::42:24ff:fe77:fa22/64 Scope:Link
          UP BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:288895 errors:0 dropped:0 overruns:0 frame:0
          TX packets:378972 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:18108677 (18.1 MB)  TX bytes:513368037 (513.3 MB)

eth0      Link encap:Ethernet  HWaddr fa:16:3e:81:7e:e4 
          inet addr:172.17.2.15  Bcast:172.17.2.255  Mask:255.255.255.0
          inet6 addr: fe80::f816:3eff:fe81:7ee4/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:65470  Metric:1
          RX packets:46574210 errors:0 dropped:0 overruns:0 frame:0
          TX packets:71910582 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:25029425939 (25.0 GB)  TX bytes:18941140725 (18.9 GB)

foo       Link encap:Ethernet  HWaddr d2:dc:88:2c:5e:72 
          UP BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

lo        Link encap:Local Loopback 
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:10570905 errors:0 dropped:0 overruns:0 frame:0
          TX packets:10570905 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:971542302 (971.5 MB)  TX bytes:971542302 (971.5 MB)

ubuntu@huzhi-ubuntu3:/var/run$
ubuntu@huzhi-ubuntu3:/var/run$ sudo ip netns exec $NIC ip link set dev bar name eth1
ubuntu@huzhi-ubuntu3:/var/run$ brctl show
bridge name    bridge id        STP enabled    interfaces
br0        8000.d2dc882c5e72    no        foo
docker0        8000.02422477fa22    no       
ubuntu@huzhi-ubuntu3:/var/run$ ip -d link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00 promiscuity 0
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 65470 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether fa:16:3e:81:7e:e4 brd ff:ff:ff:ff:ff:ff promiscuity 0
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default
    link/ether 02:42:24:77:fa:22 brd ff:ff:ff:ff:ff:ff promiscuity 0
    bridge
113: br0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default
    link/ether d2:dc:88:2c:5e:72 brd ff:ff:ff:ff:ff:ff promiscuity 0
    bridge
115: foo: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc pfifo_fast master br0 state DOWN mode DEFAULT group default qlen 1000
    link/ether d2:dc:88:2c:5e:72 brd ff:ff:ff:ff:ff:ff promiscuity 1
    veth
ubuntu@huzhi-ubuntu3:/var/run$ ifconfig -a
br0       Link encap:Ethernet  HWaddr d2:dc:88:2c:5e:72 
          inet addr:192.168.1.254  Bcast:0.0.0.0  Mask:255.255.255.0
          inet6 addr: fe80::182d:fbff:fed4:b0d/64 Scope:Link
          UP BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:8 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:0 (0.0 B)  TX bytes:648 (648.0 B)

docker0   Link encap:Ethernet  HWaddr 02:42:24:77:fa:22 
          inet addr:172.18.0.1  Bcast:0.0.0.0  Mask:255.255.0.0
          inet6 addr: fe80::42:24ff:fe77:fa22/64 Scope:Link
          UP BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:288895 errors:0 dropped:0 overruns:0 frame:0
          TX packets:378972 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:18108677 (18.1 MB)  TX bytes:513368037 (513.3 MB)

eth0      Link encap:Ethernet  HWaddr fa:16:3e:81:7e:e4 
          inet addr:172.17.2.15  Bcast:172.17.2.255  Mask:255.255.255.0
          inet6 addr: fe80::f816:3eff:fe81:7ee4/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:65470  Metric:1
          RX packets:46574376 errors:0 dropped:0 overruns:0 frame:0
          TX packets:71910702 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:25029439619 (25.0 GB)  TX bytes:18941157789 (18.9 GB)

foo       Link encap:Ethernet  HWaddr d2:dc:88:2c:5e:72 
          UP BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

lo        Link encap:Local Loopback 
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:10570913 errors:0 dropped:0 overruns:0 frame:0
          TX packets:10570913 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:971542702 (971.5 MB)  TX bytes:971542702 (971.5 MB)

ubuntu@huzhi-ubuntu3:/var/run$
ubuntu@huzhi-ubuntu3:/var/run$
ubuntu@huzhi-ubuntu3:/var/run$ sudo ip netns exec $NIC ip link set eth1 address 12:34:56:78:9a:bc
ubuntu@huzhi-ubuntu3:/var/run$ sudo ip netns exec $NIC ip link set eth1 up
ubuntu@huzhi-ubuntu3:/var/run$
ubuntu@huzhi-ubuntu3:/var/run$ sudo ip netns exec $NIC ip addr add 192.168.1.1/24 dev eth1
ubuntu@huzhi-ubuntu3:/var/run$ sudo ip netns exec $NIC ip route add default via 192.168.1.254
ubuntu@huzhi-ubuntu3:/var/run$
ubuntu@huzhi-ubuntu3:/var/run$ sudo iptables -t nat -A POSTROUTING -s 192.168.0.0/24 -j MASQUERADE
ubuntu@huzhi-ubuntu3:/var/run$




root@ced902c1f11f:/# route
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
root@ced902c1f11f:/#
root@ced902c1f11f:/#
root@ced902c1f11f:/# ip -d link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00 promiscuity 0
114: bar: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/ether 4a:e3:1e:a3:0d:dc brd ff:ff:ff:ff:ff:ff promiscuity 0
    veth
root@ced902c1f11f:/# ip -d link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00 promiscuity 0
114: eth1: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/ether 4a:e3:1e:a3:0d:dc brd ff:ff:ff:ff:ff:ff promiscuity 0
    veth
root@ced902c1f11f:/# ip -d link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00 promiscuity 0
114: eth1: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/ether 12:34:56:78:9a:bc brd ff:ff:ff:ff:ff:ff promiscuity 0
    veth
root@ced902c1f11f:/# ifconfig -a
eth1      Link encap:Ethernet  HWaddr 12:34:56:78:9a:bc 
          BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

lo        Link encap:Local Loopback 
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

root@ced902c1f11f:/# ip -d link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00 promiscuity 0
114: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether 12:34:56:78:9a:bc brd ff:ff:ff:ff:ff:ff promiscuity 0
    veth
root@ced902c1f11f:/# ifconfig -a
eth1      Link encap:Ethernet  HWaddr 12:34:56:78:9a:bc 
          inet6 addr: fe80::1034:56ff:fe78:9abc/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:8 errors:0 dropped:0 overruns:0 frame:0
          TX packets:8 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:648 (648.0 B)  TX bytes:648 (648.0 B)

lo        Link encap:Local Loopback 
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

root@ced902c1f11f:/# ifconfig -a
eth1      Link encap:Ethernet  HWaddr 12:34:56:78:9a:bc 
          inet addr:192.168.1.1  Bcast:0.0.0.0  Mask:255.255.255.0
          inet6 addr: fe80::1034:56ff:fe78:9abc/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:8 errors:0 dropped:0 overruns:0 frame:0
          TX packets:8 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:648 (648.0 B)  TX bytes:648 (648.0 B)

lo        Link encap:Local Loopback 
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

root@ced902c1f11f:/# route -n   
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.1.254   0.0.0.0         UG    0      0        0 eth1
192.168.1.0     0.0.0.0         255.255.255.0   U     0      0        0 eth1
root@ced902c1f11f:/#

GRE隧道
eth0
192.168.33.11
192.168.33.12
docker0
172.17.0.1
10101100,00010001,0|0000000,00000001
172.17.128.1
10101100,00010001,1|0000000,00000001
GRE
172.17.127.254
10101100,00010001,0|1111111,11111110
172.17.255.254
10101100,00010001,1|1111111,11111110
mask
172.17.0.0
10101100,00010001,0|0000000,00000000
172.17.128.0
10101100,00010001,1|0000000,00000000


192.168.33.11

ip tunnel add foo mode gre remote 192.168.33.12 local 192.168.33.11
ip link set foo up
ip addr add 172.17.127.254 dev foo
ip route add 172.17.128.0/17 dev foo


192.168.33.12

ip tunnel add bar mode gre remote 192.168.33.11 local 192.168.33.12
ip link set bar up
ip addr add 172.17.255.254 dev foo
ip route add 172.17.0.0/17 dev bar




bridge
host
macvlan
null
overlay
```


Docker Compose

ubuntu@huzhi-ubuntu3:~/docker$ sudo pip install -U docker-compose
ubuntu@huzhi-ubuntu3:~/docker$
ubuntu@huzhi-ubuntu3:~/docker$ docker-compose --version
docker-compose version 1.13.0, build 1719ceb
ubuntu@huzhi-ubuntu3:~/docker$
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose$ docker-compose --help
Define and run multi-container applications with Docker.

Usage:
  docker-compose [-f <arg>...] [options] [COMMAND] [ARGS...]
  docker-compose -h|--help

Options:
  -f, --file FILE             Specify an alternate compose file (default: docker-compose.yml)
  -p, --project-name NAME     Specify an alternate project name (default: directory name)
  --verbose                   Show more output
  -v, --version               Print version and exit
  -H, --host HOST             Daemon socket to connect to

  --tls                       Use TLS; implied by --tlsverify
  --tlscacert CA_PATH         Trust certs signed only by this CA
  --tlscert CLIENT_CERT_PATH  Path to TLS certificate file
  --tlskey TLS_KEY_PATH       Path to TLS key file
  --tlsverify                 Use TLS and verify the remote
  --skip-hostname-check       Don't check the daemon's hostname against the name specified
                              in the client certificate (for example if your docker host
                              is an IP address)
  --project-directory PATH    Specify an alternate working directory
                              (default: the path of the compose file)

Commands:
  build              Build or rebuild services
  bundle             Generate a Docker bundle from the Compose file
  config             Validate and view the compose file
  create             Create services
  down               Stop and remove containers, networks, images, and volumes
  events             Receive real time events from containers
  exec               Execute a command in a running container
  help               Get help on a command
  images             List images
  kill               Kill containers
  logs               View output from containers
  pause              Pause services
  port               Print the public port for a port binding
  ps                 List containers
  pull               Pull service images
  push               Push service images
  restart            Restart services
  rm                 Remove stopped containers
  run                Run a one-off command
  scale              Set number of containers for a service
  start              Start services
  stop               Stop services
  top                Display the running processes
  unpause            Unpause services
  up                 Create and start containers
  version            Show the Docker-Compose version information
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose$
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose$ cat docker-compose.yml
wordpress:
  image: wordpress
  links:
   - mysql
  ports:
   - "80:80"
  environment:
   - WORDPRESS_DB_NAME=wordpress
   - WORDPRESS_DB_USER=wordpress
   - WORDPRESS_DB_PASSWORD=wordpresspwd
mysql:
  image: mysql
  environment:
   - MYSQL_ROOT_PASSWORD=wordpressdocker
   - MYSQL_DATABASE=wordpress
   - MYSQL_USER=wordpress
   - MYSQL_PASSWORD=wordpresspwd
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose$
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose$ sudo docker-compose up -d
Pulling mysql (mysql:latest)...
latest: Pulling from library/mysql
10a267c67f42: Pull complete
c2dcc7bb2a88: Pull complete
17e7a0445698: Pull complete
9a61839a176f: Pull complete
a1033d2f1825: Pull complete
0d6792140dcc: Pull complete
cd3adf03d6e6: Pull complete
d79d216fd92b: Pull complete
b3c25bdeb4f4: Pull complete
02556e8f331f: Pull complete
4bed508a9e77: Pull complete
Digest: sha256:2f4b1900c0ee53f344564db8d85733bd8d70b0a78cd00e6d92dc107224fc84a5
Status: Downloaded newer image for mysql:latest
Pulling wordpress (wordpress:latest)...
latest: Pulling from library/wordpress
ef0380f84d05: Pull complete
d676534ff315: Pull complete
c80a1f6ddd8d: Pull complete
c3e9b0c1871f: Pull complete
b5e2756f5f08: Pull complete
cd2ca1686b17: Pull complete
529b20a8291d: Pull complete
dd0c35492a16: Pull complete
719b692e57dd: Pull complete
19f393a2429a: Pull complete
b3eb4c13a160: Pull complete
f6fa63e71a13: Pull complete
561abb46edf5: Pull complete
aa68385e1d37: Pull complete
c77c328a9969: Pull complete
f98e23828f5f: Pull complete
6323bf269528: Pull complete
898392363b19: Pull complete
Digest: sha256:b42ece3b23559e6021757e29195090ae727c4849848b01c997ac5cbbb7c27848
Status: Downloaded newer image for wordpress:latest
Creating compose_mysql_1 ...
Creating compose_mysql_1 ... done
Creating compose_wordpress_1 ...
Creating compose_wordpress_1 ... error

ERROR: for compose_wordpress_1  Cannot start service wordpress: driver failed programming external connectivity on endpoint compose_wordpress_1 (738cc4dd43164dc1acbc19ddb09edfb6344ef1af0922cec75b4d97c4caeb76a4): Error starting userland proxy: listen tcp 0.0.0.0:80: bind: address already in use

ERROR: for wordpress  Cannot start service wordpress: driver failed programming external connectivity on endpoint compose_wordpress_1 (738cc4dd43164dc1acbc19ddb09edfb6344ef1af0922cec75b4d97c4caeb76a4): Error starting userland proxy: listen tcp 0.0.0.0:80: bind: address already in use
ERROR: Encountered errors while bringing up the project.
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose$
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose$ sudo docker-compose ps
       Name                      Command                State      Ports   
--------------------------------------------------------------------------
compose_mysql_1       docker-entrypoint.sh mysqld      Up         3306/tcp
compose_wordpress_1   docker-entrypoint.sh apach ...   Exit 128           
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose$
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose$ cat docker-compose.yml
wordpress:
  image: wordpress
  links:
   - mysql
  ports:
   - "8080:80"
  environment:
   - WORDPRESS_DB_NAME=wordpress
   - WORDPRESS_DB_USER=wordpress
   - WORDPRESS_DB_PASSWORD=wordpresspwd
mysql:
  image: mysql
  environment:
   - MYSQL_ROOT_PASSWORD=wordpressdocker
   - MYSQL_DATABASE=wordpress
   - MYSQL_USER=wordpress
   - MYSQL_PASSWORD=wordpresspwd
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose$
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose$ sudo docker-compose up -d --build
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose$ sudo docker-compose up -d
compose_mysql_1 is up-to-date
Recreating compose_wordpress_1 ...
Recreating compose_wordpress_1 ... done
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose$
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose$ sudo docker-compose ps
       Name                      Command               State          Ports         
-----------------------------------------------------------------------------------
compose_mysql_1       docker-entrypoint.sh mysqld      Up      3306/tcp             
compose_wordpress_1   docker-entrypoint.sh apach ...   Up      0.0.0.0:8080->80/tcp
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose$
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose$ sudo docker-compose stop compose_wordpress_1
ERROR: No such service: compose_wordpress_1
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose$ sudo docker-compose stop wordpress
Stopping compose_wordpress_1 ... done
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose$ sudo docker-compose ps
       Name                      Command               State     Ports   
------------------------------------------------------------------------
compose_mysql_1       docker-entrypoint.sh mysqld      Up       3306/tcp
compose_wordpress_1   docker-entrypoint.sh apach ...   Exit 0           
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose$ sudo docker-compose start wordpress
Starting wordpress ... done
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose$ sudo docker-compose ps
       Name                      Command               State          Ports         
-----------------------------------------------------------------------------------
compose_mysql_1       docker-entrypoint.sh mysqld      Up      3306/tcp             
compose_wordpress_1   docker-entrypoint.sh apach ...   Up      0.0.0.0:8080->80/tcp
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose$
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose$ cat mesos.yml
zookeeper:
  image: garland/zookeeper
  ports:
   - "2181:2181"
   - "2888:2888"
   - "3888:3888"
mesosmaster:
  image: garland/mesosphere-docker-mesos-master
  ports:
   - "5050:5050"
  links:
   - zookeeper:zk
  environment:
   - MESOS_ZK=zk://zk:2181/mesos
   - MESOS_LOG_DIR=/var/log/mesos
   - MESOS_QUORUM=1
   - MESOS_REGISTRY=in_memory
   - MESOS_WORK_DIR=/var/lib/mesos
marathon:
  image: garland/mesosphere-docker-marathon
  links:
   - zookeeper:zk
   - mesosmaster:master
  command: --master zk://zk:2181/mesos --zk zk://zk:2181/marathon
  ports:
   - "8088:8080"
mesosslave:
  image: garland/mesosphere-docker-mesos-master:latest
  ports:
   - "5051:5051"
  links:
   - zookeeper:zk
   - mesosmaster:master
  entrypoint: mesos-slave
  environment:
   - MESOS_HOSTNAME=172.17.2.15
   - MESOS_MASTER=zk://zk:2181/mesos
   - MESOS_LOG_DIR=/var/log/mesos
   - MESOS_LOGGING_LEVEL=INFO
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose$
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose$ sudo docker-compose -f mesos.yml up -d
WARNING: Found orphan containers (compose_wordpress_1, compose_mysql_1) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up.
Pulling zookeeper (garland/zookeeper:latest)...
latest: Pulling from garland/zookeeper
a3ed95caeb02: Pull complete
76e26cb603d3: Downloading [==>                                                ] 2.621 MB/51.18 MB
26e3ffd0de24: Downloading [>                                                  ]  1.08 MB/106.8 MB
5b76ae9a2c66: Download complete
fdd784be067e: Download complete
9e33799177d8: Download complete
^CERROR: Aborting.
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose$
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07$ mkdir compose-mesos
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07$ cp ./compose/mesos.yml ./compose-mesos/
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07$ cd ./compose-mesos/
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose-mesos$ ll
total 12
drwxrwxr-x  2 ubuntu ubuntu 4096 Jun 11 05:51 ./
drwxrwxr-x 11 ubuntu ubuntu 4096 Jun 11 05:51 ../
-rw-rw-r--  1 ubuntu ubuntu  894 Jun 11 05:51 mesos.yml
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose-mesos$
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose-mesos$ sudo docker-compose -f mesos.yml up -d
Pulling mesosmaster (garland/mesosphere-docker-mesos-master:latest)...
latest: Pulling from garland/mesosphere-docker-mesos-master
a3ed95caeb02: Pull complete
1e12eb217551: Pull complete
d2ff49536f4d: Pull complete
f94adccdbb9c: Pull complete
ca4998197cbe: Pull complete
91b9a729dc9a: Pull complete
15b805177f74: Pull complete
ed2466789fb0: Pull complete
bb4998055501: Pull complete
d868e403d59a: Pull complete
f67af4adf421: Pull complete
34961fac32c1: Pull complete
Digest: sha256:8f2129e6d717be68ac303925931860cb9de36c653ee1433c31022801c328d41d
Status: Downloaded newer image for garland/mesosphere-docker-mesos-master:latest
Pulling marathon (garland/mesosphere-docker-marathon:latest)...
latest: Pulling from garland/mesosphere-docker-marathon
71a21fdea81d: Pull complete
cf68a3ea6e1d: Pull complete
31cb2a4d344a: Pull complete
0341b6fcb0fe: Pull complete
c8777cc48364: Pull complete
5d65d7e933fc: Pull complete
e1dbbcfa9453: Pull complete
8a1ca45cc0c5: Pull complete
84b0b841a0d2: Pull complete
e5a5bd247cee: Pull complete
9dd8112e5e51: Pull complete
Digest: sha256:2e60059263810e42ee52de0f9ed7ec7c209ede04ae3a1efe7aaefb7d2af15be1
Status: Downloaded newer image for garland/mesosphere-docker-marathon:latest
Creating composemesos_zookeeper_1 ...
Creating composemesos_zookeeper_1 ... done
Creating composemesos_mesosmaster_1 ...
Creating composemesos_mesosmaster_1 ... done
Creating composemesos_mesosslave_1 ...
Creating composemesos_marathon_1 ...
Creating composemesos_mesosslave_1
Creating composemesos_marathon_1 ... done
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/compose-mesos$




version: "3"
services:
  #insight所有前端项目
  insight-fe:
    image: openresty:latest
    command: openresty -p /home/work/app/insight-fe/openresty/ -c /home/work/app/insight-fe/openresty/conf/nginx.conf -g "daemon off;" 
    user: root
    working_dir: /home/work
    ports:
      # insight agg2
      - "80:8080"
      # insight passport
      - "8081:8081"
      # insight backend
      - "8899:8899"
      # insight data-gate
      # - "8666:8666"
    volumes:
      - ./app:/home/work/app/
    links:
      - insight-api-gate

  #insight后端API Gate
  insight-api-gate:
    image: openresty:latest
    command: openresty -p /home/work/app/app-nginx-conf/ -c /home/work/app/app-nginx-conf/conf/nginx.conf -g "daemon off;" 
    user: root
    working_dir: /home/work
    volumes:
      - ./app:/home/work/app/
      - ./var:/home/work/var/
    links:
      - insight-auth
      - insight-backend-php
      - insight-index-web
      - insight-database

  #insight Auth
  insight-auth:
    image: openresty:latest
    command: openresty -p /home/work/app/insight-auth/ -c /home/work/app/insight-auth/conf/nginx.conf -g "daemon off;"
    user: root
    working_dir: /home/work
    volumes:
      - ./app:/home/work/app/
      - ./var:/home/work/var/
    links:
      - insight-backend-php
      - insight-database

  # insight index-web 暂时独占一个docker
  insight-index-web:
    image: openresty:latest
    command: openresty -p /home/work/app/index-web/openresty/ -c /home/work/app/index-web/openresty/conf/nginx.conf -g "daemon off;"
    user: root
    working_dir: /home/work
    ports:
      - "8626:8626"
    volumes:
      - ./app:/home/work/app/
      - ./var:/home/work/var/
    links:
      - insight-backend-php
      - insight-database

  # insight后端PHP，所有php模块均在此
  insight-backend-php:
    image: php-fpm:latest
    command: php-fpm -c /home/work/app/php-backend/php-fpm/conf/php.ini -y /home/work/app/php-backend/php-fpm/conf/php-fpm.conf -F -R
    volumes:
      - ./app:/home/work/app/
      - ./var:/home/work/var/
    links:
      - insight-database

  # 数据库mysql和redis等基础服务
  insight-database:
    image: mysql-redis:latest
    command: /usr/sbin/init 
    privileged: true
    user: root 
    working_dir: /root
    ports:
      - "8123:8123"
      - "8124:8124"
    volumes:
      - ./data:/data/


sudo docker exec -ti 28bc378e8b96 bash




Docker Swarm

Docker swarm v1
ubuntu@huzhi-ubuntu3:~/docker$ sudo docker pull swarm
Using default tag: latest
latest: Pulling from library/swarm
ebe0176dcf9a: Pull complete
19f771faa982: Pull complete
902eeedf931a: Pull complete
Digest: sha256:815fc8fd4617d866e1256999c2c0a55cc8f377f3dade26c3edde3f0543a70c04
Status: Downloaded newer image for swarm:latest
ubuntu@huzhi-ubuntu3:~/docker$ sudo docker images
REPOSITORY                               TAG                 IMAGE ID            CREATED             SIZE
huzhi/ubuntu                             latest              295a670d7efa        25 hours ago        162 MB
wordpress                                latest              c8fc64de4cb3        2 days ago          406 MB
huzhi/sinatra_redis                      latest              517bd2ed6f60        4 weeks ago         384 MB
huzhi/sinatra                            latest              9430f31cd6f8        4 weeks ago         384 MB
huzhi/redis                              latest              812e2258613c        4 weeks ago         157 MB
mysql                                    latest              e799c7f9ae9c        4 weeks ago         407 MB
huzhi/nginx                              latest              8d808aefc701        4 weeks ago         212 MB
ubuntu                                   latest              f7b3f317ec73        6 weeks ago         117 MB
swarm                                    latest              36b1e23becab        4 months ago        15.9 MB
garland/mesosphere-docker-marathon       latest              590d18fc2dae        8 months ago        856 MB
garland/zookeeper                        latest              4af3d43d75b0        2 years ago         379 MB
garland/mesosphere-docker-mesos-master   latest              a237b70056b9        2 years ago         637 MB
ubuntu@huzhi-ubuntu3:~/docker$
ubuntu@huzhi-ubuntu3:~/docker$ sudo docker run --rm swarm -v
swarm version 1.2.6 (`git rev-parse --short HEAD`)
ubuntu@huzhi-ubuntu3:~/docker$
ubuntu@huzhi-ubuntu3:~/docker$ sudo docker run swarm help
Usage: swarm [OPTIONS] COMMAND [arg...]

A Docker-native clustering system

Version: 1.2.6 (`git rev-parse --short HEAD`)

Options:
  --debug            debug mode [$DEBUG]
  --log-level, -l "info"    Log level (options: debug, info, warn, error, fatal, panic)
  --experimental        enable experimental features
  --help, -h            show help
  --version, -v            print the version

Commands:
  create, c    Create a cluster
  list, l    List nodes in a cluster
  manage, m    Manage a docker cluster
  join, j    Join a docker cluster
  help        Shows a list of commands or help for one command

Run 'swarm COMMAND --help' for more information on a command.

ubuntu@huzhi-ubuntu3:~/docker$
ubuntu@huzhi-ubuntu3:~/docker$ sudo docker run swarm create --help
Usage: swarm create

Create a cluster
ubuntu@huzhi-ubuntu3:~/docker$
ubuntu@huzhi-ubuntu3:~/docker$ sudo docker run swarm list --help
Usage: swarm list [OPTIONS] <discovery>

List nodes in a cluster

Arguments:
   <discovery>    discovery service to use [$SWARM_DISCOVERY]
                   * token://<token>
                   * consul://<ip>/<path>
                   * etcd://<ip1>,<ip2>/<path>
                   * file://path/to/file
                   * zk://<ip1>,<ip2>/<path>
                   * [nodes://]<ip1>,<ip2>

Options:
   --timeout "10s"                            timeout period
   --discovery-opt [--discovery-opt option --discovery-opt option]    discovery options

ubuntu@huzhi-ubuntu3:~/docker$
ubuntu@huzhi-ubuntu3:~/docker$ sudo docker run swarm manage --help
Usage: swarm manage [OPTIONS] <discovery>

Manage a docker cluster

Arguments:
   <discovery>    discovery service to use [$SWARM_DISCOVERY]
                   * token://<token>
                   * consul://<ip>/<path>
                   * etcd://<ip1>,<ip2>/<path>
                   * file://path/to/file
                   * zk://<ip1>,<ip2>/<path>
                   * [nodes://]<ip1>,<ip2>

Options:
   --strategy "spread"                            placement strategy to use [spread, binpack, random]
   --filter, -f [--filter option --filter option]            filter to use [health, port, containerslots, dependency, affinity, constraint, whitelist]
   --host, -H [--host option --host option]                ip/socket to listen on [$SWARM_HOST]
   --replication                            Enable Swarm manager replication
   --replication-ttl "20s"                        Leader lock release time on failure
   --advertise, --addr                             Address of the swarm manager joining the cluster. Other swarm manager(s) MUST be able to reach the swarm manager at this address. [$SWARM_ADVERTISE]
   --tls                                use TLS; implied by --tlsverify=true
   --tlscacert                                 trust only remotes providing a certificate signed by the CA given here
   --tlscert                                 path to TLS certificate file
   --tlskey                                 path to TLS key file
   --tlsverify                                use TLS and verify the remote
   --engine-refresh-min-interval "30s"                    set engine refresh minimum interval
   --engine-refresh-max-interval "60s"                    set engine refresh maximum interval
   --engine-failure-retry "3"                        set engine failure retry count
   --engine-refresh-retry "3"                        deprecated; replaced by --engine-failure-retry
   --heartbeat "60s"                            period between each heartbeat
   --api-enable-cors, --cors                        enable CORS headers in the remote API
   --cluster-driver, -c "swarm"                        cluster driver to use [swarm, mesos-experimental]
   --discovery-opt [--discovery-opt option --discovery-opt option]    discovery options
   --cluster-opt [--cluster-opt option --cluster-opt option]        cluster driver options
   --refresh-on-node-filter                        If true, refresh the cache when a ContainerList call comes in with a node filter
   --container-name-refresh-filter                     If set, refresh the cache when a ContainerList call comes in with a name filter set to this value
                                        * swarm.overcommit=0.05        overcommit to apply on resources
                                                         * swarm.createretry=0            container create retry count after initial failure
                                                         * mesos.address=            address to bind on [$SWARM_MESOS_ADDRESS]
                                                         * mesos.checkpointfailover=false    checkpointing allows a restarted slave to reconnect with old executors and recover status updates, at the cost of disk I/O [$SWARM_MESOS_CHECKPOINT_FAILOVER]
                                                         * mesos.port=                port to bind on [$SWARM_MESOS_PORT]
                                                         * mesos.offertimeout=30s        timeout for offers [$SWARM_MESOS_OFFER_TIMEOUT]
                                                         * mesos.offerrefusetimeout=5s        seconds to consider unused resources refused [$SWARM_MESOS_OFFER_REFUSE_TIMEOUT]
                                                         * mesos.tasktimeout=5s            timeout for task creation [$SWARM_MESOS_TASK_TIMEOUT]
                                                         * mesos.user=                framework user [$SWARM_MESOS_USER]
ubuntu@huzhi-ubuntu3:~/docker$
ubuntu@huzhi-ubuntu3:~/docker$ sudo docker run swarm join --help
Usage: swarm join [OPTIONS] <discovery>

Join a docker cluster

Arguments:
   <discovery>    discovery service to use [$SWARM_DISCOVERY]
                   * token://<token>
                   * consul://<ip>/<path>
                   * etcd://<ip1>,<ip2>/<path>
                   * file://path/to/file
                   * zk://<ip1>,<ip2>/<path>
                   * [nodes://]<ip1>,<ip2>

Options:
   --advertise, --addr                             Address of the Docker Engine joining the cluster. Swarm manager(s) MUST be able to reach the Docker Engine at this address. [$SWARM_ADVERTISE]
   --heartbeat "60s"                            period between each heartbeat
   --ttl "180s"                                set the expiration of an ephemeral node
   --delay "0s"                                add a random delay in [0s,delay] to avoid synchronized registration
   --discovery-opt [--discovery-opt option --discovery-opt option]    discovery options

ubuntu@huzhi-ubuntu3:~/docker$

Docker swarm v2
ubuntu@huzhi-ubuntu3:~/docker$ sudo docker swarm --help

Usage:    docker swarm COMMAND

Manage Swarm

Options:
      --help   Print usage

Commands:
  init        Initialize a swarm
  join        Join a swarm as a node and/or manager
  join-token  Manage join tokens
  leave       Leave the swarm
  unlock      Unlock swarm
  unlock-key  Manage the unlock key
  update      Update the swarm

Run 'docker swarm COMMAND --help' for more information on a command.
ubuntu@huzhi-ubuntu3:~/docker$




ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/swarm$ cat README.md
Recipe for Docker Swarm
=======================

This starts a Vagrant cluster with a head node `swarm-head` and three compute nodes `swarm-{1-3}`

    $ vagrant up

The compute node install the latest version of docker and listen on the 0.0.0.0 interface for remote API access.
See the `docker-bootstrap.sh` script.
The head node installs the default ubuntu14.04 Docker, clones the swarm project and build a swarm image, see `swarm-bootstrap.sh`

    $ git clone https://github.com/docker/swarm.git
    $ cd swarm/
    $ docker build -t swarm .

When the cluster is up, ssh to the head node

    $ vagrant ssh swarm-head

Start a swarm container in background, mounting the `/vagrant` directory and exposing a port where you are going to run the swarm server.

    $ docker run -v /vagrant/:/tmp/vagrant -p 1234:1234 -d swarm manage --discovery file:///tmp/vagrant/swarm-cluster.cfg -H=0.0.0.0:1234

Mounting the /vagrant directory allows to share the `swarm-cluster.cfg` file, which is a hardcoded list of the compute nodes.
This is far from ideal, but the easiest discovery mechanism.

You are then ready to go with swarm:

    $ docker -H 172.17.42.1:1234 info
    Containers: 0
    Images: 0
    Storage Driver:
    Nodes: 3
     swarm-2: http://192.168.33.12:2375
     swarm-1: http://192.168.33.11:2375
     swarm-3: http://192.168.33.13:2375
    Execution Driver:
    Kernel Version:
    WARNING: No memory limit support
    WARNING: No swap limit support
    WARNING: IPv4 forwarding is disabled.
    $ docker -H 172.17.42.1:1234 ps
    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
    $ docker -H 172.17.42.1:1234 run -d -p 80:80 nginx
    9bbb4950cec9d0a696e00949e536b0c79e7cf688d604043662e82f11a5ad336e
    $ docker -H 172.17.42.1:1234 ps
    CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS                  PORTS                                   NAMES
    9bbb4950cec9        nginx:1             nginx -g 'daemon off   10 seconds ago      Up Less than a second   443/tcp, 192.168.33.13:80->80/tcp   swarm-3/prickly_poincare   
    $ docker -H 172.17.42.1:1234 run -d -p 80:80 nginx
    95d0f755d09490e0fbeab4819ba9d87ce654528cdc20f1723d601760137940de
    $ docker -H 172.17.42.1:1234 ps
    CONTAINER ID        IMAGE               COMMAND                CREATED                  STATUS                  PORTS                               NAMES
    95d0f755d094        nginx:1             nginx -g 'daemon off   Less than a second ago   Up Less than a second   443/tcp,   192.168.33.12:80->80/tcp   swarm-2/backstabbing_davinci   
    9bbb4950cec9        nginx:1             nginx -g 'daemon off   5 minutes ago            Up 5 minutes            443/tcp,   192.168.33.13:80->80/tcp   swarm-3/prickly_poincare       
    $ docker ps
    CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS              PORTS                              NAMES
    72acd5bc00de        swarm:latest        swarm manage --disco   12 minutes ago      Up 12 minutes       2375/tcp, 0.0.0.0:1234->1234/tcp   silly_brown         
    $ docker logs 72acd5bc00de
    time="2015-01-07T08:49:53Z" level=info msg="Listening for HTTP on tcp (0.0.0.0:1234)"
    time="2015-01-07T08:50:29Z" level=info msg="GET /v1.12/info"
    time="2015-01-07T08:50:35Z" level=info msg="GET /v1.12/containers/json"
    time="2015-01-07T08:51:30Z" level=info msg="POST /v1.12/containers/create"
    time="2015-01-07T08:56:09Z" level=info msg="event -> status: \"pull\" from: \"\" id: \"nginx\" node: \"swarm-3\""
    time="2015-01-07T08:56:09Z" level=info msg="event -> status: \"create\" from: \"nginx:1\" id:   \"9bbb4950cec9d0a696e00949e536b0c79e7cf688d604043662e82f11a5ad336e\" node: \"swarm-3\""
    time="2015-01-07T08:56:09Z" level=info msg="POST   /v1.12/containers/9bbb4950cec9d0a696e00949e536b0c79e7cf688d604043662e82f11a5ad336e/start"
    time="2015-01-07T08:56:10Z" level=info msg="event -> status: \"start\" from: \"nginx:1\" id: \"9bbb4950cec9d0a696e00949e536b0c79e7cf688d604043662e82f11a5ad336e\" node: \"swarm-3\""
    time="2015-01-07T08:56:19Z" level=info msg="GET /v1.12/containers/json"
    time="2015-01-07T08:56:31Z" level=info msg="POST /v1.12/containers/create"
    time="2015-01-07T09:01:36Z" level=info msg="event -> status: \"pull\" from: \"\" id: \"nginx\" node: \"swarm-2\""
    time="2015-01-07T09:01:36Z" level=info msg="event -> status: \"create\" from: \"nginx:1\" id: \"95d0f755d09490e0fbeab4819ba9d87ce654528cdc20f1723d601760137940de\" node: \"swarm-2\""
    time="2015-01-07T09:01:36Z" level=info msg="POST /v1.12/containers/95d0f755d09490e0fbeab4819ba9d87ce654528cdc20f1723d601760137940de/start"
    time="2015-01-07T09:01:37Z" level=info msg="event -> status: \"start\" from: \"nginx:1\" id: \"95d0f755d09490e0fbeab4819ba9d87ce654528cdc20f1723d601760137940de\" node: \"swarm-2\""
    time="2015-01-07T09:01:42Z" level=info msg="GET /v1.12/containers/json"ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/swarm$
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/swarm$
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/swarm$
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/swarm$ cat swarm-cluster.cfg
192.168.33.11:2375
192.168.33.12:2375
192.168.33.13:2375
ubuntu@huzhi-ubuntu3:~/docker/docbook/ch07/swarm$





Docker Machine

ubuntu@huzhi-ubuntu3:~/docker$ curl -L https://github.com/docker/machine/releases/download/v0.10.0/docker-machine-`uname -s`-`uname -m` >/tmp/docker-machine && chmod +x /tmp/docker-machine && sudo cp /tmp/docker-machine /usr/local/bin/docker-machine
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   617    0   617    0     0    692      0 --:--:-- --:--:-- --:--:--   691
100 24.1M  100 24.1M    0     0   371k      0  0:01:06  0:01:06 --:--:--  441k
ubuntu@huzhi-ubuntu3:~/docker$
ubuntu@huzhi-ubuntu3:~/docker$ docker-machine --help
Usage: docker-machine [OPTIONS] COMMAND [arg...]

Create and manage machines running Docker.

Version: 0.10.0, build 76ed2a6

Author:
  Docker Machine Contributors - <https://github.com/docker/machine>

Options:
  --debug, -D                        Enable debug mode
  --storage-path, -s "/home/ubuntu/.docker/machine"    Configures storage path [$MACHINE_STORAGE_PATH]
  --tls-ca-cert                     CA to verify remotes against [$MACHINE_TLS_CA_CERT]
  --tls-ca-key                         Private key to generate certificates [$MACHINE_TLS_CA_KEY]
  --tls-client-cert                     Client cert to use for TLS [$MACHINE_TLS_CLIENT_CERT]
  --tls-client-key                     Private key used in client TLS auth [$MACHINE_TLS_CLIENT_KEY]
  --github-api-token                     Token to use for requests to the Github API [$MACHINE_GITHUB_API_TOKEN]
  --native-ssh                        Use the native (Go-based) SSH implementation. [$MACHINE_NATIVE_SSH]
  --bugsnag-api-token                     BugSnag API token for crash reporting [$MACHINE_BUGSNAG_API_TOKEN]
  --help, -h                        show help
  --version, -v                        print the version

Commands:
  active        Print which machine is active
  config        Print the connection config for machine
  create        Create a machine
  env            Display the commands to set up the environment for the Docker client
  inspect        Inspect information about a machine
  ip            Get the IP address of a machine
  kill            Kill a machine
  ls            List machines
  provision        Re-provision existing machines
  regenerate-certs    Regenerate TLS Certificates for a machine
  restart        Restart a machine
  rm            Remove a machine
  ssh            Log into or run a command on a machine with SSH.
  scp            Copy files between machines
  start            Start a machine
  status        Get the status of a machine
  stop            Stop a machine
  upgrade        Upgrade a machine to the latest version of Docker
  url            Get the URL of a machine
  version        Show the Docker Machine version or a machine docker version
  help            Shows a list of commands or help for one command

Run 'docker-machine COMMAND --help' for more information on a command.
ubuntu@huzhi-ubuntu3:~/docker$





ubuntu@huzhi-ubuntu3:~/docker$ ll
total 16
drwxrwxr-x  4 ubuntu ubuntu 4096 Jun  2 00:15 ./
drwxr-xr-x 27 ubuntu ubuntu 4096 Jun 11 06:51 ../
drwxrwxr-x 14 ubuntu ubuntu 4096 Jun  2 00:15 docbook/
drwxrwxr-x  4 ubuntu ubuntu 4096 May  9 09:13 dockerbook-code/
ubuntu@huzhi-ubuntu3:~/docker$ sudo docker ps -a
CONTAINER ID        IMAGE                                           COMMAND                  CREATED             STATUS                           PORTS               NAMES
2ed42358ca1e        garland/mesosphere-docker-marathon              "/opt/marathon/bin..."   19 hours ago        Exited (137) 3 minutes ago                           composemesos_marathon_1
769a5b4e4cfb        garland/mesosphere-docker-mesos-master:latest   "mesos-slave"            19 hours ago        Exited (137) 3 minutes ago                           composemesos_mesosslave_1
a96124e167d4        garland/mesosphere-docker-mesos-master          "mesos-master"           19 hours ago        Exited (137) 2 minutes ago                           composemesos_mesosmaster_1
f53793f611f1        garland/zookeeper                               "/opt/run.sh"            19 hours ago        Exited (137) 2 minutes ago                           composemesos_zookeeper_1
ced902c1f11f        huzhi/ubuntu                                    "bash"                   22 hours ago        Exited (127) About an hour ago                       cookbook
ubuntu@huzhi-ubuntu3:~/docker$ sudo docker images
REPOSITORY                               TAG                 IMAGE ID            CREATED             SIZE
huzhi/ubuntu                             latest              295a670d7efa        23 hours ago        162 MB
wordpress                                latest              c8fc64de4cb3        2 days ago          406 MB
huzhi/sinatra_redis                      latest              517bd2ed6f60        4 weeks ago         384 MB
huzhi/sinatra                            latest              9430f31cd6f8        4 weeks ago         384 MB
huzhi/redis                              latest              812e2258613c        4 weeks ago         157 MB
mysql                                    latest              e799c7f9ae9c        4 weeks ago         407 MB
huzhi/nginx                              latest              8d808aefc701        4 weeks ago         212 MB
ubuntu                                   latest              f7b3f317ec73        6 weeks ago         117 MB
garland/mesosphere-docker-marathon       latest              590d18fc2dae        8 months ago        856 MB
garland/zookeeper                        latest              4af3d43d75b0        2 years ago         379 MB
garland/mesosphere-docker-mesos-master   latest              a237b70056b9        2 years ago         637 MB
ubuntu@huzhi-ubuntu3:~/docker$ sudo docker save -o ./huzhi_ubuntu.tar huzhi/ubuntu
ubuntu@huzhi-ubuntu3:~/docker$ ll
total 162388
drwxrwxr-x  4 ubuntu ubuntu      4096 Jun 12 04:44 ./
drwxr-xr-x 27 ubuntu ubuntu      4096 Jun 11 06:51 ../
drwxrwxr-x 14 ubuntu ubuntu      4096 Jun  2 00:15 docbook/
drwxrwxr-x  4 ubuntu ubuntu      4096 May  9 09:13 dockerbook-code/
-rw-------  1 root   root   166268416 Jun 12 04:44 huzhi_ubuntu.tar
ubuntu@huzhi-ubuntu3:~/docker$
ubuntu@huzhi-ubuntu3:~/docker$ sudo docker load --help

Usage:    docker load [OPTIONS]

Load an image from a tar archive or STDIN

Options:
      --help           Print usage
  -i, --input string   Read from tar archive file, instead of STDIN
  -q, --quiet          Suppress the load output
ubuntu@huzhi-ubuntu3:~/docker$
ubuntu@huzhi-ubuntu3:~/docker$ ll
total 162388
drwxrwxr-x  4 ubuntu ubuntu      4096 Jun 12 04:44 ./
drwxr-xr-x 27 ubuntu ubuntu      4096 Jun 11 06:51 ../
drwxrwxr-x 14 ubuntu ubuntu      4096 Jun  2 00:15 docbook/
drwxrwxr-x  4 ubuntu ubuntu      4096 May  9 09:13 dockerbook-code/
-rw-------  1 root   root   166268416 Jun 12 04:44 huzhi_ubuntu.tar
ubuntu@huzhi-ubuntu3:~/docker$ sudo docker load -i ./huzhi_ubuntu.tar

docker load < ./huzhi_ubuntu.tar 






docker如何有效的压缩镜像体积

https://wiki.avlyun.org/pages/viewpage.action?pageId=29037994


# Version: 0.0.1
FROM centos/centos7-base:latest
MAINTAINER mango "wangyazhe@antiy.cn"
USER root

# yum install ; pip install
RUN mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
ADD centos7.repo /etc/yum.repos.d/CentOS-Base.repo
# RUN yum makecache
# RUN yum -y update;yum -y clean all
RUN yum -y install python-devel python-setuptools vim wget zip unzip net-tools openssh-server openssh-clients ntp; yum -y clean all
RUN easy_install pip
RUN pip install supervisor kombu requests boto --no-cache-dir

# ssh set
RUN ssh-keygen -q -N "" -t dsa -f /etc/ssh/ssh_host_dsa_key
RUN ssh-keygen -q -N "" -t rsa -f /etc/ssh/ssh_host_rsa_key
RUN ssh-keygen -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key -N ""
RUN sed -ri 's/session    required     pam_loginuid.so/#session    required     pam_loginuid.so/g' /etc/pam.d/sshd
RUN mkdir -p /root/.ssh && chown root.root /root && chmod 700 /root/.ssh
RUN echo 'root:123456' | chpasswd

# dir set
RUN mkdir -p /var/log/supervisor
RUN mkdir -p /var/tmp
RUN mkdir -p /opt/fastdfs/storage
RUN mkdir -p /opt/pipboy/src


# file set
ADD docker.tar.gz /opt/pipboy/src/
ADD avlm_test.tar.gz /opt/pipboy/src/
ADD supervisord.conf /etc/supervisord.conf

# port set
EXPOSE 22

# cmd set
CMD ["/bin/bash"]




docker run -i -t --dns=127.0.0.1 -p 9527:9527 -v /opt/outside_adfsindex:/opt/inside_adfsindex docker.avlyun.org/platform/adfs_index /bin/bash
(注意，此处使用了--dns参数来指定使用容器本地的dnsmasq（vi /etc/dnsmasq.hosts  service dnsmasq restart）进行dns解析，如果你有其他的dns服务器，也需要添加到此处)
按ctrl+p ctrl+q的组合键将容器置于后台运行








ubuntu@huzhi-ubuntu3:~$ sudo docker network help

Usage:    docker network COMMAND

Manage networks

Options:
      --help   Print usage

Commands:
  connect     Connect a container to a network
  create      Create a network
  disconnect  Disconnect a container from a network
  inspect     Display detailed information on one or more networks
  ls          List networks
  prune       Remove all unused networks
  rm          Remove one or more networks

Run 'docker network COMMAND --help' for more information on a command.
ubuntu@huzhi-ubuntu3:~$
ubuntu@huzhi-ubuntu3:~$ sudo docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
59edb9c72659        bridge              bridge              local
cb1832ef47ac        host                host                local
323c4c57ff05        none                null                local
ubuntu@huzhi-ubuntu3:~$ sudo docker network inspect bridge
[
    {
        "Name": "bridge",
        "Id": "59edb9c72659657b7a229c63cff932ffdd8a3433e853d5b7abdb4bf4e44c26e1",
        "Created": "2017-05-08T05:54:40.22355065Z",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "172.18.0.0/16"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Containers": {},
        "Options": {
            "com.docker.network.bridge.default_bridge": "true",
            "com.docker.network.bridge.enable_icc": "true",
            "com.docker.network.bridge.enable_ip_masquerade": "true",
            "com.docker.network.bridge.host_binding_ipv4": "0.0.0.0",
            "com.docker.network.bridge.name": "docker0",
            "com.docker.network.driver.mtu": "1500"
        },
        "Labels": {}
    }
]
ubuntu@huzhi-ubuntu3:~$ sudo docker network inspect host
[
    {
        "Name": "host",
        "Id": "cb1832ef47ac663cc4fb6bc9f5fa6877af42b57129fc4ae605c8d1c888fac97d",
        "Created": "2017-05-08T05:54:40.200145247Z",
        "Scope": "local",
        "Driver": "host",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": []
        },
        "Internal": false,
        "Attachable": false,
        "Containers": {},
        "Options": {},
        "Labels": {}
    }
]
ubuntu@huzhi-ubuntu3:~$ sudo docker network inspect none
[
    {
        "Name": "none",
        "Id": "323c4c57ff054e7f4c5c924e6c313e49cbc27cd5bbe1683eb6cec52dc5416a2a",
        "Created": "2017-05-08T05:54:40.136550113Z",
        "Scope": "local",
        "Driver": "null",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": []
        },
        "Internal": false,
        "Attachable": false,
        "Containers": {},
        "Options": {},
        "Labels": {}
    }
]
ubuntu@huzhi-ubuntu3:~$ sudo docker network create my-network
f8ce1145b3e2d19ba8f9bb472a80b26ac3dd914563e5e2e3fad08dcbd8d6b384
ubuntu@huzhi-ubuntu3:~$ sudo docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
59edb9c72659        bridge              bridge              local
cb1832ef47ac        host                host                local
f8ce1145b3e2        my-network          bridge              local
323c4c57ff05        none                null                local
ubuntu@huzhi-ubuntu3:~$ sudo docker network inspect my-network
[
    {
        "Name": "my-network",
        "Id": "f8ce1145b3e2d19ba8f9bb472a80b26ac3dd914563e5e2e3fad08dcbd8d6b384",
        "Created": "2017-07-22T06:13:16.458178715Z",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "172.19.0.0/16",
                    "Gateway": "172.19.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Containers": {},
        "Options": {},
        "Labels": {}
    }
]
ubuntu@huzhi-ubuntu3:~$


ubuntu@huzhi-ubuntu3:~$ sudo docker run -d --name mysql-server --network my-network -e MYSQL_ROOT_PASSWORD=secret mysql
ubuntu@huzhi-ubuntu3:~$ sudo docker run -it --rm --network my-network mysql sh -c 'exec mysql -h"mysql-server" -P"3306" -uroot -p"secret"'
--rm，容器退出后自动删除
--network，指定需要连接的网络

ubuntu@huzhi-ubuntu3:~$ sudo docker network rm my-network
my-network
ubuntu@huzhi-ubuntu3:~$ sudo docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
59edb9c72659        bridge              bridge              local
cb1832ef47ac        host                host                local
323c4c57ff05        none                null                local
ubuntu@huzhi-ubuntu3:~$






swarm mode


SwarmKit



[root@server-1116 ~]# virsh list
 Id    Name                           State
----------------------------------------------------
 51    swarm-01                       running
 52    swarm-02                       running
 53    swarm-03                       running
 54    swarm-04                       running
 55    swarm-05                       running

[root@server-1116 ~]#


root
swarm!@#$%^


ifup eth0

ip address

vi /etc/sysconfig/network-scripts/ifcfg-eth0

service firewalld status

service firewalld stop

curl -o /etc/yum.repos.d/CentOS-Aliyun.repo http://mirrors.aliyun.com/repo/Centos-7.repo

yum makecache

yum install -y ntpdate wget vim net-tools unzip zip

timedatectl

timedatectl set-timezone Asia/Shanghai

ntpdate ntp1.aliyun.com ntp2.aliyun.com ntp3.aliyun.com ntp4.aliyun.com

date

sudo yum install -y yum-utils device-mapper-persistent-data lvm2

sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

sudo yum makecache fast

sudo yum install -y docker-ce

systemctl daemon-reload

systemctl enable docker.service

systemctl start docker.service

systemctl status docker.service

docker info

curl -L https://github.com/docker/compose/releases/download/1.15.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose

chmod +x /usr/local/bin/docker-compose

/usr/local/bin/docker-compose --version
docker-compose --version

ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/sbin/docker-compose
hostname
real_ip
role
port
swarm-01
10.128.128.110
manager节点
192.168.10.234:9001
swarm-02
10.128.128.158
worker节点
192.168.10.234:9002
swarm-03
10.128.128.238
worker节点
192.168.10.234:9003
swarm-04
10.128.128.226
worker节点
192.168.10.234:9004
swarm-05
10.128.128.213
worker节点
192.168.10.234:9005


hostnamectl set-hostname swarm-01
hostnamectl set-hostname swarm-02
hostnamectl set-hostname swarm-03
hostnamectl set-hostname swarm-04
hostnamectl set-hostname swarm-05

hostnamectl


vim /etc/hosts
10.128.128.110  swarm-01
10.128.128.158  swarm-02
10.128.128.238  swarm-03
10.128.128.226  swarm-04
10.128.128.213  swarm-05




manager节点

[root@localhost ~]# docker swarm init --advertise-addr 10.128.128.110
Swarm initialized: current node (2s6b4q4j9fi80bdu0sek2l8xj) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join --token SWMTKN-1-00r7shqn93w0o8wjs613tmfjym3x5k634jv3zryhljvo4yapct-4wonogbaovtgaezwn7la8aq3k 10.128.128.110:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.

[root@localhost ~]#
[root@localhost ~]# docker swarm join-token worker
To add a worker to this swarm, run the following command:

    docker swarm join --token SWMTKN-1-00r7shqn93w0o8wjs613tmfjym3x5k634jv3zryhljvo4yapct-4wonogbaovtgaezwn7la8aq3k 10.128.128.110:2377

[root@localhost ~]#
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
[root@localhost ~]# docker node ls
ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS
2s6b4q4j9fi80bdu0sek2l8xj *   swarm-01            Ready               Active              Leader
###################################################################################################################################
[root@localhost ~]#
[root@localhost ~]# docker node ls
ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS
2s6b4q4j9fi80bdu0sek2l8xj *   swarm-01            Ready               Active              Leader
3w3014he63242togyeyb35k1w     swarm-02            Ready               Active             
fivl9s8cvlrweptjjacu8zqv8     swarm-04            Ready               Active             
jqher5t38yyir31it3b6dxfry     swarm-05            Ready               Active             
pzuezfs7ykegw0dvslpznwssa     swarm-03            Ready               Active             
[root@localhost ~]#
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
[root@localhost ~]# docker service ps helloworld
ID                  NAME                IMAGE               NODE                    DESIRED STATE       CURRENT STATE           ERROR               PORTS
v78a07w97t0q        helloworld.1        alpine:latest       localhost.localdomain   Running             Running 2 minutes ago                       
[root@localhost ~]#
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




worker节点

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



[root@rms-test ~]# cat /etc/sysconfig/docker
OPTIONS='--selinux-enabled --log-driver=journald --insecure-registry docker-registry.innovation.os'
[root@rms-test ~]#
[root@rms-test ~]# systemctl restart docker.service
[root@rms-test ~]# systemctl status docker.service




[root@localhost ~]# docker login -u huzhi -p huzhi567233 registry.aspider.avlyun.org
Login Succeeded
[root@localhost ~]#
[root@localhost ~]# docker pull registry.aspider.avlyun.org/library/centos7
Using default tag: latest
latest: Pulling from library/centos7
d9aaf4d82f24: Pull complete
bcfccc23d085: Pull complete
d1b0237361d1: Pull complete
002d156b7065: Pull complete
Digest: sha256:c6f18a26e1886b56954c48734e1ec95af9f7ac99c284cf3457fed9b95263e3da
Status: Downloaded newer image for registry.aspider.avlyun.org/library/centos7:latest
You have mail in /var/spool/mail/root
[root@localhost ~]#
[root@localhost ~]# docker images
REPOSITORY                                    TAG                 IMAGE ID            CREATED             SIZE
registry.aspider.avlyun.org/library/centos7   latest              3b176d01caf2        6 weeks ago         205MB
[root@localhost ~]#

