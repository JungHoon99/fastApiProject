from typing import List, Dict

from fastapi import FastAPI

app = FastAPI()

todo_data = {
    1: {
        "id": 1,
        "contents": "실전 fast API 0 수강",
        "is_done": True
    },
    2: {
        "id": 2,
        "contents": "실전 fast API 1 수강",
        "is_done": False
    },
    3: {
        "id": 3,
        "contents": "실전 fast API 2 수강",
        "is_done": False
    }
}


@app.get("/")
def health_check_handler():
    return {"message": "Hello World"}


@app.get("/todos")
def get_todos(order: str | None = None):
    response = list(todo_data.values())
    if order or order == 'DESC':
        return response[::-1]
    return response


@app.get("/todos/{id}")
def get_todo(id: int) -> dict:
    return todo_data.get(id, {})
