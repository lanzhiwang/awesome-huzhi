## Django URL / 处理

```bash
# 正确的请求，url带有/
$ http -v --form POST http://appsec.1218.com.cn/rzxviruscheck/?tpl=hebeigjtest request='{"priority": 1, "scanlist": [{"url": "http://222.240.44.115:12180/apks/dee05a6c8f952adba891d345f37dd1dc.apk", "md5": "dee05a6c8f952adba891d345f37dd1dc"}]}'
POST /rzxviruscheck/?tpl=hebeigjtest HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 222
Content-Type: application/x-www-form-urlencoded; charset=utf-8
Host: appsec.1218.com.cn
User-Agent: HTTPie/0.9.2

request=%7B%22priority%22%3A+1%2C+%22scanlist%22%3A+%5B%7B%22url%22%3A+%22http%3A%2F%2F222.240.44.115%3A12180%2Fapks%2Fdee05a6c8f952adba891d345f37dd1dc.apk%22%2C+%22md5%22%3A+%22dee05a6c8f952adba891d345f37dd1dc%22%7D%5D%7D

HTTP/1.1 200 OK
Connection: keep-alive
Content-Type: text/html; charset=utf-8
Date: Tue, 15 Jan 2019 06:19:02 GMT
Server: nginx/1.7.9
Transfer-Encoding: chunked
X-Frame-Options: SAMEORIGIN

{"data":"rzx virus check post successfully !","error_code":0}
```

```bash
# 错误的请求，url没有带/
$ http -v --form POST http://appsec.1218.com.cn/rzxviruscheck?tpl=hebeigjtest request='{"priority": 1, "scanlist": [{"url": "http://222.240.44.115:12180/apks/dee05a6c8f952adba891d345f37dd1dc.apk", "md5": "dee05a6c8f952adba891d345f37dd1dc"}]}'
POST /rzxviruscheck?tpl=hebeigjtest HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 222
Content-Type: application/x-www-form-urlencoded; charset=utf-8
Host: appsec.1218.com.cn
User-Agent: HTTPie/0.9.2

request=%7B%22priority%22%3A+1%2C+%22scanlist%22%3A+%5B%7B%22url%22%3A+%22http%3A%2F%2F222.240.44.115%3A12180%2Fapks%2Fdee05a6c8f952adba891d345f37dd1dc.apk%22%2C+%22md5%22%3A+%22dee05a6c8f952adba891d345f37dd1dc%22%7D%5D%7D

HTTP/1.1 301 MOVED PERMANENTLY
Connection: keep-alive
Content-Type: text/html; charset=utf-8
Date: Tue, 15 Jan 2019 06:19:57 GMT
Location: http://appsec.1218.com.cn/rzxviruscheck/?tpl=hebeigjtest
Server: nginx/1.7.9
Transfer-Encoding: chunked
X-Frame-Options: SAMEORIGIN
```

为什么返回的状态码是 301？

1. Django seetings.py配置文件中默认没有 APPEND_SLASH 这个参数，但 Django 默认这个参数为 APPEND_SLASH = True。 作用就是自动在网址结尾加'/'。
2. 由于请求的url没有 '/'，所以 Django 自动加上'/'，返回的头字段 Location 说明了这一点。
3. 但由于 POST 请求默认是不自动跳转到重定向的 url 的，所以请求结束。


```bash
# 使用默认的 GET 请求，由于http工具的特性，还是会发生POST请求
$ http -v http://appsec.1218.com.cn/rzxviruscheck?tpl=hebeigjtest request='{"priority": 1, "scanlist": [{"url": "http://222.240.44.115:12180/apks/dee05a6c8f952adba891d345f37dd1dc.apk", "md5": "dee05a6c8f952adba891d345f37dd1dc"}]}'
POST /rzxviruscheck?tpl=hebeigjtest HTTP/1.1
Accept: application/json
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 181
Content-Type: application/json
Host: appsec.1218.com.cn
User-Agent: HTTPie/0.9.2

{
    "request": "{\"priority\": 1, \"scanlist\": [{\"url\": \"http://222.240.44.115:12180/apks/dee05a6c8f952adba891d345f37dd1dc.apk\", \"md5\": \"dee05a6c8f952adba891d345f37dd1dc\"}]}"
}

HTTP/1.1 301 MOVED PERMANENTLY
Connection: keep-alive
Content-Type: text/html; charset=utf-8
Date: Tue, 15 Jan 2019 06:21:01 GMT
Location: http://appsec.1218.com.cn/rzxviruscheck/?tpl=hebeigjtest
Server: nginx/1.7.9
Transfer-Encoding: chunked
X-Frame-Options: SAMEORIGIN


# 构造一个正确的GET请求，使自动跳转到重定向地址
$ http -v http://appsec.1218.com.cn/rzxviruscheck?tpl=hebeigjtest&request='{"priority": 1, "scanlist": [{"url": "http://222.240.44.115:12180/apks/dee05a6c8f952adba891d345f37dd1dc.apk", "md5": "dee05a6c8f952adba891d345f37dd1dc"}]}'
[1] 3390
lanzhiwang@lanzhiwang-desktop:~/work/py_web/multimediaapi_lab$ GET /rzxviruscheck?tpl=hebeigjtest HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: appsec.1218.com.cn
User-Agent: HTTPie/0.9.2



HTTP/1.1 301 MOVED PERMANENTLY
Connection: keep-alive
Content-Type: text/html; charset=utf-8
Date: Tue, 15 Jan 2019 06:21:32 GMT
Location: http://appsec.1218.com.cn/rzxviruscheck/?tpl=hebeigjtest
Server: nginx/1.7.9
Transfer-Encoding: chunked
X-Frame-Options: SAMEORIGIN



^C
[1]+  Done                    http -v http://appsec.1218.com.cn/rzxviruscheck?tpl=hebeigjtest
$ 
# http 工具出现后台执行的情况，重定向成功

```