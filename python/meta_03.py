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
    def __new__(cls, *args, **kwds):
        print("Documented __new__ cls: {}".format(cls))
        print("Documented __new__ args: {}".format(args))
        print("Documented __new__ kwds: {}".format(kwds))

        return super().__new__(cls, *args, **kwds)

    def __init__(self, *args, **kwds):
        print("Documented __init__ self: {}".format(self))
        print("Documented __init__ args: {}".format(args))
        print("Documented __init__ kwds: {}".format(kwds))

        super().__init__(*args, **kwds)


class Foo(Documented):

    def __new__(cls, *args, **kwds):
        print("Foo __new__ cls: {}".format(cls))
        print("Foo __new__ args: {}".format(args))
        print("Foo __new__ kwds: {}".format(kwds))

        return super().__new__(cls, *args, **kwds)

    def __init__(self, *args, **kwds):
        print("Foo __init__ self: {}".format(self))
        print("Foo __init__ args: {}".format(args))
        print("Foo __init__ kwds: {}".format(kwds))

        super().__init__(*args, **kwds)

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
DocMeta __new__ attrs: {'__module__': '__main__', '__qualname__': 'Documented', '__firstlineno__': 17, '__new__': <function Documented.__new__ at 0x7f3a76b476a0>, '__init__': <function Documented.__init__ at 0x7f3a76b47740>, '__static_attributes__': (), '__classcell__': <cell at 0x7f3a76b54670: empty>}

DocMeta __init__ self: <class '__main__.Documented'>
DocMeta __init__ name: Documented
DocMeta __init__ bases: ()
DocMeta __init__ attrs: {'__module__': '__main__', '__qualname__': 'Documented', '__firstlineno__': 17, '__new__': <function Documented.__new__ at 0x7f3a76b476a0>, '__init__': <function Documented.__init__ at 0x7f3a76b47740>, '__static_attributes__': (), '__classcell__': <cell at 0x7f3a76b54670: DocMeta object at 0x5647359aed30>}

DocMeta __new__ cls: <class '__main__.DocMeta'>
DocMeta __new__ name: Foo
DocMeta __new__ bases: (<class '__main__.Documented'>,)
DocMeta __new__ attrs: {'__module__': '__main__', '__qualname__': 'Foo', '__firstlineno__': 33, '__new__': <function Foo.__new__ at 0x7f3a76b477e0>, '__init__': <function Foo.__init__ at 0x7f3a76b47880>, 'spam': <function Foo.spam at 0x7f3a76b47920>, '__static_attributes__': (), '__classcell__': <cell at 0x7f3a76b54700: empty>}

DocMeta __init__ self: <class '__main__.Foo'>
DocMeta __init__ name: Foo
DocMeta __init__ bases: (<class '__main__.Documented'>,)
DocMeta __init__ attrs: {'__module__': '__main__', '__qualname__': 'Foo', '__firstlineno__': 33, '__new__': <function Foo.__new__ at 0x7f3a76b477e0>, '__init__': <function Foo.__init__ at 0x7f3a76b47880>, 'spam': <function Foo.spam at 0x7f3a76b47920>, '__static_attributes__': (), '__classcell__': <cell at 0x7f3a76b54700: DocMeta object at 0x5647359c49b0>}

Foo __new__ cls: <class '__main__.Foo'>
Foo __new__ args: ()
Foo __new__ kwds: {}

Documented __new__ cls: <class '__main__.Foo'>
Documented __new__ args: ()
Documented __new__ kwds: {}

Foo __init__ self: <__main__.Foo object at 0x7f3a76c52a50>
Foo __init__ args: ()
Foo __init__ kwds: {}

Documented __init__ self: <__main__.Foo object at 0x7f3a76c52a50>
Documented __init__ args: ()
Documented __init__ kwds: {}

<__main__.Foo object at 0x7f3a76c52a50>

"""
