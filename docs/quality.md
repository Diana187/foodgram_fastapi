# quality.md

## Цель
Единые правила качества кода для Foodgram→FastAPI:
**линтинг (Ruff)**, **форматирование (Black)**, **проверка типов (MyPy)**, **коммит-хуки (pre-commit)**.
Файл — источник правды для локальной разработки и CI.

---

## Конвенции
- Python ≥ 3.12
- Код приложения: `app/**`, тесты: `tests/**`, миграции: `alembic/**`
- Максимальная длина строки: **88**
- Импорт-стиль: **isort через Ruff**
- Миграции и автогенерированный код не проверяются строго
- Все новые функции — с аннотациями типов

---

## Установка (локально)
```bash
pip install -U ruff black mypy pre-commit \
  pydantic mypy-extensions \
  types-requests types-python-dateutil
pre-commit install
