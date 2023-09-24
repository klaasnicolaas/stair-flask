"""Blueprint for the backend of the application."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.blueprints.auth.models import User

from .models import Sensor, Workout

bp = Blueprint("backend", __name__, template_folder="templates/admin")


@bp.route("/", methods=["GET"])
@login_required
def dashboard() -> None:
    """Render the dashboard page."""
    return render_template("dashboard.html", user=current_user)


@bp.route("/sensors", methods=["GET"])
@login_required
def sensors() -> None:
    """Render the sensors page."""
    return render_template(
        "sensors/index.html",
        user=current_user,
        sensors=Sensor.query.all(),
    )


@bp.route("/workouts", methods=["GET"])
@login_required
def workouts() -> None:
    """Render the workouts page."""
    return render_template(
        "workouts/index.html",
        user=current_user,
        workouts=Workout.query.all(),
    )


@bp.route("/sensors/<int:id>", methods=["GET"])
@login_required
def show_sensor(id: int) -> None:
    """Render the sensors page."""
    return render_template(
        "sensors/show.html",
        user=current_user,
        sensor=Sensor.query.get(id),
    )


@bp.route("/workouts/add", methods=["POST"])
@login_required
def add_workout() -> None:
    """Add a workout."""
    if request.form:
        try:
            workout = Workout(
                name=request.form.get("name"),
                description=request.form.get("description"),
            )
            db.session.add(workout)
            db.session.commit()
        except Exception as e:
            print(f"Failed to add workout: {e}")
    flash("Workout added!", "success")
    return redirect(url_for("backend.workouts"))


@bp.route("/workouts/<int:id>/update", methods=["POST"])
@login_required
def update_workout(id: int) -> None:
    """Update a workout.

    Args:
    ----
        id (int): The id of the workout to update.
    """
    if request.form:
        try:
            workout = Workout.query.get(id)
            workout.name = request.form.get("name")
            workout.description = request.form.get("description")

            db.session.commit()
        except Exception as e:
            print(f"Failed to update workout: {e}")
    flash ("Workout updated!", "success")
    return redirect(url_for("backend.workouts"))


@bp.route("/sensors/delete_all", methods=["POST"])
@login_required
def delete_all_sensors() -> None:
    """Delete all sensors."""
    Sensor.query.delete()
    db.session.commit()
    flash("All sensors deleted.", "success")
    return redirect(url_for("backend.sensors"))


@bp.route("/workouts/<int:id>/delete", methods=["POST"])
def delete_workout(id: int) -> None:
    """Delete a workout.

    Args:
    ----
        id (int): The id of the workout to delete.
    """
    try:
        workout = Workout.query.get(id)
        db.session.delete(workout)
        db.session.commit()
    except Exception as e:
        print(f"Failed to delete workout: {e}")
    flash("Workout deleted!", "success")
    return redirect(url_for("backend.workouts"))


# TODO - Delete single sensor
# TODO - Add single sensor

