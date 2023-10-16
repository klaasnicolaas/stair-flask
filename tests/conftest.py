"""Test configuration."""

import os
from unittest.mock import MagicMock, patch

import pytest

from app import LEDController, create_app, db
from app.blueprints.auth.models import User
from app.blueprints.backend.models import Workout
from app.const import WORKOUTS

# --------
# Fixtures
# --------


@pytest.fixture(scope="module")
def new_user() -> pytest.fixture:
    """Create a new user."""
    return User("Tester", "test@test.com", "password")


@pytest.fixture(scope="module")
def test_client(led_controller) -> pytest.fixture:
    """Create a test client for the Flask application."""
    # Set the Testing configuration prior to creating the Flask application
    os.environ["FLASK_ENV"] = "testing"
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            flask_app.led_controller = led_controller
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


@pytest.fixture(scope="module")
def mock_pixelstrip(request) -> pytest.fixture:
    """Create a mock PixelStrip object.

    Args:
    ----
        request (pytest.fixture): Pytest request object
    """
    with patch("rpi_ws281x.PixelStrip", autospec=True) as mock_pixelstrip:
        yield mock_pixelstrip


@pytest.fixture(scope="module")
def led_controller(mock_pixelstrip) -> pytest.fixture:
    """Create a mock LEDController.

    Args:
    ----
        mock_pixelstrip (pytest.fixture): Mock PixelStrip object
    
    Returns:
    -------
        pytest.fixture: Mock LEDController
    """
    count = 10
    pin = 10
    freq_hz = 800000
    dma = 10
    brightness = 255
    invert = False
    channel = 0

    led_controller = LEDController(
        count,
        pin,
        freq_hz,
        dma,
        brightness,
        invert,
        channel,
    )
    led_controller.strip.begin = True

    return led_controller


@pytest.fixture(scope="module")
def cli_test_client() -> pytest.fixture:
    """Create a test client for the CLI."""
    # Set the Testing configuration prior to creating the Flask application
    os.environ["FLASK_ENV"] = "testing"
    flask_app = create_app()

    return flask_app.test_cli_runner()
