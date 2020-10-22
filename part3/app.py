from flask import Flask, render_template, make_response

app = Flask(__name__)

menu = [{"title": "Главная", "url": "/"},
        {"title": "Добавить статью", "url": "/add_post"}]


@app.route('/')
def index():
    #  формирование кастомного ответа сервера с использованием make_response
    content = render_template("index.html", menu=menu, posts=[])
    res = make_response(content)
    res.headers["Content-Type"] = "text/plain"
    res.headers["Server"] = "FlaskServer"
    return res


if __name__ == '__main__':
    app.run()
