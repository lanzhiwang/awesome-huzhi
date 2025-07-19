class DocMeta(type):
    def __init__(self, name, bases, attrs):
        print("DocMeta __init__ self: {}".format(self))
        print("DocMeta __init__ name: {}".format(name))
        print("DocMeta __init__ bases: {}".format(bases))
        print("DocMeta __init__ attrs: {}".format(attrs))

        for key, value in attrs.items():
            print("key:", key)
            print("value:", value)

            if key.startswith("__"):
                continue
            if not hasattr(value, "__call__"):
                continue
            if not getattr(value, "__doc__"):
                raise TypeError("%s must have a docstring" % key)
            type.__init__(self, name, bases, attrs)


class Documented(metaclass=DocMeta):
    pass


class Foo(Documented):
    name = "Tom"

    def __init__(self, age):
        self.age = age
        super().__init__()

    def spam(self, a, b):
        """
        spam does somethings
        """
        pass


if __name__ == "__main__":
    f = Foo(10)
    print(f)

"""
DocMeta __init__ self: <class '__main__.Documented'>
DocMeta __init__ name: Documented
DocMeta __init__ bases: ()
DocMeta __init__ attrs: {
    '__module__': '__main__',
    '__qualname__': 'Documented',
    '__firstlineno__': 21,
    '__static_attributes__': ()
}
key: __module__
value: __main__
key: __qualname__
value: Documented
key: __firstlineno__
value: 21
key: __static_attributes__
value: ()

DocMeta __init__ self: <class '__main__.Foo'>
DocMeta __init__ name: Foo
DocMeta __init__ bases: (<class '__main__.Documented'>,)
DocMeta __init__ attrs: {
    '__module__': '__main__',
    '__qualname__': 'Foo',
    '__firstlineno__': 25,
    'name': 'Tom',
    '__init__': <function Foo.__init__ at 0x7f1e83093600>,
    'spam': <function Foo.spam at 0x7f1e830936a0>,
    '__static_attributes__': ('age',),
    '__classcell__': <cell at 0x7f1e8308b910: DocMeta object at 0x563b49ba2690>
}
key: __module__
value: __main__
key: __qualname__
value: Foo
key: __firstlineno__
value: 25
key: name
value: Tom
key: __init__
value: <function Foo.__init__ at 0x7f1e83093600>
key: spam
value: <function Foo.spam at 0x7f1e830936a0>
key: __static_attributes__
value: ('age',)
key: __classcell__
value: <cell at 0x7f1e8308b910: DocMeta object at 0x563b49ba2690>

<__main__.Foo object at 0x7f1e8319ea50>

"""
