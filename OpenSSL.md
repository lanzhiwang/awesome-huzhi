## OpenSSL

- Generation private key and public key
  - Generation RSA private key and public key
  - Generation DSA private key
  - Generation EC private key

- 生成CSR文件(证书签署请求文件)
  - Creating Certificate Signing Requests(CSR) 直接生成 CSR 文件 fd.key -> fd-public.key -> fd.csr
  - Creating CSRs from Existing Certificates 根据已有的CRT文件生成CSR文件
  - Unattended CSR Generation 根据配置文件和private key生成CSR文件 fd.key -> fd-public.key -> fd.csr

- 生成CRT文件
  - Signing Your Own Certificates 根据CSR文件生成CRT文件 fd.key -> fd-public.key -> fd.csr -> fd.crt
  - 根据private key直接生成CRT文件，不生成CSR文件 fd.key -> fd-public.key -> fd.crt

- 根据CRT文件反向生成CSR文件

- 根据CSR文件，private key，多站点配置文件生成CRT文件，该CRT文件适用多站点



### Generation private key and public key

#### Generation RSA private key and public key

```bash
# Key Generation
# 生成RSA private key
[root@iZ94q3o9hwgZ ~]# openssl genrsa -aes128 -out fd.key 2048
Generating RSA private key, 2048 bit long modulus
......................................................+++
............................+++
e is 65537 (0x10001)
Enter pass phrase for fd.key:
Verifying - Enter pass phrase for fd.key:

[root@iZ94q3o9hwgZ ~]# ll
total 4
-rw-r--r-- 1 root root 1766 Dec 24 18:17 fd.key

[root@iZ94q3o9hwgZ ~]# cat fd.key
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,EAC56CAA0420269DC3F24B6744D48031
M/c484Y/chP0mS2x5vuD++Zp1qoEGS/1n+OfEsd48Z+nMXODyCfzDHWHZpdtMCiM
-----END RSA PRIVATE KEY-----
[root@iZ94q3o9hwgZ ~]#

[root@iZ94q3o9hwgZ ~]# openssl rsa -text -in fd.key
Enter pass phrase for fd.key:
Private-Key: (2048 bit)
modulus:
    00:ea:8e:5f:15:e2:dc:06:2b:11:fb:ae:20:eb:c6:
    d7:13
publicExponent: 65537 (0x10001)
privateExponent:
    00:cf:8e:66:93:ce:68:d6:c8:7c:24:53:44:ec:7e:
    be:f9
prime1:
    00:ff:f9:77:b3:04:fd:62:bd:74:d1:93:18:98:49:
    c2:c8:8f:56:0a:bb:c8:e5:e7
prime2:
    00:ea:94:5b:75:62:3f:b1:a3:01:33:eb:aa:c9:21:
    9a:b5:0c:78:81:a9:d3:87:f5
exponent1:
    36:1f:68:48:c8:d8:4e:a5:62:6a:e1:a0:44:aa:ed:
    2a:5e:ec:41:6e:bd:26:a7
exponent2:
    47:22:ca:41:64:93:f0:28:80:5a:e0:62:a0:2f:c4:
    bb:58:96:ca:ab:57:6c:69
coefficient:
    00:d0:5f:e4:df:65:32:5b:6d:36:c0:5a:ba:55:8a:
    6f:4c:4f:5d:50:60:89:d9:b1
writing RSA key
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA6o5fFeLcBisR+64g68aaMEmGlCEFf6sBXD0GHrU4QvqxqayQ
6uUgLL5NUIhz8UEvtk1bbsFqpTpKy/7YaD1fqLH32G9MT11QYInZsQ==
-----END RSA PRIVATE KEY-----
[root@iZ94q3o9hwgZ ~]#  

# 根据private key生成RSA public key
[root@iZ94q3o9hwgZ ~]# openssl rsa -in fd.key -pubout -out fd-public.key
Enter pass phrase for fd.key:
writing RSA key

[root@iZ94q3o9hwgZ ~]# ll
total 8
-rw-r--r-- 1 root root 1766 Dec 24 18:17 fd.key
-rw-r--r-- 1 root root  451 Dec 24 18:24 fd-public.key
[root@iZ94q3o9hwgZ ~]#

[root@iZ94q3o9hwgZ ~]# cat fd-public.key
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA6o5fFeLcBisR+64g68aa
EwIDAQAB
-----END PUBLIC KEY-----
[root@iZ94q3o9hwgZ ~]#  
```

