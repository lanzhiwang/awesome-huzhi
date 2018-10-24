## nginx + uwsgi + flask

```
# Python 虚拟环境目录
lanzhiwang@lanzhiwang-desktop:~/work/web$ pwd
/home/lanzhiwang/work/web
lanzhiwang@lanzhiwang-desktop:~/work/web$
# 在 Python 虚拟环境中安装相关模块
(web) lanzhiwang@lanzhiwang-desktop:~/work/py_workspace$ pip install Flask
(web) lanzhiwang@lanzhiwang-desktop:~/work/py_workspace$ pip install uwsgi

# 代码目录
(web) lanzhiwang@lanzhiwang-desktop:~/work/py_workspace$ pwd
/home/lanzhiwang/work/py_workspace
(web) lanzhiwang@lanzhiwang-desktop:~/work/py_workspace$ ll
total 20
drwxrwxr-x 2 lanzhiwang lanzhiwang 4096 10月 24 15:09 ./
drwxrwxr-x 8 lanzhiwang lanzhiwang 4096 10月 24 14:11 ../
-rw-rw-r-- 1 lanzhiwang lanzhiwang  173 10月 24 14:20 hello.py
-rw-rw-r-- 1 lanzhiwang lanzhiwang  130 10月 24 14:34 wsgi.ini
-rw-rw-r-- 1 lanzhiwang lanzhiwang   68 10月 24 14:24 wsgi.py
(web) lanzhiwang@lanzhiwang-desktop:~/work/py_workspace$

# flask 应用
(web) lanzhiwang@lanzhiwang-desktop:~/work/py_workspace$ cat hello.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
        return 'Hello, World!'

if __name__ == "__main__":
        app.run(host='0.0.0.0')
(web) lanzhiwang@lanzhiwang-desktop:~/work/py_workspace$
# 测试 flask 应用
(web) lanzhiwang@lanzhiwang-desktop:~/work/py_workspace$ python hello.py
 * Serving Flask app "hello" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

(web) lanzhiwang@lanzhiwang-desktop:~/work/py_workspace$

# wsgi 入口文件
(web) lanzhiwang@lanzhiwang-desktop:~/work/py_workspace$ cat wsgi.py
from hello import app # 从 flask 应用中加载 app 对象

if __name__ == "__main__":
        app.run()
(web) lanzhiwang@lanzhiwang-desktop:~/work/py_workspace$
# 测试 wsgi
(web) lanzhiwang@lanzhiwang-desktop:~/work/py_workspace$ uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app
(web) lanzhiwang@lanzhiwang-desktop:~/work/py_workspace$
# wsgi 配置文件
(web) lanzhiwang@lanzhiwang-desktop:~/work/py_workspace$ cat wsgi.ini
[uwsgi]
uid = lanzhiwang
gid = lanzhiwang
chdir = /home/lanzhiwang/work/py_workspace
wsgi-file = /home/lanzhiwang/work/py_workspace/wsgi.py
module = wsgi:app

master = true
processes = 5

socket = /tmp/uwsgi.sock
chmod-socket = 660
vacuum = true

die-on-term = true
(web) lanzhiwang@lanzhiwang-desktop:~/work/py_workspace$
# 启动 wsgi 进程
(web) lanzhiwang@lanzhiwang-desktop:~/work/py_workspace$ nohup uwsgi --ini wsgi.ini &
lanzhiwang@lanzhiwang-desktop:/etc/nginx/sites-available$ ps -ef | grep -v grep | grep wsgi
lanzhiw+  5588  2260  0 15:25 pts/0    00:00:00 uwsgi --ini wsgi.ini
lanzhiw+  5590  5588  0 15:25 pts/0    00:00:00 uwsgi --ini wsgi.ini
lanzhiw+  5591  5588  0 15:25 pts/0    00:00:00 uwsgi --ini wsgi.ini
lanzhiw+  5592  5588  0 15:25 pts/0    00:00:00 uwsgi --ini wsgi.ini
lanzhiw+  5593  5588  0 15:25 pts/0    00:00:00 uwsgi --ini wsgi.ini
lanzhiw+  5594  5588  0 15:25 pts/0    00:00:00 uwsgi --ini wsgi.ini
lanzhiwang@lanzhiwang-desktop:/etc/nginx/sites-available$
# 配置 nginx
lanzhiwang@lanzhiwang-desktop:/etc/nginx/sites-available$ pwd
/etc/nginx/sites-available
lanzhiwang@lanzhiwang-desktop:/etc/nginx/sites-available$ cat hello_py
upstream flask {
    server unix:///tmp/uwsgi.sock;
}

server {
	listen 8088 default_server;

	root /var/www/html;

	# Add index.php to the list if you are using PHP
	index index.html index.htm index.nginx-debian.html;

	server_name _;

	location / {
                include uwsgi_params;
                uwsgi_pass flask;
                uwsgi_modifier1 30;
	}

}

lanzhiwang@lanzhiwang-desktop:/etc/nginx/sites-available$
lanzhiwang@lanzhiwang-desktop:/etc/nginx/sites-available$ http :8088
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 13
Content-Type: text/html; charset=utf-8
Date: Wed, 24 Oct 2018 07:32:11 GMT
Server: nginx/1.14.0 (Ubuntu)

Hello, World!

lanzhiwang@lanzhiwang-desktop:/etc/nginx/sites-available$

# 将 wsgi 配置成服务
/etc/systemd/system/uwsgi.service
/lib/systemd/system/uwsgi.service

$ cat /etc/systemd/system/uwsgi.service
[Unit]
Description=uWSGI Emperor
After=syslog.target

[Service]
User=lanzhiwang
Group=lanzhiwang
WorkingDirectory=/home/lanzhiwang/work/py_workspace/
Environment="PATH=/home/lanzhiwang/work/web/bin"
ExecStart=/home/lanzhiwang/work/web/bin/uwsgi --ini /home/lanzhiwang/work/py_workspace/wsgi.ini
# Requires systemd version 211 or newer
Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target

$
$ systemctl start uwsgi.service

```