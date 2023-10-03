"""Test authentication pages."""
import pytest


def test_login_page(test_client: pytest.fixture) -> None:
    """Test login page.

    Args:
    ----
        test_client (pytest.fixture): Test client for the Flask application
    """
    response = test_client.get("/login")
    assert response.status_code == 200
    assert b"Inloggen" in response.data
    assert b"Email" in response.data
    assert b"Password" in response.data


def test_valid_login_logout(
    test_client: pytest.fixture,
    init_database: pytest.fixture,
) -> None:
    """Test login and logout.

    Args:
    ----
        test_client (pytest.fixture): Test client for the Flask application
        init_database (pytest.fixture): Initialize the database
    """
    response = test_client.post(
        "/login",
        data={"email": "test@test.com", "password": "SecretPass"},
        follow_redirects=True,
    )
    assert response.status_code == 200

    response = test_client.get("/logout", follow_redirects=True)
    assert response.status_code == 200


def test_registration_page(test_client: pytest.fixture) -> None:
    """Test registration page.

    Args:
    ----
        test_client (pytest.fixture): Test client for the Flask application
    """
    response = test_client.get("/register")
    assert response.status_code == 200
    assert b"Registreren" in response.data
    assert b"Email" in response.data
    assert b"Password" in response.data
