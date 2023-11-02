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
+ <font size=4>一对多关系</font> <font size = 3>
```python
# 一对多关系（外键在谁那，谁就属于“多”的那一端 ）
## User表
class User(db.Model):
    ## 数据库的表名
    __tablename__ = "user"
    ## 创建数据表的字段,注意字段类型首字母大写，如String
    ### 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)


## Article表
class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    ## 在Article模型下添加外键，author_id是外键，db.Foreignkey引用之前创建的user表里id字段。这个外键的是一种一对多的关系，比如外键中提到的一个author，在article表中有多处。
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    ## db.relationship来引用外键指向另一个要关联的ORM模型，所以添加author属性建立联系
    author = db.relationship("User")
    ## 实现的功能相当于article.author = User.query.get(article.author_id )
```
 </font>  

+ <font size=4>双向关系</font><font size = 3>
```python
# 双向关系
## 法一：back_populates(建议使用)
## User表
class User(db.Model):
    ## 数据库的表名
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    ## 要想实现双向关系就，就需要在指向的另一个表也添加db.relationship的属性，并且双方的db.relationship中都要加上back_populates参数
    articles = db.relationship("Article", back_populates="author")


## Article表
class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    ## 在db.relationship里面添加联系User表中articles属性的参数。
    # 规则就是我在这个文章表内要查到作者，那我就要在这个表里添加作者属性author，反之，我要在作者表里查到文章信息，那我就添加文章属性articles。
    author = db.relationship("User", back_populates="articles")
```
```python
## 法二：backref
## User表
class User(db.Model):
    ## 数据库的表名
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    ## 不添加acticles属性


## Article表
class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    ## 在db.relationship里面添加backref，backref能自动给对方添加articles属性
    author = db.relationship("User", backref="articles")
```
```python
## 使用方法
@app.route("/article/add")
def article_add():
    article1 = Article(title="FLASK", content="Flask基础版")
    article1.author = User.query.get(2)

    article2 = Article(title="Python", content="python基础版")
    article2.author = User.query.get(2)

    ## 存储到session中
    db.session.add_all([article1, article2])
    ## 同步到数据库
    db.session.commit()
    return "文章添加成功"


@app.route("/article/query")
def article_query():
    user = User.query.first()
    for article in user.articles:
        print(article.title)
    return "文章查询成功"
```
 </font>  

+ <font size=4>一对一关系</font><font size = 3>
```python
# 一对一关系
## User表
class User(db.Model):
    ## 数据库的表名
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    ## db.relationship中传递uselist=False可以将多变成一，即表内不能出有现一对多的关系
    extension = db.relationship("UserExtension", back_populates="user", uselist=False)

class UserExtension(db.Model):
    id = db.Column(db.Integer, primary_key = True, autpincrement = True)
    school = db.Column(db.String(100), nullable=False)

    ## 数据库的一对一同步，在外键上设置unique = True
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique = True)
    ## 在db.relationship里面添加联系User表中articles属性的参数。
    user = db.relationship("User", back_populates="extension")
```
 </font>  

# Day4 ORM模型迁移

## 准备：创建迁移对象<font size = 3>
```python
## 1. 创建迁移对象
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:lkl@127.0.0.1:3306/flask_learn?charset=utf8"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
```
 </font>

## ORM模型映射到表的三步
### 模型映射三步曲 <font size = 3>   
2.1 初始化迁移环境，这步只需要执行一次即可    
```flask db init```  
2.2 识别ORM模型的变化，生成迁移脚本   
```flask db migrate -m "备注信息" (多人开发建议加上)```  
2.3 执行迁移脚本,同步到数据库   
```flask db upgrade```
</font>

# Day5 Flask实战
## 1. 结构搭建
### 创建文件与蓝图文件夹
+ <font size = 3>app.py : 主文件
+ config.py ： 配置信息如：数据库配置信息、token、cookie等
+ exts.py ： 扩展插件，如：SQLAlchemy数据库
+ models.py : 创建的ORM模型都存放在该文件下
```python 
# app.py里引用顺序 
from flask import Flask, render_template
import config # 引用配置文件
from exts import db # 引用拓展文件
# 引用蓝图文件(注意变量名不能重复)
from blueprints.q_a import bp as qa_bp
from blueprints.user import bp as user_bp 
```

```python
app = Flask(__name__)
## 1. 绑定配置文件
app.config.from_object(config)

## 2. 先创建db，到后面再绑定到app
db.init_app(app)

## 3. 将蓝图引用到app里面
app.register_blueprint(qa_bp)
app.register_blueprint(user_bp)
```
 </font>

### 创建蓝图文件夹<font size = 3>
+ 创建blueprints的python文件夹  
> + 该文件夹下__ini__.py 自动生成  
> + q_a.py 存放有关问答相关的视图函数
> + user.py 存放用户界面的视图函数
</font>
### 各类文件的引用规则如下图
### ![初始化](D:\PyCharm 2021.3.3\project_backup\day5.png)
