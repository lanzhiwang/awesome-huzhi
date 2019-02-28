### compiled SQL query from a SQLAlchemy expression

```
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects import mysql
from sqlalchemy import inspect

if __name__ == '__main__':
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)

    session = Session(engine)

    # create catalog
    tshirt, mug, hat, crowbar = (
        Item('SA T-Shirt', 10.99),
        Item('SA Mug', 6.50),
        Item('SA Hat', 8.99),
        Item('MySQL Crowbar', 16.99)
    )
    session.add_all([tshirt, mug, hat, crowbar])
    session.commit()

    # create an order
    order = Order('john smith')

    # add three OrderItem associations to the Order and save
    order.order_items.append(OrderItem(mug))
    order.order_items.append(OrderItem(crowbar, 10.99))
    order.order_items.append(OrderItem(hat))
    session.add(order)
    session.commit()

    inspector = inspect(engine)
    print(dir(inspector))
    '''
    [
    'bind', 
    'default_schema_name', 
    'dialect', 
    'engine', 
    'from_engine', 
    'get_check_constraints', 
    'get_columns', 
    'get_foreign_keys', 
    'get_indexes', 
    'get_pk_constraint', 
    'get_primary_keys', 
    'get_schema_names', 
    'get_sorted_table_and_fkc_names', 
    'get_table_comment', 
    'get_table_names', 
    'get_table_options', 
    'get_temp_table_names', 
    'get_temp_view_names', 
    'get_unique_constraints', 
    'get_view_definition', 
    'get_view_names', 
    'info_cache', 
    'reflecttable'
    ]
    '''
    
    print(inspector.get_columns('order'))
    '''
    [
    {'name': 'order_id', 'primary_key': 1, 'nullable': False, 'type': INTEGER(), 'default': None, 'autoincrement': 'auto'},
    {'name': 'customer_name', 'primary_key': 0, 'nullable': False, 'type': VARCHAR(length=30), 'default': None, 'autoincrement': 'auto'},
    {'name': 'order_date', 'primary_key': 0, 'nullable': False, 'type': DATETIME(), 'default': None, 'autoincrement': 'auto'}
    ]
    '''


    # query the order, print items
    q = session.query(Order).filter_by(customer_name='john smith')
    print(str(q))
    print(str(q.statement.compile(dialect=postgresql.dialect())))
    
    raw_sql = str(q.statement.compile(dialect=mysql.dialect()))
    print(raw_sql)
    print(type(raw_sql))
    print(raw_sql % ("'john smith'"))
    
    order = session.query(Order).filter_by(customer_name='john smith').one()

    print([(order_item.item.description, order_item.price)
           for order_item in order.order_items])

    session.close()

```

### Executing SQL Statements

```
from sqlalchemy.sql import text
with engine.connect() as con:

    data = ( { "id": 1, "title": "The Hobbit", "primary_author": "Tolkien" },
             { "id": 2, "title": "The Silmarillion", "primary_author": "Tolkien" },
    )

    statement = text("""INSERT INTO book(id, title, primary_author) VALUES(:id, :title, :primary_author)""")

    for line in data:
        con.execute(statement, **line)
```

* [参考1](https://chartio.com/resources/tutorials/how-to-execute-raw-sql-in-sqlalchemy/)
* [参考2](https://stackoverflow.com/questions/4617291/how-do-i-get-a-raw-compiled-sql-query-from-a-sqlalchemy-expression)


