from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "sqlite:///./shop_app.db"
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
# Створення екземпляру сеансу бази даних.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# declarative_base() повертає клас, який успадковується, щоб створити кожну з моделей або класів бази даних (моделі ORM)
Base = declarative_base()

# Створення метаданних бази данних
metadata = MetaData()

# Створення, і передача сесії
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()