"""Functional tests for the backend of the Flask application."""

import pytest

from app.blueprints.auth.models import User


@pytest.mark.usefixtures("auth_client")
def test_dashboard_view(client: pytest.fixture, user: User, database) -> None:
    """Test the dashboard view.

    Args:
    ----
        client: Test client for the Flask application.
        user: User model.
    """
    user = database.session.query(User).filter_by(id=1).first()
    assert user.is_authenticated is True

    response = client.get("/admin")
    assert response.status_code == 308
    assert response.request.path == "/admin"


@pytest.mark.usefixtures("auth_client")
def test_sensors_view(client: pytest.fixture, user: User, database) -> None:
    """Test the sensors view.

    Args:
    ----
        client: Test client for the Flask application.
        user: User model.
    """
    user = database.session.query(User).filter_by(id=1).first()
    assert user.is_authenticated is True

    response = client.get("/admin/sensors")
    assert response.status_code == 200
    assert response.request.path == "/admin/sensors"
