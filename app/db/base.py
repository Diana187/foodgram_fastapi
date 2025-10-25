from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

# (опционально) именование констрейнтов — полезно для Alembic
NAMING_CONVENTION = {
    "ix": "ix_%(table_name)s__%(column_0_name)s",
    "uq": "uq_%(table_name)s__%(column_0_name)s",
    "ck": "ck_%(table_name)s__%(constraint_name)s",
    "fk": "fk_%(table_name)s__%(column_0_name)s__%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
metadata = MetaData(naming_convention=NAMING_CONVENTION)


class Base(DeclarativeBase):
    metadata = metadata


# КРИТИЧНО: импортировать модели, чтобы они зарегистрировались в Base.metadata
# (импорт по побочному эффекту — нормально для SQLAlchemy/Alembic)
from app.db.models import *  # noqa: F401,F403
