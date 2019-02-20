## email client

### imap

参考：

https://github.com/python/cpython/blob/2.7/Lib/imaplib.py

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socket import *
s = socket(AF_INET, SOCK_STREAM)
s.connect(("imap.163.com", 143))

cmd = 'HZ1 CAPABILITY \r\n'
print cmd
s.sendall(cmd)
data = s.recv(10240)
print 'Received:', repr(data)
print '===================='

cmd = 'HZ2 ID ("name" "com.tencent.foxmail" "version" "1.2" "vendor" "Tencent Limited" "contact" "foxmailapp@qq.com")\r\n'
print cmd
s.sendall(cmd)
data = s.recv(10240)
print "Received:", repr(data)
print "===================="

cmd = 'HZ3 LOGIN "hzhilamp@163.com" "huzhi567233"\r\n'
print cmd
s.sendall(cmd)
data = s.recv(10240)
print "Received:", repr(data)
print "===================="

cmd = 'HZ4 LIST "" *\r\n'
print cmd
s.sendall(cmd)
data = s.recv(10240)
print "Received:", repr(data)
print "===================="

cmd = 'HZ5 SELECT "INBOX"\r\n'
print cmd
s.sendall(cmd)
data = s.recv(10240)
print "Received:", repr(data)
print "===================="

cmd = 'HZ6 FETCH 1:* (UID)\r\n'
print cmd
s.sendall(cmd)
data = s.recv(1024000)
print "Received:", repr(data)
print "===================="

data = s.recv(1024000)
print "Received:", repr(data)
print "===================="

cmd = 'HZ7 UID FETCH 1392612616 (UID BODY.PEEK[])\r\n'
print cmd
s.sendall(cmd)
data = s.recv(1024000)
print "Received:", repr(data)
print "===================="

s.close()


```

### pop3

参考：

https://github.com/python/cpython/blob/2.7/Lib/poplib.py

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socket import *
s = socket(AF_INET, SOCK_STREAM)
s.connect(("pop.163.com", 110))

cmd = 'USER hzhilamp@163.com\r\n'
print cmd
s.sendall(cmd)
data = s.recv(10240)
print 'Received:', repr(data)
print '===================='

cmd = 'PASS huzhi567233\r\n'
print cmd
s.sendall(cmd)
data = s.recv(10240)
print "Received:", repr(data)
print "===================="

cmd = 'STAT\r\n'
print cmd
s.sendall(cmd)
data = s.recv(10240)
print "Received:", repr(data)
print "===================="

cmd = 'LIST\r\n'
print cmd
s.sendall(cmd)
data = s.recv(10240)
print "Received:", repr(data)
print "===================="

cmd = 'RETR 15\r\n'
print cmd
s.sendall(cmd)
data = s.recv(1024000)
print "Received:", repr(data)
print "===================="

data = s.recv(1024000)
print "Received:", repr(data)
print "===================="

data = s.recv(1024000)
print "Received:", repr(data)
print "===================="

s.close()

```