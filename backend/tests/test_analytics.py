from datetime import datetime, timezone
from decimal import Decimal

from app.models import Transaction, TransactionType


def test_dashboard_summary(client, db):

    # Register user
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "analytics@example.com",
            "full_name": "Analytics User",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 201

    # Log in
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "analytics@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Retrieve registered user
    from app.models import User

    user = db.query(User).filter(
        User.email == "analytics@example.com"
    ).one()

    # Add test transactions
    transactions = [
        Transaction(
            user_id=user.id,
            amount=Decimal("300000.00"),
            currency="NGN",
            type=TransactionType.INCOME,
            description="Salary",
            transaction_date=datetime(
                2026, 11, 10, tzinfo=timezone.utc
            ),
        ),
        Transaction(
            user_id=user.id,
            amount=Decimal("150000.00"),
            currency="NGN",
            type=TransactionType.INCOME,
            description="Freelance",
            transaction_date=datetime(
                2026, 11, 11, tzinfo=timezone.utc
            ),
        ),
        Transaction(
            user_id=user.id,
            amount=Decimal("90000.00"),
            currency="NGN",
            type=TransactionType.EXPENSE,
            description="Expenses",
            transaction_date=datetime(
                2026, 11, 12, tzinfo=timezone.utc
            ),
        ),
    ]

    db.add_all(transactions)
    db.commit()

    # Retrieve analytics
    response = client.get(
        "/api/v1/analytics/summary?currency=NGN",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert Decimal(data["total_income"]) == Decimal("450000.00")
    assert Decimal(data["total_expenses"]) == Decimal("90000.00")
    assert Decimal(data["net_balance"]) == Decimal("360000.00")
    assert data["transaction_count"] == 3



def test_monthly_trends(client, db):

    # Register user
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "analytics@example.com",
            "full_name": "Analytics User",
            "password": "StrongPassword123!",
        },
    )
    
    assert response.status_code == 201
    
    # Log in
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "analytics@example.com",
            "password": "StrongPassword123!",
        },
    )
    
    assert response.status_code == 200
    
    token = response.json()["access_token"]
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Retrieve registered user
    from app.models import User
    
    user = db.query(User).filter(
        User.email == "analytics@example.com"
    ).one()
    
    # Add test transactions
    transactions = [
        Transaction(
            user_id=user.id,
            amount=Decimal("300000.00"),
            currency="NGN",
            type=TransactionType.INCOME,
            description="Salary",
            transaction_date=datetime(
                2026, 11, 10, tzinfo=timezone.utc
            ),
        ),
        Transaction(
            user_id=user.id,
            amount=Decimal("150000.00"),
            currency="NGN",
            type=TransactionType.INCOME,
            description="Freelance",
            transaction_date=datetime(
                2026, 11, 11, tzinfo=timezone.utc
            ),
        ),
        Transaction(
            user_id=user.id,
            amount=Decimal("90000.00"),
            currency="NGN",
            type=TransactionType.EXPENSE,
            description="Expenses",
            transaction_date=datetime(
                2026, 11, 12, tzinfo=timezone.utc
            ),
        ),
    ]
    
    db.add_all(transactions)
    db.commit()

    response = client.get(
        "/api/v1/analytics/trends?currency=NGN&months=6",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["data"]) == 6

    assert data["currency"] == "NGN"

    assert sum(
        float(item["income"])
        for item in data["data"]
    ) == 450000.00

    assert sum(
        float(item["expenses"])
        for item in data["data"]
    ) == 90000.00



def test_category_breakdown(client, db):

    # Register user
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "analytics@example.com",
            "full_name": "Analytics User",
            "password": "StrongPassword123!",
        },
    )
    
    assert response.status_code == 201
    
    # Log in
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "analytics@example.com",
            "password": "StrongPassword123!",
        },
    )
    
    assert response.status_code == 200
    
    token = response.json()["access_token"]
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Retrieve registered user
    from app.models import User
    
    user = db.query(User).filter(
        User.email == "analytics@example.com"
    ).one()
    
    # Add test transactions
    transactions = [
        Transaction(
            user_id=user.id,
            amount=Decimal("300000.00"),
            currency="NGN",
            type=TransactionType.INCOME,
            description="Salary",
            transaction_date=datetime(
                2026, 11, 10, tzinfo=timezone.utc
            ),
        ),
        Transaction(
            user_id=user.id,
            amount=Decimal("150000.00"),
            currency="NGN",
            type=TransactionType.INCOME,
            description="Freelance",
            transaction_date=datetime(
                2026, 11, 11, tzinfo=timezone.utc
            ),
        ),
        Transaction(
            user_id=user.id,
            amount=Decimal("90000.00"),
            currency="NGN",
            type=TransactionType.EXPENSE,
            description="Expenses",
            transaction_date=datetime(
                2026, 11, 12, tzinfo=timezone.utc
            ),
        ),
    ]
    
    db.add_all(transactions)
    db.commit()

    response = client.get(
        "/api/v1/analytics/categories?currency=NGN",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["currency"] == "NGN"

    assert len(data["data"]) == 1

    assert data["data"][0]["category"] == "Uncategorized"

    assert data["data"][0]["percentage"] == 100.0