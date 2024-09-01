# import sys
from datetime import timedelta
from distutils.command.config import config
from http.client import HTTPException

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pyaspeller import YandexSpeller
# import psycopg2

import config
# import maindb
# from FDataBase import FDataBase
import user as user_data
from user import User

app = FastAPI(title="KODE")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Аутенфикация пользователей
# TODO после теста вынести в отдельный модуль
oauth2_dep = OAuth2PasswordBearer(tokenUrl="token")


def unauthed():
    raise HTTPException(status_code=401,
                        detail="Неверный логин или пароль",
                        headers={"WWW-Authenticate": "Bearer"})


@app.post("/token")
async def create_access_loken(
        form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data)
    """Получение имени пользователя и пароля из формы OAuth, возврат токена доступа."""
    user = user_data.auth_user(form_data.username, form_data.password)
    print(f"user: {user}")
    if not user:
        unauthed()
    expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = user_data.create_access_token(data={"sub": user["login"]},
                                                 expires=expires)
    print({"access_token": access_token, "token_type": "bearer"})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/token")
def get_access_token(token: str = Depends(oauth2_dep)) -> dict:
    """Возврат текущего токена доступа"""
    # user_login = user_data.get_jwt_username(token)
    # user_admin = user_data.get_jwt_admin(token)
    # print(f"user_login {user_login}")
    return {"token": token}


# @app.get("/protected")
# def protected_route(user: User = Depends(oauth2_dep)):
#     print("Защищенный эндпоинт")
#     # admin = user_data.get_jwt_admin(user)
#     return user


# # Тестовый вывод пользователей и заметок
# def print_users():
#     print(f"Запуск функции вывода списка пользователей.")
#     conn = maindb.connect_db()
#     dbase = FDataBase(conn)
#     users = dbase.get_all_user()
#     print(users)
#
#
# def print_notes():
#     print(f"Запуск функции вывода списка заметок.")
#     conn = maindb.connect_db()
#     dbase = FDataBase(conn)
#     notes = dbase.get_all_notes()
#     print(notes)


@app.post("/auth")
def auth(login: str, passw: str):
    print(f"Ваш логин: {login} Ваш пароль: {passw}")
    user = user_data.auth_user(login, passw)
    print(f"user: {user}")


# @app.get("/")
# def test():
#     print(f"Запуск эндпоинта вывода списка пользователей и заметок.")
#     print_users()
#     print_notes()
#     return "ok"


@app.post("/add_notes")
def add_notes(notes: str, user: User = Depends(oauth2_dep)):
    print("Эндпоинт добавления новой заметки.")
    print(f"get_notes: user: {user}")
    print(f"get_notes: type(user): {type(user)}")
    # Проверка ошибок текста через YandexSpeller
    print(f"Заметка до проверки: {notes}")
    speller = YandexSpeller()
    fixed_note = speller.spelled(notes)
    print(f"Проверенная заметка: {fixed_note}")
    new_note = user_data.add_user_notes(fixed_note, user)
    print(f"Полученная заметка: {new_note}")
    return new_note


@app.get("/get_notes")
def get_notes(user: User = Depends(oauth2_dep)):
    print(f"get_notes: user: {user}")
    print(f"get_notes: type(user): {type(user)}")
    notes = user_data.get_user_notes(user)
    return notes


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
    # print_users()
