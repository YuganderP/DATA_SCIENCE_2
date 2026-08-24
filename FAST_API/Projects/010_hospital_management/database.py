from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


DB_URL = "sqlite:///./hospital_management.db"

engine = create_engine(DB_URL)


SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    pass


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
