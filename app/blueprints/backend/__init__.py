"""Blueprint for the backend of the application."""
from flask import Blueprint, redirect, render_template, url_for, flash
from flask_login import current_user, login_required

from app.blueprints.auth.models import User
from app.blueprints.backend.models import Sensor

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


@bp.route("/sensors/<int:id>", methods=["GET"])
@login_required
def show_sensor(id: int) -> None:
    """Render the sensors page."""
    return render_template(
        "sensors/show.html",
        user=current_user,
        sensor=Sensor.query.get(id),
    )


@bp.route("/sensors/delete_all", methods=["POST"])
@login_required
def delete_all_sensors() -> None:
    """Delete all sensors."""
    Sensor.query.delete()
    db.session.commit()
    flash("All sensors deleted.", "success")
    return redirect(url_for("backend.sensors"))


