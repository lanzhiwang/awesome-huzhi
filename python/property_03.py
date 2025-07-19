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

    def __init__(self, name, radius):
        self.name = name
        self.radius = radius

    def __getattribute__(self, name):
        print("Foo __getattribute__")
        return super().__getattribute__(name)

    def __getattr__(self, name):
        print("Foo __getattr__")
        return super().__getattr__(name)

    def __setattr__(self, name, value):
        print("Foo __setattr__")
        super().__setattr__(name, value)

    def __delattr__(self, name):
        print("Foo __delattr__")
        super().__delattr__(name)


if __name__ == "__main__":
    f = Foo("Guido", 4.0)
    """
    Foo __setattr__
    Foo __setattr__
    """

    print(dir(f))
    """
    Foo __getattribute__
    Foo __getattribute__
    ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__firstlineno__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__static_attributes__', '__str__', '__subclasshook__', '__weakref__', 'name', 'radius']
    """
    print(f.__dict__)
    """
    Foo __getattribute__
    {'name': 'Guido', 'radius': 4.0}
    """

    n = f.name
    print("n:", n)
    """
    Foo __getattribute__
    n: Guido
    """

    try:
        print(f.notexits)
    except AttributeError as e:
        print(e)
    """
    Foo __getattribute__
    Foo __getattr__
    'super' object has no attribute '__getattr__'
    """

    f.name = "Monty"
    """
    Foo __setattr__
    """
    n = f.name
    print("n:", n)
    """
    Foo __getattribute__
    n: Monty
    """

    print("---" * 30)

    f.notexits = "notexits"
    print(f.notexits)
    print(f.__dict__)
    """
    Foo __setattr__
    Foo __getattribute__
    notexits
    Foo __getattribute__
    {'name': 'Monty', 'radius': 4.0, 'notexits': 'notexits'}
    """

    delattr(f, "name")
    """
    Foo __delattr__
    """
