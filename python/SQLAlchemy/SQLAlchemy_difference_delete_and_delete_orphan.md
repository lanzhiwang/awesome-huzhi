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