import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.models import ApplicationStatus, CreditApplication
from app.schemas import ApplicationCreate, ApplicationRead, Product
from app.service import create_application, submit_application, transition

router = APIRouter()

PRODUCTS = [
    Product(
        code="WORKING_CAPITAL",
        name="Кредит на оборотные средства",
        description="Закупка товара, сырья и покрытие текущих расходов.",
        min_amount=100_000,
        max_amount=30_000_000,
        min_term_months=3,
        max_term_months=36,
    )
]


def get_application_or_404(db: Session, application_id: uuid.UUID) -> CreditApplication:
    statement = (
        select(CreditApplication)
        .where(CreditApplication.id == application_id)
        .options(selectinload(CreditApplication.status_history))
    )
    application = db.scalar(statement)
    if application is None:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    return application


@router.get("/products", response_model=list[Product])
def list_products() -> list[Product]:
    return PRODUCTS


@router.post("/applications", response_model=ApplicationRead, status_code=status.HTTP_201_CREATED)
def create(payload: ApplicationCreate, db: Session = Depends(get_db)) -> CreditApplication:
    if payload.product_code not in {product.code for product in PRODUCTS}:
        raise HTTPException(status_code=422, detail="Неизвестный кредитный продукт")
    return create_application(db, payload)


@router.get("/applications/{application_id}", response_model=ApplicationRead)
def get(application_id: uuid.UUID, db: Session = Depends(get_db)) -> CreditApplication:
    return get_application_or_404(db, application_id)


@router.post("/applications/{application_id}/submit", response_model=ApplicationRead)
def submit(application_id: uuid.UUID, db: Session = Depends(get_db)) -> CreditApplication:
    application = get_application_or_404(db, application_id)
    if application.status is not ApplicationStatus.DRAFT:
        raise HTTPException(status_code=409, detail="Отправить можно только черновик")
    return submit_application(db, application)


@router.post("/applications/{application_id}/accept", response_model=ApplicationRead)
def accept(application_id: uuid.UUID, db: Session = Depends(get_db)) -> CreditApplication:
    application = get_application_or_404(db, application_id)
    if application.status is not ApplicationStatus.OFFERED:
        raise HTTPException(status_code=409, detail="Принять можно только активный оффер")
    transition(
        db,
        application,
        ApplicationStatus.ACCEPTED,
        actor="CLIENT",
        reason="Клиент принял условия. Подписание и выдача смоделированы.",
    )
    db.commit()
    db.refresh(application)
    return application
