## Overriding the \_\_new\_\_ method

When subclassing immutable built-in types like numbers and strings, and occasionally in other situations, the static method \_\_new\_\_ comes in handy. _\_new\_\_ is the first step in instance construction, invoked before \_\_init\_\_. The \_\_new\_\_ method is called with the class as its first argument; its responsibility is to return a new instance of that class. Compare this to \_\_init\_\_: \_\_init\_\_ is called with an instance as its first argument, and it doesn't return anything; its responsibility is to initialize the instance. There are situations where a new instance is created without calling \_\_init\_\_ (for example when the instance is loaded from a pickle). There is no way to create a new instance without calling \_\_new\_\_ (although in some cases you can get away with calling a base class's \_\_new\_\_).  当子类化不可变的内置类型（如数字和字符串）时，偶尔在其他情况下，静态方法\_\_new\_\_会派上用场。 \_\_new\_\_是实例构造的第一步，在\_\_init\_\_之前调用。 调用\_\_new\_\_方法，将类作为其第一个参数; 它的职责是返回该类的新实例。 将此与\_\_init\_\_进行比较：使用实例作为第一个参数调用\_\_init\_\_，并且它不返回任何内容; 它的职责是初始化实例。 在某些情况下，无需调用\_\_init\_\_即可创建新实例（例如，从pickle加载实例时）。 没有调用\_\_new\_\_就无法创建新实例（尽管在某些情况下你可以通过调用基类的\_\_new\_\_来逃避）。

Recall that you create class instances by calling the class. When the class is a new-style class, the following happens when it is called. First, the class's \_\_new\_\_ method is called, passing the class itself as first argument, followed by any (positional as well as keyword) arguments received by the original call. This returns a new instance. Then that instance's \_\_init\_\_ method is called to further initialize it. (This is all controlled by the \_\_call\_\_ method of the metaclass, by the way.)  回想一下，通过调用类来创建类实例。 当类是新样式类时，调用它时会发生以下情况。 首先，调用类的\_\_new\_\_方法，将类本身作为第一个参数传递，然后是原始调用接收的任何（位置和关键字）参数。 这将返回一个新实例。 然后调用该实例的\_\_init\_\_方法以进一步初始化它。 （顺便说一句，这都是由元类的\_\_call\_\_方法控制的。）

Here is an example of a subclass that overrides \_\_new\_\_ - this is how you would normally use it.  以下是覆盖\_\_new\_\_的子类的示例 - 这是您通常使用它的方式。

```python
    >>> class inch(float):
    ...     "Convert from inch to meter"
    ...     def __new__(cls, arg=0.0):
    ...         return float.__new__(cls, arg*0.0254)
    ...
    >>> print inch(12)
    0.3048
    >>> 
```

This class isn't very useful (it's not even the right way to go about unit conversions) but it shows how to extend the constructor of an immutable type. If instead of \_\_new\_\_ we had tried to override \_\_init\_\_, it wouldn't have worked:  这个类不是很有用（它甚至不是单元转换的正确方法），但它展示了如何扩展不可变类型的构造函数。 如果我们试图覆盖\_\_init\_\_而不是\_\_new\_\_，那么它就不会起作用：

```python
    >>> class inch(float):
    ...     "THIS DOESN'T WORK!!!"
    ...     def __init__(self, arg=0.0):
    ...         float.__init__(self, arg*0.0254)
    ...
    >>> print inch(12)
    12.0
    >>> 
```

The version overriding \_\_init\_\_ doesn't work because the float type's \_\_init\_\_ is a no-op: it returns immediately, ignoring its arguments.  重写\_\_init\_\_的版本不起作用，因为float类型的\_\_init\_\_是一个no-op：它会立即返回，忽略它的参数。

All this is done so that immutable types can preserve their immutability while allowing subclassing. If the value of a float object were initialized by its \_\_init\_\_ method, you could change the value of an existing float object! For example, this would work:  所有这些都是这样做的，这样不可变类型可以在允许子类化的同时保留它们的不变性。 如果float对象的值由其\_\_init\_\_方法初始化，则可以更改现有float对象的值！ 例如，这将工作：

```python
    >>> # THIS DOESN'T WORK!!!
    >>> import math
    >>> math.pi.__init__(3.0)
    >>> print math.pi
    3.0
    >>>
```

I could have fixed this problem in other ways, for example by adding an "already initialized" flag or only allowing \_\_init\_\_ to be called on subclass instances, but those solutions are inelegant. Instead, I added \_\_new\_\_, which is a perfectly general mechanism that can be used by built-in and user-defined classes, for immutable and mutable objects.  我可以通过其他方式修复此问题，例如通过添加“已初始化”标志或仅允许在子类实例上调用\_\_init\_\_，但这些解决方案不够优雅。 相反，我添加了\_\_new\_\_，这是一个完全通用的机制，可以被内置和用户定义的类用于不可变和可变对象。

