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





















Making Operators Work on Custom Classes
Comparison magic methods
Numeric magic methods
Representing your Classes
Controlling Attribute Access
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





