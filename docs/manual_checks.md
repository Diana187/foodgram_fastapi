# manual_checks.md

## Чек-лист ручных проверок (Bruno)

### Аутентификация
- [ ] POST `/auth/token/login/` → 200, вернуть `auth_token`
- [ ] GET `/users/me/` с токеном → 200
- [ ] POST `/auth/token/logout/` → 204; без токена → 401

### Пользователи / Подписки
- [ ] POST `/users/` → 201 (новый пользователь)
- [ ] POST `/users/{id}/subscribe/` → 201; повторно → 400; на себя → 400
- [ ] GET `/users/subscriptions/?recipes_limit=3` → 200, ≤3 рецепта
- [ ] DELETE `/users/{id}/subscribe/` → 204; если нет подписки → 400

### Ингредиенты
- [ ] GET `/ingredients/?name={{ingredient_query}}` → 200, поиск по началу имени

### Теги
- [ ] GET `/tags/` → 200, список тегов

### Рецепты — фильтры и пагинация
- [ ] GET `/recipes/?page=1&limit=6` → 200, ≤6 результатов
- [ ] GET `/recipes/?tags={{tag_slug1}}&tags={{tag_slug2}}` → 200, только указанные теги
- [ ] GET `/recipes/?author={{author_id}}` → 200, рецепты автора
- [ ] GET `/recipes/?is_favorited=1` → 200, только избранные
- [ ] GET `/recipes/?is_in_shopping_cart=true` → 200, только корзина

### Рецепты — CRUD
- [ ] POST `/recipes/` (валидный JSON) → 201, сохранить `recipe_id`
- [ ] POST `/recipes/` без тегов/ингредиентов → 400
- [ ] PATCH `/recipes/{{recipe_id}}/` → 200 (автор), 403 (чужой)
- [ ] DELETE `/recipes/{{recipe_id}}/` → 204 (автор), 403 (чужой)
- [ ] GET `/recipes/{{recipe_id}}/` → 200, корректные поля

### Избранное / Корзина
- [ ] POST `/recipes/{{recipe_id}}/favorite/` → 201; повторно → 400
- [ ] DELETE `/recipes/{{recipe_id}}/favorite/` → 204; если нет → 400
- [ ] POST `/recipes/{{recipe_id}}/shopping_cart/` → 201; повторно → 400
- [ ] DELETE `/recipes/{{recipe_id}}/shopping_cart/` → 204; если нет → 400

### Экспорт списка покупок
- [ ] GET `/recipes/download_shopping_cart/` → 200, файл `shopping_list.txt`
- [ ] GET `/recipes/download_shopping_cart/` при пустой корзине → 400

### Медиа
- [ ] POST `/recipes/` с base64-image → 201, `image` возвращается
- [ ] POST `/recipes/` с multipart-image → 201; неверный формат → 422

### Ошибки и статусы
- [ ] Без токена → 401
- [ ] Доступ к чужому объекту → 403
- [ ] Объект не найден → 404
- [ ] Ошибка валидации → 400
- [ ] Неверный метод → 405
