# app/db/migrations/env.py

import sys
from pathlib import Path

# 1) Добавляем корень проекта в sys.path, чтобы импортировался пакет "app"
sys.path.append(str(Path(__file__).resolve().parents[3]))

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.config import settings
from app.db.base import Base  # Base.metadata — источник моделей для автогенерации

# -----------------------------------------------------------------------------
# Alembic Config
# -----------------------------------------------------------------------------
config = context.config

# Логи Alembic (если настроены в alembic.ini)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные моделей для --autogenerate
target_metadata = Base.metadata


# -----------------------------------------------------------------------------
# URL БД: берём из настроек приложения
# В alembic.ini может быть sqlalchemy.url, но мы перекрываем его здесь.
# Для синхронного движка инспектора заменим +asyncpg на psycopg2.
# -----------------------------------------------------------------------------
def get_sync_url() -> str:
    url = str(settings.db_url)
    return url.replace("+asyncpg", "")  # 'postgresql://...'


# -----------------------------------------------------------------------------
# Offline режим (генерация SQL без подключения)
# -----------------------------------------------------------------------------
def run_migrations_offline() -> None:
    url = get_sync_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


# -----------------------------------------------------------------------------
# Online режим (обычное применение миграций)
# -----------------------------------------------------------------------------
def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = get_sync_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# -----------------------------------------------------------------------------
# Entry
# -----------------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
