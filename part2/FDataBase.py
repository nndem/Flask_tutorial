"""
This class represents solution instead of using an Alchemy
The class is binding the DB with others functions even with modelOfUser
"""

import math
import sqlite3
import time


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = """SELECT * FROM mainmenu"""
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка чтения из БД")
            return []

    def addPost(self, title, text, url):
        sql = """ INSERT INTO posts VALUES(NULL, ?, ?, ?, ?) """
        try:
            # проверка, что записи с таким url не существует
            sql_url = f"SELECT COUNT() as `count`" \
                      f"FROM posts WHERE url LIKE '{url}' "
            self.__cur.execute(sql_url)
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Статья с таким url уже существует")
                return False

            tm = math.floor(time.time())
            self.__cur.execute(sql, (title, text, url, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
            return False

        return True

    def getPost(self, alias):
        sql = f"SELECT title, text FROM posts WHERE url LIKE '{alias}' LIMIT 1"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchone()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД "+str(e))

        return (False, False)

    def getPostsAnonce(self):
        sql = f"SELECT id, title, text, url FROM posts ORDER BY time DESC"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД "+str(e))

        return []

    def addUser(self, name, email, hpsw):
        sql_count = f"SELECT COUNT() as `count` FROM users WHERE email LIKE '{email}'"
        sql_ins = f"INSERT INTO users VALUES(NULL, ?,?,?,NULL,?)"
        try:
            self.__cur.execute(sql_count)
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким email уже существует")
                return False

            tm = math.floor(time.time())
            self.__cur.execute(sql_ins, (name, email, hpsw, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавлеия пользователя в БД "+str(e))
            return False

        return True

    def getUserById(self, user_id):
        """
        this method will be used for creating a modelOfUser that will be stored in session
        """
        sql_get = f"SELECT * FROM users WHERE id ={user_id} LIMIT 1"
        try:
            self.__cur.execute(sql_get)
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД" + str(e))

        return False

    def getUserByEmail(self, email):
        """
        this  method will be used for checking email while authorization
        """
        sql_get = f"""SELECT * FROM users WHERE email="{email}" LIMIT 1"""
        try:
            self.__cur.execute(sql_get)
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД" + str(e))

    def updateUserAvatar(self, avatar, user_id):
        if not avatar:
            return False
        sql = f"UPDATE users " \
              f"SET avatar = ?" \
              f"WHERE id = ?"

        try:
            binary = sqlite3.Binary(avatar)
            self.__cur.execute(sql, (binary, user_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка обновления аватара в БД: ", str(e))
            return False
        return True