#### Generation DSA private key

```bash
# 生成DSA private key
[root@iZ94q3o9hwgZ ~]# openssl dsaparam -genkey 2048 | openssl dsa -out dsa.key -aes128
read DSA key
Generating DSA parameters, 2048 bit long prime
This could take some time
..+...+.....+.............+.....+............+.......+................................+.............+........+..............+.+...........+...+...........+...+...+........+............+......+.......+...+...+..+..+.+..+.+..+....+........+............+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*
+....+....+.....+....................................+.+..............+................+...+.......................+....+...............+...........+...+.......+......+..+....+..+........+...+....+...+.+.............+.....................+.......................+...+.+................+..+.+.............+......+.....................................+.............+......+............+.........+..+...+.........+..+.................+.......+...+..........+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*
writing DSA key
Enter PEM pass phrase:
Verifying - Enter PEM pass phrase:

[root@iZ94q3o9hwgZ ~]# ll
total 12
-rw-r--r-- 1 root root 1311 Dec 24 18:29 dsa.key

[root@iZ94q3o9hwgZ ~]# cat dsa.key
-----BEGIN DSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,0BE4A369AB1600528F7CF2B97D20A84C
ujNdFLB2sAgsj4y5+S3FAcNDfk3bPF3nggas3TkqE0CfPmAEL3zkudn8LEbVvJjR
-----END DSA PRIVATE KEY-----
[root@iZ94q3o9hwgZ ~]#
```

#### Generation EC private key

```bash
# 生成EC private key
[root@iZ94q3o9hwgZ ~]# openssl ecparam -genkey -name secp256r1 | openssl ec -out ec.key -aes128
read EC key
using curve name prime256v1 instead of secp256r1
writing EC key
Enter PEM pass phrase:
Verifying - Enter PEM pass phrase:

[root@iZ94q3o9hwgZ ~]# ll
total 16
-rw-r--r-- 1 root root  314 Dec 24 18:31 ec.key

[root@iZ94q3o9hwgZ ~]# cat ec.key
-----BEGIN EC PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,B98294039A9FD960CF06C00EE660B6B1
Ncze0kc+Be9FJjXPCJ8gzCXFKDCNiXkZiBQ0r//tjrZvY3+K1bxtkTm5DwUkFpE/
NhbEr/2//TPE/l3ebDTjhtgbLnpP1ciOCGwYCkhV70hLtoVuAN6PttBGvaPl4MTD
eylH8bsd6ph/t2kgWkj1hH9DViqOw551WNiqDqBxPLg=
-----END EC PRIVATE KEY-----
[root@iZ94q3o9hwgZ ~]#  
```

### 生成CSR文件(证书签署请求文件)

#### Creating Certificate Signing Requests(CSR)

