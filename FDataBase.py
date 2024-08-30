from datetime import datetime


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    # Поиск пользователя по логину, необходимо для аутенфикации
    def get_user_by_login(self, login):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE login = '{login}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("User not found")
                return False
            print(f"Пользователь найден: {res}")
            return res

        except Exception as _ex:
            print("Ошибка поиска пользователя в БД", _ex)

        return False

    # Простой способ определения прав админа
    def get_admin(self, login: str):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE login = '{login}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("User not found")
                return False
            print(f"Пользователь найден: {res}")
            if res[4] == 1:
                return True
            return False

        except Exception as _ex:
            print("Ошибка поиска пользователя в БД", _ex)

        return False

    # Получение списка всех пользователей
    def get_all_user(self):
        try:
            self.__cur.execute(f"SELECT * FROM users")
            res = self.__cur.fetchall()
            if not res:
                print("Users not found")
                return False

            return res
        except Exception as _ex:
            print("Ошибка поиска пользователей в БД", _ex)

        return False

    # Получение списка вообще всех заметок
    def get_all_notes(self):
        try:
            self.__cur.execute(f"SELECT * FROM notes")
            res = self.__cur.fetchall()
            if not res:
                print("Notes not found")
                return False

            return res
        except Exception as _ex:
            print("Ошибка поиска заметок в БД", _ex)

        return False

    # Получение списка всех заметок пользователя
    def get_all_notes_user(self, login: str):
        # Заметки хранятся по ид пользователей. Необходимо запросить ид по логину.
        user = self.get_user_by_login(login)
        print(f"user {user[0]}")
        print(f"type(user) {type(user[0])}")
        try:
            self.__cur.execute(f"SELECT text FROM notes where user_id = {user[0]}")
            res = self.__cur.fetchall()
            if not res:
                print("Notes not found")
                return False

            return res
        except Exception as _ex:
            print("Ошибка поиска заметок в БД", _ex)

        return False
