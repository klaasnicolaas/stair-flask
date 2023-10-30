"""Test the CLI commands."""

from unittest.mock import patch

import pytest

from app.blueprints.auth.models import User
from app.blueprints.backend.models import Workout
from app.const import WORKOUTS, IsAdmin


def test_initialize_database(cli_test_client: pytest.fixture) -> None:
    """Test the init_db command.

    Args:
    ----
        cli_test_client: Test client for the Flask application
    """
    output = cli_test_client.invoke(args=["init_db"])
    assert output.exit_code == 0
    assert "Database initialized successfully!" in output.output


def test_seed_workouts(
    cli_test_client: pytest.fixture, database: pytest.fixture
) -> None:
    """Test the seed_workouts command.

    Args:
    ----
        cli_test_client: Test client for the Flask application
        database (pytest.fixture): Database fixture
    """
    output = cli_test_client.invoke(args=["seed_workouts"])
    assert output.exit_code == 0
    assert "Workouts table seeded successfully!" in output.output

    # Assert that the database contains the correct number of workouts
    workout_count = database.session.query(Workout).count()
    assert workout_count == len(WORKOUTS)


def test_create_admin_success(
    cli_test_client: pytest.fixture, database: pytest.fixture
) -> None:
    """Test the create_admin command.

    Args:
    ----
        cli_test_client: Test client for the Flask application
        database (pytest.fixture): Database fixture
    """
    inputs = [
        "Admin Tester",  # name
        "admin@test.com",  # email
        "secretpassword",  # password
        "secretpassword",  # confirm_password
    ]

    with patch("getpass.getpass", side_effect=inputs[2:4]):
        result = cli_test_client.invoke(args=["create_admin"], input="\n".join(inputs))
    assert result.exit_code == 0

    # Check the database state
    admin_user = database.session.query(User).filter_by(email="admin@test.com").first()
    assert admin_user is not None
    assert admin_user.is_admin == IsAdmin.YES.value


def test_create_admin_password_mismatch(cli_test_client: pytest.fixture) -> None:
    """Test the create_admin command.

    Args:
    ----
        cli_test_client: Test client for the Flask application
    """
    inputs = [
        "Admin Tester",  # name
        "admin@test.com",  # email
        "secretpassword",  # password
        "wrongpassword",  # confirm_password
    ]

    with patch("getpass.getpass", side_effect=inputs[2:4]):
        result = cli_test_client.invoke(args=["create_admin"], input="\n".join(inputs))
    assert "Passwords don't match" in result.output
