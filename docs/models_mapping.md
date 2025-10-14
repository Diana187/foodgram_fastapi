# models_mapping.md

## Цель
Зафиксировать, как Django-модели и их ограничения переносятся в SQLAlchemy 2.0 (async), без ломки API-контракта.

## Конвенции (кратко)
- Имена таблиц/колонок — `snake_case`.
- Ключи/индексы: `pk_<table>`, `fk_<table>__<col>__<reftable>`, `uq_<table>__...`, `ix_<table>__<col>`, `ck_<table>__<name>`.
- Даты/время: `TIMESTAMP(timezone=True)`, UTC, `server_default=now()`, `onupdate=now()`.
- Загрузки: коллекции — `selectinload`.

---

## Ingredient  → SA: `ingredient`
**PK:** `id BIGINT SERIAL`  
**Поля:**
- `name: VARCHAR(200) NOT NULL` (`db_index=True`)
- `measurement_unit: VARCHAR(200) NOT NULL`
- `created: TIMESTAMPTZ NOT NULL DEFAULT now()`
- `updated: TIMESTAMPTZ NOT NULL DEFAULT now() ON UPDATE now()`

**Ограничения/индексы:**
- `Index ix_ingredient__name (name)`
- (при необходимости) частичные индексы не требуются.

**Отношения:**
- M2M с `recipe` через `recipe_ingredient_amount` (см. ниже).

**Отличия от Django:**
- семантика `auto_now/auto_now_add` реализуется через server default/onupdate.

---

## Tag  → SA: `tag`
**PK:** `id BIGINT SERIAL`  
**Поля:**
- `name: VARCHAR(200) NOT NULL UNIQUE` (`db_index=True`)
- `color: VARCHAR(7) NOT NULL UNIQUE`  *(HEX, формат не проверяется на уровне БД — проверка в схеме/валидаторе)*  
- `slug: VARCHAR(?) NOT NULL UNIQUE` *(длина как в Django SlugField — обычно 50/200; возьмём 200 для совместимости)*
- `created: TIMESTAMPTZ NOT NULL DEFAULT now()`
- `updated: TIMESTAMPTZ NOT NULL DEFAULT now() ON UPDATE now()`

**Ограничения/индексы:**
- `uq_tag__name`, `uq_tag__color`, `uq_tag__slug`
- `Index ix_tag__name (name)`

**Отношения:**
- M2M с `recipe` через связующую таблицу `recipe_tag` (см. ниже).

---

## Recipe  → SA: `recipe`
**PK:** `id BIGINT SERIAL`  
**Поля:**
- `author_id: BIGINT NOT NULL` → FK `user.id` `ondelete='CASCADE'`
- `name: VARCHAR(200) NOT NULL`
- `image: VARCHAR(?) NULL` *(путь/URL, как `ImageField`; `default=None`)*
- `text: TEXT NOT NULL` *(max_length=500 в Django — ограничение прикладного уровня)*
- `cooking_time: SMALLINT NOT NULL CHECK (cooking_time >= 1)`
- `pub_date: TIMESTAMPTZ NOT NULL DEFAULT now()` (`db_index=True`)
- `created: TIMESTAMPTZ NOT NULL DEFAULT now()`
- `updated: TIMESTAMPTZ NOT NULL DEFAULT now() ON UPDATE now()`

**Ограничения/индексы:**
- `Index ix_recipe__pub_date (pub_date)`
- при необходимости: `Index ix_recipe__author_id (author_id)`

**Отношения:**
- N:1 `author` → `user` (`ondelete='CASCADE'`)
- M2M `ingredients` через `recipe_ingredient_amount` (с атрибутом `amount`)
- M2M `tags` через `recipe_tag`

**Отличия от Django:**
- `TextField(max_length=500)` не ограничивается БД (валидируем в схеме).

---

## RecipeIngredientAmount (through)  → SA: `recipe_ingredient_amount`
**Роль:** связующая таблица M2M `recipe` ↔ `ingredient` с атрибутом `amount`.

**PK:** `id BIGINT SERIAL`  
**Поля:**
- `ingredient_id: BIGINT NOT NULL` → FK `ingredient.id` `ondelete='CASCADE'`
- `recipe_id: BIGINT NOT NULL` → FK `recipe.id` `ondelete='CASCADE'`
- `amount: SMALLINT NOT NULL CHECK (amount >= 1)`

