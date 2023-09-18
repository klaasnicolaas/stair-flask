"""Blueprint for the backend of the application."""
from flask import Blueprint, render_template
from flask_login import login_required, current_user

bp = Blueprint("backend", __name__, template_folder="templates")


@bp.route("/", methods=["GET"])
@login_required
def dashboard() -> None:
    """Render the dashboard page."""
    return render_template("dashboard.html", user=current_user)
