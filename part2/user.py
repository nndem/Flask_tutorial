"""
Model of class that will be stored in session
(UPD: only id of self.__user will be stored)
and attached to each request (UPD: by get_id()-method represented in Mixin-class).
The main part of the class is self.user
UserMixin contains such method as - is_authenticated(), is_anonymous(), get_id(), is_active()
get_id() method is used to extract id from the session and pass this value into user_loader-function.
"""
from flask_login import UserMixin
from flask import url_for


class User(UserMixin):

    def fromDB(self, user_id, db):
        self.__user = db.getUserById(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user['id'])

    def getName(self):
        return self.__user["name"] if self.__user else "Без имени"

    def getEmail(self):
        return self.__user["email"] if self.__user else "Без email"

    def getAvatar(self, app):
        img = None
        if not self.__user["avatar"]:
            try:
                with app.open_resource(app.root_path + url_for("static",
                                                                filename="images/default.jpg"), "rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print("Не найден аватар по умолчанию: "+str(e))
        else:
            img = self.__user["avatar"]

        return img

    def verifyExt(self, filename):
        ext = filename.rsplit(".", 1)[1]
        if ext == "jpg" or ext == "JPG" or ext == "png" or ext == "PNG":
            return True
        return False
