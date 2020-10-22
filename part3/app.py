from flask import Flask, render_template, make_response

app = Flask(__name__)

menu = [{"title": "Главная", "url": "/"},
        {"title": "Добавить статью", "url": "/add_post"}]


@app.route('/')
def index():
    # Формирование кастомного ответа при помощи кортежа
    return "<h1>Main Page</h1>", 200, {"Content-Type": "text/plain"}


@app.errorhandler(404)
def pageNot(error):
    return ("Страница не найдена", 404)


if __name__ == '__main__':
    app.run()
