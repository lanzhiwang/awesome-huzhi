# 自定义类

```python
# -*- coding: utf-8 -*-

import copy

# 自定义类
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'point({}, {})'.format(self.x, self.y)


class Rectangle:
    def __init__(self, upper_left, bottom_right):
        self.upper_left = upper_left
        self.bottom_right = bottom_right

    def __repr__(self):
        return 'Rectangle({}, {})'.format(self.upper_left, self.bottom_right)


rectangle = Rectangle(Point(1, 2), Point(5, 6))
print rectangle  # Rectangle(point(1, 2), point(5, 6))

# 浅复制
copy_rectangle = copy.copy(rectangle)
print copy_rectangle  # Rectangle(point(1, 2), point(5, 6))

# 深复制
deepcopy_rectangle = copy.deepcopy(rectangle)
print deepcopy_rectangle  # Rectangle(point(1, 2), point(5, 6))

rectangle.upper_left.x = 2
print rectangle  # Rectangle(point(2, 2), point(5, 6))
print copy_rectangle  # Rectangle(point(2, 2), point(5, 6))
print deepcopy_rectangle  # Rectangle(point(1, 2), point(5, 6))

```

# 列表

```python
# -*- coding: utf-8 -*-

import copy

l = [[1, 2], [5, 6]]
print l  # [[1, 2], [5, 6]]

copy_l = copy.copy(l)  # 相当于 copy_l = list(l)
print copy_l  # [[1, 2], [5, 6]]

deepcopy_l = copy.deepcopy(l)
print deepcopy_l  # [[1, 2], [5, 6]]

l[0][0] = 2
print l  # [[2, 2], [5, 6]]
print copy_l  # [[2, 2], [5, 6]]
print deepcopy_l  # [[1, 2], [5, 6]]
```

```python
# -*- coding: utf-8 -*-

import copy

l = [[1, 2], [5, 6]]
print l  # [[1, 2], [5, 6]]

copy_l = list(l)  # 语法糖
print copy_l  # [[1, 2], [5, 6]]

deepcopy_l = copy.deepcopy(l)
print deepcopy_l  # [[1, 2], [5, 6]]

l[0][0] = 2
print l  # [[2, 2], [5, 6]]
print copy_l  # [[2, 2], [5, 6]]
print deepcopy_l  # [[1, 2], [5, 6]]
```

[参考](https://github.com/fluentpython/example-code/blob/master/08-obj-ref/bus.py)
