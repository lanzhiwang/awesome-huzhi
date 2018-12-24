## python 描述符

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

class TypedProperty(object):
    def __init__(self, name, type, default=None):
        self.name = "_" + name
        self.type = type
        self.default = default if default else type()
        print "TypedProperty name: %s" % self.name
        print "TypedProperty type: %s" % self.type
        print "TypedProperty default: %s" % self.default

    def __get__(self, instance, cls):
        print "TypedProperty get self: %s" % id(self)
        print "TypedProperty get instance: %s" % id(instance)
        print "TypedProperty get cls: %s" % id(cls)
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError("Must be a %s" % self.type)
        setattr(instance, self.name, value)

    def __delete__(self, instance):
        raise AttributeError("Can't delete attrbute")

class Foo(object):
    name = TypedProperty("name", str, 'foo')
    print "name: %s" % id(name)

    num = TypedProperty("num", int, 42)
    print "num: %s" % id(num)

    def __init__(self):
        pass

print "Foo: %s" % id(Foo)
foo = Foo()
print "foo: %s" % id(foo)
print foo.name
print foo.num

"""
$ python pukep.py
TypedProperty name: _name
TypedProperty type: <type 'str'>
TypedProperty default: foo
name: 139968305185232
TypedProperty name: _num
TypedProperty type: <type 'int'>
TypedProperty default: 42
num: 139968305185296
Foo: 19392304
foo: 139968305185360
TypedProperty get self: 139968305185232
TypedProperty get instance: 139968305185360
TypedProperty get cls: 19392304
foo
TypedProperty get self: 139968305185296
TypedProperty get instance: 139968305185360
TypedProperty get cls: 19392304
42
$

"""


```