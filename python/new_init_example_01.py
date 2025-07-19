class inch(float):
    def __new__(cls, arg=0.0):
        print("__new__ cls: {}".format(cls))
        print("__new__ arg: {}".format(arg))
        print("cls.__dict__:", cls.__dict__)
        return float.__new__(cls, arg * 10)

    def __init__(self, arg=0.0):
        print("__init__ self: {}".format(self))
        print("__init__ arg: {}".format(arg))
        print("before self.__dict__:", self.__dict__)
        super().__init__()
        print("after self.__dict__:", self.__dict__)


if __name__ == "__main__":
    f = inch(12)
    print(f)
    """
    __new__ cls: <class '__main__.inch'>
    __new__ arg: 12
    cls.__dict__: {
        '__module__': '__main__',
        '__firstlineno__': 1,
        '__new__': <staticmethod(<function inch.__new__ at 0x7febf1c87560>)>,
        '__init__': <function inch.__init__ at 0x7febf1c87600>,
        '__static_attributes__': (),
        '__dict__': <attribute '__dict__' of 'inch' objects>,
        '__weakref__': <attribute '__weakref__' of 'inch' objects>,
        '__doc__': None
    }
    __init__ self: 120.0
    __init__ arg: 12
    before self.__dict__: {}
    after self.__dict__: {}
    120.0
    """
