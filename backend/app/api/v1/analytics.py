from datetime import date

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)

from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models import User

from app.schemas.analytics import (
    DashboardSummary,
    TrendResponse,
    CategoryBreakdownResponse,
)

from app.services import analytics_service


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get(
    "/summary",
    response_model=DashboardSummary,
)
def dashboard_summary(
    currency: str = Query(
        default="NGN",
        pattern=r"^[A-Z]{3}$",
    ),
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        return analytics_service.get_summary(
            db,
            user.id,
            currency,
            start_date,
            end_date,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        )


@router.get(
    "/trends",
    response_model=TrendResponse,
)
def dashboard_trends(
    currency: str = Query(
        default="NGN",
        pattern=r"^[A-Z]{3}$",
    ),
    months: int = Query(
        default=6,
        ge=1,
        le=24,
    ),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return analytics_service.get_monthly_trends(
        db,
        user.id,
        currency,
        months,
    )


@router.get(
    "/categories",
    response_model=CategoryBreakdownResponse,
)
def dashboard_categories(
    currency: str = Query(
        default="NGN",
        pattern=r"^[A-Z]{3}$",
    ),
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        return analytics_service.get_category_breakdown(
            db,
            user.id,
            currency,
            start_date,
            end_date,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        )