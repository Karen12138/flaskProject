from flask import Blueprint

# 蓝图blueprint
## url_prefix指定该文件下的视图函数的前缀地址
bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route("/login")
def user_login():
    pass