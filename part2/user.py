"""
Model of class that will be stored in session
(UPD: only id of self.__user will be stored)
and attached to each request (UPD: by get_id()-method represented in Mixin-class).
The main part of the class is self.user
UserMixin contains such method as - is_authenticated(), is_anonymous(), get_id(), is_active()
get_id() method is used to extract id from the session and pass this value into user_loader-function.
"""
from flask_login import UserMixin


class User(UserMixin):

    def fromDB(self, user_id, db):
        self.__user = db.getUserById(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user['id'])

