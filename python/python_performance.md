## 自定义类、闭包、生成器的性能比较

```python

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

# 自定义类
class Countdown(object):
    def __init__(self, n):
        self.n = n

    def next(self):
        r = self.n
        self.n -= 1
        return r

start_cpu = time.clock()
start_real = time.time()
c = Countdown(10000000)
while True:
    v = c.next()
    if not v:
        break

print('cpu: ', time.clock() - start_cpu)  # cpu:  13.252639
print('real: ', time.time() - start_real)  # real:  13.306921482086182

# 闭包
def countdown(n):
    def next():
        nonlocal n
        r = n
        n -= 1
        return r
    return next

start_cpu = time.clock()
start_real = time.time()
next = countdown(10000000)
while True:
    v = next()
    if not v:
        break
print('cpu: ', time.clock() - start_cpu)  # cpu:  7.480021000000001
print('real: ', time.time() - start_real)  # real:  7.515174627304077

# 生成器
def countdownyield(n):
    while n > 0:
        yield n
        n -= 1
    return

start_cpu = time.clock()
start_real = time.time()
c_yield = countdownyield(10000000)
for n in c_yield:
    pass
print('cpu: ', time.clock() - start_cpu)  # cpu:  5.4382800000000024
print('real: ', time.time() - start_real)  # real:  5.46284294128418
```