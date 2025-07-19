class TypedProperty(object):
    def __init__(self, name, type, default=None):
        self.name = "_" + name
        self.type = type
        if default is None:
            self.default = type()
        else:
            self.default = default

    def __get__(self, instance, cls):
        print("TypedProperty __get__")
        if instance:
            return getattr(instance, self.name, self.default)
        else:
            return self

    def __set__(self, instance, value):
        print("TypedProperty __set__")
        if not isinstance(value, self.type):
            raise TypeError("Must be a %s!" % self.type)
        setattr(instance, self.name, value)

    def __delete__(self, instance):
        print("TypedProperty __delete__")
        raise AttributeError("Can't delete attribute!")


class Foo(object):
    num1 = TypedProperty("num", int, 42)
    name = TypedProperty("name", str)

    def __init__(self, name, radius):
        self.__name = name
        self.radius = radius

    @property
    def name(self):
        print("Foo property")
        return self.__name

    @name.setter
    def name(self, value):
        print("Foo name.setter")
        if not isinstance(value, str):
            raise TypeError("Must be a string!")
        self.__name = value

    @name.deleter
    def name(self):
        print("Foo name.deleter")
        raise TypeError("Can't delete name!")


if __name__ == "__main__":
    f = Foo("Guido", 4.0)

    n = f.name
    print("n:", n)

    f.name = "Monty"
    n = f.name
    print("n:", n)

    try:
        f.name = 45
    except TypeError as e:
        print(e)

    try:
        del f.name
    except TypeError as e:
        print(e)
    """
    Foo property
    n: Guido
    Foo name.setter
    Foo property
    n: Monty
    Foo name.setter
    Must be a string!
    Foo name.deleter
    Can't delete name!
    """

    num1 = f.num1  # FOO.num1.__get__(f, Foo)
    print("num1:", num1)
    f.num1 = 22  # FOO.num1.__set__(f, 22)
    num1 = f.num1  # FOO.num1.__get__(f, Foo)
    print("num1:", num1)
    try:
        del f.num1  # FOO.num1.__delete__(f)
    except AttributeError as e:
        print(e)
    """
    TypedProperty __get__
    num1: 42
    TypedProperty __set__
    TypedProperty __get__
    num1: 22
    TypedProperty __delete__
    Can't delete attribute!
    """

    print(dir(Foo))
    print(Foo.__dict__)
    print(dir(f))
    print(f.__dict__)
    """
    ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__firstlineno__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__static_attributes__', '__str__', '__subclasshook__', '__weakref__', 'name', 'num1']

    {
        '__module__': '__main__',
        '__firstlineno__': 28,
        'num1': <__main__.TypedProperty object at 0x7f98afb92a50>,
        'name': <property object at 0x7f98afa770b0>,
        '__init__': <function Foo.__init__ at 0x7f98afa879c0>,
        '__static_attributes__': ('__name', 'radius'),
        '__dict__': <attribute '__dict__' of 'Foo' objects>,
        '__weakref__': <attribute '__weakref__' of 'Foo' objects>,
        '__doc__': None
    }

    ['_Foo__name', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__firstlineno__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__static_attributes__', '__str__', '__subclasshook__', '__weakref__', '_num', 'name', 'num1', 'radius']

    {
        '_Foo__name': 'Monty',
        'radius': 4.0,
        '_num': 22
    }
    """
