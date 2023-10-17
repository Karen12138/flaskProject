# Day2
## Jinja2模板
1. <font size = 3>渲染模板  
```render_template()```
2. 模板传参    
```{{  }}```
3. 过滤器(对变量进行函数操作)   
```{{name|length}}、app.templates.filter("过滤器名")```
4. 控制语句   
```{% %} 结束语句：{% endif %}、{% endfor %}```
5. 模板继承 
>* 父模板  
   > ```{% block head %} {% endblock%}```  
>* 子模版   
   > ```{% extends "base.html" %} 、{% block head %} ... {% endblock%}```
6. 加载静态文件   
```static```
</font>

# [Day3 ](https://www.bilibili.com/video/BV17r4y1y7jJ?p=14&vd_source=33207922e975d5ad1770261da92cead1)
## 3.1Flask-SQLAlchemy 连接数据库
* <font size =3 >连接数据库
```python
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

HOSTNAME = "127.0.0.1",
PORT = 3306
USERNAME = "root",
PASSWORD = "lkl",
DATABASE = "flask_learn"

### 设置本机数据库信息
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:lkl@127.0.0.1:3306/flask_learn?charset=utf8"
db = SQLAlchemy(app)

with app.app_context():
    with db.engine.connect() as conn:
        rs = conn.execute(text("select 1"))
        print(rs.fetchone())
```
 </font>

## 3.2 ORM模型
* <font size = 3>一个ORM模型对应一个数据表
* ORM模型的属性对应表内的每个字段
```python
class User(db.Model):
    ## 数据库的表名
    __tablename__ = "user"
    ## 创建数据表的字段,注意字段类型首字母大写，如String
    ### 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(100), nullable = False)

with app.app_context():
    db.create_all()
```
 </font>

## 3.3 使用ORM模型增查改删  

* <font size = 3>创建数据
```python
@app.route('/user/add')
def user_add():
    ## 创建实例对象
    user1 = User(username = "lkl2", password = 111111)
    user2 = User(username="gqx", password=222222)
    ## 添加到会话db.session中
    db.session.add(user1)
    db.session.add(user2)
    ## 同步到数据库中
    db.session.commit()
    return "用户添加成功"
```
 
* 查询数据
```python
@app.route('/user/query')
def user_query():
    ### 提取方法：获取主键查询（主键是能确定一条记录的唯一标识）
    # user = User.query.get(5)
    ### 过滤方法：filter_by，返回类型是Query对象
    users = User.query.filter_by().all()
    ### user类型是类数组Query
    for user in users:
        print( f"{user.username}:{user.password}")
    return "用户查询成功"
```

* 更新数据
```python
@app.route('/user/update')
def user_update():
    ### first()获取到的是当前username下的整个数据
    user = User.query.filter_by(username = "lkl2").first()
    user.password = 777
    ## 推送到数据库同步
    db.session.commit()
    user = User.query.get(3)
    print((user.password))
    return "数据更新成功"
```

* 删除数据
 ```python
 @app.route("/user/delete")
def user_delete():
    user = User.query.filter_by(username="lkl2").first()
    db.session.delete(user)
    ## 推送到数据库同步
    db.session.commit()
    return "数据删除成功"
 ```
 </font>

## 3.4 表关系
+ <font size=5>主键与外键</font>  

<font size=4>主键：</font>___表中经常有一个列或多列的组合，其值能唯一地标识表中的每一行。___
这样的一列或多列称为表的主键，通过它可强制表的实体完整性。
当创建或更改表时可通过定义 PRIMARY KEY 约束来创建主键。
一个表只能有一个 PRIMARY KEY 约束，而且 PRIMARY KEY 约束中的列不能接受空值。
由于 PRIMARY KEY 约束确保唯一数据，所以经常用来定义标识列。
> <font size=3>作用:</font>
>
> 1. 保证实体的完整性;  
> 2. 加快数据库的操作速度;  
> 3. 在表中添加新记录时，DBMS会自动检查新记录的主键值，不允许该值与其他记录的主键值重复。  
> 4. DBMS自动按主键值的顺序显示表中的记录。如果没有定义主键，则按输入记录的顺序显示表中的记录。   

<font size=4>外键：</font>___如果公共关键字在一个关系中是主关键字，那么这个公共关键字被称为另一个关系的外键。___
由此可见，外键表示了两个关系之间的相关联系。以另一个关系的外键作主关键字的表被称为主表，
具有此外键的表被称为主表的从表。外键又称作外关键字。   
举例：  
![Student表](https://img-blog.csdnimg.cn/20200320200706506.png)   
![Class表](https://img-blog.csdnimg.cn/20200320200754466.png)

