## Python 元类

使用元类的关键技术：
* type
* \_\_new\_\_()
* \_\_init\_\_()
* metaclass

完整示例如下：

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

def make_hook(f):
    f.is_hook = 1
    return f

class MyType(type):
    def __new__(mcls, name, bases, attrs):

        if name.startswith('None'):
            return None

        newattrs = {}
        for attrname, attrvalue in attrs.iteritems():
            print "name: ", attrname
            print "value: ", attrvalue
            if getattr(attrvalue, 'is_hook', 0):
                newattrs['__%s__' % attrname] = attrvalue
            else:
                newattrs[attrname] = attrvalue
        print newattrs

        return super(MyType, mcls).__new__(mcls, name, bases, newattrs)

    def __init__(self, name, bases, attrs):
        super(MyType, self).__init__(name, bases, attrs)
        print "Would register class %s now." % self

    def __add__(self, other):
        class AutoClass(self, other):
            pass
        return AutoClass

    def unregister(self):
        print "Would unregister class %s now." % self


# 通过 __metaclass__ 参数指定类对象的元类
class MyObject:
    __metaclass__ = MyType

print type(MyObject)
print repr(MyObject)

"""
name:  __module__
value:  __main__
name:  __metaclass__
value:  <class '__main__.MyType'>
{'__module__': '__main__', '__metaclass__': <class '__main__.MyType'>}
Would register class <class '__main__.MyObject'> now.
<class '__main__.MyType'>
<class '__main__.MyObject'>
"""


# 测试在元类中直接返回 None
class NoneSample(MyObject):
    pass

print type(NoneSample)
print repr(NoneSample)

"""
<type 'NoneType'>
None
"""

# 测试在元类中添加新的属性
class Example(MyObject):
    def __init__(self, value):
        self.value = value

    @make_hook
    def add(self, other):
        return self.__class__(self.value + other.value)

"""
name:  __module__
value:  __main__
name:  add
value:  <function add at 0x7f525fcb0938>
name:  __init__
value:  <function __init__ at 0x7f525fcb08c0>
{'__module__': '__main__', '__init__': <function __init__ at 0x7f525fcb08c0>, '__add__': <function add at 0x7f525fcb0938>}
Would register class <class '__main__.Example'> now.
"""

Example.unregister()  # Would unregister class <class '__main__.Example'> now.

inst = Example(10)
print inst  # <__main__.Example object at 0x7f478cc051d0>
# inst.unregister()  # AttributeError: 'Example' object has no attribute 'unregister'
print inst + inst  # <__main__.Example object at 0x7fb5abbbb250>


# 测试类对象的 __add__ 方法
class Sibling(MyObject):
    pass

"""
name:  __module__
value:  __main__
{'__module__': '__main__'}
Would register class <class '__main__.Sibling'> now.
"""

ExampleSibling = Example + Sibling
print ExampleSibling  # <class '__main__.AutoClass'>
print ExampleSibling.__mro__
"""
(<class '__main__.AutoClass'>,
<class '__main__.Example'>,
<class '__main__.Sibling'>,
<class '__main__.MyObject'>,
<type 'object'>)
"""

```

#### 参考：

* https://github.com/lanzhiwang/awesome-huzhi/blob/master/new_and_init.md

* https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python

* https://github.com/fluentpython/example-code/tree/master/21-class-metaprog