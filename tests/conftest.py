"""Test configuration."""

import os
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from flask_login import login_user

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
        "app.led_controller.PixelStrip",
        return_value=mock,
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


@pytest.fixture
def user() -> User:
    """Create a new user."""
    user = User(
        name="Tester",
        email="test@test.com",
        password="secretPassword",
        created_at=datetime.utcnow(),
    )
    user.set_password("secretPassword")
    return user


# @pytest.fixture
# def as_user(client, init_database, user):
#     db.session.add(user)
#     return client.post(
#         "/login",
#         data=dict(email=user.email, password="secretPassword"),
#         follow_redirects=True,
#     )


@pytest.fixture
def auth_client(
    app: pytest.fixture, user: User, database: pytest.fixture
) -> pytest.fixture:
    """Log in as a user.

    Args:
    ----
        app (pytest.fixture): Test client for the Flask application
        user (User): User to log in as

    Returns:
    -------
        pytest.fixture: Logged in user
    """
    with app.test_request_context():
        database.session.add(user)
        database.session.commit()
        test_user = database.session.query(User).filter_by(id=1).first()
        yield login_user(test_user, remember=True)


@pytest.fixture
def database(app: pytest.fixture) -> pytest.fixture:
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()


@pytest.fixture
def app(mock_strip: MagicMock) -> pytest.fixture:
    """Create the test Flask application."""
    # Set the Testing configuration prior to creating the Flask application
    os.environ["FLASK_ENV"] = "testing"
    flask_app = create_app()

    return flask_app  # this is where the testing happens!


@pytest.fixture
def client(app: pytest.fixture) -> pytest.fixture:
    """Create a test client for the Flask application."""
    with app.app_context():
        yield app.test_client()


@pytest.fixture
def init_database(database: pytest.fixture) -> None:
    """Create the database and the database tables.

    Args:
    ----
        app (pytest.fixture): Test client for the Flask application
    """
    # Add workout data
    for workout in WORKOUTS:
        database.session.add(
            Workout(
                name=workout["name"],
                description=workout["description"],
                pros=workout["pros"],
                cons=None if "cons" not in workout else workout["cons"],
            ),
        )
    database.session.commit()

    yield  # this is where the testing happens!

    database.drop_all()


@pytest.fixture
def cli_test_client(mock_strip: MagicMock) -> pytest.fixture:
    """Create a test client for the CLI."""
    # Set the Testing configuration prior to creating the Flask application
    os.environ["FLASK_ENV"] = "testing"
    flask_app = create_app()

    return flask_app.test_cli_runner()
