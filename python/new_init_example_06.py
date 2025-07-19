class Singleton(object):
    def __new__(cls, *args, **kwds):
        print("Singleton __new__ cls: {}".format(cls))
        print("Singleton __new__ args: {}".format(args))
        print("Singleton __new__ kwds: {}".format(kwds))

        print("before Singleton __new__ cls.__dict__: {}".format(cls.__dict__))

        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)

        print("after Singleton __new__ cls.__dict__: {}".format(cls.__dict__))

        return it

    def __init__(self, *args, **kwds):
        print("Singleton __init__ self: {}".format(self))
        print("Singleton __init__ args: {}".format(args))
        print("Singleton __init__ kwds: {}".format(kwds))


class MySingleton(Singleton):

    def __new__(cls, *args, **kwds):
        print("MySingleton __new__ cls: {}".format(cls))
        print("MySingleton __new__ args: {}".format(args))
        print("MySingleton __new__ kwds: {}".format(kwds))
        return super().__new__(cls, *args, **kwds)

    def __init__(self, *args, **kwds):
        print("MySingleton __init__ self: {}".format(self))
        print("MySingleton __init__ args: {}".format(args))
        print("MySingleton __init__ kwds: {}".format(kwds))
        super().__init__(*args, **kwds)


if __name__ == "__main__":
    s1 = MySingleton()
    print(s1)

    print("---" * 30)

    s2 = MySingleton()
    print(s2)

    print("---" * 30)

    try:
        print(s2.name)
    except AttributeError as e:
        print(e)
    s1.name = "jim"
    print(s2.name)

    print("---" * 30)

"""
MySingleton __new__ cls: <class '__main__.MySingleton'>
MySingleton __new__ args: ()
MySingleton __new__ kwds: {}
Singleton __new__ cls: <class '__main__.MySingleton'>
Singleton __new__ args: ()
Singleton __new__ kwds: {}
before Singleton __new__ cls.__dict__: {'__module__': '__main__', '__firstlineno__': 24, '__new__': <staticmethod(<function MySingleton.__new__ at 0x7faed14db6a0>)>, '__init__': <function MySingleton.__init__ at 0x7faed14db740>, '__static_attributes__': (), '__doc__': None}
after Singleton __new__ cls.__dict__: {'__module__': '__main__', '__firstlineno__': 24, '__new__': <staticmethod(<function MySingleton.__new__ at 0x7faed14db6a0>)>, '__init__': <function MySingleton.__init__ at 0x7faed14db740>, '__static_attributes__': (), '__doc__': None, '__it__': <__main__.MySingleton object at 0x7faed15e2a50>}
MySingleton __init__ self: <__main__.MySingleton object at 0x7faed15e2a50>
MySingleton __init__ args: ()
MySingleton __init__ kwds: {}
Singleton __init__ self: <__main__.MySingleton object at 0x7faed15e2a50>
Singleton __init__ args: ()
Singleton __init__ kwds: {}
<__main__.MySingleton object at 0x7faed15e2a50>
------------------------------------------------------------------------------------------
MySingleton __new__ cls: <class '__main__.MySingleton'>
MySingleton __new__ args: ()
MySingleton __new__ kwds: {}
Singleton __new__ cls: <class '__main__.MySingleton'>
Singleton __new__ args: ()
Singleton __new__ kwds: {}
before Singleton __new__ cls.__dict__: {'__module__': '__main__', '__firstlineno__': 24, '__new__': <staticmethod(<function MySingleton.__new__ at 0x7faed14db6a0>)>, '__init__': <function MySingleton.__init__ at 0x7faed14db740>, '__static_attributes__': (), '__doc__': None, '__it__': <__main__.MySingleton object at 0x7faed15e2a50>}
MySingleton __init__ self: <__main__.MySingleton object at 0x7faed15e2a50>
MySingleton __init__ args: ()
MySingleton __init__ kwds: {}
Singleton __init__ self: <__main__.MySingleton object at 0x7faed15e2a50>
Singleton __init__ args: ()
Singleton __init__ kwds: {}
<__main__.MySingleton object at 0x7faed15e2a50>
------------------------------------------------------------------------------------------
'MySingleton' object has no attribute 'name'
jim
------------------------------------------------------------------------------------------
"""
