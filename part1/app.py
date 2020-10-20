from flask import Flask, render_template, url_for

app = Flask(__name__)

menu = [{"name": "Установка", "url": "install-flask"},
        {"name": "Приложение", "url": "first-app"},
        {"name": "Обратная связь", "url": "contact"}]


@app.route('/')
def index():
    print(url_for('index'))
    return render_template('index.html', menu=menu)


@app.route('/about')
def about():
    print(url_for('about'))
    return render_template('about.html', title='О сайте', menu=menu)


if __name__ == '__main__':
    app.run()
