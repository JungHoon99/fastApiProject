from typing import List

from fastapi import Depends, HTTPException, Body, APIRouter
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import Todo
from database.repository import get_todos, get_todo_by_todo_id, create_todo, update_todo, delete_todo
from schema.request import CreateTodoRequest
from schema.response import TodoListSchema, TodoSchema

router = APIRouter(prefix="/todos", tags=["todos"])

@router.get("", status_code=200)
def get_todos_handler(
        order: str | None = None,
        session: Session = Depends(get_db)
):
    todos: List[Todo] = get_todos(session=session)
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
        session: Session = Depends(get_db)
) -> TodoSchema:
    todo: Todo | None = get_todo_by_todo_id(session=session, )
    if todo:
        return TodoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="Not Found")


@router.post("", status_code=201)
def post_todo_handler(
        request: CreateTodoRequest,
        session: Session = Depends(get_db)
) -> TodoSchema:
    todo: Todo = Todo.create(request)
    todo: Todo = create_todo(session=session, todo=todo)

    return TodoSchema.from_orm(todo)


@router.patch("/{id}", status_code=200)
def update_todo_handler(
        id: int,
        is_done: bool = Body(..., embed=True),
        session: Session = Depends(get_db),
):
    todo: Todo | None = get_todo_by_todo_id(session=session, todo_id=id)
    if todo:
        todo.done() if is_done else todo.undone()
        todo: Todo = update_todo(session=session, todo=todo)
        return todo
    raise HTTPException(status_code=404, detail="Not Found")


@router.delete("/{id}", status_code=204)
def delete_todo_handler(
        id: int,
        session: Session = Depends(get_db)
):
    todo: Todo | None = get_todo_by_todo_id(session=session, todo_id=id)

    if not todo:
        raise HTTPException(status_code=404, detail="Not Found")

    delete_todo(session=session, todo_id=id)
