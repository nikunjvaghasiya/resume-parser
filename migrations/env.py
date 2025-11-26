import asyncio
from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context

# Import your Base (VERY IMPORTANT)
from app.db.models import Base  
from app.db.database import DATABASE_URL

# Alembic Config
config = context.config
fileConfig(config.config_file_name)

# This is the key! Alembic needs this:
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations without DB connection (offline mode)."""
    url = DATABASE_URL.replace("+asyncpg", "")  # Convert async → sync
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Run actual DB migrations."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run in online mode using sync engine while app uses async engine."""
    sync_url = DATABASE_URL.replace("+asyncpg", "")

    connectable = create_engine(
        sync_url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        do_run_migrations(connection)

    connectable.dispose()


def run_migrations():
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        asyncio.run(run_migrations_online())


run_migrations()
