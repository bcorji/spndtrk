import enum
import uuid

from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sqlalchemy import Uuid

from app.db.base import Base


def utc_now():
    return datetime.now(timezone.utc)


class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class ReceiptStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    REVIEW = "review"
    CONFIRMED = "confirmed"
    FAILED = "failed"

transaction_type_enum = Enum(
    TransactionType,
    name="transaction_type",
)

receipt_status_enum = Enum(
    ReceiptStatus,
    name="receipt_status",
)

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )

    categories = relationship(
        "Category",
        back_populates="user",
    )

    transactions = relationship(
        "Transaction",
        back_populates="user",
    )

    receipts = relationship(
        "Receipt",
        back_populates="user",
    )


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    type: Mapped[TransactionType] = mapped_column(
        transaction_type_enum,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="categories",
    )

    transactions = relationship(
        "Transaction",
        back_populates="category",
    )


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    category_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="NGN",
    )

    type: Mapped[TransactionType] = mapped_column(
        transaction_type_enum,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    transaction_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="transactions",
    )

    category = relationship(
        "Category",
        back_populates="transactions",
    )

    receipts = relationship(
        "Receipt",
        back_populates="transaction",
    )


class Receipt(Base):
    __tablename__ = "receipts"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    transaction_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("transactions.id", ondelete="SET NULL"),
        nullable=True,
    )

    storage_key: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    status: Mapped[ReceiptStatus] = mapped_column(
        receipt_status_enum,
        default=ReceiptStatus.UPLOADED,
        nullable=False,
    )

    extracted_data: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="receipts",
    )

    transaction = relationship(
        "Transaction",
        back_populates="receipts",
    )

    items = relationship(
        "TransactionItem",
        back_populates="receipt",
        cascade="all, delete-orphan",
    )


class TransactionItem(Base):
    __tablename__ = "transaction_items"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    receipt_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("receipts.id", ondelete="CASCADE"),
        nullable=False, # Come back to this and check if it should be nullable or not
        index=True,
    )

    description: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(12, 3),
        nullable=False,
        default=Decimal("1"),
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    total_price: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    receipt = relationship(
        "Receipt",
        back_populates="items",
    )