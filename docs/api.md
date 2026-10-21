# API

Актуальный контракт генерирует FastAPI: `/openapi.json`, интерактивная документация — `/docs`.

| Метод | URL | Назначение |
| --- | --- | --- |
| `GET` | `/health` | Liveness probe |
| `GET` | `/api/v1/products` | Каталог доступных продуктов |
| `POST` | `/api/v1/applications` | Создать черновик |
| `GET` | `/api/v1/applications/{id}` | Получить заявку и историю |
| `POST` | `/api/v1/applications/{id}/submit` | Отправить и запустить решение |
| `POST` | `/api/v1/applications/{id}/accept` | Принять оффер |

Коды ошибок: `422` — некорректные данные, `404` — заявка не найдена, `409` — команда недопустима в текущем статусе.

В `postman_collection.json` первый запрос сохраняет `application_id`, поэтому запросы можно запускать по порядку.

