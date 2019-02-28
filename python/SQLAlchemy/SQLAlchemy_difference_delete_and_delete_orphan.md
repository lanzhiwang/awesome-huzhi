## What is the difference between delete-orphan and delete?

### delete 特性

```
class User(Base):
    addresses = relationship("Address", cascade="save-update, merge, delete")

>>> sess.delete(user1)
>>> sess.commit()
DELETE FROM address WHERE address.id = ?
((1,), (2,))
DELETE FROM user WHERE user.id = ?
(1,)
COMMIT

#########################################

class User(Base):
    addresses = relationship("Address")

>>> sess.delete(user1)
>>> sess.commit()
UPDATE address SET user_id=? WHERE address.id = ?
(None, 1)
UPDATE address SET user_id=? WHERE address.id = ?
(None, 2)
DELETE FROM user WHERE user.id = ?
(1,)
COMMIT

```

### delete-orphan 特性

```
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
    addresses = relationship("Address", backref='user', cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password'%s')>" % (self.name, self.fullname, self.password)

class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address
    
>>> jack = session.query(User).get(5)
BEGIN (implicit)
SELECT users.id AS users_id,
users.name AS users_name,
users.fullname AS users_fullname,
users.password AS users_password
FROM users
WHERE users.id = ?
(5,)

# 标记删除 delete-orphan 级联关系起作用
# remove one Address (lazy load fires off) 在 user 实例中标记删除 addresses
>>> del jack.addresses[1]
SELECT addresses.id AS addresses_id,
addresses.email_address AS addresses_email_address,
addresses.user_id AS addresses_user_id
FROM addresses
WHERE ? = addresses.user_id
(5,)

# only one address remains
>>> session.query(Address).filter(Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])).count() # doctest: +NORMALIZE_WHITESPACE
DELETE FROM addresses WHERE addresses.id = ?
(2,)
SELECT count(*) AS count_1
FROM (SELECT addresses.id AS addresses_id,
addresses.email_address AS addresses_email_address,
addresses.user_id AS addresses_user_id
FROM addresses
WHERE addresses.email_address IN (?, ?)) AS anon_1
('jack@google.com', 'j25@yahoo.com')
1

# 直接删除父对象 delete 级联关系起作用
>>> session.delete(jack)
>>> session.query(User).filter_by(name='jack').count()
DELETE FROM addresses WHERE addresses.id = ?
(1,)
DELETE FROM users WHERE users.id = ?
(5,)
SELECT count(*) AS count_1
FROM (SELECT users.id AS users_id,
users.name AS users_name,
users.fullname AS users_fullname,
users.password AS users_password
FROM users
WHERE users.name = ?) AS anon_1
('jack',)
0
```






###  在级联关系中使用 delete

```
import os
filename = __file__.split('.')[0]
path = os.path.dirname(os.path.realpath(__file__))
db_path = 'sqlite:///{}/{}.db'.format(path, filename)

from datetime import datetime

from sqlalchemy import (create_engine, Column, Integer, String, DateTime,
                        Float, ForeignKey, and_)
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects import mysql
from sqlalchemy import inspect

Base = declarative_base()

class Order(Base):
    __tablename__ = 'order'

    order_id = Column(Integer, primary_key=True)
    customer_name = Column(String(30), nullable=False)
    order_date = Column(DateTime, nullable=False, default=datetime.now())

    order_items = relationship("OrderItem", cascade="save-update, delete",
                               backref='order')

    def __init__(self, customer_name):
        self.customer_name = customer_name


class OrderItem(Base):
    __tablename__ = 'orderitem'
    item_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.order_id'))
    price = Column(Float, nullable=False)

    def __init__(self, price=10):
        self.price = price

if __name__ == '__main__':
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)

    session = Session(engine)

    # create an order
    order = Order('john smith')

    # add three OrderItem associations to the Order and save
    order.order_items.append(OrderItem())
    order.order_items.append(OrderItem(10.99))
    session.add(order)
    session.commit()

    print("Before delete, Order = {0}".format(session.query(Order).count()))
    print("Before delete, OrderItem = {0}".format(session.query(OrderItem).count()))

    session.delete(order)
    session.commit()

    print("After delete, Order = {0}".format(session.query(Order).count()))
    print("After delete, OrderItem = {0}".format(session.query(OrderItem).count()))

(venv) $ python test.py 
Before delete, Order = 1
Before delete, OrderItem = 2
After delete, Order = 0
After delete, OrderItem = 0
(venv) $ 

```

