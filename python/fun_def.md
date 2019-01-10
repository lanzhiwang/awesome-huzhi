## 函数的定义

### 普通参数 + 默认值参数
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''参数定义的顺序必须是：普通参数 + 默认值参数 + 位置参数 + 关键字参数
'''
def foo(x, y, z=None, t=None, *args, **kwargs):
    print x
    print y
    print z
    print t
    print args
    print kwargs

'''
x, y 必须赋值，赋值的方式是：位置参数或者关键字参数
1, 2
x=1, y=2
1, y=2
x=1, 2

z, t 可以赋值，也可以不赋值，赋值的方式是：位置参数或者关键字参数
3, 4
z=3, t=4
3, t=4
z=3, 4

args 可以赋值，也可以不赋值，赋值的方式是位置参数

kwargs 可以赋值，也可以不赋值，赋值的方式是关键字参数

'''

'''
x, y 必须赋值，z, t 不赋值
'''
foo(1, 2)
foo(x=1, y=2)  # 可以任意顺序
foo(1, y=2)
# foo(x=1, 2)  # SyntaxError: non-keyword arg after keyword arg

'''
x, y 必须赋值，z, t 赋值 3, 4
'''
foo(1, 2, 3, 4)
# foo(x=1, y=2, 3, 4)  # SyntaxError: non-keyword arg after keyword arg
# foo(1, y=2, 3, 4)  # SyntaxError: non-keyword arg after keyword arg
# foo(x=1, 2, 3, 4)  # SyntaxError: non-keyword arg after keyword arg

'''
x, y 必须赋值，z, t 赋值 z=3, t=4
'''
foo(1, 2, z=3, t=4)  # 可以任意顺序
foo(x=1, y=2, z=3, t=4)  # 可以任意顺序
foo(1, y=2, z=3, t=4)  # 可以任意顺序
# foo(x=1, 2, z=3, t=4)  # SyntaxError: non-keyword arg after keyword arg

'''
x, y 必须赋值，z, t 赋值 3, t=4
'''
foo(1, 2, 3, t=4)
# foo(x=1, y=2, 3, t=4)  # SyntaxError: non-keyword arg after keyword arg
# foo(1, y=2, 3, t=4)  # SyntaxError: non-keyword arg after keyword arg
# foo(x=1, 2, 3, t=4)  # SyntaxError: non-keyword arg after keyword arg

'''
x, y 必须赋值，z, t 赋值 z=3, 4
'''
# foo(1, 2, z=3, 4)  # SyntaxError: non-keyword arg after keyword arg
# foo(x=1, y=2, z=3, 4)  # SyntaxError: non-keyword arg after keyword arg
# foo(1, y=2, z=3, 4)  # SyntaxError: non-keyword arg after keyword arg
# foo(x=1, 2, z=3, 4)  # SyntaxError: non-keyword arg after keyword arg


```

### 普通参数 + 默认值参数 + 位置参数 + 关键字参数

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''参数定义的顺序必须是：普通参数 + 默认值参数 + 位置参数 + 关键字参数
'''
def foo(x, y, z=None, t=None, *args, **kwargs):
    print x
    print y
    print z
    print t
    print args
    print kwargs

'''
x, y 必须赋值，赋值的方式是：位置参数或者关键字参数
1, 2
x=1, y=2
1, y=2
x=1, 2

z, t 可以赋值，也可以不赋值，赋值的方式是：位置参数或者关键字参数
3, 4
z=3, t=4
3, t=4
z=3, 4

args 可以赋值，也可以不赋值，赋值的方式是位置参数

kwargs 可以赋值，也可以不赋值，赋值的方式是关键字参数

'''

'''
x, y 必须赋值，z, t 不赋值
'''
foo(1, 2)  # 此时不能对 args 赋值， 只能对 kwargs 赋值
foo(x=1, y=2)  # 此时不能对 args 赋值， 只能对 kwargs 赋值
foo(1, y=2)  # 此时不能对 args 赋值， 只能对 kwargs 赋值

'''
x, y 必须赋值，z, t 赋值 3, 4
'''
foo(1, 2, 3, 4)  # 此时可以对 args 赋值， 也能对 kwargs 赋值

'''
x, y 必须赋值，z, t 赋值 z=3, t=4
'''
foo(1, 2, z=3, t=4)  # # 此时不能对 args 赋值， 只能对 kwargs 赋值
foo(x=1, y=2, z=3, t=4)  # # 此时不能对 args 赋值， 只能对 kwargs 赋值
foo(1, y=2, z=3, t=4)  # # 此时不能对 args 赋值， 只能对 kwargs 赋值

'''
x, y 必须赋值，z, t 赋值 3, t=4
'''
foo(1, 2, 3, t=4)  # # 此时不能对 args 赋值， 只能对 kwargs 赋值

'''
x, y 必须赋值，z, t 赋值 z=3, 4
'''

```
