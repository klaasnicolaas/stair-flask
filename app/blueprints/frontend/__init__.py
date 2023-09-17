"""Blueprint for the frontend of the application."""
from flask import Blueprint, render_template

bp = Blueprint("frontend", __name__, template_folder="templates")


@bp.route("/", methods=["GET"])
def home() -> None:
    """Render the home page."""
    return render_template("home.html")
