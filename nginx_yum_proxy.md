## 使用 nginx 作为 yum 代理

```bash
## step 1 : 配置 nginx 作为代理服务器
server {
    listen 80;
    location / {
        proxy_pass http://mirrors.aliyun.com/;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-for $proxy_add_x_forwarded_for;
        proxy_set_header Host mirrors.aliyun.com;
        proxy_set_header X-Forwarded-Proto $remote_addr;
        proxy_connect_timeout 600;
        proxy_read_timeout 600;
        proxy_send_timeout 600;
        client_max_body_size 1024M;
    }
}

## step 2 : 修改 yum repo 配置文件
# CentOS-Base.repo
#
# The mirror system uses the connecting IP address of the client and the
# update status of each mirror to pick mirrors that are updated to and
# geographically close to the client.  You should use this for CentOS updates
# unless you are manually picking other mirrors.
#
# If the mirrorlist= does not work for you, as a fall back you can try the
# remarked out baseurl= line instead.
#
#

[base]
name=CentOS-$releasever - Base - 10.128.127.214
failovermethod=priority
baseurl=http://10.128.127.214/centos/$releasever/os/$basearch/
#mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=os
#gpgcheck=1
#gpgkey=http://10.128.127.214/centos/RPM-GPG-KEY-CentOS-7

#released updates
[updates]
name=CentOS-$releasever - Updates - 10.128.127.214
failovermethod=priority
baseurl=http://10.128.127.214/centos/$releasever/updates/$basearch/
#mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=updates
#gpgcheck=1
#gpgkey=http://10.128.127.214/centos/RPM-GPG-KEY-CentOS-7

#additional packages that may be useful
[extras]
name=CentOS-$releasever - Extras - 10.128.127.214
failovermethod=priority
baseurl=http://10.128.127.214/centos/$releasever/extras/$basearch/
#mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=extras
#gpgcheck=1
#gpgkey=http://10.128.127.214/centos/RPM-GPG-KEY-CentOS-7

#additional packages that extend functionality of existing packages
[centosplus]
name=CentOS-$releasever - Plus - 10.128.127.214
failovermethod=priority
baseurl=http://10.128.127.214/centos/$releasever/centosplus/$basearch/
#mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=centosplus
#gpgcheck=1
enabled=0
#gpgkey=http://10.128.127.214/centos/RPM-GPG-KEY-CentOS-7

#contrib - packages by Centos Users
[contrib]
name=CentOS-$releasever - Contrib - 10.128.127.214
failovermethod=priority
baseurl=http://10.128.127.214/centos/$releasever/contrib/$basearch/
#mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=contrib
#gpgcheck=1
enabled=0
#gpgkey=http://10.128.127.214/centos/RPM-GPG-KEY-CentOS-7
```

