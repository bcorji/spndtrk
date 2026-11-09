from app.core.security import (
    hash_password,
    verify_password,
)


def test_password_hashing():
    password = "MyStrongPassword123!"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)


def test_invalid_password():
    password = "MyStrongPassword123!"

    hashed = hash_password(password)

    assert not verify_password(
        "WrongPassword123!",
        hashed,
    )