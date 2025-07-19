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

    def __init__(self, name, radius, age):
        self.__name = name
        self.radius = radius
        self.age = age

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
    f = Foo("Guido", 4.0, 30)
    """
    Foo __setattr__
    Foo __setattr__
    Foo __setattr__
    """

    print("---" * 30)

    n = f.name
    print("n:", n)
    """
    Foo __getattribute__
    Foo property
    Foo __getattribute__
    n: Guido
    """

    print("---" * 30)

    print(f.num1)
    """
    Foo __getattribute__
    TypedProperty __get__
    Foo __getattribute__
    Foo __getattr__
    42
    """

    print("---" * 30)

    print(f.age)
    """
    Foo __getattribute__
    30
    """

    print("---" * 30)

    try:
        print(f.notexits)
    except AttributeError as e:
        print(e)
    """
    Foo __getattribute__
    Foo __getattr__
    'super' object has no attribute '__getattr__'
    """

    print("---" * 30)

    f.name = "Monty"
    """
    Foo __setattr__
    Foo name.setter
    Foo __setattr__
    """

    print("---" * 30)

    f.num1 = 22
    """
    Foo __setattr__
    TypedProperty __set__
    Foo __setattr__
    """

    print("---" * 30)

    try:
        # del f.name
        delattr(f, "name")
    except TypeError as e:
        print(e)
    """
    Foo __delattr__
    Foo name.deleter
    Can't delete name!
    """

    print("---" * 30)

    try:
        # del f.num1  # FOO.num1.__delete__(f)
        delattr(f, "num1")
    except AttributeError as e:
        print(e)
    """
    Foo __delattr__
    TypedProperty __delete__
    Can't delete attribute!
    """
