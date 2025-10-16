# infra_plan.md (compact)

## Цель
Минимальная docker-инфра на спринт: **backend(app)**, **db(PostgreSQL)**, **nginx**, (опц.) **pgAdmin**. Позже: **Redis**, **MinIO**.

## Сервисы

### backend (app)
- Образ: Python 3.9 + Gunicorn (`foodgram.wsgi`), порт **8000** (внутри).
- Тома: `static:/app/static`, `media:/app/media`, (dev) `../backend:/app:rw`.
- ENV (из `.env`): `DB_ENGINE`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `DB_HOST=db`, `DB_PORT=5432`, `SECRET_KEY`, `DEBUG`.
- Зависит от: `db`. Внешний доступ — через `nginx`.

### db (PostgreSQL)
- Образ: `postgres` (реком. закрепить: `postgres:15-alpine`), порт **5432**.
- Данные: `./database:/var/lib/postgresql/data` (или именованный `db_data`).
- ENV: `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`.

### nginx (reverse proxy + статика)
- Образ: `nginx:1.19.3` (реком. обновить), порт **80:80**.
- Тома: 
  - `./nginx.conf:/etc/nginx/conf.d/default.conf`
  - `../frontend/build:/usr/share/nginx/html/`
  - `../docs/:/usr/share/nginx/html/api/docs/`
  - `media:/usr/share/nginx/media`
  - (опц.) `static:/usr/share/nginx/static`
- Зависит от: `backend`, `frontend`.

### frontend
- Сборка из `../frontend/Dockerfile`. Артефакты читает `nginx` из `../frontend/build`.

### (опц.) pgadmin
- Образ: `dpage/pgadmin4:latest`, порт **5050:80**.
- ENV: `PGADMIN_DEFAULT_EMAIL`, `PGADMIN_DEFAULT_PASSWORD`.
- Том: `pgadmin_data:/var/lib/pgadmin`. Сеть — общая с `db`.

## Сети и тома
- Сеть: bridge по умолчанию (можно назвать `foodgram-net`).
- Томa: `media`, `static`, (опц.) `db_data`, `pgadmin_data`.

## Пример `.env`
- DB_ENGINE=django.db.backends.postgresql
- POSTGRES_DB=postgres
- POSTGRES_USER=postgres
- POSTGRES_PASSWORD=postgres
- DB_HOST=db
- DB_PORT=5432
- SECRET_KEY=change-me
- DEBUG=1
- ALLOWED_HOSTS=*

## Команды (dev)
- docker compose up -d --build
- docker compose logs -f backend
- docker compose exec backend python manage.py migrate
- docker compose exec backend python manage.py collectstatic --noinput


## Позже (следующие итерации)
- **Redis** (`redis:7-alpine`, 6379) — кэш/очереди. ENV: `REDIS_URL=redis://redis:6379/0`.
- **MinIO** (`minio/minio`, 9000/9001) — внешнее хранилище медиа. ENV: `S3_*`/`MINIO_*`.

## Прод-заметки
- Не публиковать `db:5432` наружу; убрать bind-код; закрепить теги образов; secrets вне `.env`; `restart: unless-stopped`; `healthcheck` для `backend/db`.
