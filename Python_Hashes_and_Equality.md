## Python Hashes and Equality

- [对象可hash的方法]()
- [对象是否可以作为set或者dictionary的key]()
	- [同样的参数是否可以作为同样的key]()
	- [对象的hash值在生命周期内发生变化]()
- [结论]()

### 对象可hash的方法

一个可散列的对象必须满足以下要求:
1. 支持 hash() 函数，并且通过 \_\_hash\_\_() 方法所得到的散列值是不变的。
2. 支持通过 \_\_eq\_\_() 方法来检测相等性。
3. 若 a == b 为真， 则 hash(a) == hash(b) 也为真。

Notes:
1. 所有由用户自定义的对象默认都是可散列的， 因为它们的散列值由id() 来获取， 而且它们都是不相等的。
2. 如果你实现了一个类的 \_\_eq\_\_ 方法， 并且希望它是可散列的， 那么它一定要有个恰当的 \_\_hash\_\_ 方法， 保证在 a == b 为真的情况下 hash(a) == hash(b) 也必定为真。  

---------------------------------------------------------------------------------------------------------------------


| 实现方式 | 是否可 hash | 原因 |
| -------- | ----------- | ---- | ---- |
| \_\_hash\_\_(self) 和  \_\_eq\_\_(self, other) 都不实现 | 可 hash | 所有由用户自定义的对象默认都是可散列的， 因为它们的散列值由id() 来获取， 而且它们都是不相等的 |
| 实现 \_\_hash\_\_(self)，不实现\_\_eq\_\_(self, other) | 可 hash | 支持 hash() 函数，并且通过 \_\_hash\_\_() 方法所得到的散列值是不变的；所有由用户自定义的对象默认都是不相等的 |
| \_\_hash\_\_(self) 和  \_\_eq\_\_(self, other) 都实现 | 可 hash | 支持 hash() 函数，并且通过 \_\_hash\_\_() 方法所得到的散列值是不变的； 支持通过 \_\_eq\_\_() 方法来检测相等性；如果你实现了一个类的 \_\_eq\_\_ 方法， 并且希望它是可散列的， 那么它一定要有个恰当的 \_\_hash\_\_ 方法， 保证在 a == b 为真的情况下 hash(a) == hash(b) 也必定为真 |
| 不实现\_\_hash\_\_(self)， 实现\_\_eq\_\_(self, other) | 不可 hash | 如果你实现了一个类的 \_\_eq\_\_ 方法， 并且希望它是可散列的， 那么它一定要有个恰当的 \_\_hash\_\_ 方法， 保证在 a == b 为真的情况下 hash(a) == hash(b) 也必定为真 |


* \_\_hash\_\_(self) 和  \_\_eq\_\_(self, other) 都不实现
  * 所有由用户自定义的对象默认都是可散列的， 因为它们的散列值由id() 来获取， 而且它们都是不相等的
* 实现 \_\_hash\_\_(self)，不实现 \_\_eq\_\_(self, other)
  * 支持 hash() 函数，并且通过 \_\_hash\_\_() 方法所得到的散列值是不变的
  * 所有由用户自定义的对象默认都是不相等的
* \_\_hash\_\_(self) 和  \_\_eq\_\_(self, other) 都实现
  * 支持 hash() 函数，并且通过 \_\_hash\_\_() 方法所得到的散列值是不变的
  * 支持通过 \_\_eq\_\_() 方法来检测相等性
  * 如果你实现了一个类的 \_\_eq\_\_ 方法， 并且希望它是可散列的， 那么它一定要有个恰当的 \_\_hash\_\_ 方法， 保证在 a == b 为真的情况下 hash(a) == hash(b) 也必定为真

**如果只实现 \_\_eq\_\_(self, other)，不实现 \_\_hash\_\_(self)，则对象不可hash**

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

class C1:
    ''' __hash__(self) 和  __eq__(self, other) 都不实现
    所有由用户自定义的对象默认都是可散列的， 因为它们的散列值由id() 来获取， 而且它们都是不相等的
    '''
    def __init__(self, x):
        self.x = x

print hash(C1(1))  # 8736312111280

class C2:
    '''实现 __hash__(self)，不实现 __eq__(self, other)
    支持 hash() 函数，并且通过 __hash__() 方法所得到的散列值是不变的
    所有由用户自定义的对象默认都是不相等的
    '''
    def __init__(self, x):
        self.x = x

    def __hash__(self):
        return hash(self.x)

print hash(C2(1))  # 1

