## SQLAlchemy commit(), flush(), expire(), refresh(), merge() - what's the difference?

SQLAlchemy is an object-relational mapper widely used in the Python world, making it easier (usually!) for developers to interface with their database of choice. I have always fudged my way around with the various database methods for syncing state between the in-memory object instances and the database, without fully understanding the differences. It's time to settle once and for all when to use session commit() vs flush() vs expire() vs refresh()!   SQLAlchemy是一个广泛用于Python世界的对象关系映射器，使开发人员更容易（通常！）与他们选择的数据库进行交互。 我总是勉强使用各种数据库方法在内存中对象实例和数据库之间同步状态，而没有完全理解差异。 是时候一劳永逸地解决使用session commit() vs flush() vs expire() vs refresh() 的问题！

Note: Altough my experience is with SQLAlchemy's Flask variant, most (all?) of these principles should apply to all flavours of SQLAlchemy.  注意：虽然我的经验是使用SQLAlchemy Flask变体，但这些原则中的大多数（全部？）应该适用于所有SQLAlchemy。

### Tell me about the Session

Key to the rest of this article is the concept of the Session in the SQLAlchemy world. Sessions are an in-memory "limbo" state for objects associated with database records.   本文其余部分的关键是SQLAlchemy世界中Session的概念。 对于与数据库记录关联的对象，会话是内存中的“不稳定”状态。

Let's break down what this means: 让我们分解这意味着什么：

1. As an ORM, SQLAlchemy enables you to manipulate database records as Python objects. For example, a row in your users table would be represented as a <User> object, which has attributes, methods, and so on.  作为ORM，SQLAlchemy使您可以将数据库记录作为Python对象进行操作。 例如，users表中的一行将表示为<User>对象，该对象具有属性，方法等。

2. These objects are held in memory and need to be synchronised with its representation in your database at some interval, otherwise the in-memory representation differs from your persistent database record.  这些对象保存在内存中，需要在某个时间间隔内与数据库中的表示同步，否则内存中的表示形式与持久性数据库记录不同。

3. Sessions are a scope or context within which you can change these objects. Note that this does not necessarily mean any changes you make to the objects are (yet) synchronised back to the database.  会话是一个范围或上下文，您可以在其中更改这些对象。 请注意，这并不一定意味着您对对象所做的任何更改（还）会同步回数据库。

4. Sessions have a natural lifecyle in which objects are first instantiated from the database record, changes are made to these objects, and then the changes are either persisted back to the database or discarded.   会话具有自然的生命周期，其中首先从数据库记录中实例化对象，对这些对象进行更改，然后将更改保留回数据库或丢弃。

The various methods mentioned in this article (commit / flush / expire / refresh / merge) are all slightly different ways to accomplish that last step in the lifecycle of persisting changes back to the database.  本文中提到的各种方法（commit / flush / expire / refresh / merge）都是稍微不同的方法，可以在将更改持久化回数据库的生命周期中完成最后一步。

You may be wondering at this stage what determines when the Session lifecycle begins and ends. SQLAlchemy has taken an opinionated stance where it is usually up to the developer to decide when this begins and ends, with the availability of methods such as **db.session.begin()** and **db.session.commit()** . However in most web applications, the established pattern is to begin and end the Session with each http request.  您可能在此阶段想知道什么决定会话生命周期何时开始和结束。 SQLAlchemy采取了一种自以为是的立场，通常由开发人员决定何时开始和结束，以及db.session.begin（）和db.session.commit（）等方法的可用性。 但是，在大多数Web应用程序中，已建立的模式是使用每个http请求开始和结束Session。

### Expiring objects  到期对象

Let's start with the most straightforward of the methods we are investigating.  让我们从我们正在研究的最直接的方法开始。

The methods for **db.session.expire(some_object)** and **db.session.expire_all()** expires one or all objects in the current Session respectively. This means that:

1. Expiring marks all attributes for that object as being stale or out of date.  Expiring将该对象的所有属性标记为陈旧或过时。
2. Subsequently, the next time that object is accessed, a new query will be issued to update the object with the current database record.  随后，下次访问该对象时，将发出一个新查询以使用当前数据库记录更新该对象。

A key behaviour of expiring is that **all un-flushed changes to the object is discarded** and not persisted to the database. For example:  到期的关键行为是，对象的所有未刷新更改都将被丢弃，并且不会持久保存到数据库中。 例如：

```
user.name = 'user2'
db.session.expire(user)

user.name  # ==> 'user1'
```

Note: Objects are automatically expired already whenever the Session ends. This means if there is a call to **db.session.commit()** or **db.session.rollback()** (automatically at the end of a HTTP request in the case of a web application), all objects are expired.  注意：只要会话结束，对象就会自动过期。 这意味着如果调用db.session.commit() 或db.session.rollback()（在Web应用程序的情况下，在HTTP请求结束时自动调用），则所有对象都将过期。

So when do you actually need to explicitly expire objects? You do so when you want to force an object to reload its data, because you know its current state is possibly stale. This is commonly when:  那么你何时需要明确地使对象过期？ 当您想强制对象重新加载其数据时，您会这样做，因为您知道它的当前状态可能是陈旧的。 这通常是在：

* Some SQL has been emitted outside the scope of the ORM, eg if you executed some raw SQL statements.  某些SQL已在ORM范围之外发出，例如，如果您执行了一些原始SQL语句。

* Changes are made outside the Session context, eg a concurrent Celery task has been executed  在Session上下文之外进行更改，例如，已执行并发Celery任务

### Refreshing objects  刷新对象

Now that we understand expiring objects, the methods for **db.session.refresh(some_object)** becomes much easier to understand.

