"""Blueprint for the frontend of the application."""
from flask import Blueprint, render_template

from app import db
from app.blueprints.backend.models import Sensor, Workout

bp = Blueprint("frontend", __name__, template_folder="templates/frontend")


@bp.route("/", methods=["GET"])
def home() -> None:
    """Render the home page."""
    return render_template("home.html", workouts=Workout.query.all())


@bp.route("/workouts", methods=["GET"])
def workouts() -> None:
    """Render the workouts page."""
    return render_template("workouts.html", workouts=Workout.query.all())


@bp.route("/workouts/<int:workout_id>/control", methods=["GET"])
def workout_control(workout_id: int) -> None:
    """Render the workout control page."""
    return render_template(
        "workouts/control.html",
        workout=db.session.get(Workout, workout_id),
        sensors=Sensor.query.all(),
    )


@bp.route("/info", methods=["GET"])
def info() -> None:
    """Render the info page."""
    return render_template("info.html")
