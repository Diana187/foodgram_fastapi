# permissions.md

## Цель
Зафиксировать правила доступа (кто что может) для всех эндпоинтов. Используется при миграции на FastAPI для сохранения контракта.

---

## Глобальные правила
- DRF: `DEFAULT_PERMISSION_CLASSES = IsAuthenticated` (всё закрыто по умолчанию).
- Открытые ресурсы и исключения задаются у вьюсетов/экшенов.
- Объектный уровень: `IsAuthorOrReadOnly` — изменять/удалять объект может только автор.

**Приоритет**: `@action(permission_classes=...)` > `permission_classes` на вьюсете > глобальные настройки.

**Роли**:
- **Anonymous** — неавторизованный.
- **User** — авторизованный.
- **Admin/Staff** — права в админке; в API отдельной матрицы нет.

---

## Матрица доступа по ресурсам

### Auth / Users (Djoser + кастомный UserViewSet)
| Метод | Путь | Доступ | Примечание |
|---:|---|---|---|
| POST | `/api/auth/token/login/` | Anonymous | вход (email + password), ответ `{"auth_token": "..."}`
| POST | `/api/auth/token/logout/` | User | выход (инвалидация токена)
| POST | `/api/users/` | Anonymous | регистрация
| GET | `/api/users/` | Anonymous | список (DJOSER + `HIDE_USERS=False`)
| GET | `/api/users/{id}/` | Anonymous | детали пользователя
| GET | `/api/users/me/` | User | **@action** `IsAuthenticated`
| GET | `/api/users/subscriptions/` | User | **@action** `IsAuthenticated`, пагинация, `recipes_limit`
| POST | `/api/users/{id}/subscribe/` | User | **@action** `IsAuthenticated`, запрет самоподписки/дубликатов
| DELETE | `/api/users/{id}/subscribe/` | User | **@action** `IsAuthenticated`, 400 если подписки нет

### Ingredients
| Метод | Путь | Доступ | Примечание |
|---:|---|---|---|
| GET | `/api/ingredients/` | Anonymous | ReadOnlyModelViewSet + `IsAuthenticatedOrReadOnly`, поиск `^name`
| GET | `/api/ingredients/{id}/` | Anonymous | деталь

### Tags
| Метод | Путь | Доступ | Примечание |
|---:|---|---|---|
| GET | `/api/tags/` | Anonymous | `IsAuthenticatedOrReadOnly`
| GET | `/api/tags/{id}/` | Anonymous | деталь
| POST/PUT/PATCH/DELETE | `/api/tags/*` | User | запись доступна авторизованным

### Recipes
| Метод | Путь | Доступ | Примечание |
|---:|---|---|---|
| GET | `/api/recipes/` | Anonymous | список, фильтры: `is_favorited`, `is_in_shopping_cart`, `tags`
| GET | `/api/recipes/{id}/` | Anonymous | деталь
| POST | `/api/recipes/` | User | создать рецепт
| PUT/PATCH/DELETE | `/api/recipes/{id}/` | Только автор | `IsAuthorOrReadOnly` (объектные права)
| POST | `/api/recipes/{id}/favorite/` | User | **@action** `IsAuthenticated`, защита от дублей
| DELETE | `/api/recipes/{id}/favorite/` | User | удалить из избранного
| POST | `/api/recipes/{id}/shopping_cart/` | User | **@action** `IsAuthenticated`, защита от дублей
| DELETE | `/api/recipes/{id}/shopping_cart/` | User | удалить из корзины
| GET | `/api/recipes/download_shopping_cart/` | User | **@action** `IsAuthenticated`, 400 если корзина пуста

---

## Объектные права
- **IsAuthorOrReadOnly**  
  - `SAFE_METHODS` (GET/HEAD/OPTIONS) → доступны всем.  
  - `POST/PUT/PATCH/DELETE` → только если `object.author == request.user`.

---

## Бизнес-валидации, влияющие на доступ
> Реализованы в сериализаторах/вьюсетах, возвращают 400.
- **Подписки**:  
  - нельзя подписаться на себя;  
  - нельзя подписаться повторно;  
  - при отписке — 400, если подписки нет.
- **Избранное/Корзина**:  
  - при добавлении — запрет дубликатов;  
  - при удалении — 400, если записи нет.
- **Список покупок (скачать)**: 400, если корзина пустая.

---

## Коды ошибок (основные)
- `401 Unauthorized` — нет/неверный токен.
- `403 Forbidden` — нарушение объектных прав (не автор).
- `400 Bad Request` — бизнес-ограничения (дубликаты, самоподписка, пустая корзина и т.п.).
- `404 Not Found` — объект не найден.
- `405 Method Not Allowed` — неразрешённый метод на экшене.

---

## Соответствие FastAPI (для миграции)
- Сохранить те же пути и экшены.
- Реализовать аналог `IsAuthorOrReadOnly` (объектный уровень).
- Для публичных ресурсов — эквивалент `IsAuthenticatedOrReadOnly`.
- Для защищённых экшенов — требовать аутентификацию.
- Сохранить семантику бизнес-ошибок и коды статусов.

---

## Чек-лист ручных тестов
- Anonymous:
  - ✅ GET `/tags/`, `/ingredients/`, `/recipes/`  
  - ❌ POST `/recipes/`, GET `/users/me/`, `subscribe/`, `favorite/`, `shopping_cart/`
- User:
  - ✅ Создание/правка/удаление *своих* рецептов; ❌ правка чужих.
  - ✅ Подписаться/отписаться (+ верные ошибки на дубликаты/самоподписку).
  - ✅ Добавить/удалить в избранное/корзину (+ верные ошибки).
  - ✅ Скачать список покупок (и 400 при пустой корзине).
