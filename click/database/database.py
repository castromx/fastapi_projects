from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = 'sqlite:///dev.db'
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})

Base = declarative_base()
Session = sessionmaker(autoflush=False, bind=engine)
metadata = MetaData()

def get_db_session():
    db = Session()
    try:
        yield db
    finally:
        db.close()
