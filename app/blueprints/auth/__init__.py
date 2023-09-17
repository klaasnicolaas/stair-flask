"""Blueprint for the authentication pages."""
from flask import Blueprint, render_template

bp = Blueprint("auth", __name__, template_folder="templates")


@bp.route("/login", methods=["GET"])
def login() -> None:
    """Render the login page."""
    return render_template("login.html")
