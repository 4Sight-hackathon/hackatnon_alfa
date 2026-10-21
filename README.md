# Умный кредитный кабинет предпринимателя

MVP цифрового кредитного конвейера для малого и микробизнеса. Прототип связывает клиентскую анкету, внутренние проверки, прозрачный скоринг и итоговое решение в один воспроизводимый сценарий.

> Важно: это хакатон-прототип. Все данные, проверки, скоринг и офферы синтетические и не являются реальным кредитным решением банка.

## Что уже работает

- веб-анкета для кредита на оборотные средства;
- создание и сохранение заявки в PostgreSQL;
- переходы `DRAFT → SUBMITTED → VALIDATING → SCORING → result`;
- три исхода: оффер, ручная проверка, отказ;
- понятное объяснение решения и история статусов;
- принятие оффера со смоделированными подписанием и выдачей;
- OpenAPI/Swagger на `/docs` и коллекция Postman;
- единый запуск React + FastAPI + PostgreSQL через Docker Compose.

## Быстрый запуск

Нужен Docker с Compose. Платные API или доступ к системам банка не требуются.

```bash
cp .env.example .env
docker compose up --build
```

Дождитесь healthy-статуса сервисов, затем откройте:

- интерфейс: <http://localhost:8080>;
- Swagger UI: <http://localhost:8000/docs>.

Для остановки:

```bash
docker compose down
```

Чтобы удалить также локальные демо-данные, используйте `docker compose down -v`.

## Демо-сценарий

1. Откройте <http://localhost:8080>.
2. Оставьте предзаполненные синтетические данные.
3. Нажмите **Получить решение**.
4. Убедитесь, что появились оффер и история всех этапов.
5. Нажмите **Принять условия** и убедитесь, что статус сменился.

Другие ветки: поставьте сумму 6 млн ₽ при выручке 10 млн ₽ для ручной проверки или отметьте текущую просрочку для отказа.

## Архитектура

```text
Браузер → nginx / React → FastAPI → SQLAlchemy → PostgreSQL
                              ├─ валидация
                              ├─ симулятор внешних проверок
                              └─ rule-based decision engine
```

Состав монорепозитория:

- `frontend/` — React 19 + TypeScript + Vite, статика отдаётся nginx;
- `backend/` — FastAPI, SQLAlchemy, Alembic и прозрачный decision engine;
- `docs/` — схемы, модель данных, статусы, API и тест-сценарии;
- `docker-compose.yml` — воспроизводимый локальный стенд.

Подробнее: [архитектура](docs/architecture.md), [статусы](docs/application-state-machine.md), [модель данных](docs/data-model.md), [API](docs/api.md), [тесты](docs/test-scenarios.md), [границы MVP](docs/product-scope.md).

## Локальная разработка

Backend требует Python 3.12:

```bash
cd backend
python3.12 -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Frontend требует Node.js 22 и pnpm 11.25.0:

```bash
cd frontend
corepack enable
pnpm install --frozen-lockfile
pnpm dev
```

## Проверки

```bash
cd backend
.venv/bin/pytest -q
.venv/bin/ruff check app tests

cd ../frontend
pnpm run check
pnpm run build
```

API-тесты покрывают оффер, ручную проверку, отказ и ошибку ИНН.

## Конфигурация

| Переменная | Назначение | Значение в Compose |
| --- | --- | --- |
| `POSTGRES_DB` | База PostgreSQL | `credit_cabinet` |
| `POSTGRES_USER` | Пользователь БД | `credit_app` |
| `POSTGRES_PASSWORD` | Локальный пароль БД | `credit_app_local` |
| `DATABASE_URL` | SQLAlchemy URL | связь с Compose PostgreSQL |
| `CORS_ORIGINS` | Разрешённые origin | localhost 5173 и 8080 |
| `VITE_API_URL` | Базовый URL API для UI | `/api/v1` |

## Осознанные ограничения MVP

- Аутентификация, RBAC, шифрование полей и audit trail администратора ещё не реализованы.
- ЕГРЮЛ/ЕГРИП, БКИ, АБС, подписание и выдача смоделированы.
- Скоринг — объяснимые демо-правила, не банковсая модель.
- Автоматическая обработка синхронная; следующий шаг — очередь с идемпотентными worker-ами.
