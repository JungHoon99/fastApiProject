from typing import List

from pydantic import BaseModel

'''
ORM에 선언한 컬럼과 response에 정의한 컬럼이 같은데 왜 다시 정의하냐?
-> 지금은 구조가 단순하지만 컬럼간에 연산이 있거나 객체를 중첩된 구조로 반환한다던가 주요 컬럼만 리턴하고 싶을 때가 있기 때문
'''

class TodoSchema(BaseModel):
    id: int
    contents: str
    is_done: bool

    class Config:
        orm_mode = True


class TodoListSchema(BaseModel):
    todos: List[TodoSchema]
