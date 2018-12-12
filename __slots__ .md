## \_\_slots\_\_  魔方方法说明

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from types import MethodType

class Student(object):
    '''测试 __slots__ 属性必须使用新式类
    __slots__ 只对实例属性和方法起限制作用
    
    实例属性
        - class 中定义
        - 动态添加

    实例方法
        - class 中定义
        - 动态添加

    类属性
        - class 中定义
        - 动态添加

    类方法
        - 动态添加
    '''
    __slots__ = ('name', 'age', 'score', 'set_score')

    # 在 class 中定义的类属性不需要添加到 __slots__中
    number = 10

    def __init__(self, name, age, color):
        ''' AttributeError: 'Student' object has no attribute '__dict__'
        __dict__ 和 __slots__ 不能同时使用
        '''
        # self.__dict__.update(kw)

        '''在 class 实例中添加的实例属性全部要添加到 __slots__ 中
        '''
        self.name = name
        self.age = age
        # self.color = color  # AttributeError: 'Student' object has no attribute 'color'

    '''在 class 实例中添加的实例方法不需要添加到 __slots__ 中
    '''
    def set_age(self, age):
        self.age = age

s = Student('jim', 11, 'red')
# s.other = 5  # AttributeError: 'Student' object has no attribute 'other'

print s.number

'''
动态添加的实例属性和方法全部要添加到 __slots__ 中
'''
def set_score(self, score):
    self.score = score

s.set_score = MethodType(set_score, s, Student) # 给实例绑定一个方法
s.set_score(25)
print s.score

s.set_age(15)
print s.age

'''
可以动态添加类方法不需要添加到 __slots__ 中
但是实例属性还是要添加
'''
def set_grade(self, grade):
    self.grade = grade

Student.set_grade = MethodType(set_grade, None, Student)
s.set_grade(3)  # 'Student' object has no attribute 'grade'

```