**Ограничения/индексы:**
- `UniqueConstraint(recipe_id, ingredient_id, name='uq_recipe_ingredient_amount__recipe__ingredient')`
- `Index ix_recipe_ingredient_amount__ingredient_id (ingredient_id)`
- `Index ix_recipe_ingredient_amount__recipe_id (recipe_id)`

**Отношения:**
- `recipe` (M:1), `ingredient` (M:1)
- В Django `related_name='ingredienttorecipe'` — в SA внутреннее имя можем нормализовать (не влияет на контракт API).

---

## Связующая таблица тегов  → SA: `recipe_tag`
*(в Django `ManyToManyField(Tag)` без `through`)*
**Поля:**
- `recipe_id: BIGINT NOT NULL` → FK `recipe.id` `ondelete='CASCADE'`
- `tag_id: BIGINT NOT NULL` → FK `tag.id` `ondelete='CASCADE'`

**Ограничения/индексы:**
- `UniqueConstraint(recipe_id, tag_id, name='uq_recipe_tag__recipe__tag')`
- `Index ix_recipe_tag__tag_id (tag_id)`
- `Index ix_recipe_tag__recipe_id (recipe_id)`

---

## Favorite  → SA: `favorite`
**PK:** `id BIGINT SERIAL`  
**Поля:**
- `user_id: BIGINT NOT NULL` → FK `user.id` `ondelete='CASCADE'`
- `recipe_id: BIGINT NOT NULL` → FK `recipe.id` `ondelete='CASCADE'`

**Ограничения/индексы:**
- `UniqueConstraint(user_id, recipe_id, name='favorite_recipe_user_unique')` *(сохраняем имя из абстрактной базы Django)*
- `Index ix_favorite__user_id (user_id)`
- `Index ix_favorite__recipe_id (recipe_id)`

**Отношения:** N:1 к `user`, N:1 к `recipe`.

---

## ShoppingCart  → SA: `shopping_cart`
**PK:** `id BIGINT SERIAL`  
**Поля:**
- `user_id: BIGINT NOT NULL` → FK `user.id` `ondelete='CASCADE'`
- `recipe_id: BIGINT NOT NULL` → FK `recipe.id` `ondelete='CASCADE'`

**Ограничения/индексы:**
- `UniqueConstraint(user_id, recipe_id, name='shoppingcart_recipe_user_unique')`
- `Index ix_shopping_cart__user_id (user_id)`
- `Index ix_shopping_cart__recipe_id (recipe_id)`

**Отношения:** N:1 к `user`, N:1 к `recipe`.

---

## User  → SA: `user`
**PK:** `id BIGINT SERIAL`  
**Поля:**
- `first_name: VARCHAR(200) NULL`
- `last_name: VARCHAR(200) NULL`
- `username: VARCHAR(200) NOT NULL UNIQUE`
- `email: VARCHAR(200) NOT NULL UNIQUE`

**Ограничения/индексы:**
- `uq_user__username`, `uq_user__email`
- (опц.) индексы по поиску: `ix_user__username`, `ix_user__email`

**Отношения:**
- 1:N `recipes` (автор)

---

## Follow  → SA: `follow`
**PK:** `id BIGINT SERIAL`  
**Поля:**
- `user_id: BIGINT NOT NULL` → FK `user.id` `ondelete='CASCADE'`  *(подписчик)*
- `following_id: BIGINT NOT NULL` → FK `user.id` `ondelete='CASCADE'`  *(автор/кем подписан)*

**Ограничения/индексы:**
- `UniqueConstraint(user_id, following_id, name='unique_followers')`
- `CheckConstraint(user_id <> following_id, name='ck_follow__no_self_follow')` *(перенос `clean()` из Django на уровень БД + дублируем в бизнес-логике)*
- `Index ix_follow__user_id (user_id)`
- `Index ix_follow__following_id (following_id)`

**Отношения:**
- обе стороны N:1 к `user`.

---

## Заметки по Alembic (минимум)
1) **Миграция #001 (база):** `user`, `ingredient`, `tag`.  
2) **Миграция #002:** `recipe` (FK → `user`), `recipe_ingredient_amount` (FK → `recipe`,`ingredient`), `recipe_tag`.  
3) **Миграция #003:** `favorite`, `shopping_cart`, `follow`.  
4) **Сиды:** загрузить `ingredient` из `data/ingredients.json` после миграции #001 (скрипт/команда).  
5) **Индексы/чек-констрейнты:** включены в соответствующие миграции; для `updated` можно добавить `ON UPDATE` через триггер/генерируемую колонку, либо обновлять на уровне приложения (решение за проектом).

---
