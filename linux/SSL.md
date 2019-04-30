## SSL

```
ca-key.pem  CA 私钥
ca-cert.pem  CA 数字证书

server-key.pem  服务器端私钥
server-req.pem  服务器端证书请求文件
server-req.pem、ca-cert.pem、ca-key.pem > server-cert.pem  服务器端数字证书

client-key.pem  客户端私钥
client-req.pem  客户端证书请求文件
client-req.pem、ca-cert.pem、ca-key.pem > client-cert.pem  客户端数字证书
```

### MySQL 服务端
```
[mysqld]
ssl-ca=ca.pem
ssl-cert=server-cert.pem
ssl-key=server-key.pem
```

* --ssl-ca: The path name of the Certificate Authority (CA) certificate file.

* --ssl-cert: The path name of the server public key certificate file. This can be sent to the client and authenticated against the CA certificate that it has.  服务器公钥证书文件的路径名。 这可以发送到客户端，并根据它拥有的CA证书进行身份验证。

* --ssl-key: The path name of the server private key file.


### MySQL 客户端

```
mysql --ssl-ca=ca.pem \
      --ssl-cert=client-cert.pem \
      --ssl-key=client-key.pem
```

* --ssl-ca: The path name of the Certificate Authority (CA) certificate file. This option, if used, must specify the same certificate used by the server. (--ssl-capath is similar but specifies the path name of a directory of CA certificate files.)

* --ssl-cert: The path name of the client public key certificate file.

* --ssl-key: The path name of the client private key file.

参考：

https://segmentfault.com/a/1190000007819751

### nginx ssl

```
server {
    listen              443 ssl;
    server_name         www.example.com;
    ssl_certificate     www.example.com.crt;  # server certificate
    ssl_certificate_key www.example.com.key;  # private key
    ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers         HIGH:!aNULL:!MD5;
    ...
}
```

### 相关工具

