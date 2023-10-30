"""Unit tests for auth models."""
from datetime import datetime

from app.blueprints.auth.models import User
from app.blueprints.backend.models import Sensor, Workout


def test_new_user() -> None:
    """Test user model."""
    user = User("Tester", "test@test.com", "password")
    assert user.name == "Tester"
    assert user.email == "test@test.com"
    assert user.password_hash != "password"
    assert user.is_authenticated is True
    assert user.is_active is True
    assert user.is_anonymous is False


def test_setting_password(user: User) -> None:
    """Test setting password.

    Args:
    ----
        user (User): User model
    """
    user.set_password("password")
    assert user.password_hash != "password"
    assert user.check_password("password") is True
    assert user.check_password("wrong") is False


def test_user_id(user: User) -> None:
    """Test user id.

    Args:
    ----
        user (User): User model
    """
    user.id = 1
    assert isinstance(user.id, int)
    assert not isinstance(user.id, str)
    assert user.id == 1


def test_sensor_model() -> None:
    """Test sensor model."""
    sensor = Sensor("sensor-1", "127.0.0.1", 100, 20, 50, "active", datetime.utcnow())
    assert sensor.client_id == "sensor-1"
    assert sensor.ip_address == "127.0.0.1"
    assert sensor.max_distance == 100
    assert sensor.trigger_distance == 20
    assert sensor.threshold == 50
    assert sensor.status == "active"
    assert isinstance(sensor.last_update, datetime)


def test_workout_model() -> None:
    """Test workout model."""
    workout = Workout("Test Workout", "Test Workout Description", None)
    assert workout.name == "Test Workout"
    assert workout.description == "Test Workout Description"
    assert workout.pros is None
