from flask import Flask, render_template

app = Flask(__name__)

## 视图函数
@app.route('/')
def hello_world():  # put application's code here
    return render_template("child.html")


if __name__ == '__main__':
    app.run(debug=False)
