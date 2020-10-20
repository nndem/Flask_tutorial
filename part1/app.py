from flask import Flask, render_template, url_for

app = Flask(__name__)

menu = ["Установка", "Приложение", "Обратная связь"]


@app.route('/')
def index():
    print(url_for('index'))
    return render_template('index.html', menu=menu)


@app.route('/about')
def about():
    print(url_for('about'))
    return render_template('about.html', title='О сайте', menu=menu)


@app.route("/profile/<username>")
def profile(username):
    return f"Пользователь: {username}"


# @app.route("/profile/<path:username>")
# def profile(username):
#     return f"Пользователь: {username}"


# @app.route("/profile/<int:username>/<path>")
# def profile(username, path):
#     return f"Пользователь: {username}, {path}"


if __name__ == '__main__':
    app.run()
