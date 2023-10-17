"""Test configuration."""

import os
from unittest.mock import MagicMock, patch

import pytest

from app import create_app, db
from app.blueprints.auth.models import User
from app.blueprints.backend.models import Workout
from app.const import WORKOUTS

# --------
# Fixtures
# --------


@pytest.fixture(autouse=True)
def mock_strip() -> MagicMock:
    """Mock the LED strip.

    Returns
    -------
        MagicMock: Mocked LED strip
    """
    mock = MagicMock()

    # Mock the number of pixels
    mock.numPixels.return_value = 10
    with patch("app.led_controller.PixelStrip.begin"), patch(
        "app.led_controller.PixelStrip", return_value=mock,
    ), patch("app.led_controller.PixelStrip.setPixelColor"), patch(
        "app.led_controller.PixelStrip.numPixels",
    ), patch(
        "app.led_controller.PixelStrip.show",
    ):
        yield mock


@pytest.fixture(scope="module", autouse=True)
def mock_mqtt() -> MagicMock:
    """Mock the MQTT client.

    Returns
    -------
        MagicMock: Mocked MQTT client
    """
    mock = MagicMock()
    with patch("app.mqtt.connect"):
        yield mock


@pytest.fixture(scope="module")
def new_user() -> pytest.fixture:
    """Create a new user."""
    return User("Tester", "test@test.com", "password")


@pytest.fixture()
def test_client(mock_strip: MagicMock) -> pytest.fixture:
    """Create a test client for the Flask application."""
    # Set the Testing configuration prior to creating the Flask application
    os.environ["FLASK_ENV"] = "testing"
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client


@pytest.fixture()
def init_database(test_client: pytest.fixture) -> None:
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


@pytest.fixture()
def cli_test_client(mock_strip: MagicMock) -> pytest.fixture:
    """Create a test client for the CLI."""
    # Set the Testing configuration prior to creating the Flask application
    os.environ["FLASK_ENV"] = "testing"
    flask_app = create_app()

    return flask_app.test_cli_runner()