###  在级联关系中使用 delete-orphan

```
import os
filename = __file__.split('.')[0]
path = os.path.dirname(os.path.realpath(__file__))
db_path = 'sqlite:///{}/{}.db'.format(path, filename)

from datetime import datetime

from sqlalchemy import (create_engine, Column, Integer, String, DateTime,
                        Float, ForeignKey, and_)
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects import mysql
from sqlalchemy import inspect

Base = declarative_base()

class Order(Base):
    __tablename__ = 'order'

    order_id = Column(Integer, primary_key=True)
    customer_name = Column(String(30), nullable=False)
    order_date = Column(DateTime, nullable=False, default=datetime.now())

    order_items = relationship("OrderItem", cascade="save-update, delete-orphan",
                               backref='order')

    def __init__(self, customer_name):
        self.customer_name = customer_name


class OrderItem(Base):
    __tablename__ = 'orderitem'
    item_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.order_id'))
    price = Column(Float, nullable=False)

    def __init__(self, price=10):
        self.price = price

if __name__ == '__main__':
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)

    session = Session(engine)

    # create an order
    order = Order('john smith')

    # add three OrderItem associations to the Order and save
    order.order_items.append(OrderItem())
    order.order_items.append(OrderItem(10.99))
    session.add(order)
    session.commit()

    print("Before delete, Order = {0}".format(session.query(Order).count()))
    print("Before delete, OrderItem = {0}".format(session.query(OrderItem).count()))

    session.delete(order)
    session.commit()

    print("After delete, Order = {0}".format(session.query(Order).count()))
    print("After delete, OrderItem = {0}".format(session.query(OrderItem).count()))

(venv) $ python test.py 
SAWarning: The 'delete-orphan' cascade option requires 'delete'.
  "The 'delete-orphan' cascade " "option requires 'delete'."
Before delete, Order = 1
Before delete, OrderItem = 2
After delete, Order = 0
After delete, OrderItem = 2
(venv) $ 

```

###  在级联关系中使用 delete-orphan 和 delete

```
import os
filename = __file__.split('.')[0]
path = os.path.dirname(os.path.realpath(__file__))
db_path = 'sqlite:///{}/{}.db'.format(path, filename)

from datetime import datetime

from sqlalchemy import (create_engine, Column, Integer, String, DateTime,
                        Float, ForeignKey, and_)
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects import mysql
from sqlalchemy import inspect

Base = declarative_base()

class Order(Base):
    __tablename__ = 'order'

    order_id = Column(Integer, primary_key=True)
    customer_name = Column(String(30), nullable=False)
    order_date = Column(DateTime, nullable=False, default=datetime.now())

    order_items = relationship("OrderItem", cascade="save-update, delete-orphan, delete",
                               backref='order')

    def __init__(self, customer_name):
        self.customer_name = customer_name


class OrderItem(Base):
    __tablename__ = 'orderitem'
    item_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.order_id'))
    price = Column(Float, nullable=False)

    def __init__(self, price=10):
        self.price = price

if __name__ == '__main__':
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)

    session = Session(engine)

    # create an order
    order = Order('john smith')

    # add three OrderItem associations to the Order and save
    order.order_items.append(OrderItem())
    order.order_items.append(OrderItem(10.99))
    session.add(order)
    session.commit()

    print("Before delete, Order = {0}".format(session.query(Order).count()))
    print("Before delete, OrderItem = {0}".format(session.query(OrderItem).count()))

    session.delete(order)
    session.commit()

    print("After delete, Order = {0}".format(session.query(Order).count()))
    print("After delete, OrderItem = {0}".format(session.query(OrderItem).count()))

(venv) $ python test.py 
Before delete, Order = 1
Before delete, OrderItem = 2
After delete, Order = 0
After delete, OrderItem = 0
(venv) $ 

```

[参考](https://stackoverflow.com/questions/5033547/sqlalchemy-cascade-delete)