```bash
## fd.key -> fd-public.key -> fd.csr
ubuntu@huzhi-dev:~/pki$ openssl genrsa -aes128 -out fd.key 2048
Generating RSA private key, 2048 bit long modulus
.................+++
....................+++
e is 65537 (0x10001)
Enter pass phrase for fd.key:hz67233
Verifying - Enter pass phrase for fd.key:
ubuntu@huzhi-dev:~/pki$

ubuntu@huzhi-dev:~/pki$ openssl rsa -in fd.key -pubout -out fd-public.key
Enter pass phrase for fd.key:
writing RSA key
ubuntu@huzhi-dev:~/pki$

ubuntu@huzhi-dev:~/pki$ ll
total 16
drwxrwxr-x  2 ubuntu ubuntu 4096 Nov  9 10:13 ./
drwxr-xr-x 11 ubuntu ubuntu 4096 Nov  9 10:13 ../
-rw-rw-r--  1 ubuntu ubuntu 1766 Nov  9 10:13 fd.key
-rw-rw-r--  1 ubuntu ubuntu  451 Nov  9 10:13 fd-public.key
ubuntu@huzhi-dev:~/pki$

ubuntu@huzhi-dev:~/pki$ openssl req -new -key fd.key -out fd.csr
Enter pass phrase for fd.key:
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:CN
State or Province Name (full name) [Some-State]:hubeisheng
Locality Name (eg, city) []:wuhanshi
Organization Name (eg, company) [Internet Widgits Pty Ltd]:wuhan antiy
Organizational Unit Name (eg, section) []:Technical Support
Common Name (e.g. server FQDN or YOUR name) []:www.antiy.com
Email Address []:huzhi@antiy.cn
Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:
ubuntu@huzhi-dev:~/pki$

ubuntu@huzhi-dev:~/pki$ ll
total 20
drwxrwxr-x  2 ubuntu ubuntu 4096 Nov  9 10:15 ./
drwxr-xr-x 11 ubuntu ubuntu 4096 Nov  9 10:13 ../
-rw-rw-r--  1 ubuntu ubuntu 1078 Nov  9 10:15 fd.csr
-rw-rw-r--  1 ubuntu ubuntu 1766 Nov  9 10:13 fd.key
-rw-rw-r--  1 ubuntu ubuntu  451 Nov  9 10:13 fd-public.key

ubuntu@huzhi-dev:~/pki$ cat fd.csr
-----BEGIN CERTIFICATE REQUEST-----
MIIC5DCCAcwCAQAwgZ4xCzAJBgNVBAYTAkNOMRMwEQYDVQQIDApodWJlaXNoZW5n
MREwDwYDVQQHDAh3dWhhbnNoaTEUMBIGA1UECgwLd3VoYW4gYW50aXkxGjAYBgNV
BAsMEVRlY2huaWNhbCBTdXBwb3J0MRYwFAYDVQQDDA13d3cuYW50aXkuY29tMR0w
GwYJKoZIhvcNAQkBFg5odXpoaUBhbnRpeS5jbjCCASIwDQYJKoZIhvcNAQEBBQAD
ggEPADCCAQoCggEBANckxFev2sfpzHarWIX5icG2WBUPNNfV+laewZwFzwh7LvRT
fyETjJW74Zspa/U8wLR27fup5kFuPq6qmz8+98VPE/aw4LMV9btW0NDtnFZ7DUoB
53Gqa9pIysMofOG69GJNRBq6YupSQer9pxQ0GIFolY+DZj/eHtCMW06b1tjdB6RS
8+OYg0dbqCp2f1fhXz7JYXll7+zvwPHFWlW9wpk2WKeP23UNVuF9p/d5vUCkx1eJ
39rDFgjjFjy03IpsWXk8UYQsTyZa1hPbX1YGgOQ05ok024gvukqa0gxJyDksG1Is
V0iLAg+3nM323XKyIvgpilqt6lWRQ+Q5iJpDVTkCAwEAAaAAMA0GCSqGSIb3DQEB
CwUAA4IBAQBibAIjVK5015+oFj5ZS3nKfPv2uFag9a5EW0pQaEsEaQMJ88/c054v
IF40f9d64hxtIO5hdj5VNBjAnKRdcUnC2HYzD/DIgbMrgpcTV7qmDP9ho9wE9yAo
iO6gtjOz6fXTUGYNFr94UIPNUXx+8yf+EbjUWP3zeQKnvwq7TvlfRlRD/OuQqPU+
onDhcWcILx5E6McQWasYzCtf2NOXDfNzn4k1Fv13GPqr5mO4iMBNPN6YE9PqpPst
XQTnrNElGbXUDZZnhhT53Yfnf+wGQdX/eduFrVeQMfnVT4io8gJ4NpLVUGw/DpmM
Otn8TbA1pw7ymMPzZPthizeGnzzEwYgX
-----END CERTIFICATE REQUEST-----
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
ubuntu@huzhi-dev:~/pki$


Country Name (2 letter code) [AU]:CN #国家
State or Province Name (full name) [Some-State]:hubeisheng # 省份
Locality Name (eg, city) []:wuhanshi # 城市
Organization Name (eg, company) [Internet Widgits Pty Ltd]:wuhan antiy # 公司名称
Organizational Unit Name (eg, section) []:Technical Support # 公司部门
Common Name (e.g. server FQDN or YOUR name) []:www.antiy.com # 公司完整域名
Email Address []:huzhi@antiy.cn # 联系人邮箱

###########################################################################################################################

Subject: C=CN, ST=hubeisheng, L=wuhanshi, O=wuhan antiy, OU=Technical Support, CN=www.antiy.com/emailAddress=huzhi@antiy.cn
```

#### Creating CSRs from Existing Certificates 根据已有的CRT文件生成CSR文件

```bash
[root@iZ94q3o9hwgZ ~]# ll
total 20
-rw-r--r-- 1 root root 1766 Dec 24 18:17 fd.key
-rw-r--r-- 1 root root  451 Dec 24 18:24 fd-public.key
# 根据已有的CRT文件生成CSR文件
[root@iZ94q3o9hwgZ ~]# openssl x509 -x509toreq -in fd.crt -out fd.csr -signkey fd.key
[root@iZ94q3o9hwgZ ~]#
```

