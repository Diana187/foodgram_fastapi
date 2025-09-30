# Definition of Done — Foodgram → FastAPI (Итерация 1)

**Цель итерации:** запустить FastAPI-бэкенд с функциональным паритетом по контракту **Contract v1 — FROZEN**, без ломающих изменений.

## 0 Скоуп итерации (что входит)

* Аутентификация: `POST /api/auth/token/login/`, `POST /api/auth/token/logout/` (Token header).
* Пользователи: `/api/users/`, `/api/users/{id}/`, `/api/users/me/`, `/api/users/set_password/`.
* Рецепты: CRUD (Create, Read, Patch, Delete автора), избранное, корзина, скачивание списка покупок.
* Справочники: теги, ингредиенты (+ поиск по `name`).
* Подписки: список моих, подписаться/отписаться.
* Пагинация, фильтры, форматы ошибок — строго по контракту.
* Картинки рецептов: input — Base64 data URL; output — абсолютный URL.
* Экспорт списка покупок: `application/pdf` или `text/plain` (бинарный контент).

---

## 1 Репозиторий / инфраструктура

* [ ] Создан модуль `app/` (FastAPI), структура: `main.py`, `routers/`, `schemas/`, `models/`, `services/`, `deps/`, `auth/`, `config.py`.
* [ ] Конфиг `.env` + безопасные дефолты (`ENV`, `SECRET_KEY`, `DB_*`, `CORS_*`, `MEDIA_ROOT`, `MEDIA_URL`).
* [ ] Docker/Docker Compose (API + DB + (опц.) nginx для раздачи медиа).
* [ ] Настроен CORS по списку источников из требований.
* [ ] Логирование: уровень, формат, трассировки ошибок.
* [ ] Alembic миграции отражают доменную модель (паритет с Django моделями).
* [ ] CI (pytest + линтеры) зелёный.

---

## 2 Контракт и документация

* [ ] Файл `docs/openapi-schema.yml` обновлён и совпадает с беком.
* [ ] `docs/api_contract.md` содержит обзор, таблицу эндпоинтов, правила пагинации/ошибок/аутентификации.
* [ ] `docs/domain_model.md` заполнён (сущности, связи, инварианты).
* [ ] Все ответы/ошибки соответствуют `components.schemas/*` и `components.responses/*`.
* [ ] Любые отклонения зафиксированы в `docs/contract_deltas.md` (дата, что и почему).

---

## 3 Аутентификация (Token)

* [ ] `POST /api/auth/token/login/` → `201 { "auth_token": "…" }` при валидных кредах.
* [ ] `POST /api/auth/token/logout/` → `204` и токен становится невалидным.
* [ ] Все защищённые ручки требуют `Authorization: Token <auth_token>`.
* [ ] На неавторизованные запросы возвращается `401 AuthenticationError`.

---

## 4 Поведение эндпоинтов (ядро)

### Пользователи

* [ ] `GET /api/users/` — пагинация `{count,next,previous,results}`.
* [ ] `POST /api/users/` — создаёт пользователя по `CustomUserCreate`, ответ `201 CustomUserResponseOnCreate`.
* [ ] `GET /api/users/{id}/` — публичный профиль `User`.
* [ ] `GET /api/users/me/` — текущий пользователь `User`.
* [ ] `POST /api/users/set_password/` — меняет пароль, `204`.

### Рецепты

* [ ] `GET /api/recipes/` — фильтры: `is_favorited`, `is_in_shopping_cart`, `author`, `tags` (slug[]).
* [ ] `POST /api/recipes/` — принимает `RecipeCreateUpdate` (image — Base64 data URL), ответ `201 RecipeList`.
* [ ] `GET /api/recipes/{id}/` — `RecipeList`.
* [ ] `PATCH /api/recipes/{id}/` — только автор, `200 RecipeList`.
* [ ] `DELETE /api/recipes/{id}/` — только автор, `204`.
* [ ] `POST /api/recipes/{id}/favorite/` — `201 RecipeMinified`; `DELETE` — `204`.
* [ ] `POST /api/recipes/{id}/shopping_cart/` — `201 RecipeMinified`; `DELETE` — `204`.
* [ ] `GET /api/recipes/download_shopping_cart/` — `200` (PDF или TXT), тип контента по контракту.

