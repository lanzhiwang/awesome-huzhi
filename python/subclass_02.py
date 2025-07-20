class Foo(object):
    def spam(self, a, b):
        pass


class FooProxy(object):
    def __init__(self, f):
        self.f = f

    def spam(self, a, b):
        return self.f.spam(a, b)


f = Foo()
g = FooProxy(f)
print(isinstance(g, Foo))  # False


class IClass(object):
    def __init__(self):
        self.implementors = set()

    def register(self, C):
        self.implementors.add(C)

    def __instancecheck__(self, instance):
        print("instance:", instance)
        print("type(instance):", type(instance))
        return self.__subclasscheck__(type(instance))

    def __subclasscheck__(self, subclass):
        print("subclass:", subclass)
        print("subclass.mro:", subclass.mro())
        return any(c in self.implementors for c in subclass.mro())


IFoo = IClass()
IFoo.register(Foo)
IFoo.register(FooProxy)

print(isinstance(f, IFoo))
"""
instance: <__main__.Foo object at 0x7f782b75aa50>
type(instance): <class '__main__.Foo'>
subclass: <class '__main__.Foo'>
subclass.mro: [<class '__main__.Foo'>, <class 'object'>]
True
"""

print(isinstance(g, IFoo))
"""
instance: <__main__.FooProxy object at 0x7f782b75aba0>
type(instance): <class '__main__.FooProxy'>
subclass: <class '__main__.FooProxy'>
subclass.mro: [<class '__main__.FooProxy'>, <class 'object'>]
True
"""

print(issubclass(Foo, IFoo))
"""
subclass: <class '__main__.Foo'>
subclass.mro: [<class '__main__.Foo'>, <class 'object'>]
True
"""

print(issubclass(FooProxy, IFoo))
"""
subclass: <class '__main__.FooProxy'>
subclass.mro: [<class '__main__.FooProxy'>, <class 'object'>]
True
"""
