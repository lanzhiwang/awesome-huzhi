## Generate self-signed certificates 生成自签名证书

If you build Container Linux cluster on top of public networks it is recommended to enable encryption for Container Linux services to prevent traffic interception and man-in-the-middle attacks. For these purposes you have to use Certificate Authority (CA), private keys and certificates signed by CA. Let's use cfssl and walk through the whole process to create all these components.  如果在公共网络上构建Container Linux集群，建议为Container Linux服务启用加密，以防止流量拦截和中间人攻击。 出于这些目的，您必须使用由CA签名的证书颁发机构（CA），私钥和证书。 让我们使用cfssl并遍历整个过程来创建所有这些组件。

NOTE: We will use basic procedure here. If your configuration requires advanced security options, please refer to official cfssl documentation.  注意：我们将在此处使用基本程序。 如果您的配置需要高级安全选项，请参阅官方cfssl文档。

### Download cfssl

CloudFlare's distributes cfssl source code on github page and binaries on cfssl website.  CloudFlare在cfssl网站上的github页面和二进制文件上分发cfssl源代码。

Our documentation assumes that you will run cfssl on your local x86_64 Linux host.  我们的文档假定您将在本地x86_64 Linux主机上运行cfssl。

```bash
mkdir ~/bin
curl -s -L -o ~/bin/cfssl https://pkg.cfssl.org/R1.2/cfssl_linux-amd64
curl -s -L -o ~/bin/cfssljson https://pkg.cfssl.org/R1.2/cfssljson_linux-amd64
chmod +x ~/bin/{cfssl,cfssljson}
export PATH=$PATH:~/bin
```

### Initialize a certificate authority  初始化证书颁发机构

First of all we have to save default cfssl options for future substitutions:  首先，我们必须为将来的替换保存默认的cfssl选项：

```bash
mkdir ~/cfssl
cd ~/cfssl
cfssl print-defaults config > ca-config.json
cfssl print-defaults csr > ca-csr.json
ll
total 16
drwxrwxr-x  2 lanzhiwang lanzhiwang 4096 3月  26 11:26 ./
drwxr-xr-x 28 lanzhiwang lanzhiwang 4096 3月  26 11:26 ../
-rw-rw-r--  1 lanzhiwang lanzhiwang  567 3月  26 11:26 ca-config.json
-rw-rw-r--  1 lanzhiwang lanzhiwang  287 3月  26 11:26 ca-csr.json

# 默认配置文件
cat ca-config.json 
{
    "signing": {
        "default": {
            "expiry": "168h"
        },
        "profiles": {
            "www": {
                "expiry": "8760h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "server auth"
                ]
            },
            "client": {
                "expiry": "8760h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "client auth"
                ]
            }
        }
    }
}

# 签名请求文件
cat ca-csr.json 
{
    "CN": "example.net",
    "hosts": [
        "example.net",
        "www.example.net"
    ],
    "key": {
        "algo": "ecdsa",
        "size": 256
    },
    "names": [
        {
            "C": "US",
            "L": "CA",
            "ST": "San Francisco"
        }
    ]
}

```

### Certificate types which are used inside Container Linux  Container Linux中使用的证书类型

* client certificate is used to authenticate client by server. For example etcdctl, etcd proxy, or docker clients.  客户端证书用于服务器对客户端进行身份验证。 例如etcdctl，etcd代理或docker客户端。

* server certificate is used by server and verified by client for server identity. For example docker server or kube-apiserver.  服务器证书由服务器使用，并由客户端验证服务器身份。 例如docker server或kube-apiserver。

* peer certificate is used by etcd cluster members as they communicate with each other in both ways.  对等证书由etcd集群成员使用，因为它们以两种方式相互通信。

### Configure CA options  配置CA选项

Now we can configure signing options inside `ca-config.json` config file. Default options contain following preconfigured fields:  现在我们可以在ca-config.json配置文件中配置签名选项。 默认选项包含以下预配置字段：

