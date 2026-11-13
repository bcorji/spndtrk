
"""enhance receipt model for OCR and AI extraction

Revision ID: b1e3fec8a301
Revises: c8d791469283
Create Date: 2026-11-13 16:35:49.338475
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b1e3fec8a301"
down_revision: Union[str, Sequence[str], None] = "c8d791469283"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add receipt metadata columns.
    # The receipts table is currently empty.
    op.add_column(
        "receipts",
        sa.Column("original_filename", sa.String(255), nullable=False),
    )

    op.add_column(
        "receipts",
        sa.Column("stored_filename", sa.String(255), nullable=False),
    )

    op.add_column(
        "receipts",
        sa.Column("mime_type", sa.String(100), nullable=False),
    )

    op.add_column(
        "receipts",
        sa.Column("extracted_text", sa.Text(), nullable=True),
    )

    # Add transaction lookup index.
    op.create_index(
        "ix_receipts_transaction_id",
        "receipts",
        ["transaction_id"],
        unique=False,
    )

    # Add explicitly named unique constraints.
    op.create_unique_constraint(
        "uq_receipts_stored_filename",
        "receipts",
        ["stored_filename"],
    )

    op.create_unique_constraint(
        "uq_receipts_storage_key",
        "receipts",
        ["storage_key"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_receipts_storage_key",
        "receipts",
        type_="unique",
    )

    op.drop_constraint(
        "uq_receipts_stored_filename",
        "receipts",
        type_="unique",
    )

    op.drop_index(
        "ix_receipts_transaction_id",
        table_name="receipts",
    )

    op.drop_column("receipts", "extracted_text")
    op.drop_column("receipts", "mime_type")
    op.drop_column("receipts", "stored_filename")
    op.drop_column("receipts", "original_filename")