### Теги и ингредиенты

* [ ] `GET /api/tags/` → `Tag[]`, `GET /api/tags/{id}/` → `Tag`.
* [ ] `GET /api/ingredients/` → фильтр `name` (префикс), `GET /api/ingredients/{id}/` → `Ingredient`.

### Подписки

* [ ] `GET /api/users/subscriptions/` → пагинация + `recipes_limit`.
* [ ] `POST /api/users/{id}/subscribe/` → `201 UserWithRecipes` (+ `recipes_limit`).
* [ ] `DELETE /api/users/{id}/subscribe/` → `204`.

---

## 5 Форматы и инварианты

* [ ] **Пагинация**: вход `page, limit`; выход `{count, next, previous, results}`.
* [ ] **Ошибки**: 400 `ValidationError|NestedValidationError`, 401 `AuthenticationError`, 403 `PermissionDenied`, 404 `NotFound`.
* [ ] **Флаги** `is_favorited`, `is_in_shopping_cart`, `is_subscribed` вычисляются относительно **текущего** пользователя.
* [ ] **URL изображения** в `RecipeList.image` — абсолютный (`http(s)://…/media/...`).
* [ ] **Идемпотентность** добавления/удаления избранного/корзины/подписки — корректные коды `400` при повторе, `204` при удалении отсутствующего — строго по контракту (если так описано).

---

## 6 Качество кода / безопасность

* [ ] Линтеры проходят (ruff/flake8, black, isort; mypy — опционально).
* [ ] Нет `TODO/XXX` в изменённых файлах.
* [ ] Валидация входных данных Pydantic-схемами соответствует контракту (минимумы, паттерны, required).
* [ ] Ограничения загрузки изображений: размер, типы (PNG/JPEG) — задокументированы и валидируются.
* [ ] CORS включён на нужные источники.
* [ ] Секреты не коммитятся (env, CI secrets).

---

## 7 Тестирование (обязательно)

**Авто-тесты (pytest):**

* [ ] Юнит-тесты схем/сервисов (валидация, маппинг моделей↔схем).
* [ ] Интеграционные тесты по всем эндпоинтам из скоупа (успех/ошибки/права).
* [ ] Тесты пагинации и фильтров.
* [ ] Тесты загрузки Base64-картинки и получения абсолютного URL.
* [ ] Тесты экспорта списка покупок (контент-тайпы, бинарность).
* [ ] Тесты на вычисляемые флаги (`is_favorited`, `is_in_shopping_cart`, `is_subscribed`).

**Контракт-тесты:**

* [ ] Прогон по `docs/openapi-schema.yml` (напр., Schemathesis) — зелёный.
* [ ] Линт контракта (напр., Spectral) — без критических ошибок.

**Smoke-тесты (ручные):**

* [ ] Login→GET protected→Logout→проверить 401.
* [ ] Создать рецепт → увидеть в списке/деталях.
* [ ] Добавить/удалить избранное и корзину.
* [ ] Скачать список покупок: файл открывается, код 200, корректный тип.
* [ ] Подписаться/отписаться, проверить `is_subscribed`.

---

## 8 Производительность / эксплуатация

* [ ] Индексы по полям фильтров (`author`, `tags.slug`, `ingredients.name` prefix).
* [ ] N+1 исключён (eager loading: select_related/prefetch_related).
* [ ] Базовые smoke-метрики ответа (p95 < N мс на `/api/recipes/?limit=...` с реалистичными данными).

---

## 9 Готово к релизу

* [ ] Сборка контейнеров успешна, миграции применяются на чистую БД.
* [ ] `docs/` обновлён (contract, domain model, DoD).
* [ ] Ветка смёржена, теги релиза проставлены (semver/дата).
* [ ] Стейкхолдеры подтвердили отсутствие ломающих изменений.

---

### Out of scope (явно НЕ в этой итерации)

* Глобальный поиск по полнотексту.
* Версионирование API `v2`.
* WebSockets/стримы.
* Рейт-лимиты и антибот (обсудим отдельно).