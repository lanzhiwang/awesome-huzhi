## Python Hashes and Equality

### 对象是否可以作为set或者dictionary的key

|  hash  | equality | 是否可以作为set或者dictionary的key |
| :----: | :------: | :--------------------------------: |
|  相同  |   相等   |        两个对象是同一个key         |
|  相同  |  不相等  |        两个对象是不同的key         |
| 不相同 |   相等   |        两个对象是不同的key         |
| 不相同 |  不相等  |        两个对象是不同的key         |

```python
class MyClass(object):
    '''hash 相同，对象相等
    '''

    def __hash__(self):
        return 1

    def __eq__(self, other):
        return isinstance(other, MyClass)

obj1 = MyClass()
obj2 = MyClass()

print hash(obj1), hash(obj2)  # 1 1
print obj1 == obj2  # True

result = set()
result.add(obj1)
result.add(obj2)

print len(result) # 1
```

```python
class MyClass(object):
    '''hash 相同，对象不相等
    '''

    def __hash__(self):
        return 1

    # def __eq__(self, other):
    #     return isinstance(other, MyClass)

obj1 = MyClass()
obj2 = MyClass()

print hash(obj1), hash(obj2)  # 1 1
print obj1 == obj2  # False

result = set()
result.add(obj1)
result.add(obj2)

print len(result) # 2
```

```python
class MyClass(object):
    '''hash 不相同，对象相等
    '''

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return isinstance(other, MyClass)

obj1 = MyClass()
obj2 = MyClass()

print hash(obj1), hash(obj2)  # 140622227779408 140622227779472
print obj1 == obj2  # True

result = set()
result.add(obj1)
result.add(obj2)

print len(result) # 2
```

```python
class MyClass(object):
    '''hash 不相同，对象不相等
    '''

    def __hash__(self):
        return id(self)

    # def __eq__(self, other):
    #     return isinstance(other, MyClass)

obj1 = MyClass()
obj2 = MyClass()

print hash(obj1), hash(obj2)  # 140497251938128 140497251938192
print obj1 == obj2  # False

result = set()
result.add(obj1)
result.add(obj2)

print len(result) # 2

```

### 对象可hash的方法

* \_\_hash\_\_(self) 和  \_\_eq\_\_(self, other) 都不实现
* 实现 \_\_hash\_\_(self)，不实现 \_\_eq\_\_(self, other)
* \_\_hash\_\_(self) 和  \_\_eq\_\_(self, other) 都实现

如果只实现 \_\_eq\_\_(self, other)，不实现 \_\_hash\_\_(self)，则对象不可hash

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

class C1:
    ''' __hash__(self) 和  __eq__(self, other) 都不实现
    '''
    def __init__(self, x):
        self.x = x

print hash(C1(1))  # 8736312111280

class C2:
    '''实现 __hash__(self)，不实现 __eq__(self, other)
    '''
    def __init__(self, x):
        self.x = x

    def __hash__(self):
        return hash(self.x)

print hash(C2(1))  # 1

class C3:
    ''' __hash__(self) 和  __eq__(self, other) 都实现
    '''
    def __init__(self, x):
        self.x = x

    def __hash__(self):
        return hash(self.x)

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.x == other.x
        )

print hash(C3(1))  # 1

class C4:
    '''只实现 __eq__(self, other)，不实现 __hash__(self)
    '''
    def __init__(self, x):
        self.x = x

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.x == other.x
        )

print hash(C4(1))  # TypeError: unhashable instance

