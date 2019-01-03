## Python 函数重载

函数重载：a function that has multiple versions, distinguished by the type of the arguments

示例代码如下所示：

```python
def foo(a, b):
    if isinstance(a, int) and isinstance(b, int):
        """code for two ints"""
        pass

    elif isinstance(a, float) and isinstance(b, float):
        """code for two floats"""
        pass

    elif isinstance(a, str) and isinstance(b, str):
        """code for two strings"""
        pass

    else:
        raise TypeError("unsupported argument types (%s, %s)" % (type(a), type(b)))

```

### Python 实现重载的方法之一

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

registry = {}

class MultiMethod(object):
    def __init__(self, name):
        self.name = name
        self.typemap = {}

    def register(self, types, function):
        if types in self.typemap:
            raise TypeError("duplicate registration")
        self.typemap[types] = function

    def __call__(self, *args):
        types = tuple(arg.__calss__ for arg in args)
        function = self.typemap.get(types)
        if function is None:
            raise TypeError("no match")
        return function(*args)

def multimethod(*types):
    def register(function):
        name = function.__name__
        mm = registry.get(name)
        if mm is None:
            mm = MultiMethod(name)
            registry[name] = mm
        mm.register(types, function)
        return mm
    return register

@multimethod(int, int)
def foo(a, b):
    """code for two ints"""
    pass

@multimethod(float, float)
def foo(a, b):
    """code for two floats"""
    pass

@multimethod(str, str)
def foo(a, b):
    """code for two strings"""
    pass

```



参考：

* https://www.artima.com/weblogs/viewpost.jsp?thread=101605