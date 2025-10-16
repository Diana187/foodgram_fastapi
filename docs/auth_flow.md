# auth_flow.md

## Цель
Описать текущую схему аутентификации (Django + Djoser + TokenAuth) и зафиксировать, что переносится в FastAPI без ломки фронта.

---

## Аутентификация

- Тип: **TokenAuthentication (DRF authtoken)**
- Логин по: **email**
- Токен передаётся в заголовке  
  `Authorization: Token <token>`
- Логика — через **Djoser** (`djoser.urls`, `djoser.urls.authtoken`)

---

## Основные эндпоинты

| Метод | Путь | Описание | Требуется токен |
|--------|------|-----------|----------------:|
| POST | `/api/auth/token/login/` | вход (email + password) | ❌ |
| POST | `/api/auth/token/logout/` | выход (инвалидация токена) | ✅ |
| POST | `/api/users/` | регистрация | ❌ |
| GET  | `/api/users/me/` | профиль текущего пользователя | ✅ |
| GET  | `/api/users/{id}/` | публичный профиль | ❌ |
| GET  | `/api/users/subscriptions/` | список подписок | ✅ |
| POST/DELETE | `/api/users/{id}/subscribe/` | подписка / отписка | ✅ |

---

## Поведение

- **Регистрация:** создаёт пользователя (`email`, `username`, `first_name`, `last_name`, `password`).
- **Логин:** возвращает `{"auth_token": "<token>"}`.
- **Logout:** удаляет токен (`204 No Content`).
- **/me:** возвращает данные текущего пользователя.
- **Подписки:** проверка на самоподписку и дубликаты.

---

## Права доступа
- По умолчанию: `IsAuthenticated`
- Public:
  - `/auth/token/login/`, `/users/` (создание)
  - `GET /tags/`, `GET /ingredients/`
- Private:
  - CRUD для рецептов (`IsAuthorOrReadOnly`)
  - Подписки, избранное, корзина — только авторизованным.

---

## Перенос в FastAPI
Сохраняем:
- Эндпоинты и URL-структуру;
- Формат токена (`auth_token`);
- Ответы сериалайзеров (`CustomUserSerializer`, `CreateUserSerializer`);
- Логин/логаут-логику с теми же маршрутами.

Опционально:
- перейти на JWT в cookie с тем же API-контрактом (alias `auth_token`).

---
