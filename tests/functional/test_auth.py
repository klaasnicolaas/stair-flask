"""Test authentication pages."""
import pytest

from app import db
from app.blueprints.auth.models import User


def test_login_page(client: pytest.fixture) -> None:
    """Test login page.

    Args:
    ----
        client (pytest.fixture): Test client for the Flask application
    """
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Inloggen" in response.data
    assert b"E-mail" in response.data
    assert b"Wachtwoord" in response.data


def test_valid_login_logout(
    client: pytest.fixture,
    user: User,
) -> None:
    """Test login and logout.

    Args:
    ----
        client (pytest.fixture): Test client for the Flask application
        user (User): User model
    """
    db.session.add(user)
    response = client.post(
        "/login",
        data=dict(email=user.email, password="secretPassword"),
        follow_redirects=True,
    )
    assert user.is_authenticated is True
    assert response.status_code == 200

    response_logout = client.get("/logout", follow_redirects=True)
    assert response_logout.status_code == 200
    assert len(response_logout.history) == 1


def test_registration_page(client: pytest.fixture) -> None:
    """Test registration page.

    Args:
    ----
        client (pytest.fixture): Test client for the Flask application
    """
    response = client.get("/register")
    assert response.status_code == 200
    assert b"Registreren" in response.data
    assert b"E-mail" in response.data
    assert b"Wachtwoord" in response.data
