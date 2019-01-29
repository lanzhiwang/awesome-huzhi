## SSL

### MySQL 服务端
```
[mysqld]
ssl-ca=ca.pem
ssl-cert=server-cert.pem
ssl-key=server-key.pem
```

* --ssl-ca: The path name of the Certificate Authority (CA) certificate file.

* --ssl-cert: The path name of the server public key certificate file. This can be sent to the client and authenticated against the CA certificate that it has.

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
