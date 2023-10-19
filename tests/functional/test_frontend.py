"""Functional tests for the frontend of the Flask application."""

from app.blueprints.backend.models import Workout


def test_home_view(test_client, init_database) -> None:
    """Test the home view.

    Args:
    ----
        test_client: Test client for the Flask application.
        init_database: Initialize the database.
    """
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.request.path == "/"

    # Check if specific workout models are present in the response
    for workout in Workout.query.all():
        assert workout.name.encode() in response.data


def test_workouts_view(test_client, init_database) -> None:
    """Test the workouts view.

    Args:
    ----
        test_client: Test client for the Flask application.
        init_database: Initialize the database.
    """
    response = test_client.get("/workouts")
    assert response.status_code == 200
    assert response.request.path == "/workouts"

    # Check if specific workout models are present in the response
    for workout in Workout.query.all():
        assert workout.name.encode() in response.data


def test_workout_control_view(test_client, init_database) -> None:
    """Test the workout control view.

    Args:
    ----
        test_client: Test client for the Flask application.
    """
    response = test_client.get("/workouts/1/control")
    assert response.status_code == 200
    assert response.request.path == "/workouts/1/control"
    assert b"Kameleon" in response.data


def test_info_view(test_client) -> None:
    """Test the info view.

    Args:
    ----
        test_client: Test client for the Flask application.
    """
    response = test_client.get("/info")
    assert response.status_code == 200
    assert response.request.path == "/info"
