from sqlalchemy import select
from sqlalchemy.orm import Session

from database.orm import Todo


def get_todos(session: Session) -> list[Todo]:
    return list(session.scalars(select(Todo)))


def get_todo_by_todo_id(session: Session, todo_id: int) -> Todo | None:
    return session.scalar(select(Todo).where(Todo.id == todo_id))


def create_todo(session: Session, todo: Todo) -> Todo:
    session.add(instance=todo)
    session.commit()    # db에 세이브
    session.refresh(instance=todo)  # db read -> todo에 id값이 결정되는 시기
    return todo
