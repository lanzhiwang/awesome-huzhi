## Magic Methods

- [Introduction]()
- [Construction and Initialization]()
- [Making Operators Work on Custom Classes]()
- [Comparison magic methods]()
- [Numeric magic methods]()
- [Representing your Classes]()
- [Controlling Attribute Access]()
- [Making Custom Sequences]()
- [Reflection]()
- [Abstract Base Classes]()
- [Callable Objects]()
- [Context Managers]()
- [Building Descriptor Objects]()
- [Copying]()
- [Pickling your Objects]()
- [Conclusion]()
- [Appendix 1: How to Call Magic Methods]()
- [Appendix 2: Changes in Python 3]()

### Introduction

This guide is the culmination of a few months' worth of blog posts. The subject is magic methods.  本指南是几个月博客文章的高潮。 主题是魔术方法。

What are magic methods? They're everything in object-oriented Python. They're special methods that you can define to add "magic" to your classes. They're always surrounded by double underscores (e.g. \_\_init\_\_ or \_\_lt\_\_). They're also not as well documented as they need to be. All of the magic methods for Python appear in the same section in the Python docs, but they're scattered about and only loosely organized. There's hardly an example to be found in that section (and that may very well be by design, since they're all detailed in the language reference, along with boring syntax descriptions, etc.).  什么是魔术方法？ 它们是面向对象Python中的一切。 它们是您可以定义的特殊方法，可以为您的类添加“魔力”。 它们总是被双下划线包围（例如\_\_init\_\_或\_\_lt\_\_）。 它们的记录也不像它们需要的那样好。 Python的所有神奇方法都出现在Python文档的同一部分中，但它们分散在各处，并且只是松散组织。 在该部分中几乎找不到一个例子（这很可能是设计上的，因为它们在语言参考中都有详细说明，还有无聊的语法描述等）。

So, to fix what I perceived as a flaw in Python's documentation, I set out to provide some more plain-English, example-driven documentation for Python's magic methods. I started out with weekly blog posts, and now that I've finished with those, I've put together this guide.  因此，为了解决我在Python文档中看到的缺陷，我打算为Python的魔术方法提供一些更简单，英语，示例驱动的文档。 我从每周的博客文章开始，现在我已经完成了这些，我已经整理了这个指南。

I hope you enjoy it. Use it as a tutorial, a refresher, or a reference; it's just intended to be a user-friendly guide to Python's magic methods.  我希望你喜欢它。 将它用作教程，复习或参考; 它只是一个用户友好的Python魔术方法指南。

### Construction and Initialization

Everyone knows the most basic magic method, \_\_init\_\_. It's the way that we can define the initialization behavior of an object. However, when I call x = SomeClass(), \_\_init\_\_ is not the first thing to get called. Actually, it's a method called \_\_new\_\_, which actually creates the instance, then passes any arguments at creation on to the initializer. At the other end of the object's lifespan, there's \_\_del\_\_. Let's take a closer look at these 3 magic methods:  每个人都知道最基本的魔法，\_\_ init\_\_。 这是我们定义对象初始化行为的方式。 但是，当我调用x = SomeClass（）时，\_\_ init\_\_不是第一个被调用的东西。 实际上，它是一个名为\_\_new\_\_的方法，它实际上创建了实例，然后将创建时的任何参数传递给初始化器。 在对象的生命周期的另一端，有\_\_del\_\_。 让我们仔细看看这3种魔术方法：

###### \_\_new\_\_(cls, [...)
\_\_new\_\_ is the first method to get called in an object's instantiation. It takes the class, then any other arguments that it will pass along to \_\_init\_\_. \_\_new\_\_ is used fairly rarely, but it does have its purposes, particularly when subclassing an immutable type like a tuple or a string. I don't want to go in to too much detail on \_\_new\_\_ because it's not too useful, but it is covered in great detail in the Python docs.  \_\_new\_\_是在对象的实例化中调用的第一个方法。 它接受类，然后将传递给\_\_init\_\_的任何其他参数。 \_\_new\_\_很少使用，但它确实有其用途，特别是在子类化像元组或字符串这样的不可变类型时。 我不想在\_\_new\_\_上详细介绍它，因为它不太有用，但它在Python文档中有详细介绍。

###### \_\_init\_\_(self, [...)
The initializer for the class. It gets passed whatever the primary constructor was called with (so, for example, if we called x = SomeClass(10, 'foo'), \_\_init\_\_ would get passed 10 and 'foo' as arguments. \_\_init\_\_ is almost universally used in Python class definitions.  该类的初始化程序。 无论主要构造函数被调用，它都会被传递（例如，如果我们调用x = SomeClass（10，'foo'），\_\_ init\_\_将传递10和'foo'作为参数.\_\_init\_\_几乎普遍用于Python类定义。

###### \_\_del\_\_(self)
If \_\_new\_\_ and \_\_init\_\_ formed the constructor of the object, \_\_del\_\_ is the destructor. It doesn't implement behavior for the statement del x (so that code would not translate to x.\_\_del\_\_()). Rather, it defines behavior for when an object is garbage collected. It can be quite useful for objects that might require extra cleanup upon deletion, like sockets or file objects. Be careful, however, as there is no guarantee that \_\_del\_\_ will be executed if the object is still alive when the interpreter exits, so \_\_del\_\_ can't serve as a replacement for good coding practices (like always closing a connection when you're done with it. In fact, \_\_del\_\_ should almost never be used because of the precarious circumstances under which it is called; use it with caution!  如果\_\_new\_\_和\_\_init\_\_构成了对象的构造函数，\_\_ del\_\_就是析构函数。 它没有实现语句del x的行为（因此代码不会转换为x .\_\_ del \_\_（））。 相反，它定义了对象何时被垃圾收集的行为。 对于可能需要在删除时进行额外清理的对象（如套接字或文件对象）非常有用。 但要小心，因为如果对象在解释器退出时仍处于活动状态时无法保证\_\_del\_\_将被执行，所以\_\_del\_\_不能替代良好的编码实践（比如在完成时总是关闭连接） 事实上，\_\_del\_\_几乎不应该被使用，因为它被称之为不稳定的环境;谨慎使用它！

Putting it all together, here's an example of \_\_init\_\_ and \_\_del\_\_ in action:

```python
from os.path import join

class FileObject:
    '''Wrapper for file objects to make sure the file gets closed on deletion.'''

    def __init__(self, filepath='~', filename='sample.txt'):
        # open a file filename in filepath in read and write mode
        self.file = open(join(filepath, filename), 'r+')

    def __del__(self):
        self.file.close()
        del self.file
        
```

### Making Operators Work on Custom Classes

One of the biggest advantages of using Python's magic methods is that they provide a simple way to make objects behave like built-in types. That means you can avoid ugly, counter-intuitive, and nonstandard ways of performing basic operators. In some languages, it's common to do something like this:  使用Python魔术方法的最大优势之一是它们提供了一种简单的方法来使对象的行为类似于内置类型。 这意味着您可以避免执行基本运算符的丑陋，反直觉和非标准方式。 在某些语言中，通常会执行以下操作：

```python
if instance.equals(other_instance):
    # do something
    
```

You could certainly do this in Python, too, but this adds confusion and is unnecessarily verbose. Different libraries might use different names for the same operations, making the client do way more work than necessary. With the power of magic methods, however, we can define one method (\_\_eq\_\_, in this case), and say what we mean instead: 你当然可以在Python中做到这一点，但这会增加混乱并且不必要地冗长。 不同的库可能会对相同的操作使用不同的名称，这使得客户端的工作量超出了必要的范围。 但是，借助魔法方法的强大功能，我们可以定义一个方法（在本例中为\_\_eq\_\_），并说明我们的意思：

```python
if instance == other_instance:
    #do something
    
```

That's part of the power of magic methods. The vast majority of them allow us to define meaning for operators so that we can use them on our own classes just like they were built in types.  这是魔术方法的力量的一部分。 其中绝大多数允许我们为运算符定义含义，以便我们可以在我们自己的类上使用它们，就像它们是在类型中构建的一样。

#### Comparison magic methods

Python has a whole slew of magic methods designed to implement intuitive comparisons between objects using operators, not awkward method calls. They also provide a way to override the default Python behavior for comparisons of objects (by reference). Here's the list of those methods and what they do:  Python有一大堆魔术方法，旨在使用运算符实现对象之间的直观比较，而不是笨拙的方法调用。 它们还提供了一种覆盖默认Python行为以进行对象比较的方法（通过引用）。 以下是这些方法的列表及其作用：

###### \_\_cmp\_\_(self, other)
\_\_cmp\_\_ is the most basic of the comparison magic methods. It actually implements behavior for all of the comparison operators (<, ==, !=, etc.), but it might not do it the way you want (for example, if whether one instance was equal to another were determined by one criterion and and whether an instance is greater than another were determined by something else). \_\_cmp\_\_ should return a negative integer if self < other, zero if self == other, and positive if self > other. It's usually best to define each comparison you need rather than define them all at once, but \_\_cmp\_\_ can be a good way to save repetition and improve clarity when you need all comparisons implemented with similar criteria.  \_\_cmp\_\_是比较魔术方法中最基本的。 它实际上实现了所有比较运算符（<，==，！=等）的行为，但它可能不会按照您想要的方式执行（例如，如果一个实例是否等于另一个实例由一个标准确定 并且一个实例是否大于另一个实例是由其他东西确定的。 如果self <other则\_\_cmp\_\_应返回负整数，如果self == other则返回0，如果self> other则返回positive。 通常最好定义您需要的每个比较，而不是一次定义它们，但是当您需要使用类似标准实现所有比较时，\_\_ cmp\_\_可以是保存重复和提高清晰度的好方法。

###### \_\_eq\_\_(self, other)
Defines behavior for the equality operator, ==.

###### \_\_ne\_\_(self, other)
Defines behavior for the inequality operator, !=.

###### \_\_lt\_\_(self, other)
Defines behavior for the less-than operator, <.

###### \_\_gt\_\_(self, other)
Defines behavior for the greater-than operator, >.

###### \_\_le\_\_(self, other)
Defines behavior for the less-than-or-equal-to operator, <=.

###### \_\_ge\_\_(self, other)
Defines behavior for the greater-than-or-equal-to operator, >=.

For an example, consider a class to model a word. We might want to compare words lexicographically (by the alphabet), which is the default comparison behavior for strings, but we also might want to do it based on some other criterion, like length or number of syllables. In this example, we'll compare by length. Here's an implementation:  例如，考虑一个类来建模一个单词。 我们可能希望按字典顺序（按字母表）比较单词，这是字符串的默认比较行为，但我们也可能希望根据其他一些标准（如长度或音节数）来进行。 在这个例子中，我们将按长度进行比较。 这是一个实现：

```python
class Word(str):
    '''Class for words, defining comparison based on word length.'''

    def __new__(cls, word):
        # Note that we have to use __new__. This is because str is an immutable
        # type, so we have to initialize it early (at creation)
        if ' ' in word:
            print "Value contains spaces. Truncating to first space."
            word = word[:word.index(' ')] # Word is now all chars before first space
        return str.__new__(cls, word)

    def __gt__(self, other):
        return len(self) > len(other)
    def __lt__(self, other):
        return len(self) < len(other)
    def __ge__(self, other):
        return len(self) >= len(other)
    def __le__(self, other):
        return len(self) <= len(other)
        
```

Now, we can create two Words (by using Word('foo') and Word('bar')) and compare them based on length. Note, however, that we didn't define \_\_eq\_\_ and \_\_ne\_\_. This is because this would lead to some weird behavior (notably that Word('foo') == Word('bar') would evaluate to true). It wouldn't make sense to test for equality based on length, so we fall back on str's implementation of equality.  现在，我们可以创建两个单词（使用Word（'foo'）和Word（'bar'））并根据长度进行比较。 但请注意，我们没有定义\_\_eq\_\_和\_\_ne\_\_。 这是因为这会导致一些奇怪的行为（特别是Word（'foo'）== Word（'bar'）将评估为true）。 基于长度来测试相等是没有意义的，所以我们回到str的平等实现上。

Now would be a good time to note that you don't have to define every comparison magic method to get rich comparisons. The standard library has kindly provided us with a class decorator in the module `functools` that will define all rich comparison methods if you only define \_\_eq\_\_ and one other (e.g. \_\_gt\_\_, \_\_lt\_\_, etc.) This feature is only available in Python 2.7, but when you get a chance it saves a great deal of time and effort. You can use it by placing @total_ordering above your class definition.  现在是时候注意到你不必定义每个比较魔术方法来进行丰富的比较。 标准库在模块functools中为我们提供了类装饰器，如果你只定义\_\_eq\_\_和另一个（例如\_\_gt \_\_，\_\_ lt\_\_等），它将定义所有丰富的比较方法。这个特性仅在Python 2.7中可用，但是当 你有机会节省大量的时间和精力。 您可以通过将@total_ordering放在类定义之上来使用它。

#### Numeric magic methods

Just like you can create ways for instances of your class to be compared with comparison operators, you can define behavior for numeric operators. Buckle your seat belts, folks...there's a lot of these. For organization's sake, I've split the numeric magic methods into 5 categories: unary operators, normal arithmetic operators, reflected arithmetic operators (more on this later), augmented assignment, and type conversions.  就像您可以创建类的实例与比较运算符进行比较的方法一样，您可以为数字运算符定义行为。 扣上你的安全带，伙计......有很多这些。 出于组织的考虑，我将数字魔术方法分为5类：一元运算符，普通算术运算符，反射算术运算符（稍后将详细介绍），扩充赋值和类型转换。

##### Unary operators and functions  一元运算符和函数

Unary operators and functions only have one operand, e.g. negation, absolute value, etc.

###### \_\_pos\_\_(self)
Implements behavior for unary positive (e.g. +some_object)

###### \_\_neg\_\_(self)
Implements behavior for negation (e.g. -some_object)

###### \_\_abs\_\_(self)
Implements behavior for the built in abs() function.

###### \_\_invert\_\_(self)
Implements behavior for inversion using the ~ operator. For an explanation on what this does, see the Wikipedia article on bitwise operations.

###### \_\_round\_\_(self, n)
Implements behavior for the built in round() function. n is the number of decimal places to round to.

###### \_\_floor\_\_(self)
Implements behavior for math.floor(), i.e., rounding down to the nearest integer.

###### \_\_ceil\_\_(self)
Implements behavior for math.ceil(), i.e., rounding up to the nearest integer.

###### \_\_trunc\_\_(self)
Implements behavior for math.trunc(), i.e., truncating to an integral.

##### Normal arithmetic operators  普通算术运算符

Now, we cover the typical binary operators (and a function or two): +, -, * and the like. These are, for the most part, pretty self-explanatory.

###### \_\_add\_\_(self, other)
Implements addition.

###### \_\_sub\_\_(self, other)
Implements subtraction.

###### \_\_mul\_\_(self, other)
Implements multiplication.

###### \_\_floordiv\_\_(self, other)
Implements integer division using the // operator.

###### \_\_div\_\_(self, other)
Implements division using the / operator.

###### \_\_truediv\_\_(self, other)
Implements true division. Note that this only works when from \_\_future\_\_ import division is in effect.

###### \_\_mod\_\_(self, other)
Implements modulo using the % operator.

###### \_\_divmod\_\_(self, other)
Implements behavior for long division using the divmod() built in function.

###### \_\_pow\_\_
Implements behavior for exponents using the \*\* operator.

###### \_\_lshift\_\_(self, other)
Implements left bitwise shift using the << operator.

###### \_\_rshift\_\_(self, other)
Implements right bitwise shift using the >> operator.

###### \_\_and\_\_(self, other)
Implements bitwise and using the & operator.

###### \_\_or\_\_(self, other)
Implements bitwise or using the | operator.

###### \_\_xor\_\_(self, other)
Implements bitwise xor using the ^ operator.

##### Reflected arithmetic operators  反射算术运算符

You know how I said I would get to reflected arithmetic in a bit? Some of you might think it's some big, scary, foreign concept. It's actually quite simple. Here's an example:  你知道我怎么说我会稍微反思一下算术吗？ 有些人可能会认为这是一个大而可怕的外国概念。 它实际上非常简单。 这是一个例子：

```python
some_object + other
```

That was "normal" addition. The reflected equivalent is the same thing, except with the operands switched around:  这是“正常”的补充。 反射的等价物是相同的，除了切换操作数：

```python
other + some_object
```

So, all of these magic methods do the same thing as their normal equivalents, except the perform the operation with other as the first operand and self as the second, rather than the other way around. In most cases, the result of a reflected operation is the same as its normal equivalent, so you may just end up defining \_\_radd\_\_ as calling \_\_add\_\_ and so on. Note that the object on the left hand side of the operator (other in the example) must not define (or return NotImplemented) for its definition of the non-reflected version of an operation. For instance, in the example, some_object.\_\_radd\_\_ will only be called if other does not define \_\_add\_\_.  所以，所有这些魔术方法都与它们的正常等价物做同样的事情，除了用其他作为第一个操作数执行操作而自己作为第二个操作数执行操作，而不是相反。 在大多数情况下，反射操作的结果与其正常等效操作相同，因此您可能最终将\_\_radd\_\_定义为调用\_\_add\_\_，依此类推。 请注意，运算符左侧的对象（示例中的其他对象）不得定义（或返回NotImplemented）其操作的非反射版本的定义。 例如，在示例中，some_object .\_\_ radd\_\_仅在其他人未定义\_\_add\_\_时才会被调用。

###### \_\_radd\_\_(self, other)
Implements reflected addition.

###### \_\_rsub\_\_(self, other)
Implements reflected subtraction.

###### \_\_rmul\_\_(self, other)
Implements reflected multiplication.

###### \_\_rfloordiv\_\_(self, other)
Implements reflected integer division using the // operator.

###### \_\_rdiv\_\_(self, other)
Implements reflected division using the / operator.

###### \_\_rtruediv\_\_(self, other)
Implements reflected true division. Note that this only works when from \_\_future\_\_ import division is in effect.

###### \_\_rmod\_\_(self, other)
Implements reflected modulo using the % operator.

###### \_\_rdivmod\_\_(self, other)
Implements behavior for long division using the divmod() built in function, when divmod(other, self) is called.

###### \_\_rpow\_\_
Implements behavior for reflected exponents using the \*\* operator.

###### \_\_rlshift\_\_(self, other)
Implements reflected left bitwise shift using the << operator.

###### \_\_rrshift\_\_(self, other)
Implements reflected right bitwise shift using the >> operator.

###### \_\_rand\_\_(self, other)
Implements reflected bitwise and using the & operator.

###### \_\_ror\_\_(self, other)
Implements reflected bitwise or using the | operator.

###### \_\_rxor\_\_(self, other)
Implements reflected bitwise xor using the ^ operator.

##### Augmented   增强分配 
Python also has a wide variety of magic methods to allow custom behavior to be defined for augmented assignment. You're probably already familiar with augmented assignment, it combines "normal" operators with assignment. If you still don't know what I'm talking about, here's an example:  Python还有各种各样的魔术方法，允许为增强赋值定义自定义行为。 您可能已经熟悉增强赋值，它将“常规”运算符与赋值结合起来。 如果你还不知道我在说什么，这里有一个例子：

```python
x = 5
x += 1 # in other words x = x + 1
```

Each of these methods should return the value that the variable on the left hand side should be assigned to (for instance, for a += b, \_\_iadd\_\_ might return a + b, which would be assigned to a). Here's the list:  这些方法中的每一个都应该返回应该赋予左侧变量的值（例如，对于a + = b，\_\_ iadd\_\_可能返回+ b，它将被分配给a）。 这是列表：

###### \_\_iadd\_\_(self, other)
Implements addition with assignment.

###### \_\_isub\_\_(self, other)
Implements subtraction with assignment.

###### \_\_imul\_\_(self, other)
Implements multiplication with assignment.

###### \_\_ifloordiv\_\_(self, other)
Implements integer division with assignment using the //= operator.

###### \_\_idiv\_\_(self, other)
Implements division with assignment using the /= operator.

###### \_\_itruediv\_\_(self, other)
Implements true division with assignment. Note that this only works when from \_\_future\_\_ import division is in effect.

###### \_\_imod\_\_(self, other)
Implements modulo with assignment using the %= operator.

###### \_\_ipow\_\_
Implements behavior for exponents with assignment using the \*\*= operator.

###### \_\_ilshift\_\_(self, other)
Implements left bitwise shift with assignment using the <<= operator.

###### \_\_irshift\_\_(self, other)
Implements right bitwise shift with assignment using the >>= operator.

###### \_\_iand\_\_(self, other)
Implements bitwise and with assignment using the &= operator.

###### \_\_ior\_\_(self, other)
Implements bitwise or with assignment using the |= operator.

###### \_\_ixor\_\_(self, other)
Implements bitwise xor with assignment using the ^= operator.

##### Type conversion magic methods  类型转换魔术方法

Python also has an array of magic methods designed to implement behavior for built in type conversion functions like float(). Here they are:  Python还有一系列魔术方法，用于实现内置类型转换函数（如float（））的行为。 他们来了：

###### \_\_int\_\_(self)
Implements type conversion to int.

###### \_\_long\_\_(self)
Implements type conversion to long.

###### \_\_float\_\_(self)
Implements type conversion to float.

###### \_\_complex\_\_(self)
Implements type conversion to complex.

###### \_\_oct\_\_(self)
Implements type conversion to octal.

###### \_\_hex\_\_(self)
Implements type conversion to hexadecimal.

###### \_\_index\_\_(self)
Implements type conversion to an int when the object is used in a slice expression. If you define a custom numeric type that might be used in slicing, you should define \_\_index\_\_.

###### \_\_trunc\_\_(self)
Called when math.trunc(self) is called. \_\_trunc\_\_ should return the value of \`self truncated to an integral type (usually a long).

###### \_\_coerce\_\_(self, other)
Method to implement mixed mode arithmetic. \_\_coerce\_\_ should return None if type conversion is impossible. Otherwise, it should return a pair (2-tuple) of self and other, manipulated to have the same type.

### Representing your Classes

It's often useful to have a string representation of a class. In Python, there are a few methods that you can implement in your class definition to customize how built in functions that return representations of your class behave.  拥有类的字符串表示通常很有用。 在Python中，您可以在类定义中实现一些方法，以自定义返回类的表示形式的内置函数的行为。

###### \_\_str\_\_(self)
Defines behavior for when str() is called on an instance of your class.  定义在类的实例上调用str（）时的行为。

###### \_\_repr\_\_(self)
Defines behavior for when repr() is called on an instance of your class. The major difference between str() and repr() is intended audience. repr() is intended to produce output that is mostly machine-readable (in many cases, it could be valid Python code even), whereas str() is intended to be human-readable.  定义在类的实例上调用repr（）时的行为。 str（）和repr（）之间的主要区别在于受众。 repr（）旨在生成大多数机器可读的输出（在许多情况下，它甚至可能是有效的Python代码），而str（）旨在是人类可读的。

###### \_\_unicode\_\_(self)
Defines behavior for when unicode() is called on an instance of your class. unicode() is like str(), but it returns a unicode string. Be wary: if a client calls str() on an instance of your class and you've only defined \_\_unicode\_\_(), it won't work. You should always try to define \_\_str\_\_() as well in case someone doesn't have the luxury of using unicode.  定义在类的实例上调用unicode（）时的行为。 unicode（）与str（）类似，但它返回一个unicode字符串。警惕：如果客户端在类的实例上调用str（）并且您只定义了\_\_unicode \_\_（），则它将无效。你应该总是尝试定义\_\_str \_\_（）以防万一有人没有使用unicode的奢侈。

###### \_\_format\_\_(self, formatstr)
Defines behavior for when an instance of your class is used in new-style string formatting. For instance, "Hello, {0:abc}!".format(a) would lead to the call a.\_\_format\_\_("abc"). This can be useful for defining your own numerical or string types that you might like to give special formatting options.  定义在新样式字符串格式中使用类实例的行为。例如，“Hello，{0：abc}！”格式（a）将导致调用.\_\_格式\_\_（“abc”）。这对于定义您可能希望提供特殊格式选项的数字或字符串类型非常有用。

###### \_\_hash\_\_(self)
Defines behavior for when hash() is called on an instance of your class. It has to return an integer, and its result is used for quick key comparison in dictionaries. Note that this usually entails implementing \_\_eq\_\_ as well. Live by the following rule: a == b implies hash(a) == hash(b).  定义在类的实例上调用hash（）时的行为。它必须返回一个整数，其结果用于字典中的快速键比较。请注意，这通常也需要实现\_\_eq\_\_。按以下规则生活：a == b表示哈希（a）==哈希（b）。

###### \_\_nonzero\_\_(self)
Defines behavior for when bool() is called on an instance of your class. Should return True or False, depending on whether you would want to consider the instance to be True or False.  定义在类的实例上调用bool（）时的行为。应返回True或False，具体取决于您是否要将实例视为True或False。

###### \_\_dir\_\_(self)
Defines behavior for when dir() is called on an instance of your class. This method should return a list of attributes for the user. Typically, implementing \_\_dir\_\_ is unnecessary, but it can be vitally important for interactive use of your classes if you redefine \_\_getattr\_\_ or \_\_getattribute\_\_ (which you will see in the next section) or are otherwise dynamically generating attributes.  定义在类的实例上调用dir（）时的行为。此方法应返回用户的属性列表。通常，实现\_\_dir\_\_是不必要的，但如果重新定义\_\_getattr\_\_或\_\_getattribute \_\_（您将在下一节中看到）或以其他方式动态生成属性，则对于类的交互式使用非常重要。

###### \_\_sizeof\_\_(self)
Defines behavior for when sys.getsizeof() is called on an instance of your class. This should return the size of your object, in bytes. This is generally more useful for Python classes implemented in C extensions, but it helps to be aware of it.  定义在类的实例上调用sys.getsizeof（）时的行为。这应该返回对象的大小，以字节为单位。这对于在C扩展中实现的Python类通常更有用，但它有助于了解它。

We're pretty much done with the boring (and example-free) part of the magic methods guide. Now that we've covered some of the more basic magic methods, it's time to move to more advanced material.  我们已经完成了魔术方法指南中的无聊（并且没有示例）部分。 现在我们已经介绍了一些更基本的魔术方法，现在是时候转向更高级的材料了。

### Controlling Attribute Access

Many people coming to Python from other languages complain that it lacks true encapsulation for classes; that is, there's no way to define private attributes with public getter and setters. This couldn't be farther than the truth: it just happens that Python accomplishes a great deal of encapsulation through "magic", instead of explicit modifiers for methods or fields. Take a look:  许多从其他语言进入Python的人抱怨它缺乏对类的真正封装; 也就是说，没有办法用公共getter和setter定义私有属性。 这不可能比事实更进一步：它恰好发生了Python通过“魔术”完成大量封装，而不是方法或字段的显式修饰符。 看一看：

###### \_\_getattr\_\_(self, name)
You can define behavior for when a user attempts to access an attribute that `doesn't exist` (either at all or yet). This can be useful for catching and redirecting common misspellings, giving warnings about using deprecated attributes (you can still choose to compute and return that attribute, if you wish), or deftly handing an AttributeError. It only gets called when a nonexistent attribute is accessed, however, so it isn't a true encapsulation solution.  您可以定义用户何时尝试访问不存在的属性（完全或尚未访问）的行为。这对于捕获和重定向常见的拼写错误非常有用，可以提供有关使用弃用属性的警告（如果愿意，您仍然可以选择计算并返回该属性），或者巧妙地处理AttributeError。它只在访问不存在的属性时被调用，但是，它不是真正的封装解决方案。

###### \_\_setattr\_\_(self, name, value)
Unlike \_\_getattr\_\_, \_\_setattr\_\_ is an encapsulation solution. It allows you to define behavior for assignment to an attribute regardless of whether or not that attribute exists, meaning you can define custom rules for any changes in the values of attributes. However, you have to be careful with how you use \_\_setattr\_\_, as the example at the end of the list will show.  与\_\_getattr\_\_不同，\_\_ setattr\_\_是一种封装解决方案。它允许您定义分配给属性的行为，无论该属性是否存在，这意味着您可以为属性值的任何更改定义自定义规则。但是，您必须小心如何使用\_\_setattr\_\_，因为列表末尾的示例将显示。

###### \_\_delattr\_\_(self, name)
This is the exact same as \_\_setattr\_\_, but for deleting attributes instead of setting them. The same precautions need to be taken as with \_\_setattr\_\_ as well in order to prevent infinite recursion (calling del self.name in the implementation of \_\_delattr\_\_ would cause infinite recursion).  这与\_\_setattr\_\_完全相同，但用于删除属性而不是设置它们。为了防止无限递归，需要采取与\_\_setattr\_\_相同的预防措施（在\_\_delattr\_\_的实现中调用del self.name会导致无限递归）。

###### \_\_getattribute\_\_(self, name)
After all this, \_\_getattribute\_\_ fits in pretty well with its companions \_\_setattr\_\_ and \_\_delattr\_\_. However, I don't recommend you use it. \_\_getattribute\_\_ can `only be used with new-style classes` (all classes are new-style in the newest versions of Python, and in older versions you can make a class new-style by subclassing object. It allows you to define rules for whenever an attribute's value is accessed. It suffers from some similar infinite recursion problems as its partners-in-crime (this time you call the base class's \_\_getattribute\_\_ method to prevent this). It also mainly obviates the need for \_\_getattr\_\_, which, when \_\_getattribute\_\_ is implemented, only gets called if it is called explicitly or an AttributeError is raised. This method can be used (after all, it's your choice), but I don't recommend it because it has a small use case (it's far more rare that we need special behavior to retrieve a value than to assign to it) and because it can be really difficult to implement bug-free.  毕竟，\_\_ getattribute\_\_与其同伴\_\_setattr\_\_和\_\_delattr\_\_非常吻合。但是，我不建议你使用它。 \_\_getattribute\_\_只能用于新式的类（所有类在最新版本的Python中都是新式的，而在旧版本中，你可以通过子类化对象来创建一个新类。它允许你为属性的每一个定义规则它被访问了。它遇到了一些类似的无限递归问题，就像它的犯罪伙伴一样（这次你调用基类的\_\_getattribute\_\_方法来防止这种情况）。它还主要避免了\_\_getattr\_\_的需要，当\_\_getattribute\_\_被实现时，只有在显式调用或引发AttributeError时才会被调用。这个方法可以使用（毕竟，这是你的选择），但我不推荐它，因为它有一个小的用例（我们需要的更为罕见）检索值而不是分配给它的特殊行为，并且因为实现无bug实际上很困难。

You can easily cause a problem in your definitions of any of the methods controlling attribute access. Consider this example:  您可以轻松地在控制属性访问的任何方法的定义中出现问题。 考虑这个例子：

```python
def __setattr__(self, name, value):
    self.name = value
    # since every time an attribute is assigned, __setattr__() is called, this
    # is recursion 递归.
    # so this really means self.__setattr__('name', value). Since the method
    # keeps calling itself, the recursion goes on forever causing a crash 

def __setattr__(self, name, value):
    self.__dict__[name] = value # assigning to the dict of names in the class
    # define custom behavior here
```

Again, Python's magic methods are incredibly powerful, and with great power comes great responsibility. It's important to know the proper way to use magic methods so you don't break any code.  再一次，Python的神奇方法非常强大，并且强大的功能带来了巨大的责任。 了解使用魔术方法的正确方法非常重要，这样您就不会破坏任何代码。

So, what have we learned about custom attribute access in Python? It's not to be used lightly. In fact, it tends to be excessively powerful and counter-intuitive. But the reason why it exists is to scratch a certain itch: Python doesn't seek to make bad things impossible, but just to make them difficult. Freedom is paramount, so you can really do whatever you want. Here's an example of some of the special attribute access methods in action (note that we use super because not all classes have an attribute \_\_dict\_\_):  那么，我们在Python中了解了自定义属性访问的哪些内容？ 它不能被轻易使用。 事实上，它往往过于强大和反直觉。 但它存在的原因是为了划清某种痒：Python不会试图让坏事变得不可能，而只是为了让它们变得困难。 自由是至关重要的，所以你可以真正做任何你想做的事。 以下是一些特殊属性访问方法的示例（请注意，我们使用super，因为并非所有类都具有属性\_\_dict\_\_）：

```python
class AccessCounter(object):
    '''A class that contains a value and implements an access counter.
    The counter increments each time the value is changed.'''

    def __init__(self, val):
        super(AccessCounter, self).__setattr__('counter', 0)
        super(AccessCounter, self).__setattr__('value', val)

    def __setattr__(self, name, value):
        if name == 'value':
            super(AccessCounter, self).__setattr__('counter', self.counter + 1)
        # Make this unconditional.
        # If you want to prevent other attributes to be set, raise AttributeError(name)
        super(AccessCounter, self).__setattr__(name, value)

    def __delattr__(self, name):
        if name == 'value':
            super(AccessCounter, self).__setattr__('counter', self.counter + 1)
        super(AccessCounter, self).__delattr__(name)
        
```











Making Custom Sequences
Reflection
Abstract Base Classes
Callable Objects
Context Managers
Building Descriptor Objects
Copying
Pickling your Objects
Conclusion
Appendix 1: How to Call Magic Methods
Appendix 2: Changes in Python 3



note:

\_\_hash\_\_()
\_\_eq\_\_()

\_\_getattr\_\_(self, name)
\_\_getattribute\_\_(self, name)



