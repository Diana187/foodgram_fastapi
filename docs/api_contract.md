# foodgram_fastapi

1. Обзор

- Источник: openapi-schema.yml (docs/openapi-schema.yml, commit hash bdde5cad91dec00d694139348aef6a498ac2aee1)

- Базовый URL: /

- Версия контракта: Contract v1 — FROZEN

- Совместимость: “без ломки фронта; изменения только с согласованием”

2. Аутентификация

- Механизм: токен-аутентификация.
    - POST /api/auth/token/login/ → выдает auth_token
    - POST /api/auth/token/logout/ → инвалидирует текущий токен
    - Передача токена в заголовке: Authorization: Token abc123

- Как выглядит успешный ответ:
    - Login: 201 + { "auth_token": "..." }
    - Logout: 204 (пусто)
- Как выглядит неуспешный ответ:
    - 401 AuthenticationError — неавторизован
    - 400 ValidationError — ошибки ввода (где применимо)

3. Глобальные правила

- Контент-типы
    - Запросы/ответы по умолчанию: application/json.
    - Экспорт списка покупок: application/pdf или text/plain (бинарный контент)

- Пагинация:
    - Параметры запроса: page, limit
    - Формат ответа: объект с полями count, next, previous, results

- Фильтры/поиск:
    - Рецепты (GET /api/recipes/): is_favorited, is_in_shopping_cart, author(id), tags(slug)
    - Ингредиенты (GET /api/ingredients/): name (префиксный поиск)

- Ошибки:
    - 400 ValidationError | NestedValidationError — поля с массивами сообщений
    - 401 AuthenticationError — { "detail": "..." }
    - 403 PermissionDenied — { "detail": "..." }
    - 404 NotFound — { "detail": "..." }
    - 422 ValidationError - { "detail": "..." }

4. Сводка эндпоинтов (таблица)

## Пользователи

| Метод | Путь | Назначение | Auth | Query | Тело запроса | Успешный ответ |
|-------|------|------------|------|-------|--------------|----------------|
| GET   | /api/users/ | Список пользователей | нет | page, limit | — | 200: список User |
| POST  | /api/users/ | Регистрация | нет | — | CustomUserCreate | 201: User |
| GET   | /api/users/{id}/ | Профиль пользователя | нет | id | — | 200: User |
| GET   | /api/users/me/ | Текущий пользователь | да | — | — | 200: User |
| POST  | /api/users/set_password/ | Изменение пароля | да | — | SetPassword | 204: пусто |

---

## Рецепты

| Метод | Путь | Назначение | Auth | Query | Тело запроса | Успешный ответ |
|-------|------|------------|------|-------|--------------|----------------|
| GET   | /api/recipes/ | Список рецептов | нет | page, limit, is_favorited, is_in_shopping_cart, author, tags | — | 200: список RecipeList |
| POST  | /api/recipes/ | Создание рецепта | да | — | RecipeCreateUpdate | 201: RecipeList |
| GET   | /api/recipes/{id}/ | Получение рецепта | нет | id | — | 200: RecipeList |
| PATCH | /api/recipes/{id}/ | Обновление рецепта (только автор) | да | id | RecipeCreateUpdate | 200: RecipeList |
| DELETE| /api/recipes/{id}/ | Удаление рецепта (только автор) | да | id | — | 204: пусто |
| POST  | /api/recipes/{id}/favorite/ | Добавить в избранное | да | id | — | 201: RecipeMinified |
| DELETE| /api/recipes/{id}/favorite/ | Удалить из избранного | да | id | — | 204: пусто |
| POST  | /api/recipes/{id}/shopping_cart/ | Добавить в корзину | да | id | — | 201: RecipeMinified |
| DELETE| /api/recipes/{id}/shopping_cart/ | Удалить из корзины | да | id | — | 204: пусто |
| GET   | /api/recipes/download_shopping_cart/ | Скачать список покупок (TXT/PDF/CSV) | да | — | — | 200: файл |

---

## Подписки

| Метод | Путь | Назначение | Auth | Query | Тело запроса | Успешный ответ |
|-------|------|------------|------|-------|--------------|----------------|
| GET   | /api/users/subscriptions/ | Мои подписки с рецептами | да | page, limit, recipes_limit | — | 200: список UserWithRecipes |
| POST  | /api/users/{id}/subscribe/ | Подписаться на пользователя | да | id, recipes_limit | — | 201: UserWithRecipes |
| DELETE| /api/users/{id}/subscribe/ | Отписаться от пользователя | да | id | — | 204: пусто |

---

## Теги

| Метод | Путь | Назначение | Auth | Query | Тело запроса | Успешный ответ |
|-------|------|------------|------|-------|--------------|----------------|
| GET   | /api/tags/ | Список тегов | нет | — | — | 200: Tag[] |
| GET   | /api/tags/{id}/ | Получение тега | нет | id | — | 200: Tag |

---

## Ингредиенты

| Метод | Путь | Назначение | Auth | Query | Тело запроса | Успешный ответ |
|-------|------|------------|------|-------|--------------|----------------|
| GET   | /api/ingredients/ | Список ингредиентов | нет | name | — | 200: Ingredient[] |
| GET   | /api/ingredients/{id}/ | Получение ингредиента | нет | id | — | 200: Ingredient |

---

## Список покупок

| Метод | Путь | Назначение | Auth | Query | Тело запроса | Успешный ответ |
|-------|------|------------|------|-------|--------------|----------------|
| GET   | /api/recipes/download_shopping_cart/ | Скачать список покупок | да | — | — | 200: файл |
| POST  | /api/recipes/{id}/shopping_cart/ | Добавить рецепт в корзину | да | id | — | 201: RecipeMinified |
| DELETE| /api/recipes/{id}/shopping_cart/ | Удалить рецепт из корзины | да | id | — | 204: пусто |

---

## Аутентификация

| Метод | Путь | Назначение | Auth | Query | Тело запроса | Успешный ответ |
|-------|------|------------|------|-------|--------------|----------------|
| POST  | /api/auth/token/login/ | Получить токен | нет | — | TokenCreate | 201: TokenGetResponse |
| POST  | /api/auth/token/logout/ | Удаление токена | да | — | — | 204: пусто |


5. Файлы/медиа:
- Картинка рецепта (ввод): поле image в RecipeCreateUpdate — data URL (Base64)
- Картинка рецепта (вывод): поле image в RecipeList — абсолютный URI к файлу на сервере CDN/статике
- Экспорт списка покупок: GET /api/recipes/download_shopping_cart/ → application/pdf или text/plain (binary)

6. Политика изменений

- Что считаем “ломающим изменением”:
    - Изменение путей/методов, статусов, обязательных полей, типов данных
    - Удаление полей в ответах/запросах, изменение семантики фильтров
    - Изменение формата аутентификации или заголовка Authorization
- "Неломающие изменения":
    - Добавление необязательных полей к схемам
    - Добавление новых эндпоинтов/фильтров, не влияющих на текущие

- каждое расхождение документируется в contract_deltas.md (дата, описание, обоснование)