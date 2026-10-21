import enum
import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Numeric, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ApplicationStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    VALIDATING = "VALIDATING"
    SCORING = "SCORING"
    NEEDS_INFORMATION = "NEEDS_INFORMATION"
    MANUAL_REVIEW = "MANUAL_REVIEW"
    OFFERED = "OFFERED"
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"
    CANCELLED = "CANCELLED"


status_enum = Enum(ApplicationStatus, name="application_status", native_enum=False)


class CreditApplication(Base):
    __tablename__ = "credit_applications"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    product_code: Mapped[str] = mapped_column(String(40), nullable=False)
    company_name: Mapped[str] = mapped_column(String(200), nullable=False)
    inn: Mapped[str] = mapped_column(String(12), nullable=False, index=True)
    requested_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    term_months: Mapped[int] = mapped_column(nullable=False)
    purpose: Mapped[str] = mapped_column(String(80), nullable=False)
    annual_revenue: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    monthly_debt_payments: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    years_in_business: Mapped[int] = mapped_column(nullable=False)
    has_overdue_debt: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    contact_name: Mapped[str] = mapped_column(String(160), nullable=False)
    contact_email: Mapped[str] = mapped_column(String(254), nullable=False)
    status: Mapped[ApplicationStatus] = mapped_column(
        status_enum, nullable=False, default=ApplicationStatus.DRAFT, index=True
    )
    risk_score: Mapped[int | None] = mapped_column(nullable=True)
    decision_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    approved_amount: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    approved_term_months: Mapped[int | None] = mapped_column(nullable=True)
    annual_rate: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now
    )

    status_history: Mapped[list["ApplicationStatusHistory"]] = relationship(
        back_populates="application",
        cascade="all, delete-orphan",
        order_by="ApplicationStatusHistory.created_at",
    )


class ApplicationStatusHistory(Base):
    __tablename__ = "application_status_history"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    application_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("credit_applications.id", ondelete="CASCADE"), nullable=False, index=True
    )
    from_status: Mapped[ApplicationStatus | None] = mapped_column(status_enum, nullable=True)
    to_status: Mapped[ApplicationStatus] = mapped_column(status_enum, nullable=False)
    actor: Mapped[str] = mapped_column(String(40), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    application: Mapped[CreditApplication] = relationship(back_populates="status_history")
