from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:1234@127.0.0.1:3306/todos"

engine = create_engine(DATABASE_URL, echo=True) #echo=True는 sqlalchemy에서 사용되는 쿼리 확인용
SessionFactory = sessionmaker(
    autocommit=False,   # 명시적으로 커밋을 하겠다
    autoflush=False,    # 명시적으로 플러쉬를 하겠다.
    bind=engine
)

session = SessionFactory()