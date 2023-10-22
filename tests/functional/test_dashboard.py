"""Functional tests for the backend of the Flask application."""

import pytest
from flask_login import current_user


@pytest.mark.usefixtures("auth_client")
def test_dashboard_view(client: pytest.fixture) -> None:
    """Test the dashboard view as admin.

    Args:
    ----
        client: Test client for the Flask application.
    """
    assert current_user.is_authenticated is True
    assert current_user.is_admin is True
    assert current_user.id == 1

    response = client.get("/admin")
    assert response.status_code == 308
    assert response.request.path == "/admin"


@pytest.mark.usefixtures("auth_client")
def test_sensors_view(client: pytest.fixture) -> None:
    """Test the sensors view as admin.

    Args:
    ----
        client: Test client for the Flask application.
    """
    assert current_user.is_authenticated is True
    assert current_user.is_admin is True
    assert current_user.id == 1

    response = client.get("/admin/sensors")
    assert response.status_code == 200
    assert response.request.path == "/admin/sensors"