* profiles: **www** with `server auth` (TLS Web Server Authentication) X509 V3 extension and **client** with `client auth` (TLS Web Client Authentication) X509 V3 extension.  配置文件：www与服务器身份验证（TLS Web服务器身份验证）X509 V3扩展和客户端与客户端身份验证（TLS Web客户端身份验证）X509 V3扩展。

* expiry: with `8760h` default value (or 365 days)

For compliance let's rename www profile into server, create additional peer profile with both server auth and client auth extensions, and set expiry to 43800h (5 years):  为了遵守法规，我们将www配置文件重命名为服务器，使用服务器身份验证和客户端身份验证扩展创建额外的对等配置文件，并将到期时间设置为43800h（5年）：

```
{
    "signing": {
        "default": {
            "expiry": "43800h"
        },
        "profiles": {
            "server": {
                "expiry": "43800h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "server auth"
                ]
            },
            "client": {
                "expiry": "43800h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "client auth"
                ]
            },
            "peer": {
                "expiry": "43800h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "server auth",
                    "client auth"
                ]
            }
        }
    }
}
```

You can also modify `ca-csr.json` Certificate Signing Request (CSR):

```
{
    "CN": "My own CA",
    "key": {
        "algo": "rsa",
        "size": 2048
    },
    "names": [
        {
            "C": "US",
            "L": "CA",
            "O": "My Company Name",
            "ST": "San Francisco",
            "OU": "Org Unit 1",
            "OU": "Org Unit 2"
        }
    ]
}
```

```bash
$ ll
total 16
drwxrwxr-x  2 lanzhiwang lanzhiwang 4096 3月  26 11:26 ./
drwxr-xr-x 28 lanzhiwang lanzhiwang 4096 3月  26 11:26 ../
-rw-rw-r--  1 lanzhiwang lanzhiwang  567 3月  26 11:26 ca-config.json
-rw-rw-r--  1 lanzhiwang lanzhiwang  287 3月  26 11:26 ca-csr.json

$ mv ca-config.json ca-config.json_default
$ mv ca-csr.json ca-csr.json_default

$ vim ca-config.json
$ vim ca-csr.json

$  ls -ltr
total 48
-rw-rw-r-- 1 lanzhiwang lanzhiwang  567 3月  26 11:26 ca-config.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 11:26 ca-csr.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  832 3月  26 12:30 ca-config.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang  312 3月  26 12:30 ca-csr.json
```

And generate CA with defined options:

```bash
$ cfssl gencert -initca ca-csr.json | cfssljson -bare ca -

$  ls -ltr
total 48
-rw-rw-r-- 1 lanzhiwang lanzhiwang  567 3月  26 11:26 ca-config.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 11:26 ca-csr.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  832 3月  26 12:30 ca-config.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang  312 3月  26 12:30 ca-csr.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1403 3月  26 12:32 ca.pem
-rw------- 1 lanzhiwang lanzhiwang 1675 3月  26 12:32 ca-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang 1021 3月  26 12:32 ca.csr
```
You'll get following files:

```
ca-key.pem  # 私钥
ca.csr  # 证书请求文件
ca.pem  # 根证书

$ cat ca-key.pem 
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAsbJqsXtGfLpiEym9zExBLKQ+5CFQ6+F8bZxORD4U4NJ1shPb
6e95PBHOnFCjRTtk0MgaSV3PqNjnkeX3iuvmlYCGKeYGoWF1Y6vb
-----END RSA PRIVATE KEY-----

$ cat ca.csr
-----BEGIN CERTIFICATE REQUEST-----
MIICujCCAaICAQAwdTELMAkGA1UEBhMCVVMxFjAUBgNVBAgTDVNhbiBGcmFuY2lz
88CFKA189APK5Ho+4F5N/ADkSmKM6VIfKzZz+TvL
-----END CERTIFICATE REQUEST-----

$ cat ca.pem
-----BEGIN CERTIFICATE-----
MIID3jCCAsagAwIBAgIUfF3AnuZjSJyH18UGpgsS6iyBQ78wDQYJKoZIhvcNAQEL
OkqVS1LDI2ZiGiCS1J2RK9sMx+WW9ofO+44CFVlAmM32Cg==
-----END CERTIFICATE-----
```