Here are some rules for \_\_new\_\_:

* \_\_new\_\_ is a static method. When defining it, you don't need to (but may!) use the phrase "\_\_new\_\_ = staticmethod(\_\_new\_\_)", because this is implied by its name (it is special-cased by the class constructor).  \_\_new\_\_是一种静态方法。 在定义它时，您不需要（但可能！）使用短语“\_\_new\_\_ = staticmethod（\_\_ new \_\_）”，因为它的名称暗示了它（它由类构造函数特殊引用）。

* The first argument to \_\_new\_\_ must be a class; the remaining arguments are the arguments as seen by the constructor call.  \_\_new\_\_的第一个参数必须是一个类; 其余的参数是构造函数调用所看到的参数。

* A \_\_new\_\_ method that overrides a base class's \_\_new\_\_ method may call that base class's \_\_new\_\_ method. The first argument to the base class's \_\_new\_\_ method call should be the class argument to the overriding \_\_new\_\_ method, not the base class; if you were to pass in the base class, you would get an instance of the base class.  覆盖基类的\_\_new\_\_方法的\_\_new\_\_方法可以调用该基类的\_\_new\_\_方法。 基类的\_\_new\_\_方法调用的第一个参数应该是重写\_\_new\_\_方法的类参数，而不是基类; 如果您要传入基类，您将获得基类的实例。

* Unless you want to play games like those described in the next two bullets, a \_\_new\_\_ method must call its base class's \_\_new\_\_ method; that's the only way to create an instance of your object. The subclass \_\_new\_\_ can do two things to affect the resulting object: pass different arguments to the base class \_\_new\_\_, and modify the resulting object after it's been created (for example to initialize essential instance variables).  除非您想玩下两个项目符号中描述的游戏，否则\_\_new\_\_方法必须调用其基类的\_\_new\_\_方法; 这是创建对象实例的唯一方法。 子类\_\_new\_\_可以做两件事来影响结果对象：将不同的参数传递给基类\_\_new\_\_，并在创建后修改结果对象（例如初始化基本实例变量）。

* \_\_new\_\_ must return an object. There's nothing that requires that it return a new object that is an instance of its class argument, although that is the convention. If you return an existing object, the constructor call will still call its \_\_init\_\_ method. If you return an object of a different class, its \_\_init\_\_ method will be called. If you forget to return something, Python will unhelpfully return None, and your caller will probably be very confused.  \_\_new\_\_必须返回一个对象。 没有什么要求它返回一个新对象，它是类参数的一个实例，尽管这是惯例。 如果返回现有对象，构造函数调用仍将调用其\_\_init\_\_方法。 如果返回其他类的对象，则会调用其\_\_init\_\_方法。 如果您忘记返回某些内容，Python将无助地返回None，并且您的调用者可能会非常困惑。