```bash
$ wget https://pkg.cfssl.org/R1.2/cfssl_linux-amd64
$ wget https://pkg.cfssl.org/R1.2/cfssljson_linux-amd64
$ wget https://pkg.cfssl.org/R1.2/cfssl-certinfo_linux-amd64

$ ls
cfssl-certinfo_linux-amd64  cfssljson_linux-amd64  cfssl_linux-amd64
$ 

$ mv -f cfssl_linux-amd64 cfssl
$ mv -f cfssljson_linux-amd64 cfssljson
$ mv -f cfssl-certinfo_linux-amd64 cfssl-certinfo

$ ls
cfssl  cfssl-certinfo  cfssljson
$ 

$ chmod +x ./*
$ ll
total 18808
-rwxr-xr-x. 1 root root 10376657 Mar 30  2016 cfssl
-rwxr-xr-x. 1 root root  6595195 Mar 30  2016 cfssl-certinfo
-rwxr-xr-x. 1 root root  2277873 Mar 30  2016 cfssljson

# 生成默认配置文件
$ ./cfssl print-defaults config > ca-config-default.json

# 生成默认 CA 证书请求文件 
$./cfssl print-defaults csr > ca-csr-default.json

# 生成默认文件的目的是要参考相关文件的写法

$ ll
total 18816
-rw-r--r--. 1 root root      567 Apr 30 15:13 ca-config-default.json
-rw-r--r--. 1 root root      287 Apr 30 15:13 ca-csr-default.json
-rwxr-xr-x. 1 root root 10376657 Mar 30  2016 cfssl
-rwxr-xr-x. 1 root root  6595195 Mar 30  2016 cfssl-certinfo
-rwxr-xr-x. 1 root root  2277873 Mar 30  2016 cfssljson

$ cat ca-config-default.json 
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

$ cat ca-csr-default.json 
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

# 为了说明证书请求文件各选项的意义，使用 openssl 说明生成证书请求文件的过程
# 生成私钥，公钥和证书请求文件的过程
# fd.key -> fd-public.key -> fd.csr
$ openssl genrsa -aes128 -out fd.key 2048
$ openssl rsa -in fd.key -pubout -out fd-public.key
$ openssl req -new -key fd.key -out fd.csr
Enter pass phrase for fd.key:
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:CN  # 国家
State or Province Name (full name) [Some-State]:hubeisheng  # 省份
Locality Name (eg, city) []:wuhanshi  # 城市
Organization Name (eg, company) [Internet Widgits Pty Ltd]:wuhan antiy  # 公司
Organizational Unit Name (eg, section) []:Technical Support  # 公司部门
Common Name (e.g. server FQDN or YOUR name) []:www.antiy.com  # 公司主站域名
Email Address []:huzhi@antiy.cn  # 管理员邮箱
Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:
ubuntu@huzhi-dev:~/pki$
ubuntu@huzhi-dev:~/pki$ openssl req -text -in fd.csr -noout
Certificate Request:
    Data:
        Version: 0 (0x0)
        Subject: C=CN, ST=hubeisheng, L=wuhanshi, O=wuhan antiy, OU=Technical Support, CN=www.antiy.com/emailAddress=huzhi@antiy.cn
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                Public-Key: (2048 bit)
                Modulus:
                    00:d7:24:c4:57:af:da:c7:e9:cc:76:ab:58:85:f9:
                    89:c1:b6:58:15:0f:34:d7:d5:fa:56:9e:c1:9c:05:
                    cf:08:7b:2e:f4:53:7f:21:13:8c:95:bb:e1:9b:29:
                    6b:f5:3c:c0:b4:76:ed:fb:a9:e6:41:6e:3e:ae:aa:
                    9b:3f:3e:f7:c5:4f:13:f6:b0:e0:b3:15:f5:bb:56:
                    d0:d0:ed:9c:56:7b:0d:4a:01:e7:71:aa:6b:da:48:
                    ca:c3:28:7c:e1:ba:f4:62:4d:44:1a:ba:62:ea:52:
                    41:ea:fd:a7:14:34:18:81:68:95:8f:83:66:3f:de:
                    1e:d0:8c:5b:4e:9b:d6:d8:dd:07:a4:52:f3:e3:98:
                    83:47:5b:a8:2a:76:7f:57:e1:5f:3e:c9:61:79:65:
                    ef:ec:ef:c0:f1:c5:5a:55:bd:c2:99:36:58:a7:8f:
                    db:75:0d:56:e1:7d:a7:f7:79:bd:40:a4:c7:57:89:
                    df:da:c3:16:08:e3:16:3c:b4:dc:8a:6c:59:79:3c:
                    51:84:2c:4f:26:5a:d6:13:db:5f:56:06:80:e4:34:
                    e6:89:34:db:88:2f:ba:4a:9a:d2:0c:49:c8:39:2c:
                    1b:52:2c:57:48:8b:02:0f:b7:9c:cd:f6:dd:72:b2:
                    22:f8:29:8a:5a:ad:ea:55:91:43:e4:39:88:9a:43:
                    55:39
                Exponent: 65537 (0x10001)
        Attributes:
            a0:00
    Signature Algorithm: sha256WithRSAEncryption
         62:6c:02:23:54:ae:74:d7:9f:a8:16:3e:59:4b:79:ca:7c:fb:
         f6:b8:56:a0:f5:ae:44:5b:4a:50:68:4b:04:69:03:09:f3:cf:
         dc:d3:9e:2f:20:5e:34:7f:d7:7a:e2:1c:6d:20:ee:61:76:3e:
         55:34:18:c0:9c:a4:5d:71:49:c2:d8:76:33:0f:f0:c8:81:b3:
         2b:82:97:13:57:ba:a6:0c:ff:61:a3:dc:04:f7:20:28:88:ee:
         a0:b6:33:b3:e9:f5:d3:50:66:0d:16:bf:78:50:83:cd:51:7c:
         7e:f3:27:fe:11:b8:d4:58:fd:f3:79:02:a7:bf:0a:bb:4e:f9:
         5f:46:54:43:fc:eb:90:a8:f5:3e:a2:70:e1:71:67:08:2f:1e:
         44:e8:c7:10:59:ab:18:cc:2b:5f:d8:d3:97:0d:f3:73:9f:89:
         35:16:fd:77:18:fa:ab:e6:63:b8:88:c0:4d:3c:de:98:13:d3:
         ea:a4:fb:2d:5d:04:e7:ac:d1:25:19:b5:d4:0d:96:67:86:14:
         f9:dd:87:e7:7f:ec:06:41:d5:ff:79:db:85:ad:57:90:31:f9:
         d5:4f:88:a8:f2:02:78:36:92:d5:50:6c:3f:0e:99:8c:3a:d9:
         fc:4d:b0:35:a7:0e:f2:98:c3:f3:64:fb:61:8b:37:86:9f:3c:
         c4:c1:88:17
$

##################################################
# 在 k8s 中相关文件的配置和生成
$ cat ca-config.json
{
  "signing": {
    "default": {
      "expiry": "87600h"
    },
    "profiles": {
      "kubernetes": {
        "usages": [
            "signing",
            "key encipherment",
            "server auth",
            "client auth"
        ],
        "expiry": "87600h"
      }
    }
  }
}
$
$ cat ca-csr.json
{
  "CN": "www.antiy.com/emailAddress=huzhi@antiy.cn",
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "hubeisheng",
      "L": "wuhanshi",
      "O": "wuhanantiy",
      "OU": "Technical Support"
    }
  ],
  "ca": {
    "expiry": "131400h"
  }
}
$
$ ll
total 18816
-rw-r--r--. 1 root root      292 Apr 30 15:28 ca-config.json
-rw-r--r--. 1 root root      300 Apr 30 15:29 ca-csr.json
-rwxr-xr-x. 1 root root 10376657 Mar 30  2016 cfssl
-rwxr-xr-x. 1 root root  6595195 Mar 30  2016 cfssl-certinfo
-rwxr-xr-x. 1 root root  2277873 Mar 30  2016 cfssljson
$
$ ./cfssl gencert -initca ca-csr.json | ./cfssljson -bare ca
2019/04/30 15:34:22 [INFO] generating a new CA key and certificate from CSR
2019/04/30 15:34:22 [INFO] generate received request
2019/04/30 15:34:22 [INFO] received CSR
2019/04/30 15:34:22 [INFO] generating key: rsa-2048
2019/04/30 15:34:22 [INFO] encoded CSR
2019/04/30 15:34:22 [INFO] signed certificate with serial number 394265044297767229043787806716098626236905974886
$ 
$ ll
total 18828
-rw-r--r--. 1 root root      292 Apr 30 15:28 ca-config.json
-rw-r--r--. 1 root root     1074 Apr 30 15:34 ca.csr  # CA 证书请求文件
-rw-r--r--. 1 root root      300 Apr 30 15:29 ca-csr.json
-rw-------. 1 root root     1675 Apr 30 15:34 ca-key.pem  # CA 私钥
-rw-r--r--. 1 root root     1505 Apr 30 15:34 ca.pem  # CA 公钥
-rwxr-xr-x. 1 root root 10376657 Mar 30  2016 cfssl
-rwxr-xr-x. 1 root root  6595195 Mar 30  2016 cfssl-certinfo
-rwxr-xr-x. 1 root root  2277873 Mar 30  2016 cfssljson
$
$ openssl req -text -in ca.csr -noout
Certificate Request:
    Data:
        Version: 0 (0x0)
        Subject: C=CN, ST=hubeisheng, L=wuhanshi, O=wuhanantiy, OU=Technical Support, CN=www.antiy.com/emailAddress=huzhi@antiy.cn
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                Public-Key: (2048 bit)
                Modulus:
                    00:c2:c7:dd:0f:3e:6f:d4:60:df:1c:50:ec:a1:d2:
                    18:c1:82:d4:42:df:4f:53:9d:37:0d:0d:fd:3f:29:
                    0e:81:5c:72:ae:3f:ac:fd:3c:66:7b:49:2f:a6:62:
                    3b:55:9f:7a:4c:1e:a1:0f:98:4d:ee:89:a5:fc:6e:
                    6c:23:19:f6:44:53:bb:7b:79:b6:a8:81:94:24:d2:
                    b3:15:f4:4e:6c:cb:5a:d8:e1:e8:37:94:b5:26:e3:
                    19:e4:d6:d9:dd:9c:b5:4a:92:22:3a:ab:cc:00:44:
                    8e:f8:12:0f:99:90:36:f2:96:31:a8:af:86:f3:fb:
                    2c:55:57:4f:f2:96:5a:3f:21:ed:6a:25:1f:a2:3e:
                    b7:8e:5b:9b:eb:f8:81:fa:9c:43:7b:2c:03:b8:60:
                    c5:c1:ef:1a:53:79:12:03:b3:ef:c6:78:42:6a:2c:
                    6d:22:2b:59:f1:ab:d8:11:db:58:dc:0e:9e:10:3e:
                    6a:e3:c1:71:5e:e7:f8:04:d4:2f:f6:8b:05:98:06:
                    06:7b:0c:fc:ba:25:52:62:82:20:b9:10:62:19:fd:
                    a4:68:3f:aa:c5:15:88:12:d3:b4:c9:a0:71:d0:cf:
                    c6:09:c6:63:4b:ea:18:cc:24:d3:d3:b1:8c:f2:a0:
                    54:f1:53:f1:d9:f9:bf:fe:18:f8:d7:5b:38:60:f4:
                    9d:6b
                Exponent: 65537 (0x10001)
        Attributes:
            a0:00
    Signature Algorithm: sha256WithRSAEncryption
         96:ec:6f:3f:a0:ca:4e:b1:eb:b3:fc:4f:d7:7b:b4:dd:f8:8a:
         5e:81:02:9e:ab:68:a2:52:13:38:fd:bd:ec:cc:89:6c:83:76:
         25:ef:fd:26:76:50:9d:35:ee:ef:ef:13:c9:83:d2:e1:18:6c:
         11:69:4a:75:01:a3:eb:fe:39:93:ef:2c:e9:17:45:a9:2b:f0:
         8e:72:06:85:7d:d3:da:30:44:d0:c2:d9:eb:6c:f1:25:5b:80:
         1c:30:7d:38:83:b5:d6:3d:51:7e:31:da:7c:3c:16:98:93:ad:
         56:a2:e1:33:34:7b:30:1b:73:98:7a:1b:57:ef:86:f6:76:31:
         da:c8:09:51:5f:74:1c:89:0f:e3:6a:6e:d9:42:7c:50:5d:b9:
         14:31:c2:c9:eb:9d:9a:cb:9d:10:a8:c6:0b:76:ff:5f:7e:b3:
         4e:d3:4e:93:5b:4d:5a:17:21:7a:7c:82:b2:84:92:fb:7f:22:
         95:7f:e7:96:37:2a:f1:ea:f3:16:16:75:d6:07:e5:87:73:ee:
         66:00:0c:0e:32:ea:43:bb:f8:d6:32:b5:14:ef:da:ad:b9:e1:
         69:48:93:1d:e6:ed:e6:5c:5d:b6:33:17:74:d0:36:b4:ea:fc:
         ab:19:ac:d2:db:d4:64:3e:fe:61:66:4a:03:e9:ac:fe:26:ce:
         f2:3d:d2:71
$
# 准备 kubectl 使用的 admin 证书签名请求
$ cat admin-csr.json
{
  "CN": "www.antiy.com/emailAddress=admin@antiy.cn",
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "hubeisheng",
      "L": "wuhanshi",
      "O": "wuhanantiy",
      "OU": "Technical Support"
    }
  ],
  "ca": {
    "expiry": "131400h"
  }
}

$ ll
total 18832
-rw-r--r--. 1 root root      300 Apr 30 15:41 admin-csr.json  # kubectl 使用的 admin 证书签名请求
-rw-r--r--. 1 root root      292 Apr 30 15:28 ca-config.json
-rw-r--r--. 1 root root     1074 Apr 30 15:34 ca.csr
-rw-r--r--. 1 root root      300 Apr 30 15:29 ca-csr.json
-rw-------. 1 root root     1675 Apr 30 15:34 ca-key.pem
-rw-r--r--. 1 root root     1505 Apr 30 15:34 ca.pem
-rwxr-xr-x. 1 root root 10376657 Mar 30  2016 cfssl
-rwxr-xr-x. 1 root root  6595195 Mar 30  2016 cfssl-certinfo
-rwxr-xr-x. 1 root root  2277873 Mar 30  2016 cfssljson
$
$ cat admin-csr.json
{
  "CN": "www.antiy.com/emailAddress=admin@antiy.cn",
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "hubeisheng",
      "L": "wuhanshi",
      "O": "wuhanantiy",
      "OU": "Technical Support"
    }
  ],
  "ca": {
    "expiry": "131400h"
  }
}
$
# 创建 admin 证书与私钥
$ ./cfssl gencert -ca=./ca.pem -ca-key=./ca-key.pem -config=./ca-config.json -profile=kubernetes admin-csr.json | ./cfssljson -bare admin












# 示例2
$ ./cfssl print-defaults config > ca-config.json
$ ./cfssl print-defaults csr > ca-csr.json
$ ls
ca-config.json  ca-csr.json  cfssl  cfssl-certinfo  cfssljson
$ 
$ cat ca-config.json 
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

$ cat ca-csr.json
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

$ 
$ mv ca-config.json ca-config.json-bak
$ mv ca-csr.json ca-csr.json-bak
$ ls
ca-config.json-bak  ca-csr.json-bak  cfssl  cfssl-certinfo  cfssljson
$ 
$ vim ca-config.json 
$ vim ca-csr.json
$ ls
ca-config.json  ca-config.json-bak  ca-csr.json  ca-csr.json-bak  cfssl  cfssl-certinfo  cfssljson
$ 
$ cat ca-config.json 
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
$ 
$ cat ca-csr.json
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
$ 
$ ls
ca-config.json  ca-config.json-bak  ca-csr.json  ca-csr.json-bak  cfssl  cfssl-certinfo  cfssljson
$ ./cfssl gencert -initca ca-csr.json | ./cfssljson -bare ca -
2019/01/29 16:54:54 [INFO] generating a new CA key and certificate from CSR
2019/01/29 16:54:54 [INFO] generate received request
2019/01/29 16:54:54 [INFO] received CSR
2019/01/29 16:54:54 [INFO] generating key: rsa-2048
2019/01/29 16:54:54 [INFO] encoded CSR
2019/01/29 16:54:54 [INFO] signed certificate with serial number 688956396236620997301909541064632546346454422619
$ 
$ ls
ca-config.json  ca-config.json-bak  ca.csr  ca-csr.json  ca-csr.json-bak  ca-key.pem  ca.pem  cfssl  cfssl-certinfo  cfssljson
$

ca-key.pem
ca.csr
ca.pem

$ cat ca-key.pem 
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA30YQWKGtykhQqKqgE4QfEPQLyWcDjWPOrQK3nXdxf/ZLdrfr
4weBygtRk1HuLIM4mQCNCozg3UBXOORuA2S3g7If6TsNnhjJhovZa+/aZIvaniKf
RuD6MX5MIyo12QcIC3gD4QRhM0UPW6AoW5iIbOTiCCqBvhex4GmAxmoveTdyJTlF
7c+yD/TZeeYT9VsO+IR6E1enRiE5wG9H7Y71+VzzFRGfbwOVkzotWOfQiGLq4R7S
Y5I3LZTge5OixxMCI5/Ewr2NYIBNmiadgcrN8OKOAvLgKe2DzyDDxEJWjol22iOs
JlPfw/XOLIa2ip62+oyMUICoT49WqR6I93wvjwIDAQABAoIBAQC6hHFLWWUxQs/+
1ur64riBFR5zlVbmWqZg6ZAyP4HVgA7ykhrAgZjvDB2NkDgDf2tchZVNZvrCWemD
YXB17UFRBxCZafeqRtKzT0jGXox2yk5LJGkicPcROYypI63wK2uRCSVUaLA6gEqg
JF8ShY4SSfJ5F+liv7Cc5AXruvEFtLhV2fMDS0pS1945lEEBH1tYAQv5Mp+u139c
azbo+Lqt3xiGmC3QJUVgkBZzn5pEcf0M9nyiRBrBxlxagG08zL+Y5s0TTQcyKVa3
3Exj39rjwye9q9oiZdSAMwuV+uS0/O3JkLWUkVs65FhXhbPRlztSyeK3gAsSpfrT
SH58bDKhAoGBAOjxVfajCRcww7jnnwtwXXUEBr58HyrvUajR353UUU70Ys7XdWiX
C621yv+7knVi/BQOUyHqRauj5V4hux4f86ZmAXai0puX9xRNGCihH4fqZ+Chcqps
JFMB8JGDTsk6MRRcCbMvKGss6QXWIWMH0cqEghrstm9w3if3V3AGeAA7AoGBAPVf
uBmIBS46z9ywMSzROdgqyWPb6GkHpCAcR7a5DGgf9WErhTAXCsoeAw4/4RV5Uyfa
gPqE2sO79NWioztnFv7xarq1prN3Pxijb4KDDhK9tihuCMlcTSucbeuMWpRE6CrM
qi71J5p22AXC+yDwX0vEQTg0n+Ib1Iadj+ATz8y9AoGAVJ2FumeSn8fo8LvCPCd+
60ihIoR31eLE6OwDrJM5TdLcKYJ+dZWYems06Bw8oUNpieeCLymoUSbh5IWgMNsu
aF1ZXrzagAZ9i/RNOET+7SIqxaAfxOQvda+YsWLfNZ1bwqeEJoCU0AmqQ6J60jw+
6q+jiyA9TNHVAPOJ4XmYEY0CgYA4uO3oCQeZjkLq81gK0jsa+5kemoF5dii8u4zg
cpqpn2msEtFxMoJuAs4WBzJTMn7EocBbKUchJFwO3s/5NXWdbdWMX92vcwuE+JMY
io9ASdbINdeWJN46DKlkYEe4Ks24xyM4Q7fp/zsk6dP/41FERJQHGDM1o9VXYSkX
Vb0dyQKBgQC+TESVSJr8CYsUTSfPktYFKi+gPKiS+71cc//NOnNLHKKEYTwR6bdp
n8yGWI0M/BlHL/EPWmYMk1jumDr7ShM8nXZfEPu3HK59SOq2xSuhCWaOVmAC+djD
gdspvvDkQv+IqZqm2nrbyCHdFsIxsPMABZLxuCJy6NPn9mQOuOCWhQ==
-----END RSA PRIVATE KEY-----
$ 
$ cat ca.csr 
-----BEGIN CERTIFICATE REQUEST-----
MIICujCCAaICAQAwdTELMAkGA1UEBhMCVVMxFjAUBgNVBAgTDVNhbiBGcmFuY2lz
Y28xCzAJBgNVBAcTAkNBMRgwFgYDVQQKEw9NeSBDb21wYW55IE5hbWUxEzARBgNV
BAsTCk9yZyBVbml0IDIxEjAQBgNVBAMTCU15IG93biBDQTCCASIwDQYJKoZIhvcN
AQEBBQADggEPADCCAQoCggEBAN9GEFihrcpIUKiqoBOEHxD0C8lnA41jzq0Ct513
cX/2S3a36+MHgcoLUZNR7iyDOJkAjQqM4N1AVzjkbgNkt4OyH+k7DZ4YyYaL2Wvv
2mSL2p4in0bg+jF+TCMqNdkHCAt4A+EEYTNFD1ugKFuYiGzk4ggqgb4XseBpgMZq
L3k3ciU5Re3Psg/02XnmE/VbDviEehNXp0YhOcBvR+2O9flc8xURn28DlZM6LVjn
0Ihi6uEe0mOSNy2U4HuToscTAiOfxMK9jWCATZomnYHKzfDijgLy4Cntg88gw8RC
Vo6JdtojrCZT38P1ziyGtoqetvqMjFCAqE+PVqkeiPd8L48CAwEAAaAAMA0GCSqG
SIb3DQEBCwUAA4IBAQCjnWs0We8MmWzWztgi2DHcpND/ZDX5+lx++OtDm4uAXTzD
hqqk6POqEh5fj8hzvoX6Ypfw930TI5OK+HXiJYRA5SgWz8OUmtE+bDub/H7rUuKx
u+DWyL5jYpDF4ZvboREujc06gL+auztEmfDMn7jUV48uqvmWzEd1WrVr3PNdM30b
/rWGolNU+T5XSt0tF6dDRInGIu2wFGEFJDx4YVA3EKIsWh1MYDgYEowDy12UiDx5
mKjXC4ZHiRg4vr2Xv8t6DlUFmxhTFT7VCZwJR/t9nzZxQGupQcH3ALPe1KmFDoM7
8wclvuFcZkyhxfI5X0lrs2IpKQ1bhJum8pOkolyx
-----END CERTIFICATE REQUEST-----
$ 
$ cat ca.pem 
-----BEGIN CERTIFICATE-----
MIID3jCCAsagAwIBAgIUeK3fj1j6lzDkj1a+VH6HQwKDFFswDQYJKoZIhvcNAQEL
BQAwdTELMAkGA1UEBhMCVVMxFjAUBgNVBAgTDVNhbiBGcmFuY2lzY28xCzAJBgNV
BAcTAkNBMRgwFgYDVQQKEw9NeSBDb21wYW55IE5hbWUxEzARBgNVBAsTCk9yZyBV
bml0IDIxEjAQBgNVBAMTCU15IG93biBDQTAeFw0xOTAxMjkwODUwMDBaFw0yNDAx
MjgwODUwMDBaMHUxCzAJBgNVBAYTAlVTMRYwFAYDVQQIEw1TYW4gRnJhbmNpc2Nv
MQswCQYDVQQHEwJDQTEYMBYGA1UEChMPTXkgQ29tcGFueSBOYW1lMRMwEQYDVQQL
EwpPcmcgVW5pdCAyMRIwEAYDVQQDEwlNeSBvd24gQ0EwggEiMA0GCSqGSIb3DQEB
AQUAA4IBDwAwggEKAoIBAQDfRhBYoa3KSFCoqqAThB8Q9AvJZwONY86tAredd3F/
9kt2t+vjB4HKC1GTUe4sgziZAI0KjODdQFc45G4DZLeDsh/pOw2eGMmGi9lr79pk
i9qeIp9G4PoxfkwjKjXZBwgLeAPhBGEzRQ9boChbmIhs5OIIKoG+F7HgaYDGai95
N3IlOUXtz7IP9Nl55hP1Ww74hHoTV6dGITnAb0ftjvX5XPMVEZ9vA5WTOi1Y59CI
YurhHtJjkjctlOB7k6LHEwIjn8TCvY1ggE2aJp2Bys3w4o4C8uAp7YPPIMPEQlaO
iXbaI6wmU9/D9c4shraKnrb6jIxQgKhPj1apHoj3fC+PAgMBAAGjZjBkMA4GA1Ud
DwEB/wQEAwIBBjASBgNVHRMBAf8ECDAGAQH/AgECMB0GA1UdDgQWBBSpn2KLH47x
GhwT40skoR5hZ453pzAfBgNVHSMEGDAWgBSpn2KLH47xGhwT40skoR5hZ453pzAN
BgkqhkiG9w0BAQsFAAOCAQEADoho46eGF2xVfb9p3+0NAf8DwuHcdbDBY74kjv1b
LAYVj7/FZVM8xCGaov+cLJBERO7MMKiZdWWrskQFqco8n6EHf8DxMv/L3XSX8+Vx
CRR0B6qiUltplhV3+0iJGjBV48JQS5VCkW5iJSi8ETwxOkBgWa0eQYSFuYFMTg11
UlWaaLrwcTV5evRUQn/zv2yGPEnCJ99boqk29LsV5IkwgTcNhQvcB4JRQ7LXENf/
6QBSuaTf4HRkvbUlZP7abihB24zqCZqpZgB4lzvIj5b4l8w9f8TpZ+Tav76OtxYZ
IOfk6j6CXT48wIi/CWhtFQZre7puExPEH6lv2pvAhRgpcg==
-----END CERTIFICATE-----
$ 
$ ./cfssl print-defaults csr > server.json
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

$ 
$ ./cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=server server.json | ./cfssljson -bare server
2019/01/29 17:02:21 [INFO] generate received request
2019/01/29 17:02:21 [INFO] received CSR
2019/01/29 17:02:21 [INFO] generating key: ecdsa-256
2019/01/29 17:02:21 [INFO] encoded CSR
2019/01/29 17:02:21 [INFO] signed certificate with serial number 30738989130134648125721933228092562527487145141
2019/01/29 17:02:21 [WARNING] This certificate lacks a "hosts" field. This makes it unsuitable for
websites. For more information see the Baseline Requirements for the Issuance and Management
of Publicly-Trusted Certificates, v.1.1.6, from the CA/Browser Forum (https://cabforum.org);
specifically, section 10.2.3 ("Information Requirements").
$ 

server.csr
server-key.pem
server.pem

$ cat server.csr 
-----BEGIN CERTIFICATE REQUEST-----
MIIBPDCB5AIBADBIMQswCQYDVQQGEwJVUzEWMBQGA1UECBMNU2FuIEZyYW5jaXNj
bzELMAkGA1UEBxMCQ0ExFDASBgNVBAMTC2V4YW1wbGUubmV0MFkwEwYHKoZIzj0C
AQYIKoZIzj0DAQcDQgAEXj0bp+gIGsz6Q6piNttQFfMJnBCzGrSGesMOCMllxfDB
d7jf9jz8p/4hcCnTE9MTHGMv6YeNvpV74f+nnrlNO6A6MDgGCSqGSIb3DQEJDjEr
MCkwJwYDVR0RBCAwHoILZXhhbXBsZS5uZXSCD3d3dy5leGFtcGxlLm5ldDAKBggq
hkjOPQQDAgNHADBEAiBY2q9Dy7ztVoDJIZEtTESHi7R4uXYMY/ortaHW50e8AQIg
H0U8wmAleaqC5wV8/AMo/yPy7H6oTS55bBKQkEyYq6s=
-----END CERTIFICATE REQUEST-----
$ 
$ cat server-key.pem 
-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIC0/bauHdkHIcQj4u0MqIi6uD3SdP8oHhWREnZ2tB7AzoAoGCCqGSM49
AwEHoUQDQgAEXj0bp+gIGsz6Q6piNttQFfMJnBCzGrSGesMOCMllxfDBd7jf9jz8
p/4hcCnTE9MTHGMv6YeNvpV74f+nnrlNOw==
-----END EC PRIVATE KEY-----
$ cat server.pem 
-----BEGIN CERTIFICATE-----
MIIDIDCCAgigAwIBAgIUBWJiSi5gAcxshzEWC/eFFAWSNLUwDQYJKoZIhvcNAQEL
BQAwdTELMAkGA1UEBhMCVVMxFjAUBgNVBAgTDVNhbiBGcmFuY2lzY28xCzAJBgNV
BAcTAkNBMRgwFgYDVQQKEw9NeSBDb21wYW55IE5hbWUxEzARBgNVBAsTCk9yZyBV
bml0IDIxEjAQBgNVBAMTCU15IG93biBDQTAeFw0xOTAxMjkwODU3MDBaFw0yNDAx
MjgwODU3MDBaMEgxCzAJBgNVBAYTAlVTMRYwFAYDVQQIEw1TYW4gRnJhbmNpc2Nv
MQswCQYDVQQHEwJDQTEUMBIGA1UEAxMLZXhhbXBsZS5uZXQwWTATBgcqhkjOPQIB
BggqhkjOPQMBBwNCAARePRun6AgazPpDqmI221AV8wmcELMatIZ6ww4IyWXF8MF3
uN/2PPyn/iFwKdMT0xMcYy/ph42+lXvh/6eeuU07o4GfMIGcMA4GA1UdDwEB/wQE
AwIFoDATBgNVHSUEDDAKBggrBgEFBQcDATAMBgNVHRMBAf8EAjAAMB0GA1UdDgQW
BBQh6F0l6o2g/X2xjvaZjaXTkKmpvTAfBgNVHSMEGDAWgBSpn2KLH47xGhwT40sk
oR5hZ453pzAnBgNVHREEIDAeggtleGFtcGxlLm5ldIIPd3d3LmV4YW1wbGUubmV0
MA0GCSqGSIb3DQEBCwUAA4IBAQBLMHHRUApH1c/4rrowZBbuWHIWjtp8EUPphQ4K
WWUWPoodx8gpd9g6+JvXfgUwFXlThnXoG74wa05ahndoEnaoVQLSfJ6rqGKNN78R
PuND5FYYrM1AmBr+b2WvlZuoHuNc/kVF7YI4R2BzkSblseUXWOP4KMkYxC/cg9LT
Mo72sAJR94f4zH1bvvMKvC0M+sC9n2IooK6yLMJefrsivBT9VomourzTtAmMaPxK
soyVjq/IU0zG7hxn3uwVmib3GC4gUO9slf1nhNyFCh2A2TgGNavOy8ipwX+xBRf4
6jVDXsTJoCWMTzuQ3VpbIMjK9/cV+l0YpX2wEf9lxuXZmR0g
-----END CERTIFICATE-----
$ 

```

参考：

https://coreos.com/os/docs/latest/generate-self-signed-certificates.html



