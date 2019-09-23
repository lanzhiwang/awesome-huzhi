## Difference between \_\_getattr\_\_ vs \_\_getattribute\_\_

A key difference between `__getattr__` and `__getattribute__` is that **\_\_getattr\_\_ is only invoked if the attribute wasn't found the usual ways.** It's good for implementing a fallback for missing attributes, and is probably the one of two you want.

**\_\_getattribute\_\_ is invoked before looking at the actual attributes on the object**, and so can be tricky to implement correctly. You can end up in infinite recursions very easily.  在查看对象的实际属性之前，将调用\_\_getattribute\_\_，因此正确实现可能会比较棘手。 您可以非常轻松地进行无限递归。

New-style classes derive from object, old-style classes are those in Python 2.x with no explicit base class. But the distinction between old-style and new-style classes is not the important one when choosing between `__getattr__` and `__getattribute__`.  新式类是从对象派生的，旧式类是Python 2.x中没有显式基类的类。 但是，在\_\_getattr\_\_ 和 \_\_getattribute\_\_ 之间进行选择时，旧样式类与新样式类之间的区别并不是重要的区别。

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

1
10
Traceback (most recent call last):
  File "test.py", line 11, in <module>
    print(obj1.mycurrent)
AttributeError: Count instance has no attribute 'mycurrent'

```

Now my class Count has `__getattr__` method. Now when I try to access  obj1.mycurrent attribute -- python returns me whatever I have implemented in my `__getattr__` method. In my example whenever I try to call an attribute which doesn't exist, python creates that attribute and set it to integer value 0.

```python
class Count:
    def __init__(self,mymin,mymax):
        self.mymin=mymin
        self.mymax=mymax

    def __getattr__(self, item):
        print '__getattr__ item: {}'.format(item)
        self.__dict__[item]=0
        return 0

obj1 = Count(1,10)
print(obj1.mymin)
print(obj1.mymax)
print(obj1.mycurrent)

1
10
__getattr__ item: mycurrent
0
```

### \_\_getattribute\_\_

Now lets see the `__getattribute__` method. **If you have  \_\_getattribute\_\_ method in your class, python invokes this method for every attribute regardless whether it exists or not.** So why we need `__getattribute__` method? One good reason is that you can prevent access to attributes and make them more secure as shown in the following example.

Whenever someone try to access my attributes that starts with substring 'cur' python raises AttributeError exception. Otherwise it returns that attribute.

```python
# old-style classes
# 在旧式类中 __getattribute__ 不起作用
# 属性存在，直接返回属性
# 属性不存在，raise AttributeError
# 不是每次访问任何属性都会调用 __getattribute__ 方法
class Count:

    def __init__(self, mymin, mymax):
        self.mymin = mymin
        self.mymax = mymax

    def __getattribute__(self, item):
        print '__getattribute__ item: {}'.format(item)
        if item.startswith('cur'):
            raise AttributeError
        return object.__getattribute__(self,item)
        # or you can use ---return super().__getattribute__(item)


obj1 = Count(1,10)
print(obj1.mymin)
print(obj1.mymax)
print(obj1.current)

1
10
Traceback (most recent call last):
  File "test.py", line 20, in <module>
    print(obj1.current)
AttributeError: Count instance has no attribute 'current'

###############################################################

# New-style classes
# 无论属性是否存在，都会调用 __getattribute__ 方法
class Count(object):

    def __init__(self, mymin, mymax):
        self.mymin = mymin
        self.mymax = mymax

    def __getattribute__(self, item):
        print '__getattribute__ item: {}'.format(item)
        if item.startswith('cur'):
            raise AttributeError
        return object.__getattribute__(self,item)
        # or you can use ---return super().__getattribute__(item)


obj1 = Count(1, 10)
print(obj1.mymin)
print(obj1.mymax)
print(obj1.current)

__getattribute__ item: mymin
1
__getattribute__ item: mymax
10
__getattribute__ item: current
Traceback (most recent call last):
  File "test.py", line 21, in <module>
    print(obj1.current)
  File "test.py", line 13, in __getattribute__
    raise AttributeError
AttributeError

