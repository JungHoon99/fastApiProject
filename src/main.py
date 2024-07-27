from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel

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


class CreateTodo(BaseModel):
    id: int
    contents: str
    is_done: bool


@app.get("/", status_code=200)
def health_check_handler():
    return {"message": "Hello World"}


@app.get("/todos", status_code=200)
def get_todos(order: str | None = None):
    response = list(todo_data.values())
    if order or order == 'DESC':
        return response[::-1]
    return response


@app.post("/todos", status_code=201)
def post_todo(request: CreateTodo):
    todo_data[request.id] = request.dict()
    return todo_data[request.id]


@app.get("/todos/{id}", status_code=200)
def get_todo(id: int) -> dict:
    todo = todo_data.get(id)
    if todo:
        return todo
    raise HTTPException(status_code=404, detail="Not Found")


@app.patch("/todos/{id}", status_code=200)
def update_todo(
        id: int,
        is_done: bool = Body(..., embed=True)
):
    if todo := todo_data.get(id):
        todo["is_done"] = is_done
        return todo
    raise HTTPException(status_code=404, detail="Not Found")

@app.delete("/todos/{id}", status_code=204)
def delete_todo(id: int):
    todo = todo_data.pop(id, None)
    if todo:
        return todo
    return HTTPException(status_code=404, detail="Not Found")
