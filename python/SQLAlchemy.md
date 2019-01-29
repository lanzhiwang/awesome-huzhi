## SQLAlchemy

### SQLAlchemy 入门

* 定义表
* 定义数据库连接
* 定义 CURD 操作

### 主流数据库的连接方式

### 查询条件设置

### 关系操作

* 一对一的关系

一对一关系可以用一对多关系表示，但调用 db.relationship() 时要把 uselist 设为 False，把“多”变成“一”。 

* 一对多的关系
* 多对多的关系

```
# 父表
users = db.relationship('User', backref='role')

# 子表
role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
```

* 连接查询

### 级联

```
# 父表
users = db.relationship('User', backref='role', cascade='all')

# 子表
```

* cascade 取值范围
    * save-update
    * merge ??
    * expunge ??
    * delete
    * delete-orphan
    * refresh-expire ??
    * all（save-update、merge、refresh-expire、expunge、delete）

