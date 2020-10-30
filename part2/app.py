from flask import Flask, render_template, request, g, flash, abort, redirect, url_for, make_response
import sqlite3
import os
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from user import User
from forms import LoginForm
from forms import RegisterForm
from admin.admin import admin

# конфигурация
DATABASE = "/tmp/site.db"
DEBUG = True
SECRET_KEY = "33306205a5c1a08539dcd75680aacd718f0c6ebd"
MAX_CONTENT_LENGTH = 1024 * 1024

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, "site.db")))

app.register_blueprint(admin, url_prefix="/admin")

login_manager = LoginManager(app)
login_manager.login_view = "login" # redirect for unauthorized users by default
login_manager.login_message = "Авторизуйтесь для доступа к закрытым ресурсам"
login_manager.login_message_category = "success"

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row  # записи в БД будут иметь вид не кортежа, а в виде словаря
    return conn


def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource('sql_code.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    """Соединение с БД, если оно еще не установлено"""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None
@app.before_request
def before_request():
    """Установление соединения с БД перед выполненим запроса"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/")
def index():
    return render_template("index.html", menu=dbase.getMenu(), posts=dbase.getPostsAnonce())


@app.route("/add_post", methods=["POST", "GET"])
def addPost():
    if request.method == "POST":
        if len(request.form["name"]) > 4 and \
               len(request.form["post"]) > 10:
            res = dbase.addPost(request.form["name"], request.form["post"], request.form["url"])
            if not res:
                flash("Ошибка добавления статьи", category="error")
            else:
                flash("Статья успешно добавлена", category="success")
        else:
            flash("Ошибка добавления статьи", category="error")

    return render_template("add_post.html", menu=dbase.getMenu(), title="Добавление статьи")


@app.route("/post/<alias>")
@login_required
def showPost(alias):
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)

    return render_template("post.html", menu=dbase.getMenu(), post=post)


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hash = generate_password_hash(form.psw.data)
        res = dbase.addUser(form.name.data, form.email.data, hash)
        if res:
            flash("Вы успешно зарегистрированы", category="success")
            return redirect(url_for("login"))
        else:
            flash("Ошибка при добвалении в БД", category="error")

    return render_template("register.html", menu=dbase.getMenu(), title="Регистрация", form=form)


"""
Функция login_user помещает id пользователя в сессию
"""
@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()
    if form.validate_on_submit():
        user_from_DB = dbase.getUserByEmail(form.email.data)
        if user_from_DB and check_password_hash(user_from_DB['psw'], form.psw.data):
            user_for_session = User().create(user_from_DB)
            remember_me = form.remember.data
            login_user(user_for_session, remember=remember_me)
            return redirect(request.args.get("next") or url_for("profile"))

        flash("Неверная пара логин/пароль", category="error")

    return render_template("login.html", menu=dbase.getMenu(),
                           title="Авторизация", form=form)


"""
Извлекает из сессии id пользователя
Эта функция сработает если в сессии действительно есть объект user_for_session
для которого реализован метод get_id
"""


@login_manager.user_loader
def load_user(user_id):
    return User().fromDB(user_id, dbase)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", category="success")
    return redirect(url_for("login"))


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", menu=dbase.getMenu(), title="Профиль")


@app.route("/userava")
@login_required
def userava():
    img = current_user.getAvatar(app)
    if not img:
        return ""

    h = make_response(img)
    h.headers["Content-Type"] = "image/png"
    return h


@app.route("/upload", methods=["POST", "GET"])
@login_required
def upload():
    if request.method == "POST":
        file = request.files["file"]
        if file and current_user.verifyExt(file.filename):
            try:
                img = file.read()
                res = dbase.updateUserAvatar(img, current_user.get_id())
                if not res:
                    flash("Ошибка обновления аватара", "error")
                flash("Аватар обновлен", category="success")
            except FileNotFoundError as e:
                flash("Ошибка чтения файла", "error")
        else:
            flash("Ошибка обновления аватара", "error")

    return redirect(url_for("profile"))


if __name__ == "__main__":
    app.run()