* Please keep `ca-key.pem` file in safe. This key allows to create any kind of certificates within your CA.
* **\*.csr** files are not used in our example.

### Generate server certificate

```bash
$ cfssl print-defaults csr > server.json

$  ls -ltr
total 48
-rw-rw-r-- 1 lanzhiwang lanzhiwang  567 3月  26 11:26 ca-config.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 11:26 ca-csr.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  832 3月  26 12:30 ca-config.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang  312 3月  26 12:30 ca-csr.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1403 3月  26 12:32 ca.pem
-rw------- 1 lanzhiwang lanzhiwang 1675 3月  26 12:32 ca-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang 1021 3月  26 12:32 ca.csr
-rw-rw-r-- 1 lanzhiwang lanzhiwang  330 3月  26 12:44 server.json

$ cat server.json 
{
    "CN": "example.net",
    "hosts": [
        "example.net",
        "www.example.net"
    ],
    "key": {
        "algo": "ecdsa",
        "size": 256
    },
    "names": [
        {
            "C": "US",
            "L": "CA",
            "ST": "San Francisco"
        }
    ]
}
```

Most important values for server certificate are **Common Name (CN)** and **hosts**. We have to substitute them, for example:

```
...
    "CN": "coreos1",
    "hosts": [
        "192.168.122.68",
        "ext.example.com",
        "coreos1.local",
        "coreos1"
    ],
...

$ cp server.json server.json_default
$ vim server.json

$  ls -ltr
total 48
-rw-rw-r-- 1 lanzhiwang lanzhiwang  567 3月  26 11:26 ca-config.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 11:26 ca-csr.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  832 3月  26 12:30 ca-config.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang  312 3月  26 12:30 ca-csr.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1403 3月  26 12:32 ca.pem
-rw------- 1 lanzhiwang lanzhiwang 1675 3月  26 12:32 ca-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang 1021 3月  26 12:32 ca.csr
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 12:43 server.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  330 3月  26 12:44 server.json
```

Now we are ready to generate server certificate and private key:

```bash
$ cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=server server.json | cfssljson -bare server

$  ls -ltr
total 48
-rw-rw-r-- 1 lanzhiwang lanzhiwang  567 3月  26 11:26 ca-config.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 11:26 ca-csr.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  832 3月  26 12:30 ca-config.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang  312 3月  26 12:30 ca-csr.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1403 3月  26 12:32 ca.pem
-rw------- 1 lanzhiwang lanzhiwang 1675 3月  26 12:32 ca-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang 1021 3月  26 12:32 ca.csr
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 12:43 server.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  330 3月  26 12:44 server.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1164 3月  26 12:46 server.pem
-rw------- 1 lanzhiwang lanzhiwang  227 3月  26 12:46 server-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang  525 3月  26 12:46 server.csr
$ 
```

Or without CSR json file:

```bash
echo '{"CN":"coreos1","hosts":[""],"key":{"algo":"rsa","size":2048}}' | cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=server -hostname="192.168.122.68,ext.example.com,coreos1.local,coreos1" - | cfssljson -bare server
```

You'll get following files:

```
server-key.pem
server.csr
server.pem
```

### Generate peer certificate

