# new 和 init 使用示例

## 修改内置类型

```python
class inch(float):
    def __new__(cls, arg=0.0):
        print("__new__ cls: {}".format(cls))
        print("__new__ arg: {}".format(arg))
        return float.__new__(cls, arg * 10)


f = inch(12)
print(f)

"""
__new__ cls: <class '__main__.inch'>
__new__ arg: 12
120.0
"""

###############################################################



f = inch(12)
print f

# output:
__init__ arg: 12
12.0

```

## 修改内置类型，同时使用 new 和 init

```python
###############################################################

class inch(float):
    def __new__(cls, arg=0.0):
        print '__new__ arg: {}'.format(arg)
        return float.__new__(cls, arg * 10)

    def __init__(self, arg=0.0):
        print '__init__ arg: {}'.format(arg)
        float.__init__(self, arg * 10)

f = inch(12)
print f

# output:
__new__ arg: 12
__init__ arg: 12
120.0

```

## 自定义类




```python

###############################################################
# 1. MySingleton 继承 Singleton
# 2. MySingleton 和 Singleton 两个自定义类都有 new 和 init 方法
###############################################################

class Singleton(object):
    def __new__(cls, *args, **kwds):
        print 'Singleton __new__ args: {}'.format(args)
        print 'Singleton __new__ kwds: {}'.format(kwds)

        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        return it

    def __init__(self, *args, **kwds):
        print 'Singleton __init__ args: {}'.format(args)
        print 'Singleton __init__ kwds: {}'.format(kwds)


class MySingleton(Singleton):

    def __new__(cls, *args, **kwds):
        print 'MySingleton __new__ args: {}'.format(args)
        print 'MySingleton __new__ kwds: {}'.format(kwds)

    def __init__(self, *args, **kwds):
        print 'MySingleton __init__ args: {}'.format(args)
        print 'MySingleton __init__ kwds: {}'.format(kwds)
        super(MySingleton, self).__init__(*args, **kwds)

s = MySingleton()
print s

# output:
MySingleton __new__ args: ()
MySingleton __new__ kwds: {}
None

###############################################################
# 1. 在 MySingleton 类的 new 方法中调用 Singleton 类的 new 方法
###############################################################

class Singleton(object):
    def __new__(cls, *args, **kwds):
        print 'Singleton __new__ args: {}'.format(args)
        print 'Singleton __new__ kwds: {}'.format(kwds)

        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        return it

    def __init__(self, *args, **kwds):
        print 'Singleton __init__ args: {}'.format(args)
        print 'Singleton __init__ kwds: {}'.format(kwds)


class MySingleton(Singleton):

    def __new__(cls, *args, **kwds):
        print 'MySingleton __new__ args: {}'.format(args)
        print 'MySingleton __new__ kwds: {}'.format(kwds)
        Singleton.__new__(cls, *args, **kwds)

    def __init__(self, *args, **kwds):
        print 'MySingleton __init__ args: {}'.format(args)
        print 'MySingleton __init__ kwds: {}'.format(kwds)
        super(MySingleton, self).__init__(*args, **kwds)

s = MySingleton()
print s

# output:
MySingleton __new__ args: ()
MySingleton __new__ kwds: {}
Singleton __new__ args: ((), {})
Singleton __new__ kwds: {}
None

###############################################################
# 1. 在 MySingleton 类的 new 方法中调用 Singleton 类的 new 方法
# 2. 返回 return
###############################################################

class Singleton(object):
    def __new__(cls, *args, **kwds):
        print 'Singleton __new__ args: {}'.format(args)
        print 'Singleton __new__ kwds: {}'.format(kwds)

        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        return it

    def __init__(self, *args, **kwds):
        print 'Singleton __init__ args: {}'.format(args)
        print 'Singleton __init__ kwds: {}'.format(kwds)


class MySingleton(Singleton):

    def __new__(cls, *args, **kwds):
        print 'MySingleton __new__ args: {}'.format(args)
        print 'MySingleton __new__ kwds: {}'.format(kwds)
        return Singleton.__new__(cls, *args, **kwds)

    def __init__(self, *args, **kwds):
        print 'MySingleton __init__ args: {}'.format(args)
        print 'MySingleton __init__ kwds: {}'.format(kwds)
        super(MySingleton, self).__init__(*args, **kwds)

s = MySingleton()
print s

# output:
MySingleton __new__ args: ()
MySingleton __new__ kwds: {}
Singleton __new__ args: ()
Singleton __new__ kwds: {}
MySingleton __init__ args: ()
MySingleton __init__ kwds: {}
Singleton __init__ args: ()
Singleton __init__ kwds: {}
<__main__.MySingleton object at 0x7f9d978dcdd0>

###############################################################
# 1. 去掉 MySingleton 类中的 new 方法
###############################################################

class Singleton(object):
    def __new__(cls, *args, **kwds):
        print 'Singleton __new__ args: {}'.format(args)
        print 'Singleton __new__ kwds: {}'.format(kwds)

        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        return it

    def __init__(self, *args, **kwds):
        print 'Singleton __init__ args: {}'.format(args)
        print 'Singleton __init__ kwds: {}'.format(kwds)


class MySingleton(Singleton):
    
    def __init__(self, *args, **kwds):
        print 'MySingleton __init__ args: {}'.format(args)
        print 'MySingleton __init__ kwds: {}'.format(kwds)
        super(MySingleton, self).__init__(*args, **kwds)

s = MySingleton()
print s

# output:
Singleton __new__ args: ()
Singleton __new__ kwds: {}
MySingleton __init__ args: ()
MySingleton __init__ kwds: {}
Singleton __init__ args: ()
Singleton __init__ kwds: {}
<__main__.MySingleton object at 0x7f45021b3d90>

```