* For immutable classes, your \_\_new\_\_ may return a cached reference to an existing object with the same value; this is what the int, str and tuple types do for small values. This is one of the reasons why their \_\_init\_\_ does nothing: cached objects would be re-initialized over and over. (The other reason is that there's nothing left for \_\_init\_\_ to initialize: \_\_new\_\_ returns a fully initialized object.)  对于不可变类，\_\_ new\_\_可能会返回对具有相同值的现有对象的缓存引用; 这就是int，str和tuple类型对小值的作用。 这是他们的\_\_init\_\_什么都不做的原因之一：缓存的对象会一遍又一遍地重新初始化。 （另一个原因是\_\_init\_\_没有任何内容可以初始化：\_\_ new\_\_返回一个完全初始化的对象。）

* If you subclass a built-in immutable type and want to add some mutable state (maybe you add a default conversion to a string type), it's best to initialize the mutable state in the \_\_init\_\_ method and leave \_\_new\_\_ alone.  如果你继承了一个内置的不可变类型并希望添加一些可变状态（也许你可以在字符串类型中添加一个默认转换），最好在\_\_init\_\_方法中初始化可变状态并单独留下\_\_new\_\_。

* If you want to change the constructor's signature, you often have to override both \_\_new\_\_ and \_\_init\_\_ to accept the new signature. However, most built-in types ignore the arguments to the method they don't use; in particular, the immutable types (int, long, float, complex, str, unicode, and tuple) have a dummy \_\_init\_\_, while the mutable types (dict, list, file, and also super, classmethod, staticmethod, and property) have a dummy \_\_new\_\_. The built-in type 'object' has a dummy \_\_new\_\_ and a dummy \_\_init\_\_ (which the others inherit). The built-in type 'type' is special in many respects; see the section on metaclasses.  如果要更改构造函数的签名，通常必须重写\_\_new\_\_和\_\_init\_\_以接受新签名。 但是，大多数内置类型忽略了它们不使用的方法的参数; 特别是，不可变类型（int，long，float，complex，str，unicode和tuple）有一个虚拟的\_\_init\_\_，而可变类型（dict，list，file，以及super，classmethod，staticmethod和property）都有 假\_\_new\_\_。 内置类型“对象”有一个虚拟\_\_new\_\_和一个虚拟\_\_init\_\_（其他人继承）。 内置类型“类型”在许多方面都很特别; 请参阅有关元类的部分。

* (This has nothing to do to \_\_new\_\_, but is handy to know anyway.) If you subclass a built-in type, extra space is automatically added to the instances to accomodate \_\_dict\_\_ and \_\_weakrefs\_\_. (The \_\_dict\_\_ is not initialized until you use it though, so you shouldn't worry about the space occupied by an empty dictionary for each instance you create.) If you don't need this extra space, you can add the phrase "\_\_slots\_\_ = []" to your class. (See above for more about \_\_slots\_\_.)  （这与\_\_new\_\_无关，但无论如何都很方便。）如果你继承了一个内置类型，额外的空间会自动添加到实例中以容纳\_\_dict\_\_和\_\_weakrefs\_\_。 （\_\_dict\_\_在你使用它之前不会被初始化，所以你不必担心你创建的每个实例的空字典占用的空间。）如果你不需要这个额外的空间，你可以添加短语“\_\_slots\_\_” = []“给你的班级。 （有关\_\_slots\_\_的更多信息，请参见上文。）

* Factoid: \_\_new\_\_ is a static method, not a class method. I initially thought it would have to be a class method, and that's why I added the classmethod primitive. Unfortunately, with class methods, upcalls don't work right in this case, so I had to make it a static method with an explicit class as its first argument. Ironically, there are now no known uses for class methods in the Python distribution (other than in the test suite). I might even get rid of classmethod in a future release if no good use for it can be found!  Factoid：\_\_ new\_\_是静态方法，而不是类方法。 我最初认为它必须是一个类方法，这就是我添加classmethod原语的原因。 不幸的是，对于类方法，upcalls在这种情况下不能正常工作，因此我不得不将它作为静态方法，并将显式类作为其第一个参数。 具有讽刺意味的是，Python发行版中的类方法现在没有已知的用途（测试套件除外）。 如果找不到好用的话，我甚至可能在将来的版本中摆脱classmethod！

* As another example of \_\_new\_\_, here's a way to implement the singleton pattern.  作为\_\_new\_\_的另一个例子，这是一种实现单例模式的方法。

```python
    class Singleton(object):
        def __new__(cls, *args, **kwds):
            it = cls.__dict__.get("__it__")
            if it is not None:
                return it
            cls.__it__ = it = object.__new__(cls)
            it.init(*args, **kwds)
            return it
        def init(self, *args, **kwds):
            pass
            
```

To create a singleton class, you subclass from Singleton; each subclass will have a single instance, no matter how many times its constructor is called. To further initialize the subclass instance, subclasses should override 'init' instead of \_\_init\_\_ - the \_\_init\_\_ method is called each time the constructor is called. For example:  要创建单例类，可以从Singleton中继承子类; 每个子类都有一个实例，无论其构造函数被调用多少次。 为了进一步初始化子类实例，子类应该覆盖'init'而不是\_\_init\_\_  - 每次调用构造函数时都会调用\_\_init\_\_方法。 例如：

```python
    >>> class MySingleton(Singleton):
    ...     def init(self):
    ...         print "calling init"
    ...     def __init__(self):
    ...         print "calling __init__"
    ... 
    >>> x = MySingleton()
    calling init
    calling __init__
    >>> assert x.__class__ is MySingleton
    >>> y = MySingleton()
    calling __init__
    >>> assert x is y
    >>> 
```

* As another example of \_\_new\_\_, here's a way to implement ORM.

```python
from orm import Model, StringField, IntegerField

class User(Model):
    __table__ = 'users'

    id = IntegerField(primary_key=True)
    name = StringField()

class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value

class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        # 排除Model类本身:
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)
        # 获取table名称:
        tableName = attrs.get('__table__', None) or name
        logging.info('found model: %s (table: %s)' % (name, tableName))
        # 获取所有的Field和主键名:
        mappings = dict()
        fields = []
        primaryKey = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                logging.info('  found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
                if v.primary_key:
                    # 找到主键:
                    if primaryKey:
                        raise RuntimeError('Duplicate primary key for field: %s' % k)
                    primaryKey = k
                else:
                    fields.append(k)
        if not primaryKey:
            raise RuntimeError('Primary key not found.')
        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))
        attrs['__mappings__'] = mappings # 保存属性和列的映射关系
        attrs['__table__'] = tableName
        attrs['__primary_key__'] = primaryKey # 主键属性名
        attrs['__fields__'] = fields # 除主键外的属性名
        # 构造默认的SELECT, INSERT, UPDATE和DELETE语句:
        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primaryKey, ', '.join(escaped_fields), tableName)
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)
        return type.__new__(cls, name, bases, attrs)

```