```bash
$ cfssl print-defaults csr > member1.json
$ ls -ltr
total 52
-rw-rw-r-- 1 lanzhiwang lanzhiwang  567 3月  26 11:26 ca-config.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 11:26 ca-csr.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  832 3月  26 12:30 ca-config.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang  312 3月  26 12:30 ca-csr.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1403 3月  26 12:32 ca.pem
-rw------- 1 lanzhiwang lanzhiwang 1675 3月  26 12:32 ca-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang 1021 3月  26 12:32 ca.csr
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 12:43 server.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  330 3月  26 12:44 server.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1164 3月  26 12:46 server.pem
-rw------- 1 lanzhiwang lanzhiwang  227 3月  26 12:46 server-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang  525 3月  26 12:46 server.csr
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 12:55 member1.json

$ cat member1.json 
{
    "CN": "example.net",
    "hosts": [
        "example.net",
        "www.example.net"
    ],
    "key": {
        "algo": "ecdsa",
        "size": 256
    },
    "names": [
        {
            "C": "US",
            "L": "CA",
            "ST": "San Francisco"
        }
    ]
}

$ cp member1.json member1.json_default
$ ls -ltr
total 56
-rw-rw-r-- 1 lanzhiwang lanzhiwang  567 3月  26 11:26 ca-config.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 11:26 ca-csr.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  832 3月  26 12:30 ca-config.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang  312 3月  26 12:30 ca-csr.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1403 3月  26 12:32 ca.pem
-rw------- 1 lanzhiwang lanzhiwang 1675 3月  26 12:32 ca-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang 1021 3月  26 12:32 ca.csr
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 12:43 server.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  330 3月  26 12:44 server.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1164 3月  26 12:46 server.pem
-rw------- 1 lanzhiwang lanzhiwang  227 3月  26 12:46 server-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang  525 3月  26 12:46 server.csr
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 12:55 member1.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 12:56 member1.json_default

$ vim member1.json
$ ls -ltr
total 56
-rw-rw-r-- 1 lanzhiwang lanzhiwang  567 3月  26 11:26 ca-config.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 11:26 ca-csr.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  832 3月  26 12:30 ca-config.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang  312 3月  26 12:30 ca-csr.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1403 3月  26 12:32 ca.pem
-rw------- 1 lanzhiwang lanzhiwang 1675 3月  26 12:32 ca-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang 1021 3月  26 12:32 ca.csr
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 12:43 server.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  330 3月  26 12:44 server.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1164 3月  26 12:46 server.pem
-rw------- 1 lanzhiwang lanzhiwang  227 3月  26 12:46 server-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang  525 3月  26 12:46 server.csr
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 12:56 member1.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  331 3月  26 12:57 member1.json
$ 

```

Now we are ready to generate member1 certificate and private key:

```bash
$ cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=peer member1.json | cfssljson -bare member1

$ ls -ltr
total 68
-rw-rw-r-- 1 lanzhiwang lanzhiwang  567 3月  26 11:26 ca-config.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 11:26 ca-csr.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  832 3月  26 12:30 ca-config.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang  312 3月  26 12:30 ca-csr.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1403 3月  26 12:32 ca.pem
-rw------- 1 lanzhiwang lanzhiwang 1675 3月  26 12:32 ca-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang 1021 3月  26 12:32 ca.csr
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 12:43 server.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  330 3月  26 12:44 server.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1164 3月  26 12:46 server.pem
-rw------- 1 lanzhiwang lanzhiwang  227 3月  26 12:46 server-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang  525 3月  26 12:46 server.csr
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 12:56 member1.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  331 3月  26 12:57 member1.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1176 3月  26 12:59 member1.pem
-rw------- 1 lanzhiwang lanzhiwang  227 3月  26 12:59 member1-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang  525 3月  26 12:59 member1.csr
$ 

```

Or without CSR json file:

```bash
echo '{"CN":"member1","hosts":[""],"key":{"algo":"rsa","size":2048}}' | cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=peer -hostname="192.168.122.101,ext.example.com,member1.local,member1" - | cfssljson -bare member1
```

You'll get following files:

```
member1-key.pem
member1.csr
member1.pem
```

Repeat these steps for each `etcd` member hostname.


### Generate client certificate

