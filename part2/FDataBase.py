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
        sql_ins = f"INSERT INTO users VALUES(NULL, ?,?,?,?)"
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

