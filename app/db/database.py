from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from databases import Database
import os

# DB_USER = os.getenv("DB_USER", "nikunj")
# DB_PASS = os.getenv("DB_PASS", "nikunj@04")
# DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
# DB_NAME = os.getenv("DB_NAME", "resume_db")

DATABASE_URL = f"postgresql+asyncpg://nikunj:nikunj%4004@127.0.0.1:5432/resume_db"

# SQLAlchemy async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create async session maker
async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Databases library (optional)
database = Database(DATABASE_URL)

# Dependency
async def get_db():
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
