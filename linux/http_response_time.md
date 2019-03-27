## 诊断 HTTP 响应时间

* Chrome DevTools

* cURL

```bash
$ cat curl.format 
time_namelookup:    %{time_namelookup}\n
time_connect:       %{time_connect}\n
time_appconnect:    %{time_appconnect}\n
time_pretransfer:   %{time_pretransfer}\n
time_redirect:      %{time_redirect}\n
time_starttransfer: %{time_starttransfer}\n
time_total:         %{time_total}\n

$ curl -so /dev/null -w @curl.format https://reorx.com
time_namelookup:    0.126
time_connect:       0.254
time_appconnect:    1.176
time_pretransfer:   1.177
time_redirect:      0.000
time_starttransfer: 1.313
time_total:         1.313
$ 
```

* [httpstat](https://github.com/reorx/httpstat)

```bash
$ python httpstat.py https://reorx.com
Connected to 172.104.82.25:443 from 10.0.3.15:53944

HTTP/1.1 200 OK
Server: nginx/1.10.2
Date: Wed, 27 Mar 2019 02:32:44 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 4117
Connection: keep-alive
Vary: Accept-Encoding
Etag: "77b3634a337edf43f502426b2b702ddcff1ce257"

Body stored in: /tmp/tmpye9LMQ

  DNS Lookup   TCP Connection   TLS Handshake   Server Processing   Content Transfer
[     4ms    |      117ms     |     376ms     |       133ms       |        0ms       ]
             |                |               |                   |                  |
    namelookup:4ms            |               |                   |                  |
                        connect:121ms         |                   |                  |
                                    pretransfer:497ms             |                  |
                                                      starttransfer:630ms            |
                                                                                 total:630ms  

$ 

```