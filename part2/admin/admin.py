import sqlite3
from flask import Blueprint, request, redirect, url_for, flash, render_template, session, g

admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")


def login_admin():
    session["admin_logged"] = 1


def isLogged():
    return True if session.get("admin_logged") else False


def logout_admin():
    session.pop("admin_logged", None)


menu = [{"url": ".index",  "title": "Панель"},
        {"url": ".listusers", "title": "Список пользователей"},
        {"url": ".listpubs",  "title": "Список статей"},
        {"url": ".logout", "title": "Выйти"}]

db = None
@admin.before_request
def before_request():
    global db
    db = g.get("link_db")


@admin.teardown_request
def teardown_request(request):
    global db
    db = None
    return request


@admin.route("/")
def index():
    if not isLogged():
        return redirect(url_for(".login"))

    return render_template("admin/index.html", menu=menu, title="Админ-панель")


@admin.route("/login", methods=["POST", "GET"])
def login():
    if isLogged():
        return redirect(url_for(".index"))

    if request.method == "POST":
        if request.form["user"] == "admin" and request.form["psw"] == "1234":
            login_admin()
            return redirect(url_for(".index"))  # "admin.index"
        else:
            flash("Неверная пара логин/пароль", category="error")

    return render_template("admin/login.html", title="Админ-панель")


@admin.route("/logout", methods=["POST", "GET"])
def logout():
    if not isLogged():
        return redirect(url_for(".login"))

    logout_admin()

    return redirect(url_for(".login"))


@admin.route("/listpubs")
def listpubs():
    if not isLogged():
        return redirect(url_for(".login"))

    list = []
    if db:
        try:
            cur = db.cursor()
            sql = f"SELECT title, text, url FROM posts"
            cur.execute(sql)
            list = cur.fetchall()
        except sqlite3.Error as e:
            print("Ошибка получения статец из БД " + str(e))

    return render_template("admin/listpubs.html", title="Список статей", menu=menu, list=list)


@admin.route("/listusers")
def listusers():
    if not isLogged():
        return redirect(url_for(".login"))

    list=[]
    if db:
        try:
            cur = db.cursor()
            sql = f"SELECT name, email FROM users ORDER BY time DESC"
            cur.execute(sql)
            list = cur.fetchall()
        except sqlite3.Error as e:
            print("Ошибка получения статей из БД " + str(e))

    return render_template("admin/listusers.html", title="Список пользователей", menu=menu, list=list)