```bash
$ cfssl print-defaults csr > client.json
$ ls -ltr
total 72
-rw-rw-r-- 1 lanzhiwang lanzhiwang  567 3月  26 11:26 ca-config.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 11:26 ca-csr.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  832 3月  26 12:30 ca-config.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang  312 3月  26 12:30 ca-csr.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1403 3月  26 12:32 ca.pem
-rw------- 1 lanzhiwang lanzhiwang 1675 3月  26 12:32 ca-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang 1021 3月  26 12:32 ca.csr
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 12:43 server.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  330 3月  26 12:44 server.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1164 3月  26 12:46 server.pem
-rw------- 1 lanzhiwang lanzhiwang  227 3月  26 12:46 server-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang  525 3月  26 12:46 server.csr
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 12:56 member1.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  331 3月  26 12:57 member1.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1176 3月  26 12:59 member1.pem
-rw------- 1 lanzhiwang lanzhiwang  227 3月  26 12:59 member1-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang  525 3月  26 12:59 member1.csr
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 13:01 client.json

$ cat client.json 
{
    "CN": "example.net",
    "hosts": [
        "example.net",
        "www.example.net"
    ],
    "key": {
        "algo": "ecdsa",
        "size": 256
    },
    "names": [
        {
            "C": "US",
            "L": "CA",
            "ST": "San Francisco"
        }
    ]
}

$ cp client.json client.json_default
$ vim client.json
$ ls -ltr
total 76
-rw-rw-r-- 1 lanzhiwang lanzhiwang  567 3月  26 11:26 ca-config.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 11:26 ca-csr.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  832 3月  26 12:30 ca-config.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang  312 3月  26 12:30 ca-csr.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1403 3月  26 12:32 ca.pem
-rw------- 1 lanzhiwang lanzhiwang 1675 3月  26 12:32 ca-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang 1021 3月  26 12:32 ca.csr
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 12:43 server.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  330 3月  26 12:44 server.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1164 3月  26 12:46 server.pem
-rw------- 1 lanzhiwang lanzhiwang  227 3月  26 12:46 server-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang  525 3月  26 12:46 server.csr
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 12:56 member1.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  331 3月  26 12:57 member1.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1176 3月  26 12:59 member1.pem
-rw------- 1 lanzhiwang lanzhiwang  227 3月  26 12:59 member1-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang  525 3月  26 12:59 member1.csr
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 13:02 client.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  244 3月  26 13:02 client.json

$ cat client.json
{
    "CN": "client",
    "hosts": [
        ""
    ],
    "key": {
        "algo": "ecdsa",
        "size": 256
    },
    "names": [
        {
            "C": "US",
            "L": "CA",
            "ST": "San Francisco"
        }
    ]
}

```

Generate client certificate:

```bash
$ cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=client client.json | cfssljson -bare client

$ ls -ltr
total 88
-rw-rw-r-- 1 lanzhiwang lanzhiwang  567 3月  26 11:26 ca-config.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 11:26 ca-csr.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  832 3月  26 12:30 ca-config.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang  312 3月  26 12:30 ca-csr.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1403 3月  26 12:32 ca.pem
-rw------- 1 lanzhiwang lanzhiwang 1675 3月  26 12:32 ca-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang 1021 3月  26 12:32 ca.csr
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 12:43 server.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  330 3月  26 12:44 server.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1164 3月  26 12:46 server.pem
-rw------- 1 lanzhiwang lanzhiwang  227 3月  26 12:46 server-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang  525 3月  26 12:46 server.csr
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 12:56 member1.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  331 3月  26 12:57 member1.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1176 3月  26 12:59 member1.pem
-rw------- 1 lanzhiwang lanzhiwang  227 3月  26 12:59 member1-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang  525 3月  26 12:59 member1.csr
-rw-rw-r-- 1 lanzhiwang lanzhiwang  287 3月  26 13:02 client.json_default
-rw-rw-r-- 1 lanzhiwang lanzhiwang  244 3月  26 13:02 client.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1099 3月  26 13:05 client.pem
-rw------- 1 lanzhiwang lanzhiwang  227 3月  26 13:05 client-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang  465 3月  26 13:05 client.csr

```

Or without CSR json file:

```bash
echo '{"CN":"client","hosts":[""],"key":{"algo":"rsa","size":2048}}' | cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=client - | cfssljson -bare client
```

You'll get following files:

```
client-key.pem
client.csr
client.pem
```

## TLDR

### Download binaries

```
mkdir ~/bin
curl -s -L -o ~/bin/cfssl https://pkg.cfssl.org/R1.2/cfssl_linux-amd64
curl -s -L -o ~/bin/cfssljson https://pkg.cfssl.org/R1.2/cfssljson_linux-amd64
chmod +x ~/bin/{cfssl,cfssljson}
export PATH=$PATH:~/bin
```

