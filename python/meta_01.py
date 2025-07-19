class DocMeta(type):
    def __new__(cls, name, bases, attrs):
        print("DocMeta __new__ cls: {}".format(cls))
        print("DocMeta __new__ name: {}".format(name))
        print("DocMeta __new__ bases: {}".format(bases))
        print("DocMeta __new__ attrs: {}".format(attrs))
        return type.__new__(cls, name, bases, attrs)

    def __init__(self, name, bases, attrs):
        print("DocMeta __init__ self: {}".format(self))
        print("DocMeta __init__ name: {}".format(name))
        print("DocMeta __init__ bases: {}".format(bases))
        print("DocMeta __init__ attrs: {}".format(attrs))
        type.__init__(self, name, bases, attrs)


class Documented(metaclass=DocMeta):
    pass


class Foo(Documented):

    def spam(self, a, b):
        """
        spam does somethings
        """
        pass


if __name__ == "__main__":
    f = Foo()
    print(f)

"""
DocMeta __new__ cls: <class '__main__.DocMeta'>
DocMeta __new__ name: Documented
DocMeta __new__ bases: ()
DocMeta __new__ attrs: {'__module__': '__main__', '__qualname__': 'Documented', '__firstlineno__': 16, '__static_attributes__': ()}

DocMeta __init__ self: <class '__main__.Documented'>
DocMeta __init__ name: Documented
DocMeta __init__ bases: ()
DocMeta __init__ attrs: {'__module__': '__main__', '__qualname__': 'Documented', '__firstlineno__': 16, '__static_attributes__': ()}

DocMeta __new__ cls: <class '__main__.DocMeta'>
DocMeta __new__ name: Foo
DocMeta __new__ bases: (<class '__main__.Documented'>,)
DocMeta __new__ attrs: {'__module__': '__main__', '__qualname__': 'Foo', '__firstlineno__': 22, 'spam': <function Foo.spam at 0x7fe772d936a0>, '__static_attributes__': ()}

DocMeta __init__ self: <class '__main__.Foo'>
DocMeta __init__ name: Foo
DocMeta __init__ bases: (<class '__main__.Documented'>,)
DocMeta __init__ attrs: {'__module__': '__main__', '__qualname__': 'Foo', '__firstlineno__': 22, 'spam': <function Foo.spam at 0x7fe772d936a0>, '__static_attributes__': ()}

<__main__.Foo object at 0x7fe772e9ea50>

"""
