## Python 实现单例模式

方法一：使用 \_\_new\_\_()

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Singleton(object):
    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwds)
        return it

    def init(self, *args, **kwds):
        pass


class MySingleton(Singleton):
    def init(self):
        print "calling init"

    def __init__(self):
        print "calling __init__"

x = MySingleton()
"""
calling init
calling __init__
"""
assert x.__class__ is MySingleton

y = MySingleton()
"""
calling __init__
"""

assert x is y
print id(x), id(y)  # 139839519822096 139839519822096

```

方法二：使用装饰器

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps

def singleton(cls):
    instances = {}
    @wraps(cls)
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return getinstance

@singleton
class MyClass(object):
    a = 1

a = MyClass()
b = MyClass()
print id(a), id(b)  # 140033488538768 140033488538768

```

方法三：使用元类

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

# Python2
class MyClass(object):
    __metaclass__ = Singleton

a = MyClass()
b = MyClass()
print id(a), id(b)  # 140534292209808 140534292209808

```

方法四：使用模块

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# mysingleton.py 将代码保存在文件 mysingleton.py 中
class My_Singleton(object):
    def foo(self):
        pass

my_singleton = My_Singleton()


# other.py
# 在另外的模块中导入 mysingleton
from mysingleton import my_singleton

my_singleton.foo()

```