### Create directory to store certificates:

```
mkdir ~/cfssl
cd ~/cfssl
```

### Generate CA and certificates

```bash
$ echo '{"CN":"CA","key":{"algo":"rsa","size":2048}}' | cfssl gencert -initca - | cfssljson -bare ca -

$ ls -ltr
total 12
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1119 3月  26 13:09 ca.pem
-rw------- 1 lanzhiwang lanzhiwang 1675 3月  26 13:09 ca-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang  883 3月  26 13:09 ca.csr
$ 

$ echo '{"signing":{"default":{"expiry":"43800h","usages":["signing","key encipherment","server auth","client auth"]}}}' > ca-config.json

$ ls -ltr
total 16
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1119 3月  26 13:09 ca.pem
-rw------- 1 lanzhiwang lanzhiwang 1675 3月  26 13:09 ca-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang  883 3月  26 13:09 ca.csr
-rw-rw-r-- 1 lanzhiwang lanzhiwang  112 3月  26 13:11 ca-config.json

$ cat ca-config.json 
{"signing":{"default":{"expiry":"43800h","usages":["signing","key encipherment","server auth","client auth"]}}}
$ 

$ export ADDRESS=192.168.122.68,ext1.example.com,coreos1.local,coreos1
$ export NAME=server
$ echo '{"CN":"'$NAME'","hosts":[""],"key":{"algo":"rsa","size":2048}}' | cfssl gencert -config=ca-config.json -ca=ca.pem -ca-key=ca-key.pem -hostname="$ADDRESS" - | cfssljson -bare $NAME

$ ls -ltr
total 28
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1119 3月  26 13:09 ca.pem
-rw------- 1 lanzhiwang lanzhiwang 1675 3月  26 13:09 ca-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang  883 3月  26 13:09 ca.csr
-rw-rw-r-- 1 lanzhiwang lanzhiwang  112 3月  26 13:11 ca-config.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1241 3月  26 13:12 server.pem
-rw------- 1 lanzhiwang lanzhiwang 1679 3月  26 13:12 server-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang  928 3月  26 13:12 server.csr
$ 

$ export ADDRESS=
$ export NAME=client
$ echo '{"CN":"'$NAME'","hosts":[""],"key":{"algo":"rsa","size":2048}}' | cfssl gencert -config=ca-config.json -ca=ca.pem -ca-key=ca-key.pem -hostname="$ADDRESS" - | cfssljson -bare $NAME

$ ls -ltr
total 40
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1119 3月  26 13:09 ca.pem
-rw------- 1 lanzhiwang lanzhiwang 1675 3月  26 13:09 ca-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang  883 3月  26 13:09 ca.csr
-rw-rw-r-- 1 lanzhiwang lanzhiwang  112 3月  26 13:11 ca-config.json
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1241 3月  26 13:12 server.pem
-rw------- 1 lanzhiwang lanzhiwang 1679 3月  26 13:12 server-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang  928 3月  26 13:12 server.csr
-rw-rw-r-- 1 lanzhiwang lanzhiwang 1180 3月  26 13:14 client.pem
-rw------- 1 lanzhiwang lanzhiwang 1675 3月  26 13:14 client-key.pem
-rw-r--r-- 1 lanzhiwang lanzhiwang  928 3月  26 13:14 client.csr
$ 

```

### Verify data

```
openssl x509 -in ca.pem -text -noout
openssl x509 -in server.pem -text -noout
openssl x509 -in client.pem -text -noout
```

### Things to know

* Don't put your `ca-key.pem` into a Container Linux Config, it is recommended to store it in safe place. This key allows to generate as much certificates as possible.

* Keep **key** files in safe. Don't forget to set proper file permissions, i.e. `chmod 0600 server-key.pem`.

* Certificates in this **TLDR** example have both `server auth` and `client auth` X509 V3 extensions and you can use them with servers and clients' authentication.

* You are free to generate keys and certificates for wildcard `*` address as well. They will work on any machine. It will simplify certificates routine but increase security risks.
