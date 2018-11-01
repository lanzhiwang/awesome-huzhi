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

### Docker Machine

```bash
$ curl -L https://github.com/docker/machine/releases/download/v0.10.0/docker-machine-`uname -s`-`uname -m` >/tmp/docker-machine && chmod +x /tmp/docker-machine && sudo cp /tmp/docker-machine /usr/local/bin/docker-machine
$
$ docker-machine --help
```

### 打包解包镜像
```bash
$ sudo docker save -o ./huzhi_ubuntu.tar huzhi/ubuntu
$ sudo docker load -i ./huzhi_ubuntu.tar
docker load < ./huzhi_ubuntu.tar 
```

### 登陆私有镜像库
```bash
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
[root@localhost ~]# docker logout
```

### 资源限制



### 进入容器

```bash
docker attach
docker exec -ti <container name> /bin/bash
```



### 查看容器状态

```bash
docker ps
docker top
docker stats
```