class C3:
    ''' __hash__(self) 和  __eq__(self, other) 都实现
    支持 hash() 函数，并且通过 __hash__() 方法所得到的散列值是不变的
    支持通过 __eq__() 方法来检测相等性
    如果你实现了一个类的 __eq__ 方法， 并且希望它是可散列的， 那么它一定要有个恰当的 __hash__ 方法， 保证在 a == b 为真的情况下 hash(a) == hash(b) 也必定为真
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


### 对象是否可以作为set或者dictionary的key

**对象作为key值则对象必须可hash**

#### 同样的参数是否可以作为同样的key

| hash | equality | 是否可以作为同样的key |
| ---- | -------- | ------------------ |
| 相同 | 相等 | 同一个key |
| 相同 | 不相等 | 不同的key |
| 不相同 | 相等 | 不可 hash, 不能作为key |
| 不相同 | 不相等 | 不同的key |

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

class C1:
    ''' __hash__(self) 和  __eq__(self, other) 都不实现
    所有由用户自定义的对象默认都是可散列的， 因为它们的散列值由id() 来获取， 而且它们都是不相等的
    '''
    def __init__(self, x):
        self.x = x

# 测试是否可hash
print hash(C1(1))  # 8728643443659

# 对象是否可以作为set或者dictionary的key
obj1 = C1(1)
obj2 = C1(1)
print hash(obj1), hash(obj2)  # 8728643443659 -9223363308211332145
print obj1 == obj2  # False
s = set()
s.add(obj1)
s.add(obj2)
print len(s)  # 2
print '************' * 10


class C2:
    '''实现 __hash__(self)，不实现 __eq__(self, other)
    支持 hash() 函数，并且通过 __hash__() 方法所得到的散列值是不变的
    所有由用户自定义的对象默认都是不相等的
    '''
    def __init__(self, x):
        self.x = x

    def __hash__(self):
        return hash(self.x)

# 测试是否可hash
print hash(C2(1))  # 1

# 对象是否可以作为set或者dictionary的key
obj1 = C2(1)
obj2 = C2(1)
print hash(obj1), hash(obj2)  # 1 1
print obj1 == obj2  # False
s = set()
s.add(obj1)
s.add(obj2)
print len(s)  # 2
print '************' * 10


class C3:
    ''' __hash__(self) 和  __eq__(self, other) 都实现
    支持 hash() 函数，并且通过 __hash__() 方法所得到的散列值是不变的
    支持通过 __eq__() 方法来检测相等性
    如果你实现了一个类的 __eq__ 方法， 并且希望它是可散列的， 那么它一定要有个恰当的 __hash__ 方法， 保证在 a == b 为真的情况下 hash(a) == hash(b) 也必定为真
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

# 测试是否可hash
print hash(C3(1))  # 1

# 对象是否可以作为set或者dictionary的key
obj1 = C3(1)
obj2 = C3(1)
print hash(obj1), hash(obj2)  # 1 1
print obj1 == obj2  # True
s = set()
s.add(obj1)
s.add(obj2)
print len(s)  # 1
print '************' * 10


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
# 测试是否可hash
# print hash(C4(1))  # TypeError: unhashable instance

# 对象是否可以作为set或者dictionary的key
obj1 = C4(1)
obj2 = C4(1)
# print hash(obj1), hash(obj2)  # TypeError: unhashable instance
print obj1 == obj2  # True
s = set()
# s.add(obj1)  # TypeError: unhashable instance
# s.add(obj2)  # TypeError: unhashable instance
print len(s)  # 0
print '************' * 10

```

#### 对象的hash值在生命周期内发生变化

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

class C:
    def __init__(self, x):
        self.x = x

    def __hash__(self):
        return hash(self.x)

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and self.x == other.x)

d = dict()
s = set()

c1 = C(1)
print hash(c1)  # 1

# 对象c1可hash，可以作为set和dictionary的key值
d[c1] = 42
s.add(c1)

print c1 in s  # True
print c1 in d  # True

c1.x = 2
print hash(c1)  # 2

# 对象c1的hash值在生命周期内发生变化，变化后将不能作为set和dictionary的key值
print c1 in s  # False
print c1 in d  # False


```



### 结论

* An object is hashable if it has a hash value which never changes during its lifetime (it needs a \_\_hash\_\_() method), and can be compared to other objects (it needs an \_\_eq\_\_() or \_\_cmp\_\_() method). 
* Hashable objects which compare equal must have the same hash value.
* Hashability makes an object usable as a dictionary key and a set member, because these data structures use the hash value internally.
* All of Python’s immutable built-in objects are hashable, while no mutable containers (such as lists or dictionaries) are. 
* Objects which are instances of user-defined classes are hashable by default; they all compare unequal, and their hash value is their id().
* If two objects are equal, then their hashes should be equal.
* If two objects have the same hash, then they are likely to be the same object.



### 参考

- https://hynek.me/articles/hashes-and-equality/












