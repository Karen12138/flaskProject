# 问答平台项目搭建
from flask import Flask
import config
from exts import db
from models import UserModel
from blueprints.q_a import bp as qa_bp
from blueprints.user import bp as user_bp
from flask_migrate import Migrate

app = Flask(__name__)
## 1. 绑定配置文件
app.config.from_object(config)

## 2. 先创建db，到后面再绑定到app
db.init_app(app)

## 初始化Flask-Migrate，将程序和数据库关联在一起，便于实时更新数据表
migrate = Migrate(app, db)

## 3. 将蓝图引用到app里面
app.register_blueprint(qa_bp)
app.register_blueprint(user_bp)

## 视图函数全部放到蓝图里面


if __name__ == '__main__':
    app.run(debug=True)