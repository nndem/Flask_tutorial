from flask import Flask, request, make_response, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "1213377564b1ff2de1f8e24caddea9f73736cfa1"


@app.route("/")
def index():
    if "visits" in session:
        session["visits"] = session.get("visits") + 1  # обновление данных в сессии
    else:
        session["visits"] = 1  # запись данных в сессию
    return f"<h1>Main Page</h1><p>Число просмотров: {session['visits']}"


if __name__ == '__main__':
    app.run()
