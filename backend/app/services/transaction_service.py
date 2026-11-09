from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import (
    User,
    Category,
    Transaction,
)
from app.schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
)


def validate_category(
    db: Session,
    user_id: UUID,
    category_id: UUID | None,
    transaction_type,
):
    if category_id is None:
        return

    category = db.scalar(
        select(Category).where(
            Category.id == category_id,
            (
                (Category.user_id == user_id)
                | (Category.user_id.is_(None))
            ),
        )
    )

    if category is None:
        raise ValueError("Category not found")

    if category.type != transaction_type:
        raise ValueError(
            "Category type does not match transaction type"
        )


def create_transaction(
    db: Session,
    user: User,
    data: TransactionCreate,
) -> Transaction:

    validate_category(
        db,
        user.id,
        data.category_id,
        data.type,
    )

    transaction = Transaction(
        user_id=user.id,
        amount=data.amount,
        currency=data.currency,
        type=data.type,
        description=data.description,
        category_id=data.category_id,
        transaction_date=data.transaction_date,
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction


def get_transactions(
    db: Session,
    user_id: UUID,
    skip: int = 0,
    limit: int = 20,
):
    return db.scalars(
        select(Transaction)
        .where(Transaction.user_id == user_id)
        .order_by(Transaction.transaction_date.desc())
        .offset(skip)
        .limit(limit)
    ).all()


def get_transaction(
    db: Session,
    user_id: UUID,
    transaction_id: UUID,
):
    return db.scalar(
        select(Transaction).where(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id,
        )
    )


def update_transaction(
    db: Session,
    user: User,
    transaction: Transaction,
    data: TransactionUpdate,
):

    updates = data.model_dump(exclude_unset=True)

    new_type = updates.get("type", transaction.type)

    new_category_id = updates.get(
        "category_id",
        transaction.category_id,
    )

    validate_category(
        db,
        user.id,
        new_category_id,
        new_type,
    )

    for field, value in updates.items():
        setattr(transaction, field, value)

    db.commit()
    db.refresh(transaction)

    return transaction


def delete_transaction(
    db: Session,
    transaction: Transaction,
):
    db.delete(transaction)
    db.commit()