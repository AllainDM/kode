import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="KODE")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("")
@app.get("/")
def test():
    return "ok"


@app.post("/add_notes")
def add_notes(notes: str):
    print(f"Полученная заметка: {notes}")
    return "ok"


@app.get("/get_notes")
def get_notes():
    return "ok"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
