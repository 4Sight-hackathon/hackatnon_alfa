from sqlalchemy.orm import Session

from app.models import ApplicationStatus, ApplicationStatusHistory, CreditApplication
from app.schemas import ApplicationCreate
from app.scoring import evaluate


def transition(
    db: Session,
    application: CreditApplication,
    to_status: ApplicationStatus,
    *,
    actor: str,
    reason: str,
) -> None:
    previous = application.status
    application.status = to_status
    db.add(
        ApplicationStatusHistory(
            application=application,
            from_status=previous,
            to_status=to_status,
            actor=actor,
            reason=reason,
        )
    )


def create_application(db: Session, payload: ApplicationCreate) -> CreditApplication:
    application = CreditApplication(**payload.model_dump())
    db.add(application)
    db.flush()
    db.add(
        ApplicationStatusHistory(
            application=application,
            from_status=None,
            to_status=ApplicationStatus.DRAFT,
            actor="CLIENT",
            reason="Черновик заявки создан.",
        )
    )
    db.commit()
    db.refresh(application)
    return application


def submit_application(db: Session, application: CreditApplication) -> CreditApplication:
    transition(
        db,
        application,
        ApplicationStatus.SUBMITTED,
        actor="CLIENT",
        reason="Заявка отправлена в банк.",
    )
    transition(
        db,
        application,
        ApplicationStatus.VALIDATING,
        actor="SYSTEM",
        reason=(
            "Формат ИНН и полнота анкеты проверены; статус бизнеса смоделирован как действующий."
        ),
    )
    transition(
        db,
        application,
        ApplicationStatus.SCORING,
        actor="SYSTEM",
        reason="Запущена прозрачная балльная модель MVP.",
    )

    decision = evaluate(application)
    application.risk_score = decision.risk_score
    application.decision_reason = decision.reason
    application.approved_amount = decision.approved_amount
    application.approved_term_months = decision.approved_term_months
    application.annual_rate = decision.annual_rate
    transition(
        db,
        application,
        decision.status,
        actor="DECISION_ENGINE",
        reason=decision.reason,
    )
    db.commit()
    db.refresh(application)
    return application
