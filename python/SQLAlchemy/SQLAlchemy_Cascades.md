## Cascades

Mappers support the concept of configurable cascade behavior on relationship() constructs. This refers to how operations performed on a “parent” object relative to a particular Session should be propagated to items referred to by that relationship (e.g. “child” objects), and is affected by the relationship.cascade option.  Mappers支持关系()构造的可配置级联行为的概念。 这指的是对“父”对象相对于特定会话执行的操作应如何传播到该关系所引用的项（例如“子”对象），并受relationship.cascade选项的影响。

The default behavior of cascade is limited to cascades of the so-called `save-update` and `merge` settings. The typical “alternative” setting for cascade is to add the `delete` and `delete-orphan` options; these settings are appropriate for related objects which only exist as long as they are attached to their parent, and are otherwise deleted.  级联的默认行为仅限于所谓的保存更新和合并设置的级联。 级联的典型“替代”设置是添加delete和delete-orphan选项; 这些设置适用于相关对象，这些对象只有在附加到父对象时才存在，否则将被删除。

Cascade behavior is configured using the cascade option on relationship():

```
class Order(Base):
    __tablename__ = 'order'

    items = relationship("Item", cascade="all, delete-orphan")
    customer = relationship("User", cascade="save-update")
```

To set cascades on a backref, the same flag can be used with the backref() function, which ultimately feeds its arguments back into relationship():

```
class Item(Base):
    __tablename__ = 'item'

    order = relationship("Order",
                    backref=backref("items", cascade="all, delete-orphan")
                )
```

The default value of cascade is `save-update`, `merge`. The typical alternative setting for this parameter is either `all` or more commonly `all, delete-orphan`. The `all` symbol is a synonym for `save-update, merge, refresh-expire, expunge, delete`, and using it in conjunction with `delete-orphan` indicates that the child object should follow along with its parent in all cases, and be deleted once it is no longer associated with that parent.  cascade的默认值是save-update，merge。 此参数的典型替代设置是全部或更常见的全部，delete-orphan。 all符号是save-update，merge，refresh-expire，expunge，delete的同义词，并且与delete-orphan一起使用它表示子对象在所有情况下都应该跟随其父对象，并且一旦被删除就被删除 不再与该父级关联。

The list of available values which can be specified for the cascade parameter are described in the following subsections.

* save-update
* delete
* delete-orphan
* merge
* refresh-expire
* expunge
* all（save-update、merge、refresh-expire、expunge、delete）

### 各种级联关系的简单解释

* save-update 

将一个对象添加到 session 中，与该对象关联的所有对象自动都被添加到 session 中

* delete

将父对象删除，与之关联的所有子对象也**自动被删除**

* delete-orphan

标记删除 delete-orphan 级联关系起作用，在 user 实例中标记删除 addresses
> del user.addresses[1]

* merge

Session.merge()

* refresh-expire

Session.expire()

* expunge

Session.expunge()

* all（save-update、merge、refresh-expire、expunge、delete）



### save-update

`save-update` cascade indicates that when an object is placed into a Session via Session.add(), all the objects associated with it via this relationship() should also be added to that same Session. Suppose we have an object user1 with two related objects address1, address2:

```
>>> user1 = User()
>>> address1, address2 = Address(), Address()
>>> user1.addresses = [address1, address2]
```

If we add user1 to a Session, it will also add address1, address2 implicitly:

```
>>> sess = Session()
>>> sess.add(user1)
>>> address1 in sess
True
```

save-update cascade also affects attribute operations for objects that are already present in a Session. If we add a third object, address3 to the user1.addresses collection, it becomes part of the state of that Session:

```
>>> address3 = Address()
>>> user1.append(address3)
>>> address3 in sess
>>> True
```

save-update has the possibly surprising behavior which is that persistent objects which were removed from a collection or in some cases a scalar attribute may also be pulled into the Session of a parent object; this is so that the flush process may handle that related object appropriately. This case can usually only arise if an object is removed from one Session and added to another:  save-update具有可能令人惊讶的行为，即从集合中删除的持久对象或在某些情况下标量属性也可以被拉入父对象的Session中; 这是为了使刷新过程可以适当地处理该相关对象。 通常只有在从一个会话中删除对象并将其添加到另一个会话时才会出现这种情况：

```
>>> user1 = sess1.query(User).filter_by(id=1).first()
>>> address1 = user1.addresses[0]
>>> sess1.close()   # user1, address1 no longer associated with sess1
>>> user1.addresses.remove(address1)  # address1 no longer associated with user1
>>> sess2 = Session()
>>> sess2.add(user1)   # ... but it still gets added to the new session,
>>> address1 in sess2  # because it's still "pending" for flush
True
```

The save-update cascade is on by default, and is typically taken for granted; it simplifies code by allowing a single call to Session.add() to register an entire structure of objects within that Session at once. While it can be disabled, there is usually not a need to do so.  默认情况下，保存更新级联处于启用状态，通常认为是理所当然的。 它通过允许对Session.add（）的单次调用一次性注册该Session中的整个对象结构来简化代码。 虽然它可以被禁用，但通常不需要这样做。

