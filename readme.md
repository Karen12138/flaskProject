# Day2
## Jinja2模板
1. <font size = 3>渲染模板 
> render_template()
2. 模板传参 
> {{  }}
3. 过滤器(对变量进行函数操作) 
> {{name|length}}、app.templates.filter("过滤器名")
4. 控制语句
>{% %} 结束语句：{% endif %}、{% endfor %}
5. 模板继承 
* 父模板{% block head %} {% endblock%}  
* 子模版{% extends "base.html" %} 、{% block head %} ... {% endblock%}
6. 加载静态文件 
> static
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