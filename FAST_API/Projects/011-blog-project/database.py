from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


DB_URL = "sqlite:///./blog.db"

db = create_engine(DB_URL)


class Base(DeclarativeBase):
    pass


sessionLocal = sessionmaker(bind=db, autoflush=False)


def get_db():
    session = sessionLocal()
    try:
        yield session
    finally:
        session.close()
