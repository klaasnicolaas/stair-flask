"""Functional tests for the frontend of the Flask application."""

import pytest

from app.blueprints.backend.models import Workout


def test_home_view(client: pytest.fixture, init_database: pytest.fixture) -> None:
    """Test the home view.

    Args:
    ----
        client: Test client for the Flask application.
        init_database: Initialize the database.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.request.path == "/"

    # Check if specific workout models are present in the response
    for workout in Workout.query.all():
        assert workout.name.encode() in response.data


def test_workouts_view(client: pytest.fixture, init_database: pytest.fixture) -> None:
    """Test the workouts view.

    Args:
    ----
        client: Test client for the Flask application.
        init_database: Initialize the database.
    """
    response = client.get("/workouts")
    assert response.status_code == 200
    assert response.request.path == "/workouts"

    # Check if specific workout models are present in the response
    for workout in Workout.query.all():
        assert workout.name.encode() in response.data


def test_workout_control_view(client: pytest.fixture, init_database) -> None:
    """Test the workout control view.

    Args:
    ----
        client: Test client for the Flask application.
    """
    response = client.get("/workouts/1/control")
    assert response.status_code == 200
    assert response.request.path == "/workouts/1/control"
    assert b"Kameleon" in response.data


def test_info_view(client: pytest.fixture) -> None:
    """Test the info view.

    Args:
    ----
        client: Test client for the Flask application.
    """
    response = client.get("/info")
    assert response.status_code == 200
    assert response.request.path == "/info"
