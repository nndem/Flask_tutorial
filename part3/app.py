from flask import Flask, render_template, make_response

app = Flask(__name__)

menu = [{"title": "Главная", "url": "/"},
        {"title": "Добавить статью", "url": "/add_post"}]


@app.route('/')
def index():
    #  формирование кастомного ответа сервера с использованием open_resource() и make_response()
    img = None
    with app.open_resource(app.root_path + "/static/images/ava.jpg", mode="rb") as f:
        img = f.read()

    if img is None:
        return "None image"

    res = make_response(img)
    res.headers["Content-Type"] = "image/jpg"
    return res


if __name__ == '__main__':
    app.run()
