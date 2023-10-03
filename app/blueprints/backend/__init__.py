"""Blueprint for the backend of the application."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.blueprints.auth.models import User

from .models import Sensor, Workout

bp = Blueprint("backend", __name__, template_folder="templates/admin")


@bp.route("/", methods=["GET"])
@login_required
def dashboard() -> None:
    """Render the dashboard page."""
    return render_template(
        "dashboard.html",
        user=current_user,
        sensors=Sensor.query.all(),
        workouts=Workout.query.all(),
    )


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


@bp.route("/sensors/<int:sensor_id>", methods=["GET"])
@login_required
def show_sensor(sensor_id: int) -> None:
    """Render the sensors page.

    Args:
    ----
        sensor_id (int): The id of the sensor to show.
    """
    return render_template(
        "sensors/show.html",
        user=current_user,
        sensor=Sensor.query.get(sensor_id),
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
        except SQLAlchemyError as error:
            print(f"Failed to add workout: {error}")
    flash("Workout added!", "success")
    return redirect(url_for("backend.workouts"))


@bp.route("/workouts/<int:workout_id>/update", methods=["POST"])
@login_required
def update_workout(workout_id: int) -> None:
    """Update a workout.

    Args:
    ----
        workout_id (int): The id of the workout to update.
    """
    if request.form:
        try:
            workout = Workout.query.get(workout_id)
            workout.name = request.form.get("name")
            workout.description = request.form.get("description")

            db.session.commit()
        except SQLAlchemyError as error:
            print(f"Failed to update workout: {error}")
    flash("Oefening is bijgewerkt!", "success")
    return redirect(url_for("backend.workouts"))


@bp.route("/sensors/delete_all", methods=["POST"])
@login_required
def delete_all_sensors() -> None:
    """Delete all sensors."""
    Sensor.query.delete()
    db.session.commit()
    flash("All sensors deleted.", "success")
    return redirect(url_for("backend.sensors"))


@bp.route("/workouts/<int:workout_id>/delete", methods=["POST"])
def delete_workout(workout_id: int) -> None:
    """Delete a workout.

    Args:
    ----
        workout_id (int): The id of the workout to delete.
    """
    try:
        workout = Workout.query.get(workout_id)
        db.session.delete(workout)
        db.session.commit()
    except SQLAlchemyError as error:
        print(f"Failed to delete workout: {error}")
    flash("Workout deleted!", "success")
    return redirect(url_for("backend.workouts"))


@bp.route("/led_control", methods=["GET"])
@login_required
def led_control() -> None:
    """Render the led_control page."""
    return render_template("led_control.html", user=current_user)


@bp.route("/users", methods=["GET"])
@login_required
def users() -> None:
    """Render the users page."""
    if current_user.is_admin:
        return render_template("users.html", user=current_user, users=User.query.all())
    return redirect(url_for("backend.dashboard"))
