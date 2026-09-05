from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

DB_URL = "sqlite+aiosqlite:///./hospital_management_async.db"

engine = create_async_engine(DB_URL)


SessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


async def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        await session.close()
