import asyncio
from app.db.database import engine, DATABASE_URL

print(DATABASE_URL)
async def test():
    async with engine.begin() as conn:
        await conn.run_sync(lambda _: print("DB Connected Successfully"))

asyncio.run(test())
