import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models import ApplicationStatus


class Product(BaseModel):
    code: str
    name: str
    description: str
    min_amount: int
    max_amount: int
    min_term_months: int
    max_term_months: int


class ApplicationCreate(BaseModel):
    product_code: str = "WORKING_CAPITAL"
    company_name: str = Field(min_length=2, max_length=200)
    inn: str
    requested_amount: Decimal = Field(ge=100_000, le=30_000_000)
    term_months: int = Field(ge=3, le=36)
    purpose: str = Field(min_length=2, max_length=80)
    annual_revenue: Decimal = Field(gt=0, le=5_000_000_000)
    monthly_debt_payments: Decimal = Field(ge=0, le=100_000_000)
    years_in_business: int = Field(ge=0, le=100)
    has_overdue_debt: bool = False
    contact_name: str = Field(min_length=2, max_length=160)
    contact_email: EmailStr

    @field_validator("inn")
    @classmethod
    def validate_inn(cls, value: str) -> str:
        if not value.isdigit() or len(value) not in (10, 12):
            raise ValueError("ИНН должен состоять из 10 или 12 цифр")
        return value


class StatusEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    from_status: ApplicationStatus | None
    to_status: ApplicationStatus
    actor: str
    reason: str
    created_at: datetime


class ApplicationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    product_code: str
    company_name: str
    inn: str
    requested_amount: Decimal
    term_months: int
    purpose: str
    annual_revenue: Decimal
    monthly_debt_payments: Decimal
    years_in_business: int
    has_overdue_debt: bool
    contact_name: str
    contact_email: EmailStr
    status: ApplicationStatus
    risk_score: int | None
    decision_reason: str | None
    approved_amount: Decimal | None
    approved_term_months: int | None
    annual_rate: Decimal | None
    created_at: datetime
    updated_at: datetime
    status_history: list[StatusEventRead]
