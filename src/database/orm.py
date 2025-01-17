from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import declarative_base

from schema.request import CreateTodoRequest

Base = declarative_base()

class Todo(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True, index=True)
    contents = Column(String, nullable=False)
    is_done = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Todo(id={self.id}, contents={self.contents}, is_done={self.is_done})>'

    @classmethod
    def create(cls, request: CreateTodoRequest) -> 'Todo':
        return cls(
            contents=request.contents,
            is_done=request.is_done,
        )

    def done(self) -> 'Todo':
        self.is_done = True
        return self

    def undone(self) -> 'Todo':
        self.is_done = False
        return self
