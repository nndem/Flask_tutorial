import datetime

from flask import Flask, request, make_response, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "1213377564b1ff2de1f8e24caddea9f73736cfa1"
# устанавливаем время жизни сессии в 10 дней
app.permanent_session_lifetime = datetime.timedelta(days=10)

data = [1, 2, 3, 4]


# Когда в session храним несколько объектов:
@app.route("/")
def index():
    session.permanent = True  # сохраняем сессию после закрытия браузера
    if "data" in session:
        session["data"][0] += 1  # модифицирование данных
        session.modified = True
    else:
        session["data"] = data  # запись данных в сессию
    return f"<h1>Main Page</h1><p>Данные в сессии: {session['data']}"


if __name__ == '__main__':
    app.run()
