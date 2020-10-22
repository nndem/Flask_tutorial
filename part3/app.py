from flask import Flask, render_template, make_response, redirect, url_for

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


@app.route("/transfer")
# перенаправляем URL на главную страницу с кодом 301 (навсегда)
def transfer():
    return redirect(url_for("index"), 301)


if __name__ == '__main__':
    app.run()
