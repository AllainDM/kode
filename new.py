from datetime import datetime

import psycopg2

import config

"""
   Модуль обновления(сброса) БД.
   Запуск вручную из терминала.
   Основная функция запускается сразу при импорте модуля.
"""


def update_tables():
    try:
        conn = psycopg2.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.db_name
        )

        cursor = conn.cursor()

        # Удаление таблицы с пользователями
        cursor.execute(""
                       "DROP TABLE IF EXISTS users"
                       )
        print(f"{datetime.now()}: Таблица user удалена")
        conn.commit()

        # Создание таблицы с пользователями
        cursor.execute(""
                       "CREATE TABLE IF NOT EXISTS users ("
                       "row_id serial PRIMARY KEY, "
                       "login text NOT NULL, "
                       "psw text NOT NULL, "
                       "name text, "
                       "admin int);"
                       )
        print(f"{datetime.now()}: Таблица users создана")
        conn.commit()

        # Добавление предустановленных пользователей
        # Дефолтный пароль: 1234

        cursor.execute("INSERT INTO users (login, psw, name, admin) "
                       "VALUES (%s, %s, %s, %s)",
                       ('admin', '$2b$12$lzAgnuuRHRMd5xRABM7QLeoQfOxCkRvVHdrEmrt8j8OCEYUo7cFtu',
                        'Админ', 1))
        print("Пользователь добавлен")
        conn.commit()

        cursor.execute("INSERT INTO users (login, psw, name, admin) "
                       "VALUES (%s, %s, %s, %s)",
                       ('first', '$2b$12$lzAgnuuRHRMd5xRABM7QLeoQfOxCkRvVHdrEmrt8j8OCEYUo7cFtu',
                        'Первый', 0))
        print("Пользователь добавлен")
        conn.commit()

        cursor.execute("INSERT INTO users (login, psw, name, admin) "
                       "VALUES (%s, %s, %s, %s)",
                       ('second', '$2b$12$lzAgnuuRHRMd5xRABM7QLeoQfOxCkRvVHdrEmrt8j8OCEYUo7cFtu',
                        'Второй', 0))
        print("Пользователь добавлен")
        conn.commit()

        # Удаление таблицы с заметками
        cursor.execute(""
                       "DROP TABLE IF EXISTS notes"
                       )
        print(f"{datetime.now()}: Таблица notes удалена")
        conn.commit()

        # Создание таблицы с заметками
        cursor.execute(""
                       "CREATE TABLE IF NOT EXISTS notes ("
                       "row_id serial PRIMARY KEY, "
                       "user_id int NOT NULL, "
                       "text text NOT NULL, "
                       "active int NOT NULL);"
                       )
        print(f"{datetime.now()}: Таблица notes создана")
        conn.commit()

        # Добавление предустановленных заметок
        cursor.execute("INSERT INTO notes (user_id, text, active) "
                       "VALUES (%s, %s, %s)",
                       (1, 'Тестовая заметка создаваемая при обновлении БД пользователя с ид 1.',
                        1))
        print("Запись добавлена")
        conn.commit()

        cursor.execute("INSERT INTO notes (user_id, text, active) "
                       "VALUES (%s, %s, %s)",
                       (2, 'Тестовая заметка создаваемая при обновлении БД пользователя с ид 2.',
                        1))
        print("Запись добавлена")
        conn.commit()

        cursor.execute("INSERT INTO notes (user_id, text, active) "
                       "VALUES (%s, %s, %s)",
                       (3, 'Тестовая заметка создаваемая при обновлении БД пользователя с ид 3.',
                        1))
        print("Запись добавлена")
        conn.commit()

        cursor.close()
        conn.close()

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)


update_tables()
