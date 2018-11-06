## SQLAlchemy



### `一对多`的关系

![](./images/mysql/oneandmore.png)



```python
import os
from flask import Flask ... 
...
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# 将 SQLALCHEMY_COMMIT_ON_TEARDOWN 设为 True 时，每次请求结束后都会自动提交数据库中的变动
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


'''
db.Column 参数列表：
primary_key 如果设为 True，这列就是表的主键
unique 如果设为 True，这列不允许出现重复的值
index 如果设为 True，为这列创建索引，提升查询效率
nullable 如果设为 True，这列允许使用空值；如果设为 False，这列不允许使用空值
default 为这列定义默认值
'''
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    
    '''添加到 Role 模型中的 users 属性代表这个关系的面向对象视角。
    对于一个 Role 类的实例，其 users 属性将返回与角色相关联的用户组成的列表。
    db.relationship() 的第一个参数表明这个关系的另一端是哪个模型。如果模型类尚未定义，可使用字符串形式指定。
    db.relationship() 中的 backref 参数向 User 模型中添加一个 role 属性，从而定义反向关系。这一属性可替代 role_id 访问 Role 模型，此时获取的是模型对象，而不是外键的值。

    db.relationship 参数列表：
    backref 在关系的另一个模型中添加反向引用
    primaryjoin 明确指定两个模型之间使用的联结条件。只在模棱两可的关系中需要指定。大多数情况下， db.relationship() 都能自行找到关系中的外键，但有时却无法决定把哪一列作为外键。 例如，如果 User 模型中有两个或以上的列定义为 Role 模型的外键，SQLAlchemy 就不知道该使用哪列。 如果无法决定外键，你就要为 db.relationship() 提供额外参数，从而确定所用外键
    lazy 指定如何加载相关记录。可选值有 select（首次访问时按需加载）、 immediate（源对象加载后就加载）、 joined（加载记录，但使用联结）、 subquery（立即加载，但使用子查询），noload（永不加载）和 dynamic（不加载记录，但提供加载记录的查询）
    uselist 如果设为 Fales，不使用列表，而使用标量值
    order_by 指定关系中记录的排序方式
    secondary 指定多对多关系中关系表的名字
    secondaryjoin SQLAlchemy 无法自行决定时，指定多对多关系中的二级联结条件
    '''
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    '''添加到 User 模型中的 role_id 列被定义为外键， 就是这个外键建立起了关系。
    传给 db.ForeignKey() 的参数 'roles.id' 表明，这列的值是 roles 表中行的 id 值。
    '''
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

```



### `一对一`的关系

一对一关系可以用一对多关系表示，但调用 db.relationship() 时要把 uselist 设为 False，把“多”变成“一”。 

### `多对一`的关系

多对一关系也可使用一对多表示， 对调两个表即可，或者把外键和 db.relationship() 都放在“多”这一侧。 

### `多对多`的关系

多对多的关系需要用到第三张表， 这个表称为关系表。通过关系表转为一对多的关系。