from flask import Flask, render_template, request, g
import sqlite3
import os

# конфигурация
from FDataBase import FDataBase

DATABASE = "/tmp/site.db"
DEBUG = True
SECRET_KEY = "secret_key"

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, "site.db")))


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


@app.route("/")
def index():
    db = get_db()
    # Создание экземпляра вспомогательного класса и вызов его метода
    # для заполнения index.html
    dbase = FDataBase(db)
    return render_template("index.html", menu=dbase.getMenu())


@app.teardown_appcontext
def close_db(error):
    """Закрываем соединение с БД, если оно было установлено"""
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == "__main__":
    app.run()
