from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from app.models import TransactionType


class TransactionCreate(BaseModel):
    amount: Decimal = Field(
        gt=0,
        max_digits=14,
        decimal_places=2,
    )

    currency: str = Field(
        default="NGN",
        pattern=r"^[A-Z]{3}$",
    )

    type: TransactionType

    description: str | None = Field(
        default=None,
        max_length=1000,
    )

    category_id: UUID | None = None

    transaction_date: datetime


class TransactionUpdate(BaseModel):
    amount: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=14,
        decimal_places=2,
    )

    currency: str | None = Field(
        default=None,
        pattern=r"^[A-Z]{3}$",
    )

    type: TransactionType | None = None

    description: str | None = Field(
        default=None,
        max_length=1000,
    )

    category_id: UUID | None = None

    transaction_date: datetime | None = None


class TransactionResponse(BaseModel):
    id: UUID
    user_id: UUID
    category_id: UUID | None

    amount: Decimal
    currency: str
    type: TransactionType
    description: str | None
    transaction_date: datetime

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)