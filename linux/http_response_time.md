## 诊断 HTTP 响应时间

* Chrome DevTools

* cURL

```bash
# 参考
# https://blog.kenweiner.com/2014/11/http-request-timings-with-curl.html

$ cat curl.format 
time_namelookup:    %{time_namelookup}\n
time_connect:       %{time_connect}\n
time_appconnect:    %{time_appconnect}\n
time_pretransfer:   %{time_pretransfer}\n
time_redirect:      %{time_redirect}\n
time_starttransfer: %{time_starttransfer}\n
time_total:         %{time_total}\n
speed_download:     %{speed_download}\n
speed_upload:       %{speed_upload}\n
remote_ip:          %{remote_ip}\n
remote_port:        %{remote_port}\n
local_ip:           %{local_ip}\n
local_port:         %{local_port}\n
$ 
$ curl -so /dev/null -w @curl.format https://reorx.com
time_namelookup:    0.004
time_connect:       0.121
time_appconnect:    0.850
time_pretransfer:   0.850
time_redirect:      0.000
time_starttransfer: 0.970
time_total:         0.970
speed_download:     4245.000
speed_upload:       0.000
remote_ip:          172.104.82.25
remote_port:        443
local_ip:           10.0.3.15
local_port:         53948
$ 

$ curl -w '\ncontent_type=%{content_type}\nfilename_effective=%{filename_effective}\nftp_entry_path=%{ftp_entry_path}\nhttp_code=%{http_code}\nhttp_connect=%{http_connect}\nlocal_ip=%{local_ip}\nlocal_port=%{local_port}\nnum_connects=%{num_connects}\nnum_redirects=%{num_redirects}\nredirect_url=%{redirect_url}\nremote_ip=%{remote_ip}\nremote_port=%{remote_port}\nsize_download=%{size_download}\nsize_header=%{size_header}\nsize_request=%{size_request}\nsize_upload=%{size_upload}\nspeed_download=%{speed_download}\nspeed_upload=%{speed_upload}\nssl_verify_result=%{ssl_verify_result}\ntime_appconnect=%{time_appconnect}\ntime_connect=%{time_connect}\ntime_namelookup=%{time_namelookup}\ntime_pretransfer=%{time_pretransfer}\ntime_redirect=%{time_redirect}\ntime_starttransfer=%{time_starttransfer}\ntime_total=%{time_total}\nurl_effective=%{url_effective}\n\n' -o /dev/null -s 'https://www.baidu.com/'

content_type=text/html
filename_effective=/dev/null
ftp_entry_path=
http_code=200
http_connect=000
local_ip=10.0.3.15
local_port=56762
num_connects=1
num_redirects=0
redirect_url=
remote_ip=180.97.33.108
remote_port=443
size_download=2443
size_header=400
size_request=77
size_upload=0
speed_download=15426.000
speed_upload=0.000
ssl_verify_result=0
time_appconnect=0.143
time_connect=0.018
time_namelookup=0.004
time_pretransfer=0.143
time_redirect=0.000
time_starttransfer=0.158
time_total=0.158
url_effective=https://www.baidu.com/

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