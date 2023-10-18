##  2023/10/17
## 今天学的是外键与表关系
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

# HOSTNAME = "127.0.0.1",
# PORT = 3306
# USERNAME = "root",
# PASSWORD = "lkl",
# DATABASE = "flask_learn"

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:lkl@127.0.0.1:3306/flask_learn?charset=utf8"
db = SQLAlchemy(app)

# 一对多关系（外键在谁那，谁就属于“多”的那一端 ）
## User表
class User(db.Model):
    ## 数据库的表名
    __tablename__ = "user"
    ## 创建数据表的字段,注意字段类型首字母大写，如String
    ### 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(100), nullable = False)

## Article表
class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    content = db.Column(db.Text,nullable = False)

## 在Article模型下添加外键，author_id是外键，db.Foreignkey引用之前创建的user表里id字段。这个外键的是一种一对多的关系，比如外键中提到的一个author，在article表中有多处。
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
## db.relationship来引用外键指向另一个要关联的ORM模型，所以添加author属性建立联系
    author = db.relationship("User")
    ## 实现的功能相当于article.author = User.query.get(article.author_id )

# 双向关系
## 法一：back_populates(建议使用)
## User表
class User(db.Model):
    ## 数据库的表名
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(100), nullable = False)

    ## 要想实现双向关系就，就需要在指向的另一个表也添加db.relationship的属性，并且双方的db.relationship中都要加上back_populates参数
    articles = db.relationship("Article", back_populates = "author")

## Article表
class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    content = db.Column(db.Text,nullable = False)

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    ## 在db.relationship里面添加联系User表中articles属性的参数。
    # 规则就是我在这个文章表内要查到作者，那我就要在这个表里添加作者属性author，反之，我要在作者表里查到文章信息，那我就添加文章属性articles。
    author = db.relationship("User", back_populates = "articles")

## 使用方法
@app.route("/article/add")
def article_add():
    article1 = Article(title = "FLASK", content = "Flask基础版")
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
    user= User.query.first()
    for article in user.articles:
        print(article.title)
    return "文章查询成功"

## 法二：backref
## User表
class User(db.Model):
    ## 数据库的表名
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(100), nullable = False)

    ## 不添加acticles属性

## Article表
class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    content = db.Column(db.Text,nullable = False)

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    ## 在db.relationship里面添加backref，backref能自动给对方添加articles属性
    author = db.relationship("User", backref = "articles")

# 一对一关系
