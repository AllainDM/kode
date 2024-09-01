from datetime import datetime


class FDataBase:

    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    # Поиск пользователя по логину, необходимо для аутенфикации
    def get_user_by_login(self, login):
        try:
            self.__cur.execute(
                f"SELECT * FROM users WHERE login = '{login}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден 1.")
                return False
            print(f"Пользователь найден: {res}")
            return res

        except Exception as _ex:
            print("Ошибка поиска пользователя в БД", _ex)

        return False

    # Простой способ определения прав админа
    def get_admin(self, login: str):
        try:
            self.__cur.execute(
                f"SELECT * FROM users WHERE login = '{login}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден 2.")
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
                print("Пользователи не найдены.")
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
                print("Заметки не найдены 1.")
                return False

            return res
        except Exception as _ex:
            print("Ошибка поиска заметок в БД", _ex)

        return False

    # Получение списка всех заметок пользователя
    def get_all_notes_user(self, login: str):
        # Заметки хранятся по ид пользователей. Необходимо запросить ид по логину.
        user = self.get_user_by_login(login)
        try:
            self.__cur.execute(
                f"SELECT text FROM notes where user_id = {user[0]}")
            res = self.__cur.fetchall()
            if not res:
                print("Заметки не найдены 2.")
                return False

            return res
        except Exception as _ex:
            print("Ошибка поиска заметок в БД", _ex)

        return False

    # Добавление новой заметки
    def add_note(self, note: str, login: str):
        # Заметки хранятся по ид пользователей. Необходимо получить ид по логину.
        user = self.get_user_by_login(login)
        try:
            self.__cur.execute(
                "INSERT INTO notes (user_id, text, active) "
                "VALUES (%s, %s, %s)", (user[0], note, 1))
            print("Заметка добавлена.")
            self.__db.commit()
            return note
        except Exception as _ex:
            print("Ошибка добавления заметки в БД", _ex)

        return False
