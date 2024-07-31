from fastapi import Depends

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import Todo


class TodoRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session
    def get_todos(self) -> list[Todo]:
        return list(self.session.scalars(select(Todo)))

    def get_todo_by_todo_id(self, todo_id: int) -> Todo | None:
        return self.session.scalar(select(Todo).where(Todo.id == todo_id))

    def create_todo(self, todo: Todo) -> Todo:
        self.session.add(instance=todo)
        self.session.commit()  # db에 세이브
        self.session.refresh(instance=todo)  # db read -> todo에 id값이 결정되는 시기
        return todo

    def update_todo(self, todo: Todo) -> Todo:
        self.session.add(instance=todo)
        self.session.commit()
        self.session.refresh(instance=todo)
        return todo

    def delete_todo(self, todo_id: int) -> None:
        self.session.execute(delete(Todo).where(Todo.id == todo_id))
        self.session.commit()
        return None