#### Unattended CSR Generation 根据配置文件和private key生成CSR文件

```bash
## fd.key -> fd-public.key -> fd.csr
[root@iZ94q3o9hwgZ ~]# cat fd.cnf
[req]
prompt = no
distinguished_name = distinguished_name
[distinguished_name]
CN = www.feistyduck.com
emailAddress = webmaster@feistyduck.com
O = Feisty Duck Ltd
L = London
C = GB                                                                                 
[root@iZ94q3o9hwgZ ~]# ll
total 24
-rw-r--r-- 1 root root  182 Dec 24 18:50 fd.cnf
-rw-r--r-- 1 root root 1766 Dec 24 18:17 fd.key
-rw-r--r-- 1 root root  451 Dec 24 18:24 fd-public.key
[root@iZ94q3o9hwgZ ~]#
# 根据配置文件和private key生成CSR文件
[root@iZ94q3o9hwgZ ~]# openssl req -new -config fd.cnf -key fd.key -out fdWithCnf.csr
Enter pass phrase for fd.key:
[root@iZ94q3o9hwgZ ~]# ll
total 28
-rw-r--r-- 1 root root  182 Dec 24 18:50 fd.cnf
-rw-r--r-- 1 root root 1766 Dec 24 18:17 fd.key
-rw-r--r-- 1 root root  451 Dec 24 18:24 fd-public.key
-rw-r--r-- 1 root root 1033 Dec 24 18:52 fdWithCnf.csr
[root@iZ94q3o9hwgZ ~]#  
[root@iZ94q3o9hwgZ ~]# openssl req -text -in fdWithCnf.csr -noout
Certificate Request:
    Data:
        Version: 0 (0x0)
        Subject: CN=www.feistyduck.com/emailAddress=webmaster@feistyduck.com, O=Feisty Duck Ltd, L=London, C=GB
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                Public-Key: (2048 bit)
                Modulus:
                    00:ea:8e:5f:15:e2:dc:06:2b:11:fb:ae:20:eb:c6:
                    73:f0:8f:22:ae:f9:9f:58:7a:6e:31:89:0e:a4:e5:
                    d7:13
                Exponent: 65537 (0x10001)
        Attributes:
            a0:00
    Signature Algorithm: sha1WithRSAEncryption
         4a:a3:47:9f:9b:87:8f:7e:c0:64:02:97:3c:04:bc:16:22:8c:
         af:0f:35:7b
[root@iZ94q3o9hwgZ ~]#
```

### 生成CRT文件

#### Signing Your Own Certificates 根据CSR文件生成CRT文件

```bash
## fd.key -> fd-public.key -> fd.csr -> fd.crt

## 证书标准
## X.509 - 这是一种证书标准,主要定义了证书中应该包含哪些内容.其详情可以参考
## RFC5280,SSL使用的就是这种证书标准.

[root@iZ94q3o9hwgZ ~]# ll
total 28
-rw-r--r-- 1 root root 1033 Dec 24 18:39 fd.csr
-rw-r--r-- 1 root root 1766 Dec 24 18:17 fd.key
-rw-r--r-- 1 root root  451 Dec 24 18:24 fd-public.key
# 根据CSR文件生成CRT文件
[root@iZ94q3o9hwgZ ~]# openssl x509 -req -days 365 -in fd.csr -signkey fd.key -out fd.crt
Signature ok
subject=/C=GB/L=London/O=Feisty Duck Ltd/CN=www.feistyduck.com/emailAddress=webmaster@feistyduck.com
Getting Private key
Enter pass phrase for fd.key:
[root@iZ94q3o9hwgZ ~]# ll
total 32
-rw-r--r-- 1 root root 1265 Dec 24 18:57 fd.crt
-rw-r--r-- 1 root root 1033 Dec 24 18:39 fd.csr
-rw-r--r-- 1 root root 1766 Dec 24 18:17 fd.key
-rw-r--r-- 1 root root  451 Dec 24 18:24 fd-public.key
[root@iZ94q3o9hwgZ ~]#
```

#### 根据private key直接生成CRT文件，不生成CSR文件

