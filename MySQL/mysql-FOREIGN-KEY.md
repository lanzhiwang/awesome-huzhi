# MySQL 外键约束

```
[CONSTRAINT [symbol]] FOREIGN KEY
    [index_name] (col_name, ...)
    REFERENCES tbl_name (col_name,...)
    [ON DELETE reference_option]
    [ON UPDATE reference_option]

reference_option:
    RESTRICT | CASCADE | SET NULL | NO ACTION | SET DEFAULT

##################################################################

CREATE TABLE parent (
    id INT NOT NULL,
    PRIMARY KEY (id)
) ENGINE=INNODB;

CREATE TABLE child (
    id INT,
    parent_id INT,
    INDEX par_ind (parent_id),
    FOREIGN KEY (parent_id)
        REFERENCES parent(id)
        ON DELETE CASCADE
) ENGINE=INNODB;

##################################################################

CREATE TABLE product (
    category INT NOT NULL, id INT NOT NULL,
    price DECIMAL,
    PRIMARY KEY(category, id)
)   ENGINE=INNODB;

CREATE TABLE customer (
    id INT NOT NULL,
    PRIMARY KEY (id)
)   ENGINE=INNODB;

CREATE TABLE product_order (
    no INT NOT NULL AUTO_INCREMENT,
    product_category INT NOT NULL,
    product_id INT NOT NULL,
    customer_id INT NOT NULL,

    PRIMARY KEY(no),
    INDEX (product_category, product_id),
    INDEX (customer_id),

    FOREIGN KEY (product_category, product_id)
      REFERENCES product(category, id)
      ON UPDATE CASCADE ON DELETE RESTRICT,

    FOREIGN KEY (customer_id)
      REFERENCES customer(id)
)   ENGINE=INNODB;

```


##### Referential Actions

When an [`UPDATE`](https://dev.mysql.com/doc/refman/5.6/en/update.html) or [`DELETE`](https://dev.mysql.com/doc/refman/5.6/en/delete.html) operation affects a key value in the parent table that has matching rows in the child table, the result depends on the *referential action* specified by `ON UPDATE` and `ON DELETE` subclauses of the `FOREIGN KEY` clause. Referential actions include:  当 UPDATE 或 DELETE 操作影响子表中具有匹配行的父表中的键值时，结果取决于FOREIGN KEY子句的ON UPDATE和ON DELETE子句指定的引用操作。 参照动作包括：

- `CASCADE`: Delete or update the row from the parent table and automatically delete or update the matching rows in the child table. Both `ON DELETE CASCADE` and `ON UPDATE CASCADE` are supported. Between two tables, do not define several `ON UPDATE CASCADE` clauses that act on the same column in the parent table or in the child table.  从父表中删除或更新该行，并自动删除或更新子表中的匹配行。 同时支持ON DELETE CASCADE和ON UPDATE CASCADE。 在两个表之间，不要定义几个作用于父表或子表中同一列的ON UPDATE CASCADE子句。

  Note：Cascaded foreign key actions do not activate triggers.

- `SET NULL`: Delete or update the row from the parent table and set the foreign key column or columns in the child table to `NULL`. Both `ON DELETE SET NULL` and `ON UPDATE SET NULL` clauses are supported.  从父表中删除或更新该行，并将子表中的一个或多个外键列设置为NULL。 ON DELETE SET NULL和ON UPDATE SET NULL子句均受支持。

  If you specify a `SET NULL` action, *make sure that you have not declared the columns in the child table as `NOT NULL`*.

- `RESTRICT`: Rejects the delete or update operation for the parent table. Specifying `RESTRICT` (or `NO ACTION`) is the same as omitting the `ON DELETE` or `ON UPDATE` clause.  拒绝父表的删除或更新操作。 指定RESTRICT（或NO ACTION）与省略ON DELETE或ON UPDATE子句相同。

- `NO ACTION`: A keyword from standard SQL. In MySQL, equivalent to `RESTRICT`. The MySQL Server rejects the delete or update operation for the parent table if there is a related foreign key value in the referenced table. Some database systems have deferred checks, and `NO ACTION` is a deferred check. In MySQL, foreign key constraints are checked immediately, so `NO ACTION` is the same as `RESTRICT`.  标准SQL中的关键字。 在MySQL中，等同于RESTRICT。 如果引用表中有相关的外键值，则MySQL服务器会拒绝父表的删除或更新操作。 某些数据库系统具有延迟检查，而“ NO ACTION”是延迟检查。 在MySQL中，立即检查外键约束，因此NO ACTION与RESTRICT相同。

- `SET DEFAULT`: This action is recognized by the MySQL parser, but both [`InnoDB`](https://dev.mysql.com/doc/refman/5.6/en/innodb-storage-engine.html) and [`NDB`](https://dev.mysql.com/doc/refman/5.6/en/mysql-cluster.html) reject table definitions containing `ON DELETE SET DEFAULT` or `ON UPDATE SET DEFAULT` clauses.  MySQL解析器可以识别此操作，但是InnoDB和NDB都拒绝包含ON DELETE SET DEFAULT或ON UPDATE SET DEFAULT子句的表定义。

[参考](https://dev.mysql.com/doc/refman/5.6/en/create-table-foreign-keys.html)
