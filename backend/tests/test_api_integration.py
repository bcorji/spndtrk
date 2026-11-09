def register_user(client, email):
    return client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "full_name": "Test User",
            "password": "StrongPassword123!",
        },
    )


def login_user(client, email):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": "StrongPassword123!",
        },
    )

    return response.json()["access_token"]


def test_authentication_and_transaction_crud(client):

    # Register two users
    user_a = register_user(client, "usera@example.com")
    user_b = register_user(client, "userb@example.com")

    assert user_a.status_code == 201
    assert user_b.status_code == 201

    # Authenticate user A
    token_a = login_user(client, "usera@example.com")

    headers_a = {
        "Authorization": f"Bearer {token_a}"
    }

    # Authenticate user B
    token_b = login_user(client, "userb@example.com")

    headers_b = {
        "Authorization": f"Bearer {token_b}"
    }

    # Create transaction as user A
    response = client.post(
        "/api/v1/transactions/",
        headers=headers_a,
        json={
            "amount": "15000.00",
            "currency": "NGN",
            "type": "expense",
            "description": "Internet subscription",
            "category_id": None,
            "transaction_date": "2026-11-09T10:00:00Z",
        },
    )

    assert response.status_code == 201

    transaction_id = response.json()["id"]

    # User A can retrieve their transaction
    response = client.get(
        f"/api/v1/transactions/{transaction_id}",
        headers=headers_a,
    )

    assert response.status_code == 200

    # User B cannot retrieve user A's transaction
    response = client.get(
        f"/api/v1/transactions/{transaction_id}",
        headers=headers_b,
    )

    assert response.status_code == 404

    # User B cannot update user A's transaction
    response = client.patch(
        f"/api/v1/transactions/{transaction_id}",
        headers=headers_b,
        json={"amount": "1000.00"},
    )

    assert response.status_code == 404

    # User A can update their transaction
    response = client.patch(
        f"/api/v1/transactions/{transaction_id}",
        headers=headers_a,
        json={"amount": "18000.00"},
    )

    assert response.status_code == 200
    assert response.json()["amount"] == "18000.00"

    # User A can delete their transaction
    response = client.delete(
        f"/api/v1/transactions/{transaction_id}",
        headers=headers_a,
    )

    assert response.status_code == 204

    # Deleted transaction is no longer available
    response = client.get(
        f"/api/v1/transactions/{transaction_id}",
        headers=headers_a,
    )

    assert response.status_code == 404