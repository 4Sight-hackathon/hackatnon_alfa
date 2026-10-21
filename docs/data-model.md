# Модель данных

```mermaid
erDiagram
    CREDIT_APPLICATION ||--o{ APPLICATION_STATUS_HISTORY : has
    CREDIT_APPLICATION {
        uuid id PK
        string product_code
        string company_name
        string inn
        decimal requested_amount
        int term_months
        string purpose
        decimal annual_revenue
        decimal monthly_debt_payments
        int years_in_business
        bool has_overdue_debt
        string contact_name
        string contact_email
        enum status
        int risk_score
        string decision_reason
        decimal approved_amount
        int approved_term_months
        decimal annual_rate
        datetime created_at
        datetime updated_at
    }
    APPLICATION_STATUS_HISTORY {
        uuid id PK
        uuid application_id FK
        enum from_status
        enum to_status
        string actor
        string reason
        datetime created_at
    }
```

Денежные поля хранятся как `NUMERIC`, а не float. UUID не раскрывает порядок создания заявок. История статусов append-only на уровне приложения.

Перед продакшеном нужно вынести PII в отдельный защищённый контур, добавить клиента/организацию как самостоятельные сущности и установить сроки хранения.

