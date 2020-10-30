from flask import Blueprint, request, redirect, url_for, flash, render_template, session

admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")


def login_admin():
    session["admin_logged"] = 1


def isLogged():
    return True if session.get("admin_logged") else False


def logout_admin():
    session.pop("admin_logged", None)


menu = [{"url": "",  "title": "Панель"},
        {"url": "logout", "title": "Выйти"}]


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