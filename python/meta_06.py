class TypedProperty(object):
    def __init__(self, type, default=None):
        self.name = None
        self.type = type
        if default is None:
            self.default = type()
        else:
            self.default = default

    def __get__(self, instance, cls):
        if instance:
            return getattr(instance, self.name, self.default)
        else:
            return self

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError("Must be a %s!" % self.type)
        setattr(instance, self.name, value)

    def __delete__(self, instance):
        raise AttributeError("Can't delete attribute!")


class TypedMeta(type):
    def __new__(cls, name, bases, attrs):
        print("TypedMeta __new__ cls: {}".format(cls))
        print("TypedMeta __new__ name: {}".format(name))
        print("TypedMeta __new__ bases: {}".format(bases))
        print("TypedMeta __new__ attrs: {}".format(attrs))

        slots = []
        for key, value in attrs.items():
            print("key:", key)
            print("value:", value)
            if isinstance(value, TypedProperty):
                value.name = "_" + key
                slots.append(value.name)
        attrs["__slots__"] = slots

        return type.__new__(cls, name, bases, attrs)


class Typed(metaclass=TypedMeta):
    pass


class Foo(Typed):
    name = TypedProperty(str, "Tom")
    num = TypedProperty(int, 42)


if __name__ == "__main__":
    f = Foo()
    print(f)
    print(f.name)
    print(f.num)
    print(f.__slots__)

"""
TypedMeta __new__ cls: <class '__main__.TypedMeta'>
TypedMeta __new__ name: Typed
TypedMeta __new__ bases: ()
TypedMeta __new__ attrs: {
    '__module__': '__main__',
    '__qualname__': 'Typed',
    '__firstlineno__': 44,
    '__static_attributes__': ()
}
key: __module__
value: __main__
key: __qualname__
value: Typed
key: __firstlineno__
value: 44
key: __static_attributes__
value: ()

TypedMeta __new__ cls: <class '__main__.TypedMeta'>
TypedMeta __new__ name: Foo
TypedMeta __new__ bases: (<class '__main__.Typed'>,)
TypedMeta __new__ attrs: {
    '__module__': '__main__',
    '__qualname__': 'Foo',
    '__firstlineno__': 48,
    'name': <__main__.TypedProperty object at 0x7fb6d11eeba0>,
    'num': <__main__.TypedProperty object at 0x7fb6d10c0a50>,
    '__static_attributes__': ()
}
key: __module__
value: __main__
key: __qualname__
value: Foo
key: __firstlineno__
value: 48
key: name
value: <__main__.TypedProperty object at 0x7fb6d11eeba0>
key: num
value: <__main__.TypedProperty object at 0x7fb6d10c0a50>
key: __static_attributes__
value: ()

<__main__.Foo object at 0x7fb6d10f0580>

Tom
42
['_name', '_num']

"""
