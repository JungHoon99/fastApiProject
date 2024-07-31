from typing import List

from fastapi import Depends, HTTPException, Body, APIRouter

from database.orm import Todo
from database.repository import TodoRepository
from schema.request import CreateTodoRequest
from schema.response import TodoListSchema, TodoSchema

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("", status_code=200)
def get_todos_handler(
        order: str | None = None,
        todo_repository: TodoRepository = Depends(TodoRepository),
):
    todos: List[Todo] = todo_repository.get_todos()
    if order or order == 'DESC':
        return TodoListSchema(
            todos=[TodoSchema.from_orm(todo) for todo in todos[::-1]]
        )
    return TodoListSchema(
        todos=[TodoSchema.from_orm(todo) for todo in todos]
    )


@router.get("/{id}", status_code=200)
def get_todo_handler(
        id: int,
        todo_repository: TodoRepository = Depends(TodoRepository),
) -> TodoSchema:
    todo: Todo | None = todo_repository.get_todo_by_todo_id(todo_id=id)
    if todo:
        return TodoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="Not Found")


@router.post("", status_code=201)
def post_todo_handler(
        request: CreateTodoRequest,
        todo_repository: TodoRepository = Depends(TodoRepository),
) -> TodoSchema:
    todo: Todo = Todo.create(request)
    todo: Todo = todo_repository.create_todo(todo=todo)

    return TodoSchema.from_orm(todo)


@router.patch("/{id}", status_code=200)
def update_todo_handler(
        id: int,
        is_done: bool = Body(..., embed=True),
        todo_repository: TodoRepository = Depends(TodoRepository),
):
    todo: Todo | None = todo_repository.get_todo_by_todo_id(todo_id=id)
    if todo:
        todo.done() if is_done else todo.undone()
        todo: Todo = todo_repository.update_todo(todo=todo)
        return todo
    raise HTTPException(status_code=404, detail="Not Found")


@router.delete("/{id}", status_code=204)
def delete_todo_handler(
        id: int,
        todo_repository: TodoRepository = Depends(TodoRepository),
):
    todo: Todo | None = todo_repository.get_todo_by_todo_id(todo_id=id)

    if not todo:
        raise HTTPException(status_code=404, detail="Not Found")

    todo_repository.delete_todo(todo_id=id)
