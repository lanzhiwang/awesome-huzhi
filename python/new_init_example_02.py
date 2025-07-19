class Foo(object):
    def __init__(self, *args, **kwds):
        print("Foo __init__ self: {}".format(self))
        print("Foo __init__ args: {}".format(args))
        print("Foo __init__ kwds: {}".format(kwds))


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


if __name__ == "__main__":
    s1 = Singleton()
    print(s1)

    print("---" * 30)

    s2 = Singleton()
    print(s2)

    print("---" * 30)

    try:
        print(s2.name)
    except AttributeError as e:
        print(e)
    s1.name = "jim"
    print(s2.name)

    print("---" * 30)

    f1 = Foo()
    f2 = Foo()

    try:
        print(f2.name)
    except AttributeError as e:
        print(e)

    f1.name = "tom"

    try:
        print(f2.name)
    except AttributeError as e:
        print(e)


"""
Singleton __new__ cls: <class '__main__.Singleton'>
Singleton __new__ args: ()
Singleton __new__ kwds: {}
before Singleton __new__ cls.__dict__: {
    '__module__': '__main__',
    '__firstlineno__': 1,
    '__new__': <staticmethod(<function Singleton.__new__ at 0x7f5a2e2db560>)>,
    '__init__': <function Singleton.__init__ at 0x7f5a2e2db600>,
    '__static_attributes__': (),
    '__dict__': <attribute '__dict__' of 'Singleton' objects>,
    '__weakref__': <attribute '__weakref__' of 'Singleton' objects>,
    '__doc__': None
}
after Singleton __new__ cls.__dict__: {
    '__module__': '__main__',
    '__firstlineno__': 1,
    '__new__': <staticmethod(<function Singleton.__new__ at 0x7f5a2e2db560>)>,
    '__init__': <function Singleton.__init__ at 0x7f5a2e2db600>,
    '__static_attributes__': (),
    '__dict__': <attribute '__dict__' of 'Singleton' objects>,
    '__weakref__': <attribute '__weakref__' of 'Singleton' objects>,
    '__doc__': None,
    '__it__': <__main__.Singleton object at 0x7f5a2e3e6a50>
}
Singleton __init__ self: <__main__.Singleton object at 0x7f5a2e3e6a50>
Singleton __init__ args: ()
Singleton __init__ kwds: {}
<__main__.Singleton object at 0x7f5a2e3e6a50>
------------------------------------------------------------------------------------------
Singleton __new__ cls: <class '__main__.Singleton'>
Singleton __new__ args: ()
Singleton __new__ kwds: {}
before Singleton __new__ cls.__dict__: {'__module__': '__main__', '__firstlineno__': 1, '__new__': <staticmethod(<function Singleton.__new__ at 0x7f5a2e2db560>)>, '__init__': <function Singleton.__init__ at 0x7f5a2e2db600>, '__static_attributes__': (), '__dict__': <attribute '__dict__' of 'Singleton' objects>, '__weakref__': <attribute '__weakref__' of 'Singleton' objects>, '__doc__': None, '__it__': <__main__.Singleton object at 0x7f5a2e3e6a50>}
Singleton __init__ self: <__main__.Singleton object at 0x7f5a2e3e6a50>
Singleton __init__ args: ()
Singleton __init__ kwds: {}
<__main__.Singleton object at 0x7f5a2e3e6a50>
------------------------------------------------------------------------------------------
'Singleton' object has no attribute 'name'
jim
------------------------------------------------------------------------------------------
Foo __init__ self: <__main__.Foo object at 0x7f84be672ba0>
Foo __init__ args: ()
Foo __init__ kwds: {}
Foo __init__ self: <__main__.Foo object at 0x7f84be544a50>
Foo __init__ args: ()
Foo __init__ kwds: {}
'Foo' object has no attribute 'name'
'Foo' object has no attribute 'name'
"""
