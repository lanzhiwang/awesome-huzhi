## SQLAlchemy's "backref " and "back_populates" Parameter


I have this code

```
#!/usr/bin/env python
# encoding: utf-8
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base(bind=engine)

class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    children = relationship("Child")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))
    parent = relationship("Parent")

Base.metadata.create_all()

p = Parent()
session.add(p)
session.commit()
c = Child(parent_id=p.id)
session.add(c)
session.commit()
print "children: {}".format(p.children[0].id)
print "parent: {}".format(c.parent.id)
```