```bash
## fd.key -> fd-public.key -> fd.crt

[root@iZ94q3o9hwgZ ~]# ll
total 28
-rw-r--r-- 1 root root 1766 Dec 24 18:17 fd.key
-rw-r--r-- 1 root root  451 Dec 24 18:24 fd-public.key
# 根据private key直接生成CRT文件，不生成CSR文件
root@iZ94q3o9hwgZ ~]# openssl req -new -x509 -days 365 -key fd.key -out fdNoCsr.crt
Enter pass phrase for fd.key:
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [XX]:GB
State or Province Name (full name) []:.
Locality Name (eg, city) [Default City]:London
Organization Name (eg, company) [Default Company Ltd]:Feisty Duck Ltd
Organizational Unit Name (eg, section) []:
Common Name (eg, your name or your server's hostname) []:www.feistyduck.com
Email Address []:webmaster@feistyduck.com
[root@iZ94q3o9hwgZ ~]# ll
total 40
-rw-r--r-- 1 root root 1766 Dec 24 18:17 fd.key
-rw-r--r-- 1 root root 1383 Dec 24 19:04 fdNoCsr.crt
-rw-r--r-- 1 root root  451 Dec 24 18:24 fd-public.key
[root@iZ94q3o9hwgZ ~]#  
```

### 根据CRT文件反向生成CSR文件

```bash
[root@iZ94q3o9hwgZ ~]# ll
total 36
-rw-r--r-- 1 root root 1265 Dec 24 18:57 fd.crt
-rw-r--r-- 1 root root 1766 Dec 24 18:17 fd.key
-rw-r--r-- 1 root root  451 Dec 24 18:24 fd-public.key
[root@iZ94q3o9hwgZ ~]#
# 根据CRT文件反向生成CSR文件
[root@iZ94q3o9hwgZ ~]# openssl x509 -x509toreq -in fd.crt -out fdWithCrt.csr -signkey fd.key
Getting request Private Key
Enter pass phrase for fd.key:
Generating certificate request
[root@iZ94q3o9hwgZ ~]# ll
total 36
-rw-r--r-- 1 root root 1265 Dec 24 18:57 fd.crt
-rw-r--r-- 1 root root 1766 Dec 24 18:17 fd.key
-rw-r--r-- 1 root root  451 Dec 24 18:24 fd-public.key
-rw-r--r-- 1 root root 3538 Dec 24 18:58 fdWithCrt.csr
[root@iZ94q3o9hwgZ ~]#
```

### Creating Certificates Valid for Multiple Hostnames 根据CSR文件，private key，多站点配置文件生成CRT文件，该CRT文件适用多站点

```bash
## fd.key -> fd-public.key -> fd.csr -> fd.crt

[root@iZ94q3o9hwgZ ~]# ll
total 40
-rw-r--r-- 1 root root 1033 Dec 24 18:39 fd.csr
-rw-r--r-- 1 root root 1766 Dec 24 18:17 fd.key
-rw-r--r-- 1 root root  451 Dec 24 18:24 fd-public.key
[root@iZ94q3o9hwgZ ~]# cat fd.ext
subjectAltName = DNS:*.feistyduck.com, DNS:feistyduck.com
[root@iZ94q3o9hwgZ ~]# ll
total 44
-rw-r--r-- 1 root root 1033 Dec 24 18:39 fd.csr
-rw-r--r-- 1 root root   58 Dec 24 19:09 fd.ext
-rw-r--r-- 1 root root 1766 Dec 24 18:17 fd.key
-rw-r--r-- 1 root root  451 Dec 24 18:24 fd-public.key
[root@iZ94q3o9hwgZ ~]#
# 根据CSR文件，private key，多站点配置文件生成CRT文件，该CRT文件适用多站点
[root@iZ94q3o9hwgZ ~]# openssl x509 -req -days 365 \
> -in fd.csr -signkey fd.key -out fdWithExt.crt \
> -extfile fd.ext
Signature ok
subject=/C=GB/L=London/O=Feisty Duck Ltd/CN=www.feistyduck.com/emailAddress=webmaster@feistyduck.com
Getting Private key
Enter pass phrase for fd.key:
[root@iZ94q3o9hwgZ ~]# ll
total 48
-rw-r--r-- 1 root root 1033 Dec 24 18:39 fd.csr
-rw-r--r-- 1 root root   58 Dec 24 19:09 fd.ext
-rw-r--r-- 1 root root 1766 Dec 24 18:17 fd.key
-rw-r--r-- 1 root root  451 Dec 24 18:24 fd-public.key
-rw-r--r-- 1 root root 1338 Dec 24 19:12 fdWithExt.crt
[root@iZ94q3o9hwgZ ~]#  
```
