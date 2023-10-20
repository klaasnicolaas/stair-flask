"""Functional tests for the backend of the Flask application."""

import pytest

from app.blueprints.auth.models import User

@pytest.mark.usefixtures("as_user")
def test_dashboard_view(client: pytest.fixture, user: User) -> None:
    """Test the dashboard view.
    
    Args:
    ----
        client: Test client for the Flask application.
        user: User model.
    """
    assert user.is_authenticated is True
    response = client.get("/admin")
    assert response.request.path == "/admin"
