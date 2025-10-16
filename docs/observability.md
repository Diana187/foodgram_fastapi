# observability.md

## Цель
Настроить наблюдаемость: структурированные логи, единый `request_id` и health-check эндпоинты для FastAPI.

---

## Логирование
- Формат логов: **JSON**, вывод в **stdout**.
- Уровни: `DEBUG` (dev), `INFO` (prod), `ERROR` (ошибки).
- Основные поля: `ts`, `lvl`, `msg`, `request_id`, `method`, `path`, `status`, `latency_ms`.

### Пример лога
```json
{
  "ts": "2025-10-15T12:00:01Z",
  "lvl": "INFO",
  "msg": "request completed",
  "request_id": "d4d7e3f
