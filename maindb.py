import psycopg2

import config

def connect_db():
    try:
        conn = psycopg2.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.db_name
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Ошибка подключения к БД: {e}")
        # sys.exit(1)