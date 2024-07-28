from typing import List

from fastapi import FastAPI, Body, HTTPException, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import Todo
from database.repository import get_todos, get_todo_by_todo_id
from schema.request import CreateTodoRequest
from schema.response import TodoListSchema, TodoSchema

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


@app.get("/", status_code=200)
def health_check_handler():
    return {"message": "Hello World"}


@app.get("/todos", status_code=200)
def get_todos_handler(
        order: str | None = None,
        session: Session = Depends(get_db)
):
    todos: List[Todo]=get_todos(session=session)
    if order or order == 'DESC':
        return TodoListSchema(
            todos=[TodoSchema.from_orm(todo) for todo in todos[::-1]]
        )
    return TodoListSchema(
        todos=[TodoSchema.from_orm(todo) for todo in todos]
    )


@app.post("/todos", status_code=201)
def post_todo_handler(request: CreateTodoRequest):
    todo_data[request.id] = request.dict()
    return todo_data[request.id]


@app.get("/todos/{id}", status_code=200)
def get_todo_handler(
        id: int,
        session: Session = Depends(get_db)
) -> TodoSchema:
    todo: Todo | None = get_todo_by_todo_id(session=session, )
    if todo:
        return TodoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="Not Found")


@app.patch("/todos/{id}", status_code=200)
def update_todo_handler(
        id: int,
        is_done: bool = Body(..., embed=True)
):
    if todo := todo_data.get(id):
        todo["is_done"] = is_done
        return todo
    raise HTTPException(status_code=404, detail="Not Found")

@app.delete("/todos/{id}", status_code=204)
def delete_todo_handler(id: int):
    todo = todo_data.pop(id, None)
    if todo:
        return todo
    return HTTPException(status_code=404, detail="Not Found")
