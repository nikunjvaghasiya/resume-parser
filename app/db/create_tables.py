from app.db.database import engine
from app.db.models import Base
import asyncio


async def create_tables():
    print("Creating tables...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Done.")

if __name__ == "__main__":
    asyncio.run(create_tables())
