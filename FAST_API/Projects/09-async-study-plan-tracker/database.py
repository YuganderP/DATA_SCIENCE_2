from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import event

DB_URL = "sqlite+aiosqlite:///./jobTracker.db"

engine = create_async_engine(DB_URL)


SessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
)


@event.listens_for(engine.sync_engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class Base(DeclarativeBase):
    pass


async def get_db():
    async with SessionLocal() as db:
        yield db


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
