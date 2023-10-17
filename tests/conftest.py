"""Test configuration."""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest

from app import LEDController, create_app, db
from app.blueprints.auth.models import User
from app.blueprints.backend.models import Workout
from app.const import WORKOUTS

# --------
# Fixtures
# --------
_mock_rpi_ws281x = MagicMock()
channels = {}

@pytest.fixture(scope="module")
def new_user() -> pytest.fixture:
    """Create a new user."""
    return User("Tester", "test@test.com", "password")


@pytest.fixture(scope="module")
def test_client(_rpi_ws281x) -> pytest.fixture:
    """Create a test client for the Flask application."""
    # Set the Testing configuration prior to creating the Flask application
    os.environ["FLASK_ENV"] = "testing"
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client


@pytest.fixture(scope="module")
def init_database(test_client: pytest.fixture) -> pytest.fixture:
    """Create the database and the database tables.

    Args:
    ----
        test_client (pytest.fixture): Test client for the Flask application
    """
    db.create_all()

    for workout in WORKOUTS:
        db.session.add(
            Workout(
                name=workout["name"],
                description=workout["description"],
                pros=workout["pros"],
                cons=None if "cons" not in workout else workout["cons"],
            ),
        )
        db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()


@pytest.fixture(scope='module', autouse=False)
def _rpi_ws281x() -> pytest.fixture:
    """Mock the _rpi_ws281x module.
    
    This fixture is used to mock the _rpi_ws281x module. It is used to mock the
    PixelStrip class and the ws2811_init function.

    Returns:
    -------
        pytest.fixture: Mocked _rpi_ws281x module
    """
    _mock_rpi_ws281x.ws2811_init.return_value = 0
    sys.modules['_rpi_ws281x'] = _mock_rpi_ws281x

    yield _mock_rpi_ws281x
    del sys.modules['_rpi_ws281x']
    _mock_rpi_ws281x.reset_mock()
    channels.clear()


@pytest.fixture(scope="module")
def cli_test_client() -> pytest.fixture:
    """Create a test client for the CLI."""
    # Set the Testing configuration prior to creating the Flask application
    os.environ["FLASK_ENV"] = "testing"
    flask_app = create_app()

    return flask_app.test_cli_runner()
