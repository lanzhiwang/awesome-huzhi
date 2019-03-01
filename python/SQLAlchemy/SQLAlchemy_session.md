## SQLAlchemy commit(), flush(), expire(), refresh(), merge() - what's the difference?

https://www.michaelcho.me/article/sqlalchemy-commit-flush-expire-refresh-merge-whats-the-difference

Session.add()
session.add_all()
session.commit()


q = session.query(Order)

session.close()

Session.delete()



Session.merge()



Session.expire()


Session.expunge()

Session.closed()