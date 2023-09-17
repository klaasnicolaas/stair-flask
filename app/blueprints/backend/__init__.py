"""Blueprint for the backend of the application."""
from flask import Blueprint, render_template

bp = Blueprint("backend", __name__, template_folder="templates")


@bp.route("/", methods=["GET"])
def dashboard() -> None:
    """Render the dashboard page."""
    return render_template("dashboard.html")
