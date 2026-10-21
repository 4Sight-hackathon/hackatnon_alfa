# Состояния кредитной заявки

```mermaid
stateDiagram-v2
    [*] --> DRAFT
    DRAFT --> SUBMITTED: клиент отправил анкету
    DRAFT --> CANCELLED: клиент отменил
    SUBMITTED --> VALIDATING
    VALIDATING --> NEEDS_INFORMATION: не хватает данных
    NEEDS_INFORMATION --> SUBMITTED: данные дополнены
    VALIDATING --> SCORING: данные корректны
    SCORING --> OFFERED: низкий риск
    SCORING --> MANUAL_REVIEW: пограничный риск
    SCORING --> DECLINED: высокий риск
    MANUAL_REVIEW --> NEEDS_INFORMATION
    MANUAL_REVIEW --> OFFERED
    MANUAL_REVIEW --> DECLINED
    OFFERED --> ACCEPTED: клиент принял условия
    OFFERED --> CANCELLED: клиент отказался
    ACCEPTED --> [*]
    DECLINED --> [*]
    CANCELLED --> [*]
```

В первой версии API реализованы основной автоматический путь и принятие оффера. `NEEDS_INFORMATION`, `CANCELLED` и решение андеррайтера зафиксированы в модели, но их UI/API-команды — следующая итерация.

Каждый переход сохраняет `from_status`, `to_status`, `actor`, `reason`, `created_at`.

