## SQLAlchemy Log

方法一：将日志只输出到文件中

```
import logging

# 创建处理器，将消息打印到文件
applog_hand = logging.FileHandler("app.log")
applog_hand.setLevel(logging.DEBUG)

sqlalchemy_engine = logging.getLogger('sqlalchemy.engine')
sqlalchemy_engine.addHandler(applog_hand)
sqlalchemy_engine.setLevel(logging.DEBUG)

engine = sqlalchemy.create_engine('postgres://foo/bar', echo=False)
```

方法二：将日志输出到文件和标准输出中

```
import logging

# 创建处理器，将消息打印到文件
applog_hand = logging.FileHandler("app.log")
applog_hand.setLevel(logging.DEBUG)

sqlalchemy_engine = logging.getLogger('sqlalchemy.engine')
sqlalchemy_engine.addHandler(applog_hand)
sqlalchemy_engine.setLevel(logging.DEBUG)

engine = sqlalchemy.create_engine('postgres://foo/bar', echo=True)
```

[参考](https://stackoverflow.com/questions/29114627/how-to-output-sqlalchemy-logger-only-to-a-file)


