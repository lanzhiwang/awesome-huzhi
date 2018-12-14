## exec & eval

Python privides the whole interpreter as a built-in function. You can pass a string and ask it is execute that piece of code at run time.

For example:

```python
>>> exec("x = 1")
>>> x
>>> 1
```

By default exec works in the current environment, so it updated the globals in the above example. It is also possible to specify an environment to exec.

```python
>>> env = {'a' : 42}
>>> exec('x = a+1', env)
>>> print env['x']
>>> 43
```

It is also possible to create functions or classes dynamically using exec, though it is usually not a good idea.

```python
>>> code = 'def add_%d(x): return x + %d'
>>> for i in range(1, 5):
>>> ...     exec(code % (i, i))
>>> ...
>>> add_1(3)
>>> 4
>>> add_3(3)
>>> 6
```

eval is like exec but it takes an expression and returns its value.

```python
>>> eval("2+3")
>>> 5
>>> a = 2
>>> eval("a * a")
>>> 4
>>> env = {'x' : 42}
>>> eval('x+1', env)
>>> 43
```

参考：

- https://anandology.com/python-practice-book/functional-programming.html#exec-eval

