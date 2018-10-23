## 长连接和短连接

#### 长连接示例


* 设置 HTTP 长连接并设置过期时间

在首部字段中设置`Connection:keep-alive`和`Keep-Alive: timeout=60`，表明连接建立之后，空闲时间超过60秒之后，就会失效。如果在空闲第58秒时，再次使用此连接，则连接仍然有效，使用完之后，重新计数，空闲60秒之后过期。

* 设置HTTP长连接，无过期时间

在首部字段中只设置·Connection:keep-alive·，表明连接永久有效。

```
# 设置 HTTP 长连接并设置过期时间
$ http -v www.baidu.com Connection:keep-alive 'Keep-Alive:timeout=60'
GET / HTTP/1.1
User-Agent: HTTPie/0.9.8
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Keep-Alive: timeout=60
Host: www.baidu.com



HTTP/1.1 200 OK
Bdpagetype: 1
Bdqid: 0xc102601b00048eb7
Cache-Control: private
Connection: Keep-Alive
Content-Encoding: gzip
Content-Type: text/html
Cxy_all: baidu+4211a34686ba0c957f714c54dc505eb2
Date: Tue, 23 Oct 2018 02:09:34 GMT
Expires: Tue, 23 Oct 2018 02:08:47 GMT
P3p: CP=" OTI DSP COR IVA OUR IND COM "
Server: BWS/1.1
Set-Cookie: BAIDUID=405FF591D1E692C8C08A17079C17677E:FG=1; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2147483647; path=/; domain=.baidu.com
Set-Cookie: BIDUPSID=405FF591D1E692C8C08A17079C17677E; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2147483647; path=/; domain=.baidu.com
Set-Cookie: PSTM=1540260574; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2147483647; path=/; domain=.baidu.com
Set-Cookie: delPer=0; path=/; domain=.baidu.com
Set-Cookie: BDSVRTM=0; path=/
Set-Cookie: BD_HOME=0; path=/
Set-Cookie: H_PS_PSSID=26525_1449_25810_21127_27401; path=/; domain=.baidu.com
Vary: Accept-Encoding
X-Ua-Compatible: IE=Edge,chrome=1
Transfer-Encoding: chunked

<!DOCTYPE html>
<!--STATUS OK-->
......

# 设置HTTP长连接，无过期时间
$ http -v www.baidu.com Connection:keep-alive
GET / HTTP/1.1
User-Agent: HTTPie/0.9.8
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Host: www.baidu.com



HTTP/1.1 200 OK
Bdpagetype: 1
Bdqid: 0xe163cb6d00065706
Cache-Control: private
Connection: Keep-Alive
Content-Encoding: gzip
Content-Type: text/html
Cxy_all: baidu+8f52ce6d3f27e2651857dc5f4f63c452
Date: Tue, 23 Oct 2018 02:11:23 GMT
Expires: Tue, 23 Oct 2018 02:10:48 GMT
P3p: CP=" OTI DSP COR IVA OUR IND COM "
Server: BWS/1.1
Set-Cookie: BAIDUID=460035FF7C4C2F2414E75F176B150578:FG=1; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2147483647; path=/; domain=.baidu.com
Set-Cookie: BIDUPSID=460035FF7C4C2F2414E75F176B150578; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2147483647; path=/; domain=.baidu.com
Set-Cookie: PSTM=1540260683; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2147483647; path=/; domain=.baidu.com
Set-Cookie: delPer=0; path=/; domain=.baidu.com
Set-Cookie: BDSVRTM=0; path=/
Set-Cookie: BD_HOME=0; path=/
Set-Cookie: H_PS_PSSID=1457_21114_26350_22160; path=/; domain=.baidu.com
Vary: Accept-Encoding
X-Ua-Compatible: IE=Edge,chrome=1
Transfer-Encoding: chunked

<!DOCTYPE html>
<!--STATUS OK-->
......

```

#### 短连接示例

* 设置HTTP短连接

在首部字段中设置`Connection:close`，则在一次请求/响应之后，就会关闭连接。

```
# 设置HTTP短连接
$ http -v www.baidu.com Connection:close
GET / HTTP/1.1
User-Agent: HTTPie/0.9.8
Accept-Encoding: gzip, deflate
Accept: */*
Connection: close
Host: www.baidu.com



HTTP/1.1 200 OK
Bdpagetype: 1
Bdqid: 0xb9a1c53a0005d8f9
Cache-Control: private
Content-Encoding: gzip
Content-Type: text/html
Cxy_all: baidu+44f7a90ed0be684394744f9ad81315b1
Date: Tue, 23 Oct 2018 02:07:18 GMT
Expires: Tue, 23 Oct 2018 02:06:54 GMT
P3p: CP=" OTI DSP COR IVA OUR IND COM "
Server: BWS/1.1
Set-Cookie: BAIDUID=1C1B1E53BE0EEEE9C0DD5C613912D5E5:FG=1; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2147483647; path=/; domain=.baidu.com
Set-Cookie: BIDUPSID=1C1B1E53BE0EEEE9C0DD5C613912D5E5; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2147483647; path=/; domain=.baidu.com
Set-Cookie: PSTM=1540260438; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2147483647; path=/; domain=.baidu.com
Set-Cookie: delPer=0; path=/; domain=.baidu.com
Set-Cookie: BDSVRTM=0; path=/
Set-Cookie: BD_HOME=0; path=/
Set-Cookie: H_PS_PSSID=1450_21104_18559_27400_26350_20718; path=/; domain=.baidu.com
Vary: Accept-Encoding
X-Ua-Compatible: IE=Edge,chrome=1
Connection: close
Transfer-Encoding: chunked

<!DOCTYPE html>
<!--STATUS OK-->
......

```