```



An object is hashable if it has a hash value which never changes during its lifetime (it needs a \_\_hash\_\_() method), and can be compared to other objects (it needs an \_\_eq\_\_() or \_\_cmp\_\_() method). Hashable objects which compare equal must have the same hash value.

Hashability makes an object usable as a dictionary key and a set member, because these data structures use the hash value internally.

All of Python’s immutable built-in objects are hashable, while no mutable containers (such as lists or dictionaries) are. Objects which are instances of user-defined classes are hashable by default; they all compare unequal, and their hash value is their id().


To summarize, a hash function must satisfy the property:
* If two objects are equal, then their hashes should be equal.

Additionally, a good hash function should satisfy the property:
* If two objects have the same hash, then they are likely to be the same object.






An object is hashable if it has a hash value which never changes during its lifetime (it needs a __hash__() method), and can be compared to other objects (it needs an __eq__() or __cmp__() method). Hashable objects which compare equal must have the same hash value.

Hashability makes an object usable as a dictionary key and a set member, because these data structures use the hash value internally.

All of Python’s immutable built-in objects are hashable, while no mutable containers (such as lists or dictionaries) are. Objects which are instances of user-defined classes are hashable by default; they all compare unequal, and their hash value is their id().











Most Python programmers don’t spend a lot of time thinking about how equality and hashing works. It usually just works. However there’s quite a bit of gotchas and edge cases that can lead to subtle and frustrating bugs once one starts to customize their behavior – especially if the rules on how they interact aren’t understood.  大多数Python程序员不会花很多时间考虑平等和散列是如何工作的。 它通常只是有效。 然而，一旦开始定制他们的行为，就会有相当多的陷阱和边缘情况会导致微妙和令人沮丧的错误 - 特别是如果不了解他们如何交互的规则。

### Object Equality

Equality in Python is more complicated than most people realize but at its core you have to implement a \_\_eq\_\_(self, other) method. It should return either a boolean value if your class knows how to compare itself to other or NotImplemented if it doesn’t. For inequality checks using !=, the corresponding method is \_\_ne\_\_(self, other).  Python中的平等比大多数人意识到的要复杂，但在其核心，你必须实现\_\_eq \_\_（self, other）方法。 如果你的类知道如何将自己与其他人进行比较，那么它应返回一个布尔值，否则返回NotImplemented。 对于使用！=的不等式检查，相应的方法是\_\_ne \_\_（self，other）。

By default, those methods are inherited from the object class that compares two instances by their identity – therefore instances are only equal to themselves.  默认情况下，这些方法继承自对象类，该对象类通过其标识比较两个实例 - 因此实例仅等于它们自身。

A common mistake in Python 2 was to override only \_\_eq\_\_() and forget about \_\_ne\_\_(). Python 3 is friendly enough to implement an obvious \_\_ne\_\_() for you, if you don’t yourself.  Python 2中的一个常见错误是仅覆盖\_\_eq \_\_（）并忘记\_\_ne \_\_（）。 Python 3足够友好，可以为你实现一个明显的\_\_ne \_\_（），如果你不是你自己。

### Object Hashes

An object hash is an integer number representing the value of the object and can be obtained using the hash() function if the object is hashable. `To make a class hashable, it has to implement both the __hash__(self) method and the aforementioned __eq__(self, other) method`. As with equality, the inherited object.\_\_hash\_\_ method works by identity only: barring the unlikely event of a hash collision, two instances of the same class will always have different hashes, no matter what data they carry.  对象散列是表示对象值的整数，如果对象是可散列的，则可以使用hash（）函数获取。 要使类具有hashable，它必须实现\_\_hash \_\_（self）方法和前面提到的\_\_eq \_\_（self，other）方法。 与相等一样，继承的对象.\_\_ hash\_\_方法仅按标识工作：除非发生哈希冲突的不太可能的事件，否则同一类的两个实例将始终具有不同的哈希值，无论它们携带什么数据。

Since this is usually good enough, most Pythonistas don’t realize there’s even a thing called hashing until they try to add an unhashable object into a set or a dictionary:  由于这通常足够好，大多数Pythonistas都没有意识到甚至有一个叫做散列的东西，直到他们试图将一个不可用的对象添加到一个集合或字典中：

```python
>>> set().add({})
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'dict'
unhashable type: 'dict'
```

So hashes are important because sets and dictionaries use them for their lookup tables to quickly find their keys. To do that effectively, they make an important assumption that leads to our first gotcha:  所以散列很重要，因为集合和字典使用它们来查找表格以快速找到它们的键。 为了有效地做到这一点，他们做出了一个重要的假设，导致我们的第一个问题：

**The hash of an object must never change during its lifetime. 对象的哈希值在其生命周期内不得更改。**

So if you decide to do the perfectly sensible thing and define the equality and hash of your object by the hash and equality of a tuple of the instance’s attributes, you have to make sure those attributes never change lest weird things happen:  因此，如果您决定执行完全合理的事情并通过实例属性的元组的哈希和相等来定义对象的相等性和散列，则必须确保这些属性永远不会改变，以免发生奇怪的事情：

```python
>>> class C:
...     def __init__(self, x):
...         self.x = x
...     def __repr__(self):
...         return f"C({self.x})"
...     def __hash__(self):
...         return hash(self.x)
...     def __eq__(self, other):
...         return (
...             self.__class__ == other.__class__ and
...             self.x == other.x
...         )
>>> d = dict()
>>> s = set()
>>> c = C(1)
>>> d[c] = 42
>>> s.add(c)
>>> d, s
({C(1): 42}, {C(1)})
>>> c in s and c in d  # c is in both!
True
>>> c.x = 2
>>> c in s or c in d   # c is in neither!?
False
>>> d, s
({C(2): 42}, {C(2)})   # but...it's right there!
```

Although our mutated c clearly is in both d and s, Python claims it never heard of it!  尽管我们的变异c明显同时出现在d和s中，但Python声称它从未听说过它！

This explains why all immutable data structures like tuples or strings are hashable while mutable ones like lists or dictionaries aren’t.  这解释了为什么像元组或字符串这样的所有不可变数据结构都是可以清除的，而列表或字典之类的可变数据结构则不是。

To make matters even more confusing, creating an object with the same hash value will also not work because Python is going to throw a call to \_\_eq\_\_ into the mix and C(1) is clearly not equal to C(2):  更令人困惑的是，创建具有相同散列值的对象也将无法工作，因为Python将调用\_\_eq\_\_到混合中，而C（1）显然不等于C（2）：

```python
>>> C(1) in s or C(1) in d
False
```

Why the equality check? As we’ve established before, a hash is an integer. And even though we have 64 bits to splurge on modern architectures, there’s still the possibility that two objects have the same hash.  为什么要平等检查？ 正如我们之前建立的，哈希是一个整数。 即使我们有64位在现代架构上挥霍，但仍有两个对象具有相同散列的可能性。

Given this behavior we’ve found another assumption made by sets and dictionaries:  鉴于这种行为，我们发现了集和字典的另一个假设：

**Hashable objects which compare equal must have the same hash value.  比较相等的可哈希对象必须具有相同的哈希值。**

In other words: if x == y it must follow that hash(x) == hash(y).  换句话说：如果x == y，它必须遵循hash（x）== hash（y）。

Since that’s not true in our case, we can’t access that object by its hash anymore.  由于在我们的情况下不是这样，我们不能再通过其哈希访问该对象。

### What Does All of This Mean?

** You can’t base your hash on mutable values.**  If an attribute can change in the lifetime of an object, you can’t use it for hashing or very funky things happen.  您不能将哈希基于可变值。 如果属性可以在对象的生命周期中发生变化，则不能将其用于散列或发生非常时髦的事情。

Generally speaking, immutable objects are the cleanest approach and they come with many other upsides your FP-loving friends will happily explain to you at length.  一般来说，不可变对象是最干净的方法，它们带来许多其他好处，你的FP爱好者会很乐意向你详细解释。

Practically speaking though, that’s not always possible – for performance reasons alone. Python just isn’t conceived with immutability in mind like, say Clojure.  实际上，这并不总是可行的 - 仅出于性能原因。 Clojure说，Python并不像脑子里的不变性那样被设想。



https://hynek.me/articles/hashes-and-equality/












