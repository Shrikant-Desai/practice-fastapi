# models/base.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from core.config import get_settings

settings = get_settings()

# The engine manages the connection pool
engine = create_async_engine(
    settings.database_url,  # postgresql+asyncpg://user:pass@localhost/db
    pool_size=10,  # keep 10 connections open
    max_overflow=20,  # allow 20 more under heavy load
    echo=settings.debug,  # log SQL queries in development
)

# Session factory — each request gets its own session
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # don't reload objects after commit
)


class Base(DeclarativeBase):
    pass  # all models inherit from this
