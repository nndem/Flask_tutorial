from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite://///Users/nickolay.demidov/' \
                                        'PycharmProjects/flaskProjects/Flask_tutorial' \
                                        '/part5/login.db'
app.config["SECRET_KEY"] = "fccfa6730775d28a8b9fb49c53ee1653e5892cc4"

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


# represent DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    user = User.query.filter_by(username="Nick").first()
    login_user(user)
    return "You are now logged in"


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "You are now logged out!"

@app.route("/home")
@login_required
def home():
    return "The current usr is" + current_user.username


if __name__ == '__main__':
    app.run()
