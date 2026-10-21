"""Initial credit application model.

Revision ID: 20261021_0001
Revises:
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20261021_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

statuses = (
    "DRAFT",
    "SUBMITTED",
    "VALIDATING",
    "SCORING",
    "NEEDS_INFORMATION",
    "MANUAL_REVIEW",
    "OFFERED",
    "ACCEPTED",
    "DECLINED",
    "CANCELLED",
)
status_enum = sa.Enum(*statuses, name="application_status", native_enum=False)


def upgrade() -> None:
    op.create_table(
        "credit_applications",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("product_code", sa.String(40), nullable=False),
        sa.Column("company_name", sa.String(200), nullable=False),
        sa.Column("inn", sa.String(12), nullable=False),
        sa.Column("requested_amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("term_months", sa.Integer(), nullable=False),
        sa.Column("purpose", sa.String(80), nullable=False),
        sa.Column("annual_revenue", sa.Numeric(14, 2), nullable=False),
        sa.Column("monthly_debt_payments", sa.Numeric(14, 2), nullable=False),
        sa.Column("years_in_business", sa.Integer(), nullable=False),
        sa.Column("has_overdue_debt", sa.Boolean(), nullable=False),
        sa.Column("contact_name", sa.String(160), nullable=False),
        sa.Column("contact_email", sa.String(254), nullable=False),
        sa.Column("status", status_enum, nullable=False),
        sa.Column("risk_score", sa.Integer(), nullable=True),
        sa.Column("decision_reason", sa.Text(), nullable=True),
        sa.Column("approved_amount", sa.Numeric(14, 2), nullable=True),
        sa.Column("approved_term_months", sa.Integer(), nullable=True),
        sa.Column("annual_rate", sa.Numeric(5, 2), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_credit_applications_inn", "credit_applications", ["inn"])
    op.create_index("ix_credit_applications_status", "credit_applications", ["status"])
    op.create_table(
        "application_status_history",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("application_id", sa.Uuid(), nullable=False),
        sa.Column("from_status", status_enum, nullable=True),
        sa.Column("to_status", status_enum, nullable=False),
        sa.Column("actor", sa.String(40), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["application_id"], ["credit_applications.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_application_status_history_application_id",
        "application_status_history",
        ["application_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_application_status_history_application_id",
        table_name="application_status_history",
    )
    op.drop_table("application_status_history")
    op.drop_index("ix_credit_applications_status", table_name="credit_applications")
    op.drop_index("ix_credit_applications_inn", table_name="credit_applications")
    op.drop_table("credit_applications")
