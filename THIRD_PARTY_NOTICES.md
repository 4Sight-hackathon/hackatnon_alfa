# Third-party notices

Проект использует открытые компоненты. Точные транзитивные версии см. в `frontend/pnpm-lock.yaml`.

| Компонент | Версия | Лицензия | Назначение |
| --- | --- | --- | --- |
| React / React DOM | 19.1.0 | MIT | Web UI |
| Vite | 6.3.5 | MIT | Сборка frontend |
| TypeScript | 5.8.3 | Apache-2.0 | Типизация frontend |
| FastAPI | 0.115.12 | MIT | HTTP API |
| SQLAlchemy | 2.0.41 | MIT | ORM |
| Alembic | 1.16.1 | MIT | Миграции |
| Pydantic Settings | 2.9.1 | MIT | Конфигурация |
| Uvicorn | 0.34.3 | BSD-3-Clause | ASGI server |
| psycopg | 3.2.9 | LGPL-3.0 | PostgreSQL driver |
| PostgreSQL image | 17.5-alpine | PostgreSQL License | База данных |
| nginx image | 1.28.0-alpine | BSD-2-Clause | Статика и reverse proxy |
| Python image | 3.12.10-slim | PSF | Backend runtime |
| Node.js image | 22.16.0-alpine | MIT | Frontend build runtime |

## Модели, датасеты и сервисы

- ML/LLM-модели и внешние датасеты не используются.
- Данные клиента и компании синтетические.
- Проверки ЕГРЮЛ/ЕГРИП, ФНС, БКИ, АБС, электронная подпись и выдача не вызывают реальные сервисы и явно смоделированы.

