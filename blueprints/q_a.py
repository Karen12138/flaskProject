from flask import Blueprint

## 该路径下是首页就不加前缀路径了
bp = Blueprint("qa", __name__, url_prefix="/")

@bp.route("/")
def insex():
    pass