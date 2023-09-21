"""Blueprint for the frontend of the application."""
from flask import Blueprint, render_template

bp = Blueprint("frontend", __name__, template_folder="templates")


@bp.route("/", methods=["GET"])
def home() -> None:
    """Render the home page."""
    return render_template("home.html")


@bp.route("/workout", methods=["GET"])
def workout() -> None:
    """Render the workout page."""
    return render_template("workout.html")


@bp.route("/info", methods=["GET"])
def info() -> None:
    """Render the info page."""
    return render_template("info.html")
