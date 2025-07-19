"""

A    C
^
|
B

"""


class A(object):
    pass


class B(A):
    pass


class C(object):
    pass


a = A()
b = B()
c = C()

print(type(a))  # <class '__main__.A'>
print(isinstance(a, A))  # True
print(isinstance(a, object))  # True
print(isinstance(a, B))  # False
print(isinstance(a, C))  # False

print(isinstance(b, A))  # True
print(isinstance(b, object))  # True
print(isinstance(b, B))  # True
print(isinstance(b, C))  # False

print(isinstance(c, A))  # False
print(isinstance(c, object))  # True
print(isinstance(c, B))  # False
print(isinstance(c, C))  # True

print("---" * 30)

print(issubclass(A, object))  # True
print(issubclass(A, A))  # True
print(issubclass(A, B))  # False
print(issubclass(A, C))  # False

print(issubclass(B, object))  # True
print(issubclass(B, A))  # True
print(issubclass(B, B))  # True
print(issubclass(B, C))  # False

print(issubclass(C, object))  # True
print(issubclass(C, A))  # False
print(issubclass(C, B))  # False
print(issubclass(C, C))  # True
