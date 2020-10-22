from flask import Flask, render_template, make_response

app = Flask(__name__)

menu = [{"title": "Главная", "url": "/"},
        {"title": "Добавить статью", "url": "/add_post"}]


@app.route('/')
def index():
    #  формирование кастомного ответа сервера с использованием make_response() и кода ответа
    res = make_response("<h1>Ошибка сервера</h1>", 500)
    return res


if __name__ == '__main__':
    app.run()
