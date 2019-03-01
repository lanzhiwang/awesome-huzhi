## SQLAlchemy Log

方法一：

```
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
```

方法二：

```
engine = sqlalchemy.create_engine('postgres://foo/bar', echo=True)
```