Basically, refreshing means to expire and then immediately get the latest data for the object from the database. It involves an immediate database query, which you may consider unnecessarily expensive.  基本上，刷新意味着过期，然后立即从数据库中获取对象的最新数据。 它涉及即时数据库查询，您可能认为这是不必要的昂贵。

Here's how I decide when to use expire vs refresh?  这是我如何决定何时使用expire vs refresh？

* Expire - I persisted some changes for an object to the database. I don't need this updated object anymore in the current method, but I don't want any subsequent methods to accidentally use the wrong attributes.  过期 - 我坚持对数据库的对象进行一些更改。 我不再需要在当前方法中使用此更新对象，但我不希望任何后续方法意外使用错误的属性。

* Refresh - I persisted some changes for an object to the database. I need to use this updated object within the same method.  刷新 - 我坚持对数据库的对象进行一些更改。 我需要在同一个方法中使用这个更新的对象。

### Flushing objects

Remember earlier in this article we mentioned that expiring objects will discard all un-flushed changes? Flushing means to push all object changes to the database. Note that this does not necessarily mean that changes have been made to the database records - you must still call **db.session.commit()** to update the database or **db.session.rollback()** to discard your changes.  还记得在本文前面我们提到过期对象将丢弃所有未刷新的更改吗？ 刷新意味着将所有对象更改推送到数据库。 请注意，这并不一定意味着已对数据库记录进行了更改 - 您仍必须调用db.session.commit() 来更新数据库或db.session.rollback() 以放弃更改。

Pushing object changes to the database means your database now holds the changes in its transaction buffer. This means there are 2 common gotchas with using flush():  将对象更改推送到数据库意味着您的数据库现在保存其事务缓冲区中的更改。 这意味着使用flush() 有两个常见问题：

1. If you configured your Session with autocommit: True:

	* you are essentially requesting SQLAlchemy to call **db.session.commit()** whenever a transaction is not present  您实质上是在每当事务不存在时请求SQLAlchemy调用db.session.commit()

	* therefore, **db.session.flush()** will automatically call **db.session.commit()** unless you explicitly started a transaction with **db.session.begin()**.  因此，db.session.flush() 将自动调用db.session.commit() ，除非您使用db.session.begin() 显式启动了事务。

```
# With autocommit: False
user.name  # ==> 'user1'
user.name = 'user2'
db.session.flush()
user.name  # ==> 'user2', returns the in-memory representation. If you view your db with another application, it will still show 'user1'
db.session.rollback()
user.name # ==> 'user1'

# With autocommit: True
user.name  # ==> 'user1'
user.name = 'user2'
db.session.flush()  # ==> db.session.commit() is automatically called
user.name # ==> 'user2'. If you view your db with another application, it will already show 'user2'
db.session.rollback()  # ==> too late!
user.name # ==> 'user2'
```

2. Without calling db.session.commit(), the changes remain in the database transaction buffer and any calls to refresh will get the unchanged values. That is (assuming autocommit:False) :  如果不调用db.session.commit() ，则更改将保留在数据库事务缓冲区中，并且对refresh的任何调用都将获得未更改的值。 那是（假设autocommit：False）：

```
user.name  # ==> 'user1'
user.name = 'user2'
db.session.flush()
user.name  # ==> 'user2', returns the in-memory representation. If you view your db with another application, it will still show 'user1'
db.session.refresh(user)
user.name  # ==> 'user2'  # ==> SQLAlchemy assumes the database has been changed, even if it hasn't committed! If you view your db with another application it, it will still show 'user1'
db.session.rollback()
user.name  # ==> 'user1'  # ==> Rollback discards the database transaction buffer
```

### Committing

With this understanding of flush, it's now easier to understand committing. Conceptually db.session.commit() is basically 2 steps in one:  通过对flush的理解，现在更容易理解提交。 从概念上讲，db.session.commit() 基本上是两步之一：

1. Flushing - push changes from SQLAlchemy's in-memory representation to the database transaction buffer

2. Commit - persist changes from your database's transaction buffer into the database, ie inserting / updating / deleting.

Note if your Session is configured with autocommit: True, calling flush() will automatically call commit() if outside a transaction.

### Merging

Merging is a less common scenario, where you may have more than one in-memory representation what is essentially the same object. Being the "same object" is usually based on the database's primary key.   合并是一种不太常见的情况，您可能有多个内存中表示基本上是同一个对象。 作为“相同对象”通常基于数据库的主键。

Here's an example:

```
user1 = User.query.get(1)
user1.name  # ==> 'user1'

new_user = User(user_id=1)  # ==> a second in-memory object with the same key!
new_user.name = 'user2'
user1.name  # ==> 'user1'. Without merging, user1 doesn't know it is the same as new_user

db.session.merge(new_user)
user1.name  # ==> 'user2'. Now updated in memory. Note not yet updated in db, needs flush() and commit()
```

### Conclusion

Here's how I decide what to use:

1. Expire

  * I've made some changes to an object and don't need it immediately but don't want any subsequent methods to use stale values.

2. Refresh

  * I've made some changes to an object and need its updated values immediately.

  * Costs extra database call as it expires and reads from database immediately.

3. Flush

  * Push changes from memory to your database's transaction buffer. No database statements are issued yet.

  * If Session has autocommit: False, must still call commit() to persist the changes or rollback() to discard changes.

  * If Session has autocommit: True and you are not explicitly in a transaction, commit() will be automatically called.

4. Commit

  * Persist changes in your database's transaction buffer to the database. Database statements are issued.

  * Automatically expires objects.

5. Merge

  * Used when you may have more than 1 in-memory objects which map to the same database record with some key.
  * Merging causes the in-memory objects to be synchronised with each other, does not necessarily persist to the database.


[参考](https://www.michaelcho.me/article/sqlalchemy-commit-flush-expire-refresh-merge-whats-the-difference)

