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

'''
'HZ1 CAPABILITY \r\n'

'HZ2 ID ("name" "com.tencent.foxmail" "version" "1.2" "vendor" "Tencent Limited" "contact" "foxmailapp@qq.com")\r\n'

'HZ3 LOGIN "hzhilamp@163.com" "huzhi567233"\r\n'

'HZ4 LIST "" *\r\n'

'HZ5 SELECT "INBOX"\r\n'

'HZ6 FETCH 1:* (UID)\r\n'

'HZ7 UID FETCH 1392612616 (UID BODY.PEEK[])\r\n'

'''

cmd = 'HZ1 CAPABILITY \r\n'
print cmd
s.sendall(cmd)
data = s.recv(10240)
print 'Received:', repr(data)
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

'''
'USER hzhilamp@163.com\r\n'

'PASS huzhi567233\r\n'

'STAT\r\n'

'LIST\r\n'

'RETR 15\r\n'



'''
cmd = 'USER hzhilamp@163.com\r\n'
print cmd
s.sendall(cmd)
data = s.recv(10240)
print 'Received:', repr(data)
s.close()

```