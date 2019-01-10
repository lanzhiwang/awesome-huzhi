## Difference between \_\_getattr\_\_ vs \_\_getattribute\_\_

A key difference between `__getattr__` and `__getattribute__` is that `__getattr__` is only invoked if the attribute wasn't found the usual ways. It's good for implementing a fallback for missing attributes, and is probably the one of two you want.

`__getattribute__` is invoked before looking at the actual attributes on the object, and so can be tricky to implement correctly. You can end up in infinite recursions very easily.

New-style classes derive from object, old-style classes are those in Python 2.x with no explicit base class. But the distinction between old-style and new-style classes is not the important one when choosing between `__getattr__` and `__getattribute__`.

You almost certainly want `__getattr__`.

Lets see some simple examples of both `__getattr__` and `__getattribute__` magic methods.

### \_\_getattr\_\_

Python will call  `__getattr__` method whenever you request an attribute that hasn't already been defined. In the following example my class Count has no `__getattr__` method. Now in main when I try to access both obj1.mymin and obj1.mymax attributes everything works fine. But when I try to access obj1.mycurrent attribute -- Python gives me AttributeError: 'Count' object has no attribute 'mycurrent'

```python
class Count():
    def __init__(self,mymin,mymax):
        self.mymin=mymin
        self.mymax=mymax

obj1 = Count(1,10)
print(obj1.mymin)
print(obj1.mymax)
print(obj1.mycurrent)  --> AttributeError: 'Count' object has no attribute 'mycurrent'
```

Now my class Count has `__getattr__` method. Now when I try to access  obj1.mycurrent attribute -- python returns me whatever I have implemented in my `__getattr__` method. In my example whenever I try to call an attribute which doesn't exist, python creates that attribute and set it to integer value 0.

```python
class Count:
    def __init__(self,mymin,mymax):
        self.mymin=mymin
        self.mymax=mymax    

    def __getattr__(self, item):
        self.__dict__[item]=0
        return 0

obj1 = Count(1,10)
print(obj1.mymin)
print(obj1.mymax)
print(obj1.mycurrent1)
```

### \_\_getattribute\_\_

Now lets see the `__getattribute__` method. If you have  `__getattribute__` method in your class, python invokes this method for every attribute regardless whether it exists or not. So why we need `__getattribute__` method? One good reason is that you can prevent access to attributes and make them more secure as shown in the following example.

Whenever someone try to access my attributes that starts with substring 'cur' python raises AttributeError exception. Otherwise it returns that attribute.

```python
class Count:

    def __init__(self,mymin,mymax):
        self.mymin=mymin
        self.mymax=mymax
        self.current=None

    def __getattribute__(self, item):
        if item.startswith('cur'):
            raise AttributeError
        return object.__getattribute__(self,item) 
        # or you can use ---return super().__getattribute__(item)

obj1 = Count(1,10)
print(obj1.mymin)
print(obj1.mymax)
print(obj1.current)
```

Important: In order to avoid infinite recursion in `__getattribute__` method, its implementation should always call the base class method with the same name to access any attributes it needs. For example: object.\_\_getattribute\_\_(self, name) or  super().\_\_getattribute\_\_(item) and not self.\_\_dict\_\_[item]

### IMPORTANT

If your class contain both getattr and getattribute magic methods then  `__getattribute__` is called first. But if  `__getattribute__` raises  AttributeError exception then the exception will be ignored and `__getattr__` method will be invoked. See the following example:

```python
class Count(object):

    def __init__(self,mymin,mymax):
        self.mymin=mymin
        self.mymax=mymax
        self.current=None

    def __getattr__(self, item):
            self.__dict__[item]=0  # avoid infinite recursion
            return 0

    def __getattribute__(self, item):
        if item.startswith('cur'):
            raise AttributeError
        return object.__getattribute__(self,item)  # avoid infinite recursion
        # or you can use ---return super().__getattribute__(item)
        # note this class subclass object

obj1 = Count(1,10)
print(obj1.mymin)
print(obj1.mymax)
print(obj1.current)
```