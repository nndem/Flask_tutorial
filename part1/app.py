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


# создание тестового контекста запросов
# для проверки работы url_for, не поднимая сервер
with app.test_request_context():
    print(url_for('index'))


# if __name__ == '__main__':
#     app.run()
