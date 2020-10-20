from flask import Flask, render_template, url_for, request, flash

app = Flask(__name__)
# для активации session необходимо:
app.config['SECRET_KEY'] = 'abracadabra'
# session используется для хранение flash, которые
# могут быть извлечены get_flashed_messages()

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


@app.route('/contact', methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        print(request.form['username'])

        if len(request.form['username']) > 2:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')

    return render_template('contact.html', title='Обратная связь', menu=menu), 404

# обработчик ошибок
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title="Страница не найдена", menu=menu)


if __name__ == '__main__':
    app.run()
