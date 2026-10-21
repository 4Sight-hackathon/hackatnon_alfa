from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

from app.models import ApplicationStatus, CreditApplication


@dataclass(frozen=True)
class Decision:
    status: ApplicationStatus
    risk_score: int
    reason: str
    approved_amount: Decimal | None = None
    approved_term_months: int | None = None
    annual_rate: Decimal | None = None


def evaluate(application: CreditApplication) -> Decision:
    """Transparent MVP score. This is a demo policy, not a bank underwriting model."""
    if application.has_overdue_debt:
        return Decision(
            status=ApplicationStatus.DECLINED,
            risk_score=95,
            reason="Обнаружена текущая просроченная задолженность.",
        )

    amount_to_revenue = application.requested_amount / application.annual_revenue
    annual_debt_burden = (application.monthly_debt_payments * 12) / application.annual_revenue

    score = 12
    reasons: list[str] = []

    if amount_to_revenue > Decimal("0.50"):
        score += 30
        reasons.append("сумма выше 50% годовой выручки")
    elif amount_to_revenue > Decimal("0.30"):
        score += 18
        reasons.append("запрошена значимая доля годовой выручки")
    else:
        score += 5

    if annual_debt_burden > Decimal("0.40"):
        score += 30
        reasons.append("высокая текущая долговая нагрузка")
    elif annual_debt_burden > Decimal("0.25"):
        score += 18
        reasons.append("повышенная текущая долговая нагрузка")
    else:
        score += 4

    if application.years_in_business < 1:
        score += 25
        reasons.append("бизнес работает менее года")
    elif application.years_in_business < 2:
        score += 12
        reasons.append("короткая история бизнеса")

    score = min(score, 100)
    reason_suffix = "; ".join(reasons) if reasons else "стабильные финансовые показатели"

    if score >= 70:
        return Decision(ApplicationStatus.DECLINED, score, f"Высокий риск: {reason_suffix}.")
    if score >= 45:
        return Decision(
            ApplicationStatus.MANUAL_REVIEW,
            score,
            f"Требуется экспертная проверка: {reason_suffix}.",
        )

    rate = (Decimal("18.90") + Decimal(score) * Decimal("0.06")).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    return Decision(
        status=ApplicationStatus.OFFERED,
        risk_score=score,
        reason=f"Автоматическая проверка пройдена: {reason_suffix}.",
        approved_amount=application.requested_amount,
        approved_term_months=application.term_months,
        annual_rate=rate,
    )
