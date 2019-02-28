## SQLAlchemy's "backref " and "back_populates" Parameter

### 在定义模型时没有定义 relationship

```
# 没有定义 relationship
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))

# 在没有定义 relationship 的情况下，给定参数 User.name，获取该 user 的 addresses 的方法如下：
user = session.query(User).filter_by(name=user_name).first()
addresses = session.query(Address).filter_by(user_id=user.id).all()
```

### 在定义模型时定义 relationship

```
# 在 User 中使用 relationship 定义 addresses 属性
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    addresses = relationship("Address")

class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))

# 直接在 User 对象中通过 addresses 属性获得指定用户的所有地址：
user = session.query(User).filter_by(name=user_name).first()
user.addresses

# 通过 User 对象获取所拥有的地址，但是不能通过 Address 对象获取到所属的用户，因为在 addresses 属性中没有定义 backref 属性
>>> u = User()
>>> u.addresses
[]
>>> a = Address()
>>> a.user
Traceback (most recent call last):
  File "<input>", line 1, in <module>
AttributeError: 'Address' object has no attribute 'user'

```

### 在定义模型时定义 relationship，同时定义 backref 属性

```
# 定义 backref 属性
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    addresses = relationship("Address", backref="user")

class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))

# 通过 Address 对象获取到所属的用户
>>> u = User()
>>> u.addresses
[]
>>> a = Address()
>>> a.user
[]

```

### relationship 的 back_populates 参数

在最新版本的 sqlalchemy 中对 relationship 引进了 back_populates 参数。这个参数和 backref 的区别是只提供单向的关系引用，且必须成对存在，但是完成的功能和 backref 是一样的。

```
# 使用 backref 参数
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    addresses = relationship("Address", backref="user")

class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))

```

实际上相当于：

```
# 使用 back_populates 参数
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    addresses = relationship("Address", back_populates="user")

class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="addresses")

```

### 结论

* backref 和 back_populates 两个参数不能同时使用

* back_populates 参数必须在父表和子表中成对存在

* 在父表和子表中都不定义 relationship
	* 需要两次查询

* 在父表一个表中定义 relationship
	* backref 和 back_populates 两个参数都不使用
	* 只使用 backref 参数
	* 不能只使用 back_populates 参数，因为 back_populates 参数必须在父表和子表中成对存在
	* 不能同时使用 backref 和 back_populates

* 在子表一个表中定义 relationship，类似于在父表一个表中定义 relationship

* 在父表和子表中都定义 relationship
	* 父表没有 backref 和 back_populates 两个参数，子表没有 backref 和 back_populates 两个参数
	* 父表没有 backref 和 back_populates 两个参数，子表只有 backref 参数

	* 父表只有 backref 参数，子表没有 backref 和 back_populates 两个参数
	* 父表只有 backref 参数，子表只有 backref 参数

	* 父表只有 back_populates 参数，子表只有 back_populates 参数

```
父表没有 backref 和 back_populates 两个参数
父表只有 backref 参数
父表只有 back_populates 参数
父表 backref 和 back_populates 两个参数都有，这种情况不可能

子表没有 backref 和 back_populates 两个参数
子表只有 backref 参数
子表只有 back_populates 参数
子表 backref 和 back_populates 两个参数都有，这种情况不可能
```

* [参考1](https://www.zhihu.com/question/38456789)
* [参考2](https://stackoverflow.com/questions/39869793/when-do-i-need-to-use-sqlalchemy-back-populates)

