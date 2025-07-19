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


class MySingleton(Singleton):

    def __new__(cls, *args, **kwds):
        print("MySingleton __new__ cls: {}".format(cls))
        print("MySingleton __new__ args: {}".format(args))
        print("MySingleton __new__ kwds: {}".format(kwds))

    def __init__(self, *args, **kwds):
        print("MySingleton __init__ self: {}".format(self))
        print("MySingleton __init__ args: {}".format(args))
        print("MySingleton __init__ kwds: {}".format(kwds))
        super().__init__(*args, **kwds)


if __name__ == "__main__":
    s1 = MySingleton()
    print(s1)

    print("---" * 30)

"""
MySingleton __new__ cls: <class '__main__.MySingleton'>
MySingleton __new__ args: ()
MySingleton __new__ kwds: {}
None
------------------------------------------------------------------------------------------
"""
