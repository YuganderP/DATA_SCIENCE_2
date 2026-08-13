from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

SQL_ALCHEMY_DATABASE_URL = "sqlite:///./sports_venue.db"


db = create_engine(SQL_ALCHEMY_DATABASE_URL)  # returns a engine object

SessionLocal = sessionmaker(bind=db, autoflush=False, autocommit=False)
# bind to tell the session which engine to bind


class Base(DeclarativeBase):
    pass


# "Base is the declarative base class provided by SQLAlchemy.
# Our ORM models inherit from it, which allows SQLAlchemy to recognize and manage those classes
# as database models and keep their table metadata."
# ORM : object relational mapping


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
