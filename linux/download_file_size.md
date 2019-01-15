## 不下载文件直接获取下载文件的大小

```bash
$ http --headers http://g47.gdl.netease.com/g47_netease_netease.edt_cpm_dev_1.0.25.apk
HTTP/1.1 200 OK
Accept-Ranges: bytes
Accept-Ranges: bytes
Age: 33164404
Cache-Control: max-age=31536000
Connection: keep-alive
Content-Length: 473128422
Content-Type: application/vnd.android.package-archive
Date: Tue, 15 Jan 2019 07:11:47 GMT
Expires: Wed, 26 Dec 2018 13:34:22 GMT
Last-Modified: Wed, 06 Sep 2017 12:26:25 GMT
Server: NEWs/1.14.0.4
Via: http/1.1 cdn-ats03-12004 (netease-ts/1.1.2 [cRs f ])

$ 
# 头字段 Content-Length: 473128422

```


