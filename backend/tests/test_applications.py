from fastapi.testclient import TestClient


def payload(**overrides):
    data = {
        "product_code": "WORKING_CAPITAL",
        "company_name": "ООО Будущее дело",
        "inn": "7707083893",
        "requested_amount": 2_000_000,
        "term_months": 12,
        "purpose": "Закупка товара",
        "annual_revenue": 18_000_000,
        "monthly_debt_payments": 120_000,
        "years_in_business": 4,
        "has_overdue_debt": False,
        "contact_name": "Анна Иванова",
        "contact_email": "demo@example.ru",
    }
    data.update(overrides)
    return data


def create_and_submit(client: TestClient, data: dict):
    created = client.post("/api/v1/applications", json=data)
    assert created.status_code == 201, created.text
    application_id = created.json()["id"]
    submitted = client.post(f"/api/v1/applications/{application_id}/submit")
    assert submitted.status_code == 200, submitted.text
    return submitted.json()


def test_happy_path_creates_offer_and_accepts_it(client: TestClient):
    result = create_and_submit(client, payload())

    assert result["status"] == "OFFERED"
    assert result["approved_amount"] == "2000000.00"
    assert 0 <= result["risk_score"] < 45
    assert [event["to_status"] for event in result["status_history"]] == [
        "DRAFT",
        "SUBMITTED",
        "VALIDATING",
        "SCORING",
        "OFFERED",
    ]

    accepted = client.post(f"/api/v1/applications/{result['id']}/accept")
    assert accepted.status_code == 200
    assert accepted.json()["status"] == "ACCEPTED"


def test_borderline_case_goes_to_manual_review(client: TestClient):
    result = create_and_submit(
        client,
        payload(requested_amount=6_000_000, annual_revenue=10_000_000),
    )
    assert result["status"] == "MANUAL_REVIEW"
    assert result["risk_score"] >= 45


def test_overdue_debt_is_declined(client: TestClient):
    result = create_and_submit(client, payload(has_overdue_debt=True))
    assert result["status"] == "DECLINED"
    assert result["risk_score"] == 95


def test_invalid_inn_is_rejected(client: TestClient):
    response = client.post("/api/v1/applications", json=payload(inn="123"))
    assert response.status_code == 422
