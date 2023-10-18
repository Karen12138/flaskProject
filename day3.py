# 1、2023/10/15 今天要学习的是flask-SQLAlchemy连接数据库
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

HOSTNAME = "127.0.0.1",
PORT = 3306
USERNAME = "root",
PASSWORD = "lkl",
DATABASE = "flask_learn"

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:lkl@127.0.0.1:3306/flask_learn?charset=utf8"
db = SQLAlchemy(app)

# with app.app_context():
#     with db.engine.connect() as conn:
#         rs = conn.execute(text("select 1"))
#         print(rs.fetchone())

# 2、创建数据表
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

@app.route('/')
def hello_world():  # put application's code here
    return "Hello World!"

# # 3、增查改删的数据操作
# ## 3.1 创建数据
# @app.route('/user/add')
# def user_add():
#     ## 创建实例对象
#     user1 = User(username = "lkl2", password = 111111)
#     user2 = User(username="gqx", password=222222)
#     ## 添加到会话db.session中
#     db.session.add(user1)
#     db.session.add(user2)
#     ## 同步到数据库中
#     db.session.commit()
#     return "用户添加成功"

## 3.2 查询数据
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

## 3.3 更新数据
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

## 3.4 删除数据
@app.route("/user/delete")
def user_delete():
    user = User.query.filter_by(username="lkl2").first()
    db.session.delete(user)
    ## 推送到数据库同步
    db.session.commit()
    return "数据删除成功"


if __name__ == '__main__':
    app.run(debug=True)
