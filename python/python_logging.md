## python logging

### logging base

```python
# 日志级别
Level 	  Numeric value
CRITICAL 	50
ERROR 	    40
WARNING 	30
INFO 	    20
DEBUG 	    10
NOTSET 	    0	

# 根记录器
basicConfig([**kwargs])

# 创建或者获取记录器
getLogger([logname])

# 向记录器写入日志消息
critical(fmt [, *args [, exec_info [, extra]]])
error(fmt [, *args [, exec_info [, extra]]])
warning(fmt [, *args [, exec_info [, extra]]])
info(fmt [, *args [, exec_info [, extra]]])
debug(fmt [, *args [, exec_info [, extra]]])
exception(fmt [, *args])
log(level, fmt [, *args [, exec_info [, extra]]])
findCaller()

# 消息筛选器
setLevel(level)
isEnabledFor(level)

addFilter(filter)
removeFilter(filter)

Filters can be used by Handlers and Loggers for more sophisticated filtering than is provided by levels
Filter(logname)
class FilterFunc(logging.Filter):
    def __init__(self, name):
        self.funcName = name
    def filter(self, recode):
        if recode.funcName = self.funcName:
            return False
        return True
    
# LogRecord
LogRecord(name, level, pathname, lineno, msg, args, exc_info, func=None)
LogRecord instances are created automatically by the Logger every time something is logged, and can be created manually via makeLogRecord() (for example, from a pickled event received over the wire).

# 分层记录器
app.net.client
app.net
app
根记录器

propagate 属性
getEffectiveLevel()

# 消息处理器
默认由根记录器处理
addHandler(handler)
removeHandler(handler)

# 预构建的处理器
DatagramHandler(host, port)
FileHandler(filename, mode='a', encoding=None, delay=False)
HTTPHandler(host, url, method='GET')
MemoryHandler(capacity, flushLevel=ERROR, target=None)
NTEventLogHandler(appname, dllname=None, logtype='Application')
RotatingFileHandler(filename, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=0)
SMTPHandler(mailhost, fromaddr, toaddrs, subject, credentials=None, secure=None)
SocketHandler(host, port)
StreamHandler(stream=None)
SysLogHandler(address=('localhost', SYSLOG_UDP_PORT), facility=LOG_USER, socktype=socket.SOCK_DGRAM)
TimedRotatingFileHandler(filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False)
WatchedFileHandler(filename[, mode[, encoding[, delay]]])
NullHandler()

处理器的级别和筛选
setLevel(level)

addFilter(filter)
removeFilter(filter)
自定义处理器的筛选器 

flush()
close()

# 消息格式化
Formatter(fmt=None, datefmt=None)
setFormatter()

给消息添加额外的上下文
方法一：
import logging, socket
basicConfig(
    format = "%(hostname)s %(levelname)-10s $(asctime)s %(message)s" 
)

netinfo = {
    "hostname": socket.gethostname(),
    "ip": socket.gethostbyname(socket.gethostname())
}

log = logging.getLogger('app')
log.critical("Could not connect to server", extra=netinfo)

方法二：
使用 LoggerAdapter(logger, extra)

import logging, socket
basicConfig(
    format = "%(hostname)s %(levelname)-10s $(asctime)s %(message)s" 
)

netinfo = {
    "hostname": socket.gethostname(),
    "ip": socket.gethostbyname(socket.gethostname())
}

log = LoggerAdapter(logging.getLogger('app'), extra=netinfo)
critical("Could not connect to server")

# 实用工具函数
disable(level)
addLevelName(level, levelName)
getLevelName(level)
shutdown()

# 配置文件
logging.config.dictConfig(config)
logging.config.fileConfig(fname, defaults=None, disable_existing_loggers=True)
```

### logging 基本使用

```python
import logging
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logger.debug('debug log')
```

### logging 实践方法

```python
# applogconfig.py
"""该文件只需要在程序中的唯一位置导入一次
"""

import logging
import sys

# 设置消息格式
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

# 创建处理器，将 CRITICAL 级别的数据打印到 stderr
crit_hand = logging.StreamHandler(sys.stderr)
crit_hand.setLevel(logging.CRITICAL)
crit_hand.setFormatter(formatter)

# 创建处理器，将消息打印到文件
applog_hand = logging.FileHandler("app.log")
applog_hand.setFormatter(formatter)

# 创建名为 app 的顶级记录器
app_log = logging.getLogger("app")
app_log.setLevel(logging.INFO)
app_log.addHandler(crit_hand)
app_log.addHandler(applog_hand)

# 修改 app.net 记录器的级别
logging.getLogger("app.net").setLevel(logging.ERROR)


##########################################################################
# 
# 在程序的其他位置可以获取在 applogconfig.py 中定义好的记录器
# 
##########################################################################
import logging
logger = logging.getLogger("app")  # logger = logging.getLogger("app.net")
logger.debug('debug log')
```
