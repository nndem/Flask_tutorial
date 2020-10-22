from flask import Flask, render_template

app = Flask(__name__)

menu = [{"title": "Главная", "url": "/"},
        {"title": "Добавить статью", "url": "/add_post"}]


@app.route('/')
def index():
    #  формирование ответа сервера по умолчанию
    return render_template("index.html", menu=menu, posts=[])


if __name__ == '__main__':
    app.run()
