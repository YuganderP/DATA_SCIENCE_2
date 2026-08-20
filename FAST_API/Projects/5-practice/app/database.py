# from sqlalchemy import create_engine, event
# from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import event

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


# DATABASE_URL = "sqlite:///./job_tracker.db"
DATABASE_URL = "sqlite+aiosqlite:///./job_tracker.db"


# engine = create_async_engine(DATABASE_URL)
engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})


# SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
