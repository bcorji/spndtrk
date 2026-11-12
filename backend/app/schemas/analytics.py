from decimal import Decimal
from pydantic import BaseModel


class DashboardSummary(BaseModel):
    currency: str
    total_income: Decimal
    total_expenses: Decimal
    net_balance: Decimal
    transaction_count: int


class MonthlyTrend(BaseModel):
    month: str
    income: Decimal
    expenses: Decimal


class TrendResponse(BaseModel):
    currency: str
    months: int
    data: list[MonthlyTrend]


class CategoryBreakdown(BaseModel):
    category: str
    total: Decimal
    percentage: float


class CategoryBreakdownResponse(BaseModel):
    currency: str
    data: list[CategoryBreakdown]