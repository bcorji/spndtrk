# from calendar import monthrange
from datetime import date, datetime, time, timezone
from decimal import Decimal
from uuid import UUID

from sqlalchemy import (
    case,
    func,
    select,
)

from sqlalchemy.orm import Session

from app.models import Transaction, TransactionType


def get_date_range(
    start_date: date | None = None,
    end_date: date | None = None,
):
    today = datetime.now(timezone.utc).date()

    if end_date is None:
        end_date = today

    if start_date is None:
        start_date = end_date.replace(day=1)

    if start_date > end_date:
        raise ValueError("start_date cannot be after end_date")

    start = datetime.combine(
        start_date,
        time.min,
        tzinfo=timezone.utc,
    )

    end_exclusive = datetime.combine(
        date.fromordinal(end_date.toordinal() + 1),
        time.min,
        tzinfo=timezone.utc,
    )

    return start, end_exclusive


def get_summary(
    db: Session,
    user_id: UUID,
    currency: str = "NGN",
    start_date: date | None = None,
    end_date: date | None = None,
):
    start, end = get_date_range(start_date, end_date)

    income_expression = func.coalesce(
        func.sum(
            case(
                (
                    Transaction.type == TransactionType.INCOME,
                    Transaction.amount,
                ),
                else_=0,
            )
        ),
        0,
    )

    expense_expression = func.coalesce(
        func.sum(
            case(
                (
                    Transaction.type == TransactionType.EXPENSE,
                    Transaction.amount,
                ),
                else_=0,
            )
        ),
        0,
    )

    statement = (
        select(
            income_expression.label("income"),
            expense_expression.label("expenses"),
            func.count(Transaction.id).label("count"),
        )
        .where(
            Transaction.user_id == user_id,
            Transaction.currency == currency,
            Transaction.transaction_date >= start,
            Transaction.transaction_date < end,
        )
    )

    result = db.execute(statement).one()

    income = Decimal(str(result.income))
    expenses = Decimal(str(result.expenses))

    return {
        "currency": currency,
        "total_income": income,
        "total_expenses": expenses,
        "net_balance": income - expenses,
        "transaction_count": result.count,
    }


def get_monthly_trends(
    db: Session,
    user_id: UUID,
    currency: str = "NGN",
    months: int = 6,
):
    today = datetime.now(timezone.utc).date()

    month_index = (
        today.year * 12
        + today.month - 1
        - (months - 1)
    )

    start_year, start_month_index = divmod(month_index, 12)

    first_month = date(
        start_year,
        start_month_index + 1,
        1,
    )

    start = datetime.combine(
        first_month,
        time.min,
        tzinfo=timezone.utc,
    )

    month_expression = func.date_trunc(
        "month",
        Transaction.transaction_date,
    )

    income_expression = func.coalesce(
        func.sum(
            case(
                (
                    Transaction.type == TransactionType.INCOME,
                    Transaction.amount,
                ),
                else_=0,
            )
        ),
        0,
    )

    expense_expression = func.coalesce(
        func.sum(
            case(
                (
                    Transaction.type == TransactionType.EXPENSE,
                    Transaction.amount,
                ),
                else_=0,
            )
        ),
        0,
    )

    statement = (
        select(
            month_expression.label("month"),
            income_expression.label("income"),
            expense_expression.label("expenses"),
        )
        .where(
            Transaction.user_id == user_id,
            Transaction.currency == currency,
            Transaction.transaction_date >= start,
        )
        .group_by(month_expression)
        .order_by(month_expression)
    )

    rows = db.execute(statement).all()

    results = {}

    for row in rows:
        key = row.month.strftime("%Y-%m")

        results[key] = {
            "income": Decimal(str(row.income)),
            "expenses": Decimal(str(row.expenses)),
        }

    data = []

    year = first_month.year
    month = first_month.month

    for _ in range(months):
        key = f"{year:04d}-{month:02d}"

        values = results.get(
            key,
            {
                "income": Decimal("0.00"),
                "expenses": Decimal("0.00"),
            },
        )

        data.append({
            "month": key,
            "income": values["income"],
            "expenses": values["expenses"],
        })

        if month == 12:
            month = 1
            year += 1
        else:
            month += 1

    return {
        "currency": currency,
        "months": months,
        "data": data,
    }


def get_category_breakdown(
    db: Session,
    user_id: UUID,
    currency: str = "NGN",
    start_date: date | None = None,
    end_date: date | None = None,
):
    start, end = get_date_range(start_date, end_date)

    from app.models import Category

    statement = (
        select(
            Category.name,
            func.sum(Transaction.amount).label("total"),
        )
        .outerjoin(
            Category,
            Category.id == Transaction.category_id,
        )
        .where(
            Transaction.user_id == user_id,
            Transaction.currency == currency,
            Transaction.type == TransactionType.EXPENSE,
            Transaction.transaction_date >= start,
            Transaction.transaction_date < end,
        )
        .group_by(Category.name)
        .order_by(func.sum(Transaction.amount).desc())
    )

    rows = db.execute(statement).all()

    total_spending = sum(
        (Decimal(str(row.total)) for row in rows),
        Decimal("0.00"),
    )

    data = []

    for row in rows:
        amount = Decimal(str(row.total))

        percentage = (
            float(amount / total_spending * 100)
            if total_spending > 0
            else 0.0
        )

        data.append({
            "category": row.name or "Uncategorized",
            "total": amount,
            "percentage": round(percentage, 2),
        })

    return {
        "currency": currency,
        "data": data,
    }