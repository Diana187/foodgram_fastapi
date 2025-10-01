# routes_map.md — Foodgram (FastAPI)

> Источник истины: **openapi-schema.yml**. Цель: не ломать фронт.

## Структура

* Префикс API: `/api/v1`
* Роутеры: `auth`, `users`, `recipes`, `tags`, `ingredients`, `favorites`, `shopping_cart`, `subscriptions`
* Публичные GET → без авторизации
* POST/DELETE/PATCH → только авторизованные
* Пагинация: `limit` + `offset`

## Маршруты

### Auth

* `POST /auth/token/login` → login
* `POST /auth/token/logout` → logout (auth)

### Users

* `GET /users` → список (auth? см. контракт)
* `GET /users/me` → текущий пользователь (auth)
* `GET /users/{id}` → профиль (публичный)

### Subscriptions

* `GET /users/subscriptions` (auth)
* `POST /users/{id}/subscribe` (auth)
* `DELETE /users/{id}/subscribe` (auth)

### Tags

* `GET /tags`
* `GET /tags/{id}`

### Ingredients

* `GET /ingredients`
* `GET /ingredients/{id}`

### Recipes

* `GET /recipes` (фильтры: author, tags, is_favorited, is_in_shopping_cart)
* `POST /recipes` (auth)
* `GET /recipes/{id}`
* `PATCH /recipes/{id}` (auth + owner/admin)
* `DELETE /recipes/{id}` (auth + owner/admin)

### Favorites

* `POST /recipes/{id}/favorite` (auth)
* `DELETE /recipes/{id}/favorite` (auth)

### Shopping cart

* `GET /recipes/download_shopping_cart` (auth)
* `POST /recipes/{id}/shopping_cart` (auth)
* `DELETE /recipes/{id}/shopping_cart` (auth)

## Подключение

```python
api = APIRouter(prefix="/api/v1")
api.include_router(auth.router, prefix="/auth")
api.include_router(users.router, prefix="/users")
api.include_router(subscriptions.router)
api.include_router(tags.router, prefix="/tags")
api.include_router(ingredients.router, prefix="/ingredients")
api.include_router(recipes.router, prefix="/recipes")
api.include_router(favorites.router)
api.include_router(shopping_cart.router)
app.include_router(api)
```

## Чеклист

* Все пути из `openapi-schema.yml` учтены
* Авторизация отмечена
* Пагинация: limit+offset