One case where save-update cascade does sometimes get in the way is in that it takes place in both directions for bi-directional relationships, e.g. backrefs, meaning that the association of a child object with a particular parent can have the effect of the parent object being implicitly associated with that child object’s Session; this pattern, as well as how to modify its behavior using the cascade_backrefs flag, is discussed in the section Controlling Cascade on Backrefs.  

### delete

The delete cascade indicates that when a “parent” object is marked for deletion, its related “child” objects should also be marked for deletion. If for example we have a relationship User.addresses with delete cascade configured:

```
class User(Base):
    # ...

    addresses = relationship("Address", cascade="save-update, merge, delete")
```

If using the above mapping, we have a User object and two related Address objects:

```
>>> user1 = sess.query(User).filter_by(id=1).first()
>>> address1, address2 = user1.addresses
```

If we mark user1 for deletion, after the flush operation proceeds, address1 and address2 will also be deleted:

```
>>> sess.delete(user1)
>>> sess.commit()
DELETE FROM address WHERE address.id = ?
((1,), (2,))
DELETE FROM user WHERE user.id = ?
(1,)
COMMIT
```

Alternatively, if our User.addresses relationship does not have delete cascade, SQLAlchemy’s default behavior is to instead de-associate address1 and address2 from user1 by setting their foreign key reference to NULL. Using a mapping as follows:

```
class User(Base):
    # ...

    addresses = relationship("Address")
```

Upon deletion of a parent User object, the rows in address are not deleted, but are instead de-associated:

```
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

delete cascade is more often than not used in conjunction with delete-orphan cascade, which will emit a DELETE for the related row if the “child” object is deassociated from the parent. The combination of delete and delete-orphan cascade covers both situations where SQLAlchemy has to decide between setting a foreign key column to NULL versus deleting the row entirely.  delete cascade通常与delete-orphan cascade结合使用，如果“child”对象与父对象取消关联，它将为相关行发出DELETE。 delete和delete-orphan级联的组合涵盖了SQLAlchemy必须决定将外键列设置为NULL与完全删除行之间的情况。

When using a relationship() that also includes a many-to-many table using the secondary option, SQLAlchemy’s delete cascade handles the rows in this many-to-many table automatically. Just like, as described in Deleting Rows from the Many to Many Table, the addition or removal of an object from a many-to-many collection results in the INSERT or DELETE of a row in the many-to-many table, the delete cascade, when activated as the result of a parent object delete operation, will DELETE not just the row in the “child” table but also in the many-to-many table.

### delete-orphan

delete-orphan cascade adds behavior to the delete cascade, such that a child object will be marked for deletion when it is de-associated from the parent, not just when the parent is marked for deletion. This is a common feature when dealing with a related object that is “owned” by its parent, with a NOT NULL foreign key, so that removal of the item from the parent collection results in its deletion.

delete-orphan cascade implies that each child object can only have one parent at a time, so is configured in the vast majority of cases on a one-to-many relationship. Setting it on a many-to-one or many-to-many relationship is more awkward; for this use case, SQLAlchemy requires that the relationship() be configured with the single_parent argument, establishes Python-side validation that ensures the object is associated with only one parent at a time.

### merge

merge cascade indicates that the `Session.merge()` operation should be propagated from a parent that’s the subject of the Session.merge() call down to referred objects. This cascade is also on by default.

### refresh-expire

refresh-expire is an uncommon option, indicating that the `Session.expire()` operation should be propagated from a parent down to referred objects. When using Session.refresh(), the referred objects are expired only, but not actually refreshed.

### expunge

expunge cascade indicates that when the parent object is removed from the Session using `Session.expunge()`, the operation should be propagated down to referred objects.

### Controlling Cascade on Backrefs

The save-update cascade by default takes place on attribute change events emitted from backrefs. This is probably a confusing statement more easily described through demonstration; it means that, given a mapping such as this:

```
mapper(Order, order_table, properties={
    'items' : relationship(Item, backref='order')
})
```

If an Order is already in the session, and is assigned to the order attribute of an Item, the backref appends the Item to the items collection of that Order, resulting in the save-update cascade taking place:

```
>>> o1 = Order()
>>> session.add(o1)
>>> o1 in session
True

>>> i1 = Item()
>>> i1.order = o1
>>> i1 in o1.items
True
>>> i1 in session
True
```

This behavior can be disabled using the cascade_backrefs flag:

```
mapper(Order, order_table, properties={
    'items' : relationship(Item, backref='order',
                                cascade_backrefs=False)
})
```

So above, the assignment of i1.order = o1 will append i1 to the items collection of o1, but will not add i1 to the session. You can, of course, add() i1 to the session at a later point. This option may be helpful for situations where an object needs to be kept out of a session until it’s construction is completed, but still needs to be given associations to objects which are already persistent in the target session.




















