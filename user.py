from datetime import timedelta, datetime
from pydantic import BaseModel

from passlib.context import CryptContext
from typing_extensions import deprecated
# import jose
from jose import jwt

import maindb
from FDataBase import FDataBase
import config

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    login: str
    passw: str


def get_hash(passw: str) -> str:
    """Возврат хеша пароля."""
    print("Попытка захешировать пароль.")
    print(f"Хеш пароля: {pwd_context.hash(passw)}")
    return pwd_context.hash(passw)

def get_jwt_username(token: str) -> str | None:
    """Возврат логина пользователя из JWT"""
    print(f"Определение имени пользователя")
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=ALGORITHM)
        print(f"payload {payload}")
        if not (username := payload.get("sub")):
            return None
    # except jwt.JWTError:
    except:
        return None
    return username

def get_jwt_admin(token: str) -> str | None:
    """Возврат логина пользователя из JWT"""
    print(f"Определение прав пользователя")
    # Найдем пользователя в БД
    conn = maindb.connect_db()
    dbase = FDataBase(conn)
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=ALGORITHM)
        if not (login := payload.get("sub")):
            return None
    except:
        return None
    admin = dbase.get_admin(login)
    print(f"admin {admin}")
    if admin:
        print("Текущий пользователь имеет права администратора.")
    return admin


def verify_password(passw: str, hash1: str) -> bool:
    """Хеширование полученного от пользователя пароля и сравнение с хешем из БД."""
    return pwd_context.verify(passw, hash1)


def auth_user(login: str, passw: str):
    """Аутенфикация пользователя"""
    # Найдем пользователя в БД
    conn = maindb.connect_db()
    dbase = FDataBase(conn)
    user = dbase.get_user_by_login(login)
    if not user:
        print("Пользователь не обнаружен.")
        return None
    # Для сверки достанем хеш из user[2] это готовая запись хеша пароля в БД
    print(f"user[2] {user[2]}")
    if not verify_password(passw, user[2]):
        print("Ошибка сверки пароля.")
        return None
    # Если все ок вернем логин в словаре.
    return {"login": user[1]}

def create_access_token(data: dict, expires: timedelta | None = None):
    """Возвращение токена доступа JWT"""
    src = data.copy()
    now = datetime.utcnow()
    # if not expires:
    expires = timedelta(minutes=15)
    src.update({"exp": now + expires})
    encode_jwt = jwt.encode(src, config.SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

def get_user_notes(user: str):
    """Получение всех заметок польвателя"""
    # Найдем пользователя
    login = get_jwt_username(user)
    print(f"get_user_notes: login: {login}")
    conn = maindb.connect_db()
    dbase = FDataBase(conn)
    # user = dbase.get_user_by_login(login)
    if not user:
        print("Пользователь не обнаружен.")
        return None
    notes = dbase.get_all_notes_user(login)
    return notes

def add_user_notes(note: str, user: str):
    """Добавление заметки польвателя"""
    print("Добавление заметки польвателя")
    # Найдем пользователя
    login = get_jwt_username(user)
    print(f"get_user_notes: login: {login}")
    conn = maindb.connect_db()
    dbase = FDataBase(conn)
    # user = dbase.get_user_by_login(login)
    if not user:
        print("Пользователь не обнаружен.")
        return None
    new_note = dbase.add_note(note, login)
    # Сразу вернем обратно добавленную заметку
    return new_note