```

Important: In order to avoid infinite recursion in `__getattribute__` method, its implementation should always call the base class method with the same name to access any attributes it needs. For example: object.\_\_getattribute\_\_(self, name) or  super().\_\_getattribute\_\_(item) and not self.\_\_dict\_\_[item]

### IMPORTANT

If your class contain both getattr and getattribute magic methods then  `__getattribute__` is called first. But if  `__getattribute__` raises  AttributeError exception then the exception will be ignored and `__getattr__` method will be invoked. See the following example:

```python
# old-style classes
# 在旧式类中 __getattribute__ 不起作用
# 属性存在，直接返回属性
# 属性不存在，raise AttributeError
# 不是每次访问任何属性都会调用 __getattribute__ 方法
class Count:

    def __init__(self, mymin, mymax):
        self.mymin = mymin
        self.mymax = mymax

    def __getattr__(self, item):
        print '__getattr__ item: {}'.format(item)
        self.__dict__[item]=0  # avoid infinite recursion
        return 0

    def __getattribute__(self, item):
        print '__getattribute__ item: {}'.format(item)
        if item.startswith('cur'):
            raise AttributeError
        return object.__getattribute__(self,item)  # avoid infinite recursion
        # or you can use ---return super().__getattribute__(item)
        # note this class subclass object


obj1 = Count(1, 10)
print(obj1.mymin)
print(obj1.mymax)
print(obj1.current)

1
10
__getattr__ item: current
0

###############################################################

# New-style classes
# 无论属性是否存在，都会调用 __getattribute__ 方法
# 无论属性是否存在，在 __getattribute__ 方法中 raise AttributeError 就调用 __getattr__ 方法
# 无论属性是否存在，在 __getattribute__ 方法中如果没有 raise AttributeError 就不会调用 __getattr__ 方法
# 无论属性是否存在，在 __getattribute__ 方法 raise 其他异常也不会调用 __getattr__ 方法
class Count(object):

    def __init__(self, mymin, mymax):
        self.mymin = mymin
        self.mymax = mymax

    def __getattr__(self, item):
        print '__getattr__ item: {}'.format(item)
        self.__dict__[item] = 0  # avoid infinite recursion
        return 0

    def __getattribute__(self, item):
        print '__getattribute__ item: {}'.format(item)
        if item.startswith('cur'):
            raise AttributeError
        return object.__getattribute__(self,item)  # avoid infinite recursion
        # or you can use ---return super().__getattribute__(item)
        # note this class subclass object


obj1 = Count(1, 10)
print(obj1.mymin)
print(obj1.mymax)
print(obj1.current)

__getattribute__ item: mymin
1
__getattribute__ item: mymax
10
__getattribute__ item: current
__getattr__ item: current
__getattribute__ item: __dict__
0

###############################################################

#!/usr/bin/env python


# New-style classes
class Count(object):

    def __init__(self, mymin, mymax):
        self.mymin = mymin
        self.mymax = mymax

    def __getattr__(self, item):
        print '__getattr__ item: {}'.format(item)
        self.__dict__[item] = 0  # avoid infinite recursion
        return 0

    def __getattribute__(self, item):
        print '__getattribute__ item: {}'.format(item)

        if item.startswith('1cur'):
            raise AttributeError

        if item.startswith('2cur'):
            return 0

        if item.startswith('rai'):
            raise KeyError

        if item == 'mymax':
            raise AttributeError
        return object.__getattribute__(self,item)  # avoid infinite recursion
        # or you can use ---return super().__getattribute__(item)
        # note this class subclass object


obj1 = Count(1, 10)
print(obj1.mymin)
print(obj1.mymax)
print(obj1.current)
print(obj1.rai)

__getattribute__ item: mymin
1
__getattribute__ item: mymax
__getattr__ item: mymax
__getattribute__ item: __dict__
0
__getattribute__ item: current
__getattr__ item: current
__getattribute__ item: __dict__
0
__getattribute__ item: rai
Traceback (most recent call last):
  File "test.py", line 40, in <module>
    print(obj1.rai)
  File "test.py", line 27, in __getattribute__
    raise KeyError
KeyError

```
