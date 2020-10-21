from flask import Flask, render_template, request
import sqlite3
import os

# конфигурация
DATABASE = "/tmp/site.db"
DEBUG = True
SECRET_KEY = "secret_key"

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, "site.db")))


# создание БД (из конфигурации нашего приложения)
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row  # записи в БД будут иметь вид не кортежа, а в виде словаря
    return conn


# Запуск создания БД с таблицами (без запуска веб-сервера)
def create_db():
    db = connect_db()
    with app.open_resource('sql_code.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()
# создание БД без поднятия сервера
# Python Console
# >>> from app import create_db
# >>> create_db()


# if __name__ == "__main__":
#     app.run()
