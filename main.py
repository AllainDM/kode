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
    """Возврат текущего токена доступа."""
    return {"token": token}


# @app.post("/auth")
# def auth(login: str, passw: str):
#     print(f"Ваш логин: {login} Ваш пароль: {passw}")
#     user = user_data.auth_user(login, passw)
#     print(f"user: {user}")


@app.post("/add_notes")
def add_notes(notes: str, user: User = Depends(oauth2_dep)):
    """Добавление новой заметки."""
    print(f"get_notes: user: {user}")
    print(f"get_notes: type(user): {type(user)}")
    # Проверка ошибок текста через YandexSpeller
    print(f"Заметка до проверки: {notes}")
    speller = YandexSpeller()
    fixed_note = speller.spelled(notes)
    print(f"Проверенная заметка: {fixed_note}")
    # Отправим в модуль user запрос на добавление заметки в БД
    new_note = user_data.add_user_notes(fixed_note, user)
    print(f"Полученная заметка: {new_note}")
    return new_note


@app.get("/get_notes")
def get_notes(user: User = Depends(oauth2_dep)):
    """Вывод списка заметок."""
    print(f"get_notes: user: {user}")
    print(f"get_notes: type(user): {type(user)}")
    # Отправим в модуль user запрос на получение списка заметок из БД
    notes = user_data.get_user_notes(user)
    return notes


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
