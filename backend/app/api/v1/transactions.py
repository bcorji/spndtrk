from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Response,
    status,
)
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models import User
from app.schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
)
from app.services import transaction_service


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)


@router.post(
    "/",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    data: TransactionCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        return transaction_service.create_transaction(
            db,
            user,
            data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get(
    "/",
    response_model=list[TransactionResponse],
)
def list_all(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return transaction_service.get_transactions(
        db,
        user.id,
        skip,
        limit,
    )


@router.get(
    "/{transaction_id}",
    response_model=TransactionResponse,
)
def retrieve(
    transaction_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    transaction = transaction_service.get_transaction(
        db,
        user.id,
        transaction_id,
    )

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found",
        )

    return transaction


@router.patch(
    "/{transaction_id}",
    response_model=TransactionResponse,
)
def update(
    transaction_id: UUID,
    data: TransactionUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    transaction = transaction_service.get_transaction(
        db,
        user.id,
        transaction_id,
    )

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found",
        )

    try:
        return transaction_service.update_transaction(
            db,
            user,
            transaction,
            data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.delete(
    "/{transaction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(
    transaction_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    transaction = transaction_service.get_transaction(
        db,
        user.id,
        transaction_id,
    )

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found",
        )

    transaction_service.delete_transaction(db, transaction)

    return Response(status_code=status.HTTP_204_NO_CONTENT)